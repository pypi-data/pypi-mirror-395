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
    jsii_type="@aws-cdk/mixins-preview.aws_arczonalshift.mixins.CfnAutoshiftObserverNotificationStatusMixinProps",
    jsii_struct_bases=[],
    name_mapping={"status": "status"},
)
class CfnAutoshiftObserverNotificationStatusMixinProps:
    def __init__(self, *, status: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnAutoshiftObserverNotificationStatusPropsMixin.

        :param status: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-autoshiftobservernotificationstatus.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_arczonalshift import mixins as arczonalshift_mixins
            
            cfn_autoshift_observer_notification_status_mixin_props = arczonalshift_mixins.CfnAutoshiftObserverNotificationStatusMixinProps(
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1e0a207ae1e0fbf1fb794d9c334830b45e829573eb6130954cf192e8d8c55e4)
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-autoshiftobservernotificationstatus.html#cfn-arczonalshift-autoshiftobservernotificationstatus-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAutoshiftObserverNotificationStatusMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAutoshiftObserverNotificationStatusPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_arczonalshift.mixins.CfnAutoshiftObserverNotificationStatusPropsMixin",
):
    '''Definition of AWS::ARCZonalShift::AutoshiftObserverNotificationStatus Resource Type.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-autoshiftobservernotificationstatus.html
    :cloudformationResource: AWS::ARCZonalShift::AutoshiftObserverNotificationStatus
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_arczonalshift import mixins as arczonalshift_mixins
        
        cfn_autoshift_observer_notification_status_props_mixin = arczonalshift_mixins.CfnAutoshiftObserverNotificationStatusPropsMixin(arczonalshift_mixins.CfnAutoshiftObserverNotificationStatusMixinProps(
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAutoshiftObserverNotificationStatusMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ARCZonalShift::AutoshiftObserverNotificationStatus``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6db831d23b9e3d9a78058e1fe0bd1d69d8e3fe9156dfe092a5865c61d8c0ff2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca5690888524f5790c917a08ca0c6e0b82d9c72942b9a619ee1689f9ec755c5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ec16fb2df52dbfcfd6610799beed97afdf6d70a8a64994d7730ef9d839e1e64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAutoshiftObserverNotificationStatusMixinProps:
        return typing.cast(CfnAutoshiftObserverNotificationStatusMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_arczonalshift.mixins.CfnZonalAutoshiftConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "practice_run_configuration": "practiceRunConfiguration",
        "resource_identifier": "resourceIdentifier",
        "zonal_autoshift_status": "zonalAutoshiftStatus",
    },
)
class CfnZonalAutoshiftConfigurationMixinProps:
    def __init__(
        self,
        *,
        practice_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_identifier: typing.Optional[builtins.str] = None,
        zonal_autoshift_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnZonalAutoshiftConfigurationPropsMixin.

        :param practice_run_configuration: A practice run configuration for a resource includes the Amazon CloudWatch alarms that you've specified for a practice run, as well as any blocked dates or blocked windows for the practice run. When a resource has a practice run configuration, ARC shifts traffic for the resource weekly for practice runs. Practice runs are required for zonal autoshift. The zonal shifts that ARC starts for practice runs help you to ensure that shifting away traffic from an Availability Zone during an autoshift is safe for your application. You can update or delete a practice run configuration. Before you delete a practice run configuration, you must disable zonal autoshift for the resource. A practice run configuration is required when zonal autoshift is enabled.
        :param resource_identifier: The identifier for the resource that AWS shifts traffic for. The identifier is the Amazon Resource Name (ARN) for the resource. At this time, supported resources are Network Load Balancers and Application Load Balancers.
        :param zonal_autoshift_status: When zonal autoshift is ``ENABLED`` , you authorize AWS to shift away resource traffic for an application from an Availability Zone during events, on your behalf, to help reduce time to recovery. Traffic is also shifted away for the required weekly practice runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-zonalautoshiftconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_arczonalshift import mixins as arczonalshift_mixins
            
            cfn_zonal_autoshift_configuration_mixin_props = arczonalshift_mixins.CfnZonalAutoshiftConfigurationMixinProps(
                practice_run_configuration=arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty(
                    blocked_dates=["blockedDates"],
                    blocked_windows=["blockedWindows"],
                    blocking_alarms=[arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                        alarm_identifier="alarmIdentifier",
                        type="type"
                    )],
                    outcome_alarms=[arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                        alarm_identifier="alarmIdentifier",
                        type="type"
                    )]
                ),
                resource_identifier="resourceIdentifier",
                zonal_autoshift_status="zonalAutoshiftStatus"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05e9e8f3280b971b8328da9b854c7e11658955e48d56ec89ec894b1e7b48ae2)
            check_type(argname="argument practice_run_configuration", value=practice_run_configuration, expected_type=type_hints["practice_run_configuration"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument zonal_autoshift_status", value=zonal_autoshift_status, expected_type=type_hints["zonal_autoshift_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if practice_run_configuration is not None:
            self._values["practice_run_configuration"] = practice_run_configuration
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if zonal_autoshift_status is not None:
            self._values["zonal_autoshift_status"] = zonal_autoshift_status

    @builtins.property
    def practice_run_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty"]]:
        '''A practice run configuration for a resource includes the Amazon CloudWatch alarms that you've specified for a practice run, as well as any blocked dates or blocked windows for the practice run.

        When a resource has a practice run configuration, ARC shifts traffic for the resource weekly for practice runs.

        Practice runs are required for zonal autoshift. The zonal shifts that ARC starts for practice runs help you to ensure that shifting away traffic from an Availability Zone during an autoshift is safe for your application.

        You can update or delete a practice run configuration. Before you delete a practice run configuration, you must disable zonal autoshift for the resource. A practice run configuration is required when zonal autoshift is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-zonalautoshiftconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration
        '''
        result = self._values.get("practice_run_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty"]], result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The identifier for the resource that AWS shifts traffic for.

        The identifier is the Amazon Resource Name (ARN) for the resource.

        At this time, supported resources are Network Load Balancers and Application Load Balancers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-zonalautoshiftconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zonal_autoshift_status(self) -> typing.Optional[builtins.str]:
        '''When zonal autoshift is ``ENABLED`` , you authorize AWS to shift away resource traffic for an application from an Availability Zone during events, on your behalf, to help reduce time to recovery.

        Traffic is also shifted away for the required weekly practice runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-zonalautoshiftconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-zonalautoshiftstatus
        '''
        result = self._values.get("zonal_autoshift_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnZonalAutoshiftConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnZonalAutoshiftConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_arczonalshift.mixins.CfnZonalAutoshiftConfigurationPropsMixin",
):
    '''The zonal autoshift configuration for a resource includes the practice run configuration and the status for running autoshifts, zonal autoshift status.

    When a resource has a practice run configuation, ARC starts weekly zonal shifts for the resource, to shift traffic away from an Availability Zone. Weekly practice runs help you to make sure that your application can continue to operate normally with the loss of one Availability Zone.

    You can update the zonal autoshift autoshift status to enable or disable zonal autoshift. When zonal autoshift is ``ENABLED`` , you authorize AWS to shift away resource traffic for an application from an Availability Zone during events, on your behalf, to help reduce time to recovery. Traffic is also shifted away for the required weekly practice runs.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-arczonalshift-zonalautoshiftconfiguration.html
    :cloudformationResource: AWS::ARCZonalShift::ZonalAutoshiftConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_arczonalshift import mixins as arczonalshift_mixins
        
        cfn_zonal_autoshift_configuration_props_mixin = arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin(arczonalshift_mixins.CfnZonalAutoshiftConfigurationMixinProps(
            practice_run_configuration=arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty(
                blocked_dates=["blockedDates"],
                blocked_windows=["blockedWindows"],
                blocking_alarms=[arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                    alarm_identifier="alarmIdentifier",
                    type="type"
                )],
                outcome_alarms=[arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                    alarm_identifier="alarmIdentifier",
                    type="type"
                )]
            ),
            resource_identifier="resourceIdentifier",
            zonal_autoshift_status="zonalAutoshiftStatus"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnZonalAutoshiftConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ARCZonalShift::ZonalAutoshiftConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336fac2aa7cde77b7a7f16a1382e5768c0e12322369be400ff798d9577d10117)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ba9d5a6c6f5ea8f3c537e7a4ee6daf9a75a960d6a3e0d8641e2affbd9d9e2a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce91b4b13200f035238c268333f35164f2c140c514baba637eadf36bb5c7cf29)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnZonalAutoshiftConfigurationMixinProps:
        return typing.cast(CfnZonalAutoshiftConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arczonalshift.mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_identifier": "alarmIdentifier", "type": "type"},
    )
    class ControlConditionProperty:
        def __init__(
            self,
            *,
            alarm_identifier: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A control condition is an alarm that you specify for a practice run.

            When you configure practice runs with zonal autoshift for a resource, you specify Amazon CloudWatch alarms, which you create in CloudWatch to use with the practice run. The alarms that you specify are an *outcome alarm* , to monitor application health during practice runs and, optionally, a *blocking alarm* , to block practice runs from starting or to interrupt a practice run in progress.

            Control condition alarms do not apply for autoshifts.

            For more information, see `Considerations when you configure zonal autoshift <https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-autoshift.considerations.html>`_ in the ARC Developer Guide.

            :param alarm_identifier: The Amazon Resource Name (ARN) for an Amazon CloudWatch alarm that you specify as a control condition for a practice run.
            :param type: The type of alarm specified for a practice run. You can only specify Amazon CloudWatch alarms for practice runs, so the only valid value is ``CLOUDWATCH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-controlcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arczonalshift import mixins as arczonalshift_mixins
                
                control_condition_property = arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                    alarm_identifier="alarmIdentifier",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60cedd1ca9b6d75f2ca9ae3dc615f4f094f73a34bbbe26b766d9392104e08698)
                check_type(argname="argument alarm_identifier", value=alarm_identifier, expected_type=type_hints["alarm_identifier"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_identifier is not None:
                self._values["alarm_identifier"] = alarm_identifier
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def alarm_identifier(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for an Amazon CloudWatch alarm that you specify as a control condition for a practice run.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-controlcondition.html#cfn-arczonalshift-zonalautoshiftconfiguration-controlcondition-alarmidentifier
            '''
            result = self._values.get("alarm_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of alarm specified for a practice run.

            You can only specify Amazon CloudWatch alarms for practice runs, so the only valid value is ``CLOUDWATCH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-controlcondition.html#cfn-arczonalshift-zonalautoshiftconfiguration-controlcondition-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ControlConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_arczonalshift.mixins.CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "blocked_dates": "blockedDates",
            "blocked_windows": "blockedWindows",
            "blocking_alarms": "blockingAlarms",
            "outcome_alarms": "outcomeAlarms",
        },
    )
    class PracticeRunConfigurationProperty:
        def __init__(
            self,
            *,
            blocked_dates: typing.Optional[typing.Sequence[builtins.str]] = None,
            blocked_windows: typing.Optional[typing.Sequence[builtins.str]] = None,
            blocking_alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            outcome_alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A practice run configuration for a resource includes the Amazon CloudWatch alarms that you've specified for a practice run, as well as any blocked dates or blocked windows for the practice run.

            When a resource has a practice run configuation, ARC starts weekly zonal shifts for the resource, to shift traffic away from an Availability Zone. Weekly practice runs help you to make sure that your application can continue to operate normally with the loss of one Availability Zone.

            You can update or delete a practice run configuration. When you delete a practice run configuration, zonal autoshift is disabled for the resource. A practice run configuration is required when zonal autoshift is enabled.

            :param blocked_dates: An array of one or more dates that you can specify when AWS does not start practice runs for a resource. Dates are in UTC. Specify blocked dates in the format ``YYYY-MM-DD`` , separated by spaces.
            :param blocked_windows: An array of one or more days and times that you can specify when ARC does not start practice runs for a resource. Days and times are in UTC. Specify blocked windows in the format ``DAY:HH:MM-DAY:HH:MM`` , separated by spaces. For example, ``MON:18:30-MON:19:30 TUE:18:30-TUE:19:30`` . .. epigraph:: Blocked windows have to start and end on the same day. Windows that span multiple days aren't supported.
            :param blocking_alarms: An optional alarm that you can specify that blocks practice runs when the alarm is in an ``ALARM`` state. When a blocking alarm goes into an ``ALARM`` state, it prevents practice runs from being started, and ends practice runs that are in progress.
            :param outcome_alarms: The alarm that you specify to monitor the health of your application during practice runs. When the outcome alarm goes into an ``ALARM`` state, the practice run is ended and the outcome is set to ``FAILED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_arczonalshift import mixins as arczonalshift_mixins
                
                practice_run_configuration_property = arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty(
                    blocked_dates=["blockedDates"],
                    blocked_windows=["blockedWindows"],
                    blocking_alarms=[arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                        alarm_identifier="alarmIdentifier",
                        type="type"
                    )],
                    outcome_alarms=[arczonalshift_mixins.CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty(
                        alarm_identifier="alarmIdentifier",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8efba25e9ef5e52a80a9ad252440a0acae8f4736f379faa13a2b0c2c5ddaacad)
                check_type(argname="argument blocked_dates", value=blocked_dates, expected_type=type_hints["blocked_dates"])
                check_type(argname="argument blocked_windows", value=blocked_windows, expected_type=type_hints["blocked_windows"])
                check_type(argname="argument blocking_alarms", value=blocking_alarms, expected_type=type_hints["blocking_alarms"])
                check_type(argname="argument outcome_alarms", value=outcome_alarms, expected_type=type_hints["outcome_alarms"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if blocked_dates is not None:
                self._values["blocked_dates"] = blocked_dates
            if blocked_windows is not None:
                self._values["blocked_windows"] = blocked_windows
            if blocking_alarms is not None:
                self._values["blocking_alarms"] = blocking_alarms
            if outcome_alarms is not None:
                self._values["outcome_alarms"] = outcome_alarms

        @builtins.property
        def blocked_dates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of one or more dates that you can specify when AWS does not start practice runs for a resource.

            Dates are in UTC.

            Specify blocked dates in the format ``YYYY-MM-DD`` , separated by spaces.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration-blockeddates
            '''
            result = self._values.get("blocked_dates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def blocked_windows(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of one or more days and times that you can specify when ARC does not start practice runs for a resource.

            Days and times are in UTC.

            Specify blocked windows in the format ``DAY:HH:MM-DAY:HH:MM`` , separated by spaces. For example, ``MON:18:30-MON:19:30 TUE:18:30-TUE:19:30`` .
            .. epigraph::

               Blocked windows have to start and end on the same day. Windows that span multiple days aren't supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration-blockedwindows
            '''
            result = self._values.get("blocked_windows")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def blocking_alarms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty"]]]]:
            '''An optional alarm that you can specify that blocks practice runs when the alarm is in an ``ALARM`` state.

            When a blocking alarm goes into an ``ALARM`` state, it prevents practice runs from being started, and ends practice runs that are in progress.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration-blockingalarms
            '''
            result = self._values.get("blocking_alarms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty"]]]], result)

        @builtins.property
        def outcome_alarms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty"]]]]:
            '''The alarm that you specify to monitor the health of your application during practice runs.

            When the outcome alarm goes into an ``ALARM`` state, the practice run is ended and the outcome is set to ``FAILED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration.html#cfn-arczonalshift-zonalautoshiftconfiguration-practicerunconfiguration-outcomealarms
            '''
            result = self._values.get("outcome_alarms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PracticeRunConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAutoshiftObserverNotificationStatusMixinProps",
    "CfnAutoshiftObserverNotificationStatusPropsMixin",
    "CfnZonalAutoshiftConfigurationMixinProps",
    "CfnZonalAutoshiftConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__e1e0a207ae1e0fbf1fb794d9c334830b45e829573eb6130954cf192e8d8c55e4(
    *,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6db831d23b9e3d9a78058e1fe0bd1d69d8e3fe9156dfe092a5865c61d8c0ff2(
    props: typing.Union[CfnAutoshiftObserverNotificationStatusMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5690888524f5790c917a08ca0c6e0b82d9c72942b9a619ee1689f9ec755c5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ec16fb2df52dbfcfd6610799beed97afdf6d70a8a64994d7730ef9d839e1e64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05e9e8f3280b971b8328da9b854c7e11658955e48d56ec89ec894b1e7b48ae2(
    *,
    practice_run_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnZonalAutoshiftConfigurationPropsMixin.PracticeRunConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_identifier: typing.Optional[builtins.str] = None,
    zonal_autoshift_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336fac2aa7cde77b7a7f16a1382e5768c0e12322369be400ff798d9577d10117(
    props: typing.Union[CfnZonalAutoshiftConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba9d5a6c6f5ea8f3c537e7a4ee6daf9a75a960d6a3e0d8641e2affbd9d9e2a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce91b4b13200f035238c268333f35164f2c140c514baba637eadf36bb5c7cf29(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60cedd1ca9b6d75f2ca9ae3dc615f4f094f73a34bbbe26b766d9392104e08698(
    *,
    alarm_identifier: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efba25e9ef5e52a80a9ad252440a0acae8f4736f379faa13a2b0c2c5ddaacad(
    *,
    blocked_dates: typing.Optional[typing.Sequence[builtins.str]] = None,
    blocked_windows: typing.Optional[typing.Sequence[builtins.str]] = None,
    blocking_alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    outcome_alarms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnZonalAutoshiftConfigurationPropsMixin.ControlConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
