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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


class CfnConnectorApplicationLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorApplicationLogs",
):
    '''Builder for CfnConnectorLogsMixin to generate APPLICATION_LOGS for CfnConnector.

    :cloudformationResource: AWS::KafkaConnect::Connector
    :logType: APPLICATION_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
        
        cfn_connector_application_logs = kafkaconnect_mixins.CfnConnectorApplicationLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnConnectorLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e4e82d00e8301d3ca95decc4dded0c5975c7f6b31b31f09f521b5b4e2eccd7)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnConnectorLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnConnectorLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea00e308f20b1d345663f6346b2c150fc0ee139d5065cbddd74f907a232d830)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnConnectorLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnConnectorLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96eeff00252c5f772cc28636f230c21e2cf6b7111885f5392d9a6ca8d951f333)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnConnectorLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorLogsMixin",
):
    '''Creates a connector using the specified properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
    :cloudformationResource: AWS::KafkaConnect::Connector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_connector_logs_mixin = kafkaconnect_mixins.CfnConnectorLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::KafkaConnect::Connector``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48ba35271ed994e6d2f5db7f6ed3269b0a022b2895ce2ff8c792cf51e98b9f4)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d27e4c612d1070bd185c899761853ac7c86e82596e57df636eb4ccbf81c47b5)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaa68bdbe447c322f7f47d6ba3c125eadd960f21921a5fd5bda3db78c201b499)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="APPLICATION_LOGS")
    def APPLICATION_LOGS(cls) -> CfnConnectorApplicationLogs:
        return typing.cast(CfnConnectorApplicationLogs, jsii.sget(cls, "APPLICATION_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "connector_configuration": "connectorConfiguration",
        "connector_description": "connectorDescription",
        "connector_name": "connectorName",
        "kafka_cluster": "kafkaCluster",
        "kafka_cluster_client_authentication": "kafkaClusterClientAuthentication",
        "kafka_cluster_encryption_in_transit": "kafkaClusterEncryptionInTransit",
        "kafka_connect_version": "kafkaConnectVersion",
        "log_delivery": "logDelivery",
        "plugins": "plugins",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "tags": "tags",
        "worker_configuration": "workerConfiguration",
    },
)
class CfnConnectorMixinProps:
    def __init__(
        self,
        *,
        capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.CapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connector_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        connector_description: typing.Optional[builtins.str] = None,
        connector_name: typing.Optional[builtins.str] = None,
        kafka_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.KafkaClusterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kafka_cluster_client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kafka_cluster_encryption_in_transit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kafka_connect_version: typing.Optional[builtins.str] = None,
        log_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.LogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        plugins: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.PluginProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        service_execution_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        worker_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.WorkerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConnectorPropsMixin.

        :param capacity: The connector's compute capacity settings.
        :param connector_configuration: The configuration of the connector.
        :param connector_description: The description of the connector.
        :param connector_name: The name of the connector. The connector name must be unique and can include up to 128 characters. Valid characters you can include in a connector name are: a-z, A-Z, 0-9, and -.
        :param kafka_cluster: The details of the Apache Kafka cluster to which the connector is connected.
        :param kafka_cluster_client_authentication: The type of client authentication used to connect to the Apache Kafka cluster. The value is NONE when no client authentication is used.
        :param kafka_cluster_encryption_in_transit: Details of encryption in transit to the Apache Kafka cluster.
        :param kafka_connect_version: The version of Kafka Connect. It has to be compatible with both the Apache Kafka cluster's version and the plugins.
        :param log_delivery: The settings for delivering connector logs to Amazon CloudWatch Logs.
        :param plugins: Specifies which plugin to use for the connector. You must specify a single-element list. Amazon MSK Connect does not currently support specifying multiple plugins.
        :param service_execution_role_arn: The Amazon Resource Name (ARN) of the IAM role used by the connector to access Amazon Web Services resources.
        :param tags: A collection of tags associated with a resource.
        :param worker_configuration: The worker configurations that are in use with the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
            
            cfn_connector_mixin_props = kafkaconnect_mixins.CfnConnectorMixinProps(
                capacity=kafkaconnect_mixins.CfnConnectorPropsMixin.CapacityProperty(
                    auto_scaling=kafkaconnect_mixins.CfnConnectorPropsMixin.AutoScalingProperty(
                        max_worker_count=123,
                        mcu_count=123,
                        min_worker_count=123,
                        scale_in_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleInPolicyProperty(
                            cpu_utilization_percentage=123
                        ),
                        scale_out_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleOutPolicyProperty(
                            cpu_utilization_percentage=123
                        )
                    ),
                    provisioned_capacity=kafkaconnect_mixins.CfnConnectorPropsMixin.ProvisionedCapacityProperty(
                        mcu_count=123,
                        worker_count=123
                    )
                ),
                connector_configuration={
                    "connector_configuration_key": "connectorConfiguration"
                },
                connector_description="connectorDescription",
                connector_name="connectorName",
                kafka_cluster=kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterProperty(
                    apache_kafka_cluster=kafkaconnect_mixins.CfnConnectorPropsMixin.ApacheKafkaClusterProperty(
                        bootstrap_servers="bootstrapServers",
                        vpc=kafkaconnect_mixins.CfnConnectorPropsMixin.VpcProperty(
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    )
                ),
                kafka_cluster_client_authentication=kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty(
                    authentication_type="authenticationType"
                ),
                kafka_cluster_encryption_in_transit=kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty(
                    encryption_type="encryptionType"
                ),
                kafka_connect_version="kafkaConnectVersion",
                log_delivery=kafkaconnect_mixins.CfnConnectorPropsMixin.LogDeliveryProperty(
                    worker_log_delivery=kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerLogDeliveryProperty(
                        cloud_watch_logs=kafkaconnect_mixins.CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty(
                            enabled=False,
                            log_group="logGroup"
                        ),
                        firehose=kafkaconnect_mixins.CfnConnectorPropsMixin.FirehoseLogDeliveryProperty(
                            delivery_stream="deliveryStream",
                            enabled=False
                        ),
                        s3=kafkaconnect_mixins.CfnConnectorPropsMixin.S3LogDeliveryProperty(
                            bucket="bucket",
                            enabled=False,
                            prefix="prefix"
                        )
                    )
                ),
                plugins=[kafkaconnect_mixins.CfnConnectorPropsMixin.PluginProperty(
                    custom_plugin=kafkaconnect_mixins.CfnConnectorPropsMixin.CustomPluginProperty(
                        custom_plugin_arn="customPluginArn",
                        revision=123
                    )
                )],
                service_execution_role_arn="serviceExecutionRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                worker_configuration=kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerConfigurationProperty(
                    revision=123,
                    worker_configuration_arn="workerConfigurationArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8381edde5987e5aa1ac52f249e4c8b7b89084d6f1798a079f1bb30d2c33f4f7)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument connector_configuration", value=connector_configuration, expected_type=type_hints["connector_configuration"])
            check_type(argname="argument connector_description", value=connector_description, expected_type=type_hints["connector_description"])
            check_type(argname="argument connector_name", value=connector_name, expected_type=type_hints["connector_name"])
            check_type(argname="argument kafka_cluster", value=kafka_cluster, expected_type=type_hints["kafka_cluster"])
            check_type(argname="argument kafka_cluster_client_authentication", value=kafka_cluster_client_authentication, expected_type=type_hints["kafka_cluster_client_authentication"])
            check_type(argname="argument kafka_cluster_encryption_in_transit", value=kafka_cluster_encryption_in_transit, expected_type=type_hints["kafka_cluster_encryption_in_transit"])
            check_type(argname="argument kafka_connect_version", value=kafka_connect_version, expected_type=type_hints["kafka_connect_version"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument service_execution_role_arn", value=service_execution_role_arn, expected_type=type_hints["service_execution_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capacity is not None:
            self._values["capacity"] = capacity
        if connector_configuration is not None:
            self._values["connector_configuration"] = connector_configuration
        if connector_description is not None:
            self._values["connector_description"] = connector_description
        if connector_name is not None:
            self._values["connector_name"] = connector_name
        if kafka_cluster is not None:
            self._values["kafka_cluster"] = kafka_cluster
        if kafka_cluster_client_authentication is not None:
            self._values["kafka_cluster_client_authentication"] = kafka_cluster_client_authentication
        if kafka_cluster_encryption_in_transit is not None:
            self._values["kafka_cluster_encryption_in_transit"] = kafka_cluster_encryption_in_transit
        if kafka_connect_version is not None:
            self._values["kafka_connect_version"] = kafka_connect_version
        if log_delivery is not None:
            self._values["log_delivery"] = log_delivery
        if plugins is not None:
            self._values["plugins"] = plugins
        if service_execution_role_arn is not None:
            self._values["service_execution_role_arn"] = service_execution_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if worker_configuration is not None:
            self._values["worker_configuration"] = worker_configuration

    @builtins.property
    def capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.CapacityProperty"]]:
        '''The connector's compute capacity settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-capacity
        '''
        result = self._values.get("capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.CapacityProperty"]], result)

    @builtins.property
    def connector_configuration(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The configuration of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorconfiguration
        '''
        result = self._values.get("connector_configuration")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def connector_description(self) -> typing.Optional[builtins.str]:
        '''The description of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectordescription
        '''
        result = self._values.get("connector_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connector_name(self) -> typing.Optional[builtins.str]:
        '''The name of the connector.

        The connector name must be unique and can include up to 128 characters. Valid characters you can include in a connector name are: a-z, A-Z, 0-9, and -.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-connectorname
        '''
        result = self._values.get("connector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka_cluster(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.KafkaClusterProperty"]]:
        '''The details of the Apache Kafka cluster to which the connector is connected.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkacluster
        '''
        result = self._values.get("kafka_cluster")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.KafkaClusterProperty"]], result)

    @builtins.property
    def kafka_cluster_client_authentication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty"]]:
        '''The type of client authentication used to connect to the Apache Kafka cluster.

        The value is NONE when no client authentication is used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication
        '''
        result = self._values.get("kafka_cluster_client_authentication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty"]], result)

    @builtins.property
    def kafka_cluster_encryption_in_transit(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty"]]:
        '''Details of encryption in transit to the Apache Kafka cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit
        '''
        result = self._values.get("kafka_cluster_encryption_in_transit")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty"]], result)

    @builtins.property
    def kafka_connect_version(self) -> typing.Optional[builtins.str]:
        '''The version of Kafka Connect.

        It has to be compatible with both the Apache Kafka cluster's version and the plugins.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-kafkaconnectversion
        '''
        result = self._values.get("kafka_connect_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_delivery(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.LogDeliveryProperty"]]:
        '''The settings for delivering connector logs to Amazon CloudWatch Logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-logdelivery
        '''
        result = self._values.get("log_delivery")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.LogDeliveryProperty"]], result)

    @builtins.property
    def plugins(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.PluginProperty"]]]]:
        '''Specifies which plugin to use for the connector.

        You must specify a single-element list. Amazon MSK Connect does not currently support specifying multiple plugins.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-plugins
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.PluginProperty"]]]], result)

    @builtins.property
    def service_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role used by the connector to access Amazon Web Services resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-serviceexecutionrolearn
        '''
        result = self._values.get("service_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def worker_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.WorkerConfigurationProperty"]]:
        '''The worker configurations that are in use with the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html#cfn-kafkaconnect-connector-workerconfiguration
        '''
        result = self._values.get("worker_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.WorkerConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin",
):
    '''Creates a connector using the specified properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-connector.html
    :cloudformationResource: AWS::KafkaConnect::Connector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
        
        cfn_connector_props_mixin = kafkaconnect_mixins.CfnConnectorPropsMixin(kafkaconnect_mixins.CfnConnectorMixinProps(
            capacity=kafkaconnect_mixins.CfnConnectorPropsMixin.CapacityProperty(
                auto_scaling=kafkaconnect_mixins.CfnConnectorPropsMixin.AutoScalingProperty(
                    max_worker_count=123,
                    mcu_count=123,
                    min_worker_count=123,
                    scale_in_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleInPolicyProperty(
                        cpu_utilization_percentage=123
                    ),
                    scale_out_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleOutPolicyProperty(
                        cpu_utilization_percentage=123
                    )
                ),
                provisioned_capacity=kafkaconnect_mixins.CfnConnectorPropsMixin.ProvisionedCapacityProperty(
                    mcu_count=123,
                    worker_count=123
                )
            ),
            connector_configuration={
                "connector_configuration_key": "connectorConfiguration"
            },
            connector_description="connectorDescription",
            connector_name="connectorName",
            kafka_cluster=kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterProperty(
                apache_kafka_cluster=kafkaconnect_mixins.CfnConnectorPropsMixin.ApacheKafkaClusterProperty(
                    bootstrap_servers="bootstrapServers",
                    vpc=kafkaconnect_mixins.CfnConnectorPropsMixin.VpcProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            ),
            kafka_cluster_client_authentication=kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty(
                authentication_type="authenticationType"
            ),
            kafka_cluster_encryption_in_transit=kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty(
                encryption_type="encryptionType"
            ),
            kafka_connect_version="kafkaConnectVersion",
            log_delivery=kafkaconnect_mixins.CfnConnectorPropsMixin.LogDeliveryProperty(
                worker_log_delivery=kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerLogDeliveryProperty(
                    cloud_watch_logs=kafkaconnect_mixins.CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty(
                        enabled=False,
                        log_group="logGroup"
                    ),
                    firehose=kafkaconnect_mixins.CfnConnectorPropsMixin.FirehoseLogDeliveryProperty(
                        delivery_stream="deliveryStream",
                        enabled=False
                    ),
                    s3=kafkaconnect_mixins.CfnConnectorPropsMixin.S3LogDeliveryProperty(
                        bucket="bucket",
                        enabled=False,
                        prefix="prefix"
                    )
                )
            ),
            plugins=[kafkaconnect_mixins.CfnConnectorPropsMixin.PluginProperty(
                custom_plugin=kafkaconnect_mixins.CfnConnectorPropsMixin.CustomPluginProperty(
                    custom_plugin_arn="customPluginArn",
                    revision=123
                )
            )],
            service_execution_role_arn="serviceExecutionRoleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            worker_configuration=kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerConfigurationProperty(
                revision=123,
                worker_configuration_arn="workerConfigurationArn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KafkaConnect::Connector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a86b7208a6dcf6fbce5a51b813e6b7049b50f362bce232140ce991a0386ccd5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9aeb527cc02af76b7da8fd2e8f5a70bf6302c7b6c177372b7cbcfc4c1240185)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__255a5f7776aec1063cc2063e5b6551a809209ffa7bf70e718fa85e9c5912ffe3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorMixinProps:
        return typing.cast(CfnConnectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.ApacheKafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"bootstrap_servers": "bootstrapServers", "vpc": "vpc"},
    )
    class ApacheKafkaClusterProperty:
        def __init__(
            self,
            *,
            bootstrap_servers: typing.Optional[builtins.str] = None,
            vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.VpcProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The details of the Apache Kafka cluster to which the connector is connected.

            :param bootstrap_servers: The bootstrap servers of the cluster.
            :param vpc: Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                apache_kafka_cluster_property = kafkaconnect_mixins.CfnConnectorPropsMixin.ApacheKafkaClusterProperty(
                    bootstrap_servers="bootstrapServers",
                    vpc=kafkaconnect_mixins.CfnConnectorPropsMixin.VpcProperty(
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcefba85001c791e954c75201700d71762826a6fbe5643ec7177f52cf67981fc)
                check_type(argname="argument bootstrap_servers", value=bootstrap_servers, expected_type=type_hints["bootstrap_servers"])
                check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bootstrap_servers is not None:
                self._values["bootstrap_servers"] = bootstrap_servers
            if vpc is not None:
                self._values["vpc"] = vpc

        @builtins.property
        def bootstrap_servers(self) -> typing.Optional[builtins.str]:
            '''The bootstrap servers of the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html#cfn-kafkaconnect-connector-apachekafkacluster-bootstrapservers
            '''
            result = self._values.get("bootstrap_servers")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.VpcProperty"]]:
            '''Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-apachekafkacluster.html#cfn-kafkaconnect-connector-apachekafkacluster-vpc
            '''
            result = self._values.get("vpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.VpcProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApacheKafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.AutoScalingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_worker_count": "maxWorkerCount",
            "mcu_count": "mcuCount",
            "min_worker_count": "minWorkerCount",
            "scale_in_policy": "scaleInPolicy",
            "scale_out_policy": "scaleOutPolicy",
        },
    )
    class AutoScalingProperty:
        def __init__(
            self,
            *,
            max_worker_count: typing.Optional[jsii.Number] = None,
            mcu_count: typing.Optional[jsii.Number] = None,
            min_worker_count: typing.Optional[jsii.Number] = None,
            scale_in_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ScaleInPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scale_out_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ScaleOutPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies how the connector scales.

            :param max_worker_count: The maximum number of workers allocated to the connector.
            :param mcu_count: The number of microcontroller units (MCUs) allocated to each connector worker. The valid values are 1,2,4,8.
            :param min_worker_count: The minimum number of workers allocated to the connector.
            :param scale_in_policy: The sacle-in policy for the connector.
            :param scale_out_policy: The sacle-out policy for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                auto_scaling_property = kafkaconnect_mixins.CfnConnectorPropsMixin.AutoScalingProperty(
                    max_worker_count=123,
                    mcu_count=123,
                    min_worker_count=123,
                    scale_in_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleInPolicyProperty(
                        cpu_utilization_percentage=123
                    ),
                    scale_out_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleOutPolicyProperty(
                        cpu_utilization_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6dbf9cf93e14ac19ff0de33a74d7ce3f2603acf8697b599b87d329dd9f757178)
                check_type(argname="argument max_worker_count", value=max_worker_count, expected_type=type_hints["max_worker_count"])
                check_type(argname="argument mcu_count", value=mcu_count, expected_type=type_hints["mcu_count"])
                check_type(argname="argument min_worker_count", value=min_worker_count, expected_type=type_hints["min_worker_count"])
                check_type(argname="argument scale_in_policy", value=scale_in_policy, expected_type=type_hints["scale_in_policy"])
                check_type(argname="argument scale_out_policy", value=scale_out_policy, expected_type=type_hints["scale_out_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_worker_count is not None:
                self._values["max_worker_count"] = max_worker_count
            if mcu_count is not None:
                self._values["mcu_count"] = mcu_count
            if min_worker_count is not None:
                self._values["min_worker_count"] = min_worker_count
            if scale_in_policy is not None:
                self._values["scale_in_policy"] = scale_in_policy
            if scale_out_policy is not None:
                self._values["scale_out_policy"] = scale_out_policy

        @builtins.property
        def max_worker_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of workers allocated to the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-maxworkercount
            '''
            result = self._values.get("max_worker_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mcu_count(self) -> typing.Optional[jsii.Number]:
            '''The number of microcontroller units (MCUs) allocated to each connector worker.

            The valid values are 1,2,4,8.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-mcucount
            '''
            result = self._values.get("mcu_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_worker_count(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of workers allocated to the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-minworkercount
            '''
            result = self._values.get("min_worker_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def scale_in_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ScaleInPolicyProperty"]]:
            '''The sacle-in policy for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-scaleinpolicy
            '''
            result = self._values.get("scale_in_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ScaleInPolicyProperty"]], result)

        @builtins.property
        def scale_out_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ScaleOutPolicyProperty"]]:
            '''The sacle-out policy for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-autoscaling.html#cfn-kafkaconnect-connector-autoscaling-scaleoutpolicy
            '''
            result = self._values.get("scale_out_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ScaleOutPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoScalingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.CapacityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_scaling": "autoScaling",
            "provisioned_capacity": "provisionedCapacity",
        },
    )
    class CapacityProperty:
        def __init__(
            self,
            *,
            auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.AutoScalingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            provisioned_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ProvisionedCapacityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the capacity of the connector, whether it is auto scaled or provisioned.

            :param auto_scaling: Information about the auto scaling parameters for the connector.
            :param provisioned_capacity: Details about a fixed capacity allocated to a connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                capacity_property = kafkaconnect_mixins.CfnConnectorPropsMixin.CapacityProperty(
                    auto_scaling=kafkaconnect_mixins.CfnConnectorPropsMixin.AutoScalingProperty(
                        max_worker_count=123,
                        mcu_count=123,
                        min_worker_count=123,
                        scale_in_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleInPolicyProperty(
                            cpu_utilization_percentage=123
                        ),
                        scale_out_policy=kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleOutPolicyProperty(
                            cpu_utilization_percentage=123
                        )
                    ),
                    provisioned_capacity=kafkaconnect_mixins.CfnConnectorPropsMixin.ProvisionedCapacityProperty(
                        mcu_count=123,
                        worker_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93c72cd41694780bb8eafd5b419eb9d664483cf4b3bc5aa560085df7554af22c)
                check_type(argname="argument auto_scaling", value=auto_scaling, expected_type=type_hints["auto_scaling"])
                check_type(argname="argument provisioned_capacity", value=provisioned_capacity, expected_type=type_hints["provisioned_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_scaling is not None:
                self._values["auto_scaling"] = auto_scaling
            if provisioned_capacity is not None:
                self._values["provisioned_capacity"] = provisioned_capacity

        @builtins.property
        def auto_scaling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.AutoScalingProperty"]]:
            '''Information about the auto scaling parameters for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html#cfn-kafkaconnect-connector-capacity-autoscaling
            '''
            result = self._values.get("auto_scaling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.AutoScalingProperty"]], result)

        @builtins.property
        def provisioned_capacity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ProvisionedCapacityProperty"]]:
            '''Details about a fixed capacity allocated to a connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-capacity.html#cfn-kafkaconnect-connector-capacity-provisionedcapacity
            '''
            result = self._values.get("provisioned_capacity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ProvisionedCapacityProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "log_group": "logGroup"},
    )
    class CloudWatchLogsLogDeliveryProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            log_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for delivering connector logs to Amazon CloudWatch Logs.

            :param enabled: Whether log delivery to Amazon CloudWatch Logs is enabled.
            :param log_group: The name of the CloudWatch log group that is the destination for log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                cloud_watch_logs_log_delivery_property = kafkaconnect_mixins.CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty(
                    enabled=False,
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c5de54d29de729f5555b74be8c3888263f51fffb1d269d1904956dd970bf64f)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if log_group is not None:
                self._values["log_group"] = log_group

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether log delivery to Amazon CloudWatch Logs is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html#cfn-kafkaconnect-connector-cloudwatchlogslogdelivery-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch log group that is the destination for log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-cloudwatchlogslogdelivery.html#cfn-kafkaconnect-connector-cloudwatchlogslogdelivery-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.CustomPluginProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_plugin_arn": "customPluginArn", "revision": "revision"},
    )
    class CustomPluginProperty:
        def __init__(
            self,
            *,
            custom_plugin_arn: typing.Optional[builtins.str] = None,
            revision: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A plugin is an AWS resource that contains the code that defines a connector's logic.

            :param custom_plugin_arn: The Amazon Resource Name (ARN) of the custom plugin.
            :param revision: The revision of the custom plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                custom_plugin_property = kafkaconnect_mixins.CfnConnectorPropsMixin.CustomPluginProperty(
                    custom_plugin_arn="customPluginArn",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2264585e155c919a2a7814dd240a493ff3d9cdf975028d964c95722b8c56edc)
                check_type(argname="argument custom_plugin_arn", value=custom_plugin_arn, expected_type=type_hints["custom_plugin_arn"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_plugin_arn is not None:
                self._values["custom_plugin_arn"] = custom_plugin_arn
            if revision is not None:
                self._values["revision"] = revision

        @builtins.property
        def custom_plugin_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the custom plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html#cfn-kafkaconnect-connector-customplugin-custompluginarn
            '''
            result = self._values.get("custom_plugin_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[jsii.Number]:
            '''The revision of the custom plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-customplugin.html#cfn-kafkaconnect-connector-customplugin-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPluginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.FirehoseLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream": "deliveryStream", "enabled": "enabled"},
    )
    class FirehoseLogDeliveryProperty:
        def __init__(
            self,
            *,
            delivery_stream: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings for delivering logs to Amazon Kinesis Data Firehose.

            :param delivery_stream: The name of the Kinesis Data Firehose delivery stream that is the destination for log delivery.
            :param enabled: Specifies whether connector logs get delivered to Amazon Kinesis Data Firehose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                firehose_log_delivery_property = kafkaconnect_mixins.CfnConnectorPropsMixin.FirehoseLogDeliveryProperty(
                    delivery_stream="deliveryStream",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cceb3ec09f7890cb2c990064800e38cef005d6fd79f424fb484c3c5b2473e438)
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream is not None:
                self._values["delivery_stream"] = delivery_stream
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def delivery_stream(self) -> typing.Optional[builtins.str]:
            '''The name of the Kinesis Data Firehose delivery stream that is the destination for log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html#cfn-kafkaconnect-connector-firehoselogdelivery-deliverystream
            '''
            result = self._values.get("delivery_stream")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether connector logs get delivered to Amazon Kinesis Data Firehose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-firehoselogdelivery.html#cfn-kafkaconnect-connector-firehoselogdelivery-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"authentication_type": "authenticationType"},
    )
    class KafkaClusterClientAuthenticationProperty:
        def __init__(
            self,
            *,
            authentication_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The client authentication information used in order to authenticate with the Apache Kafka cluster.

            :param authentication_type: The type of client authentication used to connect to the Apache Kafka cluster. Value NONE means that no client authentication is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterclientauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                kafka_cluster_client_authentication_property = kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty(
                    authentication_type="authenticationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1494c780c97899fab50cdbec03004cbfe41295a2234888d0ffde61ac51033460)
                check_type(argname="argument authentication_type", value=authentication_type, expected_type=type_hints["authentication_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_type is not None:
                self._values["authentication_type"] = authentication_type

        @builtins.property
        def authentication_type(self) -> typing.Optional[builtins.str]:
            '''The type of client authentication used to connect to the Apache Kafka cluster.

            Value NONE means that no client authentication is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterclientauthentication.html#cfn-kafkaconnect-connector-kafkaclusterclientauthentication-authenticationtype
            '''
            result = self._values.get("authentication_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterClientAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType"},
    )
    class KafkaClusterEncryptionInTransitProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details of encryption in transit to the Apache Kafka cluster.

            :param encryption_type: The type of encryption in transit to the Apache Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterencryptionintransit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                kafka_cluster_encryption_in_transit_property = kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty(
                    encryption_type="encryptionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__992374cdf589d423345a1b0c9132401c5ee98782cc750ef885087c249d4a54dc)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The type of encryption in transit to the Apache Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkaclusterencryptionintransit.html#cfn-kafkaconnect-connector-kafkaclusterencryptionintransit-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterEncryptionInTransitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.KafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"apache_kafka_cluster": "apacheKafkaCluster"},
    )
    class KafkaClusterProperty:
        def __init__(
            self,
            *,
            apache_kafka_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ApacheKafkaClusterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The details of the Apache Kafka cluster to which the connector is connected.

            :param apache_kafka_cluster: The Apache Kafka cluster to which the connector is connected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                kafka_cluster_property = kafkaconnect_mixins.CfnConnectorPropsMixin.KafkaClusterProperty(
                    apache_kafka_cluster=kafkaconnect_mixins.CfnConnectorPropsMixin.ApacheKafkaClusterProperty(
                        bootstrap_servers="bootstrapServers",
                        vpc=kafkaconnect_mixins.CfnConnectorPropsMixin.VpcProperty(
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c0172a12ba12970110b2492ba8be96ba4d14be8dc65f88b41c6f41220f1cfcc4)
                check_type(argname="argument apache_kafka_cluster", value=apache_kafka_cluster, expected_type=type_hints["apache_kafka_cluster"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if apache_kafka_cluster is not None:
                self._values["apache_kafka_cluster"] = apache_kafka_cluster

        @builtins.property
        def apache_kafka_cluster(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ApacheKafkaClusterProperty"]]:
            '''The Apache Kafka cluster to which the connector is connected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-kafkacluster.html#cfn-kafkaconnect-connector-kafkacluster-apachekafkacluster
            '''
            result = self._values.get("apache_kafka_cluster")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ApacheKafkaClusterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.LogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"worker_log_delivery": "workerLogDelivery"},
    )
    class LogDeliveryProperty:
        def __init__(
            self,
            *,
            worker_log_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.WorkerLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details about log delivery.

            :param worker_log_delivery: The workers can send worker logs to different destination types. This configuration specifies the details of these destinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-logdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                log_delivery_property = kafkaconnect_mixins.CfnConnectorPropsMixin.LogDeliveryProperty(
                    worker_log_delivery=kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerLogDeliveryProperty(
                        cloud_watch_logs=kafkaconnect_mixins.CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty(
                            enabled=False,
                            log_group="logGroup"
                        ),
                        firehose=kafkaconnect_mixins.CfnConnectorPropsMixin.FirehoseLogDeliveryProperty(
                            delivery_stream="deliveryStream",
                            enabled=False
                        ),
                        s3=kafkaconnect_mixins.CfnConnectorPropsMixin.S3LogDeliveryProperty(
                            bucket="bucket",
                            enabled=False,
                            prefix="prefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0260c1d917a7e74f42c2ed1967a99335aac80cd4a6502375ee7d21dbb58d3e48)
                check_type(argname="argument worker_log_delivery", value=worker_log_delivery, expected_type=type_hints["worker_log_delivery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if worker_log_delivery is not None:
                self._values["worker_log_delivery"] = worker_log_delivery

        @builtins.property
        def worker_log_delivery(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.WorkerLogDeliveryProperty"]]:
            '''The workers can send worker logs to different destination types.

            This configuration specifies the details of these destinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-logdelivery.html#cfn-kafkaconnect-connector-logdelivery-workerlogdelivery
            '''
            result = self._values.get("worker_log_delivery")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.WorkerLogDeliveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.PluginProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_plugin": "customPlugin"},
    )
    class PluginProperty:
        def __init__(
            self,
            *,
            custom_plugin: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.CustomPluginProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A plugin is an AWS resource that contains the code that defines your connector logic.

            :param custom_plugin: Details about a custom plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-plugin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                plugin_property = kafkaconnect_mixins.CfnConnectorPropsMixin.PluginProperty(
                    custom_plugin=kafkaconnect_mixins.CfnConnectorPropsMixin.CustomPluginProperty(
                        custom_plugin_arn="customPluginArn",
                        revision=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c496b7b757c86fcb007d8f614a8c09a19ac952369951f021c4feb38437a208d)
                check_type(argname="argument custom_plugin", value=custom_plugin, expected_type=type_hints["custom_plugin"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_plugin is not None:
                self._values["custom_plugin"] = custom_plugin

        @builtins.property
        def custom_plugin(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.CustomPluginProperty"]]:
            '''Details about a custom plugin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-plugin.html#cfn-kafkaconnect-connector-plugin-customplugin
            '''
            result = self._values.get("custom_plugin")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.CustomPluginProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PluginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.ProvisionedCapacityProperty",
        jsii_struct_bases=[],
        name_mapping={"mcu_count": "mcuCount", "worker_count": "workerCount"},
    )
    class ProvisionedCapacityProperty:
        def __init__(
            self,
            *,
            mcu_count: typing.Optional[jsii.Number] = None,
            worker_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Details about a connector's provisioned capacity.

            :param mcu_count: The number of microcontroller units (MCUs) allocated to each connector worker. The valid values are 1,2,4,8.
            :param worker_count: The number of workers that are allocated to the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                provisioned_capacity_property = kafkaconnect_mixins.CfnConnectorPropsMixin.ProvisionedCapacityProperty(
                    mcu_count=123,
                    worker_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ba88a78ba6cf13ba7e5ee2fd2fb418e13893ad211627bc199894bb024ca0a11)
                check_type(argname="argument mcu_count", value=mcu_count, expected_type=type_hints["mcu_count"])
                check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mcu_count is not None:
                self._values["mcu_count"] = mcu_count
            if worker_count is not None:
                self._values["worker_count"] = worker_count

        @builtins.property
        def mcu_count(self) -> typing.Optional[jsii.Number]:
            '''The number of microcontroller units (MCUs) allocated to each connector worker.

            The valid values are 1,2,4,8.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html#cfn-kafkaconnect-connector-provisionedcapacity-mcucount
            '''
            result = self._values.get("mcu_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def worker_count(self) -> typing.Optional[jsii.Number]:
            '''The number of workers that are allocated to the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-provisionedcapacity.html#cfn-kafkaconnect-connector-provisionedcapacity-workercount
            '''
            result = self._values.get("worker_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionedCapacityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.S3LogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "enabled": "enabled", "prefix": "prefix"},
    )
    class S3LogDeliveryProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details about delivering logs to Amazon S3.

            :param bucket: The name of the S3 bucket that is the destination for log delivery.
            :param enabled: Specifies whether connector logs get sent to the specified Amazon S3 destination.
            :param prefix: The S3 prefix that is the destination for log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                s3_log_delivery_property = kafkaconnect_mixins.CfnConnectorPropsMixin.S3LogDeliveryProperty(
                    bucket="bucket",
                    enabled=False,
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4dd1ff1fe62b4cb55d5e2c226a92cad1a1ab26fa31b94559b7e33078145c588)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if enabled is not None:
                self._values["enabled"] = enabled
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the S3 bucket that is the destination for log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether connector logs get sent to the specified Amazon S3 destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix that is the destination for log delivery.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-s3logdelivery.html#cfn-kafkaconnect-connector-s3logdelivery-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.ScaleInPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
    )
    class ScaleInPolicyProperty:
        def __init__(
            self,
            *,
            cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The scale-in policy for the connector.

            :param cpu_utilization_percentage: Specifies the CPU utilization percentage threshold at which you want connector scale in to be triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleinpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                scale_in_policy_property = kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleInPolicyProperty(
                    cpu_utilization_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__395cfa2fdcb1c10153692da7a23aa24843ef8d60eeea278a3ecc4b00e61355a8)
                check_type(argname="argument cpu_utilization_percentage", value=cpu_utilization_percentage, expected_type=type_hints["cpu_utilization_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu_utilization_percentage is not None:
                self._values["cpu_utilization_percentage"] = cpu_utilization_percentage

        @builtins.property
        def cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
            '''Specifies the CPU utilization percentage threshold at which you want connector scale in to be triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleinpolicy.html#cfn-kafkaconnect-connector-scaleinpolicy-cpuutilizationpercentage
            '''
            result = self._values.get("cpu_utilization_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScaleInPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.ScaleOutPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu_utilization_percentage": "cpuUtilizationPercentage"},
    )
    class ScaleOutPolicyProperty:
        def __init__(
            self,
            *,
            cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The scale-out policy for the connector.

            :param cpu_utilization_percentage: The CPU utilization percentage threshold at which you want connector scale out to be triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleoutpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                scale_out_policy_property = kafkaconnect_mixins.CfnConnectorPropsMixin.ScaleOutPolicyProperty(
                    cpu_utilization_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b592d61a9f62bd51f18b8cfc8004377b294b37cd65805d90d530b4882904a48)
                check_type(argname="argument cpu_utilization_percentage", value=cpu_utilization_percentage, expected_type=type_hints["cpu_utilization_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu_utilization_percentage is not None:
                self._values["cpu_utilization_percentage"] = cpu_utilization_percentage

        @builtins.property
        def cpu_utilization_percentage(self) -> typing.Optional[jsii.Number]:
            '''The CPU utilization percentage threshold at which you want connector scale out to be triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-scaleoutpolicy.html#cfn-kafkaconnect-connector-scaleoutpolicy-cpuutilizationpercentage
            '''
            result = self._values.get("cpu_utilization_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScaleOutPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.VpcProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnets": "subnets"},
    )
    class VpcProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about the VPC in which the connector resides.

            :param security_groups: The security group IDs for the connector.
            :param subnets: The subnets for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                vpc_property = kafkaconnect_mixins.CfnConnectorPropsMixin.VpcProperty(
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fb1f4925dd8f1644305dfd71361e228c4ad156e3d1458a379f2f13bbf1dea98)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security group IDs for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html#cfn-kafkaconnect-connector-vpc-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The subnets for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-vpc.html#cfn-kafkaconnect-connector-vpc-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.WorkerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "revision": "revision",
            "worker_configuration_arn": "workerConfigurationArn",
        },
    )
    class WorkerConfigurationProperty:
        def __init__(
            self,
            *,
            revision: typing.Optional[jsii.Number] = None,
            worker_configuration_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the workers, which are the processes that run the connector logic.

            :param revision: The revision of the worker configuration.
            :param worker_configuration_arn: The Amazon Resource Name (ARN) of the worker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                worker_configuration_property = kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerConfigurationProperty(
                    revision=123,
                    worker_configuration_arn="workerConfigurationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cc056dd832d5c9a1e9c83af24821522176e83a8730d400412357ce3f55f7dab)
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
                check_type(argname="argument worker_configuration_arn", value=worker_configuration_arn, expected_type=type_hints["worker_configuration_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if revision is not None:
                self._values["revision"] = revision
            if worker_configuration_arn is not None:
                self._values["worker_configuration_arn"] = worker_configuration_arn

        @builtins.property
        def revision(self) -> typing.Optional[jsii.Number]:
            '''The revision of the worker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html#cfn-kafkaconnect-connector-workerconfiguration-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def worker_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the worker configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerconfiguration.html#cfn-kafkaconnect-connector-workerconfiguration-workerconfigurationarn
            '''
            result = self._values.get("worker_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnConnectorPropsMixin.WorkerLogDeliveryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs": "cloudWatchLogs",
            "firehose": "firehose",
            "s3": "s3",
        },
    )
    class WorkerLogDeliveryProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.FirehoseLogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.S3LogDeliveryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Workers can send worker logs to different destination types.

            This configuration specifies the details of these destinations.

            :param cloud_watch_logs: Details about delivering logs to Amazon CloudWatch Logs.
            :param firehose: Details about delivering logs to Amazon Kinesis Data Firehose.
            :param s3: Details about delivering logs to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                worker_log_delivery_property = kafkaconnect_mixins.CfnConnectorPropsMixin.WorkerLogDeliveryProperty(
                    cloud_watch_logs=kafkaconnect_mixins.CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty(
                        enabled=False,
                        log_group="logGroup"
                    ),
                    firehose=kafkaconnect_mixins.CfnConnectorPropsMixin.FirehoseLogDeliveryProperty(
                        delivery_stream="deliveryStream",
                        enabled=False
                    ),
                    s3=kafkaconnect_mixins.CfnConnectorPropsMixin.S3LogDeliveryProperty(
                        bucket="bucket",
                        enabled=False,
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96dce8922dccb5e17010518961df33e37a6416b71b9d1e8d227aa1d2e022f1ef)
                check_type(argname="argument cloud_watch_logs", value=cloud_watch_logs, expected_type=type_hints["cloud_watch_logs"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_watch_logs is not None:
                self._values["cloud_watch_logs"] = cloud_watch_logs
            if firehose is not None:
                self._values["firehose"] = firehose
            if s3 is not None:
                self._values["s3"] = s3

        @builtins.property
        def cloud_watch_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty"]]:
            '''Details about delivering logs to Amazon CloudWatch Logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.FirehoseLogDeliveryProperty"]]:
            '''Details about delivering logs to Amazon Kinesis Data Firehose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.FirehoseLogDeliveryProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.S3LogDeliveryProperty"]]:
            '''Details about delivering logs to Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-connector-workerlogdelivery.html#cfn-kafkaconnect-connector-workerlogdelivery-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.S3LogDeliveryProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerLogDeliveryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnCustomPluginMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_type": "contentType",
        "description": "description",
        "location": "location",
        "name": "name",
        "tags": "tags",
    },
)
class CfnCustomPluginMixinProps:
    def __init__(
        self,
        *,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomPluginPropsMixin.CustomPluginLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCustomPluginPropsMixin.

        :param content_type: The format of the plugin file.
        :param description: The description of the custom plugin.
        :param location: Information about the location of the custom plugin.
        :param name: The name of the custom plugin.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
            
            cfn_custom_plugin_mixin_props = kafkaconnect_mixins.CfnCustomPluginMixinProps(
                content_type="contentType",
                description="description",
                location=kafkaconnect_mixins.CfnCustomPluginPropsMixin.CustomPluginLocationProperty(
                    s3_location=kafkaconnect_mixins.CfnCustomPluginPropsMixin.S3LocationProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey",
                        object_version="objectVersion"
                    )
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87d342aa0b5560da6cafddb267f9bdecc0337b5831dc03213b7eb6d5c704ca97)
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_type is not None:
            self._values["content_type"] = content_type
        if description is not None:
            self._values["description"] = description
        if location is not None:
            self._values["location"] = location
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The format of the plugin file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html#cfn-kafkaconnect-customplugin-contenttype
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the custom plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html#cfn-kafkaconnect-customplugin-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomPluginPropsMixin.CustomPluginLocationProperty"]]:
        '''Information about the location of the custom plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html#cfn-kafkaconnect-customplugin-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomPluginPropsMixin.CustomPluginLocationProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the custom plugin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html#cfn-kafkaconnect-customplugin-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html#cfn-kafkaconnect-customplugin-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomPluginMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomPluginPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnCustomPluginPropsMixin",
):
    '''Creates a custom plugin using the specified properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-customplugin.html
    :cloudformationResource: AWS::KafkaConnect::CustomPlugin
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
        
        cfn_custom_plugin_props_mixin = kafkaconnect_mixins.CfnCustomPluginPropsMixin(kafkaconnect_mixins.CfnCustomPluginMixinProps(
            content_type="contentType",
            description="description",
            location=kafkaconnect_mixins.CfnCustomPluginPropsMixin.CustomPluginLocationProperty(
                s3_location=kafkaconnect_mixins.CfnCustomPluginPropsMixin.S3LocationProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey",
                    object_version="objectVersion"
                )
            ),
            name="name",
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
        props: typing.Union[CfnCustomPluginMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KafkaConnect::CustomPlugin``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1c4b648a40c79ad85eec1d5a1d8601bded20429d6f39cf74dd80ce0bfcc5757)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f5d04da92d0954f2ce6df0cd29120ff4882c85cad0f2b369eb2ad0d0150d837)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7606c8eac97cfd09348cc3d83088cf63eccf64258b6a77768935cdf1288778d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomPluginMixinProps:
        return typing.cast(CfnCustomPluginMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnCustomPluginPropsMixin.CustomPluginFileDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={"file_md5": "fileMd5", "file_size": "fileSize"},
    )
    class CustomPluginFileDescriptionProperty:
        def __init__(
            self,
            *,
            file_md5: typing.Optional[builtins.str] = None,
            file_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Details about a custom plugin file.

            :param file_md5: The hex-encoded MD5 checksum of the custom plugin file. You can use it to validate the file.
            :param file_size: The size in bytes of the custom plugin file. You can use it to validate the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-custompluginfiledescription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                custom_plugin_file_description_property = kafkaconnect_mixins.CfnCustomPluginPropsMixin.CustomPluginFileDescriptionProperty(
                    file_md5="fileMd5",
                    file_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fea86d5ac62a82a10ab809dacf07d602057e9f3cbf85ca38ff1120b3e11bb5d)
                check_type(argname="argument file_md5", value=file_md5, expected_type=type_hints["file_md5"])
                check_type(argname="argument file_size", value=file_size, expected_type=type_hints["file_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_md5 is not None:
                self._values["file_md5"] = file_md5
            if file_size is not None:
                self._values["file_size"] = file_size

        @builtins.property
        def file_md5(self) -> typing.Optional[builtins.str]:
            '''The hex-encoded MD5 checksum of the custom plugin file.

            You can use it to validate the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-custompluginfiledescription.html#cfn-kafkaconnect-customplugin-custompluginfiledescription-filemd5
            '''
            result = self._values.get("file_md5")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_size(self) -> typing.Optional[jsii.Number]:
            '''The size in bytes of the custom plugin file.

            You can use it to validate the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-custompluginfiledescription.html#cfn-kafkaconnect-customplugin-custompluginfiledescription-filesize
            '''
            result = self._values.get("file_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPluginFileDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnCustomPluginPropsMixin.CustomPluginLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_location": "s3Location"},
    )
    class CustomPluginLocationProperty:
        def __init__(
            self,
            *,
            s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCustomPluginPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the location of a custom plugin.

            :param s3_location: The S3 bucket Amazon Resource Name (ARN), file key, and object version of the plugin file stored in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-custompluginlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                custom_plugin_location_property = kafkaconnect_mixins.CfnCustomPluginPropsMixin.CustomPluginLocationProperty(
                    s3_location=kafkaconnect_mixins.CfnCustomPluginPropsMixin.S3LocationProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey",
                        object_version="objectVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06b5f3aca1954dd941e19d15a95aac0c72ef0b1115c93fc41d8240264c2b0433)
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def s3_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomPluginPropsMixin.S3LocationProperty"]]:
            '''The S3 bucket Amazon Resource Name (ARN), file key, and object version of the plugin file stored in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-custompluginlocation.html#cfn-kafkaconnect-customplugin-custompluginlocation-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCustomPluginPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomPluginLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnCustomPluginPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "file_key": "fileKey",
            "object_version": "objectVersion",
        },
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            file_key: typing.Optional[builtins.str] = None,
            object_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location of an object in Amazon S3.

            :param bucket_arn: The Amazon Resource Name (ARN) of an S3 bucket.
            :param file_key: The file key for an object in an S3 bucket.
            :param object_version: The version of an object in an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
                
                s3_location_property = kafkaconnect_mixins.CfnCustomPluginPropsMixin.S3LocationProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey",
                    object_version="objectVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__889c7ba3833006da0ed3c37a285fd891d945bdeff86b30dc08406b0586da86c3)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                check_type(argname="argument object_version", value=object_version, expected_type=type_hints["object_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if file_key is not None:
                self._values["file_key"] = file_key
            if object_version is not None:
                self._values["object_version"] = object_version

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-s3location.html#cfn-kafkaconnect-customplugin-s3location-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_key(self) -> typing.Optional[builtins.str]:
            '''The file key for an object in an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-s3location.html#cfn-kafkaconnect-customplugin-s3location-filekey
            '''
            result = self._values.get("file_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_version(self) -> typing.Optional[builtins.str]:
            '''The version of an object in an S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kafkaconnect-customplugin-s3location.html#cfn-kafkaconnect-customplugin-s3location-objectversion
            '''
            result = self._values.get("object_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnWorkerConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "properties_file_content": "propertiesFileContent",
        "tags": "tags",
    },
)
class CfnWorkerConfigurationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        properties_file_content: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkerConfigurationPropsMixin.

        :param description: The description of a worker configuration.
        :param name: The name of the worker configuration.
        :param properties_file_content: Base64 encoded contents of the connect-distributed.properties file.
        :param tags: A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-workerconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
            
            cfn_worker_configuration_mixin_props = kafkaconnect_mixins.CfnWorkerConfigurationMixinProps(
                description="description",
                name="name",
                properties_file_content="propertiesFileContent",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa905eb7b650de9f21055443638729330a46ada34befa14b32f0513b687ec33d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument properties_file_content", value=properties_file_content, expected_type=type_hints["properties_file_content"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if properties_file_content is not None:
            self._values["properties_file_content"] = properties_file_content
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of a worker configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-workerconfiguration.html#cfn-kafkaconnect-workerconfiguration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the worker configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-workerconfiguration.html#cfn-kafkaconnect-workerconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties_file_content(self) -> typing.Optional[builtins.str]:
        '''Base64 encoded contents of the connect-distributed.properties file.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-workerconfiguration.html#cfn-kafkaconnect-workerconfiguration-propertiesfilecontent
        '''
        result = self._values.get("properties_file_content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A collection of tags associated with a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-workerconfiguration.html#cfn-kafkaconnect-workerconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkerConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkerConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kafkaconnect.mixins.CfnWorkerConfigurationPropsMixin",
):
    '''Creates a worker configuration using the specified properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kafkaconnect-workerconfiguration.html
    :cloudformationResource: AWS::KafkaConnect::WorkerConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kafkaconnect import mixins as kafkaconnect_mixins
        
        cfn_worker_configuration_props_mixin = kafkaconnect_mixins.CfnWorkerConfigurationPropsMixin(kafkaconnect_mixins.CfnWorkerConfigurationMixinProps(
            description="description",
            name="name",
            properties_file_content="propertiesFileContent",
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
        props: typing.Union[CfnWorkerConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KafkaConnect::WorkerConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ca1ab40ac6628a0bac62d50b8d7bbabbfcf6fc40657b64ae585241ffdd6a7ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dd03fb81c0e32251b6cf1339bde6a65c857fea56bd438131fb7c46448c8c0c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feedca252863e43999f73b6c8b566f55f887511025fc709c7035dfe0035d4c60)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkerConfigurationMixinProps:
        return typing.cast(CfnWorkerConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnConnectorApplicationLogs",
    "CfnConnectorLogsMixin",
    "CfnConnectorMixinProps",
    "CfnConnectorPropsMixin",
    "CfnCustomPluginMixinProps",
    "CfnCustomPluginPropsMixin",
    "CfnWorkerConfigurationMixinProps",
    "CfnWorkerConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__a5e4e82d00e8301d3ca95decc4dded0c5975c7f6b31b31f09f521b5b4e2eccd7(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea00e308f20b1d345663f6346b2c150fc0ee139d5065cbddd74f907a232d830(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96eeff00252c5f772cc28636f230c21e2cf6b7111885f5392d9a6ca8d951f333(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48ba35271ed994e6d2f5db7f6ed3269b0a022b2895ce2ff8c792cf51e98b9f4(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d27e4c612d1070bd185c899761853ac7c86e82596e57df636eb4ccbf81c47b5(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa68bdbe447c322f7f47d6ba3c125eadd960f21921a5fd5bda3db78c201b499(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8381edde5987e5aa1ac52f249e4c8b7b89084d6f1798a079f1bb30d2c33f4f7(
    *,
    capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.CapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connector_configuration: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    connector_description: typing.Optional[builtins.str] = None,
    connector_name: typing.Optional[builtins.str] = None,
    kafka_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.KafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kafka_cluster_client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.KafkaClusterClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kafka_cluster_encryption_in_transit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.KafkaClusterEncryptionInTransitProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kafka_connect_version: typing.Optional[builtins.str] = None,
    log_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.LogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    plugins: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.PluginProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    service_execution_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    worker_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.WorkerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a86b7208a6dcf6fbce5a51b813e6b7049b50f362bce232140ce991a0386ccd5(
    props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9aeb527cc02af76b7da8fd2e8f5a70bf6302c7b6c177372b7cbcfc4c1240185(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__255a5f7776aec1063cc2063e5b6551a809209ffa7bf70e718fa85e9c5912ffe3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcefba85001c791e954c75201700d71762826a6fbe5643ec7177f52cf67981fc(
    *,
    bootstrap_servers: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.VpcProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbf9cf93e14ac19ff0de33a74d7ce3f2603acf8697b599b87d329dd9f757178(
    *,
    max_worker_count: typing.Optional[jsii.Number] = None,
    mcu_count: typing.Optional[jsii.Number] = None,
    min_worker_count: typing.Optional[jsii.Number] = None,
    scale_in_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ScaleInPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scale_out_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ScaleOutPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c72cd41694780bb8eafd5b419eb9d664483cf4b3bc5aa560085df7554af22c(
    *,
    auto_scaling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.AutoScalingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    provisioned_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ProvisionedCapacityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c5de54d29de729f5555b74be8c3888263f51fffb1d269d1904956dd970bf64f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2264585e155c919a2a7814dd240a493ff3d9cdf975028d964c95722b8c56edc(
    *,
    custom_plugin_arn: typing.Optional[builtins.str] = None,
    revision: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cceb3ec09f7890cb2c990064800e38cef005d6fd79f424fb484c3c5b2473e438(
    *,
    delivery_stream: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1494c780c97899fab50cdbec03004cbfe41295a2234888d0ffde61ac51033460(
    *,
    authentication_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__992374cdf589d423345a1b0c9132401c5ee98782cc750ef885087c249d4a54dc(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0172a12ba12970110b2492ba8be96ba4d14be8dc65f88b41c6f41220f1cfcc4(
    *,
    apache_kafka_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ApacheKafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0260c1d917a7e74f42c2ed1967a99335aac80cd4a6502375ee7d21dbb58d3e48(
    *,
    worker_log_delivery: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.WorkerLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c496b7b757c86fcb007d8f614a8c09a19ac952369951f021c4feb38437a208d(
    *,
    custom_plugin: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.CustomPluginProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ba88a78ba6cf13ba7e5ee2fd2fb418e13893ad211627bc199894bb024ca0a11(
    *,
    mcu_count: typing.Optional[jsii.Number] = None,
    worker_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4dd1ff1fe62b4cb55d5e2c226a92cad1a1ab26fa31b94559b7e33078145c588(
    *,
    bucket: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__395cfa2fdcb1c10153692da7a23aa24843ef8d60eeea278a3ecc4b00e61355a8(
    *,
    cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b592d61a9f62bd51f18b8cfc8004377b294b37cd65805d90d530b4882904a48(
    *,
    cpu_utilization_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb1f4925dd8f1644305dfd71361e228c4ad156e3d1458a379f2f13bbf1dea98(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc056dd832d5c9a1e9c83af24821522176e83a8730d400412357ce3f55f7dab(
    *,
    revision: typing.Optional[jsii.Number] = None,
    worker_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dce8922dccb5e17010518961df33e37a6416b71b9d1e8d227aa1d2e022f1ef(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.CloudWatchLogsLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.FirehoseLogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.S3LogDeliveryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d342aa0b5560da6cafddb267f9bdecc0337b5831dc03213b7eb6d5c704ca97(
    *,
    content_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomPluginPropsMixin.CustomPluginLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1c4b648a40c79ad85eec1d5a1d8601bded20429d6f39cf74dd80ce0bfcc5757(
    props: typing.Union[CfnCustomPluginMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5d04da92d0954f2ce6df0cd29120ff4882c85cad0f2b369eb2ad0d0150d837(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7606c8eac97cfd09348cc3d83088cf63eccf64258b6a77768935cdf1288778d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fea86d5ac62a82a10ab809dacf07d602057e9f3cbf85ca38ff1120b3e11bb5d(
    *,
    file_md5: typing.Optional[builtins.str] = None,
    file_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b5f3aca1954dd941e19d15a95aac0c72ef0b1115c93fc41d8240264c2b0433(
    *,
    s3_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCustomPluginPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889c7ba3833006da0ed3c37a285fd891d945bdeff86b30dc08406b0586da86c3(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    file_key: typing.Optional[builtins.str] = None,
    object_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa905eb7b650de9f21055443638729330a46ada34befa14b32f0513b687ec33d(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    properties_file_content: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ca1ab40ac6628a0bac62d50b8d7bbabbfcf6fc40657b64ae585241ffdd6a7ec(
    props: typing.Union[CfnWorkerConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd03fb81c0e32251b6cf1339bde6a65c857fea56bd438131fb7c46448c8c0c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feedca252863e43999f73b6c8b566f55f887511025fc709c7035dfe0035d4c60(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
