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


@jsii.implements(_IMixin_11e4b965)
class CfnClusterLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterLogsMixin",
):
    '''Creates an AWS PCS cluster resource.

    For more information, see `Creating a cluster in AWS Parallel Computing Service <https://docs.aws.amazon.com/pcs/latest/userguide/working-with_clusters_create.html>`_ in the *AWS PCS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html
    :cloudformationResource: AWS::PCS::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_cluster_logs_mixin = pcs_mixins.CfnClusterLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::PCS::Cluster``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__895989435c64ce6ac8ba60f4839b019a11c9756f2dddd9df13d89ee185120eaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62ba0f970aaa3a35b0eea8e1d967c5d7b947370f9db7a78ac98b9a262357c37a)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24685fe192db49a38fd71bcc95b607b3b231591f3ce0acb13d01583294d02ed)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PCS_JOBCOMP_LOGS")
    def PCS_JOBCOMP_LOGS(cls) -> "CfnClusterPcsJobcompLogs":
        return typing.cast("CfnClusterPcsJobcompLogs", jsii.sget(cls, "PCS_JOBCOMP_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PCS_SCHEDULER_LOGS")
    def PCS_SCHEDULER_LOGS(cls) -> "CfnClusterPcsSchedulerLogs":
        return typing.cast("CfnClusterPcsSchedulerLogs", jsii.sget(cls, "PCS_SCHEDULER_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "networking": "networking",
        "scheduler": "scheduler",
        "size": "size",
        "slurm_configuration": "slurmConfiguration",
        "tags": "tags",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        networking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.NetworkingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scheduler: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SchedulerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        size: typing.Optional[builtins.str] = None,
        slurm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SlurmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param name: The name that identifies the cluster.
        :param networking: The networking configuration for the cluster's control plane.
        :param scheduler: The cluster management and job scheduling software associated with the cluster.
        :param size: The size of the cluster. - ``SMALL`` : 32 compute nodes and 256 jobs - ``MEDIUM`` : 512 compute nodes and 8192 jobs - ``LARGE`` : 2048 compute nodes and 16,384 jobs
        :param slurm_configuration: Additional options related to the Slurm scheduler.
        :param tags: 1 or more tags added to the resource. Each tag consists of a tag key and tag value. The tag value is optional and can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
            
            cfn_cluster_mixin_props = pcs_mixins.CfnClusterMixinProps(
                name="name",
                networking=pcs_mixins.CfnClusterPropsMixin.NetworkingProperty(
                    network_type="networkType",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                ),
                scheduler=pcs_mixins.CfnClusterPropsMixin.SchedulerProperty(
                    type="type",
                    version="version"
                ),
                size="size",
                slurm_configuration=pcs_mixins.CfnClusterPropsMixin.SlurmConfigurationProperty(
                    accounting=pcs_mixins.CfnClusterPropsMixin.AccountingProperty(
                        default_purge_time_in_days=123,
                        mode="mode"
                    ),
                    auth_key=pcs_mixins.CfnClusterPropsMixin.AuthKeyProperty(
                        secret_arn="secretArn",
                        secret_version="secretVersion"
                    ),
                    jwt_auth=pcs_mixins.CfnClusterPropsMixin.JwtAuthProperty(
                        jwt_key=pcs_mixins.CfnClusterPropsMixin.JwtKeyProperty(
                            secret_arn="secretArn",
                            secret_version="secretVersion"
                        )
                    ),
                    scale_down_idle_time_in_seconds=123,
                    slurm_custom_settings=[pcs_mixins.CfnClusterPropsMixin.SlurmCustomSettingProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )],
                    slurm_rest=pcs_mixins.CfnClusterPropsMixin.SlurmRestProperty(
                        mode="mode"
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22d069e354fe429fa37d463bcd8808306a156c7550c35f5a2b5b14547590a8b4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument networking", value=networking, expected_type=type_hints["networking"])
            check_type(argname="argument scheduler", value=scheduler, expected_type=type_hints["scheduler"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument slurm_configuration", value=slurm_configuration, expected_type=type_hints["slurm_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if networking is not None:
            self._values["networking"] = networking
        if scheduler is not None:
            self._values["scheduler"] = scheduler
        if size is not None:
            self._values["size"] = size
        if slurm_configuration is not None:
            self._values["slurm_configuration"] = slurm_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that identifies the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html#cfn-pcs-cluster-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def networking(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.NetworkingProperty"]]:
        '''The networking configuration for the cluster's control plane.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html#cfn-pcs-cluster-networking
        '''
        result = self._values.get("networking")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.NetworkingProperty"]], result)

    @builtins.property
    def scheduler(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SchedulerProperty"]]:
        '''The cluster management and job scheduling software associated with the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html#cfn-pcs-cluster-scheduler
        '''
        result = self._values.get("scheduler")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SchedulerProperty"]], result)

    @builtins.property
    def size(self) -> typing.Optional[builtins.str]:
        '''The size of the cluster.

        - ``SMALL`` : 32 compute nodes and 256 jobs
        - ``MEDIUM`` : 512 compute nodes and 8192 jobs
        - ``LARGE`` : 2048 compute nodes and 16,384 jobs

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html#cfn-pcs-cluster-size
        '''
        result = self._values.get("size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slurm_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SlurmConfigurationProperty"]]:
        '''Additional options related to the Slurm scheduler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html#cfn-pcs-cluster-slurmconfiguration
        '''
        result = self._values.get("slurm_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SlurmConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''1 or more tags added to the resource.

        Each tag consists of a tag key and tag value. The tag value is optional and can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html#cfn-pcs-cluster-tags
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


class CfnClusterPcsJobcompLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPcsJobcompLogs",
):
    '''Builder for CfnClusterLogsMixin to generate PCS_JOBCOMP_LOGS for CfnCluster.

    :cloudformationResource: AWS::PCS::Cluster
    :logType: PCS_JOBCOMP_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
        
        cfn_cluster_pcs_jobcomp_logs = pcs_mixins.CfnClusterPcsJobcompLogs()
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
    ) -> CfnClusterLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d3301a1e1650a5371b00fb7e336a84bbe09309bc87a173df1c8f487f161a15)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnClusterLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnClusterLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e5fb6e94f05b3033e409179570a4b40f31ff4939491f63243173c259e4adbd0)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnClusterLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnClusterLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00425dadad64c8a5d02f7361b03fb17f41cd92801e4ce5909e6a4d1a83cf667)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnClusterLogsMixin, jsii.invoke(self, "toS3", [bucket]))


class CfnClusterPcsSchedulerLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPcsSchedulerLogs",
):
    '''Builder for CfnClusterLogsMixin to generate PCS_SCHEDULER_LOGS for CfnCluster.

    :cloudformationResource: AWS::PCS::Cluster
    :logType: PCS_SCHEDULER_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
        
        cfn_cluster_pcs_scheduler_logs = pcs_mixins.CfnClusterPcsSchedulerLogs()
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
    ) -> CfnClusterLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbddd3f16d07d0b43d9bf79954fc54f49c77f115eec373bcb16bf9dd63effc1a)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnClusterLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnClusterLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f90c69aa8ef08fdb6d52d6de2cbd70db375fe9d1610fa3b7d867a296f95edab0)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnClusterLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnClusterLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1da1c528da59bd7d286c57a9e7b1f29d79e506bb7c1c1987592b5db36e9aeef)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnClusterLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin",
):
    '''Creates an AWS PCS cluster resource.

    For more information, see `Creating a cluster in AWS Parallel Computing Service <https://docs.aws.amazon.com/pcs/latest/userguide/working-with_clusters_create.html>`_ in the *AWS PCS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-cluster.html
    :cloudformationResource: AWS::PCS::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
        
        cfn_cluster_props_mixin = pcs_mixins.CfnClusterPropsMixin(pcs_mixins.CfnClusterMixinProps(
            name="name",
            networking=pcs_mixins.CfnClusterPropsMixin.NetworkingProperty(
                network_type="networkType",
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            ),
            scheduler=pcs_mixins.CfnClusterPropsMixin.SchedulerProperty(
                type="type",
                version="version"
            ),
            size="size",
            slurm_configuration=pcs_mixins.CfnClusterPropsMixin.SlurmConfigurationProperty(
                accounting=pcs_mixins.CfnClusterPropsMixin.AccountingProperty(
                    default_purge_time_in_days=123,
                    mode="mode"
                ),
                auth_key=pcs_mixins.CfnClusterPropsMixin.AuthKeyProperty(
                    secret_arn="secretArn",
                    secret_version="secretVersion"
                ),
                jwt_auth=pcs_mixins.CfnClusterPropsMixin.JwtAuthProperty(
                    jwt_key=pcs_mixins.CfnClusterPropsMixin.JwtKeyProperty(
                        secret_arn="secretArn",
                        secret_version="secretVersion"
                    )
                ),
                scale_down_idle_time_in_seconds=123,
                slurm_custom_settings=[pcs_mixins.CfnClusterPropsMixin.SlurmCustomSettingProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )],
                slurm_rest=pcs_mixins.CfnClusterPropsMixin.SlurmRestProperty(
                    mode="mode"
                )
            ),
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
        '''Create a mixin to apply properties to ``AWS::PCS::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4455d37bdb4866de78c480231e6886cc9b46f0fe8547b09f422c0be6877700a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3948bbd24aed3e0a1e2d93a8f6854b85bdcb3616f31fb161908e95ad786d5667)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce31bf49b7932c949ea341382cee17ad8d7988d66aec2db23d52cddc3e65154f)
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
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.AccountingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_purge_time_in_days": "defaultPurgeTimeInDays",
            "mode": "mode",
        },
    )
    class AccountingProperty:
        def __init__(
            self,
            *,
            default_purge_time_in_days: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The accounting configuration includes configurable settings for Slurm accounting.

            :param default_purge_time_in_days: The default value for all purge settings for ``slurmdbd.conf`` . For more information, see the `slurmdbd.conf documentation at SchedMD <https://docs.aws.amazon.com/https://slurm.schedmd.com/slurmdbd.conf.html>`_ . The default value for ``defaultPurgeTimeInDays`` is ``-1`` . A value of ``-1`` means there is no purge time and records persist as long as the cluster exists. .. epigraph:: ``0`` isn't a valid value. Default: - -1
            :param mode: The default value for ``mode`` is ``STANDARD`` . A value of ``STANDARD`` means Slurm accounting is enabled. Default: - "NONE"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-accounting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                accounting_property = pcs_mixins.CfnClusterPropsMixin.AccountingProperty(
                    default_purge_time_in_days=123,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18eb5eaa67dffbf69d952ce72164b34ac43447e29b64173d871070dd7b5b0e08)
                check_type(argname="argument default_purge_time_in_days", value=default_purge_time_in_days, expected_type=type_hints["default_purge_time_in_days"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_purge_time_in_days is not None:
                self._values["default_purge_time_in_days"] = default_purge_time_in_days
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def default_purge_time_in_days(self) -> typing.Optional[jsii.Number]:
            '''The default value for all purge settings for ``slurmdbd.conf`` . For more information, see the `slurmdbd.conf documentation at SchedMD <https://docs.aws.amazon.com/https://slurm.schedmd.com/slurmdbd.conf.html>`_ .

            The default value for ``defaultPurgeTimeInDays`` is ``-1`` .

            A value of ``-1`` means there is no purge time and records persist as long as the cluster exists.
            .. epigraph::

               ``0`` isn't a valid value.

            :default: - -1

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-accounting.html#cfn-pcs-cluster-accounting-defaultpurgetimeindays
            '''
            result = self._values.get("default_purge_time_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The default value for ``mode`` is ``STANDARD`` .

            A value of ``STANDARD`` means Slurm accounting is enabled.

            :default: - "NONE"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-accounting.html#cfn-pcs-cluster-accounting-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccountingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.AuthKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn", "secret_version": "secretVersion"},
    )
    class AuthKeyProperty:
        def __init__(
            self,
            *,
            secret_arn: typing.Optional[builtins.str] = None,
            secret_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The shared Slurm key for authentication, also known as the *cluster secret* .

            :param secret_arn: The Amazon Resource Name (ARN) of the shared Slurm key.
            :param secret_version: The version of the shared Slurm key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-authkey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                auth_key_property = pcs_mixins.CfnClusterPropsMixin.AuthKeyProperty(
                    secret_arn="secretArn",
                    secret_version="secretVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__742fffcae4a116590669545796b524aee637a9bc5aea981596920da821bb3ff3)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if secret_version is not None:
                self._values["secret_version"] = secret_version

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the shared Slurm key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-authkey.html#cfn-pcs-cluster-authkey-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_version(self) -> typing.Optional[builtins.str]:
            '''The version of the shared Slurm key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-authkey.html#cfn-pcs-cluster-authkey-secretversion
            '''
            result = self._values.get("secret_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.EndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ipv6_address": "ipv6Address",
            "port": "port",
            "private_ip_address": "privateIpAddress",
            "public_ip_address": "publicIpAddress",
            "type": "type",
        },
    )
    class EndpointProperty:
        def __init__(
            self,
            *,
            ipv6_address: typing.Optional[builtins.str] = None,
            port: typing.Optional[builtins.str] = None,
            private_ip_address: typing.Optional[builtins.str] = None,
            public_ip_address: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An endpoint available for interaction with the scheduler.

            :param ipv6_address: The endpoint's IPv6 address. Example: ``2001:db8::1``
            :param port: The endpoint's connection port number. Example: ``1234``
            :param private_ip_address: For clusters that use IPv4, this is the endpoint's private IP address. Example: ``10.1.2.3`` For clusters configured to use IPv6, this is an empty string.
            :param public_ip_address: The endpoint's public IP address. Example: ``192.0.2.1``
            :param type: Indicates the type of endpoint running at the specific IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-endpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                endpoint_property = pcs_mixins.CfnClusterPropsMixin.EndpointProperty(
                    ipv6_address="ipv6Address",
                    port="port",
                    private_ip_address="privateIpAddress",
                    public_ip_address="publicIpAddress",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__944b6239ea34402ca9bb01b202495ec1f17c86232f3c24fe20e2ee81f06e925f)
                check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument private_ip_address", value=private_ip_address, expected_type=type_hints["private_ip_address"])
                check_type(argname="argument public_ip_address", value=public_ip_address, expected_type=type_hints["public_ip_address"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ipv6_address is not None:
                self._values["ipv6_address"] = ipv6_address
            if port is not None:
                self._values["port"] = port
            if private_ip_address is not None:
                self._values["private_ip_address"] = private_ip_address
            if public_ip_address is not None:
                self._values["public_ip_address"] = public_ip_address
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def ipv6_address(self) -> typing.Optional[builtins.str]:
            '''The endpoint's IPv6 address.

            Example: ``2001:db8::1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-endpoint.html#cfn-pcs-cluster-endpoint-ipv6address
            '''
            result = self._values.get("ipv6_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The endpoint's connection port number.

            Example: ``1234``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-endpoint.html#cfn-pcs-cluster-endpoint-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_ip_address(self) -> typing.Optional[builtins.str]:
            '''For clusters that use IPv4, this is the endpoint's private IP address.

            Example: ``10.1.2.3``

            For clusters configured to use IPv6, this is an empty string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-endpoint.html#cfn-pcs-cluster-endpoint-privateipaddress
            '''
            result = self._values.get("private_ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def public_ip_address(self) -> typing.Optional[builtins.str]:
            '''The endpoint's public IP address.

            Example: ``192.0.2.1``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-endpoint.html#cfn-pcs-cluster-endpoint-publicipaddress
            '''
            result = self._values.get("public_ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Indicates the type of endpoint running at the specific IP address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-endpoint.html#cfn-pcs-cluster-endpoint-type
            '''
            result = self._values.get("type")
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
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.ErrorInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorInfoProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An error that occurred during resource creation.

            :param code: The short-form error code.
            :param message: The detailed error information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-errorinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                error_info_property = pcs_mixins.CfnClusterPropsMixin.ErrorInfoProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b60893d5dec4eeb0634087a31c9f9c2802e40d0ab55cc3b29982c3a2dd0a7f66)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The short-form error code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-errorinfo.html#cfn-pcs-cluster-errorinfo-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The detailed error information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-errorinfo.html#cfn-pcs-cluster-errorinfo-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.JwtAuthProperty",
        jsii_struct_bases=[],
        name_mapping={"jwt_key": "jwtKey"},
    )
    class JwtAuthProperty:
        def __init__(
            self,
            *,
            jwt_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.JwtKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The JWT authentication configuration for Slurm REST API access.

            :param jwt_key: The JWT key for Slurm REST API authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-jwtauth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                jwt_auth_property = pcs_mixins.CfnClusterPropsMixin.JwtAuthProperty(
                    jwt_key=pcs_mixins.CfnClusterPropsMixin.JwtKeyProperty(
                        secret_arn="secretArn",
                        secret_version="secretVersion"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b33ccfedb299ee55239e88c1bd7a4b58f4343a35459717575dccc1d42f7d6c3e)
                check_type(argname="argument jwt_key", value=jwt_key, expected_type=type_hints["jwt_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if jwt_key is not None:
                self._values["jwt_key"] = jwt_key

        @builtins.property
        def jwt_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JwtKeyProperty"]]:
            '''The JWT key for Slurm REST API authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-jwtauth.html#cfn-pcs-cluster-jwtauth-jwtkey
            '''
            result = self._values.get("jwt_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JwtKeyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtAuthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.JwtKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_arn": "secretArn", "secret_version": "secretVersion"},
    )
    class JwtKeyProperty:
        def __init__(
            self,
            *,
            secret_arn: typing.Optional[builtins.str] = None,
            secret_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The JWT key stored in AWS Secrets Manager for Slurm REST API authentication.

            :param secret_arn: The Amazon Resource Name (ARN) of the AWS Secrets Manager secret containing the JWT key.
            :param secret_version: The version of the AWS Secrets Manager secret containing the JWT key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-jwtkey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                jwt_key_property = pcs_mixins.CfnClusterPropsMixin.JwtKeyProperty(
                    secret_arn="secretArn",
                    secret_version="secretVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7eb55121bd6b90e011eb8375c59bb19c9c3c91e6b05f11ed14d2a00e530108f)
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument secret_version", value=secret_version, expected_type=type_hints["secret_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if secret_version is not None:
                self._values["secret_version"] = secret_version

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager secret containing the JWT key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-jwtkey.html#cfn-pcs-cluster-jwtkey-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_version(self) -> typing.Optional[builtins.str]:
            '''The version of the AWS Secrets Manager secret containing the JWT key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-jwtkey.html#cfn-pcs-cluster-jwtkey-secretversion
            '''
            result = self._values.get("secret_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JwtKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.NetworkingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_type": "networkType",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class NetworkingProperty:
        def __init__(
            self,
            *,
            network_type: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The networking configuration for the cluster's control plane.

            :param network_type: The IP address version the cluster uses. The default is ``IPV4`` .
            :param security_group_ids: The list of security group IDs associated with the Elastic Network Interface (ENI) created in subnets. The following rules are required: - Inbound rule 1 - Protocol: All - Ports: All - Source: Self - Outbound rule 1 - Protocol: All - Ports: All - Destination: 0.0.0.0/0 (IPv4) or ::/0 (IPv6) - Outbound rule 2 - Protocol: All - Ports: All - Destination: Self
            :param subnet_ids: The ID of the subnet where AWS PCS creates an Elastic Network Interface (ENI) to enable communication between managed controllers and AWS PCS resources. The subnet must have an available IP address, cannot reside in AWS Outposts , AWS Wavelength , or an AWS Local Zone. Example: ``subnet-abcd1234``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-networking.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                networking_property = pcs_mixins.CfnClusterPropsMixin.NetworkingProperty(
                    network_type="networkType",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a166fbc4a0e2ea1d6de1f2cb7a740dce309147cfc6dbe56fea091c606beb0d79)
                check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_type is not None:
                self._values["network_type"] = network_type
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def network_type(self) -> typing.Optional[builtins.str]:
            '''The IP address version the cluster uses.

            The default is ``IPV4`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-networking.html#cfn-pcs-cluster-networking-networktype
            '''
            result = self._values.get("network_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of security group IDs associated with the Elastic Network Interface (ENI) created in subnets.

            The following rules are required:

            - Inbound rule 1
            - Protocol: All
            - Ports: All
            - Source: Self
            - Outbound rule 1
            - Protocol: All
            - Ports: All
            - Destination: 0.0.0.0/0 (IPv4) or ::/0 (IPv6)
            - Outbound rule 2
            - Protocol: All
            - Ports: All
            - Destination: Self

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-networking.html#cfn-pcs-cluster-networking-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ID of the subnet where AWS PCS creates an Elastic Network Interface (ENI) to enable communication between managed controllers and AWS PCS resources.

            The subnet must have an available IP address, cannot reside in AWS Outposts , AWS Wavelength , or an AWS Local Zone.

            Example: ``subnet-abcd1234``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-networking.html#cfn-pcs-cluster-networking-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.SchedulerProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "version": "version"},
    )
    class SchedulerProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The cluster management and job scheduling software associated with the cluster.

            :param type: The software AWS PCS uses to manage cluster scaling and job scheduling.
            :param version: The version of the specified scheduling software that AWS PCS uses to manage cluster scaling and job scheduling. For more information, see `Slurm versions in AWS PCS <https://docs.aws.amazon.com/pcs/latest/userguide/slurm-versions.html>`_ in the *AWS PCS User Guide* . Valid Values: ``23.11 | 24.05 | 24.11``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-scheduler.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                scheduler_property = pcs_mixins.CfnClusterPropsMixin.SchedulerProperty(
                    type="type",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fefe236d3461e2f468f041f19bab4198212987d14eeff8d86170277691f7843a)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The software AWS PCS uses to manage cluster scaling and job scheduling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-scheduler.html#cfn-pcs-cluster-scheduler-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the specified scheduling software that AWS PCS uses to manage cluster scaling and job scheduling.

            For more information, see `Slurm versions in AWS PCS <https://docs.aws.amazon.com/pcs/latest/userguide/slurm-versions.html>`_ in the *AWS PCS User Guide* .

            Valid Values: ``23.11 | 24.05 | 24.11``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-scheduler.html#cfn-pcs-cluster-scheduler-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchedulerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.SlurmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "accounting": "accounting",
            "auth_key": "authKey",
            "jwt_auth": "jwtAuth",
            "scale_down_idle_time_in_seconds": "scaleDownIdleTimeInSeconds",
            "slurm_custom_settings": "slurmCustomSettings",
            "slurm_rest": "slurmRest",
        },
    )
    class SlurmConfigurationProperty:
        def __init__(
            self,
            *,
            accounting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.AccountingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            auth_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.AuthKeyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            jwt_auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.JwtAuthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            scale_down_idle_time_in_seconds: typing.Optional[jsii.Number] = None,
            slurm_custom_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SlurmCustomSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            slurm_rest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.SlurmRestProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Additional options related to the Slurm scheduler.

            :param accounting: The accounting configuration includes configurable settings for Slurm accounting.
            :param auth_key: The shared Slurm key for authentication, also known as the *cluster secret* .
            :param jwt_auth: The JWT authentication configuration for Slurm REST API access.
            :param scale_down_idle_time_in_seconds: The time (in seconds) before an idle node is scaled down. Default: ``600``
            :param slurm_custom_settings: Additional Slurm-specific configuration that directly maps to Slurm settings.
            :param slurm_rest: The Slurm REST API configuration for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_configuration_property = pcs_mixins.CfnClusterPropsMixin.SlurmConfigurationProperty(
                    accounting=pcs_mixins.CfnClusterPropsMixin.AccountingProperty(
                        default_purge_time_in_days=123,
                        mode="mode"
                    ),
                    auth_key=pcs_mixins.CfnClusterPropsMixin.AuthKeyProperty(
                        secret_arn="secretArn",
                        secret_version="secretVersion"
                    ),
                    jwt_auth=pcs_mixins.CfnClusterPropsMixin.JwtAuthProperty(
                        jwt_key=pcs_mixins.CfnClusterPropsMixin.JwtKeyProperty(
                            secret_arn="secretArn",
                            secret_version="secretVersion"
                        )
                    ),
                    scale_down_idle_time_in_seconds=123,
                    slurm_custom_settings=[pcs_mixins.CfnClusterPropsMixin.SlurmCustomSettingProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )],
                    slurm_rest=pcs_mixins.CfnClusterPropsMixin.SlurmRestProperty(
                        mode="mode"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c75c281a9143e8781f4c8ed627ff49c8ecdc2cbbe492d0ea3842d6930f3a09e)
                check_type(argname="argument accounting", value=accounting, expected_type=type_hints["accounting"])
                check_type(argname="argument auth_key", value=auth_key, expected_type=type_hints["auth_key"])
                check_type(argname="argument jwt_auth", value=jwt_auth, expected_type=type_hints["jwt_auth"])
                check_type(argname="argument scale_down_idle_time_in_seconds", value=scale_down_idle_time_in_seconds, expected_type=type_hints["scale_down_idle_time_in_seconds"])
                check_type(argname="argument slurm_custom_settings", value=slurm_custom_settings, expected_type=type_hints["slurm_custom_settings"])
                check_type(argname="argument slurm_rest", value=slurm_rest, expected_type=type_hints["slurm_rest"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if accounting is not None:
                self._values["accounting"] = accounting
            if auth_key is not None:
                self._values["auth_key"] = auth_key
            if jwt_auth is not None:
                self._values["jwt_auth"] = jwt_auth
            if scale_down_idle_time_in_seconds is not None:
                self._values["scale_down_idle_time_in_seconds"] = scale_down_idle_time_in_seconds
            if slurm_custom_settings is not None:
                self._values["slurm_custom_settings"] = slurm_custom_settings
            if slurm_rest is not None:
                self._values["slurm_rest"] = slurm_rest

        @builtins.property
        def accounting(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AccountingProperty"]]:
            '''The accounting configuration includes configurable settings for Slurm accounting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html#cfn-pcs-cluster-slurmconfiguration-accounting
            '''
            result = self._values.get("accounting")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AccountingProperty"]], result)

        @builtins.property
        def auth_key(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AuthKeyProperty"]]:
            '''The shared Slurm key for authentication, also known as the *cluster secret* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html#cfn-pcs-cluster-slurmconfiguration-authkey
            '''
            result = self._values.get("auth_key")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AuthKeyProperty"]], result)

        @builtins.property
        def jwt_auth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JwtAuthProperty"]]:
            '''The JWT authentication configuration for Slurm REST API access.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html#cfn-pcs-cluster-slurmconfiguration-jwtauth
            '''
            result = self._values.get("jwt_auth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.JwtAuthProperty"]], result)

        @builtins.property
        def scale_down_idle_time_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The time (in seconds) before an idle node is scaled down.

            Default: ``600``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html#cfn-pcs-cluster-slurmconfiguration-scaledownidletimeinseconds
            '''
            result = self._values.get("scale_down_idle_time_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def slurm_custom_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SlurmCustomSettingProperty"]]]]:
            '''Additional Slurm-specific configuration that directly maps to Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html#cfn-pcs-cluster-slurmconfiguration-slurmcustomsettings
            '''
            result = self._values.get("slurm_custom_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SlurmCustomSettingProperty"]]]], result)

        @builtins.property
        def slurm_rest(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SlurmRestProperty"]]:
            '''The Slurm REST API configuration for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html#cfn-pcs-cluster-slurmconfiguration-slurmrest
            '''
            result = self._values.get("slurm_rest")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.SlurmRestProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.SlurmCustomSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class SlurmCustomSettingProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Additional settings that directly map to Slurm settings.

            .. epigraph::

               AWS PCS supports a subset of Slurm settings. For more information, see `Configuring custom Slurm settings in AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/slurm-custom-settings.html>`_ in the *AWS PCS User Guide* .

            :param parameter_name: AWS PCS supports custom Slurm settings for clusters, compute node groups, and queues. For more information, see `Configuring custom Slurm settings in AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/slurm-custom-settings.html>`_ in the *AWS PCS User Guide* .
            :param parameter_value: The values for the configured Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmcustomsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_custom_setting_property = pcs_mixins.CfnClusterPropsMixin.SlurmCustomSettingProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0739476e5c3fe56f3adeadf5c98e293c72f95a1f530190c4c9d3121038552074)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''AWS PCS supports custom Slurm settings for clusters, compute node groups, and queues.

            For more information, see `Configuring custom Slurm settings in AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/slurm-custom-settings.html>`_ in the *AWS PCS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmcustomsetting.html#cfn-pcs-cluster-slurmcustomsetting-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The values for the configured Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmcustomsetting.html#cfn-pcs-cluster-slurmcustomsetting-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmCustomSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnClusterPropsMixin.SlurmRestProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode"},
    )
    class SlurmRestProperty:
        def __init__(self, *, mode: typing.Optional[builtins.str] = None) -> None:
            '''The Slurm REST API configuration includes settings for enabling and configuring the Slurm REST API.

            It's a property of the `ClusterSlurmConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmconfiguration.html>`_ object.

            :param mode: The default value for ``mode`` is ``STANDARD`` . A value of ``STANDARD`` means the Slurm REST API is enabled. Default: - "NONE"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmrest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_rest_property = pcs_mixins.CfnClusterPropsMixin.SlurmRestProperty(
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17a9d3fe7f1dba634eee27b8cbee40ca50f7f21600bbbfc05da63d810b91f591)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The default value for ``mode`` is ``STANDARD`` .

            A value of ``STANDARD`` means the Slurm REST API is enabled.

            :default: - "NONE"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-cluster-slurmrest.html#cfn-pcs-cluster-slurmrest-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmRestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ami_id": "amiId",
        "cluster_id": "clusterId",
        "custom_launch_template": "customLaunchTemplate",
        "iam_instance_profile_arn": "iamInstanceProfileArn",
        "instance_configs": "instanceConfigs",
        "name": "name",
        "purchase_option": "purchaseOption",
        "scaling_configuration": "scalingConfiguration",
        "slurm_configuration": "slurmConfiguration",
        "spot_options": "spotOptions",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnComputeNodeGroupMixinProps:
    def __init__(
        self,
        *,
        ami_id: typing.Optional[builtins.str] = None,
        cluster_id: typing.Optional[builtins.str] = None,
        custom_launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        iam_instance_profile_arn: typing.Optional[builtins.str] = None,
        instance_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeNodeGroupPropsMixin.InstanceConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        purchase_option: typing.Optional[builtins.str] = None,
        scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        slurm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        spot_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeNodeGroupPropsMixin.SpotOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnComputeNodeGroupPropsMixin.

        :param ami_id: The ID of the Amazon Machine Image (AMI) that AWS PCS uses to launch instances. If not provided, AWS PCS uses the AMI ID specified in the custom launch template.
        :param cluster_id: The ID of the cluster of the compute node group.
        :param custom_launch_template: An Amazon EC2 launch template AWS PCS uses to launch compute nodes.
        :param iam_instance_profile_arn: The Amazon Resource Name (ARN) of the IAM instance profile used to pass an IAM role when launching EC2 instances. The role contained in your instance profile must have the ``pcs:RegisterComputeNodeGroupInstance`` permission and the role name must start with ``AWSPCS`` or must have the path ``/aws-pcs/`` . For more information, see `IAM instance profiles for AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/security-instance-profiles.html>`_ in the *AWS PCS User Guide* .
        :param instance_configs: A list of EC2 instance configurations that AWS PCS can provision in the compute node group.
        :param name: The name that identifies the compute node group.
        :param purchase_option: Specifies how EC2 instances are purchased on your behalf. AWS PCS supports On-Demand Instances, Spot Instances, and Amazon EC2 Capacity Blocks for ML. For more information, see `Amazon EC2 billing and purchasing options <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>`_ in the *Amazon Elastic Compute Cloud User Guide* . For more information about AWS PCS support for Capacity Blocks, see `Using Amazon EC2 Capacity Blocks for ML with AWS PCS <https://docs.aws.amazon.com/pcs/latest/userguide/capacity-blocks.html>`_ in the *AWS PCS User Guide* . If you don't provide this option, it defaults to On-Demand.
        :param scaling_configuration: Specifies the boundaries of the compute node group auto scaling.
        :param slurm_configuration: Additional options related to the Slurm scheduler.
        :param spot_options: Additional configuration when you specify ``SPOT`` as the ``purchaseOption`` for the ``CreateComputeNodeGroup`` API action.
        :param subnet_ids: The list of subnet IDs where instances are provisioned by the compute node group. The subnets must be in the same VPC as the cluster.
        :param tags: 1 or more tags added to the resource. Each tag consists of a tag key and tag value. The tag value is optional and can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
            
            cfn_compute_node_group_mixin_props = pcs_mixins.CfnComputeNodeGroupMixinProps(
                ami_id="amiId",
                cluster_id="clusterId",
                custom_launch_template=pcs_mixins.CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty(
                    template_id="templateId",
                    version="version"
                ),
                iam_instance_profile_arn="iamInstanceProfileArn",
                instance_configs=[pcs_mixins.CfnComputeNodeGroupPropsMixin.InstanceConfigProperty(
                    instance_type="instanceType"
                )],
                name="name",
                purchase_option="purchaseOption",
                scaling_configuration=pcs_mixins.CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty(
                    max_instance_count=123,
                    min_instance_count=123
                ),
                slurm_configuration=pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty(
                    slurm_custom_settings=[pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )]
                ),
                spot_options=pcs_mixins.CfnComputeNodeGroupPropsMixin.SpotOptionsProperty(
                    allocation_strategy="allocationStrategy"
                ),
                subnet_ids=["subnetIds"],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8b7106ee2f5cd775cfc881f00cd253474921695b117e128b31cbbb92b2f211)
            check_type(argname="argument ami_id", value=ami_id, expected_type=type_hints["ami_id"])
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument custom_launch_template", value=custom_launch_template, expected_type=type_hints["custom_launch_template"])
            check_type(argname="argument iam_instance_profile_arn", value=iam_instance_profile_arn, expected_type=type_hints["iam_instance_profile_arn"])
            check_type(argname="argument instance_configs", value=instance_configs, expected_type=type_hints["instance_configs"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument purchase_option", value=purchase_option, expected_type=type_hints["purchase_option"])
            check_type(argname="argument scaling_configuration", value=scaling_configuration, expected_type=type_hints["scaling_configuration"])
            check_type(argname="argument slurm_configuration", value=slurm_configuration, expected_type=type_hints["slurm_configuration"])
            check_type(argname="argument spot_options", value=spot_options, expected_type=type_hints["spot_options"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_id is not None:
            self._values["ami_id"] = ami_id
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if custom_launch_template is not None:
            self._values["custom_launch_template"] = custom_launch_template
        if iam_instance_profile_arn is not None:
            self._values["iam_instance_profile_arn"] = iam_instance_profile_arn
        if instance_configs is not None:
            self._values["instance_configs"] = instance_configs
        if name is not None:
            self._values["name"] = name
        if purchase_option is not None:
            self._values["purchase_option"] = purchase_option
        if scaling_configuration is not None:
            self._values["scaling_configuration"] = scaling_configuration
        if slurm_configuration is not None:
            self._values["slurm_configuration"] = slurm_configuration
        if spot_options is not None:
            self._values["spot_options"] = spot_options
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ami_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon Machine Image (AMI) that AWS PCS uses to launch instances.

        If not provided, AWS PCS uses the AMI ID specified in the custom launch template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-amiid
        '''
        result = self._values.get("ami_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the cluster of the compute node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-clusterid
        '''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_launch_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty"]]:
        '''An Amazon EC2 launch template AWS PCS uses to launch compute nodes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-customlaunchtemplate
        '''
        result = self._values.get("custom_launch_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty"]], result)

    @builtins.property
    def iam_instance_profile_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM instance profile used to pass an IAM role when launching EC2 instances.

        The role contained in your instance profile must have the ``pcs:RegisterComputeNodeGroupInstance`` permission and the role name must start with ``AWSPCS`` or must have the path ``/aws-pcs/`` . For more information, see `IAM instance profiles for AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/security-instance-profiles.html>`_ in the *AWS PCS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-iaminstanceprofilearn
        '''
        result = self._values.get("iam_instance_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.InstanceConfigProperty"]]]]:
        '''A list of EC2 instance configurations that AWS PCS can provision in the compute node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-instanceconfigs
        '''
        result = self._values.get("instance_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.InstanceConfigProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that identifies the compute node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purchase_option(self) -> typing.Optional[builtins.str]:
        '''Specifies how EC2 instances are purchased on your behalf.

        AWS PCS supports On-Demand Instances, Spot Instances, and Amazon EC2 Capacity Blocks for ML. For more information, see `Amazon EC2 billing and purchasing options <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html>`_ in the *Amazon Elastic Compute Cloud User Guide* . For more information about AWS PCS support for Capacity Blocks, see `Using Amazon EC2 Capacity Blocks for ML with AWS PCS <https://docs.aws.amazon.com/pcs/latest/userguide/capacity-blocks.html>`_ in the *AWS PCS User Guide* . If you don't provide this option, it defaults to On-Demand.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-purchaseoption
        '''
        result = self._values.get("purchase_option")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty"]]:
        '''Specifies the boundaries of the compute node group auto scaling.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-scalingconfiguration
        '''
        result = self._values.get("scaling_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty"]], result)

    @builtins.property
    def slurm_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty"]]:
        '''Additional options related to the Slurm scheduler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-slurmconfiguration
        '''
        result = self._values.get("slurm_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty"]], result)

    @builtins.property
    def spot_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.SpotOptionsProperty"]]:
        '''Additional configuration when you specify ``SPOT`` as the ``purchaseOption`` for the ``CreateComputeNodeGroup`` API action.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-spotoptions
        '''
        result = self._values.get("spot_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.SpotOptionsProperty"]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of subnet IDs where instances are provisioned by the compute node group.

        The subnets must be in the same VPC as the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''1 or more tags added to the resource.

        Each tag consists of a tag key and tag value. The tag value is optional and can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html#cfn-pcs-computenodegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComputeNodeGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnComputeNodeGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin",
):
    '''Creates an AWS PCS compute node group resource.

    For more information, see `Creating a compute node group in AWS PCS <https://docs.aws.amazon.com/pcs/latest/userguide/working-with_cng_create.html>`_ in the *AWS PCS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-computenodegroup.html
    :cloudformationResource: AWS::PCS::ComputeNodeGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
        
        cfn_compute_node_group_props_mixin = pcs_mixins.CfnComputeNodeGroupPropsMixin(pcs_mixins.CfnComputeNodeGroupMixinProps(
            ami_id="amiId",
            cluster_id="clusterId",
            custom_launch_template=pcs_mixins.CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty(
                template_id="templateId",
                version="version"
            ),
            iam_instance_profile_arn="iamInstanceProfileArn",
            instance_configs=[pcs_mixins.CfnComputeNodeGroupPropsMixin.InstanceConfigProperty(
                instance_type="instanceType"
            )],
            name="name",
            purchase_option="purchaseOption",
            scaling_configuration=pcs_mixins.CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty(
                max_instance_count=123,
                min_instance_count=123
            ),
            slurm_configuration=pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty(
                slurm_custom_settings=[pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )]
            ),
            spot_options=pcs_mixins.CfnComputeNodeGroupPropsMixin.SpotOptionsProperty(
                allocation_strategy="allocationStrategy"
            ),
            subnet_ids=["subnetIds"],
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnComputeNodeGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCS::ComputeNodeGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14864d699f9f4fd3c724b118195264f4b8bb1151524334b58ee6ec29b5d3466c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c320ca70bdfd3a7ea2ef2c0bb5b73511556219fbfe5dd1027486010e89139f45)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5c4324e0ae0d202c59a2c5f93451c6c2a0196e9b3df67c1596a4dc5f66385f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnComputeNodeGroupMixinProps:
        return typing.cast(CfnComputeNodeGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty",
        jsii_struct_bases=[],
        name_mapping={"template_id": "templateId", "version": "version"},
    )
    class CustomLaunchTemplateProperty:
        def __init__(
            self,
            *,
            template_id: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An Amazon EC2 launch template AWS PCS uses to launch compute nodes.

            :param template_id: The ID of the EC2 launch template to use to provision instances.
            :param version: The version of the EC2 launch template to use to provision instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-customlaunchtemplate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                custom_launch_template_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty(
                    template_id="templateId",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0eb7f8e077e584c1ca3458f81c7bb201916799c3b4be0dd37fd58c4486fe3b2)
                check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if template_id is not None:
                self._values["template_id"] = template_id
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def template_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the EC2 launch template to use to provision instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-customlaunchtemplate.html#cfn-pcs-computenodegroup-customlaunchtemplate-templateid
            '''
            result = self._values.get("template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of the EC2 launch template to use to provision instances.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-customlaunchtemplate.html#cfn-pcs-computenodegroup-customlaunchtemplate-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomLaunchTemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.ErrorInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorInfoProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An error that occurred during resource creation.

            :param code: The short-form error code.
            :param message: The detailed error information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-errorinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                error_info_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.ErrorInfoProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cdfa73cd8ca68f58b9c7c290e8f5f2fcc7ac0dab2c3e1322020b1acfbd779014)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The short-form error code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-errorinfo.html#cfn-pcs-computenodegroup-errorinfo-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The detailed error information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-errorinfo.html#cfn-pcs-computenodegroup-errorinfo-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.InstanceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"instance_type": "instanceType"},
    )
    class InstanceConfigProperty:
        def __init__(
            self,
            *,
            instance_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An EC2 instance configuration AWS PCS uses to launch compute nodes.

            :param instance_type: The EC2 instance type that AWS PCS can provision in the compute node group. Example: ``t2.xlarge``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-instanceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                instance_config_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.InstanceConfigProperty(
                    instance_type="instanceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29941b8c4b48b75e370c6e097d680319240d7f4c66e0016f7a41ea9ae73e19b8)
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instance_type is not None:
                self._values["instance_type"] = instance_type

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The EC2 instance type that AWS PCS can provision in the compute node group.

            Example: ``t2.xlarge``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-instanceconfig.html#cfn-pcs-computenodegroup-instanceconfig-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_instance_count": "maxInstanceCount",
            "min_instance_count": "minInstanceCount",
        },
    )
    class ScalingConfigurationProperty:
        def __init__(
            self,
            *,
            max_instance_count: typing.Optional[jsii.Number] = None,
            min_instance_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the boundaries of the compute node group auto scaling.

            :param max_instance_count: The upper bound of the number of instances allowed in the compute fleet.
            :param min_instance_count: The lower bound of the number of instances allowed in the compute fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-scalingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                scaling_configuration_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty(
                    max_instance_count=123,
                    min_instance_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__731cdc1ea3965a47a9b7d772e9209c81212448b5e68d89b6d9a56b8c8b770e57)
                check_type(argname="argument max_instance_count", value=max_instance_count, expected_type=type_hints["max_instance_count"])
                check_type(argname="argument min_instance_count", value=min_instance_count, expected_type=type_hints["min_instance_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_instance_count is not None:
                self._values["max_instance_count"] = max_instance_count
            if min_instance_count is not None:
                self._values["min_instance_count"] = min_instance_count

        @builtins.property
        def max_instance_count(self) -> typing.Optional[jsii.Number]:
            '''The upper bound of the number of instances allowed in the compute fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-scalingconfiguration.html#cfn-pcs-computenodegroup-scalingconfiguration-maxinstancecount
            '''
            result = self._values.get("max_instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_instance_count(self) -> typing.Optional[jsii.Number]:
            '''The lower bound of the number of instances allowed in the compute fleet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-scalingconfiguration.html#cfn-pcs-computenodegroup-scalingconfiguration-mininstancecount
            '''
            result = self._values.get("min_instance_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"slurm_custom_settings": "slurmCustomSettings"},
    )
    class SlurmConfigurationProperty:
        def __init__(
            self,
            *,
            slurm_custom_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Additional options related to the Slurm scheduler.

            :param slurm_custom_settings: Additional Slurm-specific configuration that directly maps to Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-slurmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_configuration_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty(
                    slurm_custom_settings=[pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a59d49a48edb444ff862268db4e4256adddc13ecfdb3ee19447c1e3f86c3d655)
                check_type(argname="argument slurm_custom_settings", value=slurm_custom_settings, expected_type=type_hints["slurm_custom_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if slurm_custom_settings is not None:
                self._values["slurm_custom_settings"] = slurm_custom_settings

        @builtins.property
        def slurm_custom_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty"]]]]:
            '''Additional Slurm-specific configuration that directly maps to Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-slurmconfiguration.html#cfn-pcs-computenodegroup-slurmconfiguration-slurmcustomsettings
            '''
            result = self._values.get("slurm_custom_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class SlurmCustomSettingProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Additional settings that directly map to Slurm settings.

            .. epigraph::

               AWS PCS supports a subset of Slurm settings. For more information, see `Configuring custom Slurm settings in AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/slurm-custom-settings.html>`_ in the *AWS PCS User Guide* .

            :param parameter_name: AWS PCS supports custom Slurm settings for clusters, compute node groups, and queues. For more information, see `Configuring custom Slurm settings in AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/slurm-custom-settings.html>`_ in the *AWS PCS User Guide* .
            :param parameter_value: The values for the configured Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-slurmcustomsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_custom_setting_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea7f440b58dee95a211dcefcc12c57a1c24fbf4b17b9b22202b60aa513c221cc)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''AWS PCS supports custom Slurm settings for clusters, compute node groups, and queues.

            For more information, see `Configuring custom Slurm settings in AWS PCS <https://docs.aws.amazon.com//pcs/latest/userguide/slurm-custom-settings.html>`_ in the *AWS PCS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-slurmcustomsetting.html#cfn-pcs-computenodegroup-slurmcustomsetting-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The values for the configured Slurm settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-slurmcustomsetting.html#cfn-pcs-computenodegroup-slurmcustomsetting-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmCustomSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnComputeNodeGroupPropsMixin.SpotOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"allocation_strategy": "allocationStrategy"},
    )
    class SpotOptionsProperty:
        def __init__(
            self,
            *,
            allocation_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Additional configuration when you specify ``SPOT`` as the ``purchaseOption`` for the ``CreateComputeNodeGroup`` API action.

            :param allocation_strategy: The Amazon EC2 allocation strategy AWS PCS uses to provision EC2 instances. AWS PCS supports *lowest price* , *capacity optimized* , and *price capacity optimized* . For more information, see `Use allocation strategies to determine how EC2 Fleet or Spot Fleet fulfills Spot and On-Demand capacity <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet-allocation-strategy.html>`_ in the *Amazon Elastic Compute Cloud User Guide* . If you don't provide this option, it defaults to *price capacity optimized* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-spotoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                spot_options_property = pcs_mixins.CfnComputeNodeGroupPropsMixin.SpotOptionsProperty(
                    allocation_strategy="allocationStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d39f77b2bee7ade253efdb8ec452de0bc613ba27c66b06ce238791610a1253df)
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 allocation strategy AWS PCS uses to provision EC2 instances.

            AWS PCS supports *lowest price* , *capacity optimized* , and *price capacity optimized* . For more information, see `Use allocation strategies to determine how EC2 Fleet or Spot Fleet fulfills Spot and On-Demand capacity <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet-allocation-strategy.html>`_ in the *Amazon Elastic Compute Cloud User Guide* . If you don't provide this option, it defaults to *price capacity optimized* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-computenodegroup-spotoptions.html#cfn-pcs-computenodegroup-spotoptions-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpotOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnQueueMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_id": "clusterId",
        "compute_node_group_configurations": "computeNodeGroupConfigurations",
        "name": "name",
        "slurm_configuration": "slurmConfiguration",
        "tags": "tags",
    },
)
class CfnQueueMixinProps:
    def __init__(
        self,
        *,
        cluster_id: typing.Optional[builtins.str] = None,
        compute_node_group_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        slurm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.SlurmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnQueuePropsMixin.

        :param cluster_id: The ID of the cluster of the queue.
        :param compute_node_group_configurations: The list of compute node group configurations associated with the queue. Queues assign jobs to associated compute node groups.
        :param name: The name that identifies the queue.
        :param slurm_configuration: Additional options related to the Slurm scheduler.
        :param tags: 1 or more tags added to the resource. Each tag consists of a tag key and tag value. The tag value is optional and can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
            
            cfn_queue_mixin_props = pcs_mixins.CfnQueueMixinProps(
                cluster_id="clusterId",
                compute_node_group_configurations=[pcs_mixins.CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty(
                    compute_node_group_id="computeNodeGroupId"
                )],
                name="name",
                slurm_configuration=pcs_mixins.CfnQueuePropsMixin.SlurmConfigurationProperty(
                    slurm_custom_settings=[pcs_mixins.CfnQueuePropsMixin.SlurmCustomSettingProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )]
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2c2c86d399e614be4058cb95fa9b5e65a001ba701b67ca1fc6d400d820e457)
            check_type(argname="argument cluster_id", value=cluster_id, expected_type=type_hints["cluster_id"])
            check_type(argname="argument compute_node_group_configurations", value=compute_node_group_configurations, expected_type=type_hints["compute_node_group_configurations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument slurm_configuration", value=slurm_configuration, expected_type=type_hints["slurm_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_id is not None:
            self._values["cluster_id"] = cluster_id
        if compute_node_group_configurations is not None:
            self._values["compute_node_group_configurations"] = compute_node_group_configurations
        if name is not None:
            self._values["name"] = name
        if slurm_configuration is not None:
            self._values["slurm_configuration"] = slurm_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cluster_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the cluster of the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html#cfn-pcs-queue-clusterid
        '''
        result = self._values.get("cluster_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_node_group_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty"]]]]:
        '''The list of compute node group configurations associated with the queue.

        Queues assign jobs to associated compute node groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html#cfn-pcs-queue-computenodegroupconfigurations
        '''
        result = self._values.get("compute_node_group_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name that identifies the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html#cfn-pcs-queue-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slurm_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.SlurmConfigurationProperty"]]:
        '''Additional options related to the Slurm scheduler.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html#cfn-pcs-queue-slurmconfiguration
        '''
        result = self._values.get("slurm_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.SlurmConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''1 or more tags added to the resource.

        Each tag consists of a tag key and tag value. The tag value is optional and can be an empty string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html#cfn-pcs-queue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueuePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnQueuePropsMixin",
):
    '''Creates an AWS PCS queue resource.

    For more information, see `Creating a queue in AWS PCS <https://docs.aws.amazon.com/pcs/latest/userguide/working-with_queues_create.html>`_ in the *AWS PCS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcs-queue.html
    :cloudformationResource: AWS::PCS::Queue
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
        
        cfn_queue_props_mixin = pcs_mixins.CfnQueuePropsMixin(pcs_mixins.CfnQueueMixinProps(
            cluster_id="clusterId",
            compute_node_group_configurations=[pcs_mixins.CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty(
                compute_node_group_id="computeNodeGroupId"
            )],
            name="name",
            slurm_configuration=pcs_mixins.CfnQueuePropsMixin.SlurmConfigurationProperty(
                slurm_custom_settings=[pcs_mixins.CfnQueuePropsMixin.SlurmCustomSettingProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )]
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCS::Queue``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d256399afe95b0d4b692524ccfa73d971452eaf1b4c51bcc5d068706fc2dd21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55f4eab720f201cc5ace2687d9b575f7d303acd3028dce59841e950262fa4fe9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e3194cff9d4094c5242d7e089ae62d519299560b2c57e6a9506ad384cb1e03)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueMixinProps:
        return typing.cast(CfnQueueMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"compute_node_group_id": "computeNodeGroupId"},
    )
    class ComputeNodeGroupConfigurationProperty:
        def __init__(
            self,
            *,
            compute_node_group_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The compute node group configuration for a queue.

            :param compute_node_group_id: The compute node group ID for the compute node group configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-computenodegroupconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                compute_node_group_configuration_property = pcs_mixins.CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty(
                    compute_node_group_id="computeNodeGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40207f4bfa081ad3188d1663226c429cd7bc518d9289dad2a4df025f9c21a56b)
                check_type(argname="argument compute_node_group_id", value=compute_node_group_id, expected_type=type_hints["compute_node_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_node_group_id is not None:
                self._values["compute_node_group_id"] = compute_node_group_id

        @builtins.property
        def compute_node_group_id(self) -> typing.Optional[builtins.str]:
            '''The compute node group ID for the compute node group configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-computenodegroupconfiguration.html#cfn-pcs-queue-computenodegroupconfiguration-computenodegroupid
            '''
            result = self._values.get("compute_node_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeNodeGroupConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnQueuePropsMixin.ErrorInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "message": "message"},
    )
    class ErrorInfoProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            message: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An error that occurred during resource creation.

            :param code: The short-form error code.
            :param message: The detailed error information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-errorinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                error_info_property = pcs_mixins.CfnQueuePropsMixin.ErrorInfoProperty(
                    code="code",
                    message="message"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7623dfa13f2d0d9f8cfb643254a2a4001a5cef8d9f147ac996b902dcf664bb6)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if message is not None:
                self._values["message"] = message

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The short-form error code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-errorinfo.html#cfn-pcs-queue-errorinfo-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message(self) -> typing.Optional[builtins.str]:
            '''The detailed error information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-errorinfo.html#cfn-pcs-queue-errorinfo-message
            '''
            result = self._values.get("message")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ErrorInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnQueuePropsMixin.SlurmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"slurm_custom_settings": "slurmCustomSettings"},
    )
    class SlurmConfigurationProperty:
        def __init__(
            self,
            *,
            slurm_custom_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.SlurmCustomSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The Slurm configuration for the queue.

            :param slurm_custom_settings: Custom Slurm parameters that directly map to Slurm configuration settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-slurmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_configuration_property = pcs_mixins.CfnQueuePropsMixin.SlurmConfigurationProperty(
                    slurm_custom_settings=[pcs_mixins.CfnQueuePropsMixin.SlurmCustomSettingProperty(
                        parameter_name="parameterName",
                        parameter_value="parameterValue"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fafaf246e6e032765a71b58c16cd83973bbdc685fcaee489ecbe365d5a432790)
                check_type(argname="argument slurm_custom_settings", value=slurm_custom_settings, expected_type=type_hints["slurm_custom_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if slurm_custom_settings is not None:
                self._values["slurm_custom_settings"] = slurm_custom_settings

        @builtins.property
        def slurm_custom_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.SlurmCustomSettingProperty"]]]]:
            '''Custom Slurm parameters that directly map to Slurm configuration settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-slurmconfiguration.html#cfn-pcs-queue-slurmconfiguration-slurmcustomsettings
            '''
            result = self._values.get("slurm_custom_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.SlurmCustomSettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcs.mixins.CfnQueuePropsMixin.SlurmCustomSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class SlurmCustomSettingProperty:
        def __init__(
            self,
            *,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Additional settings that directly map to Slurm settings.

            :param parameter_name: AWS PCS supports configuration of the Slurm parameters for queues:.
            :param parameter_value: The value for the configured Slurm setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-slurmcustomsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcs import mixins as pcs_mixins
                
                slurm_custom_setting_property = pcs_mixins.CfnQueuePropsMixin.SlurmCustomSettingProperty(
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__291ef54ddf13f98ee0fb3a2f73ada360cc34873a763710ac7c1c66a3ac62e475)
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''AWS PCS supports configuration of the Slurm parameters for queues:.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-slurmcustomsetting.html#cfn-pcs-queue-slurmcustomsetting-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The value for the configured Slurm setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcs-queue-slurmcustomsetting.html#cfn-pcs-queue-slurmcustomsetting-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SlurmCustomSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnClusterLogsMixin",
    "CfnClusterMixinProps",
    "CfnClusterPcsJobcompLogs",
    "CfnClusterPcsSchedulerLogs",
    "CfnClusterPropsMixin",
    "CfnComputeNodeGroupMixinProps",
    "CfnComputeNodeGroupPropsMixin",
    "CfnQueueMixinProps",
    "CfnQueuePropsMixin",
]

publication.publish()

def _typecheckingstub__895989435c64ce6ac8ba60f4839b019a11c9756f2dddd9df13d89ee185120eaf(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62ba0f970aaa3a35b0eea8e1d967c5d7b947370f9db7a78ac98b9a262357c37a(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24685fe192db49a38fd71bcc95b607b3b231591f3ce0acb13d01583294d02ed(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d069e354fe429fa37d463bcd8808306a156c7550c35f5a2b5b14547590a8b4(
    *,
    name: typing.Optional[builtins.str] = None,
    networking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.NetworkingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scheduler: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SchedulerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    size: typing.Optional[builtins.str] = None,
    slurm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SlurmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d3301a1e1650a5371b00fb7e336a84bbe09309bc87a173df1c8f487f161a15(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5fb6e94f05b3033e409179570a4b40f31ff4939491f63243173c259e4adbd0(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00425dadad64c8a5d02f7361b03fb17f41cd92801e4ce5909e6a4d1a83cf667(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbddd3f16d07d0b43d9bf79954fc54f49c77f115eec373bcb16bf9dd63effc1a(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f90c69aa8ef08fdb6d52d6de2cbd70db375fe9d1610fa3b7d867a296f95edab0(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1da1c528da59bd7d286c57a9e7b1f29d79e506bb7c1c1987592b5db36e9aeef(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4455d37bdb4866de78c480231e6886cc9b46f0fe8547b09f422c0be6877700a0(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3948bbd24aed3e0a1e2d93a8f6854b85bdcb3616f31fb161908e95ad786d5667(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce31bf49b7932c949ea341382cee17ad8d7988d66aec2db23d52cddc3e65154f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18eb5eaa67dffbf69d952ce72164b34ac43447e29b64173d871070dd7b5b0e08(
    *,
    default_purge_time_in_days: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__742fffcae4a116590669545796b524aee637a9bc5aea981596920da821bb3ff3(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
    secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944b6239ea34402ca9bb01b202495ec1f17c86232f3c24fe20e2ee81f06e925f(
    *,
    ipv6_address: typing.Optional[builtins.str] = None,
    port: typing.Optional[builtins.str] = None,
    private_ip_address: typing.Optional[builtins.str] = None,
    public_ip_address: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b60893d5dec4eeb0634087a31c9f9c2802e40d0ab55cc3b29982c3a2dd0a7f66(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33ccfedb299ee55239e88c1bd7a4b58f4343a35459717575dccc1d42f7d6c3e(
    *,
    jwt_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.JwtKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7eb55121bd6b90e011eb8375c59bb19c9c3c91e6b05f11ed14d2a00e530108f(
    *,
    secret_arn: typing.Optional[builtins.str] = None,
    secret_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a166fbc4a0e2ea1d6de1f2cb7a740dce309147cfc6dbe56fea091c606beb0d79(
    *,
    network_type: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefe236d3461e2f468f041f19bab4198212987d14eeff8d86170277691f7843a(
    *,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c75c281a9143e8781f4c8ed627ff49c8ecdc2cbbe492d0ea3842d6930f3a09e(
    *,
    accounting: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.AccountingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auth_key: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.AuthKeyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    jwt_auth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.JwtAuthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scale_down_idle_time_in_seconds: typing.Optional[jsii.Number] = None,
    slurm_custom_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SlurmCustomSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    slurm_rest: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.SlurmRestProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0739476e5c3fe56f3adeadf5c98e293c72f95a1f530190c4c9d3121038552074(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a9d3fe7f1dba634eee27b8cbee40ca50f7f21600bbbfc05da63d810b91f591(
    *,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8b7106ee2f5cd775cfc881f00cd253474921695b117e128b31cbbb92b2f211(
    *,
    ami_id: typing.Optional[builtins.str] = None,
    cluster_id: typing.Optional[builtins.str] = None,
    custom_launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeNodeGroupPropsMixin.CustomLaunchTemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iam_instance_profile_arn: typing.Optional[builtins.str] = None,
    instance_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeNodeGroupPropsMixin.InstanceConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    purchase_option: typing.Optional[builtins.str] = None,
    scaling_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeNodeGroupPropsMixin.ScalingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    slurm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeNodeGroupPropsMixin.SlurmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spot_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeNodeGroupPropsMixin.SpotOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14864d699f9f4fd3c724b118195264f4b8bb1151524334b58ee6ec29b5d3466c(
    props: typing.Union[CfnComputeNodeGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c320ca70bdfd3a7ea2ef2c0bb5b73511556219fbfe5dd1027486010e89139f45(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5c4324e0ae0d202c59a2c5f93451c6c2a0196e9b3df67c1596a4dc5f66385f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0eb7f8e077e584c1ca3458f81c7bb201916799c3b4be0dd37fd58c4486fe3b2(
    *,
    template_id: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdfa73cd8ca68f58b9c7c290e8f5f2fcc7ac0dab2c3e1322020b1acfbd779014(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29941b8c4b48b75e370c6e097d680319240d7f4c66e0016f7a41ea9ae73e19b8(
    *,
    instance_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731cdc1ea3965a47a9b7d772e9209c81212448b5e68d89b6d9a56b8c8b770e57(
    *,
    max_instance_count: typing.Optional[jsii.Number] = None,
    min_instance_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59d49a48edb444ff862268db4e4256adddc13ecfdb3ee19447c1e3f86c3d655(
    *,
    slurm_custom_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputeNodeGroupPropsMixin.SlurmCustomSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7f440b58dee95a211dcefcc12c57a1c24fbf4b17b9b22202b60aa513c221cc(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39f77b2bee7ade253efdb8ec452de0bc613ba27c66b06ce238791610a1253df(
    *,
    allocation_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2c2c86d399e614be4058cb95fa9b5e65a001ba701b67ca1fc6d400d820e457(
    *,
    cluster_id: typing.Optional[builtins.str] = None,
    compute_node_group_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.ComputeNodeGroupConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    slurm_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.SlurmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d256399afe95b0d4b692524ccfa73d971452eaf1b4c51bcc5d068706fc2dd21(
    props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55f4eab720f201cc5ace2687d9b575f7d303acd3028dce59841e950262fa4fe9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e3194cff9d4094c5242d7e089ae62d519299560b2c57e6a9506ad384cb1e03(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40207f4bfa081ad3188d1663226c429cd7bc518d9289dad2a4df025f9c21a56b(
    *,
    compute_node_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7623dfa13f2d0d9f8cfb643254a2a4001a5cef8d9f147ac996b902dcf664bb6(
    *,
    code: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafaf246e6e032765a71b58c16cd83973bbdc685fcaee489ecbe365d5a432790(
    *,
    slurm_custom_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.SlurmCustomSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291ef54ddf13f98ee0fb3a2f73ada360cc34873a763710ac7c1c66a3ac62e475(
    *,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
