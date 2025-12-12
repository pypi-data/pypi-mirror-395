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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"resource_arn": "resourceArn", "resource_policy": "resourcePolicy"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        resource_arn: typing.Optional[builtins.str] = None,
        resource_policy: typing.Any = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param resource_arn: Returns the Amazon Resource Name (ARN) of the resource-based policy.
        :param resource_policy: This is the description for the resource policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
            
            # resource_policy: Any
            
            cfn_resource_policy_mixin_props = kinesis_mixins.CfnResourcePolicyMixinProps(
                resource_arn="resourceArn",
                resource_policy=resource_policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fd2649bef9218a23e93563a3a6ce252d478134407461c49212a25d1438b8ba1)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''Returns the Amazon Resource Name (ARN) of the resource-based policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-resourcepolicy.html#cfn-kinesis-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_policy(self) -> typing.Any:
        '''This is the description for the resource policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-resourcepolicy.html#cfn-kinesis-resourcepolicy-resourcepolicy
        '''
        result = self._values.get("resource_policy")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnResourcePolicyPropsMixin",
):
    '''Attaches a resource-based policy to a data stream or registered consumer.

    If you are using an identity other than the root user of the AWS account that owns the resource, the calling identity must have the ``PutResourcePolicy`` permissions on the specified Kinesis Data Streams resource and belong to the owner's account in order to use this operation. If you don't have ``PutResourcePolicy`` permissions, Amazon Kinesis Data Streams returns a ``403 Access Denied error`` . If you receive a ``ResourceNotFoundException`` , check to see if you passed a valid stream or consumer resource.

    Request patterns can be one of the following:

    - Data stream pattern: ``arn:aws.*:kinesis:.*:\\d{12}:.*stream/\\S+``
    - Consumer pattern: ``^(arn):aws.*:kinesis:.*:\\d{12}:.*stream\\/[a-zA-Z0-9_.-]+\\/consumer\\/[a-zA-Z0-9_.-]+:[0-9]+``

    For more information, see `Controlling Access to Amazon Kinesis Data Streams Resources Using IAM <https://docs.aws.amazon.com/streams/latest/dev/controlling-access.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-resourcepolicy.html
    :cloudformationResource: AWS::Kinesis::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
        
        # resource_policy: Any
        
        cfn_resource_policy_props_mixin = kinesis_mixins.CfnResourcePolicyPropsMixin(kinesis_mixins.CfnResourcePolicyMixinProps(
            resource_arn="resourceArn",
            resource_policy=resource_policy
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Kinesis::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c6c3ecfd164942ddab8777f07fd5d343f5c15100b72da763b9ebf71eae64c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15a9d86adb369dd1dad8cd85a94ff50801c976eef49016fcee484c5002a56432)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fdd3be0f5c58b756e7645b1080bd008732bed3877287f4c31e947ec69f7379)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourcePolicyMixinProps:
        return typing.cast(CfnResourcePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamConsumerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_name": "consumerName",
        "stream_arn": "streamArn",
        "tags": "tags",
    },
)
class CfnStreamConsumerMixinProps:
    def __init__(
        self,
        *,
        consumer_name: typing.Optional[builtins.str] = None,
        stream_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStreamConsumerPropsMixin.

        :param consumer_name: The name of the consumer is something you choose when you register the consumer.
        :param stream_arn: The ARN of the stream with which you registered the consumer.
        :param tags: An array of tags to be added to a specified Kinesis resource. A tag consists of a required key and an optional value. You can specify up to 50 tag key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
            
            cfn_stream_consumer_mixin_props = kinesis_mixins.CfnStreamConsumerMixinProps(
                consumer_name="consumerName",
                stream_arn="streamArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__801072109e4d1271eacf2fb0b94f2be97190f300f538ead8d21bcff225db0484)
            check_type(argname="argument consumer_name", value=consumer_name, expected_type=type_hints["consumer_name"])
            check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if consumer_name is not None:
            self._values["consumer_name"] = consumer_name
        if stream_arn is not None:
            self._values["stream_arn"] = stream_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def consumer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the consumer is something you choose when you register the consumer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-consumername
        '''
        result = self._values.get("consumer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the stream with which you registered the consumer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-streamarn
        '''
        result = self._values.get("stream_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of tags to be added to a specified Kinesis resource.

        A tag consists of a required key and an optional value. You can specify up to 50 tag key-value pairs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html#cfn-kinesis-streamconsumer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamConsumerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamConsumerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamConsumerPropsMixin",
):
    '''Use the AWS CloudFormation ``AWS::Kinesis::StreamConsumer`` resource to register a consumer with a Kinesis data stream.

    The consumer you register can then call `SubscribeToShard <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_SubscribeToShard.html>`_ to receive data from the stream using enhanced fan-out, at a rate of up to 2 MiB per second for every shard you subscribe to. This rate is unaffected by the total number of consumers that read from the same stream.

    You can register up to 20 consumers per stream. However, you can request a limit increase using the `Kinesis Data Streams limits form <https://docs.aws.amazon.com/support/v1?#/>`_ . A given consumer can only be registered with one stream at a time.

    For more information, see `Using Consumers with Enhanced Fan-Out <https://docs.aws.amazon.com/streams/latest/dev/introduction-to-enhanced-consumers.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-streamconsumer.html
    :cloudformationResource: AWS::Kinesis::StreamConsumer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
        
        cfn_stream_consumer_props_mixin = kinesis_mixins.CfnStreamConsumerPropsMixin(kinesis_mixins.CfnStreamConsumerMixinProps(
            consumer_name="consumerName",
            stream_arn="streamArn",
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
        props: typing.Union[CfnStreamConsumerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Kinesis::StreamConsumer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58ad3ac51312fa863390b8c3766e90dad75dc1911ed200082e83a68a92abc44b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b904cf3931d77c0c75ead858b8df3ae97e3e3964a05d447a274409c99aafffa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c59f9ef01ad08f00cd68e827ec925472dfcef35e759bc14c9f61ab6b7e2a20)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamConsumerMixinProps:
        return typing.cast(CfnStreamConsumerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "desired_shard_level_metrics": "desiredShardLevelMetrics",
        "max_record_size_in_kib": "maxRecordSizeInKiB",
        "name": "name",
        "retention_period_hours": "retentionPeriodHours",
        "shard_count": "shardCount",
        "stream_encryption": "streamEncryption",
        "stream_mode_details": "streamModeDetails",
        "tags": "tags",
        "warm_throughput_mi_bps": "warmThroughputMiBps",
    },
)
class CfnStreamMixinProps:
    def __init__(
        self,
        *,
        desired_shard_level_metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_record_size_in_kib: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        retention_period_hours: typing.Optional[jsii.Number] = None,
        shard_count: typing.Optional[jsii.Number] = None,
        stream_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamPropsMixin.StreamEncryptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        stream_mode_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamPropsMixin.StreamModeDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        warm_throughput_mi_bps: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnStreamPropsMixin.

        :param desired_shard_level_metrics: A list of shard-level metrics in properties to enable enhanced monitoring mode.
        :param max_record_size_in_kib: The maximum record size of a single record in kibibyte (KiB) that you can write to, and read from a stream.
        :param name: The name of the Kinesis stream. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the stream name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param retention_period_hours: The number of hours for the data records that are stored in shards to remain accessible. The default value is 24. For more information about the stream retention period, see `Changing the Data Retention Period <https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html>`_ in the Amazon Kinesis Developer Guide.
        :param shard_count: The number of shards that the stream uses. For greater provisioned throughput, increase the number of shards.
        :param stream_encryption: When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream. Removing this property from your stack template and updating your stack disables encryption.
        :param stream_mode_details: Specifies the capacity mode to which you want to set your data stream. Currently, in Kinesis Data Streams, you can choose between an *on-demand* capacity mode and a *provisioned* capacity mode for your data streams.
        :param tags: An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream. For information about constraints for this property, see `Tag Restrictions <https://docs.aws.amazon.com/streams/latest/dev/tagging.html#tagging-restrictions>`_ in the *Amazon Kinesis Developer Guide* .
        :param warm_throughput_mi_bps: The target warm throughput in MB/s that the stream should be scaled to handle. This represents the throughput capacity that will be immediately available for write operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
            
            cfn_stream_mixin_props = kinesis_mixins.CfnStreamMixinProps(
                desired_shard_level_metrics=["desiredShardLevelMetrics"],
                max_record_size_in_ki_b=123,
                name="name",
                retention_period_hours=123,
                shard_count=123,
                stream_encryption=kinesis_mixins.CfnStreamPropsMixin.StreamEncryptionProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                ),
                stream_mode_details=kinesis_mixins.CfnStreamPropsMixin.StreamModeDetailsProperty(
                    stream_mode="streamMode"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                warm_throughput_mi_bps=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9c5a5875130c3aba3dca4dd8836312c7f093e74988b1ad81c7b80a56aeef7f8)
            check_type(argname="argument desired_shard_level_metrics", value=desired_shard_level_metrics, expected_type=type_hints["desired_shard_level_metrics"])
            check_type(argname="argument max_record_size_in_kib", value=max_record_size_in_kib, expected_type=type_hints["max_record_size_in_kib"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument retention_period_hours", value=retention_period_hours, expected_type=type_hints["retention_period_hours"])
            check_type(argname="argument shard_count", value=shard_count, expected_type=type_hints["shard_count"])
            check_type(argname="argument stream_encryption", value=stream_encryption, expected_type=type_hints["stream_encryption"])
            check_type(argname="argument stream_mode_details", value=stream_mode_details, expected_type=type_hints["stream_mode_details"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument warm_throughput_mi_bps", value=warm_throughput_mi_bps, expected_type=type_hints["warm_throughput_mi_bps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if desired_shard_level_metrics is not None:
            self._values["desired_shard_level_metrics"] = desired_shard_level_metrics
        if max_record_size_in_kib is not None:
            self._values["max_record_size_in_kib"] = max_record_size_in_kib
        if name is not None:
            self._values["name"] = name
        if retention_period_hours is not None:
            self._values["retention_period_hours"] = retention_period_hours
        if shard_count is not None:
            self._values["shard_count"] = shard_count
        if stream_encryption is not None:
            self._values["stream_encryption"] = stream_encryption
        if stream_mode_details is not None:
            self._values["stream_mode_details"] = stream_mode_details
        if tags is not None:
            self._values["tags"] = tags
        if warm_throughput_mi_bps is not None:
            self._values["warm_throughput_mi_bps"] = warm_throughput_mi_bps

    @builtins.property
    def desired_shard_level_metrics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of shard-level metrics in properties to enable enhanced monitoring mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-desiredshardlevelmetrics
        '''
        result = self._values.get("desired_shard_level_metrics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_record_size_in_kib(self) -> typing.Optional[jsii.Number]:
        '''The maximum record size of a single record in kibibyte (KiB) that you can write to, and read from a stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-maxrecordsizeinkib
        '''
        result = self._values.get("max_record_size_in_kib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Kinesis stream.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the stream name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .

        If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_period_hours(self) -> typing.Optional[jsii.Number]:
        '''The number of hours for the data records that are stored in shards to remain accessible.

        The default value is 24. For more information about the stream retention period, see `Changing the Data Retention Period <https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html>`_ in the Amazon Kinesis Developer Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-retentionperiodhours
        '''
        result = self._values.get("retention_period_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shard_count(self) -> typing.Optional[jsii.Number]:
        '''The number of shards that the stream uses.

        For greater provisioned throughput, increase the number of shards.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-shardcount
        '''
        result = self._values.get("shard_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_encryption(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.StreamEncryptionProperty"]]:
        '''When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream.

        Removing this property from your stack template and updating your stack disables encryption.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streamencryption
        '''
        result = self._values.get("stream_encryption")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.StreamEncryptionProperty"]], result)

    @builtins.property
    def stream_mode_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.StreamModeDetailsProperty"]]:
        '''Specifies the capacity mode to which you want to set your data stream.

        Currently, in Kinesis Data Streams, you can choose between an *on-demand* capacity mode and a *provisioned* capacity mode for your data streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-streammodedetails
        '''
        result = self._values.get("stream_mode_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.StreamModeDetailsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream.

        For information about constraints for this property, see `Tag Restrictions <https://docs.aws.amazon.com/streams/latest/dev/tagging.html#tagging-restrictions>`_ in the *Amazon Kinesis Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def warm_throughput_mi_bps(self) -> typing.Optional[jsii.Number]:
        '''The target warm throughput in MB/s that the stream should be scaled to handle.

        This represents the throughput capacity that will be immediately available for write operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html#cfn-kinesis-stream-warmthroughputmibps
        '''
        result = self._values.get("warm_throughput_mi_bps")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamPropsMixin",
):
    '''Creates a Kinesis stream that captures and transports data records that are emitted from data sources.

    For information about creating streams, see `CreateStream <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_CreateStream.html>`_ in the Amazon Kinesis API Reference.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesis-stream.html
    :cloudformationResource: AWS::Kinesis::Stream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
        
        cfn_stream_props_mixin = kinesis_mixins.CfnStreamPropsMixin(kinesis_mixins.CfnStreamMixinProps(
            desired_shard_level_metrics=["desiredShardLevelMetrics"],
            max_record_size_in_ki_b=123,
            name="name",
            retention_period_hours=123,
            shard_count=123,
            stream_encryption=kinesis_mixins.CfnStreamPropsMixin.StreamEncryptionProperty(
                encryption_type="encryptionType",
                key_id="keyId"
            ),
            stream_mode_details=kinesis_mixins.CfnStreamPropsMixin.StreamModeDetailsProperty(
                stream_mode="streamMode"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            warm_throughput_mi_bps=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Kinesis::Stream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910e23d8089e07dae2716c5b90b4830f8e6fa77a3d4856a2c25f9e5ecbf8d0f1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8ebbd7b3f0cfe0ad4c7240a4162730bb84944188232769584e1c59bb6c94a58)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9124d4f9e18565b33fbb8020ed518e95009e5430349bd226be7314b7051d3e57)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamMixinProps:
        return typing.cast(CfnStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamPropsMixin.StreamEncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "key_id": "keyId"},
    )
    class StreamEncryptionProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[builtins.str] = None,
            key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Enables or updates server-side encryption using an AWS KMS key for a specified stream.

            .. epigraph::

               When invoking this API, you must use either the ``StreamARN`` or the ``StreamName`` parameter, or both. It is recommended that you use the ``StreamARN`` input parameter when you invoke this API.

            Starting encryption is an asynchronous operation. Upon receiving the request, Kinesis Data Streams returns immediately and sets the status of the stream to ``UPDATING`` . After the update is complete, Kinesis Data Streams sets the status of the stream back to ``ACTIVE`` . Updating or applying encryption normally takes a few seconds to complete, but it can take minutes. You can continue to read and write data to your stream while its status is ``UPDATING`` . Once the status of the stream is ``ACTIVE`` , encryption begins for records written to the stream.

            API Limits: You can successfully apply a new AWS KMS key for server-side encryption 25 times in a rolling 24-hour period.

            Note: It can take up to 5 seconds after the stream is in an ``ACTIVE`` status before all records written to the stream are encrypted. After you enable encryption, you can verify that encryption is applied by inspecting the API response from ``PutRecord`` or ``PutRecords`` .

            :param encryption_type: The encryption type to use. The only valid value is ``KMS`` .
            :param key_id: The GUID for the customer-managed AWS KMS key to use for encryption. This value can be a globally unique identifier, a fully specified Amazon Resource Name (ARN) to either an alias or a key, or an alias name prefixed by "alias/".You can also use a master key owned by Kinesis Data Streams by specifying the alias ``aws/kinesis`` . - Key ARN example: ``arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012`` - Alias ARN example: ``arn:aws:kms:us-east-1:123456789012:alias/MyAliasName`` - Globally unique key ID example: ``12345678-1234-1234-1234-123456789012`` - Alias name example: ``alias/MyAliasName`` - Master key owned by Kinesis Data Streams: ``alias/aws/kinesis``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
                
                stream_encryption_property = kinesis_mixins.CfnStreamPropsMixin.StreamEncryptionProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27d6bedd3a51e9ff78d5a28768be2a28a76998900449a9b76cf9ba4a41be3d2c)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type
            if key_id is not None:
                self._values["key_id"] = key_id

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The encryption type to use.

            The only valid value is ``KMS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_id(self) -> typing.Optional[builtins.str]:
            '''The GUID for the customer-managed AWS KMS key to use for encryption.

            This value can be a globally unique identifier, a fully specified Amazon Resource Name (ARN) to either an alias or a key, or an alias name prefixed by "alias/".You can also use a master key owned by Kinesis Data Streams by specifying the alias ``aws/kinesis`` .

            - Key ARN example: ``arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012``
            - Alias ARN example: ``arn:aws:kms:us-east-1:123456789012:alias/MyAliasName``
            - Globally unique key ID example: ``12345678-1234-1234-1234-123456789012``
            - Alias name example: ``alias/MyAliasName``
            - Master key owned by Kinesis Data Streams: ``alias/aws/kinesis``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streamencryption.html#cfn-kinesis-stream-streamencryption-keyid
            '''
            result = self._values.get("key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamEncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamPropsMixin.StreamModeDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_mode": "streamMode"},
    )
    class StreamModeDetailsProperty:
        def __init__(
            self,
            *,
            stream_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the capacity mode to which you want to set your data stream.

            Currently, in Kinesis Data Streams, you can choose between an *on-demand* capacity mode and a *provisioned* capacity mode for your data streams.

            :param stream_mode: Specifies the capacity mode to which you want to set your data stream. Currently, in Kinesis Data Streams, you can choose between an *on-demand* capacity mode and a *provisioned* capacity mode for your data streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streammodedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
                
                stream_mode_details_property = kinesis_mixins.CfnStreamPropsMixin.StreamModeDetailsProperty(
                    stream_mode="streamMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b48e5b2504d3f36807bccdc085cb6d0f357a1d06635a88136da0225ab090485)
                check_type(argname="argument stream_mode", value=stream_mode, expected_type=type_hints["stream_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stream_mode is not None:
                self._values["stream_mode"] = stream_mode

        @builtins.property
        def stream_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies the capacity mode to which you want to set your data stream.

            Currently, in Kinesis Data Streams, you can choose between an *on-demand* capacity mode and a *provisioned* capacity mode for your data streams.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-streammodedetails.html#cfn-kinesis-stream-streammodedetails-streammode
            '''
            result = self._values.get("stream_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamModeDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesis.mixins.CfnStreamPropsMixin.WarmThroughputObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "current_mi_bps": "currentMiBps",
            "target_mi_bps": "targetMiBps",
        },
    )
    class WarmThroughputObjectProperty:
        def __init__(
            self,
            *,
            current_mi_bps: typing.Optional[jsii.Number] = None,
            target_mi_bps: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Represents the warm throughput configuration on the stream.

            This is only present for On-Demand Kinesis Data Streams in accounts that have ``MinimumThroughputBillingCommitment`` enabled.

            :param current_mi_bps: The current warm throughput value on the stream. This is the write throughput in MiBps that the stream is currently scaled to handle.
            :param target_mi_bps: The target warm throughput value on the stream. This indicates that the stream is currently scaling towards this target value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-warmthroughputobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesis import mixins as kinesis_mixins
                
                warm_throughput_object_property = kinesis_mixins.CfnStreamPropsMixin.WarmThroughputObjectProperty(
                    current_mi_bps=123,
                    target_mi_bps=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c57882bea5ea967aefe650cda76dcd44bb8549c6523cf44f537f7e3782e60e3)
                check_type(argname="argument current_mi_bps", value=current_mi_bps, expected_type=type_hints["current_mi_bps"])
                check_type(argname="argument target_mi_bps", value=target_mi_bps, expected_type=type_hints["target_mi_bps"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if current_mi_bps is not None:
                self._values["current_mi_bps"] = current_mi_bps
            if target_mi_bps is not None:
                self._values["target_mi_bps"] = target_mi_bps

        @builtins.property
        def current_mi_bps(self) -> typing.Optional[jsii.Number]:
            '''The current warm throughput value on the stream.

            This is the write throughput in MiBps that the stream is currently scaled to handle.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-warmthroughputobject.html#cfn-kinesis-stream-warmthroughputobject-currentmibps
            '''
            result = self._values.get("current_mi_bps")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def target_mi_bps(self) -> typing.Optional[jsii.Number]:
            '''The target warm throughput value on the stream.

            This indicates that the stream is currently scaling towards this target value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesis-stream-warmthroughputobject.html#cfn-kinesis-stream-warmthroughputobject-targetmibps
            '''
            result = self._values.get("target_mi_bps")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WarmThroughputObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnStreamConsumerMixinProps",
    "CfnStreamConsumerPropsMixin",
    "CfnStreamMixinProps",
    "CfnStreamPropsMixin",
]

publication.publish()

def _typecheckingstub__2fd2649bef9218a23e93563a3a6ce252d478134407461c49212a25d1438b8ba1(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    resource_policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c6c3ecfd164942ddab8777f07fd5d343f5c15100b72da763b9ebf71eae64c9(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15a9d86adb369dd1dad8cd85a94ff50801c976eef49016fcee484c5002a56432(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fdd3be0f5c58b756e7645b1080bd008732bed3877287f4c31e947ec69f7379(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__801072109e4d1271eacf2fb0b94f2be97190f300f538ead8d21bcff225db0484(
    *,
    consumer_name: typing.Optional[builtins.str] = None,
    stream_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58ad3ac51312fa863390b8c3766e90dad75dc1911ed200082e83a68a92abc44b(
    props: typing.Union[CfnStreamConsumerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b904cf3931d77c0c75ead858b8df3ae97e3e3964a05d447a274409c99aafffa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c59f9ef01ad08f00cd68e827ec925472dfcef35e759bc14c9f61ab6b7e2a20(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c5a5875130c3aba3dca4dd8836312c7f093e74988b1ad81c7b80a56aeef7f8(
    *,
    desired_shard_level_metrics: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_record_size_in_kib: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    retention_period_hours: typing.Optional[jsii.Number] = None,
    shard_count: typing.Optional[jsii.Number] = None,
    stream_encryption: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamPropsMixin.StreamEncryptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stream_mode_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamPropsMixin.StreamModeDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    warm_throughput_mi_bps: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910e23d8089e07dae2716c5b90b4830f8e6fa77a3d4856a2c25f9e5ecbf8d0f1(
    props: typing.Union[CfnStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ebbd7b3f0cfe0ad4c7240a4162730bb84944188232769584e1c59bb6c94a58(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9124d4f9e18565b33fbb8020ed518e95009e5430349bd226be7314b7051d3e57(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27d6bedd3a51e9ff78d5a28768be2a28a76998900449a9b76cf9ba4a41be3d2c(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b48e5b2504d3f36807bccdc085cb6d0f357a1d06635a88136da0225ab090485(
    *,
    stream_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c57882bea5ea967aefe650cda76dcd44bb8549c6523cf44f537f7e3782e60e3(
    *,
    current_mi_bps: typing.Optional[jsii.Number] = None,
    target_mi_bps: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
