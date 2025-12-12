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
    jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_subtype_config": "channelSubtypeConfig",
        "communication_limits_override": "communicationLimitsOverride",
        "communication_time_config": "communicationTimeConfig",
        "connect_campaign_flow_arn": "connectCampaignFlowArn",
        "connect_instance_id": "connectInstanceId",
        "name": "name",
        "schedule": "schedule",
        "source": "source",
        "tags": "tags",
    },
)
class CfnCampaignMixinProps:
    def __init__(
        self,
        *,
        channel_subtype_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ChannelSubtypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        communication_limits_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CommunicationLimitsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        communication_time_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CommunicationTimeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connect_campaign_flow_arn: typing.Optional[builtins.str] = None,
        connect_instance_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ScheduleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCampaignPropsMixin.

        :param channel_subtype_config: Contains channel subtype configuration for an outbound campaign.
        :param communication_limits_override: Communication limits configuration for an outbound campaign.
        :param communication_time_config: Contains communication time configuration for an outbound campaign.
        :param connect_campaign_flow_arn: The Amazon Resource Name (ARN) of the Amazon Connect campaign flow associated with the outbound campaign.
        :param connect_instance_id: The identifier of the Amazon Connect instance. You can find the ``instanceId`` in the ARN of the instance.
        :param name: The name of the outbound campaign.
        :param schedule: Contains the schedule configuration.
        :param source: Contains source configuration.
        :param tags: The tags used to organize, track, or control access for this resource. For example, ``{ "tags": {"key1":"value1", "key2":"value2"} }`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
            
            # agentless_config: Any
            
            cfn_campaign_mixin_props = connectcampaignsv2_mixins.CfnCampaignMixinProps(
                channel_subtype_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ChannelSubtypeConfigProperty(
                    email=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty(
                        capacity=123,
                        default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundConfigProperty(
                            connect_source_email_address="connectSourceEmailAddress",
                            source_email_address_display_name="sourceEmailAddressDisplayName",
                            wisdom_template_arn="wisdomTemplateArn"
                        ),
                        outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundModeProperty(
                            agentless_config=agentless_config
                        )
                    ),
                    sms=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty(
                        capacity=123,
                        default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundConfigProperty(
                            connect_source_phone_number_arn="connectSourcePhoneNumberArn",
                            wisdom_template_arn="wisdomTemplateArn"
                        ),
                        outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundModeProperty(
                            agentless_config=agentless_config
                        )
                    ),
                    telephony=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty(
                        capacity=123,
                        connect_queue_id="connectQueueId",
                        default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundConfigProperty(
                            answer_machine_detection_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                                await_answer_machine_prompt=False,
                                enable_answer_machine_detection=False
                            ),
                            connect_contact_flow_id="connectContactFlowId",
                            connect_source_phone_number="connectSourcePhoneNumber",
                            ring_timeout=123
                        ),
                        outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundModeProperty(
                            agentless_config=agentless_config,
                            predictive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PredictiveConfigProperty(
                                bandwidth_allocation=123
                            ),
                            preview_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PreviewConfigProperty(
                                agent_actions=["agentActions"],
                                bandwidth_allocation=123,
                                timeout_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                                    duration_in_seconds=123
                                )
                            ),
                            progressive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty(
                                bandwidth_allocation=123
                            )
                        )
                    )
                ),
                communication_limits_override=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsConfigProperty(
                    all_channels_subtypes=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsProperty(
                        communication_limit_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitProperty(
                            frequency=123,
                            max_count_per_recipient=123,
                            unit="unit"
                        )]
                    ),
                    instance_limits_handling="instanceLimitsHandling"
                ),
                communication_time_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationTimeConfigProperty(
                    email=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                        open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                            daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                                key="key",
                                value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                    end_time="endTime",
                                    start_time="startTime"
                                )]
                            )]
                        ),
                        restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                            restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                                end_date="endDate",
                                name="name",
                                start_date="startDate"
                            )]
                        )
                    ),
                    local_time_zone_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.LocalTimeZoneConfigProperty(
                        default_time_zone="defaultTimeZone",
                        local_time_zone_detection=["localTimeZoneDetection"]
                    ),
                    sms=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                        open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                            daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                                key="key",
                                value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                    end_time="endTime",
                                    start_time="startTime"
                                )]
                            )]
                        ),
                        restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                            restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                                end_date="endDate",
                                name="name",
                                start_date="startDate"
                            )]
                        )
                    ),
                    telephony=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                        open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                            daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                                key="key",
                                value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                    end_time="endTime",
                                    start_time="startTime"
                                )]
                            )]
                        ),
                        restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                            restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                                end_date="endDate",
                                name="name",
                                start_date="startDate"
                            )]
                        )
                    )
                ),
                connect_campaign_flow_arn="connectCampaignFlowArn",
                connect_instance_id="connectInstanceId",
                name="name",
                schedule=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                    end_time="endTime",
                    refresh_frequency="refreshFrequency",
                    start_time="startTime"
                ),
                source=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SourceProperty(
                    customer_profiles_segment_arn="customerProfilesSegmentArn",
                    event_trigger=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EventTriggerProperty(
                        customer_profiles_domain_arn="customerProfilesDomainArn"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a80723531dc34190446fc53de16afcc0e165d0feac689f029a0ce2eb72a00bc7)
            check_type(argname="argument channel_subtype_config", value=channel_subtype_config, expected_type=type_hints["channel_subtype_config"])
            check_type(argname="argument communication_limits_override", value=communication_limits_override, expected_type=type_hints["communication_limits_override"])
            check_type(argname="argument communication_time_config", value=communication_time_config, expected_type=type_hints["communication_time_config"])
            check_type(argname="argument connect_campaign_flow_arn", value=connect_campaign_flow_arn, expected_type=type_hints["connect_campaign_flow_arn"])
            check_type(argname="argument connect_instance_id", value=connect_instance_id, expected_type=type_hints["connect_instance_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_subtype_config is not None:
            self._values["channel_subtype_config"] = channel_subtype_config
        if communication_limits_override is not None:
            self._values["communication_limits_override"] = communication_limits_override
        if communication_time_config is not None:
            self._values["communication_time_config"] = communication_time_config
        if connect_campaign_flow_arn is not None:
            self._values["connect_campaign_flow_arn"] = connect_campaign_flow_arn
        if connect_instance_id is not None:
            self._values["connect_instance_id"] = connect_instance_id
        if name is not None:
            self._values["name"] = name
        if schedule is not None:
            self._values["schedule"] = schedule
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_subtype_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ChannelSubtypeConfigProperty"]]:
        '''Contains channel subtype configuration for an outbound campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-channelsubtypeconfig
        '''
        result = self._values.get("channel_subtype_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ChannelSubtypeConfigProperty"]], result)

    @builtins.property
    def communication_limits_override(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationLimitsConfigProperty"]]:
        '''Communication limits configuration for an outbound campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-communicationlimitsoverride
        '''
        result = self._values.get("communication_limits_override")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationLimitsConfigProperty"]], result)

    @builtins.property
    def communication_time_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationTimeConfigProperty"]]:
        '''Contains communication time configuration for an outbound campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-communicationtimeconfig
        '''
        result = self._values.get("communication_time_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationTimeConfigProperty"]], result)

    @builtins.property
    def connect_campaign_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Connect campaign flow associated with the outbound campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-connectcampaignflowarn
        '''
        result = self._values.get("connect_campaign_flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_instance_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        You can find the ``instanceId`` in the ARN of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-connectinstanceid
        '''
        result = self._values.get("connect_instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the outbound campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ScheduleProperty"]]:
        '''Contains the schedule configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ScheduleProperty"]], result)

    @builtins.property
    def source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SourceProperty"]]:
        '''Contains source configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SourceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, ``{ "tags": {"key1":"value1", "key2":"value2"} }`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html#cfn-connectcampaignsv2-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCampaignPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin",
):
    '''Creates an outbound campaign.

    .. epigraph::

       - For users to be able to view or edit a campaign at a later date by using the Amazon Connect user interface, you must add the instance ID as a tag. For example, ``{ "tags": {"owner": "arn:aws:connect:{REGION}:{AWS_ACCOUNT_ID}:instance/{CONNECT_INSTANCE_ID}"}}`` .
       - After a campaign is created, you can't add/remove source.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaignsv2-campaign.html
    :cloudformationResource: AWS::ConnectCampaignsV2::Campaign
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
        
        # agentless_config: Any
        
        cfn_campaign_props_mixin = connectcampaignsv2_mixins.CfnCampaignPropsMixin(connectcampaignsv2_mixins.CfnCampaignMixinProps(
            channel_subtype_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ChannelSubtypeConfigProperty(
                email=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty(
                    capacity=123,
                    default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundConfigProperty(
                        connect_source_email_address="connectSourceEmailAddress",
                        source_email_address_display_name="sourceEmailAddressDisplayName",
                        wisdom_template_arn="wisdomTemplateArn"
                    ),
                    outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundModeProperty(
                        agentless_config=agentless_config
                    )
                ),
                sms=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty(
                    capacity=123,
                    default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundConfigProperty(
                        connect_source_phone_number_arn="connectSourcePhoneNumberArn",
                        wisdom_template_arn="wisdomTemplateArn"
                    ),
                    outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundModeProperty(
                        agentless_config=agentless_config
                    )
                ),
                telephony=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty(
                    capacity=123,
                    connect_queue_id="connectQueueId",
                    default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundConfigProperty(
                        answer_machine_detection_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                            await_answer_machine_prompt=False,
                            enable_answer_machine_detection=False
                        ),
                        connect_contact_flow_id="connectContactFlowId",
                        connect_source_phone_number="connectSourcePhoneNumber",
                        ring_timeout=123
                    ),
                    outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundModeProperty(
                        agentless_config=agentless_config,
                        predictive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PredictiveConfigProperty(
                            bandwidth_allocation=123
                        ),
                        preview_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PreviewConfigProperty(
                            agent_actions=["agentActions"],
                            bandwidth_allocation=123,
                            timeout_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                                duration_in_seconds=123
                            )
                        ),
                        progressive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty(
                            bandwidth_allocation=123
                        )
                    )
                )
            ),
            communication_limits_override=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsConfigProperty(
                all_channels_subtypes=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsProperty(
                    communication_limit_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitProperty(
                        frequency=123,
                        max_count_per_recipient=123,
                        unit="unit"
                    )]
                ),
                instance_limits_handling="instanceLimitsHandling"
            ),
            communication_time_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationTimeConfigProperty(
                email=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                    open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                        daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                            key="key",
                            value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                end_time="endTime",
                                start_time="startTime"
                            )]
                        )]
                    ),
                    restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                        restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                            end_date="endDate",
                            name="name",
                            start_date="startDate"
                        )]
                    )
                ),
                local_time_zone_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.LocalTimeZoneConfigProperty(
                    default_time_zone="defaultTimeZone",
                    local_time_zone_detection=["localTimeZoneDetection"]
                ),
                sms=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                    open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                        daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                            key="key",
                            value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                end_time="endTime",
                                start_time="startTime"
                            )]
                        )]
                    ),
                    restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                        restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                            end_date="endDate",
                            name="name",
                            start_date="startDate"
                        )]
                    )
                ),
                telephony=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                    open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                        daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                            key="key",
                            value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                end_time="endTime",
                                start_time="startTime"
                            )]
                        )]
                    ),
                    restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                        restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                            end_date="endDate",
                            name="name",
                            start_date="startDate"
                        )]
                    )
                )
            ),
            connect_campaign_flow_arn="connectCampaignFlowArn",
            connect_instance_id="connectInstanceId",
            name="name",
            schedule=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                end_time="endTime",
                refresh_frequency="refreshFrequency",
                start_time="startTime"
            ),
            source=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SourceProperty(
                customer_profiles_segment_arn="customerProfilesSegmentArn",
                event_trigger=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EventTriggerProperty(
                    customer_profiles_domain_arn="customerProfilesDomainArn"
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
        props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ConnectCampaignsV2::Campaign``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a48070fb622490b48ae112069ec3b7fc52233daaee70b79e48c4611e0979142e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8d3e635688279416999ee13fee12a6e632f38043fb603bbd9f8e21a11ec0df3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1490ebc93bf1dda6a0d447a4586e67a591ff27bee588b771ab1d5963cf01fbc9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCampaignMixinProps:
        return typing.cast(CfnCampaignMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "await_answer_machine_prompt": "awaitAnswerMachinePrompt",
            "enable_answer_machine_detection": "enableAnswerMachineDetection",
        },
    )
    class AnswerMachineDetectionConfigProperty:
        def __init__(
            self,
            *,
            await_answer_machine_prompt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enable_answer_machine_detection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains answering machine detection configuration.

            :param await_answer_machine_prompt: Whether or not waiting for an answer machine prompt is enabled.
            :param enable_answer_machine_detection: Enables answering machine detection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-answermachinedetectionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                answer_machine_detection_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                    await_answer_machine_prompt=False,
                    enable_answer_machine_detection=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c35a5c6b9dd8829ab9bab30c0455115f1b626362966535ab8c0a1f3294bde7db)
                check_type(argname="argument await_answer_machine_prompt", value=await_answer_machine_prompt, expected_type=type_hints["await_answer_machine_prompt"])
                check_type(argname="argument enable_answer_machine_detection", value=enable_answer_machine_detection, expected_type=type_hints["enable_answer_machine_detection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if await_answer_machine_prompt is not None:
                self._values["await_answer_machine_prompt"] = await_answer_machine_prompt
            if enable_answer_machine_detection is not None:
                self._values["enable_answer_machine_detection"] = enable_answer_machine_detection

        @builtins.property
        def await_answer_machine_prompt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether or not waiting for an answer machine prompt is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-answermachinedetectionconfig.html#cfn-connectcampaignsv2-campaign-answermachinedetectionconfig-awaitanswermachineprompt
            '''
            result = self._values.get("await_answer_machine_prompt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_answer_machine_detection(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables answering machine detection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-answermachinedetectionconfig.html#cfn-connectcampaignsv2-campaign-answermachinedetectionconfig-enableanswermachinedetection
            '''
            result = self._values.get("enable_answer_machine_detection")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnswerMachineDetectionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.ChannelSubtypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"email": "email", "sms": "sms", "telephony": "telephony"},
    )
    class ChannelSubtypeConfigProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            telephony: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains channel subtype configuration for an outbound campaign.

            :param email: The configuration of the email channel subtype.
            :param sms: The configuration of the SMS channel subtype.
            :param telephony: The configuration of the telephony channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-channelsubtypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                channel_subtype_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.ChannelSubtypeConfigProperty(
                    email=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty(
                        capacity=123,
                        default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundConfigProperty(
                            connect_source_email_address="connectSourceEmailAddress",
                            source_email_address_display_name="sourceEmailAddressDisplayName",
                            wisdom_template_arn="wisdomTemplateArn"
                        ),
                        outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundModeProperty(
                            agentless_config=agentless_config
                        )
                    ),
                    sms=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty(
                        capacity=123,
                        default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundConfigProperty(
                            connect_source_phone_number_arn="connectSourcePhoneNumberArn",
                            wisdom_template_arn="wisdomTemplateArn"
                        ),
                        outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundModeProperty(
                            agentless_config=agentless_config
                        )
                    ),
                    telephony=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty(
                        capacity=123,
                        connect_queue_id="connectQueueId",
                        default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundConfigProperty(
                            answer_machine_detection_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                                await_answer_machine_prompt=False,
                                enable_answer_machine_detection=False
                            ),
                            connect_contact_flow_id="connectContactFlowId",
                            connect_source_phone_number="connectSourcePhoneNumber",
                            ring_timeout=123
                        ),
                        outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundModeProperty(
                            agentless_config=agentless_config,
                            predictive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PredictiveConfigProperty(
                                bandwidth_allocation=123
                            ),
                            preview_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PreviewConfigProperty(
                                agent_actions=["agentActions"],
                                bandwidth_allocation=123,
                                timeout_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                                    duration_in_seconds=123
                                )
                            ),
                            progressive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty(
                                bandwidth_allocation=123
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0167b706025829a2b590425c70392aa9f64e8d49aa35f579f75e13c3d578699e)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument sms", value=sms, expected_type=type_hints["sms"])
                check_type(argname="argument telephony", value=telephony, expected_type=type_hints["telephony"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if sms is not None:
                self._values["sms"] = sms
            if telephony is not None:
                self._values["telephony"] = telephony

        @builtins.property
        def email(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty"]]:
            '''The configuration of the email channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-channelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-channelsubtypeconfig-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty"]], result)

        @builtins.property
        def sms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty"]]:
            '''The configuration of the SMS channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-channelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-channelsubtypeconfig-sms
            '''
            result = self._values.get("sms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty"]], result)

        @builtins.property
        def telephony(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty"]]:
            '''The configuration of the telephony channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-channelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-channelsubtypeconfig-telephony
            '''
            result = self._values.get("telephony")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelSubtypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.CommunicationLimitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "frequency": "frequency",
            "max_count_per_recipient": "maxCountPerRecipient",
            "unit": "unit",
        },
    )
    class CommunicationLimitProperty:
        def __init__(
            self,
            *,
            frequency: typing.Optional[jsii.Number] = None,
            max_count_per_recipient: typing.Optional[jsii.Number] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a communication limit.

            :param frequency: The frequency of communication limit evaluation.
            :param max_count_per_recipient: The maximum outreaching count for each recipient.
            :param unit: The unit of communication limit evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                communication_limit_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitProperty(
                    frequency=123,
                    max_count_per_recipient=123,
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__008b847915d30bd939d726b047891c8dc9ac7b27579127aaafcceead6a756706)
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
                check_type(argname="argument max_count_per_recipient", value=max_count_per_recipient, expected_type=type_hints["max_count_per_recipient"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if frequency is not None:
                self._values["frequency"] = frequency
            if max_count_per_recipient is not None:
                self._values["max_count_per_recipient"] = max_count_per_recipient
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def frequency(self) -> typing.Optional[jsii.Number]:
            '''The frequency of communication limit evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimit.html#cfn-connectcampaignsv2-campaign-communicationlimit-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_count_per_recipient(self) -> typing.Optional[jsii.Number]:
            '''The maximum outreaching count for each recipient.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimit.html#cfn-connectcampaignsv2-campaign-communicationlimit-maxcountperrecipient
            '''
            result = self._values.get("max_count_per_recipient")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of communication limit evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimit.html#cfn-connectcampaignsv2-campaign-communicationlimit-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CommunicationLimitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.CommunicationLimitsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_channels_subtypes": "allChannelsSubtypes",
            "instance_limits_handling": "instanceLimitsHandling",
        },
    )
    class CommunicationLimitsConfigProperty:
        def __init__(
            self,
            *,
            all_channels_subtypes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CommunicationLimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_limits_handling: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the communication limits configuration for an outbound campaign.

            :param all_channels_subtypes: The CommunicationLimits that apply to all channel subtypes defined in an outbound campaign.
            :param instance_limits_handling: Opt-in or Opt-out from instance-level limits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimitsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                communication_limits_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsConfigProperty(
                    all_channels_subtypes=connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsProperty(
                        communication_limit_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitProperty(
                            frequency=123,
                            max_count_per_recipient=123,
                            unit="unit"
                        )]
                    ),
                    instance_limits_handling="instanceLimitsHandling"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecc63a71441adc23d139c70aad96c1025a8d4062c47dfc95062d18ceaaaaeb4d)
                check_type(argname="argument all_channels_subtypes", value=all_channels_subtypes, expected_type=type_hints["all_channels_subtypes"])
                check_type(argname="argument instance_limits_handling", value=instance_limits_handling, expected_type=type_hints["instance_limits_handling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all_channels_subtypes is not None:
                self._values["all_channels_subtypes"] = all_channels_subtypes
            if instance_limits_handling is not None:
                self._values["instance_limits_handling"] = instance_limits_handling

        @builtins.property
        def all_channels_subtypes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationLimitsProperty"]]:
            '''The CommunicationLimits that apply to all channel subtypes defined in an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimitsconfig.html#cfn-connectcampaignsv2-campaign-communicationlimitsconfig-allchannelssubtypes
            '''
            result = self._values.get("all_channels_subtypes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationLimitsProperty"]], result)

        @builtins.property
        def instance_limits_handling(self) -> typing.Optional[builtins.str]:
            '''Opt-in or Opt-out from instance-level limits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimitsconfig.html#cfn-connectcampaignsv2-campaign-communicationlimitsconfig-instancelimitshandling
            '''
            result = self._values.get("instance_limits_handling")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CommunicationLimitsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.CommunicationLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={"communication_limit_list": "communicationLimitList"},
    )
    class CommunicationLimitsProperty:
        def __init__(
            self,
            *,
            communication_limit_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.CommunicationLimitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about communication limits.

            :param communication_limit_list: The list of CommunicationLimits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                communication_limits_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitsProperty(
                    communication_limit_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationLimitProperty(
                        frequency=123,
                        max_count_per_recipient=123,
                        unit="unit"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7927e58f0504d9e967eda2eb6b3c59df909a42c42564b4e53afa52db3319d04e)
                check_type(argname="argument communication_limit_list", value=communication_limit_list, expected_type=type_hints["communication_limit_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if communication_limit_list is not None:
                self._values["communication_limit_list"] = communication_limit_list

        @builtins.property
        def communication_limit_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationLimitProperty"]]]]:
            '''The list of CommunicationLimits.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationlimits.html#cfn-connectcampaignsv2-campaign-communicationlimits-communicationlimitlist
            '''
            result = self._values.get("communication_limit_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.CommunicationLimitProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CommunicationLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.CommunicationTimeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email": "email",
            "local_time_zone_config": "localTimeZoneConfig",
            "sms": "sms",
            "telephony": "telephony",
        },
    )
    class CommunicationTimeConfigProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            local_time_zone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.LocalTimeZoneConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            telephony: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Communication time configuration for an outbound campaign.

            :param email: The communication time configuration for the email channel subtype.
            :param local_time_zone_config: The local timezone configuration.
            :param sms: The communication time configuration for the SMS channel subtype.
            :param telephony: The communication time configuration for the telephony channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationtimeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                communication_time_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.CommunicationTimeConfigProperty(
                    email=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                        open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                            daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                                key="key",
                                value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                    end_time="endTime",
                                    start_time="startTime"
                                )]
                            )]
                        ),
                        restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                            restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                                end_date="endDate",
                                name="name",
                                start_date="startDate"
                            )]
                        )
                    ),
                    local_time_zone_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.LocalTimeZoneConfigProperty(
                        default_time_zone="defaultTimeZone",
                        local_time_zone_detection=["localTimeZoneDetection"]
                    ),
                    sms=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                        open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                            daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                                key="key",
                                value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                    end_time="endTime",
                                    start_time="startTime"
                                )]
                            )]
                        ),
                        restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                            restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                                end_date="endDate",
                                name="name",
                                start_date="startDate"
                            )]
                        )
                    ),
                    telephony=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                        open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                            daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                                key="key",
                                value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                    end_time="endTime",
                                    start_time="startTime"
                                )]
                            )]
                        ),
                        restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                            restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                                end_date="endDate",
                                name="name",
                                start_date="startDate"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0e253f743f4255aa7e1980faa5d987500196bccd0cf4c0c4e03dfa86afba307)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument local_time_zone_config", value=local_time_zone_config, expected_type=type_hints["local_time_zone_config"])
                check_type(argname="argument sms", value=sms, expected_type=type_hints["sms"])
                check_type(argname="argument telephony", value=telephony, expected_type=type_hints["telephony"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if local_time_zone_config is not None:
                self._values["local_time_zone_config"] = local_time_zone_config
            if sms is not None:
                self._values["sms"] = sms
            if telephony is not None:
                self._values["telephony"] = telephony

        @builtins.property
        def email(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeWindowProperty"]]:
            '''The communication time configuration for the email channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationtimeconfig.html#cfn-connectcampaignsv2-campaign-communicationtimeconfig-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeWindowProperty"]], result)

        @builtins.property
        def local_time_zone_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.LocalTimeZoneConfigProperty"]]:
            '''The local timezone configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationtimeconfig.html#cfn-connectcampaignsv2-campaign-communicationtimeconfig-localtimezoneconfig
            '''
            result = self._values.get("local_time_zone_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.LocalTimeZoneConfigProperty"]], result)

        @builtins.property
        def sms(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeWindowProperty"]]:
            '''The communication time configuration for the SMS channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationtimeconfig.html#cfn-connectcampaignsv2-campaign-communicationtimeconfig-sms
            '''
            result = self._values.get("sms")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeWindowProperty"]], result)

        @builtins.property
        def telephony(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeWindowProperty"]]:
            '''The communication time configuration for the telephony channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-communicationtimeconfig.html#cfn-connectcampaignsv2-campaign-communicationtimeconfig-telephony
            '''
            result = self._values.get("telephony")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeWindowProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CommunicationTimeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.DailyHourProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class DailyHourProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The daily hours configuration.

            :param key: The key for DailyHour.
            :param value: The value for DailyHour.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-dailyhour.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                daily_hour_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                    key="key",
                    value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e675133ce825e6aa6f263fecf487efb53f12e3a9c3ac690439bb77f01aeed869)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key for DailyHour.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-dailyhour.html#cfn-connectcampaignsv2-campaign-dailyhour-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeRangeProperty"]]]]:
            '''The value for DailyHour.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-dailyhour.html#cfn-connectcampaignsv2-campaign-dailyhour-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeRangeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DailyHourProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity": "capacity",
            "default_outbound_config": "defaultOutboundConfig",
            "outbound_mode": "outboundMode",
        },
    )
    class EmailChannelSubtypeConfigProperty:
        def __init__(
            self,
            *,
            capacity: typing.Optional[jsii.Number] = None,
            default_outbound_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.EmailOutboundConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outbound_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.EmailOutboundModeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for the email channel subtype.

            :param capacity: The allocation of email capacity between multiple running outbound campaigns.
            :param default_outbound_config: The default email outbound configuration of an outbound campaign.
            :param outbound_mode: The outbound mode for email of an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailchannelsubtypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                email_channel_subtype_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty(
                    capacity=123,
                    default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundConfigProperty(
                        connect_source_email_address="connectSourceEmailAddress",
                        source_email_address_display_name="sourceEmailAddressDisplayName",
                        wisdom_template_arn="wisdomTemplateArn"
                    ),
                    outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundModeProperty(
                        agentless_config=agentless_config
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eac7285331b0570ad075b3ca67aadf62e5f344e0a545faaefa940b717c21ec67)
                check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
                check_type(argname="argument default_outbound_config", value=default_outbound_config, expected_type=type_hints["default_outbound_config"])
                check_type(argname="argument outbound_mode", value=outbound_mode, expected_type=type_hints["outbound_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity is not None:
                self._values["capacity"] = capacity
            if default_outbound_config is not None:
                self._values["default_outbound_config"] = default_outbound_config
            if outbound_mode is not None:
                self._values["outbound_mode"] = outbound_mode

        @builtins.property
        def capacity(self) -> typing.Optional[jsii.Number]:
            '''The allocation of email capacity between multiple running outbound campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailchannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-emailchannelsubtypeconfig-capacity
            '''
            result = self._values.get("capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def default_outbound_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EmailOutboundConfigProperty"]]:
            '''The default email outbound configuration of an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailchannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-emailchannelsubtypeconfig-defaultoutboundconfig
            '''
            result = self._values.get("default_outbound_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EmailOutboundConfigProperty"]], result)

        @builtins.property
        def outbound_mode(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EmailOutboundModeProperty"]]:
            '''The outbound mode for email of an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailchannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-emailchannelsubtypeconfig-outboundmode
            '''
            result = self._values.get("outbound_mode")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EmailOutboundModeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailChannelSubtypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.EmailOutboundConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connect_source_email_address": "connectSourceEmailAddress",
            "source_email_address_display_name": "sourceEmailAddressDisplayName",
            "wisdom_template_arn": "wisdomTemplateArn",
        },
    )
    class EmailOutboundConfigProperty:
        def __init__(
            self,
            *,
            connect_source_email_address: typing.Optional[builtins.str] = None,
            source_email_address_display_name: typing.Optional[builtins.str] = None,
            wisdom_template_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The outbound configuration for email.

            :param connect_source_email_address: The Amazon Connect source email address.
            :param source_email_address_display_name: The display name for the Amazon Connect source email address.
            :param wisdom_template_arn: The Amazon Resource Name (ARN) of the Amazon Q in Connect template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailoutboundconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                email_outbound_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundConfigProperty(
                    connect_source_email_address="connectSourceEmailAddress",
                    source_email_address_display_name="sourceEmailAddressDisplayName",
                    wisdom_template_arn="wisdomTemplateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8824e2e4b91c36837a43be970fa81361f529ef22648f7bd98eaa6da9817e18b)
                check_type(argname="argument connect_source_email_address", value=connect_source_email_address, expected_type=type_hints["connect_source_email_address"])
                check_type(argname="argument source_email_address_display_name", value=source_email_address_display_name, expected_type=type_hints["source_email_address_display_name"])
                check_type(argname="argument wisdom_template_arn", value=wisdom_template_arn, expected_type=type_hints["wisdom_template_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connect_source_email_address is not None:
                self._values["connect_source_email_address"] = connect_source_email_address
            if source_email_address_display_name is not None:
                self._values["source_email_address_display_name"] = source_email_address_display_name
            if wisdom_template_arn is not None:
                self._values["wisdom_template_arn"] = wisdom_template_arn

        @builtins.property
        def connect_source_email_address(self) -> typing.Optional[builtins.str]:
            '''The Amazon Connect source email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailoutboundconfig.html#cfn-connectcampaignsv2-campaign-emailoutboundconfig-connectsourceemailaddress
            '''
            result = self._values.get("connect_source_email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_email_address_display_name(self) -> typing.Optional[builtins.str]:
            '''The display name for the Amazon Connect source email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailoutboundconfig.html#cfn-connectcampaignsv2-campaign-emailoutboundconfig-sourceemailaddressdisplayname
            '''
            result = self._values.get("source_email_address_display_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wisdom_template_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Q in Connect template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailoutboundconfig.html#cfn-connectcampaignsv2-campaign-emailoutboundconfig-wisdomtemplatearn
            '''
            result = self._values.get("wisdom_template_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailOutboundConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.EmailOutboundModeProperty",
        jsii_struct_bases=[],
        name_mapping={"agentless_config": "agentlessConfig"},
    )
    class EmailOutboundModeProperty:
        def __init__(self, *, agentless_config: typing.Any = None) -> None:
            '''Contains information about email outbound mode.

            :param agentless_config: The agentless outbound mode configuration for email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailoutboundmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                email_outbound_mode_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.EmailOutboundModeProperty(
                    agentless_config=agentless_config
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c541a02ab86c17dd964f7d338fbf5ad8388dc2c138371247abffcf844f37a3c8)
                check_type(argname="argument agentless_config", value=agentless_config, expected_type=type_hints["agentless_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agentless_config is not None:
                self._values["agentless_config"] = agentless_config

        @builtins.property
        def agentless_config(self) -> typing.Any:
            '''The agentless outbound mode configuration for email.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-emailoutboundmode.html#cfn-connectcampaignsv2-campaign-emailoutboundmode-agentlessconfig
            '''
            result = self._values.get("agentless_config")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailOutboundModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.EventTriggerProperty",
        jsii_struct_bases=[],
        name_mapping={"customer_profiles_domain_arn": "customerProfilesDomainArn"},
    )
    class EventTriggerProperty:
        def __init__(
            self,
            *,
            customer_profiles_domain_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The event trigger of the campaign.

            :param customer_profiles_domain_arn: The Amazon Resource Name (ARN) of the Customer Profiles domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-eventtrigger.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                event_trigger_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.EventTriggerProperty(
                    customer_profiles_domain_arn="customerProfilesDomainArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__584508cc067743cfa80ada964340cb3c5bbf4f8324af9b880f48c018b10fb0d3)
                check_type(argname="argument customer_profiles_domain_arn", value=customer_profiles_domain_arn, expected_type=type_hints["customer_profiles_domain_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_profiles_domain_arn is not None:
                self._values["customer_profiles_domain_arn"] = customer_profiles_domain_arn

        @builtins.property
        def customer_profiles_domain_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Customer Profiles domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-eventtrigger.html#cfn-connectcampaignsv2-campaign-eventtrigger-customerprofilesdomainarn
            '''
            result = self._values.get("customer_profiles_domain_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventTriggerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.LocalTimeZoneConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_time_zone": "defaultTimeZone",
            "local_time_zone_detection": "localTimeZoneDetection",
        },
    )
    class LocalTimeZoneConfigProperty:
        def __init__(
            self,
            *,
            default_time_zone: typing.Optional[builtins.str] = None,
            local_time_zone_detection: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration of timezone for recipient.

            :param default_time_zone: The timezone to use for all recipients.
            :param local_time_zone_detection: Detects methods for the recipient's timezone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-localtimezoneconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                local_time_zone_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.LocalTimeZoneConfigProperty(
                    default_time_zone="defaultTimeZone",
                    local_time_zone_detection=["localTimeZoneDetection"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1322bf61cf6f74f4ffb24c59876b09fe5034470d25a85db6d9f03292984a837)
                check_type(argname="argument default_time_zone", value=default_time_zone, expected_type=type_hints["default_time_zone"])
                check_type(argname="argument local_time_zone_detection", value=local_time_zone_detection, expected_type=type_hints["local_time_zone_detection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_time_zone is not None:
                self._values["default_time_zone"] = default_time_zone
            if local_time_zone_detection is not None:
                self._values["local_time_zone_detection"] = local_time_zone_detection

        @builtins.property
        def default_time_zone(self) -> typing.Optional[builtins.str]:
            '''The timezone to use for all recipients.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-localtimezoneconfig.html#cfn-connectcampaignsv2-campaign-localtimezoneconfig-defaulttimezone
            '''
            result = self._values.get("default_time_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_time_zone_detection(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Detects methods for the recipient's timezone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-localtimezoneconfig.html#cfn-connectcampaignsv2-campaign-localtimezoneconfig-localtimezonedetection
            '''
            result = self._values.get("local_time_zone_detection")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocalTimeZoneConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.OpenHoursProperty",
        jsii_struct_bases=[],
        name_mapping={"daily_hours": "dailyHours"},
    )
    class OpenHoursProperty:
        def __init__(
            self,
            *,
            daily_hours: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DailyHourProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about open hours.

            :param daily_hours: The daily hours configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-openhours.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                open_hours_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                    daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                        key="key",
                        value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                            end_time="endTime",
                            start_time="startTime"
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efc9409e8c4b92b7cd251d6acdffc011e22a01ec0054a9bbda8d1a78a522cb8d)
                check_type(argname="argument daily_hours", value=daily_hours, expected_type=type_hints["daily_hours"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily_hours is not None:
                self._values["daily_hours"] = daily_hours

        @builtins.property
        def daily_hours(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DailyHourProperty"]]]]:
            '''The daily hours configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-openhours.html#cfn-connectcampaignsv2-campaign-openhours-dailyhours
            '''
            result = self._values.get("daily_hours")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DailyHourProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenHoursProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.PredictiveConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bandwidth_allocation": "bandwidthAllocation"},
    )
    class PredictiveConfigProperty:
        def __init__(
            self,
            *,
            bandwidth_allocation: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains predictive outbound mode configuration.

            :param bandwidth_allocation: Bandwidth allocation for the predictive outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-predictiveconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                predictive_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.PredictiveConfigProperty(
                    bandwidth_allocation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__020132f5b8b2701cf79c1256785aae9251e1737684ab28377f67a082d2644daf)
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth_allocation is not None:
                self._values["bandwidth_allocation"] = bandwidth_allocation

        @builtins.property
        def bandwidth_allocation(self) -> typing.Optional[jsii.Number]:
            '''Bandwidth allocation for the predictive outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-predictiveconfig.html#cfn-connectcampaignsv2-campaign-predictiveconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.PreviewConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "agent_actions": "agentActions",
            "bandwidth_allocation": "bandwidthAllocation",
            "timeout_config": "timeoutConfig",
        },
    )
    class PreviewConfigProperty:
        def __init__(
            self,
            *,
            agent_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            bandwidth_allocation: typing.Optional[jsii.Number] = None,
            timeout_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TimeoutConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains preview outbound mode configuration.

            :param agent_actions: Agent actions for the preview outbound mode.
            :param bandwidth_allocation: Bandwidth allocation for the preview outbound mode.
            :param timeout_config: Countdown timer configuration for preview outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-previewconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                preview_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.PreviewConfigProperty(
                    agent_actions=["agentActions"],
                    bandwidth_allocation=123,
                    timeout_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                        duration_in_seconds=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__14453c74d02049671954a28f923bd5f7f361ea75da7db73d3ff4e86d018dfeb9)
                check_type(argname="argument agent_actions", value=agent_actions, expected_type=type_hints["agent_actions"])
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
                check_type(argname="argument timeout_config", value=timeout_config, expected_type=type_hints["timeout_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agent_actions is not None:
                self._values["agent_actions"] = agent_actions
            if bandwidth_allocation is not None:
                self._values["bandwidth_allocation"] = bandwidth_allocation
            if timeout_config is not None:
                self._values["timeout_config"] = timeout_config

        @builtins.property
        def agent_actions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Agent actions for the preview outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-previewconfig.html#cfn-connectcampaignsv2-campaign-previewconfig-agentactions
            '''
            result = self._values.get("agent_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def bandwidth_allocation(self) -> typing.Optional[jsii.Number]:
            '''Bandwidth allocation for the preview outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-previewconfig.html#cfn-connectcampaignsv2-campaign-previewconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeoutConfigProperty"]]:
            '''Countdown timer configuration for preview outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-previewconfig.html#cfn-connectcampaignsv2-campaign-previewconfig-timeoutconfig
            '''
            result = self._values.get("timeout_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TimeoutConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PreviewConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bandwidth_allocation": "bandwidthAllocation"},
    )
    class ProgressiveConfigProperty:
        def __init__(
            self,
            *,
            bandwidth_allocation: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains the progressive outbound mode configuration.

            :param bandwidth_allocation: Bandwidth allocation for the progressive outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-progressiveconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                progressive_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty(
                    bandwidth_allocation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fb0b428d81faed731379b23a9e07ece47d0ee6cd93bf1a2ed81666b8666cfad)
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth_allocation is not None:
                self._values["bandwidth_allocation"] = bandwidth_allocation

        @builtins.property
        def bandwidth_allocation(self) -> typing.Optional[jsii.Number]:
            '''Bandwidth allocation for the progressive outbound mode.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-progressiveconfig.html#cfn-connectcampaignsv2-campaign-progressiveconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProgressiveConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_date": "endDate",
            "name": "name",
            "start_date": "startDate",
        },
    )
    class RestrictedPeriodProperty:
        def __init__(
            self,
            *,
            end_date: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            start_date: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a restricted period.

            :param end_date: The end date of the restricted period.
            :param name: The name of the restricted period.
            :param start_date: The start date of the restricted period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-restrictedperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                restricted_period_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                    end_date="endDate",
                    name="name",
                    start_date="startDate"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__93b2f1f82c9a28068cb4386a0bd12199f23d47afcd4cceb9f80977b5d3300344)
                check_type(argname="argument end_date", value=end_date, expected_type=type_hints["end_date"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument start_date", value=start_date, expected_type=type_hints["start_date"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_date is not None:
                self._values["end_date"] = end_date
            if name is not None:
                self._values["name"] = name
            if start_date is not None:
                self._values["start_date"] = start_date

        @builtins.property
        def end_date(self) -> typing.Optional[builtins.str]:
            '''The end date of the restricted period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-restrictedperiod.html#cfn-connectcampaignsv2-campaign-restrictedperiod-enddate
            '''
            result = self._values.get("end_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the restricted period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-restrictedperiod.html#cfn-connectcampaignsv2-campaign-restrictedperiod-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_date(self) -> typing.Optional[builtins.str]:
            '''The start date of the restricted period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-restrictedperiod.html#cfn-connectcampaignsv2-campaign-restrictedperiod-startdate
            '''
            result = self._values.get("start_date")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RestrictedPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty",
        jsii_struct_bases=[],
        name_mapping={"restricted_period_list": "restrictedPeriodList"},
    )
    class RestrictedPeriodsProperty:
        def __init__(
            self,
            *,
            restricted_period_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.RestrictedPeriodProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about restricted periods.

            :param restricted_period_list: The restricted period list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-restrictedperiods.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                restricted_periods_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                    restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                        end_date="endDate",
                        name="name",
                        start_date="startDate"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c90c77dde6a687e4c014abad8d4583803535adaf98767dd44dc0e454c153b1c)
                check_type(argname="argument restricted_period_list", value=restricted_period_list, expected_type=type_hints["restricted_period_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if restricted_period_list is not None:
                self._values["restricted_period_list"] = restricted_period_list

        @builtins.property
        def restricted_period_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.RestrictedPeriodProperty"]]]]:
            '''The restricted period list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-restrictedperiods.html#cfn-connectcampaignsv2-campaign-restrictedperiods-restrictedperiodlist
            '''
            result = self._values.get("restricted_period_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.RestrictedPeriodProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RestrictedPeriodsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "end_time": "endTime",
            "refresh_frequency": "refreshFrequency",
            "start_time": "startTime",
        },
    )
    class ScheduleProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            refresh_frequency: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the schedule configuration.

            :param end_time: The end time of the schedule in UTC.
            :param refresh_frequency: The refresh frequency of the campaign.
            :param start_time: The start time of the schedule in UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-schedule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                schedule_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.ScheduleProperty(
                    end_time="endTime",
                    refresh_frequency="refreshFrequency",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec35b4961dc429a8f788ed170788eb56e97cc7e0001978e5c1b0645e7e4b6633)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument refresh_frequency", value=refresh_frequency, expected_type=type_hints["refresh_frequency"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if refresh_frequency is not None:
                self._values["refresh_frequency"] = refresh_frequency
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''The end time of the schedule in UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-schedule.html#cfn-connectcampaignsv2-campaign-schedule-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_frequency(self) -> typing.Optional[builtins.str]:
            '''The refresh frequency of the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-schedule.html#cfn-connectcampaignsv2-campaign-schedule-refreshfrequency
            '''
            result = self._values.get("refresh_frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The start time of the schedule in UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-schedule.html#cfn-connectcampaignsv2-campaign-schedule-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity": "capacity",
            "default_outbound_config": "defaultOutboundConfig",
            "outbound_mode": "outboundMode",
        },
    )
    class SmsChannelSubtypeConfigProperty:
        def __init__(
            self,
            *,
            capacity: typing.Optional[jsii.Number] = None,
            default_outbound_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SmsOutboundConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outbound_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.SmsOutboundModeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for the SMS channel subtype.

            :param capacity: The allocation of SMS capacity between multiple running outbound campaigns.
            :param default_outbound_config: The default SMS outbound configuration of an outbound campaign.
            :param outbound_mode: The outbound mode of SMS for an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smschannelsubtypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                sms_channel_subtype_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty(
                    capacity=123,
                    default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundConfigProperty(
                        connect_source_phone_number_arn="connectSourcePhoneNumberArn",
                        wisdom_template_arn="wisdomTemplateArn"
                    ),
                    outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundModeProperty(
                        agentless_config=agentless_config
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbdcb684fe753fb74d4acffc7dfb1092bc733189228383bd134520940805351a)
                check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
                check_type(argname="argument default_outbound_config", value=default_outbound_config, expected_type=type_hints["default_outbound_config"])
                check_type(argname="argument outbound_mode", value=outbound_mode, expected_type=type_hints["outbound_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity is not None:
                self._values["capacity"] = capacity
            if default_outbound_config is not None:
                self._values["default_outbound_config"] = default_outbound_config
            if outbound_mode is not None:
                self._values["outbound_mode"] = outbound_mode

        @builtins.property
        def capacity(self) -> typing.Optional[jsii.Number]:
            '''The allocation of SMS capacity between multiple running outbound campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smschannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-smschannelsubtypeconfig-capacity
            '''
            result = self._values.get("capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def default_outbound_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SmsOutboundConfigProperty"]]:
            '''The default SMS outbound configuration of an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smschannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-smschannelsubtypeconfig-defaultoutboundconfig
            '''
            result = self._values.get("default_outbound_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SmsOutboundConfigProperty"]], result)

        @builtins.property
        def outbound_mode(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SmsOutboundModeProperty"]]:
            '''The outbound mode of SMS for an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smschannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-smschannelsubtypeconfig-outboundmode
            '''
            result = self._values.get("outbound_mode")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.SmsOutboundModeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsChannelSubtypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.SmsOutboundConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connect_source_phone_number_arn": "connectSourcePhoneNumberArn",
            "wisdom_template_arn": "wisdomTemplateArn",
        },
    )
    class SmsOutboundConfigProperty:
        def __init__(
            self,
            *,
            connect_source_phone_number_arn: typing.Optional[builtins.str] = None,
            wisdom_template_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The outbound configuration for SMS.

            :param connect_source_phone_number_arn: The Amazon Resource Name (ARN) of the Amazon Connect source SMS phone number.
            :param wisdom_template_arn: The Amazon Resource Name (ARN) of the Amazon Q in Connect template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smsoutboundconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                sms_outbound_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundConfigProperty(
                    connect_source_phone_number_arn="connectSourcePhoneNumberArn",
                    wisdom_template_arn="wisdomTemplateArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__919b37a3e521ee4cfe13932eacaa6fe1471f4f77bb573860c49827422140e235)
                check_type(argname="argument connect_source_phone_number_arn", value=connect_source_phone_number_arn, expected_type=type_hints["connect_source_phone_number_arn"])
                check_type(argname="argument wisdom_template_arn", value=wisdom_template_arn, expected_type=type_hints["wisdom_template_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if connect_source_phone_number_arn is not None:
                self._values["connect_source_phone_number_arn"] = connect_source_phone_number_arn
            if wisdom_template_arn is not None:
                self._values["wisdom_template_arn"] = wisdom_template_arn

        @builtins.property
        def connect_source_phone_number_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Connect source SMS phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smsoutboundconfig.html#cfn-connectcampaignsv2-campaign-smsoutboundconfig-connectsourcephonenumberarn
            '''
            result = self._values.get("connect_source_phone_number_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def wisdom_template_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon Q in Connect template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smsoutboundconfig.html#cfn-connectcampaignsv2-campaign-smsoutboundconfig-wisdomtemplatearn
            '''
            result = self._values.get("wisdom_template_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsOutboundConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.SmsOutboundModeProperty",
        jsii_struct_bases=[],
        name_mapping={"agentless_config": "agentlessConfig"},
    )
    class SmsOutboundModeProperty:
        def __init__(self, *, agentless_config: typing.Any = None) -> None:
            '''Contains information about the SMS outbound mode.

            :param agentless_config: Contains agentless outbound mode configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smsoutboundmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                sms_outbound_mode_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.SmsOutboundModeProperty(
                    agentless_config=agentless_config
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a087eb86d2f4a33f0640575b73ac8cf7e1e9bd8438f53b14ce78262b57357755)
                check_type(argname="argument agentless_config", value=agentless_config, expected_type=type_hints["agentless_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agentless_config is not None:
                self._values["agentless_config"] = agentless_config

        @builtins.property
        def agentless_config(self) -> typing.Any:
            '''Contains agentless outbound mode configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-smsoutboundmode.html#cfn-connectcampaignsv2-campaign-smsoutboundmode-agentlessconfig
            '''
            result = self._values.get("agentless_config")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsOutboundModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_profiles_segment_arn": "customerProfilesSegmentArn",
            "event_trigger": "eventTrigger",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            customer_profiles_segment_arn: typing.Optional[builtins.str] = None,
            event_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.EventTriggerProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains source configuration.

            :param customer_profiles_segment_arn: The Amazon Resource Name (ARN) of the Customer Profiles segment.
            :param event_trigger: The event trigger of the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                source_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.SourceProperty(
                    customer_profiles_segment_arn="customerProfilesSegmentArn",
                    event_trigger=connectcampaignsv2_mixins.CfnCampaignPropsMixin.EventTriggerProperty(
                        customer_profiles_domain_arn="customerProfilesDomainArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98b8d850930f3f6d2f3ebdc951c6c9937104781e13eee07ba04ec178f5c34b75)
                check_type(argname="argument customer_profiles_segment_arn", value=customer_profiles_segment_arn, expected_type=type_hints["customer_profiles_segment_arn"])
                check_type(argname="argument event_trigger", value=event_trigger, expected_type=type_hints["event_trigger"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_profiles_segment_arn is not None:
                self._values["customer_profiles_segment_arn"] = customer_profiles_segment_arn
            if event_trigger is not None:
                self._values["event_trigger"] = event_trigger

        @builtins.property
        def customer_profiles_segment_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Customer Profiles segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-source.html#cfn-connectcampaignsv2-campaign-source-customerprofilessegmentarn
            '''
            result = self._values.get("customer_profiles_segment_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def event_trigger(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EventTriggerProperty"]]:
            '''The event trigger of the campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-source.html#cfn-connectcampaignsv2-campaign-source-eventtrigger
            '''
            result = self._values.get("event_trigger")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.EventTriggerProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capacity": "capacity",
            "connect_queue_id": "connectQueueId",
            "default_outbound_config": "defaultOutboundConfig",
            "outbound_mode": "outboundMode",
        },
    )
    class TelephonyChannelSubtypeConfigProperty:
        def __init__(
            self,
            *,
            capacity: typing.Optional[jsii.Number] = None,
            connect_queue_id: typing.Optional[builtins.str] = None,
            default_outbound_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TelephonyOutboundConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outbound_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.TelephonyOutboundModeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for the telephony channel subtype.

            :param capacity: The allocation of telephony capacity between multiple running outbound campaigns.
            :param connect_queue_id: The identifier of the Amazon Connect queue associated with telephony outbound requests of an outbound campaign.
            :param default_outbound_config: The default telephony outbound configuration of an outbound campaign.
            :param outbound_mode: The outbound mode of telephony for an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonychannelsubtypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                telephony_channel_subtype_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty(
                    capacity=123,
                    connect_queue_id="connectQueueId",
                    default_outbound_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundConfigProperty(
                        answer_machine_detection_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                            await_answer_machine_prompt=False,
                            enable_answer_machine_detection=False
                        ),
                        connect_contact_flow_id="connectContactFlowId",
                        connect_source_phone_number="connectSourcePhoneNumber",
                        ring_timeout=123
                    ),
                    outbound_mode=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundModeProperty(
                        agentless_config=agentless_config,
                        predictive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PredictiveConfigProperty(
                            bandwidth_allocation=123
                        ),
                        preview_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PreviewConfigProperty(
                            agent_actions=["agentActions"],
                            bandwidth_allocation=123,
                            timeout_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                                duration_in_seconds=123
                            )
                        ),
                        progressive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty(
                            bandwidth_allocation=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84d27bd0cae043225b9478657688d1a74df16fc6c465533a6af65e3bbd225221)
                check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
                check_type(argname="argument connect_queue_id", value=connect_queue_id, expected_type=type_hints["connect_queue_id"])
                check_type(argname="argument default_outbound_config", value=default_outbound_config, expected_type=type_hints["default_outbound_config"])
                check_type(argname="argument outbound_mode", value=outbound_mode, expected_type=type_hints["outbound_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capacity is not None:
                self._values["capacity"] = capacity
            if connect_queue_id is not None:
                self._values["connect_queue_id"] = connect_queue_id
            if default_outbound_config is not None:
                self._values["default_outbound_config"] = default_outbound_config
            if outbound_mode is not None:
                self._values["outbound_mode"] = outbound_mode

        @builtins.property
        def capacity(self) -> typing.Optional[jsii.Number]:
            '''The allocation of telephony capacity between multiple running outbound campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonychannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-telephonychannelsubtypeconfig-capacity
            '''
            result = self._values.get("capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def connect_queue_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the Amazon Connect queue associated with telephony outbound requests of an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonychannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-telephonychannelsubtypeconfig-connectqueueid
            '''
            result = self._values.get("connect_queue_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def default_outbound_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TelephonyOutboundConfigProperty"]]:
            '''The default telephony outbound configuration of an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonychannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-telephonychannelsubtypeconfig-defaultoutboundconfig
            '''
            result = self._values.get("default_outbound_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TelephonyOutboundConfigProperty"]], result)

        @builtins.property
        def outbound_mode(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TelephonyOutboundModeProperty"]]:
            '''The outbound mode of telephony for an outbound campaign.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonychannelsubtypeconfig.html#cfn-connectcampaignsv2-campaign-telephonychannelsubtypeconfig-outboundmode
            '''
            result = self._values.get("outbound_mode")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.TelephonyOutboundModeProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelephonyChannelSubtypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.TelephonyOutboundConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_machine_detection_config": "answerMachineDetectionConfig",
            "connect_contact_flow_id": "connectContactFlowId",
            "connect_source_phone_number": "connectSourcePhoneNumber",
            "ring_timeout": "ringTimeout",
        },
    )
    class TelephonyOutboundConfigProperty:
        def __init__(
            self,
            *,
            answer_machine_detection_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connect_contact_flow_id: typing.Optional[builtins.str] = None,
            connect_source_phone_number: typing.Optional[builtins.str] = None,
            ring_timeout: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The outbound configuration for telephony.

            :param answer_machine_detection_config: The answering machine detection configuration.
            :param connect_contact_flow_id: The identifier of the published Amazon Connect contact flow.
            :param connect_source_phone_number: The Amazon Connect source phone number.
            :param ring_timeout: Maximum ring time for outbound calls in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                telephony_outbound_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundConfigProperty(
                    answer_machine_detection_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                        await_answer_machine_prompt=False,
                        enable_answer_machine_detection=False
                    ),
                    connect_contact_flow_id="connectContactFlowId",
                    connect_source_phone_number="connectSourcePhoneNumber",
                    ring_timeout=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef9bcd8423cee252d1637bbda21fec7b4cf03c4278f023be54d9f70ec08f7f75)
                check_type(argname="argument answer_machine_detection_config", value=answer_machine_detection_config, expected_type=type_hints["answer_machine_detection_config"])
                check_type(argname="argument connect_contact_flow_id", value=connect_contact_flow_id, expected_type=type_hints["connect_contact_flow_id"])
                check_type(argname="argument connect_source_phone_number", value=connect_source_phone_number, expected_type=type_hints["connect_source_phone_number"])
                check_type(argname="argument ring_timeout", value=ring_timeout, expected_type=type_hints["ring_timeout"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_machine_detection_config is not None:
                self._values["answer_machine_detection_config"] = answer_machine_detection_config
            if connect_contact_flow_id is not None:
                self._values["connect_contact_flow_id"] = connect_contact_flow_id
            if connect_source_phone_number is not None:
                self._values["connect_source_phone_number"] = connect_source_phone_number
            if ring_timeout is not None:
                self._values["ring_timeout"] = ring_timeout

        @builtins.property
        def answer_machine_detection_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty"]]:
            '''The answering machine detection configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundconfig.html#cfn-connectcampaignsv2-campaign-telephonyoutboundconfig-answermachinedetectionconfig
            '''
            result = self._values.get("answer_machine_detection_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty"]], result)

        @builtins.property
        def connect_contact_flow_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the published Amazon Connect contact flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundconfig.html#cfn-connectcampaignsv2-campaign-telephonyoutboundconfig-connectcontactflowid
            '''
            result = self._values.get("connect_contact_flow_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connect_source_phone_number(self) -> typing.Optional[builtins.str]:
            '''The Amazon Connect source phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundconfig.html#cfn-connectcampaignsv2-campaign-telephonyoutboundconfig-connectsourcephonenumber
            '''
            result = self._values.get("connect_source_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ring_timeout(self) -> typing.Optional[jsii.Number]:
            '''Maximum ring time for outbound calls in seconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundconfig.html#cfn-connectcampaignsv2-campaign-telephonyoutboundconfig-ringtimeout
            '''
            result = self._values.get("ring_timeout")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelephonyOutboundConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.TelephonyOutboundModeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "agentless_config": "agentlessConfig",
            "predictive_config": "predictiveConfig",
            "preview_config": "previewConfig",
            "progressive_config": "progressiveConfig",
        },
    )
    class TelephonyOutboundModeProperty:
        def __init__(
            self,
            *,
            agentless_config: typing.Any = None,
            predictive_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.PredictiveConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            preview_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.PreviewConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            progressive_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ProgressiveConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about telephony outbound mode.

            :param agentless_config: The agentless outbound mode configuration for telephony.
            :param predictive_config: Contains predictive outbound mode configuration.
            :param preview_config: Contains preview outbound mode configuration.
            :param progressive_config: Contains progressive telephony outbound mode configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundmode.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                # agentless_config: Any
                
                telephony_outbound_mode_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.TelephonyOutboundModeProperty(
                    agentless_config=agentless_config,
                    predictive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PredictiveConfigProperty(
                        bandwidth_allocation=123
                    ),
                    preview_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.PreviewConfigProperty(
                        agent_actions=["agentActions"],
                        bandwidth_allocation=123,
                        timeout_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                            duration_in_seconds=123
                        )
                    ),
                    progressive_config=connectcampaignsv2_mixins.CfnCampaignPropsMixin.ProgressiveConfigProperty(
                        bandwidth_allocation=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a959b7064b15891f25ca1d6dc00c65356869968a3db54644e0d8f266a0e015b2)
                check_type(argname="argument agentless_config", value=agentless_config, expected_type=type_hints["agentless_config"])
                check_type(argname="argument predictive_config", value=predictive_config, expected_type=type_hints["predictive_config"])
                check_type(argname="argument preview_config", value=preview_config, expected_type=type_hints["preview_config"])
                check_type(argname="argument progressive_config", value=progressive_config, expected_type=type_hints["progressive_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agentless_config is not None:
                self._values["agentless_config"] = agentless_config
            if predictive_config is not None:
                self._values["predictive_config"] = predictive_config
            if preview_config is not None:
                self._values["preview_config"] = preview_config
            if progressive_config is not None:
                self._values["progressive_config"] = progressive_config

        @builtins.property
        def agentless_config(self) -> typing.Any:
            '''The agentless outbound mode configuration for telephony.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundmode.html#cfn-connectcampaignsv2-campaign-telephonyoutboundmode-agentlessconfig
            '''
            result = self._values.get("agentless_config")
            return typing.cast(typing.Any, result)

        @builtins.property
        def predictive_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.PredictiveConfigProperty"]]:
            '''Contains predictive outbound mode configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundmode.html#cfn-connectcampaignsv2-campaign-telephonyoutboundmode-predictiveconfig
            '''
            result = self._values.get("predictive_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.PredictiveConfigProperty"]], result)

        @builtins.property
        def preview_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.PreviewConfigProperty"]]:
            '''Contains preview outbound mode configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundmode.html#cfn-connectcampaignsv2-campaign-telephonyoutboundmode-previewconfig
            '''
            result = self._values.get("preview_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.PreviewConfigProperty"]], result)

        @builtins.property
        def progressive_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ProgressiveConfigProperty"]]:
            '''Contains progressive telephony outbound mode configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-telephonyoutboundmode.html#cfn-connectcampaignsv2-campaign-telephonyoutboundmode-progressiveconfig
            '''
            result = self._values.get("progressive_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ProgressiveConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TelephonyOutboundModeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.TimeRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"end_time": "endTime", "start_time": "startTime"},
    )
    class TimeRangeProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a time range.

            :param end_time: The end time of the time range.
            :param start_time: The start time of the time range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timerange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                time_range_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d1d528136f26b6f2991243cab3b0bb2225c2179e205fca8ee730bc55c654294)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''The end time of the time range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timerange.html#cfn-connectcampaignsv2-campaign-timerange-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''The start time of the time range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timerange.html#cfn-connectcampaignsv2-campaign-timerange-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.TimeWindowProperty",
        jsii_struct_bases=[],
        name_mapping={
            "open_hours": "openHours",
            "restricted_periods": "restrictedPeriods",
        },
    )
    class TimeWindowProperty:
        def __init__(
            self,
            *,
            open_hours: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.OpenHoursProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            restricted_periods: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.RestrictedPeriodsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about a time window.

            :param open_hours: The open hours configuration.
            :param restricted_periods: The restricted periods configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timewindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                time_window_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeWindowProperty(
                    open_hours=connectcampaignsv2_mixins.CfnCampaignPropsMixin.OpenHoursProperty(
                        daily_hours=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.DailyHourProperty(
                            key="key",
                            value=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeRangeProperty(
                                end_time="endTime",
                                start_time="startTime"
                            )]
                        )]
                    ),
                    restricted_periods=connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodsProperty(
                        restricted_period_list=[connectcampaignsv2_mixins.CfnCampaignPropsMixin.RestrictedPeriodProperty(
                            end_date="endDate",
                            name="name",
                            start_date="startDate"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b913e451998810e54f2e0bc7320b6d94c4c0a91f121091660f31c4010eeaaff5)
                check_type(argname="argument open_hours", value=open_hours, expected_type=type_hints["open_hours"])
                check_type(argname="argument restricted_periods", value=restricted_periods, expected_type=type_hints["restricted_periods"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if open_hours is not None:
                self._values["open_hours"] = open_hours
            if restricted_periods is not None:
                self._values["restricted_periods"] = restricted_periods

        @builtins.property
        def open_hours(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OpenHoursProperty"]]:
            '''The open hours configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timewindow.html#cfn-connectcampaignsv2-campaign-timewindow-openhours
            '''
            result = self._values.get("open_hours")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OpenHoursProperty"]], result)

        @builtins.property
        def restricted_periods(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.RestrictedPeriodsProperty"]]:
            '''The restricted periods configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timewindow.html#cfn-connectcampaignsv2-campaign-timewindow-restrictedperiods
            '''
            result = self._values.get("restricted_periods")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.RestrictedPeriodsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaignsv2.mixins.CfnCampaignPropsMixin.TimeoutConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"duration_in_seconds": "durationInSeconds"},
    )
    class TimeoutConfigProperty:
        def __init__(
            self,
            *,
            duration_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains preview outbound mode timeout configuration.

            :param duration_in_seconds: Duration in seconds for the countdown timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timeoutconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaignsv2 import mixins as connectcampaignsv2_mixins
                
                timeout_config_property = connectcampaignsv2_mixins.CfnCampaignPropsMixin.TimeoutConfigProperty(
                    duration_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5ee07b20865c358c11e607b305b49ffa0853551142f7cd002c1c1e8191df92a)
                check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''Duration in seconds for the countdown timer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaignsv2-campaign-timeoutconfig.html#cfn-connectcampaignsv2-campaign-timeoutconfig-durationinseconds
            '''
            result = self._values.get("duration_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeoutConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCampaignMixinProps",
    "CfnCampaignPropsMixin",
]

publication.publish()

def _typecheckingstub__a80723531dc34190446fc53de16afcc0e165d0feac689f029a0ce2eb72a00bc7(
    *,
    channel_subtype_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ChannelSubtypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    communication_limits_override: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CommunicationLimitsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    communication_time_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CommunicationTimeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_campaign_flow_arn: typing.Optional[builtins.str] = None,
    connect_instance_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a48070fb622490b48ae112069ec3b7fc52233daaee70b79e48c4611e0979142e(
    props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d3e635688279416999ee13fee12a6e632f38043fb603bbd9f8e21a11ec0df3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1490ebc93bf1dda6a0d447a4586e67a591ff27bee588b771ab1d5963cf01fbc9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c35a5c6b9dd8829ab9bab30c0455115f1b626362966535ab8c0a1f3294bde7db(
    *,
    await_answer_machine_prompt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_answer_machine_detection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0167b706025829a2b590425c70392aa9f64e8d49aa35f579f75e13c3d578699e(
    *,
    email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.EmailChannelSubtypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SmsChannelSubtypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    telephony: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TelephonyChannelSubtypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008b847915d30bd939d726b047891c8dc9ac7b27579127aaafcceead6a756706(
    *,
    frequency: typing.Optional[jsii.Number] = None,
    max_count_per_recipient: typing.Optional[jsii.Number] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecc63a71441adc23d139c70aad96c1025a8d4062c47dfc95062d18ceaaaaeb4d(
    *,
    all_channels_subtypes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CommunicationLimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_limits_handling: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7927e58f0504d9e967eda2eb6b3c59df909a42c42564b4e53afa52db3319d04e(
    *,
    communication_limit_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.CommunicationLimitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e253f743f4255aa7e1980faa5d987500196bccd0cf4c0c4e03dfa86afba307(
    *,
    email: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    local_time_zone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.LocalTimeZoneConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    telephony: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e675133ce825e6aa6f263fecf487efb53f12e3a9c3ac690439bb77f01aeed869(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac7285331b0570ad075b3ca67aadf62e5f344e0a545faaefa940b717c21ec67(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    default_outbound_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.EmailOutboundConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outbound_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.EmailOutboundModeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8824e2e4b91c36837a43be970fa81361f529ef22648f7bd98eaa6da9817e18b(
    *,
    connect_source_email_address: typing.Optional[builtins.str] = None,
    source_email_address_display_name: typing.Optional[builtins.str] = None,
    wisdom_template_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c541a02ab86c17dd964f7d338fbf5ad8388dc2c138371247abffcf844f37a3c8(
    *,
    agentless_config: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__584508cc067743cfa80ada964340cb3c5bbf4f8324af9b880f48c018b10fb0d3(
    *,
    customer_profiles_domain_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1322bf61cf6f74f4ffb24c59876b09fe5034470d25a85db6d9f03292984a837(
    *,
    default_time_zone: typing.Optional[builtins.str] = None,
    local_time_zone_detection: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc9409e8c4b92b7cd251d6acdffc011e22a01ec0054a9bbda8d1a78a522cb8d(
    *,
    daily_hours: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DailyHourProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__020132f5b8b2701cf79c1256785aae9251e1737684ab28377f67a082d2644daf(
    *,
    bandwidth_allocation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14453c74d02049671954a28f923bd5f7f361ea75da7db73d3ff4e86d018dfeb9(
    *,
    agent_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    bandwidth_allocation: typing.Optional[jsii.Number] = None,
    timeout_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TimeoutConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fb0b428d81faed731379b23a9e07ece47d0ee6cd93bf1a2ed81666b8666cfad(
    *,
    bandwidth_allocation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93b2f1f82c9a28068cb4386a0bd12199f23d47afcd4cceb9f80977b5d3300344(
    *,
    end_date: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    start_date: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c90c77dde6a687e4c014abad8d4583803535adaf98767dd44dc0e454c153b1c(
    *,
    restricted_period_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.RestrictedPeriodProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec35b4961dc429a8f788ed170788eb56e97cc7e0001978e5c1b0645e7e4b6633(
    *,
    end_time: typing.Optional[builtins.str] = None,
    refresh_frequency: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbdcb684fe753fb74d4acffc7dfb1092bc733189228383bd134520940805351a(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    default_outbound_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SmsOutboundConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outbound_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.SmsOutboundModeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919b37a3e521ee4cfe13932eacaa6fe1471f4f77bb573860c49827422140e235(
    *,
    connect_source_phone_number_arn: typing.Optional[builtins.str] = None,
    wisdom_template_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a087eb86d2f4a33f0640575b73ac8cf7e1e9bd8438f53b14ce78262b57357755(
    *,
    agentless_config: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b8d850930f3f6d2f3ebdc951c6c9937104781e13eee07ba04ec178f5c34b75(
    *,
    customer_profiles_segment_arn: typing.Optional[builtins.str] = None,
    event_trigger: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.EventTriggerProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d27bd0cae043225b9478657688d1a74df16fc6c465533a6af65e3bbd225221(
    *,
    capacity: typing.Optional[jsii.Number] = None,
    connect_queue_id: typing.Optional[builtins.str] = None,
    default_outbound_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TelephonyOutboundConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outbound_mode: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.TelephonyOutboundModeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9bcd8423cee252d1637bbda21fec7b4cf03c4278f023be54d9f70ec08f7f75(
    *,
    answer_machine_detection_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_contact_flow_id: typing.Optional[builtins.str] = None,
    connect_source_phone_number: typing.Optional[builtins.str] = None,
    ring_timeout: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a959b7064b15891f25ca1d6dc00c65356869968a3db54644e0d8f266a0e015b2(
    *,
    agentless_config: typing.Any = None,
    predictive_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.PredictiveConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    preview_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.PreviewConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    progressive_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ProgressiveConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1d528136f26b6f2991243cab3b0bb2225c2179e205fca8ee730bc55c654294(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b913e451998810e54f2e0bc7320b6d94c4c0a91f121091660f31c4010eeaaff5(
    *,
    open_hours: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.OpenHoursProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    restricted_periods: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.RestrictedPeriodsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ee07b20865c358c11e607b305b49ffa0853551142f7cd002c1c1e8191df92a(
    *,
    duration_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
