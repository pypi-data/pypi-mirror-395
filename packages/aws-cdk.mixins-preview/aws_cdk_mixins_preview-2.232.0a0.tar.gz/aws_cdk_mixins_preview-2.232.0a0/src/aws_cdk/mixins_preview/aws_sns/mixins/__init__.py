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
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnSubscriptionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_policy": "deliveryPolicy",
        "endpoint": "endpoint",
        "filter_policy": "filterPolicy",
        "filter_policy_scope": "filterPolicyScope",
        "protocol": "protocol",
        "raw_message_delivery": "rawMessageDelivery",
        "redrive_policy": "redrivePolicy",
        "region": "region",
        "replay_policy": "replayPolicy",
        "subscription_role_arn": "subscriptionRoleArn",
        "topic_arn": "topicArn",
    },
)
class CfnSubscriptionMixinProps:
    def __init__(
        self,
        *,
        delivery_policy: typing.Any = None,
        endpoint: typing.Optional[builtins.str] = None,
        filter_policy: typing.Any = None,
        filter_policy_scope: typing.Optional[builtins.str] = None,
        protocol: typing.Optional[builtins.str] = None,
        raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        redrive_policy: typing.Any = None,
        region: typing.Optional[builtins.str] = None,
        replay_policy: typing.Any = None,
        subscription_role_arn: typing.Optional[builtins.str] = None,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSubscriptionPropsMixin.

        :param delivery_policy: The delivery policy JSON assigned to the subscription. Enables the subscriber to define the message delivery retry strategy in the case of an HTTP/S endpoint subscribed to the topic. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon API Reference* and `Message delivery retries <https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html>`_ in the *Amazon Developer Guide* .
        :param endpoint: The subscription's endpoint. The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon API Reference* .
        :param filter_policy: The filter policy JSON assigned to the subscription. Enables the subscriber to filter out unwanted messages. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon API Reference* and `Message filtering <https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html>`_ in the *Amazon Developer Guide* .
        :param filter_policy_scope: This attribute lets you choose the filtering scope by using one of the following string value types:. - ``MessageAttributes`` (default) - The filter is applied on the message attributes. - ``MessageBody`` - The filter is applied on the message body. .. epigraph:: ``Null`` is not a valid value for ``FilterPolicyScope`` . To delete a filter policy, delete the ``FilterPolicy`` property but keep ``FilterPolicyScope`` property as is.
        :param protocol: The subscription's protocol. For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon API Reference* .
        :param raw_message_delivery: When set to ``true`` , enables raw message delivery. Raw messages don't contain any JSON formatting and can be sent to Amazon SQS and HTTP/S endpoints. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon API Reference* .
        :param redrive_policy: When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue. Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is unreachable) or server errors (for example, when the service that powers the subscribed endpoint becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing. For more information about the redrive policy and dead-letter queues, see `Amazon SQS dead-letter queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>`_ in the *Amazon SQS Developer Guide* .
        :param region: For cross-region subscriptions, the region in which the topic resides. If no region is specified, CloudFormation uses the region of the caller as the default. If you perform an update operation that only updates the ``Region`` property of a ``AWS::SNS::Subscription`` resource, that operation will fail unless you are either: - Updating the ``Region`` from ``NULL`` to the caller region. - Updating the ``Region`` from the caller region to ``NULL`` .
        :param replay_policy: Specifies whether Amazon resends the notification to the subscription when a message's attribute changes.
        :param subscription_role_arn: This property applies only to Amazon Data Firehose delivery stream subscriptions. Specify the ARN of the IAM role that has the following: - Permission to write to the Amazon Data Firehose delivery stream - Amazon listed as a trusted entity Specifying a valid ARN for this attribute is required for Firehose delivery stream subscriptions. For more information, see `Fanout to Amazon Data Firehose delivery streams <https://docs.aws.amazon.com/sns/latest/dg/sns-firehose-as-subscriber.html>`_ in the *Amazon Developer Guide.*
        :param topic_arn: The ARN of the topic to subscribe to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
            
            # delivery_policy: Any
            # filter_policy: Any
            # redrive_policy: Any
            # replay_policy: Any
            
            cfn_subscription_mixin_props = sns_mixins.CfnSubscriptionMixinProps(
                delivery_policy=delivery_policy,
                endpoint="endpoint",
                filter_policy=filter_policy,
                filter_policy_scope="filterPolicyScope",
                protocol="protocol",
                raw_message_delivery=False,
                redrive_policy=redrive_policy,
                region="region",
                replay_policy=replay_policy,
                subscription_role_arn="subscriptionRoleArn",
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5520cd517bbea5f6e383753478f47fcb47f305c3dfad2e29ae34525156ab55f5)
            check_type(argname="argument delivery_policy", value=delivery_policy, expected_type=type_hints["delivery_policy"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument filter_policy", value=filter_policy, expected_type=type_hints["filter_policy"])
            check_type(argname="argument filter_policy_scope", value=filter_policy_scope, expected_type=type_hints["filter_policy_scope"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument raw_message_delivery", value=raw_message_delivery, expected_type=type_hints["raw_message_delivery"])
            check_type(argname="argument redrive_policy", value=redrive_policy, expected_type=type_hints["redrive_policy"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument replay_policy", value=replay_policy, expected_type=type_hints["replay_policy"])
            check_type(argname="argument subscription_role_arn", value=subscription_role_arn, expected_type=type_hints["subscription_role_arn"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_policy is not None:
            self._values["delivery_policy"] = delivery_policy
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if filter_policy is not None:
            self._values["filter_policy"] = filter_policy
        if filter_policy_scope is not None:
            self._values["filter_policy_scope"] = filter_policy_scope
        if protocol is not None:
            self._values["protocol"] = protocol
        if raw_message_delivery is not None:
            self._values["raw_message_delivery"] = raw_message_delivery
        if redrive_policy is not None:
            self._values["redrive_policy"] = redrive_policy
        if region is not None:
            self._values["region"] = region
        if replay_policy is not None:
            self._values["replay_policy"] = replay_policy
        if subscription_role_arn is not None:
            self._values["subscription_role_arn"] = subscription_role_arn
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def delivery_policy(self) -> typing.Any:
        '''The delivery policy JSON assigned to the subscription.

        Enables the subscriber to define the message delivery retry strategy in the case of an HTTP/S endpoint subscribed to the topic. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon  API Reference* and `Message delivery retries <https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html>`_ in the *Amazon  Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
        '''
        result = self._values.get("delivery_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''The subscription's endpoint.

        The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon  API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-endpoint
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_policy(self) -> typing.Any:
        '''The filter policy JSON assigned to the subscription.

        Enables the subscriber to filter out unwanted messages. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon  API Reference* and `Message filtering <https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html>`_ in the *Amazon  Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
        '''
        result = self._values.get("filter_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def filter_policy_scope(self) -> typing.Optional[builtins.str]:
        '''This attribute lets you choose the filtering scope by using one of the following string value types:.

        - ``MessageAttributes`` (default) - The filter is applied on the message attributes.
        - ``MessageBody`` - The filter is applied on the message body.

        .. epigraph::

           ``Null`` is not a valid value for ``FilterPolicyScope`` . To delete a filter policy, delete the ``FilterPolicy`` property but keep ``FilterPolicyScope`` property as is.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicyscope
        '''
        result = self._values.get("filter_policy_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The subscription's protocol.

        For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon  API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def raw_message_delivery(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''When set to ``true`` , enables raw message delivery.

        Raw messages don't contain any JSON formatting and can be sent to Amazon SQS and HTTP/S endpoints. For more information, see ``[GetSubscriptionAttributes](https://docs.aws.amazon.com/sns/latest/api/API_GetSubscriptionAttributes.html)`` in the *Amazon  API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
        '''
        result = self._values.get("raw_message_delivery")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def redrive_policy(self) -> typing.Any:
        '''When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue.

        Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is unreachable) or server errors (for example, when the service that powers the subscribed endpoint becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing.

        For more information about the redrive policy and dead-letter queues, see `Amazon SQS dead-letter queues <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>`_ in the *Amazon SQS Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-redrivepolicy
        '''
        result = self._values.get("redrive_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''For cross-region subscriptions, the region in which the topic resides.

        If no region is specified, CloudFormation uses the region of the caller as the default.

        If you perform an update operation that only updates the ``Region`` property of a ``AWS::SNS::Subscription`` resource, that operation will fail unless you are either:

        - Updating the ``Region`` from ``NULL`` to the caller region.
        - Updating the ``Region`` from the caller region to ``NULL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replay_policy(self) -> typing.Any:
        '''Specifies whether Amazon  resends the notification to the subscription when a message's attribute changes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-replaypolicy
        '''
        result = self._values.get("replay_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def subscription_role_arn(self) -> typing.Optional[builtins.str]:
        '''This property applies only to Amazon Data Firehose delivery stream subscriptions.

        Specify the ARN of the IAM role that has the following:

        - Permission to write to the Amazon Data Firehose delivery stream
        - Amazon  listed as a trusted entity

        Specifying a valid ARN for this attribute is required for Firehose delivery stream subscriptions. For more information, see `Fanout to Amazon Data Firehose delivery streams <https://docs.aws.amazon.com/sns/latest/dg/sns-firehose-as-subscriber.html>`_ in the *Amazon  Developer Guide.*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-subscriptionrolearn
        '''
        result = self._values.get("subscription_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the topic to subscribe to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriptionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnSubscriptionPropsMixin",
):
    '''The ``AWS::SNS::Subscription`` resource subscribes an endpoint to an Amazon  topic.

    For a subscription to be created, the owner of the endpoint must` confirm the subscription.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
    :cloudformationResource: AWS::SNS::Subscription
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
        
        # delivery_policy: Any
        # filter_policy: Any
        # redrive_policy: Any
        # replay_policy: Any
        
        cfn_subscription_props_mixin = sns_mixins.CfnSubscriptionPropsMixin(sns_mixins.CfnSubscriptionMixinProps(
            delivery_policy=delivery_policy,
            endpoint="endpoint",
            filter_policy=filter_policy,
            filter_policy_scope="filterPolicyScope",
            protocol="protocol",
            raw_message_delivery=False,
            redrive_policy=redrive_policy,
            region="region",
            replay_policy=replay_policy,
            subscription_role_arn="subscriptionRoleArn",
            topic_arn="topicArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SNS::Subscription``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed90e5347327afd84275344faab507b2b80fd3cb0700fa5ec4304e9fed4e9006)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27ddcd8156c394442b17a5e447433761c4470d744166f84c7718d2e7e1b15c63)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd6e0f0fe00ef6e35d69f1c381999a846ed0f5fe474ae3669151818b2556ee5f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriptionMixinProps:
        return typing.cast(CfnSubscriptionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicInlinePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "topic_arn": "topicArn"},
)
class CfnTopicInlinePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTopicInlinePolicyPropsMixin.

        :param policy_document: A policy document that contains permissions to add to the specified Amazon topic.
        :param topic_arn: The Amazon Resource Name (ARN) of the topic to which you want to add the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicinlinepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
            
            # policy_document: Any
            
            cfn_topic_inline_policy_mixin_props = sns_mixins.CfnTopicInlinePolicyMixinProps(
                policy_document=policy_document,
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f9f3c7587fd220fcd572dedb2bbee7bdd891bfc485c51e4885a6ab7fa83543f)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document that contains permissions to add to the specified Amazon  topic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicinlinepolicy.html#cfn-sns-topicinlinepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the topic to which you want to add the policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicinlinepolicy.html#cfn-sns-topicinlinepolicy-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicInlinePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTopicInlinePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicInlinePolicyPropsMixin",
):
    '''The ``AWS::SNS::TopicInlinePolicy`` resource associates one Amazon  topic with one policy.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicinlinepolicy.html
    :cloudformationResource: AWS::SNS::TopicInlinePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
        
        # policy_document: Any
        
        cfn_topic_inline_policy_props_mixin = sns_mixins.CfnTopicInlinePolicyPropsMixin(sns_mixins.CfnTopicInlinePolicyMixinProps(
            policy_document=policy_document,
            topic_arn="topicArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTopicInlinePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SNS::TopicInlinePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ac80900efedc798e9dedd8e853a93ef0de232f8bbc012bdb349507333d28c28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37a613d0720b4bca229070367bfd4862e3a9ebba05ad25fa819cfcd5ab98f958)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7ea050c525b06b8967ef4e1ea87055fd25513a53c52ba2652ac2455c2689cac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTopicInlinePolicyMixinProps:
        return typing.cast(CfnTopicInlinePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "archive_policy": "archivePolicy",
        "content_based_deduplication": "contentBasedDeduplication",
        "data_protection_policy": "dataProtectionPolicy",
        "delivery_status_logging": "deliveryStatusLogging",
        "display_name": "displayName",
        "fifo_throughput_scope": "fifoThroughputScope",
        "fifo_topic": "fifoTopic",
        "kms_master_key_id": "kmsMasterKeyId",
        "signature_version": "signatureVersion",
        "subscription": "subscription",
        "tags": "tags",
        "topic_name": "topicName",
        "tracing_config": "tracingConfig",
    },
)
class CfnTopicMixinProps:
    def __init__(
        self,
        *,
        archive_policy: typing.Any = None,
        content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        data_protection_policy: typing.Any = None,
        delivery_status_logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTopicPropsMixin.LoggingConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        display_name: typing.Optional[builtins.str] = None,
        fifo_throughput_scope: typing.Optional[builtins.str] = None,
        fifo_topic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_master_key_id: typing.Optional[builtins.str] = None,
        signature_version: typing.Optional[builtins.str] = None,
        subscription: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTopicPropsMixin.SubscriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        topic_name: typing.Optional[builtins.str] = None,
        tracing_config: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTopicPropsMixin.

        :param archive_policy: The ``ArchivePolicy`` determines the number of days Amazon retains messages in FIFO topics. You can set a retention period ranging from 1 to 365 days. This property is only applicable to FIFO topics; attempting to use it with standard topics will result in a creation failure.
        :param content_based_deduplication: ``ContentBasedDeduplication`` enables deduplication of messages based on their content for FIFO topics. By default, this property is set to false. If you create a FIFO topic with ``ContentBasedDeduplication`` set to false, you must provide a ``MessageDeduplicationId`` for each ``Publish`` action. When set to true, Amazon automatically generates a ``MessageDeduplicationId`` using a SHA-256 hash of the message body (excluding message attributes). You can optionally override this generated value by specifying a ``MessageDeduplicationId`` in the ``Publish`` action. Note that this property only applies to FIFO topics; using it with standard topics will cause the creation to fail.
        :param data_protection_policy: The body of the policy document you want to use for this topic. You can only add one policy per topic. The policy must be in JSON string format. Length Constraints: Maximum length of 30,720.
        :param delivery_status_logging: The ``DeliveryStatusLogging`` configuration enables you to log the delivery status of messages sent from your Amazon SNS topic to subscribed endpoints with the following supported delivery protocols:. - HTTP - Amazon Kinesis Data Firehose - AWS Lambda - Platform application endpoint - Amazon Simple Queue Service Once configured, log entries are sent to Amazon CloudWatch Logs.
        :param display_name: The display name to use for an Amazon topic with SMS subscriptions. The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.
        :param fifo_throughput_scope: Specifies the throughput quota and deduplication behavior to apply for the FIFO topic. Valid values are ``Topic`` or ``MessageGroup`` .
        :param fifo_topic: Set to true to create a FIFO topic.
        :param kms_master_key_id: The ID of an AWS managed customer master key (CMK) for Amazon or a custom CMK. For more information, see `Key terms <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms>`_ . For more examples, see ``[KeyId](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters)`` in the *AWS Key Management Service API Reference* . This property applies only to `server-side-encryption <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html>`_ .
        :param signature_version: The signature version corresponds to the hashing algorithm used while creating the signature of the notifications, subscription confirmations, or unsubscribe confirmation messages sent by Amazon SNS. By default, ``SignatureVersion`` is set to ``1`` .
        :param subscription: The Amazon subscriptions (endpoints) for this topic. .. epigraph:: If you specify the ``Subscription`` property in the ``AWS::SNS::Topic`` resource and it creates an associated subscription resource, the associated subscription is not deleted when the ``AWS::SNS::Topic`` resource is deleted.
        :param tags: The list of tags to add to a new topic. .. epigraph:: To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.
        :param topic_name: The name of the topic you want to create. Topic names must include only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long. FIFO topic names must end with ``.fifo`` . If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param tracing_config: Tracing mode of an Amazon topic. By default ``TracingConfig`` is set to ``PassThrough`` , and the topic passes through the tracing header it receives from an Amazon publisher to its subscriptions. If set to ``Active`` , Amazon will vend X-Ray segment data to topic owner account if the sampled flag in the tracing header is true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
            
            # archive_policy: Any
            # data_protection_policy: Any
            
            cfn_topic_mixin_props = sns_mixins.CfnTopicMixinProps(
                archive_policy=archive_policy,
                content_based_deduplication=False,
                data_protection_policy=data_protection_policy,
                delivery_status_logging=[sns_mixins.CfnTopicPropsMixin.LoggingConfigProperty(
                    failure_feedback_role_arn="failureFeedbackRoleArn",
                    protocol="protocol",
                    success_feedback_role_arn="successFeedbackRoleArn",
                    success_feedback_sample_rate="successFeedbackSampleRate"
                )],
                display_name="displayName",
                fifo_throughput_scope="fifoThroughputScope",
                fifo_topic=False,
                kms_master_key_id="kmsMasterKeyId",
                signature_version="signatureVersion",
                subscription=[sns_mixins.CfnTopicPropsMixin.SubscriptionProperty(
                    endpoint="endpoint",
                    protocol="protocol"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                topic_name="topicName",
                tracing_config="tracingConfig"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe6b7e291779768d4a945a8312ecc3420de13e93369d811ab118cc71d258960)
            check_type(argname="argument archive_policy", value=archive_policy, expected_type=type_hints["archive_policy"])
            check_type(argname="argument content_based_deduplication", value=content_based_deduplication, expected_type=type_hints["content_based_deduplication"])
            check_type(argname="argument data_protection_policy", value=data_protection_policy, expected_type=type_hints["data_protection_policy"])
            check_type(argname="argument delivery_status_logging", value=delivery_status_logging, expected_type=type_hints["delivery_status_logging"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument fifo_throughput_scope", value=fifo_throughput_scope, expected_type=type_hints["fifo_throughput_scope"])
            check_type(argname="argument fifo_topic", value=fifo_topic, expected_type=type_hints["fifo_topic"])
            check_type(argname="argument kms_master_key_id", value=kms_master_key_id, expected_type=type_hints["kms_master_key_id"])
            check_type(argname="argument signature_version", value=signature_version, expected_type=type_hints["signature_version"])
            check_type(argname="argument subscription", value=subscription, expected_type=type_hints["subscription"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
            check_type(argname="argument tracing_config", value=tracing_config, expected_type=type_hints["tracing_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if archive_policy is not None:
            self._values["archive_policy"] = archive_policy
        if content_based_deduplication is not None:
            self._values["content_based_deduplication"] = content_based_deduplication
        if data_protection_policy is not None:
            self._values["data_protection_policy"] = data_protection_policy
        if delivery_status_logging is not None:
            self._values["delivery_status_logging"] = delivery_status_logging
        if display_name is not None:
            self._values["display_name"] = display_name
        if fifo_throughput_scope is not None:
            self._values["fifo_throughput_scope"] = fifo_throughput_scope
        if fifo_topic is not None:
            self._values["fifo_topic"] = fifo_topic
        if kms_master_key_id is not None:
            self._values["kms_master_key_id"] = kms_master_key_id
        if signature_version is not None:
            self._values["signature_version"] = signature_version
        if subscription is not None:
            self._values["subscription"] = subscription
        if tags is not None:
            self._values["tags"] = tags
        if topic_name is not None:
            self._values["topic_name"] = topic_name
        if tracing_config is not None:
            self._values["tracing_config"] = tracing_config

    @builtins.property
    def archive_policy(self) -> typing.Any:
        '''The ``ArchivePolicy`` determines the number of days Amazon  retains messages in FIFO topics.

        You can set a retention period ranging from 1 to 365 days. This property is only applicable to FIFO topics; attempting to use it with standard topics will result in a creation failure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-archivepolicy
        '''
        result = self._values.get("archive_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def content_based_deduplication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''``ContentBasedDeduplication`` enables deduplication of messages based on their content for FIFO topics.

        By default, this property is set to false. If you create a FIFO topic with ``ContentBasedDeduplication`` set to false, you must provide a ``MessageDeduplicationId`` for each ``Publish`` action. When set to true, Amazon  automatically generates a ``MessageDeduplicationId`` using a SHA-256 hash of the message body (excluding message attributes). You can optionally override this generated value by specifying a ``MessageDeduplicationId`` in the ``Publish`` action. Note that this property only applies to FIFO topics; using it with standard topics will cause the creation to fail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-contentbaseddeduplication
        '''
        result = self._values.get("content_based_deduplication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def data_protection_policy(self) -> typing.Any:
        '''The body of the policy document you want to use for this topic.

        You can only add one policy per topic.

        The policy must be in JSON string format.

        Length Constraints: Maximum length of 30,720.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-dataprotectionpolicy
        '''
        result = self._values.get("data_protection_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def delivery_status_logging(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTopicPropsMixin.LoggingConfigProperty"]]]]:
        '''The ``DeliveryStatusLogging`` configuration enables you to log the delivery status of messages sent from your Amazon SNS topic to subscribed endpoints with the following supported delivery protocols:.

        - HTTP
        - Amazon Kinesis Data Firehose
        - AWS Lambda
        - Platform application endpoint
        - Amazon Simple Queue Service

        Once configured, log entries are sent to Amazon CloudWatch Logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-deliverystatuslogging
        '''
        result = self._values.get("delivery_status_logging")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTopicPropsMixin.LoggingConfigProperty"]]]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name to use for an Amazon  topic with SMS subscriptions.

        The display name must be maximum 100 characters long, including hyphens (-), underscores (_), spaces, and tabs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fifo_throughput_scope(self) -> typing.Optional[builtins.str]:
        '''Specifies the throughput quota and deduplication behavior to apply for the FIFO topic.

        Valid values are ``Topic`` or ``MessageGroup`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-fifothroughputscope
        '''
        result = self._values.get("fifo_throughput_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fifo_topic(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Set to true to create a FIFO topic.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-fifotopic
        '''
        result = self._values.get("fifo_topic")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_master_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an AWS managed customer master key (CMK) for Amazon  or a custom CMK.

        For more information, see `Key terms <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html#sse-key-terms>`_ . For more examples, see ``[KeyId](https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html#API_DescribeKey_RequestParameters)`` in the *AWS Key Management Service API Reference* .

        This property applies only to `server-side-encryption <https://docs.aws.amazon.com/sns/latest/dg/sns-server-side-encryption.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
        '''
        result = self._values.get("kms_master_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signature_version(self) -> typing.Optional[builtins.str]:
        '''The signature version corresponds to the hashing algorithm used while creating the signature of the notifications, subscription confirmations, or unsubscribe confirmation messages sent by Amazon SNS.

        By default, ``SignatureVersion`` is set to ``1`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-signatureversion
        '''
        result = self._values.get("signature_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subscription(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTopicPropsMixin.SubscriptionProperty"]]]]:
        '''The Amazon  subscriptions (endpoints) for this topic.

        .. epigraph::

           If you specify the ``Subscription`` property in the ``AWS::SNS::Topic`` resource and it creates an associated subscription resource, the associated subscription is not deleted when the ``AWS::SNS::Topic`` resource is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-subscription
        '''
        result = self._values.get("subscription")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTopicPropsMixin.SubscriptionProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of tags to add to a new topic.

        .. epigraph::

           To be able to tag a topic on creation, you must have the ``sns:CreateTopic`` and ``sns:TagResource`` permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def topic_name(self) -> typing.Optional[builtins.str]:
        '''The name of the topic you want to create.

        Topic names must include only uppercase and lowercase ASCII letters, numbers, underscores, and hyphens, and must be between 1 and 256 characters long. FIFO topic names must end with ``.fifo`` .

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see `Name type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you can't perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-topicname
        '''
        result = self._values.get("topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tracing_config(self) -> typing.Optional[builtins.str]:
        '''Tracing mode of an Amazon  topic.

        By default ``TracingConfig`` is set to ``PassThrough`` , and the topic passes through the tracing header it receives from an Amazon  publisher to its subscriptions. If set to ``Active`` , Amazon  will vend X-Ray segment data to topic owner account if the sampled flag in the tracing header is true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html#cfn-sns-topic-tracingconfig
        '''
        result = self._values.get("tracing_config")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "topics": "topics"},
)
class CfnTopicPolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        topics: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnTopicPolicyPropsMixin.

        :param policy_document: A policy document that contains permissions to add to the specified SNS topics.
        :param topics: The Amazon Resource Names (ARN) of the topics to which you want to add the policy. You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html)`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
            
            # policy_document: Any
            
            cfn_topic_policy_mixin_props = sns_mixins.CfnTopicPolicyMixinProps(
                policy_document=policy_document,
                topics=["topics"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15de1bef579688eac3ca0c6e440f86daff37389db6494774421e405279df5c89)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if topics is not None:
            self._values["topics"] = topics

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''A policy document that contains permissions to add to the specified SNS topics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicpolicy.html#cfn-sns-topicpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def topics(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARN) of the topics to which you want to add the policy.

        You can use the ``[Ref](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/intrinsic-function-reference-ref.html)`` function to specify an ``[AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html)`` resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicpolicy.html#cfn-sns-topicpolicy-topics
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTopicPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTopicPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicPolicyPropsMixin",
):
    '''The ``AWS::SNS::TopicPolicy`` resource associates Amazon  topics with a policy.

    For an example snippet, see `Declaring an Amazon  policy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-sns-policy>`_ in the *CloudFormation User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topicpolicy.html
    :cloudformationResource: AWS::SNS::TopicPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
        
        # policy_document: Any
        
        cfn_topic_policy_props_mixin = sns_mixins.CfnTopicPolicyPropsMixin(sns_mixins.CfnTopicPolicyMixinProps(
            policy_document=policy_document,
            topics=["topics"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTopicPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SNS::TopicPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa67842e46309bacc6d229965791219eaf0117c4a297a280909060631117fbd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__024749a0ba1b74a51a9036366354f66df85ceae11126688b9ce27adf6495377c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__438d7e41beec29722012c38b9906fa202dc87f81e2dba26688369ee5de72d224)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTopicPolicyMixinProps:
        return typing.cast(CfnTopicPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnTopicPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicPropsMixin",
):
    '''The ``AWS::SNS::Topic`` resource creates a topic to which notifications can be published.

    .. epigraph::

       One account can create a maximum of 100,000 standard topics and 1,000 FIFO topics. For more information, see `Amazon  endpoints and quotas <https://docs.aws.amazon.com/general/latest/gr/sns.html>`_ in the *AWS General Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html
    :cloudformationResource: AWS::SNS::Topic
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
        
        # archive_policy: Any
        # data_protection_policy: Any
        
        cfn_topic_props_mixin = sns_mixins.CfnTopicPropsMixin(sns_mixins.CfnTopicMixinProps(
            archive_policy=archive_policy,
            content_based_deduplication=False,
            data_protection_policy=data_protection_policy,
            delivery_status_logging=[sns_mixins.CfnTopicPropsMixin.LoggingConfigProperty(
                failure_feedback_role_arn="failureFeedbackRoleArn",
                protocol="protocol",
                success_feedback_role_arn="successFeedbackRoleArn",
                success_feedback_sample_rate="successFeedbackSampleRate"
            )],
            display_name="displayName",
            fifo_throughput_scope="fifoThroughputScope",
            fifo_topic=False,
            kms_master_key_id="kmsMasterKeyId",
            signature_version="signatureVersion",
            subscription=[sns_mixins.CfnTopicPropsMixin.SubscriptionProperty(
                endpoint="endpoint",
                protocol="protocol"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            topic_name="topicName",
            tracing_config="tracingConfig"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTopicMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SNS::Topic``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1159db271fcbada5cbdd6aa7d07d6fad00437ebf75a0468d55a82237adca575b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35da131a9f33aedc1782f9c7889383554cc2ccaff2c9a433a49144b405cde1b1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d82b17095ab9abdf4c4f71bb885fb1327fac0e6208a6a87e1495d8f65051284)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTopicMixinProps:
        return typing.cast(CfnTopicMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicPropsMixin.LoggingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failure_feedback_role_arn": "failureFeedbackRoleArn",
            "protocol": "protocol",
            "success_feedback_role_arn": "successFeedbackRoleArn",
            "success_feedback_sample_rate": "successFeedbackSampleRate",
        },
    )
    class LoggingConfigProperty:
        def __init__(
            self,
            *,
            failure_feedback_role_arn: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            success_feedback_role_arn: typing.Optional[builtins.str] = None,
            success_feedback_sample_rate: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``LoggingConfig`` property type specifies the ``Delivery`` status logging configuration for an ```AWS::SNS::Topic`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-topic.html>`_ .

            :param failure_feedback_role_arn: The IAM role ARN to be used when logging failed message deliveries in Amazon CloudWatch.
            :param protocol: Indicates one of the supported protocols for the Amazon SNS topic. .. epigraph:: At least one of the other three ``LoggingConfig`` properties is recommend along with ``Protocol`` .
            :param success_feedback_role_arn: The IAM role ARN to be used when logging successful message deliveries in Amazon CloudWatch.
            :param success_feedback_sample_rate: The percentage of successful message deliveries to be logged in Amazon CloudWatch. Valid percentage values range from 0 to 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-loggingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
                
                logging_config_property = sns_mixins.CfnTopicPropsMixin.LoggingConfigProperty(
                    failure_feedback_role_arn="failureFeedbackRoleArn",
                    protocol="protocol",
                    success_feedback_role_arn="successFeedbackRoleArn",
                    success_feedback_sample_rate="successFeedbackSampleRate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3c7d2d0307643500315b3857161045e96f12da96b465d2208e608d0006892cc)
                check_type(argname="argument failure_feedback_role_arn", value=failure_feedback_role_arn, expected_type=type_hints["failure_feedback_role_arn"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument success_feedback_role_arn", value=success_feedback_role_arn, expected_type=type_hints["success_feedback_role_arn"])
                check_type(argname="argument success_feedback_sample_rate", value=success_feedback_sample_rate, expected_type=type_hints["success_feedback_sample_rate"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_feedback_role_arn is not None:
                self._values["failure_feedback_role_arn"] = failure_feedback_role_arn
            if protocol is not None:
                self._values["protocol"] = protocol
            if success_feedback_role_arn is not None:
                self._values["success_feedback_role_arn"] = success_feedback_role_arn
            if success_feedback_sample_rate is not None:
                self._values["success_feedback_sample_rate"] = success_feedback_sample_rate

        @builtins.property
        def failure_feedback_role_arn(self) -> typing.Optional[builtins.str]:
            '''The IAM role ARN to be used when logging failed message deliveries in Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-loggingconfig.html#cfn-sns-topic-loggingconfig-failurefeedbackrolearn
            '''
            result = self._values.get("failure_feedback_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''Indicates one of the supported protocols for the Amazon SNS topic.

            .. epigraph::

               At least one of the other three ``LoggingConfig`` properties is recommend along with ``Protocol`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-loggingconfig.html#cfn-sns-topic-loggingconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def success_feedback_role_arn(self) -> typing.Optional[builtins.str]:
            '''The IAM role ARN to be used when logging successful message deliveries in Amazon CloudWatch.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-loggingconfig.html#cfn-sns-topic-loggingconfig-successfeedbackrolearn
            '''
            result = self._values.get("success_feedback_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def success_feedback_sample_rate(self) -> typing.Optional[builtins.str]:
            '''The percentage of successful message deliveries to be logged in Amazon CloudWatch.

            Valid percentage values range from 0 to 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-loggingconfig.html#cfn-sns-topic-loggingconfig-successfeedbacksamplerate
            '''
            result = self._values.get("success_feedback_sample_rate")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sns.mixins.CfnTopicPropsMixin.SubscriptionProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint", "protocol": "protocol"},
    )
    class SubscriptionProperty:
        def __init__(
            self,
            *,
            endpoint: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Subscription`` is an embedded property that describes the subscription endpoints of an Amazon  topic.

            .. epigraph::

               For full control over subscription behavior (for example, delivery policy, filtering, raw message delivery, and cross-region subscriptions), use the `AWS::SNS::Subscription <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html>`_ resource.

            :param endpoint: The endpoint that receives notifications from the Amazon topic. The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon API Reference* .
            :param protocol: The subscription's protocol. For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-subscription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sns import mixins as sns_mixins
                
                subscription_property = sns_mixins.CfnTopicPropsMixin.SubscriptionProperty(
                    endpoint="endpoint",
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b839a6ce7042a9e8cc4c6b797683902a293012787d0602c70affad4a0a0727f4)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint that receives notifications from the Amazon  topic.

            The endpoint value depends on the protocol that you specify. For more information, see the ``Endpoint`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon  API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-subscription.html#cfn-sns-topic-subscription-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The subscription's protocol.

            For more information, see the ``Protocol`` parameter of the ``[Subscribe](https://docs.aws.amazon.com/sns/latest/api/API_Subscribe.html)`` action in the *Amazon  API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic-subscription.html#cfn-sns-topic-subscription-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubscriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnSubscriptionMixinProps",
    "CfnSubscriptionPropsMixin",
    "CfnTopicInlinePolicyMixinProps",
    "CfnTopicInlinePolicyPropsMixin",
    "CfnTopicMixinProps",
    "CfnTopicPolicyMixinProps",
    "CfnTopicPolicyPropsMixin",
    "CfnTopicPropsMixin",
]

publication.publish()

def _typecheckingstub__5520cd517bbea5f6e383753478f47fcb47f305c3dfad2e29ae34525156ab55f5(
    *,
    delivery_policy: typing.Any = None,
    endpoint: typing.Optional[builtins.str] = None,
    filter_policy: typing.Any = None,
    filter_policy_scope: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    raw_message_delivery: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    redrive_policy: typing.Any = None,
    region: typing.Optional[builtins.str] = None,
    replay_policy: typing.Any = None,
    subscription_role_arn: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed90e5347327afd84275344faab507b2b80fd3cb0700fa5ec4304e9fed4e9006(
    props: typing.Union[CfnSubscriptionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ddcd8156c394442b17a5e447433761c4470d744166f84c7718d2e7e1b15c63(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6e0f0fe00ef6e35d69f1c381999a846ed0f5fe474ae3669151818b2556ee5f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f9f3c7587fd220fcd572dedb2bbee7bdd891bfc485c51e4885a6ab7fa83543f(
    *,
    policy_document: typing.Any = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ac80900efedc798e9dedd8e853a93ef0de232f8bbc012bdb349507333d28c28(
    props: typing.Union[CfnTopicInlinePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a613d0720b4bca229070367bfd4862e3a9ebba05ad25fa819cfcd5ab98f958(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7ea050c525b06b8967ef4e1ea87055fd25513a53c52ba2652ac2455c2689cac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe6b7e291779768d4a945a8312ecc3420de13e93369d811ab118cc71d258960(
    *,
    archive_policy: typing.Any = None,
    content_based_deduplication: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_protection_policy: typing.Any = None,
    delivery_status_logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTopicPropsMixin.LoggingConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    display_name: typing.Optional[builtins.str] = None,
    fifo_throughput_scope: typing.Optional[builtins.str] = None,
    fifo_topic: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_master_key_id: typing.Optional[builtins.str] = None,
    signature_version: typing.Optional[builtins.str] = None,
    subscription: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTopicPropsMixin.SubscriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    topic_name: typing.Optional[builtins.str] = None,
    tracing_config: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15de1bef579688eac3ca0c6e440f86daff37389db6494774421e405279df5c89(
    *,
    policy_document: typing.Any = None,
    topics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa67842e46309bacc6d229965791219eaf0117c4a297a280909060631117fbd(
    props: typing.Union[CfnTopicPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__024749a0ba1b74a51a9036366354f66df85ceae11126688b9ce27adf6495377c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438d7e41beec29722012c38b9906fa202dc87f81e2dba26688369ee5de72d224(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1159db271fcbada5cbdd6aa7d07d6fad00437ebf75a0468d55a82237adca575b(
    props: typing.Union[CfnTopicMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35da131a9f33aedc1782f9c7889383554cc2ccaff2c9a433a49144b405cde1b1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d82b17095ab9abdf4c4f71bb885fb1327fac0e6208a6a87e1495d8f65051284(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3c7d2d0307643500315b3857161045e96f12da96b465d2208e608d0006892cc(
    *,
    failure_feedback_role_arn: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    success_feedback_role_arn: typing.Optional[builtins.str] = None,
    success_feedback_sample_rate: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b839a6ce7042a9e8cc4c6b797683902a293012787d0602c70affad4a0a0727f4(
    *,
    endpoint: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
