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
    jsii_type="@aws-cdk/mixins-preview.aws_detective.mixins.CfnGraphMixinProps",
    jsii_struct_bases=[],
    name_mapping={"auto_enable_members": "autoEnableMembers", "tags": "tags"},
)
class CfnGraphMixinProps:
    def __init__(
        self,
        *,
        auto_enable_members: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGraphPropsMixin.

        :param auto_enable_members: Indicates whether to automatically enable new organization accounts as member accounts in the organization behavior graph. By default, this property is set to ``false`` . If you want to change the value of this property, you must be the Detective administrator for the organization. For more information on setting a Detective administrator account, see `AWS::Detective::OrganizationAdmin <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html>`_ . Default: - false
        :param tags: The tag values to assign to the new behavior graph.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_detective import mixins as detective_mixins
            
            cfn_graph_mixin_props = detective_mixins.CfnGraphMixinProps(
                auto_enable_members=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ea3e198b2ec1168982cadf4ba33d43b14354c6a142ac7932af4af449d6f330)
            check_type(argname="argument auto_enable_members", value=auto_enable_members, expected_type=type_hints["auto_enable_members"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_enable_members is not None:
            self._values["auto_enable_members"] = auto_enable_members
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auto_enable_members(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether to automatically enable new organization accounts as member accounts in the organization behavior graph.

        By default, this property is set to ``false`` . If you want to change the value of this property, you must be the Detective administrator for the organization. For more information on setting a Detective administrator account, see `AWS::Detective::OrganizationAdmin <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html>`_ .

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html#cfn-detective-graph-autoenablemembers
        '''
        result = self._values.get("auto_enable_members")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tag values to assign to the new behavior graph.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html#cfn-detective-graph-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGraphMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGraphPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_detective.mixins.CfnGraphPropsMixin",
):
    '''The ``AWS::Detective::Graph`` resource is an Amazon Detective resource type that creates a Detective behavior graph.

    The requesting account becomes the administrator account for the behavior graph.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-graph.html
    :cloudformationResource: AWS::Detective::Graph
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_detective import mixins as detective_mixins
        
        cfn_graph_props_mixin = detective_mixins.CfnGraphPropsMixin(detective_mixins.CfnGraphMixinProps(
            auto_enable_members=False,
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
        props: typing.Union[CfnGraphMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Detective::Graph``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1b8d7cf6d92d79f63efb7405ce1f23849e4cb19d8ebffbcfbe9d6349713ab65)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d053112239cc8a16e54cae4e950f4c8455debd3a8b912d163c5bd6e3a10ee18d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fe228065fdc349edf44533c3e84640ec26d44c739f0d3efcc371198213582c6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGraphMixinProps:
        return typing.cast(CfnGraphMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_detective.mixins.CfnMemberInvitationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "disable_email_notification": "disableEmailNotification",
        "graph_arn": "graphArn",
        "member_email_address": "memberEmailAddress",
        "member_id": "memberId",
        "message": "message",
    },
)
class CfnMemberInvitationMixinProps:
    def __init__(
        self,
        *,
        disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        graph_arn: typing.Optional[builtins.str] = None,
        member_email_address: typing.Optional[builtins.str] = None,
        member_id: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMemberInvitationPropsMixin.

        :param disable_email_notification: Whether to send an invitation email to the member account. If set to true, the member account does not receive an invitation email. Default: - false
        :param graph_arn: The ARN of the behavior graph to invite the account to contribute data to.
        :param member_email_address: The root user email address of the invited account. If the email address provided is not the root user email address for the provided account, the invitation creation fails.
        :param member_id: The AWS account identifier of the invited account.
        :param message: Customized text to include in the invitation email message.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_detective import mixins as detective_mixins
            
            cfn_member_invitation_mixin_props = detective_mixins.CfnMemberInvitationMixinProps(
                disable_email_notification=False,
                graph_arn="graphArn",
                member_email_address="memberEmailAddress",
                member_id="memberId",
                message="message"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55fae1dcc3de67c348e6a873d6f0af8b49285b63842c24c771d487a8a6d1d0d2)
            check_type(argname="argument disable_email_notification", value=disable_email_notification, expected_type=type_hints["disable_email_notification"])
            check_type(argname="argument graph_arn", value=graph_arn, expected_type=type_hints["graph_arn"])
            check_type(argname="argument member_email_address", value=member_email_address, expected_type=type_hints["member_email_address"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disable_email_notification is not None:
            self._values["disable_email_notification"] = disable_email_notification
        if graph_arn is not None:
            self._values["graph_arn"] = graph_arn
        if member_email_address is not None:
            self._values["member_email_address"] = member_email_address
        if member_id is not None:
            self._values["member_id"] = member_id
        if message is not None:
            self._values["message"] = message

    @builtins.property
    def disable_email_notification(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to send an invitation email to the member account.

        If set to true, the member account does not receive an invitation email.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-disableemailnotification
        '''
        result = self._values.get("disable_email_notification")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def graph_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the behavior graph to invite the account to contribute data to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-grapharn
        '''
        result = self._values.get("graph_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_email_address(self) -> typing.Optional[builtins.str]:
        '''The root user email address of the invited account.

        If the email address provided is not the root user email address for the provided account, the invitation creation fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberemailaddress
        '''
        result = self._values.get("member_email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account identifier of the invited account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''Customized text to include in the invitation email message.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html#cfn-detective-memberinvitation-message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberInvitationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMemberInvitationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_detective.mixins.CfnMemberInvitationPropsMixin",
):
    '''The ``AWS::Detective::MemberInvitation`` resource is an Amazon Detective resource type that creates an invitation to join a Detective behavior graph.

    The administrator account can choose whether to send an email notification of the invitation to the root user email address of the AWS account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-memberinvitation.html
    :cloudformationResource: AWS::Detective::MemberInvitation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_detective import mixins as detective_mixins
        
        cfn_member_invitation_props_mixin = detective_mixins.CfnMemberInvitationPropsMixin(detective_mixins.CfnMemberInvitationMixinProps(
            disable_email_notification=False,
            graph_arn="graphArn",
            member_email_address="memberEmailAddress",
            member_id="memberId",
            message="message"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMemberInvitationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Detective::MemberInvitation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1eaa8041c30ad11b3b100226fd92b3db7b78d7f91f22e1d3342819cc814f8d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cce8ca0d679f519d540b9c5cc23cde431f5d027ff2327d1dac50c53cc0afbd09)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6673a1c0f2d0634acaefcd0b70123202acf8b8d579eef47f2c698e53c2a6a495)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMemberInvitationMixinProps:
        return typing.cast(CfnMemberInvitationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_detective.mixins.CfnOrganizationAdminMixinProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId"},
)
class CfnOrganizationAdminMixinProps:
    def __init__(self, *, account_id: typing.Optional[builtins.str] = None) -> None:
        '''Properties for CfnOrganizationAdminPropsMixin.

        :param account_id: The AWS account identifier of the account to designate as the Detective administrator account for the organization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_detective import mixins as detective_mixins
            
            cfn_organization_admin_mixin_props = detective_mixins.CfnOrganizationAdminMixinProps(
                account_id="accountId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec7d9debc6e90c2797e5b929b91db407683406e0ec73b835b517d1643149a3af)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account_id is not None:
            self._values["account_id"] = account_id

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The AWS account identifier of the account to designate as the Detective administrator account for the organization.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html#cfn-detective-organizationadmin-accountid
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOrganizationAdminMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOrganizationAdminPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_detective.mixins.CfnOrganizationAdminPropsMixin",
):
    '''The ``AWS::Detective::OrganizationAdmin`` resource is an Amazon Detective resource type that designates the Detective administrator account for the organization in the current region.

    If the account does not have Detective enabled, then this resource enables Detective for that account and creates a new behavior graph.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-detective-organizationadmin.html
    :cloudformationResource: AWS::Detective::OrganizationAdmin
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_detective import mixins as detective_mixins
        
        cfn_organization_admin_props_mixin = detective_mixins.CfnOrganizationAdminPropsMixin(detective_mixins.CfnOrganizationAdminMixinProps(
            account_id="accountId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOrganizationAdminMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Detective::OrganizationAdmin``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05a17d70cf174edcf0619a590570e2940cead4537d2167c156975b6c37456b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dfd94727ba920721800c29fa69b7a76d9afcba8d91a40d4b0f357f8b54e14aa6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5326c468cfba112b17679910edbcd7f6fceb7a53bb195f675642cb51e808da71)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOrganizationAdminMixinProps:
        return typing.cast(CfnOrganizationAdminMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnGraphMixinProps",
    "CfnGraphPropsMixin",
    "CfnMemberInvitationMixinProps",
    "CfnMemberInvitationPropsMixin",
    "CfnOrganizationAdminMixinProps",
    "CfnOrganizationAdminPropsMixin",
]

publication.publish()

def _typecheckingstub__f6ea3e198b2ec1168982cadf4ba33d43b14354c6a142ac7932af4af449d6f330(
    *,
    auto_enable_members: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1b8d7cf6d92d79f63efb7405ce1f23849e4cb19d8ebffbcfbe9d6349713ab65(
    props: typing.Union[CfnGraphMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d053112239cc8a16e54cae4e950f4c8455debd3a8b912d163c5bd6e3a10ee18d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fe228065fdc349edf44533c3e84640ec26d44c739f0d3efcc371198213582c6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55fae1dcc3de67c348e6a873d6f0af8b49285b63842c24c771d487a8a6d1d0d2(
    *,
    disable_email_notification: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    graph_arn: typing.Optional[builtins.str] = None,
    member_email_address: typing.Optional[builtins.str] = None,
    member_id: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1eaa8041c30ad11b3b100226fd92b3db7b78d7f91f22e1d3342819cc814f8d7(
    props: typing.Union[CfnMemberInvitationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce8ca0d679f519d540b9c5cc23cde431f5d027ff2327d1dac50c53cc0afbd09(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6673a1c0f2d0634acaefcd0b70123202acf8b8d579eef47f2c698e53c2a6a495(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec7d9debc6e90c2797e5b929b91db407683406e0ec73b835b517d1643149a3af(
    *,
    account_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05a17d70cf174edcf0619a590570e2940cead4537d2167c156975b6c37456b2(
    props: typing.Union[CfnOrganizationAdminMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd94727ba920721800c29fa69b7a76d9afcba8d91a40d4b0f357f8b54e14aa6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5326c468cfba112b17679910edbcd7f6fceb7a53bb195f675642cb51e808da71(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
