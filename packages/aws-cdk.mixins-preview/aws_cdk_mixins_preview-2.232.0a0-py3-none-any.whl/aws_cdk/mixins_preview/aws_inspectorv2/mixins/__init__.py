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
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "scan_name": "scanName",
        "schedule": "schedule",
        "security_level": "securityLevel",
        "tags": "tags",
        "targets": "targets",
    },
)
class CfnCisScanConfigurationMixinProps:
    def __init__(
        self,
        *,
        scan_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_level: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.CisTargetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCisScanConfigurationPropsMixin.

        :param scan_name: The name of the CIS scan configuration.
        :param schedule: The CIS scan configuration's schedule.
        :param security_level: The CIS scan configuration's CIS Benchmark level.
        :param tags: The CIS scan configuration's tags.
        :param targets: The CIS scan configuration's targets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
            
            # one_time: Any
            
            cfn_cis_scan_configuration_mixin_props = inspectorv2_mixins.CfnCisScanConfigurationMixinProps(
                scan_name="scanName",
                schedule=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.ScheduleProperty(
                    daily=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.DailyScheduleProperty(
                        start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                            time_of_day="timeOfDay",
                            time_zone="timeZone"
                        )
                    ),
                    monthly=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty(
                        day="day",
                        start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                            time_of_day="timeOfDay",
                            time_zone="timeZone"
                        )
                    ),
                    one_time=one_time,
                    weekly=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty(
                        days=["days"],
                        start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                            time_of_day="timeOfDay",
                            time_zone="timeZone"
                        )
                    )
                ),
                security_level="securityLevel",
                tags={
                    "tags_key": "tags"
                },
                targets=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.CisTargetsProperty(
                    account_ids=["accountIds"],
                    target_resource_tags={
                        "target_resource_tags_key": ["targetResourceTags"]
                    }
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9a3c2a60909e46157424b4a08a0572a7925991fcb98a1dd25599df811aaefbe)
            check_type(argname="argument scan_name", value=scan_name, expected_type=type_hints["scan_name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument security_level", value=security_level, expected_type=type_hints["security_level"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if scan_name is not None:
            self._values["scan_name"] = scan_name
        if schedule is not None:
            self._values["schedule"] = schedule
        if security_level is not None:
            self._values["security_level"] = security_level
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def scan_name(self) -> typing.Optional[builtins.str]:
        '''The name of the CIS scan configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html#cfn-inspectorv2-cisscanconfiguration-scanname
        '''
        result = self._values.get("scan_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.ScheduleProperty"]]:
        '''The CIS scan configuration's schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html#cfn-inspectorv2-cisscanconfiguration-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.ScheduleProperty"]], result)

    @builtins.property
    def security_level(self) -> typing.Optional[builtins.str]:
        '''The CIS scan configuration's CIS Benchmark level.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html#cfn-inspectorv2-cisscanconfiguration-securitylevel
        '''
        result = self._values.get("security_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The CIS scan configuration's tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html#cfn-inspectorv2-cisscanconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.CisTargetsProperty"]]:
        '''The CIS scan configuration's targets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html#cfn-inspectorv2-cisscanconfiguration-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.CisTargetsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCisScanConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCisScanConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin",
):
    '''The CIS scan configuration.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-cisscanconfiguration.html
    :cloudformationResource: AWS::InspectorV2::CisScanConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
        
        # one_time: Any
        
        cfn_cis_scan_configuration_props_mixin = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin(inspectorv2_mixins.CfnCisScanConfigurationMixinProps(
            scan_name="scanName",
            schedule=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.ScheduleProperty(
                daily=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.DailyScheduleProperty(
                    start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                        time_of_day="timeOfDay",
                        time_zone="timeZone"
                    )
                ),
                monthly=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty(
                    day="day",
                    start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                        time_of_day="timeOfDay",
                        time_zone="timeZone"
                    )
                ),
                one_time=one_time,
                weekly=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty(
                    days=["days"],
                    start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                        time_of_day="timeOfDay",
                        time_zone="timeZone"
                    )
                )
            ),
            security_level="securityLevel",
            tags={
                "tags_key": "tags"
            },
            targets=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.CisTargetsProperty(
                account_ids=["accountIds"],
                target_resource_tags={
                    "target_resource_tags_key": ["targetResourceTags"]
                }
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCisScanConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::InspectorV2::CisScanConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff8e8887aa60a5fcedd4e932df8d2aeb0d13ad3dde0651e1cd929ee83dc5ad9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9d42d273d6e89027831aa7bf162739eebfa6672bc067606e9e7b75eb941b274)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__befa26716aa3ba851788aa87858f508ac5c860b6606ea92132c658081364bfc8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCisScanConfigurationMixinProps:
        return typing.cast(CfnCisScanConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin.CisTargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_ids": "accountIds",
            "target_resource_tags": "targetResourceTags",
        },
    )
    class CisTargetsProperty:
        def __init__(
            self,
            *,
            account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            target_resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
        ) -> None:
            '''The CIS targets.

            :param account_ids: The CIS target account ids.
            :param target_resource_tags: The CIS target resource tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-cistargets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                cis_targets_property = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.CisTargetsProperty(
                    account_ids=["accountIds"],
                    target_resource_tags={
                        "target_resource_tags_key": ["targetResourceTags"]
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c87bccf8d0ce42f43e51fac9e4ee11cfbd7317dc82154df3968668980e776fc3)
                check_type(argname="argument account_ids", value=account_ids, expected_type=type_hints["account_ids"])
                check_type(argname="argument target_resource_tags", value=target_resource_tags, expected_type=type_hints["target_resource_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_ids is not None:
                self._values["account_ids"] = account_ids
            if target_resource_tags is not None:
                self._values["target_resource_tags"] = target_resource_tags

        @builtins.property
        def account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The CIS target account ids.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-cistargets.html#cfn-inspectorv2-cisscanconfiguration-cistargets-accountids
            '''
            result = self._values.get("account_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def target_resource_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]]:
            '''The CIS target resource tags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-cistargets.html#cfn-inspectorv2-cisscanconfiguration-cistargets-targetresourcetags
            '''
            result = self._values.get("target_resource_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.List[builtins.str]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CisTargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin.DailyScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"start_time": "startTime"},
    )
    class DailyScheduleProperty:
        def __init__(
            self,
            *,
            start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.TimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A daily schedule.

            :param start_time: The schedule start time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-dailyschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                daily_schedule_property = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.DailyScheduleProperty(
                    start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                        time_of_day="timeOfDay",
                        time_zone="timeZone"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f78b534217bb57a303eec64b8bbb2d3eb96ad6d8146c99bec7ce4e72abc2afe2)
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def start_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.TimeProperty"]]:
            '''The schedule start time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-dailyschedule.html#cfn-inspectorv2-cisscanconfiguration-dailyschedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.TimeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DailyScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "start_time": "startTime"},
    )
    class MonthlyScheduleProperty:
        def __init__(
            self,
            *,
            day: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.TimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A monthly schedule.

            :param day: The monthly schedule's day.
            :param start_time: The monthly schedule's start time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-monthlyschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                monthly_schedule_property = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty(
                    day="day",
                    start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                        time_of_day="timeOfDay",
                        time_zone="timeZone"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__700408d8629f043c24bfa755f2968e7cf2f498ec2ca3af37bc3aaeb4a6f0a4e8)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day is not None:
                self._values["day"] = day
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def day(self) -> typing.Optional[builtins.str]:
            '''The monthly schedule's day.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-monthlyschedule.html#cfn-inspectorv2-cisscanconfiguration-monthlyschedule-day
            '''
            result = self._values.get("day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.TimeProperty"]]:
            '''The monthly schedule's start time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-monthlyschedule.html#cfn-inspectorv2-cisscanconfiguration-monthlyschedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.TimeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonthlyScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily": "daily",
            "monthly": "monthly",
            "one_time": "oneTime",
            "weekly": "weekly",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            daily: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.DailyScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            monthly: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            one_time: typing.Any = None,
            weekly: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The schedule the CIS scan configuration runs on.

            Each CIS scan configuration has exactly one type of schedule.

            :param daily: A daily schedule.
            :param monthly: A monthly schedule.
            :param one_time: A one time schedule.
            :param weekly: A weekly schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                # one_time: Any
                
                schedule_property = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.ScheduleProperty(
                    daily=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.DailyScheduleProperty(
                        start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                            time_of_day="timeOfDay",
                            time_zone="timeZone"
                        )
                    ),
                    monthly=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty(
                        day="day",
                        start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                            time_of_day="timeOfDay",
                            time_zone="timeZone"
                        )
                    ),
                    one_time=one_time,
                    weekly=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty(
                        days=["days"],
                        start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                            time_of_day="timeOfDay",
                            time_zone="timeZone"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__761cfabf43646c5b8ed01600f1e66426137799ca503c436edb3c3ebac745875a)
                check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
                check_type(argname="argument monthly", value=monthly, expected_type=type_hints["monthly"])
                check_type(argname="argument one_time", value=one_time, expected_type=type_hints["one_time"])
                check_type(argname="argument weekly", value=weekly, expected_type=type_hints["weekly"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily is not None:
                self._values["daily"] = daily
            if monthly is not None:
                self._values["monthly"] = monthly
            if one_time is not None:
                self._values["one_time"] = one_time
            if weekly is not None:
                self._values["weekly"] = weekly

        @builtins.property
        def daily(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.DailyScheduleProperty"]]:
            '''A daily schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-schedule.html#cfn-inspectorv2-cisscanconfiguration-schedule-daily
            '''
            result = self._values.get("daily")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.DailyScheduleProperty"]], result)

        @builtins.property
        def monthly(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty"]]:
            '''A monthly schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-schedule.html#cfn-inspectorv2-cisscanconfiguration-schedule-monthly
            '''
            result = self._values.get("monthly")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty"]], result)

        @builtins.property
        def one_time(self) -> typing.Any:
            '''A one time schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-schedule.html#cfn-inspectorv2-cisscanconfiguration-schedule-onetime
            '''
            result = self._values.get("one_time")
            return typing.cast(typing.Any, result)

        @builtins.property
        def weekly(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty"]]:
            '''A weekly schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-schedule.html#cfn-inspectorv2-cisscanconfiguration-schedule-weekly
            '''
            result = self._values.get("weekly")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin.TimeProperty",
        jsii_struct_bases=[],
        name_mapping={"time_of_day": "timeOfDay", "time_zone": "timeZone"},
    )
    class TimeProperty:
        def __init__(
            self,
            *,
            time_of_day: typing.Optional[builtins.str] = None,
            time_zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The time.

            :param time_of_day: The time of day in 24-hour format (00:00).
            :param time_zone: The timezone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-time.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                time_property = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                    time_of_day="timeOfDay",
                    time_zone="timeZone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d2b3572c201a389662a471cab926eba74beeea430702f0d3c0349518cd15f1d)
                check_type(argname="argument time_of_day", value=time_of_day, expected_type=type_hints["time_of_day"])
                check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if time_of_day is not None:
                self._values["time_of_day"] = time_of_day
            if time_zone is not None:
                self._values["time_zone"] = time_zone

        @builtins.property
        def time_of_day(self) -> typing.Optional[builtins.str]:
            '''The time of day in 24-hour format (00:00).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-time.html#cfn-inspectorv2-cisscanconfiguration-time-timeofday
            '''
            result = self._values.get("time_of_day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_zone(self) -> typing.Optional[builtins.str]:
            '''The timezone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-time.html#cfn-inspectorv2-cisscanconfiguration-time-timezone
            '''
            result = self._values.get("time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={"days": "days", "start_time": "startTime"},
    )
    class WeeklyScheduleProperty:
        def __init__(
            self,
            *,
            days: typing.Optional[typing.Sequence[builtins.str]] = None,
            start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCisScanConfigurationPropsMixin.TimeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A weekly schedule.

            :param days: The weekly schedule's days.
            :param start_time: The weekly schedule's start time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-weeklyschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                weekly_schedule_property = inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty(
                    days=["days"],
                    start_time=inspectorv2_mixins.CfnCisScanConfigurationPropsMixin.TimeProperty(
                        time_of_day="timeOfDay",
                        time_zone="timeZone"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7612736c17231f2264f0c43c06d05eed71b5a74d43bb0bf3de391fa2687a95b)
                check_type(argname="argument days", value=days, expected_type=type_hints["days"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days is not None:
                self._values["days"] = days
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def days(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The weekly schedule's days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-weeklyschedule.html#cfn-inspectorv2-cisscanconfiguration-weeklyschedule-days
            '''
            result = self._values.get("days")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.TimeProperty"]]:
            '''The weekly schedule's start time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-cisscanconfiguration-weeklyschedule.html#cfn-inspectorv2-cisscanconfiguration-weeklyschedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCisScanConfigurationPropsMixin.TimeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeeklyScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "create_integration_details": "createIntegrationDetails",
        "name": "name",
        "tags": "tags",
        "type": "type",
        "update_integration_details": "updateIntegrationDetails",
    },
)
class CfnCodeSecurityIntegrationMixinProps:
    def __init__(
        self,
        *,
        create_integration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
        update_integration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCodeSecurityIntegrationPropsMixin.

        :param create_integration_details: Contains details required to create a code security integration with a specific repository provider.
        :param name: The name of the code security integration.
        :param tags: The tags to apply to the code security integration.
        :param type: The type of repository provider for the integration.
        :param update_integration_details: The updated integration details specific to the repository provider type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
            
            cfn_code_security_integration_mixin_props = inspectorv2_mixins.CfnCodeSecurityIntegrationMixinProps(
                create_integration_details=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty(
                    gitlab_self_managed=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty(
                        access_token="accessToken",
                        instance_url="instanceUrl"
                    )
                ),
                name="name",
                tags={
                    "tags_key": "tags"
                },
                type="type",
                update_integration_details=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty(
                    github=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty(
                        code="code",
                        installation_id="installationId"
                    ),
                    gitlab_self_managed=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty(
                        auth_code="authCode"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f78c26f395f43d3e3464c91a103fff6a501b0a81cfbdee60ba93d58fef08bdbb)
            check_type(argname="argument create_integration_details", value=create_integration_details, expected_type=type_hints["create_integration_details"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument update_integration_details", value=update_integration_details, expected_type=type_hints["update_integration_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create_integration_details is not None:
            self._values["create_integration_details"] = create_integration_details
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if update_integration_details is not None:
            self._values["update_integration_details"] = update_integration_details

    @builtins.property
    def create_integration_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty"]]:
        '''Contains details required to create a code security integration with a specific repository provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html#cfn-inspectorv2-codesecurityintegration-createintegrationdetails
        '''
        result = self._values.get("create_integration_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the code security integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html#cfn-inspectorv2-codesecurityintegration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to apply to the code security integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html#cfn-inspectorv2-codesecurityintegration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of repository provider for the integration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html#cfn-inspectorv2-codesecurityintegration-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update_integration_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty"]]:
        '''The updated integration details specific to the repository provider type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html#cfn-inspectorv2-codesecurityintegration-updateintegrationdetails
        '''
        result = self._values.get("update_integration_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCodeSecurityIntegrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCodeSecurityIntegrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationPropsMixin",
):
    '''Creates a code security integration with a source code repository provider.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityintegration.html
    :cloudformationResource: AWS::InspectorV2::CodeSecurityIntegration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
        
        cfn_code_security_integration_props_mixin = inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin(inspectorv2_mixins.CfnCodeSecurityIntegrationMixinProps(
            create_integration_details=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty(
                gitlab_self_managed=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty(
                    access_token="accessToken",
                    instance_url="instanceUrl"
                )
            ),
            name="name",
            tags={
                "tags_key": "tags"
            },
            type="type",
            update_integration_details=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty(
                github=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty(
                    code="code",
                    installation_id="installationId"
                ),
                gitlab_self_managed=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty(
                    auth_code="authCode"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCodeSecurityIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::InspectorV2::CodeSecurityIntegration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a5eb078167c4f3e2cd1f1901f9c9456a8a9ef31599f97b796bd07714ac727a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__23db1e751010f4165f63c7713ddcbd9c9d160910d395e96772a3f82fd2d26e18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee26753e87a7d4f6838514ff3f3a2b1df62b98b966a73772aa32c58a48bfc48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCodeSecurityIntegrationMixinProps:
        return typing.cast(CfnCodeSecurityIntegrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"gitlab_self_managed": "gitlabSelfManaged"},
    )
    class CreateDetailsProperty:
        def __init__(
            self,
            *,
            gitlab_self_managed: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details required to create a code security integration with a specific repository provider.

            :param gitlab_self_managed: Details specific to creating an integration with a self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-createdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                create_details_property = inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty(
                    gitlab_self_managed=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty(
                        access_token="accessToken",
                        instance_url="instanceUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3339eb8a786ccdf616759a5ae6a05d84f09fddc9069d62d61ed257dd17bc443e)
                check_type(argname="argument gitlab_self_managed", value=gitlab_self_managed, expected_type=type_hints["gitlab_self_managed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gitlab_self_managed is not None:
                self._values["gitlab_self_managed"] = gitlab_self_managed

        @builtins.property
        def gitlab_self_managed(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty"]]:
            '''Details specific to creating an integration with a self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-createdetails.html#cfn-inspectorv2-codesecurityintegration-createdetails-gitlabselfmanaged
            '''
            result = self._values.get("gitlab_self_managed")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"access_token": "accessToken", "instance_url": "instanceUrl"},
    )
    class CreateGitLabSelfManagedIntegrationDetailProperty:
        def __init__(
            self,
            *,
            access_token: typing.Optional[builtins.str] = None,
            instance_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details required to create an integration with a self-managed GitLab instance.

            :param access_token: The personal access token used to authenticate with the self-managed GitLab instance.
            :param instance_url: The URL of the self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-creategitlabselfmanagedintegrationdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                create_git_lab_self_managed_integration_detail_property = inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty(
                    access_token="accessToken",
                    instance_url="instanceUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7de2758fedc4fc49bccbb1e609a1ea286e52f4646de8263967dfbe79ffa5b86a)
                check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
                check_type(argname="argument instance_url", value=instance_url, expected_type=type_hints["instance_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_token is not None:
                self._values["access_token"] = access_token
            if instance_url is not None:
                self._values["instance_url"] = instance_url

        @builtins.property
        def access_token(self) -> typing.Optional[builtins.str]:
            '''The personal access token used to authenticate with the self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-creategitlabselfmanagedintegrationdetail.html#cfn-inspectorv2-codesecurityintegration-creategitlabselfmanagedintegrationdetail-accesstoken
            '''
            result = self._values.get("access_token")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-creategitlabselfmanagedintegrationdetail.html#cfn-inspectorv2-codesecurityintegration-creategitlabselfmanagedintegrationdetail-instanceurl
            '''
            result = self._values.get("instance_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateGitLabSelfManagedIntegrationDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"github": "github", "gitlab_self_managed": "gitlabSelfManaged"},
    )
    class UpdateDetailsProperty:
        def __init__(
            self,
            *,
            github: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            gitlab_self_managed: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details required to update a code security integration with a specific repository provider.

            :param github: Details specific to updating an integration with GitHub.
            :param gitlab_self_managed: Details specific to updating an integration with a self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updatedetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                update_details_property = inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty(
                    github=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty(
                        code="code",
                        installation_id="installationId"
                    ),
                    gitlab_self_managed=inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty(
                        auth_code="authCode"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3d6759b33452d08af465ba75aab87c8b2eabf3ededf3c856badbca4acbcf906)
                check_type(argname="argument github", value=github, expected_type=type_hints["github"])
                check_type(argname="argument gitlab_self_managed", value=gitlab_self_managed, expected_type=type_hints["gitlab_self_managed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if github is not None:
                self._values["github"] = github
            if gitlab_self_managed is not None:
                self._values["gitlab_self_managed"] = gitlab_self_managed

        @builtins.property
        def github(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty"]]:
            '''Details specific to updating an integration with GitHub.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updatedetails.html#cfn-inspectorv2-codesecurityintegration-updatedetails-github
            '''
            result = self._values.get("github")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty"]], result)

        @builtins.property
        def gitlab_self_managed(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty"]]:
            '''Details specific to updating an integration with a self-managed GitLab instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updatedetails.html#cfn-inspectorv2-codesecurityintegration-updatedetails-gitlabselfmanaged
            '''
            result = self._values.get("gitlab_self_managed")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"code": "code", "installation_id": "installationId"},
    )
    class UpdateGitHubIntegrationDetailProperty:
        def __init__(
            self,
            *,
            code: typing.Optional[builtins.str] = None,
            installation_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details required to update an integration with GitHub.

            :param code: The authorization code received from GitHub to update the integration.
            :param installation_id: The installation ID of the GitHub App associated with the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updategithubintegrationdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                update_git_hub_integration_detail_property = inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty(
                    code="code",
                    installation_id="installationId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f531c58883a6ba418f30ea33a63e867e1178a70242d655762e6cbdabd0b7fde3)
                check_type(argname="argument code", value=code, expected_type=type_hints["code"])
                check_type(argname="argument installation_id", value=installation_id, expected_type=type_hints["installation_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if code is not None:
                self._values["code"] = code
            if installation_id is not None:
                self._values["installation_id"] = installation_id

        @builtins.property
        def code(self) -> typing.Optional[builtins.str]:
            '''The authorization code received from GitHub to update the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updategithubintegrationdetail.html#cfn-inspectorv2-codesecurityintegration-updategithubintegrationdetail-code
            '''
            result = self._values.get("code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def installation_id(self) -> typing.Optional[builtins.str]:
            '''The installation ID of the GitHub App associated with the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updategithubintegrationdetail.html#cfn-inspectorv2-codesecurityintegration-updategithubintegrationdetail-installationid
            '''
            result = self._values.get("installation_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateGitHubIntegrationDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"auth_code": "authCode"},
    )
    class UpdateGitLabSelfManagedIntegrationDetailProperty:
        def __init__(self, *, auth_code: typing.Optional[builtins.str] = None) -> None:
            '''Contains details required to update an integration with a self-managed GitLab instance.

            :param auth_code: The authorization code received from the self-managed GitLab instance to update the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updategitlabselfmanagedintegrationdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                update_git_lab_self_managed_integration_detail_property = inspectorv2_mixins.CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty(
                    auth_code="authCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0577f4bb9d7e4ac7f691d5618241895bc0a0373d9ba96e76a85b4a8478c1d66c)
                check_type(argname="argument auth_code", value=auth_code, expected_type=type_hints["auth_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auth_code is not None:
                self._values["auth_code"] = auth_code

        @builtins.property
        def auth_code(self) -> typing.Optional[builtins.str]:
            '''The authorization code received from the self-managed GitLab instance to update the integration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityintegration-updategitlabselfmanagedintegrationdetail.html#cfn-inspectorv2-codesecurityintegration-updategitlabselfmanagedintegrationdetail-authcode
            '''
            result = self._values.get("auth_code")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateGitLabSelfManagedIntegrationDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityScanConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration": "configuration",
        "level": "level",
        "name": "name",
        "scope_settings": "scopeSettings",
        "tags": "tags",
    },
)
class CfnCodeSecurityScanConfigurationMixinProps:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        level: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        scope_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnCodeSecurityScanConfigurationPropsMixin.

        :param configuration: The configuration settings for the code security scan.
        :param level: The security level for the scan configuration.
        :param name: The name of the scan configuration.
        :param scope_settings: The scope settings that define which repositories will be scanned.
        :param tags: The tags to apply to the scan configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
            
            cfn_code_security_scan_configuration_mixin_props = inspectorv2_mixins.CfnCodeSecurityScanConfigurationMixinProps(
                configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty(
                    continuous_integration_scan_configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty(
                        supported_events=["supportedEvents"]
                    ),
                    periodic_scan_configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty(
                        frequency="frequency",
                        frequency_expression="frequencyExpression"
                    ),
                    rule_set_categories=["ruleSetCategories"]
                ),
                level="level",
                name="name",
                scope_settings=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty(
                    project_selection_scope="projectSelectionScope"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8b7dae7cd52a0385c907ce4cbd74e7edce000d0f04e1e8b59aa58730609aeb)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument scope_settings", value=scope_settings, expected_type=type_hints["scope_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if level is not None:
            self._values["level"] = level
        if name is not None:
            self._values["name"] = name
        if scope_settings is not None:
            self._values["scope_settings"] = scope_settings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty"]]:
        '''The configuration settings for the code security scan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty"]], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''The security level for the scan configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-level
        '''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the scan configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty"]]:
        '''The scope settings that define which repositories will be scanned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-scopesettings
        '''
        result = self._values.get("scope_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags to apply to the scan configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCodeSecurityScanConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCodeSecurityScanConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityScanConfigurationPropsMixin",
):
    '''Creates a scan configuration for code security scanning.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-codesecurityscanconfiguration.html
    :cloudformationResource: AWS::InspectorV2::CodeSecurityScanConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
        
        cfn_code_security_scan_configuration_props_mixin = inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin(inspectorv2_mixins.CfnCodeSecurityScanConfigurationMixinProps(
            configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty(
                continuous_integration_scan_configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty(
                    supported_events=["supportedEvents"]
                ),
                periodic_scan_configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty(
                    frequency="frequency",
                    frequency_expression="frequencyExpression"
                ),
                rule_set_categories=["ruleSetCategories"]
            ),
            level="level",
            name="name",
            scope_settings=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty(
                project_selection_scope="projectSelectionScope"
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
        props: typing.Union[CfnCodeSecurityScanConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::InspectorV2::CodeSecurityScanConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c97e6852cd396fd2baf7fd6c8a46d4b09c018380236b72e7635bad8c4ecc4fa8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86148122165322d61fe870f94e115da64dcca0704605430a724696e286a01ec3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__600db8929126d68e905ed1ec088a1453f1c6ac9aecb2e4a26a2c6226bbf8f102)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCodeSecurityScanConfigurationMixinProps:
        return typing.cast(CfnCodeSecurityScanConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "continuous_integration_scan_configuration": "continuousIntegrationScanConfiguration",
            "periodic_scan_configuration": "periodicScanConfiguration",
            "rule_set_categories": "ruleSetCategories",
        },
    )
    class CodeSecurityScanConfigurationProperty:
        def __init__(
            self,
            *,
            continuous_integration_scan_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            periodic_scan_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_set_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains the configuration settings for code security scans.

            :param continuous_integration_scan_configuration: Configuration settings for continuous integration scans that run automatically when code changes are made.
            :param periodic_scan_configuration: Configuration settings for periodic scans that run on a scheduled basis.
            :param rule_set_categories: The categories of security rules to be applied during the scan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                code_security_scan_configuration_property = inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty(
                    continuous_integration_scan_configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty(
                        supported_events=["supportedEvents"]
                    ),
                    periodic_scan_configuration=inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty(
                        frequency="frequency",
                        frequency_expression="frequencyExpression"
                    ),
                    rule_set_categories=["ruleSetCategories"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bdce7edd020d2d226ff910c54462520ea8c495debba21d00fbcc1c059ee34398)
                check_type(argname="argument continuous_integration_scan_configuration", value=continuous_integration_scan_configuration, expected_type=type_hints["continuous_integration_scan_configuration"])
                check_type(argname="argument periodic_scan_configuration", value=periodic_scan_configuration, expected_type=type_hints["periodic_scan_configuration"])
                check_type(argname="argument rule_set_categories", value=rule_set_categories, expected_type=type_hints["rule_set_categories"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if continuous_integration_scan_configuration is not None:
                self._values["continuous_integration_scan_configuration"] = continuous_integration_scan_configuration
            if periodic_scan_configuration is not None:
                self._values["periodic_scan_configuration"] = periodic_scan_configuration
            if rule_set_categories is not None:
                self._values["rule_set_categories"] = rule_set_categories

        @builtins.property
        def continuous_integration_scan_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty"]]:
            '''Configuration settings for continuous integration scans that run automatically when code changes are made.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration-continuousintegrationscanconfiguration
            '''
            result = self._values.get("continuous_integration_scan_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty"]], result)

        @builtins.property
        def periodic_scan_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty"]]:
            '''Configuration settings for periodic scans that run on a scheduled basis.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration-periodicscanconfiguration
            '''
            result = self._values.get("periodic_scan_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty"]], result)

        @builtins.property
        def rule_set_categories(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The categories of security rules to be applied during the scan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-codesecurityscanconfiguration-rulesetcategories
            '''
            result = self._values.get("rule_set_categories")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeSecurityScanConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"supported_events": "supportedEvents"},
    )
    class ContinuousIntegrationScanConfigurationProperty:
        def __init__(
            self,
            *,
            supported_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration settings for continuous integration scans that run automatically when code changes are made.

            :param supported_events: The repository events that trigger continuous integration scans, such as pull requests or commits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-continuousintegrationscanconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                continuous_integration_scan_configuration_property = inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty(
                    supported_events=["supportedEvents"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6de6db31c0ba3b74dadece9648057b400be3252bfe37f3ffe379bda977e94dd3)
                check_type(argname="argument supported_events", value=supported_events, expected_type=type_hints["supported_events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if supported_events is not None:
                self._values["supported_events"] = supported_events

        @builtins.property
        def supported_events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The repository events that trigger continuous integration scans, such as pull requests or commits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-continuousintegrationscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-continuousintegrationscanconfiguration-supportedevents
            '''
            result = self._values.get("supported_events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContinuousIntegrationScanConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "frequency": "frequency",
            "frequency_expression": "frequencyExpression",
        },
    )
    class PeriodicScanConfigurationProperty:
        def __init__(
            self,
            *,
            frequency: typing.Optional[builtins.str] = None,
            frequency_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for periodic scans that run on a scheduled basis.

            :param frequency: The frequency at which periodic scans are performed (such as weekly or monthly). If you don't provide the ``frequencyExpression`` Amazon Inspector chooses day for the scan to run. If you provide the ``frequencyExpression`` , the schedule must match the specified ``frequency`` .
            :param frequency_expression: The schedule expression for periodic scans, in cron format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-periodicscanconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                periodic_scan_configuration_property = inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty(
                    frequency="frequency",
                    frequency_expression="frequencyExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4106ffd38fef7a9d9e5e00399223be0b6a2006cbe6619baf92482915bd5ad820)
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
                check_type(argname="argument frequency_expression", value=frequency_expression, expected_type=type_hints["frequency_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if frequency is not None:
                self._values["frequency"] = frequency
            if frequency_expression is not None:
                self._values["frequency_expression"] = frequency_expression

        @builtins.property
        def frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency at which periodic scans are performed (such as weekly or monthly).

            If you don't provide the ``frequencyExpression`` Amazon Inspector chooses day for the scan to run. If you provide the ``frequencyExpression`` , the schedule must match the specified ``frequency`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-periodicscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-periodicscanconfiguration-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def frequency_expression(self) -> typing.Optional[builtins.str]:
            '''The schedule expression for periodic scans, in cron format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-periodicscanconfiguration.html#cfn-inspectorv2-codesecurityscanconfiguration-periodicscanconfiguration-frequencyexpression
            '''
            result = self._values.get("frequency_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PeriodicScanConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"project_selection_scope": "projectSelectionScope"},
    )
    class ScopeSettingsProperty:
        def __init__(
            self,
            *,
            project_selection_scope: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The scope settings that define which repositories will be scanned.

            If the ``ScopeSetting`` parameter is ``ALL`` the scan configuration applies to all existing and future projects imported into Amazon Inspector .

            :param project_selection_scope: The scope of projects to be selected for scanning within the integrated repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-scopesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                scope_settings_property = inspectorv2_mixins.CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty(
                    project_selection_scope="projectSelectionScope"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f908214c3f4bb4d7fba041925621e0840a7f461a19e2bcfc9434b567039ffd6e)
                check_type(argname="argument project_selection_scope", value=project_selection_scope, expected_type=type_hints["project_selection_scope"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if project_selection_scope is not None:
                self._values["project_selection_scope"] = project_selection_scope

        @builtins.property
        def project_selection_scope(self) -> typing.Optional[builtins.str]:
            '''The scope of projects to be selected for scanning within the integrated repositories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-codesecurityscanconfiguration-scopesettings.html#cfn-inspectorv2-codesecurityscanconfiguration-scopesettings-projectselectionscope
            '''
            result = self._values.get("project_selection_scope")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "filter_action": "filterAction",
        "filter_criteria": "filterCriteria",
        "name": "name",
        "tags": "tags",
    },
)
class CfnFilterMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        filter_action: typing.Optional[builtins.str] = None,
        filter_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.FilterCriteriaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnFilterPropsMixin.

        :param description: A description of the filter.
        :param filter_action: The action that is to be applied to the findings that match the filter.
        :param filter_criteria: Details on the filter criteria associated with this filter.
        :param name: The name of the filter.
        :param tags: The tags attached to the filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
            
            cfn_filter_mixin_props = inspectorv2_mixins.CfnFilterMixinProps(
                description="description",
                filter_action="filterAction",
                filter_criteria=inspectorv2_mixins.CfnFilterPropsMixin.FilterCriteriaProperty(
                    aws_account_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    code_vulnerability_detector_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    code_vulnerability_detector_tags=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    code_vulnerability_file_path=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    component_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    component_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ec2_instance_image_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ec2_instance_subnet_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ec2_instance_vpc_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_architecture=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_hash=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_pushed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    ecr_image_registry=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_repository_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_tags=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    epss_score=[inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                        lower_inclusive=123,
                        upper_inclusive=123
                    )],
                    exploit_available=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_arn=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_status=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    first_observed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    fix_available=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    inspector_score=[inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                        lower_inclusive=123,
                        upper_inclusive=123
                    )],
                    lambda_function_execution_role_arn=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    lambda_function_last_modified_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    lambda_function_layers=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    lambda_function_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    lambda_function_runtime=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    last_observed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    network_protocol=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    port_range=[inspectorv2_mixins.CfnFilterPropsMixin.PortRangeFilterProperty(
                        begin_inclusive=123,
                        end_inclusive=123
                    )],
                    related_vulnerabilities=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_tags=[inspectorv2_mixins.CfnFilterPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    severity=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    title=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    updated_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    vendor_severity=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerability_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerability_source=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerable_packages=[inspectorv2_mixins.CfnFilterPropsMixin.PackageFilterProperty(
                        architecture=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        epoch=inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                            lower_inclusive=123,
                            upper_inclusive=123
                        ),
                        file_path=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        name=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        release=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        source_lambda_layer_arn=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        source_layer_hash=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        version=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        )
                    )]
                ),
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9890a2a32132eb870f72a91bd3a4bd9e48239f218a138171c6912e39a69a6e49)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument filter_action", value=filter_action, expected_type=type_hints["filter_action"])
            check_type(argname="argument filter_criteria", value=filter_criteria, expected_type=type_hints["filter_criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if filter_action is not None:
            self._values["filter_action"] = filter_action
        if filter_criteria is not None:
            self._values["filter_criteria"] = filter_criteria
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html#cfn-inspectorv2-filter-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_action(self) -> typing.Optional[builtins.str]:
        '''The action that is to be applied to the findings that match the filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html#cfn-inspectorv2-filter-filteraction
        '''
        result = self._values.get("filter_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def filter_criteria(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.FilterCriteriaProperty"]]:
        '''Details on the filter criteria associated with this filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html#cfn-inspectorv2-filter-filtercriteria
        '''
        result = self._values.get("filter_criteria")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.FilterCriteriaProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html#cfn-inspectorv2-filter-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags attached to the filter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html#cfn-inspectorv2-filter-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFilterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFilterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin",
):
    '''Details about a filter.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspectorv2-filter.html
    :cloudformationResource: AWS::InspectorV2::Filter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
        
        cfn_filter_props_mixin = inspectorv2_mixins.CfnFilterPropsMixin(inspectorv2_mixins.CfnFilterMixinProps(
            description="description",
            filter_action="filterAction",
            filter_criteria=inspectorv2_mixins.CfnFilterPropsMixin.FilterCriteriaProperty(
                aws_account_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                code_vulnerability_detector_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                code_vulnerability_detector_tags=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                code_vulnerability_file_path=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                component_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                component_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ec2_instance_image_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ec2_instance_subnet_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ec2_instance_vpc_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ecr_image_architecture=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ecr_image_hash=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ecr_image_pushed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                    end_inclusive=123,
                    start_inclusive=123
                )],
                ecr_image_registry=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ecr_image_repository_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                ecr_image_tags=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                epss_score=[inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                    lower_inclusive=123,
                    upper_inclusive=123
                )],
                exploit_available=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_arn=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_status=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                finding_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                first_observed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                    end_inclusive=123,
                    start_inclusive=123
                )],
                fix_available=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                inspector_score=[inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                    lower_inclusive=123,
                    upper_inclusive=123
                )],
                lambda_function_execution_role_arn=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                lambda_function_last_modified_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                    end_inclusive=123,
                    start_inclusive=123
                )],
                lambda_function_layers=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                lambda_function_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                lambda_function_runtime=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                last_observed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                    end_inclusive=123,
                    start_inclusive=123
                )],
                network_protocol=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                port_range=[inspectorv2_mixins.CfnFilterPropsMixin.PortRangeFilterProperty(
                    begin_inclusive=123,
                    end_inclusive=123
                )],
                related_vulnerabilities=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                resource_tags=[inspectorv2_mixins.CfnFilterPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )],
                resource_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                severity=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                title=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                updated_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                    end_inclusive=123,
                    start_inclusive=123
                )],
                vendor_severity=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                vulnerability_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                vulnerability_source=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )],
                vulnerable_packages=[inspectorv2_mixins.CfnFilterPropsMixin.PackageFilterProperty(
                    architecture=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    epoch=inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                        lower_inclusive=123,
                        upper_inclusive=123
                    ),
                    file_path=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    name=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    release=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    source_lambda_layer_arn=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    source_layer_hash=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    version=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )
                )]
            ),
            name="name",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::InspectorV2::Filter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a511a9fae2a2d00c9c9840ad961c580dcee340a7af222777f334762664b911)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bd535c07e3267b87805ae8beaa019f21e81eb44774ca5baed80a266204984ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bff16b99849a31e15683edbb9b4668273b0890730613502919c4ac2cea06b9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFilterMixinProps:
        return typing.cast(CfnFilterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.DateFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_inclusive": "endInclusive",
            "start_inclusive": "startInclusive",
        },
    )
    class DateFilterProperty:
        def __init__(
            self,
            *,
            end_inclusive: typing.Optional[jsii.Number] = None,
            start_inclusive: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains details on the time range used to filter findings.

            :param end_inclusive: A timestamp representing the end of the time period filtered on.
            :param start_inclusive: A timestamp representing the start of the time period filtered on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-datefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                date_filter_property = inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                    end_inclusive=123,
                    start_inclusive=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92f0cf2bb729f9a0a49856bc44659890ce0a00b44110ca23312f444d20dfc54a)
                check_type(argname="argument end_inclusive", value=end_inclusive, expected_type=type_hints["end_inclusive"])
                check_type(argname="argument start_inclusive", value=start_inclusive, expected_type=type_hints["start_inclusive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_inclusive is not None:
                self._values["end_inclusive"] = end_inclusive
            if start_inclusive is not None:
                self._values["start_inclusive"] = start_inclusive

        @builtins.property
        def end_inclusive(self) -> typing.Optional[jsii.Number]:
            '''A timestamp representing the end of the time period filtered on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-datefilter.html#cfn-inspectorv2-filter-datefilter-endinclusive
            '''
            result = self._values.get("end_inclusive")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def start_inclusive(self) -> typing.Optional[jsii.Number]:
            '''A timestamp representing the start of the time period filtered on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-datefilter.html#cfn-inspectorv2-filter-datefilter-startinclusive
            '''
            result = self._values.get("start_inclusive")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DateFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.FilterCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_account_id": "awsAccountId",
            "code_vulnerability_detector_name": "codeVulnerabilityDetectorName",
            "code_vulnerability_detector_tags": "codeVulnerabilityDetectorTags",
            "code_vulnerability_file_path": "codeVulnerabilityFilePath",
            "component_id": "componentId",
            "component_type": "componentType",
            "ec2_instance_image_id": "ec2InstanceImageId",
            "ec2_instance_subnet_id": "ec2InstanceSubnetId",
            "ec2_instance_vpc_id": "ec2InstanceVpcId",
            "ecr_image_architecture": "ecrImageArchitecture",
            "ecr_image_hash": "ecrImageHash",
            "ecr_image_pushed_at": "ecrImagePushedAt",
            "ecr_image_registry": "ecrImageRegistry",
            "ecr_image_repository_name": "ecrImageRepositoryName",
            "ecr_image_tags": "ecrImageTags",
            "epss_score": "epssScore",
            "exploit_available": "exploitAvailable",
            "finding_arn": "findingArn",
            "finding_status": "findingStatus",
            "finding_type": "findingType",
            "first_observed_at": "firstObservedAt",
            "fix_available": "fixAvailable",
            "inspector_score": "inspectorScore",
            "lambda_function_execution_role_arn": "lambdaFunctionExecutionRoleArn",
            "lambda_function_last_modified_at": "lambdaFunctionLastModifiedAt",
            "lambda_function_layers": "lambdaFunctionLayers",
            "lambda_function_name": "lambdaFunctionName",
            "lambda_function_runtime": "lambdaFunctionRuntime",
            "last_observed_at": "lastObservedAt",
            "network_protocol": "networkProtocol",
            "port_range": "portRange",
            "related_vulnerabilities": "relatedVulnerabilities",
            "resource_id": "resourceId",
            "resource_tags": "resourceTags",
            "resource_type": "resourceType",
            "severity": "severity",
            "title": "title",
            "updated_at": "updatedAt",
            "vendor_severity": "vendorSeverity",
            "vulnerability_id": "vulnerabilityId",
            "vulnerability_source": "vulnerabilitySource",
            "vulnerable_packages": "vulnerablePackages",
        },
    )
    class FilterCriteriaProperty:
        def __init__(
            self,
            *,
            aws_account_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            code_vulnerability_detector_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            code_vulnerability_detector_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            code_vulnerability_file_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            component_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            component_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ec2_instance_image_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ec2_instance_subnet_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ec2_instance_vpc_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ecr_image_architecture: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ecr_image_hash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ecr_image_pushed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ecr_image_registry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ecr_image_repository_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ecr_image_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            epss_score: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            exploit_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            finding_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            first_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            fix_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            inspector_score: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            lambda_function_execution_role_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            lambda_function_last_modified_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            lambda_function_layers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            lambda_function_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            lambda_function_runtime: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.PortRangeFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            related_vulnerabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.MapFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            severity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            title: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.DateFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vendor_severity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vulnerability_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vulnerability_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            vulnerable_packages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.PackageFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Details on the criteria used to define the filter.

            :param aws_account_id: Details of the AWS account IDs used to filter findings.
            :param code_vulnerability_detector_name: 
            :param code_vulnerability_detector_tags: 
            :param code_vulnerability_file_path: 
            :param component_id: Details of the component IDs used to filter findings.
            :param component_type: Details of the component types used to filter findings.
            :param ec2_instance_image_id: Details of the Amazon EC2 instance image IDs used to filter findings.
            :param ec2_instance_subnet_id: Details of the Amazon EC2 instance subnet IDs used to filter findings.
            :param ec2_instance_vpc_id: Details of the Amazon EC2 instance VPC IDs used to filter findings.
            :param ecr_image_architecture: Details of the Amazon ECR image architecture types used to filter findings.
            :param ecr_image_hash: Details of the Amazon ECR image hashes used to filter findings.
            :param ecr_image_pushed_at: Details on the Amazon ECR image push date and time used to filter findings.
            :param ecr_image_registry: Details on the Amazon ECR registry used to filter findings.
            :param ecr_image_repository_name: Details on the name of the Amazon ECR repository used to filter findings.
            :param ecr_image_tags: The tags attached to the Amazon ECR container image.
            :param epss_score: 
            :param exploit_available: 
            :param finding_arn: Details on the finding ARNs used to filter findings.
            :param finding_status: Details on the finding status types used to filter findings.
            :param finding_type: Details on the finding types used to filter findings.
            :param first_observed_at: Details on the date and time a finding was first seen used to filter findings.
            :param fix_available: 
            :param inspector_score: The Amazon Inspector score to filter on.
            :param lambda_function_execution_role_arn: 
            :param lambda_function_last_modified_at: 
            :param lambda_function_layers: 
            :param lambda_function_name: 
            :param lambda_function_runtime: 
            :param last_observed_at: Details on the date and time a finding was last seen used to filter findings.
            :param network_protocol: Details on network protocol used to filter findings.
            :param port_range: Details on the port ranges used to filter findings.
            :param related_vulnerabilities: Details on the related vulnerabilities used to filter findings.
            :param resource_id: Details on the resource IDs used to filter findings.
            :param resource_tags: Details on the resource tags used to filter findings.
            :param resource_type: Details on the resource types used to filter findings.
            :param severity: Details on the severity used to filter findings.
            :param title: Details on the finding title used to filter findings.
            :param updated_at: Details on the date and time a finding was last updated at used to filter findings.
            :param vendor_severity: Details on the vendor severity used to filter findings.
            :param vulnerability_id: Details on the vulnerability ID used to filter findings.
            :param vulnerability_source: Details on the vulnerability score to filter findings by.
            :param vulnerable_packages: Details on the vulnerable packages used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                filter_criteria_property = inspectorv2_mixins.CfnFilterPropsMixin.FilterCriteriaProperty(
                    aws_account_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    code_vulnerability_detector_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    code_vulnerability_detector_tags=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    code_vulnerability_file_path=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    component_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    component_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ec2_instance_image_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ec2_instance_subnet_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ec2_instance_vpc_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_architecture=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_hash=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_pushed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    ecr_image_registry=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_repository_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    ecr_image_tags=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    epss_score=[inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                        lower_inclusive=123,
                        upper_inclusive=123
                    )],
                    exploit_available=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_arn=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_status=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    finding_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    first_observed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    fix_available=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    inspector_score=[inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                        lower_inclusive=123,
                        upper_inclusive=123
                    )],
                    lambda_function_execution_role_arn=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    lambda_function_last_modified_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    lambda_function_layers=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    lambda_function_name=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    lambda_function_runtime=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    last_observed_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    network_protocol=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    port_range=[inspectorv2_mixins.CfnFilterPropsMixin.PortRangeFilterProperty(
                        begin_inclusive=123,
                        end_inclusive=123
                    )],
                    related_vulnerabilities=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    resource_tags=[inspectorv2_mixins.CfnFilterPropsMixin.MapFilterProperty(
                        comparison="comparison",
                        key="key",
                        value="value"
                    )],
                    resource_type=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    severity=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    title=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    updated_at=[inspectorv2_mixins.CfnFilterPropsMixin.DateFilterProperty(
                        end_inclusive=123,
                        start_inclusive=123
                    )],
                    vendor_severity=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerability_id=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerability_source=[inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )],
                    vulnerable_packages=[inspectorv2_mixins.CfnFilterPropsMixin.PackageFilterProperty(
                        architecture=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        epoch=inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                            lower_inclusive=123,
                            upper_inclusive=123
                        ),
                        file_path=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        name=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        release=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        source_lambda_layer_arn=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        source_layer_hash=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        ),
                        version=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                            comparison="comparison",
                            value="value"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c1510b2f7cac2420ca2a992bb2bc390c1b6516dfbda711282aa8a9818aa69235)
                check_type(argname="argument aws_account_id", value=aws_account_id, expected_type=type_hints["aws_account_id"])
                check_type(argname="argument code_vulnerability_detector_name", value=code_vulnerability_detector_name, expected_type=type_hints["code_vulnerability_detector_name"])
                check_type(argname="argument code_vulnerability_detector_tags", value=code_vulnerability_detector_tags, expected_type=type_hints["code_vulnerability_detector_tags"])
                check_type(argname="argument code_vulnerability_file_path", value=code_vulnerability_file_path, expected_type=type_hints["code_vulnerability_file_path"])
                check_type(argname="argument component_id", value=component_id, expected_type=type_hints["component_id"])
                check_type(argname="argument component_type", value=component_type, expected_type=type_hints["component_type"])
                check_type(argname="argument ec2_instance_image_id", value=ec2_instance_image_id, expected_type=type_hints["ec2_instance_image_id"])
                check_type(argname="argument ec2_instance_subnet_id", value=ec2_instance_subnet_id, expected_type=type_hints["ec2_instance_subnet_id"])
                check_type(argname="argument ec2_instance_vpc_id", value=ec2_instance_vpc_id, expected_type=type_hints["ec2_instance_vpc_id"])
                check_type(argname="argument ecr_image_architecture", value=ecr_image_architecture, expected_type=type_hints["ecr_image_architecture"])
                check_type(argname="argument ecr_image_hash", value=ecr_image_hash, expected_type=type_hints["ecr_image_hash"])
                check_type(argname="argument ecr_image_pushed_at", value=ecr_image_pushed_at, expected_type=type_hints["ecr_image_pushed_at"])
                check_type(argname="argument ecr_image_registry", value=ecr_image_registry, expected_type=type_hints["ecr_image_registry"])
                check_type(argname="argument ecr_image_repository_name", value=ecr_image_repository_name, expected_type=type_hints["ecr_image_repository_name"])
                check_type(argname="argument ecr_image_tags", value=ecr_image_tags, expected_type=type_hints["ecr_image_tags"])
                check_type(argname="argument epss_score", value=epss_score, expected_type=type_hints["epss_score"])
                check_type(argname="argument exploit_available", value=exploit_available, expected_type=type_hints["exploit_available"])
                check_type(argname="argument finding_arn", value=finding_arn, expected_type=type_hints["finding_arn"])
                check_type(argname="argument finding_status", value=finding_status, expected_type=type_hints["finding_status"])
                check_type(argname="argument finding_type", value=finding_type, expected_type=type_hints["finding_type"])
                check_type(argname="argument first_observed_at", value=first_observed_at, expected_type=type_hints["first_observed_at"])
                check_type(argname="argument fix_available", value=fix_available, expected_type=type_hints["fix_available"])
                check_type(argname="argument inspector_score", value=inspector_score, expected_type=type_hints["inspector_score"])
                check_type(argname="argument lambda_function_execution_role_arn", value=lambda_function_execution_role_arn, expected_type=type_hints["lambda_function_execution_role_arn"])
                check_type(argname="argument lambda_function_last_modified_at", value=lambda_function_last_modified_at, expected_type=type_hints["lambda_function_last_modified_at"])
                check_type(argname="argument lambda_function_layers", value=lambda_function_layers, expected_type=type_hints["lambda_function_layers"])
                check_type(argname="argument lambda_function_name", value=lambda_function_name, expected_type=type_hints["lambda_function_name"])
                check_type(argname="argument lambda_function_runtime", value=lambda_function_runtime, expected_type=type_hints["lambda_function_runtime"])
                check_type(argname="argument last_observed_at", value=last_observed_at, expected_type=type_hints["last_observed_at"])
                check_type(argname="argument network_protocol", value=network_protocol, expected_type=type_hints["network_protocol"])
                check_type(argname="argument port_range", value=port_range, expected_type=type_hints["port_range"])
                check_type(argname="argument related_vulnerabilities", value=related_vulnerabilities, expected_type=type_hints["related_vulnerabilities"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument updated_at", value=updated_at, expected_type=type_hints["updated_at"])
                check_type(argname="argument vendor_severity", value=vendor_severity, expected_type=type_hints["vendor_severity"])
                check_type(argname="argument vulnerability_id", value=vulnerability_id, expected_type=type_hints["vulnerability_id"])
                check_type(argname="argument vulnerability_source", value=vulnerability_source, expected_type=type_hints["vulnerability_source"])
                check_type(argname="argument vulnerable_packages", value=vulnerable_packages, expected_type=type_hints["vulnerable_packages"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_account_id is not None:
                self._values["aws_account_id"] = aws_account_id
            if code_vulnerability_detector_name is not None:
                self._values["code_vulnerability_detector_name"] = code_vulnerability_detector_name
            if code_vulnerability_detector_tags is not None:
                self._values["code_vulnerability_detector_tags"] = code_vulnerability_detector_tags
            if code_vulnerability_file_path is not None:
                self._values["code_vulnerability_file_path"] = code_vulnerability_file_path
            if component_id is not None:
                self._values["component_id"] = component_id
            if component_type is not None:
                self._values["component_type"] = component_type
            if ec2_instance_image_id is not None:
                self._values["ec2_instance_image_id"] = ec2_instance_image_id
            if ec2_instance_subnet_id is not None:
                self._values["ec2_instance_subnet_id"] = ec2_instance_subnet_id
            if ec2_instance_vpc_id is not None:
                self._values["ec2_instance_vpc_id"] = ec2_instance_vpc_id
            if ecr_image_architecture is not None:
                self._values["ecr_image_architecture"] = ecr_image_architecture
            if ecr_image_hash is not None:
                self._values["ecr_image_hash"] = ecr_image_hash
            if ecr_image_pushed_at is not None:
                self._values["ecr_image_pushed_at"] = ecr_image_pushed_at
            if ecr_image_registry is not None:
                self._values["ecr_image_registry"] = ecr_image_registry
            if ecr_image_repository_name is not None:
                self._values["ecr_image_repository_name"] = ecr_image_repository_name
            if ecr_image_tags is not None:
                self._values["ecr_image_tags"] = ecr_image_tags
            if epss_score is not None:
                self._values["epss_score"] = epss_score
            if exploit_available is not None:
                self._values["exploit_available"] = exploit_available
            if finding_arn is not None:
                self._values["finding_arn"] = finding_arn
            if finding_status is not None:
                self._values["finding_status"] = finding_status
            if finding_type is not None:
                self._values["finding_type"] = finding_type
            if first_observed_at is not None:
                self._values["first_observed_at"] = first_observed_at
            if fix_available is not None:
                self._values["fix_available"] = fix_available
            if inspector_score is not None:
                self._values["inspector_score"] = inspector_score
            if lambda_function_execution_role_arn is not None:
                self._values["lambda_function_execution_role_arn"] = lambda_function_execution_role_arn
            if lambda_function_last_modified_at is not None:
                self._values["lambda_function_last_modified_at"] = lambda_function_last_modified_at
            if lambda_function_layers is not None:
                self._values["lambda_function_layers"] = lambda_function_layers
            if lambda_function_name is not None:
                self._values["lambda_function_name"] = lambda_function_name
            if lambda_function_runtime is not None:
                self._values["lambda_function_runtime"] = lambda_function_runtime
            if last_observed_at is not None:
                self._values["last_observed_at"] = last_observed_at
            if network_protocol is not None:
                self._values["network_protocol"] = network_protocol
            if port_range is not None:
                self._values["port_range"] = port_range
            if related_vulnerabilities is not None:
                self._values["related_vulnerabilities"] = related_vulnerabilities
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags
            if resource_type is not None:
                self._values["resource_type"] = resource_type
            if severity is not None:
                self._values["severity"] = severity
            if title is not None:
                self._values["title"] = title
            if updated_at is not None:
                self._values["updated_at"] = updated_at
            if vendor_severity is not None:
                self._values["vendor_severity"] = vendor_severity
            if vulnerability_id is not None:
                self._values["vulnerability_id"] = vulnerability_id
            if vulnerability_source is not None:
                self._values["vulnerability_source"] = vulnerability_source
            if vulnerable_packages is not None:
                self._values["vulnerable_packages"] = vulnerable_packages

        @builtins.property
        def aws_account_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the AWS account IDs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-awsaccountid
            '''
            result = self._values.get("aws_account_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def code_vulnerability_detector_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-codevulnerabilitydetectorname
            '''
            result = self._values.get("code_vulnerability_detector_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def code_vulnerability_detector_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-codevulnerabilitydetectortags
            '''
            result = self._values.get("code_vulnerability_detector_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def code_vulnerability_file_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-codevulnerabilityfilepath
            '''
            result = self._values.get("code_vulnerability_file_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def component_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the component IDs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-componentid
            '''
            result = self._values.get("component_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def component_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the component types used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-componenttype
            '''
            result = self._values.get("component_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ec2_instance_image_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the Amazon EC2 instance image IDs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ec2instanceimageid
            '''
            result = self._values.get("ec2_instance_image_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ec2_instance_subnet_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the Amazon EC2 instance subnet IDs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ec2instancesubnetid
            '''
            result = self._values.get("ec2_instance_subnet_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ec2_instance_vpc_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the Amazon EC2 instance VPC IDs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ec2instancevpcid
            '''
            result = self._values.get("ec2_instance_vpc_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ecr_image_architecture(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the Amazon ECR image architecture types used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ecrimagearchitecture
            '''
            result = self._values.get("ecr_image_architecture")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ecr_image_hash(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details of the Amazon ECR image hashes used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ecrimagehash
            '''
            result = self._values.get("ecr_image_hash")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ecr_image_pushed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]]:
            '''Details on the Amazon ECR image push date and time used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ecrimagepushedat
            '''
            result = self._values.get("ecr_image_pushed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def ecr_image_registry(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the Amazon ECR registry used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ecrimageregistry
            '''
            result = self._values.get("ecr_image_registry")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ecr_image_repository_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the name of the Amazon ECR repository used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ecrimagerepositoryname
            '''
            result = self._values.get("ecr_image_repository_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def ecr_image_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''The tags attached to the Amazon ECR container image.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-ecrimagetags
            '''
            result = self._values.get("ecr_image_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def epss_score(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.NumberFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-epssscore
            '''
            result = self._values.get("epss_score")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def exploit_available(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-exploitavailable
            '''
            result = self._values.get("exploit_available")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the finding ARNs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-findingarn
            '''
            result = self._values.get("finding_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_status(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the finding status types used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-findingstatus
            '''
            result = self._values.get("finding_status")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def finding_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the finding types used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-findingtype
            '''
            result = self._values.get("finding_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def first_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]]:
            '''Details on the date and time a finding was first seen used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-firstobservedat
            '''
            result = self._values.get("first_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def fix_available(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-fixavailable
            '''
            result = self._values.get("fix_available")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def inspector_score(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.NumberFilterProperty"]]]]:
            '''The Amazon Inspector score to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-inspectorscore
            '''
            result = self._values.get("inspector_score")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.NumberFilterProperty"]]]], result)

        @builtins.property
        def lambda_function_execution_role_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-lambdafunctionexecutionrolearn
            '''
            result = self._values.get("lambda_function_execution_role_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def lambda_function_last_modified_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-lambdafunctionlastmodifiedat
            '''
            result = self._values.get("lambda_function_last_modified_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def lambda_function_layers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-lambdafunctionlayers
            '''
            result = self._values.get("lambda_function_layers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def lambda_function_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-lambdafunctionname
            '''
            result = self._values.get("lambda_function_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def lambda_function_runtime(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-lambdafunctionruntime
            '''
            result = self._values.get("lambda_function_runtime")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def last_observed_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]]:
            '''Details on the date and time a finding was last seen used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-lastobservedat
            '''
            result = self._values.get("last_observed_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def network_protocol(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on network protocol used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-networkprotocol
            '''
            result = self._values.get("network_protocol")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def port_range(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.PortRangeFilterProperty"]]]]:
            '''Details on the port ranges used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-portrange
            '''
            result = self._values.get("port_range")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.PortRangeFilterProperty"]]]], result)

        @builtins.property
        def related_vulnerabilities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the related vulnerabilities used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-relatedvulnerabilities
            '''
            result = self._values.get("related_vulnerabilities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the resource IDs used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.MapFilterProperty"]]]]:
            '''Details on the resource tags used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.MapFilterProperty"]]]], result)

        @builtins.property
        def resource_type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the resource types used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def severity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the severity used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-severity
            '''
            result = self._values.get("severity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def title(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the finding title used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def updated_at(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]]:
            '''Details on the date and time a finding was last updated at used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-updatedat
            '''
            result = self._values.get("updated_at")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.DateFilterProperty"]]]], result)

        @builtins.property
        def vendor_severity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the vendor severity used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-vendorseverity
            '''
            result = self._values.get("vendor_severity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def vulnerability_id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the vulnerability ID used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-vulnerabilityid
            '''
            result = self._values.get("vulnerability_id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def vulnerability_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]]:
            '''Details on the vulnerability score to filter findings by.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-vulnerabilitysource
            '''
            result = self._values.get("vulnerability_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]]], result)

        @builtins.property
        def vulnerable_packages(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.PackageFilterProperty"]]]]:
            '''Details on the vulnerable packages used to filter findings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-filtercriteria.html#cfn-inspectorv2-filter-filtercriteria-vulnerablepackages
            '''
            result = self._values.get("vulnerable_packages")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.PackageFilterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.MapFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "key": "key", "value": "value"},
    )
    class MapFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that describes details of a map filter.

            :param comparison: The operator to use when comparing values in the filter.
            :param key: The tag key used in the filter.
            :param value: The tag value used in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-mapfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                map_filter_property = inspectorv2_mixins.CfnFilterPropsMixin.MapFilterProperty(
                    comparison="comparison",
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3718450f6e139baddd6d6b9cd286e133dcf4b86ce6ef4083fd1c9e83b417f4f3)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The operator to use when comparing values in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-mapfilter.html#cfn-inspectorv2-filter-mapfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key used in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-mapfilter.html#cfn-inspectorv2-filter-mapfilter-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value used in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-mapfilter.html#cfn-inspectorv2-filter-mapfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MapFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.NumberFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "lower_inclusive": "lowerInclusive",
            "upper_inclusive": "upperInclusive",
        },
    )
    class NumberFilterProperty:
        def __init__(
            self,
            *,
            lower_inclusive: typing.Optional[jsii.Number] = None,
            upper_inclusive: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that describes the details of a number filter.

            :param lower_inclusive: The lowest number to be included in the filter.
            :param upper_inclusive: The highest number to be included in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-numberfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                number_filter_property = inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                    lower_inclusive=123,
                    upper_inclusive=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce313c106bfc6b1184d6176b2bffa5c215b7437b709cd7cfe2e6f69bdb33b912)
                check_type(argname="argument lower_inclusive", value=lower_inclusive, expected_type=type_hints["lower_inclusive"])
                check_type(argname="argument upper_inclusive", value=upper_inclusive, expected_type=type_hints["upper_inclusive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if lower_inclusive is not None:
                self._values["lower_inclusive"] = lower_inclusive
            if upper_inclusive is not None:
                self._values["upper_inclusive"] = upper_inclusive

        @builtins.property
        def lower_inclusive(self) -> typing.Optional[jsii.Number]:
            '''The lowest number to be included in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-numberfilter.html#cfn-inspectorv2-filter-numberfilter-lowerinclusive
            '''
            result = self._values.get("lower_inclusive")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def upper_inclusive(self) -> typing.Optional[jsii.Number]:
            '''The highest number to be included in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-numberfilter.html#cfn-inspectorv2-filter-numberfilter-upperinclusive
            '''
            result = self._values.get("upper_inclusive")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumberFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.PackageFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "architecture": "architecture",
            "epoch": "epoch",
            "file_path": "filePath",
            "name": "name",
            "release": "release",
            "source_lambda_layer_arn": "sourceLambdaLayerArn",
            "source_layer_hash": "sourceLayerHash",
            "version": "version",
        },
    )
    class PackageFilterProperty:
        def __init__(
            self,
            *,
            architecture: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            epoch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.NumberFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            file_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            release: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_lambda_layer_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_layer_hash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFilterPropsMixin.StringFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information on the details of a package filter.

            :param architecture: An object that contains details on the package architecture type to filter on.
            :param epoch: An object that contains details on the package epoch to filter on.
            :param file_path: 
            :param name: An object that contains details on the name of the package to filter on.
            :param release: An object that contains details on the package release to filter on.
            :param source_lambda_layer_arn: 
            :param source_layer_hash: An object that contains details on the source layer hash to filter on.
            :param version: The package version to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                package_filter_property = inspectorv2_mixins.CfnFilterPropsMixin.PackageFilterProperty(
                    architecture=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    epoch=inspectorv2_mixins.CfnFilterPropsMixin.NumberFilterProperty(
                        lower_inclusive=123,
                        upper_inclusive=123
                    ),
                    file_path=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    name=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    release=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    source_lambda_layer_arn=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    source_layer_hash=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    ),
                    version=inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                        comparison="comparison",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a900c1e8a596d94474f91d1cf409691f29f622cd14501f93b0ca0b7045c11fc1)
                check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
                check_type(argname="argument epoch", value=epoch, expected_type=type_hints["epoch"])
                check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument release", value=release, expected_type=type_hints["release"])
                check_type(argname="argument source_lambda_layer_arn", value=source_lambda_layer_arn, expected_type=type_hints["source_lambda_layer_arn"])
                check_type(argname="argument source_layer_hash", value=source_layer_hash, expected_type=type_hints["source_layer_hash"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if architecture is not None:
                self._values["architecture"] = architecture
            if epoch is not None:
                self._values["epoch"] = epoch
            if file_path is not None:
                self._values["file_path"] = file_path
            if name is not None:
                self._values["name"] = name
            if release is not None:
                self._values["release"] = release
            if source_lambda_layer_arn is not None:
                self._values["source_lambda_layer_arn"] = source_lambda_layer_arn
            if source_layer_hash is not None:
                self._values["source_layer_hash"] = source_layer_hash
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def architecture(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''An object that contains details on the package architecture type to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-architecture
            '''
            result = self._values.get("architecture")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        @builtins.property
        def epoch(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.NumberFilterProperty"]]:
            '''An object that contains details on the package epoch to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-epoch
            '''
            result = self._values.get("epoch")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.NumberFilterProperty"]], result)

        @builtins.property
        def file_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-filepath
            '''
            result = self._values.get("file_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        @builtins.property
        def name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''An object that contains details on the name of the package to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        @builtins.property
        def release(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''An object that contains details on the package release to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-release
            '''
            result = self._values.get("release")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        @builtins.property
        def source_lambda_layer_arn(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-sourcelambdalayerarn
            '''
            result = self._values.get("source_lambda_layer_arn")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        @builtins.property
        def source_layer_hash(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''An object that contains details on the source layer hash to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-sourcelayerhash
            '''
            result = self._values.get("source_layer_hash")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        @builtins.property
        def version(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]]:
            '''The package version to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-packagefilter.html#cfn-inspectorv2-filter-packagefilter-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFilterPropsMixin.StringFilterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PackageFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.PortRangeFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "begin_inclusive": "beginInclusive",
            "end_inclusive": "endInclusive",
        },
    )
    class PortRangeFilterProperty:
        def __init__(
            self,
            *,
            begin_inclusive: typing.Optional[jsii.Number] = None,
            end_inclusive: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that describes the details of a port range filter.

            :param begin_inclusive: The port number the port range begins at.
            :param end_inclusive: The port number the port range ends at.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-portrangefilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                port_range_filter_property = inspectorv2_mixins.CfnFilterPropsMixin.PortRangeFilterProperty(
                    begin_inclusive=123,
                    end_inclusive=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0473db62091c8ba47d9d4be116982dcfc9fe69d4c15a4bda6c390ae37a353bc5)
                check_type(argname="argument begin_inclusive", value=begin_inclusive, expected_type=type_hints["begin_inclusive"])
                check_type(argname="argument end_inclusive", value=end_inclusive, expected_type=type_hints["end_inclusive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if begin_inclusive is not None:
                self._values["begin_inclusive"] = begin_inclusive
            if end_inclusive is not None:
                self._values["end_inclusive"] = end_inclusive

        @builtins.property
        def begin_inclusive(self) -> typing.Optional[jsii.Number]:
            '''The port number the port range begins at.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-portrangefilter.html#cfn-inspectorv2-filter-portrangefilter-begininclusive
            '''
            result = self._values.get("begin_inclusive")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def end_inclusive(self) -> typing.Optional[jsii.Number]:
            '''The port number the port range ends at.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-portrangefilter.html#cfn-inspectorv2-filter-portrangefilter-endinclusive
            '''
            result = self._values.get("end_inclusive")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_inspectorv2.mixins.CfnFilterPropsMixin.StringFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"comparison": "comparison", "value": "value"},
    )
    class StringFilterProperty:
        def __init__(
            self,
            *,
            comparison: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that describes the details of a string filter.

            :param comparison: The operator to use when comparing values in the filter.
            :param value: The value to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-stringfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_inspectorv2 import mixins as inspectorv2_mixins
                
                string_filter_property = inspectorv2_mixins.CfnFilterPropsMixin.StringFilterProperty(
                    comparison="comparison",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b47e440a208f3e4fb19151753b6e242ccfbc89c7b20ffa139520690694716265)
                check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison is not None:
                self._values["comparison"] = comparison
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def comparison(self) -> typing.Optional[builtins.str]:
            '''The operator to use when comparing values in the filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-stringfilter.html#cfn-inspectorv2-filter-stringfilter-comparison
            '''
            result = self._values.get("comparison")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to filter on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-inspectorv2-filter-stringfilter.html#cfn-inspectorv2-filter-stringfilter-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCisScanConfigurationMixinProps",
    "CfnCisScanConfigurationPropsMixin",
    "CfnCodeSecurityIntegrationMixinProps",
    "CfnCodeSecurityIntegrationPropsMixin",
    "CfnCodeSecurityScanConfigurationMixinProps",
    "CfnCodeSecurityScanConfigurationPropsMixin",
    "CfnFilterMixinProps",
    "CfnFilterPropsMixin",
]

publication.publish()

def _typecheckingstub__c9a3c2a60909e46157424b4a08a0572a7925991fcb98a1dd25599df811aaefbe(
    *,
    scan_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_level: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.CisTargetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff8e8887aa60a5fcedd4e932df8d2aeb0d13ad3dde0651e1cd929ee83dc5ad9(
    props: typing.Union[CfnCisScanConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d42d273d6e89027831aa7bf162739eebfa6672bc067606e9e7b75eb941b274(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__befa26716aa3ba851788aa87858f508ac5c860b6606ea92132c658081364bfc8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87bccf8d0ce42f43e51fac9e4ee11cfbd7317dc82154df3968668980e776fc3(
    *,
    account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    target_resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Sequence[builtins.str]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78b534217bb57a303eec64b8bbb2d3eb96ad6d8146c99bec7ce4e72abc2afe2(
    *,
    start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.TimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700408d8629f043c24bfa755f2968e7cf2f498ec2ca3af37bc3aaeb4a6f0a4e8(
    *,
    day: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.TimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__761cfabf43646c5b8ed01600f1e66426137799ca503c436edb3c3ebac745875a(
    *,
    daily: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.DailyScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    monthly: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.MonthlyScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    one_time: typing.Any = None,
    weekly: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.WeeklyScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2b3572c201a389662a471cab926eba74beeea430702f0d3c0349518cd15f1d(
    *,
    time_of_day: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7612736c17231f2264f0c43c06d05eed71b5a74d43bb0bf3de391fa2687a95b(
    *,
    days: typing.Optional[typing.Sequence[builtins.str]] = None,
    start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCisScanConfigurationPropsMixin.TimeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f78c26f395f43d3e3464c91a103fff6a501b0a81cfbdee60ba93d58fef08bdbb(
    *,
    create_integration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityIntegrationPropsMixin.CreateDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
    update_integration_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityIntegrationPropsMixin.UpdateDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a5eb078167c4f3e2cd1f1901f9c9456a8a9ef31599f97b796bd07714ac727a(
    props: typing.Union[CfnCodeSecurityIntegrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23db1e751010f4165f63c7713ddcbd9c9d160910d395e96772a3f82fd2d26e18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee26753e87a7d4f6838514ff3f3a2b1df62b98b966a73772aa32c58a48bfc48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3339eb8a786ccdf616759a5ae6a05d84f09fddc9069d62d61ed257dd17bc443e(
    *,
    gitlab_self_managed: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityIntegrationPropsMixin.CreateGitLabSelfManagedIntegrationDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de2758fedc4fc49bccbb1e609a1ea286e52f4646de8263967dfbe79ffa5b86a(
    *,
    access_token: typing.Optional[builtins.str] = None,
    instance_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3d6759b33452d08af465ba75aab87c8b2eabf3ededf3c856badbca4acbcf906(
    *,
    github: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityIntegrationPropsMixin.UpdateGitHubIntegrationDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gitlab_self_managed: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityIntegrationPropsMixin.UpdateGitLabSelfManagedIntegrationDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f531c58883a6ba418f30ea33a63e867e1178a70242d655762e6cbdabd0b7fde3(
    *,
    code: typing.Optional[builtins.str] = None,
    installation_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0577f4bb9d7e4ac7f691d5618241895bc0a0373d9ba96e76a85b4a8478c1d66c(
    *,
    auth_code: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8b7dae7cd52a0385c907ce4cbd74e7edce000d0f04e1e8b59aa58730609aeb(
    *,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityScanConfigurationPropsMixin.CodeSecurityScanConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    level: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    scope_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityScanConfigurationPropsMixin.ScopeSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c97e6852cd396fd2baf7fd6c8a46d4b09c018380236b72e7635bad8c4ecc4fa8(
    props: typing.Union[CfnCodeSecurityScanConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86148122165322d61fe870f94e115da64dcca0704605430a724696e286a01ec3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__600db8929126d68e905ed1ec088a1453f1c6ac9aecb2e4a26a2c6226bbf8f102(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdce7edd020d2d226ff910c54462520ea8c495debba21d00fbcc1c059ee34398(
    *,
    continuous_integration_scan_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityScanConfigurationPropsMixin.ContinuousIntegrationScanConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    periodic_scan_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCodeSecurityScanConfigurationPropsMixin.PeriodicScanConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_set_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6de6db31c0ba3b74dadece9648057b400be3252bfe37f3ffe379bda977e94dd3(
    *,
    supported_events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4106ffd38fef7a9d9e5e00399223be0b6a2006cbe6619baf92482915bd5ad820(
    *,
    frequency: typing.Optional[builtins.str] = None,
    frequency_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f908214c3f4bb4d7fba041925621e0840a7f461a19e2bcfc9434b567039ffd6e(
    *,
    project_selection_scope: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9890a2a32132eb870f72a91bd3a4bd9e48239f218a138171c6912e39a69a6e49(
    *,
    description: typing.Optional[builtins.str] = None,
    filter_action: typing.Optional[builtins.str] = None,
    filter_criteria: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.FilterCriteriaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a511a9fae2a2d00c9c9840ad961c580dcee340a7af222777f334762664b911(
    props: typing.Union[CfnFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd535c07e3267b87805ae8beaa019f21e81eb44774ca5baed80a266204984ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bff16b99849a31e15683edbb9b4668273b0890730613502919c4ac2cea06b9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92f0cf2bb729f9a0a49856bc44659890ce0a00b44110ca23312f444d20dfc54a(
    *,
    end_inclusive: typing.Optional[jsii.Number] = None,
    start_inclusive: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1510b2f7cac2420ca2a992bb2bc390c1b6516dfbda711282aa8a9818aa69235(
    *,
    aws_account_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    code_vulnerability_detector_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    code_vulnerability_detector_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    code_vulnerability_file_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    component_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    component_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_instance_image_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_instance_subnet_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_instance_vpc_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ecr_image_architecture: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ecr_image_hash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ecr_image_pushed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ecr_image_registry: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ecr_image_repository_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ecr_image_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    epss_score: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    exploit_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_status: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    finding_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    first_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    fix_available: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    inspector_score: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lambda_function_execution_role_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lambda_function_last_modified_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lambda_function_layers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lambda_function_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    lambda_function_runtime: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    last_observed_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_protocol: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    port_range: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.PortRangeFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    related_vulnerabilities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.MapFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    severity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    title: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    updated_at: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.DateFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vendor_severity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vulnerability_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vulnerability_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    vulnerable_packages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.PackageFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3718450f6e139baddd6d6b9cd286e133dcf4b86ce6ef4083fd1c9e83b417f4f3(
    *,
    comparison: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce313c106bfc6b1184d6176b2bffa5c215b7437b709cd7cfe2e6f69bdb33b912(
    *,
    lower_inclusive: typing.Optional[jsii.Number] = None,
    upper_inclusive: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a900c1e8a596d94474f91d1cf409691f29f622cd14501f93b0ca0b7045c11fc1(
    *,
    architecture: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    epoch: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.NumberFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    release: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_lambda_layer_arn: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_layer_hash: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFilterPropsMixin.StringFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0473db62091c8ba47d9d4be116982dcfc9fe69d4c15a4bda6c390ae37a353bc5(
    *,
    begin_inclusive: typing.Optional[jsii.Number] = None,
    end_inclusive: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47e440a208f3e4fb19151753b6e242ccfbc89c7b20ffa139520690694716265(
    *,
    comparison: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
