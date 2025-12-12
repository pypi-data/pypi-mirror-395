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
    jsii_type="@aws-cdk/mixins-preview.aws_aiops.mixins.CfnInvestigationGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "chatbot_notification_channels": "chatbotNotificationChannels",
        "cross_account_configurations": "crossAccountConfigurations",
        "encryption_config": "encryptionConfig",
        "investigation_group_policy": "investigationGroupPolicy",
        "is_cloud_trail_event_history_enabled": "isCloudTrailEventHistoryEnabled",
        "name": "name",
        "retention_in_days": "retentionInDays",
        "role_arn": "roleArn",
        "tag_key_boundaries": "tagKeyBoundaries",
        "tags": "tags",
    },
)
class CfnInvestigationGroupMixinProps:
    def __init__(
        self,
        *,
        chatbot_notification_channels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        cross_account_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        investigation_group_policy: typing.Optional[builtins.str] = None,
        is_cloud_trail_event_history_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        retention_in_days: typing.Optional[jsii.Number] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tag_key_boundaries: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInvestigationGroupPropsMixin.

        :param chatbot_notification_channels: Use this property to integrate CloudWatch investigations with chat applications. This property is an array. For the first string, specify the ARN of an Amazon topic. For the array of strings, specify the ARNs of one or more chat applications configurations that you want to associate with that topic. For more information about these configuration ARNs, see `Getting started with Amazon Q in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/getting-started.html>`_ and `Resource type defined by AWS Chatbot <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awschatbot.html#awschatbot-resources-for-iam-policies>`_ .
        :param cross_account_configurations: List of ``sourceRoleArn`` values that have been configured for cross-account access.
        :param encryption_config: Specifies the customer managed AWS key that the investigation group uses to encrypt data, if there is one. If not, the investigation group uses an AWS key to encrypt the data.
        :param investigation_group_policy: Returns the JSON of the IAM resource policy associated with the specified investigation group in a string. For example, ``{\\"Version\\":\\"2012-10-17\\",\\"Statement\\":[{\\"Effect\\":\\"Allow\\",\\"Principal\\":{\\"Service\\":\\"aiops.alarms.cloudwatch.amazonaws.com\\"},\\"Action\\":[\\"aiops:CreateInvestigation\\",\\"aiops:CreateInvestigationEvent\\"],\\"Resource\\":\\"*\\",\\"Condition\\":{\\"StringEquals\\":{\\"aws:SourceAccount\\":\\"111122223333\\"},\\"ArnLike\\":{\\"aws:SourceArn\\":\\"arn:aws:cloudwatch:us-east-1:111122223333:alarm:*\\"}}}]}`` .
        :param is_cloud_trail_event_history_enabled: Specify ``true`` to enable CloudWatch investigations to have access to change events that are recorded by CloudTrail. The default is ``true`` .
        :param name: Specify either the name or the ARN of the investigation group that you want to view. This is used to set the name of the investigation group.
        :param retention_in_days: Specifies how long that investigation data is kept.
        :param role_arn: The ARN of the IAM role that the investigation group uses for permissions to gather data.
        :param tag_key_boundaries: Displays the custom tag keys for custom applications in your system that you have specified in the investigation group. Resource tags help CloudWatch investigations narrow the search space when it is unable to discover definite relationships between resources.
        :param tags: The list of key-value pairs to associate with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_aiops import mixins as aiops_mixins
            
            cfn_investigation_group_mixin_props = aiops_mixins.CfnInvestigationGroupMixinProps(
                chatbot_notification_channels=[aiops_mixins.CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty(
                    chat_configuration_arns=["chatConfigurationArns"],
                    sns_topic_arn="snsTopicArn"
                )],
                cross_account_configurations=[aiops_mixins.CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty(
                    source_role_arn="sourceRoleArn"
                )],
                encryption_config=aiops_mixins.CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty(
                    encryption_configuration_type="encryptionConfigurationType",
                    kms_key_id="kmsKeyId"
                ),
                investigation_group_policy="investigationGroupPolicy",
                is_cloud_trail_event_history_enabled=False,
                name="name",
                retention_in_days=123,
                role_arn="roleArn",
                tag_key_boundaries=["tagKeyBoundaries"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87116b543371f70caddfe1753413e686922f86adb67b4beec505066909f16f14)
            check_type(argname="argument chatbot_notification_channels", value=chatbot_notification_channels, expected_type=type_hints["chatbot_notification_channels"])
            check_type(argname="argument cross_account_configurations", value=cross_account_configurations, expected_type=type_hints["cross_account_configurations"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument investigation_group_policy", value=investigation_group_policy, expected_type=type_hints["investigation_group_policy"])
            check_type(argname="argument is_cloud_trail_event_history_enabled", value=is_cloud_trail_event_history_enabled, expected_type=type_hints["is_cloud_trail_event_history_enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument retention_in_days", value=retention_in_days, expected_type=type_hints["retention_in_days"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tag_key_boundaries", value=tag_key_boundaries, expected_type=type_hints["tag_key_boundaries"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if chatbot_notification_channels is not None:
            self._values["chatbot_notification_channels"] = chatbot_notification_channels
        if cross_account_configurations is not None:
            self._values["cross_account_configurations"] = cross_account_configurations
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if investigation_group_policy is not None:
            self._values["investigation_group_policy"] = investigation_group_policy
        if is_cloud_trail_event_history_enabled is not None:
            self._values["is_cloud_trail_event_history_enabled"] = is_cloud_trail_event_history_enabled
        if name is not None:
            self._values["name"] = name
        if retention_in_days is not None:
            self._values["retention_in_days"] = retention_in_days
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tag_key_boundaries is not None:
            self._values["tag_key_boundaries"] = tag_key_boundaries
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def chatbot_notification_channels(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty"]]]]:
        '''Use this property to integrate CloudWatch investigations with chat applications.

        This property is an array. For the first string, specify the ARN of an Amazon  topic. For the array of strings, specify the ARNs of one or more chat applications configurations that you want to associate with that topic. For more information about these configuration ARNs, see `Getting started with Amazon Q in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/getting-started.html>`_ and `Resource type defined by AWS Chatbot <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awschatbot.html#awschatbot-resources-for-iam-policies>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-chatbotnotificationchannels
        '''
        result = self._values.get("chatbot_notification_channels")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty"]]]], result)

    @builtins.property
    def cross_account_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty"]]]]:
        '''List of ``sourceRoleArn`` values that have been configured for cross-account access.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-crossaccountconfigurations
        '''
        result = self._values.get("cross_account_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty"]]]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty"]]:
        '''Specifies the customer managed AWS  key that the investigation group uses to encrypt data, if there is one.

        If not, the investigation group uses an AWS key to encrypt the data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-encryptionconfig
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty"]], result)

    @builtins.property
    def investigation_group_policy(self) -> typing.Optional[builtins.str]:
        '''Returns the JSON of the IAM resource policy associated with the specified investigation group in a string.

        For example, ``{\\"Version\\":\\"2012-10-17\\",\\"Statement\\":[{\\"Effect\\":\\"Allow\\",\\"Principal\\":{\\"Service\\":\\"aiops.alarms.cloudwatch.amazonaws.com\\"},\\"Action\\":[\\"aiops:CreateInvestigation\\",\\"aiops:CreateInvestigationEvent\\"],\\"Resource\\":\\"*\\",\\"Condition\\":{\\"StringEquals\\":{\\"aws:SourceAccount\\":\\"111122223333\\"},\\"ArnLike\\":{\\"aws:SourceArn\\":\\"arn:aws:cloudwatch:us-east-1:111122223333:alarm:*\\"}}}]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-investigationgrouppolicy
        '''
        result = self._values.get("investigation_group_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_cloud_trail_event_history_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specify ``true`` to enable CloudWatch investigations to have access to change events that are recorded by CloudTrail.

        The default is ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-iscloudtraileventhistoryenabled
        '''
        result = self._values.get("is_cloud_trail_event_history_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Specify either the name or the ARN of the investigation group that you want to view.

        This is used to set the name of the investigation group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retention_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies how long that investigation data is kept.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-retentionindays
        '''
        result = self._values.get("retention_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that the investigation group uses for permissions to gather data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_key_boundaries(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Displays the custom tag keys for custom applications in your system that you have specified in the investigation group.

        Resource tags help CloudWatch investigations narrow the search space when it is unable to discover definite relationships between resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-tagkeyboundaries
        '''
        result = self._values.get("tag_key_boundaries")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value pairs to associate with the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html#cfn-aiops-investigationgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInvestigationGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInvestigationGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_aiops.mixins.CfnInvestigationGroupPropsMixin",
):
    '''Creates an *investigation group* in your account.

    Creating an investigation group is a one-time setup task for each Region in your account. It is a necessary task to be able to perform investigations.

    Settings in the investigation group help you centrally manage the common properties of your investigations, such as the following:

    - Who can access the investigations
    - Whether investigation data is encrypted with a customer managed AWS Key Management Service key.
    - How long investigations and their data are retained by default.

    Currently, you can have one investigation group in each Region in your account. Each investigation in a Region is a part of the investigation group in that Region

    To create an investigation group and set up CloudWatch investigations, you must be signed in to an IAM principal that has either the ``AIOpsConsoleAdminPolicy`` or the ``AdministratorAccess`` IAM policy attached, or to an account that has similar permissions.
    .. epigraph::

       You can configure CloudWatch alarms to start investigations and add events to investigations. If you create your investigation group with ``CreateInvestigationGroup`` and you want to enable alarms to do this, you must use ``PutInvestigationGroupPolicy`` to create a resource policy that grants this permission to CloudWatch alarms.

       For more information about configuring CloudWatch alarms, see `Using Amazon CloudWatch alarms <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-aiops-investigationgroup.html
    :cloudformationResource: AWS::AIOps::InvestigationGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_aiops import mixins as aiops_mixins
        
        cfn_investigation_group_props_mixin = aiops_mixins.CfnInvestigationGroupPropsMixin(aiops_mixins.CfnInvestigationGroupMixinProps(
            chatbot_notification_channels=[aiops_mixins.CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty(
                chat_configuration_arns=["chatConfigurationArns"],
                sns_topic_arn="snsTopicArn"
            )],
            cross_account_configurations=[aiops_mixins.CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty(
                source_role_arn="sourceRoleArn"
            )],
            encryption_config=aiops_mixins.CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty(
                encryption_configuration_type="encryptionConfigurationType",
                kms_key_id="kmsKeyId"
            ),
            investigation_group_policy="investigationGroupPolicy",
            is_cloud_trail_event_history_enabled=False,
            name="name",
            retention_in_days=123,
            role_arn="roleArn",
            tag_key_boundaries=["tagKeyBoundaries"],
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
        props: typing.Union[CfnInvestigationGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::AIOps::InvestigationGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c2cc4550a49cde8a60cd94b44b5047484b7dddac04aefda5638a5719a86b58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3aae608d6314f765274f14a48a9816bc78947b8785abf287ff664923063890c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fca22944a66b39d398ef261dea4ab080cadc850e061d08f31da977196ee89c8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInvestigationGroupMixinProps:
        return typing.cast(CfnInvestigationGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aiops.mixins.CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "chat_configuration_arns": "chatConfigurationArns",
            "sns_topic_arn": "snsTopicArn",
        },
    )
    class ChatbotNotificationChannelProperty:
        def __init__(
            self,
            *,
            chat_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            sns_topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure to integrate CloudWatch investigations with chat applications.

            This structure is a string array. For the first string, specify the ARN of an Amazon SNS topic. For the array of strings, specify the ARNs of one or more chat applications configurations that you want to associate with that topic. For more information about these configuration ARNs, see `Getting started with Amazon Q in chat applications <https://docs.aws.amazon.com/chatbot/latest/adminguide/getting-started.html>`_ and `Resource type defined by AWS Chatbot <https://docs.aws.amazon.com/service-authorization/latest/reference/list_awschatbot.html#awschatbot-resources-for-iam-policies>`_ .

            :param chat_configuration_arns: Returns the Amazon Resource Name (ARN) of any third-party chat integrations configured for the account.
            :param sns_topic_arn: Returns the ARN of an Amazon topic used for third-party chat integrations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-chatbotnotificationchannel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aiops import mixins as aiops_mixins
                
                chatbot_notification_channel_property = aiops_mixins.CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty(
                    chat_configuration_arns=["chatConfigurationArns"],
                    sns_topic_arn="snsTopicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8e09c2953ede8ad4aba9e5a992c931e6e106e82b0d5993fea78814d1d95760a)
                check_type(argname="argument chat_configuration_arns", value=chat_configuration_arns, expected_type=type_hints["chat_configuration_arns"])
                check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if chat_configuration_arns is not None:
                self._values["chat_configuration_arns"] = chat_configuration_arns
            if sns_topic_arn is not None:
                self._values["sns_topic_arn"] = sns_topic_arn

        @builtins.property
        def chat_configuration_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Returns the Amazon Resource Name (ARN) of any third-party chat integrations configured for the account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-chatbotnotificationchannel.html#cfn-aiops-investigationgroup-chatbotnotificationchannel-chatconfigurationarns
            '''
            result = self._values.get("chat_configuration_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def sns_topic_arn(self) -> typing.Optional[builtins.str]:
            '''Returns the ARN of an Amazon  topic used for third-party chat integrations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-chatbotnotificationchannel.html#cfn-aiops-investigationgroup-chatbotnotificationchannel-snstopicarn
            '''
            result = self._values.get("sns_topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChatbotNotificationChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aiops.mixins.CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"source_role_arn": "sourceRoleArn"},
    )
    class CrossAccountConfigurationProperty:
        def __init__(
            self,
            *,
            source_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This structure contains information about the cross-account configuration in the account.

            :param source_role_arn: The ARN of an existing role which will be used to do investigations on your behalf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-crossaccountconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aiops import mixins as aiops_mixins
                
                cross_account_configuration_property = aiops_mixins.CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty(
                    source_role_arn="sourceRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4ab5a74ae0ee5e84d535a965536a0a039cbd3f0f22326b019c5c1767e994fa76)
                check_type(argname="argument source_role_arn", value=source_role_arn, expected_type=type_hints["source_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_role_arn is not None:
                self._values["source_role_arn"] = source_role_arn

        @builtins.property
        def source_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of an existing role which will be used to do investigations on your behalf.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-crossaccountconfiguration.html#cfn-aiops-investigationgroup-crossaccountconfiguration-sourcerolearn
            '''
            result = self._values.get("source_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossAccountConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_aiops.mixins.CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_configuration_type": "encryptionConfigurationType",
            "kms_key_id": "kmsKeyId",
        },
    )
    class EncryptionConfigMapProperty:
        def __init__(
            self,
            *,
            encryption_configuration_type: typing.Optional[builtins.str] = None,
            kms_key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use this structure if you want to use a customer managed AWS  key to encrypt your investigation data.

            If you omit this parameter, CloudWatch investigations will use an AWS key to encrypt the data. For more information, see `Encryption of investigation data <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Investigations-Security.html#Investigations-KMS>`_ .

            :param encryption_configuration_type: Displays whether investigation data is encrypted by a customer managed key or an AWS owned key.
            :param kms_key_id: If the investigation group uses a customer managed key for encryption, this field displays the ID of that key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-encryptionconfigmap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_aiops import mixins as aiops_mixins
                
                encryption_config_map_property = aiops_mixins.CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty(
                    encryption_configuration_type="encryptionConfigurationType",
                    kms_key_id="kmsKeyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f88010ad2a79ce6665c2c876f626b87af979591273bd38ff3e33fc3c1d489c1a)
                check_type(argname="argument encryption_configuration_type", value=encryption_configuration_type, expected_type=type_hints["encryption_configuration_type"])
                check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_configuration_type is not None:
                self._values["encryption_configuration_type"] = encryption_configuration_type
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def encryption_configuration_type(self) -> typing.Optional[builtins.str]:
            '''Displays whether investigation data is encrypted by a customer managed key or an AWS owned key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-encryptionconfigmap.html#cfn-aiops-investigationgroup-encryptionconfigmap-encryptionconfigurationtype
            '''
            result = self._values.get("encryption_configuration_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''If the investigation group uses a customer managed key for encryption, this field displays the ID of that key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-aiops-investigationgroup-encryptionconfigmap.html#cfn-aiops-investigationgroup-encryptionconfigmap-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnInvestigationGroupMixinProps",
    "CfnInvestigationGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__87116b543371f70caddfe1753413e686922f86adb67b4beec505066909f16f14(
    *,
    chatbot_notification_channels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInvestigationGroupPropsMixin.ChatbotNotificationChannelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cross_account_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInvestigationGroupPropsMixin.CrossAccountConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInvestigationGroupPropsMixin.EncryptionConfigMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    investigation_group_policy: typing.Optional[builtins.str] = None,
    is_cloud_trail_event_history_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    retention_in_days: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tag_key_boundaries: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c2cc4550a49cde8a60cd94b44b5047484b7dddac04aefda5638a5719a86b58(
    props: typing.Union[CfnInvestigationGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aae608d6314f765274f14a48a9816bc78947b8785abf287ff664923063890c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fca22944a66b39d398ef261dea4ab080cadc850e061d08f31da977196ee89c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e09c2953ede8ad4aba9e5a992c931e6e106e82b0d5993fea78814d1d95760a(
    *,
    chat_configuration_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    sns_topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab5a74ae0ee5e84d535a965536a0a039cbd3f0f22326b019c5c1767e994fa76(
    *,
    source_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88010ad2a79ce6665c2c876f626b87af979591273bd38ff3e33fc3c1d489c1a(
    *,
    encryption_configuration_type: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
