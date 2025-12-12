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
    jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnScheduleGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnScheduleGroupMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnScheduleGroupPropsMixin.

        :param name: The name of the schedule group.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
            
            cfn_schedule_group_mixin_props = scheduler_mixins.CfnScheduleGroupMixinProps(
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f41809396e9b302399be27623d823e2043d84fc0fdf3e30103abe6c59fd61ad)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html#cfn-scheduler-schedulegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html#cfn-scheduler-schedulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduleGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnScheduleGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnScheduleGroupPropsMixin",
):
    '''A *schedule group* is an Amazon EventBridge Scheduler resource you use to organize your schedules.

    Your AWS account comes with a ``default`` scheduler group. You associate a new schedule with the ``default`` group or with schedule groups that you create and manage. You can create up to `500 schedule groups <https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html>`_ in your AWS account. With EventBridge Scheduler, you apply `tags <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ to schedule groups, not to individual schedules to organize your resources.

    For more information about managing schedule groups, see `Managing a schedule group <https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-group.html>`_ in the *EventBridge Scheduler User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedulegroup.html
    :cloudformationResource: AWS::Scheduler::ScheduleGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
        
        cfn_schedule_group_props_mixin = scheduler_mixins.CfnScheduleGroupPropsMixin(scheduler_mixins.CfnScheduleGroupMixinProps(
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
        props: typing.Union[CfnScheduleGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Scheduler::ScheduleGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fd3ce521c7e9aa444d8dda456e82be140727c4029eee2dda78f0fc89ee1d7e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d7cdb79dd32bc37fb9b13a16e6cd510e35875276e52455d0d32aaa9cab14401)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7a9f8db37bc7d09ac235111d6fbaf20dca16cf384b466aebbae6c3a0a73e3c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScheduleGroupMixinProps:
        return typing.cast(CfnScheduleGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnScheduleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "end_date": "endDate",
        "flexible_time_window": "flexibleTimeWindow",
        "group_name": "groupName",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "schedule_expression": "scheduleExpression",
        "schedule_expression_timezone": "scheduleExpressionTimezone",
        "start_date": "startDate",
        "state": "state",
        "target": "target",
    },
)
class CfnScheduleMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        end_date: typing.Optional[builtins.str] = None,
        flexible_time_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.FlexibleTimeWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        group_name: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schedule_expression: typing.Optional[builtins.str] = None,
        schedule_expression_timezone: typing.Optional[builtins.str] = None,
        start_date: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.TargetProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSchedulePropsMixin.

        :param description: The description you specify for the schedule.
        :param end_date: The date, in UTC, before which the schedule can invoke its target. Depending on the schedule's recurrence expression, invocations might stop on, or before, the ``EndDate`` you specify. EventBridge Scheduler ignores ``EndDate`` for one-time schedules.
        :param flexible_time_window: Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.
        :param group_name: The name of the schedule group associated with this schedule.
        :param kms_key_arn: The Amazon Resource Name (ARN) for the customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.
        :param name: The name of the schedule.
        :param schedule_expression: The expression that defines when the schedule runs. The following formats are supported. - ``at`` expression - ``at(yyyy-mm-ddThh:mm:ss)`` - ``rate`` expression - ``rate(value unit)`` - ``cron`` expression - ``cron(fields)`` You can use ``at`` expressions to create one-time schedules that invoke a target once, at the time and in the time zone, that you specify. You can use ``rate`` and ``cron`` expressions to create recurring schedules. Rate-based schedules are useful when you want to invoke a target at regular intervals, such as every 15 minutes or every five days. Cron-based schedules are useful when you want to invoke a target periodically at a specific time, such as at 8:00 am (UTC+0) every 1st day of the month. A ``cron`` expression consists of six fields separated by white spaces: ``(minutes hours day_of_month month day_of_week year)`` . A ``rate`` expression consists of a *value* as a positive integer, and a *unit* with the following options: ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days`` For more information and examples, see `Schedule types on EventBridge Scheduler <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .
        :param schedule_expression_timezone: The timezone in which the scheduling expression is evaluated.
        :param start_date: The date, in UTC, after which the schedule can begin invoking its target. Depending on the schedule's recurrence expression, invocations might occur on, or after, the ``StartDate`` you specify. EventBridge Scheduler ignores ``StartDate`` for one-time schedules.
        :param state: Specifies whether the schedule is enabled or disabled. *Allowed Values* : ``ENABLED`` | ``DISABLED``
        :param target: The schedule's target details.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
            
            # tags: Any
            
            cfn_schedule_mixin_props = scheduler_mixins.CfnScheduleMixinProps(
                description="description",
                end_date="endDate",
                flexible_time_window=scheduler_mixins.CfnSchedulePropsMixin.FlexibleTimeWindowProperty(
                    maximum_window_in_minutes=123,
                    mode="mode"
                ),
                group_name="groupName",
                kms_key_arn="kmsKeyArn",
                name="name",
                schedule_expression="scheduleExpression",
                schedule_expression_timezone="scheduleExpressionTimezone",
                start_date="startDate",
                state="state",
                target=scheduler_mixins.CfnSchedulePropsMixin.TargetProperty(
                    arn="arn",
                    dead_letter_config=scheduler_mixins.CfnSchedulePropsMixin.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    ecs_parameters=scheduler_mixins.CfnSchedulePropsMixin.EcsParametersProperty(
                        capacity_provider_strategy=[scheduler_mixins.CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty(
                            base=123,
                            capacity_provider="capacityProvider",
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=scheduler_mixins.CfnSchedulePropsMixin.NetworkConfigurationProperty(
                            awsvpc_configuration=scheduler_mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty(
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"],
                                subnets=["subnets"]
                            )
                        ),
                        placement_constraints=[scheduler_mixins.CfnSchedulePropsMixin.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategy=[scheduler_mixins.CfnSchedulePropsMixin.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tags=tags,
                        task_count=123,
                        task_definition_arn="taskDefinitionArn"
                    ),
                    event_bridge_parameters=scheduler_mixins.CfnSchedulePropsMixin.EventBridgeParametersProperty(
                        detail_type="detailType",
                        source="source"
                    ),
                    input="input",
                    kinesis_parameters=scheduler_mixins.CfnSchedulePropsMixin.KinesisParametersProperty(
                        partition_key="partitionKey"
                    ),
                    retry_policy=scheduler_mixins.CfnSchedulePropsMixin.RetryPolicyProperty(
                        maximum_event_age_in_seconds=123,
                        maximum_retry_attempts=123
                    ),
                    role_arn="roleArn",
                    sage_maker_pipeline_parameters=scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_parameters=scheduler_mixins.CfnSchedulePropsMixin.SqsParametersProperty(
                        message_group_id="messageGroupId"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55849960d7d353d3d9c111ad7d4e58768dff095382ce7edf336f0347a8c93877)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
            check_type(argname="argument flexible_time_window", value=flexible_time_window, expected_type=type_hints["flexible_time_window"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule_expression", value=schedule_expression, expected_type=type_hints["schedule_expression"])
            check_type(argname="argument schedule_expression_timezone", value=schedule_expression_timezone, expected_type=type_hints["schedule_expression_timezone"])
            check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if end_date is not None:
            self._values["end_date"] = end_date
        if flexible_time_window is not None:
            self._values["flexible_time_window"] = flexible_time_window
        if group_name is not None:
            self._values["group_name"] = group_name
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if schedule_expression is not None:
            self._values["schedule_expression"] = schedule_expression
        if schedule_expression_timezone is not None:
            self._values["schedule_expression_timezone"] = schedule_expression_timezone
        if start_date is not None:
            self._values["start_date"] = start_date
        if state is not None:
            self._values["state"] = state
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description you specify for the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_date(self) -> typing.Optional[builtins.str]:
        '''The date, in UTC, before which the schedule can invoke its target.

        Depending on the schedule's recurrence expression, invocations might stop on, or before, the ``EndDate`` you specify.
        EventBridge Scheduler ignores ``EndDate`` for one-time schedules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-enddate
        '''
        result = self._values.get("end_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flexible_time_window(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.FlexibleTimeWindowProperty"]]:
        '''Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-flexibletimewindow
        '''
        result = self._values.get("flexible_time_window")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.FlexibleTimeWindowProperty"]], result)

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule group associated with this schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression(self) -> typing.Optional[builtins.str]:
        '''The expression that defines when the schedule runs. The following formats are supported.

        - ``at`` expression - ``at(yyyy-mm-ddThh:mm:ss)``
        - ``rate`` expression - ``rate(value unit)``
        - ``cron`` expression - ``cron(fields)``

        You can use ``at`` expressions to create one-time schedules that invoke a target once, at the time and in the time zone, that you specify. You can use ``rate`` and ``cron`` expressions to create recurring schedules. Rate-based schedules are useful when you want to invoke a target at regular intervals, such as every 15 minutes or every five days. Cron-based schedules are useful when you want to invoke a target periodically at a specific time, such as at 8:00 am (UTC+0) every 1st day of the month.

        A ``cron`` expression consists of six fields separated by white spaces: ``(minutes hours day_of_month month day_of_week year)`` .

        A ``rate`` expression consists of a *value* as a positive integer, and a *unit* with the following options: ``minute`` | ``minutes`` | ``hour`` | ``hours`` | ``day`` | ``days``

        For more information and examples, see `Schedule types on EventBridge Scheduler <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-scheduleexpression
        '''
        result = self._values.get("schedule_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule_expression_timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone in which the scheduling expression is evaluated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-scheduleexpressiontimezone
        '''
        result = self._values.get("schedule_expression_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_date(self) -> typing.Optional[builtins.str]:
        '''The date, in UTC, after which the schedule can begin invoking its target.

        Depending on the schedule's recurrence expression, invocations might occur on, or after, the ``StartDate`` you specify.
        EventBridge Scheduler ignores ``StartDate`` for one-time schedules.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-startdate
        '''
        result = self._values.get("start_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the schedule is enabled or disabled.

        *Allowed Values* : ``ENABLED`` | ``DISABLED``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.TargetProperty"]]:
        '''The schedule's target details.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html#cfn-scheduler-schedule-target
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.TargetProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchedulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin",
):
    '''A *schedule* is the main resource you create, configure, and manage using Amazon EventBridge Scheduler.

    Every schedule has a *schedule expression* that determines when, and with what frequency, the schedule runs. EventBridge Scheduler supports three types of schedules: rate, cron, and one-time schedules. For more information about different schedule types, see `Schedule types <https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html>`_ in the *EventBridge Scheduler User Guide* .

    When you create a schedule, you configure a target for the schedule to invoke. A target is an API operation that EventBridge Scheduler calls on your behalf every time your schedule runs. EventBridge Scheduler supports two types of targets: *templated* targets invoke common API operations across a core groups of services, and customizeable *universal* targets that you can use to call more than 6,000 operations across over 270 services. For more information about configuring targets, see `Managing targets <https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets.html>`_ in the *EventBridge Scheduler User Guide* .

    For more information about managing schedules, changing the schedule state, setting up flexible time windows, and configuring a dead-letter queue for a schedule, see `Managing a schedule <https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule.html>`_ in the *EventBridge Scheduler User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-scheduler-schedule.html
    :cloudformationResource: AWS::Scheduler::Schedule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
        
        # tags: Any
        
        cfn_schedule_props_mixin = scheduler_mixins.CfnSchedulePropsMixin(scheduler_mixins.CfnScheduleMixinProps(
            description="description",
            end_date="endDate",
            flexible_time_window=scheduler_mixins.CfnSchedulePropsMixin.FlexibleTimeWindowProperty(
                maximum_window_in_minutes=123,
                mode="mode"
            ),
            group_name="groupName",
            kms_key_arn="kmsKeyArn",
            name="name",
            schedule_expression="scheduleExpression",
            schedule_expression_timezone="scheduleExpressionTimezone",
            start_date="startDate",
            state="state",
            target=scheduler_mixins.CfnSchedulePropsMixin.TargetProperty(
                arn="arn",
                dead_letter_config=scheduler_mixins.CfnSchedulePropsMixin.DeadLetterConfigProperty(
                    arn="arn"
                ),
                ecs_parameters=scheduler_mixins.CfnSchedulePropsMixin.EcsParametersProperty(
                    capacity_provider_strategy=[scheduler_mixins.CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty(
                        base=123,
                        capacity_provider="capacityProvider",
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=scheduler_mixins.CfnSchedulePropsMixin.NetworkConfigurationProperty(
                        awsvpc_configuration=scheduler_mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty(
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    ),
                    placement_constraints=[scheduler_mixins.CfnSchedulePropsMixin.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[scheduler_mixins.CfnSchedulePropsMixin.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=tags,
                    task_count=123,
                    task_definition_arn="taskDefinitionArn"
                ),
                event_bridge_parameters=scheduler_mixins.CfnSchedulePropsMixin.EventBridgeParametersProperty(
                    detail_type="detailType",
                    source="source"
                ),
                input="input",
                kinesis_parameters=scheduler_mixins.CfnSchedulePropsMixin.KinesisParametersProperty(
                    partition_key="partitionKey"
                ),
                retry_policy=scheduler_mixins.CfnSchedulePropsMixin.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                role_arn="roleArn",
                sage_maker_pipeline_parameters=scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                ),
                sqs_parameters=scheduler_mixins.CfnSchedulePropsMixin.SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnScheduleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Scheduler::Schedule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf2f4be196d1628cff3054470314cde2a5cfeec951349e9701246d5c70681f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31fc9ed95540311843fcfdc4db20e4e53e9ab3dacd2120c564000fc2dc4b819f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602251a262dba757f6a312b0a293fa755a33e531bb4d904bb33af1b206b83cae)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScheduleMixinProps:
        return typing.cast(CfnScheduleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assign_public_ip": "assignPublicIp",
            "security_groups": "securityGroups",
            "subnets": "subnets",
        },
    )
    class AwsVpcConfigurationProperty:
        def __init__(
            self,
            *,
            assign_public_ip: typing.Optional[builtins.str] = None,
            security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''This structure specifies the VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the awsvpc network mode.

            :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .
            :param security_groups: Specifies the security groups associated with the task. These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.
            :param subnets: Specifies the subnets associated with the task. These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                aws_vpc_configuration_property = scheduler_mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty(
                    assign_public_ip="assignPublicIp",
                    security_groups=["securityGroups"],
                    subnets=["subnets"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19d251444898c805ce9fb72ce04c05900ccf0aa8595d7c618d104dd00def4b1b)
                check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
                check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip
            if security_groups is not None:
                self._values["security_groups"] = security_groups
            if subnets is not None:
                self._values["subnets"] = subnets

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the task's elastic network interface receives a public IP address.

            You can specify ``ENABLED`` only when ``LaunchType`` in ``EcsParameters`` is set to ``FARGATE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html#cfn-scheduler-schedule-awsvpcconfiguration-assignpublicip
            '''
            result = self._values.get("assign_public_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the security groups associated with the task.

            These security groups must all be in the same VPC. You can specify as many as five security groups. If you do not specify a security group, the default security group for the VPC is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html#cfn-scheduler-schedule-awsvpcconfiguration-securitygroups
            '''
            result = self._values.get("security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the subnets associated with the task.

            These subnets must all be in the same VPC. You can specify as many as 16 subnets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-awsvpcconfiguration.html#cfn-scheduler-schedule-awsvpcconfiguration-subnets
            '''
            result = self._values.get("subnets")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base": "base",
            "capacity_provider": "capacityProvider",
            "weight": "weight",
        },
    )
    class CapacityProviderStrategyItemProperty:
        def __init__(
            self,
            *,
            base: typing.Optional[jsii.Number] = None,
            capacity_provider: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The details of a capacity provider strategy.

            :param base: The base value designates how many tasks, at a minimum, to run on the specified capacity provider. Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of ``0`` is used. Default: - 0
            :param capacity_provider: The short name of the capacity provider.
            :param weight: The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider. The weight value is taken into consideration after the base value, if defined, is satisfied. Default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                capacity_provider_strategy_item_property = scheduler_mixins.CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty(
                    base=123,
                    capacity_provider="capacityProvider",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b897a72d404a46fd766b8dadccf3d141c747f5cce0deb90847febc98b8605d1f)
                check_type(argname="argument base", value=base, expected_type=type_hints["base"])
                check_type(argname="argument capacity_provider", value=capacity_provider, expected_type=type_hints["capacity_provider"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if base is not None:
                self._values["base"] = base
            if capacity_provider is not None:
                self._values["capacity_provider"] = capacity_provider
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def base(self) -> typing.Optional[jsii.Number]:
            '''The base value designates how many tasks, at a minimum, to run on the specified capacity provider.

            Only one capacity provider in a capacity provider strategy can have a base defined. If no value is specified, the default value of ``0`` is used.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html#cfn-scheduler-schedule-capacityproviderstrategyitem-base
            '''
            result = self._values.get("base")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def capacity_provider(self) -> typing.Optional[builtins.str]:
            '''The short name of the capacity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html#cfn-scheduler-schedule-capacityproviderstrategyitem-capacityprovider
            '''
            result = self._values.get("capacity_provider")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The weight value designates the relative percentage of the total number of tasks launched that should use the specified capacity provider.

            The weight value is taken into consideration after the base value, if defined, is satisfied.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-capacityproviderstrategyitem.html#cfn-scheduler-schedule-capacityproviderstrategyitem-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapacityProviderStrategyItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.DeadLetterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class DeadLetterConfigProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule.

            If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.

            :param arn: The Amazon Resource Name (ARN) of the SQS queue specified as the destination for the dead-letter queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-deadletterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                dead_letter_config_property = scheduler_mixins.CfnSchedulePropsMixin.DeadLetterConfigProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac94e8785420a40545598d257ae0cfd23047536aa7f252c45316f2aebceb1e80)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the SQS queue specified as the destination for the dead-letter queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-deadletterconfig.html#cfn-scheduler-schedule-deadletterconfig-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeadLetterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.EcsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity_provider_strategy": "capacityProviderStrategy",
            "enable_ecs_managed_tags": "enableEcsManagedTags",
            "enable_execute_command": "enableExecuteCommand",
            "group": "group",
            "launch_type": "launchType",
            "network_configuration": "networkConfiguration",
            "placement_constraints": "placementConstraints",
            "placement_strategy": "placementStrategy",
            "platform_version": "platformVersion",
            "propagate_tags": "propagateTags",
            "reference_id": "referenceId",
            "tags": "tags",
            "task_count": "taskCount",
            "task_definition_arn": "taskDefinitionArn",
        },
    )
    class EcsParametersProperty:
        def __init__(
            self,
            *,
            capacity_provider_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            group: typing.Optional[builtins.str] = None,
            launch_type: typing.Optional[builtins.str] = None,
            network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            placement_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.PlacementConstraintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            placement_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.PlacementStrategyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            platform_version: typing.Optional[builtins.str] = None,
            propagate_tags: typing.Optional[builtins.str] = None,
            reference_id: typing.Optional[builtins.str] = None,
            tags: typing.Any = None,
            task_count: typing.Optional[jsii.Number] = None,
            task_definition_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The templated target type for the Amazon ECS ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API operation.

            :param capacity_provider_strategy: The capacity provider strategy to use for the task.
            :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the task. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the *Amazon ECS Developer Guide* .
            :param enable_execute_command: Whether or not to enable the execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task.
            :param group: Specifies an Amazon ECS task group for the task. The maximum length is 255 characters.
            :param launch_type: Specifies the launch type on which your task is running. The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html>`_ in the *Amazon ECS Developer Guide* .
            :param network_configuration: This structure specifies the network configuration for an ECS task.
            :param placement_constraints: An array of placement constraint objects to use for the task. You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).
            :param placement_strategy: The task placement strategy for a task or service.
            :param platform_version: Specifies the platform version for the task. Specify only the numeric portion of the platform version, such as ``1.1.0`` .
            :param propagate_tags: Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use the Amazon ECS ```TagResource`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_TagResource.html>`_ API action.
            :param reference_id: The reference ID to use for the task.
            :param tags: The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. For more information, see ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ in the *Amazon ECS API Reference* .
            :param task_count: The number of tasks to create based on ``TaskDefinition`` . The default is ``1`` .
            :param task_definition_arn: The Amazon Resource Name (ARN) of the task definition to use if the event target is an Amazon ECS task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                # tags: Any
                
                ecs_parameters_property = scheduler_mixins.CfnSchedulePropsMixin.EcsParametersProperty(
                    capacity_provider_strategy=[scheduler_mixins.CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty(
                        base=123,
                        capacity_provider="capacityProvider",
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=scheduler_mixins.CfnSchedulePropsMixin.NetworkConfigurationProperty(
                        awsvpc_configuration=scheduler_mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty(
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"],
                            subnets=["subnets"]
                        )
                    ),
                    placement_constraints=[scheduler_mixins.CfnSchedulePropsMixin.PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[scheduler_mixins.CfnSchedulePropsMixin.PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=tags,
                    task_count=123,
                    task_definition_arn="taskDefinitionArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d64b5fe6f0a4048453831eabd757993b75f1007690f93d655a6b31617ae613ba)
                check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
                check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
                check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
                check_type(argname="argument group", value=group, expected_type=type_hints["group"])
                check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
                check_type(argname="argument placement_strategy", value=placement_strategy, expected_type=type_hints["placement_strategy"])
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
                check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
                check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
                check_type(argname="argument task_definition_arn", value=task_definition_arn, expected_type=type_hints["task_definition_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity_provider_strategy is not None:
                self._values["capacity_provider_strategy"] = capacity_provider_strategy
            if enable_ecs_managed_tags is not None:
                self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
            if enable_execute_command is not None:
                self._values["enable_execute_command"] = enable_execute_command
            if group is not None:
                self._values["group"] = group
            if launch_type is not None:
                self._values["launch_type"] = launch_type
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if placement_constraints is not None:
                self._values["placement_constraints"] = placement_constraints
            if placement_strategy is not None:
                self._values["placement_strategy"] = placement_strategy
            if platform_version is not None:
                self._values["platform_version"] = platform_version
            if propagate_tags is not None:
                self._values["propagate_tags"] = propagate_tags
            if reference_id is not None:
                self._values["reference_id"] = reference_id
            if tags is not None:
                self._values["tags"] = tags
            if task_count is not None:
                self._values["task_count"] = task_count
            if task_definition_arn is not None:
                self._values["task_definition_arn"] = task_definition_arn

        @builtins.property
        def capacity_provider_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty"]]]]:
            '''The capacity provider strategy to use for the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-capacityproviderstrategy
            '''
            result = self._values.get("capacity_provider_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty"]]]], result)

        @builtins.property
        def enable_ecs_managed_tags(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to enable Amazon ECS managed tags for the task.

            For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ in the *Amazon ECS Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-enableecsmanagedtags
            '''
            result = self._values.get("enable_ecs_managed_tags")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_execute_command(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not to enable the execute command functionality for the containers in this task.

            If true, this enables execute command functionality on all containers in the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-enableexecutecommand
            '''
            result = self._values.get("enable_execute_command")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def group(self) -> typing.Optional[builtins.str]:
            '''Specifies an Amazon ECS task group for the task.

            The maximum length is 255 characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-group
            '''
            result = self._values.get("group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the launch type on which your task is running.

            The launch type that you specify here must match one of the launch type (compatibilities) of the target task. The ``FARGATE`` value is supported only in the Regions where Fargate with Amazon ECS is supported. For more information, see `AWS Fargate on Amazon ECS <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html>`_ in the *Amazon ECS Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-launchtype
            '''
            result = self._values.get("launch_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.NetworkConfigurationProperty"]]:
            '''This structure specifies the network configuration for an ECS task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.NetworkConfigurationProperty"]], result)

        @builtins.property
        def placement_constraints(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.PlacementConstraintProperty"]]]]:
            '''An array of placement constraint objects to use for the task.

            You can specify up to 10 constraints per task (including constraints in the task definition and those specified at runtime).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-placementconstraints
            '''
            result = self._values.get("placement_constraints")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.PlacementConstraintProperty"]]]], result)

        @builtins.property
        def placement_strategy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.PlacementStrategyProperty"]]]]:
            '''The task placement strategy for a task or service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-placementstrategy
            '''
            result = self._values.get("placement_strategy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.PlacementStrategyProperty"]]]], result)

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''Specifies the platform version for the task.

            Specify only the numeric portion of the platform version, such as ``1.1.0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def propagate_tags(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to propagate the tags from the task definition to the task.

            If no value is specified, the tags are not propagated. Tags can only be propagated to the task during task creation. To add tags to a task after task creation, use the Amazon ECS ```TagResource`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_TagResource.html>`_ API action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-propagatetags
            '''
            result = self._values.get("propagate_tags")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reference_id(self) -> typing.Optional[builtins.str]:
            '''The reference ID to use for the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-referenceid
            '''
            result = self._values.get("reference_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Any:
            '''The metadata that you apply to the task to help you categorize and organize them.

            Each tag consists of a key and an optional value, both of which you define. For more information, see ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ in the *Amazon ECS API Reference* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Any, result)

        @builtins.property
        def task_count(self) -> typing.Optional[jsii.Number]:
            '''The number of tasks to create based on ``TaskDefinition`` .

            The default is ``1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-taskcount
            '''
            result = self._values.get("task_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def task_definition_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the task definition to use if the event target is an Amazon ECS task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-ecsparameters.html#cfn-scheduler-schedule-ecsparameters-taskdefinitionarn
            '''
            result = self._values.get("task_definition_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EcsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.EventBridgeParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"detail_type": "detailType", "source": "source"},
    )
    class EventBridgeParametersProperty:
        def __init__(
            self,
            *,
            detail_type: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The templated target type for the EventBridge ```PutEvents`` <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ API operation.

            :param detail_type: A free-form string, with a maximum of 128 characters, used to decide what fields to expect in the event detail.
            :param source: The source of the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-eventbridgeparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                event_bridge_parameters_property = scheduler_mixins.CfnSchedulePropsMixin.EventBridgeParametersProperty(
                    detail_type="detailType",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95ebf16c8c12343fb0429de2af7c93fb76341078187081707ef40c29715639ae)
                check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if detail_type is not None:
                self._values["detail_type"] = detail_type
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def detail_type(self) -> typing.Optional[builtins.str]:
            '''A free-form string, with a maximum of 128 characters, used to decide what fields to expect in the event detail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-eventbridgeparameters.html#cfn-scheduler-schedule-eventbridgeparameters-detailtype
            '''
            result = self._values.get("detail_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The source of the event.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-eventbridgeparameters.html#cfn-scheduler-schedule-eventbridgeparameters-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.FlexibleTimeWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_window_in_minutes": "maximumWindowInMinutes",
            "mode": "mode",
        },
    )
    class FlexibleTimeWindowProperty:
        def __init__(
            self,
            *,
            maximum_window_in_minutes: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Allows you to configure a time window during which EventBridge Scheduler invokes the schedule.

            :param maximum_window_in_minutes: The maximum time window during which a schedule can be invoked. *Minimum* : ``1`` *Maximum* : ``1440``
            :param mode: Determines whether the schedule is invoked within a flexible time window. You must use quotation marks when you specify this value in your JSON or YAML template. *Allowed Values* : ``"OFF"`` | ``"FLEXIBLE"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-flexibletimewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                flexible_time_window_property = scheduler_mixins.CfnSchedulePropsMixin.FlexibleTimeWindowProperty(
                    maximum_window_in_minutes=123,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__39639eaeed8ea5405219574a6d8a9d8129c9341cfd2818d579344f8c0157b554)
                check_type(argname="argument maximum_window_in_minutes", value=maximum_window_in_minutes, expected_type=type_hints["maximum_window_in_minutes"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_window_in_minutes is not None:
                self._values["maximum_window_in_minutes"] = maximum_window_in_minutes
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def maximum_window_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The maximum time window during which a schedule can be invoked.

            *Minimum* : ``1``

            *Maximum* : ``1440``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-flexibletimewindow.html#cfn-scheduler-schedule-flexibletimewindow-maximumwindowinminutes
            '''
            result = self._values.get("maximum_window_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Determines whether the schedule is invoked within a flexible time window.

            You must use quotation marks when you specify this value in your JSON or YAML template.

            *Allowed Values* : ``"OFF"`` | ``"FLEXIBLE"``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-flexibletimewindow.html#cfn-scheduler-schedule-flexibletimewindow-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FlexibleTimeWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.KinesisParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"partition_key": "partitionKey"},
    )
    class KinesisParametersProperty:
        def __init__(
            self,
            *,
            partition_key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The templated target type for the Amazon Kinesis ```PutRecord`` <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html>`_ API operation.

            :param partition_key: Specifies the shard to which EventBridge Scheduler sends the event. For more information, see `Amazon Kinesis Data Streams terminology and concepts <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html>`_ in the *Amazon Kinesis Streams Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-kinesisparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                kinesis_parameters_property = scheduler_mixins.CfnSchedulePropsMixin.KinesisParametersProperty(
                    partition_key="partitionKey"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5712ea2f00e8f557c4ecb16a5e437bf4b1dbcac7f961cae2c6d73a709d5cf60)
                check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if partition_key is not None:
                self._values["partition_key"] = partition_key

        @builtins.property
        def partition_key(self) -> typing.Optional[builtins.str]:
            '''Specifies the shard to which EventBridge Scheduler sends the event.

            For more information, see `Amazon Kinesis Data Streams terminology and concepts <https://docs.aws.amazon.com/streams/latest/dev/key-concepts.html>`_ in the *Amazon Kinesis Streams Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-kinesisparameters.html#cfn-scheduler-schedule-kinesisparameters-partitionkey
            '''
            result = self._values.get("partition_key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"awsvpc_configuration": "awsvpcConfiguration"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            awsvpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.AwsVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the network configuration for an ECS task.

            :param awsvpc_configuration: Specifies the Amazon VPC subnets and security groups for the task, and whether a public IP address is to be used. This structure is relevant only for ECS tasks that use the awsvpc network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                network_configuration_property = scheduler_mixins.CfnSchedulePropsMixin.NetworkConfigurationProperty(
                    awsvpc_configuration=scheduler_mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty(
                        assign_public_ip="assignPublicIp",
                        security_groups=["securityGroups"],
                        subnets=["subnets"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b098d09a7cd07f214a4ee9fa81cf72c9bcf24c5c3de1684c9a62f07467c39e8)
                check_type(argname="argument awsvpc_configuration", value=awsvpc_configuration, expected_type=type_hints["awsvpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if awsvpc_configuration is not None:
                self._values["awsvpc_configuration"] = awsvpc_configuration

        @builtins.property
        def awsvpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.AwsVpcConfigurationProperty"]]:
            '''Specifies the Amazon VPC subnets and security groups for the task, and whether a public IP address is to be used.

            This structure is relevant only for ECS tasks that use the awsvpc network mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-networkconfiguration.html#cfn-scheduler-schedule-networkconfiguration-awsvpcconfiguration
            '''
            result = self._values.get("awsvpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.AwsVpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.PlacementConstraintProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "type": "type"},
    )
    class PlacementConstraintProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a constraint on task placement.

            :param expression: A cluster query language expression to apply to the constraint. You cannot specify an expression if the constraint type is ``distinctInstance`` . For more information, see `Cluster query language <https://docs.aws.amazon.com/latest/developerguide/cluster-query-language.html>`_ in the *Amazon ECS Developer Guide* .
            :param type: The type of constraint. Use ``distinctInstance`` to ensure that each task in a particular group is running on a different container instance. Use ``memberOf`` to restrict the selection to a group of valid candidates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementconstraint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                placement_constraint_property = scheduler_mixins.CfnSchedulePropsMixin.PlacementConstraintProperty(
                    expression="expression",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a0895c82ff773ca7f5928c634a5b1f89c4a2ea44fae7d32f2fda7e02fd86e56)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''A cluster query language expression to apply to the constraint.

            You cannot specify an expression if the constraint type is ``distinctInstance`` . For more information, see `Cluster query language <https://docs.aws.amazon.com/latest/developerguide/cluster-query-language.html>`_ in the *Amazon ECS Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementconstraint.html#cfn-scheduler-schedule-placementconstraint-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of constraint.

            Use ``distinctInstance`` to ensure that each task in a particular group is running on a different container instance. Use ``memberOf`` to restrict the selection to a group of valid candidates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementconstraint.html#cfn-scheduler-schedule-placementconstraint-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementConstraintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.PlacementStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"field": "field", "type": "type"},
    )
    class PlacementStrategyProperty:
        def __init__(
            self,
            *,
            field: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The task placement strategy for a task or service.

            :param field: The field to apply the placement strategy against. For the spread placement strategy, valid values are ``instanceId`` (or ``instanceId`` , which has the same effect), or any platform or custom attribute that is applied to a container instance, such as ``attribute:ecs.availability-zone`` . For the binpack placement strategy, valid values are ``cpu`` and ``memory`` . For the random placement strategy, this field is not used.
            :param type: The type of placement strategy. The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                placement_strategy_property = scheduler_mixins.CfnSchedulePropsMixin.PlacementStrategyProperty(
                    field="field",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e49f8ee660efd8573a9d7640f2ff297bbc431d09343398d92a2d5bbae814da48)
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field is not None:
                self._values["field"] = field
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''The field to apply the placement strategy against.

            For the spread placement strategy, valid values are ``instanceId`` (or ``instanceId`` , which has the same effect), or any platform or custom attribute that is applied to a container instance, such as ``attribute:ecs.availability-zone`` . For the binpack placement strategy, valid values are ``cpu`` and ``memory`` . For the random placement strategy, this field is not used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementstrategy.html#cfn-scheduler-schedule-placementstrategy-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of placement strategy.

            The random placement strategy randomly places tasks on available candidates. The spread placement strategy spreads placement across available candidates evenly based on the field parameter. The binpack strategy places tasks on available candidates that have the least available amount of the resource that is specified with the field parameter. For example, if you binpack on memory, a task is placed on the instance with the least amount of remaining memory (but still enough to run the task).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-placementstrategy.html#cfn-scheduler-schedule-placementstrategy-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PlacementStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.RetryPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maximum_event_age_in_seconds": "maximumEventAgeInSeconds",
            "maximum_retry_attempts": "maximumRetryAttempts",
        },
    )
    class RetryPolicyProperty:
        def __init__(
            self,
            *,
            maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
            maximum_retry_attempts: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.

            :param maximum_event_age_in_seconds: The maximum amount of time, in seconds, to continue to make retry attempts.
            :param maximum_retry_attempts: The maximum number of retry attempts to make before the request fails. Retry attempts with exponential backoff continue until either the maximum number of attempts is made or until the duration of the ``MaximumEventAgeInSeconds`` is reached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-retrypolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                retry_policy_property = scheduler_mixins.CfnSchedulePropsMixin.RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1172557826ff08bc8699e23336dbec517df8b28c0b1af69fed2fa0e062e6675f)
                check_type(argname="argument maximum_event_age_in_seconds", value=maximum_event_age_in_seconds, expected_type=type_hints["maximum_event_age_in_seconds"])
                check_type(argname="argument maximum_retry_attempts", value=maximum_retry_attempts, expected_type=type_hints["maximum_retry_attempts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if maximum_event_age_in_seconds is not None:
                self._values["maximum_event_age_in_seconds"] = maximum_event_age_in_seconds
            if maximum_retry_attempts is not None:
                self._values["maximum_retry_attempts"] = maximum_retry_attempts

        @builtins.property
        def maximum_event_age_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time, in seconds, to continue to make retry attempts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-retrypolicy.html#cfn-scheduler-schedule-retrypolicy-maximumeventageinseconds
            '''
            result = self._values.get("maximum_event_age_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum_retry_attempts(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of retry attempts to make before the request fails.

            Retry attempts with exponential backoff continue until either the maximum number of attempts is made or until the duration of the ``MaximumEventAgeInSeconds`` is reached.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-retrypolicy.html#cfn-scheduler-schedule-retrypolicy-maximumretryattempts
            '''
            result = self._values.get("maximum_retry_attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.SageMakerPipelineParameterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class SageMakerPipelineParameterProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name and value pair of a parameter to use to start execution of a SageMaker Model Building Pipeline.

            :param name: Name of parameter to start execution of a SageMaker Model Building Pipeline.
            :param value: Value of parameter to start execution of a SageMaker Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                sage_maker_pipeline_parameter_property = scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParameterProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0f9c524470b329d824328500e5ae1d5eac09f30289ddda0d28ab98a9698a85f)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of parameter to start execution of a SageMaker Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameter.html#cfn-scheduler-schedule-sagemakerpipelineparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Value of parameter to start execution of a SageMaker Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameter.html#cfn-scheduler-schedule-sagemakerpipelineparameter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.SageMakerPipelineParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"pipeline_parameter_list": "pipelineParameterList"},
    )
    class SageMakerPipelineParametersProperty:
        def __init__(
            self,
            *,
            pipeline_parameter_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.SageMakerPipelineParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The templated target type for the Amazon SageMaker ```StartPipelineExecution`` <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_StartPipelineExecution.html>`_ API operation.

            :param pipeline_parameter_list: List of parameter names and values to use when executing the SageMaker Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                sage_maker_pipeline_parameters_property = scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9502019edaf3833251c7f83dc093b91afe4b2a6a6cc7bc4365c5ec059038ee3)
                check_type(argname="argument pipeline_parameter_list", value=pipeline_parameter_list, expected_type=type_hints["pipeline_parameter_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pipeline_parameter_list is not None:
                self._values["pipeline_parameter_list"] = pipeline_parameter_list

        @builtins.property
        def pipeline_parameter_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.SageMakerPipelineParameterProperty"]]]]:
            '''List of parameter names and values to use when executing the SageMaker Model Building Pipeline.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameters.html#cfn-scheduler-schedule-sagemakerpipelineparameters-pipelineparameterlist
            '''
            result = self._values.get("pipeline_parameter_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.SageMakerPipelineParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SageMakerPipelineParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.SqsParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"message_group_id": "messageGroupId"},
    )
    class SqsParametersProperty:
        def __init__(
            self,
            *,
            message_group_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The templated target type for the Amazon SQS ```SendMessage`` <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html>`_ API operation. Contains the message group ID to use when the target is a FIFO queue. If you specify an Amazon SQS FIFO queue as a target, the queue must have content-based deduplication enabled. For more information, see `Using the Amazon SQS message deduplication ID <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html>`_ in the *Amazon SQS Developer Guide* .

            :param message_group_id: The FIFO message group ID to use as the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sqsparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                sqs_parameters_property = scheduler_mixins.CfnSchedulePropsMixin.SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81498243f5796c9ff7b0e380f102fa5a68015c0e24a88700cd6d2770b9f1bb1b)
                check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_group_id is not None:
                self._values["message_group_id"] = message_group_id

        @builtins.property
        def message_group_id(self) -> typing.Optional[builtins.str]:
            '''The FIFO message group ID to use as the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sqsparameters.html#cfn-scheduler-schedule-sqsparameters-messagegroupid
            '''
            result = self._values.get("message_group_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SqsParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_scheduler.mixins.CfnSchedulePropsMixin.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "arn": "arn",
            "dead_letter_config": "deadLetterConfig",
            "ecs_parameters": "ecsParameters",
            "event_bridge_parameters": "eventBridgeParameters",
            "input": "input",
            "kinesis_parameters": "kinesisParameters",
            "retry_policy": "retryPolicy",
            "role_arn": "roleArn",
            "sage_maker_pipeline_parameters": "sageMakerPipelineParameters",
            "sqs_parameters": "sqsParameters",
        },
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            arn: typing.Optional[builtins.str] = None,
            dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.DeadLetterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ecs_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.EcsParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            event_bridge_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.EventBridgeParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input: typing.Optional[builtins.str] = None,
            kinesis_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.KinesisParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            retry_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.RetryPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            role_arn: typing.Optional[builtins.str] = None,
            sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.SageMakerPipelineParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sqs_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSchedulePropsMixin.SqsParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The schedule's target.

            EventBridge Scheduler supports templated target that invoke common API operations, as well as universal targets that you can customize to invoke over 6,000 API operations across more than 270 services. You can only specify one templated or universal target for a schedule.

            :param arn: The Amazon Resource Name (ARN) of the target.
            :param dead_letter_config: An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule. If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.
            :param ecs_parameters: The templated target type for the Amazon ECS ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API operation.
            :param event_bridge_parameters: The templated target type for the EventBridge ```PutEvents`` <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ API operation.
            :param input: The text, or well-formed JSON, passed to the target. If you are configuring a templated Lambda , AWS Step Functions , or Amazon EventBridge target, the input must be a well-formed JSON. For all other target types, a JSON is not required. If you do not specify anything for this field, Amazon EventBridge Scheduler delivers a default notification to the target.
            :param kinesis_parameters: The templated target type for the Amazon Kinesis ```PutRecord`` <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html>`_ API operation.
            :param retry_policy: A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role that EventBridge Scheduler will use for this target when the schedule is invoked.
            :param sage_maker_pipeline_parameters: The templated target type for the Amazon SageMaker ```StartPipelineExecution`` <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_StartPipelineExecution.html>`_ API operation.
            :param sqs_parameters: The templated target type for the Amazon SQS ```SendMessage`` <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html>`_ API operation. Contains the message group ID to use when the target is a FIFO queue. If you specify an Amazon SQS FIFO queue as a target, the queue must have content-based deduplication enabled. For more information, see `Using the Amazon SQS message deduplication ID <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html>`_ in the *Amazon SQS Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_scheduler import mixins as scheduler_mixins
                
                # tags: Any
                
                target_property = scheduler_mixins.CfnSchedulePropsMixin.TargetProperty(
                    arn="arn",
                    dead_letter_config=scheduler_mixins.CfnSchedulePropsMixin.DeadLetterConfigProperty(
                        arn="arn"
                    ),
                    ecs_parameters=scheduler_mixins.CfnSchedulePropsMixin.EcsParametersProperty(
                        capacity_provider_strategy=[scheduler_mixins.CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty(
                            base=123,
                            capacity_provider="capacityProvider",
                            weight=123
                        )],
                        enable_ecs_managed_tags=False,
                        enable_execute_command=False,
                        group="group",
                        launch_type="launchType",
                        network_configuration=scheduler_mixins.CfnSchedulePropsMixin.NetworkConfigurationProperty(
                            awsvpc_configuration=scheduler_mixins.CfnSchedulePropsMixin.AwsVpcConfigurationProperty(
                                assign_public_ip="assignPublicIp",
                                security_groups=["securityGroups"],
                                subnets=["subnets"]
                            )
                        ),
                        placement_constraints=[scheduler_mixins.CfnSchedulePropsMixin.PlacementConstraintProperty(
                            expression="expression",
                            type="type"
                        )],
                        placement_strategy=[scheduler_mixins.CfnSchedulePropsMixin.PlacementStrategyProperty(
                            field="field",
                            type="type"
                        )],
                        platform_version="platformVersion",
                        propagate_tags="propagateTags",
                        reference_id="referenceId",
                        tags=tags,
                        task_count=123,
                        task_definition_arn="taskDefinitionArn"
                    ),
                    event_bridge_parameters=scheduler_mixins.CfnSchedulePropsMixin.EventBridgeParametersProperty(
                        detail_type="detailType",
                        source="source"
                    ),
                    input="input",
                    kinesis_parameters=scheduler_mixins.CfnSchedulePropsMixin.KinesisParametersProperty(
                        partition_key="partitionKey"
                    ),
                    retry_policy=scheduler_mixins.CfnSchedulePropsMixin.RetryPolicyProperty(
                        maximum_event_age_in_seconds=123,
                        maximum_retry_attempts=123
                    ),
                    role_arn="roleArn",
                    sage_maker_pipeline_parameters=scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParametersProperty(
                        pipeline_parameter_list=[scheduler_mixins.CfnSchedulePropsMixin.SageMakerPipelineParameterProperty(
                            name="name",
                            value="value"
                        )]
                    ),
                    sqs_parameters=scheduler_mixins.CfnSchedulePropsMixin.SqsParametersProperty(
                        message_group_id="messageGroupId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0731341e646835293302fad4238cc1e3da92dfc1995b5b1522d59394ace9f16)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
                check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
                check_type(argname="argument ecs_parameters", value=ecs_parameters, expected_type=type_hints["ecs_parameters"])
                check_type(argname="argument event_bridge_parameters", value=event_bridge_parameters, expected_type=type_hints["event_bridge_parameters"])
                check_type(argname="argument input", value=input, expected_type=type_hints["input"])
                check_type(argname="argument kinesis_parameters", value=kinesis_parameters, expected_type=type_hints["kinesis_parameters"])
                check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument sage_maker_pipeline_parameters", value=sage_maker_pipeline_parameters, expected_type=type_hints["sage_maker_pipeline_parameters"])
                check_type(argname="argument sqs_parameters", value=sqs_parameters, expected_type=type_hints["sqs_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn
            if dead_letter_config is not None:
                self._values["dead_letter_config"] = dead_letter_config
            if ecs_parameters is not None:
                self._values["ecs_parameters"] = ecs_parameters
            if event_bridge_parameters is not None:
                self._values["event_bridge_parameters"] = event_bridge_parameters
            if input is not None:
                self._values["input"] = input
            if kinesis_parameters is not None:
                self._values["kinesis_parameters"] = kinesis_parameters
            if retry_policy is not None:
                self._values["retry_policy"] = retry_policy
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if sage_maker_pipeline_parameters is not None:
                self._values["sage_maker_pipeline_parameters"] = sage_maker_pipeline_parameters
            if sqs_parameters is not None:
                self._values["sqs_parameters"] = sqs_parameters

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dead_letter_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.DeadLetterConfigProperty"]]:
            '''An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule.

            If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-deadletterconfig
            '''
            result = self._values.get("dead_letter_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.DeadLetterConfigProperty"]], result)

        @builtins.property
        def ecs_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.EcsParametersProperty"]]:
            '''The templated target type for the Amazon ECS ```RunTask`` <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_RunTask.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-ecsparameters
            '''
            result = self._values.get("ecs_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.EcsParametersProperty"]], result)

        @builtins.property
        def event_bridge_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.EventBridgeParametersProperty"]]:
            '''The templated target type for the EventBridge ```PutEvents`` <https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEvents.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-eventbridgeparameters
            '''
            result = self._values.get("event_bridge_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.EventBridgeParametersProperty"]], result)

        @builtins.property
        def input(self) -> typing.Optional[builtins.str]:
            '''The text, or well-formed JSON, passed to the target.

            If you are configuring a templated Lambda , AWS Step Functions , or Amazon EventBridge target, the input must be a well-formed JSON. For all other target types, a JSON is not required. If you do not specify anything for this field, Amazon EventBridge Scheduler delivers a default notification to the target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-input
            '''
            result = self._values.get("input")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kinesis_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.KinesisParametersProperty"]]:
            '''The templated target type for the Amazon Kinesis ```PutRecord`` <https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-kinesisparameters
            '''
            result = self._values.get("kinesis_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.KinesisParametersProperty"]], result)

        @builtins.property
        def retry_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.RetryPolicyProperty"]]:
            '''A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-retrypolicy
            '''
            result = self._values.get("retry_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.RetryPolicyProperty"]], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that EventBridge Scheduler will use for this target when the schedule is invoked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sage_maker_pipeline_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.SageMakerPipelineParametersProperty"]]:
            '''The templated target type for the Amazon SageMaker ```StartPipelineExecution`` <https://docs.aws.amazon.com/sagemaker/latest/APIReference/API_StartPipelineExecution.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-sagemakerpipelineparameters
            '''
            result = self._values.get("sage_maker_pipeline_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.SageMakerPipelineParametersProperty"]], result)

        @builtins.property
        def sqs_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.SqsParametersProperty"]]:
            '''The templated target type for the Amazon SQS ```SendMessage`` <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessage.html>`_ API operation. Contains the message group ID to use when the target is a FIFO queue. If you specify an Amazon SQS FIFO queue as a target, the queue must have content-based deduplication enabled. For more information, see `Using the Amazon SQS message deduplication ID <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagededuplicationid-property.html>`_ in the *Amazon SQS Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-target.html#cfn-scheduler-schedule-target-sqsparameters
            '''
            result = self._values.get("sqs_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSchedulePropsMixin.SqsParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnScheduleGroupMixinProps",
    "CfnScheduleGroupPropsMixin",
    "CfnScheduleMixinProps",
    "CfnSchedulePropsMixin",
]

publication.publish()

def _typecheckingstub__0f41809396e9b302399be27623d823e2043d84fc0fdf3e30103abe6c59fd61ad(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fd3ce521c7e9aa444d8dda456e82be140727c4029eee2dda78f0fc89ee1d7e(
    props: typing.Union[CfnScheduleGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d7cdb79dd32bc37fb9b13a16e6cd510e35875276e52455d0d32aaa9cab14401(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7a9f8db37bc7d09ac235111d6fbaf20dca16cf384b466aebbae6c3a0a73e3c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55849960d7d353d3d9c111ad7d4e58768dff095382ce7edf336f0347a8c93877(
    *,
    description: typing.Optional[builtins.str] = None,
    end_date: typing.Optional[builtins.str] = None,
    flexible_time_window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.FlexibleTimeWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    group_name: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schedule_expression: typing.Optional[builtins.str] = None,
    schedule_expression_timezone: typing.Optional[builtins.str] = None,
    start_date: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    target: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.TargetProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf2f4be196d1628cff3054470314cde2a5cfeec951349e9701246d5c70681f8(
    props: typing.Union[CfnScheduleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fc9ed95540311843fcfdc4db20e4e53e9ab3dacd2120c564000fc2dc4b819f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602251a262dba757f6a312b0a293fa755a33e531bb4d904bb33af1b206b83cae(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d251444898c805ce9fb72ce04c05900ccf0aa8595d7c618d104dd00def4b1b(
    *,
    assign_public_ip: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b897a72d404a46fd766b8dadccf3d141c747f5cce0deb90847febc98b8605d1f(
    *,
    base: typing.Optional[jsii.Number] = None,
    capacity_provider: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac94e8785420a40545598d257ae0cfd23047536aa7f252c45316f2aebceb1e80(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64b5fe6f0a4048453831eabd757993b75f1007690f93d655a6b31617ae613ba(
    *,
    capacity_provider_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.CapacityProviderStrategyItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enable_ecs_managed_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_execute_command: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    group: typing.Optional[builtins.str] = None,
    launch_type: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    placement_constraints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.PlacementConstraintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    placement_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.PlacementStrategyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_version: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.str] = None,
    reference_id: typing.Optional[builtins.str] = None,
    tags: typing.Any = None,
    task_count: typing.Optional[jsii.Number] = None,
    task_definition_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95ebf16c8c12343fb0429de2af7c93fb76341078187081707ef40c29715639ae(
    *,
    detail_type: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39639eaeed8ea5405219574a6d8a9d8129c9341cfd2818d579344f8c0157b554(
    *,
    maximum_window_in_minutes: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5712ea2f00e8f557c4ecb16a5e437bf4b1dbcac7f961cae2c6d73a709d5cf60(
    *,
    partition_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b098d09a7cd07f214a4ee9fa81cf72c9bcf24c5c3de1684c9a62f07467c39e8(
    *,
    awsvpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.AwsVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0895c82ff773ca7f5928c634a5b1f89c4a2ea44fae7d32f2fda7e02fd86e56(
    *,
    expression: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e49f8ee660efd8573a9d7640f2ff297bbc431d09343398d92a2d5bbae814da48(
    *,
    field: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1172557826ff08bc8699e23336dbec517df8b28c0b1af69fed2fa0e062e6675f(
    *,
    maximum_event_age_in_seconds: typing.Optional[jsii.Number] = None,
    maximum_retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f9c524470b329d824328500e5ae1d5eac09f30289ddda0d28ab98a9698a85f(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9502019edaf3833251c7f83dc093b91afe4b2a6a6cc7bc4365c5ec059038ee3(
    *,
    pipeline_parameter_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.SageMakerPipelineParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81498243f5796c9ff7b0e380f102fa5a68015c0e24a88700cd6d2770b9f1bb1b(
    *,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0731341e646835293302fad4238cc1e3da92dfc1995b5b1522d59394ace9f16(
    *,
    arn: typing.Optional[builtins.str] = None,
    dead_letter_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ecs_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    event_bridge_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.EventBridgeParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input: typing.Optional[builtins.str] = None,
    kinesis_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    retry_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sqs_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSchedulePropsMixin.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
