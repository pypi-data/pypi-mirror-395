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
    jsii_type="@aws-cdk/mixins-preview.aws_supportapp.mixins.CfnAccountAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={"account_alias": "accountAlias"},
)
class CfnAccountAliasMixinProps:
    def __init__(self, *, account_alias: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnAccountAliasPropsMixin.

        :param account_alias: An alias or short name for an AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_supportapp import mixins as supportapp_mixins
            
            cfn_account_alias_mixin_props = supportapp_mixins.CfnAccountAliasMixinProps(
                account_alias="accountAlias"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b13f8b90dadedca8d4d5c924f534428287dbd5b85d7a88877cfa6502d3604be)
            check_type(argname="argument account_alias", value=account_alias, expected_type=type_hints["account_alias"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_alias is not None:
            self._values["account_alias"] = account_alias

    @builtins.property
    def account_alias(self) -> typing.Optional[builtins.str]:
        '''An alias or short name for an AWS account .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html#cfn-supportapp-accountalias-accountalias
        '''
        result = self._values.get("account_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccountAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_supportapp.mixins.CfnAccountAliasPropsMixin",
):
    '''You can use the ``AWS::SupportApp::AccountAlias`` resource to specify your AWS account when you configure the AWS Support App in Slack.

    Your alias name appears on the AWS Support App page in the Support Center Console and in messages from the  App. You can use this alias to identify the account you've configured with the AWS Support App .

    For more information, see `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_ in the *User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-accountalias.html
    :cloudformationResource: AWS::SupportApp::AccountAlias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_supportapp import mixins as supportapp_mixins
        
        cfn_account_alias_props_mixin = supportapp_mixins.CfnAccountAliasPropsMixin(supportapp_mixins.CfnAccountAliasMixinProps(
            account_alias="accountAlias"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccountAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SupportApp::AccountAlias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fa3548c0ec6459513439fb1838837a31c32da1fc090852cb0312c8ae0421257)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7789b1b62c61dea6b5134059668568708bcca6a46291cddd8139462b00b8b0d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc30c2f37196691ed917b3a166c7cf8307b0bc02519417d814adffd329226e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccountAliasMixinProps:
        return typing.cast(CfnAccountAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_supportapp.mixins.CfnSlackChannelConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_id": "channelId",
        "channel_name": "channelName",
        "channel_role_arn": "channelRoleArn",
        "notify_on_add_correspondence_to_case": "notifyOnAddCorrespondenceToCase",
        "notify_on_case_severity": "notifyOnCaseSeverity",
        "notify_on_create_or_reopen_case": "notifyOnCreateOrReopenCase",
        "notify_on_resolve_case": "notifyOnResolveCase",
        "team_id": "teamId",
    },
)
class CfnSlackChannelConfigurationMixinProps:
    def __init__(
        self,
        *,
        channel_id: typing.Optional[builtins.str] = None,
        channel_name: typing.Optional[builtins.str] = None,
        channel_role_arn: typing.Optional[builtins.str] = None,
        notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        notify_on_case_severity: typing.Optional[builtins.str] = None,
        notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        team_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSlackChannelConfigurationPropsMixin.

        :param channel_id: The channel ID in Slack. This ID identifies a channel within a Slack workspace.
        :param channel_name: The channel name in Slack. This is the channel where you invite the AWS Support App .
        :param channel_role_arn: The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration. The App uses this role to perform and Service Quotas actions on your behalf.
        :param notify_on_add_correspondence_to_case: Whether to get notified when a correspondence is added to your support cases.
        :param notify_on_case_severity: The case severity for your support cases that you want to receive notifications. You can specify ``none`` , ``all`` , or ``high`` .
        :param notify_on_create_or_reopen_case: Whether to get notified when your support cases are created or reopened.
        :param notify_on_resolve_case: Whether to get notified when your support cases are resolved.
        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_supportapp import mixins as supportapp_mixins
            
            cfn_slack_channel_configuration_mixin_props = supportapp_mixins.CfnSlackChannelConfigurationMixinProps(
                channel_id="channelId",
                channel_name="channelName",
                channel_role_arn="channelRoleArn",
                notify_on_add_correspondence_to_case=False,
                notify_on_case_severity="notifyOnCaseSeverity",
                notify_on_create_or_reopen_case=False,
                notify_on_resolve_case=False,
                team_id="teamId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75676dc90b63246c8e93769f33ec8ddf495f42bc906ede1081122abd88f573ba)
            check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument channel_role_arn", value=channel_role_arn, expected_type=type_hints["channel_role_arn"])
            check_type(argname="argument notify_on_add_correspondence_to_case", value=notify_on_add_correspondence_to_case, expected_type=type_hints["notify_on_add_correspondence_to_case"])
            check_type(argname="argument notify_on_case_severity", value=notify_on_case_severity, expected_type=type_hints["notify_on_case_severity"])
            check_type(argname="argument notify_on_create_or_reopen_case", value=notify_on_create_or_reopen_case, expected_type=type_hints["notify_on_create_or_reopen_case"])
            check_type(argname="argument notify_on_resolve_case", value=notify_on_resolve_case, expected_type=type_hints["notify_on_resolve_case"])
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_id is not None:
            self._values["channel_id"] = channel_id
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if channel_role_arn is not None:
            self._values["channel_role_arn"] = channel_role_arn
        if notify_on_add_correspondence_to_case is not None:
            self._values["notify_on_add_correspondence_to_case"] = notify_on_add_correspondence_to_case
        if notify_on_case_severity is not None:
            self._values["notify_on_case_severity"] = notify_on_case_severity
        if notify_on_create_or_reopen_case is not None:
            self._values["notify_on_create_or_reopen_case"] = notify_on_create_or_reopen_case
        if notify_on_resolve_case is not None:
            self._values["notify_on_resolve_case"] = notify_on_resolve_case
        if team_id is not None:
            self._values["team_id"] = team_id

    @builtins.property
    def channel_id(self) -> typing.Optional[builtins.str]:
        '''The channel ID in Slack.

        This ID identifies a channel within a Slack workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelid
        '''
        result = self._values.get("channel_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The channel name in Slack.

        This is the channel where you invite the AWS Support App .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role for this Slack channel configuration.

        The  App uses this role to perform  and Service Quotas actions on your behalf.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-channelrolearn
        '''
        result = self._values.get("channel_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_on_add_correspondence_to_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to get notified when a correspondence is added to your support cases.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonaddcorrespondencetocase
        '''
        result = self._values.get("notify_on_add_correspondence_to_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def notify_on_case_severity(self) -> typing.Optional[builtins.str]:
        '''The case severity for your support cases that you want to receive notifications.

        You can specify ``none`` , ``all`` , or ``high`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncaseseverity
        '''
        result = self._values.get("notify_on_case_severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notify_on_create_or_reopen_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to get notified when your support cases are created or reopened.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyoncreateorreopencase
        '''
        result = self._values.get("notify_on_create_or_reopen_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def notify_on_resolve_case(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to get notified when your support cases are resolved.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-notifyonresolvecase
        '''
        result = self._values.get("notify_on_resolve_case")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html#cfn-supportapp-slackchannelconfiguration-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSlackChannelConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_supportapp.mixins.CfnSlackChannelConfigurationPropsMixin",
):
    '''You can use the ``AWS::SupportApp::SlackChannelConfiguration`` resource to specify your AWS account when you configure the AWS Support App .

    This resource includes the following information:

    - The Slack channel name and ID
    - The team ID in Slack
    - The Amazon Resource Name (ARN) of the AWS Identity and Access Management ( IAM ) role
    - Whether you want the AWS Support App to notify you when your support cases are created, updated, resolved, or reopened
    - The case severity that you want to get notified for

    For more information, see the following topics in the *User Guide* :

    - `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_
    - `Creating AWS Support App in Slack resources with AWS CloudFormation <https://docs.aws.amazon.com/awssupport/latest/user/creating-resources-with-cloudformation.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackchannelconfiguration.html
    :cloudformationResource: AWS::SupportApp::SlackChannelConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_supportapp import mixins as supportapp_mixins
        
        cfn_slack_channel_configuration_props_mixin = supportapp_mixins.CfnSlackChannelConfigurationPropsMixin(supportapp_mixins.CfnSlackChannelConfigurationMixinProps(
            channel_id="channelId",
            channel_name="channelName",
            channel_role_arn="channelRoleArn",
            notify_on_add_correspondence_to_case=False,
            notify_on_case_severity="notifyOnCaseSeverity",
            notify_on_create_or_reopen_case=False,
            notify_on_resolve_case=False,
            team_id="teamId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSlackChannelConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SupportApp::SlackChannelConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf658544fcd3ed01ed495acaa1e854ff7fd1254bcde1f24873e65742139fff47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca452ab782cfae1740620d7fbe9cdbaa8cd18c39d6f05022115babae9cb08200)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5831d0fa7837bbc6ad99f9f29508122a9b531b101590e8c9c5c52043bf2daa53)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSlackChannelConfigurationMixinProps:
        return typing.cast(CfnSlackChannelConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_supportapp.mixins.CfnSlackWorkspaceConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"team_id": "teamId", "version_id": "versionId"},
)
class CfnSlackWorkspaceConfigurationMixinProps:
    def __init__(
        self,
        *,
        team_id: typing.Optional[builtins.str] = None,
        version_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSlackWorkspaceConfigurationPropsMixin.

        :param team_id: The team ID in Slack. This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .
        :param version_id: An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_supportapp import mixins as supportapp_mixins
            
            cfn_slack_workspace_configuration_mixin_props = supportapp_mixins.CfnSlackWorkspaceConfigurationMixinProps(
                team_id="teamId",
                version_id="versionId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380b7bf6ac5691142ecf8824c6e8bf84aeea4375620e2ddfc20905f545e5c9a4)
            check_type(argname="argument team_id", value=team_id, expected_type=type_hints["team_id"])
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if team_id is not None:
            self._values["team_id"] = team_id
        if version_id is not None:
            self._values["version_id"] = version_id

    @builtins.property
    def team_id(self) -> typing.Optional[builtins.str]:
        '''The team ID in Slack.

        This ID uniquely identifies a Slack workspace, such as ``T012ABCDEFG`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-teamid
        '''
        result = self._values.get("team_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''An identifier used to update an existing Slack workspace configuration in AWS CloudFormation , such as ``100`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html#cfn-supportapp-slackworkspaceconfiguration-versionid
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackWorkspaceConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSlackWorkspaceConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_supportapp.mixins.CfnSlackWorkspaceConfigurationPropsMixin",
):
    '''You can use the ``AWS::SupportApp::SlackWorkspaceConfiguration`` resource to specify your Slack workspace configuration.

    This resource configures your AWS account so that you can use the specified Slack workspace in the AWS Support App . This resource includes the following information:

    - The team ID for the Slack workspace
    - The version ID of the resource to use with AWS CloudFormation

    For more information, see the following topics in the *User Guide* :

    - `AWS Support App in Slack <https://docs.aws.amazon.com/awssupport/latest/user/aws-support-app-for-slack.html>`_
    - `Creating AWS Support App in Slack resources with AWS CloudFormation <https://docs.aws.amazon.com/awssupport/latest/user/creating-resources-with-cloudformation.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-supportapp-slackworkspaceconfiguration.html
    :cloudformationResource: AWS::SupportApp::SlackWorkspaceConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_supportapp import mixins as supportapp_mixins
        
        cfn_slack_workspace_configuration_props_mixin = supportapp_mixins.CfnSlackWorkspaceConfigurationPropsMixin(supportapp_mixins.CfnSlackWorkspaceConfigurationMixinProps(
            team_id="teamId",
            version_id="versionId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSlackWorkspaceConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SupportApp::SlackWorkspaceConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26eaa01b4e8139e41eb91201f47c4191e7ab19d41ac620f578f1953181183ff8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0676ff9b65784538143f157dad6afd004baa66b0839519b62d34838a9490336e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4842ab4563f3db1d365c917e4ee5a206d19931b2c5e646579996dd308c48754d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSlackWorkspaceConfigurationMixinProps:
        return typing.cast(CfnSlackWorkspaceConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAccountAliasMixinProps",
    "CfnAccountAliasPropsMixin",
    "CfnSlackChannelConfigurationMixinProps",
    "CfnSlackChannelConfigurationPropsMixin",
    "CfnSlackWorkspaceConfigurationMixinProps",
    "CfnSlackWorkspaceConfigurationPropsMixin",
]

publication.publish()

def _typecheckingstub__5b13f8b90dadedca8d4d5c924f534428287dbd5b85d7a88877cfa6502d3604be(
    *,
    account_alias: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fa3548c0ec6459513439fb1838837a31c32da1fc090852cb0312c8ae0421257(
    props: typing.Union[CfnAccountAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7789b1b62c61dea6b5134059668568708bcca6a46291cddd8139462b00b8b0d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc30c2f37196691ed917b3a166c7cf8307b0bc02519417d814adffd329226e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75676dc90b63246c8e93769f33ec8ddf495f42bc906ede1081122abd88f573ba(
    *,
    channel_id: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
    channel_role_arn: typing.Optional[builtins.str] = None,
    notify_on_add_correspondence_to_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    notify_on_case_severity: typing.Optional[builtins.str] = None,
    notify_on_create_or_reopen_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    notify_on_resolve_case: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    team_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf658544fcd3ed01ed495acaa1e854ff7fd1254bcde1f24873e65742139fff47(
    props: typing.Union[CfnSlackChannelConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca452ab782cfae1740620d7fbe9cdbaa8cd18c39d6f05022115babae9cb08200(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5831d0fa7837bbc6ad99f9f29508122a9b531b101590e8c9c5c52043bf2daa53(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380b7bf6ac5691142ecf8824c6e8bf84aeea4375620e2ddfc20905f545e5c9a4(
    *,
    team_id: typing.Optional[builtins.str] = None,
    version_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26eaa01b4e8139e41eb91201f47c4191e7ab19d41ac620f578f1953181183ff8(
    props: typing.Union[CfnSlackWorkspaceConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0676ff9b65784538143f157dad6afd004baa66b0839519b62d34838a9490336e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4842ab4563f3db1d365c917e4ee5a206d19931b2c5e646579996dd308c48754d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
