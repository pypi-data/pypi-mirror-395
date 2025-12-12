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
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "destinations": "destinations",
        "name": "name",
        "source": "source",
        "tags": "tags",
    },
)
class CfnChannelMixinProps:
    def __init__(
        self,
        *,
        destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnChannelPropsMixin.DestinationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnChannelPropsMixin.

        :param destinations: One or more event data stores to which events arriving through a channel will be logged.
        :param name: The name of the channel.
        :param source: The name of the partner or external event source. You cannot change this name after you create the channel. A maximum of one channel is allowed per source. A source can be either ``Custom`` for all valid non- AWS events, or the name of a partner event source. For information about the source names for available partners, see `Additional information about integration partners <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-event-data-store-integration.html#cloudtrail-lake-partner-information>`_ in the CloudTrail User Guide.
        :param tags: A list of tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
            
            cfn_channel_mixin_props = cloudtrail_mixins.CfnChannelMixinProps(
                destinations=[cloudtrail_mixins.CfnChannelPropsMixin.DestinationProperty(
                    location="location",
                    type="type"
                )],
                name="name",
                source="source",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad43459a37c8aff023f255accc652dd44b01ab90262674bbbeba78a00c89adab)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destinations is not None:
            self._values["destinations"] = destinations
        if name is not None:
            self._values["name"] = name
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destinations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.DestinationProperty"]]]]:
        '''One or more event data stores to which events arriving through a channel will be logged.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-channel.html#cfn-cloudtrail-channel-destinations
        '''
        result = self._values.get("destinations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnChannelPropsMixin.DestinationProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-channel.html#cfn-cloudtrail-channel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The name of the partner or external event source.

        You cannot change this name after you create the channel. A maximum of one channel is allowed per source.

        A source can be either ``Custom`` for all valid non- AWS events, or the name of a partner event source. For information about the source names for available partners, see `Additional information about integration partners <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-event-data-store-integration.html#cloudtrail-lake-partner-information>`_ in the CloudTrail User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-channel.html#cfn-cloudtrail-channel-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-channel.html#cfn-cloudtrail-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnChannelPropsMixin",
):
    '''Contains information about a returned CloudTrail channel.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-channel.html
    :cloudformationResource: AWS::CloudTrail::Channel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
        
        cfn_channel_props_mixin = cloudtrail_mixins.CfnChannelPropsMixin(cloudtrail_mixins.CfnChannelMixinProps(
            destinations=[cloudtrail_mixins.CfnChannelPropsMixin.DestinationProperty(
                location="location",
                type="type"
            )],
            name="name",
            source="source",
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
        props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudTrail::Channel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c68576b71d3c13e6858249bb0eb4088ef4dc646589e3c83364b4a6d02db95c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__adbd3f37c9a1fb6409ee75b7912e163dd291e1477a5f7e6bff8e05a89b7f722d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27c1aeb1bdb23445f8124da4cacdad4e77e57cf2e2bea90b3c07d930b2362592)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChannelMixinProps:
        return typing.cast(CfnChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnChannelPropsMixin.DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"location": "location", "type": "type"},
    )
    class DestinationProperty:
        def __init__(
            self,
            *,
            location: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the destination receiving events.

            :param location: For channels used for a CloudTrail Lake integration, the location is the ARN of an event data store that receives events from a channel. For service-linked channels, the location is the name of the AWS service.
            :param type: The type of destination for events arriving from a channel. For channels used for a CloudTrail Lake integration, the value is ``EVENT_DATA_STORE`` . For service-linked channels, the value is ``AWS_SERVICE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-channel-destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                destination_property = cloudtrail_mixins.CfnChannelPropsMixin.DestinationProperty(
                    location="location",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96e70887fbff8644363731ca7f8a4f723016fe8c757677f959be3c560c7aabb3)
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location is not None:
                self._values["location"] = location
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def location(self) -> typing.Optional[builtins.str]:
            '''For channels used for a CloudTrail Lake integration, the location is the ARN of an event data store that receives events from a channel.

            For service-linked channels, the location is the name of the AWS service.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-channel-destination.html#cfn-cloudtrail-channel-destination-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of destination for events arriving from a channel.

            For channels used for a CloudTrail Lake integration, the value is ``EVENT_DATA_STORE`` . For service-linked channels, the value is ``AWS_SERVICE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-channel-destination.html#cfn-cloudtrail-channel-destination-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnDashboardMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "refresh_schedule": "refreshSchedule",
        "tags": "tags",
        "termination_protection_enabled": "terminationProtectionEnabled",
        "widgets": "widgets",
    },
)
class CfnDashboardMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        refresh_schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDashboardPropsMixin.RefreshScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        widgets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDashboardPropsMixin.WidgetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnDashboardPropsMixin.

        :param name: The name of the dashboard. The name must be unique to your account. To create the Highlights dashboard, the name must be ``AWSCloudTrail-Highlights`` .
        :param refresh_schedule: The schedule for a dashboard refresh.
        :param tags: A list of tags.
        :param termination_protection_enabled: Specifies whether termination protection is enabled for the dashboard. If termination protection is enabled, you cannot delete the dashboard until termination protection is disabled.
        :param widgets: An array of widgets for a custom dashboard. A custom dashboard can have a maximum of ten widgets. You do not need to specify widgets for the Highlights dashboard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
            
            cfn_dashboard_mixin_props = cloudtrail_mixins.CfnDashboardMixinProps(
                name="name",
                refresh_schedule=cloudtrail_mixins.CfnDashboardPropsMixin.RefreshScheduleProperty(
                    frequency=cloudtrail_mixins.CfnDashboardPropsMixin.FrequencyProperty(
                        unit="unit",
                        value=123
                    ),
                    status="status",
                    time_of_day="timeOfDay"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                termination_protection_enabled=False,
                widgets=[cloudtrail_mixins.CfnDashboardPropsMixin.WidgetProperty(
                    query_parameters=["queryParameters"],
                    query_statement="queryStatement",
                    view_properties={
                        "view_properties_key": "viewProperties"
                    }
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b564f92eab90572c9135808e8dc6a5cbe342e67e9981112e23ebb5ea1aeb5106)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument refresh_schedule", value=refresh_schedule, expected_type=type_hints["refresh_schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection_enabled", value=termination_protection_enabled, expected_type=type_hints["termination_protection_enabled"])
            check_type(argname="argument widgets", value=widgets, expected_type=type_hints["widgets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if refresh_schedule is not None:
            self._values["refresh_schedule"] = refresh_schedule
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection_enabled is not None:
            self._values["termination_protection_enabled"] = termination_protection_enabled
        if widgets is not None:
            self._values["widgets"] = widgets

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the dashboard. The name must be unique to your account.

        To create the Highlights dashboard, the name must be ``AWSCloudTrail-Highlights`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html#cfn-cloudtrail-dashboard-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def refresh_schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDashboardPropsMixin.RefreshScheduleProperty"]]:
        '''The schedule for a dashboard refresh.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html#cfn-cloudtrail-dashboard-refreshschedule
        '''
        result = self._values.get("refresh_schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDashboardPropsMixin.RefreshScheduleProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html#cfn-cloudtrail-dashboard-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def termination_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether termination protection is enabled for the dashboard.

        If termination protection is enabled, you cannot delete the dashboard until termination protection is disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html#cfn-cloudtrail-dashboard-terminationprotectionenabled
        '''
        result = self._values.get("termination_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def widgets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDashboardPropsMixin.WidgetProperty"]]]]:
        '''An array of widgets for a custom dashboard. A custom dashboard can have a maximum of ten widgets.

        You do not need to specify widgets for the Highlights dashboard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html#cfn-cloudtrail-dashboard-widgets
        '''
        result = self._values.get("widgets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDashboardPropsMixin.WidgetProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDashboardPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnDashboardPropsMixin",
):
    '''Creates a custom dashboard or the Highlights dashboard.

    - *Custom dashboards* - Custom dashboards allow you to query events in any event data store type. You can add up to 10 widgets to a custom dashboard. You can manually refresh a custom dashboard, or you can set a refresh schedule.
    - *Highlights dashboard* - You can create the Highlights dashboard to see a summary of key user activities and API usage across all your event data stores. CloudTrail Lake manages the Highlights dashboard and refreshes the dashboard every 6 hours. To create the Highlights dashboard, you must set and enable a refresh schedule.

    CloudTrail runs queries to populate the dashboard's widgets during a manual or scheduled refresh. CloudTrail must be granted permissions to run the ``StartQuery`` operation on your behalf. To provide permissions, run the ``PutResourcePolicy`` operation to attach a resource-based policy to each event data store. For more information, see `Example: Allow CloudTrail to run queries to populate a dashboard <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/security_iam_resource-based-policy-examples.html#security_iam_resource-based-policy-examples-eds-dashboard>`_ in the *AWS CloudTrail User Guide* .

    To set a refresh schedule, CloudTrail must be granted permissions to run the ``StartDashboardRefresh`` operation to refresh the dashboard on your behalf. To provide permissions, run the ``PutResourcePolicy`` operation to attach a resource-based policy to the dashboard. For more information, see `Resource-based policy example for a dashboard <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/security_iam_resource-based-policy-examples.html#security_iam_resource-based-policy-examples-dashboards>`_ in the *AWS CloudTrail User Guide* .

    For more information about dashboards, see `CloudTrail Lake dashboards <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-dashboard.html>`_ in the *AWS CloudTrail User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-dashboard.html
    :cloudformationResource: AWS::CloudTrail::Dashboard
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
        
        cfn_dashboard_props_mixin = cloudtrail_mixins.CfnDashboardPropsMixin(cloudtrail_mixins.CfnDashboardMixinProps(
            name="name",
            refresh_schedule=cloudtrail_mixins.CfnDashboardPropsMixin.RefreshScheduleProperty(
                frequency=cloudtrail_mixins.CfnDashboardPropsMixin.FrequencyProperty(
                    unit="unit",
                    value=123
                ),
                status="status",
                time_of_day="timeOfDay"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            termination_protection_enabled=False,
            widgets=[cloudtrail_mixins.CfnDashboardPropsMixin.WidgetProperty(
                query_parameters=["queryParameters"],
                query_statement="queryStatement",
                view_properties={
                    "view_properties_key": "viewProperties"
                }
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDashboardMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudTrail::Dashboard``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66db4f4b6ad9e14975931e6e8581f96f8982d1dd90a51e6c555f24b55d155fcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e04effb76cabdab6d773fabdc4570d08ba655f8842e6fbb5a32de1e56dbea46f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2cb84030858ae3db29af27ee44026ea9f4ee1c8b86b70f3947a33e5f71dd898)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDashboardMixinProps:
        return typing.cast(CfnDashboardMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnDashboardPropsMixin.FrequencyProperty",
        jsii_struct_bases=[],
        name_mapping={"unit": "unit", "value": "value"},
    )
    class FrequencyProperty:
        def __init__(
            self,
            *,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the frequency for a dashboard refresh schedule.

            For a custom dashboard, you can schedule a refresh for every 1, 6, 12, or 24 hours, or every day.

            :param unit: The unit to use for the refresh. For custom dashboards, the unit can be ``HOURS`` or ``DAYS`` . For the Highlights dashboard, the ``Unit`` must be ``HOURS`` .
            :param value: The value for the refresh schedule. For custom dashboards, the following values are valid when the unit is ``HOURS`` : ``1`` , ``6`` , ``12`` , ``24`` For custom dashboards, the only valid value when the unit is ``DAYS`` is ``1`` . For the Highlights dashboard, the ``Value`` must be ``6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-frequency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                frequency_property = cloudtrail_mixins.CfnDashboardPropsMixin.FrequencyProperty(
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c5836ff4412c4af859fb0cd6a4152d09d61996dc7a57b3f475c8cdfa66ca680)
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit to use for the refresh.

            For custom dashboards, the unit can be ``HOURS`` or ``DAYS`` .

            For the Highlights dashboard, the ``Unit`` must be ``HOURS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-frequency.html#cfn-cloudtrail-dashboard-frequency-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value for the refresh schedule.

            For custom dashboards, the following values are valid when the unit is ``HOURS`` : ``1`` , ``6`` , ``12`` , ``24``

            For custom dashboards, the only valid value when the unit is ``DAYS`` is ``1`` .

            For the Highlights dashboard, the ``Value`` must be ``6`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-frequency.html#cfn-cloudtrail-dashboard-frequency-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrequencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnDashboardPropsMixin.RefreshScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "frequency": "frequency",
            "status": "status",
            "time_of_day": "timeOfDay",
        },
    )
    class RefreshScheduleProperty:
        def __init__(
            self,
            *,
            frequency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDashboardPropsMixin.FrequencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            status: typing.Optional[builtins.str] = None,
            time_of_day: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The schedule for a dashboard refresh.

            :param frequency: The frequency at which you want the dashboard refreshed.
            :param status: Specifies whether the refresh schedule is enabled. Set the value to ``ENABLED`` to enable the refresh schedule, or to ``DISABLED`` to turn off the refresh schedule.
            :param time_of_day: The time of day in UTC to run the schedule; for hourly only refer to minutes; default is 00:00.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-refreshschedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                refresh_schedule_property = cloudtrail_mixins.CfnDashboardPropsMixin.RefreshScheduleProperty(
                    frequency=cloudtrail_mixins.CfnDashboardPropsMixin.FrequencyProperty(
                        unit="unit",
                        value=123
                    ),
                    status="status",
                    time_of_day="timeOfDay"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97458b5d40a7428dd5bb5aef0f3bb500121c5be50cef391d39691fd4c17adfd9)
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
                check_type(argname="argument time_of_day", value=time_of_day, expected_type=type_hints["time_of_day"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if frequency is not None:
                self._values["frequency"] = frequency
            if status is not None:
                self._values["status"] = status
            if time_of_day is not None:
                self._values["time_of_day"] = time_of_day

        @builtins.property
        def frequency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDashboardPropsMixin.FrequencyProperty"]]:
            '''The frequency at which you want the dashboard refreshed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-refreshschedule.html#cfn-cloudtrail-dashboard-refreshschedule-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDashboardPropsMixin.FrequencyProperty"]], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the refresh schedule is enabled.

            Set the value to ``ENABLED`` to enable the refresh schedule, or to ``DISABLED`` to turn off the refresh schedule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-refreshschedule.html#cfn-cloudtrail-dashboard-refreshschedule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def time_of_day(self) -> typing.Optional[builtins.str]:
            '''The time of day in UTC to run the schedule;

            for hourly only refer to minutes; default is 00:00.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-refreshschedule.html#cfn-cloudtrail-dashboard-refreshschedule-timeofday
            '''
            result = self._values.get("time_of_day")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RefreshScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnDashboardPropsMixin.WidgetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_parameters": "queryParameters",
            "query_statement": "queryStatement",
            "view_properties": "viewProperties",
        },
    )
    class WidgetProperty:
        def __init__(
            self,
            *,
            query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
            query_statement: typing.Optional[builtins.str] = None,
            view_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains information about a widget on a CloudTrail Lake dashboard.

            :param query_parameters: The optional query parameters. The following query parameters are valid: ``$StartTime$`` , ``$EndTime$`` , and ``$Period$`` .
            :param query_statement: The query statement for the widget. For custom dashboard widgets, you can query across multiple event data stores as long as all event data stores exist in your account. .. epigraph:: When a query uses ``?`` with ``eventTime`` , ``?`` must be surrounded by single quotes as follows: ``'?'`` .
            :param view_properties: The view properties for the widget. For more information about view properties, see `View properties for widgets <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-widget-properties.html>`_ in the *AWS CloudTrail User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-widget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                widget_property = cloudtrail_mixins.CfnDashboardPropsMixin.WidgetProperty(
                    query_parameters=["queryParameters"],
                    query_statement="queryStatement",
                    view_properties={
                        "view_properties_key": "viewProperties"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa6ed7a2242902d3d0d9b1b61cd4ba12b65ffc059021b508c732a343d86abb5d)
                check_type(argname="argument query_parameters", value=query_parameters, expected_type=type_hints["query_parameters"])
                check_type(argname="argument query_statement", value=query_statement, expected_type=type_hints["query_statement"])
                check_type(argname="argument view_properties", value=view_properties, expected_type=type_hints["view_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query_parameters is not None:
                self._values["query_parameters"] = query_parameters
            if query_statement is not None:
                self._values["query_statement"] = query_statement
            if view_properties is not None:
                self._values["view_properties"] = view_properties

        @builtins.property
        def query_parameters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The optional query parameters.

            The following query parameters are valid: ``$StartTime$`` , ``$EndTime$`` , and ``$Period$`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-widget.html#cfn-cloudtrail-dashboard-widget-queryparameters
            '''
            result = self._values.get("query_parameters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def query_statement(self) -> typing.Optional[builtins.str]:
            '''The query statement for the widget.

            For custom dashboard widgets, you can query across multiple event data stores as long as all event data stores exist in your account.
            .. epigraph::

               When a query uses ``?`` with ``eventTime`` , ``?`` must be surrounded by single quotes as follows: ``'?'`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-widget.html#cfn-cloudtrail-dashboard-widget-querystatement
            '''
            result = self._values.get("query_statement")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def view_properties(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The view properties for the widget.

            For more information about view properties, see `View properties for widgets <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-widget-properties.html>`_ in the *AWS CloudTrail User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-dashboard-widget.html#cfn-cloudtrail-dashboard-widget-viewproperties
            '''
            result = self._values.get("view_properties")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WidgetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnEventDataStoreMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_event_selectors": "advancedEventSelectors",
        "billing_mode": "billingMode",
        "context_key_selectors": "contextKeySelectors",
        "federation_enabled": "federationEnabled",
        "federation_role_arn": "federationRoleArn",
        "ingestion_enabled": "ingestionEnabled",
        "insights_destination": "insightsDestination",
        "insight_selectors": "insightSelectors",
        "kms_key_id": "kmsKeyId",
        "max_event_size": "maxEventSize",
        "multi_region_enabled": "multiRegionEnabled",
        "name": "name",
        "organization_enabled": "organizationEnabled",
        "retention_period": "retentionPeriod",
        "tags": "tags",
        "termination_protection_enabled": "terminationProtectionEnabled",
    },
)
class CfnEventDataStoreMixinProps:
    def __init__(
        self,
        *,
        advanced_event_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        billing_mode: typing.Optional[builtins.str] = None,
        context_key_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventDataStorePropsMixin.ContextKeySelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        federation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        federation_role_arn: typing.Optional[builtins.str] = None,
        ingestion_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        insights_destination: typing.Optional[builtins.str] = None,
        insight_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventDataStorePropsMixin.InsightSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        max_event_size: typing.Optional[builtins.str] = None,
        multi_region_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        organization_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnEventDataStorePropsMixin.

        :param advanced_event_selectors: The advanced event selectors to use to select the events for the data store. You can configure up to five advanced event selectors for each event data store. For more information about how to use advanced event selectors to log CloudTrail events, see `Log events by using advanced event selectors <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-advanced>`_ in the CloudTrail User Guide. For more information about how to use advanced event selectors to include AWS Config configuration items in your event data store, see `Create an event data store for AWS Config configuration items <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-eds-cli.html#lake-cli-create-eds-config>`_ in the CloudTrail User Guide. For more information about how to use advanced event selectors to include events outside of AWS events in your event data store, see `Create an integration to log events from outside AWS <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-integrations-cli.html#lake-cli-create-integration>`_ in the CloudTrail User Guide.
        :param billing_mode: The billing mode for the event data store determines the cost for ingesting events and the default and maximum retention period for the event data store. The following are the possible values: - ``EXTENDABLE_RETENTION_PRICING`` - This billing mode is generally recommended if you want a flexible retention period of up to 3653 days (about 10 years). The default retention period for this billing mode is 366 days. - ``FIXED_RETENTION_PRICING`` - This billing mode is recommended if you expect to ingest more than 25 TB of event data per month and need a retention period of up to 2557 days (about 7 years). The default retention period for this billing mode is 2557 days. The default value is ``EXTENDABLE_RETENTION_PRICING`` . For more information about CloudTrail pricing, see `AWS CloudTrail Pricing <https://docs.aws.amazon.com/cloudtrail/pricing/>`_ and `Managing CloudTrail Lake costs <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-manage-costs.html>`_ .
        :param context_key_selectors: The list of context key selectors that are configured for the event data store.
        :param federation_enabled: Indicates if `Lake query federation <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-federation.html>`_ is enabled. By default, Lake query federation is disabled. You cannot delete an event data store if Lake query federation is enabled.
        :param federation_role_arn: If Lake query federation is enabled, provides the ARN of the federation role used to access the resources for the federated event data store. The federation role must exist in your account and provide the `required minimum permissions <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-federation.html#query-federation-permissions-role>`_ .
        :param ingestion_enabled: Specifies whether the event data store should start ingesting live events. The default is true.
        :param insights_destination: The ARN (or ID suffix of the ARN) of the destination event data store that logs Insights events. For more information, see `Create an event data store for CloudTrail Insights events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-event-data-store-insights.html>`_ .
        :param insight_selectors: A JSON string that contains the Insights types you want to log on an event data store. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types. The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume. The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.
        :param kms_key_id: Specifies the AWS key ID to use to encrypt the events delivered by CloudTrail. The value can be an alias name prefixed by ``alias/`` , a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier. .. epigraph:: Disabling or deleting the KMS key, or removing CloudTrail permissions on the key, prevents CloudTrail from logging events to the event data store, and prevents users from querying the data in the event data store that was encrypted with the key. After you associate an event data store with a KMS key, the KMS key cannot be removed or changed. Before you disable or delete a KMS key that you are using with an event data store, delete or back up your event data store. CloudTrail also supports AWS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . Examples: - ``alias/MyAliasName`` - ``arn:aws:kms:us-east-2:123456789012:alias/MyAliasName`` - ``arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012`` - ``12345678-1234-1234-1234-123456789012``
        :param max_event_size: The maximum allowed size for events to be stored in the specified event data store. If you are using context key selectors, MaxEventSize must be set to Large.
        :param multi_region_enabled: Specifies whether the event data store includes events from all Regions, or only from the Region in which the event data store is created.
        :param name: The name of the event data store.
        :param organization_enabled: Specifies whether an event data store collects events logged for an organization in AWS Organizations .
        :param retention_period: The retention period of the event data store, in days. If ``BillingMode`` is set to ``EXTENDABLE_RETENTION_PRICING`` , you can set a retention period of up to 3653 days, the equivalent of 10 years. If ``BillingMode`` is set to ``FIXED_RETENTION_PRICING`` , you can set a retention period of up to 2557 days, the equivalent of seven years. CloudTrail Lake determines whether to retain an event by checking if the ``eventTime`` of the event is within the specified retention period. For example, if you set a retention period of 90 days, CloudTrail will remove events when the ``eventTime`` is older than 90 days. .. epigraph:: If you plan to copy trail events to this event data store, we recommend that you consider both the age of the events that you want to copy as well as how long you want to keep the copied events in your event data store. For example, if you copy trail events that are 5 years old and specify a retention period of 7 years, the event data store will retain those events for two years.
        :param tags: A list of tags.
        :param termination_protection_enabled: Specifies whether termination protection is enabled for the event data store. If termination protection is enabled, you cannot delete the event data store until termination protection is disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
            
            cfn_event_data_store_mixin_props = cloudtrail_mixins.CfnEventDataStoreMixinProps(
                advanced_event_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty(
                    field_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty(
                        ends_with=["endsWith"],
                        equal_to=["equalTo"],
                        field="field",
                        not_ends_with=["notEndsWith"],
                        not_equals=["notEquals"],
                        not_starts_with=["notStartsWith"],
                        starts_with=["startsWith"]
                    )],
                    name="name"
                )],
                billing_mode="billingMode",
                context_key_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.ContextKeySelectorProperty(
                    equal_to=["equalTo"],
                    type="type"
                )],
                federation_enabled=False,
                federation_role_arn="federationRoleArn",
                ingestion_enabled=False,
                insights_destination="insightsDestination",
                insight_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.InsightSelectorProperty(
                    insight_type="insightType"
                )],
                kms_key_id="kmsKeyId",
                max_event_size="maxEventSize",
                multi_region_enabled=False,
                name="name",
                organization_enabled=False,
                retention_period=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                termination_protection_enabled=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe110452f971dadfb45eea1e16ca4c0779b7ed7d58a1f36103725f97425ac140)
            check_type(argname="argument advanced_event_selectors", value=advanced_event_selectors, expected_type=type_hints["advanced_event_selectors"])
            check_type(argname="argument billing_mode", value=billing_mode, expected_type=type_hints["billing_mode"])
            check_type(argname="argument context_key_selectors", value=context_key_selectors, expected_type=type_hints["context_key_selectors"])
            check_type(argname="argument federation_enabled", value=federation_enabled, expected_type=type_hints["federation_enabled"])
            check_type(argname="argument federation_role_arn", value=federation_role_arn, expected_type=type_hints["federation_role_arn"])
            check_type(argname="argument ingestion_enabled", value=ingestion_enabled, expected_type=type_hints["ingestion_enabled"])
            check_type(argname="argument insights_destination", value=insights_destination, expected_type=type_hints["insights_destination"])
            check_type(argname="argument insight_selectors", value=insight_selectors, expected_type=type_hints["insight_selectors"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument max_event_size", value=max_event_size, expected_type=type_hints["max_event_size"])
            check_type(argname="argument multi_region_enabled", value=multi_region_enabled, expected_type=type_hints["multi_region_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument organization_enabled", value=organization_enabled, expected_type=type_hints["organization_enabled"])
            check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection_enabled", value=termination_protection_enabled, expected_type=type_hints["termination_protection_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_event_selectors is not None:
            self._values["advanced_event_selectors"] = advanced_event_selectors
        if billing_mode is not None:
            self._values["billing_mode"] = billing_mode
        if context_key_selectors is not None:
            self._values["context_key_selectors"] = context_key_selectors
        if federation_enabled is not None:
            self._values["federation_enabled"] = federation_enabled
        if federation_role_arn is not None:
            self._values["federation_role_arn"] = federation_role_arn
        if ingestion_enabled is not None:
            self._values["ingestion_enabled"] = ingestion_enabled
        if insights_destination is not None:
            self._values["insights_destination"] = insights_destination
        if insight_selectors is not None:
            self._values["insight_selectors"] = insight_selectors
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if max_event_size is not None:
            self._values["max_event_size"] = max_event_size
        if multi_region_enabled is not None:
            self._values["multi_region_enabled"] = multi_region_enabled
        if name is not None:
            self._values["name"] = name
        if organization_enabled is not None:
            self._values["organization_enabled"] = organization_enabled
        if retention_period is not None:
            self._values["retention_period"] = retention_period
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection_enabled is not None:
            self._values["termination_protection_enabled"] = termination_protection_enabled

    @builtins.property
    def advanced_event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty"]]]]:
        '''The advanced event selectors to use to select the events for the data store.

        You can configure up to five advanced event selectors for each event data store.

        For more information about how to use advanced event selectors to log CloudTrail events, see `Log events by using advanced event selectors <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#creating-data-event-selectors-advanced>`_ in the CloudTrail User Guide.

        For more information about how to use advanced event selectors to include AWS Config configuration items in your event data store, see `Create an event data store for AWS Config configuration items <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-eds-cli.html#lake-cli-create-eds-config>`_ in the CloudTrail User Guide.

        For more information about how to use advanced event selectors to include events outside of AWS events in your event data store, see `Create an integration to log events from outside AWS <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/lake-integrations-cli.html#lake-cli-create-integration>`_ in the CloudTrail User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-advancedeventselectors
        '''
        result = self._values.get("advanced_event_selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty"]]]], result)

    @builtins.property
    def billing_mode(self) -> typing.Optional[builtins.str]:
        '''The billing mode for the event data store determines the cost for ingesting events and the default and maximum retention period for the event data store.

        The following are the possible values:

        - ``EXTENDABLE_RETENTION_PRICING`` - This billing mode is generally recommended if you want a flexible retention period of up to 3653 days (about 10 years). The default retention period for this billing mode is 366 days.
        - ``FIXED_RETENTION_PRICING`` - This billing mode is recommended if you expect to ingest more than 25 TB of event data per month and need a retention period of up to 2557 days (about 7 years). The default retention period for this billing mode is 2557 days.

        The default value is ``EXTENDABLE_RETENTION_PRICING`` .

        For more information about CloudTrail pricing, see `AWS CloudTrail Pricing <https://docs.aws.amazon.com/cloudtrail/pricing/>`_ and `Managing CloudTrail Lake costs <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-manage-costs.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-billingmode
        '''
        result = self._values.get("billing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_key_selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.ContextKeySelectorProperty"]]]]:
        '''The list of context key selectors that are configured for the event data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-contextkeyselectors
        '''
        result = self._values.get("context_key_selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.ContextKeySelectorProperty"]]]], result)

    @builtins.property
    def federation_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates if `Lake query federation <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-federation.html>`_ is enabled. By default, Lake query federation is disabled. You cannot delete an event data store if Lake query federation is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-federationenabled
        '''
        result = self._values.get("federation_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def federation_role_arn(self) -> typing.Optional[builtins.str]:
        '''If Lake query federation is enabled, provides the ARN of the federation role used to access the resources for the federated event data store.

        The federation role must exist in your account and provide the `required minimum permissions <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-federation.html#query-federation-permissions-role>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-federationrolearn
        '''
        result = self._values.get("federation_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingestion_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the event data store should start ingesting live events.

        The default is true.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-ingestionenabled
        '''
        result = self._values.get("ingestion_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def insights_destination(self) -> typing.Optional[builtins.str]:
        '''The ARN (or ID suffix of the ARN) of the destination event data store that logs Insights events.

        For more information, see `Create an event data store for CloudTrail Insights events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-event-data-store-insights.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-insightsdestination
        '''
        result = self._values.get("insights_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insight_selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.InsightSelectorProperty"]]]]:
        '''A JSON string that contains the Insights types you want to log on an event data store.

        ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types.

        The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume.

        The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-insightselectors
        '''
        result = self._values.get("insight_selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.InsightSelectorProperty"]]]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the AWS  key ID to use to encrypt the events delivered by CloudTrail.

        The value can be an alias name prefixed by ``alias/`` , a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier.
        .. epigraph::

           Disabling or deleting the KMS key, or removing CloudTrail permissions on the key, prevents CloudTrail from logging events to the event data store, and prevents users from querying the data in the event data store that was encrypted with the key. After you associate an event data store with a KMS key, the KMS key cannot be removed or changed. Before you disable or delete a KMS key that you are using with an event data store, delete or back up your event data store.

        CloudTrail also supports AWS  multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        Examples:

        - ``alias/MyAliasName``
        - ``arn:aws:kms:us-east-2:123456789012:alias/MyAliasName``
        - ``arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012``
        - ``12345678-1234-1234-1234-123456789012``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_event_size(self) -> typing.Optional[builtins.str]:
        '''The maximum allowed size for events to be stored in the specified event data store.

        If you are using context key selectors, MaxEventSize must be set to Large.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-maxeventsize
        '''
        result = self._values.get("max_event_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the event data store includes events from all Regions, or only from the Region in which the event data store is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-multiregionenabled
        '''
        result = self._values.get("multi_region_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the event data store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def organization_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether an event data store collects events logged for an organization in AWS Organizations .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-organizationenabled
        '''
        result = self._values.get("organization_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def retention_period(self) -> typing.Optional[jsii.Number]:
        '''The retention period of the event data store, in days.

        If ``BillingMode`` is set to ``EXTENDABLE_RETENTION_PRICING`` , you can set a retention period of up to 3653 days, the equivalent of 10 years. If ``BillingMode`` is set to ``FIXED_RETENTION_PRICING`` , you can set a retention period of up to 2557 days, the equivalent of seven years.

        CloudTrail Lake determines whether to retain an event by checking if the ``eventTime`` of the event is within the specified retention period. For example, if you set a retention period of 90 days, CloudTrail will remove events when the ``eventTime`` is older than 90 days.
        .. epigraph::

           If you plan to copy trail events to this event data store, we recommend that you consider both the age of the events that you want to copy as well as how long you want to keep the copied events in your event data store. For example, if you copy trail events that are 5 years old and specify a retention period of 7 years, the event data store will retain those events for two years.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-retentionperiod
        '''
        result = self._values.get("retention_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def termination_protection_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether termination protection is enabled for the event data store.

        If termination protection is enabled, you cannot delete the event data store until termination protection is disabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html#cfn-cloudtrail-eventdatastore-terminationprotectionenabled
        '''
        result = self._values.get("termination_protection_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventDataStoreMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEventDataStorePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnEventDataStorePropsMixin",
):
    '''Creates a new event data store.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-eventdatastore.html
    :cloudformationResource: AWS::CloudTrail::EventDataStore
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
        
        cfn_event_data_store_props_mixin = cloudtrail_mixins.CfnEventDataStorePropsMixin(cloudtrail_mixins.CfnEventDataStoreMixinProps(
            advanced_event_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty(
                field_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty(
                    ends_with=["endsWith"],
                    equal_to=["equalTo"],
                    field="field",
                    not_ends_with=["notEndsWith"],
                    not_equals=["notEquals"],
                    not_starts_with=["notStartsWith"],
                    starts_with=["startsWith"]
                )],
                name="name"
            )],
            billing_mode="billingMode",
            context_key_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.ContextKeySelectorProperty(
                equal_to=["equalTo"],
                type="type"
            )],
            federation_enabled=False,
            federation_role_arn="federationRoleArn",
            ingestion_enabled=False,
            insights_destination="insightsDestination",
            insight_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.InsightSelectorProperty(
                insight_type="insightType"
            )],
            kms_key_id="kmsKeyId",
            max_event_size="maxEventSize",
            multi_region_enabled=False,
            name="name",
            organization_enabled=False,
            retention_period=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            termination_protection_enabled=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEventDataStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudTrail::EventDataStore``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a36a8e128e15196850079207e110d64774162d0a0a8bc51ccbcdd8d3302003bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d325877b208ab1b1f2a9501e5d6f2da41dfad09f797e74e5b9562824db20ec)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9e15ccf215cd58ba2f9721e32620ce9fb3b965d389b9e6d19692fd8f36aff6f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEventDataStoreMixinProps:
        return typing.cast(CfnEventDataStoreMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"field_selectors": "fieldSelectors", "name": "name"},
    )
    class AdvancedEventSelectorProperty:
        def __init__(
            self,
            *,
            field_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Advanced event selectors let you create fine-grained selectors for AWS CloudTrail management, data, and network activity events.

            They help you control costs by logging only those events that are important to you. For more information about configuring advanced event selectors, see the `Logging data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ , `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ , and `Logging management events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html>`_ topics in the *AWS CloudTrail User Guide* .

            You cannot apply both event selectors and advanced event selectors to a trail.

            *Supported CloudTrail event record fields for management events*

            - ``eventCategory`` (required)
            - ``eventSource``
            - ``readOnly``

            The following additional fields are available for event data stores:

            - ``eventName``
            - ``eventType``
            - ``sessionCredentialFromConsole``
            - ``userIdentity.arn``

            *Supported CloudTrail event record fields for data events*

            - ``eventCategory`` (required)
            - ``eventName``
            - ``eventSource``
            - ``eventType``
            - ``resources.ARN``
            - ``resources.type`` (required)
            - ``readOnly``
            - ``sessionCredentialFromConsole``
            - ``userIdentity.arn``

            *Supported CloudTrail event record fields for network activity events*

            - ``eventCategory`` (required)
            - ``eventSource`` (required)
            - ``eventName``
            - ``errorCode`` - The only valid value for ``errorCode`` is ``VpceAccessDenied`` .
            - ``vpcEndpointId``

            .. epigraph::

               For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the only supported field is ``eventCategory`` .

            :param field_selectors: Contains all selector statements in an advanced event selector.
            :param name: An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedeventselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                advanced_event_selector_property = cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty(
                    field_selectors=[cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty(
                        ends_with=["endsWith"],
                        equal_to=["equalTo"],
                        field="field",
                        not_ends_with=["notEndsWith"],
                        not_equals=["notEquals"],
                        not_starts_with=["notStartsWith"],
                        starts_with=["startsWith"]
                    )],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90dc153f147dee89ab651d4887df1d290fa1849a00ecdf457cce901e5beb16c0)
                check_type(argname="argument field_selectors", value=field_selectors, expected_type=type_hints["field_selectors"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_selectors is not None:
                self._values["field_selectors"] = field_selectors
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def field_selectors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty"]]]]:
            '''Contains all selector statements in an advanced event selector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedeventselector.html#cfn-cloudtrail-eventdatastore-advancedeventselector-fieldselectors
            '''
            result = self._values.get("field_selectors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedeventselector.html#cfn-cloudtrail-eventdatastore-advancedeventselector-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedEventSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ends_with": "endsWith",
            "equal_to": "equalTo",
            "field": "field",
            "not_ends_with": "notEndsWith",
            "not_equals": "notEquals",
            "not_starts_with": "notStartsWith",
            "starts_with": "startsWith",
        },
    )
    class AdvancedFieldSelectorProperty:
        def __init__(
            self,
            *,
            ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            field: typing.Optional[builtins.str] = None,
            not_ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A single selector statement in an advanced event selector.

            :param ends_with: An operator that includes events that match the last few characters of the event record field specified as the value of ``Field`` .
            :param equal_to: An operator that includes events that match the exact value of the event record field specified as the value of ``Field`` . This is the only valid operator that you can use with the ``readOnly`` , ``eventCategory`` , and ``resources.type`` fields.
            :param field: A field in a CloudTrail event record on which to filter events to be logged. For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the field is used only for selecting events as filtering is not supported. For CloudTrail management events, supported fields include ``eventCategory`` (required), ``eventSource`` , and ``readOnly`` . The following additional fields are available for event data stores: ``eventName`` , ``eventType`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` . For CloudTrail data events, supported fields include ``eventCategory`` (required), ``eventName`` , ``eventSource`` , ``eventType`` , ``resources.type`` (required), ``readOnly`` , ``resources.ARN`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` . For CloudTrail network activity events, supported fields include ``eventCategory`` (required), ``eventSource`` (required), ``eventName`` , ``errorCode`` , and ``vpcEndpointId`` . For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the only supported field is ``eventCategory`` . .. epigraph:: Selectors don't support the use of wildcards like ``*`` . To match multiple values with a single condition, you may use ``StartsWith`` , ``EndsWith`` , ``NotStartsWith`` , or ``NotEndsWith`` to explicitly match the beginning or end of the event field. - *``readOnly``* - This is an optional field that is only used for management events and data events. This field can be set to ``Equals`` with a value of ``true`` or ``false`` . If you do not add this field, CloudTrail logs both ``read`` and ``write`` events. A value of ``true`` logs only ``read`` events. A value of ``false`` logs only ``write`` events. - *``eventSource``* - This field is only used for management events, data events, and network activity events. For management events for trails, this is an optional field that can be set to ``NotEquals`` ``kms.amazonaws.com`` to exclude KMS management events, or ``NotEquals`` ``rdsdata.amazonaws.com`` to exclude RDS management events. For data events for trails, this is an optional field that you can use to include or exclude any event source and can use any operator. For management and data events for event data stores, this is an optional field that you can use to include or exclude any event source and can use any operator. For network activity events, this is a required field that only uses the ``Equals`` operator. Set this field to the event source for which you want to log network activity events. If you want to log network activity events for multiple event sources, you must create a separate field selector for each event source. For a list of services supporting network activity events, see `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* . - *``eventName``* - This is an optional field that is only used for data events, management events (for event data stores only), and network activity events. You can use any operator with ``eventName`` . You can use it to ﬁlter in or ﬁlter out specific events. You can have multiple values for this ﬁeld, separated by commas. - *``eventCategory``* - This field is required and must be set to ``Equals`` . - For CloudTrail management events, the value must be ``Management`` . - For CloudTrail data events, the value must be ``Data`` . - For CloudTrail network activity events, the value must be ``NetworkActivity`` . The following are used only for event data stores: - For CloudTrail Insights events, the value must be ``Insight`` . - For AWS Config configuration items, the value must be ``ConfigurationItem`` . - For Audit Manager evidence, the value must be ``Evidence`` . - For events outside of AWS , the value must be ``ActivityAuditLog`` . - *``eventType``* - For event data stores, this is an optional field available for event data stores to filter management and data events on the event type. For trails, this is an optional field to filter data events on the event type. For information about available event types, see `CloudTrail record contents <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html#ct-event-type>`_ in the *AWS CloudTrail user guide* . - *``errorCode``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This is the error code to filter on. Currently, the only valid ``errorCode`` is ``VpceAccessDenied`` . ``errorCode`` can only use the ``Equals`` operator. - *``sessionCredentialFromConsole``* - For event data stores, this is an optional field used to filter management and data events based on whether the events originated from an AWS Management Console session. For trails, this is an optional field used to filter data events. ``sessionCredentialFromConsole`` can only use the ``Equals`` and ``NotEquals`` operators. - *``resources.type``* - This ﬁeld is required for CloudTrail data events. ``resources.type`` can only use the ``Equals`` operator. For a list of available resource types for data events, see `Data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#logging-data-events>`_ in the *AWS CloudTrail User Guide* . You can have only one ``resources.type`` ﬁeld per selector. To log events on more than one resource type, add another selector. - *``resources.ARN``* - The ``resources.ARN`` is an optional field for data events. You can use any operator with ``resources.ARN`` , but if you use ``Equals`` or ``NotEquals`` , the value must exactly match the ARN of a valid resource of the type you've speciﬁed in the template as the value of resources.type. To log all data events for all objects in a specific S3 bucket, use the ``StartsWith`` operator, and include only the bucket ARN as the matching value. For more information about the ARN formats of data event resources, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *Service Authorization Reference* . .. epigraph:: You can't use the ``resources.ARN`` field to filter resource types that do not have ARNs. - *``userIdentity.arn``* - For event data stores, this is an optional field used to filter management and data events for actions taken by specific IAM identities. For trails, this is an optional field used to filter data events. You can use any operator with ``userIdentity.arn`` . For more information on the userIdentity element, see `CloudTrail userIdentity element <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html>`_ in the *AWS CloudTrail User Guide* . - *``vpcEndpointId``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This field identifies the VPC endpoint that the request passed through. You can use any operator with ``vpcEndpointId`` .
            :param not_ends_with: An operator that excludes events that match the last few characters of the event record field specified as the value of ``Field`` .
            :param not_equals: An operator that excludes events that match the exact value of the event record field specified as the value of ``Field`` .
            :param not_starts_with: An operator that excludes events that match the first few characters of the event record field specified as the value of ``Field`` .
            :param starts_with: An operator that includes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                advanced_field_selector_property = cloudtrail_mixins.CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty(
                    ends_with=["endsWith"],
                    equal_to=["equalTo"],
                    field="field",
                    not_ends_with=["notEndsWith"],
                    not_equals=["notEquals"],
                    not_starts_with=["notStartsWith"],
                    starts_with=["startsWith"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9176d6c6e1a546df01c76b92a3c0f0a601fce22dfb7d228c2a1d166f0a497e5d)
                check_type(argname="argument ends_with", value=ends_with, expected_type=type_hints["ends_with"])
                check_type(argname="argument equal_to", value=equal_to, expected_type=type_hints["equal_to"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument not_ends_with", value=not_ends_with, expected_type=type_hints["not_ends_with"])
                check_type(argname="argument not_equals", value=not_equals, expected_type=type_hints["not_equals"])
                check_type(argname="argument not_starts_with", value=not_starts_with, expected_type=type_hints["not_starts_with"])
                check_type(argname="argument starts_with", value=starts_with, expected_type=type_hints["starts_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ends_with is not None:
                self._values["ends_with"] = ends_with
            if equal_to is not None:
                self._values["equal_to"] = equal_to
            if field is not None:
                self._values["field"] = field
            if not_ends_with is not None:
                self._values["not_ends_with"] = not_ends_with
            if not_equals is not None:
                self._values["not_equals"] = not_equals
            if not_starts_with is not None:
                self._values["not_starts_with"] = not_starts_with
            if starts_with is not None:
                self._values["starts_with"] = starts_with

        @builtins.property
        def ends_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the last few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-endswith
            '''
            result = self._values.get("ends_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def equal_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the exact value of the event record field specified as the value of ``Field`` .

            This is the only valid operator that you can use with the ``readOnly`` , ``eventCategory`` , and ``resources.type`` fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-equals
            '''
            result = self._values.get("equal_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''A field in a CloudTrail event record on which to filter events to be logged.

            For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the field is used only for selecting events as filtering is not supported.

            For CloudTrail management events, supported fields include ``eventCategory`` (required), ``eventSource`` , and ``readOnly`` . The following additional fields are available for event data stores: ``eventName`` , ``eventType`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` .

            For CloudTrail data events, supported fields include ``eventCategory`` (required), ``eventName`` , ``eventSource`` , ``eventType`` , ``resources.type`` (required), ``readOnly`` , ``resources.ARN`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` .

            For CloudTrail network activity events, supported fields include ``eventCategory`` (required), ``eventSource`` (required), ``eventName`` , ``errorCode`` , and ``vpcEndpointId`` .

            For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the only supported field is ``eventCategory`` .
            .. epigraph::

               Selectors don't support the use of wildcards like ``*`` . To match multiple values with a single condition, you may use ``StartsWith`` , ``EndsWith`` , ``NotStartsWith`` , or ``NotEndsWith`` to explicitly match the beginning or end of the event field.

            - *``readOnly``* - This is an optional field that is only used for management events and data events. This field can be set to ``Equals`` with a value of ``true`` or ``false`` . If you do not add this field, CloudTrail logs both ``read`` and ``write`` events. A value of ``true`` logs only ``read`` events. A value of ``false`` logs only ``write`` events.
            - *``eventSource``* - This field is only used for management events, data events, and network activity events.

            For management events for trails, this is an optional field that can be set to ``NotEquals`` ``kms.amazonaws.com`` to exclude KMS management events, or ``NotEquals`` ``rdsdata.amazonaws.com`` to exclude RDS management events.

            For data events for trails, this is an optional field that you can use to include or exclude any event source and can use any operator.

            For management and data events for event data stores, this is an optional field that you can use to include or exclude any event source and can use any operator.

            For network activity events, this is a required field that only uses the ``Equals`` operator. Set this field to the event source for which you want to log network activity events. If you want to log network activity events for multiple event sources, you must create a separate field selector for each event source. For a list of services supporting network activity events, see `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .

            - *``eventName``* - This is an optional field that is only used for data events, management events (for event data stores only), and network activity events. You can use any operator with ``eventName`` . You can use it to ﬁlter in or ﬁlter out specific events. You can have multiple values for this ﬁeld, separated by commas.
            - *``eventCategory``* - This field is required and must be set to ``Equals`` .
            - For CloudTrail management events, the value must be ``Management`` .
            - For CloudTrail data events, the value must be ``Data`` .
            - For CloudTrail network activity events, the value must be ``NetworkActivity`` .

            The following are used only for event data stores:

            - For CloudTrail Insights events, the value must be ``Insight`` .
            - For AWS Config configuration items, the value must be ``ConfigurationItem`` .
            - For Audit Manager evidence, the value must be ``Evidence`` .
            - For events outside of AWS , the value must be ``ActivityAuditLog`` .
            - *``eventType``* - For event data stores, this is an optional field available for event data stores to filter management and data events on the event type. For trails, this is an optional field to filter data events on the event type. For information about available event types, see `CloudTrail record contents <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html#ct-event-type>`_ in the *AWS CloudTrail user guide* .
            - *``errorCode``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This is the error code to filter on. Currently, the only valid ``errorCode`` is ``VpceAccessDenied`` . ``errorCode`` can only use the ``Equals`` operator.
            - *``sessionCredentialFromConsole``* - For event data stores, this is an optional field used to filter management and data events based on whether the events originated from an AWS Management Console session. For trails, this is an optional field used to filter data events. ``sessionCredentialFromConsole`` can only use the ``Equals`` and ``NotEquals`` operators.
            - *``resources.type``* - This ﬁeld is required for CloudTrail data events. ``resources.type`` can only use the ``Equals`` operator.

            For a list of available resource types for data events, see `Data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#logging-data-events>`_ in the *AWS CloudTrail User Guide* .

            You can have only one ``resources.type`` ﬁeld per selector. To log events on more than one resource type, add another selector.

            - *``resources.ARN``* - The ``resources.ARN`` is an optional field for data events. You can use any operator with ``resources.ARN`` , but if you use ``Equals`` or ``NotEquals`` , the value must exactly match the ARN of a valid resource of the type you've speciﬁed in the template as the value of resources.type. To log all data events for all objects in a specific S3 bucket, use the ``StartsWith`` operator, and include only the bucket ARN as the matching value.

            For more information about the ARN formats of data event resources, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *Service Authorization Reference* .
            .. epigraph::

               You can't use the ``resources.ARN`` field to filter resource types that do not have ARNs.

            - *``userIdentity.arn``* - For event data stores, this is an optional field used to filter management and data events for actions taken by specific IAM identities. For trails, this is an optional field used to filter data events. You can use any operator with ``userIdentity.arn`` . For more information on the userIdentity element, see `CloudTrail userIdentity element <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html>`_ in the *AWS CloudTrail User Guide* .
            - *``vpcEndpointId``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This field identifies the VPC endpoint that the request passed through. You can use any operator with ``vpcEndpointId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def not_ends_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the last few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-notendswith
            '''
            result = self._values.get("not_ends_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_equals(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the exact value of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-notequals
            '''
            result = self._values.get("not_equals")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_starts_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-notstartswith
            '''
            result = self._values.get("not_starts_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def starts_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-advancedfieldselector.html#cfn-cloudtrail-eventdatastore-advancedfieldselector-startswith
            '''
            result = self._values.get("starts_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedFieldSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnEventDataStorePropsMixin.ContextKeySelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"equal_to": "equalTo", "type": "type"},
    )
    class ContextKeySelectorProperty:
        def __init__(
            self,
            *,
            equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that contains information types to be included in CloudTrail enriched events.

            :param equal_to: A list of keys defined by Type to be included in CloudTrail enriched events.
            :param type: Specifies the type of the event record field in ContextKeySelector. Valid values include RequestContext, TagContext.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-contextkeyselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                context_key_selector_property = cloudtrail_mixins.CfnEventDataStorePropsMixin.ContextKeySelectorProperty(
                    equal_to=["equalTo"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5e1c9a36340deb7851a36f753056805c521a3b318e3d2e5828c11df7575bb3e)
                check_type(argname="argument equal_to", value=equal_to, expected_type=type_hints["equal_to"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if equal_to is not None:
                self._values["equal_to"] = equal_to
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def equal_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of keys defined by Type to be included in CloudTrail enriched events.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-contextkeyselector.html#cfn-cloudtrail-eventdatastore-contextkeyselector-equals
            '''
            result = self._values.get("equal_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of the event record field in ContextKeySelector.

            Valid values include RequestContext, TagContext.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-contextkeyselector.html#cfn-cloudtrail-eventdatastore-contextkeyselector-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContextKeySelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnEventDataStorePropsMixin.InsightSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"insight_type": "insightType"},
    )
    class InsightSelectorProperty:
        def __init__(
            self,
            *,
            insight_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A JSON string that contains a list of Insights types that are logged on an event data store.

            :param insight_type: The type of Insights events to log on an event data store. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types. The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume. The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-insightselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                insight_selector_property = cloudtrail_mixins.CfnEventDataStorePropsMixin.InsightSelectorProperty(
                    insight_type="insightType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7aafa7140c3b7f3420d91eda16b780ee97d26ab5eacc1ead74f8dc2764f4166e)
                check_type(argname="argument insight_type", value=insight_type, expected_type=type_hints["insight_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if insight_type is not None:
                self._values["insight_type"] = insight_type

        @builtins.property
        def insight_type(self) -> typing.Optional[builtins.str]:
            '''The type of Insights events to log on an event data store. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types.

            The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume.

            The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-eventdatastore-insightselector.html#cfn-cloudtrail-eventdatastore-insightselector-insighttype
            '''
            result = self._values.get("insight_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InsightSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnResourcePolicyMixinProps",
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

        :param resource_arn: The Amazon Resource Name (ARN) of the CloudTrail event data store, dashboard, or channel attached to the resource-based policy. Example event data store ARN format: ``arn:aws:cloudtrail:us-east-2:123456789012:eventdatastore/EXAMPLE-f852-4e8f-8bd1-bcf6cEXAMPLE`` Example dashboard ARN format: ``arn:aws:cloudtrail:us-east-1:123456789012:dashboard/exampleDash`` Example channel ARN format: ``arn:aws:cloudtrail:us-east-2:123456789012:channel/01234567890``
        :param resource_policy: A JSON-formatted string for an AWS resource-based policy. For example resource-based policies, see `CloudTrail resource-based policy examples <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/security_iam_resource-based-policy-examples.html>`_ in the *CloudTrail User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
            
            # resource_policy: Any
            
            cfn_resource_policy_mixin_props = cloudtrail_mixins.CfnResourcePolicyMixinProps(
                resource_arn="resourceArn",
                resource_policy=resource_policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04add0adfd3bd59ef9c3262bd9b7faf0ec1e5d3353bfe07f47637aa3bfe452ef)
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument resource_policy", value=resource_policy, expected_type=type_hints["resource_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if resource_policy is not None:
            self._values["resource_policy"] = resource_policy

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the CloudTrail event data store, dashboard, or channel attached to the resource-based policy.

        Example event data store ARN format: ``arn:aws:cloudtrail:us-east-2:123456789012:eventdatastore/EXAMPLE-f852-4e8f-8bd1-bcf6cEXAMPLE``

        Example dashboard ARN format: ``arn:aws:cloudtrail:us-east-1:123456789012:dashboard/exampleDash``

        Example channel ARN format: ``arn:aws:cloudtrail:us-east-2:123456789012:channel/01234567890``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-resourcepolicy.html#cfn-cloudtrail-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_policy(self) -> typing.Any:
        '''A JSON-formatted string for an AWS resource-based policy.

        For example resource-based policies, see `CloudTrail resource-based policy examples <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/security_iam_resource-based-policy-examples.html>`_ in the *CloudTrail User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-resourcepolicy.html#cfn-cloudtrail-resourcepolicy-resourcepolicy
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
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnResourcePolicyPropsMixin",
):
    '''Attaches a resource-based permission policy to a CloudTrail event data store, dashboard, or channel.

    For more information about resource-based policies, see `CloudTrail resource-based policy examples <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/security_iam_resource-based-policy-examples.html>`_ in the *CloudTrail User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-resourcepolicy.html
    :cloudformationResource: AWS::CloudTrail::ResourcePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
        
        # resource_policy: Any
        
        cfn_resource_policy_props_mixin = cloudtrail_mixins.CfnResourcePolicyPropsMixin(cloudtrail_mixins.CfnResourcePolicyMixinProps(
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
        '''Create a mixin to apply properties to ``AWS::CloudTrail::ResourcePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e4742c7e2097996cc93c9bf40b751d0e507403e17d57c16eaec21a12b59c92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7749a25130e5c4ce9fde1a35a5d6c6fddf5c42936e36e6c5d1d4ede1278788b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0f4aea5a2b10a6b1866d6079c8947c4ead767f91a4ef82988560f04c7af3f15)
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
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "advanced_event_selectors": "advancedEventSelectors",
        "aggregation_configurations": "aggregationConfigurations",
        "cloud_watch_logs_log_group_arn": "cloudWatchLogsLogGroupArn",
        "cloud_watch_logs_role_arn": "cloudWatchLogsRoleArn",
        "enable_log_file_validation": "enableLogFileValidation",
        "event_selectors": "eventSelectors",
        "include_global_service_events": "includeGlobalServiceEvents",
        "insight_selectors": "insightSelectors",
        "is_logging": "isLogging",
        "is_multi_region_trail": "isMultiRegionTrail",
        "is_organization_trail": "isOrganizationTrail",
        "kms_key_id": "kmsKeyId",
        "s3_bucket_name": "s3BucketName",
        "s3_key_prefix": "s3KeyPrefix",
        "sns_topic_name": "snsTopicName",
        "tags": "tags",
        "trail_name": "trailName",
    },
)
class CfnTrailMixinProps:
    def __init__(
        self,
        *,
        advanced_event_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrailPropsMixin.AdvancedEventSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        aggregation_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrailPropsMixin.AggregationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
        cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
        enable_log_file_validation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        event_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrailPropsMixin.EventSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        include_global_service_events: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        insight_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrailPropsMixin.InsightSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        is_logging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        is_multi_region_trail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        is_organization_trail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        s3_bucket_name: typing.Optional[builtins.str] = None,
        s3_key_prefix: typing.Optional[builtins.str] = None,
        sns_topic_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trail_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTrailPropsMixin.

        :param advanced_event_selectors: Specifies the settings for advanced event selectors. You can use advanced event selectors to log management events, data events for all resource types, and network activity events. You can add advanced event selectors, and conditions for your advanced event selectors, up to a maximum of 500 values for all conditions and selectors on a trail. You can use either ``AdvancedEventSelectors`` or ``EventSelectors`` , but not both. If you apply ``AdvancedEventSelectors`` to a trail, any existing ``EventSelectors`` are overwritten. For more information about advanced event selectors, see `Logging data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ and `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .
        :param aggregation_configurations: Specifies the aggregation configuration to aggregate CloudTrail Events. A maximum of 1 aggregation configuration is allowed.
        :param cloud_watch_logs_log_group_arn: Specifies a log group name using an Amazon Resource Name (ARN), a unique identifier that represents the log group to which CloudTrail logs are delivered. You must use a log group that exists in your account. To enable CloudWatch Logs delivery, you must provide values for ``CloudWatchLogsLogGroupArn`` and ``CloudWatchLogsRoleArn`` . .. epigraph:: If you previously enabled CloudWatch Logs delivery and want to disable CloudWatch Logs delivery, you must set the values of the ``CloudWatchLogsRoleArn`` and ``CloudWatchLogsLogGroupArn`` fields to ``""`` .
        :param cloud_watch_logs_role_arn: Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group. You must use a role that exists in your account. To enable CloudWatch Logs delivery, you must provide values for ``CloudWatchLogsLogGroupArn`` and ``CloudWatchLogsRoleArn`` . .. epigraph:: If you previously enabled CloudWatch Logs delivery and want to disable CloudWatch Logs delivery, you must set the values of the ``CloudWatchLogsRoleArn`` and ``CloudWatchLogsLogGroupArn`` fields to ``""`` .
        :param enable_log_file_validation: Specifies whether log file validation is enabled. The default is false. .. epigraph:: When you disable log file integrity validation, the chain of digest files is broken after one hour. CloudTrail does not create digest files for log files that were delivered during a period in which log file integrity validation was disabled. For example, if you enable log file integrity validation at noon on January 1, disable it at noon on January 2, and re-enable it at noon on January 10, digest files will not be created for the log files delivered from noon on January 2 to noon on January 10. The same applies whenever you stop CloudTrail logging or delete a trail.
        :param event_selectors: Use event selectors to further specify the management and data event settings for your trail. By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event. You can configure up to five event selectors for a trail. You cannot apply both event selectors and advanced event selectors to a trail.
        :param include_global_service_events: Specifies whether the trail is publishing events from global services such as IAM to the log files.
        :param insight_selectors: A JSON string that contains the Insights types you want to log on a trail. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types. The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume. The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.
        :param is_logging: Whether the CloudTrail trail is currently logging AWS API calls.
        :param is_multi_region_trail: Specifies whether the trail applies only to the current Region or to all Regions. The default is false. If the trail exists only in the current Region and this value is set to true, shadow trails (replications of the trail) will be created in the other Regions. If the trail exists in all Regions and this value is set to false, the trail will remain in the Region where it was created, and its shadow trails in other Regions will be deleted. As a best practice, consider using trails that log events in all Regions.
        :param is_organization_trail: Specifies whether the trail is applied to all accounts in an organization in AWS Organizations , or only for the current AWS account . The default is false, and cannot be true unless the call is made on behalf of an AWS account that is the management account for an organization in AWS Organizations . If the trail is not an organization trail and this is set to ``true`` , the trail will be created in all AWS accounts that belong to the organization. If the trail is an organization trail and this is set to ``false`` , the trail will remain in the current AWS account but be deleted from all member accounts in the organization. .. epigraph:: Only the management account for the organization can convert an organization trail to a non-organization trail, or convert a non-organization trail to an organization trail.
        :param kms_key_id: Specifies the AWS key ID to use to encrypt the logs and digest files delivered by CloudTrail. The value can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier. CloudTrail also supports AWS multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . Examples: - alias/MyAliasName - arn:aws:kms:us-east-2:123456789012:alias/MyAliasName - arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012 - 12345678-1234-1234-1234-123456789012
        :param s3_bucket_name: Specifies the name of the Amazon S3 bucket designated for publishing log files. See `Amazon S3 Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
        :param s3_key_prefix: Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery. For more information, see `Finding Your CloudTrail Log Files <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/get-and-view-cloudtrail-log-files.html#cloudtrail-find-log-files>`_ . The maximum length is 200 characters.
        :param sns_topic_name: Specifies the name or ARN of the Amazon SNS topic defined for notification of log file delivery. The maximum length is 256 characters.
        :param tags: A custom set of tags (key-value pairs) for this trail.
        :param trail_name: Specifies the name of the trail. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-) - Start with a letter or number, and end with a letter or number - Be between 3 and 128 characters - Have no adjacent periods, underscores or dashes. Names like ``my-_namespace`` and ``my--namespace`` are not valid. - Not be in IP address format (for example, 192.168.5.4)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
            
            cfn_trail_mixin_props = cloudtrail_mixins.CfnTrailMixinProps(
                advanced_event_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.AdvancedEventSelectorProperty(
                    field_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.AdvancedFieldSelectorProperty(
                        ends_with=["endsWith"],
                        equal_to=["equalTo"],
                        field="field",
                        not_ends_with=["notEndsWith"],
                        not_equals=["notEquals"],
                        not_starts_with=["notStartsWith"],
                        starts_with=["startsWith"]
                    )],
                    name="name"
                )],
                aggregation_configurations=[cloudtrail_mixins.CfnTrailPropsMixin.AggregationConfigurationProperty(
                    event_category="eventCategory",
                    templates=["templates"]
                )],
                cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
                cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
                enable_log_file_validation=False,
                event_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.EventSelectorProperty(
                    data_resources=[cloudtrail_mixins.CfnTrailPropsMixin.DataResourceProperty(
                        type="type",
                        values=["values"]
                    )],
                    exclude_management_event_sources=["excludeManagementEventSources"],
                    include_management_events=False,
                    read_write_type="readWriteType"
                )],
                include_global_service_events=False,
                insight_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.InsightSelectorProperty(
                    event_categories=["eventCategories"],
                    insight_type="insightType"
                )],
                is_logging=False,
                is_multi_region_trail=False,
                is_organization_trail=False,
                kms_key_id="kmsKeyId",
                s3_bucket_name="s3BucketName",
                s3_key_prefix="s3KeyPrefix",
                sns_topic_name="snsTopicName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trail_name="trailName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76bdeb985a7f033e5c6d27e80dc18f4e1ffea2080cb370360deef53904fec53a)
            check_type(argname="argument advanced_event_selectors", value=advanced_event_selectors, expected_type=type_hints["advanced_event_selectors"])
            check_type(argname="argument aggregation_configurations", value=aggregation_configurations, expected_type=type_hints["aggregation_configurations"])
            check_type(argname="argument cloud_watch_logs_log_group_arn", value=cloud_watch_logs_log_group_arn, expected_type=type_hints["cloud_watch_logs_log_group_arn"])
            check_type(argname="argument cloud_watch_logs_role_arn", value=cloud_watch_logs_role_arn, expected_type=type_hints["cloud_watch_logs_role_arn"])
            check_type(argname="argument enable_log_file_validation", value=enable_log_file_validation, expected_type=type_hints["enable_log_file_validation"])
            check_type(argname="argument event_selectors", value=event_selectors, expected_type=type_hints["event_selectors"])
            check_type(argname="argument include_global_service_events", value=include_global_service_events, expected_type=type_hints["include_global_service_events"])
            check_type(argname="argument insight_selectors", value=insight_selectors, expected_type=type_hints["insight_selectors"])
            check_type(argname="argument is_logging", value=is_logging, expected_type=type_hints["is_logging"])
            check_type(argname="argument is_multi_region_trail", value=is_multi_region_trail, expected_type=type_hints["is_multi_region_trail"])
            check_type(argname="argument is_organization_trail", value=is_organization_trail, expected_type=type_hints["is_organization_trail"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
            check_type(argname="argument s3_key_prefix", value=s3_key_prefix, expected_type=type_hints["s3_key_prefix"])
            check_type(argname="argument sns_topic_name", value=sns_topic_name, expected_type=type_hints["sns_topic_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trail_name", value=trail_name, expected_type=type_hints["trail_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if advanced_event_selectors is not None:
            self._values["advanced_event_selectors"] = advanced_event_selectors
        if aggregation_configurations is not None:
            self._values["aggregation_configurations"] = aggregation_configurations
        if cloud_watch_logs_log_group_arn is not None:
            self._values["cloud_watch_logs_log_group_arn"] = cloud_watch_logs_log_group_arn
        if cloud_watch_logs_role_arn is not None:
            self._values["cloud_watch_logs_role_arn"] = cloud_watch_logs_role_arn
        if enable_log_file_validation is not None:
            self._values["enable_log_file_validation"] = enable_log_file_validation
        if event_selectors is not None:
            self._values["event_selectors"] = event_selectors
        if include_global_service_events is not None:
            self._values["include_global_service_events"] = include_global_service_events
        if insight_selectors is not None:
            self._values["insight_selectors"] = insight_selectors
        if is_logging is not None:
            self._values["is_logging"] = is_logging
        if is_multi_region_trail is not None:
            self._values["is_multi_region_trail"] = is_multi_region_trail
        if is_organization_trail is not None:
            self._values["is_organization_trail"] = is_organization_trail
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if s3_bucket_name is not None:
            self._values["s3_bucket_name"] = s3_bucket_name
        if s3_key_prefix is not None:
            self._values["s3_key_prefix"] = s3_key_prefix
        if sns_topic_name is not None:
            self._values["sns_topic_name"] = sns_topic_name
        if tags is not None:
            self._values["tags"] = tags
        if trail_name is not None:
            self._values["trail_name"] = trail_name

    @builtins.property
    def advanced_event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.AdvancedEventSelectorProperty"]]]]:
        '''Specifies the settings for advanced event selectors.

        You can use advanced event selectors to log management events, data events for all resource types, and network activity events.

        You can add advanced event selectors, and conditions for your advanced event selectors, up to a maximum of 500 values for all conditions and selectors on a trail. You can use either ``AdvancedEventSelectors`` or ``EventSelectors`` , but not both. If you apply ``AdvancedEventSelectors`` to a trail, any existing ``EventSelectors`` are overwritten. For more information about advanced event selectors, see `Logging data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ and `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-advancedeventselectors
        '''
        result = self._values.get("advanced_event_selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.AdvancedEventSelectorProperty"]]]], result)

    @builtins.property
    def aggregation_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.AggregationConfigurationProperty"]]]]:
        '''Specifies the aggregation configuration to aggregate CloudTrail Events.

        A maximum of 1 aggregation configuration is allowed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-aggregationconfigurations
        '''
        result = self._values.get("aggregation_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.AggregationConfigurationProperty"]]]], result)

    @builtins.property
    def cloud_watch_logs_log_group_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies a log group name using an Amazon Resource Name (ARN), a unique identifier that represents the log group to which CloudTrail logs are delivered.

        You must use a log group that exists in your account.

        To enable CloudWatch Logs delivery, you must provide values for ``CloudWatchLogsLogGroupArn`` and ``CloudWatchLogsRoleArn`` .
        .. epigraph::

           If you previously enabled CloudWatch Logs delivery and want to disable CloudWatch Logs delivery, you must set the values of the ``CloudWatchLogsRoleArn`` and ``CloudWatchLogsLogGroupArn`` fields to ``""`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsloggrouparn
        '''
        result = self._values.get("cloud_watch_logs_log_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_logs_role_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the role for the CloudWatch Logs endpoint to assume to write to a user's log group.

        You must use a role that exists in your account.

        To enable CloudWatch Logs delivery, you must provide values for ``CloudWatchLogsLogGroupArn`` and ``CloudWatchLogsRoleArn`` .
        .. epigraph::

           If you previously enabled CloudWatch Logs delivery and want to disable CloudWatch Logs delivery, you must set the values of the ``CloudWatchLogsRoleArn`` and ``CloudWatchLogsLogGroupArn`` fields to ``""`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-cloudwatchlogsrolearn
        '''
        result = self._values.get("cloud_watch_logs_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_log_file_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether log file validation is enabled. The default is false.

        .. epigraph::

           When you disable log file integrity validation, the chain of digest files is broken after one hour. CloudTrail does not create digest files for log files that were delivered during a period in which log file integrity validation was disabled. For example, if you enable log file integrity validation at noon on January 1, disable it at noon on January 2, and re-enable it at noon on January 10, digest files will not be created for the log files delivered from noon on January 2 to noon on January 10. The same applies whenever you stop CloudTrail logging or delete a trail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-enablelogfilevalidation
        '''
        result = self._values.get("enable_log_file_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def event_selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.EventSelectorProperty"]]]]:
        '''Use event selectors to further specify the management and data event settings for your trail.

        By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event.

        You can configure up to five event selectors for a trail.

        You cannot apply both event selectors and advanced event selectors to a trail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-eventselectors
        '''
        result = self._values.get("event_selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.EventSelectorProperty"]]]], result)

    @builtins.property
    def include_global_service_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the trail is publishing events from global services such as IAM to the log files.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-includeglobalserviceevents
        '''
        result = self._values.get("include_global_service_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def insight_selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.InsightSelectorProperty"]]]]:
        '''A JSON string that contains the Insights types you want to log on a trail.

        ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types.

        The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume.

        The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-insightselectors
        '''
        result = self._values.get("insight_selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.InsightSelectorProperty"]]]], result)

    @builtins.property
    def is_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the CloudTrail trail is currently logging AWS API calls.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-islogging
        '''
        result = self._values.get("is_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def is_multi_region_trail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the trail applies only to the current Region or to all Regions.

        The default is false. If the trail exists only in the current Region and this value is set to true, shadow trails (replications of the trail) will be created in the other Regions. If the trail exists in all Regions and this value is set to false, the trail will remain in the Region where it was created, and its shadow trails in other Regions will be deleted. As a best practice, consider using trails that log events in all Regions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-ismultiregiontrail
        '''
        result = self._values.get("is_multi_region_trail")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def is_organization_trail(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the trail is applied to all accounts in an organization in AWS Organizations , or only for the current AWS account .

        The default is false, and cannot be true unless the call is made on behalf of an AWS account that is the management account for an organization in AWS Organizations . If the trail is not an organization trail and this is set to ``true`` , the trail will be created in all AWS accounts that belong to the organization. If the trail is an organization trail and this is set to ``false`` , the trail will remain in the current AWS account but be deleted from all member accounts in the organization.
        .. epigraph::

           Only the management account for the organization can convert an organization trail to a non-organization trail, or convert a non-organization trail to an organization trail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-isorganizationtrail
        '''
        result = self._values.get("is_organization_trail")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the AWS  key ID to use to encrypt the logs and digest files delivered by CloudTrail.

        The value can be an alias name prefixed by "alias/", a fully specified ARN to an alias, a fully specified ARN to a key, or a globally unique identifier.

        CloudTrail also supports AWS  multi-Region keys. For more information about multi-Region keys, see `Using multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        Examples:

        - alias/MyAliasName
        - arn:aws:kms:us-east-2:123456789012:alias/MyAliasName
        - arn:aws:kms:us-east-2:123456789012:key/12345678-1234-1234-1234-123456789012
        - 12345678-1234-1234-1234-123456789012

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the Amazon S3 bucket designated for publishing log files.

        See `Amazon S3 Bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3bucketname
        '''
        result = self._values.get("s3_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery.

        For more information, see `Finding Your CloudTrail Log Files <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/get-and-view-cloudtrail-log-files.html#cloudtrail-find-log-files>`_ . The maximum length is 200 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-s3keyprefix
        '''
        result = self._values.get("s3_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name or ARN of the Amazon SNS topic defined for notification of log file delivery.

        The maximum length is 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-snstopicname
        '''
        result = self._values.get("sns_topic_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A custom set of tags (key-value pairs) for this trail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trail_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the trail. The name must meet the following requirements:.

        - Contain only ASCII letters (a-z, A-Z), numbers (0-9), periods (.), underscores (_), or dashes (-)
        - Start with a letter or number, and end with a letter or number
        - Be between 3 and 128 characters
        - Have no adjacent periods, underscores or dashes. Names like ``my-_namespace`` and ``my--namespace`` are not valid.
        - Not be in IP address format (for example, 192.168.5.4)

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html#cfn-cloudtrail-trail-trailname
        '''
        result = self._values.get("trail_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrailMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrailPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin",
):
    '''Creates a trail that specifies the settings for delivery of log data to an Amazon S3 bucket.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudtrail-trail.html
    :cloudformationResource: AWS::CloudTrail::Trail
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
        
        cfn_trail_props_mixin = cloudtrail_mixins.CfnTrailPropsMixin(cloudtrail_mixins.CfnTrailMixinProps(
            advanced_event_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.AdvancedEventSelectorProperty(
                field_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.AdvancedFieldSelectorProperty(
                    ends_with=["endsWith"],
                    equal_to=["equalTo"],
                    field="field",
                    not_ends_with=["notEndsWith"],
                    not_equals=["notEquals"],
                    not_starts_with=["notStartsWith"],
                    starts_with=["startsWith"]
                )],
                name="name"
            )],
            aggregation_configurations=[cloudtrail_mixins.CfnTrailPropsMixin.AggregationConfigurationProperty(
                event_category="eventCategory",
                templates=["templates"]
            )],
            cloud_watch_logs_log_group_arn="cloudWatchLogsLogGroupArn",
            cloud_watch_logs_role_arn="cloudWatchLogsRoleArn",
            enable_log_file_validation=False,
            event_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.EventSelectorProperty(
                data_resources=[cloudtrail_mixins.CfnTrailPropsMixin.DataResourceProperty(
                    type="type",
                    values=["values"]
                )],
                exclude_management_event_sources=["excludeManagementEventSources"],
                include_management_events=False,
                read_write_type="readWriteType"
            )],
            include_global_service_events=False,
            insight_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.InsightSelectorProperty(
                event_categories=["eventCategories"],
                insight_type="insightType"
            )],
            is_logging=False,
            is_multi_region_trail=False,
            is_organization_trail=False,
            kms_key_id="kmsKeyId",
            s3_bucket_name="s3BucketName",
            s3_key_prefix="s3KeyPrefix",
            sns_topic_name="snsTopicName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trail_name="trailName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTrailMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CloudTrail::Trail``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__993cc70000db762bfdfb93b5167c6749cc8049173be57ff4cf09b37e7a3c6401)
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
            type_hints = typing.get_type_hints(_typecheckingstub__788802407f8e66604f02798ad024b98a52f354b3308bf98b42d29fa676569212)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257bb47ba958e1516395669fb9bc6ccd3b6de4ce537d966463d4803ae003ae37)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrailMixinProps:
        return typing.cast(CfnTrailMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin.AdvancedEventSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"field_selectors": "fieldSelectors", "name": "name"},
    )
    class AdvancedEventSelectorProperty:
        def __init__(
            self,
            *,
            field_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrailPropsMixin.AdvancedFieldSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Advanced event selectors let you create fine-grained selectors for AWS CloudTrail management, data, and network activity events.

            They help you control costs by logging only those events that are important to you. For more information about configuring advanced event selectors, see the `Logging data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ , `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ , and `Logging management events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html>`_ topics in the *AWS CloudTrail User Guide* .

            You cannot apply both event selectors and advanced event selectors to a trail.

            *Supported CloudTrail event record fields for management events*

            - ``eventCategory`` (required)
            - ``eventSource``
            - ``readOnly``

            The following additional fields are available for event data stores:

            - ``eventName``
            - ``eventType``
            - ``sessionCredentialFromConsole``
            - ``userIdentity.arn``

            *Supported CloudTrail event record fields for data events*

            - ``eventCategory`` (required)
            - ``eventName``
            - ``eventSource``
            - ``eventType``
            - ``resources.ARN``
            - ``resources.type`` (required)
            - ``readOnly``
            - ``sessionCredentialFromConsole``
            - ``userIdentity.arn``

            *Supported CloudTrail event record fields for network activity events*

            - ``eventCategory`` (required)
            - ``eventSource`` (required)
            - ``eventName``
            - ``errorCode`` - The only valid value for ``errorCode`` is ``VpceAccessDenied`` .
            - ``vpcEndpointId``

            .. epigraph::

               For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the only supported field is ``eventCategory`` .

            :param field_selectors: Contains all selector statements in an advanced event selector.
            :param name: An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedeventselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                advanced_event_selector_property = cloudtrail_mixins.CfnTrailPropsMixin.AdvancedEventSelectorProperty(
                    field_selectors=[cloudtrail_mixins.CfnTrailPropsMixin.AdvancedFieldSelectorProperty(
                        ends_with=["endsWith"],
                        equal_to=["equalTo"],
                        field="field",
                        not_ends_with=["notEndsWith"],
                        not_equals=["notEquals"],
                        not_starts_with=["notStartsWith"],
                        starts_with=["startsWith"]
                    )],
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c9aaf37ec76a3ac567c018283e220da19232a7ca977888ff31e826ba43c014f)
                check_type(argname="argument field_selectors", value=field_selectors, expected_type=type_hints["field_selectors"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if field_selectors is not None:
                self._values["field_selectors"] = field_selectors
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def field_selectors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.AdvancedFieldSelectorProperty"]]]]:
            '''Contains all selector statements in an advanced event selector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedeventselector.html#cfn-cloudtrail-trail-advancedeventselector-fieldselectors
            '''
            result = self._values.get("field_selectors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.AdvancedFieldSelectorProperty"]]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''An optional, descriptive name for an advanced event selector, such as "Log data events for only two S3 buckets".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedeventselector.html#cfn-cloudtrail-trail-advancedeventselector-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedEventSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin.AdvancedFieldSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ends_with": "endsWith",
            "equal_to": "equalTo",
            "field": "field",
            "not_ends_with": "notEndsWith",
            "not_equals": "notEquals",
            "not_starts_with": "notStartsWith",
            "starts_with": "startsWith",
        },
    )
    class AdvancedFieldSelectorProperty:
        def __init__(
            self,
            *,
            ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            field: typing.Optional[builtins.str] = None,
            not_ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
            not_starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
            starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A single selector statement in an advanced event selector.

            :param ends_with: An operator that includes events that match the last few characters of the event record field specified as the value of ``Field`` .
            :param equal_to: An operator that includes events that match the exact value of the event record field specified as the value of ``Field`` . This is the only valid operator that you can use with the ``readOnly`` , ``eventCategory`` , and ``resources.type`` fields.
            :param field: A field in a CloudTrail event record on which to filter events to be logged. For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the field is used only for selecting events as filtering is not supported. For CloudTrail management events, supported fields include ``eventCategory`` (required), ``eventSource`` , and ``readOnly`` . The following additional fields are available for event data stores: ``eventName`` , ``eventType`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` . For CloudTrail data events, supported fields include ``eventCategory`` (required), ``eventName`` , ``eventSource`` , ``eventType`` , ``resources.type`` (required), ``readOnly`` , ``resources.ARN`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` . For CloudTrail network activity events, supported fields include ``eventCategory`` (required), ``eventSource`` (required), ``eventName`` , ``errorCode`` , and ``vpcEndpointId`` . For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the only supported field is ``eventCategory`` . .. epigraph:: Selectors don't support the use of wildcards like ``*`` . To match multiple values with a single condition, you may use ``StartsWith`` , ``EndsWith`` , ``NotStartsWith`` , or ``NotEndsWith`` to explicitly match the beginning or end of the event field. - *``readOnly``* - This is an optional field that is only used for management events and data events. This field can be set to ``Equals`` with a value of ``true`` or ``false`` . If you do not add this field, CloudTrail logs both ``read`` and ``write`` events. A value of ``true`` logs only ``read`` events. A value of ``false`` logs only ``write`` events. - *``eventSource``* - This field is only used for management events, data events, and network activity events. For management events for trails, this is an optional field that can be set to ``NotEquals`` ``kms.amazonaws.com`` to exclude KMS management events, or ``NotEquals`` ``rdsdata.amazonaws.com`` to exclude RDS management events. For data events for trails, this is an optional field that you can use to include or exclude any event source and can use any operator. For management and data events for event data stores, this is an optional field that you can use to include or exclude any event source and can use any operator. For network activity events, this is a required field that only uses the ``Equals`` operator. Set this field to the event source for which you want to log network activity events. If you want to log network activity events for multiple event sources, you must create a separate field selector for each event source. For a list of services supporting network activity events, see `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* . - *``eventName``* - This is an optional field that is only used for data events, management events (for event data stores only), and network activity events. You can use any operator with ``eventName`` . You can use it to ﬁlter in or ﬁlter out specific events. You can have multiple values for this ﬁeld, separated by commas. - *``eventCategory``* - This field is required and must be set to ``Equals`` . - For CloudTrail management events, the value must be ``Management`` . - For CloudTrail data events, the value must be ``Data`` . - For CloudTrail network activity events, the value must be ``NetworkActivity`` . The following are used only for event data stores: - For CloudTrail Insights events, the value must be ``Insight`` . - For AWS Config configuration items, the value must be ``ConfigurationItem`` . - For Audit Manager evidence, the value must be ``Evidence`` . - For events outside of AWS , the value must be ``ActivityAuditLog`` . - *``eventType``* - For event data stores, this is an optional field available for event data stores to filter management and data events on the event type. For trails, this is an optional field to filter data events on the event type. For information about available event types, see `CloudTrail record contents <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html#ct-event-type>`_ in the *AWS CloudTrail user guide* . - *``errorCode``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This is the error code to filter on. Currently, the only valid ``errorCode`` is ``VpceAccessDenied`` . ``errorCode`` can only use the ``Equals`` operator. - *``sessionCredentialFromConsole``* - For event data stores, this is an optional field used to filter management and data events based on whether the events originated from an AWS Management Console session. For trails, this is an optional field used to filter data events. ``sessionCredentialFromConsole`` can only use the ``Equals`` and ``NotEquals`` operators. - *``resources.type``* - This ﬁeld is required for CloudTrail data events. ``resources.type`` can only use the ``Equals`` operator. For a list of available resource types for data events, see `Data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#logging-data-events>`_ in the *AWS CloudTrail User Guide* . You can have only one ``resources.type`` ﬁeld per selector. To log events on more than one resource type, add another selector. - *``resources.ARN``* - The ``resources.ARN`` is an optional field for data events. You can use any operator with ``resources.ARN`` , but if you use ``Equals`` or ``NotEquals`` , the value must exactly match the ARN of a valid resource of the type you've speciﬁed in the template as the value of resources.type. To log all data events for all objects in a specific S3 bucket, use the ``StartsWith`` operator, and include only the bucket ARN as the matching value. For more information about the ARN formats of data event resources, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *Service Authorization Reference* . .. epigraph:: You can't use the ``resources.ARN`` field to filter resource types that do not have ARNs. - *``userIdentity.arn``* - For event data stores, this is an optional field used to filter management and data events for actions taken by specific IAM identities. For trails, this is an optional field used to filter data events. You can use any operator with ``userIdentity.arn`` . For more information on the userIdentity element, see `CloudTrail userIdentity element <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html>`_ in the *AWS CloudTrail User Guide* . - *``vpcEndpointId``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This field identifies the VPC endpoint that the request passed through. You can use any operator with ``vpcEndpointId`` .
            :param not_ends_with: An operator that excludes events that match the last few characters of the event record field specified as the value of ``Field`` .
            :param not_equals: An operator that excludes events that match the exact value of the event record field specified as the value of ``Field`` .
            :param not_starts_with: An operator that excludes events that match the first few characters of the event record field specified as the value of ``Field`` .
            :param starts_with: An operator that includes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                advanced_field_selector_property = cloudtrail_mixins.CfnTrailPropsMixin.AdvancedFieldSelectorProperty(
                    ends_with=["endsWith"],
                    equal_to=["equalTo"],
                    field="field",
                    not_ends_with=["notEndsWith"],
                    not_equals=["notEquals"],
                    not_starts_with=["notStartsWith"],
                    starts_with=["startsWith"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7195c9f0ccd4aebe00c0e275be7892dd466586c07f49a3634a1bea67a51a6139)
                check_type(argname="argument ends_with", value=ends_with, expected_type=type_hints["ends_with"])
                check_type(argname="argument equal_to", value=equal_to, expected_type=type_hints["equal_to"])
                check_type(argname="argument field", value=field, expected_type=type_hints["field"])
                check_type(argname="argument not_ends_with", value=not_ends_with, expected_type=type_hints["not_ends_with"])
                check_type(argname="argument not_equals", value=not_equals, expected_type=type_hints["not_equals"])
                check_type(argname="argument not_starts_with", value=not_starts_with, expected_type=type_hints["not_starts_with"])
                check_type(argname="argument starts_with", value=starts_with, expected_type=type_hints["starts_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ends_with is not None:
                self._values["ends_with"] = ends_with
            if equal_to is not None:
                self._values["equal_to"] = equal_to
            if field is not None:
                self._values["field"] = field
            if not_ends_with is not None:
                self._values["not_ends_with"] = not_ends_with
            if not_equals is not None:
                self._values["not_equals"] = not_equals
            if not_starts_with is not None:
                self._values["not_starts_with"] = not_starts_with
            if starts_with is not None:
                self._values["starts_with"] = starts_with

        @builtins.property
        def ends_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the last few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-endswith
            '''
            result = self._values.get("ends_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def equal_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the exact value of the event record field specified as the value of ``Field`` .

            This is the only valid operator that you can use with the ``readOnly`` , ``eventCategory`` , and ``resources.type`` fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-equals
            '''
            result = self._values.get("equal_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def field(self) -> typing.Optional[builtins.str]:
            '''A field in a CloudTrail event record on which to filter events to be logged.

            For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the field is used only for selecting events as filtering is not supported.

            For CloudTrail management events, supported fields include ``eventCategory`` (required), ``eventSource`` , and ``readOnly`` . The following additional fields are available for event data stores: ``eventName`` , ``eventType`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` .

            For CloudTrail data events, supported fields include ``eventCategory`` (required), ``eventName`` , ``eventSource`` , ``eventType`` , ``resources.type`` (required), ``readOnly`` , ``resources.ARN`` , ``sessionCredentialFromConsole`` , and ``userIdentity.arn`` .

            For CloudTrail network activity events, supported fields include ``eventCategory`` (required), ``eventSource`` (required), ``eventName`` , ``errorCode`` , and ``vpcEndpointId`` .

            For event data stores for CloudTrail Insights events, AWS Config configuration items, Audit Manager evidence, or events outside of AWS , the only supported field is ``eventCategory`` .
            .. epigraph::

               Selectors don't support the use of wildcards like ``*`` . To match multiple values with a single condition, you may use ``StartsWith`` , ``EndsWith`` , ``NotStartsWith`` , or ``NotEndsWith`` to explicitly match the beginning or end of the event field.

            - *``readOnly``* - This is an optional field that is only used for management events and data events. This field can be set to ``Equals`` with a value of ``true`` or ``false`` . If you do not add this field, CloudTrail logs both ``read`` and ``write`` events. A value of ``true`` logs only ``read`` events. A value of ``false`` logs only ``write`` events.
            - *``eventSource``* - This field is only used for management events, data events, and network activity events.

            For management events for trails, this is an optional field that can be set to ``NotEquals`` ``kms.amazonaws.com`` to exclude KMS management events, or ``NotEquals`` ``rdsdata.amazonaws.com`` to exclude RDS management events.

            For data events for trails, this is an optional field that you can use to include or exclude any event source and can use any operator.

            For management and data events for event data stores, this is an optional field that you can use to include or exclude any event source and can use any operator.

            For network activity events, this is a required field that only uses the ``Equals`` operator. Set this field to the event source for which you want to log network activity events. If you want to log network activity events for multiple event sources, you must create a separate field selector for each event source. For a list of services supporting network activity events, see `Logging network activity events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-network-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .

            - *``eventName``* - This is an optional field that is only used for data events, management events (for event data stores only), and network activity events. You can use any operator with ``eventName`` . You can use it to ﬁlter in or ﬁlter out specific events. You can have multiple values for this ﬁeld, separated by commas.
            - *``eventCategory``* - This field is required and must be set to ``Equals`` .
            - For CloudTrail management events, the value must be ``Management`` .
            - For CloudTrail data events, the value must be ``Data`` .
            - For CloudTrail network activity events, the value must be ``NetworkActivity`` .

            The following are used only for event data stores:

            - For CloudTrail Insights events, the value must be ``Insight`` .
            - For AWS Config configuration items, the value must be ``ConfigurationItem`` .
            - For Audit Manager evidence, the value must be ``Evidence`` .
            - For events outside of AWS , the value must be ``ActivityAuditLog`` .
            - *``eventType``* - For event data stores, this is an optional field available for event data stores to filter management and data events on the event type. For trails, this is an optional field to filter data events on the event type. For information about available event types, see `CloudTrail record contents <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-record-contents.html#ct-event-type>`_ in the *AWS CloudTrail user guide* .
            - *``errorCode``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This is the error code to filter on. Currently, the only valid ``errorCode`` is ``VpceAccessDenied`` . ``errorCode`` can only use the ``Equals`` operator.
            - *``sessionCredentialFromConsole``* - For event data stores, this is an optional field used to filter management and data events based on whether the events originated from an AWS Management Console session. For trails, this is an optional field used to filter data events. ``sessionCredentialFromConsole`` can only use the ``Equals`` and ``NotEquals`` operators.
            - *``resources.type``* - This ﬁeld is required for CloudTrail data events. ``resources.type`` can only use the ``Equals`` operator.

            For a list of available resource types for data events, see `Data events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html#logging-data-events>`_ in the *AWS CloudTrail User Guide* .

            You can have only one ``resources.type`` ﬁeld per selector. To log events on more than one resource type, add another selector.

            - *``resources.ARN``* - The ``resources.ARN`` is an optional field for data events. You can use any operator with ``resources.ARN`` , but if you use ``Equals`` or ``NotEquals`` , the value must exactly match the ARN of a valid resource of the type you've speciﬁed in the template as the value of resources.type. To log all data events for all objects in a specific S3 bucket, use the ``StartsWith`` operator, and include only the bucket ARN as the matching value.

            For more information about the ARN formats of data event resources, see `Actions, resources, and condition keys for AWS services <https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html>`_ in the *Service Authorization Reference* .
            .. epigraph::

               You can't use the ``resources.ARN`` field to filter resource types that do not have ARNs.

            - *``userIdentity.arn``* - For event data stores, this is an optional field used to filter management and data events for actions taken by specific IAM identities. For trails, this is an optional field used to filter data events. You can use any operator with ``userIdentity.arn`` . For more information on the userIdentity element, see `CloudTrail userIdentity element <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference-user-identity.html>`_ in the *AWS CloudTrail User Guide* .
            - *``vpcEndpointId``* - This ﬁeld is only used to filter CloudTrail network activity events and is optional. This field identifies the VPC endpoint that the request passed through. You can use any operator with ``vpcEndpointId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-field
            '''
            result = self._values.get("field")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def not_ends_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the last few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-notendswith
            '''
            result = self._values.get("not_ends_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_equals(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the exact value of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-notequals
            '''
            result = self._values.get("not_equals")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def not_starts_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that excludes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-notstartswith
            '''
            result = self._values.get("not_starts_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def starts_with(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An operator that includes events that match the first few characters of the event record field specified as the value of ``Field`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-advancedfieldselector.html#cfn-cloudtrail-trail-advancedfieldselector-startswith
            '''
            result = self._values.get("starts_with")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AdvancedFieldSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin.AggregationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"event_category": "eventCategory", "templates": "templates"},
    )
    class AggregationConfigurationProperty:
        def __init__(
            self,
            *,
            event_category: typing.Optional[builtins.str] = None,
            templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that contains configuration settings for aggregating events.

            :param event_category: Specifies the event category for which aggregation should be performed.
            :param templates: A list of aggregation templates that can be used to configure event aggregation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-aggregationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                aggregation_configuration_property = cloudtrail_mixins.CfnTrailPropsMixin.AggregationConfigurationProperty(
                    event_category="eventCategory",
                    templates=["templates"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71a2459b95190b3e362434ff3b22d0aa208ac9f5facfb84306b01886697998f0)
                check_type(argname="argument event_category", value=event_category, expected_type=type_hints["event_category"])
                check_type(argname="argument templates", value=templates, expected_type=type_hints["templates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_category is not None:
                self._values["event_category"] = event_category
            if templates is not None:
                self._values["templates"] = templates

        @builtins.property
        def event_category(self) -> typing.Optional[builtins.str]:
            '''Specifies the event category for which aggregation should be performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-aggregationconfiguration.html#cfn-cloudtrail-trail-aggregationconfiguration-eventcategory
            '''
            result = self._values.get("event_category")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def templates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of aggregation templates that can be used to configure event aggregation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-aggregationconfiguration.html#cfn-cloudtrail-trail-aggregationconfiguration-templates
            '''
            result = self._values.get("templates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin.DataResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "values": "values"},
    )
    class DataResourceProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''You can configure the ``DataResource`` in an ``EventSelector`` to log data events for the following three resource types:.

            - ``AWS::DynamoDB::Table``
            - ``AWS::Lambda::Function``
            - ``AWS::S3::Object``

            To log data events for all other resource types including objects stored in `directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html>`_ , you must use `AdvancedEventSelectors <https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html>`_ . You must also use ``AdvancedEventSelectors`` if you want to filter on the ``eventName`` field.

            Configure the ``DataResource`` to specify the resource type and resource ARNs for which you want to log data events.
            .. epigraph::

               The total number of allowed data resources is 250. This number can be distributed between 1 and 5 event selectors, but the total cannot exceed 250 across all selectors for the trail.

            The following example demonstrates how logging works when you configure logging of all data events for a general purpose bucket named ``amzn-s3-demo-bucket1`` . In this example, the CloudTrail user specified an empty prefix, and the option to log both ``Read`` and ``Write`` data events.

            - A user uploads an image file to ``amzn-s3-demo-bucket1`` .
            - The ``PutObject`` API operation is an Amazon S3 object-level API. It is recorded as a data event in CloudTrail. Because the CloudTrail user specified an S3 bucket with an empty prefix, events that occur on any object in that bucket are logged. The trail processes and logs the event.
            - A user uploads an object to an Amazon S3 bucket named ``arn:aws:s3:::amzn-s3-demo-bucket1`` .
            - The ``PutObject`` API operation occurred for an object in an S3 bucket that the CloudTrail user didn't specify for the trail. The trail doesn’t log the event.

            The following example demonstrates how logging works when you configure logging of AWS Lambda data events for a Lambda function named *MyLambdaFunction* , but not for all Lambda functions.

            - A user runs a script that includes a call to the *MyLambdaFunction* function and the *MyOtherLambdaFunction* function.
            - The ``Invoke`` API operation on *MyLambdaFunction* is an Lambda API. It is recorded as a data event in CloudTrail. Because the CloudTrail user specified logging data events for *MyLambdaFunction* , any invocations of that function are logged. The trail processes and logs the event.
            - The ``Invoke`` API operation on *MyOtherLambdaFunction* is an Lambda API. Because the CloudTrail user did not specify logging data events for all Lambda functions, the ``Invoke`` operation for *MyOtherLambdaFunction* does not match the function specified for the trail. The trail doesn’t log the event.

            :param type: The resource type in which you want to log data events. You can specify the following *basic* event selector resource types: - ``AWS::DynamoDB::Table`` - ``AWS::Lambda::Function`` - ``AWS::S3::Object`` Additional resource types are available through *advanced* event selectors. For more information, see `AdvancedEventSelector <https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html>`_ .
            :param values: An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified resource type. - To log data events for all objects in all S3 buckets in your AWS account , specify the prefix as ``arn:aws:s3`` . .. epigraph:: This also enables logging of data event activity performed by any user or role in your AWS account , even if that activity is performed on a bucket that belongs to another AWS account . - To log data events for all objects in an S3 bucket, specify the bucket and an empty object prefix such as ``arn:aws:s3:::amzn-s3-demo-bucket1/`` . The trail logs data events for all objects in this S3 bucket. - To log data events for specific objects, specify the S3 bucket and object prefix such as ``arn:aws:s3:::amzn-s3-demo-bucket1/example-images`` . The trail logs data events for objects in this S3 bucket that match the prefix. - To log data events for all Lambda functions in your AWS account , specify the prefix as ``arn:aws:lambda`` . .. epigraph:: This also enables logging of ``Invoke`` activity performed by any user or role in your AWS account , even if that activity is performed on a function that belongs to another AWS account . - To log data events for a specific Lambda function, specify the function ARN. .. epigraph:: Lambda function ARNs are exact. For example, if you specify a function ARN *arn:aws:lambda:us-west-2:111111111111:function:helloworld* , data events will only be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld* . They will not be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld2* . - To log data events for all DynamoDB tables in your AWS account , specify the prefix as ``arn:aws:dynamodb`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                data_resource_property = cloudtrail_mixins.CfnTrailPropsMixin.DataResourceProperty(
                    type="type",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef992f238d4d47b2690dc93f648d88f2f923164d7c097d0ba6f4223f1a4141c9)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The resource type in which you want to log data events.

            You can specify the following *basic* event selector resource types:

            - ``AWS::DynamoDB::Table``
            - ``AWS::Lambda::Function``
            - ``AWS::S3::Object``

            Additional resource types are available through *advanced* event selectors. For more information, see `AdvancedEventSelector <https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html#cfn-cloudtrail-trail-dataresource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified resource type.

            - To log data events for all objects in all S3 buckets in your AWS account , specify the prefix as ``arn:aws:s3`` .

            .. epigraph::

               This also enables logging of data event activity performed by any user or role in your AWS account , even if that activity is performed on a bucket that belongs to another AWS account .

            - To log data events for all objects in an S3 bucket, specify the bucket and an empty object prefix such as ``arn:aws:s3:::amzn-s3-demo-bucket1/`` . The trail logs data events for all objects in this S3 bucket.
            - To log data events for specific objects, specify the S3 bucket and object prefix such as ``arn:aws:s3:::amzn-s3-demo-bucket1/example-images`` . The trail logs data events for objects in this S3 bucket that match the prefix.
            - To log data events for all Lambda functions in your AWS account , specify the prefix as ``arn:aws:lambda`` .

            .. epigraph::

               This also enables logging of ``Invoke`` activity performed by any user or role in your AWS account , even if that activity is performed on a function that belongs to another AWS account .

            - To log data events for a specific Lambda function, specify the function ARN.

            .. epigraph::

               Lambda function ARNs are exact. For example, if you specify a function ARN *arn:aws:lambda:us-west-2:111111111111:function:helloworld* , data events will only be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld* . They will not be logged for *arn:aws:lambda:us-west-2:111111111111:function:helloworld2* .

            - To log data events for all DynamoDB tables in your AWS account , specify the prefix as ``arn:aws:dynamodb`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-dataresource.html#cfn-cloudtrail-trail-dataresource-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin.EventSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_resources": "dataResources",
            "exclude_management_event_sources": "excludeManagementEventSources",
            "include_management_events": "includeManagementEvents",
            "read_write_type": "readWriteType",
        },
    )
    class EventSelectorProperty:
        def __init__(
            self,
            *,
            data_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrailPropsMixin.DataResourceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            exclude_management_event_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
            include_management_events: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            read_write_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use event selectors to further specify the management and data event settings for your trail.

            By default, trails created without specific event selectors will be configured to log all read and write management events, and no data events. When an event occurs in your account, CloudTrail evaluates the event selector for all trails. For each trail, if the event matches any event selector, the trail processes and logs the event. If the event doesn't match any event selector, the trail doesn't log the event.

            You can configure up to five event selectors for a trail.

            You cannot apply both event selectors and advanced event selectors to a trail.

            :param data_resources: CloudTrail supports data event logging for Amazon S3 objects in standard S3 buckets, AWS Lambda functions, and Amazon DynamoDB tables with basic event selectors. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events. For more information, see `Data Events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ and `Limits in AWS CloudTrail <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html>`_ in the *AWS CloudTrail User Guide* . .. epigraph:: To log data events for all other resource types including objects stored in `directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html>`_ , you must use `AdvancedEventSelectors <https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html>`_ . You must also use ``AdvancedEventSelectors`` if you want to filter on the ``eventName`` field.
            :param exclude_management_event_sources: An optional list of service event sources from which you do not want management events to be logged on your trail. In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service or Amazon RDS Data API events by containing ``kms.amazonaws.com`` or ``rdsdata.amazonaws.com`` . By default, ``ExcludeManagementEventSources`` is empty, and AWS and Amazon RDS Data API events are logged to your trail. You can exclude management event sources only in Regions that support the event source.
            :param include_management_events: Specify if you want your event selector to include management events for your trail. For more information, see `Management Events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* . By default, the value is ``true`` . The first copy of management events is free. You are charged for additional copies of management events that you are logging on any subsequent trail in the same Region. For more information about CloudTrail pricing, see `AWS CloudTrail Pricing <https://docs.aws.amazon.com/cloudtrail/pricing/>`_ .
            :param read_write_type: Specify if you want your trail to log read-only events, write-only events, or all. For example, the EC2 ``GetConsoleOutput`` is a read-only API operation and ``RunInstances`` is a write-only API operation. By default, the value is ``All`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                event_selector_property = cloudtrail_mixins.CfnTrailPropsMixin.EventSelectorProperty(
                    data_resources=[cloudtrail_mixins.CfnTrailPropsMixin.DataResourceProperty(
                        type="type",
                        values=["values"]
                    )],
                    exclude_management_event_sources=["excludeManagementEventSources"],
                    include_management_events=False,
                    read_write_type="readWriteType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b18d69f5051baee39d4d30cf6285af587d3378af6e38d5dbdbec4cf9f8a13fc3)
                check_type(argname="argument data_resources", value=data_resources, expected_type=type_hints["data_resources"])
                check_type(argname="argument exclude_management_event_sources", value=exclude_management_event_sources, expected_type=type_hints["exclude_management_event_sources"])
                check_type(argname="argument include_management_events", value=include_management_events, expected_type=type_hints["include_management_events"])
                check_type(argname="argument read_write_type", value=read_write_type, expected_type=type_hints["read_write_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_resources is not None:
                self._values["data_resources"] = data_resources
            if exclude_management_event_sources is not None:
                self._values["exclude_management_event_sources"] = exclude_management_event_sources
            if include_management_events is not None:
                self._values["include_management_events"] = include_management_events
            if read_write_type is not None:
                self._values["read_write_type"] = read_write_type

        @builtins.property
        def data_resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.DataResourceProperty"]]]]:
            '''CloudTrail supports data event logging for Amazon S3 objects in standard S3 buckets, AWS Lambda functions, and Amazon DynamoDB tables with basic event selectors.

            You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.

            For more information, see `Data Events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-data-events-with-cloudtrail.html>`_ and `Limits in AWS CloudTrail <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/WhatIsCloudTrail-Limits.html>`_ in the *AWS CloudTrail User Guide* .
            .. epigraph::

               To log data events for all other resource types including objects stored in `directory buckets <https://docs.aws.amazon.com/AmazonS3/latest/userguide/directory-buckets-overview.html>`_ , you must use `AdvancedEventSelectors <https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_AdvancedEventSelector.html>`_ . You must also use ``AdvancedEventSelectors`` if you want to filter on the ``eventName`` field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-dataresources
            '''
            result = self._values.get("data_resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrailPropsMixin.DataResourceProperty"]]]], result)

        @builtins.property
        def exclude_management_event_sources(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''An optional list of service event sources from which you do not want management events to be logged on your trail.

            In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service or Amazon RDS Data API events by containing ``kms.amazonaws.com`` or ``rdsdata.amazonaws.com`` . By default, ``ExcludeManagementEventSources`` is empty, and AWS  and Amazon RDS Data API events are logged to your trail. You can exclude management event sources only in Regions that support the event source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-excludemanagementeventsources
            '''
            result = self._values.get("exclude_management_event_sources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def include_management_events(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specify if you want your event selector to include management events for your trail.

            For more information, see `Management Events <https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-management-events-with-cloudtrail.html>`_ in the *AWS CloudTrail User Guide* .

            By default, the value is ``true`` .

            The first copy of management events is free. You are charged for additional copies of management events that you are logging on any subsequent trail in the same Region. For more information about CloudTrail pricing, see `AWS CloudTrail Pricing <https://docs.aws.amazon.com/cloudtrail/pricing/>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-includemanagementevents
            '''
            result = self._values.get("include_management_events")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def read_write_type(self) -> typing.Optional[builtins.str]:
            '''Specify if you want your trail to log read-only events, write-only events, or all.

            For example, the EC2 ``GetConsoleOutput`` is a read-only API operation and ``RunInstances`` is a write-only API operation.

            By default, the value is ``All`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-eventselector.html#cfn-cloudtrail-trail-eventselector-readwritetype
            '''
            result = self._values.get("read_write_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cloudtrail.mixins.CfnTrailPropsMixin.InsightSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_categories": "eventCategories",
            "insight_type": "insightType",
        },
    )
    class InsightSelectorProperty:
        def __init__(
            self,
            *,
            event_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
            insight_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A JSON string that contains a list of Insights types that are logged on a trail.

            :param event_categories: Select the event category on which Insights should be enabled. - If EventCategories is not provided, the specified Insights types are enabled on management API calls by default. - If EventCategories is provided, the given event categories will overwrite the existing ones. For example, if a trail already has Insights enabled on management events, and then a PutInsightSelectors request is made with only data events specified in EventCategories, Insights on management events will be disabled.
            :param insight_type: The type of Insights events to log on a trail. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types. The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume. The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-insightselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cloudtrail import mixins as cloudtrail_mixins
                
                insight_selector_property = cloudtrail_mixins.CfnTrailPropsMixin.InsightSelectorProperty(
                    event_categories=["eventCategories"],
                    insight_type="insightType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ea478c82c3a080670a49ae24d8f745613463b8e85ea2412d3bf84844a71f430)
                check_type(argname="argument event_categories", value=event_categories, expected_type=type_hints["event_categories"])
                check_type(argname="argument insight_type", value=insight_type, expected_type=type_hints["insight_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_categories is not None:
                self._values["event_categories"] = event_categories
            if insight_type is not None:
                self._values["insight_type"] = insight_type

        @builtins.property
        def event_categories(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Select the event category on which Insights should be enabled.

            - If EventCategories is not provided, the specified Insights types are enabled on management API calls by default.
            - If EventCategories is provided, the given event categories will overwrite the existing ones. For example, if a trail already has Insights enabled on management events, and then a PutInsightSelectors request is made with only data events specified in EventCategories, Insights on management events will be disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-insightselector.html#cfn-cloudtrail-trail-insightselector-eventcategories
            '''
            result = self._values.get("event_categories")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def insight_type(self) -> typing.Optional[builtins.str]:
            '''The type of Insights events to log on a trail. ``ApiCallRateInsight`` and ``ApiErrorRateInsight`` are valid Insight types.

            The ``ApiCallRateInsight`` Insights type analyzes write-only management API calls that are aggregated per minute against a baseline API call volume.

            The ``ApiErrorRateInsight`` Insights type analyzes management API calls that result in error codes. The error is shown if the API call is unsuccessful.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudtrail-trail-insightselector.html#cfn-cloudtrail-trail-insightselector-insighttype
            '''
            result = self._values.get("insight_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InsightSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnChannelMixinProps",
    "CfnChannelPropsMixin",
    "CfnDashboardMixinProps",
    "CfnDashboardPropsMixin",
    "CfnEventDataStoreMixinProps",
    "CfnEventDataStorePropsMixin",
    "CfnResourcePolicyMixinProps",
    "CfnResourcePolicyPropsMixin",
    "CfnTrailMixinProps",
    "CfnTrailPropsMixin",
]

publication.publish()

def _typecheckingstub__ad43459a37c8aff023f255accc652dd44b01ab90262674bbbeba78a00c89adab(
    *,
    destinations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnChannelPropsMixin.DestinationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c68576b71d3c13e6858249bb0eb4088ef4dc646589e3c83364b4a6d02db95c(
    props: typing.Union[CfnChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbd3f37c9a1fb6409ee75b7912e163dd291e1477a5f7e6bff8e05a89b7f722d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c1aeb1bdb23445f8124da4cacdad4e77e57cf2e2bea90b3c07d930b2362592(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e70887fbff8644363731ca7f8a4f723016fe8c757677f959be3c560c7aabb3(
    *,
    location: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b564f92eab90572c9135808e8dc6a5cbe342e67e9981112e23ebb5ea1aeb5106(
    *,
    name: typing.Optional[builtins.str] = None,
    refresh_schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDashboardPropsMixin.RefreshScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    widgets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDashboardPropsMixin.WidgetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66db4f4b6ad9e14975931e6e8581f96f8982d1dd90a51e6c555f24b55d155fcf(
    props: typing.Union[CfnDashboardMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04effb76cabdab6d773fabdc4570d08ba655f8842e6fbb5a32de1e56dbea46f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2cb84030858ae3db29af27ee44026ea9f4ee1c8b86b70f3947a33e5f71dd898(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c5836ff4412c4af859fb0cd6a4152d09d61996dc7a57b3f475c8cdfa66ca680(
    *,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97458b5d40a7428dd5bb5aef0f3bb500121c5be50cef391d39691fd4c17adfd9(
    *,
    frequency: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDashboardPropsMixin.FrequencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
    time_of_day: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa6ed7a2242902d3d0d9b1b61cd4ba12b65ffc059021b508c732a343d86abb5d(
    *,
    query_parameters: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_statement: typing.Optional[builtins.str] = None,
    view_properties: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe110452f971dadfb45eea1e16ca4c0779b7ed7d58a1f36103725f97425ac140(
    *,
    advanced_event_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventDataStorePropsMixin.AdvancedEventSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    billing_mode: typing.Optional[builtins.str] = None,
    context_key_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventDataStorePropsMixin.ContextKeySelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    federation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    federation_role_arn: typing.Optional[builtins.str] = None,
    ingestion_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    insights_destination: typing.Optional[builtins.str] = None,
    insight_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventDataStorePropsMixin.InsightSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    max_event_size: typing.Optional[builtins.str] = None,
    multi_region_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    organization_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    retention_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    termination_protection_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36a8e128e15196850079207e110d64774162d0a0a8bc51ccbcdd8d3302003bf(
    props: typing.Union[CfnEventDataStoreMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d325877b208ab1b1f2a9501e5d6f2da41dfad09f797e74e5b9562824db20ec(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e15ccf215cd58ba2f9721e32620ce9fb3b965d389b9e6d19692fd8f36aff6f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90dc153f147dee89ab651d4887df1d290fa1849a00ecdf457cce901e5beb16c0(
    *,
    field_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEventDataStorePropsMixin.AdvancedFieldSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9176d6c6e1a546df01c76b92a3c0f0a601fce22dfb7d228c2a1d166f0a497e5d(
    *,
    ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    field: typing.Optional[builtins.str] = None,
    not_ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e1c9a36340deb7851a36f753056805c521a3b318e3d2e5828c11df7575bb3e(
    *,
    equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aafa7140c3b7f3420d91eda16b780ee97d26ab5eacc1ead74f8dc2764f4166e(
    *,
    insight_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04add0adfd3bd59ef9c3262bd9b7faf0ec1e5d3353bfe07f47637aa3bfe452ef(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    resource_policy: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e4742c7e2097996cc93c9bf40b751d0e507403e17d57c16eaec21a12b59c92(
    props: typing.Union[CfnResourcePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7749a25130e5c4ce9fde1a35a5d6c6fddf5c42936e36e6c5d1d4ede1278788b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0f4aea5a2b10a6b1866d6079c8947c4ead767f91a4ef82988560f04c7af3f15(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76bdeb985a7f033e5c6d27e80dc18f4e1ffea2080cb370360deef53904fec53a(
    *,
    advanced_event_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrailPropsMixin.AdvancedEventSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    aggregation_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrailPropsMixin.AggregationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cloud_watch_logs_log_group_arn: typing.Optional[builtins.str] = None,
    cloud_watch_logs_role_arn: typing.Optional[builtins.str] = None,
    enable_log_file_validation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    event_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrailPropsMixin.EventSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    include_global_service_events: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    insight_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrailPropsMixin.InsightSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    is_logging: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_multi_region_trail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_organization_trail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_key_prefix: typing.Optional[builtins.str] = None,
    sns_topic_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trail_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__993cc70000db762bfdfb93b5167c6749cc8049173be57ff4cf09b37e7a3c6401(
    props: typing.Union[CfnTrailMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788802407f8e66604f02798ad024b98a52f354b3308bf98b42d29fa676569212(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257bb47ba958e1516395669fb9bc6ccd3b6de4ce537d966463d4803ae003ae37(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c9aaf37ec76a3ac567c018283e220da19232a7ca977888ff31e826ba43c014f(
    *,
    field_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrailPropsMixin.AdvancedFieldSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7195c9f0ccd4aebe00c0e275be7892dd466586c07f49a3634a1bea67a51a6139(
    *,
    ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    equal_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    field: typing.Optional[builtins.str] = None,
    not_ends_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_equals: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
    starts_with: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71a2459b95190b3e362434ff3b22d0aa208ac9f5facfb84306b01886697998f0(
    *,
    event_category: typing.Optional[builtins.str] = None,
    templates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef992f238d4d47b2690dc93f648d88f2f923164d7c097d0ba6f4223f1a4141c9(
    *,
    type: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b18d69f5051baee39d4d30cf6285af587d3378af6e38d5dbdbec4cf9f8a13fc3(
    *,
    data_resources: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrailPropsMixin.DataResourceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    exclude_management_event_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    include_management_events: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    read_write_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea478c82c3a080670a49ae24d8f745613463b8e85ea2412d3bf84844a71f430(
    *,
    event_categories: typing.Optional[typing.Sequence[builtins.str]] = None,
    insight_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
