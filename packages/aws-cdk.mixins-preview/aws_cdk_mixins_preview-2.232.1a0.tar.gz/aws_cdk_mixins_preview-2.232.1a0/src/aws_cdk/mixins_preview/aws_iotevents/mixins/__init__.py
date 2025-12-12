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
    jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarm_capabilities": "alarmCapabilities",
        "alarm_event_actions": "alarmEventActions",
        "alarm_model_description": "alarmModelDescription",
        "alarm_model_name": "alarmModelName",
        "alarm_rule": "alarmRule",
        "key": "key",
        "role_arn": "roleArn",
        "severity": "severity",
        "tags": "tags",
    },
)
class CfnAlarmModelMixinProps:
    def __init__(
        self,
        *,
        alarm_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        alarm_event_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AlarmEventActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        alarm_model_description: typing.Optional[builtins.str] = None,
        alarm_model_name: typing.Optional[builtins.str] = None,
        alarm_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AlarmRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        key: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAlarmModelPropsMixin.

        :param alarm_capabilities: Contains the configuration information of alarm state changes.
        :param alarm_event_actions: Contains information about one or more alarm actions.
        :param alarm_model_description: The description of the alarm model.
        :param alarm_model_name: The name of the alarm model.
        :param alarm_rule: Defines when your alarm is invoked.
        :param key: An input attribute used as a key to create an alarm. AWS IoT Events routes `inputs <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Input.html>`_ associated with this key to the alarm.
        :param role_arn: The ARN of the IAM role that allows the alarm to perform actions and access AWS resources. For more information, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param severity: A non-negative integer that reflects the severity level of the alarm.
        :param tags: A list of key-value pairs that contain metadata for the alarm model. The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* . You can create up to 50 tags for one alarm model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
            
            cfn_alarm_model_mixin_props = iotevents_mixins.CfnAlarmModelMixinProps(
                alarm_capabilities=iotevents_mixins.CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty(
                    acknowledge_flow=iotevents_mixins.CfnAlarmModelPropsMixin.AcknowledgeFlowProperty(
                        enabled=False
                    ),
                    initialization_configuration=iotevents_mixins.CfnAlarmModelPropsMixin.InitializationConfigurationProperty(
                        disabled_on_initialization=False
                    )
                ),
                alarm_event_actions=iotevents_mixins.CfnAlarmModelPropsMixin.AlarmEventActionsProperty(
                    alarm_actions=[iotevents_mixins.CfnAlarmModelPropsMixin.AlarmActionProperty(
                        dynamo_db=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_type="hashKeyType",
                            hash_key_value="hashKeyValue",
                            operation="operation",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue",
                            table_name="tableName"
                        ),
                        dynamo_dBv2=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBv2Property(
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            table_name="tableName"
                        ),
                        firehose=iotevents_mixins.CfnAlarmModelPropsMixin.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents_mixins.CfnAlarmModelPropsMixin.IotEventsProperty(
                            input_name="inputName",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents_mixins.CfnAlarmModelPropsMixin.IotSiteWiseProperty(
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId",
                            property_value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty(
                                quality="quality",
                                timestamp=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                                    offset_in_nanos="offsetInNanos",
                                    time_in_seconds="timeInSeconds"
                                ),
                                value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                )
                            )
                        ),
                        iot_topic_publish=iotevents_mixins.CfnAlarmModelPropsMixin.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents_mixins.CfnAlarmModelPropsMixin.LambdaProperty(
                            function_arn="functionArn",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sns=iotevents_mixins.CfnAlarmModelPropsMixin.SnsProperty(
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            target_arn="targetArn"
                        ),
                        sqs=iotevents_mixins.CfnAlarmModelPropsMixin.SqsProperty(
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            queue_url="queueUrl",
                            use_base64=False
                        )
                    )]
                ),
                alarm_model_description="alarmModelDescription",
                alarm_model_name="alarmModelName",
                alarm_rule=iotevents_mixins.CfnAlarmModelPropsMixin.AlarmRuleProperty(
                    simple_rule=iotevents_mixins.CfnAlarmModelPropsMixin.SimpleRuleProperty(
                        comparison_operator="comparisonOperator",
                        input_property="inputProperty",
                        threshold="threshold"
                    )
                ),
                key="key",
                role_arn="roleArn",
                severity=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__855730260361424d37f6c3756ee8ec6a82b30ad8850dfbe28ff77ae55132c78e)
            check_type(argname="argument alarm_capabilities", value=alarm_capabilities, expected_type=type_hints["alarm_capabilities"])
            check_type(argname="argument alarm_event_actions", value=alarm_event_actions, expected_type=type_hints["alarm_event_actions"])
            check_type(argname="argument alarm_model_description", value=alarm_model_description, expected_type=type_hints["alarm_model_description"])
            check_type(argname="argument alarm_model_name", value=alarm_model_name, expected_type=type_hints["alarm_model_name"])
            check_type(argname="argument alarm_rule", value=alarm_rule, expected_type=type_hints["alarm_rule"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarm_capabilities is not None:
            self._values["alarm_capabilities"] = alarm_capabilities
        if alarm_event_actions is not None:
            self._values["alarm_event_actions"] = alarm_event_actions
        if alarm_model_description is not None:
            self._values["alarm_model_description"] = alarm_model_description
        if alarm_model_name is not None:
            self._values["alarm_model_name"] = alarm_model_name
        if alarm_rule is not None:
            self._values["alarm_rule"] = alarm_rule
        if key is not None:
            self._values["key"] = key
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if severity is not None:
            self._values["severity"] = severity
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def alarm_capabilities(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty"]]:
        '''Contains the configuration information of alarm state changes.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmcapabilities
        '''
        result = self._values.get("alarm_capabilities")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty"]], result)

    @builtins.property
    def alarm_event_actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmEventActionsProperty"]]:
        '''Contains information about one or more alarm actions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmeventactions
        '''
        result = self._values.get("alarm_event_actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmEventActionsProperty"]], result)

    @builtins.property
    def alarm_model_description(self) -> typing.Optional[builtins.str]:
        '''The description of the alarm model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmmodeldescription
        '''
        result = self._values.get("alarm_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the alarm model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmmodelname
        '''
        result = self._values.get("alarm_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def alarm_rule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmRuleProperty"]]:
        '''Defines when your alarm is invoked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-alarmrule
        '''
        result = self._values.get("alarm_rule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmRuleProperty"]], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''An input attribute used as a key to create an alarm.

        AWS IoT Events routes `inputs <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Input.html>`_ associated with this key to the alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that allows the alarm to perform actions and access AWS resources.

        For more information, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[jsii.Number]:
        '''A non-negative integer that reflects the severity level of the alarm.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-severity
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the alarm model.

        The tags help you manage the alarm model. For more information, see `Tagging your AWS IoT Events resources <https://docs.aws.amazon.com/iotevents/latest/developerguide/tagging-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

        You can create up to 50 tags for one alarm model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html#cfn-iotevents-alarmmodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAlarmModelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAlarmModelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin",
):
    '''Represents an alarm model to monitor an AWS IoT Events input attribute.

    You can use the alarm to get notified when the value is outside a specified range. For more information, see `Create an alarm model <https://docs.aws.amazon.com/iotevents/latest/developerguide/create-alarms.html>`_ in the *AWS IoT Events Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-alarmmodel.html
    :cloudformationResource: AWS::IoTEvents::AlarmModel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
        
        cfn_alarm_model_props_mixin = iotevents_mixins.CfnAlarmModelPropsMixin(iotevents_mixins.CfnAlarmModelMixinProps(
            alarm_capabilities=iotevents_mixins.CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty(
                acknowledge_flow=iotevents_mixins.CfnAlarmModelPropsMixin.AcknowledgeFlowProperty(
                    enabled=False
                ),
                initialization_configuration=iotevents_mixins.CfnAlarmModelPropsMixin.InitializationConfigurationProperty(
                    disabled_on_initialization=False
                )
            ),
            alarm_event_actions=iotevents_mixins.CfnAlarmModelPropsMixin.AlarmEventActionsProperty(
                alarm_actions=[iotevents_mixins.CfnAlarmModelPropsMixin.AlarmActionProperty(
                    dynamo_db=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_type="hashKeyType",
                        hash_key_value="hashKeyValue",
                        operation="operation",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue",
                        table_name="tableName"
                    ),
                    dynamo_dBv2=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBv2Property(
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        table_name="tableName"
                    ),
                    firehose=iotevents_mixins.CfnAlarmModelPropsMixin.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents_mixins.CfnAlarmModelPropsMixin.IotEventsProperty(
                        input_name="inputName",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents_mixins.CfnAlarmModelPropsMixin.IotSiteWiseProperty(
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId",
                        property_value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty(
                            quality="quality",
                            timestamp=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                                offset_in_nanos="offsetInNanos",
                                time_in_seconds="timeInSeconds"
                            ),
                            value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            )
                        )
                    ),
                    iot_topic_publish=iotevents_mixins.CfnAlarmModelPropsMixin.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents_mixins.CfnAlarmModelPropsMixin.LambdaProperty(
                        function_arn="functionArn",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sns=iotevents_mixins.CfnAlarmModelPropsMixin.SnsProperty(
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        target_arn="targetArn"
                    ),
                    sqs=iotevents_mixins.CfnAlarmModelPropsMixin.SqsProperty(
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        queue_url="queueUrl",
                        use_base64=False
                    )
                )]
            ),
            alarm_model_description="alarmModelDescription",
            alarm_model_name="alarmModelName",
            alarm_rule=iotevents_mixins.CfnAlarmModelPropsMixin.AlarmRuleProperty(
                simple_rule=iotevents_mixins.CfnAlarmModelPropsMixin.SimpleRuleProperty(
                    comparison_operator="comparisonOperator",
                    input_property="inputProperty",
                    threshold="threshold"
                )
            ),
            key="key",
            role_arn="roleArn",
            severity=123,
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
        props: typing.Union[CfnAlarmModelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTEvents::AlarmModel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6188ec30d1473ec967d5fdafc22c90b5f76fd0cd297d3af5b71bd57a25dc5512)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c6de4cbe0dd807800f373499231bc4a3d6cca65605b660c9acabe5632d2601c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca3d663363e6af35814a2a7940995e69fac7c1b2d5ca69a3c0e2bc2ee081ba0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAlarmModelMixinProps:
        return typing.cast(CfnAlarmModelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AcknowledgeFlowProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AcknowledgeFlowProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies whether to get notified for alarm state changes.

            :param enabled: The value must be ``TRUE`` or ``FALSE`` . If ``TRUE`` , you receive a notification when the alarm state changes. You must choose to acknowledge the notification before the alarm state can return to ``NORMAL`` . If ``FALSE`` , you won't receive notifications. The alarm automatically changes to the ``NORMAL`` state when the input property value returns to the specified range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-acknowledgeflow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                acknowledge_flow_property = iotevents_mixins.CfnAlarmModelPropsMixin.AcknowledgeFlowProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6fd8997d2cfd50d606678ec2b395302c928862c06f06dcc5a280bd6f9158b429)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value must be ``TRUE`` or ``FALSE`` .

            If ``TRUE`` , you receive a notification when the alarm state changes. You must choose to acknowledge the notification before the alarm state can return to ``NORMAL`` . If ``FALSE`` , you won't receive notifications. The alarm automatically changes to the ``NORMAL`` state when the input property value returns to the specified range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-acknowledgeflow.html#cfn-iotevents-alarmmodel-acknowledgeflow-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AcknowledgeFlowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AlarmActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dynamo_db": "dynamoDb",
            "dynamo_d_bv2": "dynamoDBv2",
            "firehose": "firehose",
            "iot_events": "iotEvents",
            "iot_site_wise": "iotSiteWise",
            "iot_topic_publish": "iotTopicPublish",
            "lambda_": "lambda",
            "sns": "sns",
            "sqs": "sqs",
        },
    )
    class AlarmActionProperty:
        def __init__(
            self,
            *,
            dynamo_db: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.DynamoDBProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.DynamoDBv2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.FirehoseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.IotEventsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_site_wise: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.IotSiteWiseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.IotTopicPublishProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.LambdaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.SnsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.SqsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies one of the following actions to receive notifications when the alarm state changes.

            :param dynamo_db: Defines an action to write to the Amazon DynamoDB table that you created. The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates. **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` . - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` . - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template. ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'`` - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``tableName`` parameter uses a string concatenation. ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date`` For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* . If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .
            :param dynamo_d_bv2: Defines an action to write to the Amazon DynamoDB table that you created. The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates. **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` . - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` . - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template. ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'`` - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``tableName`` parameter uses a string concatenation. ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date`` For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* . The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .
            :param firehose: Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.
            :param iot_events: Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.
            :param iot_site_wise: Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise . You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates. **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` . - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` . - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates. In the following example, the value for the ``propertyAlias`` parameter uses a substitution template. ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'`` You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise . For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .
            :param iot_topic_publish: Information required to publish the MQTT message through the AWS IoT message broker.
            :param lambda_: Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.
            :param sns: Information required to publish the Amazon SNS message.
            :param sqs: Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                alarm_action_property = iotevents_mixins.CfnAlarmModelPropsMixin.AlarmActionProperty(
                    dynamo_db=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_type="hashKeyType",
                        hash_key_value="hashKeyValue",
                        operation="operation",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue",
                        table_name="tableName"
                    ),
                    dynamo_dBv2=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBv2Property(
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        table_name="tableName"
                    ),
                    firehose=iotevents_mixins.CfnAlarmModelPropsMixin.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents_mixins.CfnAlarmModelPropsMixin.IotEventsProperty(
                        input_name="inputName",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents_mixins.CfnAlarmModelPropsMixin.IotSiteWiseProperty(
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId",
                        property_value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty(
                            quality="quality",
                            timestamp=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                                offset_in_nanos="offsetInNanos",
                                time_in_seconds="timeInSeconds"
                            ),
                            value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            )
                        )
                    ),
                    iot_topic_publish=iotevents_mixins.CfnAlarmModelPropsMixin.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents_mixins.CfnAlarmModelPropsMixin.LambdaProperty(
                        function_arn="functionArn",
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    sns=iotevents_mixins.CfnAlarmModelPropsMixin.SnsProperty(
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        target_arn="targetArn"
                    ),
                    sqs=iotevents_mixins.CfnAlarmModelPropsMixin.SqsProperty(
                        payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        queue_url="queueUrl",
                        use_base64=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3bd0d4e69997a3df421ca4917a50f4d61b961bf11a7524ae5ba6be324f458565)
                check_type(argname="argument dynamo_db", value=dynamo_db, expected_type=type_hints["dynamo_db"])
                check_type(argname="argument dynamo_d_bv2", value=dynamo_d_bv2, expected_type=type_hints["dynamo_d_bv2"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
                check_type(argname="argument iot_site_wise", value=iot_site_wise, expected_type=type_hints["iot_site_wise"])
                check_type(argname="argument iot_topic_publish", value=iot_topic_publish, expected_type=type_hints["iot_topic_publish"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
                check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
                check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dynamo_db is not None:
                self._values["dynamo_db"] = dynamo_db
            if dynamo_d_bv2 is not None:
                self._values["dynamo_d_bv2"] = dynamo_d_bv2
            if firehose is not None:
                self._values["firehose"] = firehose
            if iot_events is not None:
                self._values["iot_events"] = iot_events
            if iot_site_wise is not None:
                self._values["iot_site_wise"] = iot_site_wise
            if iot_topic_publish is not None:
                self._values["iot_topic_publish"] = iot_topic_publish
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if sns is not None:
                self._values["sns"] = sns
            if sqs is not None:
                self._values["sqs"] = sqs

        @builtins.property
        def dynamo_db(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.DynamoDBProperty"]]:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template.

            ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-dynamodb
            '''
            result = self._values.get("dynamo_db")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.DynamoDBProperty"]], result)

        @builtins.property
        def dynamo_d_bv2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.DynamoDBv2Property"]]:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template.

            ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-dynamodbv2
            '''
            result = self._values.get("dynamo_d_bv2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.DynamoDBv2Property"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.FirehoseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.FirehoseProperty"]], result)

        @builtins.property
        def iot_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.IotEventsProperty"]]:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iotevents
            '''
            result = self._values.get("iot_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.IotEventsProperty"]], result)

        @builtins.property
        def iot_site_wise(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.IotSiteWiseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise .

            You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``propertyAlias`` parameter uses a substitution template.

            ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'``

            You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iotsitewise
            '''
            result = self._values.get("iot_site_wise")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.IotSiteWiseProperty"]], result)

        @builtins.property
        def iot_topic_publish(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.IotTopicPublishProperty"]]:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-iottopicpublish
            '''
            result = self._values.get("iot_topic_publish")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.IotTopicPublishProperty"]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.LambdaProperty"]]:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.LambdaProperty"]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.SnsProperty"]]:
            '''Information required to publish the Amazon SNS message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.SnsProperty"]], result)

        @builtins.property
        def sqs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.SqsProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmaction.html#cfn-iotevents-alarmmodel-alarmaction-sqs
            '''
            result = self._values.get("sqs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.SqsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "acknowledge_flow": "acknowledgeFlow",
            "initialization_configuration": "initializationConfiguration",
        },
    )
    class AlarmCapabilitiesProperty:
        def __init__(
            self,
            *,
            acknowledge_flow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AcknowledgeFlowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            initialization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.InitializationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the configuration information of alarm state changes.

            :param acknowledge_flow: Specifies whether to get notified for alarm state changes.
            :param initialization_configuration: Specifies the default alarm state. The configuration applies to all alarms that were created based on this alarm model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                alarm_capabilities_property = iotevents_mixins.CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty(
                    acknowledge_flow=iotevents_mixins.CfnAlarmModelPropsMixin.AcknowledgeFlowProperty(
                        enabled=False
                    ),
                    initialization_configuration=iotevents_mixins.CfnAlarmModelPropsMixin.InitializationConfigurationProperty(
                        disabled_on_initialization=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5da6d85f7e7346795d838a56ba374fe625ffc92c9aa5d51afe005062cb623c55)
                check_type(argname="argument acknowledge_flow", value=acknowledge_flow, expected_type=type_hints["acknowledge_flow"])
                check_type(argname="argument initialization_configuration", value=initialization_configuration, expected_type=type_hints["initialization_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if acknowledge_flow is not None:
                self._values["acknowledge_flow"] = acknowledge_flow
            if initialization_configuration is not None:
                self._values["initialization_configuration"] = initialization_configuration

        @builtins.property
        def acknowledge_flow(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AcknowledgeFlowProperty"]]:
            '''Specifies whether to get notified for alarm state changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html#cfn-iotevents-alarmmodel-alarmcapabilities-acknowledgeflow
            '''
            result = self._values.get("acknowledge_flow")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AcknowledgeFlowProperty"]], result)

        @builtins.property
        def initialization_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.InitializationConfigurationProperty"]]:
            '''Specifies the default alarm state.

            The configuration applies to all alarms that were created based on this alarm model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmcapabilities.html#cfn-iotevents-alarmmodel-alarmcapabilities-initializationconfiguration
            '''
            result = self._values.get("initialization_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.InitializationConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmCapabilitiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AlarmEventActionsProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_actions": "alarmActions"},
    )
    class AlarmEventActionsProperty:
        def __init__(
            self,
            *,
            alarm_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AlarmActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about one or more alarm actions.

            :param alarm_actions: Specifies one or more supported actions to receive notifications when the alarm state changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmeventactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                alarm_event_actions_property = iotevents_mixins.CfnAlarmModelPropsMixin.AlarmEventActionsProperty(
                    alarm_actions=[iotevents_mixins.CfnAlarmModelPropsMixin.AlarmActionProperty(
                        dynamo_db=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_type="hashKeyType",
                            hash_key_value="hashKeyValue",
                            operation="operation",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue",
                            table_name="tableName"
                        ),
                        dynamo_dBv2=iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBv2Property(
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            table_name="tableName"
                        ),
                        firehose=iotevents_mixins.CfnAlarmModelPropsMixin.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents_mixins.CfnAlarmModelPropsMixin.IotEventsProperty(
                            input_name="inputName",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents_mixins.CfnAlarmModelPropsMixin.IotSiteWiseProperty(
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId",
                            property_value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty(
                                quality="quality",
                                timestamp=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                                    offset_in_nanos="offsetInNanos",
                                    time_in_seconds="timeInSeconds"
                                ),
                                value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                )
                            )
                        ),
                        iot_topic_publish=iotevents_mixins.CfnAlarmModelPropsMixin.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents_mixins.CfnAlarmModelPropsMixin.LambdaProperty(
                            function_arn="functionArn",
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        sns=iotevents_mixins.CfnAlarmModelPropsMixin.SnsProperty(
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            target_arn="targetArn"
                        ),
                        sqs=iotevents_mixins.CfnAlarmModelPropsMixin.SqsProperty(
                            payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            queue_url="queueUrl",
                            use_base64=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__787a85a50437ab0e519b1e6e049099a23a68964d4405adf1dac4f63b83a039e3)
                check_type(argname="argument alarm_actions", value=alarm_actions, expected_type=type_hints["alarm_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_actions is not None:
                self._values["alarm_actions"] = alarm_actions

        @builtins.property
        def alarm_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmActionProperty"]]]]:
            '''Specifies one or more supported actions to receive notifications when the alarm state changes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmeventactions.html#cfn-iotevents-alarmmodel-alarmeventactions-alarmactions
            '''
            result = self._values.get("alarm_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AlarmActionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmEventActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AlarmRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"simple_rule": "simpleRule"},
    )
    class AlarmRuleProperty:
        def __init__(
            self,
            *,
            simple_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.SimpleRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines when your alarm is invoked.

            :param simple_rule: A rule that compares an input property value to a threshold value with a comparison operator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                alarm_rule_property = iotevents_mixins.CfnAlarmModelPropsMixin.AlarmRuleProperty(
                    simple_rule=iotevents_mixins.CfnAlarmModelPropsMixin.SimpleRuleProperty(
                        comparison_operator="comparisonOperator",
                        input_property="inputProperty",
                        threshold="threshold"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0f90c5fe0b8eb05e118fb1763b9b9c551ca8c58ad64f7606bafdc3c2e233ce5)
                check_type(argname="argument simple_rule", value=simple_rule, expected_type=type_hints["simple_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if simple_rule is not None:
                self._values["simple_rule"] = simple_rule

        @builtins.property
        def simple_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.SimpleRuleProperty"]]:
            '''A rule that compares an input property value to a threshold value with a comparison operator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-alarmrule.html#cfn-iotevents-alarmmodel-alarmrule-simplerule
            '''
            result = self._values.get("simple_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.SimpleRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty",
        jsii_struct_bases=[],
        name_mapping={
            "offset_in_nanos": "offsetInNanos",
            "time_in_seconds": "timeInSeconds",
        },
    )
    class AssetPropertyTimestampProperty:
        def __init__(
            self,
            *,
            offset_in_nanos: typing.Optional[builtins.str] = None,
            time_in_seconds: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains timestamp information. For more information, see `TimeInNanos <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_TimeInNanos.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyTimestamp`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``timeInSeconds`` parameter can be ``'1586400675'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``offsetInNanos`` parameter can be ``$variable.time`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``timeInSeconds`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.timestamp / 1000}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param offset_in_nanos: The nanosecond offset converted from ``timeInSeconds`` . The valid range is between 0-999999999.
            :param time_in_seconds: The timestamp, in seconds, in the Unix epoch format. The valid range is between 1-31556889864403199.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertytimestamp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                asset_property_timestamp_property = iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                    offset_in_nanos="offsetInNanos",
                    time_in_seconds="timeInSeconds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__629b1196d5b7d0a8a2075adb40c66175e2a43c1fb17804325ea36d025850a4ca)
                check_type(argname="argument offset_in_nanos", value=offset_in_nanos, expected_type=type_hints["offset_in_nanos"])
                check_type(argname="argument time_in_seconds", value=time_in_seconds, expected_type=type_hints["time_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if offset_in_nanos is not None:
                self._values["offset_in_nanos"] = offset_in_nanos
            if time_in_seconds is not None:
                self._values["time_in_seconds"] = time_in_seconds

        @builtins.property
        def offset_in_nanos(self) -> typing.Optional[builtins.str]:
            '''The nanosecond offset converted from ``timeInSeconds`` .

            The valid range is between 0-999999999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertytimestamp.html#cfn-iotevents-alarmmodel-assetpropertytimestamp-offsetinnanos
            '''
            result = self._values.get("offset_in_nanos")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_in_seconds(self) -> typing.Optional[builtins.str]:
            '''The timestamp, in seconds, in the Unix epoch format.

            The valid range is between 1-31556889864403199.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertytimestamp.html#cfn-iotevents-alarmmodel-assetpropertytimestamp-timeinseconds
            '''
            result = self._values.get("time_in_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyTimestampProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "quality": "quality",
            "timestamp": "timestamp",
            "value": "value",
        },
    )
    class AssetPropertyValueProperty:
        def __init__(
            self,
            *,
            quality: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AssetPropertyVariantProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains value information. For more information, see `AssetPropertyValue <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetPropertyValue.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyValue`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``quality`` parameter can be ``'GOOD'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``quality`` parameter can be ``$input.TemperatureInput.sensorData.quality`` .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param quality: The quality of the asset property value. The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .
            :param timestamp: The timestamp associated with the asset property value. The default is the current event time.
            :param value: The value to send to an asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                asset_property_value_property = iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty(
                    quality="quality",
                    timestamp=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                        offset_in_nanos="offsetInNanos",
                        time_in_seconds="timeInSeconds"
                    ),
                    value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                        boolean_value="booleanValue",
                        double_value="doubleValue",
                        integer_value="integerValue",
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d83533a8facffc8851e795cf3a459c108416cba16d921d59a56d1921df74006)
                check_type(argname="argument quality", value=quality, expected_type=type_hints["quality"])
                check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if quality is not None:
                self._values["quality"] = quality
            if timestamp is not None:
                self._values["timestamp"] = timestamp
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def quality(self) -> typing.Optional[builtins.str]:
            '''The quality of the asset property value.

            The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-quality
            '''
            result = self._values.get("quality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty"]]:
            '''The timestamp associated with the asset property value.

            The default is the current event time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty"]], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AssetPropertyVariantProperty"]]:
            '''The value to send to an asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvalue.html#cfn-iotevents-alarmmodel-assetpropertyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AssetPropertyVariantProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "integer_value": "integerValue",
            "string_value": "stringValue",
        },
    )
    class AssetPropertyVariantProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[builtins.str] = None,
            double_value: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains an asset property value.

            For more information, see `Variant <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_Variant.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyVariant`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``integerValue`` parameter can be ``'100'`` .

            - For references, you must specify either variables or parameters. For example, the value for the ``booleanValue`` parameter can be ``$variable.offline`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``doubleValue`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.temperature * 6 / 5 + 32}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            You must specify one of the following value types, depending on the ``dataType`` of the specified asset property. For more information, see `AssetProperty <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetProperty.html>`_ in the *AWS IoT SiteWise API Reference* .

            :param boolean_value: The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` . You must use an expression, and the evaluated result should be a Boolean value.
            :param double_value: The asset property value is a double. You must use an expression, and the evaluated result should be a double.
            :param integer_value: The asset property value is an integer. You must use an expression, and the evaluated result should be an integer.
            :param string_value: The asset property value is a string. You must use an expression, and the evaluated result should be a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                asset_property_variant_property = iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                    boolean_value="booleanValue",
                    double_value="doubleValue",
                    integer_value="integerValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c74301ebf81ed4f67dd308ba6ba2475dd336091d289a1b7d73993fec6a42a02)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` .

            You must use an expression, and the evaluated result should be a Boolean value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def double_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a double.

            You must use an expression, and the evaluated result should be a double.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is an integer.

            You must use an expression, and the evaluated result should be an integer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a string.

            You must use an expression, and the evaluated result should be a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-assetpropertyvariant.html#cfn-iotevents-alarmmodel-assetpropertyvariant-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.DynamoDBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hash_key_field": "hashKeyField",
            "hash_key_type": "hashKeyType",
            "hash_key_value": "hashKeyValue",
            "operation": "operation",
            "payload": "payload",
            "payload_field": "payloadField",
            "range_key_field": "rangeKeyField",
            "range_key_type": "rangeKeyType",
            "range_key_value": "rangeKeyValue",
            "table_name": "tableName",
        },
    )
    class DynamoDBProperty:
        def __init__(
            self,
            *,
            hash_key_field: typing.Optional[builtins.str] = None,
            hash_key_type: typing.Optional[builtins.str] = None,
            hash_key_value: typing.Optional[builtins.str] = None,
            operation: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            payload_field: typing.Optional[builtins.str] = None,
            range_key_field: typing.Optional[builtins.str] = None,
            range_key_type: typing.Optional[builtins.str] = None,
            range_key_value: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template.

            ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .

            :param hash_key_field: The name of the hash key (also called the partition key). The ``hashKeyField`` value must match the partition key of the target DynamoDB table.
            :param hash_key_type: The data type for the hash key (also called the partition key). You can specify the following values:. - ``'STRING'`` - The hash key is a string. - ``'NUMBER'`` - The hash key is a number. If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .
            :param hash_key_value: The value of the hash key (also called the partition key).
            :param operation: The type of operation to perform. You can specify the following values:. - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key. - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.
            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .
            :param payload_field: The name of the DynamoDB column that receives the action payload. If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .
            :param range_key_field: The name of the range key (also called the sort key). The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.
            :param range_key_type: The data type for the range key (also called the sort key), You can specify the following values:. - ``'STRING'`` - The range key is a string. - ``'NUMBER'`` - The range key is number. If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .
            :param range_key_value: The value of the range key (also called the sort key).
            :param table_name: The name of the DynamoDB table. The ``tableName`` value must match the table name of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                dynamo_dBProperty = iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBProperty(
                    hash_key_field="hashKeyField",
                    hash_key_type="hashKeyType",
                    hash_key_value="hashKeyValue",
                    operation="operation",
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    payload_field="payloadField",
                    range_key_field="rangeKeyField",
                    range_key_type="rangeKeyType",
                    range_key_value="rangeKeyValue",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1de654499e95da7b5d7290b6006a0f42c63b3e09fa977d8b18588129ab4296ed)
                check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
                check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
                check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
                check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
                check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
                check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
                check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hash_key_field is not None:
                self._values["hash_key_field"] = hash_key_field
            if hash_key_type is not None:
                self._values["hash_key_type"] = hash_key_type
            if hash_key_value is not None:
                self._values["hash_key_value"] = hash_key_value
            if operation is not None:
                self._values["operation"] = operation
            if payload is not None:
                self._values["payload"] = payload
            if payload_field is not None:
                self._values["payload_field"] = payload_field
            if range_key_field is not None:
                self._values["range_key_field"] = range_key_field
            if range_key_type is not None:
                self._values["range_key_type"] = range_key_type
            if range_key_value is not None:
                self._values["range_key_value"] = range_key_value
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def hash_key_field(self) -> typing.Optional[builtins.str]:
            '''The name of the hash key (also called the partition key).

            The ``hashKeyField`` value must match the partition key of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-hashkeyfield
            '''
            result = self._values.get("hash_key_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hash_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the hash key (also called the partition key). You can specify the following values:.

            - ``'STRING'`` - The hash key is a string.
            - ``'NUMBER'`` - The hash key is a number.

            If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-hashkeytype
            '''
            result = self._values.get("hash_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hash_key_value(self) -> typing.Optional[builtins.str]:
            '''The value of the hash key (also called the partition key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-hashkeyvalue
            '''
            result = self._values.get("hash_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation(self) -> typing.Optional[builtins.str]:
            '''The type of operation to perform. You can specify the following values:.

            - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key.
            - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.
            - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.

            If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-operation
            '''
            result = self._values.get("operation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def payload_field(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB column that receives the action payload.

            If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-payloadfield
            '''
            result = self._values.get("payload_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_field(self) -> typing.Optional[builtins.str]:
            '''The name of the range key (also called the sort key).

            The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-rangekeyfield
            '''
            result = self._values.get("range_key_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the range key (also called the sort key), You can specify the following values:.

            - ``'STRING'`` - The range key is a string.
            - ``'NUMBER'`` - The range key is number.

            If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-rangekeytype
            '''
            result = self._values.get("range_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_value(self) -> typing.Optional[builtins.str]:
            '''The value of the range key (also called the sort key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-rangekeyvalue
            '''
            result = self._values.get("range_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB table.

            The ``tableName`` value must match the table name of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodb.html#cfn-iotevents-alarmmodel-dynamodb-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.DynamoDBv2Property",
        jsii_struct_bases=[],
        name_mapping={"payload": "payload", "table_name": "tableName"},
    )
    class DynamoDBv2Property:
        def __init__(
            self,
            *,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template.

            ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .

            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .
            :param table_name: The name of the DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                dynamo_dBv2_property = iotevents_mixins.CfnAlarmModelPropsMixin.DynamoDBv2Property(
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__984c363aa8c2ea65257b1af55cc9da541517822a18f405fe7b27356c3a64409c)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html#cfn-iotevents-alarmmodel-dynamodbv2-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-dynamodbv2.html#cfn-iotevents-alarmmodel-dynamodbv2-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBv2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.FirehoseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_stream_name": "deliveryStreamName",
            "payload": "payload",
            "separator": "separator",
        },
    )
    class FirehoseProperty:
        def __init__(
            self,
            *,
            delivery_stream_name: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            separator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :param delivery_stream_name: The name of the Kinesis Data Firehose delivery stream where the data is written.
            :param payload: You can configure the action payload when you send a message to an Amazon Data Firehose delivery stream.
            :param separator: A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream. Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                firehose_property = iotevents_mixins.CfnAlarmModelPropsMixin.FirehoseProperty(
                    delivery_stream_name="deliveryStreamName",
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    separator="separator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03187648ebc1fe3403e835d2968260e293cecb65f2fdea9c0dc3498c81faa2d9)
                check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream_name is not None:
                self._values["delivery_stream_name"] = delivery_stream_name
            if payload is not None:
                self._values["payload"] = payload
            if separator is not None:
                self._values["separator"] = separator

        @builtins.property
        def delivery_stream_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Kinesis Data Firehose delivery stream where the data is written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-deliverystreamname
            '''
            result = self._values.get("delivery_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def separator(self) -> typing.Optional[builtins.str]:
            '''A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream.

            Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-firehose.html#cfn-iotevents-alarmmodel-firehose-separator
            '''
            result = self._values.get("separator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.InitializationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"disabled_on_initialization": "disabledOnInitialization"},
    )
    class InitializationConfigurationProperty:
        def __init__(
            self,
            *,
            disabled_on_initialization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies the default alarm state.

            The configuration applies to all alarms that were created based on this alarm model.

            :param disabled_on_initialization: The value must be ``TRUE`` or ``FALSE`` . If ``FALSE`` , all alarm instances created based on the alarm model are activated. The default value is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-initializationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                initialization_configuration_property = iotevents_mixins.CfnAlarmModelPropsMixin.InitializationConfigurationProperty(
                    disabled_on_initialization=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d0937ce94f5763c68b15b03ffd03307a6f79599353a69ba7c55d8e92fdb680f)
                check_type(argname="argument disabled_on_initialization", value=disabled_on_initialization, expected_type=type_hints["disabled_on_initialization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if disabled_on_initialization is not None:
                self._values["disabled_on_initialization"] = disabled_on_initialization

        @builtins.property
        def disabled_on_initialization(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The value must be ``TRUE`` or ``FALSE`` .

            If ``FALSE`` , all alarm instances created based on the alarm model are activated. The default value is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-initializationconfiguration.html#cfn-iotevents-alarmmodel-initializationconfiguration-disabledoninitialization
            '''
            result = self._values.get("disabled_on_initialization")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitializationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.IotEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "payload": "payload"},
    )
    class IotEventsProperty:
        def __init__(
            self,
            *,
            input_name: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :param input_name: The name of the AWS IoT Events input where the data is sent.
            :param payload: You can configure the action payload when you send a message to an AWS IoT Events input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                iot_events_property = iotevents_mixins.CfnAlarmModelPropsMixin.IotEventsProperty(
                    input_name="inputName",
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b1b1ae8b0056c0bcb9ec59347e5d739deec20d878ebcfa530fc90933392229b)
                check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_name is not None:
                self._values["input_name"] = input_name
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def input_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS IoT Events input where the data is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html#cfn-iotevents-alarmmodel-iotevents-inputname
            '''
            result = self._values.get("input_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an AWS IoT Events input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotevents.html#cfn-iotevents-alarmmodel-iotevents-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.IotSiteWiseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asset_id": "assetId",
            "entry_id": "entryId",
            "property_alias": "propertyAlias",
            "property_id": "propertyId",
            "property_value": "propertyValue",
        },
    )
    class IotSiteWiseProperty:
        def __init__(
            self,
            *,
            asset_id: typing.Optional[builtins.str] = None,
            entry_id: typing.Optional[builtins.str] = None,
            property_alias: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
            property_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.AssetPropertyValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise .

            You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``propertyAlias`` parameter uses a substitution template.

            ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'``

            You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param asset_id: The ID of the asset that has the specified property.
            :param entry_id: A unique identifier for this entry. You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.
            :param property_alias: The alias of the asset property.
            :param property_id: The ID of the asset property.
            :param property_value: The value to send to the asset property. This value contains timestamp, quality, and value (TQV) information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                iot_site_wise_property = iotevents_mixins.CfnAlarmModelPropsMixin.IotSiteWiseProperty(
                    asset_id="assetId",
                    entry_id="entryId",
                    property_alias="propertyAlias",
                    property_id="propertyId",
                    property_value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyValueProperty(
                        quality="quality",
                        timestamp=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty(
                            offset_in_nanos="offsetInNanos",
                            time_in_seconds="timeInSeconds"
                        ),
                        value=iotevents_mixins.CfnAlarmModelPropsMixin.AssetPropertyVariantProperty(
                            boolean_value="booleanValue",
                            double_value="doubleValue",
                            integer_value="integerValue",
                            string_value="stringValue"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__56b4a49b5172e76309519ada5cb34d77a2003350bfb3f9fa310cd0d1bfae508a)
                check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
                check_type(argname="argument entry_id", value=entry_id, expected_type=type_hints["entry_id"])
                check_type(argname="argument property_alias", value=property_alias, expected_type=type_hints["property_alias"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
                check_type(argname="argument property_value", value=property_value, expected_type=type_hints["property_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_id is not None:
                self._values["asset_id"] = asset_id
            if entry_id is not None:
                self._values["entry_id"] = entry_id
            if property_alias is not None:
                self._values["property_alias"] = property_alias
            if property_id is not None:
                self._values["property_id"] = property_id
            if property_value is not None:
                self._values["property_value"] = property_value

        @builtins.property
        def asset_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset that has the specified property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-assetid
            '''
            result = self._values.get("asset_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entry_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for this entry.

            You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-entryid
            '''
            result = self._values.get("entry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_alias(self) -> typing.Optional[builtins.str]:
            '''The alias of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyalias
            '''
            result = self._values.get("property_alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AssetPropertyValueProperty"]]:
            '''The value to send to the asset property.

            This value contains timestamp, quality, and value (TQV) information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iotsitewise.html#cfn-iotevents-alarmmodel-iotsitewise-propertyvalue
            '''
            result = self._values.get("property_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.AssetPropertyValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotSiteWiseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.IotTopicPublishProperty",
        jsii_struct_bases=[],
        name_mapping={"mqtt_topic": "mqttTopic", "payload": "payload"},
    )
    class IotTopicPublishProperty:
        def __init__(
            self,
            *,
            mqtt_topic: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :param mqtt_topic: The MQTT topic of the message. You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.
            :param payload: You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                iot_topic_publish_property = iotevents_mixins.CfnAlarmModelPropsMixin.IotTopicPublishProperty(
                    mqtt_topic="mqttTopic",
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27eb6bb6fd0ba2b28981da9ca8bbd9547b62be114f4bcfd17a4242fae34b8cd4)
                check_type(argname="argument mqtt_topic", value=mqtt_topic, expected_type=type_hints["mqtt_topic"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mqtt_topic is not None:
                self._values["mqtt_topic"] = mqtt_topic
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def mqtt_topic(self) -> typing.Optional[builtins.str]:
            '''The MQTT topic of the message.

            You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html#cfn-iotevents-alarmmodel-iottopicpublish-mqtttopic
            '''
            result = self._values.get("mqtt_topic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-iottopicpublish.html#cfn-iotevents-alarmmodel-iottopicpublish-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotTopicPublishProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={"function_arn": "functionArn", "payload": "payload"},
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            function_arn: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :param function_arn: The ARN of the Lambda function that is executed.
            :param payload: You can configure the action payload when you send a message to a Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                lambda_property = iotevents_mixins.CfnAlarmModelPropsMixin.LambdaProperty(
                    function_arn="functionArn",
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7382a5cbc523a5c6c8dc636406249f8985f3b956f215f1281309ff961ba1ffe)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_arn is not None:
                self._values["function_arn"] = function_arn
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def function_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function that is executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html#cfn-iotevents-alarmmodel-lambda-functionarn
            '''
            result = self._values.get("function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to a Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-lambda.html#cfn-iotevents-alarmmodel-lambda-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.PayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"content_expression": "contentExpression", "type": "type"},
    )
    class PayloadProperty:
        def __init__(
            self,
            *,
            content_expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :param content_expression: The content of the payload. You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.
            :param type: The value of the payload type can be either ``STRING`` or ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-payload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                payload_property = iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                    content_expression="contentExpression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ddd6fef3ca64ccdbb6a884e1886cc3607e58fb417087c79887db29d014da5c0)
                check_type(argname="argument content_expression", value=content_expression, expected_type=type_hints["content_expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_expression is not None:
                self._values["content_expression"] = content_expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def content_expression(self) -> typing.Optional[builtins.str]:
            '''The content of the payload.

            You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-payload.html#cfn-iotevents-alarmmodel-payload-contentexpression
            '''
            result = self._values.get("content_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The value of the payload type can be either ``STRING`` or ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-payload.html#cfn-iotevents-alarmmodel-payload-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.SimpleRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "input_property": "inputProperty",
            "threshold": "threshold",
        },
    )
    class SimpleRuleProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            input_property: typing.Optional[builtins.str] = None,
            threshold: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A rule that compares an input property value to a threshold value with a comparison operator.

            :param comparison_operator: The comparison operator.
            :param input_property: The value on the left side of the comparison operator. You can specify an AWS IoT Events input attribute as an input property.
            :param threshold: The value on the right side of the comparison operator. You can enter a number or specify an AWS IoT Events input attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                simple_rule_property = iotevents_mixins.CfnAlarmModelPropsMixin.SimpleRuleProperty(
                    comparison_operator="comparisonOperator",
                    input_property="inputProperty",
                    threshold="threshold"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c5f4f33187a7d8774e1a4fa21067dcc750390df3ec269786a646a75af67f8e9)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument input_property", value=input_property, expected_type=type_hints["input_property"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if input_property is not None:
                self._values["input_property"] = input_property
            if threshold is not None:
                self._values["threshold"] = threshold

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The comparison operator.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html#cfn-iotevents-alarmmodel-simplerule-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def input_property(self) -> typing.Optional[builtins.str]:
            '''The value on the left side of the comparison operator.

            You can specify an AWS IoT Events input attribute as an input property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html#cfn-iotevents-alarmmodel-simplerule-inputproperty
            '''
            result = self._values.get("input_property")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold(self) -> typing.Optional[builtins.str]:
            '''The value on the right side of the comparison operator.

            You can enter a number or specify an AWS IoT Events input attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-simplerule.html#cfn-iotevents-alarmmodel-simplerule-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SimpleRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.SnsProperty",
        jsii_struct_bases=[],
        name_mapping={"payload": "payload", "target_arn": "targetArn"},
    )
    class SnsProperty:
        def __init__(
            self,
            *,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information required to publish the Amazon SNS message.

            :param payload: You can configure the action payload when you send a message as an Amazon SNS push notification.
            :param target_arn: The ARN of the Amazon SNS target where the message is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                sns_property = iotevents_mixins.CfnAlarmModelPropsMixin.SnsProperty(
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    target_arn="targetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f930f65f0c30d952a5df47e8562e2c5917c1a2956ccfae38ee67da30a569c0e0)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if target_arn is not None:
                self._values["target_arn"] = target_arn

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message as an Amazon SNS push notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html#cfn-iotevents-alarmmodel-sns-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def target_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon SNS target where the message is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sns.html#cfn-iotevents-alarmmodel-sns-targetarn
            '''
            result = self._values.get("target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnAlarmModelPropsMixin.SqsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "payload": "payload",
            "queue_url": "queueUrl",
            "use_base64": "useBase64",
        },
    )
    class SqsProperty:
        def __init__(
            self,
            *,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAlarmModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            queue_url: typing.Optional[builtins.str] = None,
            use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :param payload: You can configure the action payload when you send a message to an Amazon SQS queue.
            :param queue_url: The URL of the SQS queue where the data is written.
            :param use_base64: Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue. Otherwise, set this to FALSE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                sqs_property = iotevents_mixins.CfnAlarmModelPropsMixin.SqsProperty(
                    payload=iotevents_mixins.CfnAlarmModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    queue_url="queueUrl",
                    use_base64=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbe96585898417569bb23acffdb80c9c6cf391820f8327896c83ae88fd6bf119)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
                check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if queue_url is not None:
                self._values["queue_url"] = queue_url
            if use_base64 is not None:
                self._values["use_base64"] = use_base64

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAlarmModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def queue_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the SQS queue where the data is written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-queueurl
            '''
            result = self._values.get("queue_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_base64(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue.

            Otherwise, set this to FALSE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-alarmmodel-sqs.html#cfn-iotevents-alarmmodel-sqs-usebase64
            '''
            result = self._values.get("use_base64")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "detector_model_definition": "detectorModelDefinition",
        "detector_model_description": "detectorModelDescription",
        "detector_model_name": "detectorModelName",
        "evaluation_method": "evaluationMethod",
        "key": "key",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnDetectorModelMixinProps:
    def __init__(
        self,
        *,
        detector_model_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        detector_model_description: typing.Optional[builtins.str] = None,
        detector_model_name: typing.Optional[builtins.str] = None,
        evaluation_method: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDetectorModelPropsMixin.

        :param detector_model_definition: Information that defines how a detector operates.
        :param detector_model_description: A brief description of the detector model.
        :param detector_model_name: The name of the detector model.
        :param evaluation_method: Information about the order in which events are evaluated and how actions are executed.
        :param key: The value used to identify a detector instance. When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information. This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value.
        :param role_arn: The ARN of the role that grants permission to AWS IoT Events to perform its operations.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
            
            cfn_detector_model_mixin_props = iotevents_mixins.CfnDetectorModelMixinProps(
                detector_model_definition=iotevents_mixins.CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty(
                    initial_state_name="initialStateName",
                    states=[iotevents_mixins.CfnDetectorModelPropsMixin.StateProperty(
                        on_enter=iotevents_mixins.CfnDetectorModelPropsMixin.OnEnterProperty(
                            events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName"
                            )]
                        ),
                        on_exit=iotevents_mixins.CfnDetectorModelPropsMixin.OnExitProperty(
                            events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName"
                            )]
                        ),
                        on_input=iotevents_mixins.CfnDetectorModelPropsMixin.OnInputProperty(
                            events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName"
                            )],
                            transition_events=[iotevents_mixins.CfnDetectorModelPropsMixin.TransitionEventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName",
                                next_state="nextState"
                            )]
                        ),
                        state_name="stateName"
                    )]
                ),
                detector_model_description="detectorModelDescription",
                detector_model_name="detectorModelName",
                evaluation_method="evaluationMethod",
                key="key",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dc29225a6f2766a41fa1f4f3b12b974fdbb5f7a13e25d0ec57228f87c100dfb)
            check_type(argname="argument detector_model_definition", value=detector_model_definition, expected_type=type_hints["detector_model_definition"])
            check_type(argname="argument detector_model_description", value=detector_model_description, expected_type=type_hints["detector_model_description"])
            check_type(argname="argument detector_model_name", value=detector_model_name, expected_type=type_hints["detector_model_name"])
            check_type(argname="argument evaluation_method", value=evaluation_method, expected_type=type_hints["evaluation_method"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detector_model_definition is not None:
            self._values["detector_model_definition"] = detector_model_definition
        if detector_model_description is not None:
            self._values["detector_model_description"] = detector_model_description
        if detector_model_name is not None:
            self._values["detector_model_name"] = detector_model_name
        if evaluation_method is not None:
            self._values["evaluation_method"] = evaluation_method
        if key is not None:
            self._values["key"] = key
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def detector_model_definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty"]]:
        '''Information that defines how a detector operates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldefinition
        '''
        result = self._values.get("detector_model_definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty"]], result)

    @builtins.property
    def detector_model_description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the detector model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodeldescription
        '''
        result = self._values.get("detector_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def detector_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the detector model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-detectormodelname
        '''
        result = self._values.get("detector_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def evaluation_method(self) -> typing.Optional[builtins.str]:
        '''Information about the order in which events are evaluated and how actions are executed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-evaluationmethod
        '''
        result = self._values.get("evaluation_method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''The value used to identify a detector instance.

        When a device or system sends input, a new detector instance with a unique key value is created. AWS IoT Events can continue to route input to its corresponding detector instance based on this identifying information.

        This parameter uses a JSON-path expression to select the attribute-value pair in the message payload that is used for identification. To route the message to the correct detector instance, the device must send a message payload that contains the same attribute-value.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the role that grants permission to AWS IoT Events to perform its operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html#cfn-iotevents-detectormodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDetectorModelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDetectorModelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin",
):
    '''The AWS::IoTEvents::DetectorModel resource creates a detector model.

    You create a *detector model* (a model of your equipment or process) using *states* . For each state, you define conditional (Boolean) logic that evaluates the incoming inputs to detect significant events. When an event is detected, it can change the state or trigger custom-built or predefined actions using other AWS services. You can define additional events that trigger actions when entering or exiting a state and, optionally, when a condition is met. For more information, see `How to Use AWS IoT Events <https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .
    .. epigraph::

       When you successfully update a detector model (using the AWS IoT Events console, AWS IoT Events API or CLI commands, or CloudFormation ) all detector instances created by the model are reset to their initial states. (The detector's ``state`` , and the values of any variables and timers are reset.)

       When you successfully update a detector model (using the AWS IoT Events console, AWS IoT Events API or CLI commands, or CloudFormation ) the version number of the detector model is incremented. (A detector model with version number 1 before the update has version number 2 after the update succeeds.)

       If you attempt to update a detector model using CloudFormation and the update does not succeed, the system may, in some cases, restore the original detector model. When this occurs, the detector model's version is incremented twice (for example, from version 1 to version 3) and the detector instances are reset.

       Also, be aware that if you attempt to update several detector models at once using CloudFormation , some updates may succeed and others fail. In this case, the effects on each detector model's detector instances and version number depend on whether the update succeeded or failed, with the results as stated.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-detectormodel.html
    :cloudformationResource: AWS::IoTEvents::DetectorModel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
        
        cfn_detector_model_props_mixin = iotevents_mixins.CfnDetectorModelPropsMixin(iotevents_mixins.CfnDetectorModelMixinProps(
            detector_model_definition=iotevents_mixins.CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty(
                initial_state_name="initialStateName",
                states=[iotevents_mixins.CfnDetectorModelPropsMixin.StateProperty(
                    on_enter=iotevents_mixins.CfnDetectorModelPropsMixin.OnEnterProperty(
                        events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName"
                        )]
                    ),
                    on_exit=iotevents_mixins.CfnDetectorModelPropsMixin.OnExitProperty(
                        events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName"
                        )]
                    ),
                    on_input=iotevents_mixins.CfnDetectorModelPropsMixin.OnInputProperty(
                        events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName"
                        )],
                        transition_events=[iotevents_mixins.CfnDetectorModelPropsMixin.TransitionEventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName",
                            next_state="nextState"
                        )]
                    ),
                    state_name="stateName"
                )]
            ),
            detector_model_description="detectorModelDescription",
            detector_model_name="detectorModelName",
            evaluation_method="evaluationMethod",
            key="key",
            role_arn="roleArn",
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
        props: typing.Union[CfnDetectorModelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTEvents::DetectorModel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155b570ea75baab89f386d5ba02ff00287fda9ca4547ac62b562e86c7882ce76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a26c59f3f6d85581e38b932238456920099dce80480b697bfdea5785662a80b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f856275da4d53a5aea294d45a6ab52704620cbc683eca3447663f88700fd5b73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDetectorModelMixinProps:
        return typing.cast(CfnDetectorModelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "clear_timer": "clearTimer",
            "dynamo_db": "dynamoDb",
            "dynamo_d_bv2": "dynamoDBv2",
            "firehose": "firehose",
            "iot_events": "iotEvents",
            "iot_site_wise": "iotSiteWise",
            "iot_topic_publish": "iotTopicPublish",
            "lambda_": "lambda",
            "reset_timer": "resetTimer",
            "set_timer": "setTimer",
            "set_variable": "setVariable",
            "sns": "sns",
            "sqs": "sqs",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            clear_timer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.ClearTimerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_db: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.DynamoDBProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.DynamoDBv2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.FirehoseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.IotEventsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_site_wise: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.IotSiteWiseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.IotTopicPublishProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.LambdaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            reset_timer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.ResetTimerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            set_timer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.SetTimerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            set_variable: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.SetVariableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.SnsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.SqsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An action to be performed when the ``condition`` is TRUE.

            :param clear_timer: Information needed to clear the timer.
            :param dynamo_db: Writes to the DynamoDB table that you created. The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .
            :param dynamo_d_bv2: Writes to the DynamoDB table that you created. The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .
            :param firehose: Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.
            :param iot_events: Sends AWS IoT Events input, which passes information about the detector model instance and the event that triggered the action.
            :param iot_site_wise: Sends information about the detector model instance and the event that triggered the action to an asset property in AWS IoT SiteWise .
            :param iot_topic_publish: Publishes an MQTT message with the given topic to the AWS IoT message broker.
            :param lambda_: Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.
            :param reset_timer: Information needed to reset the timer.
            :param set_timer: Information needed to set the timer.
            :param set_variable: Sets a variable to a specified value.
            :param sns: Sends an Amazon SNS message.
            :param sqs: Sends an Amazon SNS message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                action_property = iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                        timer_name="timerName"
                    ),
                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                        hash_key_field="hashKeyField",
                        hash_key_type="hashKeyType",
                        hash_key_value="hashKeyValue",
                        operation="operation",
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        payload_field="payloadField",
                        range_key_field="rangeKeyField",
                        range_key_type="rangeKeyType",
                        range_key_value="rangeKeyValue",
                        table_name="tableName"
                    ),
                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        table_name="tableName"
                    ),
                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                        delivery_stream_name="deliveryStreamName",
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        separator="separator"
                    ),
                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                        input_name="inputName",
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                        asset_id="assetId",
                        entry_id="entryId",
                        property_alias="propertyAlias",
                        property_id="propertyId",
                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                            quality="quality",
                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                offset_in_nanos="offsetInNanos",
                                time_in_seconds="timeInSeconds"
                            ),
                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                boolean_value="booleanValue",
                                double_value="doubleValue",
                                integer_value="integerValue",
                                string_value="stringValue"
                            )
                        )
                    ),
                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                        mqtt_topic="mqttTopic",
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                        function_arn="functionArn",
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        )
                    ),
                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                        timer_name="timerName"
                    ),
                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                        duration_expression="durationExpression",
                        seconds=123,
                        timer_name="timerName"
                    ),
                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                        value="value",
                        variable_name="variableName"
                    ),
                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        target_arn="targetArn"
                    ),
                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                            content_expression="contentExpression",
                            type="type"
                        ),
                        queue_url="queueUrl",
                        use_base64=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c49eb462e6ae94250c442a25203366b7b1abba35dda9c575cccb528ebb21b6b4)
                check_type(argname="argument clear_timer", value=clear_timer, expected_type=type_hints["clear_timer"])
                check_type(argname="argument dynamo_db", value=dynamo_db, expected_type=type_hints["dynamo_db"])
                check_type(argname="argument dynamo_d_bv2", value=dynamo_d_bv2, expected_type=type_hints["dynamo_d_bv2"])
                check_type(argname="argument firehose", value=firehose, expected_type=type_hints["firehose"])
                check_type(argname="argument iot_events", value=iot_events, expected_type=type_hints["iot_events"])
                check_type(argname="argument iot_site_wise", value=iot_site_wise, expected_type=type_hints["iot_site_wise"])
                check_type(argname="argument iot_topic_publish", value=iot_topic_publish, expected_type=type_hints["iot_topic_publish"])
                check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
                check_type(argname="argument reset_timer", value=reset_timer, expected_type=type_hints["reset_timer"])
                check_type(argname="argument set_timer", value=set_timer, expected_type=type_hints["set_timer"])
                check_type(argname="argument set_variable", value=set_variable, expected_type=type_hints["set_variable"])
                check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
                check_type(argname="argument sqs", value=sqs, expected_type=type_hints["sqs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clear_timer is not None:
                self._values["clear_timer"] = clear_timer
            if dynamo_db is not None:
                self._values["dynamo_db"] = dynamo_db
            if dynamo_d_bv2 is not None:
                self._values["dynamo_d_bv2"] = dynamo_d_bv2
            if firehose is not None:
                self._values["firehose"] = firehose
            if iot_events is not None:
                self._values["iot_events"] = iot_events
            if iot_site_wise is not None:
                self._values["iot_site_wise"] = iot_site_wise
            if iot_topic_publish is not None:
                self._values["iot_topic_publish"] = iot_topic_publish
            if lambda_ is not None:
                self._values["lambda_"] = lambda_
            if reset_timer is not None:
                self._values["reset_timer"] = reset_timer
            if set_timer is not None:
                self._values["set_timer"] = set_timer
            if set_variable is not None:
                self._values["set_variable"] = set_variable
            if sns is not None:
                self._values["sns"] = sns
            if sqs is not None:
                self._values["sqs"] = sqs

        @builtins.property
        def clear_timer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ClearTimerProperty"]]:
            '''Information needed to clear the timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-cleartimer
            '''
            result = self._values.get("clear_timer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ClearTimerProperty"]], result)

        @builtins.property
        def dynamo_db(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.DynamoDBProperty"]]:
            '''Writes to the DynamoDB table that you created.

            The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodb
            '''
            result = self._values.get("dynamo_db")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.DynamoDBProperty"]], result)

        @builtins.property
        def dynamo_d_bv2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.DynamoDBv2Property"]]:
            '''Writes to the DynamoDB table that you created.

            The default action payload contains all attribute-value pairs that have the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify. For more information, see `Actions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-event-actions.html>`_ in *AWS IoT Events Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-dynamodbv2
            '''
            result = self._values.get("dynamo_d_bv2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.DynamoDBv2Property"]], result)

        @builtins.property
        def firehose(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.FirehoseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-firehose
            '''
            result = self._values.get("firehose")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.FirehoseProperty"]], result)

        @builtins.property
        def iot_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.IotEventsProperty"]]:
            '''Sends AWS IoT Events input, which passes information about the detector model instance and the event that triggered the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotevents
            '''
            result = self._values.get("iot_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.IotEventsProperty"]], result)

        @builtins.property
        def iot_site_wise(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.IotSiteWiseProperty"]]:
            '''Sends information about the detector model instance and the event that triggered the action to an asset property in AWS IoT SiteWise .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iotsitewise
            '''
            result = self._values.get("iot_site_wise")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.IotSiteWiseProperty"]], result)

        @builtins.property
        def iot_topic_publish(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.IotTopicPublishProperty"]]:
            '''Publishes an MQTT message with the given topic to the AWS IoT message broker.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-iottopicpublish
            '''
            result = self._values.get("iot_topic_publish")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.IotTopicPublishProperty"]], result)

        @builtins.property
        def lambda_(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.LambdaProperty"]]:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-lambda
            '''
            result = self._values.get("lambda_")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.LambdaProperty"]], result)

        @builtins.property
        def reset_timer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ResetTimerProperty"]]:
            '''Information needed to reset the timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-resettimer
            '''
            result = self._values.get("reset_timer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ResetTimerProperty"]], result)

        @builtins.property
        def set_timer(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SetTimerProperty"]]:
            '''Information needed to set the timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-settimer
            '''
            result = self._values.get("set_timer")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SetTimerProperty"]], result)

        @builtins.property
        def set_variable(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SetVariableProperty"]]:
            '''Sets a variable to a specified value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-setvariable
            '''
            result = self._values.get("set_variable")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SetVariableProperty"]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SnsProperty"]]:
            '''Sends an Amazon SNS message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SnsProperty"]], result)

        @builtins.property
        def sqs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SqsProperty"]]:
            '''Sends an Amazon SNS message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-action.html#cfn-iotevents-detectormodel-action-sqs
            '''
            result = self._values.get("sqs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.SqsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty",
        jsii_struct_bases=[],
        name_mapping={
            "offset_in_nanos": "offsetInNanos",
            "time_in_seconds": "timeInSeconds",
        },
    )
    class AssetPropertyTimestampProperty:
        def __init__(
            self,
            *,
            offset_in_nanos: typing.Optional[builtins.str] = None,
            time_in_seconds: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains timestamp information. For more information, see `TimeInNanos <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_TimeInNanos.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyTimestamp`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``timeInSeconds`` parameter can be ``'1586400675'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``offsetInNanos`` parameter can be ``$variable.time`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``timeInSeconds`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.timestamp / 1000}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param offset_in_nanos: The nanosecond offset converted from ``timeInSeconds`` . The valid range is between 0-999999999.
            :param time_in_seconds: The timestamp, in seconds, in the Unix epoch format. The valid range is between 1-31556889864403199.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                asset_property_timestamp_property = iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                    offset_in_nanos="offsetInNanos",
                    time_in_seconds="timeInSeconds"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__27bb8b8d5d6292c976272f983bcc4e8473095abc2e3d8f5955bbc57244ce36b9)
                check_type(argname="argument offset_in_nanos", value=offset_in_nanos, expected_type=type_hints["offset_in_nanos"])
                check_type(argname="argument time_in_seconds", value=time_in_seconds, expected_type=type_hints["time_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if offset_in_nanos is not None:
                self._values["offset_in_nanos"] = offset_in_nanos
            if time_in_seconds is not None:
                self._values["time_in_seconds"] = time_in_seconds

        @builtins.property
        def offset_in_nanos(self) -> typing.Optional[builtins.str]:
            '''The nanosecond offset converted from ``timeInSeconds`` .

            The valid range is between 0-999999999.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html#cfn-iotevents-detectormodel-assetpropertytimestamp-offsetinnanos
            '''
            result = self._values.get("offset_in_nanos")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_in_seconds(self) -> typing.Optional[builtins.str]:
            '''The timestamp, in seconds, in the Unix epoch format.

            The valid range is between 1-31556889864403199.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertytimestamp.html#cfn-iotevents-detectormodel-assetpropertytimestamp-timeinseconds
            '''
            result = self._values.get("time_in_seconds")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyTimestampProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "quality": "quality",
            "timestamp": "timestamp",
            "value": "value",
        },
    )
    class AssetPropertyValueProperty:
        def __init__(
            self,
            *,
            quality: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.AssetPropertyVariantProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure that contains value information. For more information, see `AssetPropertyValue <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetPropertyValue.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyValue`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``quality`` parameter can be ``'GOOD'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``quality`` parameter can be ``$input.TemperatureInput.sensorData.quality`` .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param quality: The quality of the asset property value. The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .
            :param timestamp: The timestamp associated with the asset property value. The default is the current event time.
            :param value: The value to send to an asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                asset_property_value_property = iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                    quality="quality",
                    timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                        offset_in_nanos="offsetInNanos",
                        time_in_seconds="timeInSeconds"
                    ),
                    value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                        boolean_value="booleanValue",
                        double_value="doubleValue",
                        integer_value="integerValue",
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3e3c7ce9dc7f70750e9c1c6df361e4e9231686910e7fd2935269c17d75c8995)
                check_type(argname="argument quality", value=quality, expected_type=type_hints["quality"])
                check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if quality is not None:
                self._values["quality"] = quality
            if timestamp is not None:
                self._values["timestamp"] = timestamp
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def quality(self) -> typing.Optional[builtins.str]:
            '''The quality of the asset property value.

            The value must be ``'GOOD'`` , ``'BAD'`` , or ``'UNCERTAIN'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-quality
            '''
            result = self._values.get("quality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty"]]:
            '''The timestamp associated with the asset property value.

            The default is the current event time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty"]], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.AssetPropertyVariantProperty"]]:
            '''The value to send to an asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvalue.html#cfn-iotevents-detectormodel-assetpropertyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.AssetPropertyVariantProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "integer_value": "integerValue",
            "string_value": "stringValue",
        },
    )
    class AssetPropertyVariantProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[builtins.str] = None,
            double_value: typing.Optional[builtins.str] = None,
            integer_value: typing.Optional[builtins.str] = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains an asset property value.

            For more information, see `Variant <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_Variant.html>`_ in the *AWS IoT SiteWise API Reference* .

            You must use expressions for all parameters in ``AssetPropertyVariant`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``integerValue`` parameter can be ``'100'`` .

            - For references, you must specify either variables or parameters. For example, the value for the ``booleanValue`` parameter can be ``$variable.offline`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``doubleValue`` parameter uses a substitution template.

            ``'${$input.TemperatureInput.sensorData.temperature * 6 / 5 + 32}'``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            You must specify one of the following value types, depending on the ``dataType`` of the specified asset property. For more information, see `AssetProperty <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_AssetProperty.html>`_ in the *AWS IoT SiteWise API Reference* .

            :param boolean_value: The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` . You must use an expression, and the evaluated result should be a Boolean value.
            :param double_value: The asset property value is a double. You must use an expression, and the evaluated result should be a double.
            :param integer_value: The asset property value is an integer. You must use an expression, and the evaluated result should be an integer.
            :param string_value: The asset property value is a string. You must use an expression, and the evaluated result should be a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                asset_property_variant_property = iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                    boolean_value="booleanValue",
                    double_value="doubleValue",
                    integer_value="integerValue",
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3913825f4d04dfdb1643d1aaa15bc86c3eafcc96b0778589e085f17a9dc63337)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument integer_value", value=integer_value, expected_type=type_hints["integer_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if integer_value is not None:
                self._values["integer_value"] = integer_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a Boolean value that must be ``'TRUE'`` or ``'FALSE'`` .

            You must use an expression, and the evaluated result should be a Boolean value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def double_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a double.

            You must use an expression, and the evaluated result should be a double.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integer_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is an integer.

            You must use an expression, and the evaluated result should be an integer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-integervalue
            '''
            result = self._values.get("integer_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''The asset property value is a string.

            You must use an expression, and the evaluated result should be a string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-assetpropertyvariant.html#cfn-iotevents-detectormodel-assetpropertyvariant-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyVariantProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.ClearTimerProperty",
        jsii_struct_bases=[],
        name_mapping={"timer_name": "timerName"},
    )
    class ClearTimerProperty:
        def __init__(self, *, timer_name: typing.Optional[builtins.str] = None) -> None:
            '''Information needed to clear the timer.

            :param timer_name: The name of the timer to clear.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-cleartimer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                clear_timer_property = iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__41a93e4deb81fbac6127b1f2df0d8dc0ca21f5f141e03dfa69bff66a6fabc308)
                check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timer_name is not None:
                self._values["timer_name"] = timer_name

        @builtins.property
        def timer_name(self) -> typing.Optional[builtins.str]:
            '''The name of the timer to clear.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-cleartimer.html#cfn-iotevents-detectormodel-cleartimer-timername
            '''
            result = self._values.get("timer_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClearTimerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"initial_state_name": "initialStateName", "states": "states"},
    )
    class DetectorModelDefinitionProperty:
        def __init__(
            self,
            *,
            initial_state_name: typing.Optional[builtins.str] = None,
            states: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.StateProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information that defines how a detector operates.

            :param initial_state_name: The state that is entered at the creation of each detector (instance).
            :param states: Information about the states of the detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                detector_model_definition_property = iotevents_mixins.CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty(
                    initial_state_name="initialStateName",
                    states=[iotevents_mixins.CfnDetectorModelPropsMixin.StateProperty(
                        on_enter=iotevents_mixins.CfnDetectorModelPropsMixin.OnEnterProperty(
                            events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName"
                            )]
                        ),
                        on_exit=iotevents_mixins.CfnDetectorModelPropsMixin.OnExitProperty(
                            events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName"
                            )]
                        ),
                        on_input=iotevents_mixins.CfnDetectorModelPropsMixin.OnInputProperty(
                            events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName"
                            )],
                            transition_events=[iotevents_mixins.CfnDetectorModelPropsMixin.TransitionEventProperty(
                                actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                    clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                        hash_key_field="hashKeyField",
                                        hash_key_type="hashKeyType",
                                        hash_key_value="hashKeyValue",
                                        operation="operation",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        payload_field="payloadField",
                                        range_key_field="rangeKeyField",
                                        range_key_type="rangeKeyType",
                                        range_key_value="rangeKeyValue",
                                        table_name="tableName"
                                    ),
                                    dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        table_name="tableName"
                                    ),
                                    firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                        delivery_stream_name="deliveryStreamName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        separator="separator"
                                    ),
                                    iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                        input_name="inputName",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                        asset_id="assetId",
                                        entry_id="entryId",
                                        property_alias="propertyAlias",
                                        property_id="propertyId",
                                        property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                            quality="quality",
                                            timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                                offset_in_nanos="offsetInNanos",
                                                time_in_seconds="timeInSeconds"
                                            ),
                                            value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                                boolean_value="booleanValue",
                                                double_value="doubleValue",
                                                integer_value="integerValue",
                                                string_value="stringValue"
                                            )
                                        )
                                    ),
                                    iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                        mqtt_topic="mqttTopic",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                        function_arn="functionArn",
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        )
                                    ),
                                    reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                        timer_name="timerName"
                                    ),
                                    set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                        duration_expression="durationExpression",
                                        seconds=123,
                                        timer_name="timerName"
                                    ),
                                    set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                        value="value",
                                        variable_name="variableName"
                                    ),
                                    sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        target_arn="targetArn"
                                    ),
                                    sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                        payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                            content_expression="contentExpression",
                                            type="type"
                                        ),
                                        queue_url="queueUrl",
                                        use_base64=False
                                    )
                                )],
                                condition="condition",
                                event_name="eventName",
                                next_state="nextState"
                            )]
                        ),
                        state_name="stateName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45663007aed6e9e50d4dcca6f5b921125cd55f13e3db3efeaf27061619c5b533)
                check_type(argname="argument initial_state_name", value=initial_state_name, expected_type=type_hints["initial_state_name"])
                check_type(argname="argument states", value=states, expected_type=type_hints["states"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if initial_state_name is not None:
                self._values["initial_state_name"] = initial_state_name
            if states is not None:
                self._values["states"] = states

        @builtins.property
        def initial_state_name(self) -> typing.Optional[builtins.str]:
            '''The state that is entered at the creation of each detector (instance).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-initialstatename
            '''
            result = self._values.get("initial_state_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def states(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.StateProperty"]]]]:
            '''Information about the states of the detector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-detectormodeldefinition.html#cfn-iotevents-detectormodel-detectormodeldefinition-states
            '''
            result = self._values.get("states")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.StateProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DetectorModelDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.DynamoDBProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hash_key_field": "hashKeyField",
            "hash_key_type": "hashKeyType",
            "hash_key_value": "hashKeyValue",
            "operation": "operation",
            "payload": "payload",
            "payload_field": "payloadField",
            "range_key_field": "rangeKeyField",
            "range_key_type": "rangeKeyType",
            "range_key_value": "rangeKeyValue",
            "table_name": "tableName",
        },
    )
    class DynamoDBProperty:
        def __init__(
            self,
            *,
            hash_key_field: typing.Optional[builtins.str] = None,
            hash_key_type: typing.Optional[builtins.str] = None,
            hash_key_value: typing.Optional[builtins.str] = None,
            operation: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            payload_field: typing.Optional[builtins.str] = None,
            range_key_field: typing.Optional[builtins.str] = None,
            range_key_type: typing.Optional[builtins.str] = None,
            range_key_value: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The standard action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . One column of the DynamoDB table receives all attribute-value pairs in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBAction`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``hashKeyType`` parameter can be ``'STRING'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``hashKeyField`` parameter can be ``$input.GreenhouseInput.name`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``hashKeyValue`` parameter uses a substitution template.

            ``'${$input.GreenhouseInput.temperature * 6 / 5 + 32} in Fahrenheit'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            If the defined payload type is a string, ``DynamoDBAction`` writes non-JSON data to the DynamoDB table as binary data. The DynamoDB console displays the data as Base64-encoded text. The value for the ``payloadField`` parameter is ``<payload-field>_raw`` .

            :param hash_key_field: The name of the hash key (also called the partition key). The ``hashKeyField`` value must match the partition key of the target DynamoDB table.
            :param hash_key_type: The data type for the hash key (also called the partition key). You can specify the following values:. - ``'STRING'`` - The hash key is a string. - ``'NUMBER'`` - The hash key is a number. If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .
            :param hash_key_value: The value of the hash key (also called the partition key).
            :param operation: The type of operation to perform. You can specify the following values:. - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key. - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key. If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.
            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .
            :param payload_field: The name of the DynamoDB column that receives the action payload. If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .
            :param range_key_field: The name of the range key (also called the sort key). The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.
            :param range_key_type: The data type for the range key (also called the sort key), You can specify the following values:. - ``'STRING'`` - The range key is a string. - ``'NUMBER'`` - The range key is number. If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .
            :param range_key_value: The value of the range key (also called the sort key).
            :param table_name: The name of the DynamoDB table. The ``tableName`` value must match the table name of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                dynamo_dBProperty = iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                    hash_key_field="hashKeyField",
                    hash_key_type="hashKeyType",
                    hash_key_value="hashKeyValue",
                    operation="operation",
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    payload_field="payloadField",
                    range_key_field="rangeKeyField",
                    range_key_type="rangeKeyType",
                    range_key_value="rangeKeyValue",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6193985997a8c0a323039f634523782dfd61a9d952561c8dd875fa7de37d1b17)
                check_type(argname="argument hash_key_field", value=hash_key_field, expected_type=type_hints["hash_key_field"])
                check_type(argname="argument hash_key_type", value=hash_key_type, expected_type=type_hints["hash_key_type"])
                check_type(argname="argument hash_key_value", value=hash_key_value, expected_type=type_hints["hash_key_value"])
                check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument payload_field", value=payload_field, expected_type=type_hints["payload_field"])
                check_type(argname="argument range_key_field", value=range_key_field, expected_type=type_hints["range_key_field"])
                check_type(argname="argument range_key_type", value=range_key_type, expected_type=type_hints["range_key_type"])
                check_type(argname="argument range_key_value", value=range_key_value, expected_type=type_hints["range_key_value"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hash_key_field is not None:
                self._values["hash_key_field"] = hash_key_field
            if hash_key_type is not None:
                self._values["hash_key_type"] = hash_key_type
            if hash_key_value is not None:
                self._values["hash_key_value"] = hash_key_value
            if operation is not None:
                self._values["operation"] = operation
            if payload is not None:
                self._values["payload"] = payload
            if payload_field is not None:
                self._values["payload_field"] = payload_field
            if range_key_field is not None:
                self._values["range_key_field"] = range_key_field
            if range_key_type is not None:
                self._values["range_key_type"] = range_key_type
            if range_key_value is not None:
                self._values["range_key_value"] = range_key_value
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def hash_key_field(self) -> typing.Optional[builtins.str]:
            '''The name of the hash key (also called the partition key).

            The ``hashKeyField`` value must match the partition key of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeyfield
            '''
            result = self._values.get("hash_key_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hash_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the hash key (also called the partition key). You can specify the following values:.

            - ``'STRING'`` - The hash key is a string.
            - ``'NUMBER'`` - The hash key is a number.

            If you don't specify ``hashKeyType`` , the default value is ``'STRING'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeytype
            '''
            result = self._values.get("hash_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hash_key_value(self) -> typing.Optional[builtins.str]:
            '''The value of the hash key (also called the partition key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-hashkeyvalue
            '''
            result = self._values.get("hash_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation(self) -> typing.Optional[builtins.str]:
            '''The type of operation to perform. You can specify the following values:.

            - ``'INSERT'`` - Insert data as a new item into the DynamoDB table. This item uses the specified hash key as a partition key. If you specified a range key, the item uses the range key as a sort key.
            - ``'UPDATE'`` - Update an existing item of the DynamoDB table with new data. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.
            - ``'DELETE'`` - Delete an existing item of the DynamoDB table. This item's partition key must match the specified hash key. If you specified a range key, the range key must match the item's sort key.

            If you don't specify this parameter, AWS IoT Events triggers the ``'INSERT'`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-operation
            '''
            result = self._values.get("operation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def payload_field(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB column that receives the action payload.

            If you don't specify this parameter, the name of the DynamoDB column is ``payload`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-payloadfield
            '''
            result = self._values.get("payload_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_field(self) -> typing.Optional[builtins.str]:
            '''The name of the range key (also called the sort key).

            The ``rangeKeyField`` value must match the sort key of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeyfield
            '''
            result = self._values.get("range_key_field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_type(self) -> typing.Optional[builtins.str]:
            '''The data type for the range key (also called the sort key), You can specify the following values:.

            - ``'STRING'`` - The range key is a string.
            - ``'NUMBER'`` - The range key is number.

            If you don't specify ``rangeKeyField`` , the default value is ``'STRING'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeytype
            '''
            result = self._values.get("range_key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def range_key_value(self) -> typing.Optional[builtins.str]:
            '''The value of the range key (also called the sort key).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-rangekeyvalue
            '''
            result = self._values.get("range_key_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB table.

            The ``tableName`` value must match the table name of the target DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodb.html#cfn-iotevents-detectormodel-dynamodb-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property",
        jsii_struct_bases=[],
        name_mapping={"payload": "payload", "table_name": "tableName"},
    )
    class DynamoDBv2Property:
        def __init__(
            self,
            *,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines an action to write to the Amazon DynamoDB table that you created.

            The default action payload contains all the information about the detector model instance and the event that triggered the action. You can customize the `payload <https://docs.aws.amazon.com/iotevents/latest/apireference/API_Payload.html>`_ . A separate column of the DynamoDB table receives one attribute-value pair in the payload that you specify.

            You must use expressions for all parameters in ``DynamoDBv2Action`` . The expressions accept literals, operators, functions, references, and substitution templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``tableName`` parameter can be ``'GreenhouseTemperatureTable'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``tableName`` parameter can be ``$variable.ddbtableName`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``contentExpression`` parameter in ``Payload`` uses a substitution template.

            ``'{\\"sensorID\\": \\"${$input.GreenhouseInput.sensor_id}\\", \\"temperature\\": \\"${$input.GreenhouseInput.temperature * 9 / 5 + 32}\\"}'``

            - For a string concatenation, you must use ``+`` . A string concatenation can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``tableName`` parameter uses a string concatenation.

            ``'GreenhouseTemperatureTable ' + $input.GreenhouseInput.date``

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            The value for the ``type`` parameter in ``Payload`` must be ``JSON`` .

            :param payload: Information needed to configure the payload. By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .
            :param table_name: The name of the DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                dynamo_dBv2_property = iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b310dd62c15cfd42a2877a032504a5235d69f371a2c2ab29c9db186796033bfd)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the DynamoDB table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-dynamodbv2.html#cfn-iotevents-detectormodel-dynamodbv2-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DynamoDBv2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.EventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "condition": "condition",
            "event_name": "eventName",
        },
    )
    class EventProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            condition: typing.Optional[builtins.str] = None,
            event_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the ``actions`` to be performed when the ``condition`` evaluates to TRUE.

            :param actions: The actions to be performed.
            :param condition: Optional. The Boolean expression that, when TRUE, causes the ``actions`` to be performed. If not present, the actions are performed (=TRUE). If the expression result is not a Boolean value, the actions are not performed (=FALSE).
            :param event_name: The name of the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                event_property = iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                    actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                        clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                            timer_name="timerName"
                        ),
                        dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_type="hashKeyType",
                            hash_key_value="hashKeyValue",
                            operation="operation",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue",
                            table_name="tableName"
                        ),
                        dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            table_name="tableName"
                        ),
                        firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                            input_name="inputName",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId",
                            property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                quality="quality",
                                timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                    offset_in_nanos="offsetInNanos",
                                    time_in_seconds="timeInSeconds"
                                ),
                                value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                )
                            )
                        ),
                        iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                            function_arn="functionArn",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                            timer_name="timerName"
                        ),
                        set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                            duration_expression="durationExpression",
                            seconds=123,
                            timer_name="timerName"
                        ),
                        set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                            value="value",
                            variable_name="variableName"
                        ),
                        sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            target_arn="targetArn"
                        ),
                        sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            queue_url="queueUrl",
                            use_base64=False
                        )
                    )],
                    condition="condition",
                    event_name="eventName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6d374a401522bb63c5fd1e32dee5a321922c65ecdb22a1d519147410de635cd)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if condition is not None:
                self._values["condition"] = condition
            if event_name is not None:
                self._values["event_name"] = event_name

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ActionProperty"]]]]:
            '''The actions to be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ActionProperty"]]]], result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''Optional.

            The Boolean expression that, when TRUE, causes the ``actions`` to be performed. If not present, the actions are performed (=TRUE). If the expression result is not a Boolean value, the actions are not performed (=FALSE).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_name(self) -> typing.Optional[builtins.str]:
            '''The name of the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-event.html#cfn-iotevents-detectormodel-event-eventname
            '''
            result = self._values.get("event_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.FirehoseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_stream_name": "deliveryStreamName",
            "payload": "payload",
            "separator": "separator",
        },
    )
    class FirehoseProperty:
        def __init__(
            self,
            *,
            delivery_stream_name: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            separator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon Kinesis Data Firehose delivery stream.

            :param delivery_stream_name: The name of the Kinesis Data Firehose delivery stream where the data is written.
            :param payload: You can configure the action payload when you send a message to an Amazon Data Firehose delivery stream.
            :param separator: A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream. Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                firehose_property = iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                    delivery_stream_name="deliveryStreamName",
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    separator="separator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b82cae05cd72d86df560734db81af243e70552af00b50a2ef0d9c9021f788c9)
                check_type(argname="argument delivery_stream_name", value=delivery_stream_name, expected_type=type_hints["delivery_stream_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delivery_stream_name is not None:
                self._values["delivery_stream_name"] = delivery_stream_name
            if payload is not None:
                self._values["payload"] = payload
            if separator is not None:
                self._values["separator"] = separator

        @builtins.property
        def delivery_stream_name(self) -> typing.Optional[builtins.str]:
            '''The name of the Kinesis Data Firehose delivery stream where the data is written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-deliverystreamname
            '''
            result = self._values.get("delivery_stream_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon Data Firehose delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def separator(self) -> typing.Optional[builtins.str]:
            '''A character separator that is used to separate records written to the Kinesis Data Firehose delivery stream.

            Valid values are: '\\n' (newline), '\\t' (tab), '\\r\\n' (Windows newline), ',' (comma).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-firehose.html#cfn-iotevents-detectormodel-firehose-separator
            '''
            result = self._values.get("separator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirehoseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.IotEventsProperty",
        jsii_struct_bases=[],
        name_mapping={"input_name": "inputName", "payload": "payload"},
    )
    class IotEventsProperty:
        def __init__(
            self,
            *,
            input_name: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends an AWS IoT Events input, passing in information about the detector model instance and the event that triggered the action.

            :param input_name: The name of the AWS IoT Events input where the data is sent.
            :param payload: You can configure the action payload when you send a message to an AWS IoT Events input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                iot_events_property = iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                    input_name="inputName",
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__36cad8c9e9a957eed118c1184875661ccafe7c69547cb8680a04d651f304fff9)
                check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_name is not None:
                self._values["input_name"] = input_name
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def input_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS IoT Events input where the data is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-inputname
            '''
            result = self._values.get("input_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an AWS IoT Events input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotevents.html#cfn-iotevents-detectormodel-iotevents-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotEventsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asset_id": "assetId",
            "entry_id": "entryId",
            "property_alias": "propertyAlias",
            "property_id": "propertyId",
            "property_value": "propertyValue",
        },
    )
    class IotSiteWiseProperty:
        def __init__(
            self,
            *,
            asset_id: typing.Optional[builtins.str] = None,
            entry_id: typing.Optional[builtins.str] = None,
            property_alias: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
            property_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.AssetPropertyValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to a specified asset property in AWS IoT SiteWise .

            You must use expressions for all parameters in ``IotSiteWiseAction`` . The expressions accept literals, operators, functions, references, and substitutions templates.

            **Examples** - For literal values, the expressions must contain single quotes. For example, the value for the ``propertyAlias`` parameter can be ``'/company/windfarm/3/turbine/7/temperature'`` .

            - For references, you must specify either variables or input values. For example, the value for the ``assetId`` parameter can be ``$input.TurbineInput.assetId1`` .
            - For a substitution template, you must use ``${}`` , and the template must be in single quotes. A substitution template can also contain a combination of literals, operators, functions, references, and substitution templates.

            In the following example, the value for the ``propertyAlias`` parameter uses a substitution template.

            ``'company/windfarm/${$input.TemperatureInput.sensorData.windfarmID}/turbine/ ${$input.TemperatureInput.sensorData.turbineID}/temperature'``

            You must specify either ``propertyAlias`` or both ``assetId`` and ``propertyId`` to identify the target asset property in AWS IoT SiteWise .

            For more information, see `Expressions <https://docs.aws.amazon.com/iotevents/latest/developerguide/iotevents-expressions.html>`_ in the *AWS IoT Events Developer Guide* .

            :param asset_id: The ID of the asset that has the specified property.
            :param entry_id: A unique identifier for this entry. You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.
            :param property_alias: The alias of the asset property.
            :param property_id: The ID of the asset property.
            :param property_value: The value to send to the asset property. This value contains timestamp, quality, and value (TQV) information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                iot_site_wise_property = iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                    asset_id="assetId",
                    entry_id="entryId",
                    property_alias="propertyAlias",
                    property_id="propertyId",
                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                        quality="quality",
                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                            offset_in_nanos="offsetInNanos",
                            time_in_seconds="timeInSeconds"
                        ),
                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                            boolean_value="booleanValue",
                            double_value="doubleValue",
                            integer_value="integerValue",
                            string_value="stringValue"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e220f619a8405516aa36eae4a541a1c3bbec460dd5948a8badfe0ef89c400043)
                check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
                check_type(argname="argument entry_id", value=entry_id, expected_type=type_hints["entry_id"])
                check_type(argname="argument property_alias", value=property_alias, expected_type=type_hints["property_alias"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
                check_type(argname="argument property_value", value=property_value, expected_type=type_hints["property_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_id is not None:
                self._values["asset_id"] = asset_id
            if entry_id is not None:
                self._values["entry_id"] = entry_id
            if property_alias is not None:
                self._values["property_alias"] = property_alias
            if property_id is not None:
                self._values["property_id"] = property_id
            if property_value is not None:
                self._values["property_value"] = property_value

        @builtins.property
        def asset_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset that has the specified property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-assetid
            '''
            result = self._values.get("asset_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entry_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for this entry.

            You can use the entry ID to track which data entry causes an error in case of failure. The default is a new unique identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-entryid
            '''
            result = self._values.get("entry_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_alias(self) -> typing.Optional[builtins.str]:
            '''The alias of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyalias
            '''
            result = self._values.get("property_alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.AssetPropertyValueProperty"]]:
            '''The value to send to the asset property.

            This value contains timestamp, quality, and value (TQV) information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iotsitewise.html#cfn-iotevents-detectormodel-iotsitewise-propertyvalue
            '''
            result = self._values.get("property_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.AssetPropertyValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotSiteWiseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty",
        jsii_struct_bases=[],
        name_mapping={"mqtt_topic": "mqttTopic", "payload": "payload"},
    )
    class IotTopicPublishProperty:
        def __init__(
            self,
            *,
            mqtt_topic: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information required to publish the MQTT message through the AWS IoT message broker.

            :param mqtt_topic: The MQTT topic of the message. You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.
            :param payload: You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                iot_topic_publish_property = iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                    mqtt_topic="mqttTopic",
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e58c4454e5fb8082e61ac5a83ab2a4c1fb8b26fc54322eca521836398a95358f)
                check_type(argname="argument mqtt_topic", value=mqtt_topic, expected_type=type_hints["mqtt_topic"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mqtt_topic is not None:
                self._values["mqtt_topic"] = mqtt_topic
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def mqtt_topic(self) -> typing.Optional[builtins.str]:
            '''The MQTT topic of the message.

            You can use a string expression that includes variables ( ``$variable.<variable-name>`` ) and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the topic string.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-mqtttopic
            '''
            result = self._values.get("mqtt_topic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you publish a message to an AWS IoT Core topic.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-iottopicpublish.html#cfn-iotevents-detectormodel-iottopicpublish-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IotTopicPublishProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.LambdaProperty",
        jsii_struct_bases=[],
        name_mapping={"function_arn": "functionArn", "payload": "payload"},
    )
    class LambdaProperty:
        def __init__(
            self,
            *,
            function_arn: typing.Optional[builtins.str] = None,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Calls a Lambda function, passing in information about the detector model instance and the event that triggered the action.

            :param function_arn: The ARN of the Lambda function that is executed.
            :param payload: You can configure the action payload when you send a message to a Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                lambda_property = iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                    function_arn="functionArn",
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__746b58641282fdfd9712ec99315a2874f22bbc0875e559ec00d4b6f8f677993c)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if function_arn is not None:
                self._values["function_arn"] = function_arn
            if payload is not None:
                self._values["payload"] = payload

        @builtins.property
        def function_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function that is executed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-functionarn
            '''
            result = self._values.get("function_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to a Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-lambda.html#cfn-iotevents-detectormodel-lambda-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.OnEnterProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class OnEnterProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.EventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''When entering this state, perform these ``actions`` if the ``condition`` is TRUE.

            :param events: Specifies the actions that are performed when the state is entered and the ``condition`` is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                on_enter_property = iotevents_mixins.CfnDetectorModelPropsMixin.OnEnterProperty(
                    events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                        actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                            clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_type="hashKeyType",
                                hash_key_value="hashKeyValue",
                                operation="operation",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue",
                                table_name="tableName"
                            ),
                            dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                table_name="tableName"
                            ),
                            firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                input_name="inputName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId",
                                property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                    quality="quality",
                                    timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                        offset_in_nanos="offsetInNanos",
                                        time_in_seconds="timeInSeconds"
                                    ),
                                    value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    )
                                )
                            ),
                            iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                function_arn="functionArn",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                duration_expression="durationExpression",
                                seconds=123,
                                timer_name="timerName"
                            ),
                            set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                target_arn="targetArn"
                            ),
                            sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                queue_url="queueUrl",
                                use_base64=False
                            )
                        )],
                        condition="condition",
                        event_name="eventName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__08fd4f9afeac8a0364c5b07f308162c8d2a2ff86b5b6490c6fd73867b33f07ae)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.EventProperty"]]]]:
            '''Specifies the actions that are performed when the state is entered and the ``condition`` is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onenter.html#cfn-iotevents-detectormodel-onenter-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.EventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnEnterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.OnExitProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class OnExitProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.EventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .

            :param events: Specifies the ``actions`` that are performed when the state is exited and the ``condition`` is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                on_exit_property = iotevents_mixins.CfnDetectorModelPropsMixin.OnExitProperty(
                    events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                        actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                            clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_type="hashKeyType",
                                hash_key_value="hashKeyValue",
                                operation="operation",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue",
                                table_name="tableName"
                            ),
                            dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                table_name="tableName"
                            ),
                            firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                input_name="inputName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId",
                                property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                    quality="quality",
                                    timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                        offset_in_nanos="offsetInNanos",
                                        time_in_seconds="timeInSeconds"
                                    ),
                                    value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    )
                                )
                            ),
                            iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                function_arn="functionArn",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                duration_expression="durationExpression",
                                seconds=123,
                                timer_name="timerName"
                            ),
                            set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                target_arn="targetArn"
                            ),
                            sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                queue_url="queueUrl",
                                use_base64=False
                            )
                        )],
                        condition="condition",
                        event_name="eventName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9466f6299a646b523e58a201e1a96c70f34b44ad624a26dea66037d0825d96aa)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.EventProperty"]]]]:
            '''Specifies the ``actions`` that are performed when the state is exited and the ``condition`` is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-onexit.html#cfn-iotevents-detectormodel-onexit-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.EventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnExitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.OnInputProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events", "transition_events": "transitionEvents"},
    )
    class OnInputProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.EventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            transition_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.TransitionEventProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the actions performed when the ``condition`` evaluates to TRUE.

            :param events: Specifies the actions performed when the ``condition`` evaluates to TRUE.
            :param transition_events: Specifies the actions performed, and the next state entered, when a ``condition`` evaluates to TRUE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                on_input_property = iotevents_mixins.CfnDetectorModelPropsMixin.OnInputProperty(
                    events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                        actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                            clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_type="hashKeyType",
                                hash_key_value="hashKeyValue",
                                operation="operation",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue",
                                table_name="tableName"
                            ),
                            dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                table_name="tableName"
                            ),
                            firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                input_name="inputName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId",
                                property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                    quality="quality",
                                    timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                        offset_in_nanos="offsetInNanos",
                                        time_in_seconds="timeInSeconds"
                                    ),
                                    value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    )
                                )
                            ),
                            iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                function_arn="functionArn",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                duration_expression="durationExpression",
                                seconds=123,
                                timer_name="timerName"
                            ),
                            set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                target_arn="targetArn"
                            ),
                            sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                queue_url="queueUrl",
                                use_base64=False
                            )
                        )],
                        condition="condition",
                        event_name="eventName"
                    )],
                    transition_events=[iotevents_mixins.CfnDetectorModelPropsMixin.TransitionEventProperty(
                        actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                            clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                timer_name="timerName"
                            ),
                            dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                hash_key_field="hashKeyField",
                                hash_key_type="hashKeyType",
                                hash_key_value="hashKeyValue",
                                operation="operation",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                payload_field="payloadField",
                                range_key_field="rangeKeyField",
                                range_key_type="rangeKeyType",
                                range_key_value="rangeKeyValue",
                                table_name="tableName"
                            ),
                            dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                table_name="tableName"
                            ),
                            firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                delivery_stream_name="deliveryStreamName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                separator="separator"
                            ),
                            iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                input_name="inputName",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                asset_id="assetId",
                                entry_id="entryId",
                                property_alias="propertyAlias",
                                property_id="propertyId",
                                property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                    quality="quality",
                                    timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                        offset_in_nanos="offsetInNanos",
                                        time_in_seconds="timeInSeconds"
                                    ),
                                    value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                        boolean_value="booleanValue",
                                        double_value="doubleValue",
                                        integer_value="integerValue",
                                        string_value="stringValue"
                                    )
                                )
                            ),
                            iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                mqtt_topic="mqttTopic",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                function_arn="functionArn",
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                )
                            ),
                            reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                timer_name="timerName"
                            ),
                            set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                duration_expression="durationExpression",
                                seconds=123,
                                timer_name="timerName"
                            ),
                            set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                value="value",
                                variable_name="variableName"
                            ),
                            sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                target_arn="targetArn"
                            ),
                            sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                    content_expression="contentExpression",
                                    type="type"
                                ),
                                queue_url="queueUrl",
                                use_base64=False
                            )
                        )],
                        condition="condition",
                        event_name="eventName",
                        next_state="nextState"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70ab32c38665458e1e5e2bafa89e7da8c0b529a5143cc9a3af9d0924b186de43)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
                check_type(argname="argument transition_events", value=transition_events, expected_type=type_hints["transition_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events
            if transition_events is not None:
                self._values["transition_events"] = transition_events

        @builtins.property
        def events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.EventProperty"]]]]:
            '''Specifies the actions performed when the ``condition`` evaluates to TRUE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.EventProperty"]]]], result)

        @builtins.property
        def transition_events(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.TransitionEventProperty"]]]]:
            '''Specifies the actions performed, and the next state entered, when a ``condition`` evaluates to TRUE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-oninput.html#cfn-iotevents-detectormodel-oninput-transitionevents
            '''
            result = self._values.get("transition_events")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.TransitionEventProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OnInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.PayloadProperty",
        jsii_struct_bases=[],
        name_mapping={"content_expression": "contentExpression", "type": "type"},
    )
    class PayloadProperty:
        def __init__(
            self,
            *,
            content_expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information needed to configure the payload.

            By default, AWS IoT Events generates a standard payload in JSON for any action. This action payload contains all attribute-value pairs that have the information about the detector model instance and the event triggered the action. To configure the action payload, you can use ``contentExpression`` .

            :param content_expression: The content of the payload. You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.
            :param type: The value of the payload type can be either ``STRING`` or ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                payload_property = iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                    content_expression="contentExpression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7773e440c229a886826407d9e08429e2e046d8eaa7893b7eb6767e5b0bc56b4)
                check_type(argname="argument content_expression", value=content_expression, expected_type=type_hints["content_expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_expression is not None:
                self._values["content_expression"] = content_expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def content_expression(self) -> typing.Optional[builtins.str]:
            '''The content of the payload.

            You can use a string expression that includes quoted strings ( ``'<string>'`` ), variables ( ``$variable.<variable-name>`` ), input values ( ``$input.<input-name>.<path-to-datum>`` ), string concatenations, and quoted strings that contain ``${}`` as the content. The recommended maximum size of a content expression is 1 KB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html#cfn-iotevents-detectormodel-payload-contentexpression
            '''
            result = self._values.get("content_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The value of the payload type can be either ``STRING`` or ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-payload.html#cfn-iotevents-detectormodel-payload-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PayloadProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.ResetTimerProperty",
        jsii_struct_bases=[],
        name_mapping={"timer_name": "timerName"},
    )
    class ResetTimerProperty:
        def __init__(self, *, timer_name: typing.Optional[builtins.str] = None) -> None:
            '''Information required to reset the timer.

            The timer is reset to the previously evaluated result of the duration. The duration expression isn't reevaluated when you reset the timer.

            :param timer_name: The name of the timer to reset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-resettimer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                reset_timer_property = iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__268ee25dc374e233f795e0cd3a18b7a3f2c481da5cebd9c5e5aa640448d5e0d9)
                check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timer_name is not None:
                self._values["timer_name"] = timer_name

        @builtins.property
        def timer_name(self) -> typing.Optional[builtins.str]:
            '''The name of the timer to reset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-resettimer.html#cfn-iotevents-detectormodel-resettimer-timername
            '''
            result = self._values.get("timer_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResetTimerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.SetTimerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_expression": "durationExpression",
            "seconds": "seconds",
            "timer_name": "timerName",
        },
    )
    class SetTimerProperty:
        def __init__(
            self,
            *,
            duration_expression: typing.Optional[builtins.str] = None,
            seconds: typing.Optional[jsii.Number] = None,
            timer_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information needed to set the timer.

            :param duration_expression: The duration of the timer, in seconds. You can use a string expression that includes numbers, variables ( ``$variable.<variable-name>`` ), and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the duration. The range of the duration is 1-31622400 seconds. To ensure accuracy, the minimum duration is 60 seconds. The evaluated result of the duration is rounded down to the nearest whole number.
            :param seconds: The number of seconds until the timer expires. The minimum value is 60 seconds to ensure accuracy. The maximum value is 31622400 seconds.
            :param timer_name: The name of the timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                set_timer_property = iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                    duration_expression="durationExpression",
                    seconds=123,
                    timer_name="timerName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f94a024fe9b3fb1f2b638764f97065e382f7c63b4534ddadf90e13e61d91853)
                check_type(argname="argument duration_expression", value=duration_expression, expected_type=type_hints["duration_expression"])
                check_type(argname="argument seconds", value=seconds, expected_type=type_hints["seconds"])
                check_type(argname="argument timer_name", value=timer_name, expected_type=type_hints["timer_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_expression is not None:
                self._values["duration_expression"] = duration_expression
            if seconds is not None:
                self._values["seconds"] = seconds
            if timer_name is not None:
                self._values["timer_name"] = timer_name

        @builtins.property
        def duration_expression(self) -> typing.Optional[builtins.str]:
            '''The duration of the timer, in seconds.

            You can use a string expression that includes numbers, variables ( ``$variable.<variable-name>`` ), and input values ( ``$input.<input-name>.<path-to-datum>`` ) as the duration. The range of the duration is 1-31622400 seconds. To ensure accuracy, the minimum duration is 60 seconds. The evaluated result of the duration is rounded down to the nearest whole number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-durationexpression
            '''
            result = self._values.get("duration_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds until the timer expires.

            The minimum value is 60 seconds to ensure accuracy. The maximum value is 31622400 seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-seconds
            '''
            result = self._values.get("seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timer_name(self) -> typing.Optional[builtins.str]:
            '''The name of the timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-settimer.html#cfn-iotevents-detectormodel-settimer-timername
            '''
            result = self._values.get("timer_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetTimerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.SetVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "variable_name": "variableName"},
    )
    class SetVariableProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[builtins.str] = None,
            variable_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the variable and its new value.

            :param value: The new value of the variable.
            :param variable_name: The name of the variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                set_variable_property = iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                    value="value",
                    variable_name="variableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a0cc4912f2e62bc84708729538a6df0b54ce14c7c4b4893757a65fe9ee412fd)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if variable_name is not None:
                self._values["variable_name"] = variable_name

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The new value of the variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html#cfn-iotevents-detectormodel-setvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variable_name(self) -> typing.Optional[builtins.str]:
            '''The name of the variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-setvariable.html#cfn-iotevents-detectormodel-setvariable-variablename
            '''
            result = self._values.get("variable_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SetVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.SnsProperty",
        jsii_struct_bases=[],
        name_mapping={"payload": "payload", "target_arn": "targetArn"},
    )
    class SnsProperty:
        def __init__(
            self,
            *,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information required to publish the Amazon SNS message.

            :param payload: You can configure the action payload when you send a message as an Amazon SNS push notification.
            :param target_arn: The ARN of the Amazon SNS target where the message is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                sns_property = iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    target_arn="targetArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b751cfeef2f687796c048a67c4d1de397153c4a27db608541c4e5e43a259d3d5)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if target_arn is not None:
                self._values["target_arn"] = target_arn

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message as an Amazon SNS push notification.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def target_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon SNS target where the message is sent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sns.html#cfn-iotevents-detectormodel-sns-targetarn
            '''
            result = self._values.get("target_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.SqsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "payload": "payload",
            "queue_url": "queueUrl",
            "use_base64": "useBase64",
        },
    )
    class SqsProperty:
        def __init__(
            self,
            *,
            payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.PayloadProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            queue_url: typing.Optional[builtins.str] = None,
            use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Sends information about the detector model instance and the event that triggered the action to an Amazon SQS queue.

            :param payload: You can configure the action payload when you send a message to an Amazon SQS queue.
            :param queue_url: The URL of the SQS queue where the data is written.
            :param use_base64: Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue. Otherwise, set this to FALSE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                sqs_property = iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                        content_expression="contentExpression",
                        type="type"
                    ),
                    queue_url="queueUrl",
                    use_base64=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1563c421c9045ca94312646be10a90b6571890c47dc85b19331dff535f2f5195)
                check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
                check_type(argname="argument queue_url", value=queue_url, expected_type=type_hints["queue_url"])
                check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if payload is not None:
                self._values["payload"] = payload
            if queue_url is not None:
                self._values["queue_url"] = queue_url
            if use_base64 is not None:
                self._values["use_base64"] = use_base64

        @builtins.property
        def payload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]]:
            '''You can configure the action payload when you send a message to an Amazon SQS queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-payload
            '''
            result = self._values.get("payload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.PayloadProperty"]], result)

        @builtins.property
        def queue_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the SQS queue where the data is written.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-queueurl
            '''
            result = self._values.get("queue_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def use_base64(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this to TRUE if you want the data to be base-64 encoded before it is written to the queue.

            Otherwise, set this to FALSE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-sqs.html#cfn-iotevents-detectormodel-sqs-usebase64
            '''
            result = self._values.get("use_base64")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.StateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "on_enter": "onEnter",
            "on_exit": "onExit",
            "on_input": "onInput",
            "state_name": "stateName",
        },
    )
    class StateProperty:
        def __init__(
            self,
            *,
            on_enter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.OnEnterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_exit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.OnExitProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            on_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.OnInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            state_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information that defines a state of a detector.

            :param on_enter: When entering this state, perform these ``actions`` if the ``condition`` is TRUE.
            :param on_exit: When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .
            :param on_input: When an input is received and the ``condition`` is TRUE, perform the specified ``actions`` .
            :param state_name: The name of the state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                state_property = iotevents_mixins.CfnDetectorModelPropsMixin.StateProperty(
                    on_enter=iotevents_mixins.CfnDetectorModelPropsMixin.OnEnterProperty(
                        events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName"
                        )]
                    ),
                    on_exit=iotevents_mixins.CfnDetectorModelPropsMixin.OnExitProperty(
                        events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName"
                        )]
                    ),
                    on_input=iotevents_mixins.CfnDetectorModelPropsMixin.OnInputProperty(
                        events=[iotevents_mixins.CfnDetectorModelPropsMixin.EventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName"
                        )],
                        transition_events=[iotevents_mixins.CfnDetectorModelPropsMixin.TransitionEventProperty(
                            actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                                clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                                    timer_name="timerName"
                                ),
                                dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                                    hash_key_field="hashKeyField",
                                    hash_key_type="hashKeyType",
                                    hash_key_value="hashKeyValue",
                                    operation="operation",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    payload_field="payloadField",
                                    range_key_field="rangeKeyField",
                                    range_key_type="rangeKeyType",
                                    range_key_value="rangeKeyValue",
                                    table_name="tableName"
                                ),
                                dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    table_name="tableName"
                                ),
                                firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                                    delivery_stream_name="deliveryStreamName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    separator="separator"
                                ),
                                iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                                    input_name="inputName",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                                    asset_id="assetId",
                                    entry_id="entryId",
                                    property_alias="propertyAlias",
                                    property_id="propertyId",
                                    property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                        quality="quality",
                                        timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                            offset_in_nanos="offsetInNanos",
                                            time_in_seconds="timeInSeconds"
                                        ),
                                        value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                            boolean_value="booleanValue",
                                            double_value="doubleValue",
                                            integer_value="integerValue",
                                            string_value="stringValue"
                                        )
                                    )
                                ),
                                iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                                    mqtt_topic="mqttTopic",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                                    function_arn="functionArn",
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    )
                                ),
                                reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                                    timer_name="timerName"
                                ),
                                set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                                    duration_expression="durationExpression",
                                    seconds=123,
                                    timer_name="timerName"
                                ),
                                set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                                    value="value",
                                    variable_name="variableName"
                                ),
                                sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    target_arn="targetArn"
                                ),
                                sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                                    payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                        content_expression="contentExpression",
                                        type="type"
                                    ),
                                    queue_url="queueUrl",
                                    use_base64=False
                                )
                            )],
                            condition="condition",
                            event_name="eventName",
                            next_state="nextState"
                        )]
                    ),
                    state_name="stateName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__867f7b876edcaf29160843f5e49ed98686a5895356cff83fe1fe3f14a45e657b)
                check_type(argname="argument on_enter", value=on_enter, expected_type=type_hints["on_enter"])
                check_type(argname="argument on_exit", value=on_exit, expected_type=type_hints["on_exit"])
                check_type(argname="argument on_input", value=on_input, expected_type=type_hints["on_input"])
                check_type(argname="argument state_name", value=state_name, expected_type=type_hints["state_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_enter is not None:
                self._values["on_enter"] = on_enter
            if on_exit is not None:
                self._values["on_exit"] = on_exit
            if on_input is not None:
                self._values["on_input"] = on_input
            if state_name is not None:
                self._values["state_name"] = state_name

        @builtins.property
        def on_enter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.OnEnterProperty"]]:
            '''When entering this state, perform these ``actions`` if the ``condition`` is TRUE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onenter
            '''
            result = self._values.get("on_enter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.OnEnterProperty"]], result)

        @builtins.property
        def on_exit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.OnExitProperty"]]:
            '''When exiting this state, perform these ``actions`` if the specified ``condition`` is ``TRUE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-onexit
            '''
            result = self._values.get("on_exit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.OnExitProperty"]], result)

        @builtins.property
        def on_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.OnInputProperty"]]:
            '''When an input is received and the ``condition`` is TRUE, perform the specified ``actions`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-oninput
            '''
            result = self._values.get("on_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.OnInputProperty"]], result)

        @builtins.property
        def state_name(self) -> typing.Optional[builtins.str]:
            '''The name of the state.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-state.html#cfn-iotevents-detectormodel-state-statename
            '''
            result = self._values.get("state_name")
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
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnDetectorModelPropsMixin.TransitionEventProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "condition": "condition",
            "event_name": "eventName",
            "next_state": "nextState",
        },
    )
    class TransitionEventProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDetectorModelPropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            condition: typing.Optional[builtins.str] = None,
            event_name: typing.Optional[builtins.str] = None,
            next_state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the actions performed and the next state entered when a ``condition`` evaluates to TRUE.

            :param actions: The actions to be performed.
            :param condition: Required. A Boolean expression that when TRUE causes the actions to be performed and the ``nextState`` to be entered.
            :param event_name: The name of the transition event.
            :param next_state: The next state to enter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                transition_event_property = iotevents_mixins.CfnDetectorModelPropsMixin.TransitionEventProperty(
                    actions=[iotevents_mixins.CfnDetectorModelPropsMixin.ActionProperty(
                        clear_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ClearTimerProperty(
                            timer_name="timerName"
                        ),
                        dynamo_db=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBProperty(
                            hash_key_field="hashKeyField",
                            hash_key_type="hashKeyType",
                            hash_key_value="hashKeyValue",
                            operation="operation",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            payload_field="payloadField",
                            range_key_field="rangeKeyField",
                            range_key_type="rangeKeyType",
                            range_key_value="rangeKeyValue",
                            table_name="tableName"
                        ),
                        dynamo_dBv2=iotevents_mixins.CfnDetectorModelPropsMixin.DynamoDBv2Property(
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            table_name="tableName"
                        ),
                        firehose=iotevents_mixins.CfnDetectorModelPropsMixin.FirehoseProperty(
                            delivery_stream_name="deliveryStreamName",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            separator="separator"
                        ),
                        iot_events=iotevents_mixins.CfnDetectorModelPropsMixin.IotEventsProperty(
                            input_name="inputName",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        iot_site_wise=iotevents_mixins.CfnDetectorModelPropsMixin.IotSiteWiseProperty(
                            asset_id="assetId",
                            entry_id="entryId",
                            property_alias="propertyAlias",
                            property_id="propertyId",
                            property_value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyValueProperty(
                                quality="quality",
                                timestamp=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty(
                                    offset_in_nanos="offsetInNanos",
                                    time_in_seconds="timeInSeconds"
                                ),
                                value=iotevents_mixins.CfnDetectorModelPropsMixin.AssetPropertyVariantProperty(
                                    boolean_value="booleanValue",
                                    double_value="doubleValue",
                                    integer_value="integerValue",
                                    string_value="stringValue"
                                )
                            )
                        ),
                        iot_topic_publish=iotevents_mixins.CfnDetectorModelPropsMixin.IotTopicPublishProperty(
                            mqtt_topic="mqttTopic",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        lambda_=iotevents_mixins.CfnDetectorModelPropsMixin.LambdaProperty(
                            function_arn="functionArn",
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            )
                        ),
                        reset_timer=iotevents_mixins.CfnDetectorModelPropsMixin.ResetTimerProperty(
                            timer_name="timerName"
                        ),
                        set_timer=iotevents_mixins.CfnDetectorModelPropsMixin.SetTimerProperty(
                            duration_expression="durationExpression",
                            seconds=123,
                            timer_name="timerName"
                        ),
                        set_variable=iotevents_mixins.CfnDetectorModelPropsMixin.SetVariableProperty(
                            value="value",
                            variable_name="variableName"
                        ),
                        sns=iotevents_mixins.CfnDetectorModelPropsMixin.SnsProperty(
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            target_arn="targetArn"
                        ),
                        sqs=iotevents_mixins.CfnDetectorModelPropsMixin.SqsProperty(
                            payload=iotevents_mixins.CfnDetectorModelPropsMixin.PayloadProperty(
                                content_expression="contentExpression",
                                type="type"
                            ),
                            queue_url="queueUrl",
                            use_base64=False
                        )
                    )],
                    condition="condition",
                    event_name="eventName",
                    next_state="nextState"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__938ba7d78cd53c68239279c89880bba418ec4fe544fae51eda18ffb14ef899dc)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
                check_type(argname="argument next_state", value=next_state, expected_type=type_hints["next_state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if condition is not None:
                self._values["condition"] = condition
            if event_name is not None:
                self._values["event_name"] = event_name
            if next_state is not None:
                self._values["next_state"] = next_state

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ActionProperty"]]]]:
            '''The actions to be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDetectorModelPropsMixin.ActionProperty"]]]], result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''Required.

            A Boolean expression that when TRUE causes the actions to be performed and the ``nextState`` to be entered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_name(self) -> typing.Optional[builtins.str]:
            '''The name of the transition event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-eventname
            '''
            result = self._values.get("event_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next_state(self) -> typing.Optional[builtins.str]:
            '''The next state to enter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-detectormodel-transitionevent.html#cfn-iotevents-detectormodel-transitionevent-nextstate
            '''
            result = self._values.get("next_state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransitionEventProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnInputMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "input_definition": "inputDefinition",
        "input_description": "inputDescription",
        "input_name": "inputName",
        "tags": "tags",
    },
)
class CfnInputMixinProps:
    def __init__(
        self,
        *,
        input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInputPropsMixin.InputDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        input_description: typing.Optional[builtins.str] = None,
        input_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInputPropsMixin.

        :param input_definition: The definition of the input.
        :param input_description: A brief description of the input.
        :param input_name: The name of the input.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
            
            cfn_input_mixin_props = iotevents_mixins.CfnInputMixinProps(
                input_definition=iotevents_mixins.CfnInputPropsMixin.InputDefinitionProperty(
                    attributes=[iotevents_mixins.CfnInputPropsMixin.AttributeProperty(
                        json_path="jsonPath"
                    )]
                ),
                input_description="inputDescription",
                input_name="inputName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44dea10d9f88d3c5812f03c02808065de975e6f484a28d57f32df664e98510b6)
            check_type(argname="argument input_definition", value=input_definition, expected_type=type_hints["input_definition"])
            check_type(argname="argument input_description", value=input_description, expected_type=type_hints["input_description"])
            check_type(argname="argument input_name", value=input_name, expected_type=type_hints["input_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_definition is not None:
            self._values["input_definition"] = input_definition
        if input_description is not None:
            self._values["input_description"] = input_description
        if input_name is not None:
            self._values["input_name"] = input_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def input_definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInputPropsMixin.InputDefinitionProperty"]]:
        '''The definition of the input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdefinition
        '''
        result = self._values.get("input_definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInputPropsMixin.InputDefinitionProperty"]], result)

    @builtins.property
    def input_description(self) -> typing.Optional[builtins.str]:
        '''A brief description of the input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputdescription
        '''
        result = self._values.get("input_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_name(self) -> typing.Optional[builtins.str]:
        '''The name of the input.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-inputname
        '''
        result = self._values.get("input_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html#cfn-iotevents-input-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInputMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInputPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnInputPropsMixin",
):
    '''The AWS::IoTEvents::Input resource creates an input.

    To monitor your devices and processes, they must have a way to get telemetry data into AWS IoT Events . This is done by sending messages as *inputs* to AWS IoT Events . For more information, see `How to Use AWS IoT Events <https://docs.aws.amazon.com/iotevents/latest/developerguide/how-to-use-iotevents.html>`_ in the *AWS IoT Events Developer Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotevents-input.html
    :cloudformationResource: AWS::IoTEvents::Input
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
        
        cfn_input_props_mixin = iotevents_mixins.CfnInputPropsMixin(iotevents_mixins.CfnInputMixinProps(
            input_definition=iotevents_mixins.CfnInputPropsMixin.InputDefinitionProperty(
                attributes=[iotevents_mixins.CfnInputPropsMixin.AttributeProperty(
                    json_path="jsonPath"
                )]
            ),
            input_description="inputDescription",
            input_name="inputName",
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
        props: typing.Union[CfnInputMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTEvents::Input``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83a7bbdcc9e232c223d592678daab20ff36066007617b169d6b776dff40d19e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22de6ff67020e158d8eb46c6def8b07b0cc48f83d45a3a57ad9ad63ccc1ec4cb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c48e266ae9e18381d9458ed19dea0f1e0283b2ddff0433a2032776b7043677a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInputMixinProps:
        return typing.cast(CfnInputMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnInputPropsMixin.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"json_path": "jsonPath"},
    )
    class AttributeProperty:
        def __init__(self, *, json_path: typing.Optional[builtins.str] = None) -> None:
            '''The attributes from the JSON payload that are made available by the input.

            Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload. Those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors.

            :param json_path: An expression that specifies an attribute-value pair in a JSON structure. Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events ( ``BatchPutMessage`` ). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the ``condition`` expressions used by detectors. Syntax: ``<field-name>.<field-name>...``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                attribute_property = iotevents_mixins.CfnInputPropsMixin.AttributeProperty(
                    json_path="jsonPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93f78ecf85d951271ce18d0fdd26c78e31df4460da8d1ea7122ebd55225730bd)
                check_type(argname="argument json_path", value=json_path, expected_type=type_hints["json_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if json_path is not None:
                self._values["json_path"] = json_path

        @builtins.property
        def json_path(self) -> typing.Optional[builtins.str]:
            '''An expression that specifies an attribute-value pair in a JSON structure.

            Use this to specify an attribute from the JSON payload that is made available by the input. Inputs are derived from messages sent to AWS IoT Events ( ``BatchPutMessage`` ). Each such message contains a JSON payload. The attribute (and its paired value) specified here are available for use in the ``condition`` expressions used by detectors.

            Syntax: ``<field-name>.<field-name>...``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-attribute.html#cfn-iotevents-input-attribute-jsonpath
            '''
            result = self._values.get("json_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotevents.mixins.CfnInputPropsMixin.InputDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes"},
    )
    class InputDefinitionProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInputPropsMixin.AttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The definition of the input.

            :param attributes: The attributes from the JSON payload that are made available by the input. Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload, and those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors that monitor this input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotevents import mixins as iotevents_mixins
                
                input_definition_property = iotevents_mixins.CfnInputPropsMixin.InputDefinitionProperty(
                    attributes=[iotevents_mixins.CfnInputPropsMixin.AttributeProperty(
                        json_path="jsonPath"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce88ed5f7176c6118e7c706accf9a2cca9f00d86db759597e57e6a97c1fbc092)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInputPropsMixin.AttributeProperty"]]]]:
            '''The attributes from the JSON payload that are made available by the input.

            Inputs are derived from messages sent to the AWS IoT Events system using ``BatchPutMessage`` . Each such message contains a JSON payload, and those attributes (and their paired values) specified here are available for use in the ``condition`` expressions used by detectors that monitor this input.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotevents-input-inputdefinition.html#cfn-iotevents-input-inputdefinition-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInputPropsMixin.AttributeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAlarmModelMixinProps",
    "CfnAlarmModelPropsMixin",
    "CfnDetectorModelMixinProps",
    "CfnDetectorModelPropsMixin",
    "CfnInputMixinProps",
    "CfnInputPropsMixin",
]

publication.publish()

def _typecheckingstub__855730260361424d37f6c3756ee8ec6a82b30ad8850dfbe28ff77ae55132c78e(
    *,
    alarm_capabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AlarmCapabilitiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alarm_event_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AlarmEventActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    alarm_model_description: typing.Optional[builtins.str] = None,
    alarm_model_name: typing.Optional[builtins.str] = None,
    alarm_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AlarmRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6188ec30d1473ec967d5fdafc22c90b5f76fd0cd297d3af5b71bd57a25dc5512(
    props: typing.Union[CfnAlarmModelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c6de4cbe0dd807800f373499231bc4a3d6cca65605b660c9acabe5632d2601c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca3d663363e6af35814a2a7940995e69fac7c1b2d5ca69a3c0e2bc2ee081ba0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd8997d2cfd50d606678ec2b395302c928862c06f06dcc5a280bd6f9158b429(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd0d4e69997a3df421ca4917a50f4d61b961bf11a7524ae5ba6be324f458565(
    *,
    dynamo_db: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.DynamoDBProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.DynamoDBv2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.FirehoseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.IotEventsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_site_wise: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.IotSiteWiseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.IotTopicPublishProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.LambdaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.SnsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.SqsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da6d85f7e7346795d838a56ba374fe625ffc92c9aa5d51afe005062cb623c55(
    *,
    acknowledge_flow: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AcknowledgeFlowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initialization_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.InitializationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787a85a50437ab0e519b1e6e049099a23a68964d4405adf1dac4f63b83a039e3(
    *,
    alarm_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AlarmActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f90c5fe0b8eb05e118fb1763b9b9c551ca8c58ad64f7606bafdc3c2e233ce5(
    *,
    simple_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.SimpleRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629b1196d5b7d0a8a2075adb40c66175e2a43c1fb17804325ea36d025850a4ca(
    *,
    offset_in_nanos: typing.Optional[builtins.str] = None,
    time_in_seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d83533a8facffc8851e795cf3a459c108416cba16d921d59a56d1921df74006(
    *,
    quality: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AssetPropertyTimestampProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AssetPropertyVariantProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c74301ebf81ed4f67dd308ba6ba2475dd336091d289a1b7d73993fec6a42a02(
    *,
    boolean_value: typing.Optional[builtins.str] = None,
    double_value: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de654499e95da7b5d7290b6006a0f42c63b3e09fa977d8b18588129ab4296ed(
    *,
    hash_key_field: typing.Optional[builtins.str] = None,
    hash_key_type: typing.Optional[builtins.str] = None,
    hash_key_value: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984c363aa8c2ea65257b1af55cc9da541517822a18f405fe7b27356c3a64409c(
    *,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03187648ebc1fe3403e835d2968260e293cecb65f2fdea9c0dc3498c81faa2d9(
    *,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0937ce94f5763c68b15b03ffd03307a6f79599353a69ba7c55d8e92fdb680f(
    *,
    disabled_on_initialization: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1b1ae8b0056c0bcb9ec59347e5d739deec20d878ebcfa530fc90933392229b(
    *,
    input_name: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b4a49b5172e76309519ada5cb34d77a2003350bfb3f9fa310cd0d1bfae508a(
    *,
    asset_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    property_alias: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
    property_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.AssetPropertyValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27eb6bb6fd0ba2b28981da9ca8bbd9547b62be114f4bcfd17a4242fae34b8cd4(
    *,
    mqtt_topic: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7382a5cbc523a5c6c8dc636406249f8985f3b956f215f1281309ff961ba1ffe(
    *,
    function_arn: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddd6fef3ca64ccdbb6a884e1886cc3607e58fb417087c79887db29d014da5c0(
    *,
    content_expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c5f4f33187a7d8774e1a4fa21067dcc750390df3ec269786a646a75af67f8e9(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    input_property: typing.Optional[builtins.str] = None,
    threshold: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f930f65f0c30d952a5df47e8562e2c5917c1a2956ccfae38ee67da30a569c0e0(
    *,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe96585898417569bb23acffdb80c9c6cf391820f8327896c83ae88fd6bf119(
    *,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAlarmModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    queue_url: typing.Optional[builtins.str] = None,
    use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dc29225a6f2766a41fa1f4f3b12b974fdbb5f7a13e25d0ec57228f87c100dfb(
    *,
    detector_model_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.DetectorModelDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    detector_model_description: typing.Optional[builtins.str] = None,
    detector_model_name: typing.Optional[builtins.str] = None,
    evaluation_method: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155b570ea75baab89f386d5ba02ff00287fda9ca4547ac62b562e86c7882ce76(
    props: typing.Union[CfnDetectorModelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a26c59f3f6d85581e38b932238456920099dce80480b697bfdea5785662a80b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f856275da4d53a5aea294d45a6ab52704620cbc683eca3447663f88700fd5b73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49eb462e6ae94250c442a25203366b7b1abba35dda9c575cccb528ebb21b6b4(
    *,
    clear_timer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.ClearTimerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_db: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.DynamoDBProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dynamo_d_bv2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.DynamoDBv2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    firehose: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.FirehoseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.IotEventsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_site_wise: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.IotSiteWiseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iot_topic_publish: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.IotTopicPublishProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.LambdaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    reset_timer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.ResetTimerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    set_timer: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.SetTimerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    set_variable: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.SetVariableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.SnsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.SqsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bb8b8d5d6292c976272f983bcc4e8473095abc2e3d8f5955bbc57244ce36b9(
    *,
    offset_in_nanos: typing.Optional[builtins.str] = None,
    time_in_seconds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3e3c7ce9dc7f70750e9c1c6df361e4e9231686910e7fd2935269c17d75c8995(
    *,
    quality: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.AssetPropertyTimestampProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.AssetPropertyVariantProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3913825f4d04dfdb1643d1aaa15bc86c3eafcc96b0778589e085f17a9dc63337(
    *,
    boolean_value: typing.Optional[builtins.str] = None,
    double_value: typing.Optional[builtins.str] = None,
    integer_value: typing.Optional[builtins.str] = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a93e4deb81fbac6127b1f2df0d8dc0ca21f5f141e03dfa69bff66a6fabc308(
    *,
    timer_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45663007aed6e9e50d4dcca6f5b921125cd55f13e3db3efeaf27061619c5b533(
    *,
    initial_state_name: typing.Optional[builtins.str] = None,
    states: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.StateProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6193985997a8c0a323039f634523782dfd61a9d952561c8dd875fa7de37d1b17(
    *,
    hash_key_field: typing.Optional[builtins.str] = None,
    hash_key_type: typing.Optional[builtins.str] = None,
    hash_key_value: typing.Optional[builtins.str] = None,
    operation: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    payload_field: typing.Optional[builtins.str] = None,
    range_key_field: typing.Optional[builtins.str] = None,
    range_key_type: typing.Optional[builtins.str] = None,
    range_key_value: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b310dd62c15cfd42a2877a032504a5235d69f371a2c2ab29c9db186796033bfd(
    *,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d374a401522bb63c5fd1e32dee5a321922c65ecdb22a1d519147410de635cd(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    condition: typing.Optional[builtins.str] = None,
    event_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b82cae05cd72d86df560734db81af243e70552af00b50a2ef0d9c9021f788c9(
    *,
    delivery_stream_name: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cad8c9e9a957eed118c1184875661ccafe7c69547cb8680a04d651f304fff9(
    *,
    input_name: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e220f619a8405516aa36eae4a541a1c3bbec460dd5948a8badfe0ef89c400043(
    *,
    asset_id: typing.Optional[builtins.str] = None,
    entry_id: typing.Optional[builtins.str] = None,
    property_alias: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
    property_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.AssetPropertyValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58c4454e5fb8082e61ac5a83ab2a4c1fb8b26fc54322eca521836398a95358f(
    *,
    mqtt_topic: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746b58641282fdfd9712ec99315a2874f22bbc0875e559ec00d4b6f8f677993c(
    *,
    function_arn: typing.Optional[builtins.str] = None,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08fd4f9afeac8a0364c5b07f308162c8d2a2ff86b5b6490c6fd73867b33f07ae(
    *,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.EventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9466f6299a646b523e58a201e1a96c70f34b44ad624a26dea66037d0825d96aa(
    *,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.EventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ab32c38665458e1e5e2bafa89e7da8c0b529a5143cc9a3af9d0924b186de43(
    *,
    events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.EventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    transition_events: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.TransitionEventProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7773e440c229a886826407d9e08429e2e046d8eaa7893b7eb6767e5b0bc56b4(
    *,
    content_expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__268ee25dc374e233f795e0cd3a18b7a3f2c481da5cebd9c5e5aa640448d5e0d9(
    *,
    timer_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f94a024fe9b3fb1f2b638764f97065e382f7c63b4534ddadf90e13e61d91853(
    *,
    duration_expression: typing.Optional[builtins.str] = None,
    seconds: typing.Optional[jsii.Number] = None,
    timer_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a0cc4912f2e62bc84708729538a6df0b54ce14c7c4b4893757a65fe9ee412fd(
    *,
    value: typing.Optional[builtins.str] = None,
    variable_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b751cfeef2f687796c048a67c4d1de397153c4a27db608541c4e5e43a259d3d5(
    *,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1563c421c9045ca94312646be10a90b6571890c47dc85b19331dff535f2f5195(
    *,
    payload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.PayloadProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    queue_url: typing.Optional[builtins.str] = None,
    use_base64: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__867f7b876edcaf29160843f5e49ed98686a5895356cff83fe1fe3f14a45e657b(
    *,
    on_enter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.OnEnterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_exit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.OnExitProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    on_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.OnInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    state_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938ba7d78cd53c68239279c89880bba418ec4fe544fae51eda18ffb14ef899dc(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDetectorModelPropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    condition: typing.Optional[builtins.str] = None,
    event_name: typing.Optional[builtins.str] = None,
    next_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44dea10d9f88d3c5812f03c02808065de975e6f484a28d57f32df664e98510b6(
    *,
    input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInputPropsMixin.InputDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_description: typing.Optional[builtins.str] = None,
    input_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83a7bbdcc9e232c223d592678daab20ff36066007617b169d6b776dff40d19e2(
    props: typing.Union[CfnInputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22de6ff67020e158d8eb46c6def8b07b0cc48f83d45a3a57ad9ad63ccc1ec4cb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c48e266ae9e18381d9458ed19dea0f1e0283b2ddff0433a2032776b7043677a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f78ecf85d951271ce18d0fdd26c78e31df4460da8d1ea7122ebd55225730bd(
    *,
    json_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce88ed5f7176c6118e7c706accf9a2cca9f00d86db759597e57e6a97c1fbc092(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInputPropsMixin.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
