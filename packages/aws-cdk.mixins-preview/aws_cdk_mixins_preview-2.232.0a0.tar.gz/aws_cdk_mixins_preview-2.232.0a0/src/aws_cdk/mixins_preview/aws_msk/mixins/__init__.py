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


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnBatchScramSecretMixinProps",
    jsii_struct_bases=[],
    name_mapping={"cluster_arn": "clusterArn", "secret_arn_list": "secretArnList"},
)
class CfnBatchScramSecretMixinProps:
    def __init__(
        self,
        *,
        cluster_arn: typing.Optional[builtins.str] = None,
        secret_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnBatchScramSecretPropsMixin.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param secret_arn_list: List of Amazon Resource Name (ARN)s of Secrets Manager secrets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-batchscramsecret.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            cfn_batch_scram_secret_mixin_props = msk_mixins.CfnBatchScramSecretMixinProps(
                cluster_arn="clusterArn",
                secret_arn_list=["secretArnList"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b9c1c4094867258cb92c7fe7d7db58ead70886e6c077d2b3ddf1b0f34d282f1)
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
            check_type(argname="argument secret_arn_list", value=secret_arn_list, expected_type=type_hints["secret_arn_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_arn is not None:
            self._values["cluster_arn"] = cluster_arn
        if secret_arn_list is not None:
            self._values["secret_arn_list"] = secret_arn_list

    @builtins.property
    def cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that uniquely identifies the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-batchscramsecret.html#cfn-msk-batchscramsecret-clusterarn
        '''
        result = self._values.get("cluster_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_arn_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of Amazon Resource Name (ARN)s of Secrets Manager secrets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-batchscramsecret.html#cfn-msk-batchscramsecret-secretarnlist
        '''
        result = self._values.get("secret_arn_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBatchScramSecretMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBatchScramSecretPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnBatchScramSecretPropsMixin",
):
    '''Represents a secret stored in the AWS Secrets Manager that can be used to authenticate with a cluster using a user name and a password.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-batchscramsecret.html
    :cloudformationResource: AWS::MSK::BatchScramSecret
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_batch_scram_secret_props_mixin = msk_mixins.CfnBatchScramSecretPropsMixin(msk_mixins.CfnBatchScramSecretMixinProps(
            cluster_arn="clusterArn",
            secret_arn_list=["secretArnList"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnBatchScramSecretMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MSK::BatchScramSecret``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a54e31319ea0222e266e24d3375b7eb04ea6d4ea1814777a27ebe3a0668be6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f482e8c3ab39b7ba79adc87096b3b217deacbbb6a68d50c88817eacbe09ddb7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e964675b913fcbacda566496b97447f923226f0459fd1101a156342f69aabbce)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBatchScramSecretMixinProps:
        return typing.cast(CfnBatchScramSecretMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


class CfnClusterBrokerLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterBrokerLogs",
):
    '''Builder for CfnClusterLogsMixin to generate BROKER_LOGS for CfnCluster.

    :cloudformationResource: AWS::MSK::Cluster
    :logType: BROKER_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_cluster_broker_logs = msk_mixins.CfnClusterBrokerLogs()
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
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0d0196f5e1b6085f13aa7add4b61e98c7263880649d308845844c68ea73a09b)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9e66f8848f874d92a0a11a214079ebdc2afdce8ed8e0faaa82107feea8a470)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed8ead99a56d8e1f5e0445250b71c7b6a3a76358b7df256e3ed9741f095eda6d)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnClusterLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterLogsMixin",
):
    '''Creates a new MSK cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html
    :cloudformationResource: AWS::MSK::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_cluster_logs_mixin = msk_mixins.CfnClusterLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::MSK::Cluster``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e01f7b8be2507fdc2823cf5853912165511bfa960c4b8f6ed93b75a3ff740f72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7831fbc241cdebf05f30b34b379fc2c976a8ec5ab5e5b212b2527dda64918758)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244c28a448fa4ff847baca8b4ced3099fdebf2d6c9e2f65731e2fa4ba306563a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BROKER_LOGS")
    def BROKER_LOGS(cls) -> CfnClusterBrokerLogs:
        return typing.cast(CfnClusterBrokerLogs, jsii.sget(cls, "BROKER_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "broker_node_group_info": "brokerNodeGroupInfo",
        "client_authentication": "clientAuthentication",
        "cluster_name": "clusterName",
        "configuration_info": "configurationInfo",
        "current_version": "currentVersion",
        "encryption_info": "encryptionInfo",
        "enhanced_monitoring": "enhancedMonitoring",
        "kafka_version": "kafkaVersion",
        "logging_info": "loggingInfo",
        "number_of_broker_nodes": "numberOfBrokerNodes",
        "open_monitoring": "openMonitoring",
        "rebalancing": "rebalancing",
        "storage_mode": "storageMode",
        "tags": "tags",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        broker_node_group_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.BrokerNodeGroupInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ClientAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        configuration_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ConfigurationInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        current_version: typing.Optional[builtins.str] = None,
        encryption_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EncryptionInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        enhanced_monitoring: typing.Optional[builtins.str] = None,
        kafka_version: typing.Optional[builtins.str] = None,
        logging_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.LoggingInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        number_of_broker_nodes: typing.Optional[jsii.Number] = None,
        open_monitoring: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.OpenMonitoringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        rebalancing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.RebalancingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param broker_node_group_info: Information about the broker nodes in the cluster.
        :param client_authentication: Includes all client authentication related information.
        :param cluster_name: The name of the cluster.
        :param configuration_info: Represents the configuration that you want MSK to use for the cluster.
        :param current_version: 
        :param encryption_info: Includes all encryption-related information.
        :param enhanced_monitoring: Specifies the level of monitoring for the MSK cluster.
        :param kafka_version: The version of Apache Kafka. You can use Amazon MSK to create clusters that use `supported Apache Kafka versions <https://docs.aws.amazon.com/msk/latest/developerguide/supported-kafka-versions.html>`_ .
        :param logging_info: Logging info details for the cluster.
        :param number_of_broker_nodes: The number of broker nodes in the cluster.
        :param open_monitoring: The settings for open monitoring.
        :param rebalancing: 
        :param storage_mode: This controls storage mode for supported storage tiers.
        :param tags: An arbitrary set of tags (key-value pairs) for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            cfn_cluster_mixin_props = msk_mixins.CfnClusterMixinProps(
                broker_node_group_info=msk_mixins.CfnClusterPropsMixin.BrokerNodeGroupInfoProperty(
                    broker_az_distribution="brokerAzDistribution",
                    client_subnets=["clientSubnets"],
                    connectivity_info=msk_mixins.CfnClusterPropsMixin.ConnectivityInfoProperty(
                        public_access=msk_mixins.CfnClusterPropsMixin.PublicAccessProperty(
                            type="type"
                        ),
                        vpc_connectivity=msk_mixins.CfnClusterPropsMixin.VpcConnectivityProperty(
                            client_authentication=msk_mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty(
                                sasl=msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                                    iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                                        enabled=False
                                    ),
                                    scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                                        enabled=False
                                    )
                                ),
                                tls=msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                                    enabled=False
                                )
                            )
                        )
                    ),
                    instance_type="instanceType",
                    security_groups=["securityGroups"],
                    storage_info=msk_mixins.CfnClusterPropsMixin.StorageInfoProperty(
                        ebs_storage_info=msk_mixins.CfnClusterPropsMixin.EBSStorageInfoProperty(
                            provisioned_throughput=msk_mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty(
                                enabled=False,
                                volume_throughput=123
                            ),
                            volume_size=123
                        )
                    )
                ),
                client_authentication=msk_mixins.CfnClusterPropsMixin.ClientAuthenticationProperty(
                    sasl=msk_mixins.CfnClusterPropsMixin.SaslProperty(
                        iam=msk_mixins.CfnClusterPropsMixin.IamProperty(
                            enabled=False
                        ),
                        scram=msk_mixins.CfnClusterPropsMixin.ScramProperty(
                            enabled=False
                        )
                    ),
                    tls=msk_mixins.CfnClusterPropsMixin.TlsProperty(
                        certificate_authority_arn_list=["certificateAuthorityArnList"],
                        enabled=False
                    ),
                    unauthenticated=msk_mixins.CfnClusterPropsMixin.UnauthenticatedProperty(
                        enabled=False
                    )
                ),
                cluster_name="clusterName",
                configuration_info=msk_mixins.CfnClusterPropsMixin.ConfigurationInfoProperty(
                    arn="arn",
                    revision=123
                ),
                current_version="currentVersion",
                encryption_info=msk_mixins.CfnClusterPropsMixin.EncryptionInfoProperty(
                    encryption_at_rest=msk_mixins.CfnClusterPropsMixin.EncryptionAtRestProperty(
                        data_volume_kms_key_id="dataVolumeKmsKeyId"
                    ),
                    encryption_in_transit=msk_mixins.CfnClusterPropsMixin.EncryptionInTransitProperty(
                        client_broker="clientBroker",
                        in_cluster=False
                    )
                ),
                enhanced_monitoring="enhancedMonitoring",
                kafka_version="kafkaVersion",
                logging_info=msk_mixins.CfnClusterPropsMixin.LoggingInfoProperty(
                    broker_logs=msk_mixins.CfnClusterPropsMixin.BrokerLogsProperty(
                        cloud_watch_logs=msk_mixins.CfnClusterPropsMixin.CloudWatchLogsProperty(
                            enabled=False,
                            log_group="logGroup"
                        ),
                        firehose=msk_mixins.CfnClusterPropsMixin.FirehoseProperty(
                            delivery_stream="deliveryStream",
                            enabled=False
                        ),
                        s3=msk_mixins.CfnClusterPropsMixin.S3Property(
                            bucket="bucket",
                            enabled=False,
                            prefix="prefix"
                        )
                    )
                ),
                number_of_broker_nodes=123,
                open_monitoring=msk_mixins.CfnClusterPropsMixin.OpenMonitoringProperty(
                    prometheus=msk_mixins.CfnClusterPropsMixin.PrometheusProperty(
                        jmx_exporter=msk_mixins.CfnClusterPropsMixin.JmxExporterProperty(
                            enabled_in_broker=False
                        ),
                        node_exporter=msk_mixins.CfnClusterPropsMixin.NodeExporterProperty(
                            enabled_in_broker=False
                        )
                    )
                ),
                rebalancing=msk_mixins.CfnClusterPropsMixin.RebalancingProperty(
                    status="status"
                ),
                storage_mode="storageMode",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a18d8070d499ae07dd95e173de27914339d7e4678479a62025e5fd9e611e0ec)
            check_type(argname="argument broker_node_group_info", value=broker_node_group_info, expected_type=type_hints["broker_node_group_info"])
            check_type(argname="argument client_authentication", value=client_authentication, expected_type=type_hints["client_authentication"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument configuration_info", value=configuration_info, expected_type=type_hints["configuration_info"])
            check_type(argname="argument current_version", value=current_version, expected_type=type_hints["current_version"])
            check_type(argname="argument encryption_info", value=encryption_info, expected_type=type_hints["encryption_info"])
            check_type(argname="argument enhanced_monitoring", value=enhanced_monitoring, expected_type=type_hints["enhanced_monitoring"])
            check_type(argname="argument kafka_version", value=kafka_version, expected_type=type_hints["kafka_version"])
            check_type(argname="argument logging_info", value=logging_info, expected_type=type_hints["logging_info"])
            check_type(argname="argument number_of_broker_nodes", value=number_of_broker_nodes, expected_type=type_hints["number_of_broker_nodes"])
            check_type(argname="argument open_monitoring", value=open_monitoring, expected_type=type_hints["open_monitoring"])
            check_type(argname="argument rebalancing", value=rebalancing, expected_type=type_hints["rebalancing"])
            check_type(argname="argument storage_mode", value=storage_mode, expected_type=type_hints["storage_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if broker_node_group_info is not None:
            self._values["broker_node_group_info"] = broker_node_group_info
        if client_authentication is not None:
            self._values["client_authentication"] = client_authentication
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if configuration_info is not None:
            self._values["configuration_info"] = configuration_info
        if current_version is not None:
            self._values["current_version"] = current_version
        if encryption_info is not None:
            self._values["encryption_info"] = encryption_info
        if enhanced_monitoring is not None:
            self._values["enhanced_monitoring"] = enhanced_monitoring
        if kafka_version is not None:
            self._values["kafka_version"] = kafka_version
        if logging_info is not None:
            self._values["logging_info"] = logging_info
        if number_of_broker_nodes is not None:
            self._values["number_of_broker_nodes"] = number_of_broker_nodes
        if open_monitoring is not None:
            self._values["open_monitoring"] = open_monitoring
        if rebalancing is not None:
            self._values["rebalancing"] = rebalancing
        if storage_mode is not None:
            self._values["storage_mode"] = storage_mode
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def broker_node_group_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BrokerNodeGroupInfoProperty"]]:
        '''Information about the broker nodes in the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-brokernodegroupinfo
        '''
        result = self._values.get("broker_node_group_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BrokerNodeGroupInfoProperty"]], result)

    @builtins.property
    def client_authentication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ClientAuthenticationProperty"]]:
        '''Includes all client authentication related information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-clientauthentication
        '''
        result = self._values.get("client_authentication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ClientAuthenticationProperty"]], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationInfoProperty"]]:
        '''Represents the configuration that you want MSK to use for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-configurationinfo
        '''
        result = self._values.get("configuration_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConfigurationInfoProperty"]], result)

    @builtins.property
    def current_version(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-currentversion
        '''
        result = self._values.get("current_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionInfoProperty"]]:
        '''Includes all encryption-related information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-encryptioninfo
        '''
        result = self._values.get("encryption_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionInfoProperty"]], result)

    @builtins.property
    def enhanced_monitoring(self) -> typing.Optional[builtins.str]:
        '''Specifies the level of monitoring for the MSK cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-enhancedmonitoring
        '''
        result = self._values.get("enhanced_monitoring")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka_version(self) -> typing.Optional[builtins.str]:
        '''The version of Apache Kafka.

        You can use Amazon MSK to create clusters that use `supported Apache Kafka versions <https://docs.aws.amazon.com/msk/latest/developerguide/supported-kafka-versions.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-kafkaversion
        '''
        result = self._values.get("kafka_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingInfoProperty"]]:
        '''Logging info details for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-logginginfo
        '''
        result = self._values.get("logging_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingInfoProperty"]], result)

    @builtins.property
    def number_of_broker_nodes(self) -> typing.Optional[jsii.Number]:
        '''The number of broker nodes in the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-numberofbrokernodes
        '''
        result = self._values.get("number_of_broker_nodes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def open_monitoring(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OpenMonitoringProperty"]]:
        '''The settings for open monitoring.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-openmonitoring
        '''
        result = self._values.get("open_monitoring")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OpenMonitoringProperty"]], result)

    @builtins.property
    def rebalancing(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RebalancingProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-rebalancing
        '''
        result = self._values.get("rebalancing")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RebalancingProperty"]], result)

    @builtins.property
    def storage_mode(self) -> typing.Optional[builtins.str]:
        '''This controls storage mode for supported storage tiers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-storagemode
        '''
        result = self._values.get("storage_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An arbitrary set of tags (key-value pairs) for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html#cfn-msk-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"cluster_arn": "clusterArn", "policy": "policy"},
)
class CfnClusterPolicyMixinProps:
    def __init__(
        self,
        *,
        cluster_arn: typing.Optional[builtins.str] = None,
        policy: typing.Any = None,
    ) -> None:
        '''Properties for CfnClusterPolicyPropsMixin.

        :param cluster_arn: The Amazon Resource Name (ARN) that uniquely identifies the cluster.
        :param policy: Resource policy for the cluster. The maximum size supported for a resource-based policy document is 20 KB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-clusterpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            # policy: Any
            
            cfn_cluster_policy_mixin_props = msk_mixins.CfnClusterPolicyMixinProps(
                cluster_arn="clusterArn",
                policy=policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcb10a9c280132894606670c091f342edc58469b31bbcae5bdebf1ec70ee2a6)
            check_type(argname="argument cluster_arn", value=cluster_arn, expected_type=type_hints["cluster_arn"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_arn is not None:
            self._values["cluster_arn"] = cluster_arn
        if policy is not None:
            self._values["policy"] = policy

    @builtins.property
    def cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that uniquely identifies the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-clusterpolicy.html#cfn-msk-clusterpolicy-clusterarn
        '''
        result = self._values.get("cluster_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Any:
        '''Resource policy for the cluster.

        The maximum size supported for a resource-based policy document is 20 KB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-clusterpolicy.html#cfn-msk-clusterpolicy-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPolicyPropsMixin",
):
    '''Create or update cluster policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-clusterpolicy.html
    :cloudformationResource: AWS::MSK::ClusterPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        # policy: Any
        
        cfn_cluster_policy_props_mixin = msk_mixins.CfnClusterPolicyPropsMixin(msk_mixins.CfnClusterPolicyMixinProps(
            cluster_arn="clusterArn",
            policy=policy
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnClusterPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MSK::ClusterPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11388492a4ed143d083b6034f2ded1270f608a8b5dc2655127fc0d9c6da80a89)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f65c450fc5a1592068372da35e39a6aed8b6296448bc74db187b4a4de951e532)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f138bb95daab7e5d62b4314bd496b2cd694aea69b92074b3578fea400c767833)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterPolicyMixinProps:
        return typing.cast(CfnClusterPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin",
):
    '''Creates a new MSK cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-cluster.html
    :cloudformationResource: AWS::MSK::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_cluster_props_mixin = msk_mixins.CfnClusterPropsMixin(msk_mixins.CfnClusterMixinProps(
            broker_node_group_info=msk_mixins.CfnClusterPropsMixin.BrokerNodeGroupInfoProperty(
                broker_az_distribution="brokerAzDistribution",
                client_subnets=["clientSubnets"],
                connectivity_info=msk_mixins.CfnClusterPropsMixin.ConnectivityInfoProperty(
                    public_access=msk_mixins.CfnClusterPropsMixin.PublicAccessProperty(
                        type="type"
                    ),
                    vpc_connectivity=msk_mixins.CfnClusterPropsMixin.VpcConnectivityProperty(
                        client_authentication=msk_mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty(
                            sasl=msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                                iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                                    enabled=False
                                ),
                                scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                                    enabled=False
                                )
                            ),
                            tls=msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                                enabled=False
                            )
                        )
                    )
                ),
                instance_type="instanceType",
                security_groups=["securityGroups"],
                storage_info=msk_mixins.CfnClusterPropsMixin.StorageInfoProperty(
                    ebs_storage_info=msk_mixins.CfnClusterPropsMixin.EBSStorageInfoProperty(
                        provisioned_throughput=msk_mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty(
                            enabled=False,
                            volume_throughput=123
                        ),
                        volume_size=123
                    )
                )
            ),
            client_authentication=msk_mixins.CfnClusterPropsMixin.ClientAuthenticationProperty(
                sasl=msk_mixins.CfnClusterPropsMixin.SaslProperty(
                    iam=msk_mixins.CfnClusterPropsMixin.IamProperty(
                        enabled=False
                    ),
                    scram=msk_mixins.CfnClusterPropsMixin.ScramProperty(
                        enabled=False
                    )
                ),
                tls=msk_mixins.CfnClusterPropsMixin.TlsProperty(
                    certificate_authority_arn_list=["certificateAuthorityArnList"],
                    enabled=False
                ),
                unauthenticated=msk_mixins.CfnClusterPropsMixin.UnauthenticatedProperty(
                    enabled=False
                )
            ),
            cluster_name="clusterName",
            configuration_info=msk_mixins.CfnClusterPropsMixin.ConfigurationInfoProperty(
                arn="arn",
                revision=123
            ),
            current_version="currentVersion",
            encryption_info=msk_mixins.CfnClusterPropsMixin.EncryptionInfoProperty(
                encryption_at_rest=msk_mixins.CfnClusterPropsMixin.EncryptionAtRestProperty(
                    data_volume_kms_key_id="dataVolumeKmsKeyId"
                ),
                encryption_in_transit=msk_mixins.CfnClusterPropsMixin.EncryptionInTransitProperty(
                    client_broker="clientBroker",
                    in_cluster=False
                )
            ),
            enhanced_monitoring="enhancedMonitoring",
            kafka_version="kafkaVersion",
            logging_info=msk_mixins.CfnClusterPropsMixin.LoggingInfoProperty(
                broker_logs=msk_mixins.CfnClusterPropsMixin.BrokerLogsProperty(
                    cloud_watch_logs=msk_mixins.CfnClusterPropsMixin.CloudWatchLogsProperty(
                        enabled=False,
                        log_group="logGroup"
                    ),
                    firehose=msk_mixins.CfnClusterPropsMixin.FirehoseProperty(
                        delivery_stream="deliveryStream",
                        enabled=False
                    ),
                    s3=msk_mixins.CfnClusterPropsMixin.S3Property(
                        bucket="bucket",
                        enabled=False,
                        prefix="prefix"
                    )
                )
            ),
            number_of_broker_nodes=123,
            open_monitoring=msk_mixins.CfnClusterPropsMixin.OpenMonitoringProperty(
                prometheus=msk_mixins.CfnClusterPropsMixin.PrometheusProperty(
                    jmx_exporter=msk_mixins.CfnClusterPropsMixin.JmxExporterProperty(
                        enabled_in_broker=False
                    ),
                    node_exporter=msk_mixins.CfnClusterPropsMixin.NodeExporterProperty(
                        enabled_in_broker=False
                    )
                )
            ),
            rebalancing=msk_mixins.CfnClusterPropsMixin.RebalancingProperty(
                status="status"
            ),
            storage_mode="storageMode",
            tags={
                "tags_key": "tags"
            }
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
        '''Create a mixin to apply properties to ``AWS::MSK::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89fa5b44b5604772a70709a2678556ef79c1d5034167488e0740e288ab696af8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__042c107c60ed230ed2ac1af2c9a7818bda427817f2420a767b926c0b1717cf89)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0dd809cc395196a795888e8a68d69e9fc9a0d95490b06cacb1981161f1b8ea1)
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
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.BrokerLogsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cloud_watch_logs": "cloudWatchLogs",
            "firehose": "firehose",
            "s3": "s3",
        },
    )
    class BrokerLogsProperty:
        def __init__(
            self,
            *,
            cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.CloudWatchLogsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.FirehoseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.S3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The broker logs configuration for this MSK cluster.

            :param cloud_watch_logs: 
            :param firehose: Details of the Kinesis Data Firehose delivery stream that is the destination for broker logs.
            :param s3: Details of the Amazon S3 destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokerlogs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                broker_logs_property = msk_mixins.CfnClusterPropsMixin.BrokerLogsProperty(
                    cloud_watch_logs=msk_mixins.CfnClusterPropsMixin.CloudWatchLogsProperty(
                        enabled=False,
                        log_group="logGroup"
                    ),
                    firehose=msk_mixins.CfnClusterPropsMixin.FirehoseProperty(
                        delivery_stream="deliveryStream",
                        enabled=False
                    ),
                    s3=msk_mixins.CfnClusterPropsMixin.S3Property(
                        bucket="bucket",
                        enabled=False,
                        prefix="prefix"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99fabf641d0b75c4951659227281826b268461b10911b61433bf4700278d1fc5)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.CloudWatchLogsProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokerlogs.html#cfn-msk-cluster-brokerlogs-cloudwatchlogs
            '''
            result = self._values.get("cloud_watch_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.CloudWatchLogsProperty"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.FirehoseProperty"]]:
            '''Details of the Kinesis Data Firehose delivery stream that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokerlogs.html#cfn-msk-cluster-brokerlogs-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.FirehoseProperty"]], result)

        @builtins.property
        def s3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.S3Property"]]:
            '''Details of the Amazon S3 destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokerlogs.html#cfn-msk-cluster-brokerlogs-s3
            '''
            result = self._values.get("s3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.S3Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BrokerLogsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.BrokerNodeGroupInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "broker_az_distribution": "brokerAzDistribution",
            "client_subnets": "clientSubnets",
            "connectivity_info": "connectivityInfo",
            "instance_type": "instanceType",
            "security_groups": "securityGroups",
            "storage_info": "storageInfo",
        },
    )
    class BrokerNodeGroupInfoProperty:
        def __init__(
            self,
            *,
            broker_az_distribution: typing.Optional[builtins.str] = None,
            client_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
            connectivity_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ConnectivityInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            storage_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.StorageInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the setup to be used for the broker nodes in the cluster.

            :param broker_az_distribution: This parameter is currently not in use.
            :param client_subnets: The list of subnets to connect to in the client virtual private cloud (VPC). Amazon creates elastic network interfaces (ENIs) inside these subnets. Client applications use ENIs to produce and consume data. If you use the US West (N. California) Region, specify exactly two subnets. For other Regions where Amazon MSK is available, you can specify either two or three subnets. The subnets that you specify must be in distinct Availability Zones. When you create a cluster, Amazon MSK distributes the broker nodes evenly across the subnets that you specify. Client subnets can't occupy the Availability Zone with ID ``use1-az3`` .
            :param connectivity_info: Information about the cluster's connectivity setting.
            :param instance_type: The type of Amazon EC2 instances to use for brokers. Depending on the `broker type <https://docs.aws.amazon.com/msk/latest/developerguide/broker-instance-types.html>`_ , Amazon MSK supports the following broker sizes: *Standard broker sizes* - kafka.t3.small .. epigraph:: You can't select the kafka.t3.small instance type when the metadata mode is KRaft. - kafka.m5.large, kafka.m5.xlarge, kafka.m5.2xlarge, kafka.m5.4xlarge, kafka.m5.8xlarge, kafka.m5.12xlarge, kafka.m5.16xlarge, kafka.m5.24xlarge - kafka.m7g.large, kafka.m7g.xlarge, kafka.m7g.2xlarge, kafka.m7g.4xlarge, kafka.m7g.8xlarge, kafka.m7g.12xlarge, kafka.m7g.16xlarge *Express broker sizes* - express.m7g.large, express.m7g.xlarge, express.m7g.2xlarge, express.m7g.4xlarge, express.m7g.8xlarge, express.m7g.12xlarge, express.m7g.16xlarge .. epigraph:: Some broker sizes might not be available in certian AWS Regions. See the updated `Pricing tools <https://docs.aws.amazon.com/msk/pricing/>`_ section on the Amazon MSK pricing page for the latest list of available instances by Region.
            :param security_groups: The security groups to associate with the ENIs in order to specify who can connect to and communicate with the Amazon MSK cluster. If you don't specify a security group, Amazon MSK uses the default security group associated with the VPC. If you specify security groups that were shared with you, you must ensure that you have permissions to them. Specifically, you need the ``ec2:DescribeSecurityGroups`` permission.
            :param storage_info: Contains information about storage volumes attached to Amazon MSK broker nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                broker_node_group_info_property = msk_mixins.CfnClusterPropsMixin.BrokerNodeGroupInfoProperty(
                    broker_az_distribution="brokerAzDistribution",
                    client_subnets=["clientSubnets"],
                    connectivity_info=msk_mixins.CfnClusterPropsMixin.ConnectivityInfoProperty(
                        public_access=msk_mixins.CfnClusterPropsMixin.PublicAccessProperty(
                            type="type"
                        ),
                        vpc_connectivity=msk_mixins.CfnClusterPropsMixin.VpcConnectivityProperty(
                            client_authentication=msk_mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty(
                                sasl=msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                                    iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                                        enabled=False
                                    ),
                                    scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                                        enabled=False
                                    )
                                ),
                                tls=msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                                    enabled=False
                                )
                            )
                        )
                    ),
                    instance_type="instanceType",
                    security_groups=["securityGroups"],
                    storage_info=msk_mixins.CfnClusterPropsMixin.StorageInfoProperty(
                        ebs_storage_info=msk_mixins.CfnClusterPropsMixin.EBSStorageInfoProperty(
                            provisioned_throughput=msk_mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty(
                                enabled=False,
                                volume_throughput=123
                            ),
                            volume_size=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3b395b2931e590500cc9269112a1ee884c5ccf15df7a0040d8907167455486c)
                check_type(argname="argument broker_az_distribution", value=broker_az_distribution, expected_type=type_hints["broker_az_distribution"])
                check_type(argname="argument client_subnets", value=client_subnets, expected_type=type_hints["client_subnets"])
                check_type(argname="argument connectivity_info", value=connectivity_info, expected_type=type_hints["connectivity_info"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument storage_info", value=storage_info, expected_type=type_hints["storage_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if broker_az_distribution is not None:
                self._values["broker_az_distribution"] = broker_az_distribution
            if client_subnets is not None:
                self._values["client_subnets"] = client_subnets
            if connectivity_info is not None:
                self._values["connectivity_info"] = connectivity_info
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if storage_info is not None:
                self._values["storage_info"] = storage_info

        @builtins.property
        def broker_az_distribution(self) -> typing.Optional[builtins.str]:
            '''This parameter is currently not in use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-brokerazdistribution
            '''
            result = self._values.get("broker_az_distribution")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def client_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of subnets to connect to in the client virtual private cloud (VPC).

            Amazon creates elastic network interfaces (ENIs) inside these subnets. Client applications use ENIs to produce and consume data.

            If you use the US West (N. California) Region, specify exactly two subnets. For other Regions where Amazon MSK is available, you can specify either two or three subnets. The subnets that you specify must be in distinct Availability Zones. When you create a cluster, Amazon MSK distributes the broker nodes evenly across the subnets that you specify.

            Client subnets can't occupy the Availability Zone with ID ``use1-az3`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-clientsubnets
            '''
            result = self._values.get("client_subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def connectivity_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConnectivityInfoProperty"]]:
            '''Information about the cluster's connectivity setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-connectivityinfo
            '''
            result = self._values.get("connectivity_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ConnectivityInfoProperty"]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The type of Amazon EC2 instances to use for brokers.

            Depending on the `broker type <https://docs.aws.amazon.com/msk/latest/developerguide/broker-instance-types.html>`_ , Amazon MSK supports the following broker sizes:

            *Standard broker sizes*

            - kafka.t3.small

            .. epigraph::

               You can't select the kafka.t3.small instance type when the metadata mode is KRaft.

            - kafka.m5.large, kafka.m5.xlarge, kafka.m5.2xlarge, kafka.m5.4xlarge, kafka.m5.8xlarge, kafka.m5.12xlarge, kafka.m5.16xlarge, kafka.m5.24xlarge
            - kafka.m7g.large, kafka.m7g.xlarge, kafka.m7g.2xlarge, kafka.m7g.4xlarge, kafka.m7g.8xlarge, kafka.m7g.12xlarge, kafka.m7g.16xlarge

            *Express broker sizes*

            - express.m7g.large, express.m7g.xlarge, express.m7g.2xlarge, express.m7g.4xlarge, express.m7g.8xlarge, express.m7g.12xlarge, express.m7g.16xlarge

            .. epigraph::

               Some broker sizes might not be available in certian AWS Regions. See the updated `Pricing tools <https://docs.aws.amazon.com/msk/pricing/>`_ section on the Amazon MSK pricing page for the latest list of available instances by Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security groups to associate with the ENIs in order to specify who can connect to and communicate with the Amazon MSK cluster.

            If you don't specify a security group, Amazon MSK uses the default security group associated with the VPC. If you specify security groups that were shared with you, you must ensure that you have permissions to them. Specifically, you need the ``ec2:DescribeSecurityGroups`` permission.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def storage_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.StorageInfoProperty"]]:
            '''Contains information about storage volumes attached to Amazon MSK broker nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-brokernodegroupinfo.html#cfn-msk-cluster-brokernodegroupinfo-storageinfo
            '''
            result = self._values.get("storage_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.StorageInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BrokerNodeGroupInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.ClientAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sasl": "sasl",
            "tls": "tls",
            "unauthenticated": "unauthenticated",
        },
    )
    class ClientAuthenticationProperty:
        def __init__(
            self,
            *,
            sasl: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SaslProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.TlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            unauthenticated: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.UnauthenticatedProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param sasl: Details for client authentication using SASL. To turn on SASL, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true. You must set ``clientBroker`` to either ``TLS`` or ``TLS_PLAINTEXT`` . If you choose ``TLS_PLAINTEXT`` , then you must also set ``unauthenticated`` to true.
            :param tls: Details for ClientAuthentication using TLS. To turn on TLS access control, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true and ``clientBroker`` to ``TLS`` .
            :param unauthenticated: Details for ClientAuthentication using no authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-clientauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                client_authentication_property = msk_mixins.CfnClusterPropsMixin.ClientAuthenticationProperty(
                    sasl=msk_mixins.CfnClusterPropsMixin.SaslProperty(
                        iam=msk_mixins.CfnClusterPropsMixin.IamProperty(
                            enabled=False
                        ),
                        scram=msk_mixins.CfnClusterPropsMixin.ScramProperty(
                            enabled=False
                        )
                    ),
                    tls=msk_mixins.CfnClusterPropsMixin.TlsProperty(
                        certificate_authority_arn_list=["certificateAuthorityArnList"],
                        enabled=False
                    ),
                    unauthenticated=msk_mixins.CfnClusterPropsMixin.UnauthenticatedProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b073c3781a2352f12bfd438ccb236d58156044003eccbd82aeaf2c775e5510e7)
                check_type(argname="argument sasl", value=sasl, expected_type=type_hints["sasl"])
                check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
                check_type(argname="argument unauthenticated", value=unauthenticated, expected_type=type_hints["unauthenticated"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sasl is not None:
                self._values["sasl"] = sasl
            if tls is not None:
                self._values["tls"] = tls
            if unauthenticated is not None:
                self._values["unauthenticated"] = unauthenticated

        @builtins.property
        def sasl(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SaslProperty"]]:
            '''Details for client authentication using SASL.

            To turn on SASL, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true. You must set ``clientBroker`` to either ``TLS`` or ``TLS_PLAINTEXT`` . If you choose ``TLS_PLAINTEXT`` , then you must also set ``unauthenticated`` to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-clientauthentication.html#cfn-msk-cluster-clientauthentication-sasl
            '''
            result = self._values.get("sasl")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SaslProperty"]], result)

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.TlsProperty"]]:
            '''Details for ClientAuthentication using TLS.

            To turn on TLS access control, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true and ``clientBroker`` to ``TLS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-clientauthentication.html#cfn-msk-cluster-clientauthentication-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.TlsProperty"]], result)

        @builtins.property
        def unauthenticated(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.UnauthenticatedProperty"]]:
            '''Details for ClientAuthentication using no authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-clientauthentication.html#cfn-msk-cluster-clientauthentication-unauthenticated
            '''
            result = self._values.get("unauthenticated")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.UnauthenticatedProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.CloudWatchLogsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "log_group": "logGroup"},
    )
    class CloudWatchLogsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            log_group: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details of the CloudWatch Logs destination for broker logs.

            :param enabled: Specifies whether broker logs get sent to the specified CloudWatch Logs destination.
            :param log_group: The CloudWatch log group that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-cloudwatchlogs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                cloud_watch_logs_property = msk_mixins.CfnClusterPropsMixin.CloudWatchLogsProperty(
                    enabled=False,
                    log_group="logGroup"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__21cdfdd2e8c4843cfd05c10b04f8dc48762d5b18adc170f653c02482ae0e59d4)
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
            '''Specifies whether broker logs get sent to the specified CloudWatch Logs destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-cloudwatchlogs.html#cfn-msk-cluster-cloudwatchlogs-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def log_group(self) -> typing.Optional[builtins.str]:
            '''The CloudWatch log group that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-cloudwatchlogs.html#cfn-msk-cluster-cloudwatchlogs-loggroup
            '''
            result = self._values.get("log_group")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.ConfigurationInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn", "revision": "revision"},
    )
    class ConfigurationInfoProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            revision: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the configuration to use for the brokers.

            :param arn: ARN of the configuration to use.
            :param revision: The revision of the configuration to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-configurationinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                configuration_info_property = msk_mixins.CfnClusterPropsMixin.ConfigurationInfoProperty(
                    arn="arn",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea285c1e35997aca39a30ff414e1017fca3c699cd71ea68312215a82eda10cb9)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if revision is not None:
                self._values["revision"] = revision

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the configuration to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-configurationinfo.html#cfn-msk-cluster-configurationinfo-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[jsii.Number]:
            '''The revision of the configuration to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-configurationinfo.html#cfn-msk-cluster-configurationinfo-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.ConnectivityInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "public_access": "publicAccess",
            "vpc_connectivity": "vpcConnectivity",
        },
    )
    class ConnectivityInfoProperty:
        def __init__(
            self,
            *,
            public_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.PublicAccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_connectivity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VpcConnectivityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Broker access controls.

            :param public_access: Access control settings for the cluster's brokers.
            :param vpc_connectivity: VPC connection control settings for brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-connectivityinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                connectivity_info_property = msk_mixins.CfnClusterPropsMixin.ConnectivityInfoProperty(
                    public_access=msk_mixins.CfnClusterPropsMixin.PublicAccessProperty(
                        type="type"
                    ),
                    vpc_connectivity=msk_mixins.CfnClusterPropsMixin.VpcConnectivityProperty(
                        client_authentication=msk_mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty(
                            sasl=msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                                iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                                    enabled=False
                                ),
                                scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                                    enabled=False
                                )
                            ),
                            tls=msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                                enabled=False
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d25998fd59a3e4db5f44062648f83a062ac916ad186828a946adfc61696da26)
                check_type(argname="argument public_access", value=public_access, expected_type=type_hints["public_access"])
                check_type(argname="argument vpc_connectivity", value=vpc_connectivity, expected_type=type_hints["vpc_connectivity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if public_access is not None:
                self._values["public_access"] = public_access
            if vpc_connectivity is not None:
                self._values["vpc_connectivity"] = vpc_connectivity

        @builtins.property
        def public_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PublicAccessProperty"]]:
            '''Access control settings for the cluster's brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-connectivityinfo.html#cfn-msk-cluster-connectivityinfo-publicaccess
            '''
            result = self._values.get("public_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PublicAccessProperty"]], result)

        @builtins.property
        def vpc_connectivity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityProperty"]]:
            '''VPC connection control settings for brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-connectivityinfo.html#cfn-msk-cluster-connectivityinfo-vpcconnectivity
            '''
            result = self._values.get("vpc_connectivity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectivityInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.EBSStorageInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "provisioned_throughput": "provisionedThroughput",
            "volume_size": "volumeSize",
        },
    )
    class EBSStorageInfoProperty:
        def __init__(
            self,
            *,
            provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ProvisionedThroughputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about the EBS storage volumes attached to the broker nodes.

            :param provisioned_throughput: EBS volume provisioned throughput information.
            :param volume_size: The size in GiB of the EBS volume for the data drive on each broker node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-ebsstorageinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                e_bSStorage_info_property = msk_mixins.CfnClusterPropsMixin.EBSStorageInfoProperty(
                    provisioned_throughput=msk_mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty(
                        enabled=False,
                        volume_throughput=123
                    ),
                    volume_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e610a184dc671a0f8f3dece730eec00f1b4e513dc736a4860d2b266bd375cafc)
                check_type(argname="argument provisioned_throughput", value=provisioned_throughput, expected_type=type_hints["provisioned_throughput"])
                check_type(argname="argument volume_size", value=volume_size, expected_type=type_hints["volume_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provisioned_throughput is not None:
                self._values["provisioned_throughput"] = provisioned_throughput
            if volume_size is not None:
                self._values["volume_size"] = volume_size

        @builtins.property
        def provisioned_throughput(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ProvisionedThroughputProperty"]]:
            '''EBS volume provisioned throughput information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-ebsstorageinfo.html#cfn-msk-cluster-ebsstorageinfo-provisionedthroughput
            '''
            result = self._values.get("provisioned_throughput")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ProvisionedThroughputProperty"]], result)

        @builtins.property
        def volume_size(self) -> typing.Optional[jsii.Number]:
            '''The size in GiB of the EBS volume for the data drive on each broker node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-ebsstorageinfo.html#cfn-msk-cluster-ebsstorageinfo-volumesize
            '''
            result = self._values.get("volume_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EBSStorageInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.EncryptionAtRestProperty",
        jsii_struct_bases=[],
        name_mapping={"data_volume_kms_key_id": "dataVolumeKmsKeyId"},
    )
    class EncryptionAtRestProperty:
        def __init__(
            self,
            *,
            data_volume_kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The data-volume encryption details.

            You can't update encryption at rest settings for existing clusters.

            :param data_volume_kms_key_id: The ARN of the Amazon KMS key for encrypting data at rest. If you don't specify a KMS key, MSK creates one for you and uses it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionatrest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                encryption_at_rest_property = msk_mixins.CfnClusterPropsMixin.EncryptionAtRestProperty(
                    data_volume_kms_key_id="dataVolumeKmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fff6cb8cb2dcfe4f58c277712aa26bdc011c986a2bba971c418dbd9a7ba64c4)
                check_type(argname="argument data_volume_kms_key_id", value=data_volume_kms_key_id, expected_type=type_hints["data_volume_kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_volume_kms_key_id is not None:
                self._values["data_volume_kms_key_id"] = data_volume_kms_key_id

        @builtins.property
        def data_volume_kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon KMS key for encrypting data at rest.

            If you don't specify a KMS key, MSK creates one for you and uses it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionatrest.html#cfn-msk-cluster-encryptionatrest-datavolumekmskeyid
            '''
            result = self._values.get("data_volume_kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionAtRestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.EncryptionInTransitProperty",
        jsii_struct_bases=[],
        name_mapping={"client_broker": "clientBroker", "in_cluster": "inCluster"},
    )
    class EncryptionInTransitProperty:
        def __init__(
            self,
            *,
            client_broker: typing.Optional[builtins.str] = None,
            in_cluster: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The settings for encrypting data in transit.

            :param client_broker: Indicates the encryption setting for data in transit between clients and brokers. You must set it to one of the following values. - ``TLS`` : Indicates that client-broker communication is enabled with TLS only. - ``TLS_PLAINTEXT`` : Indicates that client-broker communication is enabled for both TLS-encrypted, as well as plaintext data. - ``PLAINTEXT`` : Indicates that client-broker communication is enabled in plaintext only. The default value is ``TLS`` .
            :param in_cluster: When set to true, it indicates that data communication among the broker nodes of the cluster is encrypted. When set to false, the communication happens in plaintext. The default value is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionintransit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                encryption_in_transit_property = msk_mixins.CfnClusterPropsMixin.EncryptionInTransitProperty(
                    client_broker="clientBroker",
                    in_cluster=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31e7381ca963e62bf161c2b669ab68c19a815c2fb6bafb73d9ccaf585ebaa4ea)
                check_type(argname="argument client_broker", value=client_broker, expected_type=type_hints["client_broker"])
                check_type(argname="argument in_cluster", value=in_cluster, expected_type=type_hints["in_cluster"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_broker is not None:
                self._values["client_broker"] = client_broker
            if in_cluster is not None:
                self._values["in_cluster"] = in_cluster

        @builtins.property
        def client_broker(self) -> typing.Optional[builtins.str]:
            '''Indicates the encryption setting for data in transit between clients and brokers.

            You must set it to one of the following values.

            - ``TLS`` : Indicates that client-broker communication is enabled with TLS only.
            - ``TLS_PLAINTEXT`` : Indicates that client-broker communication is enabled for both TLS-encrypted, as well as plaintext data.
            - ``PLAINTEXT`` : Indicates that client-broker communication is enabled in plaintext only.

            The default value is ``TLS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionintransit.html#cfn-msk-cluster-encryptionintransit-clientbroker
            '''
            result = self._values.get("client_broker")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def in_cluster(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When set to true, it indicates that data communication among the broker nodes of the cluster is encrypted.

            When set to false, the communication happens in plaintext.

            The default value is true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptionintransit.html#cfn-msk-cluster-encryptionintransit-incluster
            '''
            result = self._values.get("in_cluster")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionInTransitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.EncryptionInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_at_rest": "encryptionAtRest",
            "encryption_in_transit": "encryptionInTransit",
        },
    )
    class EncryptionInfoProperty:
        def __init__(
            self,
            *,
            encryption_at_rest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EncryptionAtRestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            encryption_in_transit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EncryptionInTransitProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Includes encryption-related information, such as the Amazon KMS key used for encrypting data at rest and whether you want MSK to encrypt your data in transit.

            :param encryption_at_rest: The data-volume encryption details.
            :param encryption_in_transit: The details for encryption in transit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptioninfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                encryption_info_property = msk_mixins.CfnClusterPropsMixin.EncryptionInfoProperty(
                    encryption_at_rest=msk_mixins.CfnClusterPropsMixin.EncryptionAtRestProperty(
                        data_volume_kms_key_id="dataVolumeKmsKeyId"
                    ),
                    encryption_in_transit=msk_mixins.CfnClusterPropsMixin.EncryptionInTransitProperty(
                        client_broker="clientBroker",
                        in_cluster=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77d9f94ae9254e09e879588e0dc35f8c879e6e6e8eb18e682318ce0ea7446bb2)
                check_type(argname="argument encryption_at_rest", value=encryption_at_rest, expected_type=type_hints["encryption_at_rest"])
                check_type(argname="argument encryption_in_transit", value=encryption_in_transit, expected_type=type_hints["encryption_in_transit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_at_rest is not None:
                self._values["encryption_at_rest"] = encryption_at_rest
            if encryption_in_transit is not None:
                self._values["encryption_in_transit"] = encryption_in_transit

        @builtins.property
        def encryption_at_rest(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionAtRestProperty"]]:
            '''The data-volume encryption details.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptioninfo.html#cfn-msk-cluster-encryptioninfo-encryptionatrest
            '''
            result = self._values.get("encryption_at_rest")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionAtRestProperty"]], result)

        @builtins.property
        def encryption_in_transit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionInTransitProperty"]]:
            '''The details for encryption in transit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-encryptioninfo.html#cfn-msk-cluster-encryptioninfo-encryptionintransit
            '''
            result = self._values.get("encryption_in_transit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionInTransitProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.FirehoseProperty",
        jsii_struct_bases=[],
        name_mapping={"delivery_stream": "deliveryStream", "enabled": "enabled"},
    )
    class FirehoseProperty:
        def __init__(
            self,
            *,
            delivery_stream: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Firehose details for BrokerLogs.

            :param delivery_stream: The Kinesis Data Firehose delivery stream that is the destination for broker logs.
            :param enabled: Specifies whether broker logs get send to the specified Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-firehose.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                firehose_property = msk_mixins.CfnClusterPropsMixin.FirehoseProperty(
                    delivery_stream="deliveryStream",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8f10605804c1447706f3f3d87f03d9693009073ab40af3ecac00754ef6709c4)
                check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream is not None:
                self._values["delivery_stream"] = delivery_stream
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def delivery_stream(self) -> typing.Optional[builtins.str]:
            '''The Kinesis Data Firehose delivery stream that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-firehose.html#cfn-msk-cluster-firehose-deliverystream
            '''
            result = self._values.get("delivery_stream")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether broker logs get send to the specified Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-firehose.html#cfn-msk-cluster-firehose-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.IamProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class IamProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for SASL/IAM client authentication.

            :param enabled: SASL/IAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-iam.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                iam_property = msk_mixins.CfnClusterPropsMixin.IamProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77dadf6a70d734cc0f2a2aace9bd5d763dd9165740e63e8e2a1975f5b04e3d2c)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''SASL/IAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-iam.html#cfn-msk-cluster-iam-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.JmxExporterProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled_in_broker": "enabledInBroker"},
    )
    class JmxExporterProperty:
        def __init__(
            self,
            *,
            enabled_in_broker: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Indicates whether you want to enable or disable the JMX Exporter.

            :param enabled_in_broker: Indicates whether you want to enable or disable the JMX Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-jmxexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                jmx_exporter_property = msk_mixins.CfnClusterPropsMixin.JmxExporterProperty(
                    enabled_in_broker=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9cd03d4217e8aed3d069df4a3a662713f638998532efa7a7575aa939b41df179)
                check_type(argname="argument enabled_in_broker", value=enabled_in_broker, expected_type=type_hints["enabled_in_broker"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled_in_broker is not None:
                self._values["enabled_in_broker"] = enabled_in_broker

        @builtins.property
        def enabled_in_broker(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether you want to enable or disable the JMX Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-jmxexporter.html#cfn-msk-cluster-jmxexporter-enabledinbroker
            '''
            result = self._values.get("enabled_in_broker")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JmxExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.LoggingInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"broker_logs": "brokerLogs"},
    )
    class LoggingInfoProperty:
        def __init__(
            self,
            *,
            broker_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.BrokerLogsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''You can configure your MSK cluster to send broker logs to different destination types.

            This is a container for the configuration details related to broker logs.

            :param broker_logs: You can configure your MSK cluster to send broker logs to different destination types. This configuration specifies the details of these destinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-logginginfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                logging_info_property = msk_mixins.CfnClusterPropsMixin.LoggingInfoProperty(
                    broker_logs=msk_mixins.CfnClusterPropsMixin.BrokerLogsProperty(
                        cloud_watch_logs=msk_mixins.CfnClusterPropsMixin.CloudWatchLogsProperty(
                            enabled=False,
                            log_group="logGroup"
                        ),
                        firehose=msk_mixins.CfnClusterPropsMixin.FirehoseProperty(
                            delivery_stream="deliveryStream",
                            enabled=False
                        ),
                        s3=msk_mixins.CfnClusterPropsMixin.S3Property(
                            bucket="bucket",
                            enabled=False,
                            prefix="prefix"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a2650c466d52c0e685b2616a240e17ec78d958f8f8a5754e4a7426fc7582182)
                check_type(argname="argument broker_logs", value=broker_logs, expected_type=type_hints["broker_logs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if broker_logs is not None:
                self._values["broker_logs"] = broker_logs

        @builtins.property
        def broker_logs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BrokerLogsProperty"]]:
            '''You can configure your MSK cluster to send broker logs to different destination types.

            This configuration specifies the details of these destinations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-logginginfo.html#cfn-msk-cluster-logginginfo-brokerlogs
            '''
            result = self._values.get("broker_logs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BrokerLogsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.NodeExporterProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled_in_broker": "enabledInBroker"},
    )
    class NodeExporterProperty:
        def __init__(
            self,
            *,
            enabled_in_broker: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Indicates whether you want to enable or disable the Node Exporter.

            :param enabled_in_broker: Indicates whether you want to enable or disable the Node Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-nodeexporter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                node_exporter_property = msk_mixins.CfnClusterPropsMixin.NodeExporterProperty(
                    enabled_in_broker=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__337606c7e198f51b7a7fb53a4dd88f905aa7511112eef88d3a4c621b92535108)
                check_type(argname="argument enabled_in_broker", value=enabled_in_broker, expected_type=type_hints["enabled_in_broker"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled_in_broker is not None:
                self._values["enabled_in_broker"] = enabled_in_broker

        @builtins.property
        def enabled_in_broker(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether you want to enable or disable the Node Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-nodeexporter.html#cfn-msk-cluster-nodeexporter-enabledinbroker
            '''
            result = self._values.get("enabled_in_broker")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeExporterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.OpenMonitoringProperty",
        jsii_struct_bases=[],
        name_mapping={"prometheus": "prometheus"},
    )
    class OpenMonitoringProperty:
        def __init__(
            self,
            *,
            prometheus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.PrometheusProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''JMX and Node monitoring for the MSK cluster.

            :param prometheus: Prometheus exporter settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-openmonitoring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                open_monitoring_property = msk_mixins.CfnClusterPropsMixin.OpenMonitoringProperty(
                    prometheus=msk_mixins.CfnClusterPropsMixin.PrometheusProperty(
                        jmx_exporter=msk_mixins.CfnClusterPropsMixin.JmxExporterProperty(
                            enabled_in_broker=False
                        ),
                        node_exporter=msk_mixins.CfnClusterPropsMixin.NodeExporterProperty(
                            enabled_in_broker=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5df05b95f25f523959ad0ccda74a67613a4f31caaf78f266fb4d88b054ec3eaa)
                check_type(argname="argument prometheus", value=prometheus, expected_type=type_hints["prometheus"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if prometheus is not None:
                self._values["prometheus"] = prometheus

        @builtins.property
        def prometheus(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PrometheusProperty"]]:
            '''Prometheus exporter settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-openmonitoring.html#cfn-msk-cluster-openmonitoring-prometheus
            '''
            result = self._values.get("prometheus")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.PrometheusProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenMonitoringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.PrometheusProperty",
        jsii_struct_bases=[],
        name_mapping={"jmx_exporter": "jmxExporter", "node_exporter": "nodeExporter"},
    )
    class PrometheusProperty:
        def __init__(
            self,
            *,
            jmx_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.JmxExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            node_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.NodeExporterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Prometheus settings for open monitoring.

            :param jmx_exporter: Indicates whether you want to enable or disable the JMX Exporter.
            :param node_exporter: Indicates whether you want to enable or disable the Node Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-prometheus.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                prometheus_property = msk_mixins.CfnClusterPropsMixin.PrometheusProperty(
                    jmx_exporter=msk_mixins.CfnClusterPropsMixin.JmxExporterProperty(
                        enabled_in_broker=False
                    ),
                    node_exporter=msk_mixins.CfnClusterPropsMixin.NodeExporterProperty(
                        enabled_in_broker=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd7223f8b8e51d45f6f9bbeb9e8f1bdf34b0c15ed3524513a0142890b00808ca)
                check_type(argname="argument jmx_exporter", value=jmx_exporter, expected_type=type_hints["jmx_exporter"])
                check_type(argname="argument node_exporter", value=node_exporter, expected_type=type_hints["node_exporter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if jmx_exporter is not None:
                self._values["jmx_exporter"] = jmx_exporter
            if node_exporter is not None:
                self._values["node_exporter"] = node_exporter

        @builtins.property
        def jmx_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JmxExporterProperty"]]:
            '''Indicates whether you want to enable or disable the JMX Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-prometheus.html#cfn-msk-cluster-prometheus-jmxexporter
            '''
            result = self._values.get("jmx_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JmxExporterProperty"]], result)

        @builtins.property
        def node_exporter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.NodeExporterProperty"]]:
            '''Indicates whether you want to enable or disable the Node Exporter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-prometheus.html#cfn-msk-cluster-prometheus-nodeexporter
            '''
            result = self._values.get("node_exporter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.NodeExporterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrometheusProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "volume_throughput": "volumeThroughput"},
    )
    class ProvisionedThroughputProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            volume_throughput: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about provisioned throughput for EBS storage volumes attached to kafka broker nodes.

            :param enabled: Provisioned throughput is on or off.
            :param volume_throughput: Throughput value of the EBS volumes for the data drive on each kafka broker node in MiB per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-provisionedthroughput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                provisioned_throughput_property = msk_mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty(
                    enabled=False,
                    volume_throughput=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3382a5226baa81f23f60d39625eb18caef2f334c9276ae1c95b09fbf026c7128)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument volume_throughput", value=volume_throughput, expected_type=type_hints["volume_throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if volume_throughput is not None:
                self._values["volume_throughput"] = volume_throughput

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Provisioned throughput is on or off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-provisionedthroughput.html#cfn-msk-cluster-provisionedthroughput-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def volume_throughput(self) -> typing.Optional[jsii.Number]:
            '''Throughput value of the EBS volumes for the data drive on each kafka broker node in MiB per second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-provisionedthroughput.html#cfn-msk-cluster-provisionedthroughput-volumethroughput
            '''
            result = self._values.get("volume_throughput")
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
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.PublicAccessProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class PublicAccessProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''Broker access controls.

            :param type: DISABLED means that public access is turned off. SERVICE_PROVIDED_EIPS means that public access is turned on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-publicaccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                public_access_property = msk_mixins.CfnClusterPropsMixin.PublicAccessProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27edfdf964bea0b29c632401c8a058fb3339a3ac5d8aab66efb5ba5fb0af26ff)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''DISABLED means that public access is turned off.

            SERVICE_PROVIDED_EIPS means that public access is turned on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-publicaccess.html#cfn-msk-cluster-publicaccess-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.RebalancingProperty",
        jsii_struct_bases=[],
        name_mapping={"status": "status"},
    )
    class RebalancingProperty:
        def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
            '''
            :param status: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-rebalancing.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                rebalancing_property = msk_mixins.CfnClusterPropsMixin.RebalancingProperty(
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__359ce1419d958f4b0c875714d3b04522a5245257061b4429f14277ba9b208c7a)
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-rebalancing.html#cfn-msk-cluster-rebalancing-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RebalancingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.S3Property",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "enabled": "enabled", "prefix": "prefix"},
    )
    class S3Property:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the Amazon S3 destination for broker logs.

            :param bucket: The name of the S3 bucket that is the destination for broker logs.
            :param enabled: Specifies whether broker logs get sent to the specified Amazon S3 destination.
            :param prefix: The S3 prefix that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                s3_property = msk_mixins.CfnClusterPropsMixin.S3Property(
                    bucket="bucket",
                    enabled=False,
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd62805d8b77137915562f5cff7948dca6986b3db7637193fa22433d03e90f38)
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
            '''The name of the S3 bucket that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-s3.html#cfn-msk-cluster-s3-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether broker logs get sent to the specified Amazon S3 destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-s3.html#cfn-msk-cluster-s3-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 prefix that is the destination for broker logs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-s3.html#cfn-msk-cluster-s3-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.SaslProperty",
        jsii_struct_bases=[],
        name_mapping={"iam": "iam", "scram": "scram"},
    )
    class SaslProperty:
        def __init__(
            self,
            *,
            iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.IamProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scram: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ScramProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details for client authentication using SASL.

            To turn on SASL, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true. You must set ``clientBroker`` to either ``TLS`` or ``TLS_PLAINTEXT`` . If you choose ``TLS_PLAINTEXT`` , then you must also set ``unauthenticated`` to true.

            :param iam: Details for ClientAuthentication using IAM.
            :param scram: Details for SASL/SCRAM client authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-sasl.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                sasl_property = msk_mixins.CfnClusterPropsMixin.SaslProperty(
                    iam=msk_mixins.CfnClusterPropsMixin.IamProperty(
                        enabled=False
                    ),
                    scram=msk_mixins.CfnClusterPropsMixin.ScramProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d86dbd9b5445111d1717934ff350a9dab92103936955b52b55d595bdedf36bf)
                check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
                check_type(argname="argument scram", value=scram, expected_type=type_hints["scram"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam is not None:
                self._values["iam"] = iam
            if scram is not None:
                self._values["scram"] = scram

        @builtins.property
        def iam(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.IamProperty"]]:
            '''Details for ClientAuthentication using IAM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-sasl.html#cfn-msk-cluster-sasl-iam
            '''
            result = self._values.get("iam")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.IamProperty"]], result)

        @builtins.property
        def scram(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScramProperty"]]:
            '''Details for SASL/SCRAM client authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-sasl.html#cfn-msk-cluster-sasl-scram
            '''
            result = self._values.get("scram")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ScramProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SaslProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.ScramProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ScramProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for SASL/SCRAM client authentication.

            :param enabled: SASL/SCRAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-scram.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                scram_property = msk_mixins.CfnClusterPropsMixin.ScramProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc8fcbdfa7f8267fa44d181ba27e8387bce546e43452c0554c850fafa52dc4c0)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''SASL/SCRAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-scram.html#cfn-msk-cluster-scram-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScramProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.StorageInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"ebs_storage_info": "ebsStorageInfo"},
    )
    class StorageInfoProperty:
        def __init__(
            self,
            *,
            ebs_storage_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EBSStorageInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about storage volumes attached to Amazon MSK broker nodes.

            :param ebs_storage_info: EBS volume information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-storageinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                storage_info_property = msk_mixins.CfnClusterPropsMixin.StorageInfoProperty(
                    ebs_storage_info=msk_mixins.CfnClusterPropsMixin.EBSStorageInfoProperty(
                        provisioned_throughput=msk_mixins.CfnClusterPropsMixin.ProvisionedThroughputProperty(
                            enabled=False,
                            volume_throughput=123
                        ),
                        volume_size=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54ba410e71611a28c31d3d99aee5f80d592d813fe0b4e79e23e5841a4f28c2b1)
                check_type(argname="argument ebs_storage_info", value=ebs_storage_info, expected_type=type_hints["ebs_storage_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ebs_storage_info is not None:
                self._values["ebs_storage_info"] = ebs_storage_info

        @builtins.property
        def ebs_storage_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EBSStorageInfoProperty"]]:
            '''EBS volume information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-storageinfo.html#cfn-msk-cluster-storageinfo-ebsstorageinfo
            '''
            result = self._values.get("ebs_storage_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EBSStorageInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.TlsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_authority_arn_list": "certificateAuthorityArnList",
            "enabled": "enabled",
        },
    )
    class TlsProperty:
        def __init__(
            self,
            *,
            certificate_authority_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for client authentication using TLS.

            :param certificate_authority_arn_list: List of AWS Private CA ARNs.
            :param enabled: TLS authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-tls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                tls_property = msk_mixins.CfnClusterPropsMixin.TlsProperty(
                    certificate_authority_arn_list=["certificateAuthorityArnList"],
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__420097dbe358b66067925f982f42877df2958e538bff966a4c6501a7c95bff55)
                check_type(argname="argument certificate_authority_arn_list", value=certificate_authority_arn_list, expected_type=type_hints["certificate_authority_arn_list"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_authority_arn_list is not None:
                self._values["certificate_authority_arn_list"] = certificate_authority_arn_list
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def certificate_authority_arn_list(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''List of AWS Private CA ARNs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-tls.html#cfn-msk-cluster-tls-certificateauthorityarnlist
            '''
            result = self._values.get("certificate_authority_arn_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''TLS authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-tls.html#cfn-msk-cluster-tls-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.UnauthenticatedProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class UnauthenticatedProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for allowing no client authentication.

            :param enabled: Unauthenticated is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-unauthenticated.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                unauthenticated_property = msk_mixins.CfnClusterPropsMixin.UnauthenticatedProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7f2409abc68c52d982f75baa40cfdab4fbb4b289fb15d8c8fd74a38b8aead7f)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Unauthenticated is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-unauthenticated.html#cfn-msk-cluster-unauthenticated-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UnauthenticatedProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"sasl": "sasl", "tls": "tls"},
    )
    class VpcConnectivityClientAuthenticationProperty:
        def __init__(
            self,
            *,
            sasl: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VpcConnectivitySaslProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VpcConnectivityTlsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Includes all client authentication information for VpcConnectivity.

            :param sasl: Details for VpcConnectivity ClientAuthentication using SASL.
            :param tls: Details for VpcConnectivity ClientAuthentication using TLS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityclientauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_connectivity_client_authentication_property = msk_mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty(
                    sasl=msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                        iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                            enabled=False
                        ),
                        scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                            enabled=False
                        )
                    ),
                    tls=msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__508a81b64a2cb9a407be54f1c257a40fe23d37612156d292242424b33edb770d)
                check_type(argname="argument sasl", value=sasl, expected_type=type_hints["sasl"])
                check_type(argname="argument tls", value=tls, expected_type=type_hints["tls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sasl is not None:
                self._values["sasl"] = sasl
            if tls is not None:
                self._values["tls"] = tls

        @builtins.property
        def sasl(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivitySaslProperty"]]:
            '''Details for VpcConnectivity ClientAuthentication using SASL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityclientauthentication.html#cfn-msk-cluster-vpcconnectivityclientauthentication-sasl
            '''
            result = self._values.get("sasl")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivitySaslProperty"]], result)

        @builtins.property
        def tls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityTlsProperty"]]:
            '''Details for VpcConnectivity ClientAuthentication using TLS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityclientauthentication.html#cfn-msk-cluster-vpcconnectivityclientauthentication-tls
            '''
            result = self._values.get("tls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityTlsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConnectivityClientAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class VpcConnectivityIamProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for SASL/IAM client authentication for VpcConnectivity.

            :param enabled: SASL/IAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityiam.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_connectivity_iam_property = msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2c4b210c49b092c1dc328ca1fa398fd34f247e00b60e8cb057abaef23ef9fc0)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''SASL/IAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityiam.html#cfn-msk-cluster-vpcconnectivityiam-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConnectivityIamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.VpcConnectivityProperty",
        jsii_struct_bases=[],
        name_mapping={"client_authentication": "clientAuthentication"},
    )
    class VpcConnectivityProperty:
        def __init__(
            self,
            *,
            client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''VPC connection control settings for brokers.

            :param client_authentication: VPC connection control settings for brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_connectivity_property = msk_mixins.CfnClusterPropsMixin.VpcConnectivityProperty(
                    client_authentication=msk_mixins.CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty(
                        sasl=msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                            iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                                enabled=False
                            ),
                            scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                                enabled=False
                            )
                        ),
                        tls=msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                            enabled=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74a814713cb9d3d580e69ac9a4cfdef0fad55e82eb2aef115273e111ddde7e58)
                check_type(argname="argument client_authentication", value=client_authentication, expected_type=type_hints["client_authentication"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_authentication is not None:
                self._values["client_authentication"] = client_authentication

        @builtins.property
        def client_authentication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty"]]:
            '''VPC connection control settings for brokers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivity.html#cfn-msk-cluster-vpcconnectivity-clientauthentication
            '''
            result = self._values.get("client_authentication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConnectivityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty",
        jsii_struct_bases=[],
        name_mapping={"iam": "iam", "scram": "scram"},
    )
    class VpcConnectivitySaslProperty:
        def __init__(
            self,
            *,
            iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VpcConnectivityIamProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scram: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.VpcConnectivityScramProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details for client authentication using SASL for VpcConnectivity.

            :param iam: Details for ClientAuthentication using IAM for VpcConnectivity.
            :param scram: Details for SASL/SCRAM client authentication for VpcConnectivity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivitysasl.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_connectivity_sasl_property = msk_mixins.CfnClusterPropsMixin.VpcConnectivitySaslProperty(
                    iam=msk_mixins.CfnClusterPropsMixin.VpcConnectivityIamProperty(
                        enabled=False
                    ),
                    scram=msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa7032805e8d923b77a845776df62972119fb10889d311da4be83345fa325a9d)
                check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
                check_type(argname="argument scram", value=scram, expected_type=type_hints["scram"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam is not None:
                self._values["iam"] = iam
            if scram is not None:
                self._values["scram"] = scram

        @builtins.property
        def iam(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityIamProperty"]]:
            '''Details for ClientAuthentication using IAM for VpcConnectivity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivitysasl.html#cfn-msk-cluster-vpcconnectivitysasl-iam
            '''
            result = self._values.get("iam")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityIamProperty"]], result)

        @builtins.property
        def scram(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityScramProperty"]]:
            '''Details for SASL/SCRAM client authentication for VpcConnectivity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivitysasl.html#cfn-msk-cluster-vpcconnectivitysasl-scram
            '''
            result = self._values.get("scram")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.VpcConnectivityScramProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConnectivitySaslProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class VpcConnectivityScramProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for SASL/SCRAM client authentication for VpcConnectivity.

            :param enabled: SASL/SCRAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityscram.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_connectivity_scram_property = msk_mixins.CfnClusterPropsMixin.VpcConnectivityScramProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9a37c16e63adb809eaa22ea09d28074aacfccf844734b20c3cf5ea9d83a2557)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''SASL/SCRAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivityscram.html#cfn-msk-cluster-vpcconnectivityscram-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConnectivityScramProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class VpcConnectivityTlsProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for client authentication using TLS for VpcConnectivity.

            :param enabled: TLS authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivitytls.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_connectivity_tls_property = msk_mixins.CfnClusterPropsMixin.VpcConnectivityTlsProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de1a87fb3d457d9df064a47597e0f529c244a012cb0e99d8d8570ea28d2fc433)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''TLS authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-cluster-vpcconnectivitytls.html#cfn-msk-cluster-vpcconnectivitytls-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConnectivityTlsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "kafka_versions_list": "kafkaVersionsList",
        "latest_revision": "latestRevision",
        "name": "name",
        "server_properties": "serverProperties",
    },
)
class CfnConfigurationMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        kafka_versions_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        latest_revision: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConfigurationPropsMixin.LatestRevisionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        server_properties: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConfigurationPropsMixin.

        :param description: The description of the configuration.
        :param kafka_versions_list: The `versions of Apache Kafka <https://docs.aws.amazon.com/msk/latest/developerguide/supported-kafka-versions.html>`_ with which you can use this MSK configuration. When you update the ``KafkaVersionsList`` property, CloudFormation recreates a new configuration with the updated property before deleting the old configuration. Such an update requires a `resource replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ . To successfully update ``KafkaVersionsList`` , you must also update the ``Name`` property in the same operation. If your configuration is attached with any clusters created using the AWS Management Console or AWS CLI , you'll need to manually delete the old configuration from the console after the update completes. For more information, see `Can’t update KafkaVersionsList in MSK configuration <https://docs.aws.amazon.com/msk/latest/developerguide/troubleshooting.html#troubleshoot-kafkaversionslist-cfn-update-failure>`_ in the *Amazon MSK Developer Guide* .
        :param latest_revision: Latest revision of the MSK configuration.
        :param name: The name of the configuration. Configuration names are strings that match the regex "^[0-9A-Za-z][0-9A-Za-z-]{0,}$".
        :param server_properties: Contents of the ``server.properties`` file. When using the console, the SDK, or the AWS CLI , the contents of ``server.properties`` can be in plaintext.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            cfn_configuration_mixin_props = msk_mixins.CfnConfigurationMixinProps(
                description="description",
                kafka_versions_list=["kafkaVersionsList"],
                latest_revision=msk_mixins.CfnConfigurationPropsMixin.LatestRevisionProperty(
                    creation_time="creationTime",
                    description="description",
                    revision=123
                ),
                name="name",
                server_properties="serverProperties"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__309e186ba1333c2dfeb8257ffa2fa9622898a42eebe6e692ea5a9dd8da9321db)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kafka_versions_list", value=kafka_versions_list, expected_type=type_hints["kafka_versions_list"])
            check_type(argname="argument latest_revision", value=latest_revision, expected_type=type_hints["latest_revision"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument server_properties", value=server_properties, expected_type=type_hints["server_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if kafka_versions_list is not None:
            self._values["kafka_versions_list"] = kafka_versions_list
        if latest_revision is not None:
            self._values["latest_revision"] = latest_revision
        if name is not None:
            self._values["name"] = name
        if server_properties is not None:
            self._values["server_properties"] = server_properties

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html#cfn-msk-configuration-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka_versions_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The `versions of Apache Kafka <https://docs.aws.amazon.com/msk/latest/developerguide/supported-kafka-versions.html>`_ with which you can use this MSK configuration.

        When you update the ``KafkaVersionsList`` property, CloudFormation recreates a new configuration with the updated property before deleting the old configuration. Such an update requires a `resource replacement <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement>`_ . To successfully update ``KafkaVersionsList`` , you must also update the ``Name`` property in the same operation.

        If your configuration is attached with any clusters created using the AWS Management Console or AWS CLI , you'll need to manually delete the old configuration from the console after the update completes.

        For more information, see `Can’t update KafkaVersionsList in MSK configuration <https://docs.aws.amazon.com/msk/latest/developerguide/troubleshooting.html#troubleshoot-kafkaversionslist-cfn-update-failure>`_ in the *Amazon MSK Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html#cfn-msk-configuration-kafkaversionslist
        '''
        result = self._values.get("kafka_versions_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def latest_revision(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPropsMixin.LatestRevisionProperty"]]:
        '''Latest revision of the MSK configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html#cfn-msk-configuration-latestrevision
        '''
        result = self._values.get("latest_revision")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConfigurationPropsMixin.LatestRevisionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration.

        Configuration names are strings that match the regex "^[0-9A-Za-z][0-9A-Za-z-]{0,}$".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html#cfn-msk-configuration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_properties(self) -> typing.Optional[builtins.str]:
        '''Contents of the ``server.properties`` file. When using the console, the SDK, or the AWS CLI , the contents of ``server.properties`` can be in plaintext.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html#cfn-msk-configuration-serverproperties
        '''
        result = self._values.get("server_properties")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnConfigurationPropsMixin",
):
    '''Creates a new MSK configuration.

    To see an example of how to use this operation, first save the following text to a file and name the file ``config-file.txt`` .

    ``auto.create.topics.enable = true zookeeper.connection.timeout.ms = 1000 log.roll.ms = 604800000``

    Now run the following Python 3.6 script in the folder where you saved ``config-file.txt`` . This script uses the properties specified in ``config-file.txt`` to create a configuration named ``SalesClusterConfiguration`` . This configuration can work with Apache Kafka versions 1.1.1 and 2.1.0::

       import boto3 client = boto3.client('kafka') config_file = open('config-file.txt', 'r') server_properties = config_file.read() response = client.create_configuration( Name='SalesClusterConfiguration', Description='The configuration to use on all sales clusters.', KafkaVersions=['1.1.1', '2.1.0'], ServerProperties=server_properties
       ) print(response)

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-configuration.html
    :cloudformationResource: AWS::MSK::Configuration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_configuration_props_mixin = msk_mixins.CfnConfigurationPropsMixin(msk_mixins.CfnConfigurationMixinProps(
            description="description",
            kafka_versions_list=["kafkaVersionsList"],
            latest_revision=msk_mixins.CfnConfigurationPropsMixin.LatestRevisionProperty(
                creation_time="creationTime",
                description="description",
                revision=123
            ),
            name="name",
            server_properties="serverProperties"
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
        '''Create a mixin to apply properties to ``AWS::MSK::Configuration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89df9e38322e2db2a4596a4d0ab7f8557fb188a1dfae6b0ebd570ba8d8d4b583)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d984ac079bf6cb94b7139b33726a7405eb4b153a3f01f78e0a88589881e85a39)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439d0cf5cc83dd0aa96b0a956f2e38d83e3fe40bfc41951fef63728cc76f665b)
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
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnConfigurationPropsMixin.LatestRevisionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "creation_time": "creationTime",
            "description": "description",
            "revision": "revision",
        },
    )
    class LatestRevisionProperty:
        def __init__(
            self,
            *,
            creation_time: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            revision: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a configuration revision.

            :param creation_time: The time when the configuration revision was created.
            :param description: The description of the configuration revision.
            :param revision: The revision number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-configuration-latestrevision.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                latest_revision_property = msk_mixins.CfnConfigurationPropsMixin.LatestRevisionProperty(
                    creation_time="creationTime",
                    description="description",
                    revision=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5b2b7f531189d93c16b8070b70a734accb17fcaab9cfc503e1797b1f42a7d45)
                check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument revision", value=revision, expected_type=type_hints["revision"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if creation_time is not None:
                self._values["creation_time"] = creation_time
            if description is not None:
                self._values["description"] = description
            if revision is not None:
                self._values["revision"] = revision

        @builtins.property
        def creation_time(self) -> typing.Optional[builtins.str]:
            '''The time when the configuration revision was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-configuration-latestrevision.html#cfn-msk-configuration-latestrevision-creationtime
            '''
            result = self._values.get("creation_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the configuration revision.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-configuration-latestrevision.html#cfn-msk-configuration-latestrevision-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def revision(self) -> typing.Optional[jsii.Number]:
            '''The revision number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-configuration-latestrevision.html#cfn-msk-configuration-latestrevision-revision
            '''
            result = self._values.get("revision")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LatestRevisionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "kafka_clusters": "kafkaClusters",
        "replication_info_list": "replicationInfoList",
        "replicator_name": "replicatorName",
        "service_execution_role_arn": "serviceExecutionRoleArn",
        "tags": "tags",
    },
)
class CfnReplicatorMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        kafka_clusters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.KafkaClusterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        replication_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.ReplicationInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        replicator_name: typing.Optional[builtins.str] = None,
        service_execution_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReplicatorPropsMixin.

        :param description: A summary description of the replicator.
        :param kafka_clusters: Kafka Clusters to use in setting up sources / targets for replication.
        :param replication_info_list: A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.
        :param replicator_name: The name of the replicator. Alpha-numeric characters with '-' are allowed.
        :param service_execution_role_arn: The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).
        :param tags: List of tags to attach to created Replicator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            cfn_replicator_mixin_props = msk_mixins.CfnReplicatorMixinProps(
                description="description",
                kafka_clusters=[msk_mixins.CfnReplicatorPropsMixin.KafkaClusterProperty(
                    amazon_msk_cluster=msk_mixins.CfnReplicatorPropsMixin.AmazonMskClusterProperty(
                        msk_cluster_arn="mskClusterArn"
                    ),
                    vpc_config=msk_mixins.CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )],
                replication_info_list=[msk_mixins.CfnReplicatorPropsMixin.ReplicationInfoProperty(
                    consumer_group_replication=msk_mixins.CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty(
                        consumer_groups_to_exclude=["consumerGroupsToExclude"],
                        consumer_groups_to_replicate=["consumerGroupsToReplicate"],
                        detect_and_copy_new_consumer_groups=False,
                        synchronise_consumer_group_offsets=False
                    ),
                    source_kafka_cluster_arn="sourceKafkaClusterArn",
                    target_compression_type="targetCompressionType",
                    target_kafka_cluster_arn="targetKafkaClusterArn",
                    topic_replication=msk_mixins.CfnReplicatorPropsMixin.TopicReplicationProperty(
                        copy_access_control_lists_for_topics=False,
                        copy_topic_configurations=False,
                        detect_and_copy_new_topics=False,
                        starting_position=msk_mixins.CfnReplicatorPropsMixin.ReplicationStartingPositionProperty(
                            type="type"
                        ),
                        topic_name_configuration=msk_mixins.CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty(
                            type="type"
                        ),
                        topics_to_exclude=["topicsToExclude"],
                        topics_to_replicate=["topicsToReplicate"]
                    )
                )],
                replicator_name="replicatorName",
                service_execution_role_arn="serviceExecutionRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c218f31baa5e3a133c8e81420ac8bca409eb478262f9d5c99d08d65aeafa8c4)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kafka_clusters", value=kafka_clusters, expected_type=type_hints["kafka_clusters"])
            check_type(argname="argument replication_info_list", value=replication_info_list, expected_type=type_hints["replication_info_list"])
            check_type(argname="argument replicator_name", value=replicator_name, expected_type=type_hints["replicator_name"])
            check_type(argname="argument service_execution_role_arn", value=service_execution_role_arn, expected_type=type_hints["service_execution_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if kafka_clusters is not None:
            self._values["kafka_clusters"] = kafka_clusters
        if replication_info_list is not None:
            self._values["replication_info_list"] = replication_info_list
        if replicator_name is not None:
            self._values["replicator_name"] = replicator_name
        if service_execution_role_arn is not None:
            self._values["service_execution_role_arn"] = service_execution_role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A summary description of the replicator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html#cfn-msk-replicator-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kafka_clusters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.KafkaClusterProperty"]]]]:
        '''Kafka Clusters to use in setting up sources / targets for replication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html#cfn-msk-replicator-kafkaclusters
        '''
        result = self._values.get("kafka_clusters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.KafkaClusterProperty"]]]], result)

    @builtins.property
    def replication_info_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ReplicationInfoProperty"]]]]:
        '''A list of replication configurations, where each configuration targets a given source cluster to target cluster replication flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html#cfn-msk-replicator-replicationinfolist
        '''
        result = self._values.get("replication_info_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ReplicationInfoProperty"]]]], result)

    @builtins.property
    def replicator_name(self) -> typing.Optional[builtins.str]:
        '''The name of the replicator.

        Alpha-numeric characters with '-' are allowed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html#cfn-msk-replicator-replicatorname
        '''
        result = self._values.get("replicator_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role used by the replicator to access resources in the customer's account (e.g source and target clusters).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html#cfn-msk-replicator-serviceexecutionrolearn
        '''
        result = self._values.get("service_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''List of tags to attach to created Replicator.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html#cfn-msk-replicator-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicatorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicatorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin",
):
    '''Creates the replicator.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-replicator.html
    :cloudformationResource: AWS::MSK::Replicator
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_replicator_props_mixin = msk_mixins.CfnReplicatorPropsMixin(msk_mixins.CfnReplicatorMixinProps(
            description="description",
            kafka_clusters=[msk_mixins.CfnReplicatorPropsMixin.KafkaClusterProperty(
                amazon_msk_cluster=msk_mixins.CfnReplicatorPropsMixin.AmazonMskClusterProperty(
                    msk_cluster_arn="mskClusterArn"
                ),
                vpc_config=msk_mixins.CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )],
            replication_info_list=[msk_mixins.CfnReplicatorPropsMixin.ReplicationInfoProperty(
                consumer_group_replication=msk_mixins.CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty(
                    consumer_groups_to_exclude=["consumerGroupsToExclude"],
                    consumer_groups_to_replicate=["consumerGroupsToReplicate"],
                    detect_and_copy_new_consumer_groups=False,
                    synchronise_consumer_group_offsets=False
                ),
                source_kafka_cluster_arn="sourceKafkaClusterArn",
                target_compression_type="targetCompressionType",
                target_kafka_cluster_arn="targetKafkaClusterArn",
                topic_replication=msk_mixins.CfnReplicatorPropsMixin.TopicReplicationProperty(
                    copy_access_control_lists_for_topics=False,
                    copy_topic_configurations=False,
                    detect_and_copy_new_topics=False,
                    starting_position=msk_mixins.CfnReplicatorPropsMixin.ReplicationStartingPositionProperty(
                        type="type"
                    ),
                    topic_name_configuration=msk_mixins.CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty(
                        type="type"
                    ),
                    topics_to_exclude=["topicsToExclude"],
                    topics_to_replicate=["topicsToReplicate"]
                )
            )],
            replicator_name="replicatorName",
            service_execution_role_arn="serviceExecutionRoleArn",
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
        props: typing.Union[CfnReplicatorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MSK::Replicator``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aac4c8062ff523e649e7f78fae2e10d01cc73b6ddbb4c83baddc7c819e24954)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ae68ad892efb47115870b56e52ce70de37b01a1891db3b5dde03d09fa068093)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac34e13cb18c088589f4f56eeaef4035f6e3949cec3a7c3b7174e27366e52d8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicatorMixinProps:
        return typing.cast(CfnReplicatorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.AmazonMskClusterProperty",
        jsii_struct_bases=[],
        name_mapping={"msk_cluster_arn": "mskClusterArn"},
    )
    class AmazonMskClusterProperty:
        def __init__(
            self,
            *,
            msk_cluster_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details of an Amazon MSK Cluster.

            :param msk_cluster_arn: The Amazon Resource Name (ARN) of an Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-amazonmskcluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                amazon_msk_cluster_property = msk_mixins.CfnReplicatorPropsMixin.AmazonMskClusterProperty(
                    msk_cluster_arn="mskClusterArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95ec19edb1b8794d84cc2657d8f9af2d914516539b146c3bb939985ec6c05dc8)
                check_type(argname="argument msk_cluster_arn", value=msk_cluster_arn, expected_type=type_hints["msk_cluster_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if msk_cluster_arn is not None:
                self._values["msk_cluster_arn"] = msk_cluster_arn

        @builtins.property
        def msk_cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon MSK cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-amazonmskcluster.html#cfn-msk-replicator-amazonmskcluster-mskclusterarn
            '''
            result = self._values.get("msk_cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AmazonMskClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "consumer_groups_to_exclude": "consumerGroupsToExclude",
            "consumer_groups_to_replicate": "consumerGroupsToReplicate",
            "detect_and_copy_new_consumer_groups": "detectAndCopyNewConsumerGroups",
            "synchronise_consumer_group_offsets": "synchroniseConsumerGroupOffsets",
        },
    )
    class ConsumerGroupReplicationProperty:
        def __init__(
            self,
            *,
            consumer_groups_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            consumer_groups_to_replicate: typing.Optional[typing.Sequence[builtins.str]] = None,
            detect_and_copy_new_consumer_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            synchronise_consumer_group_offsets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details about consumer group replication.

            :param consumer_groups_to_exclude: List of regular expression patterns indicating the consumer groups that should not be replicated.
            :param consumer_groups_to_replicate: List of regular expression patterns indicating the consumer groups to copy.
            :param detect_and_copy_new_consumer_groups: Enables synchronization of consumer groups to target cluster.
            :param synchronise_consumer_group_offsets: Enables synchronization of consumer group offsets to target cluster. The translated offsets will be written to topic __consumer_offsets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-consumergroupreplication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                consumer_group_replication_property = msk_mixins.CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty(
                    consumer_groups_to_exclude=["consumerGroupsToExclude"],
                    consumer_groups_to_replicate=["consumerGroupsToReplicate"],
                    detect_and_copy_new_consumer_groups=False,
                    synchronise_consumer_group_offsets=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fd253d1ac0930f5041912257682a62121cdbb82ca50cd272ecd210ca503e3f0)
                check_type(argname="argument consumer_groups_to_exclude", value=consumer_groups_to_exclude, expected_type=type_hints["consumer_groups_to_exclude"])
                check_type(argname="argument consumer_groups_to_replicate", value=consumer_groups_to_replicate, expected_type=type_hints["consumer_groups_to_replicate"])
                check_type(argname="argument detect_and_copy_new_consumer_groups", value=detect_and_copy_new_consumer_groups, expected_type=type_hints["detect_and_copy_new_consumer_groups"])
                check_type(argname="argument synchronise_consumer_group_offsets", value=synchronise_consumer_group_offsets, expected_type=type_hints["synchronise_consumer_group_offsets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumer_groups_to_exclude is not None:
                self._values["consumer_groups_to_exclude"] = consumer_groups_to_exclude
            if consumer_groups_to_replicate is not None:
                self._values["consumer_groups_to_replicate"] = consumer_groups_to_replicate
            if detect_and_copy_new_consumer_groups is not None:
                self._values["detect_and_copy_new_consumer_groups"] = detect_and_copy_new_consumer_groups
            if synchronise_consumer_group_offsets is not None:
                self._values["synchronise_consumer_group_offsets"] = synchronise_consumer_group_offsets

        @builtins.property
        def consumer_groups_to_exclude(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''List of regular expression patterns indicating the consumer groups that should not be replicated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-consumergroupreplication.html#cfn-msk-replicator-consumergroupreplication-consumergroupstoexclude
            '''
            result = self._values.get("consumer_groups_to_exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def consumer_groups_to_replicate(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''List of regular expression patterns indicating the consumer groups to copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-consumergroupreplication.html#cfn-msk-replicator-consumergroupreplication-consumergroupstoreplicate
            '''
            result = self._values.get("consumer_groups_to_replicate")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def detect_and_copy_new_consumer_groups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables synchronization of consumer groups to target cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-consumergroupreplication.html#cfn-msk-replicator-consumergroupreplication-detectandcopynewconsumergroups
            '''
            result = self._values.get("detect_and_copy_new_consumer_groups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def synchronise_consumer_group_offsets(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables synchronization of consumer group offsets to target cluster.

            The translated offsets will be written to topic __consumer_offsets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-consumergroupreplication.html#cfn-msk-replicator-consumergroupreplication-synchroniseconsumergroupoffsets
            '''
            result = self._values.get("synchronise_consumer_group_offsets")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsumerGroupReplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class KafkaClusterClientVpcConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :param security_group_ids: The security groups to attach to the ENIs for the broker nodes.
            :param subnet_ids: The list of subnets in the client VPC to connect to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-kafkaclusterclientvpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                kafka_cluster_client_vpc_config_property = msk_mixins.CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb372f333acc0c5e098e55c2af58adfa41309c82e8b445542acef7b2aff2f6ce)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security groups to attach to the ENIs for the broker nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-kafkaclusterclientvpcconfig.html#cfn-msk-replicator-kafkaclusterclientvpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of subnets in the client VPC to connect to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-kafkaclusterclientvpcconfig.html#cfn-msk-replicator-kafkaclusterclientvpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterClientVpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.KafkaClusterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "amazon_msk_cluster": "amazonMskCluster",
            "vpc_config": "vpcConfig",
        },
    )
    class KafkaClusterProperty:
        def __init__(
            self,
            *,
            amazon_msk_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.AmazonMskClusterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about Kafka Cluster to be used as source / target for replication.

            :param amazon_msk_cluster: Details of an Amazon MSK Cluster.
            :param vpc_config: Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-kafkacluster.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                kafka_cluster_property = msk_mixins.CfnReplicatorPropsMixin.KafkaClusterProperty(
                    amazon_msk_cluster=msk_mixins.CfnReplicatorPropsMixin.AmazonMskClusterProperty(
                        msk_cluster_arn="mskClusterArn"
                    ),
                    vpc_config=msk_mixins.CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty(
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2160c05823ac9cf8876d5132db89a98a39e7f9b0f8359c86804ae3a751888b39)
                check_type(argname="argument amazon_msk_cluster", value=amazon_msk_cluster, expected_type=type_hints["amazon_msk_cluster"])
                check_type(argname="argument vpc_config", value=vpc_config, expected_type=type_hints["vpc_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if amazon_msk_cluster is not None:
                self._values["amazon_msk_cluster"] = amazon_msk_cluster
            if vpc_config is not None:
                self._values["vpc_config"] = vpc_config

        @builtins.property
        def amazon_msk_cluster(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.AmazonMskClusterProperty"]]:
            '''Details of an Amazon MSK Cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-kafkacluster.html#cfn-msk-replicator-kafkacluster-amazonmskcluster
            '''
            result = self._values.get("amazon_msk_cluster")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.AmazonMskClusterProperty"]], result)

        @builtins.property
        def vpc_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty"]]:
            '''Details of an Amazon VPC which has network connectivity to the Apache Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-kafkacluster.html#cfn-msk-replicator-kafkacluster-vpcconfig
            '''
            result = self._values.get("vpc_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KafkaClusterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.ReplicationInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "consumer_group_replication": "consumerGroupReplication",
            "source_kafka_cluster_arn": "sourceKafkaClusterArn",
            "target_compression_type": "targetCompressionType",
            "target_kafka_cluster_arn": "targetKafkaClusterArn",
            "topic_replication": "topicReplication",
        },
    )
    class ReplicationInfoProperty:
        def __init__(
            self,
            *,
            consumer_group_replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_kafka_cluster_arn: typing.Optional[builtins.str] = None,
            target_compression_type: typing.Optional[builtins.str] = None,
            target_kafka_cluster_arn: typing.Optional[builtins.str] = None,
            topic_replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.TopicReplicationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies configuration for replication between a source and target Kafka cluster.

            :param consumer_group_replication: Configuration relating to consumer group replication.
            :param source_kafka_cluster_arn: The ARN of the source Kafka cluster.
            :param target_compression_type: The compression type to use when producing records to target cluster.
            :param target_kafka_cluster_arn: The ARN of the target Kafka cluster.
            :param topic_replication: Configuration relating to topic replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                replication_info_property = msk_mixins.CfnReplicatorPropsMixin.ReplicationInfoProperty(
                    consumer_group_replication=msk_mixins.CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty(
                        consumer_groups_to_exclude=["consumerGroupsToExclude"],
                        consumer_groups_to_replicate=["consumerGroupsToReplicate"],
                        detect_and_copy_new_consumer_groups=False,
                        synchronise_consumer_group_offsets=False
                    ),
                    source_kafka_cluster_arn="sourceKafkaClusterArn",
                    target_compression_type="targetCompressionType",
                    target_kafka_cluster_arn="targetKafkaClusterArn",
                    topic_replication=msk_mixins.CfnReplicatorPropsMixin.TopicReplicationProperty(
                        copy_access_control_lists_for_topics=False,
                        copy_topic_configurations=False,
                        detect_and_copy_new_topics=False,
                        starting_position=msk_mixins.CfnReplicatorPropsMixin.ReplicationStartingPositionProperty(
                            type="type"
                        ),
                        topic_name_configuration=msk_mixins.CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty(
                            type="type"
                        ),
                        topics_to_exclude=["topicsToExclude"],
                        topics_to_replicate=["topicsToReplicate"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8eb7e3aab5bc466ad34dad437ffa159712a9df68212bf2ff2a51ccd8120b374)
                check_type(argname="argument consumer_group_replication", value=consumer_group_replication, expected_type=type_hints["consumer_group_replication"])
                check_type(argname="argument source_kafka_cluster_arn", value=source_kafka_cluster_arn, expected_type=type_hints["source_kafka_cluster_arn"])
                check_type(argname="argument target_compression_type", value=target_compression_type, expected_type=type_hints["target_compression_type"])
                check_type(argname="argument target_kafka_cluster_arn", value=target_kafka_cluster_arn, expected_type=type_hints["target_kafka_cluster_arn"])
                check_type(argname="argument topic_replication", value=topic_replication, expected_type=type_hints["topic_replication"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if consumer_group_replication is not None:
                self._values["consumer_group_replication"] = consumer_group_replication
            if source_kafka_cluster_arn is not None:
                self._values["source_kafka_cluster_arn"] = source_kafka_cluster_arn
            if target_compression_type is not None:
                self._values["target_compression_type"] = target_compression_type
            if target_kafka_cluster_arn is not None:
                self._values["target_kafka_cluster_arn"] = target_kafka_cluster_arn
            if topic_replication is not None:
                self._values["topic_replication"] = topic_replication

        @builtins.property
        def consumer_group_replication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty"]]:
            '''Configuration relating to consumer group replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationinfo.html#cfn-msk-replicator-replicationinfo-consumergroupreplication
            '''
            result = self._values.get("consumer_group_replication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty"]], result)

        @builtins.property
        def source_kafka_cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationinfo.html#cfn-msk-replicator-replicationinfo-sourcekafkaclusterarn
            '''
            result = self._values.get("source_kafka_cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_compression_type(self) -> typing.Optional[builtins.str]:
            '''The compression type to use when producing records to target cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationinfo.html#cfn-msk-replicator-replicationinfo-targetcompressiontype
            '''
            result = self._values.get("target_compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_kafka_cluster_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the target Kafka cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationinfo.html#cfn-msk-replicator-replicationinfo-targetkafkaclusterarn
            '''
            result = self._values.get("target_kafka_cluster_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_replication(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.TopicReplicationProperty"]]:
            '''Configuration relating to topic replication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationinfo.html#cfn-msk-replicator-replicationinfo-topicreplication
            '''
            result = self._values.get("topic_replication")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.TopicReplicationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.ReplicationStartingPositionProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ReplicationStartingPositionProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''Specifies the position in the topics to start replicating from.

            :param type: The type of replication starting position.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationstartingposition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                replication_starting_position_property = msk_mixins.CfnReplicatorPropsMixin.ReplicationStartingPositionProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51cf2fe95d8326a9749a416ece377ff7406bfba1b932d804b5ce3e7434bdd16c)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of replication starting position.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationstartingposition.html#cfn-msk-replicator-replicationstartingposition-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationStartingPositionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class ReplicationTopicNameConfigurationProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''Configuration for specifying replicated topic names will be the same as their corresponding upstream topics or prefixed with source cluster alias.

            :param type: The type of replication topic name configuration, identical to upstream topic name or prefixed with source cluster alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationtopicnameconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                replication_topic_name_configuration_property = msk_mixins.CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65c927c2dce9421a019ecc01b3c8d226c2000e7ecb9b80d268eef7baf96d9a01)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of replication topic name configuration, identical to upstream topic name or prefixed with source cluster alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-replicationtopicnameconfiguration.html#cfn-msk-replicator-replicationtopicnameconfiguration-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReplicationTopicNameConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnReplicatorPropsMixin.TopicReplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_access_control_lists_for_topics": "copyAccessControlListsForTopics",
            "copy_topic_configurations": "copyTopicConfigurations",
            "detect_and_copy_new_topics": "detectAndCopyNewTopics",
            "starting_position": "startingPosition",
            "topic_name_configuration": "topicNameConfiguration",
            "topics_to_exclude": "topicsToExclude",
            "topics_to_replicate": "topicsToReplicate",
        },
    )
    class TopicReplicationProperty:
        def __init__(
            self,
            *,
            copy_access_control_lists_for_topics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            copy_topic_configurations: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            detect_and_copy_new_topics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            starting_position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.ReplicationStartingPositionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            topic_name_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            topics_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
            topics_to_replicate: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Details about topic replication.

            :param copy_access_control_lists_for_topics: Whether to periodically configure remote topic ACLs to match their corresponding upstream topics.
            :param copy_topic_configurations: Whether to periodically configure remote topics to match their corresponding upstream topics.
            :param detect_and_copy_new_topics: Whether to periodically check for new topics and partitions.
            :param starting_position: Specifies the position in the topics to start replicating from.
            :param topic_name_configuration: Configuration for specifying replicated topic names will be the same as their corresponding upstream topics or prefixed with source cluster alias.
            :param topics_to_exclude: List of regular expression patterns indicating the topics that should not be replicated.
            :param topics_to_replicate: List of regular expression patterns indicating the topics to copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                topic_replication_property = msk_mixins.CfnReplicatorPropsMixin.TopicReplicationProperty(
                    copy_access_control_lists_for_topics=False,
                    copy_topic_configurations=False,
                    detect_and_copy_new_topics=False,
                    starting_position=msk_mixins.CfnReplicatorPropsMixin.ReplicationStartingPositionProperty(
                        type="type"
                    ),
                    topic_name_configuration=msk_mixins.CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty(
                        type="type"
                    ),
                    topics_to_exclude=["topicsToExclude"],
                    topics_to_replicate=["topicsToReplicate"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f71ebf20d492d2d318fec5e43dc4152128ea4d08fde4ee4a410d75e507c5dcf2)
                check_type(argname="argument copy_access_control_lists_for_topics", value=copy_access_control_lists_for_topics, expected_type=type_hints["copy_access_control_lists_for_topics"])
                check_type(argname="argument copy_topic_configurations", value=copy_topic_configurations, expected_type=type_hints["copy_topic_configurations"])
                check_type(argname="argument detect_and_copy_new_topics", value=detect_and_copy_new_topics, expected_type=type_hints["detect_and_copy_new_topics"])
                check_type(argname="argument starting_position", value=starting_position, expected_type=type_hints["starting_position"])
                check_type(argname="argument topic_name_configuration", value=topic_name_configuration, expected_type=type_hints["topic_name_configuration"])
                check_type(argname="argument topics_to_exclude", value=topics_to_exclude, expected_type=type_hints["topics_to_exclude"])
                check_type(argname="argument topics_to_replicate", value=topics_to_replicate, expected_type=type_hints["topics_to_replicate"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_access_control_lists_for_topics is not None:
                self._values["copy_access_control_lists_for_topics"] = copy_access_control_lists_for_topics
            if copy_topic_configurations is not None:
                self._values["copy_topic_configurations"] = copy_topic_configurations
            if detect_and_copy_new_topics is not None:
                self._values["detect_and_copy_new_topics"] = detect_and_copy_new_topics
            if starting_position is not None:
                self._values["starting_position"] = starting_position
            if topic_name_configuration is not None:
                self._values["topic_name_configuration"] = topic_name_configuration
            if topics_to_exclude is not None:
                self._values["topics_to_exclude"] = topics_to_exclude
            if topics_to_replicate is not None:
                self._values["topics_to_replicate"] = topics_to_replicate

        @builtins.property
        def copy_access_control_lists_for_topics(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to periodically configure remote topic ACLs to match their corresponding upstream topics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-copyaccesscontrollistsfortopics
            '''
            result = self._values.get("copy_access_control_lists_for_topics")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def copy_topic_configurations(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to periodically configure remote topics to match their corresponding upstream topics.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-copytopicconfigurations
            '''
            result = self._values.get("copy_topic_configurations")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def detect_and_copy_new_topics(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether to periodically check for new topics and partitions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-detectandcopynewtopics
            '''
            result = self._values.get("detect_and_copy_new_topics")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def starting_position(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ReplicationStartingPositionProperty"]]:
            '''Specifies the position in the topics to start replicating from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-startingposition
            '''
            result = self._values.get("starting_position")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ReplicationStartingPositionProperty"]], result)

        @builtins.property
        def topic_name_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty"]]:
            '''Configuration for specifying replicated topic names will be the same as their corresponding upstream topics or prefixed with source cluster alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-topicnameconfiguration
            '''
            result = self._values.get("topic_name_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty"]], result)

        @builtins.property
        def topics_to_exclude(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of regular expression patterns indicating the topics that should not be replicated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-topicstoexclude
            '''
            result = self._values.get("topics_to_exclude")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def topics_to_replicate(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of regular expression patterns indicating the topics to copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-replicator-topicreplication.html#cfn-msk-replicator-topicreplication-topicstoreplicate
            '''
            result = self._values.get("topics_to_replicate")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicReplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnServerlessClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_authentication": "clientAuthentication",
        "cluster_name": "clusterName",
        "tags": "tags",
        "vpc_configs": "vpcConfigs",
    },
)
class CfnServerlessClusterMixinProps:
    def __init__(
        self,
        *,
        client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessClusterPropsMixin.ClientAuthenticationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessClusterPropsMixin.VpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnServerlessClusterPropsMixin.

        :param client_authentication: Includes all client authentication related information.
        :param cluster_name: The name of the cluster.
        :param tags: An arbitrary set of tags (key-value pairs) for the cluster.
        :param vpc_configs: VPC configuration information for the serverless cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-serverlesscluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            cfn_serverless_cluster_mixin_props = msk_mixins.CfnServerlessClusterMixinProps(
                client_authentication=msk_mixins.CfnServerlessClusterPropsMixin.ClientAuthenticationProperty(
                    sasl=msk_mixins.CfnServerlessClusterPropsMixin.SaslProperty(
                        iam=msk_mixins.CfnServerlessClusterPropsMixin.IamProperty(
                            enabled=False
                        )
                    )
                ),
                cluster_name="clusterName",
                tags={
                    "tags_key": "tags"
                },
                vpc_configs=[msk_mixins.CfnServerlessClusterPropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnet_ids=["subnetIds"]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041c440d4636e27a215c3e2dd8d8dd37b7d9dcb20a556e9cb17cbb8f17bf8118)
            check_type(argname="argument client_authentication", value=client_authentication, expected_type=type_hints["client_authentication"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_configs", value=vpc_configs, expected_type=type_hints["vpc_configs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_authentication is not None:
            self._values["client_authentication"] = client_authentication
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if tags is not None:
            self._values["tags"] = tags
        if vpc_configs is not None:
            self._values["vpc_configs"] = vpc_configs

    @builtins.property
    def client_authentication(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.ClientAuthenticationProperty"]]:
        '''Includes all client authentication related information.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-serverlesscluster.html#cfn-msk-serverlesscluster-clientauthentication
        '''
        result = self._values.get("client_authentication")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.ClientAuthenticationProperty"]], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-serverlesscluster.html#cfn-msk-serverlesscluster-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An arbitrary set of tags (key-value pairs) for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-serverlesscluster.html#cfn-msk-serverlesscluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.VpcConfigProperty"]]]]:
        '''VPC configuration information for the serverless cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-serverlesscluster.html#cfn-msk-serverlesscluster-vpcconfigs
        '''
        result = self._values.get("vpc_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.VpcConfigProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerlessClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServerlessClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnServerlessClusterPropsMixin",
):
    '''Specifies the properties required for creating a serverless cluster.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-serverlesscluster.html
    :cloudformationResource: AWS::MSK::ServerlessCluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_serverless_cluster_props_mixin = msk_mixins.CfnServerlessClusterPropsMixin(msk_mixins.CfnServerlessClusterMixinProps(
            client_authentication=msk_mixins.CfnServerlessClusterPropsMixin.ClientAuthenticationProperty(
                sasl=msk_mixins.CfnServerlessClusterPropsMixin.SaslProperty(
                    iam=msk_mixins.CfnServerlessClusterPropsMixin.IamProperty(
                        enabled=False
                    )
                )
            ),
            cluster_name="clusterName",
            tags={
                "tags_key": "tags"
            },
            vpc_configs=[msk_mixins.CfnServerlessClusterPropsMixin.VpcConfigProperty(
                security_groups=["securityGroups"],
                subnet_ids=["subnetIds"]
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServerlessClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MSK::ServerlessCluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4304df7015a709e04403b09643307190af4dd6080e426056bec2609689047e77)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36c259e7abb1145f9cbfd844281db4a92cc3923bbe831ffe2e5d9a9767927b6a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__becb4ce8b2a52524ff7925c36c090a346763e651b8350db9413b36560a684b7d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServerlessClusterMixinProps:
        return typing.cast(CfnServerlessClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnServerlessClusterPropsMixin.ClientAuthenticationProperty",
        jsii_struct_bases=[],
        name_mapping={"sasl": "sasl"},
    )
    class ClientAuthenticationProperty:
        def __init__(
            self,
            *,
            sasl: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessClusterPropsMixin.SaslProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Includes all client authentication information.

            :param sasl: Details for client authentication using SASL. To turn on SASL, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true. You must set ``clientBroker`` to either ``TLS`` or ``TLS_PLAINTEXT`` . If you choose ``TLS_PLAINTEXT`` , then you must also set ``unauthenticated`` to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-clientauthentication.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                client_authentication_property = msk_mixins.CfnServerlessClusterPropsMixin.ClientAuthenticationProperty(
                    sasl=msk_mixins.CfnServerlessClusterPropsMixin.SaslProperty(
                        iam=msk_mixins.CfnServerlessClusterPropsMixin.IamProperty(
                            enabled=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__833c64cad1b6b31fb965d25161829fb50f4b4b72449e00e959b9217cfc91eddd)
                check_type(argname="argument sasl", value=sasl, expected_type=type_hints["sasl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sasl is not None:
                self._values["sasl"] = sasl

        @builtins.property
        def sasl(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.SaslProperty"]]:
            '''Details for client authentication using SASL.

            To turn on SASL, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true. You must set ``clientBroker`` to either ``TLS`` or ``TLS_PLAINTEXT`` . If you choose ``TLS_PLAINTEXT`` , then you must also set ``unauthenticated`` to true.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-clientauthentication.html#cfn-msk-serverlesscluster-clientauthentication-sasl
            '''
            result = self._values.get("sasl")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.SaslProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientAuthenticationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnServerlessClusterPropsMixin.IamProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class IamProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Details for SASL/IAM client authentication.

            :param enabled: SASL/IAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-iam.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                iam_property = msk_mixins.CfnServerlessClusterPropsMixin.IamProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90ffc954cae4e3c0c844099b0383bf3978651d67d3fd16f1f1f97b6ad6d0040f)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''SASL/IAM authentication is enabled or not.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-iam.html#cfn-msk-serverlesscluster-iam-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnServerlessClusterPropsMixin.SaslProperty",
        jsii_struct_bases=[],
        name_mapping={"iam": "iam"},
    )
    class SaslProperty:
        def __init__(
            self,
            *,
            iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerlessClusterPropsMixin.IamProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details for client authentication using SASL.

            To turn on SASL, you must also turn on ``EncryptionInTransit`` by setting ``inCluster`` to true. You must set ``clientBroker`` to either ``TLS`` or ``TLS_PLAINTEXT`` . If you choose ``TLS_PLAINTEXT`` , then you must also set ``unauthenticated`` to true.

            :param iam: Details for ClientAuthentication using IAM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-sasl.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                sasl_property = msk_mixins.CfnServerlessClusterPropsMixin.SaslProperty(
                    iam=msk_mixins.CfnServerlessClusterPropsMixin.IamProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__903785bc9bafb306f5a9bc4c9b7813e4d77fc6cc4e9176cf7d751bd5ba84d33e)
                check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam is not None:
                self._values["iam"] = iam

        @builtins.property
        def iam(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.IamProperty"]]:
            '''Details for ClientAuthentication using IAM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-sasl.html#cfn-msk-serverlesscluster-sasl-iam
            '''
            result = self._values.get("iam")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerlessClusterPropsMixin.IamProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SaslProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnServerlessClusterPropsMixin.VpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"security_groups": "securityGroups", "subnet_ids": "subnetIds"},
    )
    class VpcConfigProperty:
        def __init__(
            self,
            *,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param security_groups: 
            :param subnet_ids: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-vpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
                
                vpc_config_property = msk_mixins.CfnServerlessClusterPropsMixin.VpcConfigProperty(
                    security_groups=["securityGroups"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd40eab6deed2cc9f0da0d32f8b7631cf40d6f03efc9b02fad0a0ce2f80b7bef)
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-vpcconfig.html#cfn-msk-serverlesscluster-vpcconfig-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-msk-serverlesscluster-vpcconfig.html#cfn-msk-serverlesscluster-vpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnVpcConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "authentication": "authentication",
        "client_subnets": "clientSubnets",
        "security_groups": "securityGroups",
        "tags": "tags",
        "target_cluster_arn": "targetClusterArn",
        "vpc_id": "vpcId",
    },
)
class CfnVpcConnectionMixinProps:
    def __init__(
        self,
        *,
        authentication: typing.Optional[builtins.str] = None,
        client_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_cluster_arn: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVpcConnectionPropsMixin.

        :param authentication: The type of private link authentication.
        :param client_subnets: The list of subnets in the client VPC to connect to.
        :param security_groups: The security groups to attach to the ENIs for the broker nodes.
        :param tags: An arbitrary set of tags (key-value pairs) you specify while creating the VPC connection.
        :param target_cluster_arn: The Amazon Resource Name (ARN) of the cluster.
        :param vpc_id: The VPC ID of the remote client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
            
            cfn_vpc_connection_mixin_props = msk_mixins.CfnVpcConnectionMixinProps(
                authentication="authentication",
                client_subnets=["clientSubnets"],
                security_groups=["securityGroups"],
                tags={
                    "tags_key": "tags"
                },
                target_cluster_arn="targetClusterArn",
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e718463797be065e26e918063dc9d4442d88691bcbdcb1c476a205fb307041ae)
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument client_subnets", value=client_subnets, expected_type=type_hints["client_subnets"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_cluster_arn", value=target_cluster_arn, expected_type=type_hints["target_cluster_arn"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication is not None:
            self._values["authentication"] = authentication
        if client_subnets is not None:
            self._values["client_subnets"] = client_subnets
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if target_cluster_arn is not None:
            self._values["target_cluster_arn"] = target_cluster_arn
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def authentication(self) -> typing.Optional[builtins.str]:
        '''The type of private link authentication.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html#cfn-msk-vpcconnection-authentication
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of subnets in the client VPC to connect to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html#cfn-msk-vpcconnection-clientsubnets
        '''
        result = self._values.get("client_subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The security groups to attach to the ENIs for the broker nodes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html#cfn-msk-vpcconnection-securitygroups
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An arbitrary set of tags (key-value pairs) you specify while creating the VPC connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html#cfn-msk-vpcconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_cluster_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html#cfn-msk-vpcconnection-targetclusterarn
        '''
        result = self._values.get("target_cluster_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''The VPC ID of the remote client.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html#cfn-msk-vpcconnection-vpcid
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_msk.mixins.CfnVpcConnectionPropsMixin",
):
    '''Create remote VPC connection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-msk-vpcconnection.html
    :cloudformationResource: AWS::MSK::VpcConnection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_msk import mixins as msk_mixins
        
        cfn_vpc_connection_props_mixin = msk_mixins.CfnVpcConnectionPropsMixin(msk_mixins.CfnVpcConnectionMixinProps(
            authentication="authentication",
            client_subnets=["clientSubnets"],
            security_groups=["securityGroups"],
            tags={
                "tags_key": "tags"
            },
            target_cluster_arn="targetClusterArn",
            vpc_id="vpcId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVpcConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MSK::VpcConnection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9691e2e1a73842fbb526063f22b45864a8ba73c327a29bd7cbdc88b3897c650)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11dca44d2ad2ba874f6872427dd645e5b082e76dd2b52c514b1cd99e8c364c5d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__533846e772506494206ae462299700731d378ad71c9b7fc35b566a8e44ed967c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcConnectionMixinProps:
        return typing.cast(CfnVpcConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnBatchScramSecretMixinProps",
    "CfnBatchScramSecretPropsMixin",
    "CfnClusterBrokerLogs",
    "CfnClusterLogsMixin",
    "CfnClusterMixinProps",
    "CfnClusterPolicyMixinProps",
    "CfnClusterPolicyPropsMixin",
    "CfnClusterPropsMixin",
    "CfnConfigurationMixinProps",
    "CfnConfigurationPropsMixin",
    "CfnReplicatorMixinProps",
    "CfnReplicatorPropsMixin",
    "CfnServerlessClusterMixinProps",
    "CfnServerlessClusterPropsMixin",
    "CfnVpcConnectionMixinProps",
    "CfnVpcConnectionPropsMixin",
]

publication.publish()

def _typecheckingstub__0b9c1c4094867258cb92c7fe7d7db58ead70886e6c077d2b3ddf1b0f34d282f1(
    *,
    cluster_arn: typing.Optional[builtins.str] = None,
    secret_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4a54e31319ea0222e266e24d3375b7eb04ea6d4ea1814777a27ebe3a0668be6(
    props: typing.Union[CfnBatchScramSecretMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f482e8c3ab39b7ba79adc87096b3b217deacbbb6a68d50c88817eacbe09ddb7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e964675b913fcbacda566496b97447f923226f0459fd1101a156342f69aabbce(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0d0196f5e1b6085f13aa7add4b61e98c7263880649d308845844c68ea73a09b(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9e66f8848f874d92a0a11a214079ebdc2afdce8ed8e0faaa82107feea8a470(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8ead99a56d8e1f5e0445250b71c7b6a3a76358b7df256e3ed9741f095eda6d(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e01f7b8be2507fdc2823cf5853912165511bfa960c4b8f6ed93b75a3ff740f72(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7831fbc241cdebf05f30b34b379fc2c976a8ec5ab5e5b212b2527dda64918758(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244c28a448fa4ff847baca8b4ced3099fdebf2d6c9e2f65731e2fa4ba306563a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a18d8070d499ae07dd95e173de27914339d7e4678479a62025e5fd9e611e0ec(
    *,
    broker_node_group_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.BrokerNodeGroupInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    configuration_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ConfigurationInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    current_version: typing.Optional[builtins.str] = None,
    encryption_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EncryptionInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enhanced_monitoring: typing.Optional[builtins.str] = None,
    kafka_version: typing.Optional[builtins.str] = None,
    logging_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.LoggingInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    number_of_broker_nodes: typing.Optional[jsii.Number] = None,
    open_monitoring: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.OpenMonitoringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rebalancing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.RebalancingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcb10a9c280132894606670c091f342edc58469b31bbcae5bdebf1ec70ee2a6(
    *,
    cluster_arn: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11388492a4ed143d083b6034f2ded1270f608a8b5dc2655127fc0d9c6da80a89(
    props: typing.Union[CfnClusterPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65c450fc5a1592068372da35e39a6aed8b6296448bc74db187b4a4de951e532(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f138bb95daab7e5d62b4314bd496b2cd694aea69b92074b3578fea400c767833(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89fa5b44b5604772a70709a2678556ef79c1d5034167488e0740e288ab696af8(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042c107c60ed230ed2ac1af2c9a7818bda427817f2420a767b926c0b1717cf89(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0dd809cc395196a795888e8a68d69e9fc9a0d95490b06cacb1981161f1b8ea1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99fabf641d0b75c4951659227281826b268461b10911b61433bf4700278d1fc5(
    *,
    cloud_watch_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.CloudWatchLogsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.FirehoseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.S3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b395b2931e590500cc9269112a1ee884c5ccf15df7a0040d8907167455486c(
    *,
    broker_az_distribution: typing.Optional[builtins.str] = None,
    client_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    connectivity_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ConnectivityInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.StorageInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b073c3781a2352f12bfd438ccb236d58156044003eccbd82aeaf2c775e5510e7(
    *,
    sasl: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SaslProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.TlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    unauthenticated: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.UnauthenticatedProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cdfdd2e8c4843cfd05c10b04f8dc48762d5b18adc170f653c02482ae0e59d4(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    log_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea285c1e35997aca39a30ff414e1017fca3c699cd71ea68312215a82eda10cb9(
    *,
    arn: typing.Optional[builtins.str] = None,
    revision: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d25998fd59a3e4db5f44062648f83a062ac916ad186828a946adfc61696da26(
    *,
    public_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.PublicAccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_connectivity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VpcConnectivityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e610a184dc671a0f8f3dece730eec00f1b4e513dc736a4860d2b266bd375cafc(
    *,
    provisioned_throughput: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ProvisionedThroughputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fff6cb8cb2dcfe4f58c277712aa26bdc011c986a2bba971c418dbd9a7ba64c4(
    *,
    data_volume_kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31e7381ca963e62bf161c2b669ab68c19a815c2fb6bafb73d9ccaf585ebaa4ea(
    *,
    client_broker: typing.Optional[builtins.str] = None,
    in_cluster: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d9f94ae9254e09e879588e0dc35f8c879e6e6e8eb18e682318ce0ea7446bb2(
    *,
    encryption_at_rest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EncryptionAtRestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption_in_transit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EncryptionInTransitProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f10605804c1447706f3f3d87f03d9693009073ab40af3ecac00754ef6709c4(
    *,
    delivery_stream: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77dadf6a70d734cc0f2a2aace9bd5d763dd9165740e63e8e2a1975f5b04e3d2c(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd03d4217e8aed3d069df4a3a662713f638998532efa7a7575aa939b41df179(
    *,
    enabled_in_broker: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2650c466d52c0e685b2616a240e17ec78d958f8f8a5754e4a7426fc7582182(
    *,
    broker_logs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.BrokerLogsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337606c7e198f51b7a7fb53a4dd88f905aa7511112eef88d3a4c621b92535108(
    *,
    enabled_in_broker: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df05b95f25f523959ad0ccda74a67613a4f31caaf78f266fb4d88b054ec3eaa(
    *,
    prometheus: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.PrometheusProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd7223f8b8e51d45f6f9bbeb9e8f1bdf34b0c15ed3524513a0142890b00808ca(
    *,
    jmx_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.JmxExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    node_exporter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.NodeExporterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3382a5226baa81f23f60d39625eb18caef2f334c9276ae1c95b09fbf026c7128(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    volume_throughput: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27edfdf964bea0b29c632401c8a058fb3339a3ac5d8aab66efb5ba5fb0af26ff(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359ce1419d958f4b0c875714d3b04522a5245257061b4429f14277ba9b208c7a(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd62805d8b77137915562f5cff7948dca6986b3db7637193fa22433d03e90f38(
    *,
    bucket: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d86dbd9b5445111d1717934ff350a9dab92103936955b52b55d595bdedf36bf(
    *,
    iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.IamProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scram: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ScramProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8fcbdfa7f8267fa44d181ba27e8387bce546e43452c0554c850fafa52dc4c0(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ba410e71611a28c31d3d99aee5f80d592d813fe0b4e79e23e5841a4f28c2b1(
    *,
    ebs_storage_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EBSStorageInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420097dbe358b66067925f982f42877df2958e538bff966a4c6501a7c95bff55(
    *,
    certificate_authority_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f2409abc68c52d982f75baa40cfdab4fbb4b289fb15d8c8fd74a38b8aead7f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508a81b64a2cb9a407be54f1c257a40fe23d37612156d292242424b33edb770d(
    *,
    sasl: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VpcConnectivitySaslProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VpcConnectivityTlsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c4b210c49b092c1dc328ca1fa398fd34f247e00b60e8cb057abaef23ef9fc0(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a814713cb9d3d580e69ac9a4cfdef0fad55e82eb2aef115273e111ddde7e58(
    *,
    client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VpcConnectivityClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7032805e8d923b77a845776df62972119fb10889d311da4be83345fa325a9d(
    *,
    iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VpcConnectivityIamProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scram: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.VpcConnectivityScramProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a37c16e63adb809eaa22ea09d28074aacfccf844734b20c3cf5ea9d83a2557(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1a87fb3d457d9df064a47597e0f529c244a012cb0e99d8d8570ea28d2fc433(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__309e186ba1333c2dfeb8257ffa2fa9622898a42eebe6e692ea5a9dd8da9321db(
    *,
    description: typing.Optional[builtins.str] = None,
    kafka_versions_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    latest_revision: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConfigurationPropsMixin.LatestRevisionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    server_properties: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89df9e38322e2db2a4596a4d0ab7f8557fb188a1dfae6b0ebd570ba8d8d4b583(
    props: typing.Union[CfnConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d984ac079bf6cb94b7139b33726a7405eb4b153a3f01f78e0a88589881e85a39(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439d0cf5cc83dd0aa96b0a956f2e38d83e3fe40bfc41951fef63728cc76f665b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b2b7f531189d93c16b8070b70a734accb17fcaab9cfc503e1797b1f42a7d45(
    *,
    creation_time: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    revision: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c218f31baa5e3a133c8e81420ac8bca409eb478262f9d5c99d08d65aeafa8c4(
    *,
    description: typing.Optional[builtins.str] = None,
    kafka_clusters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.KafkaClusterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    replication_info_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.ReplicationInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    replicator_name: typing.Optional[builtins.str] = None,
    service_execution_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aac4c8062ff523e649e7f78fae2e10d01cc73b6ddbb4c83baddc7c819e24954(
    props: typing.Union[CfnReplicatorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae68ad892efb47115870b56e52ce70de37b01a1891db3b5dde03d09fa068093(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac34e13cb18c088589f4f56eeaef4035f6e3949cec3a7c3b7174e27366e52d8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ec19edb1b8794d84cc2657d8f9af2d914516539b146c3bb939985ec6c05dc8(
    *,
    msk_cluster_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd253d1ac0930f5041912257682a62121cdbb82ca50cd272ecd210ca503e3f0(
    *,
    consumer_groups_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    consumer_groups_to_replicate: typing.Optional[typing.Sequence[builtins.str]] = None,
    detect_and_copy_new_consumer_groups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    synchronise_consumer_group_offsets: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb372f333acc0c5e098e55c2af58adfa41309c82e8b445542acef7b2aff2f6ce(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2160c05823ac9cf8876d5132db89a98a39e7f9b0f8359c86804ae3a751888b39(
    *,
    amazon_msk_cluster: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.AmazonMskClusterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.KafkaClusterClientVpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8eb7e3aab5bc466ad34dad437ffa159712a9df68212bf2ff2a51ccd8120b374(
    *,
    consumer_group_replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.ConsumerGroupReplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_kafka_cluster_arn: typing.Optional[builtins.str] = None,
    target_compression_type: typing.Optional[builtins.str] = None,
    target_kafka_cluster_arn: typing.Optional[builtins.str] = None,
    topic_replication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.TopicReplicationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cf2fe95d8326a9749a416ece377ff7406bfba1b932d804b5ce3e7434bdd16c(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65c927c2dce9421a019ecc01b3c8d226c2000e7ecb9b80d268eef7baf96d9a01(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71ebf20d492d2d318fec5e43dc4152128ea4d08fde4ee4a410d75e507c5dcf2(
    *,
    copy_access_control_lists_for_topics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    copy_topic_configurations: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    detect_and_copy_new_topics: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    starting_position: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.ReplicationStartingPositionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    topic_name_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnReplicatorPropsMixin.ReplicationTopicNameConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    topics_to_exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    topics_to_replicate: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041c440d4636e27a215c3e2dd8d8dd37b7d9dcb20a556e9cb17cbb8f17bf8118(
    *,
    client_authentication: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessClusterPropsMixin.ClientAuthenticationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessClusterPropsMixin.VpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4304df7015a709e04403b09643307190af4dd6080e426056bec2609689047e77(
    props: typing.Union[CfnServerlessClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c259e7abb1145f9cbfd844281db4a92cc3923bbe831ffe2e5d9a9767927b6a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__becb4ce8b2a52524ff7925c36c090a346763e651b8350db9413b36560a684b7d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__833c64cad1b6b31fb965d25161829fb50f4b4b72449e00e959b9217cfc91eddd(
    *,
    sasl: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessClusterPropsMixin.SaslProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ffc954cae4e3c0c844099b0383bf3978651d67d3fd16f1f1f97b6ad6d0040f(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903785bc9bafb306f5a9bc4c9b7813e4d77fc6cc4e9176cf7d751bd5ba84d33e(
    *,
    iam: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerlessClusterPropsMixin.IamProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd40eab6deed2cc9f0da0d32f8b7631cf40d6f03efc9b02fad0a0ce2f80b7bef(
    *,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e718463797be065e26e918063dc9d4442d88691bcbdcb1c476a205fb307041ae(
    *,
    authentication: typing.Optional[builtins.str] = None,
    client_subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_cluster_arn: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9691e2e1a73842fbb526063f22b45864a8ba73c327a29bd7cbdc88b3897c650(
    props: typing.Union[CfnVpcConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11dca44d2ad2ba874f6872427dd645e5b082e76dd2b52c514b1cd99e8c364c5d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__533846e772506494206ae462299700731d378ad71c9b7fc35b566a8e44ed967c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
