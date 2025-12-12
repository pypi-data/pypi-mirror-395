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
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnAccountPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "policy_type": "policyType",
        "scope": "scope",
        "selection_criteria": "selectionCriteria",
    },
)
class CfnAccountPolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
        policy_type: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        selection_criteria: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAccountPolicyPropsMixin.

        :param policy_document: Specify the policy, in JSON. *Data protection policy* A data protection policy must include two JSON blocks: - The first block must include both a ``DataIdentifer`` array and an ``Operation`` property with an ``Audit`` action. The ``DataIdentifer`` array lists the types of sensitive data that you want to mask. For more information about the available options, see `Types of data that you can mask <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data-types.html>`_ . The ``Operation`` property with an ``Audit`` action is required to find the sensitive data terms. This ``Audit`` action must contain a ``FindingsDestination`` object. You can optionally use that ``FindingsDestination`` object to list one or more destinations to send audit findings to. If you specify destinations such as log groups, Firehose streams, and S3 buckets, they must already exist. - The second block must include both a ``DataIdentifer`` array and an ``Operation`` property with an ``Deidentify`` action. The ``DataIdentifer`` array must exactly match the ``DataIdentifer`` array in the first block of the policy. The ``Operation`` property with the ``Deidentify`` action is what actually masks the data, and it must contain the ``"MaskConfig": {}`` object. The ``"MaskConfig": {}`` object must be empty. .. epigraph:: The contents of the two ``DataIdentifer`` arrays must match exactly. In addition to the two JSON blocks, the ``policyDocument`` can also include ``Name`` , ``Description`` , and ``Version`` fields. The ``Name`` is different than the operation's ``policyName`` parameter, and is used as a dimension when CloudWatch Logs reports audit findings metrics to CloudWatch . The JSON specified in ``policyDocument`` can be up to 30,720 characters long. *Subscription filter policy* A subscription filter policy can include the following attributes in a JSON block: - *DestinationArn* The ARN of the destination to deliver log events to. Supported destinations are: - An Kinesis Data Streams data stream in the same account as the subscription policy, for same-account delivery. - An Firehose data stream in the same account as the subscription policy, for same-account delivery. - A Lambda function in the same account as the subscription policy, for same-account delivery. - A logical destination in a different account created with `PutDestination <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDestination.html>`_ , for cross-account delivery. Kinesis Data Streams and Firehose are supported as logical destinations. - *RoleArn* The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery. - *FilterPattern* A filter pattern for subscribing to a filtered stream of log events. - *Distribution* The method used to distribute log data to the destination. By default, log data is grouped by log stream, but the grouping can be set to ``Random`` for a more even distribution. This property is only applicable when the destination is an Kinesis Data Streams data stream. *Field index policy* A field index filter policy can include the following attribute in a JSON block: - *Fields* The array of field indexes to create. The following is an example of an index policy document that creates two indexes, ``RequestId`` and ``TransactionId`` . ``"policyDocument": "{ \\"Fields\\": [ \\"RequestId\\", \\"TransactionId\\" ] }"`` *Transformer policy* A transformer policy must include one JSON block with the array of processors and their configurations. For more information about available processors, see `Processors that you can use <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-Processors>`_ .
        :param policy_name: A name for the policy. This must be unique within the account.
        :param policy_type: The type of policy that you're creating or updating.
        :param scope: Currently the only valid value for this parameter is ``ALL`` , which specifies that the policy applies to all log groups in the account. If you omit this parameter, the default of ``ALL`` is used. To scope down a subscription filter policy to a subset of log groups, use the ``SelectionCriteria`` parameter.
        :param selection_criteria: Use this parameter to apply the new policy to a subset of log groups in the account. You need to specify ``SelectionCriteria`` only when you specify ``SUBSCRIPTION_FILTER_POLICY`` , ``FIELD_INDEX_POLICY`` or ``TRANSFORMER_POLICY`` for ``PolicyType`` . If ``PolicyType`` is ``SUBSCRIPTION_FILTER_POLICY`` , the only supported ``SelectionCriteria`` filter is ``LogGroupName NOT IN []`` If ``PolicyType`` is ``FIELD_INDEX_POLICY`` or ``TRANSFORMER_POLICY`` , the only supported ``SelectionCriteria`` filter is ``LogGroupNamePrefix`` The ``SelectionCriteria`` string can be up to 25KB in length. The length is determined by using its UTF-8 bytes. Using the ``SelectionCriteria`` parameter with ``SUBSCRIPTION_FILTER_POLICY`` is useful to help prevent infinite loops. For more information, see `Log recursion prevention <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions-recursion-prevention.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_account_policy_mixin_props = logs_mixins.CfnAccountPolicyMixinProps(
                policy_document="policyDocument",
                policy_name="policyName",
                policy_type="policyType",
                scope="scope",
                selection_criteria="selectionCriteria"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e9f7747f7ed71835091ec3783faae5a96fef3ed5b1f4e48bc0ecae27c0bfe7)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument selection_criteria", value=selection_criteria, expected_type=type_hints["selection_criteria"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if policy_type is not None:
            self._values["policy_type"] = policy_type
        if scope is not None:
            self._values["scope"] = scope
        if selection_criteria is not None:
            self._values["selection_criteria"] = selection_criteria

    @builtins.property
    def policy_document(self) -> typing.Optional[builtins.str]:
        '''Specify the policy, in JSON.

        *Data protection policy*

        A data protection policy must include two JSON blocks:

        - The first block must include both a ``DataIdentifer`` array and an ``Operation`` property with an ``Audit`` action. The ``DataIdentifer`` array lists the types of sensitive data that you want to mask. For more information about the available options, see `Types of data that you can mask <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data-types.html>`_ .

        The ``Operation`` property with an ``Audit`` action is required to find the sensitive data terms. This ``Audit`` action must contain a ``FindingsDestination`` object. You can optionally use that ``FindingsDestination`` object to list one or more destinations to send audit findings to. If you specify destinations such as log groups, Firehose streams, and S3 buckets, they must already exist.

        - The second block must include both a ``DataIdentifer`` array and an ``Operation`` property with an ``Deidentify`` action. The ``DataIdentifer`` array must exactly match the ``DataIdentifer`` array in the first block of the policy.

        The ``Operation`` property with the ``Deidentify`` action is what actually masks the data, and it must contain the ``"MaskConfig": {}`` object. The ``"MaskConfig": {}`` object must be empty.
        .. epigraph::

           The contents of the two ``DataIdentifer`` arrays must match exactly.

        In addition to the two JSON blocks, the ``policyDocument`` can also include ``Name`` , ``Description`` , and ``Version`` fields. The ``Name`` is different than the operation's ``policyName`` parameter, and is used as a dimension when CloudWatch Logs reports audit findings metrics to CloudWatch .

        The JSON specified in ``policyDocument`` can be up to 30,720 characters long.

        *Subscription filter policy*

        A subscription filter policy can include the following attributes in a JSON block:

        - *DestinationArn* The ARN of the destination to deliver log events to. Supported destinations are:
        - An Kinesis Data Streams data stream in the same account as the subscription policy, for same-account delivery.
        - An Firehose data stream in the same account as the subscription policy, for same-account delivery.
        - A Lambda function in the same account as the subscription policy, for same-account delivery.
        - A logical destination in a different account created with `PutDestination <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDestination.html>`_ , for cross-account delivery. Kinesis Data Streams and Firehose are supported as logical destinations.
        - *RoleArn* The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.
        - *FilterPattern* A filter pattern for subscribing to a filtered stream of log events.
        - *Distribution* The method used to distribute log data to the destination. By default, log data is grouped by log stream, but the grouping can be set to ``Random`` for a more even distribution. This property is only applicable when the destination is an Kinesis Data Streams data stream.

        *Field index policy*

        A field index filter policy can include the following attribute in a JSON block:

        - *Fields* The array of field indexes to create.

        The following is an example of an index policy document that creates two indexes, ``RequestId`` and ``TransactionId`` .

        ``"policyDocument": "{ \\"Fields\\": [ \\"RequestId\\", \\"TransactionId\\" ] }"``

        *Transformer policy*

        A transformer policy must include one JSON block with the array of processors and their configurations. For more information about available processors, see `Processors that you can use <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-Processors>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html#cfn-logs-accountpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''A name for the policy.

        This must be unique within the account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html#cfn-logs-accountpolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_type(self) -> typing.Optional[builtins.str]:
        '''The type of policy that you're creating or updating.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html#cfn-logs-accountpolicy-policytype
        '''
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''Currently the only valid value for this parameter is ``ALL`` , which specifies that the policy applies to all log groups in the account.

        If you omit this parameter, the default of ``ALL`` is used. To scope down a subscription filter policy to a subset of log groups, use the ``SelectionCriteria`` parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html#cfn-logs-accountpolicy-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selection_criteria(self) -> typing.Optional[builtins.str]:
        '''Use this parameter to apply the new policy to a subset of log groups in the account.

        You need to specify ``SelectionCriteria`` only when you specify ``SUBSCRIPTION_FILTER_POLICY`` , ``FIELD_INDEX_POLICY`` or ``TRANSFORMER_POLICY`` for ``PolicyType`` .

        If ``PolicyType`` is ``SUBSCRIPTION_FILTER_POLICY`` , the only supported ``SelectionCriteria`` filter is ``LogGroupName NOT IN []``

        If ``PolicyType`` is ``FIELD_INDEX_POLICY`` or ``TRANSFORMER_POLICY`` , the only supported ``SelectionCriteria`` filter is ``LogGroupNamePrefix``

        The ``SelectionCriteria`` string can be up to 25KB in length. The length is determined by using its UTF-8 bytes.

        Using the ``SelectionCriteria`` parameter with ``SUBSCRIPTION_FILTER_POLICY`` is useful to help prevent infinite loops. For more information, see `Log recursion prevention <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions-recursion-prevention.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html#cfn-logs-accountpolicy-selectioncriteria
        '''
        result = self._values.get("selection_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccountPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnAccountPolicyPropsMixin",
):
    '''Creates or updates an account-level data protection policy or subscription filter policy that applies to all log groups or a subset of log groups in the account.

    *Data protection policy*

    A data protection policy can help safeguard sensitive data that's ingested by your log groups by auditing and masking the sensitive log data. Each account can have only one account-level data protection policy.
    .. epigraph::

       Sensitive data is detected and masked when it is ingested into a log group. When you set a data protection policy, log events ingested into the log groups before that time are not masked.

    If you create a data protection policy for your whole account, it applies to both existing log groups and all log groups that are created later in this account. The account policy is applied to existing log groups with eventual consistency. It might take up to 5 minutes before sensitive data in existing log groups begins to be masked.

    By default, when a user views a log event that includes masked data, the sensitive data is replaced by asterisks. A user who has the ``logs:Unmask`` permission can use a `GetLogEvents <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetLogEvents.html>`_ or `FilterLogEvents <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_FilterLogEvents.html>`_ operation with the ``unmask`` parameter set to ``true`` to view the unmasked log events. Users with the ``logs:Unmask`` can also view unmasked data in the CloudWatch Logs console by running a CloudWatch Logs Insights query with the ``unmask`` query command.

    For more information, including a list of types of data that can be audited and masked, see `Protect sensitive log data with masking <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html>`_ .

    To create an account-level policy, you must be signed on with the ``logs:PutDataProtectionPolicy`` and ``logs:PutAccountPolicy`` permissions.

    An account-level policy applies to all log groups in the account. You can also create a data protection policy that applies to just one log group. If a log group has its own data protection policy and the account also has an account-level data protection policy, then the two policies are cumulative. Any sensitive term specified in either policy is masked.

    *Subscription filter policy*

    A subscription filter policy sets up a real-time feed of log events from CloudWatch Logs to other AWS services. Account-level subscription filter policies apply to both existing log groups and log groups that are created later in this account. Supported destinations are Kinesis Data Streams , Firehose , and Lambda . When log events are sent to the receiving service, they are Base64 encoded and compressed with the GZIP format.

    The following destinations are supported for subscription filters:

    - An Kinesis Data Streams data stream in the same account as the subscription policy, for same-account delivery.
    - An Firehose data stream in the same account as the subscription policy, for same-account delivery.
    - A Lambda function in the same account as the subscription policy, for same-account delivery.
    - A logical destination in a different account created with `PutDestination <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDestination.html>`_ , for cross-account delivery. Kinesis Data Streams and Firehose are supported as logical destinations.

    Each account can have one account-level subscription filter policy. If you are updating an existing filter, you must specify the correct name in ``PolicyName`` . To perform a ``PutAccountPolicy`` subscription filter operation for any destination except a Lambda function, you must also have the ``iam:PassRole`` permission.

    *Field index policy*

    You can use field index policies to create indexes on fields found in log events in the log group. Creating field indexes lowers the scan volume for CloudWatch Logs Insights queries that reference those fields, because these queries attempt to skip the processing of log events that are known to not match the indexed field. Good fields to index are fields that you often need to query for. Common examples of indexes include request ID, session ID, user IDs, or instance IDs. For more information, see `Create field indexes to improve query performance and reduce costs <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs-Field-Indexing.html>`_

    For example, suppose you have created a field index for ``requestId`` . Then, any CloudWatch Logs Insights query on that log group that includes ``requestId = *value*`` or ``requestId IN [ *value* , *value* , ...]`` will attempt to process only the log events where the indexed field matches the specified value.

    Matches of log events to the names of indexed fields are case-sensitive. For example, an indexed field of ``RequestId`` won't match a log event containing ``requestId`` .

    You can have one account-level field index policy that applies to all log groups in the account. Or you can create as many as 20 account-level field index policies that are each scoped to a subset of log groups with the ``SelectionCriteria`` parameter. If you have multiple account-level index policies with selection criteria, no two of them can use the same or overlapping log group name prefixes. For example, if you have one policy filtered to log groups that start with ``my-log`` , you can't have another field index policy filtered to ``my-logpprod`` or ``my-logging`` .

    *Transformer policy*

    A *log transformer policy* transforms ingested log events into a different format, making them easier for you to process and analyze. You can also transform logs from different sources into standardized formats that contain relevant, source-specific information. After you have created a transformer, CloudWatch Logs performs this transformation at the time of log ingestion. You can then refer to the transformed versions of the logs during operations such as querying with CloudWatch Logs Insights or creating metric filters or subscription filters.

    You can also use a transformer to copy metadata from metadata keys into the log events themselves. This metadata can include log group name, log stream name, account ID and Region.

    A transformer for a log group is a series of processors, where each processor applies one type of transformation to the log events ingested into this log group. For more information about the available processors to use in a transformer, see `Processors that you can use <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-Processors>`_ .

    Having log events in standardized format enables visibility across your applications for your log analysis, reporting, and alarming needs. CloudWatch Logs provides transformation for common log types with out-of-the-box transformation templates for major AWS log sources such as VPC flow logs, Lambda , and Amazon RDS . You can use pre-built transformation templates or create custom transformation policies.

    You can create transformers only for the log groups in the Standard log class.

    You can have one account-level transformer policy that applies to all log groups in the account. Or you can create as many as 20 account-level transformer policies that are each scoped to a subset of log groups with the ``selectionCriteria`` parameter. If you have multiple account-level transformer policies with selection criteria, no two of them can use the same or overlapping log group name prefixes. For example, if you have one policy filtered to log groups that start with ``my-log`` , you can't have another field index policy filtered to ``my-logpprod`` or ``my-logging`` .

    You can also set up a transformer at the log-group level. For more information, see `AWS::Logs::Transformer <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-transformer.html>`_ . If there is both a log-group level transformer created with ``PutTransformer`` and an account-level transformer that could apply to the same log group, the log group uses only the log-group level transformer. It ignores the account-level transformer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-accountpolicy.html
    :cloudformationResource: AWS::Logs::AccountPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_account_policy_props_mixin = logs_mixins.CfnAccountPolicyPropsMixin(logs_mixins.CfnAccountPolicyMixinProps(
            policy_document="policyDocument",
            policy_name="policyName",
            policy_type="policyType",
            scope="scope",
            selection_criteria="selectionCriteria"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccountPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::AccountPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b4e4698b738ed0a1969dcd9a6bf207f2ab4df20f7bb22022e6b5c4cd50b905)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bce0ade5dd433eae28f8021404f593ad0cb77f657355c0598e3e0e8ef159e5d4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3926564a102acf5c9fa3753a42d9d54e37fc83e417b7611da2cfee62354488c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccountPolicyMixinProps:
        return typing.cast(CfnAccountPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliveryDestinationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_destination_policy": "deliveryDestinationPolicy",
        "delivery_destination_type": "deliveryDestinationType",
        "destination_resource_arn": "destinationResourceArn",
        "name": "name",
        "output_format": "outputFormat",
        "tags": "tags",
    },
)
class CfnDeliveryDestinationMixinProps:
    def __init__(
        self,
        *,
        delivery_destination_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        delivery_destination_type: typing.Optional[builtins.str] = None,
        destination_resource_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        output_format: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDeliveryDestinationPropsMixin.

        :param delivery_destination_policy: An IAM policy that grants permissions to CloudWatch Logs to deliver logs cross-account to a specified destination in this account. For examples of this policy, see `Examples <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliveryDestinationPolicy.html#API_PutDeliveryDestinationPolicy_Examples>`_ in the CloudWatch Logs API Reference.
        :param delivery_destination_type: Displays whether this delivery destination is CloudWatch Logs, Amazon S3, Firehose, or X-Ray.
        :param destination_resource_arn: The ARN of the AWS destination that this delivery destination represents. That AWS destination can be a log group in CloudWatch Logs , an Amazon S3 bucket, or a Firehose stream.
        :param name: The name of this delivery destination.
        :param output_format: The format of the logs that are sent to this delivery destination.
        :param tags: An array of key-value pairs to apply to the delivery destination. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            # delivery_destination_policy: Any
            
            cfn_delivery_destination_mixin_props = logs_mixins.CfnDeliveryDestinationMixinProps(
                delivery_destination_policy=logs_mixins.CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty(
                    delivery_destination_name="deliveryDestinationName",
                    delivery_destination_policy=delivery_destination_policy
                ),
                delivery_destination_type="deliveryDestinationType",
                destination_resource_arn="destinationResourceArn",
                name="name",
                output_format="outputFormat",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e140ffa7516223860f4cabe5d8e75d264ed74f5ad12d39823f88dbad992186)
            check_type(argname="argument delivery_destination_policy", value=delivery_destination_policy, expected_type=type_hints["delivery_destination_policy"])
            check_type(argname="argument delivery_destination_type", value=delivery_destination_type, expected_type=type_hints["delivery_destination_type"])
            check_type(argname="argument destination_resource_arn", value=destination_resource_arn, expected_type=type_hints["destination_resource_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_destination_policy is not None:
            self._values["delivery_destination_policy"] = delivery_destination_policy
        if delivery_destination_type is not None:
            self._values["delivery_destination_type"] = delivery_destination_type
        if destination_resource_arn is not None:
            self._values["destination_resource_arn"] = destination_resource_arn
        if name is not None:
            self._values["name"] = name
        if output_format is not None:
            self._values["output_format"] = output_format
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def delivery_destination_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty"]]:
        '''An IAM policy that grants permissions to CloudWatch Logs to deliver logs cross-account to a specified destination in this account.

        For examples of this policy, see `Examples <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliveryDestinationPolicy.html#API_PutDeliveryDestinationPolicy_Examples>`_ in the CloudWatch Logs API Reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html#cfn-logs-deliverydestination-deliverydestinationpolicy
        '''
        result = self._values.get("delivery_destination_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty"]], result)

    @builtins.property
    def delivery_destination_type(self) -> typing.Optional[builtins.str]:
        '''Displays whether this delivery destination is CloudWatch Logs, Amazon S3, Firehose, or X-Ray.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html#cfn-logs-deliverydestination-deliverydestinationtype
        '''
        result = self._values.get("delivery_destination_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_resource_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS destination that this delivery destination represents.

        That AWS destination can be a log group in CloudWatch Logs , an Amazon S3 bucket, or a Firehose stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html#cfn-logs-deliverydestination-destinationresourcearn
        '''
        result = self._values.get("destination_resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of this delivery destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html#cfn-logs-deliverydestination-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_format(self) -> typing.Optional[builtins.str]:
        '''The format of the logs that are sent to this delivery destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html#cfn-logs-deliverydestination-outputformat
        '''
        result = self._values.get("output_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the delivery destination.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html#cfn-logs-deliverydestination-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliveryDestinationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeliveryDestinationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliveryDestinationPropsMixin",
):
    '''This structure contains information about one *delivery destination* in your account.

    A delivery destination is an AWS resource that represents an AWS service that logs can be sent to. CloudWatch Logs, Amazon S3, Firehose, and X-Ray are supported as delivery destinations.

    To configure logs delivery between a supported AWS service and a destination, you must do the following:

    - Create a delivery source, which is a logical object that represents the resource that is actually sending the logs. For more information, see `PutDeliverySource <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliverySource.html>`_ .
    - Create a *delivery destination* , which is a logical object that represents the actual delivery destination.
    - If you are delivering logs cross-account, you must use `PutDeliveryDestinationPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliveryDestinationPolicy.html>`_ in the destination account to assign an IAM policy to the destination. This policy allows delivery to that destination.
    - Create a *delivery* by pairing exactly one delivery source and one delivery destination. For more information, see `CreateDelivery <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html>`_ .

    You can configure a single delivery source to send logs to multiple destinations by creating multiple deliveries. You can also create multiple deliveries to configure multiple delivery sources to send logs to the same delivery destination.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html
    :cloudformationResource: AWS::Logs::DeliveryDestination
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        # delivery_destination_policy: Any
        
        cfn_delivery_destination_props_mixin = logs_mixins.CfnDeliveryDestinationPropsMixin(logs_mixins.CfnDeliveryDestinationMixinProps(
            delivery_destination_policy=logs_mixins.CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty(
                delivery_destination_name="deliveryDestinationName",
                delivery_destination_policy=delivery_destination_policy
            ),
            delivery_destination_type="deliveryDestinationType",
            destination_resource_arn="destinationResourceArn",
            name="name",
            output_format="outputFormat",
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
        props: typing.Union[CfnDeliveryDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::DeliveryDestination``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e3484831d6c4a56b29112a049d9912c0374c0d6609e1f1c313909400d23cc3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b741c7d24389f30f8422259c838236bc4520b64688f0155f233402d40b4c50e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e648e811fe74409270723b2c2fb69fd8a517f5abf7202e08eb2f3d9b85b434)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeliveryDestinationMixinProps:
        return typing.cast(CfnDeliveryDestinationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_destination_name": "deliveryDestinationName",
            "delivery_destination_policy": "deliveryDestinationPolicy",
        },
    )
    class DestinationPolicyProperty:
        def __init__(
            self,
            *,
            delivery_destination_name: typing.Optional[builtins.str] = None,
            delivery_destination_policy: typing.Any = None,
        ) -> None:
            '''An IAM policy that grants permissions to CloudWatch Logs to deliver logs cross-account to a specified destination in this account.

            :param delivery_destination_name: A name for an existing destination.
            :param delivery_destination_policy: Creates or updates an access policy associated with an existing destination. An access policy is an `IAM policy document <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies_overview.html>`_ that is used to authorize claims to register a subscription filter against a given destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-deliverydestination-destinationpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                # delivery_destination_policy: Any
                
                destination_policy_property = logs_mixins.CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty(
                    delivery_destination_name="deliveryDestinationName",
                    delivery_destination_policy=delivery_destination_policy
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d951f283038c601c8b734c9a9c0c5a39d61fdfc6276bc71138bc76059874326)
                check_type(argname="argument delivery_destination_name", value=delivery_destination_name, expected_type=type_hints["delivery_destination_name"])
                check_type(argname="argument delivery_destination_policy", value=delivery_destination_policy, expected_type=type_hints["delivery_destination_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_destination_name is not None:
                self._values["delivery_destination_name"] = delivery_destination_name
            if delivery_destination_policy is not None:
                self._values["delivery_destination_policy"] = delivery_destination_policy

        @builtins.property
        def delivery_destination_name(self) -> typing.Optional[builtins.str]:
            '''A name for an existing destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-deliverydestination-destinationpolicy.html#cfn-logs-deliverydestination-destinationpolicy-deliverydestinationname
            '''
            result = self._values.get("delivery_destination_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def delivery_destination_policy(self) -> typing.Any:
            '''Creates or updates an access policy associated with an existing destination.

            An access policy is an `IAM policy document <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies_overview.html>`_ that is used to authorize claims to register a subscription filter against a given destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-deliverydestination-destinationpolicy.html#cfn-logs-deliverydestination-destinationpolicy-deliverydestinationpolicy
            '''
            result = self._values.get("delivery_destination_policy")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliveryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_destination_arn": "deliveryDestinationArn",
        "delivery_source_name": "deliverySourceName",
        "field_delimiter": "fieldDelimiter",
        "record_fields": "recordFields",
        "s3_enable_hive_compatible_path": "s3EnableHiveCompatiblePath",
        "s3_suffix_path": "s3SuffixPath",
        "tags": "tags",
    },
)
class CfnDeliveryMixinProps:
    def __init__(
        self,
        *,
        delivery_destination_arn: typing.Optional[builtins.str] = None,
        delivery_source_name: typing.Optional[builtins.str] = None,
        field_delimiter: typing.Optional[builtins.str] = None,
        record_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_enable_hive_compatible_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        s3_suffix_path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDeliveryPropsMixin.

        :param delivery_destination_arn: The ARN of the delivery destination that is associated with this delivery.
        :param delivery_source_name: The name of the delivery source that is associated with this delivery.
        :param field_delimiter: The field delimiter that is used between record fields when the final output format of a delivery is in ``Plain`` , ``W3C`` , or ``Raw`` format.
        :param record_fields: The list of record fields to be delivered to the destination, in order. If the delivery's log source has mandatory fields, they must be included in this list.
        :param s3_enable_hive_compatible_path: Use this parameter to cause the S3 objects that contain delivered logs to use a prefix structure that allows for integration with Apache Hive.
        :param s3_suffix_path: Use this to reconfigure the S3 object prefix to contain either static or variable sections. The valid variables to use in the suffix path will vary by each log source. To find the values supported for the suffix path for each log source, use the `DescribeConfigurationTemplates <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeConfigurationTemplates.html>`_ operation and check the ``allowedSuffixPathFields`` field in the response.
        :param tags: An array of key-value pairs to apply to the delivery. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_delivery_mixin_props = logs_mixins.CfnDeliveryMixinProps(
                delivery_destination_arn="deliveryDestinationArn",
                delivery_source_name="deliverySourceName",
                field_delimiter="fieldDelimiter",
                record_fields=["recordFields"],
                s3_enable_hive_compatible_path=False,
                s3_suffix_path="s3SuffixPath",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2813e3a55bb7f6dd4ebbdaf6691cac31127bc792ed24f7f3aa1a5bdf34804d06)
            check_type(argname="argument delivery_destination_arn", value=delivery_destination_arn, expected_type=type_hints["delivery_destination_arn"])
            check_type(argname="argument delivery_source_name", value=delivery_source_name, expected_type=type_hints["delivery_source_name"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument record_fields", value=record_fields, expected_type=type_hints["record_fields"])
            check_type(argname="argument s3_enable_hive_compatible_path", value=s3_enable_hive_compatible_path, expected_type=type_hints["s3_enable_hive_compatible_path"])
            check_type(argname="argument s3_suffix_path", value=s3_suffix_path, expected_type=type_hints["s3_suffix_path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_destination_arn is not None:
            self._values["delivery_destination_arn"] = delivery_destination_arn
        if delivery_source_name is not None:
            self._values["delivery_source_name"] = delivery_source_name
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if record_fields is not None:
            self._values["record_fields"] = record_fields
        if s3_enable_hive_compatible_path is not None:
            self._values["s3_enable_hive_compatible_path"] = s3_enable_hive_compatible_path
        if s3_suffix_path is not None:
            self._values["s3_suffix_path"] = s3_suffix_path
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def delivery_destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the delivery destination that is associated with this delivery.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-deliverydestinationarn
        '''
        result = self._values.get("delivery_destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delivery_source_name(self) -> typing.Optional[builtins.str]:
        '''The name of the delivery source that is associated with this delivery.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-deliverysourcename
        '''
        result = self._values.get("delivery_source_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[builtins.str]:
        '''The field delimiter that is used between record fields when the final output format of a delivery is in ``Plain`` , ``W3C`` , or ``Raw`` format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-fielddelimiter
        '''
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def record_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of record fields to be delivered to the destination, in order.

        If the delivery's log source has mandatory fields, they must be included in this list.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-recordfields
        '''
        result = self._values.get("record_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_enable_hive_compatible_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Use this parameter to cause the S3 objects that contain delivered logs to use a prefix structure that allows for integration with Apache Hive.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-s3enablehivecompatiblepath
        '''
        result = self._values.get("s3_enable_hive_compatible_path")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def s3_suffix_path(self) -> typing.Optional[builtins.str]:
        '''Use this to reconfigure the S3 object prefix to contain either static or variable sections.

        The valid variables to use in the suffix path will vary by each log source. To find the values supported for the suffix path for each log source, use the `DescribeConfigurationTemplates <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_DescribeConfigurationTemplates.html>`_ operation and check the ``allowedSuffixPathFields`` field in the response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-s3suffixpath
        '''
        result = self._values.get("s3_suffix_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the delivery.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html#cfn-logs-delivery-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliveryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeliveryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliveryPropsMixin",
):
    '''This structure contains information about one *delivery* in your account.

    A delivery is a connection between a logical *delivery source* and a logical *delivery destination* .

    For more information, see `CreateDelivery <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html>`_ .

    To update an existing delivery configuration, use `UpdateDeliveryConfiguration <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_UpdateDeliveryConfiguration.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html
    :cloudformationResource: AWS::Logs::Delivery
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_delivery_props_mixin = logs_mixins.CfnDeliveryPropsMixin(logs_mixins.CfnDeliveryMixinProps(
            delivery_destination_arn="deliveryDestinationArn",
            delivery_source_name="deliverySourceName",
            field_delimiter="fieldDelimiter",
            record_fields=["recordFields"],
            s3_enable_hive_compatible_path=False,
            s3_suffix_path="s3SuffixPath",
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
        props: typing.Union[CfnDeliveryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::Delivery``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78170b657e59651144b2e9e0fcfe39ab5878aa031374d52745dec68c22225bda)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fbc4dba2680ca421f5b7f04b9063cf658cdaf1ce84c40f41be2a9a54d4691bf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1644fe16dae2f7d56a55c064293eb0b930fa0bf50dc807ddd4f4be574c22f41)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeliveryMixinProps:
        return typing.cast(CfnDeliveryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliverySourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_type": "logType",
        "name": "name",
        "resource_arn": "resourceArn",
        "tags": "tags",
    },
)
class CfnDeliverySourceMixinProps:
    def __init__(
        self,
        *,
        log_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        resource_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDeliverySourcePropsMixin.

        :param log_type: The type of log that the source is sending. For valid values for this parameter, see the documentation for the source service.
        :param name: The unique name of the delivery source.
        :param resource_arn: The ARN of the AWS resource that is generating and sending logs. For example, ``arn:aws:workmail:us-east-1:123456789012:organization/m-1234EXAMPLEabcd1234abcd1234abcd1234``
        :param tags: An array of key-value pairs to apply to the delivery source. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverysource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_delivery_source_mixin_props = logs_mixins.CfnDeliverySourceMixinProps(
                log_type="logType",
                name="name",
                resource_arn="resourceArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03b9eadeb0e7078d0b7954f59805831368c2b5338190cb04637ccfa64521706c)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_type is not None:
            self._values["log_type"] = log_type
        if name is not None:
            self._values["name"] = name
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def log_type(self) -> typing.Optional[builtins.str]:
        '''The type of log that the source is sending.

        For valid values for this parameter, see the documentation for the source service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverysource.html#cfn-logs-deliverysource-logtype
        '''
        result = self._values.get("log_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the delivery source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverysource.html#cfn-logs-deliverysource-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS resource that is generating and sending logs.

        For example, ``arn:aws:workmail:us-east-1:123456789012:organization/m-1234EXAMPLEabcd1234abcd1234abcd1234``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverysource.html#cfn-logs-deliverysource-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the delivery source.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverysource.html#cfn-logs-deliverysource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeliverySourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDeliverySourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDeliverySourcePropsMixin",
):
    '''Creates or updates one *delivery source* in your account.

    A delivery source is an AWS resource that sends logs to an AWS destination. The destination can be CloudWatch Logs , Amazon S3 , or Firehose .

    Only some AWS services support being configured as a delivery source. These services are listed as *Supported [V2 Permissions]* in the table at `Enabling logging from AWS services. <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AWS-logs-and-resource-policy.html>`_

    To configure logs delivery between a supported AWS service and a destination, you must do the following:

    - Create a delivery source, which is a logical object that represents the resource that is actually sending the logs.
    - Create a *delivery destination* , which is a logical object that represents the actual delivery destination. For more information, see `AWS::Logs::DeliveryDestination <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverydestination.html>`_ or `PutDeliveryDestination <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutDeliveryDestination.html>`_ .
    - Create a *delivery* by pairing exactly one delivery source and one delivery destination. For more information, see `AWS::Logs::Delivery <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-delivery.html>`_ or `CreateDelivery <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_CreateDelivery.html>`_ .

    You can configure a single delivery source to send logs to multiple destinations by creating multiple deliveries. You can also create multiple deliveries to configure multiple delivery sources to send logs to the same delivery destination.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-deliverysource.html
    :cloudformationResource: AWS::Logs::DeliverySource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_delivery_source_props_mixin = logs_mixins.CfnDeliverySourcePropsMixin(logs_mixins.CfnDeliverySourceMixinProps(
            log_type="logType",
            name="name",
            resource_arn="resourceArn",
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
        props: typing.Union[CfnDeliverySourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::DeliverySource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab946efc54d0e40b9272ff741e610c41612474f906f33975a49d22ddb7590ef8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d538e3d35b21f2692a0b81a06da6ad7c8936f35ade13a9d89d8405f13ca8808)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d834b7effd7c5d8f7ae1e66f65bfb649b3ed549d1eed5912b253617aae4f0acc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeliverySourceMixinProps:
        return typing.cast(CfnDeliverySourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDestinationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_name": "destinationName",
        "destination_policy": "destinationPolicy",
        "role_arn": "roleArn",
        "tags": "tags",
        "target_arn": "targetArn",
    },
)
class CfnDestinationMixinProps:
    def __init__(
        self,
        *,
        destination_name: typing.Optional[builtins.str] = None,
        destination_policy: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDestinationPropsMixin.

        :param destination_name: The name of the destination.
        :param destination_policy: An IAM policy document that governs which AWS accounts can create subscription filters against this destination.
        :param role_arn: The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.
        :param tags: The tags that have been assigned to this delivery destination.
        :param target_arn: The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_destination_mixin_props = logs_mixins.CfnDestinationMixinProps(
                destination_name="destinationName",
                destination_policy="destinationPolicy",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arn="targetArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51c0e11cbf0218875c845eb85c4e565f8013ec425d3d2dc6d779cfffa67a3eb5)
            check_type(argname="argument destination_name", value=destination_name, expected_type=type_hints["destination_name"])
            check_type(argname="argument destination_policy", value=destination_policy, expected_type=type_hints["destination_policy"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_name is not None:
            self._values["destination_name"] = destination_name
        if destination_policy is not None:
            self._values["destination_policy"] = destination_policy
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn

    @builtins.property
    def destination_name(self) -> typing.Optional[builtins.str]:
        '''The name of the destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationname
        '''
        result = self._values.get("destination_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination_policy(self) -> typing.Optional[builtins.str]:
        '''An IAM policy document that governs which AWS accounts can create subscription filters against this destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-destinationpolicy
        '''
        result = self._values.get("destination_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that permits CloudWatch Logs to send data to the specified AWS resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags that have been assigned to this delivery destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the physical target where the log events are delivered (for example, a Kinesis stream).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html#cfn-logs-destination-targetarn
        '''
        result = self._values.get("target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDestinationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDestinationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnDestinationPropsMixin",
):
    '''The AWS::Logs::Destination resource specifies a CloudWatch Logs destination.

    A destination encapsulates a physical resource (such as an Amazon Kinesis data stream) and enables you to subscribe that resource to a stream of log events.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-destination.html
    :cloudformationResource: AWS::Logs::Destination
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_destination_props_mixin = logs_mixins.CfnDestinationPropsMixin(logs_mixins.CfnDestinationMixinProps(
            destination_name="destinationName",
            destination_policy="destinationPolicy",
            role_arn="roleArn",
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
        props: typing.Union[CfnDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::Destination``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4a30e19bceccd3dd25bf89196507954a3b31a352974bdd429cbab2c433ad49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d69974d0b6fc339030d104d058801e112c135015119ba7cb5782cfde68fa006a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b014e964cf09f995ba397487d4a0fefa6241b8deac6afcaf8178c9ced13d2d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDestinationMixinProps:
        return typing.cast(CfnDestinationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "integration_name": "integrationName",
        "integration_type": "integrationType",
        "resource_config": "resourceConfig",
    },
)
class CfnIntegrationMixinProps:
    def __init__(
        self,
        *,
        integration_name: typing.Optional[builtins.str] = None,
        integration_type: typing.Optional[builtins.str] = None,
        resource_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.ResourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIntegrationPropsMixin.

        :param integration_name: The name of this integration.
        :param integration_type: The type of integration. Integrations with OpenSearch Service have the type ``OPENSEARCH`` .
        :param resource_config: This structure contains configuration details about an integration between CloudWatch Logs and another entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-integration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_integration_mixin_props = logs_mixins.CfnIntegrationMixinProps(
                integration_name="integrationName",
                integration_type="integrationType",
                resource_config=logs_mixins.CfnIntegrationPropsMixin.ResourceConfigProperty(
                    open_search_resource_config=logs_mixins.CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty(
                        application_arn="applicationArn",
                        dashboard_viewer_principals=["dashboardViewerPrincipals"],
                        data_source_role_arn="dataSourceRoleArn",
                        kms_key_arn="kmsKeyArn",
                        retention_days=123
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91bf1924fcc92e466527874a42dfec87f8a948bb89e9ac123894a8c344a99cd3)
            check_type(argname="argument integration_name", value=integration_name, expected_type=type_hints["integration_name"])
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
            check_type(argname="argument resource_config", value=resource_config, expected_type=type_hints["resource_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if integration_name is not None:
            self._values["integration_name"] = integration_name
        if integration_type is not None:
            self._values["integration_type"] = integration_type
        if resource_config is not None:
            self._values["resource_config"] = resource_config

    @builtins.property
    def integration_name(self) -> typing.Optional[builtins.str]:
        '''The name of this integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-integration.html#cfn-logs-integration-integrationname
        '''
        result = self._values.get("integration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_type(self) -> typing.Optional[builtins.str]:
        '''The type of integration.

        Integrations with OpenSearch Service have the type ``OPENSEARCH`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-integration.html#cfn-logs-integration-integrationtype
        '''
        result = self._values.get("integration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ResourceConfigProperty"]]:
        '''This structure contains configuration details about an integration between CloudWatch Logs and another entity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-integration.html#cfn-logs-integration-resourceconfig
        '''
        result = self._values.get("resource_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.ResourceConfigProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnIntegrationPropsMixin",
):
    '''Creates an integration between CloudWatch Logs and another service in this account.

    Currently, only integrations with OpenSearch Service are supported, and currently you can have only one integration in your account.

    Integrating with OpenSearch Service makes it possible for you to create curated vended logs dashboards, powered by OpenSearch Service analytics. For more information, see `Vended log dashboards powered by Amazon OpenSearch Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs-OpenSearch-Dashboards.html>`_ .

    You can use this operation only to create a new integration. You can't modify an existing integration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-integration.html
    :cloudformationResource: AWS::Logs::Integration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_integration_props_mixin = logs_mixins.CfnIntegrationPropsMixin(logs_mixins.CfnIntegrationMixinProps(
            integration_name="integrationName",
            integration_type="integrationType",
            resource_config=logs_mixins.CfnIntegrationPropsMixin.ResourceConfigProperty(
                open_search_resource_config=logs_mixins.CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty(
                    application_arn="applicationArn",
                    dashboard_viewer_principals=["dashboardViewerPrincipals"],
                    data_source_role_arn="dataSourceRoleArn",
                    kms_key_arn="kmsKeyArn",
                    retention_days=123
                )
            )
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
        '''Create a mixin to apply properties to ``AWS::Logs::Integration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37b5d1da24fe0202150d41aebb0280fecf9f8c2313dd9b011471fe521968befe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bcbfb774d1a790990e7d72775f06c886f46aa878ee272b3db8e6c396b203d356)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98363275cc5186becfe597c122fa83d08b169e4fc6e2f1ae58c713bb85dd0f54)
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
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_arn": "applicationArn",
            "dashboard_viewer_principals": "dashboardViewerPrincipals",
            "data_source_role_arn": "dataSourceRoleArn",
            "kms_key_arn": "kmsKeyArn",
            "retention_days": "retentionDays",
        },
    )
    class OpenSearchResourceConfigProperty:
        def __init__(
            self,
            *,
            application_arn: typing.Optional[builtins.str] = None,
            dashboard_viewer_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
            data_source_role_arn: typing.Optional[builtins.str] = None,
            kms_key_arn: typing.Optional[builtins.str] = None,
            retention_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This structure contains configuration details about an integration between CloudWatch Logs and OpenSearch Service.

            :param application_arn: If you want to use an existing OpenSearch Service application for your integration with OpenSearch Service, specify it here. If you omit this, a new application will be created.
            :param dashboard_viewer_principals: Specify the ARNs of IAM roles and IAM users who you want to grant permission to for viewing the dashboards. .. epigraph:: In addition to specifying these users here, you must also grant them the *CloudWatchOpenSearchDashboardAccess* IAM policy. For more information, see `IAM policies for users <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/OpenSearch-Dashboards-UserRoles.html>`_ .
            :param data_source_role_arn: Specify the ARN of an IAM role that CloudWatch Logs will use to create the integration. This role must have the permissions necessary to access the OpenSearch Service collection to be able to create the dashboards. For more information about the permissions needed, see `Permissions that the integration needs <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/OpenSearch-Dashboards-CreateRole.html>`_ in the CloudWatch Logs User Guide.
            :param kms_key_arn: To have the vended dashboard data encrypted with AWS instead of the CloudWatch Logs default encryption method, specify the ARN of the AWS key that you want to use.
            :param retention_days: Specify how many days that you want the data derived by OpenSearch Service to be retained in the index that the dashboard refers to. This also sets the maximum time period that you can choose when viewing data in the dashboard. Choosing a longer time frame will incur additional costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-opensearchresourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                open_search_resource_config_property = logs_mixins.CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty(
                    application_arn="applicationArn",
                    dashboard_viewer_principals=["dashboardViewerPrincipals"],
                    data_source_role_arn="dataSourceRoleArn",
                    kms_key_arn="kmsKeyArn",
                    retention_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0fdfcdaca7a0ffdb5ec3990a595f52661b6534ba0c01b9e71ac24fce87d311a4)
                check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
                check_type(argname="argument dashboard_viewer_principals", value=dashboard_viewer_principals, expected_type=type_hints["dashboard_viewer_principals"])
                check_type(argname="argument data_source_role_arn", value=data_source_role_arn, expected_type=type_hints["data_source_role_arn"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument retention_days", value=retention_days, expected_type=type_hints["retention_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_arn is not None:
                self._values["application_arn"] = application_arn
            if dashboard_viewer_principals is not None:
                self._values["dashboard_viewer_principals"] = dashboard_viewer_principals
            if data_source_role_arn is not None:
                self._values["data_source_role_arn"] = data_source_role_arn
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if retention_days is not None:
                self._values["retention_days"] = retention_days

        @builtins.property
        def application_arn(self) -> typing.Optional[builtins.str]:
            '''If you want to use an existing OpenSearch Service application for your integration with OpenSearch Service, specify it here.

            If you omit this, a new application will be created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-opensearchresourceconfig.html#cfn-logs-integration-opensearchresourceconfig-applicationarn
            '''
            result = self._values.get("application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dashboard_viewer_principals(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify the ARNs of IAM roles and IAM users who you want to grant permission to for viewing the dashboards.

            .. epigraph::

               In addition to specifying these users here, you must also grant them the *CloudWatchOpenSearchDashboardAccess* IAM policy. For more information, see `IAM policies for users <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/OpenSearch-Dashboards-UserRoles.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-opensearchresourceconfig.html#cfn-logs-integration-opensearchresourceconfig-dashboardviewerprincipals
            '''
            result = self._values.get("dashboard_viewer_principals")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def data_source_role_arn(self) -> typing.Optional[builtins.str]:
            '''Specify the ARN of an IAM role that CloudWatch Logs will use to create the integration.

            This role must have the permissions necessary to access the OpenSearch Service collection to be able to create the dashboards. For more information about the permissions needed, see `Permissions that the integration needs <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/OpenSearch-Dashboards-CreateRole.html>`_ in the CloudWatch Logs User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-opensearchresourceconfig.html#cfn-logs-integration-opensearchresourceconfig-datasourcerolearn
            '''
            result = self._values.get("data_source_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''To have the vended dashboard data encrypted with AWS  instead of the CloudWatch Logs default encryption method, specify the ARN of the AWS  key that you want to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-opensearchresourceconfig.html#cfn-logs-integration-opensearchresourceconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_days(self) -> typing.Optional[jsii.Number]:
            '''Specify how many days that you want the data derived by OpenSearch Service to be retained in the index that the dashboard refers to.

            This also sets the maximum time period that you can choose when viewing data in the dashboard. Choosing a longer time frame will incur additional costs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-opensearchresourceconfig.html#cfn-logs-integration-opensearchresourceconfig-retentiondays
            '''
            result = self._values.get("retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenSearchResourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnIntegrationPropsMixin.ResourceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"open_search_resource_config": "openSearchResourceConfig"},
    )
    class ResourceConfigProperty:
        def __init__(
            self,
            *,
            open_search_resource_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This structure contains configuration details about an integration between CloudWatch Logs and another entity.

            :param open_search_resource_config: This structure contains configuration details about an integration between CloudWatch Logs and OpenSearch Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-resourceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                resource_config_property = logs_mixins.CfnIntegrationPropsMixin.ResourceConfigProperty(
                    open_search_resource_config=logs_mixins.CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty(
                        application_arn="applicationArn",
                        dashboard_viewer_principals=["dashboardViewerPrincipals"],
                        data_source_role_arn="dataSourceRoleArn",
                        kms_key_arn="kmsKeyArn",
                        retention_days=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6016ad3647dd01167a3bc4c44c648093c83230c3265c638a6ca74cf1312ebab6)
                check_type(argname="argument open_search_resource_config", value=open_search_resource_config, expected_type=type_hints["open_search_resource_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if open_search_resource_config is not None:
                self._values["open_search_resource_config"] = open_search_resource_config

        @builtins.property
        def open_search_resource_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty"]]:
            '''This structure contains configuration details about an integration between CloudWatch Logs and OpenSearch Service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-integration-resourceconfig.html#cfn-logs-integration-resourceconfig-opensearchresourceconfig
            '''
            result = self._values.get("open_search_resource_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnLogAnomalyDetectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountId",
        "anomaly_visibility_time": "anomalyVisibilityTime",
        "detector_name": "detectorName",
        "evaluation_frequency": "evaluationFrequency",
        "filter_pattern": "filterPattern",
        "kms_key_id": "kmsKeyId",
        "log_group_arn_list": "logGroupArnList",
    },
)
class CfnLogAnomalyDetectorMixinProps:
    def __init__(
        self,
        *,
        account_id: typing.Optional[builtins.str] = None,
        anomaly_visibility_time: typing.Optional[jsii.Number] = None,
        detector_name: typing.Optional[builtins.str] = None,
        evaluation_frequency: typing.Optional[builtins.str] = None,
        filter_pattern: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnLogAnomalyDetectorPropsMixin.

        :param account_id: The ID of the account to create the anomaly detector in.
        :param anomaly_visibility_time: The number of days to have visibility on an anomaly. After this time period has elapsed for an anomaly, it will be automatically baselined and the anomaly detector will treat new occurrences of a similar anomaly as normal. Therefore, if you do not correct the cause of an anomaly during the time period specified in ``AnomalyVisibilityTime`` , it will be considered normal going forward and will not be detected as an anomaly.
        :param detector_name: A name for this anomaly detector.
        :param evaluation_frequency: Specifies how often the anomaly detector is to run and look for anomalies. Set this value according to the frequency that the log group receives new logs. For example, if the log group receives new log events every 10 minutes, then 15 minutes might be a good setting for ``EvaluationFrequency`` .
        :param filter_pattern: You can use this parameter to limit the anomaly detection model to examine only log events that match the pattern you specify here. For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param kms_key_id: Optionally assigns a AWS key to secure this anomaly detector and its findings. If a key is assigned, the anomalies found and the model used by this detector are encrypted at rest with the key. If a key is assigned to an anomaly detector, a user must have permissions for both this key and for the anomaly detector to retrieve information about the anomalies that it finds. For more information about using a AWS key and to see the required IAM policy, see `Use a AWS key with an anomaly detector <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsAnomalyDetection-KMS.html>`_ .
        :param log_group_arn_list: The ARN of the log group that is associated with this anomaly detector. You can specify only one log group ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_log_anomaly_detector_mixin_props = logs_mixins.CfnLogAnomalyDetectorMixinProps(
                account_id="accountId",
                anomaly_visibility_time=123,
                detector_name="detectorName",
                evaluation_frequency="evaluationFrequency",
                filter_pattern="filterPattern",
                kms_key_id="kmsKeyId",
                log_group_arn_list=["logGroupArnList"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8091252a33657603d33b68415c1ada5da2daef79054e92d2e40e05ea28603ff5)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument anomaly_visibility_time", value=anomaly_visibility_time, expected_type=type_hints["anomaly_visibility_time"])
            check_type(argname="argument detector_name", value=detector_name, expected_type=type_hints["detector_name"])
            check_type(argname="argument evaluation_frequency", value=evaluation_frequency, expected_type=type_hints["evaluation_frequency"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_group_arn_list", value=log_group_arn_list, expected_type=type_hints["log_group_arn_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id
        if anomaly_visibility_time is not None:
            self._values["anomaly_visibility_time"] = anomaly_visibility_time
        if detector_name is not None:
            self._values["detector_name"] = detector_name
        if evaluation_frequency is not None:
            self._values["evaluation_frequency"] = evaluation_frequency
        if filter_pattern is not None:
            self._values["filter_pattern"] = filter_pattern
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_group_arn_list is not None:
            self._values["log_group_arn_list"] = log_group_arn_list

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the account to create the anomaly detector in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-accountid
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def anomaly_visibility_time(self) -> typing.Optional[jsii.Number]:
        '''The number of days to have visibility on an anomaly.

        After this time period has elapsed for an anomaly, it will be automatically baselined and the anomaly detector will treat new occurrences of a similar anomaly as normal. Therefore, if you do not correct the cause of an anomaly during the time period specified in ``AnomalyVisibilityTime`` , it will be considered normal going forward and will not be detected as an anomaly.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-anomalyvisibilitytime
        '''
        result = self._values.get("anomaly_visibility_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def detector_name(self) -> typing.Optional[builtins.str]:
        '''A name for this anomaly detector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-detectorname
        '''
        result = self._values.get("detector_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_frequency(self) -> typing.Optional[builtins.str]:
        '''Specifies how often the anomaly detector is to run and look for anomalies.

        Set this value according to the frequency that the log group receives new logs. For example, if the log group receives new log events every 10 minutes, then 15 minutes might be a good setting for ``EvaluationFrequency`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-evaluationfrequency
        '''
        result = self._values.get("evaluation_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_pattern(self) -> typing.Optional[builtins.str]:
        '''You can use this parameter to limit the anomaly detection model to examine only log events that match the pattern you specify here.

        For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-filterpattern
        '''
        result = self._values.get("filter_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Optionally assigns a AWS  key to secure this anomaly detector and its findings.

        If a key is assigned, the anomalies found and the model used by this detector are encrypted at rest with the key. If a key is assigned to an anomaly detector, a user must have permissions for both this key and for the anomaly detector to retrieve information about the anomalies that it finds.

        For more information about using a AWS  key and to see the required IAM policy, see `Use a AWS  key with an anomaly detector <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsAnomalyDetection-KMS.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_arn_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARN of the log group that is associated with this anomaly detector.

        You can specify only one log group ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html#cfn-logs-loganomalydetector-loggrouparnlist
        '''
        result = self._values.get("log_group_arn_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogAnomalyDetectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLogAnomalyDetectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnLogAnomalyDetectorPropsMixin",
):
    '''Creates or updates an *anomaly detector* that regularly scans one or more log groups and look for patterns and anomalies in the logs.

    An anomaly detector can help surface issues by automatically discovering anomalies in your log event traffic. An anomaly detector uses machine learning algorithms to scan log events and find *patterns* . A pattern is a shared text structure that recurs among your log fields. Patterns provide a useful tool for analyzing large sets of logs because a large number of log events can often be compressed into a few patterns.

    The anomaly detector uses pattern recognition to find ``anomalies`` , which are unusual log events. It compares current log events and patterns with trained baselines.

    Fields within a pattern are called *tokens* . Fields that vary within a pattern, such as a request ID or timestamp, are referred to as *dynamic tokens* and represented by ``<*>`` .

    For more information see `Log anomaly detection <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsAnomalyDetection.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loganomalydetector.html
    :cloudformationResource: AWS::Logs::LogAnomalyDetector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_log_anomaly_detector_props_mixin = logs_mixins.CfnLogAnomalyDetectorPropsMixin(logs_mixins.CfnLogAnomalyDetectorMixinProps(
            account_id="accountId",
            anomaly_visibility_time=123,
            detector_name="detectorName",
            evaluation_frequency="evaluationFrequency",
            filter_pattern="filterPattern",
            kms_key_id="kmsKeyId",
            log_group_arn_list=["logGroupArnList"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLogAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::LogAnomalyDetector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9c7386b4d5d41219a865b789addeaf5b5e9ca261f5dae4cf913653b7e1fd75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2656bf8e2a4704f127e1c7eea975e301985a02ce1f577fe1ecc1996ec9f7321)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42015450c2adda1ce4cc44330d0e6706e20a8d67c6498493bb3e950d829dbd31)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLogAnomalyDetectorMixinProps:
        return typing.cast(CfnLogAnomalyDetectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnLogGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_protection_policy": "dataProtectionPolicy",
        "field_index_policies": "fieldIndexPolicies",
        "kms_key_id": "kmsKeyId",
        "log_group_class": "logGroupClass",
        "log_group_name": "logGroupName",
        "resource_policy_document": "resourcePolicyDocument",
        "retention_in_days": "retentionInDays",
        "tags": "tags",
    },
)
class CfnLogGroupMixinProps:
    def __init__(
        self,
        *,
        data_protection_policy: typing.Any = None,
        field_index_policies: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        log_group_class: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        resource_policy_document: typing.Any = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLogGroupPropsMixin.

        :param data_protection_policy: Creates a data protection policy and assigns it to the log group. A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks.
        :param field_index_policies: Creates or updates a *field index policy* for the specified log group. Only log groups in the Standard log class support field index policies. For more information about log classes, see `Log classes <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html>`_ . You can use field index policies to create *field indexes* on fields found in log events in the log group. Creating field indexes lowers the costs for CloudWatch Logs Insights queries that reference those field indexes, because these queries attempt to skip the processing of log events that are known to not match the indexed field. Good fields to index are fields that you often need to query for and fields that have high cardinality of values Common examples of indexes include request ID, session ID, userID, and instance IDs. For more information, see `Create field indexes to improve query performance and reduce costs <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs-Field-Indexing.html>`_ . Currently, this array supports only one field index policy object.
        :param kms_key_id: The Amazon Resource Name (ARN) of the AWS key to use when encrypting log data. To associate an AWS key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested. If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error. Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_
        :param log_group_class: Specifies the log group class for this log group. There are two classes:. - The ``Standard`` log class supports all CloudWatch Logs features. - The ``Infrequent Access`` log class supports a subset of CloudWatch Logs features and incurs lower costs. For details about the features supported by each class, see `Log classes <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html>`_ Default: - "STANDARD"
        :param log_group_name: The name of the log group. If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.
        :param resource_policy_document: Creates or updates a resource policy for the specified log group that allows other services to put log events to this account. A LogGroup can have 1 resource policy.
        :param retention_in_days: The number of days to retain the log events in the specified log group. Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653. To set a log group so that its log events do not expire, do not specify this property.
        :param tags: An array of key-value pairs to apply to the log group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            # data_protection_policy: Any
            # field_index_policies: Any
            # resource_policy_document: Any
            
            cfn_log_group_mixin_props = logs_mixins.CfnLogGroupMixinProps(
                data_protection_policy=data_protection_policy,
                field_index_policies=[field_index_policies],
                kms_key_id="kmsKeyId",
                log_group_class="logGroupClass",
                log_group_name="logGroupName",
                resource_policy_document=resource_policy_document,
                retention_in_days=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcfd36f3547ccea21154310cb409dd269198e62678326cf43b7418109b08b10)
            check_type(argname="argument data_protection_policy", value=data_protection_policy, expected_type=type_hints["data_protection_policy"])
            check_type(argname="argument field_index_policies", value=field_index_policies, expected_type=type_hints["field_index_policies"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument log_group_class", value=log_group_class, expected_type=type_hints["log_group_class"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument resource_policy_document", value=resource_policy_document, expected_type=type_hints["resource_policy_document"])
            check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_protection_policy is not None:
            self._values["data_protection_policy"] = data_protection_policy
        if field_index_policies is not None:
            self._values["field_index_policies"] = field_index_policies
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if log_group_class is not None:
            self._values["log_group_class"] = log_group_class
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if resource_policy_document is not None:
            self._values["resource_policy_document"] = resource_policy_document
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_protection_policy(self) -> typing.Any:
        '''Creates a data protection policy and assigns it to the log group.

        A data protection policy can help safeguard sensitive data that's ingested by the log group by auditing and masking the sensitive log data. When a user who does not have permission to view masked data views a log event that includes masked data, the sensitive data is replaced by asterisks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-dataprotectionpolicy
        '''
        result = self._values.get("data_protection_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def field_index_policies(
        self,
    ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
        '''Creates or updates a *field index policy* for the specified log group.

        Only log groups in the Standard log class support field index policies. For more information about log classes, see `Log classes <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html>`_ .

        You can use field index policies to create *field indexes* on fields found in log events in the log group. Creating field indexes lowers the costs for CloudWatch Logs Insights queries that reference those field indexes, because these queries attempt to skip the processing of log events that are known to not match the indexed field. Good fields to index are fields that you often need to query for and fields that have high cardinality of values Common examples of indexes include request ID, session ID, userID, and instance IDs. For more information, see `Create field indexes to improve query performance and reduce costs <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs-Field-Indexing.html>`_ .

        Currently, this array supports only one field index policy object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-fieldindexpolicies
        '''
        result = self._values.get("field_index_policies")
        return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS  key to use when encrypting log data.

        To associate an AWS  key with the log group, specify the ARN of that KMS key here. If you do so, ingested data is encrypted using this key. This association is stored as long as the data encrypted with the KMS key is still within CloudWatch Logs . This enables CloudWatch Logs to decrypt this data whenever it is requested.

        If you attempt to associate a KMS key with the log group but the KMS key doesn't exist or is deactivated, you will receive an ``InvalidParameterException`` error.

        Log group data is always encrypted in CloudWatch Logs . If you omit this key, the encryption does not use AWS  . For more information, see `Encrypt log data in CloudWatch Logs using AWS Key Management Service <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_class(self) -> typing.Optional[builtins.str]:
        '''Specifies the log group class for this log group. There are two classes:.

        - The ``Standard`` log class supports all CloudWatch Logs features.
        - The ``Infrequent Access`` log class supports a subset of CloudWatch Logs features and incurs lower costs.

        For details about the features supported by each class, see `Log classes <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html>`_

        :default: - "STANDARD"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupclass
        '''
        result = self._values.get("log_group_class")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log group.

        If you don't specify a name, AWS CloudFormation generates a unique ID for the log group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_policy_document(self) -> typing.Any:
        '''Creates or updates a resource policy for the specified log group that allows other services to put log events to this account.

        A LogGroup can have 1 resource policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-resourcepolicydocument
        '''
        result = self._values.get("resource_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''The number of days to retain the log events in the specified log group.

        Possible values are: 1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1096, 1827, 2192, 2557, 2922, 3288, and 3653.

        To set a log group so that its log events do not expire, do not specify this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-retentionindays
        '''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to the log group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html#cfn-logs-loggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLogGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnLogGroupPropsMixin",
):
    '''The ``AWS::Logs::LogGroup`` resource specifies a log group.

    A log group defines common properties for log streams, such as their retention and access control rules. Each log stream must belong to one log group.

    You can create up to 1,000,000 log groups per Region per account. You must use the following guidelines when naming a log group:

    - Log group names must be unique within a Region for an AWS account.
    - Log group names can be between 1 and 512 characters long.
    - Log group names consist of the following characters: a-z, A-Z, 0-9, '_' (underscore), '-' (hyphen), '/' (forward slash), and '.' (period).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-loggroup.html
    :cloudformationResource: AWS::Logs::LogGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        # data_protection_policy: Any
        # field_index_policies: Any
        # resource_policy_document: Any
        
        cfn_log_group_props_mixin = logs_mixins.CfnLogGroupPropsMixin(logs_mixins.CfnLogGroupMixinProps(
            data_protection_policy=data_protection_policy,
            field_index_policies=[field_index_policies],
            kms_key_id="kmsKeyId",
            log_group_class="logGroupClass",
            log_group_name="logGroupName",
            resource_policy_document=resource_policy_document,
            retention_in_days=123,
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
        props: typing.Union[CfnLogGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::LogGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8d50e8b584f8ee1a76db798f0ebdca5c38e01b57a8417c6c99287a2b9e3374)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ca2eecd83565ff1e2ca9ead627b16918917a791159a611295cbc203fdc57d01)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e188a6c2cadda4bfa9e60bf5697dffe63f77b1c1c960eadea162a04a7a9619)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLogGroupMixinProps:
        return typing.cast(CfnLogGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnLogStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_name": "logGroupName",
        "log_stream_name": "logStreamName",
    },
)
class CfnLogStreamMixinProps:
    def __init__(
        self,
        *,
        log_group_name: typing.Optional[builtins.str] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLogStreamPropsMixin.

        :param log_group_name: The name of the log group where the log stream is created.
        :param log_stream_name: The name of the log stream. The name must be unique within the log group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_log_stream_mixin_props = logs_mixins.CfnLogStreamMixinProps(
                log_group_name="logGroupName",
                log_stream_name="logStreamName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8c9e04946990dabab366c72294fe0cf40f76d69efbd528f0c2ad8aa3620bca)
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log group where the log stream is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''The name of the log stream.

        The name must be unique within the log group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html#cfn-logs-logstream-logstreamname
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLogStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLogStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnLogStreamPropsMixin",
):
    '''The ``AWS::Logs::LogStream`` resource specifies an Amazon CloudWatch Logs log stream in a specific log group.

    A log stream represents the sequence of events coming from an application instance or resource that you are monitoring.

    There is no limit on the number of log streams that you can create for a log group.

    You must use the following guidelines when naming a log stream:

    - Log stream names must be unique within the log group.
    - Log stream names can be between 1 and 512 characters long.
    - The ':' (colon) and '*' (asterisk) characters are not allowed.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-logstream.html
    :cloudformationResource: AWS::Logs::LogStream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_log_stream_props_mixin = logs_mixins.CfnLogStreamPropsMixin(logs_mixins.CfnLogStreamMixinProps(
            log_group_name="logGroupName",
            log_stream_name="logStreamName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLogStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::LogStream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f3e3444e26a482dc65223cc4e7a99872ef98500b321af35923daeddb4fe5f54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12d118a2f81f692e58a5cbd7382bd0f14bec00354eb8d6177a282a5c56a50181)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__630fcb337b32d4fd1f293498effbffd42da1be814c622bce5b60110b1b9be845)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLogStreamMixinProps:
        return typing.cast(CfnLogStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnMetricFilterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "apply_on_transformed_logs": "applyOnTransformedLogs",
        "emit_system_field_dimensions": "emitSystemFieldDimensions",
        "field_selection_criteria": "fieldSelectionCriteria",
        "filter_name": "filterName",
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "metric_transformations": "metricTransformations",
    },
)
class CfnMetricFilterMixinProps:
    def __init__(
        self,
        *,
        apply_on_transformed_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        emit_system_field_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
        field_selection_criteria: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        filter_pattern: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        metric_transformations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMetricFilterPropsMixin.MetricTransformationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnMetricFilterPropsMixin.

        :param apply_on_transformed_logs: This parameter is valid only for log groups that have an active log transformer. For more information about log transformers, see `PutTransformer <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html>`_ . If this value is ``true`` , the metric filter is applied on the transformed version of the log events instead of the original ingested log events.
        :param emit_system_field_dimensions: The list of system fields that are emitted as additional dimensions in the generated metrics. Returns the ``emitSystemFieldDimensions`` value if it was specified when the metric filter was created.
        :param field_selection_criteria: The filter expression that specifies which log events are processed by this metric filter based on system fields. Returns the ``fieldSelectionCriteria`` value if it was specified when the metric filter was created.
        :param filter_name: The name of the metric filter.
        :param filter_pattern: A filter pattern for extracting metric data out of ingested log events. For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The name of an existing log group that you want to associate with this metric filter.
        :param metric_transformations: The metric transformations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_metric_filter_mixin_props = logs_mixins.CfnMetricFilterMixinProps(
                apply_on_transformed_logs=False,
                emit_system_field_dimensions=["emitSystemFieldDimensions"],
                field_selection_criteria="fieldSelectionCriteria",
                filter_name="filterName",
                filter_pattern="filterPattern",
                log_group_name="logGroupName",
                metric_transformations=[logs_mixins.CfnMetricFilterPropsMixin.MetricTransformationProperty(
                    default_value=123,
                    dimensions=[logs_mixins.CfnMetricFilterPropsMixin.DimensionProperty(
                        key="key",
                        value="value"
                    )],
                    metric_name="metricName",
                    metric_namespace="metricNamespace",
                    metric_value="metricValue",
                    unit="unit"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12afaf3844ca8961e1e3fb91073af969d7d5443f669fef5737c445d0812f8322)
            check_type(argname="argument apply_on_transformed_logs", value=apply_on_transformed_logs, expected_type=type_hints["apply_on_transformed_logs"])
            check_type(argname="argument emit_system_field_dimensions", value=emit_system_field_dimensions, expected_type=type_hints["emit_system_field_dimensions"])
            check_type(argname="argument field_selection_criteria", value=field_selection_criteria, expected_type=type_hints["field_selection_criteria"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument metric_transformations", value=metric_transformations, expected_type=type_hints["metric_transformations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apply_on_transformed_logs is not None:
            self._values["apply_on_transformed_logs"] = apply_on_transformed_logs
        if emit_system_field_dimensions is not None:
            self._values["emit_system_field_dimensions"] = emit_system_field_dimensions
        if field_selection_criteria is not None:
            self._values["field_selection_criteria"] = field_selection_criteria
        if filter_name is not None:
            self._values["filter_name"] = filter_name
        if filter_pattern is not None:
            self._values["filter_pattern"] = filter_pattern
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if metric_transformations is not None:
            self._values["metric_transformations"] = metric_transformations

    @builtins.property
    def apply_on_transformed_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''This parameter is valid only for log groups that have an active log transformer.

        For more information about log transformers, see `PutTransformer <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html>`_ .

        If this value is ``true`` , the metric filter is applied on the transformed version of the log events instead of the original ingested log events.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-applyontransformedlogs
        '''
        result = self._values.get("apply_on_transformed_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def emit_system_field_dimensions(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of system fields that are emitted as additional dimensions in the generated metrics.

        Returns the ``emitSystemFieldDimensions`` value if it was specified when the metric filter was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-emitsystemfielddimensions
        '''
        result = self._values.get("emit_system_field_dimensions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def field_selection_criteria(self) -> typing.Optional[builtins.str]:
        '''The filter expression that specifies which log events are processed by this metric filter based on system fields.

        Returns the ``fieldSelectionCriteria`` value if it was specified when the metric filter was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-fieldselectioncriteria
        '''
        result = self._values.get("field_selection_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filtername
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_pattern(self) -> typing.Optional[builtins.str]:
        '''A filter pattern for extracting metric data out of ingested log events.

        For more information, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of an existing log group that you want to associate with this metric filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metric_transformations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricFilterPropsMixin.MetricTransformationProperty"]]]]:
        '''The metric transformations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html#cfn-logs-metricfilter-metrictransformations
        '''
        result = self._values.get("metric_transformations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricFilterPropsMixin.MetricTransformationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMetricFilterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMetricFilterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnMetricFilterPropsMixin",
):
    '''The ``AWS::Logs::MetricFilter`` resource specifies a metric filter that describes how CloudWatch Logs extracts information from logs and transforms it into Amazon CloudWatch metrics.

    If you have multiple metric filters that are associated with a log group, all the filters are applied to the log streams in that group.

    The maximum number of metric filters that can be associated with a log group is 100.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-metricfilter.html
    :cloudformationResource: AWS::Logs::MetricFilter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_metric_filter_props_mixin = logs_mixins.CfnMetricFilterPropsMixin(logs_mixins.CfnMetricFilterMixinProps(
            apply_on_transformed_logs=False,
            emit_system_field_dimensions=["emitSystemFieldDimensions"],
            field_selection_criteria="fieldSelectionCriteria",
            filter_name="filterName",
            filter_pattern="filterPattern",
            log_group_name="logGroupName",
            metric_transformations=[logs_mixins.CfnMetricFilterPropsMixin.MetricTransformationProperty(
                default_value=123,
                dimensions=[logs_mixins.CfnMetricFilterPropsMixin.DimensionProperty(
                    key="key",
                    value="value"
                )],
                metric_name="metricName",
                metric_namespace="metricNamespace",
                metric_value="metricValue",
                unit="unit"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMetricFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::MetricFilter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244449fd6cfbff41a6b557b5a3dce05abdde8da042a647d7fce1b6fd9609dee5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__36902c8bbb50d401af7a986179c9369abb61b07abe240869fcf64f1b4261fc3b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5d66476210d8b53eb8b7209c5068026b80a78aadde39d845a5cfe546d58e0c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMetricFilterMixinProps:
        return typing.cast(CfnMetricFilterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnMetricFilterPropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DimensionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the CloudWatch metric dimensions to publish with this metric.

            Because dimensions are part of the unique identifier for a metric, whenever a unique dimension name/value pair is extracted from your logs, you are creating a new variation of that metric.

            For more information about publishing dimensions with metrics created by metric filters, see `Publishing dimensions with metrics from values in JSON or space-delimited log events <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html#logs-metric-filters-dimensions>`_ .
            .. epigraph::

               Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric.

               To help prevent accidental high charges, Amazon disables a metric filter if it generates 1000 different name/value pairs for the dimensions that you have specified within a certain amount of time.

               You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .

            :param key: The name for the CloudWatch metric dimension that the metric filter creates. Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon (:).
            :param value: The log event field that will contain the value for this dimension. This dimension will only be published for a metric if the value is found in the log event. For example, ``$.eventType`` for JSON log events, or ``$server`` for space-delimited log events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                dimension_property = logs_mixins.CfnMetricFilterPropsMixin.DimensionProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13c17365c0cbf8ab8061494e453e2f2f8f3982480aa0a346a6288a7617cc49c2)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name for the CloudWatch metric dimension that the metric filter creates.

            Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon (:).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html#cfn-logs-metricfilter-dimension-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The log event field that will contain the value for this dimension.

            This dimension will only be published for a metric if the value is found in the log event. For example, ``$.eventType`` for JSON log events, or ``$server`` for space-delimited log events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-dimension.html#cfn-logs-metricfilter-dimension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnMetricFilterPropsMixin.MetricTransformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_value": "defaultValue",
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "metric_namespace": "metricNamespace",
            "metric_value": "metricValue",
            "unit": "unit",
        },
    )
    class MetricTransformationProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[jsii.Number] = None,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMetricFilterPropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            metric_namespace: typing.Optional[builtins.str] = None,
            metric_value: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MetricTransformation`` is a property of the ``AWS::Logs::MetricFilter`` resource that describes how to transform log streams into a CloudWatch metric.

            :param default_value: (Optional) The value to emit when a filter pattern does not match a log event. This value can be null.
            :param dimensions: The fields to use as dimensions for the metric. One metric filter can include as many as three dimensions. .. epigraph:: Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric. CloudWatch Logs disables a metric filter if it generates 1000 different name/value pairs for your specified dimensions within a certain amount of time. This helps to prevent accidental high charges. You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .
            :param metric_name: The name of the CloudWatch metric.
            :param metric_namespace: A custom namespace to contain your metric in CloudWatch. Use namespaces to group together metrics that are similar. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .
            :param metric_value: The value that is published to the CloudWatch metric. For example, if you're counting the occurrences of a particular term like ``Error`` , specify 1 for the metric value. If you're counting the number of bytes transferred, reference the value that is in the log event by using $. followed by the name of the field that you specified in the filter pattern, such as ``$.size`` .
            :param unit: The unit to assign to the metric. If you omit this, the unit is set as ``None`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                metric_transformation_property = logs_mixins.CfnMetricFilterPropsMixin.MetricTransformationProperty(
                    default_value=123,
                    dimensions=[logs_mixins.CfnMetricFilterPropsMixin.DimensionProperty(
                        key="key",
                        value="value"
                    )],
                    metric_name="metricName",
                    metric_namespace="metricNamespace",
                    metric_value="metricValue",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b8509f92d16a099fa4fa39f63077ba54904091b4d1fad7656dce5994ab8f2d81)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
                check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if metric_namespace is not None:
                self._values["metric_namespace"] = metric_namespace
            if metric_value is not None:
                self._values["metric_value"] = metric_value
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def default_value(self) -> typing.Optional[jsii.Number]:
            '''(Optional) The value to emit when a filter pattern does not match a log event.

            This value can be null.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricFilterPropsMixin.DimensionProperty"]]]]:
            '''The fields to use as dimensions for the metric. One metric filter can include as many as three dimensions.

            .. epigraph::

               Metrics extracted from log events are charged as custom metrics. To prevent unexpected high charges, do not specify high-cardinality fields such as ``IPAddress`` or ``requestID`` as dimensions. Each different value found for a dimension is treated as a separate metric and accrues charges as a separate custom metric.

               CloudWatch Logs disables a metric filter if it generates 1000 different name/value pairs for your specified dimensions within a certain amount of time. This helps to prevent accidental high charges.

               You can also set up a billing alarm to alert you if your charges are higher than expected. For more information, see `Creating a Billing Alarm to Monitor Your Estimated AWS Charges <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitor_estimated_charges_with_cloudwatch.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMetricFilterPropsMixin.DimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the CloudWatch metric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_namespace(self) -> typing.Optional[builtins.str]:
            '''A custom namespace to contain your metric in CloudWatch.

            Use namespaces to group together metrics that are similar. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricnamespace
            '''
            result = self._values.get("metric_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_value(self) -> typing.Optional[builtins.str]:
            '''The value that is published to the CloudWatch metric.

            For example, if you're counting the occurrences of a particular term like ``Error`` , specify 1 for the metric value. If you're counting the number of bytes transferred, reference the value that is in the log event by using $. followed by the name of the field that you specified in the filter pattern, such as ``$.size`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-metricvalue
            '''
            result = self._values.get("metric_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to assign to the metric.

            If you omit this, the unit is set as ``None`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-metricfilter-metrictransformation.html#cfn-logs-metricfilter-metrictransformation-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricTransformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnQueryDefinitionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_names": "logGroupNames",
        "name": "name",
        "query_language": "queryLanguage",
        "query_string": "queryString",
    },
)
class CfnQueryDefinitionMixinProps:
    def __init__(
        self,
        *,
        log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        query_language: typing.Optional[builtins.str] = None,
        query_string: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnQueryDefinitionPropsMixin.

        :param log_group_names: Use this parameter if you want the query to query only certain log groups.
        :param name: A name for the query definition. .. epigraph:: You can use the name to create a folder structure for your queries. To create a folder, use a forward slash (/) to prefix your desired query name with your desired folder name. For example, ``*folder-name* / *query-name*`` .
        :param query_language: The query language used for this query. For more information about the query languages that CloudWatch Logs supports, see `Supported query languages <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_AnalyzeLogData_Languages.html>`_ . Default: - "CWLI"
        :param query_string: The query string to use for this query definition. For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_query_definition_mixin_props = logs_mixins.CfnQueryDefinitionMixinProps(
                log_group_names=["logGroupNames"],
                name="name",
                query_language="queryLanguage",
                query_string="queryString"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4c993fa29bebca5c6105c766e26bf83c23b46e71a5259b92387872fcc5d990)
            check_type(argname="argument log_group_names", value=log_group_names, expected_type=type_hints["log_group_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument query_language", value=query_language, expected_type=type_hints["query_language"])
            check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_group_names is not None:
            self._values["log_group_names"] = log_group_names
        if name is not None:
            self._values["name"] = name
        if query_language is not None:
            self._values["query_language"] = query_language
        if query_string is not None:
            self._values["query_string"] = query_string

    @builtins.property
    def log_group_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Use this parameter if you want the query to query only certain log groups.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-loggroupnames
        '''
        result = self._values.get("log_group_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the query definition.

        .. epigraph::

           You can use the name to create a folder structure for your queries. To create a folder, use a forward slash (/) to prefix your desired query name with your desired folder name. For example, ``*folder-name* / *query-name*`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_language(self) -> typing.Optional[builtins.str]:
        '''The query language used for this query.

        For more information about the query languages that CloudWatch Logs supports, see `Supported query languages <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_AnalyzeLogData_Languages.html>`_ .

        :default: - "CWLI"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-querylanguage
        '''
        result = self._values.get("query_language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_string(self) -> typing.Optional[builtins.str]:
        '''The query string to use for this query definition.

        For more information, see `CloudWatch Logs Insights Query Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html#cfn-logs-querydefinition-querystring
        '''
        result = self._values.get("query_string")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueryDefinitionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueryDefinitionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnQueryDefinitionPropsMixin",
):
    '''Creates a query definition for CloudWatch Logs Insights.

    For more information, see `Analyzing Log Data with CloudWatch Logs Insights <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-querydefinition.html
    :cloudformationResource: AWS::Logs::QueryDefinition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_query_definition_props_mixin = logs_mixins.CfnQueryDefinitionPropsMixin(logs_mixins.CfnQueryDefinitionMixinProps(
            log_group_names=["logGroupNames"],
            name="name",
            query_language="queryLanguage",
            query_string="queryString"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnQueryDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::QueryDefinition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4707fc858d287deb7a0b4607b67c32b77d8adf161b300d9d9322767a77a99e1f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e61033d80288d1b8ba7f540e142e50b0501e73a225d7693755f93075a2cf73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7281cdc9e2c6535840e6243accfbeb09f237bd0b54283e6b4ebe66d85f485899)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueryDefinitionMixinProps:
        return typing.cast(CfnQueryDefinitionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnResourcePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"policy_document": "policyDocument", "policy_name": "policyName"},
)
class CfnResourcePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Optional[builtins.str] = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnResourcePolicyPropsMixin.

        :param policy_document: The details of the policy. It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.
        :param policy_name: The name of the resource policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_resource_policy_mixin_props = logs_mixins.CfnResourcePolicyMixinProps(
                policy_document="policyDocument",
                policy_name="policyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8098d5b1556c49e4b798b680fce0da63d816f14cc1908909bbf87c774d79ad07)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def policy_document(self) -> typing.Optional[builtins.str]:
        '''The details of the policy.

        It must be formatted in JSON, and you must use backslashes to escape characters that need to be escaped in JSON strings, such as double quote marks.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the resource policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html#cfn-logs-resourcepolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnResourcePolicyPropsMixin",
):
    '''Creates or updates a resource policy that allows other AWS services to put log events to this account.

    An account can have up to 10 resource policies per AWS Region.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-resourcepolicy.html
    :cloudformationResource: AWS::Logs::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_resource_policy_props_mixin = logs_mixins.CfnResourcePolicyPropsMixin(logs_mixins.CfnResourcePolicyMixinProps(
            policy_document="policyDocument",
            policy_name="policyName"
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
        '''Create a mixin to apply properties to ``AWS::Logs::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73536152504d3636cde5f329bf2fa20e688751d271de326fe58475da0a796cbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcfdf7bdab4e5fb5cdaae391a63bd67ce9892f8ac8e403d235aa6b1029c27277)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68e922ef7dfe319721cca6b6d49941876d635334d3a90856c7a030a7b37cdee)
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
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnSubscriptionFilterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "apply_on_transformed_logs": "applyOnTransformedLogs",
        "destination_arn": "destinationArn",
        "distribution": "distribution",
        "emit_system_fields": "emitSystemFields",
        "field_selection_criteria": "fieldSelectionCriteria",
        "filter_name": "filterName",
        "filter_pattern": "filterPattern",
        "log_group_name": "logGroupName",
        "role_arn": "roleArn",
    },
)
class CfnSubscriptionFilterMixinProps:
    def __init__(
        self,
        *,
        apply_on_transformed_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        destination_arn: typing.Optional[builtins.str] = None,
        distribution: typing.Optional[builtins.str] = None,
        emit_system_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        field_selection_criteria: typing.Optional[builtins.str] = None,
        filter_name: typing.Optional[builtins.str] = None,
        filter_pattern: typing.Optional[builtins.str] = None,
        log_group_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSubscriptionFilterPropsMixin.

        :param apply_on_transformed_logs: This parameter is valid only for log groups that have an active log transformer. For more information about log transformers, see `PutTransformer <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html>`_ . If this value is ``true`` , the subscription filter is applied on the transformed version of the log events instead of the original ingested log events.
        :param destination_arn: The Amazon Resource Name (ARN) of the destination.
        :param distribution: The method used to distribute log data to the destination, which can be either random or grouped by log stream.
        :param emit_system_fields: The list of system fields that are included in the log events sent to the subscription destination. Returns the ``emitSystemFields`` value if it was specified when the subscription filter was created.
        :param field_selection_criteria: The filter expression that specifies which log events are processed by this subscription filter based on system fields. Returns the ``fieldSelectionCriteria`` value if it was specified when the subscription filter was created.
        :param filter_name: The name of the subscription filter.
        :param filter_pattern: The filtering expressions that restrict what gets delivered to the destination AWS resource. For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .
        :param log_group_name: The log group to associate with the subscription filter. All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.
        :param role_arn: The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream. You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_subscription_filter_mixin_props = logs_mixins.CfnSubscriptionFilterMixinProps(
                apply_on_transformed_logs=False,
                destination_arn="destinationArn",
                distribution="distribution",
                emit_system_fields=["emitSystemFields"],
                field_selection_criteria="fieldSelectionCriteria",
                filter_name="filterName",
                filter_pattern="filterPattern",
                log_group_name="logGroupName",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662da04ba6d51433c3529ff8ec3e212d90e65562c0eab0a07870ee9fc7fc9062)
            check_type(argname="argument apply_on_transformed_logs", value=apply_on_transformed_logs, expected_type=type_hints["apply_on_transformed_logs"])
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument distribution", value=distribution, expected_type=type_hints["distribution"])
            check_type(argname="argument emit_system_fields", value=emit_system_fields, expected_type=type_hints["emit_system_fields"])
            check_type(argname="argument field_selection_criteria", value=field_selection_criteria, expected_type=type_hints["field_selection_criteria"])
            check_type(argname="argument filter_name", value=filter_name, expected_type=type_hints["filter_name"])
            check_type(argname="argument filter_pattern", value=filter_pattern, expected_type=type_hints["filter_pattern"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if apply_on_transformed_logs is not None:
            self._values["apply_on_transformed_logs"] = apply_on_transformed_logs
        if destination_arn is not None:
            self._values["destination_arn"] = destination_arn
        if distribution is not None:
            self._values["distribution"] = distribution
        if emit_system_fields is not None:
            self._values["emit_system_fields"] = emit_system_fields
        if field_selection_criteria is not None:
            self._values["field_selection_criteria"] = field_selection_criteria
        if filter_name is not None:
            self._values["filter_name"] = filter_name
        if filter_pattern is not None:
            self._values["filter_pattern"] = filter_pattern
        if log_group_name is not None:
            self._values["log_group_name"] = log_group_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def apply_on_transformed_logs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''This parameter is valid only for log groups that have an active log transformer.

        For more information about log transformers, see `PutTransformer <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutTransformer.html>`_ .

        If this value is ``true`` , the subscription filter is applied on the transformed version of the log events instead of the original ingested log events.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-applyontransformedlogs
        '''
        result = self._values.get("apply_on_transformed_logs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def destination_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-destinationarn
        '''
        result = self._values.get("destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def distribution(self) -> typing.Optional[builtins.str]:
        '''The method used to distribute log data to the destination, which can be either random or grouped by log stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-distribution
        '''
        result = self._values.get("distribution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def emit_system_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of system fields that are included in the log events sent to the subscription destination.

        Returns the ``emitSystemFields`` value if it was specified when the subscription filter was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-emitsystemfields
        '''
        result = self._values.get("emit_system_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def field_selection_criteria(self) -> typing.Optional[builtins.str]:
        '''The filter expression that specifies which log events are processed by this subscription filter based on system fields.

        Returns the ``fieldSelectionCriteria`` value if it was specified when the subscription filter was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-fieldselectioncriteria
        '''
        result = self._values.get("field_selection_criteria")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the subscription filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filtername
        '''
        result = self._values.get("filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_pattern(self) -> typing.Optional[builtins.str]:
        '''The filtering expressions that restrict what gets delivered to the destination AWS resource.

        For more information about the filter pattern syntax, see `Filter and Pattern Syntax <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-filterpattern
        '''
        result = self._values.get("filter_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group_name(self) -> typing.Optional[builtins.str]:
        '''The log group to associate with the subscription filter.

        All log events that are uploaded to this log group are filtered and delivered to the specified AWS resource if the filter pattern matches the log events.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-loggroupname
        '''
        result = self._values.get("log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role that grants CloudWatch Logs permissions to deliver ingested log events to the destination stream.

        You don't need to provide the ARN when you are working with a logical destination for cross-account delivery.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html#cfn-logs-subscriptionfilter-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSubscriptionFilterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSubscriptionFilterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnSubscriptionFilterPropsMixin",
):
    '''The ``AWS::Logs::SubscriptionFilter`` resource specifies a subscription filter and associates it with the specified log group.

    Subscription filters allow you to subscribe to a real-time stream of log events and have them delivered to a specific destination. Currently, the supported destinations are:

    - An Amazon Kinesis data stream belonging to the same account as the subscription filter, for same-account delivery.
    - A logical destination that belongs to a different account, for cross-account delivery.
    - An Amazon Kinesis Firehose delivery stream that belongs to the same account as the subscription filter, for same-account delivery.
    - An AWS Lambda function that belongs to the same account as the subscription filter, for same-account delivery.

    There can be as many as two subscription filters associated with a log group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-subscriptionfilter.html
    :cloudformationResource: AWS::Logs::SubscriptionFilter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_subscription_filter_props_mixin = logs_mixins.CfnSubscriptionFilterPropsMixin(logs_mixins.CfnSubscriptionFilterMixinProps(
            apply_on_transformed_logs=False,
            destination_arn="destinationArn",
            distribution="distribution",
            emit_system_fields=["emitSystemFields"],
            field_selection_criteria="fieldSelectionCriteria",
            filter_name="filterName",
            filter_pattern="filterPattern",
            log_group_name="logGroupName",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSubscriptionFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::SubscriptionFilter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c08bd8f99c3ec897d7eab414504709326176223c115b0ed89420683ec331488)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a94adb0624e83dc095f72e15139df5c0392267b22ed528fbf316051d5474357d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b565d3dd7a767f9b5f10f8d976e9146082c357a0b77876c276045b091dca63)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSubscriptionFilterMixinProps:
        return typing.cast(CfnSubscriptionFilterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "log_group_identifier": "logGroupIdentifier",
        "transformer_config": "transformerConfig",
    },
)
class CfnTransformerMixinProps:
    def __init__(
        self,
        *,
        log_group_identifier: typing.Optional[builtins.str] = None,
        transformer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ProcessorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnTransformerPropsMixin.

        :param log_group_identifier: Specify either the name or ARN of the log group to create the transformer for.
        :param transformer_config: This structure is an array that contains the configuration of this log transformer. A log transformer is an array of processors, where each processor applies one type of transformation to the log events that are ingested.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-transformer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
            
            cfn_transformer_mixin_props = logs_mixins.CfnTransformerMixinProps(
                log_group_identifier="logGroupIdentifier",
                transformer_config=[logs_mixins.CfnTransformerPropsMixin.ProcessorProperty(
                    add_keys=logs_mixins.CfnTransformerPropsMixin.AddKeysProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.AddKeyEntryProperty(
                            key="key",
                            overwrite_if_exists=False,
                            value="value"
                        )]
                    ),
                    copy_value=logs_mixins.CfnTransformerPropsMixin.CopyValueProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.CopyValueEntryProperty(
                            overwrite_if_exists=False,
                            source="source",
                            target="target"
                        )]
                    ),
                    csv=logs_mixins.CfnTransformerPropsMixin.CsvProperty(
                        columns=["columns"],
                        delimiter="delimiter",
                        quote_character="quoteCharacter",
                        source="source"
                    ),
                    date_time_converter=logs_mixins.CfnTransformerPropsMixin.DateTimeConverterProperty(
                        locale="locale",
                        match_patterns=["matchPatterns"],
                        source="source",
                        source_timezone="sourceTimezone",
                        target="target",
                        target_format="targetFormat",
                        target_timezone="targetTimezone"
                    ),
                    delete_keys=logs_mixins.CfnTransformerPropsMixin.DeleteKeysProperty(
                        with_keys=["withKeys"]
                    ),
                    grok=logs_mixins.CfnTransformerPropsMixin.GrokProperty(
                        match="match",
                        source="source"
                    ),
                    list_to_map=logs_mixins.CfnTransformerPropsMixin.ListToMapProperty(
                        flatten=False,
                        flattened_element="flattenedElement",
                        key="key",
                        source="source",
                        target="target",
                        value_key="valueKey"
                    ),
                    lower_case_string=logs_mixins.CfnTransformerPropsMixin.LowerCaseStringProperty(
                        with_keys=["withKeys"]
                    ),
                    move_keys=logs_mixins.CfnTransformerPropsMixin.MoveKeysProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.MoveKeyEntryProperty(
                            overwrite_if_exists=False,
                            source="source",
                            target="target"
                        )]
                    ),
                    parse_cloudfront=logs_mixins.CfnTransformerPropsMixin.ParseCloudfrontProperty(
                        source="source"
                    ),
                    parse_json=logs_mixins.CfnTransformerPropsMixin.ParseJSONProperty(
                        destination="destination",
                        source="source"
                    ),
                    parse_key_value=logs_mixins.CfnTransformerPropsMixin.ParseKeyValueProperty(
                        destination="destination",
                        field_delimiter="fieldDelimiter",
                        key_prefix="keyPrefix",
                        key_value_delimiter="keyValueDelimiter",
                        non_match_value="nonMatchValue",
                        overwrite_if_exists=False,
                        source="source"
                    ),
                    parse_postgres=logs_mixins.CfnTransformerPropsMixin.ParsePostgresProperty(
                        source="source"
                    ),
                    parse_route53=logs_mixins.CfnTransformerPropsMixin.ParseRoute53Property(
                        source="source"
                    ),
                    parse_to_ocsf=logs_mixins.CfnTransformerPropsMixin.ParseToOCSFProperty(
                        event_source="eventSource",
                        ocsf_version="ocsfVersion",
                        source="source"
                    ),
                    parse_vpc=logs_mixins.CfnTransformerPropsMixin.ParseVPCProperty(
                        source="source"
                    ),
                    parse_waf=logs_mixins.CfnTransformerPropsMixin.ParseWAFProperty(
                        source="source"
                    ),
                    rename_keys=logs_mixins.CfnTransformerPropsMixin.RenameKeysProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.RenameKeyEntryProperty(
                            key="key",
                            overwrite_if_exists=False,
                            rename_to="renameTo"
                        )]
                    ),
                    split_string=logs_mixins.CfnTransformerPropsMixin.SplitStringProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.SplitStringEntryProperty(
                            delimiter="delimiter",
                            source="source"
                        )]
                    ),
                    substitute_string=logs_mixins.CfnTransformerPropsMixin.SubstituteStringProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.SubstituteStringEntryProperty(
                            from="from",
                            source="source",
                            to="to"
                        )]
                    ),
                    trim_string=logs_mixins.CfnTransformerPropsMixin.TrimStringProperty(
                        with_keys=["withKeys"]
                    ),
                    type_converter=logs_mixins.CfnTransformerPropsMixin.TypeConverterProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.TypeConverterEntryProperty(
                            key="key",
                            type="type"
                        )]
                    ),
                    upper_case_string=logs_mixins.CfnTransformerPropsMixin.UpperCaseStringProperty(
                        with_keys=["withKeys"]
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f26e528cf71b5cb429c4d0a3316e752366ee84bf582296e385038b6ca019f2)
            check_type(argname="argument log_group_identifier", value=log_group_identifier, expected_type=type_hints["log_group_identifier"])
            check_type(argname="argument transformer_config", value=transformer_config, expected_type=type_hints["transformer_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_group_identifier is not None:
            self._values["log_group_identifier"] = log_group_identifier
        if transformer_config is not None:
            self._values["transformer_config"] = transformer_config

    @builtins.property
    def log_group_identifier(self) -> typing.Optional[builtins.str]:
        '''Specify either the name or ARN of the log group to create the transformer for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-transformer.html#cfn-logs-transformer-loggroupidentifier
        '''
        result = self._values.get("log_group_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transformer_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ProcessorProperty"]]]]:
        '''This structure is an array that contains the configuration of this log transformer.

        A log transformer is an array of processors, where each processor applies one type of transformation to the log events that are ingested.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-transformer.html#cfn-logs-transformer-transformerconfig
        '''
        result = self._values.get("transformer_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ProcessorProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransformerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTransformerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin",
):
    '''Creates or updates a *log transformer* for a single log group.

    You use log transformers to transform log events into a different format, making them easier for you to process and analyze. You can also transform logs from different sources into standardized formats that contains relevant, source-specific information.

    After you have created a transformer, CloudWatch Logs performs the transformations at the time of log ingestion. You can then refer to the transformed versions of the logs during operations such as querying with CloudWatch Logs Insights or creating metric filters or subscription filers.

    You can also use a transformer to copy metadata from metadata keys into the log events themselves. This metadata can include log group name, log stream name, account ID and Region.

    A transformer for a log group is a series of processors, where each processor applies one type of transformation to the log events ingested into this log group. The processors work one after another, in the order that you list them, like a pipeline. For more information about the available processors to use in a transformer, see `Processors that you can use <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-Processors>`_ .

    Having log events in standardized format enables visibility across your applications for your log analysis, reporting, and alarming needs. CloudWatch Logs provides transformation for common log types with out-of-the-box transformation templates for major AWS log sources such as VPC flow logs, Lambda, and Amazon RDS. You can use pre-built transformation templates or create custom transformation policies.

    You can create transformers only for the log groups in the Standard log class.

    You can also set up a transformer at the account level. For more information, see `PutAccountPolicy <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutAccountPolicy.html>`_ . If there is both a log-group level transformer created with ``PutTransformer`` and an account-level transformer that could apply to the same log group, the log group uses only the log-group level transformer. It ignores the account-level transformer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-logs-transformer.html
    :cloudformationResource: AWS::Logs::Transformer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
        
        cfn_transformer_props_mixin = logs_mixins.CfnTransformerPropsMixin(logs_mixins.CfnTransformerMixinProps(
            log_group_identifier="logGroupIdentifier",
            transformer_config=[logs_mixins.CfnTransformerPropsMixin.ProcessorProperty(
                add_keys=logs_mixins.CfnTransformerPropsMixin.AddKeysProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.AddKeyEntryProperty(
                        key="key",
                        overwrite_if_exists=False,
                        value="value"
                    )]
                ),
                copy_value=logs_mixins.CfnTransformerPropsMixin.CopyValueProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.CopyValueEntryProperty(
                        overwrite_if_exists=False,
                        source="source",
                        target="target"
                    )]
                ),
                csv=logs_mixins.CfnTransformerPropsMixin.CsvProperty(
                    columns=["columns"],
                    delimiter="delimiter",
                    quote_character="quoteCharacter",
                    source="source"
                ),
                date_time_converter=logs_mixins.CfnTransformerPropsMixin.DateTimeConverterProperty(
                    locale="locale",
                    match_patterns=["matchPatterns"],
                    source="source",
                    source_timezone="sourceTimezone",
                    target="target",
                    target_format="targetFormat",
                    target_timezone="targetTimezone"
                ),
                delete_keys=logs_mixins.CfnTransformerPropsMixin.DeleteKeysProperty(
                    with_keys=["withKeys"]
                ),
                grok=logs_mixins.CfnTransformerPropsMixin.GrokProperty(
                    match="match",
                    source="source"
                ),
                list_to_map=logs_mixins.CfnTransformerPropsMixin.ListToMapProperty(
                    flatten=False,
                    flattened_element="flattenedElement",
                    key="key",
                    source="source",
                    target="target",
                    value_key="valueKey"
                ),
                lower_case_string=logs_mixins.CfnTransformerPropsMixin.LowerCaseStringProperty(
                    with_keys=["withKeys"]
                ),
                move_keys=logs_mixins.CfnTransformerPropsMixin.MoveKeysProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.MoveKeyEntryProperty(
                        overwrite_if_exists=False,
                        source="source",
                        target="target"
                    )]
                ),
                parse_cloudfront=logs_mixins.CfnTransformerPropsMixin.ParseCloudfrontProperty(
                    source="source"
                ),
                parse_json=logs_mixins.CfnTransformerPropsMixin.ParseJSONProperty(
                    destination="destination",
                    source="source"
                ),
                parse_key_value=logs_mixins.CfnTransformerPropsMixin.ParseKeyValueProperty(
                    destination="destination",
                    field_delimiter="fieldDelimiter",
                    key_prefix="keyPrefix",
                    key_value_delimiter="keyValueDelimiter",
                    non_match_value="nonMatchValue",
                    overwrite_if_exists=False,
                    source="source"
                ),
                parse_postgres=logs_mixins.CfnTransformerPropsMixin.ParsePostgresProperty(
                    source="source"
                ),
                parse_route53=logs_mixins.CfnTransformerPropsMixin.ParseRoute53Property(
                    source="source"
                ),
                parse_to_ocsf=logs_mixins.CfnTransformerPropsMixin.ParseToOCSFProperty(
                    event_source="eventSource",
                    ocsf_version="ocsfVersion",
                    source="source"
                ),
                parse_vpc=logs_mixins.CfnTransformerPropsMixin.ParseVPCProperty(
                    source="source"
                ),
                parse_waf=logs_mixins.CfnTransformerPropsMixin.ParseWAFProperty(
                    source="source"
                ),
                rename_keys=logs_mixins.CfnTransformerPropsMixin.RenameKeysProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.RenameKeyEntryProperty(
                        key="key",
                        overwrite_if_exists=False,
                        rename_to="renameTo"
                    )]
                ),
                split_string=logs_mixins.CfnTransformerPropsMixin.SplitStringProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.SplitStringEntryProperty(
                        delimiter="delimiter",
                        source="source"
                    )]
                ),
                substitute_string=logs_mixins.CfnTransformerPropsMixin.SubstituteStringProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.SubstituteStringEntryProperty(
                        from="from",
                        source="source",
                        to="to"
                    )]
                ),
                trim_string=logs_mixins.CfnTransformerPropsMixin.TrimStringProperty(
                    with_keys=["withKeys"]
                ),
                type_converter=logs_mixins.CfnTransformerPropsMixin.TypeConverterProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.TypeConverterEntryProperty(
                        key="key",
                        type="type"
                    )]
                ),
                upper_case_string=logs_mixins.CfnTransformerPropsMixin.UpperCaseStringProperty(
                    with_keys=["withKeys"]
                )
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTransformerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Logs::Transformer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea10f667828fffb65fbb6710fca7d2b13742745b7af831a23dd705abf3f1f253)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d15148b0d55b83011953e1cda962cc1cb2c57e744974fbd9ab7b438fc922936)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__882ff36a1be15cdce7b703f4b52b9beb5de6d315313134bd74a8366849c50af6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTransformerMixinProps:
        return typing.cast(CfnTransformerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.AddKeyEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "overwrite_if_exists": "overwriteIfExists",
            "value": "value",
        },
    )
    class AddKeyEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one key that will be added with the `addKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-addKey>`_ processor.

            :param key: The key of the new entry to be added to the log event.
            :param overwrite_if_exists: Specifies whether to overwrite the value if the key already exists in the log event. If you omit this, the default is ``false`` .
            :param value: The value of the new entry to be added to the log event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-addkeyentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                add_key_entry_property = logs_mixins.CfnTransformerPropsMixin.AddKeyEntryProperty(
                    key="key",
                    overwrite_if_exists=False,
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5f45d7aa3eca126a2d3f429b6323c30c747099c3608b3ba29efbad426ed0d65)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if overwrite_if_exists is not None:
                self._values["overwrite_if_exists"] = overwrite_if_exists
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the new entry to be added to the log event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-addkeyentry.html#cfn-logs-transformer-addkeyentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_if_exists(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to overwrite the value if the key already exists in the log event.

            If you omit this, the default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-addkeyentry.html#cfn-logs-transformer-addkeyentry-overwriteifexists
            '''
            result = self._values.get("overwrite_if_exists")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the new entry to be added to the log event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-addkeyentry.html#cfn-logs-transformer-addkeyentry-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddKeyEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.AddKeysProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class AddKeysProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.AddKeyEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This processor adds new key-value pairs to the log event.

            For more information about this processor including examples, see `addKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-addKeys>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of objects, where each object contains the information about one key to add to the log event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-addkeys.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                add_keys_property = logs_mixins.CfnTransformerPropsMixin.AddKeysProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.AddKeyEntryProperty(
                        key="key",
                        overwrite_if_exists=False,
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__703a0aecb9526ba4cdb6da9e9055d7e7f25fbe51c319a64488ce4d3293effb1b)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AddKeyEntryProperty"]]]]:
            '''An array of objects, where each object contains the information about one key to add to the log event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-addkeys.html#cfn-logs-transformer-addkeys-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AddKeyEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddKeysProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.CopyValueEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "overwrite_if_exists": "overwriteIfExists",
            "source": "source",
            "target": "target",
        },
    )
    class CopyValueEntryProperty:
        def __init__(
            self,
            *,
            overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one value to be copied with the `copyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-copyValue>`_ processor.

            :param overwrite_if_exists: Specifies whether to overwrite the value if the destination key already exists. If you omit this, the default is ``false`` .
            :param source: The key to copy.
            :param target: The key of the field to copy the value to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-copyvalueentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                copy_value_entry_property = logs_mixins.CfnTransformerPropsMixin.CopyValueEntryProperty(
                    overwrite_if_exists=False,
                    source="source",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67d49a1bc306e4ca525b566f40955e956daed3c06c2ed3cf36ce960903ddac8c)
                check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if overwrite_if_exists is not None:
                self._values["overwrite_if_exists"] = overwrite_if_exists
            if source is not None:
                self._values["source"] = source
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def overwrite_if_exists(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to overwrite the value if the destination key already exists.

            If you omit this, the default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-copyvalueentry.html#cfn-logs-transformer-copyvalueentry-overwriteifexists
            '''
            result = self._values.get("overwrite_if_exists")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The key to copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-copyvalueentry.html#cfn-logs-transformer-copyvalueentry-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The key of the field to copy the value to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-copyvalueentry.html#cfn-logs-transformer-copyvalueentry-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyValueEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.CopyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class CopyValueProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.CopyValueEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This processor copies values within a log event.

            You can also use this processor to add metadata to log events by copying the values of the following metadata keys into the log events: ``@logGroupName`` , ``@logGroupStream`` , ``@accountId`` , ``@regionName`` .

            For more information about this processor including examples, see `copyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-copyValue>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of ``CopyValueEntry`` objects, where each object contains the information about one field value to copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-copyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                copy_value_property = logs_mixins.CfnTransformerPropsMixin.CopyValueProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.CopyValueEntryProperty(
                        overwrite_if_exists=False,
                        source="source",
                        target="target"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__abfa5782899e07f00e40154465dc891eb4f44adaa1420c14d9d23fc9d8939aab)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.CopyValueEntryProperty"]]]]:
            '''An array of ``CopyValueEntry`` objects, where each object contains the information about one field value to copy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-copyvalue.html#cfn-logs-transformer-copyvalue-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.CopyValueEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CopyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.CsvProperty",
        jsii_struct_bases=[],
        name_mapping={
            "columns": "columns",
            "delimiter": "delimiter",
            "quote_character": "quoteCharacter",
            "source": "source",
        },
    )
    class CsvProperty:
        def __init__(
            self,
            *,
            columns: typing.Optional[typing.Sequence[builtins.str]] = None,
            delimiter: typing.Optional[builtins.str] = None,
            quote_character: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``CSV`` processor parses comma-separated values (CSV) from the log events into columns.

            For more information about this processor including examples, see `csv <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-csv>`_ in the *CloudWatch Logs User Guide* .

            :param columns: An array of names to use for the columns in the transformed log event. If you omit this, default column names ( ``[column_1, column_2 ...]`` ) are used.
            :param delimiter: The character used to separate each column in the original comma-separated value log event. If you omit this, the processor looks for the comma ``,`` character as the delimiter.
            :param quote_character: The character used used as a text qualifier for a single column of data. If you omit this, the double quotation mark ``"`` character is used.
            :param source: The path to the field in the log event that has the comma separated values to be parsed. If you omit this value, the whole log message is processed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-csv.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                csv_property = logs_mixins.CfnTransformerPropsMixin.CsvProperty(
                    columns=["columns"],
                    delimiter="delimiter",
                    quote_character="quoteCharacter",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__460d7382089bbf89bf43cb1dd88f28fb69f218ee1256484790fb651a599adc76)
                check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument quote_character", value=quote_character, expected_type=type_hints["quote_character"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if columns is not None:
                self._values["columns"] = columns
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if quote_character is not None:
                self._values["quote_character"] = quote_character
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of names to use for the columns in the transformed log event.

            If you omit this, default column names ( ``[column_1, column_2 ...]`` ) are used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-csv.html#cfn-logs-transformer-csv-columns
            '''
            result = self._values.get("columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''The character used to separate each column in the original comma-separated value log event.

            If you omit this, the processor looks for the comma ``,`` character as the delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-csv.html#cfn-logs-transformer-csv-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def quote_character(self) -> typing.Optional[builtins.str]:
            '''The character used used as a text qualifier for a single column of data.

            If you omit this, the double quotation mark ``"`` character is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-csv.html#cfn-logs-transformer-csv-quotecharacter
            '''
            result = self._values.get("quote_character")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The path to the field in the log event that has the comma separated values to be parsed.

            If you omit this value, the whole log message is processed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-csv.html#cfn-logs-transformer-csv-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.DateTimeConverterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "locale": "locale",
            "match_patterns": "matchPatterns",
            "source": "source",
            "source_timezone": "sourceTimezone",
            "target": "target",
            "target_format": "targetFormat",
            "target_timezone": "targetTimezone",
        },
    )
    class DateTimeConverterProperty:
        def __init__(
            self,
            *,
            locale: typing.Optional[builtins.str] = None,
            match_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            source: typing.Optional[builtins.str] = None,
            source_timezone: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
            target_format: typing.Optional[builtins.str] = None,
            target_timezone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This processor converts a datetime string into a format that you specify.

            For more information about this processor including examples, see `datetimeConverter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-datetimeConverter>`_ in the *CloudWatch Logs User Guide* .

            :param locale: The locale of the source field. If you omit this, the default of ``locale.ROOT`` is used.
            :param match_patterns: A list of patterns to match against the ``source`` field.
            :param source: The key to apply the date conversion to.
            :param source_timezone: The time zone of the source field. If you omit this, the default used is the UTC zone.
            :param target: The JSON field to store the result in.
            :param target_format: The datetime format to use for the converted data in the target field. If you omit this, the default of ``yyyy-MM-dd'T'HH:mm:ss.SSS'Z`` is used.
            :param target_timezone: The time zone of the target field. If you omit this, the default used is the UTC zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                date_time_converter_property = logs_mixins.CfnTransformerPropsMixin.DateTimeConverterProperty(
                    locale="locale",
                    match_patterns=["matchPatterns"],
                    source="source",
                    source_timezone="sourceTimezone",
                    target="target",
                    target_format="targetFormat",
                    target_timezone="targetTimezone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0747024fa607c26ba2bee148ae3cfe7eba779035901211feaee117feadb6a907)
                check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
                check_type(argname="argument match_patterns", value=match_patterns, expected_type=type_hints["match_patterns"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument source_timezone", value=source_timezone, expected_type=type_hints["source_timezone"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument target_format", value=target_format, expected_type=type_hints["target_format"])
                check_type(argname="argument target_timezone", value=target_timezone, expected_type=type_hints["target_timezone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if locale is not None:
                self._values["locale"] = locale
            if match_patterns is not None:
                self._values["match_patterns"] = match_patterns
            if source is not None:
                self._values["source"] = source
            if source_timezone is not None:
                self._values["source_timezone"] = source_timezone
            if target is not None:
                self._values["target"] = target
            if target_format is not None:
                self._values["target_format"] = target_format
            if target_timezone is not None:
                self._values["target_timezone"] = target_timezone

        @builtins.property
        def locale(self) -> typing.Optional[builtins.str]:
            '''The locale of the source field.

            If you omit this, the default of ``locale.ROOT`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-locale
            '''
            result = self._values.get("locale")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def match_patterns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of patterns to match against the ``source`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-matchpatterns
            '''
            result = self._values.get("match_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The key to apply the date conversion to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_timezone(self) -> typing.Optional[builtins.str]:
            '''The time zone of the source field.

            If you omit this, the default used is the UTC zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-sourcetimezone
            '''
            result = self._values.get("source_timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The JSON field to store the result in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_format(self) -> typing.Optional[builtins.str]:
            '''The datetime format to use for the converted data in the target field.

            If you omit this, the default of ``yyyy-MM-dd'T'HH:mm:ss.SSS'Z`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-targetformat
            '''
            result = self._values.get("target_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_timezone(self) -> typing.Optional[builtins.str]:
            '''The time zone of the target field.

            If you omit this, the default used is the UTC zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-datetimeconverter.html#cfn-logs-transformer-datetimeconverter-targettimezone
            '''
            result = self._values.get("target_timezone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateTimeConverterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.DeleteKeysProperty",
        jsii_struct_bases=[],
        name_mapping={"with_keys": "withKeys"},
    )
    class DeleteKeysProperty:
        def __init__(
            self,
            *,
            with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This processor deletes entries from a log event. These entries are key-value pairs.

            For more information about this processor including examples, see `deleteKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-deleteKeys>`_ in the *CloudWatch Logs User Guide* .

            :param with_keys: The list of keys to delete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-deletekeys.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                delete_keys_property = logs_mixins.CfnTransformerPropsMixin.DeleteKeysProperty(
                    with_keys=["withKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ddbc74b302a9896bec24e3cfd1ad824ad641e5d624802c0fc09c9f772abb8c3)
                check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if with_keys is not None:
                self._values["with_keys"] = with_keys

        @builtins.property
        def with_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of keys to delete.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-deletekeys.html#cfn-logs-transformer-deletekeys-withkeys
            '''
            result = self._values.get("with_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeleteKeysProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.GrokProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match", "source": "source"},
    )
    class GrokProperty:
        def __init__(
            self,
            *,
            match: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This processor uses pattern matching to parse and structure unstructured data.

            This processor can also extract fields from log messages.

            For more information about this processor including examples, see `grok <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-Grok>`_ in the *CloudWatch Logs User Guide* .

            :param match: The grok pattern to match against the log event. For a list of supported grok patterns, see `Supported grok patterns <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#Grok-Patterns>`_ .
            :param source: The path to the field in the log event that you want to parse. If you omit this value, the whole log message is parsed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-grok.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                grok_property = logs_mixins.CfnTransformerPropsMixin.GrokProperty(
                    match="match",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d84752e0a340d8b821fbc87d2717384a271b9c9eae4f0ff3cc961c85b562256d)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if match is not None:
                self._values["match"] = match
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def match(self) -> typing.Optional[builtins.str]:
            '''The grok pattern to match against the log event.

            For a list of supported grok patterns, see `Supported grok patterns <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#Grok-Patterns>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-grok.html#cfn-logs-transformer-grok-match
            '''
            result = self._values.get("match")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The path to the field in the log event that you want to parse.

            If you omit this value, the whole log message is parsed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-grok.html#cfn-logs-transformer-grok-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GrokProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ListToMapProperty",
        jsii_struct_bases=[],
        name_mapping={
            "flatten": "flatten",
            "flattened_element": "flattenedElement",
            "key": "key",
            "source": "source",
            "target": "target",
            "value_key": "valueKey",
        },
    )
    class ListToMapProperty:
        def __init__(
            self,
            *,
            flatten: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            flattened_element: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
            value_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This processor takes a list of objects that contain key fields, and converts them into a map of target keys.

            For more information about this processor including examples, see `listToMap <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-listToMap>`_ in the *CloudWatch Logs User Guide* .

            :param flatten: A Boolean value to indicate whether the list will be flattened into single items. Specify ``true`` to flatten the list. The default is ``false``
            :param flattened_element: If you set ``flatten`` to ``true`` , use ``flattenedElement`` to specify which element, ``first`` or ``last`` , to keep. You must specify this parameter if ``flatten`` is ``true``
            :param key: The key of the field to be extracted as keys in the generated map.
            :param source: The key in the log event that has a list of objects that will be converted to a map.
            :param target: The key of the field that will hold the generated map.
            :param value_key: If this is specified, the values that you specify in this parameter will be extracted from the ``source`` objects and put into the values of the generated map. Otherwise, original objects in the source list will be put into the values of the generated map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                list_to_map_property = logs_mixins.CfnTransformerPropsMixin.ListToMapProperty(
                    flatten=False,
                    flattened_element="flattenedElement",
                    key="key",
                    source="source",
                    target="target",
                    value_key="valueKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__120c4ae0a72d13a64b472141df1fdcca20739df6d3b5c789ca8eebeb664afad2)
                check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
                check_type(argname="argument flattened_element", value=flattened_element, expected_type=type_hints["flattened_element"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument value_key", value=value_key, expected_type=type_hints["value_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if flatten is not None:
                self._values["flatten"] = flatten
            if flattened_element is not None:
                self._values["flattened_element"] = flattened_element
            if key is not None:
                self._values["key"] = key
            if source is not None:
                self._values["source"] = source
            if target is not None:
                self._values["target"] = target
            if value_key is not None:
                self._values["value_key"] = value_key

        @builtins.property
        def flatten(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value to indicate whether the list will be flattened into single items.

            Specify ``true`` to flatten the list. The default is ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html#cfn-logs-transformer-listtomap-flatten
            '''
            result = self._values.get("flatten")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def flattened_element(self) -> typing.Optional[builtins.str]:
            '''If you set ``flatten`` to ``true`` , use ``flattenedElement`` to specify which element, ``first`` or ``last`` , to keep.

            You must specify this parameter if ``flatten`` is ``true``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html#cfn-logs-transformer-listtomap-flattenedelement
            '''
            result = self._values.get("flattened_element")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the field to be extracted as keys in the generated map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html#cfn-logs-transformer-listtomap-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The key in the log event that has a list of objects that will be converted to a map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html#cfn-logs-transformer-listtomap-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The key of the field that will hold the generated map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html#cfn-logs-transformer-listtomap-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_key(self) -> typing.Optional[builtins.str]:
            '''If this is specified, the values that you specify in this parameter will be extracted from the ``source`` objects and put into the values of the generated map.

            Otherwise, original objects in the source list will be put into the values of the generated map.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-listtomap.html#cfn-logs-transformer-listtomap-valuekey
            '''
            result = self._values.get("value_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ListToMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.LowerCaseStringProperty",
        jsii_struct_bases=[],
        name_mapping={"with_keys": "withKeys"},
    )
    class LowerCaseStringProperty:
        def __init__(
            self,
            *,
            with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This processor converts a string to lowercase.

            For more information about this processor including examples, see `lowerCaseString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-lowerCaseString>`_ in the *CloudWatch Logs User Guide* .

            :param with_keys: The array caontaining the keys of the fields to convert to lowercase.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-lowercasestring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                lower_case_string_property = logs_mixins.CfnTransformerPropsMixin.LowerCaseStringProperty(
                    with_keys=["withKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac9227498a241896bf211756e2424d3c286de2c2d45a50fdc5909433620a6cda)
                check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if with_keys is not None:
                self._values["with_keys"] = with_keys

        @builtins.property
        def with_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array caontaining the keys of the fields to convert to lowercase.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-lowercasestring.html#cfn-logs-transformer-lowercasestring-withkeys
            '''
            result = self._values.get("with_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LowerCaseStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.MoveKeyEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "overwrite_if_exists": "overwriteIfExists",
            "source": "source",
            "target": "target",
        },
    )
    class MoveKeyEntryProperty:
        def __init__(
            self,
            *,
            overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one key that will be moved with the `moveKey <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-moveKey>`_ processor.

            :param overwrite_if_exists: Specifies whether to overwrite the value if the destination key already exists. If you omit this, the default is ``false`` .
            :param source: The key to move.
            :param target: The key to move to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-movekeyentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                move_key_entry_property = logs_mixins.CfnTransformerPropsMixin.MoveKeyEntryProperty(
                    overwrite_if_exists=False,
                    source="source",
                    target="target"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d4f68f435a379518350c7c1ac69b7a739d0f93e1613080a4b07213e8e5b5a27)
                check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if overwrite_if_exists is not None:
                self._values["overwrite_if_exists"] = overwrite_if_exists
            if source is not None:
                self._values["source"] = source
            if target is not None:
                self._values["target"] = target

        @builtins.property
        def overwrite_if_exists(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to overwrite the value if the destination key already exists.

            If you omit this, the default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-movekeyentry.html#cfn-logs-transformer-movekeyentry-overwriteifexists
            '''
            result = self._values.get("overwrite_if_exists")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The key to move.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-movekeyentry.html#cfn-logs-transformer-movekeyentry-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The key to move to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-movekeyentry.html#cfn-logs-transformer-movekeyentry-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MoveKeyEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.MoveKeysProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class MoveKeysProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.MoveKeyEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This processor moves a key from one field to another. The original key is deleted.

            For more information about this processor including examples, see `moveKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-moveKeys>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of objects, where each object contains the information about one key to move.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-movekeys.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                move_keys_property = logs_mixins.CfnTransformerPropsMixin.MoveKeysProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.MoveKeyEntryProperty(
                        overwrite_if_exists=False,
                        source="source",
                        target="target"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3eb685b55e665b546e13653599231f1fcf5f27c2f9784e302e972b9e70e7f54)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.MoveKeyEntryProperty"]]]]:
            '''An array of objects, where each object contains the information about one key to move.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-movekeys.html#cfn-logs-transformer-movekeys-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.MoveKeyEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MoveKeysProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseCloudfrontProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class ParseCloudfrontProperty:
        def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
            '''This processor parses CloudFront vended logs, extract fields, and convert them into JSON format.

            Encoded field values are decoded. Values that are integers and doubles are treated as such. For more information about this processor including examples, see `parseCloudfront <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseCloudfront>`_

            For more information about CloudFront log format, see `Configure and use standard logs (access logs) <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/AccessLogs.html>`_ .

            If you use this processor, it must be the first processor in your transformer.

            :param source: Omit this parameter and the whole log message will be processed by this processor. No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsecloudfront.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_cloudfront_property = logs_mixins.CfnTransformerPropsMixin.ParseCloudfrontProperty(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9b47409c3ccaa43ec9960596be0ca68018e4897df29bfc098b7b1a724310a79)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Omit this parameter and the whole log message will be processed by this processor.

            No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsecloudfront.html#cfn-logs-transformer-parsecloudfront-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseCloudfrontProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseJSONProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "source": "source"},
    )
    class ParseJSONProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This processor parses log events that are in JSON format.

            It can extract JSON key-value pairs and place them under a destination that you specify.

            Additionally, because you must have at least one parse-type processor in a transformer, you can use ``ParseJSON`` as that processor for JSON-format logs, so that you can also apply other processors, such as mutate processors, to these logs.

            For more information about this processor including examples, see `parseJSON <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseJSON>`_ in the *CloudWatch Logs User Guide* .

            :param destination: The location to put the parsed key value pair into. If you omit this parameter, it is placed under the root node.
            :param source: Path to the field in the log event that will be parsed. Use dot notation to access child fields. For example, ``store.book``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsejson.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_jSONProperty = logs_mixins.CfnTransformerPropsMixin.ParseJSONProperty(
                    destination="destination",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c37538c6a6f7db2044e9862c3980c8a6295cdb8db40544fda8791e4bc61ca325)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The location to put the parsed key value pair into.

            If you omit this parameter, it is placed under the root node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsejson.html#cfn-logs-transformer-parsejson-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Path to the field in the log event that will be parsed.

            Use dot notation to access child fields. For example, ``store.book``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsejson.html#cfn-logs-transformer-parsejson-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseJSONProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseKeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "field_delimiter": "fieldDelimiter",
            "key_prefix": "keyPrefix",
            "key_value_delimiter": "keyValueDelimiter",
            "non_match_value": "nonMatchValue",
            "overwrite_if_exists": "overwriteIfExists",
            "source": "source",
        },
    )
    class ParseKeyValueProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            field_delimiter: typing.Optional[builtins.str] = None,
            key_prefix: typing.Optional[builtins.str] = None,
            key_value_delimiter: typing.Optional[builtins.str] = None,
            non_match_value: typing.Optional[builtins.str] = None,
            overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This processor parses a specified field in the original log event into key-value pairs.

            For more information about this processor including examples, see `parseKeyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parseKeyValue>`_ in the *CloudWatch Logs User Guide* .

            :param destination: The destination field to put the extracted key-value pairs into.
            :param field_delimiter: The field delimiter string that is used between key-value pairs in the original log events. If you omit this, the ampersand ``&`` character is used.
            :param key_prefix: If you want to add a prefix to all transformed keys, specify it here.
            :param key_value_delimiter: The delimiter string to use between the key and value in each pair in the transformed log event. If you omit this, the equal ``=`` character is used.
            :param non_match_value: A value to insert into the value field in the result, when a key-value pair is not successfully split.
            :param overwrite_if_exists: Specifies whether to overwrite the value if the destination key already exists. If you omit this, the default is ``false`` .
            :param source: Path to the field in the log event that will be parsed. Use dot notation to access child fields. For example, ``store.book``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_key_value_property = logs_mixins.CfnTransformerPropsMixin.ParseKeyValueProperty(
                    destination="destination",
                    field_delimiter="fieldDelimiter",
                    key_prefix="keyPrefix",
                    key_value_delimiter="keyValueDelimiter",
                    non_match_value="nonMatchValue",
                    overwrite_if_exists=False,
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b28faa21f8d101e6d647b62e5add73b27e4613f69641ed2441a1b821aebbfe6)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
                check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
                check_type(argname="argument key_value_delimiter", value=key_value_delimiter, expected_type=type_hints["key_value_delimiter"])
                check_type(argname="argument non_match_value", value=non_match_value, expected_type=type_hints["non_match_value"])
                check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if field_delimiter is not None:
                self._values["field_delimiter"] = field_delimiter
            if key_prefix is not None:
                self._values["key_prefix"] = key_prefix
            if key_value_delimiter is not None:
                self._values["key_value_delimiter"] = key_value_delimiter
            if non_match_value is not None:
                self._values["non_match_value"] = non_match_value
            if overwrite_if_exists is not None:
                self._values["overwrite_if_exists"] = overwrite_if_exists
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The destination field to put the extracted key-value pairs into.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def field_delimiter(self) -> typing.Optional[builtins.str]:
            '''The field delimiter string that is used between key-value pairs in the original log events.

            If you omit this, the ampersand ``&`` character is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-fielddelimiter
            '''
            result = self._values.get("field_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_prefix(self) -> typing.Optional[builtins.str]:
            '''If you want to add a prefix to all transformed keys, specify it here.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-keyprefix
            '''
            result = self._values.get("key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_value_delimiter(self) -> typing.Optional[builtins.str]:
            '''The delimiter string to use between the key and value in each pair in the transformed log event.

            If you omit this, the equal ``=`` character is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-keyvaluedelimiter
            '''
            result = self._values.get("key_value_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def non_match_value(self) -> typing.Optional[builtins.str]:
            '''A value to insert into the value field in the result, when a key-value pair is not successfully split.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-nonmatchvalue
            '''
            result = self._values.get("non_match_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_if_exists(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to overwrite the value if the destination key already exists.

            If you omit this, the default is ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-overwriteifexists
            '''
            result = self._values.get("overwrite_if_exists")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Path to the field in the log event that will be parsed.

            Use dot notation to access child fields. For example, ``store.book``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsekeyvalue.html#cfn-logs-transformer-parsekeyvalue-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseKeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParsePostgresProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class ParsePostgresProperty:
        def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
            '''Use this processor to parse RDS for PostgreSQL vended logs, extract fields, and and convert them into a JSON format.

            This processor always processes the entire log event message. For more information about this processor including examples, see `parsePostGres <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parsePostGres>`_ .

            For more information about RDS for PostgreSQL log format, see `RDS for PostgreSQL database log filesTCP flag sequence <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_LogAccess.Concepts.PostgreSQL.html#USER_LogAccess.Concepts.PostgreSQL.Log_Format.log-line-prefix>`_ .
            .. epigraph::

               If you use this processor, it must be the first processor in your transformer.

            :param source: Omit this parameter and the whole log message will be processed by this processor. No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsepostgres.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_postgres_property = logs_mixins.CfnTransformerPropsMixin.ParsePostgresProperty(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__180c1874554a3e0bae9b8eb8fe6990a360e3910fc326aeb720ca2ce93f0c93a3)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Omit this parameter and the whole log message will be processed by this processor.

            No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsepostgres.html#cfn-logs-transformer-parsepostgres-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParsePostgresProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseRoute53Property",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class ParseRoute53Property:
        def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
            '''Use this processor to parse Route 53 vended logs, extract fields, and and convert them into a JSON format.

            This processor always processes the entire log event message. For more information about this processor including examples, see `parseRoute53 <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseRoute53>`_ .
            .. epigraph::

               If you use this processor, it must be the first processor in your transformer.

            :param source: Omit this parameter and the whole log message will be processed by this processor. No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parseroute53.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_route53_property = logs_mixins.CfnTransformerPropsMixin.ParseRoute53Property(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__349a95cb16adda610810c95dacd0f461374b7f19e50836ece0c525c0369ff0d9)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Omit this parameter and the whole log message will be processed by this processor.

            No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parseroute53.html#cfn-logs-transformer-parseroute53-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseRoute53Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseToOCSFProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_source": "eventSource",
            "ocsf_version": "ocsfVersion",
            "source": "source",
        },
    )
    class ParseToOCSFProperty:
        def __init__(
            self,
            *,
            event_source: typing.Optional[builtins.str] = None,
            ocsf_version: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This processor converts logs into `Open Cybersecurity Schema Framework (OCSF) <https://docs.aws.amazon.com/https://ocsf.io>`_ events.

            For more information about this processor including examples, see `parseToOCSF <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parseToOCSF>`_ in the *CloudWatch Logs User Guide* .

            :param event_source: Specify the service or process that produces the log events that will be converted with this processor.
            :param ocsf_version: Specify which version of the OCSF schema to use for the transformed log events.
            :param source: The path to the field in the log event that you want to parse. If you omit this value, the whole log message is parsed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsetoocsf.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_to_oCSFProperty = logs_mixins.CfnTransformerPropsMixin.ParseToOCSFProperty(
                    event_source="eventSource",
                    ocsf_version="ocsfVersion",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76748002f7cf25283b716246d4fb5fb2b46685bcbd0f453150ebe74df29d3668)
                check_type(argname="argument event_source", value=event_source, expected_type=type_hints["event_source"])
                check_type(argname="argument ocsf_version", value=ocsf_version, expected_type=type_hints["ocsf_version"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_source is not None:
                self._values["event_source"] = event_source
            if ocsf_version is not None:
                self._values["ocsf_version"] = ocsf_version
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def event_source(self) -> typing.Optional[builtins.str]:
            '''Specify the service or process that produces the log events that will be converted with this processor.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsetoocsf.html#cfn-logs-transformer-parsetoocsf-eventsource
            '''
            result = self._values.get("event_source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ocsf_version(self) -> typing.Optional[builtins.str]:
            '''Specify which version of the OCSF schema to use for the transformed log events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsetoocsf.html#cfn-logs-transformer-parsetoocsf-ocsfversion
            '''
            result = self._values.get("ocsf_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The path to the field in the log event that you want to parse.

            If you omit this value, the whole log message is parsed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsetoocsf.html#cfn-logs-transformer-parsetoocsf-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseToOCSFProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseVPCProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class ParseVPCProperty:
        def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
            '''Use this processor to parse Amazon VPC vended logs, extract fields, and and convert them into a JSON format.

            This processor always processes the entire log event message.

            This processor doesn't support custom log formats, such as NAT gateway logs. For more information about custom log formats in Amazon VPC, see `parseVPC <https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-records-examples.html#flow-log-example-tcp-flag>`_ For more information about this processor including examples, see `parseVPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parseVPC>`_ .
            .. epigraph::

               If you use this processor, it must be the first processor in your transformer.

            :param source: Omit this parameter and the whole log message will be processed by this processor. No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsevpc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_vPCProperty = logs_mixins.CfnTransformerPropsMixin.ParseVPCProperty(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4aa00c38e75bcf71c7625f014320839b0e55f0b46c4d3fee9309d11e1b3bf0de)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Omit this parameter and the whole log message will be processed by this processor.

            No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsevpc.html#cfn-logs-transformer-parsevpc-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseVPCProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ParseWAFProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class ParseWAFProperty:
        def __init__(self, *, source: typing.Optional[builtins.str] = None) -> None:
            '''Use this processor to parse AWS WAF vended logs, extract fields, and and convert them into a JSON format.

            This processor always processes the entire log event message. For more information about this processor including examples, see `parseWAF <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parsePostGres>`_ .

            For more information about AWS WAF log format, see `Log examples for web ACL traffic <https://docs.aws.amazon.com/waf/latest/developerguide/logging-examples.html>`_ .
            .. epigraph::

               If you use this processor, it must be the first processor in your transformer.

            :param source: Omit this parameter and the whole log message will be processed by this processor. No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsewaf.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                parse_wAFProperty = logs_mixins.CfnTransformerPropsMixin.ParseWAFProperty(
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a00e1815820d45c2551135e23cc210c46461f40114f0b31273e405f56aa01f7)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''Omit this parameter and the whole log message will be processed by this processor.

            No other value than ``@message`` is allowed for ``source`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-parsewaf.html#cfn-logs-transformer-parsewaf-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParseWAFProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.ProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_keys": "addKeys",
            "copy_value": "copyValue",
            "csv": "csv",
            "date_time_converter": "dateTimeConverter",
            "delete_keys": "deleteKeys",
            "grok": "grok",
            "list_to_map": "listToMap",
            "lower_case_string": "lowerCaseString",
            "move_keys": "moveKeys",
            "parse_cloudfront": "parseCloudfront",
            "parse_json": "parseJson",
            "parse_key_value": "parseKeyValue",
            "parse_postgres": "parsePostgres",
            "parse_route53": "parseRoute53",
            "parse_to_ocsf": "parseToOcsf",
            "parse_vpc": "parseVpc",
            "parse_waf": "parseWaf",
            "rename_keys": "renameKeys",
            "split_string": "splitString",
            "substitute_string": "substituteString",
            "trim_string": "trimString",
            "type_converter": "typeConverter",
            "upper_case_string": "upperCaseString",
        },
    )
    class ProcessorProperty:
        def __init__(
            self,
            *,
            add_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.AddKeysProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            copy_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.CopyValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.CsvProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            date_time_converter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.DateTimeConverterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            delete_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.DeleteKeysProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            grok: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.GrokProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            list_to_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ListToMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lower_case_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.LowerCaseStringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            move_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.MoveKeysProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_cloudfront: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseCloudfrontProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseJSONProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_key_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseKeyValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_postgres: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParsePostgresProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_route53: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseRoute53Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_to_ocsf: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseToOCSFProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseVPCProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parse_waf: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.ParseWAFProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rename_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.RenameKeysProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            split_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.SplitStringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            substitute_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.SubstituteStringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            trim_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.TrimStringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type_converter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.TypeConverterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            upper_case_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.UpperCaseStringProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This structure contains the information about one processor in a log transformer.

            :param add_keys: Use this parameter to include the `addKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-addKeys>`_ processor in your transformer.
            :param copy_value: Use this parameter to include the `copyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-copyValue>`_ processor in your transformer.
            :param csv: Use this parameter to include the `CSV <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-CSV>`_ processor in your transformer.
            :param date_time_converter: Use this parameter to include the `datetimeConverter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-datetimeConverter>`_ processor in your transformer.
            :param delete_keys: Use this parameter to include the `deleteKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-deleteKeys>`_ processor in your transformer.
            :param grok: Use this parameter to include the `grok <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-grok>`_ processor in your transformer.
            :param list_to_map: Use this parameter to include the `listToMap <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-listToMap>`_ processor in your transformer.
            :param lower_case_string: Use this parameter to include the `lowerCaseString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-lowerCaseString>`_ processor in your transformer.
            :param move_keys: Use this parameter to include the `moveKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-moveKeys>`_ processor in your transformer.
            :param parse_cloudfront: Use this parameter to include the `parseCloudfront <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseCloudfront>`_ processor in your transformer. If you use this processor, it must be the first processor in your transformer.
            :param parse_json: Use this parameter to include the `parseJSON <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseJSON>`_ processor in your transformer.
            :param parse_key_value: Use this parameter to include the `parseKeyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseKeyValue>`_ processor in your transformer.
            :param parse_postgres: Use this parameter to include the `parsePostGres <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parsePostGres>`_ processor in your transformer. If you use this processor, it must be the first processor in your transformer.
            :param parse_route53: Use this parameter to include the `parseRoute53 <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseRoute53>`_ processor in your transformer. If you use this processor, it must be the first processor in your transformer.
            :param parse_to_ocsf: Use this parameter to convert logs into Open Cybersecurity Schema (OCSF) format.
            :param parse_vpc: Use this parameter to include the `parseVPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseVPC>`_ processor in your transformer. If you use this processor, it must be the first processor in your transformer.
            :param parse_waf: Use this parameter to include the `parseWAF <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parseWAF>`_ processor in your transformer. If you use this processor, it must be the first processor in your transformer.
            :param rename_keys: Use this parameter to include the `renameKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-renameKeys>`_ processor in your transformer.
            :param split_string: Use this parameter to include the `splitString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-splitString>`_ processor in your transformer.
            :param substitute_string: Use this parameter to include the `substituteString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-substituteString>`_ processor in your transformer.
            :param trim_string: Use this parameter to include the `trimString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-trimString>`_ processor in your transformer.
            :param type_converter: Use this parameter to include the `typeConverter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-typeConverter>`_ processor in your transformer.
            :param upper_case_string: Use this parameter to include the `upperCaseString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-upperCaseString>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                processor_property = logs_mixins.CfnTransformerPropsMixin.ProcessorProperty(
                    add_keys=logs_mixins.CfnTransformerPropsMixin.AddKeysProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.AddKeyEntryProperty(
                            key="key",
                            overwrite_if_exists=False,
                            value="value"
                        )]
                    ),
                    copy_value=logs_mixins.CfnTransformerPropsMixin.CopyValueProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.CopyValueEntryProperty(
                            overwrite_if_exists=False,
                            source="source",
                            target="target"
                        )]
                    ),
                    csv=logs_mixins.CfnTransformerPropsMixin.CsvProperty(
                        columns=["columns"],
                        delimiter="delimiter",
                        quote_character="quoteCharacter",
                        source="source"
                    ),
                    date_time_converter=logs_mixins.CfnTransformerPropsMixin.DateTimeConverterProperty(
                        locale="locale",
                        match_patterns=["matchPatterns"],
                        source="source",
                        source_timezone="sourceTimezone",
                        target="target",
                        target_format="targetFormat",
                        target_timezone="targetTimezone"
                    ),
                    delete_keys=logs_mixins.CfnTransformerPropsMixin.DeleteKeysProperty(
                        with_keys=["withKeys"]
                    ),
                    grok=logs_mixins.CfnTransformerPropsMixin.GrokProperty(
                        match="match",
                        source="source"
                    ),
                    list_to_map=logs_mixins.CfnTransformerPropsMixin.ListToMapProperty(
                        flatten=False,
                        flattened_element="flattenedElement",
                        key="key",
                        source="source",
                        target="target",
                        value_key="valueKey"
                    ),
                    lower_case_string=logs_mixins.CfnTransformerPropsMixin.LowerCaseStringProperty(
                        with_keys=["withKeys"]
                    ),
                    move_keys=logs_mixins.CfnTransformerPropsMixin.MoveKeysProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.MoveKeyEntryProperty(
                            overwrite_if_exists=False,
                            source="source",
                            target="target"
                        )]
                    ),
                    parse_cloudfront=logs_mixins.CfnTransformerPropsMixin.ParseCloudfrontProperty(
                        source="source"
                    ),
                    parse_json=logs_mixins.CfnTransformerPropsMixin.ParseJSONProperty(
                        destination="destination",
                        source="source"
                    ),
                    parse_key_value=logs_mixins.CfnTransformerPropsMixin.ParseKeyValueProperty(
                        destination="destination",
                        field_delimiter="fieldDelimiter",
                        key_prefix="keyPrefix",
                        key_value_delimiter="keyValueDelimiter",
                        non_match_value="nonMatchValue",
                        overwrite_if_exists=False,
                        source="source"
                    ),
                    parse_postgres=logs_mixins.CfnTransformerPropsMixin.ParsePostgresProperty(
                        source="source"
                    ),
                    parse_route53=logs_mixins.CfnTransformerPropsMixin.ParseRoute53Property(
                        source="source"
                    ),
                    parse_to_ocsf=logs_mixins.CfnTransformerPropsMixin.ParseToOCSFProperty(
                        event_source="eventSource",
                        ocsf_version="ocsfVersion",
                        source="source"
                    ),
                    parse_vpc=logs_mixins.CfnTransformerPropsMixin.ParseVPCProperty(
                        source="source"
                    ),
                    parse_waf=logs_mixins.CfnTransformerPropsMixin.ParseWAFProperty(
                        source="source"
                    ),
                    rename_keys=logs_mixins.CfnTransformerPropsMixin.RenameKeysProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.RenameKeyEntryProperty(
                            key="key",
                            overwrite_if_exists=False,
                            rename_to="renameTo"
                        )]
                    ),
                    split_string=logs_mixins.CfnTransformerPropsMixin.SplitStringProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.SplitStringEntryProperty(
                            delimiter="delimiter",
                            source="source"
                        )]
                    ),
                    substitute_string=logs_mixins.CfnTransformerPropsMixin.SubstituteStringProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.SubstituteStringEntryProperty(
                            from="from",
                            source="source",
                            to="to"
                        )]
                    ),
                    trim_string=logs_mixins.CfnTransformerPropsMixin.TrimStringProperty(
                        with_keys=["withKeys"]
                    ),
                    type_converter=logs_mixins.CfnTransformerPropsMixin.TypeConverterProperty(
                        entries=[logs_mixins.CfnTransformerPropsMixin.TypeConverterEntryProperty(
                            key="key",
                            type="type"
                        )]
                    ),
                    upper_case_string=logs_mixins.CfnTransformerPropsMixin.UpperCaseStringProperty(
                        with_keys=["withKeys"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__678c8d1a1d5f553cd5b933cd04f953f086c5d28186b21786cde4cb0256558d28)
                check_type(argname="argument add_keys", value=add_keys, expected_type=type_hints["add_keys"])
                check_type(argname="argument copy_value", value=copy_value, expected_type=type_hints["copy_value"])
                check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
                check_type(argname="argument date_time_converter", value=date_time_converter, expected_type=type_hints["date_time_converter"])
                check_type(argname="argument delete_keys", value=delete_keys, expected_type=type_hints["delete_keys"])
                check_type(argname="argument grok", value=grok, expected_type=type_hints["grok"])
                check_type(argname="argument list_to_map", value=list_to_map, expected_type=type_hints["list_to_map"])
                check_type(argname="argument lower_case_string", value=lower_case_string, expected_type=type_hints["lower_case_string"])
                check_type(argname="argument move_keys", value=move_keys, expected_type=type_hints["move_keys"])
                check_type(argname="argument parse_cloudfront", value=parse_cloudfront, expected_type=type_hints["parse_cloudfront"])
                check_type(argname="argument parse_json", value=parse_json, expected_type=type_hints["parse_json"])
                check_type(argname="argument parse_key_value", value=parse_key_value, expected_type=type_hints["parse_key_value"])
                check_type(argname="argument parse_postgres", value=parse_postgres, expected_type=type_hints["parse_postgres"])
                check_type(argname="argument parse_route53", value=parse_route53, expected_type=type_hints["parse_route53"])
                check_type(argname="argument parse_to_ocsf", value=parse_to_ocsf, expected_type=type_hints["parse_to_ocsf"])
                check_type(argname="argument parse_vpc", value=parse_vpc, expected_type=type_hints["parse_vpc"])
                check_type(argname="argument parse_waf", value=parse_waf, expected_type=type_hints["parse_waf"])
                check_type(argname="argument rename_keys", value=rename_keys, expected_type=type_hints["rename_keys"])
                check_type(argname="argument split_string", value=split_string, expected_type=type_hints["split_string"])
                check_type(argname="argument substitute_string", value=substitute_string, expected_type=type_hints["substitute_string"])
                check_type(argname="argument trim_string", value=trim_string, expected_type=type_hints["trim_string"])
                check_type(argname="argument type_converter", value=type_converter, expected_type=type_hints["type_converter"])
                check_type(argname="argument upper_case_string", value=upper_case_string, expected_type=type_hints["upper_case_string"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_keys is not None:
                self._values["add_keys"] = add_keys
            if copy_value is not None:
                self._values["copy_value"] = copy_value
            if csv is not None:
                self._values["csv"] = csv
            if date_time_converter is not None:
                self._values["date_time_converter"] = date_time_converter
            if delete_keys is not None:
                self._values["delete_keys"] = delete_keys
            if grok is not None:
                self._values["grok"] = grok
            if list_to_map is not None:
                self._values["list_to_map"] = list_to_map
            if lower_case_string is not None:
                self._values["lower_case_string"] = lower_case_string
            if move_keys is not None:
                self._values["move_keys"] = move_keys
            if parse_cloudfront is not None:
                self._values["parse_cloudfront"] = parse_cloudfront
            if parse_json is not None:
                self._values["parse_json"] = parse_json
            if parse_key_value is not None:
                self._values["parse_key_value"] = parse_key_value
            if parse_postgres is not None:
                self._values["parse_postgres"] = parse_postgres
            if parse_route53 is not None:
                self._values["parse_route53"] = parse_route53
            if parse_to_ocsf is not None:
                self._values["parse_to_ocsf"] = parse_to_ocsf
            if parse_vpc is not None:
                self._values["parse_vpc"] = parse_vpc
            if parse_waf is not None:
                self._values["parse_waf"] = parse_waf
            if rename_keys is not None:
                self._values["rename_keys"] = rename_keys
            if split_string is not None:
                self._values["split_string"] = split_string
            if substitute_string is not None:
                self._values["substitute_string"] = substitute_string
            if trim_string is not None:
                self._values["trim_string"] = trim_string
            if type_converter is not None:
                self._values["type_converter"] = type_converter
            if upper_case_string is not None:
                self._values["upper_case_string"] = upper_case_string

        @builtins.property
        def add_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AddKeysProperty"]]:
            '''Use this parameter to include the `addKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-addKeys>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-addkeys
            '''
            result = self._values.get("add_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.AddKeysProperty"]], result)

        @builtins.property
        def copy_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.CopyValueProperty"]]:
            '''Use this parameter to include the `copyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-copyValue>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-copyvalue
            '''
            result = self._values.get("copy_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.CopyValueProperty"]], result)

        @builtins.property
        def csv(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.CsvProperty"]]:
            '''Use this parameter to include the `CSV <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-CSV>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-csv
            '''
            result = self._values.get("csv")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.CsvProperty"]], result)

        @builtins.property
        def date_time_converter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.DateTimeConverterProperty"]]:
            '''Use this parameter to include the `datetimeConverter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-datetimeConverter>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-datetimeconverter
            '''
            result = self._values.get("date_time_converter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.DateTimeConverterProperty"]], result)

        @builtins.property
        def delete_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.DeleteKeysProperty"]]:
            '''Use this parameter to include the `deleteKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-deleteKeys>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-deletekeys
            '''
            result = self._values.get("delete_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.DeleteKeysProperty"]], result)

        @builtins.property
        def grok(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.GrokProperty"]]:
            '''Use this parameter to include the `grok <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-grok>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-grok
            '''
            result = self._values.get("grok")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.GrokProperty"]], result)

        @builtins.property
        def list_to_map(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ListToMapProperty"]]:
            '''Use this parameter to include the `listToMap <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-listToMap>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-listtomap
            '''
            result = self._values.get("list_to_map")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ListToMapProperty"]], result)

        @builtins.property
        def lower_case_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.LowerCaseStringProperty"]]:
            '''Use this parameter to include the `lowerCaseString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-lowerCaseString>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-lowercasestring
            '''
            result = self._values.get("lower_case_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.LowerCaseStringProperty"]], result)

        @builtins.property
        def move_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.MoveKeysProperty"]]:
            '''Use this parameter to include the `moveKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-moveKeys>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-movekeys
            '''
            result = self._values.get("move_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.MoveKeysProperty"]], result)

        @builtins.property
        def parse_cloudfront(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseCloudfrontProperty"]]:
            '''Use this parameter to include the `parseCloudfront <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseCloudfront>`_ processor in your transformer.

            If you use this processor, it must be the first processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsecloudfront
            '''
            result = self._values.get("parse_cloudfront")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseCloudfrontProperty"]], result)

        @builtins.property
        def parse_json(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseJSONProperty"]]:
            '''Use this parameter to include the `parseJSON <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseJSON>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsejson
            '''
            result = self._values.get("parse_json")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseJSONProperty"]], result)

        @builtins.property
        def parse_key_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseKeyValueProperty"]]:
            '''Use this parameter to include the `parseKeyValue <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseKeyValue>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsekeyvalue
            '''
            result = self._values.get("parse_key_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseKeyValueProperty"]], result)

        @builtins.property
        def parse_postgres(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParsePostgresProperty"]]:
            '''Use this parameter to include the `parsePostGres <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parsePostGres>`_ processor in your transformer.

            If you use this processor, it must be the first processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsepostgres
            '''
            result = self._values.get("parse_postgres")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParsePostgresProperty"]], result)

        @builtins.property
        def parse_route53(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseRoute53Property"]]:
            '''Use this parameter to include the `parseRoute53 <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseRoute53>`_ processor in your transformer.

            If you use this processor, it must be the first processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parseroute53
            '''
            result = self._values.get("parse_route53")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseRoute53Property"]], result)

        @builtins.property
        def parse_to_ocsf(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseToOCSFProperty"]]:
            '''Use this parameter to convert logs into Open Cybersecurity Schema (OCSF) format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsetoocsf
            '''
            result = self._values.get("parse_to_ocsf")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseToOCSFProperty"]], result)

        @builtins.property
        def parse_vpc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseVPCProperty"]]:
            '''Use this parameter to include the `parseVPC <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-parseVPC>`_ processor in your transformer.

            If you use this processor, it must be the first processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsevpc
            '''
            result = self._values.get("parse_vpc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseVPCProperty"]], result)

        @builtins.property
        def parse_waf(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseWAFProperty"]]:
            '''Use this parameter to include the `parseWAF <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-parseWAF>`_ processor in your transformer.

            If you use this processor, it must be the first processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-parsewaf
            '''
            result = self._values.get("parse_waf")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.ParseWAFProperty"]], result)

        @builtins.property
        def rename_keys(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.RenameKeysProperty"]]:
            '''Use this parameter to include the `renameKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation.html#CloudWatch-Logs-Transformation-renameKeys>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-renamekeys
            '''
            result = self._values.get("rename_keys")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.RenameKeysProperty"]], result)

        @builtins.property
        def split_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SplitStringProperty"]]:
            '''Use this parameter to include the `splitString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-splitString>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-splitstring
            '''
            result = self._values.get("split_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SplitStringProperty"]], result)

        @builtins.property
        def substitute_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SubstituteStringProperty"]]:
            '''Use this parameter to include the `substituteString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-substituteString>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-substitutestring
            '''
            result = self._values.get("substitute_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SubstituteStringProperty"]], result)

        @builtins.property
        def trim_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.TrimStringProperty"]]:
            '''Use this parameter to include the `trimString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-trimString>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-trimstring
            '''
            result = self._values.get("trim_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.TrimStringProperty"]], result)

        @builtins.property
        def type_converter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.TypeConverterProperty"]]:
            '''Use this parameter to include the `typeConverter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-typeConverter>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-typeconverter
            '''
            result = self._values.get("type_converter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.TypeConverterProperty"]], result)

        @builtins.property
        def upper_case_string(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.UpperCaseStringProperty"]]:
            '''Use this parameter to include the `upperCaseString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-upperCaseString>`_ processor in your transformer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-processor.html#cfn-logs-transformer-processor-uppercasestring
            '''
            result = self._values.get("upper_case_string")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.UpperCaseStringProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.RenameKeyEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key": "key",
            "overwrite_if_exists": "overwriteIfExists",
            "rename_to": "renameTo",
        },
    )
    class RenameKeyEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            rename_to: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one key that will be renamed with the `renameKey <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-renameKey>`_ processor.

            :param key: The key to rename.
            :param overwrite_if_exists: Specifies whether to overwrite the existing value if the destination key already exists. The default is ``false``
            :param rename_to: The string to use for the new key name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-renamekeyentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                rename_key_entry_property = logs_mixins.CfnTransformerPropsMixin.RenameKeyEntryProperty(
                    key="key",
                    overwrite_if_exists=False,
                    rename_to="renameTo"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7d06ad74a814c796821473476aac8877f36d118ab411e2190266816077bfd871)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument overwrite_if_exists", value=overwrite_if_exists, expected_type=type_hints["overwrite_if_exists"])
                check_type(argname="argument rename_to", value=rename_to, expected_type=type_hints["rename_to"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if overwrite_if_exists is not None:
                self._values["overwrite_if_exists"] = overwrite_if_exists
            if rename_to is not None:
                self._values["rename_to"] = rename_to

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key to rename.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-renamekeyentry.html#cfn-logs-transformer-renamekeyentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_if_exists(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to overwrite the existing value if the destination key already exists.

            The default is ``false``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-renamekeyentry.html#cfn-logs-transformer-renamekeyentry-overwriteifexists
            '''
            result = self._values.get("overwrite_if_exists")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def rename_to(self) -> typing.Optional[builtins.str]:
            '''The string to use for the new key name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-renamekeyentry.html#cfn-logs-transformer-renamekeyentry-renameto
            '''
            result = self._values.get("rename_to")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenameKeyEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.RenameKeysProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class RenameKeysProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.RenameKeyEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use this processor to rename keys in a log event.

            For more information about this processor including examples, see `renameKeys <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-renameKeys>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of ``RenameKeyEntry`` objects, where each object contains the information about a single key to rename.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-renamekeys.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                rename_keys_property = logs_mixins.CfnTransformerPropsMixin.RenameKeysProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.RenameKeyEntryProperty(
                        key="key",
                        overwrite_if_exists=False,
                        rename_to="renameTo"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8361a7518ff73929443a1172ed4efbae851af7874f1a88381c977b1ba7cff20)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.RenameKeyEntryProperty"]]]]:
            '''An array of ``RenameKeyEntry`` objects, where each object contains the information about a single key to rename.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-renamekeys.html#cfn-logs-transformer-renamekeys-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.RenameKeyEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenameKeysProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.SplitStringEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"delimiter": "delimiter", "source": "source"},
    )
    class SplitStringEntryProperty:
        def __init__(
            self,
            *,
            delimiter: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one log field that will be split with the `splitString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-splitString>`_ processor.

            :param delimiter: The separator characters to split the string entry on.
            :param source: The key of the field to split.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-splitstringentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                split_string_entry_property = logs_mixins.CfnTransformerPropsMixin.SplitStringEntryProperty(
                    delimiter="delimiter",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b897841b17b95154334a7f6cbeaf6a762d4b9df5d26d325899e7d3638706e16e)
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''The separator characters to split the string entry on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-splitstringentry.html#cfn-logs-transformer-splitstringentry-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The key of the field to split.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-splitstringentry.html#cfn-logs-transformer-splitstringentry-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplitStringEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.SplitStringProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class SplitStringProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.SplitStringEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use this processor to split a field into an array of strings using a delimiting character.

            For more information about this processor including examples, see `splitString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-splitString>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of ``SplitStringEntry`` objects, where each object contains the information about one field to split.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-splitstring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                split_string_property = logs_mixins.CfnTransformerPropsMixin.SplitStringProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.SplitStringEntryProperty(
                        delimiter="delimiter",
                        source="source"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__290ae2d89995870f580e4b4e3bbaf47078cb386f272cb75ea438c70aa6153142)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SplitStringEntryProperty"]]]]:
            '''An array of ``SplitStringEntry`` objects, where each object contains the information about one field to split.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-splitstring.html#cfn-logs-transformer-splitstring-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SplitStringEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SplitStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.SubstituteStringEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"from_": "from", "source": "source", "to": "to"},
    )
    class SubstituteStringEntryProperty:
        def __init__(
            self,
            *,
            from_: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
            to: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one log field key that will be replaced using the `substituteString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-substituteString>`_ processor.

            :param from_: The regular expression string to be replaced. Special regex characters such as [ and ] must be escaped using \\ when using double quotes and with \\ when using single quotes. For more information, see `Class Pattern <https://docs.aws.amazon.com/https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/regex/Pattern.html>`_ on the Oracle web site.
            :param source: The key to modify.
            :param to: The string to be substituted for each match of ``from``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-substitutestringentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                substitute_string_entry_property = logs_mixins.CfnTransformerPropsMixin.SubstituteStringEntryProperty(
                    from="from",
                    source="source",
                    to="to"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__113ae74aa71e85cd245c88cdc3dd785fa39b82d9f84817d7f32ea7b3bccd4fd6)
                check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument to", value=to, expected_type=type_hints["to"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if from_ is not None:
                self._values["from_"] = from_
            if source is not None:
                self._values["source"] = source
            if to is not None:
                self._values["to"] = to

        @builtins.property
        def from_(self) -> typing.Optional[builtins.str]:
            '''The regular expression string to be replaced.

            Special regex characters such as [ and ] must be escaped using \\ when using double quotes and with \\ when using single quotes. For more information, see `Class Pattern <https://docs.aws.amazon.com/https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/regex/Pattern.html>`_ on the Oracle web site.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-substitutestringentry.html#cfn-logs-transformer-substitutestringentry-from
            '''
            result = self._values.get("from_")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The key to modify.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-substitutestringentry.html#cfn-logs-transformer-substitutestringentry-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def to(self) -> typing.Optional[builtins.str]:
            '''The string to be substituted for each match of ``from``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-substitutestringentry.html#cfn-logs-transformer-substitutestringentry-to
            '''
            result = self._values.get("to")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubstituteStringEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.SubstituteStringProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class SubstituteStringProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.SubstituteStringEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This processor matches a key’s value against a regular expression and replaces all matches with a replacement string.

            For more information about this processor including examples, see `substituteString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-substituteString>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of objects, where each object contains the information about one key to match and replace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-substitutestring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                substitute_string_property = logs_mixins.CfnTransformerPropsMixin.SubstituteStringProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.SubstituteStringEntryProperty(
                        from="from",
                        source="source",
                        to="to"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da120fa5bea1f632b577093b0d146867ea23f50e3c7ecde650fdc2a1b76d5434)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SubstituteStringEntryProperty"]]]]:
            '''An array of objects, where each object contains the information about one key to match and replace.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-substitutestring.html#cfn-logs-transformer-substitutestring-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.SubstituteStringEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubstituteStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.TrimStringProperty",
        jsii_struct_bases=[],
        name_mapping={"with_keys": "withKeys"},
    )
    class TrimStringProperty:
        def __init__(
            self,
            *,
            with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Use this processor to remove leading and trailing whitespace.

            For more information about this processor including examples, see `trimString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-trimString>`_ in the *CloudWatch Logs User Guide* .

            :param with_keys: The array containing the keys of the fields to trim.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-trimstring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                trim_string_property = logs_mixins.CfnTransformerPropsMixin.TrimStringProperty(
                    with_keys=["withKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa7a8ed7c0e78c0a8895e2f84d958c5ad21b282dd1aa8f180e5d5534766184c6)
                check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if with_keys is not None:
                self._values["with_keys"] = with_keys

        @builtins.property
        def with_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array containing the keys of the fields to trim.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-trimstring.html#cfn-logs-transformer-trimstring-withkeys
            '''
            result = self._values.get("with_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrimStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.TypeConverterEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "type": "type"},
    )
    class TypeConverterEntryProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This object defines one value type that will be converted using the `typeConverter <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-typeConverter>`_ processor.

            :param key: The key with the value that is to be converted to a different type.
            :param type: The type to convert the field value to. Valid values are ``integer`` , ``double`` , ``string`` and ``boolean`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-typeconverterentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                type_converter_entry_property = logs_mixins.CfnTransformerPropsMixin.TypeConverterEntryProperty(
                    key="key",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c96b1114fb41faf72381a2bf5aa82fa807e78b3df49b435c3c7430b815d2ece)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key with the value that is to be converted to a different type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-typeconverterentry.html#cfn-logs-transformer-typeconverterentry-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type to convert the field value to.

            Valid values are ``integer`` , ``double`` , ``string`` and ``boolean`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-typeconverterentry.html#cfn-logs-transformer-typeconverterentry-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TypeConverterEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.TypeConverterProperty",
        jsii_struct_bases=[],
        name_mapping={"entries": "entries"},
    )
    class TypeConverterProperty:
        def __init__(
            self,
            *,
            entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransformerPropsMixin.TypeConverterEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Use this processor to convert a value type associated with the specified key to the specified type.

            It's a casting processor that changes the types of the specified fields. Values can be converted into one of the following datatypes: ``integer`` , ``double`` , ``string`` and ``boolean`` .

            For more information about this processor including examples, see `trimString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-trimString>`_ in the *CloudWatch Logs User Guide* .

            :param entries: An array of ``TypeConverterEntry`` objects, where each object contains the information about one field to change the type of.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-typeconverter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                type_converter_property = logs_mixins.CfnTransformerPropsMixin.TypeConverterProperty(
                    entries=[logs_mixins.CfnTransformerPropsMixin.TypeConverterEntryProperty(
                        key="key",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__933917532699d3fbadc2c1d2241f718967156b3052788c2589b4d4656809ec5c)
                check_type(argname="argument entries", value=entries, expected_type=type_hints["entries"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entries is not None:
                self._values["entries"] = entries

        @builtins.property
        def entries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.TypeConverterEntryProperty"]]]]:
            '''An array of ``TypeConverterEntry`` objects, where each object contains the information about one field to change the type of.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-typeconverter.html#cfn-logs-transformer-typeconverter-entries
            '''
            result = self._values.get("entries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransformerPropsMixin.TypeConverterEntryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TypeConverterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_logs.mixins.CfnTransformerPropsMixin.UpperCaseStringProperty",
        jsii_struct_bases=[],
        name_mapping={"with_keys": "withKeys"},
    )
    class UpperCaseStringProperty:
        def __init__(
            self,
            *,
            with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This processor converts a string field to uppercase.

            For more information about this processor including examples, see `upperCaseString <https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch-Logs-Transformation-Processors.html#CloudWatch-Logs-Transformation-upperCaseString>`_ in the *CloudWatch Logs User Guide* .

            :param with_keys: The array of containing the keys of the field to convert to uppercase.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-uppercasestring.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_logs import mixins as logs_mixins
                
                upper_case_string_property = logs_mixins.CfnTransformerPropsMixin.UpperCaseStringProperty(
                    with_keys=["withKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__821b85069db85a977f38c87264db847a59599dca68cb224328c7c40d225111af)
                check_type(argname="argument with_keys", value=with_keys, expected_type=type_hints["with_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if with_keys is not None:
                self._values["with_keys"] = with_keys

        @builtins.property
        def with_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of containing the keys of the field to convert to uppercase.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-logs-transformer-uppercasestring.html#cfn-logs-transformer-uppercasestring-withkeys
            '''
            result = self._values.get("with_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpperCaseStringProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccountPolicyMixinProps",
    "CfnAccountPolicyPropsMixin",
    "CfnDeliveryDestinationMixinProps",
    "CfnDeliveryDestinationPropsMixin",
    "CfnDeliveryMixinProps",
    "CfnDeliveryPropsMixin",
    "CfnDeliverySourceMixinProps",
    "CfnDeliverySourcePropsMixin",
    "CfnDestinationMixinProps",
    "CfnDestinationPropsMixin",
    "CfnIntegrationMixinProps",
    "CfnIntegrationPropsMixin",
    "CfnLogAnomalyDetectorMixinProps",
    "CfnLogAnomalyDetectorPropsMixin",
    "CfnLogGroupMixinProps",
    "CfnLogGroupPropsMixin",
    "CfnLogStreamMixinProps",
    "CfnLogStreamPropsMixin",
    "CfnMetricFilterMixinProps",
    "CfnMetricFilterPropsMixin",
    "CfnQueryDefinitionMixinProps",
    "CfnQueryDefinitionPropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnSubscriptionFilterMixinProps",
    "CfnSubscriptionFilterPropsMixin",
    "CfnTransformerMixinProps",
    "CfnTransformerPropsMixin",
]

publication.publish()

def _typecheckingstub__05e9f7747f7ed71835091ec3783faae5a96fef3ed5b1f4e48bc0ecae27c0bfe7(
    *,
    policy_document: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    selection_criteria: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b4e4698b738ed0a1969dcd9a6bf207f2ab4df20f7bb22022e6b5c4cd50b905(
    props: typing.Union[CfnAccountPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce0ade5dd433eae28f8021404f593ad0cb77f657355c0598e3e0e8ef159e5d4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3926564a102acf5c9fa3753a42d9d54e37fc83e417b7611da2cfee62354488c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e140ffa7516223860f4cabe5d8e75d264ed74f5ad12d39823f88dbad992186(
    *,
    delivery_destination_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDeliveryDestinationPropsMixin.DestinationPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delivery_destination_type: typing.Optional[builtins.str] = None,
    destination_resource_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    output_format: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e3484831d6c4a56b29112a049d9912c0374c0d6609e1f1c313909400d23cc3(
    props: typing.Union[CfnDeliveryDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b741c7d24389f30f8422259c838236bc4520b64688f0155f233402d40b4c50e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e648e811fe74409270723b2c2fb69fd8a517f5abf7202e08eb2f3d9b85b434(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d951f283038c601c8b734c9a9c0c5a39d61fdfc6276bc71138bc76059874326(
    *,
    delivery_destination_name: typing.Optional[builtins.str] = None,
    delivery_destination_policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2813e3a55bb7f6dd4ebbdaf6691cac31127bc792ed24f7f3aa1a5bdf34804d06(
    *,
    delivery_destination_arn: typing.Optional[builtins.str] = None,
    delivery_source_name: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    record_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_enable_hive_compatible_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    s3_suffix_path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78170b657e59651144b2e9e0fcfe39ab5878aa031374d52745dec68c22225bda(
    props: typing.Union[CfnDeliveryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbc4dba2680ca421f5b7f04b9063cf658cdaf1ce84c40f41be2a9a54d4691bf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1644fe16dae2f7d56a55c064293eb0b930fa0bf50dc807ddd4f4be574c22f41(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03b9eadeb0e7078d0b7954f59805831368c2b5338190cb04637ccfa64521706c(
    *,
    log_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab946efc54d0e40b9272ff741e610c41612474f906f33975a49d22ddb7590ef8(
    props: typing.Union[CfnDeliverySourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d538e3d35b21f2692a0b81a06da6ad7c8936f35ade13a9d89d8405f13ca8808(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d834b7effd7c5d8f7ae1e66f65bfb649b3ed549d1eed5912b253617aae4f0acc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c0e11cbf0218875c845eb85c4e565f8013ec425d3d2dc6d779cfffa67a3eb5(
    *,
    destination_name: typing.Optional[builtins.str] = None,
    destination_policy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4a30e19bceccd3dd25bf89196507954a3b31a352974bdd429cbab2c433ad49(
    props: typing.Union[CfnDestinationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69974d0b6fc339030d104d058801e112c135015119ba7cb5782cfde68fa006a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b014e964cf09f995ba397487d4a0fefa6241b8deac6afcaf8178c9ced13d2d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91bf1924fcc92e466527874a42dfec87f8a948bb89e9ac123894a8c344a99cd3(
    *,
    integration_name: typing.Optional[builtins.str] = None,
    integration_type: typing.Optional[builtins.str] = None,
    resource_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.ResourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37b5d1da24fe0202150d41aebb0280fecf9f8c2313dd9b011471fe521968befe(
    props: typing.Union[CfnIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbfb774d1a790990e7d72775f06c886f46aa878ee272b3db8e6c396b203d356(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98363275cc5186becfe597c122fa83d08b169e4fc6e2f1ae58c713bb85dd0f54(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fdfcdaca7a0ffdb5ec3990a595f52661b6534ba0c01b9e71ac24fce87d311a4(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    dashboard_viewer_principals: typing.Optional[typing.Sequence[builtins.str]] = None,
    data_source_role_arn: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    retention_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6016ad3647dd01167a3bc4c44c648093c83230c3265c638a6ca74cf1312ebab6(
    *,
    open_search_resource_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIntegrationPropsMixin.OpenSearchResourceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8091252a33657603d33b68415c1ada5da2daef79054e92d2e40e05ea28603ff5(
    *,
    account_id: typing.Optional[builtins.str] = None,
    anomaly_visibility_time: typing.Optional[jsii.Number] = None,
    detector_name: typing.Optional[builtins.str] = None,
    evaluation_frequency: typing.Optional[builtins.str] = None,
    filter_pattern: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_group_arn_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9c7386b4d5d41219a865b789addeaf5b5e9ca261f5dae4cf913653b7e1fd75(
    props: typing.Union[CfnLogAnomalyDetectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2656bf8e2a4704f127e1c7eea975e301985a02ce1f577fe1ecc1996ec9f7321(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42015450c2adda1ce4cc44330d0e6706e20a8d67c6498493bb3e950d829dbd31(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcfd36f3547ccea21154310cb409dd269198e62678326cf43b7418109b08b10(
    *,
    data_protection_policy: typing.Any = None,
    field_index_policies: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    log_group_class: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    resource_policy_document: typing.Any = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8d50e8b584f8ee1a76db798f0ebdca5c38e01b57a8417c6c99287a2b9e3374(
    props: typing.Union[CfnLogGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ca2eecd83565ff1e2ca9ead627b16918917a791159a611295cbc203fdc57d01(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e188a6c2cadda4bfa9e60bf5697dffe63f77b1c1c960eadea162a04a7a9619(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8c9e04946990dabab366c72294fe0cf40f76d69efbd528f0c2ad8aa3620bca(
    *,
    log_group_name: typing.Optional[builtins.str] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f3e3444e26a482dc65223cc4e7a99872ef98500b321af35923daeddb4fe5f54(
    props: typing.Union[CfnLogStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d118a2f81f692e58a5cbd7382bd0f14bec00354eb8d6177a282a5c56a50181(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630fcb337b32d4fd1f293498effbffd42da1be814c622bce5b60110b1b9be845(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12afaf3844ca8961e1e3fb91073af969d7d5443f669fef5737c445d0812f8322(
    *,
    apply_on_transformed_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    emit_system_field_dimensions: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_selection_criteria: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    filter_pattern: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    metric_transformations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMetricFilterPropsMixin.MetricTransformationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244449fd6cfbff41a6b557b5a3dce05abdde8da042a647d7fce1b6fd9609dee5(
    props: typing.Union[CfnMetricFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36902c8bbb50d401af7a986179c9369abb61b07abe240869fcf64f1b4261fc3b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5d66476210d8b53eb8b7209c5068026b80a78aadde39d845a5cfe546d58e0c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c17365c0cbf8ab8061494e453e2f2f8f3982480aa0a346a6288a7617cc49c2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8509f92d16a099fa4fa39f63077ba54904091b4d1fad7656dce5994ab8f2d81(
    *,
    default_value: typing.Optional[jsii.Number] = None,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMetricFilterPropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    metric_namespace: typing.Optional[builtins.str] = None,
    metric_value: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4c993fa29bebca5c6105c766e26bf83c23b46e71a5259b92387872fcc5d990(
    *,
    log_group_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    query_language: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4707fc858d287deb7a0b4607b67c32b77d8adf161b300d9d9322767a77a99e1f(
    props: typing.Union[CfnQueryDefinitionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e61033d80288d1b8ba7f540e142e50b0501e73a225d7693755f93075a2cf73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7281cdc9e2c6535840e6243accfbeb09f237bd0b54283e6b4ebe66d85f485899(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8098d5b1556c49e4b798b680fce0da63d816f14cc1908909bbf87c774d79ad07(
    *,
    policy_document: typing.Optional[builtins.str] = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73536152504d3636cde5f329bf2fa20e688751d271de326fe58475da0a796cbb(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfdf7bdab4e5fb5cdaae391a63bd67ce9892f8ac8e403d235aa6b1029c27277(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68e922ef7dfe319721cca6b6d49941876d635334d3a90856c7a030a7b37cdee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662da04ba6d51433c3529ff8ec3e212d90e65562c0eab0a07870ee9fc7fc9062(
    *,
    apply_on_transformed_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    destination_arn: typing.Optional[builtins.str] = None,
    distribution: typing.Optional[builtins.str] = None,
    emit_system_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    field_selection_criteria: typing.Optional[builtins.str] = None,
    filter_name: typing.Optional[builtins.str] = None,
    filter_pattern: typing.Optional[builtins.str] = None,
    log_group_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c08bd8f99c3ec897d7eab414504709326176223c115b0ed89420683ec331488(
    props: typing.Union[CfnSubscriptionFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94adb0624e83dc095f72e15139df5c0392267b22ed528fbf316051d5474357d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b565d3dd7a767f9b5f10f8d976e9146082c357a0b77876c276045b091dca63(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f26e528cf71b5cb429c4d0a3316e752366ee84bf582296e385038b6ca019f2(
    *,
    log_group_identifier: typing.Optional[builtins.str] = None,
    transformer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ProcessorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea10f667828fffb65fbb6710fca7d2b13742745b7af831a23dd705abf3f1f253(
    props: typing.Union[CfnTransformerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d15148b0d55b83011953e1cda962cc1cb2c57e744974fbd9ab7b438fc922936(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__882ff36a1be15cdce7b703f4b52b9beb5de6d315313134bd74a8366849c50af6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f45d7aa3eca126a2d3f429b6323c30c747099c3608b3ba29efbad426ed0d65(
    *,
    key: typing.Optional[builtins.str] = None,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703a0aecb9526ba4cdb6da9e9055d7e7f25fbe51c319a64488ce4d3293effb1b(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.AddKeyEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d49a1bc306e4ca525b566f40955e956daed3c06c2ed3cf36ce960903ddac8c(
    *,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfa5782899e07f00e40154465dc891eb4f44adaa1420c14d9d23fc9d8939aab(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.CopyValueEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460d7382089bbf89bf43cb1dd88f28fb69f218ee1256484790fb651a599adc76(
    *,
    columns: typing.Optional[typing.Sequence[builtins.str]] = None,
    delimiter: typing.Optional[builtins.str] = None,
    quote_character: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0747024fa607c26ba2bee148ae3cfe7eba779035901211feaee117feadb6a907(
    *,
    locale: typing.Optional[builtins.str] = None,
    match_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    source_timezone: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    target_format: typing.Optional[builtins.str] = None,
    target_timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddbc74b302a9896bec24e3cfd1ad824ad641e5d624802c0fc09c9f772abb8c3(
    *,
    with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84752e0a340d8b821fbc87d2717384a271b9c9eae4f0ff3cc961c85b562256d(
    *,
    match: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120c4ae0a72d13a64b472141df1fdcca20739df6d3b5c789ca8eebeb664afad2(
    *,
    flatten: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    flattened_element: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    value_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac9227498a241896bf211756e2424d3c286de2c2d45a50fdc5909433620a6cda(
    *,
    with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d4f68f435a379518350c7c1ac69b7a739d0f93e1613080a4b07213e8e5b5a27(
    *,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3eb685b55e665b546e13653599231f1fcf5f27c2f9784e302e972b9e70e7f54(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.MoveKeyEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b47409c3ccaa43ec9960596be0ca68018e4897df29bfc098b7b1a724310a79(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37538c6a6f7db2044e9862c3980c8a6295cdb8db40544fda8791e4bc61ca325(
    *,
    destination: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b28faa21f8d101e6d647b62e5add73b27e4613f69641ed2441a1b821aebbfe6(
    *,
    destination: typing.Optional[builtins.str] = None,
    field_delimiter: typing.Optional[builtins.str] = None,
    key_prefix: typing.Optional[builtins.str] = None,
    key_value_delimiter: typing.Optional[builtins.str] = None,
    non_match_value: typing.Optional[builtins.str] = None,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180c1874554a3e0bae9b8eb8fe6990a360e3910fc326aeb720ca2ce93f0c93a3(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349a95cb16adda610810c95dacd0f461374b7f19e50836ece0c525c0369ff0d9(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76748002f7cf25283b716246d4fb5fb2b46685bcbd0f453150ebe74df29d3668(
    *,
    event_source: typing.Optional[builtins.str] = None,
    ocsf_version: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa00c38e75bcf71c7625f014320839b0e55f0b46c4d3fee9309d11e1b3bf0de(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a00e1815820d45c2551135e23cc210c46461f40114f0b31273e405f56aa01f7(
    *,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678c8d1a1d5f553cd5b933cd04f953f086c5d28186b21786cde4cb0256558d28(
    *,
    add_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.AddKeysProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    copy_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.CopyValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.CsvProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    date_time_converter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.DateTimeConverterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delete_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.DeleteKeysProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    grok: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.GrokProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    list_to_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ListToMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lower_case_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.LowerCaseStringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    move_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.MoveKeysProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_cloudfront: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseCloudfrontProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseJSONProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_key_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseKeyValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_postgres: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParsePostgresProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_route53: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseRoute53Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_to_ocsf: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseToOCSFProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_vpc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseVPCProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parse_waf: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.ParseWAFProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rename_keys: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.RenameKeysProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    split_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.SplitStringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    substitute_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.SubstituteStringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    trim_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.TrimStringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_converter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.TypeConverterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    upper_case_string: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.UpperCaseStringProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d06ad74a814c796821473476aac8877f36d118ab411e2190266816077bfd871(
    *,
    key: typing.Optional[builtins.str] = None,
    overwrite_if_exists: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    rename_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8361a7518ff73929443a1172ed4efbae851af7874f1a88381c977b1ba7cff20(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.RenameKeyEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b897841b17b95154334a7f6cbeaf6a762d4b9df5d26d325899e7d3638706e16e(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__290ae2d89995870f580e4b4e3bbaf47078cb386f272cb75ea438c70aa6153142(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.SplitStringEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113ae74aa71e85cd245c88cdc3dd785fa39b82d9f84817d7f32ea7b3bccd4fd6(
    *,
    from_: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da120fa5bea1f632b577093b0d146867ea23f50e3c7ecde650fdc2a1b76d5434(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.SubstituteStringEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7a8ed7c0e78c0a8895e2f84d958c5ad21b282dd1aa8f180e5d5534766184c6(
    *,
    with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c96b1114fb41faf72381a2bf5aa82fa807e78b3df49b435c3c7430b815d2ece(
    *,
    key: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933917532699d3fbadc2c1d2241f718967156b3052788c2589b4d4656809ec5c(
    *,
    entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransformerPropsMixin.TypeConverterEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821b85069db85a977f38c87264db847a59599dca68cb224328c7c40d225111af(
    *,
    with_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
