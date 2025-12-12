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
    jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnDiscoveryMixinProps",
    jsii_struct_bases=[],
    name_mapping={},
)
class CfnDiscoveryMixinProps:
    def __init__(self) -> None:
        '''Properties for CfnDiscoveryPropsMixin.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-discovery.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
            
            cfn_discovery_mixin_props = applicationsignals_mixins.CfnDiscoveryMixinProps()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDiscoveryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDiscoveryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnDiscoveryPropsMixin",
):
    '''.. epigraph::

   If you have existing ``AWS::ApplicationSignals::Discovery`` resources that were created prior to the Application Map release, you will need to delete and recreate these resources in your account to enable Application Map.

    Enables this AWS account to be able to use CloudWatch Application Signals by creating the ``AWSServiceRoleForCloudWatchApplicationSignals`` service-linked role. This service-linked role has the following permissions:

    - ``xray:GetServiceGraph``
    - ``logs:StartQuery``
    - ``logs:GetQueryResults``
    - ``cloudwatch:GetMetricData``
    - ``cloudwatch:ListMetrics``
    - ``tag:GetResources``
    - ``autoscaling:DescribeAutoScalingGroups``

    A service-linked CloudTrail event channel is created to process CloudTrail events and return change event information. This includes last deployment time, userName, eventName, and other event metadata.

    After completing this step, you still need to instrument your Java and Python applications to send data to Application Signals. For more information, see `Enabling Application Signals <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals-Enable.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-discovery.html
    :cloudformationResource: AWS::ApplicationSignals::Discovery
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
        
        cfn_discovery_props_mixin = applicationsignals_mixins.CfnDiscoveryPropsMixin(applicationsignals_mixins.CfnDiscoveryMixinProps(),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDiscoveryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApplicationSignals::Discovery``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce182fa4b83be550fb2703fb7e306c0ebb87166173d1b1f1f721d685abbcecb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd1216fdacbacf3f63d6cdf0f05eb83c2ea658dd9672d69de03a1c79186f3a1c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6685f4fdf7f7c6005355d0143ad30bb4128338149db31c306d146e22a732c41e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDiscoveryMixinProps:
        return typing.cast(CfnDiscoveryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnGroupingConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"grouping_attribute_definitions": "groupingAttributeDefinitions"},
)
class CfnGroupingConfigurationMixinProps:
    def __init__(
        self,
        *,
        grouping_attribute_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnGroupingConfigurationPropsMixin.

        :param grouping_attribute_definitions: An array of grouping attribute definitions that specify how services should be grouped based on various attributes and source keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-groupingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
            
            cfn_grouping_configuration_mixin_props = applicationsignals_mixins.CfnGroupingConfigurationMixinProps(
                grouping_attribute_definitions=[applicationsignals_mixins.CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty(
                    default_grouping_value="defaultGroupingValue",
                    grouping_name="groupingName",
                    grouping_source_keys=["groupingSourceKeys"]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efab68f15db54b8727ad0521e06409801765f795438fa3a3e492f5fe77c365a)
            check_type(argname="argument grouping_attribute_definitions", value=grouping_attribute_definitions, expected_type=type_hints["grouping_attribute_definitions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grouping_attribute_definitions is not None:
            self._values["grouping_attribute_definitions"] = grouping_attribute_definitions

    @builtins.property
    def grouping_attribute_definitions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty"]]]]:
        '''An array of grouping attribute definitions that specify how services should be grouped based on various attributes and source keys.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-groupingconfiguration.html#cfn-applicationsignals-groupingconfiguration-groupingattributedefinitions
        '''
        result = self._values.get("grouping_attribute_definitions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupingConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupingConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnGroupingConfigurationPropsMixin",
):
    '''A structure that contains the complete grouping configuration for an account, including all defined grouping attributes and metadata about when it was last updated.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-groupingconfiguration.html
    :cloudformationResource: AWS::ApplicationSignals::GroupingConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
        
        cfn_grouping_configuration_props_mixin = applicationsignals_mixins.CfnGroupingConfigurationPropsMixin(applicationsignals_mixins.CfnGroupingConfigurationMixinProps(
            grouping_attribute_definitions=[applicationsignals_mixins.CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty(
                default_grouping_value="defaultGroupingValue",
                grouping_name="groupingName",
                grouping_source_keys=["groupingSourceKeys"]
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApplicationSignals::GroupingConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bbbc0b86917c09405076c83806f75c09efec66c818d0f22451a21b4bb3a6617)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3548046ad6ac456910fac9c082cd1443ea0eb4d8f8d3860ea53263705e73c98)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3f98e6bb9559c3ffc611afcacc67eb72a82d45c24ea4f0775c927ea31c806c2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupingConfigurationMixinProps:
        return typing.cast(CfnGroupingConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_grouping_value": "defaultGroupingValue",
            "grouping_name": "groupingName",
            "grouping_source_keys": "groupingSourceKeys",
        },
    )
    class GroupingAttributeDefinitionProperty:
        def __init__(
            self,
            *,
            default_grouping_value: typing.Optional[builtins.str] = None,
            grouping_name: typing.Optional[builtins.str] = None,
            grouping_source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A structure that defines how services should be grouped based on specific attributes.

            This includes the friendly name for the grouping, the source keys to derive values from, and an optional default value.

            :param default_grouping_value: The default value to use for this grouping attribute when no value can be derived from the source keys. This ensures all services have a grouping value even if the source data is missing.
            :param grouping_name: The friendly name for this grouping attribute, such as ``BusinessUnit`` or ``Environment`` . This name is used to identify the grouping in the console and APIs.
            :param grouping_source_keys: An array of source keys used to derive the grouping attribute value from telemetry data, AWS tags, or other sources. For example, ["business_unit", "team"] would look for values in those fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-groupingconfiguration-groupingattributedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                grouping_attribute_definition_property = applicationsignals_mixins.CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty(
                    default_grouping_value="defaultGroupingValue",
                    grouping_name="groupingName",
                    grouping_source_keys=["groupingSourceKeys"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d449e3390eaf2afabebe2b309bd4f197d32a9b7219d153a94bd7c7a1c1b59095)
                check_type(argname="argument default_grouping_value", value=default_grouping_value, expected_type=type_hints["default_grouping_value"])
                check_type(argname="argument grouping_name", value=grouping_name, expected_type=type_hints["grouping_name"])
                check_type(argname="argument grouping_source_keys", value=grouping_source_keys, expected_type=type_hints["grouping_source_keys"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_grouping_value is not None:
                self._values["default_grouping_value"] = default_grouping_value
            if grouping_name is not None:
                self._values["grouping_name"] = grouping_name
            if grouping_source_keys is not None:
                self._values["grouping_source_keys"] = grouping_source_keys

        @builtins.property
        def default_grouping_value(self) -> typing.Optional[builtins.str]:
            '''The default value to use for this grouping attribute when no value can be derived from the source keys.

            This ensures all services have a grouping value even if the source data is missing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-groupingconfiguration-groupingattributedefinition.html#cfn-applicationsignals-groupingconfiguration-groupingattributedefinition-defaultgroupingvalue
            '''
            result = self._values.get("default_grouping_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def grouping_name(self) -> typing.Optional[builtins.str]:
            '''The friendly name for this grouping attribute, such as ``BusinessUnit`` or ``Environment`` .

            This name is used to identify the grouping in the console and APIs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-groupingconfiguration-groupingattributedefinition.html#cfn-applicationsignals-groupingconfiguration-groupingattributedefinition-groupingname
            '''
            result = self._values.get("grouping_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def grouping_source_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of source keys used to derive the grouping attribute value from telemetry data, AWS tags, or other sources.

            For example, ["business_unit", "team"] would look for values in those fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-groupingconfiguration-groupingattributedefinition.html#cfn-applicationsignals-groupingconfiguration-groupingattributedefinition-groupingsourcekeys
            '''
            result = self._values.get("grouping_source_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupingAttributeDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectiveMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "burn_rate_configurations": "burnRateConfigurations",
        "description": "description",
        "exclusion_windows": "exclusionWindows",
        "goal": "goal",
        "name": "name",
        "request_based_sli": "requestBasedSli",
        "sli": "sli",
        "tags": "tags",
    },
)
class CfnServiceLevelObjectiveMixinProps:
    def __init__(
        self,
        *,
        burn_rate_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        exclusion_windows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        goal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.GoalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        request_based_sli: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sli: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.SliProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServiceLevelObjectivePropsMixin.

        :param burn_rate_configurations: Each object in this array defines the length of the look-back window used to calculate one burn rate metric for this SLO. The burn rate measures how fast the service is consuming the error budget, relative to the attainment goal of the SLO.
        :param description: An optional description for this SLO. Default: - "No description"
        :param exclusion_windows: The time window to be excluded from the SLO performance metrics.
        :param goal: This structure contains the attributes that determine the goal of an SLO. This includes the time period for evaluation and the attainment threshold.
        :param name: A name for this SLO.
        :param request_based_sli: A structure containing information about the performance metric that this SLO monitors, if this is a request-based SLO.
        :param sli: A structure containing information about the performance metric that this SLO monitors, if this is a period-based SLO.
        :param tags: A list of key-value pairs to associate with the SLO. You can associate as many as 50 tags with an SLO. To be able to associate tags with the SLO when you create the SLO, you must have the cloudwatch:TagResource permission. Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
            
            cfn_service_level_objective_mixin_props = applicationsignals_mixins.CfnServiceLevelObjectiveMixinProps(
                burn_rate_configurations=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty(
                    look_back_window_minutes=123
                )],
                description="description",
                exclusion_windows=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty(
                    reason="reason",
                    recurrence_rule=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty(
                        expression="expression"
                    ),
                    start_time="startTime",
                    window=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.WindowProperty(
                        duration=123,
                        duration_unit="durationUnit"
                    )
                )],
                goal=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.GoalProperty(
                    attainment_goal=123,
                    interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.IntervalProperty(
                        calendar_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty(
                            duration=123,
                            duration_unit="durationUnit",
                            start_time=123
                        ),
                        rolling_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty(
                            duration=123,
                            duration_unit="durationUnit"
                        )
                    ),
                    warning_threshold=123
                ),
                name="name",
                request_based_sli=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty(
                    comparison_operator="comparisonOperator",
                    metric_threshold=123,
                    request_based_sli_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty(
                        dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                            dependency_key_attributes={
                                "dependency_key_attributes_key": "dependencyKeyAttributes"
                            },
                            dependency_operation_name="dependencyOperationName"
                        ),
                        key_attributes={
                            "key_attributes_key": "keyAttributes"
                        },
                        metric_type="metricType",
                        monitored_request_count_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty(
                            bad_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                                account_id="accountId",
                                expression="expression",
                                id="id",
                                metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                    metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                        dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    period=123,
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )],
                            good_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                                account_id="accountId",
                                expression="expression",
                                id="id",
                                metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                    metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                        dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    period=123,
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        operation_name="operationName",
                        total_request_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    )
                ),
                sli=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliProperty(
                    comparison_operator="comparisonOperator",
                    metric_threshold=123,
                    sli_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliMetricProperty(
                        dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                            dependency_key_attributes={
                                "dependency_key_attributes_key": "dependencyKeyAttributes"
                            },
                            dependency_operation_name="dependencyOperationName"
                        ),
                        key_attributes={
                            "key_attributes_key": "keyAttributes"
                        },
                        metric_data_queries=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )],
                        metric_type="metricType",
                        operation_name="operationName",
                        period_seconds=123,
                        statistic="statistic"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0f72afb86742419d109416d6ca5d34dc09dcd54a978cd7e3d675fd372132812)
            check_type(argname="argument burn_rate_configurations", value=burn_rate_configurations, expected_type=type_hints["burn_rate_configurations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument exclusion_windows", value=exclusion_windows, expected_type=type_hints["exclusion_windows"])
            check_type(argname="argument goal", value=goal, expected_type=type_hints["goal"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument request_based_sli", value=request_based_sli, expected_type=type_hints["request_based_sli"])
            check_type(argname="argument sli", value=sli, expected_type=type_hints["sli"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if burn_rate_configurations is not None:
            self._values["burn_rate_configurations"] = burn_rate_configurations
        if description is not None:
            self._values["description"] = description
        if exclusion_windows is not None:
            self._values["exclusion_windows"] = exclusion_windows
        if goal is not None:
            self._values["goal"] = goal
        if name is not None:
            self._values["name"] = name
        if request_based_sli is not None:
            self._values["request_based_sli"] = request_based_sli
        if sli is not None:
            self._values["sli"] = sli
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def burn_rate_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty"]]]]:
        '''Each object in this array defines the length of the look-back window used to calculate one burn rate metric for this SLO.

        The burn rate measures how fast the service is consuming the error budget, relative to the attainment goal of the SLO.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-burnrateconfigurations
        '''
        result = self._values.get("burn_rate_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this SLO.

        :default: - "No description"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def exclusion_windows(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty"]]]]:
        '''The time window to be excluded from the SLO performance metrics.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-exclusionwindows
        '''
        result = self._values.get("exclusion_windows")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty"]]]], result)

    @builtins.property
    def goal(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.GoalProperty"]]:
        '''This structure contains the attributes that determine the goal of an SLO.

        This includes the time period for evaluation and the attainment threshold.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-goal
        '''
        result = self._values.get("goal")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.GoalProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for this SLO.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def request_based_sli(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty"]]:
        '''A structure containing information about the performance metric that this SLO monitors, if this is a request-based SLO.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-requestbasedsli
        '''
        result = self._values.get("request_based_sli")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty"]], result)

    @builtins.property
    def sli(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.SliProperty"]]:
        '''A structure containing information about the performance metric that this SLO monitors, if this is a period-based SLO.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-sli
        '''
        result = self._values.get("sli")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.SliProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs to associate with the SLO.

        You can associate as many as 50 tags with an SLO. To be able to associate tags with the SLO when you create the SLO, you must have the cloudwatch:TagResource permission.

        Tags can help you organize and categorize your resources. You can also use them to scope user permissions by granting a user permission to access or change only resources with certain tag values.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html#cfn-applicationsignals-servicelevelobjective-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceLevelObjectiveMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceLevelObjectivePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin",
):
    '''Creates or updates a service level objective (SLO), which can help you ensure that your critical business operations are meeting customer expectations.

    Use SLOs to set and track specific target levels for the reliability and availability of your applications and services. SLOs use service level indicators (SLIs) to calculate whether the application is performing at the level that you want.

    Create an SLO to set a target for a service operation, or service dependency's availability or latency. CloudWatch measures this target frequently you can find whether it has been breached.

    The target performance quality that is defined for an SLO is the *attainment goal* . An attainment goal is the percentage of time or requests that the SLI is expected to meet the threshold over each time interval. For example, an attainment goal of 99.9% means that within your interval, you are targeting 99.9% of the periods to be in healthy state.

    When you create an SLO, you specify whether it is a *period-based SLO* or a *request-based SLO* . Each type of SLO has a different way of evaluating your application's performance against its attainment goal.

    - A *period-based SLO* uses defined *periods* of time within a specified total time interval. For each period of time, Application Signals determines whether the application met its goal. The attainment rate is calculated as the ``number of good periods/number of total periods`` .

    For example, for a period-based SLO, meeting an attainment goal of 99.9% means that within your interval, your application must meet its performance goal during at least 99.9% of the time periods.

    - A *request-based SLO* doesn't use pre-defined periods of time. Instead, the SLO measures ``number of good requests/number of total requests`` during the interval. At any time, you can find the ratio of good requests to total requests for the interval up to the time stamp that you specify, and measure that ratio against the goal set in your SLO.

    After you have created an SLO, you can retrieve error budget reports for it. An *error budget* is the amount of time or amount of requests that your application can be non-compliant with the SLO's goal, and still have your application meet the goal.

    - For a period-based SLO, the error budget starts at a number defined by the highest number of periods that can fail to meet the threshold, while still meeting the overall goal. The *remaining error budget* decreases with every failed period that is recorded. The error budget within one interval can never increase.

    For example, an SLO with a threshold that 99.95% of requests must be completed under 2000ms every month translates to an error budget of 21.9 minutes of downtime per month.

    - For a request-based SLO, the remaining error budget is dynamic and can increase or decrease, depending on the ratio of good requests to total requests.

    When you call this operation, Application Signals creates the *AWSServiceRoleForCloudWatchApplicationSignals* service-linked role, if it doesn't already exist in your account. This service- linked role has the following permissions:

    - ``xray:GetServiceGraph``
    - ``logs:StartQuery``
    - ``logs:GetQueryResults``
    - ``cloudwatch:GetMetricData``
    - ``cloudwatch:ListMetrics``
    - ``tag:GetResources``
    - ``autoscaling:DescribeAutoScalingGroups``

    You can easily set SLO targets for your applications, and their dependencies, that are discovered by Application Signals, using critical metrics such as latency and availability. You can also set SLOs against any CloudWatch metric or math expression that produces a time series.
    .. epigraph::

       You can't create an SLO for a service operation that was discovered by Application Signals until after that operation has reported standard metrics to Application Signals.

    You cannot change from a period-based SLO to a request-based SLO, or change from a request-based SLO to a period-based SLO.

    For more information about SLOs, see `Service level objectives (SLOs) <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-ServiceLevelObjectives.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationsignals-servicelevelobjective.html
    :cloudformationResource: AWS::ApplicationSignals::ServiceLevelObjective
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
        
        cfn_service_level_objective_props_mixin = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin(applicationsignals_mixins.CfnServiceLevelObjectiveMixinProps(
            burn_rate_configurations=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty(
                look_back_window_minutes=123
            )],
            description="description",
            exclusion_windows=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty(
                reason="reason",
                recurrence_rule=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty(
                    expression="expression"
                ),
                start_time="startTime",
                window=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.WindowProperty(
                    duration=123,
                    duration_unit="durationUnit"
                )
            )],
            goal=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.GoalProperty(
                attainment_goal=123,
                interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.IntervalProperty(
                    calendar_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty(
                        duration=123,
                        duration_unit="durationUnit",
                        start_time=123
                    ),
                    rolling_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty(
                        duration=123,
                        duration_unit="durationUnit"
                    )
                ),
                warning_threshold=123
            ),
            name="name",
            request_based_sli=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty(
                comparison_operator="comparisonOperator",
                metric_threshold=123,
                request_based_sli_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty(
                    dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                        dependency_key_attributes={
                            "dependency_key_attributes_key": "dependencyKeyAttributes"
                        },
                        dependency_operation_name="dependencyOperationName"
                    ),
                    key_attributes={
                        "key_attributes_key": "keyAttributes"
                    },
                    metric_type="metricType",
                    monitored_request_count_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty(
                        bad_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )],
                        good_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    operation_name="operationName",
                    total_request_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                            metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            ),
            sli=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliProperty(
                comparison_operator="comparisonOperator",
                metric_threshold=123,
                sli_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliMetricProperty(
                    dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                        dependency_key_attributes={
                            "dependency_key_attributes_key": "dependencyKeyAttributes"
                        },
                        dependency_operation_name="dependencyOperationName"
                    ),
                    key_attributes={
                        "key_attributes_key": "keyAttributes"
                    },
                    metric_data_queries=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                            metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )],
                    metric_type="metricType",
                    operation_name="operationName",
                    period_seconds=123,
                    statistic="statistic"
                )
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
        props: typing.Union[CfnServiceLevelObjectiveMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ApplicationSignals::ServiceLevelObjective``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532520fe3bfa694185d2d8118551fd89af8a023205535283580129d0f87ea92f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62f64b26621722d8db001a72944e696c6a28eeeb23b5c58dea5215382de579a5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d84e34b3b5521a8650cb001577f4ef3c0b7408241d35cade53a0639de2ba65aa)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceLevelObjectiveMixinProps:
        return typing.cast(CfnServiceLevelObjectiveMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"look_back_window_minutes": "lookBackWindowMinutes"},
    )
    class BurnRateConfigurationProperty:
        def __init__(
            self,
            *,
            look_back_window_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This object defines the length of the look-back window used to calculate one burn rate metric for this SLO.

            The burn rate measures how fast the service is consuming the error budget, relative to the attainment goal of the SLO. A burn rate of exactly 1 indicates that the SLO goal will be met exactly.

            For example, if you specify 60 as the number of minutes in the look-back window, the burn rate is calculated as the following:

            *burn rate = error rate over the look-back window / (100% - attainment goal percentage)*

            For more information about burn rates, see `Calculate burn rates <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-ServiceLevelObjectives.html#CloudWatch-ServiceLevelObjectives-burn>`_ .

            :param look_back_window_minutes: The number of minutes to use as the look-back window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-burnrateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                burn_rate_configuration_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty(
                    look_back_window_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8dbf05d1b15247e01d3f913e139aa65d96e5f09962fb551aab8ba141cfe833f3)
                check_type(argname="argument look_back_window_minutes", value=look_back_window_minutes, expected_type=type_hints["look_back_window_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if look_back_window_minutes is not None:
                self._values["look_back_window_minutes"] = look_back_window_minutes

        @builtins.property
        def look_back_window_minutes(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes to use as the look-back window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-burnrateconfiguration.html#cfn-applicationsignals-servicelevelobjective-burnrateconfiguration-lookbackwindowminutes
            '''
            result = self._values.get("look_back_window_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BurnRateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration": "duration",
            "duration_unit": "durationUnit",
            "start_time": "startTime",
        },
    )
    class CalendarIntervalProperty:
        def __init__(
            self,
            *,
            duration: typing.Optional[jsii.Number] = None,
            duration_unit: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''If the interval for this service level objective is a calendar interval, this structure contains the interval specifications.

            :param duration: Specifies the duration of each calendar interval. For example, if ``Duration`` is ``1`` and ``DurationUnit`` is ``MONTH`` , each interval is one month, aligned with the calendar.
            :param duration_unit: Specifies the calendar interval unit.
            :param start_time: The date and time when you want the first interval to start. Be sure to choose a time that configures the intervals the way that you want. For example, if you want weekly intervals starting on Mondays at 6 a.m., be sure to specify a start time that is a Monday at 6 a.m. When used in a raw HTTP Query API, it is formatted as be epoch time in seconds. For example: ``1698778057`` As soon as one calendar interval ends, another automatically begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-calendarinterval.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                calendar_interval_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty(
                    duration=123,
                    duration_unit="durationUnit",
                    start_time=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9cf90d2302025d5ee551908d6ba24ad374bed0411f8ee2728aa0c6a4011b6c3)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument duration_unit", value=duration_unit, expected_type=type_hints["duration_unit"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration is not None:
                self._values["duration"] = duration
            if duration_unit is not None:
                self._values["duration_unit"] = duration_unit
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def duration(self) -> typing.Optional[jsii.Number]:
            '''Specifies the duration of each calendar interval.

            For example, if ``Duration`` is ``1`` and ``DurationUnit`` is ``MONTH`` , each interval is one month, aligned with the calendar.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-calendarinterval.html#cfn-applicationsignals-servicelevelobjective-calendarinterval-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def duration_unit(self) -> typing.Optional[builtins.str]:
            '''Specifies the calendar interval unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-calendarinterval.html#cfn-applicationsignals-servicelevelobjective-calendarinterval-durationunit
            '''
            result = self._values.get("duration_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(self) -> typing.Optional[jsii.Number]:
            '''The date and time when you want the first interval to start.

            Be sure to choose a time that configures the intervals the way that you want. For example, if you want weekly intervals starting on Mondays at 6 a.m., be sure to specify a start time that is a Monday at 6 a.m.

            When used in a raw HTTP Query API, it is formatted as be epoch time in seconds. For example: ``1698778057``

            As soon as one calendar interval ends, another automatically begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-calendarinterval.html#cfn-applicationsignals-servicelevelobjective-calendarinterval-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CalendarIntervalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dependency_key_attributes": "dependencyKeyAttributes",
            "dependency_operation_name": "dependencyOperationName",
        },
    )
    class DependencyConfigProperty:
        def __init__(
            self,
            *,
            dependency_key_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            dependency_operation_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies the dependency using the ``DependencyKeyAttributes`` and ``DependencyOperationName`` .

            :param dependency_key_attributes: If this SLO is related to a metric collected by Application Signals, you must use this field to specify which dependency the SLO metric is related to. - ``Type`` designates the type of object this is. - ``ResourceType`` specifies the type of the resource. This field is used only when the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` . - ``Name`` specifies the name of the object. This is used only if the value of the ``Type`` field is ``Service`` , ``RemoteService`` , or ``AWS::Service`` . - ``Identifier`` identifies the resource objects of this resource. This is used only if the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` . - ``Environment`` specifies the location where this object is hosted, or what it belongs to.
            :param dependency_operation_name: When the SLO monitors a specific operation of the dependency, this field specifies the name of that operation in the dependency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-dependencyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                dependency_config_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                    dependency_key_attributes={
                        "dependency_key_attributes_key": "dependencyKeyAttributes"
                    },
                    dependency_operation_name="dependencyOperationName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97ff6909a5170c5d77c85cad52b4bf1c6f3db9f0712385c057ca6a696a9124cf)
                check_type(argname="argument dependency_key_attributes", value=dependency_key_attributes, expected_type=type_hints["dependency_key_attributes"])
                check_type(argname="argument dependency_operation_name", value=dependency_operation_name, expected_type=type_hints["dependency_operation_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dependency_key_attributes is not None:
                self._values["dependency_key_attributes"] = dependency_key_attributes
            if dependency_operation_name is not None:
                self._values["dependency_operation_name"] = dependency_operation_name

        @builtins.property
        def dependency_key_attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''If this SLO is related to a metric collected by Application Signals, you must use this field to specify which dependency the SLO metric is related to.

            - ``Type`` designates the type of object this is.
            - ``ResourceType`` specifies the type of the resource. This field is used only when the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` .
            - ``Name`` specifies the name of the object. This is used only if the value of the ``Type`` field is ``Service`` , ``RemoteService`` , or ``AWS::Service`` .
            - ``Identifier`` identifies the resource objects of this resource. This is used only if the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` .
            - ``Environment`` specifies the location where this object is hosted, or what it belongs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-dependencyconfig.html#cfn-applicationsignals-servicelevelobjective-dependencyconfig-dependencykeyattributes
            '''
            result = self._values.get("dependency_key_attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def dependency_operation_name(self) -> typing.Optional[builtins.str]:
            '''When the SLO monitors a specific operation of the dependency, this field specifies the name of that operation in the dependency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-dependencyconfig.html#cfn-applicationsignals-servicelevelobjective-dependencyconfig-dependencyoperationname
            '''
            result = self._values.get("dependency_operation_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DependencyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class DimensionProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A dimension is a name/value pair that is part of the identity of a metric.

            Because dimensions are part of the unique identifier for a metric, whenever you add a unique name/value pair to one of your metrics, you are creating a new variation of that metric. For example, many Amazon EC2 metrics publish ``InstanceId`` as a dimension name, and the actual instance ID as the value for that dimension.

            You can assign up to 30 dimensions to a metric.

            :param name: The name of the dimension. Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon ( ``:`` ). ASCII control characters are not supported as part of dimension names.
            :param value: The value of the dimension. Dimension values must contain only ASCII characters and must include at least one non-whitespace character. ASCII control characters are not supported as part of dimension values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                dimension_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60d464a778a9d6dbe753fd6399d83b0009927fe1cb54c52c35dfac7300443bde)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the dimension.

            Dimension names must contain only ASCII characters, must include at least one non-whitespace character, and cannot start with a colon ( ``:`` ). ASCII control characters are not supported as part of dimension names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-dimension.html#cfn-applicationsignals-servicelevelobjective-dimension-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the dimension.

            Dimension values must contain only ASCII characters and must include at least one non-whitespace character. ASCII control characters are not supported as part of dimension values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-dimension.html#cfn-applicationsignals-servicelevelobjective-dimension-value
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
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "reason": "reason",
            "recurrence_rule": "recurrenceRule",
            "start_time": "startTime",
            "window": "window",
        },
    )
    class ExclusionWindowProperty:
        def __init__(
            self,
            *,
            reason: typing.Optional[builtins.str] = None,
            recurrence_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_time: typing.Optional[builtins.str] = None,
            window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.WindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The time window to be excluded from the SLO performance metrics.

            :param reason: The reason for the time exclusion windows. For example, maintenance. Default: - "No reason"
            :param recurrence_rule: The recurrence rule for the time exclusion window.
            :param start_time: The start time of the time exclusion window.
            :param window: The time exclusion window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-exclusionwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                exclusion_window_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty(
                    reason="reason",
                    recurrence_rule=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty(
                        expression="expression"
                    ),
                    start_time="startTime",
                    window=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.WindowProperty(
                        duration=123,
                        duration_unit="durationUnit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44ec70aac0d5a05def582836bdaac4aa8320b481bae6be35f1b0bd3b5b327b9b)
                check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
                check_type(argname="argument recurrence_rule", value=recurrence_rule, expected_type=type_hints["recurrence_rule"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
                check_type(argname="argument window", value=window, expected_type=type_hints["window"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reason is not None:
                self._values["reason"] = reason
            if recurrence_rule is not None:
                self._values["recurrence_rule"] = recurrence_rule
            if start_time is not None:
                self._values["start_time"] = start_time
            if window is not None:
                self._values["window"] = window

        @builtins.property
        def reason(self) -> typing.Optional[builtins.str]:
            '''The reason for the time exclusion windows.

            For example, maintenance.

            :default: - "No reason"

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-exclusionwindow.html#cfn-applicationsignals-servicelevelobjective-exclusionwindow-reason
            '''
            result = self._values.get("reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recurrence_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty"]]:
            '''The recurrence rule for the time exclusion window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-exclusionwindow.html#cfn-applicationsignals-servicelevelobjective-exclusionwindow-recurrencerule
            '''
            result = self._values.get("recurrence_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty"]], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The start time of the time exclusion window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-exclusionwindow.html#cfn-applicationsignals-servicelevelobjective-exclusionwindow-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def window(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.WindowProperty"]]:
            '''The time exclusion window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-exclusionwindow.html#cfn-applicationsignals-servicelevelobjective-exclusionwindow-window
            '''
            result = self._values.get("window")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.WindowProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExclusionWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.GoalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attainment_goal": "attainmentGoal",
            "interval": "interval",
            "warning_threshold": "warningThreshold",
        },
    )
    class GoalProperty:
        def __init__(
            self,
            *,
            attainment_goal: typing.Optional[jsii.Number] = None,
            interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.IntervalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            warning_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This structure contains the attributes that determine the goal of an SLO.

            This includes the time period for evaluation and the attainment threshold.

            :param attainment_goal: The threshold that determines if the goal is being met. If this is a period-based SLO, the attainment goal is the percentage of good periods that meet the threshold requirements to the total periods within the interval. For example, an attainment goal of 99.9% means that within your interval, you are targeting 99.9% of the periods to be in healthy state. If this is a request-based SLO, the attainment goal is the percentage of requests that must be successful to meet the attainment goal. If you omit this parameter, 99 is used to represent 99% as the attainment goal.
            :param interval: The time period used to evaluate the SLO. It can be either a calendar interval or rolling interval. If you omit this parameter, a rolling interval of 7 days is used.
            :param warning_threshold: The percentage of remaining budget over total budget that you want to get warnings for. If you omit this parameter, the default of 50.0 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-goal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                goal_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.GoalProperty(
                    attainment_goal=123,
                    interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.IntervalProperty(
                        calendar_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty(
                            duration=123,
                            duration_unit="durationUnit",
                            start_time=123
                        ),
                        rolling_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty(
                            duration=123,
                            duration_unit="durationUnit"
                        )
                    ),
                    warning_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bd9059b066f6aa2a276f71650260518f53a56953bbdcb2d43adff9de0702face)
                check_type(argname="argument attainment_goal", value=attainment_goal, expected_type=type_hints["attainment_goal"])
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument warning_threshold", value=warning_threshold, expected_type=type_hints["warning_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attainment_goal is not None:
                self._values["attainment_goal"] = attainment_goal
            if interval is not None:
                self._values["interval"] = interval
            if warning_threshold is not None:
                self._values["warning_threshold"] = warning_threshold

        @builtins.property
        def attainment_goal(self) -> typing.Optional[jsii.Number]:
            '''The threshold that determines if the goal is being met.

            If this is a period-based SLO, the attainment goal is the percentage of good periods that meet the threshold requirements to the total periods within the interval. For example, an attainment goal of 99.9% means that within your interval, you are targeting 99.9% of the periods to be in healthy state.

            If this is a request-based SLO, the attainment goal is the percentage of requests that must be successful to meet the attainment goal.

            If you omit this parameter, 99 is used to represent 99% as the attainment goal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-goal.html#cfn-applicationsignals-servicelevelobjective-goal-attainmentgoal
            '''
            result = self._values.get("attainment_goal")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def interval(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.IntervalProperty"]]:
            '''The time period used to evaluate the SLO. It can be either a calendar interval or rolling interval.

            If you omit this parameter, a rolling interval of 7 days is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-goal.html#cfn-applicationsignals-servicelevelobjective-goal-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.IntervalProperty"]], result)

        @builtins.property
        def warning_threshold(self) -> typing.Optional[jsii.Number]:
            '''The percentage of remaining budget over total budget that you want to get warnings for.

            If you omit this parameter, the default of 50.0 is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-goal.html#cfn-applicationsignals-servicelevelobjective-goal-warningthreshold
            '''
            result = self._values.get("warning_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GoalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.IntervalProperty",
        jsii_struct_bases=[],
        name_mapping={
            "calendar_interval": "calendarInterval",
            "rolling_interval": "rollingInterval",
        },
    )
    class IntervalProperty:
        def __init__(
            self,
            *,
            calendar_interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rolling_interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The time period used to evaluate the SLO.

            It can be either a calendar interval or rolling interval.

            :param calendar_interval: If the interval is a calendar interval, this structure contains the interval specifications.
            :param rolling_interval: If the interval is a rolling interval, this structure contains the interval specifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-interval.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                interval_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.IntervalProperty(
                    calendar_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty(
                        duration=123,
                        duration_unit="durationUnit",
                        start_time=123
                    ),
                    rolling_interval=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty(
                        duration=123,
                        duration_unit="durationUnit"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2fbea2f1e33354202c940a66e7064de28a00d83167e17dfbc2d7d5e3f44c3264)
                check_type(argname="argument calendar_interval", value=calendar_interval, expected_type=type_hints["calendar_interval"])
                check_type(argname="argument rolling_interval", value=rolling_interval, expected_type=type_hints["rolling_interval"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if calendar_interval is not None:
                self._values["calendar_interval"] = calendar_interval
            if rolling_interval is not None:
                self._values["rolling_interval"] = rolling_interval

        @builtins.property
        def calendar_interval(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty"]]:
            '''If the interval is a calendar interval, this structure contains the interval specifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-interval.html#cfn-applicationsignals-servicelevelobjective-interval-calendarinterval
            '''
            result = self._values.get("calendar_interval")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty"]], result)

        @builtins.property
        def rolling_interval(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty"]]:
            '''If the interval is a rolling interval, this structure contains the interval specifications.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-interval.html#cfn-applicationsignals-servicelevelobjective-interval-rollinginterval
            '''
            result = self._values.get("rolling_interval")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntervalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_id": "accountId",
            "expression": "expression",
            "id": "id",
            "metric_stat": "metricStat",
            "return_data": "returnData",
        },
    )
    class MetricDataQueryProperty:
        def __init__(
            self,
            *,
            account_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MetricStatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Use this structure to define a metric or metric math expression that you want to use as for a service level objective.

            Each ``MetricDataQuery`` in the ``MetricDataQueries`` array specifies either a metric to retrieve, or a metric math expression to be performed on retrieved metrics. A single ``MetricDataQueries`` array can include as many as 20 ``MetricDataQuery`` structures in the array. The 20 structures can include as many as 10 structures that contain a ``MetricStat`` parameter to retrieve a metric, and as many as 10 structures that contain the ``Expression`` parameter to perform a math expression. Of those ``Expression`` structures, exactly one must have true as the value for ``ReturnData`` . The result of this expression used for the SLO.

            For more information about metric math expressions, see `Use metric math <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html>`_ .

            Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :param account_id: The ID of the account where this metric is located. If you are performing this operation in a monitoring account, use this to specify which source account to retrieve this metric from.
            :param expression: This field can contain a metric math expression to be performed on the other metrics that you are retrieving within this ``MetricDataQueries`` structure. A math expression can use the ``Id`` of the other metrics or queries to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* . Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param id: A short name used to tie this object to the results in the response. This ``Id`` must be unique within a ``MetricDataQueries`` array. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the metric math expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.
            :param metric_stat: A metric to be used directly for the SLO, or to be used in the math expression that will be used for the SLO. Within one ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` but not both.
            :param return_data: Use this only if you are using a metric math expression for the SLO. Specify ``true`` for ``ReturnData`` for only the one expression result to use as the alarm. For all other metrics and expressions in the same ``CreateServiceLevelObjective`` operation, specify ``ReturnData`` as ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricdataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                metric_data_query_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                    account_id="accountId",
                    expression="expression",
                    id="id",
                    metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                        metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                            dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                name="name",
                                value="value"
                            )],
                            metric_name="metricName",
                            namespace="namespace"
                        ),
                        period=123,
                        stat="stat",
                        unit="unit"
                    ),
                    return_data=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d157cdc7c931b3b563e06c007167e0c11fc5259c2e32d3b6d9f938eafc0860d1)
                check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument metric_stat", value=metric_stat, expected_type=type_hints["metric_stat"])
                check_type(argname="argument return_data", value=return_data, expected_type=type_hints["return_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_id is not None:
                self._values["account_id"] = account_id
            if expression is not None:
                self._values["expression"] = expression
            if id is not None:
                self._values["id"] = id
            if metric_stat is not None:
                self._values["metric_stat"] = metric_stat
            if return_data is not None:
                self._values["return_data"] = return_data

        @builtins.property
        def account_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the account where this metric is located.

            If you are performing this operation in a monitoring account, use this to specify which source account to retrieve this metric from.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricdataquery.html#cfn-applicationsignals-servicelevelobjective-metricdataquery-accountid
            '''
            result = self._values.get("account_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''This field can contain a metric math expression to be performed on the other metrics that you are retrieving within this ``MetricDataQueries`` structure.

            A math expression can use the ``Id`` of the other metrics or queries to refer to those metrics, and can also use the ``Id`` of other expressions to use the result of those expressions. For more information about metric math expressions, see `Metric Math Syntax and Functions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/using-metric-math.html#metric-math-syntax>`_ in the *Amazon CloudWatch User Guide* .

            Within each ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricdataquery.html#cfn-applicationsignals-servicelevelobjective-metricdataquery-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''A short name used to tie this object to the results in the response.

            This ``Id`` must be unique within a ``MetricDataQueries`` array. If you are performing math expressions on this set of data, this name represents that data and can serve as a variable in the metric math expression. The valid characters are letters, numbers, and underscore. The first character must be a lowercase letter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricdataquery.html#cfn-applicationsignals-servicelevelobjective-metricdataquery-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_stat(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricStatProperty"]]:
            '''A metric to be used directly for the SLO, or to be used in the math expression that will be used for the SLO.

            Within one ``MetricDataQuery`` object, you must specify either ``Expression`` or ``MetricStat`` but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricdataquery.html#cfn-applicationsignals-servicelevelobjective-metricdataquery-metricstat
            '''
            result = self._values.get("metric_stat")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricStatProperty"]], result)

        @builtins.property
        def return_data(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Use this only if you are using a metric math expression for the SLO.

            Specify ``true`` for ``ReturnData`` for only the one expression result to use as the alarm. For all other metrics and expressions in the same ``CreateServiceLevelObjective`` operation, specify ``ReturnData`` as ``false`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricdataquery.html#cfn-applicationsignals-servicelevelobjective-metricdataquery-returndata
            '''
            result = self._values.get("return_data")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricDataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dimensions": "dimensions",
            "metric_name": "metricName",
            "namespace": "namespace",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_name: typing.Optional[builtins.str] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the metric used for a service level indicator, including the metric name, namespace, and dimensions.

            :param dimensions: An array of one or more dimensions to use to define the metric that you want to use. For more information, see `Dimensions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Dimension>`_ .
            :param metric_name: The name of the metric to use.
            :param namespace: The namespace of the metric. For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                metric_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                        name="name",
                        value="value"
                    )],
                    metric_name="metricName",
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a01b3aa74fdc491397c335994204b6560d9c1e84f6619ae6b310c17fd8596b6)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
                check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimensions is not None:
                self._values["dimensions"] = dimensions
            if metric_name is not None:
                self._values["metric_name"] = metric_name
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.DimensionProperty"]]]]:
            '''An array of one or more dimensions to use to define the metric that you want to use.

            For more information, see `Dimensions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Dimension>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metric.html#cfn-applicationsignals-servicelevelobjective-metric-dimensions
            '''
            result = self._values.get("dimensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.DimensionProperty"]]]], result)

        @builtins.property
        def metric_name(self) -> typing.Optional[builtins.str]:
            '''The name of the metric to use.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metric.html#cfn-applicationsignals-servicelevelobjective-metric-metricname
            '''
            result = self._values.get("metric_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the metric.

            For more information, see `Namespaces <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html#Namespace>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metric.html#cfn-applicationsignals-servicelevelobjective-metric-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "metric": "metric",
            "period": "period",
            "stat": "stat",
            "unit": "unit",
        },
    )
    class MetricStatProperty:
        def __init__(
            self,
            *,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            period: typing.Optional[jsii.Number] = None,
            stat: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure defines the metric to be used as the service level indicator, along with the statistics, period, and unit.

            :param metric: The metric to use as the service level indicator, including the metric name, namespace, and dimensions.
            :param period: The granularity, in seconds, to be used for the metric. For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second.
            :param stat: The statistic to use for comparison to the threshold. It can be any CloudWatch statistic or extended statistic. For more information about statistics, see `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html>`_ .
            :param unit: If you omit ``Unit`` then all data that was collected with any unit is returned, along with the corresponding units that were specified when the data was reported to CloudWatch. If you specify a unit, the operation returns only data that was collected with that unit specified. If you specify a unit that does not match the data collected, the results of the operation are null. CloudWatch does not perform unit conversions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricstat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                metric_stat_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                    metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                        dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                            name="name",
                            value="value"
                        )],
                        metric_name="metricName",
                        namespace="namespace"
                    ),
                    period=123,
                    stat="stat",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab64a4bac315a69a6705c1eb549b1ab2edabc1ff26af40a1e8886f26c64fab88)
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument stat", value=stat, expected_type=type_hints["stat"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if metric is not None:
                self._values["metric"] = metric
            if period is not None:
                self._values["period"] = period
            if stat is not None:
                self._values["stat"] = stat
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricProperty"]]:
            '''The metric to use as the service level indicator, including the metric name, namespace, and dimensions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricstat.html#cfn-applicationsignals-servicelevelobjective-metricstat-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricProperty"]], result)

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The granularity, in seconds, to be used for the metric.

            For metrics with regular resolution, a period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60, or any multiple of 60. High-resolution metrics are those metrics stored by a ``PutMetricData`` call that includes a ``StorageResolution`` of 1 second.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricstat.html#cfn-applicationsignals-servicelevelobjective-metricstat-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stat(self) -> typing.Optional[builtins.str]:
            '''The statistic to use for comparison to the threshold.

            It can be any CloudWatch statistic or extended statistic. For more information about statistics, see `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricstat.html#cfn-applicationsignals-servicelevelobjective-metricstat-stat
            '''
            result = self._values.get("stat")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''If you omit ``Unit`` then all data that was collected with any unit is returned, along with the corresponding units that were specified when the data was reported to CloudWatch.

            If you specify a unit, the operation returns only data that was collected with that unit specified. If you specify a unit that does not match the data collected, the results of the operation are null. CloudWatch does not perform unit conversions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-metricstat.html#cfn-applicationsignals-servicelevelobjective-metricstat-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricStatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bad_count_metric": "badCountMetric",
            "good_count_metric": "goodCountMetric",
        },
    )
    class MonitoredRequestCountMetricProperty:
        def __init__(
            self,
            *,
            bad_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            good_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This structure defines the metric that is used as the "good request" or "bad request" value for a request-based SLO.

            This value observed for the metric defined in ``TotalRequestCountMetric`` is divided by the number found for ``MonitoredRequestCountMetric`` to determine the percentage of successful requests that this SLO tracks.

            :param bad_count_metric: If you want to count "bad requests" to determine the percentage of successful requests for this request-based SLO, specify the metric to use as "bad requests" in this structure.
            :param good_count_metric: If you want to count "good requests" to determine the percentage of successful requests for this request-based SLO, specify the metric to use as "good requests" in this structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-monitoredrequestcountmetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                monitored_request_count_metric_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty(
                    bad_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                            metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )],
                    good_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                            metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5f554a7d969871e785473184d35fab1cd3bc33bdbf9e306445257ea3358fb38)
                check_type(argname="argument bad_count_metric", value=bad_count_metric, expected_type=type_hints["bad_count_metric"])
                check_type(argname="argument good_count_metric", value=good_count_metric, expected_type=type_hints["good_count_metric"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bad_count_metric is not None:
                self._values["bad_count_metric"] = bad_count_metric
            if good_count_metric is not None:
                self._values["good_count_metric"] = good_count_metric

        @builtins.property
        def bad_count_metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]]:
            '''If you want to count "bad requests" to determine the percentage of successful requests for this request-based SLO, specify the metric to use as "bad requests" in this structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-monitoredrequestcountmetric.html#cfn-applicationsignals-servicelevelobjective-monitoredrequestcountmetric-badcountmetric
            '''
            result = self._values.get("bad_count_metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]], result)

        @builtins.property
        def good_count_metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]]:
            '''If you want to count "good requests" to determine the percentage of successful requests for this request-based SLO, specify the metric to use as "good requests" in this structure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-monitoredrequestcountmetric.html#cfn-applicationsignals-servicelevelobjective-monitoredrequestcountmetric-goodcountmetric
            '''
            result = self._values.get("good_count_metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonitoredRequestCountMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression"},
    )
    class RecurrenceRuleProperty:
        def __init__(self, *, expression: typing.Optional[builtins.str] = None) -> None:
            '''The recurrence rule for the time exclusion window.

            :param expression: The following two rules are supported:. - rate(value unit) - The value must be a positive integer and the unit can be hour|day|month. - cron - An expression which consists of six fields separated by white spaces: (minutes hours day_of_month month day_of_week year).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-recurrencerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                recurrence_rule_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty(
                    expression="expression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b06122ec1bdacd6a7c15f9c80c4cfb4cf7f59f7fa34da0d18c62897b6c38176f)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The following two rules are supported:.

            - rate(value unit) - The value must be a positive integer and the unit can be hour|day|month.
            - cron - An expression which consists of six fields separated by white spaces: (minutes hours day_of_month month day_of_week year).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-recurrencerule.html#cfn-applicationsignals-servicelevelobjective-recurrencerule-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecurrenceRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dependency_config": "dependencyConfig",
            "key_attributes": "keyAttributes",
            "metric_type": "metricType",
            "monitored_request_count_metric": "monitoredRequestCountMetric",
            "operation_name": "operationName",
            "total_request_count_metric": "totalRequestCountMetric",
        },
    )
    class RequestBasedSliMetricProperty:
        def __init__(
            self,
            *,
            dependency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            metric_type: typing.Optional[builtins.str] = None,
            monitored_request_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            operation_name: typing.Optional[builtins.str] = None,
            total_request_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''This structure contains the information about the metric that is used for a request-based SLO.

            :param dependency_config: Identifies the dependency using the ``DependencyKeyAttributes`` and ``DependencyOperationName`` .
            :param key_attributes: This is a string-to-string map that contains information about the type of object that this SLO is related to. It can include the following fields. - ``Type`` designates the type of object that this SLO is related to. - ``ResourceType`` specifies the type of the resource. This field is used only when the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` . - ``Name`` specifies the name of the object. This is used only if the value of the ``Type`` field is ``Service`` , ``RemoteService`` , or ``AWS::Service`` . - ``Identifier`` identifies the resource objects of this resource. This is used only if the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` . - ``Environment`` specifies the location where this object is hosted, or what it belongs to. - ``AwsAccountId`` allows you to create an SLO for an object that exists in another account.
            :param metric_type: If the SLO monitors either the ``LATENCY`` or ``AVAILABILITY`` metric that Application Signals collects, this field displays which of those metrics is used.
            :param monitored_request_count_metric: Use this structure to define the metric that you want to use as the "good request" or "bad request" value for a request-based SLO. This value observed for the metric defined in ``TotalRequestCountMetric`` will be divided by the number found for ``MonitoredRequestCountMetric`` to determine the percentage of successful requests that this SLO tracks.
            :param operation_name: If the SLO monitors a specific operation of the service, this field displays that operation name.
            :param total_request_count_metric: This structure defines the metric that is used as the "total requests" number for a request-based SLO. The number observed for this metric is divided by the number of "good requests" or "bad requests" that is observed for the metric defined in ``MonitoredRequestCountMetric`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                request_based_sli_metric_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty(
                    dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                        dependency_key_attributes={
                            "dependency_key_attributes_key": "dependencyKeyAttributes"
                        },
                        dependency_operation_name="dependencyOperationName"
                    ),
                    key_attributes={
                        "key_attributes_key": "keyAttributes"
                    },
                    metric_type="metricType",
                    monitored_request_count_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty(
                        bad_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )],
                        good_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    ),
                    operation_name="operationName",
                    total_request_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                            metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fc1fd10c3758112aaee2577a1e9648d252c1800d2a3f030865b662baea544eb)
                check_type(argname="argument dependency_config", value=dependency_config, expected_type=type_hints["dependency_config"])
                check_type(argname="argument key_attributes", value=key_attributes, expected_type=type_hints["key_attributes"])
                check_type(argname="argument metric_type", value=metric_type, expected_type=type_hints["metric_type"])
                check_type(argname="argument monitored_request_count_metric", value=monitored_request_count_metric, expected_type=type_hints["monitored_request_count_metric"])
                check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
                check_type(argname="argument total_request_count_metric", value=total_request_count_metric, expected_type=type_hints["total_request_count_metric"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dependency_config is not None:
                self._values["dependency_config"] = dependency_config
            if key_attributes is not None:
                self._values["key_attributes"] = key_attributes
            if metric_type is not None:
                self._values["metric_type"] = metric_type
            if monitored_request_count_metric is not None:
                self._values["monitored_request_count_metric"] = monitored_request_count_metric
            if operation_name is not None:
                self._values["operation_name"] = operation_name
            if total_request_count_metric is not None:
                self._values["total_request_count_metric"] = total_request_count_metric

        @builtins.property
        def dependency_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty"]]:
            '''Identifies the dependency using the ``DependencyKeyAttributes`` and ``DependencyOperationName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html#cfn-applicationsignals-servicelevelobjective-requestbasedslimetric-dependencyconfig
            '''
            result = self._values.get("dependency_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty"]], result)

        @builtins.property
        def key_attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''This is a string-to-string map that contains information about the type of object that this SLO is related to.

            It can include the following fields.

            - ``Type`` designates the type of object that this SLO is related to.
            - ``ResourceType`` specifies the type of the resource. This field is used only when the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` .
            - ``Name`` specifies the name of the object. This is used only if the value of the ``Type`` field is ``Service`` , ``RemoteService`` , or ``AWS::Service`` .
            - ``Identifier`` identifies the resource objects of this resource. This is used only if the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` .
            - ``Environment`` specifies the location where this object is hosted, or what it belongs to.
            - ``AwsAccountId`` allows you to create an SLO for an object that exists in another account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html#cfn-applicationsignals-servicelevelobjective-requestbasedslimetric-keyattributes
            '''
            result = self._values.get("key_attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def metric_type(self) -> typing.Optional[builtins.str]:
            '''If the SLO monitors either the ``LATENCY`` or ``AVAILABILITY`` metric that Application Signals collects, this field displays which of those metrics is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html#cfn-applicationsignals-servicelevelobjective-requestbasedslimetric-metrictype
            '''
            result = self._values.get("metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def monitored_request_count_metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty"]]:
            '''Use this structure to define the metric that you want to use as the "good request" or "bad request" value for a request-based SLO.

            This value observed for the metric defined in ``TotalRequestCountMetric`` will be divided by the number found for ``MonitoredRequestCountMetric`` to determine the percentage of successful requests that this SLO tracks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html#cfn-applicationsignals-servicelevelobjective-requestbasedslimetric-monitoredrequestcountmetric
            '''
            result = self._values.get("monitored_request_count_metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty"]], result)

        @builtins.property
        def operation_name(self) -> typing.Optional[builtins.str]:
            '''If the SLO monitors a specific operation of the service, this field displays that operation name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html#cfn-applicationsignals-servicelevelobjective-requestbasedslimetric-operationname
            '''
            result = self._values.get("operation_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def total_request_count_metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]]:
            '''This structure defines the metric that is used as the "total requests" number for a request-based SLO.

            The number observed for this metric is divided by the number of "good requests" or "bad requests" that is observed for the metric defined in ``MonitoredRequestCountMetric`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedslimetric.html#cfn-applicationsignals-servicelevelobjective-requestbasedslimetric-totalrequestcountmetric
            '''
            result = self._values.get("total_request_count_metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestBasedSliMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "metric_threshold": "metricThreshold",
            "request_based_sli_metric": "requestBasedSliMetric",
        },
    )
    class RequestBasedSliProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            metric_threshold: typing.Optional[jsii.Number] = None,
            request_based_sli_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This structure contains information about the performance metric that a request-based SLO monitors.

            :param comparison_operator: The arithmetic operation used when comparing the specified metric to the threshold.
            :param metric_threshold: This value is the threshold that the observed metric values of the SLI metric are compared to.
            :param request_based_sli_metric: A structure that contains information about the metric that the SLO monitors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedsli.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                request_based_sli_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty(
                    comparison_operator="comparisonOperator",
                    metric_threshold=123,
                    request_based_sli_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty(
                        dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                            dependency_key_attributes={
                                "dependency_key_attributes_key": "dependencyKeyAttributes"
                            },
                            dependency_operation_name="dependencyOperationName"
                        ),
                        key_attributes={
                            "key_attributes_key": "keyAttributes"
                        },
                        metric_type="metricType",
                        monitored_request_count_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty(
                            bad_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                                account_id="accountId",
                                expression="expression",
                                id="id",
                                metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                    metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                        dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    period=123,
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )],
                            good_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                                account_id="accountId",
                                expression="expression",
                                id="id",
                                metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                    metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                        dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                            name="name",
                                            value="value"
                                        )],
                                        metric_name="metricName",
                                        namespace="namespace"
                                    ),
                                    period=123,
                                    stat="stat",
                                    unit="unit"
                                ),
                                return_data=False
                            )]
                        ),
                        operation_name="operationName",
                        total_request_count_metric=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aca60beebe140c8dadc81d383dd7cd3736a935bd4e6dd17e57fe87ee6a5c6c93)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument metric_threshold", value=metric_threshold, expected_type=type_hints["metric_threshold"])
                check_type(argname="argument request_based_sli_metric", value=request_based_sli_metric, expected_type=type_hints["request_based_sli_metric"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if metric_threshold is not None:
                self._values["metric_threshold"] = metric_threshold
            if request_based_sli_metric is not None:
                self._values["request_based_sli_metric"] = request_based_sli_metric

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The arithmetic operation used when comparing the specified metric to the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedsli.html#cfn-applicationsignals-servicelevelobjective-requestbasedsli-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_threshold(self) -> typing.Optional[jsii.Number]:
            '''This value is the threshold that the observed metric values of the SLI metric are compared to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedsli.html#cfn-applicationsignals-servicelevelobjective-requestbasedsli-metricthreshold
            '''
            result = self._values.get("metric_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def request_based_sli_metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty"]]:
            '''A structure that contains information about the metric that the SLO monitors.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-requestbasedsli.html#cfn-applicationsignals-servicelevelobjective-requestbasedsli-requestbasedslimetric
            '''
            result = self._values.get("request_based_sli_metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequestBasedSliProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty",
        jsii_struct_bases=[],
        name_mapping={"duration": "duration", "duration_unit": "durationUnit"},
    )
    class RollingIntervalProperty:
        def __init__(
            self,
            *,
            duration: typing.Optional[jsii.Number] = None,
            duration_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''If the interval for this SLO is a rolling interval, this structure contains the interval specifications.

            :param duration: Specifies the duration of each rolling interval. For example, if ``Duration`` is ``7`` and ``DurationUnit`` is ``DAY`` , each rolling interval is seven days.
            :param duration_unit: Specifies the rolling interval unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-rollinginterval.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                rolling_interval_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty(
                    duration=123,
                    duration_unit="durationUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e2644b5b96f465eb7471d0bd06cefd5dfaa1b74a16c75ba327ca061064ba204)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument duration_unit", value=duration_unit, expected_type=type_hints["duration_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration is not None:
                self._values["duration"] = duration
            if duration_unit is not None:
                self._values["duration_unit"] = duration_unit

        @builtins.property
        def duration(self) -> typing.Optional[jsii.Number]:
            '''Specifies the duration of each rolling interval.

            For example, if ``Duration`` is ``7`` and ``DurationUnit`` is ``DAY`` , each rolling interval is seven days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-rollinginterval.html#cfn-applicationsignals-servicelevelobjective-rollinginterval-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def duration_unit(self) -> typing.Optional[builtins.str]:
            '''Specifies the rolling interval unit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-rollinginterval.html#cfn-applicationsignals-servicelevelobjective-rollinginterval-durationunit
            '''
            result = self._values.get("duration_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RollingIntervalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.SliMetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dependency_config": "dependencyConfig",
            "key_attributes": "keyAttributes",
            "metric_data_queries": "metricDataQueries",
            "metric_type": "metricType",
            "operation_name": "operationName",
            "period_seconds": "periodSeconds",
            "statistic": "statistic",
        },
    )
    class SliMetricProperty:
        def __init__(
            self,
            *,
            dependency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            metric_type: typing.Optional[builtins.str] = None,
            operation_name: typing.Optional[builtins.str] = None,
            period_seconds: typing.Optional[jsii.Number] = None,
            statistic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to specify the metric to be used for the SLO.

            :param dependency_config: Identifies the dependency using the ``DependencyKeyAttributes`` and ``DependencyOperationName`` .
            :param key_attributes: If this SLO is related to a metric collected by Application Signals, you must use this field to specify which service the SLO metric is related to. To do so, you must specify at least the ``Type`` , ``Name`` , and ``Environment`` attributes. This is a string-to-string map. It can include the following fields. - ``Type`` designates the type of object this is. - ``ResourceType`` specifies the type of the resource. This field is used only when the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` . - ``Name`` specifies the name of the object. This is used only if the value of the ``Type`` field is ``Service`` , ``RemoteService`` , or ``AWS::Service`` . - ``Identifier`` identifies the resource objects of this resource. This is used only if the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` . - ``Environment`` specifies the location where this object is hosted, or what it belongs to.
            :param metric_data_queries: If this SLO monitors a CloudWatch metric or the result of a CloudWatch metric math expression, use this structure to specify that metric or expression.
            :param metric_type: If the SLO is to monitor either the ``LATENCY`` or ``AVAILABILITY`` metric that Application Signals collects, use this field to specify which of those metrics is used.
            :param operation_name: If the SLO is to monitor a specific operation of the service, use this field to specify the name of that operation.
            :param period_seconds: The number of seconds to use as the period for SLO evaluation. Your application's performance is compared to the SLI during each period. For each period, the application is determined to have either achieved or not achieved the necessary performance.
            :param statistic: The statistic to use for comparison to the threshold. It can be any CloudWatch statistic or extended statistic. For more information about statistics, see `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                sli_metric_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliMetricProperty(
                    dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                        dependency_key_attributes={
                            "dependency_key_attributes_key": "dependencyKeyAttributes"
                        },
                        dependency_operation_name="dependencyOperationName"
                    ),
                    key_attributes={
                        "key_attributes_key": "keyAttributes"
                    },
                    metric_data_queries=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                        account_id="accountId",
                        expression="expression",
                        id="id",
                        metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                            metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                    name="name",
                                    value="value"
                                )],
                                metric_name="metricName",
                                namespace="namespace"
                            ),
                            period=123,
                            stat="stat",
                            unit="unit"
                        ),
                        return_data=False
                    )],
                    metric_type="metricType",
                    operation_name="operationName",
                    period_seconds=123,
                    statistic="statistic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8be5fad24d1e40d8dc0911ebff7b3c2d77e0948600e073d40ed48b40723867a0)
                check_type(argname="argument dependency_config", value=dependency_config, expected_type=type_hints["dependency_config"])
                check_type(argname="argument key_attributes", value=key_attributes, expected_type=type_hints["key_attributes"])
                check_type(argname="argument metric_data_queries", value=metric_data_queries, expected_type=type_hints["metric_data_queries"])
                check_type(argname="argument metric_type", value=metric_type, expected_type=type_hints["metric_type"])
                check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
                check_type(argname="argument period_seconds", value=period_seconds, expected_type=type_hints["period_seconds"])
                check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dependency_config is not None:
                self._values["dependency_config"] = dependency_config
            if key_attributes is not None:
                self._values["key_attributes"] = key_attributes
            if metric_data_queries is not None:
                self._values["metric_data_queries"] = metric_data_queries
            if metric_type is not None:
                self._values["metric_type"] = metric_type
            if operation_name is not None:
                self._values["operation_name"] = operation_name
            if period_seconds is not None:
                self._values["period_seconds"] = period_seconds
            if statistic is not None:
                self._values["statistic"] = statistic

        @builtins.property
        def dependency_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty"]]:
            '''Identifies the dependency using the ``DependencyKeyAttributes`` and ``DependencyOperationName`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-dependencyconfig
            '''
            result = self._values.get("dependency_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty"]], result)

        @builtins.property
        def key_attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''If this SLO is related to a metric collected by Application Signals, you must use this field to specify which service the SLO metric is related to.

            To do so, you must specify at least the ``Type`` , ``Name`` , and ``Environment`` attributes.

            This is a string-to-string map. It can include the following fields.

            - ``Type`` designates the type of object this is.
            - ``ResourceType`` specifies the type of the resource. This field is used only when the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` .
            - ``Name`` specifies the name of the object. This is used only if the value of the ``Type`` field is ``Service`` , ``RemoteService`` , or ``AWS::Service`` .
            - ``Identifier`` identifies the resource objects of this resource. This is used only if the value of the ``Type`` field is ``Resource`` or ``AWS::Resource`` .
            - ``Environment`` specifies the location where this object is hosted, or what it belongs to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-keyattributes
            '''
            result = self._values.get("key_attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def metric_data_queries(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]]:
            '''If this SLO monitors a CloudWatch metric or the result of a CloudWatch metric math expression, use this structure to specify that metric or expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-metricdataqueries
            '''
            result = self._values.get("metric_data_queries")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty"]]]], result)

        @builtins.property
        def metric_type(self) -> typing.Optional[builtins.str]:
            '''If the SLO is to monitor either the ``LATENCY`` or ``AVAILABILITY`` metric that Application Signals collects, use this field to specify which of those metrics is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-metrictype
            '''
            result = self._values.get("metric_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def operation_name(self) -> typing.Optional[builtins.str]:
            '''If the SLO is to monitor a specific operation of the service, use this field to specify the name of that operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-operationname
            '''
            result = self._values.get("operation_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def period_seconds(self) -> typing.Optional[jsii.Number]:
            '''The number of seconds to use as the period for SLO evaluation.

            Your application's performance is compared to the SLI during each period. For each period, the application is determined to have either achieved or not achieved the necessary performance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-periodseconds
            '''
            result = self._values.get("period_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def statistic(self) -> typing.Optional[builtins.str]:
            '''The statistic to use for comparison to the threshold.

            It can be any CloudWatch statistic or extended statistic. For more information about statistics, see `CloudWatch statistics definitions <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Statistics-definitions.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-slimetric.html#cfn-applicationsignals-servicelevelobjective-slimetric-statistic
            '''
            result = self._values.get("statistic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SliMetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.SliProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparison_operator": "comparisonOperator",
            "metric_threshold": "metricThreshold",
            "sli_metric": "sliMetric",
        },
    )
    class SliProperty:
        def __init__(
            self,
            *,
            comparison_operator: typing.Optional[builtins.str] = None,
            metric_threshold: typing.Optional[jsii.Number] = None,
            sli_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServiceLevelObjectivePropsMixin.SliMetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''This structure specifies the information about the service and the performance metric that an SLO is to monitor.

            :param comparison_operator: The arithmetic operation to use when comparing the specified metric to the threshold.
            :param metric_threshold: The value that the SLI metric is compared to.
            :param sli_metric: Use this structure to specify the metric to be used for the SLO.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-sli.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                sli_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliProperty(
                    comparison_operator="comparisonOperator",
                    metric_threshold=123,
                    sli_metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.SliMetricProperty(
                        dependency_config=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty(
                            dependency_key_attributes={
                                "dependency_key_attributes_key": "dependencyKeyAttributes"
                            },
                            dependency_operation_name="dependencyOperationName"
                        ),
                        key_attributes={
                            "key_attributes_key": "keyAttributes"
                        },
                        metric_data_queries=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty(
                            account_id="accountId",
                            expression="expression",
                            id="id",
                            metric_stat=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricStatProperty(
                                metric=applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.MetricProperty(
                                    dimensions=[applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.DimensionProperty(
                                        name="name",
                                        value="value"
                                    )],
                                    metric_name="metricName",
                                    namespace="namespace"
                                ),
                                period=123,
                                stat="stat",
                                unit="unit"
                            ),
                            return_data=False
                        )],
                        metric_type="metricType",
                        operation_name="operationName",
                        period_seconds=123,
                        statistic="statistic"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84c9ff82c766da2650d8d055fbeefec43e7fa31d9544178daf8a6fa69798c8e7)
                check_type(argname="argument comparison_operator", value=comparison_operator, expected_type=type_hints["comparison_operator"])
                check_type(argname="argument metric_threshold", value=metric_threshold, expected_type=type_hints["metric_threshold"])
                check_type(argname="argument sli_metric", value=sli_metric, expected_type=type_hints["sli_metric"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparison_operator is not None:
                self._values["comparison_operator"] = comparison_operator
            if metric_threshold is not None:
                self._values["metric_threshold"] = metric_threshold
            if sli_metric is not None:
                self._values["sli_metric"] = sli_metric

        @builtins.property
        def comparison_operator(self) -> typing.Optional[builtins.str]:
            '''The arithmetic operation to use when comparing the specified metric to the threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-sli.html#cfn-applicationsignals-servicelevelobjective-sli-comparisonoperator
            '''
            result = self._values.get("comparison_operator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metric_threshold(self) -> typing.Optional[jsii.Number]:
            '''The value that the SLI metric is compared to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-sli.html#cfn-applicationsignals-servicelevelobjective-sli-metricthreshold
            '''
            result = self._values.get("metric_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def sli_metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.SliMetricProperty"]]:
            '''Use this structure to specify the metric to be used for the SLO.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-sli.html#cfn-applicationsignals-servicelevelobjective-sli-slimetric
            '''
            result = self._values.get("sli_metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServiceLevelObjectivePropsMixin.SliMetricProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SliProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_applicationsignals.mixins.CfnServiceLevelObjectivePropsMixin.WindowProperty",
        jsii_struct_bases=[],
        name_mapping={"duration": "duration", "duration_unit": "durationUnit"},
    )
    class WindowProperty:
        def __init__(
            self,
            *,
            duration: typing.Optional[jsii.Number] = None,
            duration_unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The start and end time of the time exclusion window.

            :param duration: The start and end time of the time exclusion window.
            :param duration_unit: The unit of measurement to use during the time window exclusion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-window.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_applicationsignals import mixins as applicationsignals_mixins
                
                window_property = applicationsignals_mixins.CfnServiceLevelObjectivePropsMixin.WindowProperty(
                    duration=123,
                    duration_unit="durationUnit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42b84a6a215f574aadc86d64cee514f7714aaf1ef08fb1a21c59e6c827927a02)
                check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
                check_type(argname="argument duration_unit", value=duration_unit, expected_type=type_hints["duration_unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration is not None:
                self._values["duration"] = duration
            if duration_unit is not None:
                self._values["duration_unit"] = duration_unit

        @builtins.property
        def duration(self) -> typing.Optional[jsii.Number]:
            '''The start and end time of the time exclusion window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-window.html#cfn-applicationsignals-servicelevelobjective-window-duration
            '''
            result = self._values.get("duration")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def duration_unit(self) -> typing.Optional[builtins.str]:
            '''The unit of measurement to use during the time window exclusion.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationsignals-servicelevelobjective-window.html#cfn-applicationsignals-servicelevelobjective-window-durationunit
            '''
            result = self._values.get("duration_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDiscoveryMixinProps",
    "CfnDiscoveryPropsMixin",
    "CfnGroupingConfigurationMixinProps",
    "CfnGroupingConfigurationPropsMixin",
    "CfnServiceLevelObjectiveMixinProps",
    "CfnServiceLevelObjectivePropsMixin",
]

publication.publish()

def _typecheckingstub__ce182fa4b83be550fb2703fb7e306c0ebb87166173d1b1f1f721d685abbcecb3(
    props: typing.Union[CfnDiscoveryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1216fdacbacf3f63d6cdf0f05eb83c2ea658dd9672d69de03a1c79186f3a1c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6685f4fdf7f7c6005355d0143ad30bb4128338149db31c306d146e22a732c41e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efab68f15db54b8727ad0521e06409801765f795438fa3a3e492f5fe77c365a(
    *,
    grouping_attribute_definitions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupingConfigurationPropsMixin.GroupingAttributeDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bbbc0b86917c09405076c83806f75c09efec66c818d0f22451a21b4bb3a6617(
    props: typing.Union[CfnGroupingConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3548046ad6ac456910fac9c082cd1443ea0eb4d8f8d3860ea53263705e73c98(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3f98e6bb9559c3ffc611afcacc67eb72a82d45c24ea4f0775c927ea31c806c2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d449e3390eaf2afabebe2b309bd4f197d32a9b7219d153a94bd7c7a1c1b59095(
    *,
    default_grouping_value: typing.Optional[builtins.str] = None,
    grouping_name: typing.Optional[builtins.str] = None,
    grouping_source_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0f72afb86742419d109416d6ca5d34dc09dcd54a978cd7e3d675fd372132812(
    *,
    burn_rate_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.BurnRateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    exclusion_windows: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.ExclusionWindowProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    goal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.GoalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    request_based_sli: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.RequestBasedSliProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sli: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.SliProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532520fe3bfa694185d2d8118551fd89af8a023205535283580129d0f87ea92f(
    props: typing.Union[CfnServiceLevelObjectiveMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f64b26621722d8db001a72944e696c6a28eeeb23b5c58dea5215382de579a5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d84e34b3b5521a8650cb001577f4ef3c0b7408241d35cade53a0639de2ba65aa(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbf05d1b15247e01d3f913e139aa65d96e5f09962fb551aab8ba141cfe833f3(
    *,
    look_back_window_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cf90d2302025d5ee551908d6ba24ad374bed0411f8ee2728aa0c6a4011b6c3(
    *,
    duration: typing.Optional[jsii.Number] = None,
    duration_unit: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ff6909a5170c5d77c85cad52b4bf1c6f3db9f0712385c057ca6a696a9124cf(
    *,
    dependency_key_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    dependency_operation_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d464a778a9d6dbe753fd6399d83b0009927fe1cb54c52c35dfac7300443bde(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ec70aac0d5a05def582836bdaac4aa8320b481bae6be35f1b0bd3b5b327b9b(
    *,
    reason: typing.Optional[builtins.str] = None,
    recurrence_rule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.RecurrenceRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.WindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9059b066f6aa2a276f71650260518f53a56953bbdcb2d43adff9de0702face(
    *,
    attainment_goal: typing.Optional[jsii.Number] = None,
    interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.IntervalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    warning_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbea2f1e33354202c940a66e7064de28a00d83167e17dfbc2d7d5e3f44c3264(
    *,
    calendar_interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.CalendarIntervalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rolling_interval: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.RollingIntervalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d157cdc7c931b3b563e06c007167e0c11fc5259c2e32d3b6d9f938eafc0860d1(
    *,
    account_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    metric_stat: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MetricStatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    return_data: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a01b3aa74fdc491397c335994204b6560d9c1e84f6619ae6b310c17fd8596b6(
    *,
    dimensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_name: typing.Optional[builtins.str] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab64a4bac315a69a6705c1eb549b1ab2edabc1ff26af40a1e8886f26c64fab88(
    *,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    period: typing.Optional[jsii.Number] = None,
    stat: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5f554a7d969871e785473184d35fab1cd3bc33bdbf9e306445257ea3358fb38(
    *,
    bad_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    good_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06122ec1bdacd6a7c15f9c80c4cfb4cf7f59f7fa34da0d18c62897b6c38176f(
    *,
    expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc1fd10c3758112aaee2577a1e9648d252c1800d2a3f030865b662baea544eb(
    *,
    dependency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    metric_type: typing.Optional[builtins.str] = None,
    monitored_request_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MonitoredRequestCountMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    operation_name: typing.Optional[builtins.str] = None,
    total_request_count_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca60beebe140c8dadc81d383dd7cd3736a935bd4e6dd17e57fe87ee6a5c6c93(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    metric_threshold: typing.Optional[jsii.Number] = None,
    request_based_sli_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.RequestBasedSliMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2644b5b96f465eb7471d0bd06cefd5dfaa1b74a16c75ba327ca061064ba204(
    *,
    duration: typing.Optional[jsii.Number] = None,
    duration_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be5fad24d1e40d8dc0911ebff7b3c2d77e0948600e073d40ed48b40723867a0(
    *,
    dependency_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.DependencyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    metric_data_queries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.MetricDataQueryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    metric_type: typing.Optional[builtins.str] = None,
    operation_name: typing.Optional[builtins.str] = None,
    period_seconds: typing.Optional[jsii.Number] = None,
    statistic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84c9ff82c766da2650d8d055fbeefec43e7fa31d9544178daf8a6fa69798c8e7(
    *,
    comparison_operator: typing.Optional[builtins.str] = None,
    metric_threshold: typing.Optional[jsii.Number] = None,
    sli_metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServiceLevelObjectivePropsMixin.SliMetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b84a6a215f574aadc86d64cee514f7714aaf1ef08fb1a21c59e6c827927a02(
    *,
    duration: typing.Optional[jsii.Number] = None,
    duration_unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
