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
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnAlarmMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_name": "alarmName",
        "comparison_operator": "comparisonOperator",
        "contact_protocols": "contactProtocols",
        "datapoints_to_alarm": "datapointsToAlarm",
        "evaluation_periods": "evaluationPeriods",
        "metric_name": "metricName",
        "monitored_resource_name": "monitoredResourceName",
        "notification_enabled": "notificationEnabled",
        "notification_triggers": "notificationTriggers",
        "threshold": "threshold",
        "treat_missing_data": "treatMissingData",
    },
)
class CfnAlarmMixinProps:
    def __init__(
        self,
        *,
        alarm_name: typing.Optional[builtins.str] = None,
        comparison_operator: typing.Optional[builtins.str] = None,
        contact_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        datapoints_to_alarm: typing.Optional[jsii.Number] = None,
        evaluation_periods: typing.Optional[jsii.Number] = None,
        metric_name: typing.Optional[builtins.str] = None,
        monitored_resource_name: typing.Optional[builtins.str] = None,
        notification_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        notification_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
        threshold: typing.Optional[jsii.Number] = None,
        treat_missing_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAlarmPropsMixin.

        :param alarm_name: The name of the alarm.
        :param comparison_operator: The arithmetic operation to use when comparing the specified statistic and threshold.
        :param contact_protocols: The contact protocols for the alarm, such as ``Email`` , ``SMS`` (text messaging), or both. *Allowed Values* : ``Email`` | ``SMS``
        :param datapoints_to_alarm: The number of data points within the evaluation periods that must be breaching to cause the alarm to go to the ``ALARM`` state.
        :param evaluation_periods: The number of periods over which data is compared to the specified threshold.
        :param metric_name: The name of the metric associated with the alarm.
        :param monitored_resource_name: The name of the Lightsail resource that the alarm monitors.
        :param notification_enabled: A Boolean value indicating whether the alarm is enabled.
        :param notification_triggers: The alarm states that trigger a notification. .. epigraph:: To specify the ``OK`` and ``INSUFFICIENT_DATA`` values, you must also specify ``ContactProtocols`` values. Otherwise, the ``OK`` and ``INSUFFICIENT_DATA`` values will not take effect and the stack will drift. *Allowed Values* : ``OK`` | ``ALARM`` | ``INSUFFICIENT_DATA``
        :param threshold: The value against which the specified statistic is compared.
        :param treat_missing_data: Specifies how the alarm handles missing data points. An alarm can treat missing data in the following ways: - ``breaching`` - Assumes the missing data is not within the threshold. Missing data counts towards the number of times that the metric is not within the threshold. - ``notBreaching`` - Assumes the missing data is within the threshold. Missing data does not count towards the number of times that the metric is not within the threshold. - ``ignore`` - Ignores the missing data. Maintains the current alarm state. - ``missing`` - Missing data is treated as missing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_alarm_mixin_props = lightsail_mixins.CfnAlarmMixinProps(
                alarm_name="alarmName",
                comparison_operator="comparisonOperator",
                contact_protocols=["contactProtocols"],
                datapoints_to_alarm=123,
                evaluation_periods=123,
                metric_name="metricName",
                monitored_resource_name="monitoredResourceName",
                notification_enabled=False,
                notification_triggers=["notificationTriggers"],
                threshold=123,
                treat_missing_data="treatMissingData"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c4104dc7bd29b63dfc786678fc328c3102ea78923154761ce34c802ab27e43)
            check_type(argname="argument alarm_name", value=alarm_name, expected_type=type_hints["alarm_name"])
            check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
            check_type(argname="argument contact_protocols", value=contact_protocols, expected_type=type_hints["contact_protocols"])
            check_type(argname="argument datapoints_to_alarm", value=datapoints_to_alarm, expected_type=type_hints["datapoints_to_alarm"])
            check_type(argname="argument evaluation_periods", value=evaluation_periods, expected_type=type_hints["evaluation_periods"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument monitored_resource_name", value=monitored_resource_name, expected_type=type_hints["monitored_resource_name"])
            check_type(argname="argument notification_enabled", value=notification_enabled, expected_type=type_hints["notification_enabled"])
            check_type(argname="argument notification_triggers", value=notification_triggers, expected_type=type_hints["notification_triggers"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument treat_missing_data", value=treat_missing_data, expected_type=type_hints["treat_missing_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_name is not None:
            self._values["alarm_name"] = alarm_name
        if comparison_operator is not None:
            self._values["comparison_operator"] = comparison_operator
        if contact_protocols is not None:
            self._values["contact_protocols"] = contact_protocols
        if datapoints_to_alarm is not None:
            self._values["datapoints_to_alarm"] = datapoints_to_alarm
        if evaluation_periods is not None:
            self._values["evaluation_periods"] = evaluation_periods
        if metric_name is not None:
            self._values["metric_name"] = metric_name
        if monitored_resource_name is not None:
            self._values["monitored_resource_name"] = monitored_resource_name
        if notification_enabled is not None:
            self._values["notification_enabled"] = notification_enabled
        if notification_triggers is not None:
            self._values["notification_triggers"] = notification_triggers
        if threshold is not None:
            self._values["threshold"] = threshold
        if treat_missing_data is not None:
            self._values["treat_missing_data"] = treat_missing_data

    @builtins.property
    def alarm_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-alarmname
        '''
        result = self._values.get("alarm_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comparison_operator(self) -> typing.Optional[builtins.str]:
        '''The arithmetic operation to use when comparing the specified statistic and threshold.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-comparisonoperator
        '''
        result = self._values.get("comparison_operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The contact protocols for the alarm, such as ``Email`` , ``SMS`` (text messaging), or both.

        *Allowed Values* : ``Email`` | ``SMS``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-contactprotocols
        '''
        result = self._values.get("contact_protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def datapoints_to_alarm(self) -> typing.Optional[jsii.Number]:
        '''The number of data points within the evaluation periods that must be breaching to cause the alarm to go to the ``ALARM`` state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-datapointstoalarm
        '''
        result = self._values.get("datapoints_to_alarm")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_periods(self) -> typing.Optional[jsii.Number]:
        '''The number of periods over which data is compared to the specified threshold.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-evaluationperiods
        '''
        result = self._values.get("evaluation_periods")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def metric_name(self) -> typing.Optional[builtins.str]:
        '''The name of the metric associated with the alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-metricname
        '''
        result = self._values.get("metric_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitored_resource_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Lightsail resource that the alarm monitors.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-monitoredresourcename
        '''
        result = self._values.get("monitored_resource_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether the alarm is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-notificationenabled
        '''
        result = self._values.get("notification_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def notification_triggers(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The alarm states that trigger a notification.

        .. epigraph::

           To specify the ``OK`` and ``INSUFFICIENT_DATA`` values, you must also specify ``ContactProtocols`` values. Otherwise, the ``OK`` and ``INSUFFICIENT_DATA`` values will not take effect and the stack will drift.

        *Allowed Values* : ``OK`` | ``ALARM`` | ``INSUFFICIENT_DATA``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-notificationtriggers
        '''
        result = self._values.get("notification_triggers")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def threshold(self) -> typing.Optional[jsii.Number]:
        '''The value against which the specified statistic is compared.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-threshold
        '''
        result = self._values.get("threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def treat_missing_data(self) -> typing.Optional[builtins.str]:
        '''Specifies how the alarm handles missing data points.

        An alarm can treat missing data in the following ways:

        - ``breaching`` - Assumes the missing data is not within the threshold. Missing data counts towards the number of times that the metric is not within the threshold.
        - ``notBreaching`` - Assumes the missing data is within the threshold. Missing data does not count towards the number of times that the metric is not within the threshold.
        - ``ignore`` - Ignores the missing data. Maintains the current alarm state.
        - ``missing`` - Missing data is treated as missing.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html#cfn-lightsail-alarm-treatmissingdata
        '''
        result = self._values.get("treat_missing_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAlarmPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnAlarmPropsMixin",
):
    '''The ``AWS::Lightsail::Alarm`` resource specifies an alarm that can be used to monitor a single metric for one of your Lightsail resources.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-alarm.html
    :cloudformationResource: AWS::Lightsail::Alarm
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_alarm_props_mixin = lightsail_mixins.CfnAlarmPropsMixin(lightsail_mixins.CfnAlarmMixinProps(
            alarm_name="alarmName",
            comparison_operator="comparisonOperator",
            contact_protocols=["contactProtocols"],
            datapoints_to_alarm=123,
            evaluation_periods=123,
            metric_name="metricName",
            monitored_resource_name="monitoredResourceName",
            notification_enabled=False,
            notification_triggers=["notificationTriggers"],
            threshold=123,
            treat_missing_data="treatMissingData"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAlarmMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Alarm``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b5aea57f2b8e0a452deb42ab445a8fa8a21440862e5a06a154ee5484db1ffe1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb36785a64e66b89161d8e034d6d74dbdb98cde0fb952e5f84c5efbc03e82a9e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5245735186592cfdccf663aab9bbf1a560f80ed7b6880b61beddba0ded04c0ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAlarmMixinProps:
        return typing.cast(CfnAlarmMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnBucketMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_rules": "accessRules",
        "bucket_name": "bucketName",
        "bundle_id": "bundleId",
        "object_versioning": "objectVersioning",
        "read_only_access_accounts": "readOnlyAccessAccounts",
        "resources_receiving_access": "resourcesReceivingAccess",
        "tags": "tags",
    },
)
class CfnBucketMixinProps:
    def __init__(
        self,
        *,
        access_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnBucketPropsMixin.AccessRulesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        object_versioning: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        read_only_access_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources_receiving_access: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnBucketPropsMixin.

        :param access_rules: An object that describes the access rules for the bucket.
        :param bucket_name: The name of the bucket.
        :param bundle_id: The bundle ID for the bucket (for example, ``small_1_0`` ). A bucket bundle specifies the monthly cost, storage space, and data transfer quota for a bucket.
        :param object_versioning: Indicates whether object versioning is enabled for the bucket. The following options can be configured: - ``Enabled`` - Object versioning is enabled. - ``Suspended`` - Object versioning was previously enabled but is currently suspended. Existing object versions are retained. - ``NeverEnabled`` - Object versioning has never been enabled.
        :param read_only_access_accounts: An array of AWS account IDs that have read-only access to the bucket.
        :param resources_receiving_access: An array of Lightsail instances that have access to the bucket.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_bucket_mixin_props = lightsail_mixins.CfnBucketMixinProps(
                access_rules=lightsail_mixins.CfnBucketPropsMixin.AccessRulesProperty(
                    allow_public_overrides=False,
                    object_access="objectAccess"
                ),
                bucket_name="bucketName",
                bundle_id="bundleId",
                object_versioning=False,
                read_only_access_accounts=["readOnlyAccessAccounts"],
                resources_receiving_access=["resourcesReceivingAccess"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6037093d3feff3d1f46e02491953c4102aac6a1590c80687fea9133784941caf)
            check_type(argname="argument access_rules", value=access_rules, expected_type=type_hints["access_rules"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument object_versioning", value=object_versioning, expected_type=type_hints["object_versioning"])
            check_type(argname="argument read_only_access_accounts", value=read_only_access_accounts, expected_type=type_hints["read_only_access_accounts"])
            check_type(argname="argument resources_receiving_access", value=resources_receiving_access, expected_type=type_hints["resources_receiving_access"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_rules is not None:
            self._values["access_rules"] = access_rules
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if object_versioning is not None:
            self._values["object_versioning"] = object_versioning
        if read_only_access_accounts is not None:
            self._values["read_only_access_accounts"] = read_only_access_accounts
        if resources_receiving_access is not None:
            self._values["resources_receiving_access"] = resources_receiving_access
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AccessRulesProperty"]]:
        '''An object that describes the access rules for the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-accessrules
        '''
        result = self._values.get("access_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnBucketPropsMixin.AccessRulesProperty"]], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-bucketname
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle ID for the bucket (for example, ``small_1_0`` ).

        A bucket bundle specifies the monthly cost, storage space, and data transfer quota for a bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_versioning(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether object versioning is enabled for the bucket.

        The following options can be configured:

        - ``Enabled`` - Object versioning is enabled.
        - ``Suspended`` - Object versioning was previously enabled but is currently suspended. Existing object versions are retained.
        - ``NeverEnabled`` - Object versioning has never been enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-objectversioning
        '''
        result = self._values.get("object_versioning")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def read_only_access_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of AWS account IDs that have read-only access to the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-readonlyaccessaccounts
        '''
        result = self._values.get("read_only_access_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources_receiving_access(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of Lightsail instances that have access to the bucket.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-resourcesreceivingaccess
        '''
        result = self._values.get("resources_receiving_access")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html#cfn-lightsail-bucket-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBucketMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnBucketPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnBucketPropsMixin",
):
    '''The ``AWS::Lightsail::Bucket`` resource specifies a bucket.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html
    :cloudformationResource: AWS::Lightsail::Bucket
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_bucket_props_mixin = lightsail_mixins.CfnBucketPropsMixin(lightsail_mixins.CfnBucketMixinProps(
            access_rules=lightsail_mixins.CfnBucketPropsMixin.AccessRulesProperty(
                allow_public_overrides=False,
                object_access="objectAccess"
            ),
            bucket_name="bucketName",
            bundle_id="bundleId",
            object_versioning=False,
            read_only_access_accounts=["readOnlyAccessAccounts"],
            resources_receiving_access=["resourcesReceivingAccess"],
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
        props: typing.Union[CfnBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Bucket``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c8cd239908826720d68c786f053b71ae338d823560ddb5e2793ae2501b046fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__810ac2b5750d84ddf471f519f65e30d743c84f12d5faa67527b7a115e8532273)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3a7ef5e30db690c22ee5c17b5bc5cf9cd0255860c492b1fb51ae690658c606c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnBucketMixinProps:
        return typing.cast(CfnBucketMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnBucketPropsMixin.AccessRulesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_public_overrides": "allowPublicOverrides",
            "object_access": "objectAccess",
        },
    )
    class AccessRulesProperty:
        def __init__(
            self,
            *,
            allow_public_overrides: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            object_access: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``AccessRules`` is a property of the `AWS::Lightsail::Bucket <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-bucket.html>`_ resource. It describes access rules for a bucket.

            :param allow_public_overrides: A Boolean value indicating whether the access control list (ACL) permissions that are applied to individual objects override the ``GetObject`` option that is currently specified. When this is true, you can use the `PutObjectAcl <https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectAcl.html>`_ Amazon S3 API operation to set individual objects to public (read-only) or private, using either the ``public-read`` ACL or the ``private`` ACL.
            :param object_access: Specifies the anonymous access to all objects in a bucket. The following options can be specified: - ``public`` - Sets all objects in the bucket to public (read-only), making them readable by everyone on the internet. If the ``GetObject`` value is set to ``public`` , then all objects in the bucket default to public regardless of the ``allowPublicOverrides`` value. - ``private`` - Sets all objects in the bucket to private, making them readable only by you and anyone that you grant access to. If the ``GetObject`` value is set to ``private`` , and the ``allowPublicOverrides`` value is set to ``true`` , then all objects in the bucket default to private unless they are configured with a ``public-read`` ACL. Individual objects with a ``public-read`` ACL are readable by everyone on the internet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-bucket-accessrules.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                access_rules_property = lightsail_mixins.CfnBucketPropsMixin.AccessRulesProperty(
                    allow_public_overrides=False,
                    object_access="objectAccess"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a96a94ca6dec170b7ef9bf06513c6d7e2ef08c364dfb69a7c1807a558dc39d2)
                check_type(argname="argument allow_public_overrides", value=allow_public_overrides, expected_type=type_hints["allow_public_overrides"])
                check_type(argname="argument object_access", value=object_access, expected_type=type_hints["object_access"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allow_public_overrides is not None:
                self._values["allow_public_overrides"] = allow_public_overrides
            if object_access is not None:
                self._values["object_access"] = object_access

        @builtins.property
        def allow_public_overrides(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether the access control list (ACL) permissions that are applied to individual objects override the ``GetObject`` option that is currently specified.

            When this is true, you can use the `PutObjectAcl <https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObjectAcl.html>`_ Amazon S3 API operation to set individual objects to public (read-only) or private, using either the ``public-read`` ACL or the ``private`` ACL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-bucket-accessrules.html#cfn-lightsail-bucket-accessrules-allowpublicoverrides
            '''
            result = self._values.get("allow_public_overrides")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def object_access(self) -> typing.Optional[builtins.str]:
            '''Specifies the anonymous access to all objects in a bucket.

            The following options can be specified:

            - ``public`` - Sets all objects in the bucket to public (read-only), making them readable by everyone on the internet.

            If the ``GetObject`` value is set to ``public`` , then all objects in the bucket default to public regardless of the ``allowPublicOverrides`` value.

            - ``private`` - Sets all objects in the bucket to private, making them readable only by you and anyone that you grant access to.

            If the ``GetObject`` value is set to ``private`` , and the ``allowPublicOverrides`` value is set to ``true`` , then all objects in the bucket default to private unless they are configured with a ``public-read`` ACL. Individual objects with a ``public-read`` ACL are readable by everyone on the internet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-bucket-accessrules.html#cfn-lightsail-bucket-accessrules-getobject
            '''
            result = self._values.get("object_access")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessRulesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_name": "certificateName",
        "domain_name": "domainName",
        "subject_alternative_names": "subjectAlternativeNames",
        "tags": "tags",
    },
)
class CfnCertificateMixinProps:
    def __init__(
        self,
        *,
        certificate_name: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCertificatePropsMixin.

        :param certificate_name: The name of the certificate.
        :param domain_name: The domain name of the certificate.
        :param subject_alternative_names: An array of strings that specify the alternate domains (such as ``example.org`` ) and subdomains (such as ``blog.example.com`` ) of the certificate.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_certificate_mixin_props = lightsail_mixins.CfnCertificateMixinProps(
                certificate_name="certificateName",
                domain_name="domainName",
                subject_alternative_names=["subjectAlternativeNames"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__498a48b3130aa8a805613a7f823eb500f0059e4312c6f314a666f9d99afafde1)
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name of the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html#cfn-lightsail-certificate-certificatename
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name of the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html#cfn-lightsail-certificate-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of strings that specify the alternate domains (such as ``example.org`` ) and subdomains (such as ``blog.example.com`` ) of the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html#cfn-lightsail-certificate-subjectalternativenames
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html#cfn-lightsail-certificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnCertificatePropsMixin",
):
    '''The ``AWS::Lightsail::Certificate`` resource specifies an SSL/TLS certificate that you can use with a content delivery network (CDN) distribution and a container service.

    .. epigraph::

       For information about certificates that you can use with a load balancer, see `AWS::Lightsail::LoadBalancerTlsCertificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html
    :cloudformationResource: AWS::Lightsail::Certificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_certificate_props_mixin = lightsail_mixins.CfnCertificatePropsMixin(lightsail_mixins.CfnCertificateMixinProps(
            certificate_name="certificateName",
            domain_name="domainName",
            subject_alternative_names=["subjectAlternativeNames"],
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
        props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Certificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70f751dc8447b965a1016d2fd16a8f7e854a5cb09e3f86579a3b96ecd3f3ef2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cb4c0ad3444da416a5f62498f418c8c36d2450f2a279f7629b9f87b860f1a06)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f92bc2ecb146c7f32d4d198e76d3ffcc7cc4d67e0583c3e5b5959d79b44f95d5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCertificateMixinProps:
        return typing.cast(CfnCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_service_deployment": "containerServiceDeployment",
        "is_disabled": "isDisabled",
        "power": "power",
        "private_registry_access": "privateRegistryAccess",
        "public_domain_names": "publicDomainNames",
        "scale": "scale",
        "service_name": "serviceName",
        "tags": "tags",
    },
)
class CfnContainerMixinProps:
    def __init__(
        self,
        *,
        container_service_deployment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.ContainerServiceDeploymentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        is_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        power: typing.Optional[builtins.str] = None,
        private_registry_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.PrivateRegistryAccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        public_domain_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.PublicDomainNameProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        scale: typing.Optional[jsii.Number] = None,
        service_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnContainerPropsMixin.

        :param container_service_deployment: An object that describes the current container deployment of the container service.
        :param is_disabled: A Boolean value indicating whether the container service is disabled.
        :param power: The power specification of the container service. The power specifies the amount of RAM, the number of vCPUs, and the base price of the container service.
        :param private_registry_access: An object that describes the configuration for the container service to access private container image repositories, such as ( Amazon ECR ) private repositories. For more information, see `Configuring access to an Amazon ECR private repository for an Amazon Lightsail container service <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-container-service-ecr-private-repo-access>`_ in the *Amazon Lightsail Developer Guide* .
        :param public_domain_names: The public domain name of the container service, such as ``example.com`` and ``www.example.com`` . You can specify up to four public domain names for a container service. The domain names that you specify are used when you create a deployment with a container that is configured as the public endpoint of your container service. If you don't specify public domain names, then you can use the default domain of the container service. .. epigraph:: You must create and validate an SSL/TLS certificate before you can use public domain names with your container service. Use the `AWS::Lightsail::Certificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html>`_ resource to create a certificate for the public domain names that you want to use with your container service.
        :param scale: The scale specification of the container service. The scale specifies the allocated compute nodes of the container service.
        :param service_name: The name of the container service.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_container_mixin_props = lightsail_mixins.CfnContainerMixinProps(
                container_service_deployment=lightsail_mixins.CfnContainerPropsMixin.ContainerServiceDeploymentProperty(
                    containers=[lightsail_mixins.CfnContainerPropsMixin.ContainerProperty(
                        command=["command"],
                        container_name="containerName",
                        environment=[lightsail_mixins.CfnContainerPropsMixin.EnvironmentVariableProperty(
                            value="value",
                            variable="variable"
                        )],
                        image="image",
                        ports=[lightsail_mixins.CfnContainerPropsMixin.PortInfoProperty(
                            port="port",
                            protocol="protocol"
                        )]
                    )],
                    public_endpoint=lightsail_mixins.CfnContainerPropsMixin.PublicEndpointProperty(
                        container_name="containerName",
                        container_port=123,
                        health_check_config=lightsail_mixins.CfnContainerPropsMixin.HealthCheckConfigProperty(
                            healthy_threshold=123,
                            interval_seconds=123,
                            path="path",
                            success_codes="successCodes",
                            timeout_seconds=123,
                            unhealthy_threshold=123
                        )
                    )
                ),
                is_disabled=False,
                power="power",
                private_registry_access=lightsail_mixins.CfnContainerPropsMixin.PrivateRegistryAccessProperty(
                    ecr_image_puller_role=lightsail_mixins.CfnContainerPropsMixin.EcrImagePullerRoleProperty(
                        is_active=False,
                        principal_arn="principalArn"
                    )
                ),
                public_domain_names=[lightsail_mixins.CfnContainerPropsMixin.PublicDomainNameProperty(
                    certificate_name="certificateName",
                    domain_names=["domainNames"]
                )],
                scale=123,
                service_name="serviceName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13edaaaf210c53bbed4b243d01f049502134f0e13dff47f72b69a274e29fb1ac)
            check_type(argname="argument container_service_deployment", value=container_service_deployment, expected_type=type_hints["container_service_deployment"])
            check_type(argname="argument is_disabled", value=is_disabled, expected_type=type_hints["is_disabled"])
            check_type(argname="argument power", value=power, expected_type=type_hints["power"])
            check_type(argname="argument private_registry_access", value=private_registry_access, expected_type=type_hints["private_registry_access"])
            check_type(argname="argument public_domain_names", value=public_domain_names, expected_type=type_hints["public_domain_names"])
            check_type(argname="argument scale", value=scale, expected_type=type_hints["scale"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_service_deployment is not None:
            self._values["container_service_deployment"] = container_service_deployment
        if is_disabled is not None:
            self._values["is_disabled"] = is_disabled
        if power is not None:
            self._values["power"] = power
        if private_registry_access is not None:
            self._values["private_registry_access"] = private_registry_access
        if public_domain_names is not None:
            self._values["public_domain_names"] = public_domain_names
        if scale is not None:
            self._values["scale"] = scale
        if service_name is not None:
            self._values["service_name"] = service_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def container_service_deployment(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.ContainerServiceDeploymentProperty"]]:
        '''An object that describes the current container deployment of the container service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-containerservicedeployment
        '''
        result = self._values.get("container_service_deployment")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.ContainerServiceDeploymentProperty"]], result)

    @builtins.property
    def is_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether the container service is disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-isdisabled
        '''
        result = self._values.get("is_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def power(self) -> typing.Optional[builtins.str]:
        '''The power specification of the container service.

        The power specifies the amount of RAM, the number of vCPUs, and the base price of the container service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-power
        '''
        result = self._values.get("power")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_registry_access(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PrivateRegistryAccessProperty"]]:
        '''An object that describes the configuration for the container service to access private container image repositories, such as  ( Amazon ECR ) private repositories.

        For more information, see `Configuring access to an Amazon ECR private repository for an Amazon Lightsail container service <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-container-service-ecr-private-repo-access>`_ in the *Amazon Lightsail Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-privateregistryaccess
        '''
        result = self._values.get("private_registry_access")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PrivateRegistryAccessProperty"]], result)

    @builtins.property
    def public_domain_names(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PublicDomainNameProperty"]]]]:
        '''The public domain name of the container service, such as ``example.com`` and ``www.example.com`` .

        You can specify up to four public domain names for a container service. The domain names that you specify are used when you create a deployment with a container that is configured as the public endpoint of your container service.

        If you don't specify public domain names, then you can use the default domain of the container service.
        .. epigraph::

           You must create and validate an SSL/TLS certificate before you can use public domain names with your container service. Use the `AWS::Lightsail::Certificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-certificate.html>`_ resource to create a certificate for the public domain names that you want to use with your container service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-publicdomainnames
        '''
        result = self._values.get("public_domain_names")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PublicDomainNameProperty"]]]], result)

    @builtins.property
    def scale(self) -> typing.Optional[jsii.Number]:
        '''The scale specification of the container service.

        The scale specifies the allocated compute nodes of the container service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-scale
        '''
        result = self._values.get("scale")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''The name of the container service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-servicename
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html#cfn-lightsail-container-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContainerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContainerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin",
):
    '''The ``AWS::Lightsail::Container`` resource specifies a container service.

    A Lightsail container service is a compute resource to which you can deploy containers.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html
    :cloudformationResource: AWS::Lightsail::Container
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_container_props_mixin = lightsail_mixins.CfnContainerPropsMixin(lightsail_mixins.CfnContainerMixinProps(
            container_service_deployment=lightsail_mixins.CfnContainerPropsMixin.ContainerServiceDeploymentProperty(
                containers=[lightsail_mixins.CfnContainerPropsMixin.ContainerProperty(
                    command=["command"],
                    container_name="containerName",
                    environment=[lightsail_mixins.CfnContainerPropsMixin.EnvironmentVariableProperty(
                        value="value",
                        variable="variable"
                    )],
                    image="image",
                    ports=[lightsail_mixins.CfnContainerPropsMixin.PortInfoProperty(
                        port="port",
                        protocol="protocol"
                    )]
                )],
                public_endpoint=lightsail_mixins.CfnContainerPropsMixin.PublicEndpointProperty(
                    container_name="containerName",
                    container_port=123,
                    health_check_config=lightsail_mixins.CfnContainerPropsMixin.HealthCheckConfigProperty(
                        healthy_threshold=123,
                        interval_seconds=123,
                        path="path",
                        success_codes="successCodes",
                        timeout_seconds=123,
                        unhealthy_threshold=123
                    )
                )
            ),
            is_disabled=False,
            power="power",
            private_registry_access=lightsail_mixins.CfnContainerPropsMixin.PrivateRegistryAccessProperty(
                ecr_image_puller_role=lightsail_mixins.CfnContainerPropsMixin.EcrImagePullerRoleProperty(
                    is_active=False,
                    principal_arn="principalArn"
                )
            ),
            public_domain_names=[lightsail_mixins.CfnContainerPropsMixin.PublicDomainNameProperty(
                certificate_name="certificateName",
                domain_names=["domainNames"]
            )],
            scale=123,
            service_name="serviceName",
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
        props: typing.Union[CfnContainerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Container``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57474a8e564273737b3a61b9c16c5ee028f8abae9743cde4dee403e3f8921415)
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
            type_hints = typing.get_type_hints(_typecheckingstub__264652ffb4c9dc2800b82c6ada55ca8d4e21e95bfa87e9f42f8225c0dc95dfbb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7cf33e897dd9ec3919d056148139445769726f7a6ead86d9f94e51163783667)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContainerMixinProps:
        return typing.cast(CfnContainerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.ContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "command": "command",
            "container_name": "containerName",
            "environment": "environment",
            "image": "image",
            "ports": "ports",
        },
    )
    class ContainerProperty:
        def __init__(
            self,
            *,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            container_name: typing.Optional[builtins.str] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image: typing.Optional[builtins.str] = None,
            ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.PortInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``Container`` is a property of the `ContainerServiceDeployment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-containerservicedeployment.html>`_ property. It describes the settings of a container that will be launched, or that is launched, to an Amazon Lightsail container service.

            :param command: The launch command for the container.
            :param container_name: The name of the container.
            :param environment: The environment variables of the container.
            :param image: The name of the image used for the container. Container images that are sourced from (registered and stored on) your container service start with a colon ( ``:`` ). For example, if your container service name is ``container-service-1`` , the container image label is ``mystaticsite`` , and you want to use the third version ( ``3`` ) of the registered container image, then you should specify ``:container-service-1.mystaticsite.3`` . To use the latest version of a container image, specify ``latest`` instead of a version number (for example, ``:container-service-1.mystaticsite.latest`` ). Your container service will automatically use the highest numbered version of the registered container image. Container images that are sourced from a public registry like Docker Hub don’t start with a colon. For example, ``nginx:latest`` or ``nginx`` .
            :param ports: An object that describes the open firewall ports and protocols of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                container_property = lightsail_mixins.CfnContainerPropsMixin.ContainerProperty(
                    command=["command"],
                    container_name="containerName",
                    environment=[lightsail_mixins.CfnContainerPropsMixin.EnvironmentVariableProperty(
                        value="value",
                        variable="variable"
                    )],
                    image="image",
                    ports=[lightsail_mixins.CfnContainerPropsMixin.PortInfoProperty(
                        port="port",
                        protocol="protocol"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ebbfcf054baa169fea214bda4e73fbbde264e9e6f5f76bb1034efabc8caffb4b)
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if command is not None:
                self._values["command"] = command
            if container_name is not None:
                self._values["container_name"] = container_name
            if environment is not None:
                self._values["environment"] = environment
            if image is not None:
                self._values["image"] = image
            if ports is not None:
                self._values["ports"] = ports

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The launch command for the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html#cfn-lightsail-container-container-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def container_name(self) -> typing.Optional[builtins.str]:
            '''The name of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html#cfn-lightsail-container-container-containername
            '''
            result = self._values.get("container_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.EnvironmentVariableProperty"]]]]:
            '''The environment variables of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html#cfn-lightsail-container-container-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.EnvironmentVariableProperty"]]]], result)

        @builtins.property
        def image(self) -> typing.Optional[builtins.str]:
            '''The name of the image used for the container.

            Container images that are sourced from (registered and stored on) your container service start with a colon ( ``:`` ). For example, if your container service name is ``container-service-1`` , the container image label is ``mystaticsite`` , and you want to use the third version ( ``3`` ) of the registered container image, then you should specify ``:container-service-1.mystaticsite.3`` . To use the latest version of a container image, specify ``latest`` instead of a version number (for example, ``:container-service-1.mystaticsite.latest`` ). Your container service will automatically use the highest numbered version of the registered container image.

            Container images that are sourced from a public registry like Docker Hub don’t start with a colon. For example, ``nginx:latest`` or ``nginx`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html#cfn-lightsail-container-container-image
            '''
            result = self._values.get("image")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PortInfoProperty"]]]]:
            '''An object that describes the open firewall ports and protocols of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html#cfn-lightsail-container-container-ports
            '''
            result = self._values.get("ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PortInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.ContainerServiceDeploymentProperty",
        jsii_struct_bases=[],
        name_mapping={"containers": "containers", "public_endpoint": "publicEndpoint"},
    )
    class ContainerServiceDeploymentProperty:
        def __init__(
            self,
            *,
            containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.ContainerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            public_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.PublicEndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``ContainerServiceDeployment`` is a property of the `AWS::Lightsail::Container <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html>`_ resource. It describes a container deployment configuration of a container service.

            A deployment specifies the settings, such as the ports and launch command, of containers that are deployed to your container service.

            :param containers: An object that describes the configuration for the containers of the deployment.
            :param public_endpoint: An object that describes the endpoint of the deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-containerservicedeployment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                container_service_deployment_property = lightsail_mixins.CfnContainerPropsMixin.ContainerServiceDeploymentProperty(
                    containers=[lightsail_mixins.CfnContainerPropsMixin.ContainerProperty(
                        command=["command"],
                        container_name="containerName",
                        environment=[lightsail_mixins.CfnContainerPropsMixin.EnvironmentVariableProperty(
                            value="value",
                            variable="variable"
                        )],
                        image="image",
                        ports=[lightsail_mixins.CfnContainerPropsMixin.PortInfoProperty(
                            port="port",
                            protocol="protocol"
                        )]
                    )],
                    public_endpoint=lightsail_mixins.CfnContainerPropsMixin.PublicEndpointProperty(
                        container_name="containerName",
                        container_port=123,
                        health_check_config=lightsail_mixins.CfnContainerPropsMixin.HealthCheckConfigProperty(
                            healthy_threshold=123,
                            interval_seconds=123,
                            path="path",
                            success_codes="successCodes",
                            timeout_seconds=123,
                            unhealthy_threshold=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51b4191d87caf9ee3be130e5dfc7f5da1a08138a1350ca23e5e9759a6f8a221f)
                check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                check_type(argname="argument public_endpoint", value=public_endpoint, expected_type=type_hints["public_endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if containers is not None:
                self._values["containers"] = containers
            if public_endpoint is not None:
                self._values["public_endpoint"] = public_endpoint

        @builtins.property
        def containers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.ContainerProperty"]]]]:
            '''An object that describes the configuration for the containers of the deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-containerservicedeployment.html#cfn-lightsail-container-containerservicedeployment-containers
            '''
            result = self._values.get("containers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.ContainerProperty"]]]], result)

        @builtins.property
        def public_endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PublicEndpointProperty"]]:
            '''An object that describes the endpoint of the deployment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-containerservicedeployment.html#cfn-lightsail-container-containerservicedeployment-publicendpoint
            '''
            result = self._values.get("public_endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.PublicEndpointProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerServiceDeploymentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.EcrImagePullerRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"is_active": "isActive", "principal_arn": "principalArn"},
    )
    class EcrImagePullerRoleProperty:
        def __init__(
            self,
            *,
            is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            principal_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the IAM role that you can use to grant a Lightsail container service access to Amazon ECR private repositories.

            :param is_active: A boolean value that indicates whether the ``ECRImagePullerRole`` is active.
            :param principal_arn: The principle Amazon Resource Name (ARN) of the role. This property is read-only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-ecrimagepullerrole.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                ecr_image_puller_role_property = lightsail_mixins.CfnContainerPropsMixin.EcrImagePullerRoleProperty(
                    is_active=False,
                    principal_arn="principalArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40f785495f02afe1d663a4c0a886b893d75ba51b78a5ba1c46120cd9f3cc7eae)
                check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
                check_type(argname="argument principal_arn", value=principal_arn, expected_type=type_hints["principal_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if is_active is not None:
                self._values["is_active"] = is_active
            if principal_arn is not None:
                self._values["principal_arn"] = principal_arn

        @builtins.property
        def is_active(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean value that indicates whether the ``ECRImagePullerRole`` is active.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-ecrimagepullerrole.html#cfn-lightsail-container-ecrimagepullerrole-isactive
            '''
            result = self._values.get("is_active")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def principal_arn(self) -> typing.Optional[builtins.str]:
            '''The principle Amazon Resource Name (ARN) of the role.

            This property is read-only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-ecrimagepullerrole.html#cfn-lightsail-container-ecrimagepullerrole-principalarn
            '''
            result = self._values.get("principal_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcrImagePullerRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "variable": "variable"},
    )
    class EnvironmentVariableProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[builtins.str] = None,
            variable: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``EnvironmentVariable`` is a property of the `Container <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html>`_ property. It describes the environment variables of a container on a container service which are key-value parameters that provide dynamic configuration of the application or script run by the container.

            :param value: The environment variable value.
            :param variable: The environment variable key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                environment_variable_property = lightsail_mixins.CfnContainerPropsMixin.EnvironmentVariableProperty(
                    value="value",
                    variable="variable"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9978e5514bf1e3933e60f87bc096abaec946bb34d03d63763ef667b3941ed115)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if variable is not None:
                self._values["variable"] = variable

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The environment variable value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-environmentvariable.html#cfn-lightsail-container-environmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variable(self) -> typing.Optional[builtins.str]:
            '''The environment variable key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-environmentvariable.html#cfn-lightsail-container-environmentvariable-variable
            '''
            result = self._values.get("variable")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "healthy_threshold": "healthyThreshold",
            "interval_seconds": "intervalSeconds",
            "path": "path",
            "success_codes": "successCodes",
            "timeout_seconds": "timeoutSeconds",
            "unhealthy_threshold": "unhealthyThreshold",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            healthy_threshold: typing.Optional[jsii.Number] = None,
            interval_seconds: typing.Optional[jsii.Number] = None,
            path: typing.Optional[builtins.str] = None,
            success_codes: typing.Optional[builtins.str] = None,
            timeout_seconds: typing.Optional[jsii.Number] = None,
            unhealthy_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``HealthCheckConfig`` is a property of the `PublicEndpoint <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicendpoint.html>`_ property. It describes the healthcheck configuration of a container deployment on a container service.

            :param healthy_threshold: The number of consecutive health check successes required before moving the container to the ``Healthy`` state. The default value is ``2`` .
            :param interval_seconds: The approximate interval, in seconds, between health checks of an individual container. You can specify between ``5`` and ``300`` seconds. The default value is ``5`` .
            :param path: The path on the container on which to perform the health check. The default value is ``/`` .
            :param success_codes: The HTTP codes to use when checking for a successful response from a container. You can specify values between ``200`` and ``499`` . You can specify multiple values (for example, ``200,202`` ) or a range of values (for example, ``200-299`` ).
            :param timeout_seconds: The amount of time, in seconds, during which no response means a failed health check. You can specify between ``2`` and ``60`` seconds. The default value is ``2`` .
            :param unhealthy_threshold: The number of consecutive health check failures required before moving the container to the ``Unhealthy`` state. The default value is ``2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                health_check_config_property = lightsail_mixins.CfnContainerPropsMixin.HealthCheckConfigProperty(
                    healthy_threshold=123,
                    interval_seconds=123,
                    path="path",
                    success_codes="successCodes",
                    timeout_seconds=123,
                    unhealthy_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25e614ac6ec6a7ac1cce3f21e5db31769a9235eb7ab19e998c2cba5770795762)
                check_type(argname="argument healthy_threshold", value=healthy_threshold, expected_type=type_hints["healthy_threshold"])
                check_type(argname="argument interval_seconds", value=interval_seconds, expected_type=type_hints["interval_seconds"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument success_codes", value=success_codes, expected_type=type_hints["success_codes"])
                check_type(argname="argument timeout_seconds", value=timeout_seconds, expected_type=type_hints["timeout_seconds"])
                check_type(argname="argument unhealthy_threshold", value=unhealthy_threshold, expected_type=type_hints["unhealthy_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if healthy_threshold is not None:
                self._values["healthy_threshold"] = healthy_threshold
            if interval_seconds is not None:
                self._values["interval_seconds"] = interval_seconds
            if path is not None:
                self._values["path"] = path
            if success_codes is not None:
                self._values["success_codes"] = success_codes
            if timeout_seconds is not None:
                self._values["timeout_seconds"] = timeout_seconds
            if unhealthy_threshold is not None:
                self._values["unhealthy_threshold"] = unhealthy_threshold

        @builtins.property
        def healthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive health check successes required before moving the container to the ``Healthy`` state.

            The default value is ``2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html#cfn-lightsail-container-healthcheckconfig-healthythreshold
            '''
            result = self._values.get("healthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The approximate interval, in seconds, between health checks of an individual container.

            You can specify between ``5`` and ``300`` seconds. The default value is ``5`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html#cfn-lightsail-container-healthcheckconfig-intervalseconds
            '''
            result = self._values.get("interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path on the container on which to perform the health check.

            The default value is ``/`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html#cfn-lightsail-container-healthcheckconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def success_codes(self) -> typing.Optional[builtins.str]:
            '''The HTTP codes to use when checking for a successful response from a container.

            You can specify values between ``200`` and ``499`` . You can specify multiple values (for example, ``200,202`` ) or a range of values (for example, ``200-299`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html#cfn-lightsail-container-healthcheckconfig-successcodes
            '''
            result = self._values.get("success_codes")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, during which no response means a failed health check.

            You can specify between ``2`` and ``60`` seconds. The default value is ``2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html#cfn-lightsail-container-healthcheckconfig-timeoutseconds
            '''
            result = self._values.get("timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unhealthy_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive health check failures required before moving the container to the ``Unhealthy`` state.

            The default value is ``2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-healthcheckconfig.html#cfn-lightsail-container-healthcheckconfig-unhealthythreshold
            '''
            result = self._values.get("unhealthy_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.PortInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"port": "port", "protocol": "protocol"},
    )
    class PortInfoProperty:
        def __init__(
            self,
            *,
            port: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``PortInfo`` is a property of the `Container <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-container.html>`_ property. It describes the ports to open and the protocols to use for a container on a Amazon Lightsail container service.

            :param port: The open firewall ports of the container.
            :param protocol: The protocol name for the open ports. *Allowed values* : ``HTTP`` | ``HTTPS`` | ``TCP`` | ``UDP``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-portinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                port_info_property = lightsail_mixins.CfnContainerPropsMixin.PortInfoProperty(
                    port="port",
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db5a77030ca196ec96ac9703babc465270b04f30afb7c43d641d3db1e4a27684)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The open firewall ports of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-portinfo.html#cfn-lightsail-container-portinfo-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol name for the open ports.

            *Allowed values* : ``HTTP`` | ``HTTPS`` | ``TCP`` | ``UDP``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-portinfo.html#cfn-lightsail-container-portinfo-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.PrivateRegistryAccessProperty",
        jsii_struct_bases=[],
        name_mapping={"ecr_image_puller_role": "ecrImagePullerRole"},
    )
    class PrivateRegistryAccessProperty:
        def __init__(
            self,
            *,
            ecr_image_puller_role: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.EcrImagePullerRoleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the configuration for an Amazon Lightsail container service to access private container image repositories, such as  ( Amazon ECR ) private repositories.

            For more information, see `Configuring access to an Amazon ECR private repository for an Amazon Lightsail container service <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-container-service-ecr-private-repo-access>`_ in the *Amazon Lightsail Developer Guide* .

            :param ecr_image_puller_role: An object that describes the activation status of the role that you can use to grant a Lightsail container service access to Amazon ECR private repositories. If the role is activated, the Amazon Resource Name (ARN) of the role is also listed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-privateregistryaccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                private_registry_access_property = lightsail_mixins.CfnContainerPropsMixin.PrivateRegistryAccessProperty(
                    ecr_image_puller_role=lightsail_mixins.CfnContainerPropsMixin.EcrImagePullerRoleProperty(
                        is_active=False,
                        principal_arn="principalArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0bd87e5f5cbd1a76dbd3820214b2c7213ce29c695088c6336741ddc21a101668)
                check_type(argname="argument ecr_image_puller_role", value=ecr_image_puller_role, expected_type=type_hints["ecr_image_puller_role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ecr_image_puller_role is not None:
                self._values["ecr_image_puller_role"] = ecr_image_puller_role

        @builtins.property
        def ecr_image_puller_role(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.EcrImagePullerRoleProperty"]]:
            '''An object that describes the activation status of the role that you can use to grant a Lightsail container service access to Amazon ECR private repositories.

            If the role is activated, the Amazon Resource Name (ARN) of the role is also listed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-privateregistryaccess.html#cfn-lightsail-container-privateregistryaccess-ecrimagepullerrole
            '''
            result = self._values.get("ecr_image_puller_role")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.EcrImagePullerRoleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateRegistryAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.PublicDomainNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_name": "certificateName",
            "domain_names": "domainNames",
        },
    )
    class PublicDomainNameProperty:
        def __init__(
            self,
            *,
            certificate_name: typing.Optional[builtins.str] = None,
            domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''``PublicDomainName`` is a property of the `AWS::Lightsail::Container <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-container.html>`_ resource. It describes the public domain names to use with a container service, such as ``example.com`` and ``www.example.com`` . It also describes the certificates to use with a container service.

            :param certificate_name: The name of the certificate for the public domains.
            :param domain_names: The public domain names to use with the container service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicdomainname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                public_domain_name_property = lightsail_mixins.CfnContainerPropsMixin.PublicDomainNameProperty(
                    certificate_name="certificateName",
                    domain_names=["domainNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a55b29f0e2cf8bbedd1c224bb7b0d2ca3d7f21c917571466e522f1dffd3480cb)
                check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
                check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_name is not None:
                self._values["certificate_name"] = certificate_name
            if domain_names is not None:
                self._values["domain_names"] = domain_names

        @builtins.property
        def certificate_name(self) -> typing.Optional[builtins.str]:
            '''The name of the certificate for the public domains.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicdomainname.html#cfn-lightsail-container-publicdomainname-certificatename
            '''
            result = self._values.get("certificate_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The public domain names to use with the container service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicdomainname.html#cfn-lightsail-container-publicdomainname-domainnames
            '''
            result = self._values.get("domain_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicDomainNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnContainerPropsMixin.PublicEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_name": "containerName",
            "container_port": "containerPort",
            "health_check_config": "healthCheckConfig",
        },
    )
    class PublicEndpointProperty:
        def __init__(
            self,
            *,
            container_name: typing.Optional[builtins.str] = None,
            container_port: typing.Optional[jsii.Number] = None,
            health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContainerPropsMixin.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''``PublicEndpoint`` is a property of the `ContainerServiceDeployment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-containerservicedeployment.html>`_ property. It describes describes the settings of the public endpoint of a container on a container service.

            :param container_name: The name of the container entry of the deployment that the endpoint configuration applies to.
            :param container_port: The port of the specified container to which traffic is forwarded to.
            :param health_check_config: An object that describes the health check configuration of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                public_endpoint_property = lightsail_mixins.CfnContainerPropsMixin.PublicEndpointProperty(
                    container_name="containerName",
                    container_port=123,
                    health_check_config=lightsail_mixins.CfnContainerPropsMixin.HealthCheckConfigProperty(
                        healthy_threshold=123,
                        interval_seconds=123,
                        path="path",
                        success_codes="successCodes",
                        timeout_seconds=123,
                        unhealthy_threshold=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__051e98bf0218deae0f209b4a93e2e9c3592524510a1e9e96081974311c7cb125)
                check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
                check_type(argname="argument container_port", value=container_port, expected_type=type_hints["container_port"])
                check_type(argname="argument health_check_config", value=health_check_config, expected_type=type_hints["health_check_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_name is not None:
                self._values["container_name"] = container_name
            if container_port is not None:
                self._values["container_port"] = container_port
            if health_check_config is not None:
                self._values["health_check_config"] = health_check_config

        @builtins.property
        def container_name(self) -> typing.Optional[builtins.str]:
            '''The name of the container entry of the deployment that the endpoint configuration applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicendpoint.html#cfn-lightsail-container-publicendpoint-containername
            '''
            result = self._values.get("container_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def container_port(self) -> typing.Optional[jsii.Number]:
            '''The port of the specified container to which traffic is forwarded to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicendpoint.html#cfn-lightsail-container-publicendpoint-containerport
            '''
            result = self._values.get("container_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def health_check_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.HealthCheckConfigProperty"]]:
            '''An object that describes the health check configuration of the container.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-container-publicendpoint.html#cfn-lightsail-container-publicendpoint-healthcheckconfig
            '''
            result = self._values.get("health_check_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContainerPropsMixin.HealthCheckConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDatabaseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "ca_certificate_identifier": "caCertificateIdentifier",
        "master_database_name": "masterDatabaseName",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "relational_database_blueprint_id": "relationalDatabaseBlueprintId",
        "relational_database_bundle_id": "relationalDatabaseBundleId",
        "relational_database_name": "relationalDatabaseName",
        "relational_database_parameters": "relationalDatabaseParameters",
        "rotate_master_user_password": "rotateMasterUserPassword",
        "tags": "tags",
    },
)
class CfnDatabaseMixinProps:
    def __init__(
        self,
        *,
        availability_zone: typing.Optional[builtins.str] = None,
        backup_retention: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ca_certificate_identifier: typing.Optional[builtins.str] = None,
        master_database_name: typing.Optional[builtins.str] = None,
        master_username: typing.Optional[builtins.str] = None,
        master_user_password: typing.Optional[builtins.str] = None,
        preferred_backup_window: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        relational_database_blueprint_id: typing.Optional[builtins.str] = None,
        relational_database_bundle_id: typing.Optional[builtins.str] = None,
        relational_database_name: typing.Optional[builtins.str] = None,
        relational_database_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatabasePropsMixin.RelationalDatabaseParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        rotate_master_user_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatabasePropsMixin.

        :param availability_zone: The Availability Zone for the database.
        :param backup_retention: A Boolean value indicating whether automated backup retention is enabled for the database. Data Import Mode is enabled when ``BackupRetention`` is set to ``false`` , and is disabled when ``BackupRetention`` is set to ``true`` .
        :param ca_certificate_identifier: The certificate associated with the database.
        :param master_database_name: The meaning of this parameter differs according to the database engine you use. *MySQL* The name of the database to create when the Lightsail database resource is created. If this parameter isn't specified, no database is created in the database resource. Constraints: - Must contain 1-64 letters or numbers. - Must begin with a letter. Subsequent characters can be letters, underscores, or numbers (0-9). - Can't be a word reserved by the specified database engine. For more information about reserved words in MySQL, see the Keywords and Reserved Words articles for `MySQL 5.6 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.6/en/keywords.html>`_ , `MySQL 5.7 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.7/en/keywords.html>`_ , and `MySQL 8.0 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/8.0/en/keywords.html>`_ . *PostgreSQL* The name of the database to create when the Lightsail database resource is created. If this parameter isn't specified, a database named ``postgres`` is created in the database resource. Constraints: - Must contain 1-63 letters or numbers. - Must begin with a letter. Subsequent characters can be letters, underscores, or numbers (0-9). - Can't be a word reserved by the specified database engine. For more information about reserved words in PostgreSQL, see the SQL Key Words articles for `PostgreSQL 9.6 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/9.6/sql-keywords-appendix.html>`_ , `PostgreSQL 10 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/10/sql-keywords-appendix.html>`_ , `PostgreSQL 11 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/11/sql-keywords-appendix.html>`_ , and `PostgreSQL 12 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/12/sql-keywords-appendix.html>`_ .
        :param master_username: The name for the primary user. *MySQL* Constraints: - Required for MySQL. - Must be 1-16 letters or numbers. Can contain underscores. - First character must be a letter. - Can't be a reserved word for the chosen database engine. For more information about reserved words in MySQL 5.6 or 5.7, see the Keywords and Reserved Words articles for `MySQL 5.6 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.6/en/keywords.html>`_ , `MySQL 5.7 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.7/en/keywords.html>`_ , or `MySQL 8.0 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/8.0/en/keywords.html>`_ . *PostgreSQL* Constraints: - Required for PostgreSQL. - Must be 1-63 letters or numbers. Can contain underscores. - First character must be a letter. - Can't be a reserved word for the chosen database engine. For more information about reserved words in MySQL 5.6 or 5.7, see the Keywords and Reserved Words articles for `PostgreSQL 9.6 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/9.6/sql-keywords-appendix.html>`_ , `PostgreSQL 10 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/10/sql-keywords-appendix.html>`_ , `PostgreSQL 11 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/11/sql-keywords-appendix.html>`_ , and `PostgreSQL 12 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/12/sql-keywords-appendix.html>`_ .
        :param master_user_password: The password for the primary user of the database. The password can include any printable ASCII character except the following: /, ", or
        :param preferred_backup_window: The daily time range during which automated backups are created for the database (for example, ``16:00-16:30`` ).
        :param preferred_maintenance_window: The weekly time range during which system maintenance can occur for the database, formatted as follows: ``ddd:hh24:mi-ddd:hh24:mi`` . For example, ``Tue:17:00-Tue:17:30`` .
        :param publicly_accessible: A Boolean value indicating whether the database is accessible to anyone on the internet.
        :param relational_database_blueprint_id: The blueprint ID for the database (for example, ``mysql_8_0`` ).
        :param relational_database_bundle_id: The bundle ID for the database (for example, ``medium_1_0`` ).
        :param relational_database_name: The name of the instance.
        :param relational_database_parameters: An array of parameters for the database.
        :param rotate_master_user_password: A Boolean value indicating whether to change the primary user password to a new, strong password generated by Lightsail . .. epigraph:: The ``RotateMasterUserPassword`` and ``MasterUserPassword`` parameters cannot be used together in the same template.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_database_mixin_props = lightsail_mixins.CfnDatabaseMixinProps(
                availability_zone="availabilityZone",
                backup_retention=False,
                ca_certificate_identifier="caCertificateIdentifier",
                master_database_name="masterDatabaseName",
                master_username="masterUsername",
                master_user_password="masterUserPassword",
                preferred_backup_window="preferredBackupWindow",
                preferred_maintenance_window="preferredMaintenanceWindow",
                publicly_accessible=False,
                relational_database_blueprint_id="relationalDatabaseBlueprintId",
                relational_database_bundle_id="relationalDatabaseBundleId",
                relational_database_name="relationalDatabaseName",
                relational_database_parameters=[lightsail_mixins.CfnDatabasePropsMixin.RelationalDatabaseParameterProperty(
                    allowed_values="allowedValues",
                    apply_method="applyMethod",
                    apply_type="applyType",
                    data_type="dataType",
                    description="description",
                    is_modifiable=False,
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )],
                rotate_master_user_password=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b89ca13cd483b28dcc119e3026114071882c1f8d2dd34afa9dfcc1d1758050cc)
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument backup_retention", value=backup_retention, expected_type=type_hints["backup_retention"])
            check_type(argname="argument ca_certificate_identifier", value=ca_certificate_identifier, expected_type=type_hints["ca_certificate_identifier"])
            check_type(argname="argument master_database_name", value=master_database_name, expected_type=type_hints["master_database_name"])
            check_type(argname="argument master_username", value=master_username, expected_type=type_hints["master_username"])
            check_type(argname="argument master_user_password", value=master_user_password, expected_type=type_hints["master_user_password"])
            check_type(argname="argument preferred_backup_window", value=preferred_backup_window, expected_type=type_hints["preferred_backup_window"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument relational_database_blueprint_id", value=relational_database_blueprint_id, expected_type=type_hints["relational_database_blueprint_id"])
            check_type(argname="argument relational_database_bundle_id", value=relational_database_bundle_id, expected_type=type_hints["relational_database_bundle_id"])
            check_type(argname="argument relational_database_name", value=relational_database_name, expected_type=type_hints["relational_database_name"])
            check_type(argname="argument relational_database_parameters", value=relational_database_parameters, expected_type=type_hints["relational_database_parameters"])
            check_type(argname="argument rotate_master_user_password", value=rotate_master_user_password, expected_type=type_hints["rotate_master_user_password"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if ca_certificate_identifier is not None:
            self._values["ca_certificate_identifier"] = ca_certificate_identifier
        if master_database_name is not None:
            self._values["master_database_name"] = master_database_name
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if relational_database_blueprint_id is not None:
            self._values["relational_database_blueprint_id"] = relational_database_blueprint_id
        if relational_database_bundle_id is not None:
            self._values["relational_database_bundle_id"] = relational_database_bundle_id
        if relational_database_name is not None:
            self._values["relational_database_name"] = relational_database_name
        if relational_database_parameters is not None:
            self._values["relational_database_parameters"] = relational_database_parameters
        if rotate_master_user_password is not None:
            self._values["rotate_master_user_password"] = rotate_master_user_password
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone for the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def backup_retention(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether automated backup retention is enabled for the database.

        Data Import Mode is enabled when ``BackupRetention`` is set to ``false`` , and is disabled when ``BackupRetention`` is set to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-backupretention
        '''
        result = self._values.get("backup_retention")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def ca_certificate_identifier(self) -> typing.Optional[builtins.str]:
        '''The certificate associated with the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-cacertificateidentifier
        '''
        result = self._values.get("ca_certificate_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_database_name(self) -> typing.Optional[builtins.str]:
        '''The meaning of this parameter differs according to the database engine you use.

        *MySQL*

        The name of the database to create when the Lightsail database resource is created. If this parameter isn't specified, no database is created in the database resource.

        Constraints:

        - Must contain 1-64 letters or numbers.
        - Must begin with a letter. Subsequent characters can be letters, underscores, or numbers (0-9).
        - Can't be a word reserved by the specified database engine.

        For more information about reserved words in MySQL, see the Keywords and Reserved Words articles for `MySQL 5.6 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.6/en/keywords.html>`_ , `MySQL 5.7 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.7/en/keywords.html>`_ , and `MySQL 8.0 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/8.0/en/keywords.html>`_ .

        *PostgreSQL*

        The name of the database to create when the Lightsail database resource is created. If this parameter isn't specified, a database named ``postgres`` is created in the database resource.

        Constraints:

        - Must contain 1-63 letters or numbers.
        - Must begin with a letter. Subsequent characters can be letters, underscores, or numbers (0-9).
        - Can't be a word reserved by the specified database engine.

        For more information about reserved words in PostgreSQL, see the SQL Key Words articles for `PostgreSQL 9.6 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/9.6/sql-keywords-appendix.html>`_ , `PostgreSQL 10 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/10/sql-keywords-appendix.html>`_ , `PostgreSQL 11 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/11/sql-keywords-appendix.html>`_ , and `PostgreSQL 12 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/12/sql-keywords-appendix.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-masterdatabasename
        '''
        result = self._values.get("master_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_username(self) -> typing.Optional[builtins.str]:
        '''The name for the primary user.

        *MySQL*

        Constraints:

        - Required for MySQL.
        - Must be 1-16 letters or numbers. Can contain underscores.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        For more information about reserved words in MySQL 5.6 or 5.7, see the Keywords and Reserved Words articles for `MySQL 5.6 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.6/en/keywords.html>`_ , `MySQL 5.7 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/5.7/en/keywords.html>`_ , or `MySQL 8.0 <https://docs.aws.amazon.com/https://dev.mysql.com/doc/refman/8.0/en/keywords.html>`_ .

        *PostgreSQL*

        Constraints:

        - Required for PostgreSQL.
        - Must be 1-63 letters or numbers. Can contain underscores.
        - First character must be a letter.
        - Can't be a reserved word for the chosen database engine.

        For more information about reserved words in MySQL 5.6 or 5.7, see the Keywords and Reserved Words articles for `PostgreSQL 9.6 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/9.6/sql-keywords-appendix.html>`_ , `PostgreSQL 10 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/10/sql-keywords-appendix.html>`_ , `PostgreSQL 11 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/11/sql-keywords-appendix.html>`_ , and `PostgreSQL 12 <https://docs.aws.amazon.com/https://www.postgresql.org/docs/12/sql-keywords-appendix.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-masterusername
        '''
        result = self._values.get("master_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def master_user_password(self) -> typing.Optional[builtins.str]:
        '''The password for the primary user of the database.

        The password can include any printable ASCII character except the following: /, ", or

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-masteruserpassword
        ::

        . It cannot contain spaces.
        .. epigraph::

        The ``MasterUserPassword`` and ``RotateMasterUserPassword`` parameters cannot be used together in the same template.

        *MySQL*

        Constraints: Must contain 8-41 characters.

        *PostgreSQL*

        Constraints: Must contain 8-128 characters.
        '''
        result = self._values.get("master_user_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[builtins.str]:
        '''The daily time range during which automated backups are created for the database (for example, ``16:00-16:30`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-preferredbackupwindow
        '''
        result = self._values.get("preferred_backup_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''The weekly time range during which system maintenance can occur for the database, formatted as follows: ``ddd:hh24:mi-ddd:hh24:mi`` .

        For example, ``Tue:17:00-Tue:17:30`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether the database is accessible to anyone on the internet.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def relational_database_blueprint_id(self) -> typing.Optional[builtins.str]:
        '''The blueprint ID for the database (for example, ``mysql_8_0`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-relationaldatabaseblueprintid
        '''
        result = self._values.get("relational_database_blueprint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relational_database_bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle ID for the database (for example, ``medium_1_0`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-relationaldatabasebundleid
        '''
        result = self._values.get("relational_database_bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relational_database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-relationaldatabasename
        '''
        result = self._values.get("relational_database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def relational_database_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.RelationalDatabaseParameterProperty"]]]]:
        '''An array of parameters for the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-relationaldatabaseparameters
        '''
        result = self._values.get("relational_database_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatabasePropsMixin.RelationalDatabaseParameterProperty"]]]], result)

    @builtins.property
    def rotate_master_user_password(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether to change the primary user password to a new, strong password generated by Lightsail .

        .. epigraph::

           The ``RotateMasterUserPassword`` and ``MasterUserPassword`` parameters cannot be used together in the same template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-rotatemasteruserpassword
        '''
        result = self._values.get("rotate_master_user_password")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html#cfn-lightsail-database-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatabaseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatabasePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDatabasePropsMixin",
):
    '''The ``AWS::Lightsail::Database`` resource specifies an Amazon Lightsail database.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html
    :cloudformationResource: AWS::Lightsail::Database
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_database_props_mixin = lightsail_mixins.CfnDatabasePropsMixin(lightsail_mixins.CfnDatabaseMixinProps(
            availability_zone="availabilityZone",
            backup_retention=False,
            ca_certificate_identifier="caCertificateIdentifier",
            master_database_name="masterDatabaseName",
            master_username="masterUsername",
            master_user_password="masterUserPassword",
            preferred_backup_window="preferredBackupWindow",
            preferred_maintenance_window="preferredMaintenanceWindow",
            publicly_accessible=False,
            relational_database_blueprint_id="relationalDatabaseBlueprintId",
            relational_database_bundle_id="relationalDatabaseBundleId",
            relational_database_name="relationalDatabaseName",
            relational_database_parameters=[lightsail_mixins.CfnDatabasePropsMixin.RelationalDatabaseParameterProperty(
                allowed_values="allowedValues",
                apply_method="applyMethod",
                apply_type="applyType",
                data_type="dataType",
                description="description",
                is_modifiable=False,
                parameter_name="parameterName",
                parameter_value="parameterValue"
            )],
            rotate_master_user_password=False,
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
        props: typing.Union[CfnDatabaseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Database``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d912645c81b36aec03719a1ec0199d4ce9af90cb9958af3ad8b2729bf51b02ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d587dfe663f2e05d9a0bb69fa270a8d574e926d33af4e82fa5b7a32835a2c64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf36ace9278c3c1cff419d48f4fb3d7b95d89fa2fca06066bd5fd90f5ec2fc2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatabaseMixinProps:
        return typing.cast(CfnDatabaseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDatabasePropsMixin.RelationalDatabaseParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_values": "allowedValues",
            "apply_method": "applyMethod",
            "apply_type": "applyType",
            "data_type": "dataType",
            "description": "description",
            "is_modifiable": "isModifiable",
            "parameter_name": "parameterName",
            "parameter_value": "parameterValue",
        },
    )
    class RelationalDatabaseParameterProperty:
        def __init__(
            self,
            *,
            allowed_values: typing.Optional[builtins.str] = None,
            apply_method: typing.Optional[builtins.str] = None,
            apply_type: typing.Optional[builtins.str] = None,
            data_type: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            is_modifiable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            parameter_name: typing.Optional[builtins.str] = None,
            parameter_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``RelationalDatabaseParameter`` is a property of the `AWS::Lightsail::Database <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-database.html>`_ resource. It describes parameters for the database.

            :param allowed_values: The valid range of values for the parameter.
            :param apply_method: Indicates when parameter updates are applied. Can be ``immediate`` or ``pending-reboot`` .
            :param apply_type: Specifies the engine-specific parameter type.
            :param data_type: The valid data type of the parameter.
            :param description: A description of the parameter.
            :param is_modifiable: A Boolean value indicating whether the parameter can be modified.
            :param parameter_name: The name of the parameter.
            :param parameter_value: The value for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                relational_database_parameter_property = lightsail_mixins.CfnDatabasePropsMixin.RelationalDatabaseParameterProperty(
                    allowed_values="allowedValues",
                    apply_method="applyMethod",
                    apply_type="applyType",
                    data_type="dataType",
                    description="description",
                    is_modifiable=False,
                    parameter_name="parameterName",
                    parameter_value="parameterValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2d27b6590eb1cdd7c322ed86ebb3b7ff1615fdd9e36897cefd7b5b8b5dea3e4)
                check_type(argname="argument allowed_values", value=allowed_values, expected_type=type_hints["allowed_values"])
                check_type(argname="argument apply_method", value=apply_method, expected_type=type_hints["apply_method"])
                check_type(argname="argument apply_type", value=apply_type, expected_type=type_hints["apply_type"])
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument is_modifiable", value=is_modifiable, expected_type=type_hints["is_modifiable"])
                check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
                check_type(argname="argument parameter_value", value=parameter_value, expected_type=type_hints["parameter_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_values is not None:
                self._values["allowed_values"] = allowed_values
            if apply_method is not None:
                self._values["apply_method"] = apply_method
            if apply_type is not None:
                self._values["apply_type"] = apply_type
            if data_type is not None:
                self._values["data_type"] = data_type
            if description is not None:
                self._values["description"] = description
            if is_modifiable is not None:
                self._values["is_modifiable"] = is_modifiable
            if parameter_name is not None:
                self._values["parameter_name"] = parameter_name
            if parameter_value is not None:
                self._values["parameter_value"] = parameter_value

        @builtins.property
        def allowed_values(self) -> typing.Optional[builtins.str]:
            '''The valid range of values for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-allowedvalues
            '''
            result = self._values.get("allowed_values")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def apply_method(self) -> typing.Optional[builtins.str]:
            '''Indicates when parameter updates are applied.

            Can be ``immediate`` or ``pending-reboot`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-applymethod
            '''
            result = self._values.get("apply_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def apply_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the engine-specific parameter type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-applytype
            '''
            result = self._values.get("apply_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The valid data type of the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_modifiable(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether the parameter can be modified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-ismodifiable
            '''
            result = self._values.get("is_modifiable")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def parameter_name(self) -> typing.Optional[builtins.str]:
            '''The name of the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-parametername
            '''
            result = self._values.get("parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameter_value(self) -> typing.Optional[builtins.str]:
            '''The value for the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-database-relationaldatabaseparameter.html#cfn-lightsail-database-relationaldatabaseparameter-parametervalue
            '''
            result = self._values.get("parameter_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RelationalDatabaseParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_ons": "addOns",
        "availability_zone": "availabilityZone",
        "disk_name": "diskName",
        "location": "location",
        "size_in_gb": "sizeInGb",
        "tags": "tags",
    },
)
class CfnDiskMixinProps:
    def __init__(
        self,
        *,
        add_ons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDiskPropsMixin.AddOnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        disk_name: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDiskPropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        size_in_gb: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDiskPropsMixin.

        :param add_ons: An array of add-ons for the disk. .. epigraph:: If the disk has an add-on enabled when performing a delete disk request, the add-on is automatically disabled before the disk is deleted.
        :param availability_zone: The AWS Region and Availability Zone location for the disk (for example, ``us-east-1a`` ).
        :param disk_name: The name of the disk.
        :param location: The AWS Region and Availability Zone where the disk is located.
        :param size_in_gb: The size of the disk in GB.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_disk_mixin_props = lightsail_mixins.CfnDiskMixinProps(
                add_ons=[lightsail_mixins.CfnDiskPropsMixin.AddOnProperty(
                    add_on_type="addOnType",
                    auto_snapshot_add_on_request=lightsail_mixins.CfnDiskPropsMixin.AutoSnapshotAddOnProperty(
                        snapshot_time_of_day="snapshotTimeOfDay"
                    ),
                    status="status"
                )],
                availability_zone="availabilityZone",
                disk_name="diskName",
                location=lightsail_mixins.CfnDiskPropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                ),
                size_in_gb=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45c01e1b3f572ea4bed99965f2c474e8e854a7cc0fcf79f73cc3203c29bf91d4)
            check_type(argname="argument add_ons", value=add_ons, expected_type=type_hints["add_ons"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument disk_name", value=disk_name, expected_type=type_hints["disk_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_ons is not None:
            self._values["add_ons"] = add_ons
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if disk_name is not None:
            self._values["disk_name"] = disk_name
        if location is not None:
            self._values["location"] = location
        if size_in_gb is not None:
            self._values["size_in_gb"] = size_in_gb
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def add_ons(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDiskPropsMixin.AddOnProperty"]]]]:
        '''An array of add-ons for the disk.

        .. epigraph::

           If the disk has an add-on enabled when performing a delete disk request, the add-on is automatically disabled before the disk is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html#cfn-lightsail-disk-addons
        '''
        result = self._values.get("add_ons")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDiskPropsMixin.AddOnProperty"]]]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The AWS Region and Availability Zone location for the disk (for example, ``us-east-1a`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html#cfn-lightsail-disk-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_name(self) -> typing.Optional[builtins.str]:
        '''The name of the disk.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html#cfn-lightsail-disk-diskname
        '''
        result = self._values.get("disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDiskPropsMixin.LocationProperty"]]:
        '''The AWS Region and Availability Zone where the disk is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html#cfn-lightsail-disk-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDiskPropsMixin.LocationProperty"]], result)

    @builtins.property
    def size_in_gb(self) -> typing.Optional[jsii.Number]:
        '''The size of the disk in GB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html#cfn-lightsail-disk-sizeingb
        '''
        result = self._values.get("size_in_gb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html#cfn-lightsail-disk-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDiskMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDiskPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskPropsMixin",
):
    '''The ``AWS::Lightsail::Disk`` resource specifies a disk that can be attached to an Amazon Lightsail instance that is in the same AWS Region and Availability Zone.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html
    :cloudformationResource: AWS::Lightsail::Disk
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_disk_props_mixin = lightsail_mixins.CfnDiskPropsMixin(lightsail_mixins.CfnDiskMixinProps(
            add_ons=[lightsail_mixins.CfnDiskPropsMixin.AddOnProperty(
                add_on_type="addOnType",
                auto_snapshot_add_on_request=lightsail_mixins.CfnDiskPropsMixin.AutoSnapshotAddOnProperty(
                    snapshot_time_of_day="snapshotTimeOfDay"
                ),
                status="status"
            )],
            availability_zone="availabilityZone",
            disk_name="diskName",
            location=lightsail_mixins.CfnDiskPropsMixin.LocationProperty(
                availability_zone="availabilityZone",
                region_name="regionName"
            ),
            size_in_gb=123,
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
        props: typing.Union[CfnDiskMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Disk``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b0d42b5420127f0e4dfd885756fa0d81f864c23fec3e3763e1d7474623562c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f3eb0c6658dd33d8caaf948c49198906a0a96681843b10b1dbf1a0fdf0b9a59)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b35feea8b0cc760d76f529607733c6155f39f66cb17c2edbaa8e0135b02a6f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDiskMixinProps:
        return typing.cast(CfnDiskMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskPropsMixin.AddOnProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_on_type": "addOnType",
            "auto_snapshot_add_on_request": "autoSnapshotAddOnRequest",
            "status": "status",
        },
    )
    class AddOnProperty:
        def __init__(
            self,
            *,
            add_on_type: typing.Optional[builtins.str] = None,
            auto_snapshot_add_on_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDiskPropsMixin.AutoSnapshotAddOnProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``AddOn`` is a property of the `AWS::Lightsail::Disk <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disk.html>`_ resource. It describes the add-ons for a disk.

            :param add_on_type: The add-on type (for example, ``AutoSnapshot`` ). .. epigraph:: ``AutoSnapshot`` is the only add-on that can be enabled for a disk.
            :param auto_snapshot_add_on_request: The parameters for the automatic snapshot add-on, such as the daily time when an automatic snapshot will be created.
            :param status: The status of the add-on. Valid Values: ``Enabled`` | ``Disabled``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-addon.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                add_on_property = lightsail_mixins.CfnDiskPropsMixin.AddOnProperty(
                    add_on_type="addOnType",
                    auto_snapshot_add_on_request=lightsail_mixins.CfnDiskPropsMixin.AutoSnapshotAddOnProperty(
                        snapshot_time_of_day="snapshotTimeOfDay"
                    ),
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__761aff583ef0d298a3f996c87dd35534487b15c8f5d69dabcf9e0842056b7b6a)
                check_type(argname="argument add_on_type", value=add_on_type, expected_type=type_hints["add_on_type"])
                check_type(argname="argument auto_snapshot_add_on_request", value=auto_snapshot_add_on_request, expected_type=type_hints["auto_snapshot_add_on_request"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_on_type is not None:
                self._values["add_on_type"] = add_on_type
            if auto_snapshot_add_on_request is not None:
                self._values["auto_snapshot_add_on_request"] = auto_snapshot_add_on_request
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def add_on_type(self) -> typing.Optional[builtins.str]:
            '''The add-on type (for example, ``AutoSnapshot`` ).

            .. epigraph::

               ``AutoSnapshot`` is the only add-on that can be enabled for a disk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-addon.html#cfn-lightsail-disk-addon-addontype
            '''
            result = self._values.get("add_on_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auto_snapshot_add_on_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDiskPropsMixin.AutoSnapshotAddOnProperty"]]:
            '''The parameters for the automatic snapshot add-on, such as the daily time when an automatic snapshot will be created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-addon.html#cfn-lightsail-disk-addon-autosnapshotaddonrequest
            '''
            result = self._values.get("auto_snapshot_add_on_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDiskPropsMixin.AutoSnapshotAddOnProperty"]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the add-on.

            Valid Values: ``Enabled`` | ``Disabled``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-addon.html#cfn-lightsail-disk-addon-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddOnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskPropsMixin.AutoSnapshotAddOnProperty",
        jsii_struct_bases=[],
        name_mapping={"snapshot_time_of_day": "snapshotTimeOfDay"},
    )
    class AutoSnapshotAddOnProperty:
        def __init__(
            self,
            *,
            snapshot_time_of_day: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``AutoSnapshotAddOn`` is a property of the `AddOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-addon.html>`_ property. It describes the automatic snapshot add-on for a disk.

            :param snapshot_time_of_day: The daily time when an automatic snapshot will be created. Constraints: - Must be in ``HH:00`` format, and in an hourly increment. - Specified in Coordinated Universal Time (UTC). - The snapshot will be automatically created between the time specified and up to 45 minutes after.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-autosnapshotaddon.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                auto_snapshot_add_on_property = lightsail_mixins.CfnDiskPropsMixin.AutoSnapshotAddOnProperty(
                    snapshot_time_of_day="snapshotTimeOfDay"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cf6938e15b2e0f84bccb6620246af57dc4353c4903b8dd3075b95492f5cc936)
                check_type(argname="argument snapshot_time_of_day", value=snapshot_time_of_day, expected_type=type_hints["snapshot_time_of_day"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if snapshot_time_of_day is not None:
                self._values["snapshot_time_of_day"] = snapshot_time_of_day

        @builtins.property
        def snapshot_time_of_day(self) -> typing.Optional[builtins.str]:
            '''The daily time when an automatic snapshot will be created.

            Constraints:

            - Must be in ``HH:00`` format, and in an hourly increment.
            - Specified in Coordinated Universal Time (UTC).
            - The snapshot will be automatically created between the time specified and up to 45 minutes after.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-autosnapshotaddon.html#cfn-lightsail-disk-autosnapshotaddon-snapshottimeofday
            '''
            result = self._values.get("snapshot_time_of_day")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoSnapshotAddOnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "region_name": "regionName",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Region and Availability Zone where the disk is located.

            :param availability_zone: The Availability Zone where the disk is located.
            :param region_name: The AWS Region where the disk is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                location_property = lightsail_mixins.CfnDiskPropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__963a5399a31ae070a82b6b996743c04de9ca6486dfb70ccb6bae81fef1b9b783)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone where the disk is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-location.html#cfn-lightsail-disk-location-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Region where the disk is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disk-location.html#cfn-lightsail-disk-location-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskSnapshotMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "disk_name": "diskName",
        "disk_snapshot_name": "diskSnapshotName",
        "tags": "tags",
    },
)
class CfnDiskSnapshotMixinProps:
    def __init__(
        self,
        *,
        disk_name: typing.Optional[builtins.str] = None,
        disk_snapshot_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDiskSnapshotPropsMixin.

        :param disk_name: The unique name of the disk.
        :param disk_snapshot_name: The name of the disk snapshot ( ``my-disk-snapshot`` ).
        :param tags: The tag keys and optional values for the resource. For more information about tags in Lightsail, see the `Amazon Lightsail Developer Guide <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-tags>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disksnapshot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_disk_snapshot_mixin_props = lightsail_mixins.CfnDiskSnapshotMixinProps(
                disk_name="diskName",
                disk_snapshot_name="diskSnapshotName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5554ec3968b0aa4e473d189d96e0c752915c28e854d70df0c553549243b2159)
            check_type(argname="argument disk_name", value=disk_name, expected_type=type_hints["disk_name"])
            check_type(argname="argument disk_snapshot_name", value=disk_snapshot_name, expected_type=type_hints["disk_snapshot_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_name is not None:
            self._values["disk_name"] = disk_name
        if disk_snapshot_name is not None:
            self._values["disk_snapshot_name"] = disk_snapshot_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def disk_name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the disk.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disksnapshot.html#cfn-lightsail-disksnapshot-diskname
        '''
        result = self._values.get("disk_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of the disk snapshot ( ``my-disk-snapshot`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disksnapshot.html#cfn-lightsail-disksnapshot-disksnapshotname
        '''
        result = self._values.get("disk_snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag keys and optional values for the resource.

        For more information about tags in Lightsail, see the `Amazon Lightsail Developer Guide <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-tags>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disksnapshot.html#cfn-lightsail-disksnapshot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDiskSnapshotMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDiskSnapshotPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskSnapshotPropsMixin",
):
    '''Describes a block storage disk snapshot.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-disksnapshot.html
    :cloudformationResource: AWS::Lightsail::DiskSnapshot
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_disk_snapshot_props_mixin = lightsail_mixins.CfnDiskSnapshotPropsMixin(lightsail_mixins.CfnDiskSnapshotMixinProps(
            disk_name="diskName",
            disk_snapshot_name="diskSnapshotName",
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
        props: typing.Union[CfnDiskSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::DiskSnapshot``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed0fa14c50441c9030562d270f566f63f4be14cc2d354b91680a13e181a3ea00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d2e8a7bd725b58e963d60f8f4e0644f2896c1ecf9f099123de9382cb0e76293)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62624609725b66f4062347cd000f3d4c2d0cdfb0b69c04e2c118f417d08782fc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDiskSnapshotMixinProps:
        return typing.cast(CfnDiskSnapshotMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDiskSnapshotPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "region_name": "regionName",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Region and Availability Zone where the disk snapshot was created.

            :param availability_zone: The Availability Zone where the disk snapshot was created.
            :param region_name: The AWS Region where the disk snapshot was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disksnapshot-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                location_property = lightsail_mixins.CfnDiskSnapshotPropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5019a2797292a713ce770b30399ac131989276ff3d2626b3c7f7e57c5bde02ac)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone where the disk snapshot was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disksnapshot-location.html#cfn-lightsail-disksnapshot-location-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Region where the disk snapshot was created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-disksnapshot-location.html#cfn-lightsail-disksnapshot-location-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bundle_id": "bundleId",
        "cache_behaviors": "cacheBehaviors",
        "cache_behavior_settings": "cacheBehaviorSettings",
        "certificate_name": "certificateName",
        "default_cache_behavior": "defaultCacheBehavior",
        "distribution_name": "distributionName",
        "ip_address_type": "ipAddressType",
        "is_enabled": "isEnabled",
        "origin": "origin",
        "tags": "tags",
    },
)
class CfnDistributionMixinProps:
    def __init__(
        self,
        *,
        bundle_id: typing.Optional[builtins.str] = None,
        cache_behaviors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.CacheBehaviorPerPathProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        cache_behavior_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.CacheSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate_name: typing.Optional[builtins.str] = None,
        default_cache_behavior: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.CacheBehaviorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        distribution_name: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        origin: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.InputOriginProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDistributionPropsMixin.

        :param bundle_id: The ID of the bundle applied to the distribution.
        :param cache_behaviors: An array of objects that describe the per-path cache behavior of the distribution.
        :param cache_behavior_settings: An object that describes the cache behavior settings of the distribution.
        :param certificate_name: The name of the SSL/TLS certificate attached to the distribution.
        :param default_cache_behavior: An object that describes the default cache behavior of the distribution.
        :param distribution_name: The name of the distribution.
        :param ip_address_type: The IP address type of the distribution. The possible values are ``ipv4`` for IPv4 only, and ``dualstack`` for IPv4 and IPv6.
        :param is_enabled: A Boolean value indicating whether the distribution is enabled.
        :param origin: An object that describes the origin resource of the distribution, such as a Lightsail instance, bucket, or load balancer. The distribution pulls, caches, and serves content from the origin.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_distribution_mixin_props = lightsail_mixins.CfnDistributionMixinProps(
                bundle_id="bundleId",
                cache_behaviors=[lightsail_mixins.CfnDistributionPropsMixin.CacheBehaviorPerPathProperty(
                    behavior="behavior",
                    path="path"
                )],
                cache_behavior_settings=lightsail_mixins.CfnDistributionPropsMixin.CacheSettingsProperty(
                    allowed_http_methods="allowedHttpMethods",
                    cached_http_methods="cachedHttpMethods",
                    default_ttl=123,
                    forwarded_cookies=lightsail_mixins.CfnDistributionPropsMixin.CookieObjectProperty(
                        cookies_allow_list=["cookiesAllowList"],
                        option="option"
                    ),
                    forwarded_headers=lightsail_mixins.CfnDistributionPropsMixin.HeaderObjectProperty(
                        headers_allow_list=["headersAllowList"],
                        option="option"
                    ),
                    forwarded_query_strings=lightsail_mixins.CfnDistributionPropsMixin.QueryStringObjectProperty(
                        option=False,
                        query_strings_allow_list=["queryStringsAllowList"]
                    ),
                    maximum_ttl=123,
                    minimum_ttl=123
                ),
                certificate_name="certificateName",
                default_cache_behavior=lightsail_mixins.CfnDistributionPropsMixin.CacheBehaviorProperty(
                    behavior="behavior"
                ),
                distribution_name="distributionName",
                ip_address_type="ipAddressType",
                is_enabled=False,
                origin=lightsail_mixins.CfnDistributionPropsMixin.InputOriginProperty(
                    name="name",
                    protocol_policy="protocolPolicy",
                    region_name="regionName"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06244b8225cc9dbe34f69eaf03b9d79676fdb754abdd4da38e382b380dfa3a48)
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument cache_behaviors", value=cache_behaviors, expected_type=type_hints["cache_behaviors"])
            check_type(argname="argument cache_behavior_settings", value=cache_behavior_settings, expected_type=type_hints["cache_behavior_settings"])
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument default_cache_behavior", value=default_cache_behavior, expected_type=type_hints["default_cache_behavior"])
            check_type(argname="argument distribution_name", value=distribution_name, expected_type=type_hints["distribution_name"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument is_enabled", value=is_enabled, expected_type=type_hints["is_enabled"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if cache_behaviors is not None:
            self._values["cache_behaviors"] = cache_behaviors
        if cache_behavior_settings is not None:
            self._values["cache_behavior_settings"] = cache_behavior_settings
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if default_cache_behavior is not None:
            self._values["default_cache_behavior"] = default_cache_behavior
        if distribution_name is not None:
            self._values["distribution_name"] = distribution_name
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if is_enabled is not None:
            self._values["is_enabled"] = is_enabled
        if origin is not None:
            self._values["origin"] = origin
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the bundle applied to the distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_behaviors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CacheBehaviorPerPathProperty"]]]]:
        '''An array of objects that describe the per-path cache behavior of the distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-cachebehaviors
        '''
        result = self._values.get("cache_behaviors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CacheBehaviorPerPathProperty"]]]], result)

    @builtins.property
    def cache_behavior_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CacheSettingsProperty"]]:
        '''An object that describes the cache behavior settings of the distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-cachebehaviorsettings
        '''
        result = self._values.get("cache_behavior_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CacheSettingsProperty"]], result)

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name of the SSL/TLS certificate attached to the distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-certificatename
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_cache_behavior(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CacheBehaviorProperty"]]:
        '''An object that describes the default cache behavior of the distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-defaultcachebehavior
        '''
        result = self._values.get("default_cache_behavior")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CacheBehaviorProperty"]], result)

    @builtins.property
    def distribution_name(self) -> typing.Optional[builtins.str]:
        '''The name of the distribution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-distributionname
        '''
        result = self._values.get("distribution_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type of the distribution.

        The possible values are ``ipv4`` for IPv4 only, and ``dualstack`` for IPv4 and IPv6.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether the distribution is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-isenabled
        '''
        result = self._values.get("is_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def origin(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.InputOriginProperty"]]:
        '''An object that describes the origin resource of the distribution, such as a Lightsail instance, bucket, or load balancer.

        The distribution pulls, caches, and serves content from the origin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-origin
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.InputOriginProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html#cfn-lightsail-distribution-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDistributionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDistributionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin",
):
    '''The ``AWS::Lightsail::Distribution`` resource specifies a content delivery network (CDN) distribution.

    You can create distributions only in the ``us-east-1`` AWS Region.

    A distribution is a globally distributed network of caching servers that improve the performance of your website or web application hosted on a Lightsail instance, static content hosted on a Lightsail bucket, or through a Lightsail load balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html
    :cloudformationResource: AWS::Lightsail::Distribution
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_distribution_props_mixin = lightsail_mixins.CfnDistributionPropsMixin(lightsail_mixins.CfnDistributionMixinProps(
            bundle_id="bundleId",
            cache_behaviors=[lightsail_mixins.CfnDistributionPropsMixin.CacheBehaviorPerPathProperty(
                behavior="behavior",
                path="path"
            )],
            cache_behavior_settings=lightsail_mixins.CfnDistributionPropsMixin.CacheSettingsProperty(
                allowed_http_methods="allowedHttpMethods",
                cached_http_methods="cachedHttpMethods",
                default_ttl=123,
                forwarded_cookies=lightsail_mixins.CfnDistributionPropsMixin.CookieObjectProperty(
                    cookies_allow_list=["cookiesAllowList"],
                    option="option"
                ),
                forwarded_headers=lightsail_mixins.CfnDistributionPropsMixin.HeaderObjectProperty(
                    headers_allow_list=["headersAllowList"],
                    option="option"
                ),
                forwarded_query_strings=lightsail_mixins.CfnDistributionPropsMixin.QueryStringObjectProperty(
                    option=False,
                    query_strings_allow_list=["queryStringsAllowList"]
                ),
                maximum_ttl=123,
                minimum_ttl=123
            ),
            certificate_name="certificateName",
            default_cache_behavior=lightsail_mixins.CfnDistributionPropsMixin.CacheBehaviorProperty(
                behavior="behavior"
            ),
            distribution_name="distributionName",
            ip_address_type="ipAddressType",
            is_enabled=False,
            origin=lightsail_mixins.CfnDistributionPropsMixin.InputOriginProperty(
                name="name",
                protocol_policy="protocolPolicy",
                region_name="regionName"
            ),
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
        props: typing.Union[CfnDistributionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Distribution``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f67064e88414aecf42dd7619f3601cedc7912fc97d20a516132ff50a7eec0a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceae9f207e0659938f2edbe1235b39788dd19c1b7fa84e96012073c9dd002133)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41bcb20b0c96722bd263a98818ff0a6c604513f85097b00cf79a0b0243b0570c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDistributionMixinProps:
        return typing.cast(CfnDistributionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.CacheBehaviorPerPathProperty",
        jsii_struct_bases=[],
        name_mapping={"behavior": "behavior", "path": "path"},
    )
    class CacheBehaviorPerPathProperty:
        def __init__(
            self,
            *,
            behavior: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``CacheBehaviorPerPath`` is a property of the `AWS::Lightsail::Distribution <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html>`_ resource. It describes the per-path cache behavior of an Amazon Lightsail content delivery network (CDN) distribution.

            Use a per-path cache behavior to override the default cache behavior of a distribution, or to add an exception to it. For example, if you set the ``CacheBehavior`` to ``cache`` , you can use a per-path cache behavior to specify a directory, file, or file type that your distribution will cache. If you don’t want your distribution to cache a specified directory, file, or file type, set the per-path cache behavior to ``dont-cache`` .

            :param behavior: The cache behavior for the specified path. You can specify one of the following per-path cache behaviors: - *``cache``* - This behavior caches the specified path. - *``dont-cache``* - This behavior doesn't cache the specified path.
            :param path: The path to a directory or file to cache, or not cache. Use an asterisk symbol to specify wildcard directories ( ``path/to/assets/*`` ), and file types ( ``*.html`` , ``*jpg`` , ``*js`` ). Directories and file paths are case-sensitive. Examples: - Specify the following to cache all files in the document root of an Apache web server running on a instance. ``var/www/html/`` - Specify the following file to cache only the index page in the document root of an Apache web server. ``var/www/html/index.html`` - Specify the following to cache only the .html files in the document root of an Apache web server. ``var/www/html/*.html`` - Specify the following to cache only the .jpg, .png, and .gif files in the images sub-directory of the document root of an Apache web server. ``var/www/html/images/*.jpg`` ``var/www/html/images/*.png`` ``var/www/html/images/*.gif`` Specify the following to cache all files in the images subdirectory of the document root of an Apache web server. ``var/www/html/images/``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachebehaviorperpath.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                cache_behavior_per_path_property = lightsail_mixins.CfnDistributionPropsMixin.CacheBehaviorPerPathProperty(
                    behavior="behavior",
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__086fc6ced7af705cf4cc3c981d85b87ef60dbf980755265b8e0204404b310d6e)
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior is not None:
                self._values["behavior"] = behavior
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def behavior(self) -> typing.Optional[builtins.str]:
            '''The cache behavior for the specified path.

            You can specify one of the following per-path cache behaviors:

            - *``cache``* - This behavior caches the specified path.
            - *``dont-cache``* - This behavior doesn't cache the specified path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachebehaviorperpath.html#cfn-lightsail-distribution-cachebehaviorperpath-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path to a directory or file to cache, or not cache.

            Use an asterisk symbol to specify wildcard directories ( ``path/to/assets/*`` ), and file types ( ``*.html`` , ``*jpg`` , ``*js`` ). Directories and file paths are case-sensitive.

            Examples:

            - Specify the following to cache all files in the document root of an Apache web server running on a instance.

            ``var/www/html/``

            - Specify the following file to cache only the index page in the document root of an Apache web server.

            ``var/www/html/index.html``

            - Specify the following to cache only the .html files in the document root of an Apache web server.

            ``var/www/html/*.html``

            - Specify the following to cache only the .jpg, .png, and .gif files in the images sub-directory of the document root of an Apache web server.

            ``var/www/html/images/*.jpg``

            ``var/www/html/images/*.png``

            ``var/www/html/images/*.gif``

            Specify the following to cache all files in the images subdirectory of the document root of an Apache web server.

            ``var/www/html/images/``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachebehaviorperpath.html#cfn-lightsail-distribution-cachebehaviorperpath-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheBehaviorPerPathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.CacheBehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={"behavior": "behavior"},
    )
    class CacheBehaviorProperty:
        def __init__(self, *, behavior: typing.Optional[builtins.str] = None) -> None:
            '''``CacheBehavior`` is a property of the `AWS::Lightsail::Distribution <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html>`_ resource. It describes the default cache behavior of an Amazon Lightsail content delivery network (CDN) distribution.

            :param behavior: The cache behavior of the distribution. The following cache behaviors can be specified: - *``cache``* - This option is best for static sites. When specified, your distribution caches and serves your entire website as static content. This behavior is ideal for websites with static content that doesn't change depending on who views it, or for websites that don't use cookies, headers, or query strings to personalize content. - *``dont-cache``* - This option is best for sites that serve a mix of static and dynamic content. When specified, your distribution caches and serves only the content that is specified in the distribution’s ``CacheBehaviorPerPath`` parameter. This behavior is ideal for websites or web applications that use cookies, headers, and query strings to personalize content for individual users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachebehavior.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                cache_behavior_property = lightsail_mixins.CfnDistributionPropsMixin.CacheBehaviorProperty(
                    behavior="behavior"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2f7ca779722be8b7d7cff1f3ff979afe5a9d0dbdfa402739b9b359e58719677)
                check_type(argname="argument behavior", value=behavior, expected_type=type_hints["behavior"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior is not None:
                self._values["behavior"] = behavior

        @builtins.property
        def behavior(self) -> typing.Optional[builtins.str]:
            '''The cache behavior of the distribution.

            The following cache behaviors can be specified:

            - *``cache``* - This option is best for static sites. When specified, your distribution caches and serves your entire website as static content. This behavior is ideal for websites with static content that doesn't change depending on who views it, or for websites that don't use cookies, headers, or query strings to personalize content.
            - *``dont-cache``* - This option is best for sites that serve a mix of static and dynamic content. When specified, your distribution caches and serves only the content that is specified in the distribution’s ``CacheBehaviorPerPath`` parameter. This behavior is ideal for websites or web applications that use cookies, headers, and query strings to personalize content for individual users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachebehavior.html#cfn-lightsail-distribution-cachebehavior-behavior
            '''
            result = self._values.get("behavior")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheBehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.CacheSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_http_methods": "allowedHttpMethods",
            "cached_http_methods": "cachedHttpMethods",
            "default_ttl": "defaultTtl",
            "forwarded_cookies": "forwardedCookies",
            "forwarded_headers": "forwardedHeaders",
            "forwarded_query_strings": "forwardedQueryStrings",
            "maximum_ttl": "maximumTtl",
            "minimum_ttl": "minimumTtl",
        },
    )
    class CacheSettingsProperty:
        def __init__(
            self,
            *,
            allowed_http_methods: typing.Optional[builtins.str] = None,
            cached_http_methods: typing.Optional[builtins.str] = None,
            default_ttl: typing.Optional[jsii.Number] = None,
            forwarded_cookies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.CookieObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forwarded_headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.HeaderObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forwarded_query_strings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDistributionPropsMixin.QueryStringObjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_ttl: typing.Optional[jsii.Number] = None,
            minimum_ttl: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``CacheSettings`` is a property of the `AWS::Lightsail::Distribution <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html>`_ resource. It describes the cache settings of an Amazon Lightsail content delivery network (CDN) distribution.

            These settings apply only to your distribution’s ``CacheBehaviors`` that have a ``Behavior`` of ``cache`` . This includes the ``DefaultCacheBehavior`` .

            :param allowed_http_methods: The HTTP methods that are processed and forwarded to the distribution's origin. You can specify the following options: - ``GET,HEAD`` - The distribution forwards the ``GET`` and ``HEAD`` methods. - ``GET,HEAD,OPTIONS`` - The distribution forwards the ``GET`` , ``HEAD`` , and ``OPTIONS`` methods. - ``GET,HEAD,OPTIONS,PUT,PATCH,POST,DELETE`` - The distribution forwards the ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PUT`` , ``PATCH`` , ``POST`` , and ``DELETE`` methods. If you specify ``GET,HEAD,OPTIONS,PUT,PATCH,POST,DELETE`` , you might need to restrict access to your distribution's origin so users can't perform operations that you don't want them to. For example, you might not want users to have permission to delete objects from your origin.
            :param cached_http_methods: The HTTP method responses that are cached by your distribution. You can specify the following options: - ``GET,HEAD`` - The distribution caches responses to the ``GET`` and ``HEAD`` methods. - ``GET,HEAD,OPTIONS`` - The distribution caches responses to the ``GET`` , ``HEAD`` , and ``OPTIONS`` methods.
            :param default_ttl: The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated. .. epigraph:: The value specified applies only when the origin does not add HTTP headers such as ``Cache-Control max-age`` , ``Cache-Control s-maxage`` , and ``Expires`` to objects.
            :param forwarded_cookies: An object that describes the cookies that are forwarded to the origin. Your content is cached based on the cookies that are forwarded.
            :param forwarded_headers: An object that describes the headers that are forwarded to the origin. Your content is cached based on the headers that are forwarded.
            :param forwarded_query_strings: An object that describes the query strings that are forwarded to the origin. Your content is cached based on the query strings that are forwarded.
            :param maximum_ttl: The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. The value specified applies only when the origin adds HTTP headers such as ``Cache-Control max-age`` , ``Cache-Control s-maxage`` , and ``Expires`` to objects.
            :param minimum_ttl: The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated. A value of ``0`` must be specified for ``minimumTTL`` if the distribution is configured to forward all headers to the origin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                cache_settings_property = lightsail_mixins.CfnDistributionPropsMixin.CacheSettingsProperty(
                    allowed_http_methods="allowedHttpMethods",
                    cached_http_methods="cachedHttpMethods",
                    default_ttl=123,
                    forwarded_cookies=lightsail_mixins.CfnDistributionPropsMixin.CookieObjectProperty(
                        cookies_allow_list=["cookiesAllowList"],
                        option="option"
                    ),
                    forwarded_headers=lightsail_mixins.CfnDistributionPropsMixin.HeaderObjectProperty(
                        headers_allow_list=["headersAllowList"],
                        option="option"
                    ),
                    forwarded_query_strings=lightsail_mixins.CfnDistributionPropsMixin.QueryStringObjectProperty(
                        option=False,
                        query_strings_allow_list=["queryStringsAllowList"]
                    ),
                    maximum_ttl=123,
                    minimum_ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5db8305f26c53a347ff768a189d1569872b210f72adba6ebc56ef79af222e5db)
                check_type(argname="argument allowed_http_methods", value=allowed_http_methods, expected_type=type_hints["allowed_http_methods"])
                check_type(argname="argument cached_http_methods", value=cached_http_methods, expected_type=type_hints["cached_http_methods"])
                check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
                check_type(argname="argument forwarded_cookies", value=forwarded_cookies, expected_type=type_hints["forwarded_cookies"])
                check_type(argname="argument forwarded_headers", value=forwarded_headers, expected_type=type_hints["forwarded_headers"])
                check_type(argname="argument forwarded_query_strings", value=forwarded_query_strings, expected_type=type_hints["forwarded_query_strings"])
                check_type(argname="argument maximum_ttl", value=maximum_ttl, expected_type=type_hints["maximum_ttl"])
                check_type(argname="argument minimum_ttl", value=minimum_ttl, expected_type=type_hints["minimum_ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_http_methods is not None:
                self._values["allowed_http_methods"] = allowed_http_methods
            if cached_http_methods is not None:
                self._values["cached_http_methods"] = cached_http_methods
            if default_ttl is not None:
                self._values["default_ttl"] = default_ttl
            if forwarded_cookies is not None:
                self._values["forwarded_cookies"] = forwarded_cookies
            if forwarded_headers is not None:
                self._values["forwarded_headers"] = forwarded_headers
            if forwarded_query_strings is not None:
                self._values["forwarded_query_strings"] = forwarded_query_strings
            if maximum_ttl is not None:
                self._values["maximum_ttl"] = maximum_ttl
            if minimum_ttl is not None:
                self._values["minimum_ttl"] = minimum_ttl

        @builtins.property
        def allowed_http_methods(self) -> typing.Optional[builtins.str]:
            '''The HTTP methods that are processed and forwarded to the distribution's origin.

            You can specify the following options:

            - ``GET,HEAD`` - The distribution forwards the ``GET`` and ``HEAD`` methods.
            - ``GET,HEAD,OPTIONS`` - The distribution forwards the ``GET`` , ``HEAD`` , and ``OPTIONS`` methods.
            - ``GET,HEAD,OPTIONS,PUT,PATCH,POST,DELETE`` - The distribution forwards the ``GET`` , ``HEAD`` , ``OPTIONS`` , ``PUT`` , ``PATCH`` , ``POST`` , and ``DELETE`` methods.

            If you specify ``GET,HEAD,OPTIONS,PUT,PATCH,POST,DELETE`` , you might need to restrict access to your distribution's origin so users can't perform operations that you don't want them to. For example, you might not want users to have permission to delete objects from your origin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-allowedhttpmethods
            '''
            result = self._values.get("allowed_http_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cached_http_methods(self) -> typing.Optional[builtins.str]:
            '''The HTTP method responses that are cached by your distribution.

            You can specify the following options:

            - ``GET,HEAD`` - The distribution caches responses to the ``GET`` and ``HEAD`` methods.
            - ``GET,HEAD,OPTIONS`` - The distribution caches responses to the ``GET`` , ``HEAD`` , and ``OPTIONS`` methods.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-cachedhttpmethods
            '''
            result = self._values.get("cached_http_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_ttl(self) -> typing.Optional[jsii.Number]:
            '''The default amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the content has been updated.

            .. epigraph::

               The value specified applies only when the origin does not add HTTP headers such as ``Cache-Control max-age`` , ``Cache-Control s-maxage`` , and ``Expires`` to objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-defaultttl
            '''
            result = self._values.get("default_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def forwarded_cookies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CookieObjectProperty"]]:
            '''An object that describes the cookies that are forwarded to the origin.

            Your content is cached based on the cookies that are forwarded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-forwardedcookies
            '''
            result = self._values.get("forwarded_cookies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.CookieObjectProperty"]], result)

        @builtins.property
        def forwarded_headers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.HeaderObjectProperty"]]:
            '''An object that describes the headers that are forwarded to the origin.

            Your content is cached based on the headers that are forwarded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-forwardedheaders
            '''
            result = self._values.get("forwarded_headers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.HeaderObjectProperty"]], result)

        @builtins.property
        def forwarded_query_strings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.QueryStringObjectProperty"]]:
            '''An object that describes the query strings that are forwarded to the origin.

            Your content is cached based on the query strings that are forwarded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-forwardedquerystrings
            '''
            result = self._values.get("forwarded_query_strings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDistributionPropsMixin.QueryStringObjectProperty"]], result)

        @builtins.property
        def maximum_ttl(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated.

            The value specified applies only when the origin adds HTTP headers such as ``Cache-Control max-age`` , ``Cache-Control s-maxage`` , and ``Expires`` to objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-maximumttl
            '''
            result = self._values.get("maximum_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum_ttl(self) -> typing.Optional[jsii.Number]:
            '''The minimum amount of time that objects stay in the distribution's cache before the distribution forwards another request to the origin to determine whether the object has been updated.

            A value of ``0`` must be specified for ``minimumTTL`` if the distribution is configured to forward all headers to the origin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html#cfn-lightsail-distribution-cachesettings-minimumttl
            '''
            result = self._values.get("minimum_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CacheSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.CookieObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"cookies_allow_list": "cookiesAllowList", "option": "option"},
    )
    class CookieObjectProperty:
        def __init__(
            self,
            *,
            cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            option: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``CookieObject`` is a property of the `CacheSettings <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html>`_ property. It describes whether an Amazon Lightsail content delivery network (CDN) distribution forwards cookies to the origin and, if so, which ones.

            For the cookies that you specify, your distribution caches separate versions of the specified content based on the cookie values in viewer requests.

            :param cookies_allow_list: The specific cookies to forward to your distribution's origin.
            :param option: Specifies which cookies to forward to the distribution's origin for a cache behavior. Use one of the following configurations for your distribution: - *``all``* - Forwards all cookies to your origin. - *``none``* - Doesn’t forward cookies to your origin. - *``allow-list``* - Forwards only the cookies that you specify using the ``CookiesAllowList`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cookieobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                cookie_object_property = lightsail_mixins.CfnDistributionPropsMixin.CookieObjectProperty(
                    cookies_allow_list=["cookiesAllowList"],
                    option="option"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e382f94294921ac04e32a333799553417ac00956c6cc2fd0470e607693f38d9e)
                check_type(argname="argument cookies_allow_list", value=cookies_allow_list, expected_type=type_hints["cookies_allow_list"])
                check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cookies_allow_list is not None:
                self._values["cookies_allow_list"] = cookies_allow_list
            if option is not None:
                self._values["option"] = option

        @builtins.property
        def cookies_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The specific cookies to forward to your distribution's origin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cookieobject.html#cfn-lightsail-distribution-cookieobject-cookiesallowlist
            '''
            result = self._values.get("cookies_allow_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def option(self) -> typing.Optional[builtins.str]:
            '''Specifies which cookies to forward to the distribution's origin for a cache behavior.

            Use one of the following configurations for your distribution:

            - *``all``* - Forwards all cookies to your origin.
            - *``none``* - Doesn’t forward cookies to your origin.
            - *``allow-list``* - Forwards only the cookies that you specify using the ``CookiesAllowList`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cookieobject.html#cfn-lightsail-distribution-cookieobject-option
            '''
            result = self._values.get("option")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CookieObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.HeaderObjectProperty",
        jsii_struct_bases=[],
        name_mapping={"headers_allow_list": "headersAllowList", "option": "option"},
    )
    class HeaderObjectProperty:
        def __init__(
            self,
            *,
            headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
            option: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``HeaderObject`` is a property of the `CacheSettings <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html>`_ property. It describes the request headers used by your distribution, which caches your content based on the request headers.

            For the headers that you specify, your distribution caches separate versions of the specified content based on the header values in viewer requests. For example, suppose that viewer requests for logo.jpg contain a custom product header that has a value of either acme or apex. Also, suppose that you configure your distribution to cache your content based on values in the product header. Your distribution forwards the product header to the origin and caches the response from the origin once for each header value.

            :param headers_allow_list: The specific headers to forward to your distribution's origin.
            :param option: The headers that you want your distribution to forward to your origin. Your distribution caches your content based on these headers. Use one of the following configurations for your distribution: - *``all``* - Forwards all headers to your origin.. - *``none``* - Forwards only the default headers. - *``allow-list``* - Forwards only the headers that you specify using the ``HeadersAllowList`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-headerobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                header_object_property = lightsail_mixins.CfnDistributionPropsMixin.HeaderObjectProperty(
                    headers_allow_list=["headersAllowList"],
                    option="option"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06dcb8d759c29515bb6d4566be1539ec6426f75f61847728555a91107e926bd6)
                check_type(argname="argument headers_allow_list", value=headers_allow_list, expected_type=type_hints["headers_allow_list"])
                check_type(argname="argument option", value=option, expected_type=type_hints["option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if headers_allow_list is not None:
                self._values["headers_allow_list"] = headers_allow_list
            if option is not None:
                self._values["option"] = option

        @builtins.property
        def headers_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The specific headers to forward to your distribution's origin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-headerobject.html#cfn-lightsail-distribution-headerobject-headersallowlist
            '''
            result = self._values.get("headers_allow_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def option(self) -> typing.Optional[builtins.str]:
            '''The headers that you want your distribution to forward to your origin.

            Your distribution caches your content based on these headers.

            Use one of the following configurations for your distribution:

            - *``all``* - Forwards all headers to your origin..
            - *``none``* - Forwards only the default headers.
            - *``allow-list``* - Forwards only the headers that you specify using the ``HeadersAllowList`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-headerobject.html#cfn-lightsail-distribution-headerobject-option
            '''
            result = self._values.get("option")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.InputOriginProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "protocol_policy": "protocolPolicy",
            "region_name": "regionName",
        },
    )
    class InputOriginProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            protocol_policy: typing.Optional[builtins.str] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``InputOrigin`` is a property of the `AWS::Lightsail::Distribution <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-distribution.html>`_ resource. It describes the origin resource of an Amazon Lightsail content delivery network (CDN) distribution.

            An origin can be a instance, bucket, or load balancer. A distribution pulls content from an origin, caches it, and serves it to viewers through a worldwide network of edge servers.

            :param name: The name of the origin resource.
            :param protocol_policy: The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content.
            :param region_name: The AWS Region name of the origin resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-inputorigin.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                input_origin_property = lightsail_mixins.CfnDistributionPropsMixin.InputOriginProperty(
                    name="name",
                    protocol_policy="protocolPolicy",
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a400724aa6e98a5fbff97f31dc5c5fd2e1ea9bd063285544e0ac8fd747a3af73)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument protocol_policy", value=protocol_policy, expected_type=type_hints["protocol_policy"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if protocol_policy is not None:
                self._values["protocol_policy"] = protocol_policy
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the origin resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-inputorigin.html#cfn-lightsail-distribution-inputorigin-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_policy(self) -> typing.Optional[builtins.str]:
            '''The protocol that your Amazon Lightsail distribution uses when establishing a connection with your origin to pull content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-inputorigin.html#cfn-lightsail-distribution-inputorigin-protocolpolicy
            '''
            result = self._values.get("protocol_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Region name of the origin resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-inputorigin.html#cfn-lightsail-distribution-inputorigin-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputOriginProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDistributionPropsMixin.QueryStringObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "option": "option",
            "query_strings_allow_list": "queryStringsAllowList",
        },
    )
    class QueryStringObjectProperty:
        def __init__(
            self,
            *,
            option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            query_strings_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''``QueryStringObject`` is a property of the `CacheSettings <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-cachesettings.html>`_ property. It describes the query string parameters that an Amazon Lightsail content delivery network (CDN) distribution to bases caching on.

            For the query strings that you specify, your distribution caches separate versions of the specified content based on the query string values in viewer requests.

            :param option: Indicates whether the distribution forwards and caches based on query strings.
            :param query_strings_allow_list: The specific query strings that the distribution forwards to the origin. Your distribution caches content based on the specified query strings. If the ``option`` parameter is true, then your distribution forwards all query strings, regardless of what you specify using the ``QueryStringsAllowList`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-querystringobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                query_string_object_property = lightsail_mixins.CfnDistributionPropsMixin.QueryStringObjectProperty(
                    option=False,
                    query_strings_allow_list=["queryStringsAllowList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a30a38453300d326d81c4095adb4a330267a897879a3a2d0af1707e4fb9b24b2)
                check_type(argname="argument option", value=option, expected_type=type_hints["option"])
                check_type(argname="argument query_strings_allow_list", value=query_strings_allow_list, expected_type=type_hints["query_strings_allow_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if option is not None:
                self._values["option"] = option
            if query_strings_allow_list is not None:
                self._values["query_strings_allow_list"] = query_strings_allow_list

        @builtins.property
        def option(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether the distribution forwards and caches based on query strings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-querystringobject.html#cfn-lightsail-distribution-querystringobject-option
            '''
            result = self._values.get("option")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def query_strings_allow_list(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The specific query strings that the distribution forwards to the origin.

            Your distribution caches content based on the specified query strings.

            If the ``option`` parameter is true, then your distribution forwards all query strings, regardless of what you specify using the ``QueryStringsAllowList`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-distribution-querystringobject.html#cfn-lightsail-distribution-querystringobject-querystringsallowlist
            '''
            result = self._values.get("query_strings_allow_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueryStringObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDomainMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_entries": "domainEntries",
        "domain_name": "domainName",
        "tags": "tags",
    },
)
class CfnDomainMixinProps:
    def __init__(
        self,
        *,
        domain_entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDomainPropsMixin.DomainEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDomainPropsMixin.

        :param domain_entries: An array of key-value pairs containing information about the domain entries.
        :param domain_name: The fully qualified domain name in the certificate request.
        :param tags: The tag keys and optional values for the resource. For more information about tags in Lightsail, see the `Amazon Lightsail Developer Guide <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-tags>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_domain_mixin_props = lightsail_mixins.CfnDomainMixinProps(
                domain_entries=[lightsail_mixins.CfnDomainPropsMixin.DomainEntryProperty(
                    id="id",
                    is_alias=False,
                    name="name",
                    target="target",
                    type="type"
                )],
                domain_name="domainName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da6671f1b16853f406744126b11e343330d4ba01cd74e5e307a0d2d3189fde5d)
            check_type(argname="argument domain_entries", value=domain_entries, expected_type=type_hints["domain_entries"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_entries is not None:
            self._values["domain_entries"] = domain_entries
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_entries(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.DomainEntryProperty"]]]]:
        '''An array of key-value pairs containing information about the domain entries.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-domain.html#cfn-lightsail-domain-domainentries
        '''
        result = self._values.get("domain_entries")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDomainPropsMixin.DomainEntryProperty"]]]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified domain name in the certificate request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-domain.html#cfn-lightsail-domain-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag keys and optional values for the resource.

        For more information about tags in Lightsail, see the `Amazon Lightsail Developer Guide <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-tags>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-domain.html#cfn-lightsail-domain-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDomainPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDomainPropsMixin",
):
    '''Describes a domain where you are storing recordsets.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-domain.html
    :cloudformationResource: AWS::Lightsail::Domain
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_domain_props_mixin = lightsail_mixins.CfnDomainPropsMixin(lightsail_mixins.CfnDomainMixinProps(
            domain_entries=[lightsail_mixins.CfnDomainPropsMixin.DomainEntryProperty(
                id="id",
                is_alias=False,
                name="name",
                target="target",
                type="type"
            )],
            domain_name="domainName",
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
        props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Domain``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36010ba423b98bff0b7bf9c2f11851a6c7e5253356a197718f96095b75418ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a63c7fde922ddeba8db9e1f9ad5ac2b52f9ac1bb418b2bc8808ecb78c3abf17a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213f19a1fd3ebffa7c2989340fd1255ca3b9a9c17d47cc348e3e77933617b92b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDomainMixinProps:
        return typing.cast(CfnDomainMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDomainPropsMixin.DomainEntryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "is_alias": "isAlias",
            "name": "name",
            "target": "target",
            "type": "type",
        },
    )
    class DomainEntryProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            is_alias: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a domain recordset entry.

            :param id: The ID of the domain recordset entry.
            :param is_alias: When ``true`` , specifies whether the domain entry is an alias used by the Lightsail load balancer, Lightsail container service, Lightsail content delivery network (CDN) distribution, or another AWS resource. You can include an alias (A type) record in your request, which points to the DNS name of a load balancer, container service, CDN distribution, or other AWS resource and routes traffic to that resource.
            :param name: The name of the domain.
            :param target: The target IP address ( ``192.0.2.0`` ), or AWS name server ( ``ns-111.awsdns-22.com.`` ). For Lightsail load balancers, the value looks like ``ab1234c56789c6b86aba6fb203d443bc-123456789.us-east-2.elb.amazonaws.com`` . For Lightsail distributions, the value looks like ``exampled1182ne.cloudfront.net`` . For Lightsail container services, the value looks like ``container-service-1.example23scljs.us-west-2.cs.amazonlightsail.com`` . Be sure to also set ``isAlias`` to ``true`` when setting up an A record for a Lightsail load balancer, distribution, or container service.
            :param type: The type of domain entry, such as address for IPv4 (A), address for IPv6 (AAAA), canonical name (CNAME), mail exchanger (MX), name server (NS), start of authority (SOA), service locator (SRV), or text (TXT). The following domain entry types can be used: - ``A`` - ``AAAA`` - ``CNAME`` - ``MX`` - ``NS`` - ``SOA`` - ``SRV`` - ``TXT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-domainentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                domain_entry_property = lightsail_mixins.CfnDomainPropsMixin.DomainEntryProperty(
                    id="id",
                    is_alias=False,
                    name="name",
                    target="target",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f9f4ab48a52b75f554b0e83544394d317d3e6a41f919c8d12af0dc4b37ff94e9)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument is_alias", value=is_alias, expected_type=type_hints["is_alias"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if is_alias is not None:
                self._values["is_alias"] = is_alias
            if name is not None:
                self._values["name"] = name
            if target is not None:
                self._values["target"] = target
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the domain recordset entry.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-domainentry.html#cfn-lightsail-domain-domainentry-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_alias(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''When ``true`` , specifies whether the domain entry is an alias used by the Lightsail load balancer, Lightsail container service, Lightsail content delivery network (CDN) distribution, or another AWS resource.

            You can include an alias (A type) record in your request, which points to the DNS name of a load balancer, container service, CDN distribution, or other AWS resource and routes traffic to that resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-domainentry.html#cfn-lightsail-domain-domainentry-isalias
            '''
            result = self._values.get("is_alias")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-domainentry.html#cfn-lightsail-domain-domainentry-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''The target IP address ( ``192.0.2.0`` ), or AWS name server ( ``ns-111.awsdns-22.com.`` ).

            For Lightsail load balancers, the value looks like ``ab1234c56789c6b86aba6fb203d443bc-123456789.us-east-2.elb.amazonaws.com`` . For Lightsail distributions, the value looks like ``exampled1182ne.cloudfront.net`` . For Lightsail container services, the value looks like ``container-service-1.example23scljs.us-west-2.cs.amazonlightsail.com`` . Be sure to also set ``isAlias`` to ``true`` when setting up an A record for a Lightsail load balancer, distribution, or container service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-domainentry.html#cfn-lightsail-domain-domainentry-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of domain entry, such as address for IPv4 (A), address for IPv6 (AAAA), canonical name (CNAME), mail exchanger (MX), name server (NS), start of authority (SOA), service locator (SRV), or text (TXT).

            The following domain entry types can be used:

            - ``A``
            - ``AAAA``
            - ``CNAME``
            - ``MX``
            - ``NS``
            - ``SOA``
            - ``SRV``
            - ``TXT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-domainentry.html#cfn-lightsail-domain-domainentry-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnDomainPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "region_name": "regionName",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Region and Availability Zone where the domain was created (read-only).

            :param availability_zone: The Availability Zone.
            :param region_name: The AWS Region name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                location_property = lightsail_mixins.CfnDomainPropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__15563ad8e13aef0a6feca82f9b36de9df25e0bd0db05e7bb2e7b392c6b13133b)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-location.html#cfn-lightsail-domain-location-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Region name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-domain-location.html#cfn-lightsail-domain-location-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_ons": "addOns",
        "availability_zone": "availabilityZone",
        "blueprint_id": "blueprintId",
        "bundle_id": "bundleId",
        "hardware": "hardware",
        "instance_name": "instanceName",
        "key_pair_name": "keyPairName",
        "location": "location",
        "networking": "networking",
        "state": "state",
        "tags": "tags",
        "user_data": "userData",
    },
)
class CfnInstanceMixinProps:
    def __init__(
        self,
        *,
        add_ons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.AddOnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        availability_zone: typing.Optional[builtins.str] = None,
        blueprint_id: typing.Optional[builtins.str] = None,
        bundle_id: typing.Optional[builtins.str] = None,
        hardware: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.HardwareProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_name: typing.Optional[builtins.str] = None,
        key_pair_name: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        networking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.NetworkingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.StateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_data: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInstancePropsMixin.

        :param add_ons: An array of add-ons for the instance. .. epigraph:: If the instance has an add-on enabled when performing a delete instance request, the add-on is automatically disabled before the instance is deleted.
        :param availability_zone: The Availability Zone for the instance.
        :param blueprint_id: The blueprint ID for the instance (for example, ``os_amlinux_2016_03`` ).
        :param bundle_id: The bundle ID for the instance (for example, ``micro_1_0`` ).
        :param hardware: The hardware properties for the instance, such as the vCPU count, attached disks, and amount of RAM. .. epigraph:: The instance restarts when performing an attach disk or detach disk request. This resets the public IP address of your instance if a static IP isn't attached to it.
        :param instance_name: The name of the instance.
        :param key_pair_name: The name of the key pair to use for the instance. If no key pair name is specified, the Regional Lightsail default key pair is used.
        :param location: The location for the instance, such as the AWS Region and Availability Zone. .. epigraph:: The ``Location`` property is read-only and should not be specified in a create instance or update instance request.
        :param networking: The public ports and the monthly amount of data transfer allocated for the instance.
        :param state: The status code and the state (for example, ``running`` ) of the instance. .. epigraph:: The ``State`` property is read-only and should not be specified in a create instance or update instance request.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.
        :param user_data: The optional launch script for the instance. Specify a launch script to configure an instance with additional user data. For example, you might want to specify ``apt-get -y update`` as a launch script. .. epigraph:: Depending on the blueprint of your instance, the command to get software on your instance varies. Amazon Linux and CentOS use ``yum`` , Debian and Ubuntu use ``apt-get`` , and FreeBSD uses ``pkg`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_instance_mixin_props = lightsail_mixins.CfnInstanceMixinProps(
                add_ons=[lightsail_mixins.CfnInstancePropsMixin.AddOnProperty(
                    add_on_type="addOnType",
                    auto_snapshot_add_on_request=lightsail_mixins.CfnInstancePropsMixin.AutoSnapshotAddOnProperty(
                        snapshot_time_of_day="snapshotTimeOfDay"
                    ),
                    status="status"
                )],
                availability_zone="availabilityZone",
                blueprint_id="blueprintId",
                bundle_id="bundleId",
                hardware=lightsail_mixins.CfnInstancePropsMixin.HardwareProperty(
                    cpu_count=123,
                    disks=[lightsail_mixins.CfnInstancePropsMixin.DiskProperty(
                        attached_to="attachedTo",
                        attachment_state="attachmentState",
                        disk_name="diskName",
                        iops=123,
                        is_system_disk=False,
                        path="path",
                        size_in_gb="sizeInGb"
                    )],
                    ram_size_in_gb=123
                ),
                instance_name="instanceName",
                key_pair_name="keyPairName",
                location=lightsail_mixins.CfnInstancePropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                ),
                networking=lightsail_mixins.CfnInstancePropsMixin.NetworkingProperty(
                    monthly_transfer=lightsail_mixins.CfnInstancePropsMixin.MonthlyTransferProperty(
                        gb_per_month_allocated="gbPerMonthAllocated"
                    ),
                    ports=[lightsail_mixins.CfnInstancePropsMixin.PortProperty(
                        access_direction="accessDirection",
                        access_from="accessFrom",
                        access_type="accessType",
                        cidr_list_aliases=["cidrListAliases"],
                        cidrs=["cidrs"],
                        common_name="commonName",
                        from_port=123,
                        ipv6_cidrs=["ipv6Cidrs"],
                        protocol="protocol",
                        to_port=123
                    )]
                ),
                state=lightsail_mixins.CfnInstancePropsMixin.StateProperty(
                    code=123,
                    name="name"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_data="userData"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78f219faec21a2d975fe934d7b38f196487b9f8a505d9f7ca01c688042d8b38a)
            check_type(argname="argument add_ons", value=add_ons, expected_type=type_hints["add_ons"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument blueprint_id", value=blueprint_id, expected_type=type_hints["blueprint_id"])
            check_type(argname="argument bundle_id", value=bundle_id, expected_type=type_hints["bundle_id"])
            check_type(argname="argument hardware", value=hardware, expected_type=type_hints["hardware"])
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument key_pair_name", value=key_pair_name, expected_type=type_hints["key_pair_name"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument networking", value=networking, expected_type=type_hints["networking"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_data", value=user_data, expected_type=type_hints["user_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_ons is not None:
            self._values["add_ons"] = add_ons
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if blueprint_id is not None:
            self._values["blueprint_id"] = blueprint_id
        if bundle_id is not None:
            self._values["bundle_id"] = bundle_id
        if hardware is not None:
            self._values["hardware"] = hardware
        if instance_name is not None:
            self._values["instance_name"] = instance_name
        if key_pair_name is not None:
            self._values["key_pair_name"] = key_pair_name
        if location is not None:
            self._values["location"] = location
        if networking is not None:
            self._values["networking"] = networking
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def add_ons(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.AddOnProperty"]]]]:
        '''An array of add-ons for the instance.

        .. epigraph::

           If the instance has an add-on enabled when performing a delete instance request, the add-on is automatically disabled before the instance is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-addons
        '''
        result = self._values.get("add_ons")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.AddOnProperty"]]]], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone for the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blueprint_id(self) -> typing.Optional[builtins.str]:
        '''The blueprint ID for the instance (for example, ``os_amlinux_2016_03`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-blueprintid
        '''
        result = self._values.get("blueprint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bundle_id(self) -> typing.Optional[builtins.str]:
        '''The bundle ID for the instance (for example, ``micro_1_0`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-bundleid
        '''
        result = self._values.get("bundle_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hardware(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.HardwareProperty"]]:
        '''The hardware properties for the instance, such as the vCPU count, attached disks, and amount of RAM.

        .. epigraph::

           The instance restarts when performing an attach disk or detach disk request. This resets the public IP address of your instance if a static IP isn't attached to it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-hardware
        '''
        result = self._values.get("hardware")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.HardwareProperty"]], result)

    @builtins.property
    def instance_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-instancename
        '''
        result = self._values.get("instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_pair_name(self) -> typing.Optional[builtins.str]:
        '''The name of the key pair to use for the instance.

        If no key pair name is specified, the Regional Lightsail default key pair is used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-keypairname
        '''
        result = self._values.get("key_pair_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.LocationProperty"]]:
        '''The location for the instance, such as the AWS Region and Availability Zone.

        .. epigraph::

           The ``Location`` property is read-only and should not be specified in a create instance or update instance request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.LocationProperty"]], result)

    @builtins.property
    def networking(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.NetworkingProperty"]]:
        '''The public ports and the monthly amount of data transfer allocated for the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-networking
        '''
        result = self._values.get("networking")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.NetworkingProperty"]], result)

    @builtins.property
    def state(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.StateProperty"]]:
        '''The status code and the state (for example, ``running`` ) of the instance.

        .. epigraph::

           The ``State`` property is read-only and should not be specified in a create instance or update instance request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.StateProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_data(self) -> typing.Optional[builtins.str]:
        '''The optional launch script for the instance.

        Specify a launch script to configure an instance with additional user data. For example, you might want to specify ``apt-get -y update`` as a launch script.
        .. epigraph::

           Depending on the blueprint of your instance, the command to get software on your instance varies. Amazon Linux and CentOS use ``yum`` , Debian and Ubuntu use ``apt-get`` , and FreeBSD uses ``pkg`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html#cfn-lightsail-instance-userdata
        '''
        result = self._values.get("user_data")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin",
):
    '''The ``AWS::Lightsail::Instance`` resource specifies an Amazon Lightsail instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html
    :cloudformationResource: AWS::Lightsail::Instance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_instance_props_mixin = lightsail_mixins.CfnInstancePropsMixin(lightsail_mixins.CfnInstanceMixinProps(
            add_ons=[lightsail_mixins.CfnInstancePropsMixin.AddOnProperty(
                add_on_type="addOnType",
                auto_snapshot_add_on_request=lightsail_mixins.CfnInstancePropsMixin.AutoSnapshotAddOnProperty(
                    snapshot_time_of_day="snapshotTimeOfDay"
                ),
                status="status"
            )],
            availability_zone="availabilityZone",
            blueprint_id="blueprintId",
            bundle_id="bundleId",
            hardware=lightsail_mixins.CfnInstancePropsMixin.HardwareProperty(
                cpu_count=123,
                disks=[lightsail_mixins.CfnInstancePropsMixin.DiskProperty(
                    attached_to="attachedTo",
                    attachment_state="attachmentState",
                    disk_name="diskName",
                    iops=123,
                    is_system_disk=False,
                    path="path",
                    size_in_gb="sizeInGb"
                )],
                ram_size_in_gb=123
            ),
            instance_name="instanceName",
            key_pair_name="keyPairName",
            location=lightsail_mixins.CfnInstancePropsMixin.LocationProperty(
                availability_zone="availabilityZone",
                region_name="regionName"
            ),
            networking=lightsail_mixins.CfnInstancePropsMixin.NetworkingProperty(
                monthly_transfer=lightsail_mixins.CfnInstancePropsMixin.MonthlyTransferProperty(
                    gb_per_month_allocated="gbPerMonthAllocated"
                ),
                ports=[lightsail_mixins.CfnInstancePropsMixin.PortProperty(
                    access_direction="accessDirection",
                    access_from="accessFrom",
                    access_type="accessType",
                    cidr_list_aliases=["cidrListAliases"],
                    cidrs=["cidrs"],
                    common_name="commonName",
                    from_port=123,
                    ipv6_cidrs=["ipv6Cidrs"],
                    protocol="protocol",
                    to_port=123
                )]
            ),
            state=lightsail_mixins.CfnInstancePropsMixin.StateProperty(
                code=123,
                name="name"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_data="userData"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::Instance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eed61aee1127bacd88b2a6b3dcb92a7e671eba6f47c93a682797e1fb28d6677)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f9537f0d8bc8bb0f60e3c1eb701ec06828ef5fea6cf86cc1e3bbaa8c529100e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cbfef30d060961682293ed464665caf31ee0d0a39fb33aac9400c036e58d5cc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceMixinProps:
        return typing.cast(CfnInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.AddOnProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_on_type": "addOnType",
            "auto_snapshot_add_on_request": "autoSnapshotAddOnRequest",
            "status": "status",
        },
    )
    class AddOnProperty:
        def __init__(
            self,
            *,
            add_on_type: typing.Optional[builtins.str] = None,
            auto_snapshot_add_on_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.AutoSnapshotAddOnProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``AddOn`` is a property of the `AWS::Lightsail::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html>`_ resource. It describes the add-ons for an instance.

            :param add_on_type: The add-on type (for example, ``AutoSnapshot`` ). .. epigraph:: ``AutoSnapshot`` is the only add-on that can be enabled for an instance.
            :param auto_snapshot_add_on_request: The parameters for the automatic snapshot add-on, such as the daily time when an automatic snapshot will be created.
            :param status: The status of the add-on. Valid Values: ``Enabled`` | ``Disabled``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-addon.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                add_on_property = lightsail_mixins.CfnInstancePropsMixin.AddOnProperty(
                    add_on_type="addOnType",
                    auto_snapshot_add_on_request=lightsail_mixins.CfnInstancePropsMixin.AutoSnapshotAddOnProperty(
                        snapshot_time_of_day="snapshotTimeOfDay"
                    ),
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1d68d84dd2df528acab42b5f506dc52997e430a55fda94596c8665a06c0d60d)
                check_type(argname="argument add_on_type", value=add_on_type, expected_type=type_hints["add_on_type"])
                check_type(argname="argument auto_snapshot_add_on_request", value=auto_snapshot_add_on_request, expected_type=type_hints["auto_snapshot_add_on_request"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_on_type is not None:
                self._values["add_on_type"] = add_on_type
            if auto_snapshot_add_on_request is not None:
                self._values["auto_snapshot_add_on_request"] = auto_snapshot_add_on_request
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def add_on_type(self) -> typing.Optional[builtins.str]:
            '''The add-on type (for example, ``AutoSnapshot`` ).

            .. epigraph::

               ``AutoSnapshot`` is the only add-on that can be enabled for an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-addon.html#cfn-lightsail-instance-addon-addontype
            '''
            result = self._values.get("add_on_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def auto_snapshot_add_on_request(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.AutoSnapshotAddOnProperty"]]:
            '''The parameters for the automatic snapshot add-on, such as the daily time when an automatic snapshot will be created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-addon.html#cfn-lightsail-instance-addon-autosnapshotaddonrequest
            '''
            result = self._values.get("auto_snapshot_add_on_request")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.AutoSnapshotAddOnProperty"]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the add-on.

            Valid Values: ``Enabled`` | ``Disabled``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-addon.html#cfn-lightsail-instance-addon-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddOnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.AutoSnapshotAddOnProperty",
        jsii_struct_bases=[],
        name_mapping={"snapshot_time_of_day": "snapshotTimeOfDay"},
    )
    class AutoSnapshotAddOnProperty:
        def __init__(
            self,
            *,
            snapshot_time_of_day: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``AutoSnapshotAddOn`` is a property of the `AddOn <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-addon.html>`_ property. It describes the automatic snapshot add-on for an instance.

            :param snapshot_time_of_day: The daily time when an automatic snapshot will be created. Constraints: - Must be in ``HH:00`` format, and in an hourly increment. - Specified in Coordinated Universal Time (UTC). - The snapshot will be automatically created between the time specified and up to 45 minutes after.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-autosnapshotaddon.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                auto_snapshot_add_on_property = lightsail_mixins.CfnInstancePropsMixin.AutoSnapshotAddOnProperty(
                    snapshot_time_of_day="snapshotTimeOfDay"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab9e1599fa4ce18373c0bf6aa5174d7c906be878455dbd05be4b7e635c094d42)
                check_type(argname="argument snapshot_time_of_day", value=snapshot_time_of_day, expected_type=type_hints["snapshot_time_of_day"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if snapshot_time_of_day is not None:
                self._values["snapshot_time_of_day"] = snapshot_time_of_day

        @builtins.property
        def snapshot_time_of_day(self) -> typing.Optional[builtins.str]:
            '''The daily time when an automatic snapshot will be created.

            Constraints:

            - Must be in ``HH:00`` format, and in an hourly increment.
            - Specified in Coordinated Universal Time (UTC).
            - The snapshot will be automatically created between the time specified and up to 45 minutes after.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-autosnapshotaddon.html#cfn-lightsail-instance-autosnapshotaddon-snapshottimeofday
            '''
            result = self._values.get("snapshot_time_of_day")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoSnapshotAddOnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.DiskProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attached_to": "attachedTo",
            "attachment_state": "attachmentState",
            "disk_name": "diskName",
            "iops": "iops",
            "is_system_disk": "isSystemDisk",
            "path": "path",
            "size_in_gb": "sizeInGb",
        },
    )
    class DiskProperty:
        def __init__(
            self,
            *,
            attached_to: typing.Optional[builtins.str] = None,
            attachment_state: typing.Optional[builtins.str] = None,
            disk_name: typing.Optional[builtins.str] = None,
            iops: typing.Optional[jsii.Number] = None,
            is_system_disk: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            path: typing.Optional[builtins.str] = None,
            size_in_gb: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Disk`` is a property of the `Hardware <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-hardware.html>`_ property. It describes a disk attached to an instance.

            :param attached_to: The resources to which the disk is attached.
            :param attachment_state: (Deprecated) The attachment state of the disk. .. epigraph:: In releases prior to November 14, 2017, this parameter returned ``attached`` for system disks in the API response. It is now deprecated, but still included in the response. Use ``isAttached`` instead.
            :param disk_name: The unique name of the disk.
            :param iops: The input/output operations per second (IOPS) of the disk.
            :param is_system_disk: A Boolean value indicating whether this disk is a system disk (has an operating system loaded on it).
            :param path: The disk path.
            :param size_in_gb: The size of the disk in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                disk_property = lightsail_mixins.CfnInstancePropsMixin.DiskProperty(
                    attached_to="attachedTo",
                    attachment_state="attachmentState",
                    disk_name="diskName",
                    iops=123,
                    is_system_disk=False,
                    path="path",
                    size_in_gb="sizeInGb"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4949ac016b5fa48240c1c99f21e2d718eddf2922089269d7c5a26831473c562)
                check_type(argname="argument attached_to", value=attached_to, expected_type=type_hints["attached_to"])
                check_type(argname="argument attachment_state", value=attachment_state, expected_type=type_hints["attachment_state"])
                check_type(argname="argument disk_name", value=disk_name, expected_type=type_hints["disk_name"])
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument is_system_disk", value=is_system_disk, expected_type=type_hints["is_system_disk"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument size_in_gb", value=size_in_gb, expected_type=type_hints["size_in_gb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attached_to is not None:
                self._values["attached_to"] = attached_to
            if attachment_state is not None:
                self._values["attachment_state"] = attachment_state
            if disk_name is not None:
                self._values["disk_name"] = disk_name
            if iops is not None:
                self._values["iops"] = iops
            if is_system_disk is not None:
                self._values["is_system_disk"] = is_system_disk
            if path is not None:
                self._values["path"] = path
            if size_in_gb is not None:
                self._values["size_in_gb"] = size_in_gb

        @builtins.property
        def attached_to(self) -> typing.Optional[builtins.str]:
            '''The resources to which the disk is attached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-attachedto
            '''
            result = self._values.get("attached_to")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attachment_state(self) -> typing.Optional[builtins.str]:
            '''(Deprecated) The attachment state of the disk.

            .. epigraph::

               In releases prior to November 14, 2017, this parameter returned ``attached`` for system disks in the API response. It is now deprecated, but still included in the response. Use ``isAttached`` instead.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-attachmentstate
            '''
            result = self._values.get("attachment_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk_name(self) -> typing.Optional[builtins.str]:
            '''The unique name of the disk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-diskname
            '''
            result = self._values.get("disk_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The input/output operations per second (IOPS) of the disk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def is_system_disk(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether this disk is a system disk (has an operating system loaded on it).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-issystemdisk
            '''
            result = self._values.get("is_system_disk")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The disk path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def size_in_gb(self) -> typing.Optional[builtins.str]:
            '''The size of the disk in GB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-disk.html#cfn-lightsail-instance-disk-sizeingb
            '''
            result = self._values.get("size_in_gb")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DiskProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.HardwareProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cpu_count": "cpuCount",
            "disks": "disks",
            "ram_size_in_gb": "ramSizeInGb",
        },
    )
    class HardwareProperty:
        def __init__(
            self,
            *,
            cpu_count: typing.Optional[jsii.Number] = None,
            disks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.DiskProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ram_size_in_gb: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``Hardware`` is a property of the `AWS::Lightsail::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html>`_ resource. It describes the hardware properties for the instance, such as the vCPU count, attached disks, and amount of RAM.

            :param cpu_count: The number of vCPUs the instance has. .. epigraph:: The ``CpuCount`` property is read-only and should not be specified in a create instance or update instance request.
            :param disks: The disks attached to the instance. The instance restarts when performing an attach disk or detach disk request. This resets the public IP address of your instance if a static IP isn't attached to it.
            :param ram_size_in_gb: The amount of RAM in GB on the instance (for example, ``1.0`` ). .. epigraph:: The ``RamSizeInGb`` property is read-only and should not be specified in a create instance or update instance request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-hardware.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                hardware_property = lightsail_mixins.CfnInstancePropsMixin.HardwareProperty(
                    cpu_count=123,
                    disks=[lightsail_mixins.CfnInstancePropsMixin.DiskProperty(
                        attached_to="attachedTo",
                        attachment_state="attachmentState",
                        disk_name="diskName",
                        iops=123,
                        is_system_disk=False,
                        path="path",
                        size_in_gb="sizeInGb"
                    )],
                    ram_size_in_gb=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcf70ef3f018d437c634152d797c62ca0d85bbaa34d461524cf3623ec16051cf)
                check_type(argname="argument cpu_count", value=cpu_count, expected_type=type_hints["cpu_count"])
                check_type(argname="argument disks", value=disks, expected_type=type_hints["disks"])
                check_type(argname="argument ram_size_in_gb", value=ram_size_in_gb, expected_type=type_hints["ram_size_in_gb"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpu_count is not None:
                self._values["cpu_count"] = cpu_count
            if disks is not None:
                self._values["disks"] = disks
            if ram_size_in_gb is not None:
                self._values["ram_size_in_gb"] = ram_size_in_gb

        @builtins.property
        def cpu_count(self) -> typing.Optional[jsii.Number]:
            '''The number of vCPUs the instance has.

            .. epigraph::

               The ``CpuCount`` property is read-only and should not be specified in a create instance or update instance request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-hardware.html#cfn-lightsail-instance-hardware-cpucount
            '''
            result = self._values.get("cpu_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def disks(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.DiskProperty"]]]]:
            '''The disks attached to the instance.

            The instance restarts when performing an attach disk or detach disk request. This resets the public IP address of your instance if a static IP isn't attached to it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-hardware.html#cfn-lightsail-instance-hardware-disks
            '''
            result = self._values.get("disks")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.DiskProperty"]]]], result)

        @builtins.property
        def ram_size_in_gb(self) -> typing.Optional[jsii.Number]:
            '''The amount of RAM in GB on the instance (for example, ``1.0`` ).

            .. epigraph::

               The ``RamSizeInGb`` property is read-only and should not be specified in a create instance or update instance request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-hardware.html#cfn-lightsail-instance-hardware-ramsizeingb
            '''
            result = self._values.get("ram_size_in_gb")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HardwareProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "region_name": "regionName",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``Location`` is a property of the `AWS::Lightsail::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html>`_ resource. It describes the location for an instance.

            :param availability_zone: The Availability Zone for the instance.
            :param region_name: The name of the AWS Region for the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                location_property = lightsail_mixins.CfnInstancePropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fba003ee2a965b852c4555fb59bd34548f83902bf233fb20259da74225868fe)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone for the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-location.html#cfn-lightsail-instance-location-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS Region for the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-location.html#cfn-lightsail-instance-location-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.MonthlyTransferProperty",
        jsii_struct_bases=[],
        name_mapping={"gb_per_month_allocated": "gbPerMonthAllocated"},
    )
    class MonthlyTransferProperty:
        def __init__(
            self,
            *,
            gb_per_month_allocated: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``MonthlyTransfer`` is a property of the `Networking <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-networking.html>`_ property. It describes the amount of allocated monthly data transfer (in GB) for an instance.

            :param gb_per_month_allocated: The amount of allocated monthly data transfer (in GB) for an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-monthlytransfer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                monthly_transfer_property = lightsail_mixins.CfnInstancePropsMixin.MonthlyTransferProperty(
                    gb_per_month_allocated="gbPerMonthAllocated"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2c687fadc9faa81b47830a8fbcb90ad9dfad0036c34a7358eff8f1e0cd44bfc)
                check_type(argname="argument gb_per_month_allocated", value=gb_per_month_allocated, expected_type=type_hints["gb_per_month_allocated"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gb_per_month_allocated is not None:
                self._values["gb_per_month_allocated"] = gb_per_month_allocated

        @builtins.property
        def gb_per_month_allocated(self) -> typing.Optional[builtins.str]:
            '''The amount of allocated monthly data transfer (in GB) for an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-monthlytransfer.html#cfn-lightsail-instance-monthlytransfer-gbpermonthallocated
            '''
            result = self._values.get("gb_per_month_allocated")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonthlyTransferProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.NetworkingProperty",
        jsii_struct_bases=[],
        name_mapping={"monthly_transfer": "monthlyTransfer", "ports": "ports"},
    )
    class NetworkingProperty:
        def __init__(
            self,
            *,
            monthly_transfer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.MonthlyTransferProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.PortProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''``Networking`` is a property of the `AWS::Lightsail::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html>`_ resource. It describes the public ports and the monthly amount of data transfer allocated for the instance.

            :param monthly_transfer: The monthly amount of data transfer, in GB, allocated for the instance.
            :param ports: An array of ports to open on the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-networking.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                networking_property = lightsail_mixins.CfnInstancePropsMixin.NetworkingProperty(
                    monthly_transfer=lightsail_mixins.CfnInstancePropsMixin.MonthlyTransferProperty(
                        gb_per_month_allocated="gbPerMonthAllocated"
                    ),
                    ports=[lightsail_mixins.CfnInstancePropsMixin.PortProperty(
                        access_direction="accessDirection",
                        access_from="accessFrom",
                        access_type="accessType",
                        cidr_list_aliases=["cidrListAliases"],
                        cidrs=["cidrs"],
                        common_name="commonName",
                        from_port=123,
                        ipv6_cidrs=["ipv6Cidrs"],
                        protocol="protocol",
                        to_port=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc6405aefb7bd66d95df4b7287bcdb884ae025743771dd24256c2da606a62e4d)
                check_type(argname="argument monthly_transfer", value=monthly_transfer, expected_type=type_hints["monthly_transfer"])
                check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if monthly_transfer is not None:
                self._values["monthly_transfer"] = monthly_transfer
            if ports is not None:
                self._values["ports"] = ports

        @builtins.property
        def monthly_transfer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.MonthlyTransferProperty"]]:
            '''The monthly amount of data transfer, in GB, allocated for the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-networking.html#cfn-lightsail-instance-networking-monthlytransfer
            '''
            result = self._values.get("monthly_transfer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.MonthlyTransferProperty"]], result)

        @builtins.property
        def ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.PortProperty"]]]]:
            '''An array of ports to open on the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-networking.html#cfn-lightsail-instance-networking-ports
            '''
            result = self._values.get("ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.PortProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.PortProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_direction": "accessDirection",
            "access_from": "accessFrom",
            "access_type": "accessType",
            "cidr_list_aliases": "cidrListAliases",
            "cidrs": "cidrs",
            "common_name": "commonName",
            "from_port": "fromPort",
            "ipv6_cidrs": "ipv6Cidrs",
            "protocol": "protocol",
            "to_port": "toPort",
        },
    )
    class PortProperty:
        def __init__(
            self,
            *,
            access_direction: typing.Optional[builtins.str] = None,
            access_from: typing.Optional[builtins.str] = None,
            access_type: typing.Optional[builtins.str] = None,
            cidr_list_aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
            cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
            common_name: typing.Optional[builtins.str] = None,
            from_port: typing.Optional[jsii.Number] = None,
            ipv6_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
            protocol: typing.Optional[builtins.str] = None,
            to_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''``Port`` is a property of the `Networking <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-networking.html>`_ property. It describes information about ports for an instance.

            :param access_direction: The access direction ( ``inbound`` or ``outbound`` ). .. epigraph:: Lightsail currently supports only ``inbound`` access direction.
            :param access_from: The location from which access is allowed. For example, ``Anywhere (0.0.0.0/0)`` , or ``Custom`` if a specific IP address or range of IP addresses is allowed.
            :param access_type: The type of access ( ``Public`` or ``Private`` ).
            :param cidr_list_aliases: An alias that defines access for a preconfigured range of IP addresses. The only alias currently supported is ``lightsail-connect`` , which allows IP addresses of the browser-based RDP/SSH client in the Lightsail console to connect to your instance.
            :param cidrs: The IPv4 address, or range of IPv4 addresses (in CIDR notation) that are allowed to connect to an instance through the ports, and the protocol. .. epigraph:: The ``ipv6Cidrs`` parameter lists the IPv6 addresses that are allowed to connect to an instance. Examples: - To allow the IP address ``192.0.2.44`` , specify ``192.0.2.44`` or ``192.0.2.44/32`` . - To allow the IP addresses ``192.0.2.0`` to ``192.0.2.255`` , specify ``192.0.2.0/24`` .
            :param common_name: The common name of the port information.
            :param from_port: The first port in a range of open ports on an instance. Allowed ports: - TCP and UDP - ``0`` to ``65535`` - ICMP - The ICMP type for IPv4 addresses. For example, specify ``8`` as the ``fromPort`` (ICMP type), and ``-1`` as the ``toPort`` (ICMP code), to enable ICMP Ping. - ICMPv6 - The ICMP type for IPv6 addresses. For example, specify ``128`` as the ``fromPort`` (ICMPv6 type), and ``0`` as ``toPort`` (ICMPv6 code).
            :param ipv6_cidrs: The IPv6 address, or range of IPv6 addresses (in CIDR notation) that are allowed to connect to an instance through the ports, and the protocol. Only devices with an IPv6 address can connect to an instance through IPv6; otherwise, IPv4 should be used. .. epigraph:: The ``cidrs`` parameter lists the IPv4 addresses that are allowed to connect to an instance.
            :param protocol: The IP protocol name. The name can be one of the following: - ``tcp`` - Transmission Control Protocol (TCP) provides reliable, ordered, and error-checked delivery of streamed data between applications running on hosts communicating by an IP network. If you have an application that doesn't require reliable data stream service, use UDP instead. - ``all`` - All transport layer protocol types. - ``udp`` - With User Datagram Protocol (UDP), computer applications can send messages (or datagrams) to other hosts on an Internet Protocol (IP) network. Prior communications are not required to set up transmission channels or data paths. Applications that don't require reliable data stream service can use UDP, which provides a connectionless datagram service that emphasizes reduced latency over reliability. If you do require reliable data stream service, use TCP instead. - ``icmp`` - Internet Control Message Protocol (ICMP) is used to send error messages and operational information indicating success or failure when communicating with an instance. For example, an error is indicated when an instance could not be reached. When you specify ``icmp`` as the ``protocol`` , you must specify the ICMP type using the ``fromPort`` parameter, and ICMP code using the ``toPort`` parameter.
            :param to_port: The last port in a range of open ports on an instance. Allowed ports: - TCP and UDP - ``0`` to ``65535`` - ICMP - The ICMP code for IPv4 addresses. For example, specify ``8`` as the ``fromPort`` (ICMP type), and ``-1`` as the ``toPort`` (ICMP code), to enable ICMP Ping. - ICMPv6 - The ICMP code for IPv6 addresses. For example, specify ``128`` as the ``fromPort`` (ICMPv6 type), and ``0`` as ``toPort`` (ICMPv6 code).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                port_property = lightsail_mixins.CfnInstancePropsMixin.PortProperty(
                    access_direction="accessDirection",
                    access_from="accessFrom",
                    access_type="accessType",
                    cidr_list_aliases=["cidrListAliases"],
                    cidrs=["cidrs"],
                    common_name="commonName",
                    from_port=123,
                    ipv6_cidrs=["ipv6Cidrs"],
                    protocol="protocol",
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__392ef54f46283c6f3ac96036f850aa043fd2f9ee24285526a4908ef7ce95dd34)
                check_type(argname="argument access_direction", value=access_direction, expected_type=type_hints["access_direction"])
                check_type(argname="argument access_from", value=access_from, expected_type=type_hints["access_from"])
                check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
                check_type(argname="argument cidr_list_aliases", value=cidr_list_aliases, expected_type=type_hints["cidr_list_aliases"])
                check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
                check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument ipv6_cidrs", value=ipv6_cidrs, expected_type=type_hints["ipv6_cidrs"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_direction is not None:
                self._values["access_direction"] = access_direction
            if access_from is not None:
                self._values["access_from"] = access_from
            if access_type is not None:
                self._values["access_type"] = access_type
            if cidr_list_aliases is not None:
                self._values["cidr_list_aliases"] = cidr_list_aliases
            if cidrs is not None:
                self._values["cidrs"] = cidrs
            if common_name is not None:
                self._values["common_name"] = common_name
            if from_port is not None:
                self._values["from_port"] = from_port
            if ipv6_cidrs is not None:
                self._values["ipv6_cidrs"] = ipv6_cidrs
            if protocol is not None:
                self._values["protocol"] = protocol
            if to_port is not None:
                self._values["to_port"] = to_port

        @builtins.property
        def access_direction(self) -> typing.Optional[builtins.str]:
            '''The access direction ( ``inbound`` or ``outbound`` ).

            .. epigraph::

               Lightsail currently supports only ``inbound`` access direction.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-accessdirection
            '''
            result = self._values.get("access_direction")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def access_from(self) -> typing.Optional[builtins.str]:
            '''The location from which access is allowed.

            For example, ``Anywhere (0.0.0.0/0)`` , or ``Custom`` if a specific IP address or range of IP addresses is allowed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-accessfrom
            '''
            result = self._values.get("access_from")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def access_type(self) -> typing.Optional[builtins.str]:
            '''The type of access ( ``Public`` or ``Private`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-accesstype
            '''
            result = self._values.get("access_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def cidr_list_aliases(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An alias that defines access for a preconfigured range of IP addresses.

            The only alias currently supported is ``lightsail-connect`` , which allows IP addresses of the browser-based RDP/SSH client in the Lightsail console to connect to your instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-cidrlistaliases
            '''
            result = self._values.get("cidr_list_aliases")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IPv4 address, or range of IPv4 addresses (in CIDR notation) that are allowed to connect to an instance through the ports, and the protocol.

            .. epigraph::

               The ``ipv6Cidrs`` parameter lists the IPv6 addresses that are allowed to connect to an instance.

            Examples:

            - To allow the IP address ``192.0.2.44`` , specify ``192.0.2.44`` or ``192.0.2.44/32`` .
            - To allow the IP addresses ``192.0.2.0`` to ``192.0.2.255`` , specify ``192.0.2.0/24`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-cidrs
            '''
            result = self._values.get("cidrs")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            '''The common name of the port information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-commonname
            '''
            result = self._values.get("common_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def from_port(self) -> typing.Optional[jsii.Number]:
            '''The first port in a range of open ports on an instance.

            Allowed ports:

            - TCP and UDP - ``0`` to ``65535``
            - ICMP - The ICMP type for IPv4 addresses. For example, specify ``8`` as the ``fromPort`` (ICMP type), and ``-1`` as the ``toPort`` (ICMP code), to enable ICMP Ping.
            - ICMPv6 - The ICMP type for IPv6 addresses. For example, specify ``128`` as the ``fromPort`` (ICMPv6 type), and ``0`` as ``toPort`` (ICMPv6 code).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-fromport
            '''
            result = self._values.get("from_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ipv6_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The IPv6 address, or range of IPv6 addresses (in CIDR notation) that are allowed to connect to an instance through the ports, and the protocol.

            Only devices with an IPv6 address can connect to an instance through IPv6; otherwise, IPv4 should be used.
            .. epigraph::

               The ``cidrs`` parameter lists the IPv4 addresses that are allowed to connect to an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-ipv6cidrs
            '''
            result = self._values.get("ipv6_cidrs")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The IP protocol name.

            The name can be one of the following:

            - ``tcp`` - Transmission Control Protocol (TCP) provides reliable, ordered, and error-checked delivery of streamed data between applications running on hosts communicating by an IP network. If you have an application that doesn't require reliable data stream service, use UDP instead.
            - ``all`` - All transport layer protocol types.
            - ``udp`` - With User Datagram Protocol (UDP), computer applications can send messages (or datagrams) to other hosts on an Internet Protocol (IP) network. Prior communications are not required to set up transmission channels or data paths. Applications that don't require reliable data stream service can use UDP, which provides a connectionless datagram service that emphasizes reduced latency over reliability. If you do require reliable data stream service, use TCP instead.
            - ``icmp`` - Internet Control Message Protocol (ICMP) is used to send error messages and operational information indicating success or failure when communicating with an instance. For example, an error is indicated when an instance could not be reached. When you specify ``icmp`` as the ``protocol`` , you must specify the ICMP type using the ``fromPort`` parameter, and ICMP code using the ``toPort`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def to_port(self) -> typing.Optional[jsii.Number]:
            '''The last port in a range of open ports on an instance.

            Allowed ports:

            - TCP and UDP - ``0`` to ``65535``
            - ICMP - The ICMP code for IPv4 addresses. For example, specify ``8`` as the ``fromPort`` (ICMP type), and ``-1`` as the ``toPort`` (ICMP code), to enable ICMP Ping.
            - ICMPv6 - The ICMP code for IPv6 addresses. For example, specify ``128`` as the ``fromPort`` (ICMPv6 type), and ``0`` as ``toPort`` (ICMPv6 code).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-port.html#cfn-lightsail-instance-port-toport
            '''
            result = self._values.get("to_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstancePropsMixin.StateProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "name": "name"},
    )
    class StateProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``State`` is a property of the `AWS::Lightsail::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instance.html>`_ resource. It describes the status code and the state (for example, ``running`` ) of an instance.

            :param code: The status code of the instance.
            :param name: The state of the instance (for example, ``running`` or ``pending`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-state.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                state_property = lightsail_mixins.CfnInstancePropsMixin.StateProperty(
                    code=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f224011fa173a70c8dbc4549ec610a5638f4aaaac31d1a5e934dee7bc2737811)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def code(self) -> typing.Optional[jsii.Number]:
            '''The status code of the instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-state.html#cfn-lightsail-instance-state-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The state of the instance (for example, ``running`` or ``pending`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instance-state.html#cfn-lightsail-instance-state-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstanceSnapshotMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_name": "instanceName",
        "instance_snapshot_name": "instanceSnapshotName",
        "tags": "tags",
    },
)
class CfnInstanceSnapshotMixinProps:
    def __init__(
        self,
        *,
        instance_name: typing.Optional[builtins.str] = None,
        instance_snapshot_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInstanceSnapshotPropsMixin.

        :param instance_name: The name the user gave the instance ( ``Amazon_Linux_2023-1`` ).
        :param instance_snapshot_name: The name of the snapshot.
        :param tags: The tag keys and optional values for the resource. For more information about tags in Lightsail, see the `Amazon Lightsail Developer Guide <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-tags>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instancesnapshot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_instance_snapshot_mixin_props = lightsail_mixins.CfnInstanceSnapshotMixinProps(
                instance_name="instanceName",
                instance_snapshot_name="instanceSnapshotName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382c6df5172e936388696072b07796ae03e3c6a028e3f1883fa96ec76d65a211)
            check_type(argname="argument instance_name", value=instance_name, expected_type=type_hints["instance_name"])
            check_type(argname="argument instance_snapshot_name", value=instance_snapshot_name, expected_type=type_hints["instance_snapshot_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_name is not None:
            self._values["instance_name"] = instance_name
        if instance_snapshot_name is not None:
            self._values["instance_snapshot_name"] = instance_snapshot_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_name(self) -> typing.Optional[builtins.str]:
        '''The name the user gave the instance ( ``Amazon_Linux_2023-1`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instancesnapshot.html#cfn-lightsail-instancesnapshot-instancename
        '''
        result = self._values.get("instance_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_snapshot_name(self) -> typing.Optional[builtins.str]:
        '''The name of the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instancesnapshot.html#cfn-lightsail-instancesnapshot-instancesnapshotname
        '''
        result = self._values.get("instance_snapshot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag keys and optional values for the resource.

        For more information about tags in Lightsail, see the `Amazon Lightsail Developer Guide <https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-tags>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instancesnapshot.html#cfn-lightsail-instancesnapshot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceSnapshotMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceSnapshotPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstanceSnapshotPropsMixin",
):
    '''Describes an instance snapshot.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-instancesnapshot.html
    :cloudformationResource: AWS::Lightsail::InstanceSnapshot
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_instance_snapshot_props_mixin = lightsail_mixins.CfnInstanceSnapshotPropsMixin(lightsail_mixins.CfnInstanceSnapshotMixinProps(
            instance_name="instanceName",
            instance_snapshot_name="instanceSnapshotName",
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
        props: typing.Union[CfnInstanceSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::InstanceSnapshot``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8dffd6454db0421cb8036738bc9d4284965466e3babccf40706c3405046f77a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c964702a52c47ba47944f2d41ae88e4bfb9a52a19c28e4949cbcf0f21833d47)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6c28f63ff4080750a6a8586e8f3c1d3c5e9c65265f9ef20fa5e2e6b000a1f3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceSnapshotMixinProps:
        return typing.cast(CfnInstanceSnapshotMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnInstanceSnapshotPropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "region_name": "regionName",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            region_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The region name and Availability Zone where you created the snapshot.

            :param availability_zone: The Availability Zone. Follows the format us-east-2a (case-sensitive).
            :param region_name: The AWS Region name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instancesnapshot-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
                
                location_property = lightsail_mixins.CfnInstanceSnapshotPropsMixin.LocationProperty(
                    availability_zone="availabilityZone",
                    region_name="regionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d7914235ebca539686d6fd62fdb6050940c0b08010ddcec0a542c2aa239dc94)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument region_name", value=region_name, expected_type=type_hints["region_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if region_name is not None:
                self._values["region_name"] = region_name

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone.

            Follows the format us-east-2a (case-sensitive).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instancesnapshot-location.html#cfn-lightsail-instancesnapshot-location-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Region name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lightsail-instancesnapshot-location.html#cfn-lightsail-instancesnapshot-location-regionname
            '''
            result = self._values.get("region_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnLoadBalancerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attached_instances": "attachedInstances",
        "health_check_path": "healthCheckPath",
        "instance_port": "instancePort",
        "ip_address_type": "ipAddressType",
        "load_balancer_name": "loadBalancerName",
        "session_stickiness_enabled": "sessionStickinessEnabled",
        "session_stickiness_lb_cookie_duration_seconds": "sessionStickinessLbCookieDurationSeconds",
        "tags": "tags",
        "tls_policy_name": "tlsPolicyName",
    },
)
class CfnLoadBalancerMixinProps:
    def __init__(
        self,
        *,
        attached_instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        instance_port: typing.Optional[jsii.Number] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        session_stickiness_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        session_stickiness_lb_cookie_duration_seconds: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        tls_policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLoadBalancerPropsMixin.

        :param attached_instances: The Lightsail instances to attach to the load balancer.
        :param health_check_path: The path on the attached instance where the health check will be performed. If no path is specified, the load balancer tries to make a request to the default (root) page ( ``/index.html`` ).
        :param instance_port: The port that the load balancer uses to direct traffic to your Lightsail instances. For HTTP traffic, specify port ``80`` . For HTTPS traffic, specify port ``443`` .
        :param ip_address_type: The IP address type of the load balancer. The possible values are ``ipv4`` for IPv4 only, and ``dualstack`` for both IPv4 and IPv6.
        :param load_balancer_name: The name of the load balancer.
        :param session_stickiness_enabled: A Boolean value indicating whether session stickiness is enabled. Enable session stickiness (also known as *session affinity* ) to bind a user's session to a specific instance. This ensures that all requests from the user during the session are sent to the same instance.
        :param session_stickiness_lb_cookie_duration_seconds: The time period, in seconds, after which the load balancer session stickiness cookie should be considered stale. If you do not specify this parameter, the default value is 0, which indicates that the sticky session should last for the duration of the browser session.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* . .. epigraph:: The ``Value`` of ``Tags`` is optional for Lightsail resources.
        :param tls_policy_name: The name of the TLS security policy for the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_load_balancer_mixin_props = lightsail_mixins.CfnLoadBalancerMixinProps(
                attached_instances=["attachedInstances"],
                health_check_path="healthCheckPath",
                instance_port=123,
                ip_address_type="ipAddressType",
                load_balancer_name="loadBalancerName",
                session_stickiness_enabled=False,
                session_stickiness_lb_cookie_duration_seconds="sessionStickinessLbCookieDurationSeconds",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                tls_policy_name="tlsPolicyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__851d2c2ffee133a2ab841ff3145be43ea91a6bd5e7f30eca3f1e0593651dbe23)
            check_type(argname="argument attached_instances", value=attached_instances, expected_type=type_hints["attached_instances"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument instance_port", value=instance_port, expected_type=type_hints["instance_port"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument session_stickiness_enabled", value=session_stickiness_enabled, expected_type=type_hints["session_stickiness_enabled"])
            check_type(argname="argument session_stickiness_lb_cookie_duration_seconds", value=session_stickiness_lb_cookie_duration_seconds, expected_type=type_hints["session_stickiness_lb_cookie_duration_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tls_policy_name", value=tls_policy_name, expected_type=type_hints["tls_policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attached_instances is not None:
            self._values["attached_instances"] = attached_instances
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if instance_port is not None:
            self._values["instance_port"] = instance_port
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if session_stickiness_enabled is not None:
            self._values["session_stickiness_enabled"] = session_stickiness_enabled
        if session_stickiness_lb_cookie_duration_seconds is not None:
            self._values["session_stickiness_lb_cookie_duration_seconds"] = session_stickiness_lb_cookie_duration_seconds
        if tags is not None:
            self._values["tags"] = tags
        if tls_policy_name is not None:
            self._values["tls_policy_name"] = tls_policy_name

    @builtins.property
    def attached_instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Lightsail instances to attach to the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-attachedinstances
        '''
        result = self._values.get("attached_instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''The path on the attached instance where the health check will be performed.

        If no path is specified, the load balancer tries to make a request to the default (root) page ( ``/index.html`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-healthcheckpath
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_port(self) -> typing.Optional[jsii.Number]:
        '''The port that the load balancer uses to direct traffic to your Lightsail instances.

        For HTTP traffic, specify port ``80`` . For HTTPS traffic, specify port ``443`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-instanceport
        '''
        result = self._values.get("instance_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''The IP address type of the load balancer.

        The possible values are ``ipv4`` for IPv4 only, and ``dualstack`` for both IPv4 and IPv6.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-loadbalancername
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_stickiness_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether session stickiness is enabled.

        Enable session stickiness (also known as *session affinity* ) to bind a user's session to a specific instance. This ensures that all requests from the user during the session are sent to the same instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-sessionstickinessenabled
        '''
        result = self._values.get("session_stickiness_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def session_stickiness_lb_cookie_duration_seconds(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The time period, in seconds, after which the load balancer session stickiness cookie should be considered stale.

        If you do not specify this parameter, the default value is 0, which indicates that the sticky session should last for the duration of the browser session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-sessionstickinesslbcookiedurationseconds
        '''
        result = self._values.get("session_stickiness_lb_cookie_duration_seconds")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ in the *AWS CloudFormation User Guide* .
        .. epigraph::

           The ``Value`` of ``Tags`` is optional for Lightsail resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def tls_policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the TLS security policy for the load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html#cfn-lightsail-loadbalancer-tlspolicyname
        '''
        result = self._values.get("tls_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoadBalancerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnLoadBalancerPropsMixin",
):
    '''The ``AWS::Lightsail::LoadBalancer`` resource specifies a load balancer that can be used with Lightsail instances.

    .. epigraph::

       You cannot attach a TLS certificate to a load balancer using the ``AWS::Lightsail::LoadBalancer`` resource type. Instead, use the ``AWS::Lightsail::LoadBalancerTlsCertificate`` resource type to create a certificate and attach it to a load balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancer.html
    :cloudformationResource: AWS::Lightsail::LoadBalancer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_load_balancer_props_mixin = lightsail_mixins.CfnLoadBalancerPropsMixin(lightsail_mixins.CfnLoadBalancerMixinProps(
            attached_instances=["attachedInstances"],
            health_check_path="healthCheckPath",
            instance_port=123,
            ip_address_type="ipAddressType",
            load_balancer_name="loadBalancerName",
            session_stickiness_enabled=False,
            session_stickiness_lb_cookie_duration_seconds="sessionStickinessLbCookieDurationSeconds",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            tls_policy_name="tlsPolicyName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLoadBalancerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::LoadBalancer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570f32af544a85d7ca54153794f4bc345323f52eca33dcdd90a9f38243205188)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6390764d14660c19c85b674efb0532902110727c776c3119e7d73a760335145)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a73439c892011bc5fca80fa9a51d633fe78ef8e575ad876921f737f35ca169a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoadBalancerMixinProps:
        return typing.cast(CfnLoadBalancerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnLoadBalancerTlsCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_alternative_names": "certificateAlternativeNames",
        "certificate_domain_name": "certificateDomainName",
        "certificate_name": "certificateName",
        "https_redirection_enabled": "httpsRedirectionEnabled",
        "is_attached": "isAttached",
        "load_balancer_name": "loadBalancerName",
    },
)
class CfnLoadBalancerTlsCertificateMixinProps:
    def __init__(
        self,
        *,
        certificate_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificate_domain_name: typing.Optional[builtins.str] = None,
        certificate_name: typing.Optional[builtins.str] = None,
        https_redirection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        is_attached: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLoadBalancerTlsCertificatePropsMixin.

        :param certificate_alternative_names: An array of alternative domain names and subdomain names for your SSL/TLS certificate. In addition to the primary domain name, you can have up to nine alternative domain names. Wildcards (such as ``*.example.com`` ) are not supported.
        :param certificate_domain_name: The domain name for the SSL/TLS certificate. For example, ``example.com`` or ``www.example.com`` .
        :param certificate_name: The name of the SSL/TLS certificate.
        :param https_redirection_enabled: A Boolean value indicating whether HTTPS redirection is enabled for the load balancer that the TLS certificate is attached to.
        :param is_attached: A Boolean value indicating whether the SSL/TLS certificate is attached to a Lightsail load balancer.
        :param load_balancer_name: The name of the load balancer that the SSL/TLS certificate is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_load_balancer_tls_certificate_mixin_props = lightsail_mixins.CfnLoadBalancerTlsCertificateMixinProps(
                certificate_alternative_names=["certificateAlternativeNames"],
                certificate_domain_name="certificateDomainName",
                certificate_name="certificateName",
                https_redirection_enabled=False,
                is_attached=False,
                load_balancer_name="loadBalancerName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c84d491d542d7e62a077c8cfdb5d537cd730087a6545d44723c0bc191abe70d2)
            check_type(argname="argument certificate_alternative_names", value=certificate_alternative_names, expected_type=type_hints["certificate_alternative_names"])
            check_type(argname="argument certificate_domain_name", value=certificate_domain_name, expected_type=type_hints["certificate_domain_name"])
            check_type(argname="argument certificate_name", value=certificate_name, expected_type=type_hints["certificate_name"])
            check_type(argname="argument https_redirection_enabled", value=https_redirection_enabled, expected_type=type_hints["https_redirection_enabled"])
            check_type(argname="argument is_attached", value=is_attached, expected_type=type_hints["is_attached"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_alternative_names is not None:
            self._values["certificate_alternative_names"] = certificate_alternative_names
        if certificate_domain_name is not None:
            self._values["certificate_domain_name"] = certificate_domain_name
        if certificate_name is not None:
            self._values["certificate_name"] = certificate_name
        if https_redirection_enabled is not None:
            self._values["https_redirection_enabled"] = https_redirection_enabled
        if is_attached is not None:
            self._values["is_attached"] = is_attached
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name

    @builtins.property
    def certificate_alternative_names(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of alternative domain names and subdomain names for your SSL/TLS certificate.

        In addition to the primary domain name, you can have up to nine alternative domain names. Wildcards (such as ``*.example.com`` ) are not supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html#cfn-lightsail-loadbalancertlscertificate-certificatealternativenames
        '''
        result = self._values.get("certificate_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificate_domain_name(self) -> typing.Optional[builtins.str]:
        '''The domain name for the SSL/TLS certificate.

        For example, ``example.com`` or ``www.example.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html#cfn-lightsail-loadbalancertlscertificate-certificatedomainname
        '''
        result = self._values.get("certificate_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name of the SSL/TLS certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html#cfn-lightsail-loadbalancertlscertificate-certificatename
        '''
        result = self._values.get("certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_redirection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether HTTPS redirection is enabled for the load balancer that the TLS certificate is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html#cfn-lightsail-loadbalancertlscertificate-httpsredirectionenabled
        '''
        result = self._values.get("https_redirection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def is_attached(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A Boolean value indicating whether the SSL/TLS certificate is attached to a Lightsail load balancer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html#cfn-lightsail-loadbalancertlscertificate-isattached
        '''
        result = self._values.get("is_attached")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''The name of the load balancer that the SSL/TLS certificate is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html#cfn-lightsail-loadbalancertlscertificate-loadbalancername
        '''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoadBalancerTlsCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLoadBalancerTlsCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnLoadBalancerTlsCertificatePropsMixin",
):
    '''The ``AWS::Lightsail::LoadBalancerTlsCertificate`` resource specifies a TLS certificate that can be used with a Lightsail load balancer.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-loadbalancertlscertificate.html
    :cloudformationResource: AWS::Lightsail::LoadBalancerTlsCertificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_load_balancer_tls_certificate_props_mixin = lightsail_mixins.CfnLoadBalancerTlsCertificatePropsMixin(lightsail_mixins.CfnLoadBalancerTlsCertificateMixinProps(
            certificate_alternative_names=["certificateAlternativeNames"],
            certificate_domain_name="certificateDomainName",
            certificate_name="certificateName",
            https_redirection_enabled=False,
            is_attached=False,
            load_balancer_name="loadBalancerName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLoadBalancerTlsCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::LoadBalancerTlsCertificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fba978d652928178e1e0d6ee27d0c76f9ba17fa6f40c452c636d36afe1165bce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5593cad554a4309bca25bced99771b5f3b3b6c93b0025c43d490c68a905b89ee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7923ed65c49d97ce179b79efc4c3124df571addfae877723b80ec261257254a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLoadBalancerTlsCertificateMixinProps:
        return typing.cast(CfnLoadBalancerTlsCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnStaticIpMixinProps",
    jsii_struct_bases=[],
    name_mapping={"attached_to": "attachedTo", "static_ip_name": "staticIpName"},
)
class CfnStaticIpMixinProps:
    def __init__(
        self,
        *,
        attached_to: typing.Optional[builtins.str] = None,
        static_ip_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnStaticIpPropsMixin.

        :param attached_to: The instance that the static IP is attached to.
        :param static_ip_name: The name of the static IP.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-staticip.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
            
            cfn_static_ip_mixin_props = lightsail_mixins.CfnStaticIpMixinProps(
                attached_to="attachedTo",
                static_ip_name="staticIpName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2db7f8d1ccd29c22f982df8ca5fe6c1c6bc0724d7598f14a3530a49adfa465)
            check_type(argname="argument attached_to", value=attached_to, expected_type=type_hints["attached_to"])
            check_type(argname="argument static_ip_name", value=static_ip_name, expected_type=type_hints["static_ip_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attached_to is not None:
            self._values["attached_to"] = attached_to
        if static_ip_name is not None:
            self._values["static_ip_name"] = static_ip_name

    @builtins.property
    def attached_to(self) -> typing.Optional[builtins.str]:
        '''The instance that the static IP is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-staticip.html#cfn-lightsail-staticip-attachedto
        '''
        result = self._values.get("attached_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def static_ip_name(self) -> typing.Optional[builtins.str]:
        '''The name of the static IP.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-staticip.html#cfn-lightsail-staticip-staticipname
        '''
        result = self._values.get("static_ip_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStaticIpMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStaticIpPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lightsail.mixins.CfnStaticIpPropsMixin",
):
    '''The ``AWS::Lightsail::StaticIp`` resource specifies a static IP that can be attached to an Amazon Lightsail instance that is in the same AWS Region and Availability Zone.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lightsail-staticip.html
    :cloudformationResource: AWS::Lightsail::StaticIp
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lightsail import mixins as lightsail_mixins
        
        cfn_static_ip_props_mixin = lightsail_mixins.CfnStaticIpPropsMixin(lightsail_mixins.CfnStaticIpMixinProps(
            attached_to="attachedTo",
            static_ip_name="staticIpName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnStaticIpMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Lightsail::StaticIp``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__800915f18d9816972a07253443adc485ed60928e21ad05c135c198f8fa71c44c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11059417ea4f236188aa223a84f2c6d84fb9773966bb919e99c41b7bd6e208d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef71a8cbebe7a2312ff7da37bfd133b594fef14faa1df29d054abc15333f75c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStaticIpMixinProps:
        return typing.cast(CfnStaticIpMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAlarmMixinProps",
    "CfnAlarmPropsMixin",
    "CfnBucketMixinProps",
    "CfnBucketPropsMixin",
    "CfnCertificateMixinProps",
    "CfnCertificatePropsMixin",
    "CfnContainerMixinProps",
    "CfnContainerPropsMixin",
    "CfnDatabaseMixinProps",
    "CfnDatabasePropsMixin",
    "CfnDiskMixinProps",
    "CfnDiskPropsMixin",
    "CfnDiskSnapshotMixinProps",
    "CfnDiskSnapshotPropsMixin",
    "CfnDistributionMixinProps",
    "CfnDistributionPropsMixin",
    "CfnDomainMixinProps",
    "CfnDomainPropsMixin",
    "CfnInstanceMixinProps",
    "CfnInstancePropsMixin",
    "CfnInstanceSnapshotMixinProps",
    "CfnInstanceSnapshotPropsMixin",
    "CfnLoadBalancerMixinProps",
    "CfnLoadBalancerPropsMixin",
    "CfnLoadBalancerTlsCertificateMixinProps",
    "CfnLoadBalancerTlsCertificatePropsMixin",
    "CfnStaticIpMixinProps",
    "CfnStaticIpPropsMixin",
]

publication.publish()

def _typecheckingstub__31c4104dc7bd29b63dfc786678fc328c3102ea78923154761ce34c802ab27e43(
    *,
    alarm_name: typing.Optional[builtins.str] = None,
    comparison_operator: typing.Optional[builtins.str] = None,
    contact_protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    datapoints_to_alarm: typing.Optional[jsii.Number] = None,
    evaluation_periods: typing.Optional[jsii.Number] = None,
    metric_name: typing.Optional[builtins.str] = None,
    monitored_resource_name: typing.Optional[builtins.str] = None,
    notification_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    notification_triggers: typing.Optional[typing.Sequence[builtins.str]] = None,
    threshold: typing.Optional[jsii.Number] = None,
    treat_missing_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b5aea57f2b8e0a452deb42ab445a8fa8a21440862e5a06a154ee5484db1ffe1(
    props: typing.Union[CfnAlarmMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb36785a64e66b89161d8e034d6d74dbdb98cde0fb952e5f84c5efbc03e82a9e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5245735186592cfdccf663aab9bbf1a560f80ed7b6880b61beddba0ded04c0ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6037093d3feff3d1f46e02491953c4102aac6a1590c80687fea9133784941caf(
    *,
    access_rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnBucketPropsMixin.AccessRulesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    object_versioning: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    read_only_access_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources_receiving_access: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8cd239908826720d68c786f053b71ae338d823560ddb5e2793ae2501b046fb(
    props: typing.Union[CfnBucketMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810ac2b5750d84ddf471f519f65e30d743c84f12d5faa67527b7a115e8532273(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3a7ef5e30db690c22ee5c17b5bc5cf9cd0255860c492b1fb51ae690658c606c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a96a94ca6dec170b7ef9bf06513c6d7e2ef08c364dfb69a7c1807a558dc39d2(
    *,
    allow_public_overrides: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    object_access: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__498a48b3130aa8a805613a7f823eb500f0059e4312c6f314a666f9d99afafde1(
    *,
    certificate_name: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70f751dc8447b965a1016d2fd16a8f7e854a5cb09e3f86579a3b96ecd3f3ef2(
    props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb4c0ad3444da416a5f62498f418c8c36d2450f2a279f7629b9f87b860f1a06(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f92bc2ecb146c7f32d4d198e76d3ffcc7cc4d67e0583c3e5b5959d79b44f95d5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13edaaaf210c53bbed4b243d01f049502134f0e13dff47f72b69a274e29fb1ac(
    *,
    container_service_deployment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.ContainerServiceDeploymentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    power: typing.Optional[builtins.str] = None,
    private_registry_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.PrivateRegistryAccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    public_domain_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.PublicDomainNameProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    scale: typing.Optional[jsii.Number] = None,
    service_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57474a8e564273737b3a61b9c16c5ee028f8abae9743cde4dee403e3f8921415(
    props: typing.Union[CfnContainerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264652ffb4c9dc2800b82c6ada55ca8d4e21e95bfa87e9f42f8225c0dc95dfbb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7cf33e897dd9ec3919d056148139445769726f7a6ead86d9f94e51163783667(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbfcf054baa169fea214bda4e73fbbde264e9e6f5f76bb1034efabc8caffb4b(
    *,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    container_name: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image: typing.Optional[builtins.str] = None,
    ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.PortInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b4191d87caf9ee3be130e5dfc7f5da1a08138a1350ca23e5e9759a6f8a221f(
    *,
    containers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.ContainerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    public_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.PublicEndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40f785495f02afe1d663a4c0a886b893d75ba51b78a5ba1c46120cd9f3cc7eae(
    *,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    principal_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9978e5514bf1e3933e60f87bc096abaec946bb34d03d63763ef667b3941ed115(
    *,
    value: typing.Optional[builtins.str] = None,
    variable: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e614ac6ec6a7ac1cce3f21e5db31769a9235eb7ab19e998c2cba5770795762(
    *,
    healthy_threshold: typing.Optional[jsii.Number] = None,
    interval_seconds: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    success_codes: typing.Optional[builtins.str] = None,
    timeout_seconds: typing.Optional[jsii.Number] = None,
    unhealthy_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db5a77030ca196ec96ac9703babc465270b04f30afb7c43d641d3db1e4a27684(
    *,
    port: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bd87e5f5cbd1a76dbd3820214b2c7213ce29c695088c6336741ddc21a101668(
    *,
    ecr_image_puller_role: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.EcrImagePullerRoleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55b29f0e2cf8bbedd1c224bb7b0d2ca3d7f21c917571466e522f1dffd3480cb(
    *,
    certificate_name: typing.Optional[builtins.str] = None,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__051e98bf0218deae0f209b4a93e2e9c3592524510a1e9e96081974311c7cb125(
    *,
    container_name: typing.Optional[builtins.str] = None,
    container_port: typing.Optional[jsii.Number] = None,
    health_check_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContainerPropsMixin.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b89ca13cd483b28dcc119e3026114071882c1f8d2dd34afa9dfcc1d1758050cc(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    backup_retention: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ca_certificate_identifier: typing.Optional[builtins.str] = None,
    master_database_name: typing.Optional[builtins.str] = None,
    master_username: typing.Optional[builtins.str] = None,
    master_user_password: typing.Optional[builtins.str] = None,
    preferred_backup_window: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    relational_database_blueprint_id: typing.Optional[builtins.str] = None,
    relational_database_bundle_id: typing.Optional[builtins.str] = None,
    relational_database_name: typing.Optional[builtins.str] = None,
    relational_database_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatabasePropsMixin.RelationalDatabaseParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    rotate_master_user_password: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d912645c81b36aec03719a1ec0199d4ce9af90cb9958af3ad8b2729bf51b02ce(
    props: typing.Union[CfnDatabaseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d587dfe663f2e05d9a0bb69fa270a8d574e926d33af4e82fa5b7a32835a2c64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf36ace9278c3c1cff419d48f4fb3d7b95d89fa2fca06066bd5fd90f5ec2fc2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2d27b6590eb1cdd7c322ed86ebb3b7ff1615fdd9e36897cefd7b5b8b5dea3e4(
    *,
    allowed_values: typing.Optional[builtins.str] = None,
    apply_method: typing.Optional[builtins.str] = None,
    apply_type: typing.Optional[builtins.str] = None,
    data_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    is_modifiable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45c01e1b3f572ea4bed99965f2c474e8e854a7cc0fcf79f73cc3203c29bf91d4(
    *,
    add_ons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDiskPropsMixin.AddOnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    disk_name: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDiskPropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    size_in_gb: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b0d42b5420127f0e4dfd885756fa0d81f864c23fec3e3763e1d7474623562c(
    props: typing.Union[CfnDiskMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3eb0c6658dd33d8caaf948c49198906a0a96681843b10b1dbf1a0fdf0b9a59(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b35feea8b0cc760d76f529607733c6155f39f66cb17c2edbaa8e0135b02a6f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761aff583ef0d298a3f996c87dd35534487b15c8f5d69dabcf9e0842056b7b6a(
    *,
    add_on_type: typing.Optional[builtins.str] = None,
    auto_snapshot_add_on_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDiskPropsMixin.AutoSnapshotAddOnProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf6938e15b2e0f84bccb6620246af57dc4353c4903b8dd3075b95492f5cc936(
    *,
    snapshot_time_of_day: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963a5399a31ae070a82b6b996743c04de9ca6486dfb70ccb6bae81fef1b9b783(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5554ec3968b0aa4e473d189d96e0c752915c28e854d70df0c553549243b2159(
    *,
    disk_name: typing.Optional[builtins.str] = None,
    disk_snapshot_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed0fa14c50441c9030562d270f566f63f4be14cc2d354b91680a13e181a3ea00(
    props: typing.Union[CfnDiskSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2e8a7bd725b58e963d60f8f4e0644f2896c1ecf9f099123de9382cb0e76293(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62624609725b66f4062347cd000f3d4c2d0cdfb0b69c04e2c118f417d08782fc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5019a2797292a713ce770b30399ac131989276ff3d2626b3c7f7e57c5bde02ac(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06244b8225cc9dbe34f69eaf03b9d79676fdb754abdd4da38e382b380dfa3a48(
    *,
    bundle_id: typing.Optional[builtins.str] = None,
    cache_behaviors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.CacheBehaviorPerPathProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cache_behavior_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.CacheSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate_name: typing.Optional[builtins.str] = None,
    default_cache_behavior: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.CacheBehaviorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    distribution_name: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    is_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    origin: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.InputOriginProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f67064e88414aecf42dd7619f3601cedc7912fc97d20a516132ff50a7eec0a9(
    props: typing.Union[CfnDistributionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceae9f207e0659938f2edbe1235b39788dd19c1b7fa84e96012073c9dd002133(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41bcb20b0c96722bd263a98818ff0a6c604513f85097b00cf79a0b0243b0570c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__086fc6ced7af705cf4cc3c981d85b87ef60dbf980755265b8e0204404b310d6e(
    *,
    behavior: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f7ca779722be8b7d7cff1f3ff979afe5a9d0dbdfa402739b9b359e58719677(
    *,
    behavior: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db8305f26c53a347ff768a189d1569872b210f72adba6ebc56ef79af222e5db(
    *,
    allowed_http_methods: typing.Optional[builtins.str] = None,
    cached_http_methods: typing.Optional[builtins.str] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    forwarded_cookies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.CookieObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forwarded_headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.HeaderObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forwarded_query_strings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDistributionPropsMixin.QueryStringObjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_ttl: typing.Optional[jsii.Number] = None,
    minimum_ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e382f94294921ac04e32a333799553417ac00956c6cc2fd0470e607693f38d9e(
    *,
    cookies_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06dcb8d759c29515bb6d4566be1539ec6426f75f61847728555a91107e926bd6(
    *,
    headers_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    option: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a400724aa6e98a5fbff97f31dc5c5fd2e1ea9bd063285544e0ac8fd747a3af73(
    *,
    name: typing.Optional[builtins.str] = None,
    protocol_policy: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30a38453300d326d81c4095adb4a330267a897879a3a2d0af1707e4fb9b24b2(
    *,
    option: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    query_strings_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da6671f1b16853f406744126b11e343330d4ba01cd74e5e307a0d2d3189fde5d(
    *,
    domain_entries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDomainPropsMixin.DomainEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36010ba423b98bff0b7bf9c2f11851a6c7e5253356a197718f96095b75418ea(
    props: typing.Union[CfnDomainMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a63c7fde922ddeba8db9e1f9ad5ac2b52f9ac1bb418b2bc8808ecb78c3abf17a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213f19a1fd3ebffa7c2989340fd1255ca3b9a9c17d47cc348e3e77933617b92b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f4ab48a52b75f554b0e83544394d317d3e6a41f919c8d12af0dc4b37ff94e9(
    *,
    id: typing.Optional[builtins.str] = None,
    is_alias: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15563ad8e13aef0a6feca82f9b36de9df25e0bd0db05e7bb2e7b392c6b13133b(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78f219faec21a2d975fe934d7b38f196487b9f8a505d9f7ca01c688042d8b38a(
    *,
    add_ons: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.AddOnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    availability_zone: typing.Optional[builtins.str] = None,
    blueprint_id: typing.Optional[builtins.str] = None,
    bundle_id: typing.Optional[builtins.str] = None,
    hardware: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.HardwareProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_name: typing.Optional[builtins.str] = None,
    key_pair_name: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    networking: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.NetworkingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.StateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_data: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eed61aee1127bacd88b2a6b3dcb92a7e671eba6f47c93a682797e1fb28d6677(
    props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9537f0d8bc8bb0f60e3c1eb701ec06828ef5fea6cf86cc1e3bbaa8c529100e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cbfef30d060961682293ed464665caf31ee0d0a39fb33aac9400c036e58d5cc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1d68d84dd2df528acab42b5f506dc52997e430a55fda94596c8665a06c0d60d(
    *,
    add_on_type: typing.Optional[builtins.str] = None,
    auto_snapshot_add_on_request: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.AutoSnapshotAddOnProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab9e1599fa4ce18373c0bf6aa5174d7c906be878455dbd05be4b7e635c094d42(
    *,
    snapshot_time_of_day: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4949ac016b5fa48240c1c99f21e2d718eddf2922089269d7c5a26831473c562(
    *,
    attached_to: typing.Optional[builtins.str] = None,
    attachment_state: typing.Optional[builtins.str] = None,
    disk_name: typing.Optional[builtins.str] = None,
    iops: typing.Optional[jsii.Number] = None,
    is_system_disk: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    path: typing.Optional[builtins.str] = None,
    size_in_gb: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf70ef3f018d437c634152d797c62ca0d85bbaa34d461524cf3623ec16051cf(
    *,
    cpu_count: typing.Optional[jsii.Number] = None,
    disks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.DiskProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ram_size_in_gb: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fba003ee2a965b852c4555fb59bd34548f83902bf233fb20259da74225868fe(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c687fadc9faa81b47830a8fbcb90ad9dfad0036c34a7358eff8f1e0cd44bfc(
    *,
    gb_per_month_allocated: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc6405aefb7bd66d95df4b7287bcdb884ae025743771dd24256c2da606a62e4d(
    *,
    monthly_transfer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.MonthlyTransferProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.PortProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__392ef54f46283c6f3ac96036f850aa043fd2f9ee24285526a4908ef7ce95dd34(
    *,
    access_direction: typing.Optional[builtins.str] = None,
    access_from: typing.Optional[builtins.str] = None,
    access_type: typing.Optional[builtins.str] = None,
    cidr_list_aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    common_name: typing.Optional[builtins.str] = None,
    from_port: typing.Optional[jsii.Number] = None,
    ipv6_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    protocol: typing.Optional[builtins.str] = None,
    to_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f224011fa173a70c8dbc4549ec610a5638f4aaaac31d1a5e934dee7bc2737811(
    *,
    code: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382c6df5172e936388696072b07796ae03e3c6a028e3f1883fa96ec76d65a211(
    *,
    instance_name: typing.Optional[builtins.str] = None,
    instance_snapshot_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dffd6454db0421cb8036738bc9d4284965466e3babccf40706c3405046f77a(
    props: typing.Union[CfnInstanceSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c964702a52c47ba47944f2d41ae88e4bfb9a52a19c28e4949cbcf0f21833d47(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6c28f63ff4080750a6a8586e8f3c1d3c5e9c65265f9ef20fa5e2e6b000a1f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d7914235ebca539686d6fd62fdb6050940c0b08010ddcec0a542c2aa239dc94(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    region_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851d2c2ffee133a2ab841ff3145be43ea91a6bd5e7f30eca3f1e0593651dbe23(
    *,
    attached_instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    instance_port: typing.Optional[jsii.Number] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    session_stickiness_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    session_stickiness_lb_cookie_duration_seconds: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    tls_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570f32af544a85d7ca54153794f4bc345323f52eca33dcdd90a9f38243205188(
    props: typing.Union[CfnLoadBalancerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6390764d14660c19c85b674efb0532902110727c776c3119e7d73a760335145(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a73439c892011bc5fca80fa9a51d633fe78ef8e575ad876921f737f35ca169a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c84d491d542d7e62a077c8cfdb5d537cd730087a6545d44723c0bc191abe70d2(
    *,
    certificate_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate_domain_name: typing.Optional[builtins.str] = None,
    certificate_name: typing.Optional[builtins.str] = None,
    https_redirection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_attached: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba978d652928178e1e0d6ee27d0c76f9ba17fa6f40c452c636d36afe1165bce(
    props: typing.Union[CfnLoadBalancerTlsCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5593cad554a4309bca25bced99771b5f3b3b6c93b0025c43d490c68a905b89ee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7923ed65c49d97ce179b79efc4c3124df571addfae877723b80ec261257254a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2db7f8d1ccd29c22f982df8ca5fe6c1c6bc0724d7598f14a3530a49adfa465(
    *,
    attached_to: typing.Optional[builtins.str] = None,
    static_ip_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__800915f18d9816972a07253443adc485ed60928e21ad05c135c198f8fa71c44c(
    props: typing.Union[CfnStaticIpMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11059417ea4f236188aa223a84f2c6d84fb9773966bb919e99c41b7bd6e208d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef71a8cbebe7a2312ff7da37bfd133b594fef14faa1df29d054abc15333f75c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
