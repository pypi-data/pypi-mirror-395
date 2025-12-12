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
    jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connect_instance_arn": "connectInstanceArn",
        "dialer_config": "dialerConfig",
        "name": "name",
        "outbound_call_config": "outboundCallConfig",
        "tags": "tags",
    },
)
class CfnCampaignMixinProps:
    def __init__(
        self,
        *,
        connect_instance_arn: typing.Optional[builtins.str] = None,
        dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.DialerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        outbound_call_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.OutboundCallConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCampaignPropsMixin.

        :param connect_instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param dialer_config: Contains information about the dialer configuration.
        :param name: The name of the campaign.
        :param outbound_call_config: Contains information about the outbound call configuration.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
            
            cfn_campaign_mixin_props = connectcampaigns_mixins.CfnCampaignMixinProps(
                connect_instance_arn="connectInstanceArn",
                dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.DialerConfigProperty(
                    agentless_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.AgentlessDialerConfigProperty(
                        dialing_capacity=123
                    ),
                    predictive_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.PredictiveDialerConfigProperty(
                        bandwidth_allocation=123,
                        dialing_capacity=123
                    ),
                    progressive_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.ProgressiveDialerConfigProperty(
                        bandwidth_allocation=123,
                        dialing_capacity=123
                    )
                ),
                name="name",
                outbound_call_config=connectcampaigns_mixins.CfnCampaignPropsMixin.OutboundCallConfigProperty(
                    answer_machine_detection_config=connectcampaigns_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                        await_answer_machine_prompt=False,
                        enable_answer_machine_detection=False
                    ),
                    connect_contact_flow_arn="connectContactFlowArn",
                    connect_queue_arn="connectQueueArn",
                    connect_source_phone_number="connectSourcePhoneNumber"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb77fde443387c4a631ed91b57d0d94ace84daf9522cb6a6525356e1afa09fe5)
            check_type(argname="argument connect_instance_arn", value=connect_instance_arn, expected_type=type_hints["connect_instance_arn"])
            check_type(argname="argument dialer_config", value=dialer_config, expected_type=type_hints["dialer_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outbound_call_config", value=outbound_call_config, expected_type=type_hints["outbound_call_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connect_instance_arn is not None:
            self._values["connect_instance_arn"] = connect_instance_arn
        if dialer_config is not None:
            self._values["dialer_config"] = dialer_config
        if name is not None:
            self._values["name"] = name
        if outbound_call_config is not None:
            self._values["outbound_call_config"] = outbound_call_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connect_instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-connectinstancearn
        '''
        result = self._values.get("connect_instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dialer_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DialerConfigProperty"]]:
        '''Contains information about the dialer configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-dialerconfig
        '''
        result = self._values.get("dialer_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.DialerConfigProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the campaign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_call_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OutboundCallConfigProperty"]]:
        '''Contains information about the outbound call configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-outboundcallconfig
        '''
        result = self._values.get("outbound_call_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.OutboundCallConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin",
):
    '''Contains information about an outbound campaign.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html
    :cloudformationResource: AWS::ConnectCampaigns::Campaign
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
        
        cfn_campaign_props_mixin = connectcampaigns_mixins.CfnCampaignPropsMixin(connectcampaigns_mixins.CfnCampaignMixinProps(
            connect_instance_arn="connectInstanceArn",
            dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.DialerConfigProperty(
                agentless_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.AgentlessDialerConfigProperty(
                    dialing_capacity=123
                ),
                predictive_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.PredictiveDialerConfigProperty(
                    bandwidth_allocation=123,
                    dialing_capacity=123
                ),
                progressive_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.ProgressiveDialerConfigProperty(
                    bandwidth_allocation=123,
                    dialing_capacity=123
                )
            ),
            name="name",
            outbound_call_config=connectcampaigns_mixins.CfnCampaignPropsMixin.OutboundCallConfigProperty(
                answer_machine_detection_config=connectcampaigns_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                    await_answer_machine_prompt=False,
                    enable_answer_machine_detection=False
                ),
                connect_contact_flow_arn="connectContactFlowArn",
                connect_queue_arn="connectQueueArn",
                connect_source_phone_number="connectSourcePhoneNumber"
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
        '''Create a mixin to apply properties to ``AWS::ConnectCampaigns::Campaign``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62d9f9ad44ef760e0d77688b6652080d979465692b4bfc65587c1968ebb14602)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40d6984c84679ff8e36a372729c36ea7057c2658f26b2689a2cef96358711a05)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33ba64f88dbcdb5c698bfa571725e01fd7b19c0d1c7019a4b2a9cfe6d5a33a53)
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
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin.AgentlessDialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"dialing_capacity": "dialingCapacity"},
    )
    class AgentlessDialerConfigProperty:
        def __init__(
            self,
            *,
            dialing_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains agentless dialer configuration for an outbound campaign.

            :param dialing_capacity: The allocation of dialing capacity between multiple active campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-agentlessdialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
                
                agentless_dialer_config_property = connectcampaigns_mixins.CfnCampaignPropsMixin.AgentlessDialerConfigProperty(
                    dialing_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e2c3ddf551b78f7d99bd552d2b70d19dfe1ad63cee4661845df48df725638458)
                check_type(argname="argument dialing_capacity", value=dialing_capacity, expected_type=type_hints["dialing_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dialing_capacity is not None:
                self._values["dialing_capacity"] = dialing_capacity

        @builtins.property
        def dialing_capacity(self) -> typing.Optional[jsii.Number]:
            '''The allocation of dialing capacity between multiple active campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-agentlessdialerconfig.html#cfn-connectcampaigns-campaign-agentlessdialerconfig-dialingcapacity
            '''
            result = self._values.get("dialing_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentlessDialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty",
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
            '''Contains information about answering machine detection.

            :param await_answer_machine_prompt: Whether waiting for answer machine prompt is enabled.
            :param enable_answer_machine_detection: Whether answering machine detection is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-answermachinedetectionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
                
                answer_machine_detection_config_property = connectcampaigns_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                    await_answer_machine_prompt=False,
                    enable_answer_machine_detection=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d58ab208f993548b6b089f6991855c1e14ef9e5c305b706cdb9f7f17d14056b6)
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
            '''Whether waiting for answer machine prompt is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-answermachinedetectionconfig.html#cfn-connectcampaigns-campaign-answermachinedetectionconfig-awaitanswermachineprompt
            '''
            result = self._values.get("await_answer_machine_prompt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enable_answer_machine_detection(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Whether answering machine detection is enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-answermachinedetectionconfig.html#cfn-connectcampaigns-campaign-answermachinedetectionconfig-enableanswermachinedetection
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
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin.DialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "agentless_dialer_config": "agentlessDialerConfig",
            "predictive_dialer_config": "predictiveDialerConfig",
            "progressive_dialer_config": "progressiveDialerConfig",
        },
    )
    class DialerConfigProperty:
        def __init__(
            self,
            *,
            agentless_dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.AgentlessDialerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            predictive_dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.PredictiveDialerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            progressive_dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.ProgressiveDialerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains dialer configuration for an outbound campaign.

            :param agentless_dialer_config: The configuration of the agentless dialer.
            :param predictive_dialer_config: The configuration of the predictive dialer.
            :param progressive_dialer_config: The configuration of the progressive dialer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
                
                dialer_config_property = connectcampaigns_mixins.CfnCampaignPropsMixin.DialerConfigProperty(
                    agentless_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.AgentlessDialerConfigProperty(
                        dialing_capacity=123
                    ),
                    predictive_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.PredictiveDialerConfigProperty(
                        bandwidth_allocation=123,
                        dialing_capacity=123
                    ),
                    progressive_dialer_config=connectcampaigns_mixins.CfnCampaignPropsMixin.ProgressiveDialerConfigProperty(
                        bandwidth_allocation=123,
                        dialing_capacity=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a90582d1c34400c6ef7d8a96604697bafdcd5de5c12087e890d051ec16e72599)
                check_type(argname="argument agentless_dialer_config", value=agentless_dialer_config, expected_type=type_hints["agentless_dialer_config"])
                check_type(argname="argument predictive_dialer_config", value=predictive_dialer_config, expected_type=type_hints["predictive_dialer_config"])
                check_type(argname="argument progressive_dialer_config", value=progressive_dialer_config, expected_type=type_hints["progressive_dialer_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agentless_dialer_config is not None:
                self._values["agentless_dialer_config"] = agentless_dialer_config
            if predictive_dialer_config is not None:
                self._values["predictive_dialer_config"] = predictive_dialer_config
            if progressive_dialer_config is not None:
                self._values["progressive_dialer_config"] = progressive_dialer_config

        @builtins.property
        def agentless_dialer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.AgentlessDialerConfigProperty"]]:
            '''The configuration of the agentless dialer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-agentlessdialerconfig
            '''
            result = self._values.get("agentless_dialer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.AgentlessDialerConfigProperty"]], result)

        @builtins.property
        def predictive_dialer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.PredictiveDialerConfigProperty"]]:
            '''The configuration of the predictive dialer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-predictivedialerconfig
            '''
            result = self._values.get("predictive_dialer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.PredictiveDialerConfigProperty"]], result)

        @builtins.property
        def progressive_dialer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ProgressiveDialerConfigProperty"]]:
            '''The configuration of the progressive dialer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-progressivedialerconfig
            '''
            result = self._values.get("progressive_dialer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.ProgressiveDialerConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin.OutboundCallConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_machine_detection_config": "answerMachineDetectionConfig",
            "connect_contact_flow_arn": "connectContactFlowArn",
            "connect_queue_arn": "connectQueueArn",
            "connect_source_phone_number": "connectSourcePhoneNumber",
        },
    )
    class OutboundCallConfigProperty:
        def __init__(
            self,
            *,
            answer_machine_detection_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            connect_contact_flow_arn: typing.Optional[builtins.str] = None,
            connect_queue_arn: typing.Optional[builtins.str] = None,
            connect_source_phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains outbound call configuration for an outbound campaign.

            :param answer_machine_detection_config: Whether answering machine detection has been enabled.
            :param connect_contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param connect_queue_arn: The Amazon Resource Name (ARN) of the queue.
            :param connect_source_phone_number: The phone number associated with the outbound call. This is the caller ID that is displayed to customers when an agent calls them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
                
                outbound_call_config_property = connectcampaigns_mixins.CfnCampaignPropsMixin.OutboundCallConfigProperty(
                    answer_machine_detection_config=connectcampaigns_mixins.CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty(
                        await_answer_machine_prompt=False,
                        enable_answer_machine_detection=False
                    ),
                    connect_contact_flow_arn="connectContactFlowArn",
                    connect_queue_arn="connectQueueArn",
                    connect_source_phone_number="connectSourcePhoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f7b56462643f441f219755f72a9ba2634cd7885d42dffee853bade6deab2301)
                check_type(argname="argument answer_machine_detection_config", value=answer_machine_detection_config, expected_type=type_hints["answer_machine_detection_config"])
                check_type(argname="argument connect_contact_flow_arn", value=connect_contact_flow_arn, expected_type=type_hints["connect_contact_flow_arn"])
                check_type(argname="argument connect_queue_arn", value=connect_queue_arn, expected_type=type_hints["connect_queue_arn"])
                check_type(argname="argument connect_source_phone_number", value=connect_source_phone_number, expected_type=type_hints["connect_source_phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_machine_detection_config is not None:
                self._values["answer_machine_detection_config"] = answer_machine_detection_config
            if connect_contact_flow_arn is not None:
                self._values["connect_contact_flow_arn"] = connect_contact_flow_arn
            if connect_queue_arn is not None:
                self._values["connect_queue_arn"] = connect_queue_arn
            if connect_source_phone_number is not None:
                self._values["connect_source_phone_number"] = connect_source_phone_number

        @builtins.property
        def answer_machine_detection_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty"]]:
            '''Whether answering machine detection has been enabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-answermachinedetectionconfig
            '''
            result = self._values.get("answer_machine_detection_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty"]], result)

        @builtins.property
        def connect_contact_flow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-connectcontactflowarn
            '''
            result = self._values.get("connect_contact_flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connect_queue_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-connectqueuearn
            '''
            result = self._values.get("connect_queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def connect_source_phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number associated with the outbound call.

            This is the caller ID that is displayed to customers when an agent calls them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-connectsourcephonenumber
            '''
            result = self._values.get("connect_source_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutboundCallConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin.PredictiveDialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bandwidth_allocation": "bandwidthAllocation",
            "dialing_capacity": "dialingCapacity",
        },
    )
    class PredictiveDialerConfigProperty:
        def __init__(
            self,
            *,
            bandwidth_allocation: typing.Optional[jsii.Number] = None,
            dialing_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains predictive dialer configuration for an outbound campaign.

            :param bandwidth_allocation: Bandwidth allocation for the predictive dialer.
            :param dialing_capacity: The allocation of dialing capacity between multiple active campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-predictivedialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
                
                predictive_dialer_config_property = connectcampaigns_mixins.CfnCampaignPropsMixin.PredictiveDialerConfigProperty(
                    bandwidth_allocation=123,
                    dialing_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__19d0febeef4223da0502d2c1c96d4ba4005417169800e3129fe2a458db27cf87)
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
                check_type(argname="argument dialing_capacity", value=dialing_capacity, expected_type=type_hints["dialing_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth_allocation is not None:
                self._values["bandwidth_allocation"] = bandwidth_allocation
            if dialing_capacity is not None:
                self._values["dialing_capacity"] = dialing_capacity

        @builtins.property
        def bandwidth_allocation(self) -> typing.Optional[jsii.Number]:
            '''Bandwidth allocation for the predictive dialer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-predictivedialerconfig.html#cfn-connectcampaigns-campaign-predictivedialerconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dialing_capacity(self) -> typing.Optional[jsii.Number]:
            '''The allocation of dialing capacity between multiple active campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-predictivedialerconfig.html#cfn-connectcampaigns-campaign-predictivedialerconfig-dialingcapacity
            '''
            result = self._values.get("dialing_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveDialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connectcampaigns.mixins.CfnCampaignPropsMixin.ProgressiveDialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bandwidth_allocation": "bandwidthAllocation",
            "dialing_capacity": "dialingCapacity",
        },
    )
    class ProgressiveDialerConfigProperty:
        def __init__(
            self,
            *,
            bandwidth_allocation: typing.Optional[jsii.Number] = None,
            dialing_capacity: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains progressive dialer configuration for an outbound campaign.

            :param bandwidth_allocation: Bandwidth allocation for the progressive dialer.
            :param dialing_capacity: The allocation of dialing capacity between multiple active campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-progressivedialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connectcampaigns import mixins as connectcampaigns_mixins
                
                progressive_dialer_config_property = connectcampaigns_mixins.CfnCampaignPropsMixin.ProgressiveDialerConfigProperty(
                    bandwidth_allocation=123,
                    dialing_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d58133f9e8b56e0997784f4414ad90a36b6aa7aeb4ef117e1bfdc55c5246d2f)
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
                check_type(argname="argument dialing_capacity", value=dialing_capacity, expected_type=type_hints["dialing_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth_allocation is not None:
                self._values["bandwidth_allocation"] = bandwidth_allocation
            if dialing_capacity is not None:
                self._values["dialing_capacity"] = dialing_capacity

        @builtins.property
        def bandwidth_allocation(self) -> typing.Optional[jsii.Number]:
            '''Bandwidth allocation for the progressive dialer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-progressivedialerconfig.html#cfn-connectcampaigns-campaign-progressivedialerconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def dialing_capacity(self) -> typing.Optional[jsii.Number]:
            '''The allocation of dialing capacity between multiple active campaigns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-progressivedialerconfig.html#cfn-connectcampaigns-campaign-progressivedialerconfig-dialingcapacity
            '''
            result = self._values.get("dialing_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProgressiveDialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnCampaignMixinProps",
    "CfnCampaignPropsMixin",
]

publication.publish()

def _typecheckingstub__cb77fde443387c4a631ed91b57d0d94ace84daf9522cb6a6525356e1afa09fe5(
    *,
    connect_instance_arn: typing.Optional[builtins.str] = None,
    dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    outbound_call_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62d9f9ad44ef760e0d77688b6652080d979465692b4bfc65587c1968ebb14602(
    props: typing.Union[CfnCampaignMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d6984c84679ff8e36a372729c36ea7057c2658f26b2689a2cef96358711a05(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33ba64f88dbcdb5c698bfa571725e01fd7b19c0d1c7019a4b2a9cfe6d5a33a53(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c3ddf551b78f7d99bd552d2b70d19dfe1ad63cee4661845df48df725638458(
    *,
    dialing_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58ab208f993548b6b089f6991855c1e14ef9e5c305b706cdb9f7f17d14056b6(
    *,
    await_answer_machine_prompt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_answer_machine_detection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90582d1c34400c6ef7d8a96604697bafdcd5de5c12087e890d051ec16e72599(
    *,
    agentless_dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.AgentlessDialerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    predictive_dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.PredictiveDialerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    progressive_dialer_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.ProgressiveDialerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7b56462643f441f219755f72a9ba2634cd7885d42dffee853bade6deab2301(
    *,
    answer_machine_detection_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCampaignPropsMixin.AnswerMachineDetectionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_contact_flow_arn: typing.Optional[builtins.str] = None,
    connect_queue_arn: typing.Optional[builtins.str] = None,
    connect_source_phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d0febeef4223da0502d2c1c96d4ba4005417169800e3129fe2a458db27cf87(
    *,
    bandwidth_allocation: typing.Optional[jsii.Number] = None,
    dialing_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d58133f9e8b56e0997784f4414ad90a36b6aa7aeb4ef117e1bfdc55c5246d2f(
    *,
    bandwidth_allocation: typing.Optional[jsii.Number] = None,
    dialing_capacity: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
