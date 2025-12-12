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
    jsii_type="@aws-cdk/mixins-preview.aws_sqs.mixins.CfnQueueInlinePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "queue": "queue"},
)
class CfnQueueInlinePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        queue: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnQueueInlinePolicyPropsMixin.

        :param policy_document: A policy document that contains the permissions for the specified Amazon SQS queues. For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .
        :param queue: The URLs of the queues to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html)`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queueinlinepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sqs import mixins as sqs_mixins
            
            # policy_document: Any
            
            cfn_queue_inline_policy_mixin_props = sqs_mixins.CfnQueueInlinePolicyMixinProps(
                policy_document=policy_document,
                queue="queue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__053571c78be752eb77cf7a9e0f55b2f3064098d3a57ef326d62a56efb13d502a)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if queue is not None:
            self._values["queue"] = queue

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document that contains the permissions for the specified Amazon SQS queues.

        For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queueinlinepolicy.html#cfn-sqs-queueinlinepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def queue(self) -> typing.Optional[builtins.str]:
        '''The URLs of the queues to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sqs-queues.html)`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queueinlinepolicy.html#cfn-sqs-queueinlinepolicy-queue
        '''
        result = self._values.get("queue")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueInlinePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueueInlinePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sqs.mixins.CfnQueueInlinePolicyPropsMixin",
):
    '''The ``AWS::SQS::QueueInlinePolicy`` resource associates one Amazon SQS queue with one policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queueinlinepolicy.html
    :cloudformationResource: AWS::SQS::QueueInlinePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sqs import mixins as sqs_mixins
        
        # policy_document: Any
        
        cfn_queue_inline_policy_props_mixin = sqs_mixins.CfnQueueInlinePolicyPropsMixin(sqs_mixins.CfnQueueInlinePolicyMixinProps(
            policy_document=policy_document,
            queue="queue"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueueInlinePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SQS::QueueInlinePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417131eb648657657f65ce1caa872e6d6c4eff4333672e0fb102f3c2bc19aeb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd05728452d52157d00f8aff09e55e6d4f44e8af5a23bbb05f2182c025273716)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57a99846ac7528daa2847a2e73a5632e4ff4caf4fde40f73d142604108cd3d13)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueInlinePolicyMixinProps:
        return typing.cast(CfnQueueInlinePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sqs.mixins.CfnQueueMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content_based_deduplication": "contentBasedDeduplication",
        "deduplication_scope": "deduplicationScope",
        "delay_seconds": "delaySeconds",
        "fifo_queue": "fifoQueue",
        "fifo_throughput_limit": "fifoThroughputLimit",
        "kms_data_key_reuse_period_seconds": "kmsDataKeyReusePeriodSeconds",
        "kms_master_key_id": "kmsMasterKeyId",
        "maximum_message_size": "maximumMessageSize",
        "message_retention_period": "messageRetentionPeriod",
        "queue_name": "queueName",
        "receive_message_wait_time_seconds": "receiveMessageWaitTimeSeconds",
        "redrive_allow_policy": "redriveAllowPolicy",
        "redrive_policy": "redrivePolicy",
        "sqs_managed_sse_enabled": "sqsManagedSseEnabled",
        "tags": "tags",
        "visibility_timeout": "visibilityTimeout",
    },
)
class CfnQueueMixinProps:
    def __init__(
        self,
        *,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        deduplication_scope: typing.Optional[builtins.str] = None,
        delay_seconds: typing.Optional[jsii.Number] = None,
        fifo_queue: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        fifo_throughput_limit: typing.Optional[builtins.str] = None,
        kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        maximum_message_size: typing.Optional[jsii.Number] = None,
        message_retention_period: typing.Optional[jsii.Number] = None,
        queue_name: typing.Optional[builtins.str] = None,
        receive_message_wait_time_seconds: typing.Optional[jsii.Number] = None,
        redrive_allow_policy: typing.Any = None,
        redrive_policy: typing.Any = None,
        sqs_managed_sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        visibility_timeout: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnQueuePropsMixin.

        :param content_based_deduplication: For first-in-first-out (FIFO) queues, specifies whether to enable content-based deduplication. During the deduplication interval, Amazon SQS treats messages that are sent with identical content as duplicates and delivers only one copy of the message. For more information, see the ``ContentBasedDeduplication`` attribute for the ``[CreateQueue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)`` action in the *Amazon SQS API Reference* .
        :param deduplication_scope: For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level. Valid values are ``messageGroup`` and ``queue`` . To enable high throughput for a FIFO queue, set this attribute to ``messageGroup`` *and* set the ``FifoThroughputLimit`` attribute to ``perMessageGroupId`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .
        :param delay_seconds: The time in seconds for which the delivery of all messages in the queue is delayed. You can specify an integer value of ``0`` to ``900`` (15 minutes). The default value is ``0`` .
        :param fifo_queue: If set to true, creates a FIFO queue. If you don't specify this property, Amazon SQS creates a standard queue. For more information, see `Amazon SQS FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html>`_ in the *Amazon SQS Developer Guide* .
        :param fifo_throughput_limit: For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group. Valid values are ``perQueue`` and ``perMessageGroupId`` . To enable high throughput for a FIFO queue, set this attribute to ``perMessageGroupId`` *and* set the ``DeduplicationScope`` attribute to ``messageGroup`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .
        :param kms_data_key_reuse_period_seconds: The length of time in seconds for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS again. The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes). .. epigraph:: A shorter time period provides better security, but results in more calls to AWS , which might incur charges after Free Tier. For more information, see `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-how-does-the-data-key-reuse-period-work>`_ in the *Amazon SQS Developer Guide* .
        :param kms_master_key_id: The ID of an AWS Key Management Service (KMS) for Amazon SQS , or a custom KMS. To use the AWS managed KMS for Amazon SQS , specify a (default) alias ARN, alias name (for example ``alias/aws/sqs`` ), key ARN, or key ID. For more information, see the following: - `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html>`_ in the *Amazon SQS Developer Guide* - `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ in the *Amazon SQS API Reference* - `Request Parameters <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters>`_ in the *AWS Key Management Service API Reference* - The Key Management Service (KMS) section of the `Security best practices for AWS Key Management Service <https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html>`_ in the *AWS Key Management Service Developer Guide*
        :param maximum_message_size: The limit of how many bytes that a message can contain before Amazon SQS rejects it. You can specify an integer from 1,024 bytes (1 KiB) to 1,048,576 bytes (1 MiB). Default: 1,048,576 bytes (1 MiB).
        :param message_retention_period: The number of seconds that Amazon SQS retains a message. You can specify an integer value from ``60`` seconds (1 minute) to ``1,209,600`` seconds (14 days). The default value is ``345,600`` seconds (4 days).
        :param queue_name: A name for the queue. To create a FIFO queue, the name of your FIFO queue must end with the ``.fifo`` suffix. For more information, see `Amazon SQS FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html>`_ in the *Amazon SQS Developer Guide* . If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the queue name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ in the *CloudFormation User Guide* . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param receive_message_wait_time_seconds: Specifies the duration, in seconds, that the ReceiveMessage action call waits until a message is in the queue in order to include it in the response, rather than returning an empty response if a message isn't yet available. You can specify an integer from 1 to 20. Short polling is used as the default or when you specify 0 for this property. For more information, see `Consuming messages using long polling <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling>`_ in the *Amazon SQS Developer Guide* .
        :param redrive_allow_policy: The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues as a JSON object. The parameters are as follows: - ``redrivePermission`` : The permission type that defines which source queues can specify the current queue as the dead-letter queue. Valid values are: - ``allowAll`` : (Default) Any source queues in this AWS account in the same Region can specify this queue as the dead-letter queue. - ``denyAll`` : No source queues can specify this queue as the dead-letter queue. - ``byQueue`` : Only queues specified by the ``sourceQueueArns`` parameter can specify this queue as the dead-letter queue. - ``sourceQueueArns`` : The Amazon Resource Names (ARN)s of the source queues that can specify this queue as the dead-letter queue and redrive messages. You can specify this parameter only when the ``redrivePermission`` parameter is set to ``byQueue`` . You can specify up to 10 source queue ARNs. To allow more than 10 source queues to specify dead-letter queues, set the ``redrivePermission`` parameter to ``allowAll`` .
        :param redrive_policy: The string that includes the parameters for the dead-letter queue functionality of the source queue as a JSON object. The parameters are as follows: - ``deadLetterTargetArn`` : The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the value of ``maxReceiveCount`` is exceeded. - ``maxReceiveCount`` : The number of times a message is received by a consumer of the source queue before being moved to the dead-letter queue. When the ``ReceiveCount`` for a message exceeds the ``maxReceiveCount`` for a queue, Amazon SQS moves the message to the dead-letter-queue. .. epigraph:: The dead-letter queue of a FIFO queue must also be a FIFO queue. Similarly, the dead-letter queue of a standard queue must also be a standard queue. *JSON* ``{ "deadLetterTargetArn" : *String* , "maxReceiveCount" : *Integer* }`` *YAML* ``deadLetterTargetArn : *String*`` ``maxReceiveCount : *Integer*``
        :param sqs_managed_sse_enabled: Enables server-side queue encryption using SQS owned encryption keys. Only one server-side encryption option is supported per queue (for example, `SSE-KMS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sse-existing-queue.html>`_ or `SSE-SQS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sqs-sse-queue.html>`_ ). When ``SqsManagedSseEnabled`` is not defined, ``SSE-SQS`` encryption is enabled by default.
        :param tags: The tags that you attach to this queue. For more information, see `Resource tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *CloudFormation User Guide* .
        :param visibility_timeout: The length of time during which a message will be unavailable after a message is delivered from the queue. This blocks other components from receiving the same message and gives the initial component time to process and delete the message from the queue. Values must be from 0 to 43,200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds. For more information about Amazon SQS queue visibility timeouts, see `Visibility timeout <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sqs import mixins as sqs_mixins
            
            # redrive_allow_policy: Any
            # redrive_policy: Any
            
            cfn_queue_mixin_props = sqs_mixins.CfnQueueMixinProps(
                content_based_deduplication=False,
                deduplication_scope="deduplicationScope",
                delay_seconds=123,
                fifo_queue=False,
                fifo_throughput_limit="fifoThroughputLimit",
                kms_data_key_reuse_period_seconds=123,
                kms_master_key_id="kmsMasterKeyId",
                maximum_message_size=123,
                message_retention_period=123,
                queue_name="queueName",
                receive_message_wait_time_seconds=123,
                redrive_allow_policy=redrive_allow_policy,
                redrive_policy=redrive_policy,
                sqs_managed_sse_enabled=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                visibility_timeout=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05cfd28395c6a764a488eb3bbef1584680f92d239b1c12506573292bd66fd648)
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument deduplication_scope", value=deduplication_scope, expected_type=type_hints["deduplication_scope"])
            check_type(argname="argument delay_seconds", value=delay_seconds, expected_type=type_hints["delay_seconds"])
            check_type(argname="argument fifo_queue", value=fifo_queue, expected_type=type_hints["fifo_queue"])
            check_type(argname="argument fifo_throughput_limit", value=fifo_throughput_limit, expected_type=type_hints["fifo_throughput_limit"])
            check_type(argname="argument kms_data_key_reuse_period_seconds", value=kms_data_key_reuse_period_seconds, expected_type=type_hints["kms_data_key_reuse_period_seconds"])
            check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            check_type(argname="argument maximum_message_size", value=maximum_message_size, expected_type=type_hints["maximum_message_size"])
            check_type(argname="argument message_retention_period", value=message_retention_period, expected_type=type_hints["message_retention_period"])
            check_type(argname="argument queue_name", value=queue_name, expected_type=type_hints["queue_name"])
            check_type(argname="argument receive_message_wait_time_seconds", value=receive_message_wait_time_seconds, expected_type=type_hints["receive_message_wait_time_seconds"])
            check_type(argname="argument redrive_allow_policy", value=redrive_allow_policy, expected_type=type_hints["redrive_allow_policy"])
            check_type(argname="argument redrive_policy", value=redrive_policy, expected_type=type_hints["redrive_policy"])
            check_type(argname="argument sqs_managed_sse_enabled", value=sqs_managed_sse_enabled, expected_type=type_hints["sqs_managed_sse_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument visibility_timeout", value=visibility_timeout, expected_type=type_hints["visibility_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if deduplication_scope is not None:
            self._values["deduplication_scope"] = deduplication_scope
        if delay_seconds is not None:
            self._values["delay_seconds"] = delay_seconds
        if fifo_queue is not None:
            self._values["fifo_queue"] = fifo_queue
        if fifo_throughput_limit is not None:
            self._values["fifo_throughput_limit"] = fifo_throughput_limit
        if kms_data_key_reuse_period_seconds is not None:
            self._values["kms_data_key_reuse_period_seconds"] = kms_data_key_reuse_period_seconds
        if kms_master_key_id is not None:
            self._values["kms_master_key_id"] = kms_master_key_id
        if maximum_message_size is not None:
            self._values["maximum_message_size"] = maximum_message_size
        if message_retention_period is not None:
            self._values["message_retention_period"] = message_retention_period
        if queue_name is not None:
            self._values["queue_name"] = queue_name
        if receive_message_wait_time_seconds is not None:
            self._values["receive_message_wait_time_seconds"] = receive_message_wait_time_seconds
        if redrive_allow_policy is not None:
            self._values["redrive_allow_policy"] = redrive_allow_policy
        if redrive_policy is not None:
            self._values["redrive_policy"] = redrive_policy
        if sqs_managed_sse_enabled is not None:
            self._values["sqs_managed_sse_enabled"] = sqs_managed_sse_enabled
        if tags is not None:
            self._values["tags"] = tags
        if visibility_timeout is not None:
            self._values["visibility_timeout"] = visibility_timeout

    @builtins.property
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''For first-in-first-out (FIFO) queues, specifies whether to enable content-based deduplication.

        During the deduplication interval, Amazon SQS treats messages that are sent with identical content as duplicates and delivers only one copy of the message. For more information, see the ``ContentBasedDeduplication`` attribute for the ``[CreateQueue](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html)`` action in the *Amazon SQS API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-contentbaseddeduplication
        '''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def deduplication_scope(self) -> typing.Optional[builtins.str]:
        '''For high throughput for FIFO queues, specifies whether message deduplication occurs at the message group or queue level.

        Valid values are ``messageGroup`` and ``queue`` .

        To enable high throughput for a FIFO queue, set this attribute to ``messageGroup`` *and* set the ``FifoThroughputLimit`` attribute to ``perMessageGroupId`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-deduplicationscope
        '''
        result = self._values.get("deduplication_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delay_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time in seconds for which the delivery of all messages in the queue is delayed.

        You can specify an integer value of ``0`` to ``900`` (15 minutes). The default value is ``0`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-delayseconds
        '''
        result = self._values.get("delay_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fifo_queue(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If set to true, creates a FIFO queue.

        If you don't specify this property, Amazon SQS creates a standard queue. For more information, see `Amazon SQS FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-fifoqueue
        '''
        result = self._values.get("fifo_queue")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def fifo_throughput_limit(self) -> typing.Optional[builtins.str]:
        '''For high throughput for FIFO queues, specifies whether the FIFO queue throughput quota applies to the entire queue or per message group.

        Valid values are ``perQueue`` and ``perMessageGroupId`` .

        To enable high throughput for a FIFO queue, set this attribute to ``perMessageGroupId`` *and* set the ``DeduplicationScope`` attribute to ``messageGroup`` . If you set these attributes to anything other than these values, normal throughput is in effect and deduplication occurs as specified. For more information, see `High throughput for FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html>`_ and `Quotas related to messages <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-fifothroughputlimit
        '''
        result = self._values.get("fifo_throughput_limit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_data_key_reuse_period_seconds(self) -> typing.Optional[jsii.Number]:
        '''The length of time in seconds for which Amazon SQS can reuse a data key to encrypt or decrypt messages before calling AWS  again.

        The value must be an integer between 60 (1 minute) and 86,400 (24 hours). The default is 300 (5 minutes).
        .. epigraph::

           A shorter time period provides better security, but results in more calls to AWS  , which might incur charges after Free Tier. For more information, see `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html#sqs-how-does-the-data-key-reuse-period-work>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-kmsdatakeyreuseperiodseconds
        '''
        result = self._values.get("kms_data_key_reuse_period_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an AWS Key Management Service (KMS) for Amazon SQS , or a custom KMS.

        To use the AWS managed KMS for Amazon SQS , specify a (default) alias ARN, alias name (for example ``alias/aws/sqs`` ), key ARN, or key ID. For more information, see the following:

        - `Encryption at rest <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-server-side-encryption.html>`_ in the *Amazon SQS Developer Guide*
        - `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ in the *Amazon SQS API Reference*
        - `Request Parameters <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters>`_ in the *AWS Key Management Service API Reference*
        - The Key Management Service (KMS) section of the `Security best practices for AWS Key Management Service <https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html>`_ in the *AWS Key Management Service Developer Guide*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-kmsmasterkeyid
        '''
        result = self._values.get("kms_master_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maximum_message_size(self) -> typing.Optional[jsii.Number]:
        '''The limit of how many bytes that a message can contain before Amazon SQS rejects it.

        You can specify an integer from 1,024 bytes (1 KiB) to 1,048,576 bytes (1 MiB).
        Default: 1,048,576 bytes (1 MiB).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-maximummessagesize
        '''
        result = self._values.get("maximum_message_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def message_retention_period(self) -> typing.Optional[jsii.Number]:
        '''The number of seconds that Amazon SQS retains a message.

        You can specify an integer value from ``60`` seconds (1 minute) to ``1,209,600`` seconds (14 days). The default value is ``345,600`` seconds (4 days).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-messageretentionperiod
        '''
        result = self._values.get("message_retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def queue_name(self) -> typing.Optional[builtins.str]:
        '''A name for the queue.

        To create a FIFO queue, the name of your FIFO queue must end with the ``.fifo`` suffix. For more information, see `Amazon SQS FIFO queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html>`_ in the *Amazon SQS Developer Guide* .

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the queue name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ in the *CloudFormation User Guide* .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-queuename
        '''
        result = self._values.get("queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def receive_message_wait_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''Specifies the duration, in seconds, that the ReceiveMessage action call waits until a message is in the queue in order to include it in the response, rather than returning an empty response if a message isn't yet available.

        You can specify an integer from 1 to 20. Short polling is used as the default or when you specify 0 for this property. For more information, see `Consuming messages using long polling <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html#sqs-long-polling>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-receivemessagewaittimeseconds
        '''
        result = self._values.get("receive_message_wait_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def redrive_allow_policy(self) -> typing.Any:
        '''The string that includes the parameters for the permissions for the dead-letter queue redrive permission and which source queues can specify dead-letter queues as a JSON object.

        The parameters are as follows:

        - ``redrivePermission`` : The permission type that defines which source queues can specify the current queue as the dead-letter queue. Valid values are:
        - ``allowAll`` : (Default) Any source queues in this AWS account in the same Region can specify this queue as the dead-letter queue.
        - ``denyAll`` : No source queues can specify this queue as the dead-letter queue.
        - ``byQueue`` : Only queues specified by the ``sourceQueueArns`` parameter can specify this queue as the dead-letter queue.
        - ``sourceQueueArns`` : The Amazon Resource Names (ARN)s of the source queues that can specify this queue as the dead-letter queue and redrive messages. You can specify this parameter only when the ``redrivePermission`` parameter is set to ``byQueue`` . You can specify up to 10 source queue ARNs. To allow more than 10 source queues to specify dead-letter queues, set the ``redrivePermission`` parameter to ``allowAll`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-redriveallowpolicy
        '''
        result = self._values.get("redrive_allow_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        '''The string that includes the parameters for the dead-letter queue functionality of the source queue as a JSON object.

        The parameters are as follows:

        - ``deadLetterTargetArn`` : The Amazon Resource Name (ARN) of the dead-letter queue to which Amazon SQS moves messages after the value of ``maxReceiveCount`` is exceeded.
        - ``maxReceiveCount`` : The number of times a message is received by a consumer of the source queue before being moved to the dead-letter queue. When the ``ReceiveCount`` for a message exceeds the ``maxReceiveCount`` for a queue, Amazon SQS moves the message to the dead-letter-queue.

        .. epigraph::

           The dead-letter queue of a FIFO queue must also be a FIFO queue. Similarly, the dead-letter queue of a standard queue must also be a standard queue.

        *JSON*

        ``{ "deadLetterTargetArn" : *String* , "maxReceiveCount" : *Integer* }``

        *YAML*

        ``deadLetterTargetArn : *String*``

        ``maxReceiveCount : *Integer*``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-redrivepolicy
        '''
        result = self._values.get("redrive_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def sqs_managed_sse_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables server-side queue encryption using SQS owned encryption keys.

        Only one server-side encryption option is supported per queue (for example, `SSE-KMS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sse-existing-queue.html>`_ or `SSE-SQS <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-sqs-sse-queue.html>`_ ). When ``SqsManagedSseEnabled`` is not defined, ``SSE-SQS`` encryption is enabled by default.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-sqsmanagedsseenabled
        '''
        result = self._values.get("sqs_managed_sse_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags that you attach to this queue.

        For more information, see `Resource tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *CloudFormation User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def visibility_timeout(self) -> typing.Optional[jsii.Number]:
        '''The length of time during which a message will be unavailable after a message is delivered from the queue.

        This blocks other components from receiving the same message and gives the initial component time to process and delete the message from the queue.

        Values must be from 0 to 43,200 seconds (12 hours). If you don't specify a value, AWS CloudFormation uses the default value of 30 seconds.

        For more information about Amazon SQS queue visibility timeouts, see `Visibility timeout <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html#cfn-sqs-queue-visibilitytimeout
        '''
        result = self._values.get("visibility_timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sqs.mixins.CfnQueuePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "queues": "queues"},
)
class CfnQueuePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        queues: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnQueuePolicyPropsMixin.

        :param policy_document: A policy document that contains the permissions for the specified Amazon SQS queues. For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .
        :param queues: The URLs of the queues to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html)`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queuepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sqs import mixins as sqs_mixins
            
            # policy_document: Any
            
            cfn_queue_policy_mixin_props = sqs_mixins.CfnQueuePolicyMixinProps(
                policy_document=policy_document,
                queues=["queues"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad310ea126b13e9be680af6468d9c20a48e10bd1067c15519a26432f66a64bcb)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument queues", value=queues, expected_type=type_hints["queues"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if queues is not None:
            self._values["queues"] = queues

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document that contains the permissions for the specified Amazon SQS queues.

        For more information about Amazon SQS policies, see `Using custom policies with the Amazon SQS access policy language <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-creating-custom-policies.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queuepolicy.html#cfn-sqs-queuepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def queues(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The URLs of the queues to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html)`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queuepolicy.html#cfn-sqs-queuepolicy-queues
        '''
        result = self._values.get("queues")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueuePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueuePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sqs.mixins.CfnQueuePolicyPropsMixin",
):
    '''The ``AWS::SQS::QueuePolicy`` type applies a policy to Amazon SQS queues.

    For an example snippet, see `Declaring an Amazon SQS policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-sqs-policy>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queuepolicy.html
    :cloudformationResource: AWS::SQS::QueuePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sqs import mixins as sqs_mixins
        
        # policy_document: Any
        
        cfn_queue_policy_props_mixin = sqs_mixins.CfnQueuePolicyPropsMixin(sqs_mixins.CfnQueuePolicyMixinProps(
            policy_document=policy_document,
            queues=["queues"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueuePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SQS::QueuePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd92cd85dacc700e3ceb12b24188a3f207611e51df5754c2e4d808320056ed3a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c48055d6f33e14b855387906ff9a0fa7b286784266a9e81fc9b17c0b01a33ea5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3f258e2498d4a6d7a2349108fe6eeeb81e7b582da94b7094a90e870b7fc664e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueuePolicyMixinProps:
        return typing.cast(CfnQueuePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnQueuePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sqs.mixins.CfnQueuePropsMixin",
):
    '''The ``AWS::SQS::Queue`` resource creates an Amazon SQS standard or FIFO queue.

    Keep the following caveats in mind:

    - If you don't specify the ``FifoQueue`` property, Amazon SQS creates a standard queue.

    .. epigraph::

       You can't change the queue type after you create it and you can't convert an existing standard queue into a FIFO queue. You must either create a new FIFO queue for your application or delete your existing standard queue and recreate it as a FIFO queue. For more information, see `Moving from a standard queue to a FIFO queue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-moving.html>`_ in the *Amazon SQS Developer Guide* .

    - If you don't provide a value for a property, the queue is created with the default value for the property.
    - If you delete a queue, you must wait at least 60 seconds before creating a queue with the same name.
    - To successfully create a new queue, you must provide a queue name that adheres to the `limits related to queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/limits-queues.html>`_ and is unique within the scope of your queues.

    For more information about creating FIFO (first-in-first-out) queues, see `Creating an Amazon SQS queue ( CloudFormation ) <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/create-queue-cloudformation.html>`_ in the *Amazon SQS Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sqs-queue.html
    :cloudformationResource: AWS::SQS::Queue
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sqs import mixins as sqs_mixins
        
        # redrive_allow_policy: Any
        # redrive_policy: Any
        
        cfn_queue_props_mixin = sqs_mixins.CfnQueuePropsMixin(sqs_mixins.CfnQueueMixinProps(
            content_based_deduplication=False,
            deduplication_scope="deduplicationScope",
            delay_seconds=123,
            fifo_queue=False,
            fifo_throughput_limit="fifoThroughputLimit",
            kms_data_key_reuse_period_seconds=123,
            kms_master_key_id="kmsMasterKeyId",
            maximum_message_size=123,
            message_retention_period=123,
            queue_name="queueName",
            receive_message_wait_time_seconds=123,
            redrive_allow_policy=redrive_allow_policy,
            redrive_policy=redrive_policy,
            sqs_managed_sse_enabled=False,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            visibility_timeout=123
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
        '''Create a mixin to apply properties to ``AWS::SQS::Queue``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f5e85a31d85ed48a07aa3786f26deffb76fc8268caa5484e9797bbaaafa230)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dadd2273219d2acb0546813a11153fd06d7f8ec681eb49b247f6a6a3618fa1b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f5e05f0e77e7a0f486650d71feae7af85dbd5a5be22888c7cb021f4a47b6c2)
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


__all__ = [
    "CfnQueueInlinePolicyMixinProps",
    "CfnQueueInlinePolicyPropsMixin",
    "CfnQueueMixinProps",
    "CfnQueuePolicyMixinProps",
    "CfnQueuePolicyPropsMixin",
    "CfnQueuePropsMixin",
]

publication.publish()

def _typecheckingstub__053571c78be752eb77cf7a9e0f55b2f3064098d3a57ef326d62a56efb13d502a(
    *,
    policy_document: typing.Any = None,
    queue: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417131eb648657657f65ce1caa872e6d6c4eff4333672e0fb102f3c2bc19aeb5(
    props: typing.Union[CfnQueueInlinePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd05728452d52157d00f8aff09e55e6d4f44e8af5a23bbb05f2182c025273716(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a99846ac7528daa2847a2e73a5632e4ff4caf4fde40f73d142604108cd3d13(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05cfd28395c6a764a488eb3bbef1584680f92d239b1c12506573292bd66fd648(
    *,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    deduplication_scope: typing.Optional[builtins.str] = None,
    delay_seconds: typing.Optional[jsii.Number] = None,
    fifo_queue: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    fifo_throughput_limit: typing.Optional[builtins.str] = None,
    kms_data_key_reuse_period_seconds: typing.Optional[jsii.Number] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    maximum_message_size: typing.Optional[jsii.Number] = None,
    message_retention_period: typing.Optional[jsii.Number] = None,
    queue_name: typing.Optional[builtins.str] = None,
    receive_message_wait_time_seconds: typing.Optional[jsii.Number] = None,
    redrive_allow_policy: typing.Any = None,
    redrive_policy: typing.Any = None,
    sqs_managed_sse_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    visibility_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad310ea126b13e9be680af6468d9c20a48e10bd1067c15519a26432f66a64bcb(
    *,
    policy_document: typing.Any = None,
    queues: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd92cd85dacc700e3ceb12b24188a3f207611e51df5754c2e4d808320056ed3a(
    props: typing.Union[CfnQueuePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48055d6f33e14b855387906ff9a0fa7b286784266a9e81fc9b17c0b01a33ea5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3f258e2498d4a6d7a2349108fe6eeeb81e7b582da94b7094a90e870b7fc664e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f5e85a31d85ed48a07aa3786f26deffb76fc8268caa5484e9797bbaaafa230(
    props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dadd2273219d2acb0546813a11153fd06d7f8ec681eb49b247f6a6a3618fa1b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f5e05f0e77e7a0f486650d71feae7af85dbd5a5be22888c7cb021f4a47b6c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
