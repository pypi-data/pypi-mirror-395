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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assistant_id": "assistantId",
        "configuration": "configuration",
        "description": "description",
        "name": "name",
        "tags": "tags",
        "type": "type",
    },
)
class CfnAIAgentMixinProps:
    def __init__(
        self,
        *,
        assistant_id: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAIAgentPropsMixin.

        :param assistant_id: The identifier of the Amazon Q in Connect assistant. Can be either the ID or the ARN. URLs cannot contain the ARN.
        :param configuration: Configuration for the AI Agent.
        :param description: The description of the AI Agent.
        :param name: The name of the AI Agent.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param type: The type of the AI Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_aIAgent_mixin_props = wisdom_mixins.CfnAIAgentMixinProps(
                assistant_id="assistantId",
                configuration=wisdom_mixins.CfnAIAgentPropsMixin.AIAgentConfigurationProperty(
                    answer_recommendation_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty(
                        answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                        answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        intent_labeling_generation_ai_prompt_id="intentLabelingGenerationAiPromptId",
                        locale="locale",
                        query_reformulation_ai_prompt_id="queryReformulationAiPromptId"
                    ),
                    email_generative_answer_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty(
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        email_generative_answer_ai_prompt_id="emailGenerativeAnswerAiPromptId",
                        email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                        locale="locale"
                    ),
                    email_overview_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty(
                        email_overview_ai_prompt_id="emailOverviewAiPromptId",
                        locale="locale"
                    ),
                    email_response_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty(
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                        email_response_ai_prompt_id="emailResponseAiPromptId",
                        locale="locale"
                    ),
                    manual_search_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty(
                        answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                        answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        locale="locale"
                    ),
                    self_service_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty(
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        self_service_ai_guardrail_id="selfServiceAiGuardrailId",
                        self_service_answer_generation_ai_prompt_id="selfServiceAnswerGenerationAiPromptId",
                        self_service_pre_processing_ai_prompt_id="selfServicePreProcessingAiPromptId"
                    )
                ),
                description="description",
                name="name",
                tags={
                    "tags_key": "tags"
                },
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27814174d706c442bf0c49f6a8cb21bba026f9a1674b38823df3400afad50d30)
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q in Connect assistant.

        Can be either the ID or the ARN. URLs cannot contain the ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html#cfn-wisdom-aiagent-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AIAgentConfigurationProperty"]]:
        '''Configuration for the AI Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html#cfn-wisdom-aiagent-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AIAgentConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the AI Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html#cfn-wisdom-aiagent-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AI Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html#cfn-wisdom-aiagent-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html#cfn-wisdom-aiagent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the AI Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html#cfn-wisdom-aiagent-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAIAgentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAIAgentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin",
):
    '''Creates an Amazon Q in Connect AI Agent.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagent.html
    :cloudformationResource: AWS::Wisdom::AIAgent
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_aIAgent_props_mixin = wisdom_mixins.CfnAIAgentPropsMixin(wisdom_mixins.CfnAIAgentMixinProps(
            assistant_id="assistantId",
            configuration=wisdom_mixins.CfnAIAgentPropsMixin.AIAgentConfigurationProperty(
                answer_recommendation_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty(
                    answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                    answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    intent_labeling_generation_ai_prompt_id="intentLabelingGenerationAiPromptId",
                    locale="locale",
                    query_reformulation_ai_prompt_id="queryReformulationAiPromptId"
                ),
                email_generative_answer_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty(
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    email_generative_answer_ai_prompt_id="emailGenerativeAnswerAiPromptId",
                    email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                    locale="locale"
                ),
                email_overview_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty(
                    email_overview_ai_prompt_id="emailOverviewAiPromptId",
                    locale="locale"
                ),
                email_response_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty(
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                    email_response_ai_prompt_id="emailResponseAiPromptId",
                    locale="locale"
                ),
                manual_search_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty(
                    answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                    answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    locale="locale"
                ),
                self_service_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty(
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    self_service_ai_guardrail_id="selfServiceAiGuardrailId",
                    self_service_answer_generation_ai_prompt_id="selfServiceAnswerGenerationAiPromptId",
                    self_service_pre_processing_ai_prompt_id="selfServicePreProcessingAiPromptId"
                )
            ),
            description="description",
            name="name",
            tags={
                "tags_key": "tags"
            },
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAIAgentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AIAgent``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653f77c98a2394dacf7f699b69ed637b4cf42a4db75c9f4523ce52a6b08a546c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d999820ff4ef670e7029dcbe51f2488680661d188f7d16552455042e31126284)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb46838782e66f52dcbe96cddf0e292daee05e157d3eee66c49dfb3330dd1a32)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAIAgentMixinProps:
        return typing.cast(CfnAIAgentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.AIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_recommendation_ai_agent_configuration": "answerRecommendationAiAgentConfiguration",
            "email_generative_answer_ai_agent_configuration": "emailGenerativeAnswerAiAgentConfiguration",
            "email_overview_ai_agent_configuration": "emailOverviewAiAgentConfiguration",
            "email_response_ai_agent_configuration": "emailResponseAiAgentConfiguration",
            "manual_search_ai_agent_configuration": "manualSearchAiAgentConfiguration",
            "self_service_ai_agent_configuration": "selfServiceAiAgentConfiguration",
        },
    )
    class AIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            answer_recommendation_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            email_generative_answer_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            email_overview_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            email_response_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            manual_search_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            self_service_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A typed union that specifies the configuration based on the type of AI Agent.

            :param answer_recommendation_ai_agent_configuration: The configuration for AI Agents of type ``ANSWER_RECOMMENDATION`` .
            :param email_generative_answer_ai_agent_configuration: 
            :param email_overview_ai_agent_configuration: 
            :param email_response_ai_agent_configuration: 
            :param manual_search_ai_agent_configuration: The configuration for AI Agents of type ``MANUAL_SEARCH`` .
            :param self_service_ai_agent_configuration: The self-service AI agent configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.AIAgentConfigurationProperty(
                    answer_recommendation_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty(
                        answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                        answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        intent_labeling_generation_ai_prompt_id="intentLabelingGenerationAiPromptId",
                        locale="locale",
                        query_reformulation_ai_prompt_id="queryReformulationAiPromptId"
                    ),
                    email_generative_answer_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty(
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        email_generative_answer_ai_prompt_id="emailGenerativeAnswerAiPromptId",
                        email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                        locale="locale"
                    ),
                    email_overview_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty(
                        email_overview_ai_prompt_id="emailOverviewAiPromptId",
                        locale="locale"
                    ),
                    email_response_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty(
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                        email_response_ai_prompt_id="emailResponseAiPromptId",
                        locale="locale"
                    ),
                    manual_search_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty(
                        answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                        answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        locale="locale"
                    ),
                    self_service_ai_agent_configuration=wisdom_mixins.CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty(
                        association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                            association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                                knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )],
                                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                                key="key",
                                                value="value"
                                            )
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    ),
                                    max_results=123,
                                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                                )
                            ),
                            association_id="associationId",
                            association_type="associationType"
                        )],
                        self_service_ai_guardrail_id="selfServiceAiGuardrailId",
                        self_service_answer_generation_ai_prompt_id="selfServiceAnswerGenerationAiPromptId",
                        self_service_pre_processing_ai_prompt_id="selfServicePreProcessingAiPromptId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71da4bc2d98c15d65fcbafc685c90a346d7807ac59e6b52b8967b8afe774b6f2)
                check_type(argname="argument answer_recommendation_ai_agent_configuration", value=answer_recommendation_ai_agent_configuration, expected_type=type_hints["answer_recommendation_ai_agent_configuration"])
                check_type(argname="argument email_generative_answer_ai_agent_configuration", value=email_generative_answer_ai_agent_configuration, expected_type=type_hints["email_generative_answer_ai_agent_configuration"])
                check_type(argname="argument email_overview_ai_agent_configuration", value=email_overview_ai_agent_configuration, expected_type=type_hints["email_overview_ai_agent_configuration"])
                check_type(argname="argument email_response_ai_agent_configuration", value=email_response_ai_agent_configuration, expected_type=type_hints["email_response_ai_agent_configuration"])
                check_type(argname="argument manual_search_ai_agent_configuration", value=manual_search_ai_agent_configuration, expected_type=type_hints["manual_search_ai_agent_configuration"])
                check_type(argname="argument self_service_ai_agent_configuration", value=self_service_ai_agent_configuration, expected_type=type_hints["self_service_ai_agent_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_recommendation_ai_agent_configuration is not None:
                self._values["answer_recommendation_ai_agent_configuration"] = answer_recommendation_ai_agent_configuration
            if email_generative_answer_ai_agent_configuration is not None:
                self._values["email_generative_answer_ai_agent_configuration"] = email_generative_answer_ai_agent_configuration
            if email_overview_ai_agent_configuration is not None:
                self._values["email_overview_ai_agent_configuration"] = email_overview_ai_agent_configuration
            if email_response_ai_agent_configuration is not None:
                self._values["email_response_ai_agent_configuration"] = email_response_ai_agent_configuration
            if manual_search_ai_agent_configuration is not None:
                self._values["manual_search_ai_agent_configuration"] = manual_search_ai_agent_configuration
            if self_service_ai_agent_configuration is not None:
                self._values["self_service_ai_agent_configuration"] = self_service_ai_agent_configuration

        @builtins.property
        def answer_recommendation_ai_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty"]]:
            '''The configuration for AI Agents of type ``ANSWER_RECOMMENDATION`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html#cfn-wisdom-aiagent-aiagentconfiguration-answerrecommendationaiagentconfiguration
            '''
            result = self._values.get("answer_recommendation_ai_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty"]], result)

        @builtins.property
        def email_generative_answer_ai_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html#cfn-wisdom-aiagent-aiagentconfiguration-emailgenerativeansweraiagentconfiguration
            '''
            result = self._values.get("email_generative_answer_ai_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty"]], result)

        @builtins.property
        def email_overview_ai_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html#cfn-wisdom-aiagent-aiagentconfiguration-emailoverviewaiagentconfiguration
            '''
            result = self._values.get("email_overview_ai_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty"]], result)

        @builtins.property
        def email_response_ai_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html#cfn-wisdom-aiagent-aiagentconfiguration-emailresponseaiagentconfiguration
            '''
            result = self._values.get("email_response_ai_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty"]], result)

        @builtins.property
        def manual_search_ai_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty"]]:
            '''The configuration for AI Agents of type ``MANUAL_SEARCH`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html#cfn-wisdom-aiagent-aiagentconfiguration-manualsearchaiagentconfiguration
            '''
            result = self._values.get("manual_search_ai_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty"]], result)

        @builtins.property
        def self_service_ai_agent_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty"]]:
            '''The self-service AI agent configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-aiagentconfiguration.html#cfn-wisdom-aiagent-aiagentconfiguration-selfserviceaiagentconfiguration
            '''
            result = self._values.get("self_service_ai_agent_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_generation_ai_guardrail_id": "answerGenerationAiGuardrailId",
            "answer_generation_ai_prompt_id": "answerGenerationAiPromptId",
            "association_configurations": "associationConfigurations",
            "intent_labeling_generation_ai_prompt_id": "intentLabelingGenerationAiPromptId",
            "locale": "locale",
            "query_reformulation_ai_prompt_id": "queryReformulationAiPromptId",
        },
    )
    class AnswerRecommendationAIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            answer_generation_ai_guardrail_id: typing.Optional[builtins.str] = None,
            answer_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
            association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AssociationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            intent_labeling_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
            locale: typing.Optional[builtins.str] = None,
            query_reformulation_ai_prompt_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for AI Agents of type ``ANSWER_RECOMMENDATION`` .

            :param answer_generation_ai_guardrail_id: The ID of the answer generation AI guardrail.
            :param answer_generation_ai_prompt_id: The AI Prompt identifier for the Answer Generation prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.
            :param association_configurations: The association configurations for overriding behavior on this AI Agent.
            :param intent_labeling_generation_ai_prompt_id: The AI Prompt identifier for the Intent Labeling prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.
            :param locale: The locale to which specifies the language and region settings that determine the response language for `QueryAssistant <https://docs.aws.amazon.com/connect/latest/APIReference/API_amazon-q-connect_QueryAssistant.html>`_ .
            :param query_reformulation_ai_prompt_id: The AI Prompt identifier for the Query Reformulation prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                answer_recommendation_aIAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty(
                    answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                    answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    intent_labeling_generation_ai_prompt_id="intentLabelingGenerationAiPromptId",
                    locale="locale",
                    query_reformulation_ai_prompt_id="queryReformulationAiPromptId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f3a97f9c5f20f59253470458669541d2ae79b45039a19c2c9b1f56bc349f7fa)
                check_type(argname="argument answer_generation_ai_guardrail_id", value=answer_generation_ai_guardrail_id, expected_type=type_hints["answer_generation_ai_guardrail_id"])
                check_type(argname="argument answer_generation_ai_prompt_id", value=answer_generation_ai_prompt_id, expected_type=type_hints["answer_generation_ai_prompt_id"])
                check_type(argname="argument association_configurations", value=association_configurations, expected_type=type_hints["association_configurations"])
                check_type(argname="argument intent_labeling_generation_ai_prompt_id", value=intent_labeling_generation_ai_prompt_id, expected_type=type_hints["intent_labeling_generation_ai_prompt_id"])
                check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
                check_type(argname="argument query_reformulation_ai_prompt_id", value=query_reformulation_ai_prompt_id, expected_type=type_hints["query_reformulation_ai_prompt_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_generation_ai_guardrail_id is not None:
                self._values["answer_generation_ai_guardrail_id"] = answer_generation_ai_guardrail_id
            if answer_generation_ai_prompt_id is not None:
                self._values["answer_generation_ai_prompt_id"] = answer_generation_ai_prompt_id
            if association_configurations is not None:
                self._values["association_configurations"] = association_configurations
            if intent_labeling_generation_ai_prompt_id is not None:
                self._values["intent_labeling_generation_ai_prompt_id"] = intent_labeling_generation_ai_prompt_id
            if locale is not None:
                self._values["locale"] = locale
            if query_reformulation_ai_prompt_id is not None:
                self._values["query_reformulation_ai_prompt_id"] = query_reformulation_ai_prompt_id

        @builtins.property
        def answer_generation_ai_guardrail_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the answer generation AI guardrail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html#cfn-wisdom-aiagent-answerrecommendationaiagentconfiguration-answergenerationaiguardrailid
            '''
            result = self._values.get("answer_generation_ai_guardrail_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def answer_generation_ai_prompt_id(self) -> typing.Optional[builtins.str]:
            '''The AI Prompt identifier for the Answer Generation prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html#cfn-wisdom-aiagent-answerrecommendationaiagentconfiguration-answergenerationaipromptid
            '''
            result = self._values.get("answer_generation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def association_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]]:
            '''The association configurations for overriding behavior on this AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html#cfn-wisdom-aiagent-answerrecommendationaiagentconfiguration-associationconfigurations
            '''
            result = self._values.get("association_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]], result)

        @builtins.property
        def intent_labeling_generation_ai_prompt_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The AI Prompt identifier for the Intent Labeling prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html#cfn-wisdom-aiagent-answerrecommendationaiagentconfiguration-intentlabelinggenerationaipromptid
            '''
            result = self._values.get("intent_labeling_generation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locale(self) -> typing.Optional[builtins.str]:
            '''The locale to which specifies the language and region settings that determine the response language for `QueryAssistant <https://docs.aws.amazon.com/connect/latest/APIReference/API_amazon-q-connect_QueryAssistant.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html#cfn-wisdom-aiagent-answerrecommendationaiagentconfiguration-locale
            '''
            result = self._values.get("locale")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_reformulation_ai_prompt_id(self) -> typing.Optional[builtins.str]:
            '''The AI Prompt identifier for the Query Reformulation prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-answerrecommendationaiagentconfiguration.html#cfn-wisdom-aiagent-answerrecommendationaiagentconfiguration-queryreformulationaipromptid
            '''
            result = self._values.get("query_reformulation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnswerRecommendationAIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "knowledge_base_association_configuration_data": "knowledgeBaseAssociationConfigurationData",
        },
    )
    class AssociationConfigurationDataProperty:
        def __init__(
            self,
            *,
            knowledge_base_association_configuration_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A typed union of the data of the configuration for an Amazon Q in Connect Assistant Association.

            :param knowledge_base_association_configuration_data: The data of the configuration for a ``KNOWLEDGE_BASE`` type Amazon Q in Connect Assistant Association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-associationconfigurationdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                association_configuration_data_property = wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                    knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                        content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                key="key",
                                value="value"
                            )],
                            or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                    key="key",
                                    value="value"
                                )],
                                tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                    key="key",
                                    value="value"
                                )
                            )],
                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                key="key",
                                value="value"
                            )
                        ),
                        max_results=123,
                        override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e896547aa203a0d26a01ac838077831c7df2901bc4265e346fa0ca5e7863a289)
                check_type(argname="argument knowledge_base_association_configuration_data", value=knowledge_base_association_configuration_data, expected_type=type_hints["knowledge_base_association_configuration_data"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if knowledge_base_association_configuration_data is not None:
                self._values["knowledge_base_association_configuration_data"] = knowledge_base_association_configuration_data

        @builtins.property
        def knowledge_base_association_configuration_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty"]]:
            '''The data of the configuration for a ``KNOWLEDGE_BASE`` type Amazon Q in Connect Assistant Association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-associationconfigurationdata.html#cfn-wisdom-aiagent-associationconfigurationdata-knowledgebaseassociationconfigurationdata
            '''
            result = self._values.get("knowledge_base_association_configuration_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociationConfigurationDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "association_configuration_data": "associationConfigurationData",
            "association_id": "associationId",
            "association_type": "associationType",
        },
    )
    class AssociationConfigurationProperty:
        def __init__(
            self,
            *,
            association_configuration_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AssociationConfigurationDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            association_id: typing.Optional[builtins.str] = None,
            association_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for an Amazon Q in Connect Assistant Association.

            :param association_configuration_data: A typed union of the data of the configuration for an Amazon Q in Connect Assistant Association.
            :param association_id: The identifier of the association for this Association Configuration.
            :param association_type: The type of the association for this Association Configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-associationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                association_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                    association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                        knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                            content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                    key="key",
                                    value="value"
                                )],
                                or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                )],
                                tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                    key="key",
                                    value="value"
                                )
                            ),
                            max_results=123,
                            override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                        )
                    ),
                    association_id="associationId",
                    association_type="associationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da70c2c4a16d7d9681550416155356f436f5b206af691b6b9b3844469ecddc8f)
                check_type(argname="argument association_configuration_data", value=association_configuration_data, expected_type=type_hints["association_configuration_data"])
                check_type(argname="argument association_id", value=association_id, expected_type=type_hints["association_id"])
                check_type(argname="argument association_type", value=association_type, expected_type=type_hints["association_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if association_configuration_data is not None:
                self._values["association_configuration_data"] = association_configuration_data
            if association_id is not None:
                self._values["association_id"] = association_id
            if association_type is not None:
                self._values["association_type"] = association_type

        @builtins.property
        def association_configuration_data(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationDataProperty"]]:
            '''A typed union of the data of the configuration for an Amazon Q in Connect Assistant Association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-associationconfiguration.html#cfn-wisdom-aiagent-associationconfiguration-associationconfigurationdata
            '''
            result = self._values.get("association_configuration_data")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationDataProperty"]], result)

        @builtins.property
        def association_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the association for this Association Configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-associationconfiguration.html#cfn-wisdom-aiagent-associationconfiguration-associationid
            '''
            result = self._values.get("association_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def association_type(self) -> typing.Optional[builtins.str]:
            '''The type of the association for this Association Configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-associationconfiguration.html#cfn-wisdom-aiagent-associationconfiguration-associationtype
            '''
            result = self._values.get("association_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "association_configurations": "associationConfigurations",
            "email_generative_answer_ai_prompt_id": "emailGenerativeAnswerAiPromptId",
            "email_query_reformulation_ai_prompt_id": "emailQueryReformulationAiPromptId",
            "locale": "locale",
        },
    )
    class EmailGenerativeAnswerAIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AssociationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            email_generative_answer_ai_prompt_id: typing.Optional[builtins.str] = None,
            email_query_reformulation_ai_prompt_id: typing.Optional[builtins.str] = None,
            locale: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param association_configurations: 
            :param email_generative_answer_ai_prompt_id: 
            :param email_query_reformulation_ai_prompt_id: 
            :param locale: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailgenerativeansweraiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                email_generative_answer_aIAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty(
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    email_generative_answer_ai_prompt_id="emailGenerativeAnswerAiPromptId",
                    email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                    locale="locale"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c2aa4bf99f36cfe0dc3d468197fbc00378e5d9a208cf406889f89b04f61022f)
                check_type(argname="argument association_configurations", value=association_configurations, expected_type=type_hints["association_configurations"])
                check_type(argname="argument email_generative_answer_ai_prompt_id", value=email_generative_answer_ai_prompt_id, expected_type=type_hints["email_generative_answer_ai_prompt_id"])
                check_type(argname="argument email_query_reformulation_ai_prompt_id", value=email_query_reformulation_ai_prompt_id, expected_type=type_hints["email_query_reformulation_ai_prompt_id"])
                check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if association_configurations is not None:
                self._values["association_configurations"] = association_configurations
            if email_generative_answer_ai_prompt_id is not None:
                self._values["email_generative_answer_ai_prompt_id"] = email_generative_answer_ai_prompt_id
            if email_query_reformulation_ai_prompt_id is not None:
                self._values["email_query_reformulation_ai_prompt_id"] = email_query_reformulation_ai_prompt_id
            if locale is not None:
                self._values["locale"] = locale

        @builtins.property
        def association_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailgenerativeansweraiagentconfiguration.html#cfn-wisdom-aiagent-emailgenerativeansweraiagentconfiguration-associationconfigurations
            '''
            result = self._values.get("association_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]], result)

        @builtins.property
        def email_generative_answer_ai_prompt_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailgenerativeansweraiagentconfiguration.html#cfn-wisdom-aiagent-emailgenerativeansweraiagentconfiguration-emailgenerativeansweraipromptid
            '''
            result = self._values.get("email_generative_answer_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_query_reformulation_ai_prompt_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailgenerativeansweraiagentconfiguration.html#cfn-wisdom-aiagent-emailgenerativeansweraiagentconfiguration-emailqueryreformulationaipromptid
            '''
            result = self._values.get("email_query_reformulation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locale(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailgenerativeansweraiagentconfiguration.html#cfn-wisdom-aiagent-emailgenerativeansweraiagentconfiguration-locale
            '''
            result = self._values.get("locale")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailGenerativeAnswerAIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_overview_ai_prompt_id": "emailOverviewAiPromptId",
            "locale": "locale",
        },
    )
    class EmailOverviewAIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            email_overview_ai_prompt_id: typing.Optional[builtins.str] = None,
            locale: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param email_overview_ai_prompt_id: 
            :param locale: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailoverviewaiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                email_overview_aIAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty(
                    email_overview_ai_prompt_id="emailOverviewAiPromptId",
                    locale="locale"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fc918b332ea23a60477a33368c58178e80d7c1af6bdf15f3ae994ac8d062ff5)
                check_type(argname="argument email_overview_ai_prompt_id", value=email_overview_ai_prompt_id, expected_type=type_hints["email_overview_ai_prompt_id"])
                check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_overview_ai_prompt_id is not None:
                self._values["email_overview_ai_prompt_id"] = email_overview_ai_prompt_id
            if locale is not None:
                self._values["locale"] = locale

        @builtins.property
        def email_overview_ai_prompt_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailoverviewaiagentconfiguration.html#cfn-wisdom-aiagent-emailoverviewaiagentconfiguration-emailoverviewaipromptid
            '''
            result = self._values.get("email_overview_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locale(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailoverviewaiagentconfiguration.html#cfn-wisdom-aiagent-emailoverviewaiagentconfiguration-locale
            '''
            result = self._values.get("locale")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailOverviewAIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "association_configurations": "associationConfigurations",
            "email_query_reformulation_ai_prompt_id": "emailQueryReformulationAiPromptId",
            "email_response_ai_prompt_id": "emailResponseAiPromptId",
            "locale": "locale",
        },
    )
    class EmailResponseAIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AssociationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            email_query_reformulation_ai_prompt_id: typing.Optional[builtins.str] = None,
            email_response_ai_prompt_id: typing.Optional[builtins.str] = None,
            locale: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param association_configurations: 
            :param email_query_reformulation_ai_prompt_id: 
            :param email_response_ai_prompt_id: 
            :param locale: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailresponseaiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                email_response_aIAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty(
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    email_query_reformulation_ai_prompt_id="emailQueryReformulationAiPromptId",
                    email_response_ai_prompt_id="emailResponseAiPromptId",
                    locale="locale"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01bf9b4c7838e4e0490f476ba8f9b0243b22353597d4facf45d1ffdd6cf71e29)
                check_type(argname="argument association_configurations", value=association_configurations, expected_type=type_hints["association_configurations"])
                check_type(argname="argument email_query_reformulation_ai_prompt_id", value=email_query_reformulation_ai_prompt_id, expected_type=type_hints["email_query_reformulation_ai_prompt_id"])
                check_type(argname="argument email_response_ai_prompt_id", value=email_response_ai_prompt_id, expected_type=type_hints["email_response_ai_prompt_id"])
                check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if association_configurations is not None:
                self._values["association_configurations"] = association_configurations
            if email_query_reformulation_ai_prompt_id is not None:
                self._values["email_query_reformulation_ai_prompt_id"] = email_query_reformulation_ai_prompt_id
            if email_response_ai_prompt_id is not None:
                self._values["email_response_ai_prompt_id"] = email_response_ai_prompt_id
            if locale is not None:
                self._values["locale"] = locale

        @builtins.property
        def association_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailresponseaiagentconfiguration.html#cfn-wisdom-aiagent-emailresponseaiagentconfiguration-associationconfigurations
            '''
            result = self._values.get("association_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]], result)

        @builtins.property
        def email_query_reformulation_ai_prompt_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailresponseaiagentconfiguration.html#cfn-wisdom-aiagent-emailresponseaiagentconfiguration-emailqueryreformulationaipromptid
            '''
            result = self._values.get("email_query_reformulation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def email_response_ai_prompt_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailresponseaiagentconfiguration.html#cfn-wisdom-aiagent-emailresponseaiagentconfiguration-emailresponseaipromptid
            '''
            result = self._values.get("email_response_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locale(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-emailresponseaiagentconfiguration.html#cfn-wisdom-aiagent-emailresponseaiagentconfiguration-locale
            '''
            result = self._values.get("locale")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailResponseAIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content_tag_filter": "contentTagFilter",
            "max_results": "maxResults",
            "override_knowledge_base_search_type": "overrideKnowledgeBaseSearchType",
        },
    )
    class KnowledgeBaseAssociationConfigurationDataProperty:
        def __init__(
            self,
            *,
            content_tag_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.TagFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_results: typing.Optional[jsii.Number] = None,
            override_knowledge_base_search_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The data of the configuration for a ``KNOWLEDGE_BASE`` type Amazon Q in Connect Assistant Association.

            :param content_tag_filter: An object that can be used to specify Tag conditions.
            :param max_results: The maximum number of results to return per page.
            :param override_knowledge_base_search_type: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-knowledgebaseassociationconfigurationdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                knowledge_base_association_configuration_data_property = wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                    content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                            key="key",
                            value="value"
                        )],
                        or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                            and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                key="key",
                                value="value"
                            )],
                            tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                key="key",
                                value="value"
                            )
                        )],
                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                            key="key",
                            value="value"
                        )
                    ),
                    max_results=123,
                    override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba0ab106ee71fc3667316fe727a475ce430c5584f3ebf313f3c7d9325c2a52bc)
                check_type(argname="argument content_tag_filter", value=content_tag_filter, expected_type=type_hints["content_tag_filter"])
                check_type(argname="argument max_results", value=max_results, expected_type=type_hints["max_results"])
                check_type(argname="argument override_knowledge_base_search_type", value=override_knowledge_base_search_type, expected_type=type_hints["override_knowledge_base_search_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content_tag_filter is not None:
                self._values["content_tag_filter"] = content_tag_filter
            if max_results is not None:
                self._values["max_results"] = max_results
            if override_knowledge_base_search_type is not None:
                self._values["override_knowledge_base_search_type"] = override_knowledge_base_search_type

        @builtins.property
        def content_tag_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagFilterProperty"]]:
            '''An object that can be used to specify Tag conditions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-knowledgebaseassociationconfigurationdata.html#cfn-wisdom-aiagent-knowledgebaseassociationconfigurationdata-contenttagfilter
            '''
            result = self._values.get("content_tag_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagFilterProperty"]], result)

        @builtins.property
        def max_results(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of results to return per page.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-knowledgebaseassociationconfigurationdata.html#cfn-wisdom-aiagent-knowledgebaseassociationconfigurationdata-maxresults
            '''
            result = self._values.get("max_results")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def override_knowledge_base_search_type(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-knowledgebaseassociationconfigurationdata.html#cfn-wisdom-aiagent-knowledgebaseassociationconfigurationdata-overrideknowledgebasesearchtype
            '''
            result = self._values.get("override_knowledge_base_search_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KnowledgeBaseAssociationConfigurationDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_generation_ai_guardrail_id": "answerGenerationAiGuardrailId",
            "answer_generation_ai_prompt_id": "answerGenerationAiPromptId",
            "association_configurations": "associationConfigurations",
            "locale": "locale",
        },
    )
    class ManualSearchAIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            answer_generation_ai_guardrail_id: typing.Optional[builtins.str] = None,
            answer_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
            association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AssociationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            locale: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for AI Agents of type ``MANUAL_SEARCH`` .

            :param answer_generation_ai_guardrail_id: The ID of the answer generation AI guardrail.
            :param answer_generation_ai_prompt_id: The AI Prompt identifier for the Answer Generation prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.
            :param association_configurations: The association configurations for overriding behavior on this AI Agent.
            :param locale: The locale to which specifies the language and region settings that determine the response language for `QueryAssistant <https://docs.aws.amazon.com/connect/latest/APIReference/API_amazon-q-connect_QueryAssistant.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-manualsearchaiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                manual_search_aIAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty(
                    answer_generation_ai_guardrail_id="answerGenerationAiGuardrailId",
                    answer_generation_ai_prompt_id="answerGenerationAiPromptId",
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    locale="locale"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b6397bca0a4ad1e89715ed0440adb9144887a057790323a07f885351aeb3316)
                check_type(argname="argument answer_generation_ai_guardrail_id", value=answer_generation_ai_guardrail_id, expected_type=type_hints["answer_generation_ai_guardrail_id"])
                check_type(argname="argument answer_generation_ai_prompt_id", value=answer_generation_ai_prompt_id, expected_type=type_hints["answer_generation_ai_prompt_id"])
                check_type(argname="argument association_configurations", value=association_configurations, expected_type=type_hints["association_configurations"])
                check_type(argname="argument locale", value=locale, expected_type=type_hints["locale"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_generation_ai_guardrail_id is not None:
                self._values["answer_generation_ai_guardrail_id"] = answer_generation_ai_guardrail_id
            if answer_generation_ai_prompt_id is not None:
                self._values["answer_generation_ai_prompt_id"] = answer_generation_ai_prompt_id
            if association_configurations is not None:
                self._values["association_configurations"] = association_configurations
            if locale is not None:
                self._values["locale"] = locale

        @builtins.property
        def answer_generation_ai_guardrail_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the answer generation AI guardrail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-manualsearchaiagentconfiguration.html#cfn-wisdom-aiagent-manualsearchaiagentconfiguration-answergenerationaiguardrailid
            '''
            result = self._values.get("answer_generation_ai_guardrail_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def answer_generation_ai_prompt_id(self) -> typing.Optional[builtins.str]:
            '''The AI Prompt identifier for the Answer Generation prompt used by the ``ANSWER_RECOMMENDATION`` AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-manualsearchaiagentconfiguration.html#cfn-wisdom-aiagent-manualsearchaiagentconfiguration-answergenerationaipromptid
            '''
            result = self._values.get("answer_generation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def association_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]]:
            '''The association configurations for overriding behavior on this AI Agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-manualsearchaiagentconfiguration.html#cfn-wisdom-aiagent-manualsearchaiagentconfiguration-associationconfigurations
            '''
            result = self._values.get("association_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]], result)

        @builtins.property
        def locale(self) -> typing.Optional[builtins.str]:
            '''The locale to which specifies the language and region settings that determine the response language for `QueryAssistant <https://docs.aws.amazon.com/connect/latest/APIReference/API_amazon-q-connect_QueryAssistant.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-manualsearchaiagentconfiguration.html#cfn-wisdom-aiagent-manualsearchaiagentconfiguration-locale
            '''
            result = self._values.get("locale")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManualSearchAIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.OrConditionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_conditions": "andConditions",
            "tag_condition": "tagCondition",
        },
    )
    class OrConditionProperty:
        def __init__(
            self,
            *,
            and_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.TagConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tag_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.TagConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param and_conditions: 
            :param tag_condition: A leaf node condition which can be used to specify a tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-orcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                or_condition_property = wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                        key="key",
                        value="value"
                    )],
                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                        key="key",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a1ae7a4e615e80eac5f1b8603beea51c897295cecc0ab431e5419bbce430496)
                check_type(argname="argument and_conditions", value=and_conditions, expected_type=type_hints["and_conditions"])
                check_type(argname="argument tag_condition", value=tag_condition, expected_type=type_hints["tag_condition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_conditions is not None:
                self._values["and_conditions"] = and_conditions
            if tag_condition is not None:
                self._values["tag_condition"] = tag_condition

        @builtins.property
        def and_conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-orcondition.html#cfn-wisdom-aiagent-orcondition-andconditions
            '''
            result = self._values.get("and_conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]]]], result)

        @builtins.property
        def tag_condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]]:
            '''A leaf node condition which can be used to specify a tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-orcondition.html#cfn-wisdom-aiagent-orcondition-tagcondition
            '''
            result = self._values.get("tag_condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OrConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "association_configurations": "associationConfigurations",
            "self_service_ai_guardrail_id": "selfServiceAiGuardrailId",
            "self_service_answer_generation_ai_prompt_id": "selfServiceAnswerGenerationAiPromptId",
            "self_service_pre_processing_ai_prompt_id": "selfServicePreProcessingAiPromptId",
        },
    )
    class SelfServiceAIAgentConfigurationProperty:
        def __init__(
            self,
            *,
            association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.AssociationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            self_service_ai_guardrail_id: typing.Optional[builtins.str] = None,
            self_service_answer_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
            self_service_pre_processing_ai_prompt_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration of the self-service AI agent.

            :param association_configurations: The association configuration of the self-service AI agent.
            :param self_service_ai_guardrail_id: The ID of the self-service AI guardrail.
            :param self_service_answer_generation_ai_prompt_id: The ID of the self-service answer generation AI prompt.
            :param self_service_pre_processing_ai_prompt_id: The ID of the self-service preprocessing AI prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-selfserviceaiagentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                self_service_aIAgent_configuration_property = wisdom_mixins.CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty(
                    association_configurations=[wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationProperty(
                        association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.AssociationConfigurationDataProperty(
                            knowledge_base_association_configuration_data=wisdom_mixins.CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty(
                                content_tag_filter=wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )],
                                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )],
                                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                            key="key",
                                            value="value"
                                        )
                                    )],
                                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                                        key="key",
                                        value="value"
                                    )
                                ),
                                max_results=123,
                                override_knowledge_base_search_type="overrideKnowledgeBaseSearchType"
                            )
                        ),
                        association_id="associationId",
                        association_type="associationType"
                    )],
                    self_service_ai_guardrail_id="selfServiceAiGuardrailId",
                    self_service_answer_generation_ai_prompt_id="selfServiceAnswerGenerationAiPromptId",
                    self_service_pre_processing_ai_prompt_id="selfServicePreProcessingAiPromptId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4657129cba3a012b0307cf16f29f73ce08edd03501ba59f87700f6437d167e64)
                check_type(argname="argument association_configurations", value=association_configurations, expected_type=type_hints["association_configurations"])
                check_type(argname="argument self_service_ai_guardrail_id", value=self_service_ai_guardrail_id, expected_type=type_hints["self_service_ai_guardrail_id"])
                check_type(argname="argument self_service_answer_generation_ai_prompt_id", value=self_service_answer_generation_ai_prompt_id, expected_type=type_hints["self_service_answer_generation_ai_prompt_id"])
                check_type(argname="argument self_service_pre_processing_ai_prompt_id", value=self_service_pre_processing_ai_prompt_id, expected_type=type_hints["self_service_pre_processing_ai_prompt_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if association_configurations is not None:
                self._values["association_configurations"] = association_configurations
            if self_service_ai_guardrail_id is not None:
                self._values["self_service_ai_guardrail_id"] = self_service_ai_guardrail_id
            if self_service_answer_generation_ai_prompt_id is not None:
                self._values["self_service_answer_generation_ai_prompt_id"] = self_service_answer_generation_ai_prompt_id
            if self_service_pre_processing_ai_prompt_id is not None:
                self._values["self_service_pre_processing_ai_prompt_id"] = self_service_pre_processing_ai_prompt_id

        @builtins.property
        def association_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]]:
            '''The association configuration of the self-service AI agent.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-selfserviceaiagentconfiguration.html#cfn-wisdom-aiagent-selfserviceaiagentconfiguration-associationconfigurations
            '''
            result = self._values.get("association_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.AssociationConfigurationProperty"]]]], result)

        @builtins.property
        def self_service_ai_guardrail_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the self-service AI guardrail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-selfserviceaiagentconfiguration.html#cfn-wisdom-aiagent-selfserviceaiagentconfiguration-selfserviceaiguardrailid
            '''
            result = self._values.get("self_service_ai_guardrail_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def self_service_answer_generation_ai_prompt_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The ID of the self-service answer generation AI prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-selfserviceaiagentconfiguration.html#cfn-wisdom-aiagent-selfserviceaiagentconfiguration-selfserviceanswergenerationaipromptid
            '''
            result = self._values.get("self_service_answer_generation_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def self_service_pre_processing_ai_prompt_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The ID of the self-service preprocessing AI prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-selfserviceaiagentconfiguration.html#cfn-wisdom-aiagent-selfserviceaiagentconfiguration-selfservicepreprocessingaipromptid
            '''
            result = self._values.get("self_service_pre_processing_ai_prompt_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfServiceAIAgentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.TagConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagConditionProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that can be used to specify tag conditions.

            :param key: The tag key in the tag condition.
            :param value: The tag value in the tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                tag_condition_property = wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ba42bd711c75ac17cc6f435703e4ed37cb7229f737aa9be9c73a5dc81a0e44a)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The tag key in the tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagcondition.html#cfn-wisdom-aiagent-tagcondition-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value in the tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagcondition.html#cfn-wisdom-aiagent-tagcondition-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentPropsMixin.TagFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "and_conditions": "andConditions",
            "or_conditions": "orConditions",
            "tag_condition": "tagCondition",
        },
    )
    class TagFilterProperty:
        def __init__(
            self,
            *,
            and_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.TagConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            or_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.OrConditionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tag_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIAgentPropsMixin.TagConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that can be used to specify tag conditions.

            :param and_conditions: A list of conditions which would be applied together with an ``AND`` condition.
            :param or_conditions: A list of conditions which would be applied together with an ``OR`` condition.
            :param tag_condition: A leaf node condition which can be used to specify a tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                tag_filter_property = wisdom_mixins.CfnAIAgentPropsMixin.TagFilterProperty(
                    and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                        key="key",
                        value="value"
                    )],
                    or_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.OrConditionProperty(
                        and_conditions=[wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                            key="key",
                            value="value"
                        )],
                        tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                            key="key",
                            value="value"
                        )
                    )],
                    tag_condition=wisdom_mixins.CfnAIAgentPropsMixin.TagConditionProperty(
                        key="key",
                        value="value"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__87bdf4e2dc86a1e41c1fc39eb9cf72c57798a78443d687a89ba65df038d4ff75)
                check_type(argname="argument and_conditions", value=and_conditions, expected_type=type_hints["and_conditions"])
                check_type(argname="argument or_conditions", value=or_conditions, expected_type=type_hints["or_conditions"])
                check_type(argname="argument tag_condition", value=tag_condition, expected_type=type_hints["tag_condition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if and_conditions is not None:
                self._values["and_conditions"] = and_conditions
            if or_conditions is not None:
                self._values["or_conditions"] = or_conditions
            if tag_condition is not None:
                self._values["tag_condition"] = tag_condition

        @builtins.property
        def and_conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]]]]:
            '''A list of conditions which would be applied together with an ``AND`` condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagfilter.html#cfn-wisdom-aiagent-tagfilter-andconditions
            '''
            result = self._values.get("and_conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]]]], result)

        @builtins.property
        def or_conditions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.OrConditionProperty"]]]]:
            '''A list of conditions which would be applied together with an ``OR`` condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagfilter.html#cfn-wisdom-aiagent-tagfilter-orconditions
            '''
            result = self._values.get("or_conditions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.OrConditionProperty"]]]], result)

        @builtins.property
        def tag_condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]]:
            '''A leaf node condition which can be used to specify a tag condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiagent-tagfilter.html#cfn-wisdom-aiagent-tagfilter-tagcondition
            '''
            result = self._values.get("tag_condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIAgentPropsMixin.TagConditionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ai_agent_id": "aiAgentId",
        "assistant_id": "assistantId",
        "modified_time_seconds": "modifiedTimeSeconds",
    },
)
class CfnAIAgentVersionMixinProps:
    def __init__(
        self,
        *,
        ai_agent_id: typing.Optional[builtins.str] = None,
        assistant_id: typing.Optional[builtins.str] = None,
        modified_time_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnAIAgentVersionPropsMixin.

        :param ai_agent_id: The identifier of the AI Agent.
        :param assistant_id: 
        :param modified_time_seconds: The time the AI Agent version was last modified in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagentversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_aIAgent_version_mixin_props = wisdom_mixins.CfnAIAgentVersionMixinProps(
                ai_agent_id="aiAgentId",
                assistant_id="assistantId",
                modified_time_seconds=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc06dc518fa2e4dab70d374b1450a5e5f6c567728b64ba9f1d17a49d8b80257e)
            check_type(argname="argument ai_agent_id", value=ai_agent_id, expected_type=type_hints["ai_agent_id"])
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument modified_time_seconds", value=modified_time_seconds, expected_type=type_hints["modified_time_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ai_agent_id is not None:
            self._values["ai_agent_id"] = ai_agent_id
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if modified_time_seconds is not None:
            self._values["modified_time_seconds"] = modified_time_seconds

    @builtins.property
    def ai_agent_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the AI Agent.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagentversion.html#cfn-wisdom-aiagentversion-aiagentid
        '''
        result = self._values.get("ai_agent_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagentversion.html#cfn-wisdom-aiagentversion-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modified_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time the AI Agent version was last modified in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagentversion.html#cfn-wisdom-aiagentversion-modifiedtimeseconds
        '''
        result = self._values.get("modified_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAIAgentVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAIAgentVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIAgentVersionPropsMixin",
):
    '''Creates and Amazon Q in Connect AI Agent version.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiagentversion.html
    :cloudformationResource: AWS::Wisdom::AIAgentVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_aIAgent_version_props_mixin = wisdom_mixins.CfnAIAgentVersionPropsMixin(wisdom_mixins.CfnAIAgentVersionMixinProps(
            ai_agent_id="aiAgentId",
            assistant_id="assistantId",
            modified_time_seconds=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAIAgentVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AIAgentVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f816ae07085b54433b3b755de67e1bf15e0b82493509ed8e5356b68cc0992043)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfa90b8a2e726e25113cfae6d3392d047fe0c3e278dd3c85045a47880324b32d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4d9b5597e370c198e462b17060126b5e455170e4e77fd2c15d938531a35120)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAIAgentVersionMixinProps:
        return typing.cast(CfnAIAgentVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assistant_id": "assistantId",
        "blocked_input_messaging": "blockedInputMessaging",
        "blocked_outputs_messaging": "blockedOutputsMessaging",
        "content_policy_config": "contentPolicyConfig",
        "contextual_grounding_policy_config": "contextualGroundingPolicyConfig",
        "description": "description",
        "name": "name",
        "sensitive_information_policy_config": "sensitiveInformationPolicyConfig",
        "tags": "tags",
        "topic_policy_config": "topicPolicyConfig",
        "word_policy_config": "wordPolicyConfig",
    },
)
class CfnAIGuardrailMixinProps:
    def __init__(
        self,
        *,
        assistant_id: typing.Optional[builtins.str] = None,
        blocked_input_messaging: typing.Optional[builtins.str] = None,
        blocked_outputs_messaging: typing.Optional[builtins.str] = None,
        content_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        contextual_grounding_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        sensitive_information_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        topic_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        word_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAIGuardrailPropsMixin.

        :param assistant_id: The identifier of the Amazon Q in Connect assistant. Can be either the ID or the ARN. URLs cannot contain the ARN.
        :param blocked_input_messaging: The message to return when the AI Guardrail blocks a prompt.
        :param blocked_outputs_messaging: The message to return when the AI Guardrail blocks a model response.
        :param content_policy_config: Contains details about how to handle harmful content.
        :param contextual_grounding_policy_config: The policy configuration details for the AI Guardrail's contextual grounding policy.
        :param description: A description of the AI Guardrail.
        :param name: The name of the AI Guardrail.
        :param sensitive_information_policy_config: Contains details about PII entities and regular expressions to configure for the AI Guardrail.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param topic_policy_config: Contains details about topics that the AI Guardrail should identify and deny.
        :param word_policy_config: Contains details about the word policy to configured for the AI Guardrail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_aIGuardrail_mixin_props = wisdom_mixins.CfnAIGuardrailMixinProps(
                assistant_id="assistantId",
                blocked_input_messaging="blockedInputMessaging",
                blocked_outputs_messaging="blockedOutputsMessaging",
                content_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty(
                    filters_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty(
                        input_strength="inputStrength",
                        output_strength="outputStrength",
                        type="type"
                    )]
                ),
                contextual_grounding_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty(
                    filters_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty(
                        threshold=123,
                        type="type"
                    )]
                ),
                description="description",
                name="name",
                sensitive_information_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty(
                    pii_entities_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty(
                        action="action",
                        type="type"
                    )],
                    regexes_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty(
                        action="action",
                        description="description",
                        name="name",
                        pattern="pattern"
                    )]
                ),
                tags={
                    "tags_key": "tags"
                },
                topic_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty(
                    topics_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty(
                        definition="definition",
                        examples=["examples"],
                        name="name",
                        type="type"
                    )]
                ),
                word_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty(
                    managed_word_lists_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty(
                        type="type"
                    )],
                    words_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty(
                        text="text"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2ecd494593bfb75be5ba578ec9a97ef09eaac58369015f5c987ba265b85ce3)
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument blocked_input_messaging", value=blocked_input_messaging, expected_type=type_hints["blocked_input_messaging"])
            check_type(argname="argument blocked_outputs_messaging", value=blocked_outputs_messaging, expected_type=type_hints["blocked_outputs_messaging"])
            check_type(argname="argument content_policy_config", value=content_policy_config, expected_type=type_hints["content_policy_config"])
            check_type(argname="argument contextual_grounding_policy_config", value=contextual_grounding_policy_config, expected_type=type_hints["contextual_grounding_policy_config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument sensitive_information_policy_config", value=sensitive_information_policy_config, expected_type=type_hints["sensitive_information_policy_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument topic_policy_config", value=topic_policy_config, expected_type=type_hints["topic_policy_config"])
            check_type(argname="argument word_policy_config", value=word_policy_config, expected_type=type_hints["word_policy_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if blocked_input_messaging is not None:
            self._values["blocked_input_messaging"] = blocked_input_messaging
        if blocked_outputs_messaging is not None:
            self._values["blocked_outputs_messaging"] = blocked_outputs_messaging
        if content_policy_config is not None:
            self._values["content_policy_config"] = content_policy_config
        if contextual_grounding_policy_config is not None:
            self._values["contextual_grounding_policy_config"] = contextual_grounding_policy_config
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if sensitive_information_policy_config is not None:
            self._values["sensitive_information_policy_config"] = sensitive_information_policy_config
        if tags is not None:
            self._values["tags"] = tags
        if topic_policy_config is not None:
            self._values["topic_policy_config"] = topic_policy_config
        if word_policy_config is not None:
            self._values["word_policy_config"] = word_policy_config

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q in Connect assistant.

        Can be either the ID or the ARN. URLs cannot contain the ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blocked_input_messaging(self) -> typing.Optional[builtins.str]:
        '''The message to return when the AI Guardrail blocks a prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-blockedinputmessaging
        '''
        result = self._values.get("blocked_input_messaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def blocked_outputs_messaging(self) -> typing.Optional[builtins.str]:
        '''The message to return when the AI Guardrail blocks a model response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-blockedoutputsmessaging
        '''
        result = self._values.get("blocked_outputs_messaging")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty"]]:
        '''Contains details about how to handle harmful content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-contentpolicyconfig
        '''
        result = self._values.get("content_policy_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty"]], result)

    @builtins.property
    def contextual_grounding_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty"]]:
        '''The policy configuration details for the AI Guardrail's contextual grounding policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-contextualgroundingpolicyconfig
        '''
        result = self._values.get("contextual_grounding_policy_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the AI Guardrail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AI Guardrail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sensitive_information_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty"]]:
        '''Contains details about PII entities and regular expressions to configure for the AI Guardrail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-sensitiveinformationpolicyconfig
        '''
        result = self._values.get("sensitive_information_policy_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def topic_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty"]]:
        '''Contains details about topics that the AI Guardrail should identify and deny.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-topicpolicyconfig
        '''
        result = self._values.get("topic_policy_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty"]], result)

    @builtins.property
    def word_policy_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty"]]:
        '''Contains details about the word policy to configured for the AI Guardrail.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html#cfn-wisdom-aiguardrail-wordpolicyconfig
        '''
        result = self._values.get("word_policy_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAIGuardrailMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAIGuardrailPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin",
):
    '''Creates an Amazon Q in Connect AI Guardrail.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrail.html
    :cloudformationResource: AWS::Wisdom::AIGuardrail
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_aIGuardrail_props_mixin = wisdom_mixins.CfnAIGuardrailPropsMixin(wisdom_mixins.CfnAIGuardrailMixinProps(
            assistant_id="assistantId",
            blocked_input_messaging="blockedInputMessaging",
            blocked_outputs_messaging="blockedOutputsMessaging",
            content_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty(
                filters_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty(
                    input_strength="inputStrength",
                    output_strength="outputStrength",
                    type="type"
                )]
            ),
            contextual_grounding_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty(
                filters_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty(
                    threshold=123,
                    type="type"
                )]
            ),
            description="description",
            name="name",
            sensitive_information_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty(
                pii_entities_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty(
                    action="action",
                    type="type"
                )],
                regexes_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty(
                    action="action",
                    description="description",
                    name="name",
                    pattern="pattern"
                )]
            ),
            tags={
                "tags_key": "tags"
            },
            topic_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty(
                topics_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty(
                    definition="definition",
                    examples=["examples"],
                    name="name",
                    type="type"
                )]
            ),
            word_policy_config=wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty(
                managed_word_lists_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty(
                    type="type"
                )],
                words_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty(
                    text="text"
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAIGuardrailMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AIGuardrail``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7f3a7b018e37e12bd0f97f7d763c9aa3246c6a2f9bac53a3406ff3fe4f1037)
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
            type_hints = typing.get_type_hints(_typecheckingstub__966bfef618026193f80825121659fb5740fa44eae7ab08440ecc36812bf75c64)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb2aa24a9ef6717102b82330b125e4a6657eb7a6aa674696f6cdca7bcfccf915)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAIGuardrailMixinProps:
        return typing.cast(CfnAIGuardrailMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"filters_config": "filtersConfig"},
    )
    class AIGuardrailContentPolicyConfigProperty:
        def __init__(
            self,
            *,
            filters_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Content policy config for a guardrail.

            :param filters_config: List of content filter configurations in a content policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailcontentpolicyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iGuardrail_content_policy_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty(
                    filters_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty(
                        input_strength="inputStrength",
                        output_strength="outputStrength",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e025a44b044b97d8f0b16ef1436d3183fa791bb4f8fb20e36f8cc97ffa1c6f60)
                check_type(argname="argument filters_config", value=filters_config, expected_type=type_hints["filters_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters_config is not None:
                self._values["filters_config"] = filters_config

        @builtins.property
        def filters_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty"]]]]:
            '''List of content filter configurations in a content policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailcontentpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailcontentpolicyconfig-filtersconfig
            '''
            result = self._values.get("filters_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIGuardrailContentPolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"filters_config": "filtersConfig"},
    )
    class AIGuardrailContextualGroundingPolicyConfigProperty:
        def __init__(
            self,
            *,
            filters_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contextual grounding policy config for a guardrail.

            :param filters_config: List of contextual grounding filter configs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailcontextualgroundingpolicyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iGuardrail_contextual_grounding_policy_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty(
                    filters_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty(
                        threshold=123,
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__deed4e8b272406bae1be463e4fb05093bad17abe64f3f22275ab09d670dab1e2)
                check_type(argname="argument filters_config", value=filters_config, expected_type=type_hints["filters_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters_config is not None:
                self._values["filters_config"] = filters_config

        @builtins.property
        def filters_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty"]]]]:
            '''List of contextual grounding filter configs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailcontextualgroundingpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailcontextualgroundingpolicyconfig-filtersconfig
            '''
            result = self._values.get("filters_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIGuardrailContextualGroundingPolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "pii_entities_config": "piiEntitiesConfig",
            "regexes_config": "regexesConfig",
        },
    )
    class AIGuardrailSensitiveInformationPolicyConfigProperty:
        def __init__(
            self,
            *,
            pii_entities_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            regexes_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Sensitive information policy configuration for a guardrail.

            :param pii_entities_config: List of entities.
            :param regexes_config: List of regex.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailsensitiveinformationpolicyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iGuardrail_sensitive_information_policy_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty(
                    pii_entities_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty(
                        action="action",
                        type="type"
                    )],
                    regexes_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty(
                        action="action",
                        description="description",
                        name="name",
                        pattern="pattern"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e6bc70fbe536546c27bcb82d73edb87b728b473681e921d79e17826b7e1e0c4)
                check_type(argname="argument pii_entities_config", value=pii_entities_config, expected_type=type_hints["pii_entities_config"])
                check_type(argname="argument regexes_config", value=regexes_config, expected_type=type_hints["regexes_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pii_entities_config is not None:
                self._values["pii_entities_config"] = pii_entities_config
            if regexes_config is not None:
                self._values["regexes_config"] = regexes_config

        @builtins.property
        def pii_entities_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty"]]]]:
            '''List of entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailsensitiveinformationpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailsensitiveinformationpolicyconfig-piientitiesconfig
            '''
            result = self._values.get("pii_entities_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty"]]]], result)

        @builtins.property
        def regexes_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty"]]]]:
            '''List of regex.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailsensitiveinformationpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailsensitiveinformationpolicyconfig-regexesconfig
            '''
            result = self._values.get("regexes_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIGuardrailSensitiveInformationPolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"topics_config": "topicsConfig"},
    )
    class AIGuardrailTopicPolicyConfigProperty:
        def __init__(
            self,
            *,
            topics_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Topic policy configuration for a guardrail.

            :param topics_config: List of topic configs in topic policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailtopicpolicyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iGuardrail_topic_policy_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty(
                    topics_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty(
                        definition="definition",
                        examples=["examples"],
                        name="name",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__512aa48ed4f90c3fbbbef2a13aad28514e0a03f7f53a747b190d15c012eb2dce)
                check_type(argname="argument topics_config", value=topics_config, expected_type=type_hints["topics_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topics_config is not None:
                self._values["topics_config"] = topics_config

        @builtins.property
        def topics_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty"]]]]:
            '''List of topic configs in topic policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailtopicpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailtopicpolicyconfig-topicsconfig
            '''
            result = self._values.get("topics_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIGuardrailTopicPolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "managed_word_lists_config": "managedWordListsConfig",
            "words_config": "wordsConfig",
        },
    )
    class AIGuardrailWordPolicyConfigProperty:
        def __init__(
            self,
            *,
            managed_word_lists_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            words_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Word policy config for a guardrail.

            :param managed_word_lists_config: A config for the list of managed words.
            :param words_config: List of custom word configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailwordpolicyconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iGuardrail_word_policy_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty(
                    managed_word_lists_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty(
                        type="type"
                    )],
                    words_config=[wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty(
                        text="text"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__398383d201eb7a0ef5b7a8bdcd59fc1c056802de729057444d300074b44c96ab)
                check_type(argname="argument managed_word_lists_config", value=managed_word_lists_config, expected_type=type_hints["managed_word_lists_config"])
                check_type(argname="argument words_config", value=words_config, expected_type=type_hints["words_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if managed_word_lists_config is not None:
                self._values["managed_word_lists_config"] = managed_word_lists_config
            if words_config is not None:
                self._values["words_config"] = words_config

        @builtins.property
        def managed_word_lists_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty"]]]]:
            '''A config for the list of managed words.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailwordpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailwordpolicyconfig-managedwordlistsconfig
            '''
            result = self._values.get("managed_word_lists_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty"]]]], result)

        @builtins.property
        def words_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty"]]]]:
            '''List of custom word configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-aiguardrailwordpolicyconfig.html#cfn-wisdom-aiguardrail-aiguardrailwordpolicyconfig-wordsconfig
            '''
            result = self._values.get("words_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIGuardrailWordPolicyConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_strength": "inputStrength",
            "output_strength": "outputStrength",
            "type": "type",
        },
    )
    class GuardrailContentFilterConfigProperty:
        def __init__(
            self,
            *,
            input_strength: typing.Optional[builtins.str] = None,
            output_strength: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Content filter configuration in content policy.

            :param input_strength: The strength of the input for the guardrail content filter.
            :param output_strength: The output strength of the guardrail content filter.
            :param type: The type of the guardrail content filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontentfilterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_content_filter_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty(
                    input_strength="inputStrength",
                    output_strength="outputStrength",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3a34bddba69dba5f8224859c6092c4855fac8112a35c05e0204438fc8f00a4f)
                check_type(argname="argument input_strength", value=input_strength, expected_type=type_hints["input_strength"])
                check_type(argname="argument output_strength", value=output_strength, expected_type=type_hints["output_strength"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_strength is not None:
                self._values["input_strength"] = input_strength
            if output_strength is not None:
                self._values["output_strength"] = output_strength
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def input_strength(self) -> typing.Optional[builtins.str]:
            '''The strength of the input for the guardrail content filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontentfilterconfig.html#cfn-wisdom-aiguardrail-guardrailcontentfilterconfig-inputstrength
            '''
            result = self._values.get("input_strength")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_strength(self) -> typing.Optional[builtins.str]:
            '''The output strength of the guardrail content filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontentfilterconfig.html#cfn-wisdom-aiguardrail-guardrailcontentfilterconfig-outputstrength
            '''
            result = self._values.get("output_strength")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the guardrail content filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontentfilterconfig.html#cfn-wisdom-aiguardrail-guardrailcontentfilterconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailContentFilterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"threshold": "threshold", "type": "type"},
    )
    class GuardrailContextualGroundingFilterConfigProperty:
        def __init__(
            self,
            *,
            threshold: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A configuration for grounding filter.

            :param threshold: The threshold for this filter. Default: - 0
            :param type: The type of this filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontextualgroundingfilterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_contextual_grounding_filter_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty(
                    threshold=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a2e308a2e55bab2e081d98869fe0d3fbd159f6460d1b78d04b0a3405b6945f3)
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if threshold is not None:
                self._values["threshold"] = threshold
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def threshold(self) -> typing.Optional[jsii.Number]:
            '''The threshold for this filter.

            :default: - 0

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontextualgroundingfilterconfig.html#cfn-wisdom-aiguardrail-guardrailcontextualgroundingfilterconfig-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of this filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailcontextualgroundingfilterconfig.html#cfn-wisdom-aiguardrail-guardrailcontextualgroundingfilterconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailContextualGroundingFilterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class GuardrailManagedWordsConfigProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''A managed words config.

            :param type: The type of guardrail managed words.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailmanagedwordsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_managed_words_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3f4d2eae5667fc6c4538e20fe93434b222dc24b9866bf19a49bb82e6bb37e30)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of guardrail managed words.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailmanagedwordsconfig.html#cfn-wisdom-aiguardrail-guardrailmanagedwordsconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailManagedWordsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "type": "type"},
    )
    class GuardrailPiiEntityConfigProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''PII entity configuration.

            :param action: The action of guardrail PII entity configuration.
            :param type: The currently supported PII entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailpiientityconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_pii_entity_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty(
                    action="action",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0bb3cfb203a72b86af357dc07551c59adc3b80c472f1f53458a3604bdbf36d6d)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action of guardrail PII entity configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailpiientityconfig.html#cfn-wisdom-aiguardrail-guardrailpiientityconfig-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The currently supported PII entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailpiientityconfig.html#cfn-wisdom-aiguardrail-guardrailpiientityconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailPiiEntityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "description": "description",
            "name": "name",
            "pattern": "pattern",
        },
    )
    class GuardrailRegexConfigProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            pattern: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A regex configuration.

            :param action: The action of the guardrail regex configuration.
            :param description: The regex description.
            :param name: A regex configuration.
            :param pattern: The regex pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailregexconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_regex_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty(
                    action="action",
                    description="description",
                    name="name",
                    pattern="pattern"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f7edfaf74f192951df230992e86113616049bf65ea4b73d0d775fa17cd4fc80)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if pattern is not None:
                self._values["pattern"] = pattern

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action of the guardrail regex configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailregexconfig.html#cfn-wisdom-aiguardrail-guardrailregexconfig-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The regex description.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailregexconfig.html#cfn-wisdom-aiguardrail-guardrailregexconfig-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''A regex configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailregexconfig.html#cfn-wisdom-aiguardrail-guardrailregexconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pattern(self) -> typing.Optional[builtins.str]:
            '''The regex pattern.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailregexconfig.html#cfn-wisdom-aiguardrail-guardrailregexconfig-pattern
            '''
            result = self._values.get("pattern")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailRegexConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "definition": "definition",
            "examples": "examples",
            "name": "name",
            "type": "type",
        },
    )
    class GuardrailTopicConfigProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[builtins.str] = None,
            examples: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Topic configuration in topic policy.

            :param definition: Definition of topic in topic policy.
            :param examples: Text example in topic policy.
            :param name: Name of topic in topic policy.
            :param type: Type of topic in a policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailtopicconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_topic_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty(
                    definition="definition",
                    examples=["examples"],
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c315c0639181a1ebf861cfeac750fd0e178659c01ec60a92a1e4cbf03daca4fc)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
                check_type(argname="argument examples", value=examples, expected_type=type_hints["examples"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition
            if examples is not None:
                self._values["examples"] = examples
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def definition(self) -> typing.Optional[builtins.str]:
            '''Definition of topic in topic policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailtopicconfig.html#cfn-wisdom-aiguardrail-guardrailtopicconfig-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def examples(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Text example in topic policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailtopicconfig.html#cfn-wisdom-aiguardrail-guardrailtopicconfig-examples
            '''
            result = self._values.get("examples")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of topic in topic policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailtopicconfig.html#cfn-wisdom-aiguardrail-guardrailtopicconfig-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Type of topic in a policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailtopicconfig.html#cfn-wisdom-aiguardrail-guardrailtopicconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailTopicConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text"},
    )
    class GuardrailWordConfigProperty:
        def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
            '''A custom word config.

            :param text: The custom word text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailwordconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                guardrail_word_config_property = wisdom_mixins.CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty(
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5c87c11f88f405f9143136932dbe869839acbb63263f7aca8c6d4e1da8f004a)
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The custom word text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiguardrail-guardrailwordconfig.html#cfn-wisdom-aiguardrail-guardrailwordconfig-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardrailWordConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ai_guardrail_id": "aiGuardrailId",
        "assistant_id": "assistantId",
        "modified_time_seconds": "modifiedTimeSeconds",
    },
)
class CfnAIGuardrailVersionMixinProps:
    def __init__(
        self,
        *,
        ai_guardrail_id: typing.Optional[builtins.str] = None,
        assistant_id: typing.Optional[builtins.str] = None,
        modified_time_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnAIGuardrailVersionPropsMixin.

        :param ai_guardrail_id: The ID of the AI guardrail version.
        :param assistant_id: The ID of the AI guardrail version assistant.
        :param modified_time_seconds: The modified time of the AI guardrail version in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrailversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_aIGuardrail_version_mixin_props = wisdom_mixins.CfnAIGuardrailVersionMixinProps(
                ai_guardrail_id="aiGuardrailId",
                assistant_id="assistantId",
                modified_time_seconds=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ab20783a9c0493742d1fd3adf2afca85ff24b6994f3bf846be20250bc8a850)
            check_type(argname="argument ai_guardrail_id", value=ai_guardrail_id, expected_type=type_hints["ai_guardrail_id"])
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument modified_time_seconds", value=modified_time_seconds, expected_type=type_hints["modified_time_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ai_guardrail_id is not None:
            self._values["ai_guardrail_id"] = ai_guardrail_id
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if modified_time_seconds is not None:
            self._values["modified_time_seconds"] = modified_time_seconds

    @builtins.property
    def ai_guardrail_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AI guardrail version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrailversion.html#cfn-wisdom-aiguardrailversion-aiguardrailid
        '''
        result = self._values.get("ai_guardrail_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AI guardrail version assistant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrailversion.html#cfn-wisdom-aiguardrailversion-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modified_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''The modified time of the AI guardrail version in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrailversion.html#cfn-wisdom-aiguardrailversion-modifiedtimeseconds
        '''
        result = self._values.get("modified_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAIGuardrailVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAIGuardrailVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIGuardrailVersionPropsMixin",
):
    '''Creates an Amazon Q in Connect AI Guardrail version.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiguardrailversion.html
    :cloudformationResource: AWS::Wisdom::AIGuardrailVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_aIGuardrail_version_props_mixin = wisdom_mixins.CfnAIGuardrailVersionPropsMixin(wisdom_mixins.CfnAIGuardrailVersionMixinProps(
            ai_guardrail_id="aiGuardrailId",
            assistant_id="assistantId",
            modified_time_seconds=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAIGuardrailVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AIGuardrailVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f248bf7e3973d2b331526981ddaecb4121c538cbd2fb07f367a155f435b25fc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7610cc47ffb85b2bcb7891cce617a032a5299f368aff6dcbfb721bd7fe41c5ce)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a1335ba2446f8e62a795cb087448c47cbb061dd1f2adc07e0c3095c168bbba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAIGuardrailVersionMixinProps:
        return typing.cast(CfnAIGuardrailVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIPromptMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_format": "apiFormat",
        "assistant_id": "assistantId",
        "description": "description",
        "model_id": "modelId",
        "name": "name",
        "tags": "tags",
        "template_configuration": "templateConfiguration",
        "template_type": "templateType",
        "type": "type",
    },
)
class CfnAIPromptMixinProps:
    def __init__(
        self,
        *,
        api_format: typing.Optional[builtins.str] = None,
        assistant_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        model_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        template_type: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAIPromptPropsMixin.

        :param api_format: The API format used for this AI Prompt.
        :param assistant_id: The identifier of the Amazon Q in Connect assistant. Can be either the ID or the ARN. URLs cannot contain the ARN.
        :param description: The description of the AI Prompt.
        :param model_id: The identifier of the model used for this AI Prompt. The following model Ids are supported:. - ``anthropic.claude-3-haiku--v1:0`` - ``apac.amazon.nova-lite-v1:0`` - ``apac.amazon.nova-micro-v1:0`` - ``apac.amazon.nova-pro-v1:0`` - ``apac.anthropic.claude-3-5-sonnet--v2:0`` - ``apac.anthropic.claude-3-haiku-20240307-v1:0`` - ``eu.amazon.nova-lite-v1:0`` - ``eu.amazon.nova-micro-v1:0`` - ``eu.amazon.nova-pro-v1:0`` - ``eu.anthropic.claude-3-7-sonnet-20250219-v1:0`` - ``eu.anthropic.claude-3-haiku-20240307-v1:0`` - ``us.amazon.nova-lite-v1:0`` - ``us.amazon.nova-micro-v1:0`` - ``us.amazon.nova-pro-v1:0`` - ``us.anthropic.claude-3-5-haiku-20241022-v1:0`` - ``us.anthropic.claude-3-7-sonnet-20250219-v1:0`` - ``us.anthropic.claude-3-haiku-20240307-v1:0``
        :param name: The name of the AI Prompt.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param template_configuration: The configuration of the prompt template for this AI Prompt.
        :param template_type: The type of the prompt template for this AI Prompt.
        :param type: The type of this AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_aIPrompt_mixin_props = wisdom_mixins.CfnAIPromptMixinProps(
                api_format="apiFormat",
                assistant_id="assistantId",
                description="description",
                model_id="modelId",
                name="name",
                tags={
                    "tags_key": "tags"
                },
                template_configuration=wisdom_mixins.CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty(
                    text_full_ai_prompt_edit_template_configuration=wisdom_mixins.CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty(
                        text="text"
                    )
                ),
                template_type="templateType",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c13025093ae01c51eaadc6032480b41018dae255bb2f7df83ce0511d7f96e610)
            check_type(argname="argument api_format", value=api_format, expected_type=type_hints["api_format"])
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument model_id", value=model_id, expected_type=type_hints["model_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_configuration", value=template_configuration, expected_type=type_hints["template_configuration"])
            check_type(argname="argument template_type", value=template_type, expected_type=type_hints["template_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_format is not None:
            self._values["api_format"] = api_format
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if description is not None:
            self._values["description"] = description
        if model_id is not None:
            self._values["model_id"] = model_id
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if template_configuration is not None:
            self._values["template_configuration"] = template_configuration
        if template_type is not None:
            self._values["template_type"] = template_type
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def api_format(self) -> typing.Optional[builtins.str]:
        '''The API format used for this AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-apiformat
        '''
        result = self._values.get("api_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q in Connect assistant.

        Can be either the ID or the ARN. URLs cannot contain the ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the model used for this AI Prompt. The following model Ids are supported:.

        - ``anthropic.claude-3-haiku--v1:0``
        - ``apac.amazon.nova-lite-v1:0``
        - ``apac.amazon.nova-micro-v1:0``
        - ``apac.amazon.nova-pro-v1:0``
        - ``apac.anthropic.claude-3-5-sonnet--v2:0``
        - ``apac.anthropic.claude-3-haiku-20240307-v1:0``
        - ``eu.amazon.nova-lite-v1:0``
        - ``eu.amazon.nova-micro-v1:0``
        - ``eu.amazon.nova-pro-v1:0``
        - ``eu.anthropic.claude-3-7-sonnet-20250219-v1:0``
        - ``eu.anthropic.claude-3-haiku-20240307-v1:0``
        - ``us.amazon.nova-lite-v1:0``
        - ``us.amazon.nova-micro-v1:0``
        - ``us.amazon.nova-pro-v1:0``
        - ``us.anthropic.claude-3-5-haiku-20241022-v1:0``
        - ``us.anthropic.claude-3-7-sonnet-20250219-v1:0``
        - ``us.anthropic.claude-3-haiku-20240307-v1:0``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-modelid
        '''
        result = self._values.get("model_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def template_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty"]]:
        '''The configuration of the prompt template for this AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-templateconfiguration
        '''
        result = self._values.get("template_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty"]], result)

    @builtins.property
    def template_type(self) -> typing.Optional[builtins.str]:
        '''The type of the prompt template for this AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-templatetype
        '''
        result = self._values.get("template_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of this AI Prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html#cfn-wisdom-aiprompt-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAIPromptMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAIPromptPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIPromptPropsMixin",
):
    '''Creates an Amazon Q in Connect AI Prompt.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aiprompt.html
    :cloudformationResource: AWS::Wisdom::AIPrompt
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_aIPrompt_props_mixin = wisdom_mixins.CfnAIPromptPropsMixin(wisdom_mixins.CfnAIPromptMixinProps(
            api_format="apiFormat",
            assistant_id="assistantId",
            description="description",
            model_id="modelId",
            name="name",
            tags={
                "tags_key": "tags"
            },
            template_configuration=wisdom_mixins.CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty(
                text_full_ai_prompt_edit_template_configuration=wisdom_mixins.CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty(
                    text="text"
                )
            ),
            template_type="templateType",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAIPromptMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AIPrompt``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4895b89a13c58c1f08d274defe2ceeb2fd73449fb8b9b124aa8667aadd1b8a08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59140de25182a23cf66948116bbc193ebd3469c5d69ca78c3f71b566b68e3892)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5838c0582a13143c7cacff4cce65602b54c027ac2dad12a7ae0edd24f742e1ac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAIPromptMixinProps:
        return typing.cast(CfnAIPromptMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "text_full_ai_prompt_edit_template_configuration": "textFullAiPromptEditTemplateConfiguration",
        },
    )
    class AIPromptTemplateConfigurationProperty:
        def __init__(
            self,
            *,
            text_full_ai_prompt_edit_template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A typed union that specifies the configuration for a prompt template based on its type.

            :param text_full_ai_prompt_edit_template_configuration: The configuration for a prompt template that supports full textual prompt configuration using a YAML prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiprompt-aiprompttemplateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                a_iPrompt_template_configuration_property = wisdom_mixins.CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty(
                    text_full_ai_prompt_edit_template_configuration=wisdom_mixins.CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty(
                        text="text"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74af076bc67e0f4c9544fbc580371ec775e456ff4f085993a7093ab5a3093022)
                check_type(argname="argument text_full_ai_prompt_edit_template_configuration", value=text_full_ai_prompt_edit_template_configuration, expected_type=type_hints["text_full_ai_prompt_edit_template_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if text_full_ai_prompt_edit_template_configuration is not None:
                self._values["text_full_ai_prompt_edit_template_configuration"] = text_full_ai_prompt_edit_template_configuration

        @builtins.property
        def text_full_ai_prompt_edit_template_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty"]]:
            '''The configuration for a prompt template that supports full textual prompt configuration using a YAML prompt.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiprompt-aiprompttemplateconfiguration.html#cfn-wisdom-aiprompt-aiprompttemplateconfiguration-textfullaipromptedittemplateconfiguration
            '''
            result = self._values.get("text_full_ai_prompt_edit_template_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AIPromptTemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"text": "text"},
    )
    class TextFullAIPromptEditTemplateConfigurationProperty:
        def __init__(self, *, text: typing.Optional[builtins.str] = None) -> None:
            '''The configuration for a prompt template that supports full textual prompt configuration using a YAML prompt.

            :param text: The YAML text for the AI Prompt template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiprompt-textfullaipromptedittemplateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                text_full_aIPrompt_edit_template_configuration_property = wisdom_mixins.CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty(
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e88371ccae1f83823f5ca63e969c4fa27fff33dbaa2b3b8a5f5b4396eb1d5258)
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The YAML text for the AI Prompt template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-aiprompt-textfullaipromptedittemplateconfiguration.html#cfn-wisdom-aiprompt-textfullaipromptedittemplateconfiguration-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TextFullAIPromptEditTemplateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIPromptVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ai_prompt_id": "aiPromptId",
        "assistant_id": "assistantId",
        "modified_time_seconds": "modifiedTimeSeconds",
    },
)
class CfnAIPromptVersionMixinProps:
    def __init__(
        self,
        *,
        ai_prompt_id: typing.Optional[builtins.str] = None,
        assistant_id: typing.Optional[builtins.str] = None,
        modified_time_seconds: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for CfnAIPromptVersionPropsMixin.

        :param ai_prompt_id: The identifier of the Amazon Q in Connect AI prompt.
        :param assistant_id: The identifier of the Amazon Q in Connect assistant. Can be either the ID or the ARN. URLs cannot contain the ARN.
        :param modified_time_seconds: The time the AI Prompt version was last modified in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aipromptversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_aIPrompt_version_mixin_props = wisdom_mixins.CfnAIPromptVersionMixinProps(
                ai_prompt_id="aiPromptId",
                assistant_id="assistantId",
                modified_time_seconds=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__695f52af8d0bbc6a87cbf2604f5fdb96b6eefa7c9b4345bf2083f6628281f888)
            check_type(argname="argument ai_prompt_id", value=ai_prompt_id, expected_type=type_hints["ai_prompt_id"])
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument modified_time_seconds", value=modified_time_seconds, expected_type=type_hints["modified_time_seconds"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ai_prompt_id is not None:
            self._values["ai_prompt_id"] = ai_prompt_id
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if modified_time_seconds is not None:
            self._values["modified_time_seconds"] = modified_time_seconds

    @builtins.property
    def ai_prompt_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q in Connect AI prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aipromptversion.html#cfn-wisdom-aipromptversion-aipromptid
        '''
        result = self._values.get("ai_prompt_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Q in Connect assistant.

        Can be either the ID or the ARN. URLs cannot contain the ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aipromptversion.html#cfn-wisdom-aipromptversion-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def modified_time_seconds(self) -> typing.Optional[jsii.Number]:
        '''The time the AI Prompt version was last modified in seconds.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aipromptversion.html#cfn-wisdom-aipromptversion-modifiedtimeseconds
        '''
        result = self._values.get("modified_time_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAIPromptVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAIPromptVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAIPromptVersionPropsMixin",
):
    '''Creates an Amazon Q in Connect AI Prompt version.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-aipromptversion.html
    :cloudformationResource: AWS::Wisdom::AIPromptVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_aIPrompt_version_props_mixin = wisdom_mixins.CfnAIPromptVersionPropsMixin(wisdom_mixins.CfnAIPromptVersionMixinProps(
            ai_prompt_id="aiPromptId",
            assistant_id="assistantId",
            modified_time_seconds=123
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAIPromptVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AIPromptVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6625a81343e258f3725ebabcc5137e46c29b17564c0697d16e5f095898bb4e1e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4b16a131fd4636e6f3526c3df2a2954410c107c60d4bc2def2fb8559d18524c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560153980f2a4daf95c73f03f75bc6b273d933102adb5df23a9f1ac57adbdb4a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAIPromptVersionMixinProps:
        return typing.cast(CfnAIPromptVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assistant_id": "assistantId",
        "association": "association",
        "association_type": "associationType",
        "tags": "tags",
    },
)
class CfnAssistantAssociationMixinProps:
    def __init__(
        self,
        *,
        assistant_id: typing.Optional[builtins.str] = None,
        association: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssistantAssociationPropsMixin.AssociationDataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        association_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAssistantAssociationPropsMixin.

        :param assistant_id: The identifier of the Wisdom assistant.
        :param association: The identifier of the associated resource.
        :param association_type: The type of association.
        :param tags: The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_assistant_association_mixin_props = wisdom_mixins.CfnAssistantAssociationMixinProps(
                assistant_id="assistantId",
                association=wisdom_mixins.CfnAssistantAssociationPropsMixin.AssociationDataProperty(
                    knowledge_base_id="knowledgeBaseId"
                ),
                association_type="associationType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa55980f006d13bf393a8acffe522cd23dc4d731bae129d17bee6404d0c72de8)
            check_type(argname="argument assistant_id", value=assistant_id, expected_type=type_hints["assistant_id"])
            check_type(argname="argument association", value=association, expected_type=type_hints["association"])
            check_type(argname="argument association_type", value=association_type, expected_type=type_hints["association_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assistant_id is not None:
            self._values["assistant_id"] = assistant_id
        if association is not None:
            self._values["association"] = association
        if association_type is not None:
            self._values["association_type"] = association_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assistant_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Wisdom assistant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-assistantid
        '''
        result = self._values.get("assistant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def association(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssistantAssociationPropsMixin.AssociationDataProperty"]]:
        '''The identifier of the associated resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-association
        '''
        result = self._values.get("association")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssistantAssociationPropsMixin.AssociationDataProperty"]], result)

    @builtins.property
    def association_type(self) -> typing.Optional[builtins.str]:
        '''The type of association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-associationtype
        '''
        result = self._values.get("association_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssistantAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssistantAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantAssociationPropsMixin",
):
    '''Specifies an association between an Amazon Connect Wisdom assistant and another resource.

    Currently, the only supported association is with a knowledge base. An assistant can have only a single association.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html
    :cloudformationResource: AWS::Wisdom::AssistantAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_assistant_association_props_mixin = wisdom_mixins.CfnAssistantAssociationPropsMixin(wisdom_mixins.CfnAssistantAssociationMixinProps(
            assistant_id="assistantId",
            association=wisdom_mixins.CfnAssistantAssociationPropsMixin.AssociationDataProperty(
                knowledge_base_id="knowledgeBaseId"
            ),
            association_type="associationType",
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
        props: typing.Union[CfnAssistantAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::AssistantAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7ac832a83cd6d5854f7f1e9cd388ffa98061c8bd33537f27ee3d08025fcd8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__27b269f107dccc64302163bbb5520aabccdd89fbf4677d377300b6e5c1226e8a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1fb247a57610b3873b7f7da67e55476e57e3bf81c42434d41806cf6bcbc7de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssistantAssociationMixinProps:
        return typing.cast(CfnAssistantAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantAssociationPropsMixin.AssociationDataProperty",
        jsii_struct_bases=[],
        name_mapping={"knowledge_base_id": "knowledgeBaseId"},
    )
    class AssociationDataProperty:
        def __init__(
            self,
            *,
            knowledge_base_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A union type that currently has a single argument, which is the knowledge base ID.

            :param knowledge_base_id: The identifier of the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistantassociation-associationdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                association_data_property = wisdom_mixins.CfnAssistantAssociationPropsMixin.AssociationDataProperty(
                    knowledge_base_id="knowledgeBaseId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3a3a3b65037c6ca0957b6bdb456a8c495921f516ce689c810b6ec0ffcab777c)
                check_type(argname="argument knowledge_base_id", value=knowledge_base_id, expected_type=type_hints["knowledge_base_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if knowledge_base_id is not None:
                self._values["knowledge_base_id"] = knowledge_base_id

        @builtins.property
        def knowledge_base_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the knowledge base.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistantassociation-associationdata.html#cfn-wisdom-assistantassociation-associationdata-knowledgebaseid
            '''
            result = self._values.get("knowledge_base_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociationDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnAssistantEventLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantEventLogs",
):
    '''Builder for CfnAssistantLogsMixin to generate EVENT_LOGS for CfnAssistant.

    :cloudformationResource: AWS::Wisdom::Assistant
    :logType: EVENT_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_assistant_event_logs = wisdom_mixins.CfnAssistantEventLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> "CfnAssistantLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be1ec0cdb72cb1c75dd57fb48a570af82b8a72a1550eda9d8873197f890ad0d)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnAssistantLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnAssistantLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edce08554f08839ee68a5f2d43c3e32707efd6317fb88d0d35b7752eb2003445)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnAssistantLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnAssistantLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a28785ffe00f875cd2df2705cf80706365f5ebd09b9b4e6dff83a576301ae7)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnAssistantLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnAssistantLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantLogsMixin",
):
    '''Specifies an Amazon Connect Wisdom assistant.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
    :cloudformationResource: AWS::Wisdom::Assistant
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_assistant_logs_mixin = wisdom_mixins.CfnAssistantLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Wisdom::Assistant``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0449472693d2fbe600e1725f76b4c3af145009e8dd010b158349d45c42fd265f)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd6722602a152a3fc5db4dc9fada43780ef6612cb7661007d0ae6e427d69934)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6498dd1e57078422137442bb580110f368407a455ff4d9ed5e6b8e3f5e476113)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EVENT_LOGS")
    def EVENT_LOGS(cls) -> CfnAssistantEventLogs:
        return typing.cast(CfnAssistantEventLogs, jsii.sget(cls, "EVENT_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
        "type": "type",
    },
)
class CfnAssistantMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAssistantPropsMixin.

        :param description: The description of the assistant.
        :param name: The name of the assistant.
        :param server_side_encryption_configuration: The configuration information for the customer managed key used for encryption. The customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom. To use Wisdom with chat, the key policy must also allow ``kms:Decrypt`` , ``kms:GenerateDataKey*`` , and ``kms:DescribeKey`` permissions to the ``connect.amazonaws.com`` service principal. For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ .
        :param tags: The tags used to organize, track, or control access for this resource.
        :param type: The type of assistant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_assistant_mixin_props = wisdom_mixins.CfnAssistantMixinProps(
                description="description",
                name="name",
                server_side_encryption_configuration=wisdom_mixins.CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d030372bc6874e27a3de1a443c868e39a336c235578537759fece591f20feef)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the assistant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the assistant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty"]]:
        '''The configuration information for the customer managed key used for encryption.

        The customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom. To use Wisdom with chat, the key policy must also allow ``kms:Decrypt`` , ``kms:GenerateDataKey*`` , and ``kms:DescribeKey`` permissions to the ``connect.amazonaws.com`` service principal. For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of assistant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssistantMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssistantPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantPropsMixin",
):
    '''Specifies an Amazon Connect Wisdom assistant.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
    :cloudformationResource: AWS::Wisdom::Assistant
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_assistant_props_mixin = wisdom_mixins.CfnAssistantPropsMixin(wisdom_mixins.CfnAssistantMixinProps(
            description="description",
            name="name",
            server_side_encryption_configuration=wisdom_mixins.CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAssistantMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::Assistant``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9bfcded539e1ea116eaa36e3f36e946aa1a73bfb13930d05ced7e84577827f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5453798ee90507207b057c393a4cccb14bc8393da5fda4255038527ac7bc9c7a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db984015f82ad62a20a72e3537d98d15b5a9f7f02e002177d291857b57e3e726)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssistantMixinProps:
        return typing.cast(CfnAssistantMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''The configuration information for the customer managed key used for encryption.

            :param kms_key_id: The customer managed key used for encryption. The customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom. To use Wisdom with chat, the key policy must also allow ``kms:Decrypt`` , ``kms:GenerateDataKey*`` , and ``kms:DescribeKey`` permissions to the ``connect.amazonaws.com`` service principal. For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistant-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                server_side_encryption_configuration_property = wisdom_mixins.CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afee51dc1a5efef9ad6f836c1f3b6a9cdbda4341934d497e3232793d13e21baa)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The customer managed key used for encryption.

            The customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom. To use Wisdom with chat, the key policy must also allow ``kms:Decrypt`` , ``kms:GenerateDataKey*`` , and ``kms:DescribeKey`` permissions to the ``connect.amazonaws.com`` service principal. For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistant-serversideencryptionconfiguration.html#cfn-wisdom-assistant-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBaseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "knowledge_base_type": "knowledgeBaseType",
        "name": "name",
        "rendering_configuration": "renderingConfiguration",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "source_configuration": "sourceConfiguration",
        "tags": "tags",
        "vector_ingestion_configuration": "vectorIngestionConfiguration",
    },
)
class CfnKnowledgeBaseMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        knowledge_base_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rendering_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vector_ingestion_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnKnowledgeBasePropsMixin.

        :param description: The description.
        :param knowledge_base_type: The type of knowledge base. Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.
        :param name: The name of the knowledge base.
        :param rendering_configuration: Information about how to render the content.
        :param server_side_encryption_configuration: This customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom. For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .
        :param source_configuration: The source of the knowledge base content. Only set this argument for EXTERNAL or Managed knowledge bases.
        :param tags: The tags used to organize, track, or control access for this resource.
        :param vector_ingestion_configuration: Contains details about how to ingest the documents in a data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_knowledge_base_mixin_props = wisdom_mixins.CfnKnowledgeBaseMixinProps(
                description="description",
                knowledge_base_type="knowledgeBaseType",
                name="name",
                rendering_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty(
                    template_uri="templateUri"
                ),
                server_side_encryption_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                ),
                source_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.SourceConfigurationProperty(
                    app_integrations=wisdom_mixins.CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty(
                        app_integration_arn="appIntegrationArn",
                        object_fields=["objectFields"]
                    ),
                    managed_source_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty(
                        web_crawler_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty(
                            crawler_limits=wisdom_mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty(
                                rate_limit=123
                            ),
                            exclusion_filters=["exclusionFilters"],
                            inclusion_filters=["inclusionFilters"],
                            scope="scope",
                            url_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty(
                                seed_urls=[wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                                    url="url"
                                )]
                            )
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vector_ingestion_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty(
                    chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty(
                        chunking_strategy="chunkingStrategy",
                        fixed_size_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty(
                            max_tokens=123,
                            overlap_percentage=123
                        ),
                        hierarchical_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty(
                            level_configurations=[wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty(
                                max_tokens=123
                            )],
                            overlap_tokens=123
                        ),
                        semantic_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty(
                            breakpoint_percentile_threshold=123,
                            buffer_size=123,
                            max_tokens=123
                        )
                    ),
                    parsing_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty(
                        bedrock_foundation_model_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty(
                            model_arn="modelArn",
                            parsing_prompt=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty(
                                parsing_prompt_text="parsingPromptText"
                            )
                        ),
                        parsing_strategy="parsingStrategy"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de922f4b9249ae8835b37c47e237d5247070849e80461bb75c13311d6e472b59)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument knowledge_base_type", value=knowledge_base_type, expected_type=type_hints["knowledge_base_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rendering_configuration", value=rendering_configuration, expected_type=type_hints["rendering_configuration"])
            check_type(argname="argument server_side_encryption_configuration", value=server_side_encryption_configuration, expected_type=type_hints["server_side_encryption_configuration"])
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vector_ingestion_configuration", value=vector_ingestion_configuration, expected_type=type_hints["vector_ingestion_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if knowledge_base_type is not None:
            self._values["knowledge_base_type"] = knowledge_base_type
        if name is not None:
            self._values["name"] = name
        if rendering_configuration is not None:
            self._values["rendering_configuration"] = rendering_configuration
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration
        if tags is not None:
            self._values["tags"] = tags
        if vector_ingestion_configuration is not None:
            self._values["vector_ingestion_configuration"] = vector_ingestion_configuration

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def knowledge_base_type(self) -> typing.Optional[builtins.str]:
        '''The type of knowledge base.

        Only CUSTOM knowledge bases allow you to upload your own content. EXTERNAL knowledge bases support integrations with third-party systems whose content is synchronized automatically.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-knowledgebasetype
        '''
        result = self._values.get("knowledge_base_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rendering_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty"]]:
        '''Information about how to render the content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-renderingconfiguration
        '''
        result = self._values.get("rendering_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty"]], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty"]]:
        '''This customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom.

        For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty"]], result)

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.SourceConfigurationProperty"]]:
        '''The source of the knowledge base content.

        Only set this argument for EXTERNAL or Managed knowledge bases.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.SourceConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vector_ingestion_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty"]]:
        '''Contains details about how to ingest the documents in a data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-vectoringestionconfiguration
        '''
        result = self._values.get("vector_ingestion_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKnowledgeBaseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnKnowledgeBasePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin",
):
    '''Specifies a knowledge base.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html
    :cloudformationResource: AWS::Wisdom::KnowledgeBase
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_knowledge_base_props_mixin = wisdom_mixins.CfnKnowledgeBasePropsMixin(wisdom_mixins.CfnKnowledgeBaseMixinProps(
            description="description",
            knowledge_base_type="knowledgeBaseType",
            name="name",
            rendering_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty(
                template_uri="templateUri"
            ),
            server_side_encryption_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty(
                kms_key_id="kmsKeyId"
            ),
            source_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.SourceConfigurationProperty(
                app_integrations=wisdom_mixins.CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty(
                    app_integration_arn="appIntegrationArn",
                    object_fields=["objectFields"]
                ),
                managed_source_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty(
                    web_crawler_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty(
                        crawler_limits=wisdom_mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty(
                            rate_limit=123
                        ),
                        exclusion_filters=["exclusionFilters"],
                        inclusion_filters=["inclusionFilters"],
                        scope="scope",
                        url_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty(
                            seed_urls=[wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                                url="url"
                            )]
                        )
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vector_ingestion_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty(
                chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty(
                    chunking_strategy="chunkingStrategy",
                    fixed_size_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty(
                        max_tokens=123,
                        overlap_percentage=123
                    ),
                    hierarchical_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty(
                        level_configurations=[wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty(
                            max_tokens=123
                        )],
                        overlap_tokens=123
                    ),
                    semantic_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty(
                        breakpoint_percentile_threshold=123,
                        buffer_size=123,
                        max_tokens=123
                    )
                ),
                parsing_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty(
                    bedrock_foundation_model_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty(
                        model_arn="modelArn",
                        parsing_prompt=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty(
                            parsing_prompt_text="parsingPromptText"
                        )
                    ),
                    parsing_strategy="parsingStrategy"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnKnowledgeBaseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::KnowledgeBase``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619ec8f23c86516960ab44ab2201ceef808a6a3a6758c18ae4f0f48674f758b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__151163af4b0ed0d10b679c10b0f8766b1b3255d7097d8cd83457ad013830bfe7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e129aa530eb0d4a3a5285f3c1c9006603fe2270efbc1c7fa66d1b7c595031b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnKnowledgeBaseMixinProps:
        return typing.cast(CfnKnowledgeBaseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_integration_arn": "appIntegrationArn",
            "object_fields": "objectFields",
        },
    )
    class AppIntegrationsConfigurationProperty:
        def __init__(
            self,
            *,
            app_integration_arn: typing.Optional[builtins.str] = None,
            object_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration information for Amazon AppIntegrations to automatically ingest content.

            :param app_integration_arn: The Amazon Resource Name (ARN) of the AppIntegrations DataIntegration to use for ingesting content. - For `Salesforce <https://docs.aws.amazon.com/https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledge__kav.htm>`_ , your AppIntegrations DataIntegration must have an ObjectConfiguration if objectFields is not provided, including at least ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , and ``IsDeleted`` as source fields. - For `ServiceNow <https://docs.aws.amazon.com/https://developer.servicenow.com/dev.do#!/reference/api/rome/rest/knowledge-management-api>`_ , your AppIntegrations DataIntegration must have an ObjectConfiguration if objectFields is not provided, including at least ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , and ``active`` as source fields. - For `Zendesk <https://docs.aws.amazon.com/https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/>`_ , your AppIntegrations DataIntegration must have an ObjectConfiguration if ``objectFields`` is not provided, including at least ``id`` , ``title`` , ``updated_at`` , and ``draft`` as source fields. - For `SharePoint <https://docs.aws.amazon.com/https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/sharepoint-net-server-csom-jsom-and-rest-api-index>`_ , your AppIntegrations DataIntegration must have a FileConfiguration, including only file extensions that are among ``docx`` , ``pdf`` , ``html`` , ``htm`` , and ``txt`` . - For `Amazon S3 <https://docs.aws.amazon.com/s3/>`_ , the ObjectConfiguration and FileConfiguration of your AppIntegrations DataIntegration must be null. The ``SourceURI`` of your DataIntegration must use the following format: ``s3://your_s3_bucket_name`` . .. epigraph:: The bucket policy of the corresponding S3 bucket must allow the AWS principal ``app-integrations.amazonaws.com`` to perform ``s3:ListBucket`` , ``s3:GetObject`` , and ``s3:GetBucketLocation`` against the bucket.
            :param object_fields: The fields from the source that are made available to your agents in Amazon Q in Connect. Optional if ObjectConfiguration is included in the provided DataIntegration. - For `Salesforce <https://docs.aws.amazon.com/https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledge__kav.htm>`_ , you must include at least ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , and ``IsDeleted`` . - For `ServiceNow <https://docs.aws.amazon.com/https://developer.servicenow.com/dev.do#!/reference/api/rome/rest/knowledge-management-api>`_ , you must include at least ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , and ``active`` . - For `Zendesk <https://docs.aws.amazon.com/https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/>`_ , you must include at least ``id`` , ``title`` , ``updated_at`` , and ``draft`` . Make sure to include additional fields. These fields are indexed and used to source recommendations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                app_integrations_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty(
                    app_integration_arn="appIntegrationArn",
                    object_fields=["objectFields"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a0e0caeefd5d44386afccb22e80e424d6b71cf4ced5cbfcc32d49ce886920d9d)
                check_type(argname="argument app_integration_arn", value=app_integration_arn, expected_type=type_hints["app_integration_arn"])
                check_type(argname="argument object_fields", value=object_fields, expected_type=type_hints["object_fields"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_integration_arn is not None:
                self._values["app_integration_arn"] = app_integration_arn
            if object_fields is not None:
                self._values["object_fields"] = object_fields

        @builtins.property
        def app_integration_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AppIntegrations DataIntegration to use for ingesting content.

            - For `Salesforce <https://docs.aws.amazon.com/https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledge__kav.htm>`_ , your AppIntegrations DataIntegration must have an ObjectConfiguration if objectFields is not provided, including at least ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , and ``IsDeleted`` as source fields.
            - For `ServiceNow <https://docs.aws.amazon.com/https://developer.servicenow.com/dev.do#!/reference/api/rome/rest/knowledge-management-api>`_ , your AppIntegrations DataIntegration must have an ObjectConfiguration if objectFields is not provided, including at least ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , and ``active`` as source fields.
            - For `Zendesk <https://docs.aws.amazon.com/https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/>`_ , your AppIntegrations DataIntegration must have an ObjectConfiguration if ``objectFields`` is not provided, including at least ``id`` , ``title`` , ``updated_at`` , and ``draft`` as source fields.
            - For `SharePoint <https://docs.aws.amazon.com/https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/sharepoint-net-server-csom-jsom-and-rest-api-index>`_ , your AppIntegrations DataIntegration must have a FileConfiguration, including only file extensions that are among ``docx`` , ``pdf`` , ``html`` , ``htm`` , and ``txt`` .
            - For `Amazon S3 <https://docs.aws.amazon.com/s3/>`_ , the ObjectConfiguration and FileConfiguration of your AppIntegrations DataIntegration must be null. The ``SourceURI`` of your DataIntegration must use the following format: ``s3://your_s3_bucket_name`` .

            .. epigraph::

               The bucket policy of the corresponding S3 bucket must allow the AWS principal ``app-integrations.amazonaws.com`` to perform ``s3:ListBucket`` , ``s3:GetObject`` , and ``s3:GetBucketLocation`` against the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html#cfn-wisdom-knowledgebase-appintegrationsconfiguration-appintegrationarn
            '''
            result = self._values.get("app_integration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_fields(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The fields from the source that are made available to your agents in Amazon Q in Connect.

            Optional if ObjectConfiguration is included in the provided DataIntegration.

            - For `Salesforce <https://docs.aws.amazon.com/https://developer.salesforce.com/docs/atlas.en-us.knowledge_dev.meta/knowledge_dev/sforce_api_objects_knowledge__kav.htm>`_ , you must include at least ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , and ``IsDeleted`` .
            - For `ServiceNow <https://docs.aws.amazon.com/https://developer.servicenow.com/dev.do#!/reference/api/rome/rest/knowledge-management-api>`_ , you must include at least ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , and ``active`` .
            - For `Zendesk <https://docs.aws.amazon.com/https://developer.zendesk.com/api-reference/help_center/help-center-api/articles/>`_ , you must include at least ``id`` , ``title`` , ``updated_at`` , and ``draft`` .

            Make sure to include additional fields. These fields are indexed and used to source recommendations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html#cfn-wisdom-knowledgebase-appintegrationsconfiguration-objectfields
            '''
            result = self._values.get("object_fields")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppIntegrationsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"model_arn": "modelArn", "parsing_prompt": "parsingPrompt"},
    )
    class BedrockFoundationModelConfigurationProperty:
        def __init__(
            self,
            *,
            model_arn: typing.Optional[builtins.str] = None,
            parsing_prompt: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.ParsingPromptProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the Bedrock foundation model.

            :param model_arn: The model ARN of the Bedrock foundation model.
            :param parsing_prompt: The parsing prompt of the Bedrock foundation model configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-bedrockfoundationmodelconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                bedrock_foundation_model_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty(
                    model_arn="modelArn",
                    parsing_prompt=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty(
                        parsing_prompt_text="parsingPromptText"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4e488d5587e9215556f7d5d9562e3b54e563d560bff8bd15a8b632b3ad10d3e2)
                check_type(argname="argument model_arn", value=model_arn, expected_type=type_hints["model_arn"])
                check_type(argname="argument parsing_prompt", value=parsing_prompt, expected_type=type_hints["parsing_prompt"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if model_arn is not None:
                self._values["model_arn"] = model_arn
            if parsing_prompt is not None:
                self._values["parsing_prompt"] = parsing_prompt

        @builtins.property
        def model_arn(self) -> typing.Optional[builtins.str]:
            '''The model ARN of the Bedrock foundation model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-bedrockfoundationmodelconfiguration.html#cfn-wisdom-knowledgebase-bedrockfoundationmodelconfiguration-modelarn
            '''
            result = self._values.get("model_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parsing_prompt(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ParsingPromptProperty"]]:
            '''The parsing prompt of the Bedrock foundation model configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-bedrockfoundationmodelconfiguration.html#cfn-wisdom-knowledgebase-bedrockfoundationmodelconfiguration-parsingprompt
            '''
            result = self._values.get("parsing_prompt")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ParsingPromptProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BedrockFoundationModelConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "chunking_strategy": "chunkingStrategy",
            "fixed_size_chunking_configuration": "fixedSizeChunkingConfiguration",
            "hierarchical_chunking_configuration": "hierarchicalChunkingConfiguration",
            "semantic_chunking_configuration": "semanticChunkingConfiguration",
        },
    )
    class ChunkingConfigurationProperty:
        def __init__(
            self,
            *,
            chunking_strategy: typing.Optional[builtins.str] = None,
            fixed_size_chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            hierarchical_chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            semantic_chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details about how to chunk the documents in the data source.

            A chunk refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried.

            :param chunking_strategy: Knowledge base can split your source data into chunks. A chunk refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried. You have the following options for chunking your data. If you opt for ``NONE`` , then you may want to pre-process your files by splitting them up such that each file corresponds to a chunk.
            :param fixed_size_chunking_configuration: Configurations for when you choose fixed-size chunking. If you set the ``chunkingStrategy`` as ``NONE`` , exclude this field.
            :param hierarchical_chunking_configuration: Settings for hierarchical document chunking for a data source. Hierarchical chunking splits documents into layers of chunks where the first layer contains large chunks, and the second layer contains smaller chunks derived from the first layer.
            :param semantic_chunking_configuration: Settings for semantic document chunking for a data source. Semantic chunking splits a document into smaller documents based on groups of similar content derived from the text with natural language processing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-chunkingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                chunking_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty(
                    chunking_strategy="chunkingStrategy",
                    fixed_size_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty(
                        max_tokens=123,
                        overlap_percentage=123
                    ),
                    hierarchical_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty(
                        level_configurations=[wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty(
                            max_tokens=123
                        )],
                        overlap_tokens=123
                    ),
                    semantic_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty(
                        breakpoint_percentile_threshold=123,
                        buffer_size=123,
                        max_tokens=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__179292bc2f780cbf1aef6ed2c84970e7b5b36ef2589b2526c36c32c3dde2bdf6)
                check_type(argname="argument chunking_strategy", value=chunking_strategy, expected_type=type_hints["chunking_strategy"])
                check_type(argname="argument fixed_size_chunking_configuration", value=fixed_size_chunking_configuration, expected_type=type_hints["fixed_size_chunking_configuration"])
                check_type(argname="argument hierarchical_chunking_configuration", value=hierarchical_chunking_configuration, expected_type=type_hints["hierarchical_chunking_configuration"])
                check_type(argname="argument semantic_chunking_configuration", value=semantic_chunking_configuration, expected_type=type_hints["semantic_chunking_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if chunking_strategy is not None:
                self._values["chunking_strategy"] = chunking_strategy
            if fixed_size_chunking_configuration is not None:
                self._values["fixed_size_chunking_configuration"] = fixed_size_chunking_configuration
            if hierarchical_chunking_configuration is not None:
                self._values["hierarchical_chunking_configuration"] = hierarchical_chunking_configuration
            if semantic_chunking_configuration is not None:
                self._values["semantic_chunking_configuration"] = semantic_chunking_configuration

        @builtins.property
        def chunking_strategy(self) -> typing.Optional[builtins.str]:
            '''Knowledge base can split your source data into chunks.

            A chunk refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried. You have the following options for chunking your data. If you opt for ``NONE`` , then you may want to pre-process your files by splitting them up such that each file corresponds to a chunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-chunkingconfiguration.html#cfn-wisdom-knowledgebase-chunkingconfiguration-chunkingstrategy
            '''
            result = self._values.get("chunking_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fixed_size_chunking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty"]]:
            '''Configurations for when you choose fixed-size chunking.

            If you set the ``chunkingStrategy`` as ``NONE`` , exclude this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-chunkingconfiguration.html#cfn-wisdom-knowledgebase-chunkingconfiguration-fixedsizechunkingconfiguration
            '''
            result = self._values.get("fixed_size_chunking_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty"]], result)

        @builtins.property
        def hierarchical_chunking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty"]]:
            '''Settings for hierarchical document chunking for a data source.

            Hierarchical chunking splits documents into layers of chunks where the first layer contains large chunks, and the second layer contains smaller chunks derived from the first layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-chunkingconfiguration.html#cfn-wisdom-knowledgebase-chunkingconfiguration-hierarchicalchunkingconfiguration
            '''
            result = self._values.get("hierarchical_chunking_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty"]], result)

        @builtins.property
        def semantic_chunking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty"]]:
            '''Settings for semantic document chunking for a data source.

            Semantic chunking splits a document into smaller documents based on groups of similar content derived from the text with natural language processing.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-chunkingconfiguration.html#cfn-wisdom-knowledgebase-chunkingconfiguration-semanticchunkingconfiguration
            '''
            result = self._values.get("semantic_chunking_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChunkingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={"rate_limit": "rateLimit"},
    )
    class CrawlerLimitsProperty:
        def __init__(self, *, rate_limit: typing.Optional[jsii.Number] = None) -> None:
            '''The limits of the crawler.

            :param rate_limit: The limit rate at which the crawler is configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-crawlerlimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                crawler_limits_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty(
                    rate_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3eacd125b12d2428b3d9c6d96aa3a05d54a181b79e3a9c08947c68225ba98b63)
                check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rate_limit is not None:
                self._values["rate_limit"] = rate_limit

        @builtins.property
        def rate_limit(self) -> typing.Optional[jsii.Number]:
            '''The limit rate at which the crawler is configured.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-crawlerlimits.html#cfn-wisdom-knowledgebase-crawlerlimits-ratelimit
            '''
            result = self._values.get("rate_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrawlerLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_tokens": "maxTokens",
            "overlap_percentage": "overlapPercentage",
        },
    )
    class FixedSizeChunkingConfigurationProperty:
        def __init__(
            self,
            *,
            max_tokens: typing.Optional[jsii.Number] = None,
            overlap_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configurations for when you choose fixed-size chunking.

            If you set the ``chunkingStrategy`` as ``NONE`` , exclude this field.

            :param max_tokens: The maximum number of tokens to include in a chunk.
            :param overlap_percentage: The percentage of overlap between adjacent chunks of a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-fixedsizechunkingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                fixed_size_chunking_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty(
                    max_tokens=123,
                    overlap_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__34a317c1896ed5b4542bc70ecef7cce89e7f61e963a89c916f7b26d16a1bb4bd)
                check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
                check_type(argname="argument overlap_percentage", value=overlap_percentage, expected_type=type_hints["overlap_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_tokens is not None:
                self._values["max_tokens"] = max_tokens
            if overlap_percentage is not None:
                self._values["overlap_percentage"] = overlap_percentage

        @builtins.property
        def max_tokens(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of tokens to include in a chunk.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-fixedsizechunkingconfiguration.html#cfn-wisdom-knowledgebase-fixedsizechunkingconfiguration-maxtokens
            '''
            result = self._values.get("max_tokens")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def overlap_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of overlap between adjacent chunks of a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-fixedsizechunkingconfiguration.html#cfn-wisdom-knowledgebase-fixedsizechunkingconfiguration-overlappercentage
            '''
            result = self._values.get("overlap_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedSizeChunkingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "level_configurations": "levelConfigurations",
            "overlap_tokens": "overlapTokens",
        },
    )
    class HierarchicalChunkingConfigurationProperty:
        def __init__(
            self,
            *,
            level_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            overlap_tokens: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Settings for hierarchical document chunking for a data source.

            Hierarchical chunking splits documents into layers of chunks where the first layer contains large chunks, and the second layer contains smaller chunks derived from the first layer.

            :param level_configurations: Token settings for each layer.
            :param overlap_tokens: The number of tokens to repeat across chunks in the same layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-hierarchicalchunkingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                hierarchical_chunking_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty(
                    level_configurations=[wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty(
                        max_tokens=123
                    )],
                    overlap_tokens=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae8dfc4c4ba20e0ddb053e60a31acb5bae6b665a26b9e2864edf8952f1ee0fda)
                check_type(argname="argument level_configurations", value=level_configurations, expected_type=type_hints["level_configurations"])
                check_type(argname="argument overlap_tokens", value=overlap_tokens, expected_type=type_hints["overlap_tokens"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if level_configurations is not None:
                self._values["level_configurations"] = level_configurations
            if overlap_tokens is not None:
                self._values["overlap_tokens"] = overlap_tokens

        @builtins.property
        def level_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty"]]]]:
            '''Token settings for each layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-hierarchicalchunkingconfiguration.html#cfn-wisdom-knowledgebase-hierarchicalchunkingconfiguration-levelconfigurations
            '''
            result = self._values.get("level_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty"]]]], result)

        @builtins.property
        def overlap_tokens(self) -> typing.Optional[jsii.Number]:
            '''The number of tokens to repeat across chunks in the same layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-hierarchicalchunkingconfiguration.html#cfn-wisdom-knowledgebase-hierarchicalchunkingconfiguration-overlaptokens
            '''
            result = self._values.get("overlap_tokens")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HierarchicalChunkingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_tokens": "maxTokens"},
    )
    class HierarchicalChunkingLevelConfigurationProperty:
        def __init__(self, *, max_tokens: typing.Optional[jsii.Number] = None) -> None:
            '''Token settings for each layer.

            :param max_tokens: The maximum number of tokens that a chunk can contain in this layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-hierarchicalchunkinglevelconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                hierarchical_chunking_level_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty(
                    max_tokens=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__76782e28d9c187515b28993698ed69ec43f20e313e2d5ffa0a21220778cd80bc)
                check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_tokens is not None:
                self._values["max_tokens"] = max_tokens

        @builtins.property
        def max_tokens(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of tokens that a chunk can contain in this layer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-hierarchicalchunkinglevelconfiguration.html#cfn-wisdom-knowledgebase-hierarchicalchunkinglevelconfiguration-maxtokens
            '''
            result = self._values.get("max_tokens")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HierarchicalChunkingLevelConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"web_crawler_configuration": "webCrawlerConfiguration"},
    )
    class ManagedSourceConfigurationProperty:
        def __init__(
            self,
            *,
            web_crawler_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Source configuration for managed resources.

            :param web_crawler_configuration: Configuration data for web crawler data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-managedsourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                managed_source_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty(
                    web_crawler_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty(
                        crawler_limits=wisdom_mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty(
                            rate_limit=123
                        ),
                        exclusion_filters=["exclusionFilters"],
                        inclusion_filters=["inclusionFilters"],
                        scope="scope",
                        url_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty(
                            seed_urls=[wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                                url="url"
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d409af7754eb47e2a3c0d015e9e8f9cbdb9820ece41294f0ae60d158912a8ff)
                check_type(argname="argument web_crawler_configuration", value=web_crawler_configuration, expected_type=type_hints["web_crawler_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if web_crawler_configuration is not None:
                self._values["web_crawler_configuration"] = web_crawler_configuration

        @builtins.property
        def web_crawler_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty"]]:
            '''Configuration data for web crawler data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-managedsourceconfiguration.html#cfn-wisdom-knowledgebase-managedsourceconfiguration-webcrawlerconfiguration
            '''
            result = self._values.get("web_crawler_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ManagedSourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bedrock_foundation_model_configuration": "bedrockFoundationModelConfiguration",
            "parsing_strategy": "parsingStrategy",
        },
    )
    class ParsingConfigurationProperty:
        def __init__(
            self,
            *,
            bedrock_foundation_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parsing_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for parsing document contents.

            By default, the service converts the contents of each document into text before splitting it into chunks. To improve processing of PDF files with tables and images, you can configure the data source to convert the pages of text into images and use a model to describe the contents of each page.

            :param bedrock_foundation_model_configuration: Settings for a foundation model used to parse documents for a data source.
            :param parsing_strategy: The parsing strategy for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-parsingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                parsing_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty(
                    bedrock_foundation_model_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty(
                        model_arn="modelArn",
                        parsing_prompt=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty(
                            parsing_prompt_text="parsingPromptText"
                        )
                    ),
                    parsing_strategy="parsingStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70cb11f4bfe6dcc2c017891a334a1a2348d5f6377abb14f2f91a4947a6721a12)
                check_type(argname="argument bedrock_foundation_model_configuration", value=bedrock_foundation_model_configuration, expected_type=type_hints["bedrock_foundation_model_configuration"])
                check_type(argname="argument parsing_strategy", value=parsing_strategy, expected_type=type_hints["parsing_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bedrock_foundation_model_configuration is not None:
                self._values["bedrock_foundation_model_configuration"] = bedrock_foundation_model_configuration
            if parsing_strategy is not None:
                self._values["parsing_strategy"] = parsing_strategy

        @builtins.property
        def bedrock_foundation_model_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty"]]:
            '''Settings for a foundation model used to parse documents for a data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-parsingconfiguration.html#cfn-wisdom-knowledgebase-parsingconfiguration-bedrockfoundationmodelconfiguration
            '''
            result = self._values.get("bedrock_foundation_model_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty"]], result)

        @builtins.property
        def parsing_strategy(self) -> typing.Optional[builtins.str]:
            '''The parsing strategy for the data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-parsingconfiguration.html#cfn-wisdom-knowledgebase-parsingconfiguration-parsingstrategy
            '''
            result = self._values.get("parsing_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParsingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty",
        jsii_struct_bases=[],
        name_mapping={"parsing_prompt_text": "parsingPromptText"},
    )
    class ParsingPromptProperty:
        def __init__(
            self,
            *,
            parsing_prompt_text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Instructions for interpreting the contents of a document.

            :param parsing_prompt_text: Instructions for interpreting the contents of a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-parsingprompt.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                parsing_prompt_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty(
                    parsing_prompt_text="parsingPromptText"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acab42a3a6651a64995b633044b635e016f92123852fe8a8fa1cd406d9de8e17)
                check_type(argname="argument parsing_prompt_text", value=parsing_prompt_text, expected_type=type_hints["parsing_prompt_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parsing_prompt_text is not None:
                self._values["parsing_prompt_text"] = parsing_prompt_text

        @builtins.property
        def parsing_prompt_text(self) -> typing.Optional[builtins.str]:
            '''Instructions for interpreting the contents of a document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-parsingprompt.html#cfn-wisdom-knowledgebase-parsingprompt-parsingprompttext
            '''
            result = self._values.get("parsing_prompt_text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ParsingPromptProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"template_uri": "templateUri"},
    )
    class RenderingConfigurationProperty:
        def __init__(
            self,
            *,
            template_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about how to render the content.

            :param template_uri: A URI template containing exactly one variable in ``${variableName}`` format. This can only be set for ``EXTERNAL`` knowledge bases. For Salesforce, ServiceNow, and Zendesk, the variable must be one of the following: - Salesforce: ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , or ``IsDeleted`` - ServiceNow: ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , or ``active`` - Zendesk: ``id`` , ``title`` , ``updated_at`` , or ``draft`` The variable is replaced with the actual value for a piece of content when calling `GetContent <https://docs.aws.amazon.com/amazon-q-connect/latest/APIReference/API_GetContent.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-renderingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                rendering_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty(
                    template_uri="templateUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b305b837d4bd6dd7ca216138425ea64208842f56272971afe594a40e3eb4bf1)
                check_type(argname="argument template_uri", value=template_uri, expected_type=type_hints["template_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if template_uri is not None:
                self._values["template_uri"] = template_uri

        @builtins.property
        def template_uri(self) -> typing.Optional[builtins.str]:
            '''A URI template containing exactly one variable in ``${variableName}`` format.

            This can only be set for ``EXTERNAL`` knowledge bases. For Salesforce, ServiceNow, and Zendesk, the variable must be one of the following:

            - Salesforce: ``Id`` , ``ArticleNumber`` , ``VersionNumber`` , ``Title`` , ``PublishStatus`` , or ``IsDeleted``
            - ServiceNow: ``number`` , ``short_description`` , ``sys_mod_count`` , ``workflow_state`` , or ``active``
            - Zendesk: ``id`` , ``title`` , ``updated_at`` , or ``draft``

            The variable is replaced with the actual value for a piece of content when calling `GetContent <https://docs.aws.amazon.com/amazon-q-connect/latest/APIReference/API_GetContent.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-renderingconfiguration.html#cfn-wisdom-knowledgebase-renderingconfiguration-templateuri
            '''
            result = self._values.get("template_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenderingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty",
        jsii_struct_bases=[],
        name_mapping={"url": "url"},
    )
    class SeedUrlProperty:
        def __init__(self, *, url: typing.Optional[builtins.str] = None) -> None:
            '''A URL for crawling.

            :param url: URL for crawling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-seedurl.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                seed_url_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eef69ab233a26e6764c5f6d6fb441e58fb474196659096b6a6abd1b7fa7766a0)
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''URL for crawling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-seedurl.html#cfn-wisdom-knowledgebase-seedurl-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SeedUrlProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "breakpoint_percentile_threshold": "breakpointPercentileThreshold",
            "buffer_size": "bufferSize",
            "max_tokens": "maxTokens",
        },
    )
    class SemanticChunkingConfigurationProperty:
        def __init__(
            self,
            *,
            breakpoint_percentile_threshold: typing.Optional[jsii.Number] = None,
            buffer_size: typing.Optional[jsii.Number] = None,
            max_tokens: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Settings for semantic document chunking for a data source.

            Semantic chunking splits a document into smaller documents based on groups of similar content derived from the text with natural language processing.

            :param breakpoint_percentile_threshold: The dissimilarity threshold for splitting chunks.
            :param buffer_size: The buffer size.
            :param max_tokens: The maximum number of tokens that a chunk can contain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-semanticchunkingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                semantic_chunking_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty(
                    breakpoint_percentile_threshold=123,
                    buffer_size=123,
                    max_tokens=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5f389a536a85a3ed9a7451d4a5105d157c2db551930323b3f06d9456a7f9bd5)
                check_type(argname="argument breakpoint_percentile_threshold", value=breakpoint_percentile_threshold, expected_type=type_hints["breakpoint_percentile_threshold"])
                check_type(argname="argument buffer_size", value=buffer_size, expected_type=type_hints["buffer_size"])
                check_type(argname="argument max_tokens", value=max_tokens, expected_type=type_hints["max_tokens"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if breakpoint_percentile_threshold is not None:
                self._values["breakpoint_percentile_threshold"] = breakpoint_percentile_threshold
            if buffer_size is not None:
                self._values["buffer_size"] = buffer_size
            if max_tokens is not None:
                self._values["max_tokens"] = max_tokens

        @builtins.property
        def breakpoint_percentile_threshold(self) -> typing.Optional[jsii.Number]:
            '''The dissimilarity threshold for splitting chunks.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-semanticchunkingconfiguration.html#cfn-wisdom-knowledgebase-semanticchunkingconfiguration-breakpointpercentilethreshold
            '''
            result = self._values.get("breakpoint_percentile_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def buffer_size(self) -> typing.Optional[jsii.Number]:
            '''The buffer size.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-semanticchunkingconfiguration.html#cfn-wisdom-knowledgebase-semanticchunkingconfiguration-buffersize
            '''
            result = self._values.get("buffer_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_tokens(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of tokens that a chunk can contain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-semanticchunkingconfiguration.html#cfn-wisdom-knowledgebase-semanticchunkingconfiguration-maxtokens
            '''
            result = self._values.get("max_tokens")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SemanticChunkingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''The configuration information for the customer managed key used for encryption.

            :param kms_key_id: The customer managed key used for encryption. This customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom. For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-serversideencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                server_side_encryption_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty(
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29b6fe90a3247fbfaa5a89bb8d739366f41a8158bfacd41d10371accad6ab40b)
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''The customer managed key used for encryption.

            This customer managed key must have a policy that allows ``kms:CreateGrant`` and ``kms:DescribeKey`` permissions to the IAM identity using the key to invoke Wisdom.

            For more information about setting up a customer managed key for Wisdom, see `Enable Amazon Connect Wisdom for your instance <https://docs.aws.amazon.com/connect/latest/adminguide/enable-wisdom.html>`_ . For information about valid ID values, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-serversideencryptionconfiguration.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_integrations": "appIntegrations",
            "managed_source_configuration": "managedSourceConfiguration",
        },
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            app_integrations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            managed_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration information about the external data source.

            :param app_integrations: Configuration information for Amazon AppIntegrations to automatically ingest content.
            :param managed_source_configuration: Source configuration for managed resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                source_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.SourceConfigurationProperty(
                    app_integrations=wisdom_mixins.CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty(
                        app_integration_arn="appIntegrationArn",
                        object_fields=["objectFields"]
                    ),
                    managed_source_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty(
                        web_crawler_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty(
                            crawler_limits=wisdom_mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty(
                                rate_limit=123
                            ),
                            exclusion_filters=["exclusionFilters"],
                            inclusion_filters=["inclusionFilters"],
                            scope="scope",
                            url_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty(
                                seed_urls=[wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                                    url="url"
                                )]
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16087d6dbdd25e2798b001c30fc92247bb6815f50dbd9a886975b14e1eb20ef1)
                check_type(argname="argument app_integrations", value=app_integrations, expected_type=type_hints["app_integrations"])
                check_type(argname="argument managed_source_configuration", value=managed_source_configuration, expected_type=type_hints["managed_source_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_integrations is not None:
                self._values["app_integrations"] = app_integrations
            if managed_source_configuration is not None:
                self._values["managed_source_configuration"] = managed_source_configuration

        @builtins.property
        def app_integrations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty"]]:
            '''Configuration information for Amazon AppIntegrations to automatically ingest content.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html#cfn-wisdom-knowledgebase-sourceconfiguration-appintegrations
            '''
            result = self._values.get("app_integrations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty"]], result)

        @builtins.property
        def managed_source_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty"]]:
            '''Source configuration for managed resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html#cfn-wisdom-knowledgebase-sourceconfiguration-managedsourceconfiguration
            '''
            result = self._values.get("managed_source_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"seed_urls": "seedUrls"},
    )
    class UrlConfigurationProperty:
        def __init__(
            self,
            *,
            seed_urls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.SeedUrlProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration of the URL/URLs for the web content that you want to crawl.

            You should be authorized to crawl the URLs.

            :param seed_urls: List of URLs for crawling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-urlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                url_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty(
                    seed_urls=[wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                        url="url"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b77cac5eabd9968767a656c4b6c14d06465e97593f2f0e257735ede41919f57c)
                check_type(argname="argument seed_urls", value=seed_urls, expected_type=type_hints["seed_urls"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if seed_urls is not None:
                self._values["seed_urls"] = seed_urls

        @builtins.property
        def seed_urls(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.SeedUrlProperty"]]]]:
            '''List of URLs for crawling.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-urlconfiguration.html#cfn-wisdom-knowledgebase-urlconfiguration-seedurls
            '''
            result = self._values.get("seed_urls")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.SeedUrlProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "chunking_configuration": "chunkingConfiguration",
            "parsing_configuration": "parsingConfiguration",
        },
    )
    class VectorIngestionConfigurationProperty:
        def __init__(
            self,
            *,
            chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parsing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details about how to ingest the documents in a data source.

            :param chunking_configuration: Details about how to chunk the documents in the data source. A chunk refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried.
            :param parsing_configuration: A custom parser for data source documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-vectoringestionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                vector_ingestion_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty(
                    chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty(
                        chunking_strategy="chunkingStrategy",
                        fixed_size_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty(
                            max_tokens=123,
                            overlap_percentage=123
                        ),
                        hierarchical_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty(
                            level_configurations=[wisdom_mixins.CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty(
                                max_tokens=123
                            )],
                            overlap_tokens=123
                        ),
                        semantic_chunking_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty(
                            breakpoint_percentile_threshold=123,
                            buffer_size=123,
                            max_tokens=123
                        )
                    ),
                    parsing_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty(
                        bedrock_foundation_model_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty(
                            model_arn="modelArn",
                            parsing_prompt=wisdom_mixins.CfnKnowledgeBasePropsMixin.ParsingPromptProperty(
                                parsing_prompt_text="parsingPromptText"
                            )
                        ),
                        parsing_strategy="parsingStrategy"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e16629e5e37798600ed3f07d5b61e05f80db64a941c1a6da649f3f550870ebcb)
                check_type(argname="argument chunking_configuration", value=chunking_configuration, expected_type=type_hints["chunking_configuration"])
                check_type(argname="argument parsing_configuration", value=parsing_configuration, expected_type=type_hints["parsing_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if chunking_configuration is not None:
                self._values["chunking_configuration"] = chunking_configuration
            if parsing_configuration is not None:
                self._values["parsing_configuration"] = parsing_configuration

        @builtins.property
        def chunking_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty"]]:
            '''Details about how to chunk the documents in the data source.

            A chunk refers to an excerpt from a data source that is returned when the knowledge base that it belongs to is queried.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-vectoringestionconfiguration.html#cfn-wisdom-knowledgebase-vectoringestionconfiguration-chunkingconfiguration
            '''
            result = self._values.get("chunking_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty"]], result)

        @builtins.property
        def parsing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty"]]:
            '''A custom parser for data source documents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-vectoringestionconfiguration.html#cfn-wisdom-knowledgebase-vectoringestionconfiguration-parsingconfiguration
            '''
            result = self._values.get("parsing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VectorIngestionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crawler_limits": "crawlerLimits",
            "exclusion_filters": "exclusionFilters",
            "inclusion_filters": "inclusionFilters",
            "scope": "scope",
            "url_configuration": "urlConfiguration",
        },
    )
    class WebCrawlerConfigurationProperty:
        def __init__(
            self,
            *,
            crawler_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclusion_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
            inclusion_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
            scope: typing.Optional[builtins.str] = None,
            url_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKnowledgeBasePropsMixin.UrlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration details for the web data source.

            :param crawler_limits: The configuration of crawl limits for the web URLs.
            :param exclusion_filters: A list of one or more exclusion regular expression patterns to exclude certain URLs. If you specify an inclusion and exclusion filter/pattern and both match a URL, the exclusion filter takes precedence and the web content of the URL isn’t crawled.
            :param inclusion_filters: A list of one or more inclusion regular expression patterns to include certain URLs. If you specify an inclusion and exclusion filter/pattern and both match a URL, the exclusion filter takes precedence and the web content of the URL isn’t crawled.
            :param scope: The scope of what is crawled for your URLs. You can choose to crawl only web pages that belong to the same host or primary domain. For example, only web pages that contain the seed URL ``https://docs.aws.amazon.com/bedrock/latest/userguide/`` and no other domains. You can choose to include sub domains in addition to the host or primary domain. For example, web pages that contain ``aws.amazon.com`` can also include sub domain ``docs.aws.amazon.com`` .
            :param url_configuration: The configuration of the URL/URLs for the web content that you want to crawl. You should be authorized to crawl the URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-webcrawlerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                web_crawler_configuration_property = wisdom_mixins.CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty(
                    crawler_limits=wisdom_mixins.CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty(
                        rate_limit=123
                    ),
                    exclusion_filters=["exclusionFilters"],
                    inclusion_filters=["inclusionFilters"],
                    scope="scope",
                    url_configuration=wisdom_mixins.CfnKnowledgeBasePropsMixin.UrlConfigurationProperty(
                        seed_urls=[wisdom_mixins.CfnKnowledgeBasePropsMixin.SeedUrlProperty(
                            url="url"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a13cb912ac7eb05b27e9b64fc92108cc692ee3ccfd54038007b4db5dabbe350)
                check_type(argname="argument crawler_limits", value=crawler_limits, expected_type=type_hints["crawler_limits"])
                check_type(argname="argument exclusion_filters", value=exclusion_filters, expected_type=type_hints["exclusion_filters"])
                check_type(argname="argument inclusion_filters", value=inclusion_filters, expected_type=type_hints["inclusion_filters"])
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument url_configuration", value=url_configuration, expected_type=type_hints["url_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crawler_limits is not None:
                self._values["crawler_limits"] = crawler_limits
            if exclusion_filters is not None:
                self._values["exclusion_filters"] = exclusion_filters
            if inclusion_filters is not None:
                self._values["inclusion_filters"] = inclusion_filters
            if scope is not None:
                self._values["scope"] = scope
            if url_configuration is not None:
                self._values["url_configuration"] = url_configuration

        @builtins.property
        def crawler_limits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty"]]:
            '''The configuration of crawl limits for the web URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-webcrawlerconfiguration.html#cfn-wisdom-knowledgebase-webcrawlerconfiguration-crawlerlimits
            '''
            result = self._values.get("crawler_limits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty"]], result)

        @builtins.property
        def exclusion_filters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more exclusion regular expression patterns to exclude certain URLs.

            If you specify an inclusion and exclusion filter/pattern and both match a URL, the exclusion filter takes precedence and the web content of the URL isn’t crawled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-webcrawlerconfiguration.html#cfn-wisdom-knowledgebase-webcrawlerconfiguration-exclusionfilters
            '''
            result = self._values.get("exclusion_filters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def inclusion_filters(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of one or more inclusion regular expression patterns to include certain URLs.

            If you specify an inclusion and exclusion filter/pattern and both match a URL, the exclusion filter takes precedence and the web content of the URL isn’t crawled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-webcrawlerconfiguration.html#cfn-wisdom-knowledgebase-webcrawlerconfiguration-inclusionfilters
            '''
            result = self._values.get("inclusion_filters")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scope(self) -> typing.Optional[builtins.str]:
            '''The scope of what is crawled for your URLs.

            You can choose to crawl only web pages that belong to the same host or primary domain. For example, only web pages that contain the seed URL ``https://docs.aws.amazon.com/bedrock/latest/userguide/`` and no other domains. You can choose to include sub domains in addition to the host or primary domain. For example, web pages that contain ``aws.amazon.com`` can also include sub domain ``docs.aws.amazon.com`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-webcrawlerconfiguration.html#cfn-wisdom-knowledgebase-webcrawlerconfiguration-scope
            '''
            result = self._values.get("scope")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.UrlConfigurationProperty"]]:
            '''The configuration of the URL/URLs for the web content that you want to crawl.

            You should be authorized to crawl the URLs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-webcrawlerconfiguration.html#cfn-wisdom-knowledgebase-webcrawlerconfiguration-urlconfiguration
            '''
            result = self._values.get("url_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKnowledgeBasePropsMixin.UrlConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebCrawlerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_subtype": "channelSubtype",
        "content": "content",
        "default_attributes": "defaultAttributes",
        "description": "description",
        "grouping_configuration": "groupingConfiguration",
        "knowledge_base_arn": "knowledgeBaseArn",
        "language": "language",
        "message_template_attachments": "messageTemplateAttachments",
        "name": "name",
        "tags": "tags",
    },
)
class CfnMessageTemplateMixinProps:
    def __init__(
        self,
        *,
        channel_subtype: typing.Optional[builtins.str] = None,
        content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.ContentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        default_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        grouping_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.GroupingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        knowledge_base_arn: typing.Optional[builtins.str] = None,
        language: typing.Optional[builtins.str] = None,
        message_template_attachments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnMessageTemplatePropsMixin.

        :param channel_subtype: The channel subtype this message template applies to.
        :param content: The content of the message template.
        :param default_attributes: An object that specifies the default values to use for variables in the message template. This object contains different categories of key-value pairs. Each key defines a variable or placeholder in the message template. The corresponding value defines the default value for that variable.
        :param description: The description of the message template.
        :param grouping_configuration: The configuration information of the external data source.
        :param knowledge_base_arn: The Amazon Resource Name (ARN) of the knowledge base.
        :param language: The language code value for the language in which the quick response is written. The supported language codes include ``de_DE`` , ``en_US`` , ``es_ES`` , ``fr_FR`` , ``id_ID`` , ``it_IT`` , ``ja_JP`` , ``ko_KR`` , ``pt_BR`` , ``zh_CN`` , ``zh_TW``
        :param message_template_attachments: List of message template attachments.
        :param name: The name of the message template.
        :param tags: The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_message_template_mixin_props = wisdom_mixins.CfnMessageTemplateMixinProps(
                channel_subtype="channelSubtype",
                content=wisdom_mixins.CfnMessageTemplatePropsMixin.ContentProperty(
                    email_message_template_content=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty(
                        body=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty(
                            html=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                                content="content"
                            ),
                            plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                                content="content"
                            )
                        ),
                        headers=[wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty(
                            name="name",
                            value="value"
                        )],
                        subject="subject"
                    ),
                    sms_message_template_content=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty(
                        body=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty(
                            plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                                content="content"
                            )
                        )
                    )
                ),
                default_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty(
                    agent_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.AgentAttributesProperty(
                        first_name="firstName",
                        last_name="lastName"
                    ),
                    custom_attributes={
                        "custom_attributes_key": "customAttributes"
                    },
                    customer_profile_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty(
                        account_number="accountNumber",
                        additional_information="additionalInformation",
                        address1="address1",
                        address2="address2",
                        address3="address3",
                        address4="address4",
                        billing_address1="billingAddress1",
                        billing_address2="billingAddress2",
                        billing_address3="billingAddress3",
                        billing_address4="billingAddress4",
                        billing_city="billingCity",
                        billing_country="billingCountry",
                        billing_county="billingCounty",
                        billing_postal_code="billingPostalCode",
                        billing_province="billingProvince",
                        billing_state="billingState",
                        birth_date="birthDate",
                        business_email_address="businessEmailAddress",
                        business_name="businessName",
                        business_phone_number="businessPhoneNumber",
                        city="city",
                        country="country",
                        county="county",
                        custom={
                            "custom_key": "custom"
                        },
                        email_address="emailAddress",
                        first_name="firstName",
                        gender="gender",
                        home_phone_number="homePhoneNumber",
                        last_name="lastName",
                        mailing_address1="mailingAddress1",
                        mailing_address2="mailingAddress2",
                        mailing_address3="mailingAddress3",
                        mailing_address4="mailingAddress4",
                        mailing_city="mailingCity",
                        mailing_country="mailingCountry",
                        mailing_county="mailingCounty",
                        mailing_postal_code="mailingPostalCode",
                        mailing_province="mailingProvince",
                        mailing_state="mailingState",
                        middle_name="middleName",
                        mobile_phone_number="mobilePhoneNumber",
                        party_type="partyType",
                        phone_number="phoneNumber",
                        postal_code="postalCode",
                        profile_arn="profileArn",
                        profile_id="profileId",
                        province="province",
                        shipping_address1="shippingAddress1",
                        shipping_address2="shippingAddress2",
                        shipping_address3="shippingAddress3",
                        shipping_address4="shippingAddress4",
                        shipping_city="shippingCity",
                        shipping_country="shippingCountry",
                        shipping_county="shippingCounty",
                        shipping_postal_code="shippingPostalCode",
                        shipping_province="shippingProvince",
                        shipping_state="shippingState",
                        state="state"
                    ),
                    system_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemAttributesProperty(
                        customer_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                            address="address"
                        ),
                        name="name",
                        system_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                            address="address"
                        )
                    )
                ),
                description="description",
                grouping_configuration=wisdom_mixins.CfnMessageTemplatePropsMixin.GroupingConfigurationProperty(
                    criteria="criteria",
                    values=["values"]
                ),
                knowledge_base_arn="knowledgeBaseArn",
                language="language",
                message_template_attachments=[wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty(
                    attachment_id="attachmentId",
                    attachment_name="attachmentName",
                    s3_presigned_url="s3PresignedUrl"
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca5cc8f9fb58c60c4f731bb247c19bacb7b5531779a428d32fff6f8dac9ad339)
            check_type(argname="argument channel_subtype", value=channel_subtype, expected_type=type_hints["channel_subtype"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument default_attributes", value=default_attributes, expected_type=type_hints["default_attributes"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument grouping_configuration", value=grouping_configuration, expected_type=type_hints["grouping_configuration"])
            check_type(argname="argument knowledge_base_arn", value=knowledge_base_arn, expected_type=type_hints["knowledge_base_arn"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument message_template_attachments", value=message_template_attachments, expected_type=type_hints["message_template_attachments"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_subtype is not None:
            self._values["channel_subtype"] = channel_subtype
        if content is not None:
            self._values["content"] = content
        if default_attributes is not None:
            self._values["default_attributes"] = default_attributes
        if description is not None:
            self._values["description"] = description
        if grouping_configuration is not None:
            self._values["grouping_configuration"] = grouping_configuration
        if knowledge_base_arn is not None:
            self._values["knowledge_base_arn"] = knowledge_base_arn
        if language is not None:
            self._values["language"] = language
        if message_template_attachments is not None:
            self._values["message_template_attachments"] = message_template_attachments
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_subtype(self) -> typing.Optional[builtins.str]:
        '''The channel subtype this message template applies to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-channelsubtype
        '''
        result = self._values.get("channel_subtype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.ContentProperty"]]:
        '''The content of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.ContentProperty"]], result)

    @builtins.property
    def default_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty"]]:
        '''An object that specifies the default values to use for variables in the message template.

        This object contains different categories of key-value pairs. Each key defines a variable or placeholder in the message template. The corresponding value defines the default value for that variable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-defaultattributes
        '''
        result = self._values.get("default_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grouping_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.GroupingConfigurationProperty"]]:
        '''The configuration information of the external data source.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-groupingconfiguration
        '''
        result = self._values.get("grouping_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.GroupingConfigurationProperty"]], result)

    @builtins.property
    def knowledge_base_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-knowledgebasearn
        '''
        result = self._values.get("knowledge_base_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''The language code value for the language in which the quick response is written.

        The supported language codes include ``de_DE`` , ``en_US`` , ``es_ES`` , ``fr_FR`` , ``id_ID`` , ``it_IT`` , ``ja_JP`` , ``ko_KR`` , ``pt_BR`` , ``zh_CN`` , ``zh_TW``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-language
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_template_attachments(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty"]]]]:
        '''List of message template attachments.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-messagetemplateattachments
        '''
        result = self._values.get("message_template_attachments")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html#cfn-wisdom-messagetemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMessageTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMessageTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin",
):
    '''Creates an Amazon Q in Connect message template.

    The name of the message template has to be unique for each knowledge base. The channel subtype of the message template is immutable and cannot be modified after creation. After the message template is created, you can use the ``$LATEST`` qualifier to reference the created message template.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplate.html
    :cloudformationResource: AWS::Wisdom::MessageTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_message_template_props_mixin = wisdom_mixins.CfnMessageTemplatePropsMixin(wisdom_mixins.CfnMessageTemplateMixinProps(
            channel_subtype="channelSubtype",
            content=wisdom_mixins.CfnMessageTemplatePropsMixin.ContentProperty(
                email_message_template_content=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty(
                    body=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty(
                        html=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                            content="content"
                        ),
                        plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                            content="content"
                        )
                    ),
                    headers=[wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty(
                        name="name",
                        value="value"
                    )],
                    subject="subject"
                ),
                sms_message_template_content=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty(
                    body=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty(
                        plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                            content="content"
                        )
                    )
                )
            ),
            default_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty(
                agent_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.AgentAttributesProperty(
                    first_name="firstName",
                    last_name="lastName"
                ),
                custom_attributes={
                    "custom_attributes_key": "customAttributes"
                },
                customer_profile_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty(
                    account_number="accountNumber",
                    additional_information="additionalInformation",
                    address1="address1",
                    address2="address2",
                    address3="address3",
                    address4="address4",
                    billing_address1="billingAddress1",
                    billing_address2="billingAddress2",
                    billing_address3="billingAddress3",
                    billing_address4="billingAddress4",
                    billing_city="billingCity",
                    billing_country="billingCountry",
                    billing_county="billingCounty",
                    billing_postal_code="billingPostalCode",
                    billing_province="billingProvince",
                    billing_state="billingState",
                    birth_date="birthDate",
                    business_email_address="businessEmailAddress",
                    business_name="businessName",
                    business_phone_number="businessPhoneNumber",
                    city="city",
                    country="country",
                    county="county",
                    custom={
                        "custom_key": "custom"
                    },
                    email_address="emailAddress",
                    first_name="firstName",
                    gender="gender",
                    home_phone_number="homePhoneNumber",
                    last_name="lastName",
                    mailing_address1="mailingAddress1",
                    mailing_address2="mailingAddress2",
                    mailing_address3="mailingAddress3",
                    mailing_address4="mailingAddress4",
                    mailing_city="mailingCity",
                    mailing_country="mailingCountry",
                    mailing_county="mailingCounty",
                    mailing_postal_code="mailingPostalCode",
                    mailing_province="mailingProvince",
                    mailing_state="mailingState",
                    middle_name="middleName",
                    mobile_phone_number="mobilePhoneNumber",
                    party_type="partyType",
                    phone_number="phoneNumber",
                    postal_code="postalCode",
                    profile_arn="profileArn",
                    profile_id="profileId",
                    province="province",
                    shipping_address1="shippingAddress1",
                    shipping_address2="shippingAddress2",
                    shipping_address3="shippingAddress3",
                    shipping_address4="shippingAddress4",
                    shipping_city="shippingCity",
                    shipping_country="shippingCountry",
                    shipping_county="shippingCounty",
                    shipping_postal_code="shippingPostalCode",
                    shipping_province="shippingProvince",
                    shipping_state="shippingState",
                    state="state"
                ),
                system_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemAttributesProperty(
                    customer_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                        address="address"
                    ),
                    name="name",
                    system_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                        address="address"
                    )
                )
            ),
            description="description",
            grouping_configuration=wisdom_mixins.CfnMessageTemplatePropsMixin.GroupingConfigurationProperty(
                criteria="criteria",
                values=["values"]
            ),
            knowledge_base_arn="knowledgeBaseArn",
            language="language",
            message_template_attachments=[wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty(
                attachment_id="attachmentId",
                attachment_name="attachmentName",
                s3_presigned_url="s3PresignedUrl"
            )],
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
        props: typing.Union[CfnMessageTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::MessageTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf9c7969afab71d8a654334bfe0759b801afc30b3b743ef7ac7981846d8a965)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33f1ae760591b49c23ca9546cb15e6d5454423827b3ab9911e9004be38e35224)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb197805db30033184669fd80b6244da39cfd0cbb101543225b07455bd2f4ae8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMessageTemplateMixinProps:
        return typing.cast(CfnMessageTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.AgentAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"first_name": "firstName", "last_name": "lastName"},
    )
    class AgentAttributesProperty:
        def __init__(
            self,
            *,
            first_name: typing.Optional[builtins.str] = None,
            last_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about an agent.

            :param first_name: The agent’s first name as entered in their Amazon Connect user account.
            :param last_name: The agent’s last name as entered in their Amazon Connect user account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-agentattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                agent_attributes_property = wisdom_mixins.CfnMessageTemplatePropsMixin.AgentAttributesProperty(
                    first_name="firstName",
                    last_name="lastName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc7ec0f569df73abac0d8bb23135caec52bd8de0fd9b7c12f9cfde699dbbfabe)
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if first_name is not None:
                self._values["first_name"] = first_name
            if last_name is not None:
                self._values["last_name"] = last_name

        @builtins.property
        def first_name(self) -> typing.Optional[builtins.str]:
            '''The agent’s first name as entered in their Amazon Connect user account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-agentattributes.html#cfn-wisdom-messagetemplate-agentattributes-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_name(self) -> typing.Optional[builtins.str]:
            '''The agent’s last name as entered in their Amazon Connect user account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-agentattributes.html#cfn-wisdom-messagetemplate-agentattributes-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.ContentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email_message_template_content": "emailMessageTemplateContent",
            "sms_message_template_content": "smsMessageTemplateContent",
        },
    )
    class ContentProperty:
        def __init__(
            self,
            *,
            email_message_template_content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sms_message_template_content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The content of the message template.

            :param email_message_template_content: The content of the message template that applies to the email channel subtype.
            :param sms_message_template_content: The content of message template that applies to SMS channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-content.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                content_property = wisdom_mixins.CfnMessageTemplatePropsMixin.ContentProperty(
                    email_message_template_content=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty(
                        body=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty(
                            html=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                                content="content"
                            ),
                            plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                                content="content"
                            )
                        ),
                        headers=[wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty(
                            name="name",
                            value="value"
                        )],
                        subject="subject"
                    ),
                    sms_message_template_content=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty(
                        body=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty(
                            plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                                content="content"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b2015e27291cff0949e9993ebeac12cb053b2e02c763a1fb217ecc4ece19e06)
                check_type(argname="argument email_message_template_content", value=email_message_template_content, expected_type=type_hints["email_message_template_content"])
                check_type(argname="argument sms_message_template_content", value=sms_message_template_content, expected_type=type_hints["sms_message_template_content"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_message_template_content is not None:
                self._values["email_message_template_content"] = email_message_template_content
            if sms_message_template_content is not None:
                self._values["sms_message_template_content"] = sms_message_template_content

        @builtins.property
        def email_message_template_content(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty"]]:
            '''The content of the message template that applies to the email channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-content.html#cfn-wisdom-messagetemplate-content-emailmessagetemplatecontent
            '''
            result = self._values.get("email_message_template_content")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty"]], result)

        @builtins.property
        def sms_message_template_content(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty"]]:
            '''The content of message template that applies to SMS channel subtype.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-content.html#cfn-wisdom-messagetemplate-content-smsmessagetemplatecontent
            '''
            result = self._values.get("sms_message_template_content")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "account_number": "accountNumber",
            "additional_information": "additionalInformation",
            "address1": "address1",
            "address2": "address2",
            "address3": "address3",
            "address4": "address4",
            "billing_address1": "billingAddress1",
            "billing_address2": "billingAddress2",
            "billing_address3": "billingAddress3",
            "billing_address4": "billingAddress4",
            "billing_city": "billingCity",
            "billing_country": "billingCountry",
            "billing_county": "billingCounty",
            "billing_postal_code": "billingPostalCode",
            "billing_province": "billingProvince",
            "billing_state": "billingState",
            "birth_date": "birthDate",
            "business_email_address": "businessEmailAddress",
            "business_name": "businessName",
            "business_phone_number": "businessPhoneNumber",
            "city": "city",
            "country": "country",
            "county": "county",
            "custom": "custom",
            "email_address": "emailAddress",
            "first_name": "firstName",
            "gender": "gender",
            "home_phone_number": "homePhoneNumber",
            "last_name": "lastName",
            "mailing_address1": "mailingAddress1",
            "mailing_address2": "mailingAddress2",
            "mailing_address3": "mailingAddress3",
            "mailing_address4": "mailingAddress4",
            "mailing_city": "mailingCity",
            "mailing_country": "mailingCountry",
            "mailing_county": "mailingCounty",
            "mailing_postal_code": "mailingPostalCode",
            "mailing_province": "mailingProvince",
            "mailing_state": "mailingState",
            "middle_name": "middleName",
            "mobile_phone_number": "mobilePhoneNumber",
            "party_type": "partyType",
            "phone_number": "phoneNumber",
            "postal_code": "postalCode",
            "profile_arn": "profileArn",
            "profile_id": "profileId",
            "province": "province",
            "shipping_address1": "shippingAddress1",
            "shipping_address2": "shippingAddress2",
            "shipping_address3": "shippingAddress3",
            "shipping_address4": "shippingAddress4",
            "shipping_city": "shippingCity",
            "shipping_country": "shippingCountry",
            "shipping_county": "shippingCounty",
            "shipping_postal_code": "shippingPostalCode",
            "shipping_province": "shippingProvince",
            "shipping_state": "shippingState",
            "state": "state",
        },
    )
    class CustomerProfileAttributesProperty:
        def __init__(
            self,
            *,
            account_number: typing.Optional[builtins.str] = None,
            additional_information: typing.Optional[builtins.str] = None,
            address1: typing.Optional[builtins.str] = None,
            address2: typing.Optional[builtins.str] = None,
            address3: typing.Optional[builtins.str] = None,
            address4: typing.Optional[builtins.str] = None,
            billing_address1: typing.Optional[builtins.str] = None,
            billing_address2: typing.Optional[builtins.str] = None,
            billing_address3: typing.Optional[builtins.str] = None,
            billing_address4: typing.Optional[builtins.str] = None,
            billing_city: typing.Optional[builtins.str] = None,
            billing_country: typing.Optional[builtins.str] = None,
            billing_county: typing.Optional[builtins.str] = None,
            billing_postal_code: typing.Optional[builtins.str] = None,
            billing_province: typing.Optional[builtins.str] = None,
            billing_state: typing.Optional[builtins.str] = None,
            birth_date: typing.Optional[builtins.str] = None,
            business_email_address: typing.Optional[builtins.str] = None,
            business_name: typing.Optional[builtins.str] = None,
            business_phone_number: typing.Optional[builtins.str] = None,
            city: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            county: typing.Optional[builtins.str] = None,
            custom: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            email_address: typing.Optional[builtins.str] = None,
            first_name: typing.Optional[builtins.str] = None,
            gender: typing.Optional[builtins.str] = None,
            home_phone_number: typing.Optional[builtins.str] = None,
            last_name: typing.Optional[builtins.str] = None,
            mailing_address1: typing.Optional[builtins.str] = None,
            mailing_address2: typing.Optional[builtins.str] = None,
            mailing_address3: typing.Optional[builtins.str] = None,
            mailing_address4: typing.Optional[builtins.str] = None,
            mailing_city: typing.Optional[builtins.str] = None,
            mailing_country: typing.Optional[builtins.str] = None,
            mailing_county: typing.Optional[builtins.str] = None,
            mailing_postal_code: typing.Optional[builtins.str] = None,
            mailing_province: typing.Optional[builtins.str] = None,
            mailing_state: typing.Optional[builtins.str] = None,
            middle_name: typing.Optional[builtins.str] = None,
            mobile_phone_number: typing.Optional[builtins.str] = None,
            party_type: typing.Optional[builtins.str] = None,
            phone_number: typing.Optional[builtins.str] = None,
            postal_code: typing.Optional[builtins.str] = None,
            profile_arn: typing.Optional[builtins.str] = None,
            profile_id: typing.Optional[builtins.str] = None,
            province: typing.Optional[builtins.str] = None,
            shipping_address1: typing.Optional[builtins.str] = None,
            shipping_address2: typing.Optional[builtins.str] = None,
            shipping_address3: typing.Optional[builtins.str] = None,
            shipping_address4: typing.Optional[builtins.str] = None,
            shipping_city: typing.Optional[builtins.str] = None,
            shipping_country: typing.Optional[builtins.str] = None,
            shipping_county: typing.Optional[builtins.str] = None,
            shipping_postal_code: typing.Optional[builtins.str] = None,
            shipping_province: typing.Optional[builtins.str] = None,
            shipping_state: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The customer profile attributes that are used with the message template.

            :param account_number: A unique account number that you have given to the customer.
            :param additional_information: Any additional information relevant to the customer's profile.
            :param address1: The first line of a customer address.
            :param address2: The second line of a customer address.
            :param address3: The third line of a customer address.
            :param address4: The fourth line of a customer address.
            :param billing_address1: The first line of a customer’s billing address.
            :param billing_address2: The second line of a customer’s billing address.
            :param billing_address3: The third line of a customer’s billing address.
            :param billing_address4: The fourth line of a customer’s billing address.
            :param billing_city: The city of a customer’s billing address.
            :param billing_country: The country of a customer’s billing address.
            :param billing_county: The county of a customer’s billing address.
            :param billing_postal_code: The postal code of a customer’s billing address.
            :param billing_province: The province of a customer’s billing address.
            :param billing_state: The state of a customer’s billing address.
            :param birth_date: The customer's birth date.
            :param business_email_address: The customer's business email address.
            :param business_name: The name of the customer's business.
            :param business_phone_number: The customer's business phone number.
            :param city: The city in which a customer lives.
            :param country: The country in which a customer lives.
            :param county: The county in which a customer lives.
            :param custom: The custom attributes in customer profile attributes.
            :param email_address: The customer's email address, which has not been specified as a personal or business address.
            :param first_name: The customer's first name.
            :param gender: The customer's gender.
            :param home_phone_number: The customer's mobile phone number.
            :param last_name: The customer's last name.
            :param mailing_address1: The first line of a customer’s mailing address.
            :param mailing_address2: The second line of a customer’s mailing address.
            :param mailing_address3: The third line of a customer’s mailing address.
            :param mailing_address4: The fourth line of a customer’s mailing address.
            :param mailing_city: The city of a customer’s mailing address.
            :param mailing_country: The country of a customer’s mailing address.
            :param mailing_county: The county of a customer’s mailing address.
            :param mailing_postal_code: The postal code of a customer’s mailing address.
            :param mailing_province: The province of a customer’s mailing address.
            :param mailing_state: The state of a customer’s mailing address.
            :param middle_name: The customer's middle name.
            :param mobile_phone_number: The customer's mobile phone number.
            :param party_type: The customer's party type.
            :param phone_number: The customer's phone number, which has not been specified as a mobile, home, or business number.
            :param postal_code: The postal code of a customer address.
            :param profile_arn: The ARN of a customer profile.
            :param profile_id: The unique identifier of a customer profile.
            :param province: The province in which a customer lives.
            :param shipping_address1: The first line of a customer’s shipping address.
            :param shipping_address2: The second line of a customer’s shipping address.
            :param shipping_address3: The third line of a customer’s shipping address.
            :param shipping_address4: The fourth line of a customer’s shipping address.
            :param shipping_city: The city of a customer’s shipping address.
            :param shipping_country: The country of a customer’s shipping address.
            :param shipping_county: The county of a customer’s shipping address.
            :param shipping_postal_code: The postal code of a customer’s shipping address.
            :param shipping_province: The province of a customer’s shipping address.
            :param shipping_state: The state of a customer’s shipping address.
            :param state: The state in which a customer lives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                customer_profile_attributes_property = wisdom_mixins.CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty(
                    account_number="accountNumber",
                    additional_information="additionalInformation",
                    address1="address1",
                    address2="address2",
                    address3="address3",
                    address4="address4",
                    billing_address1="billingAddress1",
                    billing_address2="billingAddress2",
                    billing_address3="billingAddress3",
                    billing_address4="billingAddress4",
                    billing_city="billingCity",
                    billing_country="billingCountry",
                    billing_county="billingCounty",
                    billing_postal_code="billingPostalCode",
                    billing_province="billingProvince",
                    billing_state="billingState",
                    birth_date="birthDate",
                    business_email_address="businessEmailAddress",
                    business_name="businessName",
                    business_phone_number="businessPhoneNumber",
                    city="city",
                    country="country",
                    county="county",
                    custom={
                        "custom_key": "custom"
                    },
                    email_address="emailAddress",
                    first_name="firstName",
                    gender="gender",
                    home_phone_number="homePhoneNumber",
                    last_name="lastName",
                    mailing_address1="mailingAddress1",
                    mailing_address2="mailingAddress2",
                    mailing_address3="mailingAddress3",
                    mailing_address4="mailingAddress4",
                    mailing_city="mailingCity",
                    mailing_country="mailingCountry",
                    mailing_county="mailingCounty",
                    mailing_postal_code="mailingPostalCode",
                    mailing_province="mailingProvince",
                    mailing_state="mailingState",
                    middle_name="middleName",
                    mobile_phone_number="mobilePhoneNumber",
                    party_type="partyType",
                    phone_number="phoneNumber",
                    postal_code="postalCode",
                    profile_arn="profileArn",
                    profile_id="profileId",
                    province="province",
                    shipping_address1="shippingAddress1",
                    shipping_address2="shippingAddress2",
                    shipping_address3="shippingAddress3",
                    shipping_address4="shippingAddress4",
                    shipping_city="shippingCity",
                    shipping_country="shippingCountry",
                    shipping_county="shippingCounty",
                    shipping_postal_code="shippingPostalCode",
                    shipping_province="shippingProvince",
                    shipping_state="shippingState",
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5def9c96428c19124b9dc756e3fbd86cf649620bf10aa947bb8c62492dad405e)
                check_type(argname="argument account_number", value=account_number, expected_type=type_hints["account_number"])
                check_type(argname="argument additional_information", value=additional_information, expected_type=type_hints["additional_information"])
                check_type(argname="argument address1", value=address1, expected_type=type_hints["address1"])
                check_type(argname="argument address2", value=address2, expected_type=type_hints["address2"])
                check_type(argname="argument address3", value=address3, expected_type=type_hints["address3"])
                check_type(argname="argument address4", value=address4, expected_type=type_hints["address4"])
                check_type(argname="argument billing_address1", value=billing_address1, expected_type=type_hints["billing_address1"])
                check_type(argname="argument billing_address2", value=billing_address2, expected_type=type_hints["billing_address2"])
                check_type(argname="argument billing_address3", value=billing_address3, expected_type=type_hints["billing_address3"])
                check_type(argname="argument billing_address4", value=billing_address4, expected_type=type_hints["billing_address4"])
                check_type(argname="argument billing_city", value=billing_city, expected_type=type_hints["billing_city"])
                check_type(argname="argument billing_country", value=billing_country, expected_type=type_hints["billing_country"])
                check_type(argname="argument billing_county", value=billing_county, expected_type=type_hints["billing_county"])
                check_type(argname="argument billing_postal_code", value=billing_postal_code, expected_type=type_hints["billing_postal_code"])
                check_type(argname="argument billing_province", value=billing_province, expected_type=type_hints["billing_province"])
                check_type(argname="argument billing_state", value=billing_state, expected_type=type_hints["billing_state"])
                check_type(argname="argument birth_date", value=birth_date, expected_type=type_hints["birth_date"])
                check_type(argname="argument business_email_address", value=business_email_address, expected_type=type_hints["business_email_address"])
                check_type(argname="argument business_name", value=business_name, expected_type=type_hints["business_name"])
                check_type(argname="argument business_phone_number", value=business_phone_number, expected_type=type_hints["business_phone_number"])
                check_type(argname="argument city", value=city, expected_type=type_hints["city"])
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument county", value=county, expected_type=type_hints["county"])
                check_type(argname="argument custom", value=custom, expected_type=type_hints["custom"])
                check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument gender", value=gender, expected_type=type_hints["gender"])
                check_type(argname="argument home_phone_number", value=home_phone_number, expected_type=type_hints["home_phone_number"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
                check_type(argname="argument mailing_address1", value=mailing_address1, expected_type=type_hints["mailing_address1"])
                check_type(argname="argument mailing_address2", value=mailing_address2, expected_type=type_hints["mailing_address2"])
                check_type(argname="argument mailing_address3", value=mailing_address3, expected_type=type_hints["mailing_address3"])
                check_type(argname="argument mailing_address4", value=mailing_address4, expected_type=type_hints["mailing_address4"])
                check_type(argname="argument mailing_city", value=mailing_city, expected_type=type_hints["mailing_city"])
                check_type(argname="argument mailing_country", value=mailing_country, expected_type=type_hints["mailing_country"])
                check_type(argname="argument mailing_county", value=mailing_county, expected_type=type_hints["mailing_county"])
                check_type(argname="argument mailing_postal_code", value=mailing_postal_code, expected_type=type_hints["mailing_postal_code"])
                check_type(argname="argument mailing_province", value=mailing_province, expected_type=type_hints["mailing_province"])
                check_type(argname="argument mailing_state", value=mailing_state, expected_type=type_hints["mailing_state"])
                check_type(argname="argument middle_name", value=middle_name, expected_type=type_hints["middle_name"])
                check_type(argname="argument mobile_phone_number", value=mobile_phone_number, expected_type=type_hints["mobile_phone_number"])
                check_type(argname="argument party_type", value=party_type, expected_type=type_hints["party_type"])
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
                check_type(argname="argument postal_code", value=postal_code, expected_type=type_hints["postal_code"])
                check_type(argname="argument profile_arn", value=profile_arn, expected_type=type_hints["profile_arn"])
                check_type(argname="argument profile_id", value=profile_id, expected_type=type_hints["profile_id"])
                check_type(argname="argument province", value=province, expected_type=type_hints["province"])
                check_type(argname="argument shipping_address1", value=shipping_address1, expected_type=type_hints["shipping_address1"])
                check_type(argname="argument shipping_address2", value=shipping_address2, expected_type=type_hints["shipping_address2"])
                check_type(argname="argument shipping_address3", value=shipping_address3, expected_type=type_hints["shipping_address3"])
                check_type(argname="argument shipping_address4", value=shipping_address4, expected_type=type_hints["shipping_address4"])
                check_type(argname="argument shipping_city", value=shipping_city, expected_type=type_hints["shipping_city"])
                check_type(argname="argument shipping_country", value=shipping_country, expected_type=type_hints["shipping_country"])
                check_type(argname="argument shipping_county", value=shipping_county, expected_type=type_hints["shipping_county"])
                check_type(argname="argument shipping_postal_code", value=shipping_postal_code, expected_type=type_hints["shipping_postal_code"])
                check_type(argname="argument shipping_province", value=shipping_province, expected_type=type_hints["shipping_province"])
                check_type(argname="argument shipping_state", value=shipping_state, expected_type=type_hints["shipping_state"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account_number is not None:
                self._values["account_number"] = account_number
            if additional_information is not None:
                self._values["additional_information"] = additional_information
            if address1 is not None:
                self._values["address1"] = address1
            if address2 is not None:
                self._values["address2"] = address2
            if address3 is not None:
                self._values["address3"] = address3
            if address4 is not None:
                self._values["address4"] = address4
            if billing_address1 is not None:
                self._values["billing_address1"] = billing_address1
            if billing_address2 is not None:
                self._values["billing_address2"] = billing_address2
            if billing_address3 is not None:
                self._values["billing_address3"] = billing_address3
            if billing_address4 is not None:
                self._values["billing_address4"] = billing_address4
            if billing_city is not None:
                self._values["billing_city"] = billing_city
            if billing_country is not None:
                self._values["billing_country"] = billing_country
            if billing_county is not None:
                self._values["billing_county"] = billing_county
            if billing_postal_code is not None:
                self._values["billing_postal_code"] = billing_postal_code
            if billing_province is not None:
                self._values["billing_province"] = billing_province
            if billing_state is not None:
                self._values["billing_state"] = billing_state
            if birth_date is not None:
                self._values["birth_date"] = birth_date
            if business_email_address is not None:
                self._values["business_email_address"] = business_email_address
            if business_name is not None:
                self._values["business_name"] = business_name
            if business_phone_number is not None:
                self._values["business_phone_number"] = business_phone_number
            if city is not None:
                self._values["city"] = city
            if country is not None:
                self._values["country"] = country
            if county is not None:
                self._values["county"] = county
            if custom is not None:
                self._values["custom"] = custom
            if email_address is not None:
                self._values["email_address"] = email_address
            if first_name is not None:
                self._values["first_name"] = first_name
            if gender is not None:
                self._values["gender"] = gender
            if home_phone_number is not None:
                self._values["home_phone_number"] = home_phone_number
            if last_name is not None:
                self._values["last_name"] = last_name
            if mailing_address1 is not None:
                self._values["mailing_address1"] = mailing_address1
            if mailing_address2 is not None:
                self._values["mailing_address2"] = mailing_address2
            if mailing_address3 is not None:
                self._values["mailing_address3"] = mailing_address3
            if mailing_address4 is not None:
                self._values["mailing_address4"] = mailing_address4
            if mailing_city is not None:
                self._values["mailing_city"] = mailing_city
            if mailing_country is not None:
                self._values["mailing_country"] = mailing_country
            if mailing_county is not None:
                self._values["mailing_county"] = mailing_county
            if mailing_postal_code is not None:
                self._values["mailing_postal_code"] = mailing_postal_code
            if mailing_province is not None:
                self._values["mailing_province"] = mailing_province
            if mailing_state is not None:
                self._values["mailing_state"] = mailing_state
            if middle_name is not None:
                self._values["middle_name"] = middle_name
            if mobile_phone_number is not None:
                self._values["mobile_phone_number"] = mobile_phone_number
            if party_type is not None:
                self._values["party_type"] = party_type
            if phone_number is not None:
                self._values["phone_number"] = phone_number
            if postal_code is not None:
                self._values["postal_code"] = postal_code
            if profile_arn is not None:
                self._values["profile_arn"] = profile_arn
            if profile_id is not None:
                self._values["profile_id"] = profile_id
            if province is not None:
                self._values["province"] = province
            if shipping_address1 is not None:
                self._values["shipping_address1"] = shipping_address1
            if shipping_address2 is not None:
                self._values["shipping_address2"] = shipping_address2
            if shipping_address3 is not None:
                self._values["shipping_address3"] = shipping_address3
            if shipping_address4 is not None:
                self._values["shipping_address4"] = shipping_address4
            if shipping_city is not None:
                self._values["shipping_city"] = shipping_city
            if shipping_country is not None:
                self._values["shipping_country"] = shipping_country
            if shipping_county is not None:
                self._values["shipping_county"] = shipping_county
            if shipping_postal_code is not None:
                self._values["shipping_postal_code"] = shipping_postal_code
            if shipping_province is not None:
                self._values["shipping_province"] = shipping_province
            if shipping_state is not None:
                self._values["shipping_state"] = shipping_state
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def account_number(self) -> typing.Optional[builtins.str]:
            '''A unique account number that you have given to the customer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-accountnumber
            '''
            result = self._values.get("account_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def additional_information(self) -> typing.Optional[builtins.str]:
            '''Any additional information relevant to the customer's profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-additionalinformation
            '''
            result = self._values.get("additional_information")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def address1(self) -> typing.Optional[builtins.str]:
            '''The first line of a customer address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-address1
            '''
            result = self._values.get("address1")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def address2(self) -> typing.Optional[builtins.str]:
            '''The second line of a customer address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-address2
            '''
            result = self._values.get("address2")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def address3(self) -> typing.Optional[builtins.str]:
            '''The third line of a customer address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-address3
            '''
            result = self._values.get("address3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def address4(self) -> typing.Optional[builtins.str]:
            '''The fourth line of a customer address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-address4
            '''
            result = self._values.get("address4")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_address1(self) -> typing.Optional[builtins.str]:
            '''The first line of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingaddress1
            '''
            result = self._values.get("billing_address1")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_address2(self) -> typing.Optional[builtins.str]:
            '''The second line of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingaddress2
            '''
            result = self._values.get("billing_address2")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_address3(self) -> typing.Optional[builtins.str]:
            '''The third line of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingaddress3
            '''
            result = self._values.get("billing_address3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_address4(self) -> typing.Optional[builtins.str]:
            '''The fourth line of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingaddress4
            '''
            result = self._values.get("billing_address4")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_city(self) -> typing.Optional[builtins.str]:
            '''The city of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingcity
            '''
            result = self._values.get("billing_city")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_country(self) -> typing.Optional[builtins.str]:
            '''The country of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingcountry
            '''
            result = self._values.get("billing_country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_county(self) -> typing.Optional[builtins.str]:
            '''The county of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingcounty
            '''
            result = self._values.get("billing_county")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_postal_code(self) -> typing.Optional[builtins.str]:
            '''The postal code of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingpostalcode
            '''
            result = self._values.get("billing_postal_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_province(self) -> typing.Optional[builtins.str]:
            '''The province of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingprovince
            '''
            result = self._values.get("billing_province")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def billing_state(self) -> typing.Optional[builtins.str]:
            '''The state of a customer’s billing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-billingstate
            '''
            result = self._values.get("billing_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def birth_date(self) -> typing.Optional[builtins.str]:
            '''The customer's birth date.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-birthdate
            '''
            result = self._values.get("birth_date")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def business_email_address(self) -> typing.Optional[builtins.str]:
            '''The customer's business email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-businessemailaddress
            '''
            result = self._values.get("business_email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def business_name(self) -> typing.Optional[builtins.str]:
            '''The name of the customer's business.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-businessname
            '''
            result = self._values.get("business_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def business_phone_number(self) -> typing.Optional[builtins.str]:
            '''The customer's business phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-businessphonenumber
            '''
            result = self._values.get("business_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def city(self) -> typing.Optional[builtins.str]:
            '''The city in which a customer lives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-city
            '''
            result = self._values.get("city")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            '''The country in which a customer lives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def county(self) -> typing.Optional[builtins.str]:
            '''The county in which a customer lives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-county
            '''
            result = self._values.get("county")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The custom attributes in customer profile attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-custom
            '''
            result = self._values.get("custom")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def email_address(self) -> typing.Optional[builtins.str]:
            '''The customer's email address, which has not been specified as a personal or business address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-emailaddress
            '''
            result = self._values.get("email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_name(self) -> typing.Optional[builtins.str]:
            '''The customer's first name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def gender(self) -> typing.Optional[builtins.str]:
            '''The customer's gender.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-gender
            '''
            result = self._values.get("gender")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def home_phone_number(self) -> typing.Optional[builtins.str]:
            '''The customer's mobile phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-homephonenumber
            '''
            result = self._values.get("home_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_name(self) -> typing.Optional[builtins.str]:
            '''The customer's last name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_address1(self) -> typing.Optional[builtins.str]:
            '''The first line of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingaddress1
            '''
            result = self._values.get("mailing_address1")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_address2(self) -> typing.Optional[builtins.str]:
            '''The second line of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingaddress2
            '''
            result = self._values.get("mailing_address2")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_address3(self) -> typing.Optional[builtins.str]:
            '''The third line of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingaddress3
            '''
            result = self._values.get("mailing_address3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_address4(self) -> typing.Optional[builtins.str]:
            '''The fourth line of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingaddress4
            '''
            result = self._values.get("mailing_address4")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_city(self) -> typing.Optional[builtins.str]:
            '''The city of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingcity
            '''
            result = self._values.get("mailing_city")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_country(self) -> typing.Optional[builtins.str]:
            '''The country of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingcountry
            '''
            result = self._values.get("mailing_country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_county(self) -> typing.Optional[builtins.str]:
            '''The county of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingcounty
            '''
            result = self._values.get("mailing_county")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_postal_code(self) -> typing.Optional[builtins.str]:
            '''The postal code of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingpostalcode
            '''
            result = self._values.get("mailing_postal_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_province(self) -> typing.Optional[builtins.str]:
            '''The province of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingprovince
            '''
            result = self._values.get("mailing_province")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mailing_state(self) -> typing.Optional[builtins.str]:
            '''The state of a customer’s mailing address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mailingstate
            '''
            result = self._values.get("mailing_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def middle_name(self) -> typing.Optional[builtins.str]:
            '''The customer's middle name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-middlename
            '''
            result = self._values.get("middle_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mobile_phone_number(self) -> typing.Optional[builtins.str]:
            '''The customer's mobile phone number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-mobilephonenumber
            '''
            result = self._values.get("mobile_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def party_type(self) -> typing.Optional[builtins.str]:
            '''The customer's party type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-partytype
            '''
            result = self._values.get("party_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def phone_number(self) -> typing.Optional[builtins.str]:
            '''The customer's phone number, which has not been specified as a mobile, home, or business number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-phonenumber
            '''
            result = self._values.get("phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def postal_code(self) -> typing.Optional[builtins.str]:
            '''The postal code of a customer address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-postalcode
            '''
            result = self._values.get("postal_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def profile_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of a customer profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-profilearn
            '''
            result = self._values.get("profile_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def profile_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of a customer profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-profileid
            '''
            result = self._values.get("profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def province(self) -> typing.Optional[builtins.str]:
            '''The province in which a customer lives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-province
            '''
            result = self._values.get("province")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_address1(self) -> typing.Optional[builtins.str]:
            '''The first line of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingaddress1
            '''
            result = self._values.get("shipping_address1")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_address2(self) -> typing.Optional[builtins.str]:
            '''The second line of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingaddress2
            '''
            result = self._values.get("shipping_address2")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_address3(self) -> typing.Optional[builtins.str]:
            '''The third line of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingaddress3
            '''
            result = self._values.get("shipping_address3")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_address4(self) -> typing.Optional[builtins.str]:
            '''The fourth line of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingaddress4
            '''
            result = self._values.get("shipping_address4")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_city(self) -> typing.Optional[builtins.str]:
            '''The city of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingcity
            '''
            result = self._values.get("shipping_city")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_country(self) -> typing.Optional[builtins.str]:
            '''The country of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingcountry
            '''
            result = self._values.get("shipping_country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_county(self) -> typing.Optional[builtins.str]:
            '''The county of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingcounty
            '''
            result = self._values.get("shipping_county")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_postal_code(self) -> typing.Optional[builtins.str]:
            '''The postal code of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingpostalcode
            '''
            result = self._values.get("shipping_postal_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_province(self) -> typing.Optional[builtins.str]:
            '''The province of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingprovince
            '''
            result = self._values.get("shipping_province")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shipping_state(self) -> typing.Optional[builtins.str]:
            '''The state of a customer’s shipping address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-shippingstate
            '''
            result = self._values.get("shipping_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The state in which a customer lives.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-customerprofileattributes.html#cfn-wisdom-messagetemplate-customerprofileattributes-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerProfileAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty",
        jsii_struct_bases=[],
        name_mapping={"html": "html", "plain_text": "plainText"},
    )
    class EmailMessageTemplateContentBodyProperty:
        def __init__(
            self,
            *,
            html: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            plain_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The body to use in email messages.

            :param html: The message body, in HTML format, to use in email messages that are based on the message template. We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.
            :param plain_text: The message body, in plain text format, to use in email messages that are based on the message template. We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontentbody.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                email_message_template_content_body_property = wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty(
                    html=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                        content="content"
                    ),
                    plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                        content="content"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3759b1610a34d1250a9385aefae69cf3adb766dcf222ac88453a1496159b223a)
                check_type(argname="argument html", value=html, expected_type=type_hints["html"])
                check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if html is not None:
                self._values["html"] = html
            if plain_text is not None:
                self._values["plain_text"] = plain_text

        @builtins.property
        def html(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty"]]:
            '''The message body, in HTML format, to use in email messages that are based on the message template.

            We recommend using HTML format for email clients that render HTML content. You can include links, formatted text, and more in an HTML message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontentbody.html#cfn-wisdom-messagetemplate-emailmessagetemplatecontentbody-html
            '''
            result = self._values.get("html")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty"]], result)

        @builtins.property
        def plain_text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty"]]:
            '''The message body, in plain text format, to use in email messages that are based on the message template.

            We recommend using plain text format for email clients that don't render HTML content and clients that are connected to high-latency networks, such as mobile devices.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontentbody.html#cfn-wisdom-messagetemplate-emailmessagetemplatecontentbody-plaintext
            '''
            result = self._values.get("plain_text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailMessageTemplateContentBodyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty",
        jsii_struct_bases=[],
        name_mapping={"body": "body", "headers": "headers", "subject": "subject"},
    )
    class EmailMessageTemplateContentProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            subject: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The content of the message template that applies to the email channel subtype.

            :param body: The body to use in email messages.
            :param headers: The email headers to include in email messages.
            :param subject: The subject line, or title, to use in email messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                email_message_template_content_property = wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty(
                    body=wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty(
                        html=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                            content="content"
                        ),
                        plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                            content="content"
                        )
                    ),
                    headers=[wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty(
                        name="name",
                        value="value"
                    )],
                    subject="subject"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f07021687a553cf2d24315ba18ebebd31ea3a1626afae8b5082b07390c736e85)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
                check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body
            if headers is not None:
                self._values["headers"] = headers
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def body(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty"]]:
            '''The body to use in email messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontent.html#cfn-wisdom-messagetemplate-emailmessagetemplatecontent-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty"]], result)

        @builtins.property
        def headers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty"]]]]:
            '''The email headers to include in email messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontent.html#cfn-wisdom-messagetemplate-emailmessagetemplatecontent-headers
            '''
            result = self._values.get("headers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty"]]]], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The subject line, or title, to use in email messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplatecontent.html#cfn-wisdom-messagetemplate-emailmessagetemplatecontent-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailMessageTemplateContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EmailMessageTemplateHeaderProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The email headers to include in email messages.

            :param name: The name of the email header.
            :param value: The value of the email header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplateheader.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                email_message_template_header_property = wisdom_mixins.CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5a7cfd0f890a4d7c4768f59a06f1bc006bb43eaa779f6a4ff81974b31b58b37)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the email header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplateheader.html#cfn-wisdom-messagetemplate-emailmessagetemplateheader-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the email header.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-emailmessagetemplateheader.html#cfn-wisdom-messagetemplate-emailmessagetemplateheader-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmailMessageTemplateHeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.GroupingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"criteria": "criteria", "values": "values"},
    )
    class GroupingConfigurationProperty:
        def __init__(
            self,
            *,
            criteria: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration information of the grouping of Amazon Q in Connect users.

            :param criteria: The criteria used for grouping Amazon Q in Connect users. The following is the list of supported criteria values. - ``RoutingProfileArn`` : Grouping the users by their `Amazon Connect routing profile ARN <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ . User should have `SearchRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_SearchRoutingProfiles.html>`_ and `DescribeRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_DescribeRoutingProfile.html>`_ permissions when setting criteria to this value.
            :param values: The list of values that define different groups of Amazon Q in Connect users. - When setting ``criteria`` to ``RoutingProfileArn`` , you need to provide a list of ARNs of `Amazon Connect routing profiles <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ as values of this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-groupingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                grouping_configuration_property = wisdom_mixins.CfnMessageTemplatePropsMixin.GroupingConfigurationProperty(
                    criteria="criteria",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b446ec188648c430386cf440e46f93f2daa522d6f80edc6f08641c4fdc9896b6)
                check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criteria is not None:
                self._values["criteria"] = criteria
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def criteria(self) -> typing.Optional[builtins.str]:
            '''The criteria used for grouping Amazon Q in Connect users.

            The following is the list of supported criteria values.

            - ``RoutingProfileArn`` : Grouping the users by their `Amazon Connect routing profile ARN <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ . User should have `SearchRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_SearchRoutingProfiles.html>`_ and `DescribeRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_DescribeRoutingProfile.html>`_ permissions when setting criteria to this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-groupingconfiguration.html#cfn-wisdom-messagetemplate-groupingconfiguration-criteria
            '''
            result = self._values.get("criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of values that define different groups of Amazon Q in Connect users.

            - When setting ``criteria`` to ``RoutingProfileArn`` , you need to provide a list of ARNs of `Amazon Connect routing profiles <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ as values of this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-groupingconfiguration.html#cfn-wisdom-messagetemplate-groupingconfiguration-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_id": "attachmentId",
            "attachment_name": "attachmentName",
            "s3_presigned_url": "s3PresignedUrl",
        },
    )
    class MessageTemplateAttachmentProperty:
        def __init__(
            self,
            *,
            attachment_id: typing.Optional[builtins.str] = None,
            attachment_name: typing.Optional[builtins.str] = None,
            s3_presigned_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the message template attachment.

            :param attachment_id: The identifier of the attachment file.
            :param attachment_name: The name of the attachment file being uploaded. The name should include the file extension.
            :param s3_presigned_url: The S3 Presigned URL for the attachment file. When generating the PreSignedUrl, please ensure that the expires-in time is set to 30 minutes. The URL can be generated through the AWS Console or through the AWS CLI. For more information, see `Sharing objects with presigned URLs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                message_template_attachment_property = wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty(
                    attachment_id="attachmentId",
                    attachment_name="attachmentName",
                    s3_presigned_url="s3PresignedUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d551f98b55c89688039e30c45db17cb68dc43be16655f1ea066fc32f9ced9c5e)
                check_type(argname="argument attachment_id", value=attachment_id, expected_type=type_hints["attachment_id"])
                check_type(argname="argument attachment_name", value=attachment_name, expected_type=type_hints["attachment_name"])
                check_type(argname="argument s3_presigned_url", value=s3_presigned_url, expected_type=type_hints["s3_presigned_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_id is not None:
                self._values["attachment_id"] = attachment_id
            if attachment_name is not None:
                self._values["attachment_name"] = attachment_name
            if s3_presigned_url is not None:
                self._values["s3_presigned_url"] = s3_presigned_url

        @builtins.property
        def attachment_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the attachment file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattachment.html#cfn-wisdom-messagetemplate-messagetemplateattachment-attachmentid
            '''
            result = self._values.get("attachment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attachment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the attachment file being uploaded.

            The name should include the file extension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattachment.html#cfn-wisdom-messagetemplate-messagetemplateattachment-attachmentname
            '''
            result = self._values.get("attachment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_presigned_url(self) -> typing.Optional[builtins.str]:
            '''The S3 Presigned URL for the attachment file.

            When generating the PreSignedUrl, please ensure that the expires-in time is set to 30 minutes. The URL can be generated through the AWS Console or through the AWS CLI. For more information, see `Sharing objects with presigned URLs <https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattachment.html#cfn-wisdom-messagetemplate-messagetemplateattachment-s3presignedurl
            '''
            result = self._values.get("s3_presigned_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageTemplateAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "agent_attributes": "agentAttributes",
            "custom_attributes": "customAttributes",
            "customer_profile_attributes": "customerProfileAttributes",
            "system_attributes": "systemAttributes",
        },
    )
    class MessageTemplateAttributesProperty:
        def __init__(
            self,
            *,
            agent_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.AgentAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            custom_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            customer_profile_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            system_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.SystemAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The attributes that are used with the message template.

            :param agent_attributes: The agent attributes that are used with the message template.
            :param custom_attributes: The custom attributes that are used with the message template.
            :param customer_profile_attributes: The customer profile attributes that are used with the message template.
            :param system_attributes: The system attributes that are used with the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                message_template_attributes_property = wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty(
                    agent_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.AgentAttributesProperty(
                        first_name="firstName",
                        last_name="lastName"
                    ),
                    custom_attributes={
                        "custom_attributes_key": "customAttributes"
                    },
                    customer_profile_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty(
                        account_number="accountNumber",
                        additional_information="additionalInformation",
                        address1="address1",
                        address2="address2",
                        address3="address3",
                        address4="address4",
                        billing_address1="billingAddress1",
                        billing_address2="billingAddress2",
                        billing_address3="billingAddress3",
                        billing_address4="billingAddress4",
                        billing_city="billingCity",
                        billing_country="billingCountry",
                        billing_county="billingCounty",
                        billing_postal_code="billingPostalCode",
                        billing_province="billingProvince",
                        billing_state="billingState",
                        birth_date="birthDate",
                        business_email_address="businessEmailAddress",
                        business_name="businessName",
                        business_phone_number="businessPhoneNumber",
                        city="city",
                        country="country",
                        county="county",
                        custom={
                            "custom_key": "custom"
                        },
                        email_address="emailAddress",
                        first_name="firstName",
                        gender="gender",
                        home_phone_number="homePhoneNumber",
                        last_name="lastName",
                        mailing_address1="mailingAddress1",
                        mailing_address2="mailingAddress2",
                        mailing_address3="mailingAddress3",
                        mailing_address4="mailingAddress4",
                        mailing_city="mailingCity",
                        mailing_country="mailingCountry",
                        mailing_county="mailingCounty",
                        mailing_postal_code="mailingPostalCode",
                        mailing_province="mailingProvince",
                        mailing_state="mailingState",
                        middle_name="middleName",
                        mobile_phone_number="mobilePhoneNumber",
                        party_type="partyType",
                        phone_number="phoneNumber",
                        postal_code="postalCode",
                        profile_arn="profileArn",
                        profile_id="profileId",
                        province="province",
                        shipping_address1="shippingAddress1",
                        shipping_address2="shippingAddress2",
                        shipping_address3="shippingAddress3",
                        shipping_address4="shippingAddress4",
                        shipping_city="shippingCity",
                        shipping_country="shippingCountry",
                        shipping_county="shippingCounty",
                        shipping_postal_code="shippingPostalCode",
                        shipping_province="shippingProvince",
                        shipping_state="shippingState",
                        state="state"
                    ),
                    system_attributes=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemAttributesProperty(
                        customer_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                            address="address"
                        ),
                        name="name",
                        system_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                            address="address"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__daacd804b2dfc5df29232dafcac695ef660a983a95137fd9ddffaa8012434388)
                check_type(argname="argument agent_attributes", value=agent_attributes, expected_type=type_hints["agent_attributes"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument customer_profile_attributes", value=customer_profile_attributes, expected_type=type_hints["customer_profile_attributes"])
                check_type(argname="argument system_attributes", value=system_attributes, expected_type=type_hints["system_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if agent_attributes is not None:
                self._values["agent_attributes"] = agent_attributes
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if customer_profile_attributes is not None:
                self._values["customer_profile_attributes"] = customer_profile_attributes
            if system_attributes is not None:
                self._values["system_attributes"] = system_attributes

        @builtins.property
        def agent_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.AgentAttributesProperty"]]:
            '''The agent attributes that are used with the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattributes.html#cfn-wisdom-messagetemplate-messagetemplateattributes-agentattributes
            '''
            result = self._values.get("agent_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.AgentAttributesProperty"]], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The custom attributes that are used with the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattributes.html#cfn-wisdom-messagetemplate-messagetemplateattributes-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def customer_profile_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty"]]:
            '''The customer profile attributes that are used with the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattributes.html#cfn-wisdom-messagetemplate-messagetemplateattributes-customerprofileattributes
            '''
            result = self._values.get("customer_profile_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty"]], result)

        @builtins.property
        def system_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SystemAttributesProperty"]]:
            '''The system attributes that are used with the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplateattributes.html#cfn-wisdom-messagetemplate-messagetemplateattributes-systemattributes
            '''
            result = self._values.get("system_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SystemAttributesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageTemplateAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"content": "content"},
    )
    class MessageTemplateBodyContentProviderProperty:
        def __init__(self, *, content: typing.Optional[builtins.str] = None) -> None:
            '''The container of the message template body.

            :param content: The content of the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplatebodycontentprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                message_template_body_content_provider_property = wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                    content="content"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9e31b2bc5113de977be3b46fd1b53e262a02c7e8ef556ecb83a4f93e4b6be5b)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''The content of the message template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-messagetemplatebodycontentprovider.html#cfn-wisdom-messagetemplate-messagetemplatebodycontentprovider-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MessageTemplateBodyContentProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty",
        jsii_struct_bases=[],
        name_mapping={"plain_text": "plainText"},
    )
    class SmsMessageTemplateContentBodyProperty:
        def __init__(
            self,
            *,
            plain_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The body to use in SMS messages.

            :param plain_text: The message body to use in SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-smsmessagetemplatecontentbody.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                sms_message_template_content_body_property = wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty(
                    plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                        content="content"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22d5828a366b37644966b825565122702001c59f720987e9b4932194d9816b25)
                check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if plain_text is not None:
                self._values["plain_text"] = plain_text

        @builtins.property
        def plain_text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty"]]:
            '''The message body to use in SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-smsmessagetemplatecontentbody.html#cfn-wisdom-messagetemplate-smsmessagetemplatecontentbody-plaintext
            '''
            result = self._values.get("plain_text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsMessageTemplateContentBodyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty",
        jsii_struct_bases=[],
        name_mapping={"body": "body"},
    )
    class SmsMessageTemplateContentProperty:
        def __init__(
            self,
            *,
            body: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The content of the message template that applies to the SMS channel subtype.

            :param body: The body to use in SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-smsmessagetemplatecontent.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                sms_message_template_content_property = wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty(
                    body=wisdom_mixins.CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty(
                        plain_text=wisdom_mixins.CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty(
                            content="content"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c56959e3976d7c4090a139e10926571b72c8cf561d75766fe484fc454ec9ce45)
                check_type(argname="argument body", value=body, expected_type=type_hints["body"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if body is not None:
                self._values["body"] = body

        @builtins.property
        def body(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty"]]:
            '''The body to use in SMS messages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-smsmessagetemplatecontent.html#cfn-wisdom-messagetemplate-smsmessagetemplatecontent-body
            '''
            result = self._values.get("body")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SmsMessageTemplateContentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.SystemAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_endpoint": "customerEndpoint",
            "name": "name",
            "system_endpoint": "systemEndpoint",
        },
    )
    class SystemAttributesProperty:
        def __init__(
            self,
            *,
            customer_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            system_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The system attributes that are used with the message template.

            :param customer_endpoint: The CustomerEndpoint attribute.
            :param name: The name of the task.
            :param system_endpoint: The SystemEndpoint attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-systemattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                system_attributes_property = wisdom_mixins.CfnMessageTemplatePropsMixin.SystemAttributesProperty(
                    customer_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                        address="address"
                    ),
                    name="name",
                    system_endpoint=wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                        address="address"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4174e68c69a55ec116e385974805e1c54d815193b1bb15712cf044322353713e)
                check_type(argname="argument customer_endpoint", value=customer_endpoint, expected_type=type_hints["customer_endpoint"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument system_endpoint", value=system_endpoint, expected_type=type_hints["system_endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_endpoint is not None:
                self._values["customer_endpoint"] = customer_endpoint
            if name is not None:
                self._values["name"] = name
            if system_endpoint is not None:
                self._values["system_endpoint"] = system_endpoint

        @builtins.property
        def customer_endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty"]]:
            '''The CustomerEndpoint attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-systemattributes.html#cfn-wisdom-messagetemplate-systemattributes-customerendpoint
            '''
            result = self._values.get("customer_endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the task.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-systemattributes.html#cfn-wisdom-messagetemplate-systemattributes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def system_endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty"]]:
            '''The SystemEndpoint attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-systemattributes.html#cfn-wisdom-messagetemplate-systemattributes-systemendpoint
            '''
            result = self._values.get("system_endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SystemAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address"},
    )
    class SystemEndpointAttributesProperty:
        def __init__(self, *, address: typing.Optional[builtins.str] = None) -> None:
            '''The system endpoint attributes that are used with the message template.

            :param address: The customer's phone number if used with ``customerEndpoint`` , or the number the customer dialed to call your contact center if used with ``systemEndpoint`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-systemendpointattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                system_endpoint_attributes_property = wisdom_mixins.CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty(
                    address="address"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c403c6a1d2544b9cfb108e7fae7a445ec1e59be5ca2d61a361c758554af9bcf3)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The customer's phone number if used with ``customerEndpoint`` , or the number the customer dialed to call your contact center if used with ``systemEndpoint`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-messagetemplate-systemendpointattributes.html#cfn-wisdom-messagetemplate-systemendpointattributes-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SystemEndpointAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplateVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "message_template_arn": "messageTemplateArn",
        "message_template_content_sha256": "messageTemplateContentSha256",
    },
)
class CfnMessageTemplateVersionMixinProps:
    def __init__(
        self,
        *,
        message_template_arn: typing.Optional[builtins.str] = None,
        message_template_content_sha256: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMessageTemplateVersionPropsMixin.

        :param message_template_arn: The Amazon Resource Name (ARN) of the message template.
        :param message_template_content_sha256: The content SHA256 of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplateversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_message_template_version_mixin_props = wisdom_mixins.CfnMessageTemplateVersionMixinProps(
                message_template_arn="messageTemplateArn",
                message_template_content_sha256="messageTemplateContentSha256"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b51e1ed0e829bf59b1cbb6e52b262888c172c26342bbb8aad63a2bfc61cb7e8)
            check_type(argname="argument message_template_arn", value=message_template_arn, expected_type=type_hints["message_template_arn"])
            check_type(argname="argument message_template_content_sha256", value=message_template_content_sha256, expected_type=type_hints["message_template_content_sha256"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_template_arn is not None:
            self._values["message_template_arn"] = message_template_arn
        if message_template_content_sha256 is not None:
            self._values["message_template_content_sha256"] = message_template_content_sha256

    @builtins.property
    def message_template_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplateversion.html#cfn-wisdom-messagetemplateversion-messagetemplatearn
        '''
        result = self._values.get("message_template_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_template_content_sha256(self) -> typing.Optional[builtins.str]:
        '''The content SHA256 of the message template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplateversion.html#cfn-wisdom-messagetemplateversion-messagetemplatecontentsha256
        '''
        result = self._values.get("message_template_content_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMessageTemplateVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMessageTemplateVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnMessageTemplateVersionPropsMixin",
):
    '''Creates a new Amazon Q in Connect message template version from the current content and configuration of a message template.

    Versions are immutable and monotonically increasing. Once a version is created, you can reference a specific version of the message template by passing in ``<messageTemplateArn>:<versionNumber>`` as the message template identifier. An error is displayed if the supplied ``messageTemplateContentSha256`` is different from the ``messageTemplateContentSha256`` of the message template with ``$LATEST`` qualifier. If multiple ``CreateMessageTemplateVersion`` requests are made while the message template remains the same, only the first invocation creates a new version and the succeeding requests will return the same response as the first invocation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-messagetemplateversion.html
    :cloudformationResource: AWS::Wisdom::MessageTemplateVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_message_template_version_props_mixin = wisdom_mixins.CfnMessageTemplateVersionPropsMixin(wisdom_mixins.CfnMessageTemplateVersionMixinProps(
            message_template_arn="messageTemplateArn",
            message_template_content_sha256="messageTemplateContentSha256"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMessageTemplateVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::MessageTemplateVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d981415698ad531878ebaf57bc4eab3da64c894c52446d31a6afc6918462407)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa7e89a99300890342ea43ea73e610271eb03746056ffdc0b5efe0351fa33e5e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637b99296c836e71fd0795e401c6ddccaddf2a14b38993cde924a149f015951a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMessageTemplateVersionMixinProps:
        return typing.cast(CfnMessageTemplateVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnQuickResponseMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channels": "channels",
        "content": "content",
        "content_type": "contentType",
        "description": "description",
        "grouping_configuration": "groupingConfiguration",
        "is_active": "isActive",
        "knowledge_base_arn": "knowledgeBaseArn",
        "language": "language",
        "name": "name",
        "shortcut_key": "shortcutKey",
        "tags": "tags",
    },
)
class CfnQuickResponseMixinProps:
    def __init__(
        self,
        *,
        channels: typing.Optional[typing.Sequence[builtins.str]] = None,
        content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        content_type: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        grouping_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickResponsePropsMixin.GroupingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        knowledge_base_arn: typing.Optional[builtins.str] = None,
        language: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        shortcut_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnQuickResponsePropsMixin.

        :param channels: The Amazon Connect contact channels this quick response applies to. The supported contact channel types include ``Chat`` .
        :param content: The content of the quick response.
        :param content_type: The media type of the quick response content. - Use ``application/x.quickresponse;format=plain`` for quick response written in plain text. - Use ``application/x.quickresponse;format=markdown`` for quick response written in richtext.
        :param description: The description of the quick response.
        :param grouping_configuration: The configuration information of the user groups that the quick response is accessible to.
        :param is_active: Whether the quick response is active.
        :param knowledge_base_arn: The Amazon Resource Name (ARN) of the knowledge base.
        :param language: The language code value for the language in which the quick response is written. The supported language codes include ``de_DE`` , ``en_US`` , ``es_ES`` , ``fr_FR`` , ``id_ID`` , ``it_IT`` , ``ja_JP`` , ``ko_KR`` , ``pt_BR`` , ``zh_CN`` , ``zh_TW``
        :param name: The name of the quick response.
        :param shortcut_key: The shortcut key of the quick response. The value should be unique across the knowledge base.
        :param tags: The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
            
            cfn_quick_response_mixin_props = wisdom_mixins.CfnQuickResponseMixinProps(
                channels=["channels"],
                content=wisdom_mixins.CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty(
                    content="content"
                ),
                content_type="contentType",
                description="description",
                grouping_configuration=wisdom_mixins.CfnQuickResponsePropsMixin.GroupingConfigurationProperty(
                    criteria="criteria",
                    values=["values"]
                ),
                is_active=False,
                knowledge_base_arn="knowledgeBaseArn",
                language="language",
                name="name",
                shortcut_key="shortcutKey",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dda0347dd3466e0ca54808c6c24756ad430900c9056013b35f5cd4e78bc88635)
            check_type(argname="argument channels", value=channels, expected_type=type_hints["channels"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument grouping_configuration", value=grouping_configuration, expected_type=type_hints["grouping_configuration"])
            check_type(argname="argument is_active", value=is_active, expected_type=type_hints["is_active"])
            check_type(argname="argument knowledge_base_arn", value=knowledge_base_arn, expected_type=type_hints["knowledge_base_arn"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument shortcut_key", value=shortcut_key, expected_type=type_hints["shortcut_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channels is not None:
            self._values["channels"] = channels
        if content is not None:
            self._values["content"] = content
        if content_type is not None:
            self._values["content_type"] = content_type
        if description is not None:
            self._values["description"] = description
        if grouping_configuration is not None:
            self._values["grouping_configuration"] = grouping_configuration
        if is_active is not None:
            self._values["is_active"] = is_active
        if knowledge_base_arn is not None:
            self._values["knowledge_base_arn"] = knowledge_base_arn
        if language is not None:
            self._values["language"] = language
        if name is not None:
            self._values["name"] = name
        if shortcut_key is not None:
            self._values["shortcut_key"] = shortcut_key
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channels(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Connect contact channels this quick response applies to.

        The supported contact channel types include ``Chat`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-channels
        '''
        result = self._values.get("channels")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def content(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty"]]:
        '''The content of the quick response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty"]], result)

    @builtins.property
    def content_type(self) -> typing.Optional[builtins.str]:
        '''The media type of the quick response content.

        - Use ``application/x.quickresponse;format=plain`` for quick response written in plain text.
        - Use ``application/x.quickresponse;format=markdown`` for quick response written in richtext.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-contenttype
        '''
        result = self._values.get("content_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def grouping_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.GroupingConfigurationProperty"]]:
        '''The configuration information of the user groups that the quick response is accessible to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-groupingconfiguration
        '''
        result = self._values.get("grouping_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.GroupingConfigurationProperty"]], result)

    @builtins.property
    def is_active(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether the quick response is active.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-isactive
        '''
        result = self._values.get("is_active")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def knowledge_base_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-knowledgebasearn
        '''
        result = self._values.get("knowledge_base_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''The language code value for the language in which the quick response is written.

        The supported language codes include ``de_DE`` , ``en_US`` , ``es_ES`` , ``fr_FR`` , ``id_ID`` , ``it_IT`` , ``ja_JP`` , ``ko_KR`` , ``pt_BR`` , ``zh_CN`` , ``zh_TW``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-language
        '''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the quick response.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def shortcut_key(self) -> typing.Optional[builtins.str]:
        '''The shortcut key of the quick response.

        The value should be unique across the knowledge base.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-shortcutkey
        '''
        result = self._values.get("shortcut_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html#cfn-wisdom-quickresponse-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQuickResponseMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQuickResponsePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnQuickResponsePropsMixin",
):
    '''Creates an Amazon Q in Connect quick response.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-quickresponse.html
    :cloudformationResource: AWS::Wisdom::QuickResponse
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
        
        cfn_quick_response_props_mixin = wisdom_mixins.CfnQuickResponsePropsMixin(wisdom_mixins.CfnQuickResponseMixinProps(
            channels=["channels"],
            content=wisdom_mixins.CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty(
                content="content"
            ),
            content_type="contentType",
            description="description",
            grouping_configuration=wisdom_mixins.CfnQuickResponsePropsMixin.GroupingConfigurationProperty(
                criteria="criteria",
                values=["values"]
            ),
            is_active=False,
            knowledge_base_arn="knowledgeBaseArn",
            language="language",
            name="name",
            shortcut_key="shortcutKey",
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
        props: typing.Union[CfnQuickResponseMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Wisdom::QuickResponse``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__568b4ecb16fb2ee7d9836d777588301e1dae5606a27dd03788ebc3d6c13c838b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5403d7d3567e281ebb56eba8426d8da4cb58511ade49a3edaf7e22ece4b76ef2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00b57ab6f8d5268387cb6845cc5bb41adf4819ad9bc0ab659ca9016773bf983)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQuickResponseMixinProps:
        return typing.cast(CfnQuickResponseMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnQuickResponsePropsMixin.GroupingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"criteria": "criteria", "values": "values"},
    )
    class GroupingConfigurationProperty:
        def __init__(
            self,
            *,
            criteria: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration information of the grouping of Amazon Q in Connect users.

            :param criteria: The criteria used for grouping Amazon Q in Connect users. The following is the list of supported criteria values. - ``RoutingProfileArn`` : Grouping the users by their `Amazon Connect routing profile ARN <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ . User should have `SearchRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_SearchRoutingProfiles.html>`_ and `DescribeRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_DescribeRoutingProfile.html>`_ permissions when setting criteria to this value.
            :param values: The list of values that define different groups of Amazon Q in Connect users. - When setting ``criteria`` to ``RoutingProfileArn`` , you need to provide a list of ARNs of `Amazon Connect routing profiles <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ as values of this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-groupingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                grouping_configuration_property = wisdom_mixins.CfnQuickResponsePropsMixin.GroupingConfigurationProperty(
                    criteria="criteria",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5f9551fb1307f7cddf8b5eed789c9d9ff3a051a8c19acd715ed7a9c24dc0b0e)
                check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if criteria is not None:
                self._values["criteria"] = criteria
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def criteria(self) -> typing.Optional[builtins.str]:
            '''The criteria used for grouping Amazon Q in Connect users.

            The following is the list of supported criteria values.

            - ``RoutingProfileArn`` : Grouping the users by their `Amazon Connect routing profile ARN <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ . User should have `SearchRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_SearchRoutingProfiles.html>`_ and `DescribeRoutingProfile <https://docs.aws.amazon.com/connect/latest/APIReference/API_DescribeRoutingProfile.html>`_ permissions when setting criteria to this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-groupingconfiguration.html#cfn-wisdom-quickresponse-groupingconfiguration-criteria
            '''
            result = self._values.get("criteria")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of values that define different groups of Amazon Q in Connect users.

            - When setting ``criteria`` to ``RoutingProfileArn`` , you need to provide a list of ARNs of `Amazon Connect routing profiles <https://docs.aws.amazon.com/connect/latest/APIReference/API_RoutingProfile.html>`_ as values of this parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-groupingconfiguration.html#cfn-wisdom-quickresponse-groupingconfiguration-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GroupingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"content": "content"},
    )
    class QuickResponseContentProviderProperty:
        def __init__(self, *, content: typing.Optional[builtins.str] = None) -> None:
            '''The container quick response content.

            :param content: The content of the quick response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-quickresponsecontentprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                quick_response_content_provider_property = wisdom_mixins.CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty(
                    content="content"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3cd1c6db8b6ee2df25169811e91f8e5ea0f74334721c5f77ecb076c5ce2e452)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''The content of the quick response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-quickresponsecontentprovider.html#cfn-wisdom-quickresponse-quickresponsecontentprovider-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickResponseContentProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_wisdom.mixins.CfnQuickResponsePropsMixin.QuickResponseContentsProperty",
        jsii_struct_bases=[],
        name_mapping={"markdown": "markdown", "plain_text": "plainText"},
    )
    class QuickResponseContentsProperty:
        def __init__(
            self,
            *,
            markdown: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            plain_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The content of the quick response stored in different media types.

            :param markdown: The quick response content in markdown format.
            :param plain_text: The quick response content in plaintext format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-quickresponsecontents.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_wisdom import mixins as wisdom_mixins
                
                quick_response_contents_property = wisdom_mixins.CfnQuickResponsePropsMixin.QuickResponseContentsProperty(
                    markdown=wisdom_mixins.CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty(
                        content="content"
                    ),
                    plain_text=wisdom_mixins.CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty(
                        content="content"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d4223c662ae0c9aa89e49519337a72e1cf6405cd56505c95c66aecc32e62ba5)
                check_type(argname="argument markdown", value=markdown, expected_type=type_hints["markdown"])
                check_type(argname="argument plain_text", value=plain_text, expected_type=type_hints["plain_text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if markdown is not None:
                self._values["markdown"] = markdown
            if plain_text is not None:
                self._values["plain_text"] = plain_text

        @builtins.property
        def markdown(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty"]]:
            '''The quick response content in markdown format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-quickresponsecontents.html#cfn-wisdom-quickresponse-quickresponsecontents-markdown
            '''
            result = self._values.get("markdown")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty"]], result)

        @builtins.property
        def plain_text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty"]]:
            '''The quick response content in plaintext format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-quickresponse-quickresponsecontents.html#cfn-wisdom-quickresponse-quickresponsecontents-plaintext
            '''
            result = self._values.get("plain_text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickResponseContentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAIAgentMixinProps",
    "CfnAIAgentPropsMixin",
    "CfnAIAgentVersionMixinProps",
    "CfnAIAgentVersionPropsMixin",
    "CfnAIGuardrailMixinProps",
    "CfnAIGuardrailPropsMixin",
    "CfnAIGuardrailVersionMixinProps",
    "CfnAIGuardrailVersionPropsMixin",
    "CfnAIPromptMixinProps",
    "CfnAIPromptPropsMixin",
    "CfnAIPromptVersionMixinProps",
    "CfnAIPromptVersionPropsMixin",
    "CfnAssistantAssociationMixinProps",
    "CfnAssistantAssociationPropsMixin",
    "CfnAssistantEventLogs",
    "CfnAssistantLogsMixin",
    "CfnAssistantMixinProps",
    "CfnAssistantPropsMixin",
    "CfnKnowledgeBaseMixinProps",
    "CfnKnowledgeBasePropsMixin",
    "CfnMessageTemplateMixinProps",
    "CfnMessageTemplatePropsMixin",
    "CfnMessageTemplateVersionMixinProps",
    "CfnMessageTemplateVersionPropsMixin",
    "CfnQuickResponseMixinProps",
    "CfnQuickResponsePropsMixin",
]

publication.publish()

def _typecheckingstub__27814174d706c442bf0c49f6a8cb21bba026f9a1674b38823df3400afad50d30(
    *,
    assistant_id: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653f77c98a2394dacf7f699b69ed637b4cf42a4db75c9f4523ce52a6b08a546c(
    props: typing.Union[CfnAIAgentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d999820ff4ef670e7029dcbe51f2488680661d188f7d16552455042e31126284(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb46838782e66f52dcbe96cddf0e292daee05e157d3eee66c49dfb3330dd1a32(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71da4bc2d98c15d65fcbafc685c90a346d7807ac59e6b52b8967b8afe774b6f2(
    *,
    answer_recommendation_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AnswerRecommendationAIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_generative_answer_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.EmailGenerativeAnswerAIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_overview_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.EmailOverviewAIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    email_response_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.EmailResponseAIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    manual_search_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.ManualSearchAIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    self_service_ai_agent_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.SelfServiceAIAgentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f3a97f9c5f20f59253470458669541d2ae79b45039a19c2c9b1f56bc349f7fa(
    *,
    answer_generation_ai_guardrail_id: typing.Optional[builtins.str] = None,
    answer_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
    association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AssociationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    intent_labeling_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
    locale: typing.Optional[builtins.str] = None,
    query_reformulation_ai_prompt_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e896547aa203a0d26a01ac838077831c7df2901bc4265e346fa0ca5e7863a289(
    *,
    knowledge_base_association_configuration_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.KnowledgeBaseAssociationConfigurationDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da70c2c4a16d7d9681550416155356f436f5b206af691b6b9b3844469ecddc8f(
    *,
    association_configuration_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AssociationConfigurationDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    association_id: typing.Optional[builtins.str] = None,
    association_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c2aa4bf99f36cfe0dc3d468197fbc00378e5d9a208cf406889f89b04f61022f(
    *,
    association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AssociationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    email_generative_answer_ai_prompt_id: typing.Optional[builtins.str] = None,
    email_query_reformulation_ai_prompt_id: typing.Optional[builtins.str] = None,
    locale: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc918b332ea23a60477a33368c58178e80d7c1af6bdf15f3ae994ac8d062ff5(
    *,
    email_overview_ai_prompt_id: typing.Optional[builtins.str] = None,
    locale: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bf9b4c7838e4e0490f476ba8f9b0243b22353597d4facf45d1ffdd6cf71e29(
    *,
    association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AssociationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    email_query_reformulation_ai_prompt_id: typing.Optional[builtins.str] = None,
    email_response_ai_prompt_id: typing.Optional[builtins.str] = None,
    locale: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0ab106ee71fc3667316fe727a475ce430c5584f3ebf313f3c7d9325c2a52bc(
    *,
    content_tag_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.TagFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_results: typing.Optional[jsii.Number] = None,
    override_knowledge_base_search_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b6397bca0a4ad1e89715ed0440adb9144887a057790323a07f885351aeb3316(
    *,
    answer_generation_ai_guardrail_id: typing.Optional[builtins.str] = None,
    answer_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
    association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AssociationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    locale: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a1ae7a4e615e80eac5f1b8603beea51c897295cecc0ab431e5419bbce430496(
    *,
    and_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.TagConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tag_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.TagConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4657129cba3a012b0307cf16f29f73ce08edd03501ba59f87700f6437d167e64(
    *,
    association_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.AssociationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    self_service_ai_guardrail_id: typing.Optional[builtins.str] = None,
    self_service_answer_generation_ai_prompt_id: typing.Optional[builtins.str] = None,
    self_service_pre_processing_ai_prompt_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ba42bd711c75ac17cc6f435703e4ed37cb7229f737aa9be9c73a5dc81a0e44a(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87bdf4e2dc86a1e41c1fc39eb9cf72c57798a78443d687a89ba65df038d4ff75(
    *,
    and_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.TagConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    or_conditions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.OrConditionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tag_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIAgentPropsMixin.TagConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc06dc518fa2e4dab70d374b1450a5e5f6c567728b64ba9f1d17a49d8b80257e(
    *,
    ai_agent_id: typing.Optional[builtins.str] = None,
    assistant_id: typing.Optional[builtins.str] = None,
    modified_time_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f816ae07085b54433b3b755de67e1bf15e0b82493509ed8e5356b68cc0992043(
    props: typing.Union[CfnAIAgentVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfa90b8a2e726e25113cfae6d3392d047fe0c3e278dd3c85045a47880324b32d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4d9b5597e370c198e462b17060126b5e455170e4e77fd2c15d938531a35120(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2ecd494593bfb75be5ba578ec9a97ef09eaac58369015f5c987ba265b85ce3(
    *,
    assistant_id: typing.Optional[builtins.str] = None,
    blocked_input_messaging: typing.Optional[builtins.str] = None,
    blocked_outputs_messaging: typing.Optional[builtins.str] = None,
    content_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.AIGuardrailContentPolicyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contextual_grounding_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.AIGuardrailContextualGroundingPolicyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sensitive_information_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.AIGuardrailSensitiveInformationPolicyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    topic_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.AIGuardrailTopicPolicyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    word_policy_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.AIGuardrailWordPolicyConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7f3a7b018e37e12bd0f97f7d763c9aa3246c6a2f9bac53a3406ff3fe4f1037(
    props: typing.Union[CfnAIGuardrailMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966bfef618026193f80825121659fb5740fa44eae7ab08440ecc36812bf75c64(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb2aa24a9ef6717102b82330b125e4a6657eb7a6aa674696f6cdca7bcfccf915(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e025a44b044b97d8f0b16ef1436d3183fa791bb4f8fb20e36f8cc97ffa1c6f60(
    *,
    filters_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailContentFilterConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deed4e8b272406bae1be463e4fb05093bad17abe64f3f22275ab09d670dab1e2(
    *,
    filters_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailContextualGroundingFilterConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e6bc70fbe536546c27bcb82d73edb87b728b473681e921d79e17826b7e1e0c4(
    *,
    pii_entities_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailPiiEntityConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    regexes_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailRegexConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__512aa48ed4f90c3fbbbef2a13aad28514e0a03f7f53a747b190d15c012eb2dce(
    *,
    topics_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailTopicConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398383d201eb7a0ef5b7a8bdcd59fc1c056802de729057444d300074b44c96ab(
    *,
    managed_word_lists_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailManagedWordsConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    words_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIGuardrailPropsMixin.GuardrailWordConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a34bddba69dba5f8224859c6092c4855fac8112a35c05e0204438fc8f00a4f(
    *,
    input_strength: typing.Optional[builtins.str] = None,
    output_strength: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2e308a2e55bab2e081d98869fe0d3fbd159f6460d1b78d04b0a3405b6945f3(
    *,
    threshold: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f4d2eae5667fc6c4538e20fe93434b222dc24b9866bf19a49bb82e6bb37e30(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb3cfb203a72b86af357dc07551c59adc3b80c472f1f53458a3604bdbf36d6d(
    *,
    action: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7edfaf74f192951df230992e86113616049bf65ea4b73d0d775fa17cd4fc80(
    *,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c315c0639181a1ebf861cfeac750fd0e178659c01ec60a92a1e4cbf03daca4fc(
    *,
    definition: typing.Optional[builtins.str] = None,
    examples: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c87c11f88f405f9143136932dbe869839acbb63263f7aca8c6d4e1da8f004a(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ab20783a9c0493742d1fd3adf2afca85ff24b6994f3bf846be20250bc8a850(
    *,
    ai_guardrail_id: typing.Optional[builtins.str] = None,
    assistant_id: typing.Optional[builtins.str] = None,
    modified_time_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f248bf7e3973d2b331526981ddaecb4121c538cbd2fb07f367a155f435b25fc9(
    props: typing.Union[CfnAIGuardrailVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7610cc47ffb85b2bcb7891cce617a032a5299f368aff6dcbfb721bd7fe41c5ce(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a1335ba2446f8e62a795cb087448c47cbb061dd1f2adc07e0c3095c168bbba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13025093ae01c51eaadc6032480b41018dae255bb2f7df83ce0511d7f96e610(
    *,
    api_format: typing.Optional[builtins.str] = None,
    assistant_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    model_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIPromptPropsMixin.AIPromptTemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_type: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4895b89a13c58c1f08d274defe2ceeb2fd73449fb8b9b124aa8667aadd1b8a08(
    props: typing.Union[CfnAIPromptMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59140de25182a23cf66948116bbc193ebd3469c5d69ca78c3f71b566b68e3892(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5838c0582a13143c7cacff4cce65602b54c027ac2dad12a7ae0edd24f742e1ac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74af076bc67e0f4c9544fbc580371ec775e456ff4f085993a7093ab5a3093022(
    *,
    text_full_ai_prompt_edit_template_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAIPromptPropsMixin.TextFullAIPromptEditTemplateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88371ccae1f83823f5ca63e969c4fa27fff33dbaa2b3b8a5f5b4396eb1d5258(
    *,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__695f52af8d0bbc6a87cbf2604f5fdb96b6eefa7c9b4345bf2083f6628281f888(
    *,
    ai_prompt_id: typing.Optional[builtins.str] = None,
    assistant_id: typing.Optional[builtins.str] = None,
    modified_time_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6625a81343e258f3725ebabcc5137e46c29b17564c0697d16e5f095898bb4e1e(
    props: typing.Union[CfnAIPromptVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4b16a131fd4636e6f3526c3df2a2954410c107c60d4bc2def2fb8559d18524c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560153980f2a4daf95c73f03f75bc6b273d933102adb5df23a9f1ac57adbdb4a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa55980f006d13bf393a8acffe522cd23dc4d731bae129d17bee6404d0c72de8(
    *,
    assistant_id: typing.Optional[builtins.str] = None,
    association: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssistantAssociationPropsMixin.AssociationDataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    association_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7ac832a83cd6d5854f7f1e9cd388ffa98061c8bd33537f27ee3d08025fcd8c(
    props: typing.Union[CfnAssistantAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27b269f107dccc64302163bbb5520aabccdd89fbf4677d377300b6e5c1226e8a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1fb247a57610b3873b7f7da67e55476e57e3bf81c42434d41806cf6bcbc7de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a3a3b65037c6ca0957b6bdb456a8c495921f516ce689c810b6ec0ffcab777c(
    *,
    knowledge_base_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be1ec0cdb72cb1c75dd57fb48a570af82b8a72a1550eda9d8873197f890ad0d(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edce08554f08839ee68a5f2d43c3e32707efd6317fb88d0d35b7752eb2003445(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a28785ffe00f875cd2df2705cf80706365f5ebd09b9b4e6dff83a576301ae7(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0449472693d2fbe600e1725f76b4c3af145009e8dd010b158349d45c42fd265f(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd6722602a152a3fc5db4dc9fada43780ef6612cb7661007d0ae6e427d69934(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6498dd1e57078422137442bb580110f368407a455ff4d9ed5e6b8e3f5e476113(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d030372bc6874e27a3de1a443c868e39a336c235578537759fece591f20feef(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssistantPropsMixin.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9bfcded539e1ea116eaa36e3f36e946aa1a73bfb13930d05ced7e84577827f(
    props: typing.Union[CfnAssistantMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5453798ee90507207b057c393a4cccb14bc8393da5fda4255038527ac7bc9c7a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db984015f82ad62a20a72e3537d98d15b5a9f7f02e002177d291857b57e3e726(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afee51dc1a5efef9ad6f836c1f3b6a9cdbda4341934d497e3232793d13e21baa(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de922f4b9249ae8835b37c47e237d5247070849e80461bb75c13311d6e472b59(
    *,
    description: typing.Optional[builtins.str] = None,
    knowledge_base_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rendering_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.RenderingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    server_side_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.ServerSideEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vector_ingestion_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.VectorIngestionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619ec8f23c86516960ab44ab2201ceef808a6a3a6758c18ae4f0f48674f758b6(
    props: typing.Union[CfnKnowledgeBaseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151163af4b0ed0d10b679c10b0f8766b1b3255d7097d8cd83457ad013830bfe7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e129aa530eb0d4a3a5285f3c1c9006603fe2270efbc1c7fa66d1b7c595031b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e0caeefd5d44386afccb22e80e424d6b71cf4ced5cbfcc32d49ce886920d9d(
    *,
    app_integration_arn: typing.Optional[builtins.str] = None,
    object_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e488d5587e9215556f7d5d9562e3b54e563d560bff8bd15a8b632b3ad10d3e2(
    *,
    model_arn: typing.Optional[builtins.str] = None,
    parsing_prompt: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.ParsingPromptProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__179292bc2f780cbf1aef6ed2c84970e7b5b36ef2589b2526c36c32c3dde2bdf6(
    *,
    chunking_strategy: typing.Optional[builtins.str] = None,
    fixed_size_chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.FixedSizeChunkingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hierarchical_chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.HierarchicalChunkingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    semantic_chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.SemanticChunkingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eacd125b12d2428b3d9c6d96aa3a05d54a181b79e3a9c08947c68225ba98b63(
    *,
    rate_limit: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a317c1896ed5b4542bc70ecef7cce89e7f61e963a89c916f7b26d16a1bb4bd(
    *,
    max_tokens: typing.Optional[jsii.Number] = None,
    overlap_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8dfc4c4ba20e0ddb053e60a31acb5bae6b665a26b9e2864edf8952f1ee0fda(
    *,
    level_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.HierarchicalChunkingLevelConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    overlap_tokens: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76782e28d9c187515b28993698ed69ec43f20e313e2d5ffa0a21220778cd80bc(
    *,
    max_tokens: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d409af7754eb47e2a3c0d015e9e8f9cbdb9820ece41294f0ae60d158912a8ff(
    *,
    web_crawler_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.WebCrawlerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70cb11f4bfe6dcc2c017891a334a1a2348d5f6377abb14f2f91a4947a6721a12(
    *,
    bedrock_foundation_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.BedrockFoundationModelConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parsing_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acab42a3a6651a64995b633044b635e016f92123852fe8a8fa1cd406d9de8e17(
    *,
    parsing_prompt_text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b305b837d4bd6dd7ca216138425ea64208842f56272971afe594a40e3eb4bf1(
    *,
    template_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eef69ab233a26e6764c5f6d6fb441e58fb474196659096b6a6abd1b7fa7766a0(
    *,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f389a536a85a3ed9a7451d4a5105d157c2db551930323b3f06d9456a7f9bd5(
    *,
    breakpoint_percentile_threshold: typing.Optional[jsii.Number] = None,
    buffer_size: typing.Optional[jsii.Number] = None,
    max_tokens: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b6fe90a3247fbfaa5a89bb8d739366f41a8158bfacd41d10371accad6ab40b(
    *,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16087d6dbdd25e2798b001c30fc92247bb6815f50dbd9a886975b14e1eb20ef1(
    *,
    app_integrations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.AppIntegrationsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_source_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.ManagedSourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b77cac5eabd9968767a656c4b6c14d06465e97593f2f0e257735ede41919f57c(
    *,
    seed_urls: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.SeedUrlProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e16629e5e37798600ed3f07d5b61e05f80db64a941c1a6da649f3f550870ebcb(
    *,
    chunking_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.ChunkingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parsing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.ParsingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a13cb912ac7eb05b27e9b64fc92108cc692ee3ccfd54038007b4db5dabbe350(
    *,
    crawler_limits: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.CrawlerLimitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclusion_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    inclusion_filters: typing.Optional[typing.Sequence[builtins.str]] = None,
    scope: typing.Optional[builtins.str] = None,
    url_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKnowledgeBasePropsMixin.UrlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca5cc8f9fb58c60c4f731bb247c19bacb7b5531779a428d32fff6f8dac9ad339(
    *,
    channel_subtype: typing.Optional[builtins.str] = None,
    content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.ContentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.MessageTemplateAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    grouping_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.GroupingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    knowledge_base_arn: typing.Optional[builtins.str] = None,
    language: typing.Optional[builtins.str] = None,
    message_template_attachments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.MessageTemplateAttachmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf9c7969afab71d8a654334bfe0759b801afc30b3b743ef7ac7981846d8a965(
    props: typing.Union[CfnMessageTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f1ae760591b49c23ca9546cb15e6d5454423827b3ab9911e9004be38e35224(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb197805db30033184669fd80b6244da39cfd0cbb101543225b07455bd2f4ae8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc7ec0f569df73abac0d8bb23135caec52bd8de0fd9b7c12f9cfde699dbbfabe(
    *,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2015e27291cff0949e9993ebeac12cb053b2e02c763a1fb217ecc4ece19e06(
    *,
    email_message_template_content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.EmailMessageTemplateContentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sms_message_template_content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.SmsMessageTemplateContentProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5def9c96428c19124b9dc756e3fbd86cf649620bf10aa947bb8c62492dad405e(
    *,
    account_number: typing.Optional[builtins.str] = None,
    additional_information: typing.Optional[builtins.str] = None,
    address1: typing.Optional[builtins.str] = None,
    address2: typing.Optional[builtins.str] = None,
    address3: typing.Optional[builtins.str] = None,
    address4: typing.Optional[builtins.str] = None,
    billing_address1: typing.Optional[builtins.str] = None,
    billing_address2: typing.Optional[builtins.str] = None,
    billing_address3: typing.Optional[builtins.str] = None,
    billing_address4: typing.Optional[builtins.str] = None,
    billing_city: typing.Optional[builtins.str] = None,
    billing_country: typing.Optional[builtins.str] = None,
    billing_county: typing.Optional[builtins.str] = None,
    billing_postal_code: typing.Optional[builtins.str] = None,
    billing_province: typing.Optional[builtins.str] = None,
    billing_state: typing.Optional[builtins.str] = None,
    birth_date: typing.Optional[builtins.str] = None,
    business_email_address: typing.Optional[builtins.str] = None,
    business_name: typing.Optional[builtins.str] = None,
    business_phone_number: typing.Optional[builtins.str] = None,
    city: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    county: typing.Optional[builtins.str] = None,
    custom: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    email_address: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    gender: typing.Optional[builtins.str] = None,
    home_phone_number: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mailing_address1: typing.Optional[builtins.str] = None,
    mailing_address2: typing.Optional[builtins.str] = None,
    mailing_address3: typing.Optional[builtins.str] = None,
    mailing_address4: typing.Optional[builtins.str] = None,
    mailing_city: typing.Optional[builtins.str] = None,
    mailing_country: typing.Optional[builtins.str] = None,
    mailing_county: typing.Optional[builtins.str] = None,
    mailing_postal_code: typing.Optional[builtins.str] = None,
    mailing_province: typing.Optional[builtins.str] = None,
    mailing_state: typing.Optional[builtins.str] = None,
    middle_name: typing.Optional[builtins.str] = None,
    mobile_phone_number: typing.Optional[builtins.str] = None,
    party_type: typing.Optional[builtins.str] = None,
    phone_number: typing.Optional[builtins.str] = None,
    postal_code: typing.Optional[builtins.str] = None,
    profile_arn: typing.Optional[builtins.str] = None,
    profile_id: typing.Optional[builtins.str] = None,
    province: typing.Optional[builtins.str] = None,
    shipping_address1: typing.Optional[builtins.str] = None,
    shipping_address2: typing.Optional[builtins.str] = None,
    shipping_address3: typing.Optional[builtins.str] = None,
    shipping_address4: typing.Optional[builtins.str] = None,
    shipping_city: typing.Optional[builtins.str] = None,
    shipping_country: typing.Optional[builtins.str] = None,
    shipping_county: typing.Optional[builtins.str] = None,
    shipping_postal_code: typing.Optional[builtins.str] = None,
    shipping_province: typing.Optional[builtins.str] = None,
    shipping_state: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3759b1610a34d1250a9385aefae69cf3adb766dcf222ac88453a1496159b223a(
    *,
    html: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    plain_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07021687a553cf2d24315ba18ebebd31ea3a1626afae8b5082b07390c736e85(
    *,
    body: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.EmailMessageTemplateContentBodyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    headers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.EmailMessageTemplateHeaderProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5a7cfd0f890a4d7c4768f59a06f1bc006bb43eaa779f6a4ff81974b31b58b37(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b446ec188648c430386cf440e46f93f2daa522d6f80edc6f08641c4fdc9896b6(
    *,
    criteria: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d551f98b55c89688039e30c45db17cb68dc43be16655f1ea066fc32f9ced9c5e(
    *,
    attachment_id: typing.Optional[builtins.str] = None,
    attachment_name: typing.Optional[builtins.str] = None,
    s3_presigned_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daacd804b2dfc5df29232dafcac695ef660a983a95137fd9ddffaa8012434388(
    *,
    agent_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.AgentAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_attributes: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    customer_profile_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.CustomerProfileAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    system_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.SystemAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9e31b2bc5113de977be3b46fd1b53e262a02c7e8ef556ecb83a4f93e4b6be5b(
    *,
    content: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22d5828a366b37644966b825565122702001c59f720987e9b4932194d9816b25(
    *,
    plain_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.MessageTemplateBodyContentProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c56959e3976d7c4090a139e10926571b72c8cf561d75766fe484fc454ec9ce45(
    *,
    body: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.SmsMessageTemplateContentBodyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4174e68c69a55ec116e385974805e1c54d815193b1bb15712cf044322353713e(
    *,
    customer_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    system_endpoint: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMessageTemplatePropsMixin.SystemEndpointAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c403c6a1d2544b9cfb108e7fae7a445ec1e59be5ca2d61a361c758554af9bcf3(
    *,
    address: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b51e1ed0e829bf59b1cbb6e52b262888c172c26342bbb8aad63a2bfc61cb7e8(
    *,
    message_template_arn: typing.Optional[builtins.str] = None,
    message_template_content_sha256: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d981415698ad531878ebaf57bc4eab3da64c894c52446d31a6afc6918462407(
    props: typing.Union[CfnMessageTemplateVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa7e89a99300890342ea43ea73e610271eb03746056ffdc0b5efe0351fa33e5e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637b99296c836e71fd0795e401c6ddccaddf2a14b38993cde924a149f015951a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dda0347dd3466e0ca54808c6c24756ad430900c9056013b35f5cd4e78bc88635(
    *,
    channels: typing.Optional[typing.Sequence[builtins.str]] = None,
    content: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    content_type: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    grouping_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickResponsePropsMixin.GroupingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    is_active: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    knowledge_base_arn: typing.Optional[builtins.str] = None,
    language: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    shortcut_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__568b4ecb16fb2ee7d9836d777588301e1dae5606a27dd03788ebc3d6c13c838b(
    props: typing.Union[CfnQuickResponseMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5403d7d3567e281ebb56eba8426d8da4cb58511ade49a3edaf7e22ece4b76ef2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00b57ab6f8d5268387cb6845cc5bb41adf4819ad9bc0ab659ca9016773bf983(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f9551fb1307f7cddf8b5eed789c9d9ff3a051a8c19acd715ed7a9c24dc0b0e(
    *,
    criteria: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3cd1c6db8b6ee2df25169811e91f8e5ea0f74334721c5f77ecb076c5ce2e452(
    *,
    content: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4223c662ae0c9aa89e49519337a72e1cf6405cd56505c95c66aecc32e62ba5(
    *,
    markdown: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    plain_text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickResponsePropsMixin.QuickResponseContentProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
