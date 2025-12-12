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
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactChannelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "channel_address": "channelAddress",
        "channel_name": "channelName",
        "channel_type": "channelType",
        "contact_id": "contactId",
        "defer_activation": "deferActivation",
    },
)
class CfnContactChannelMixinProps:
    def __init__(
        self,
        *,
        channel_address: typing.Optional[builtins.str] = None,
        channel_name: typing.Optional[builtins.str] = None,
        channel_type: typing.Optional[builtins.str] = None,
        contact_id: typing.Optional[builtins.str] = None,
        defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnContactChannelPropsMixin.

        :param channel_address: The details that Incident Manager uses when trying to engage the contact channel.
        :param channel_name: The name of the contact channel.
        :param channel_type: The type of the contact channel. Incident Manager supports three contact methods:. - SMS - VOICE - EMAIL
        :param contact_id: The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.
        :param defer_activation: If you want to activate the channel at a later time, you can choose to defer activation. Incident Manager can't engage your contact channel until it has been activated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
            
            cfn_contact_channel_mixin_props = ssmcontacts_mixins.CfnContactChannelMixinProps(
                channel_address="channelAddress",
                channel_name="channelName",
                channel_type="channelType",
                contact_id="contactId",
                defer_activation=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e203018f319daceea7c187f662dc35b2145478a4dba0fb4624cee97b049f14a)
            check_type(argname="argument channel_address", value=channel_address, expected_type=type_hints["channel_address"])
            check_type(argname="argument channel_name", value=channel_name, expected_type=type_hints["channel_name"])
            check_type(argname="argument channel_type", value=channel_type, expected_type=type_hints["channel_type"])
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
            check_type(argname="argument defer_activation", value=defer_activation, expected_type=type_hints["defer_activation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel_address is not None:
            self._values["channel_address"] = channel_address
        if channel_name is not None:
            self._values["channel_name"] = channel_name
        if channel_type is not None:
            self._values["channel_type"] = channel_type
        if contact_id is not None:
            self._values["contact_id"] = contact_id
        if defer_activation is not None:
            self._values["defer_activation"] = defer_activation

    @builtins.property
    def channel_address(self) -> typing.Optional[builtins.str]:
        '''The details that Incident Manager uses when trying to engage the contact channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeladdress
        '''
        result = self._values.get("channel_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_name(self) -> typing.Optional[builtins.str]:
        '''The name of the contact channel.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channelname
        '''
        result = self._values.get("channel_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def channel_type(self) -> typing.Optional[builtins.str]:
        '''The type of the contact channel. Incident Manager supports three contact methods:.

        - SMS
        - VOICE
        - EMAIL

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-channeltype
        '''
        result = self._values.get("channel_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def contact_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the contact you are adding the contact channel to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-contactid
        '''
        result = self._values.get("contact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defer_activation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If you want to activate the channel at a later time, you can choose to defer activation.

        Incident Manager can't engage your contact channel until it has been activated.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html#cfn-ssmcontacts-contactchannel-deferactivation
        '''
        result = self._values.get("defer_activation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactChannelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContactChannelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactChannelPropsMixin",
):
    '''The ``AWS::SSMContacts::ContactChannel`` resource specifies a contact channel as the method that Incident Manager uses to engage your contact.

    .. epigraph::

       *Template example* : We recommend creating all Incident Manager ``Contacts`` resources using a single AWS CloudFormation template. For a demonstration, see the examples for `AWS::SSMContacts::Contacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contactchannel.html
    :cloudformationResource: AWS::SSMContacts::ContactChannel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
        
        cfn_contact_channel_props_mixin = ssmcontacts_mixins.CfnContactChannelPropsMixin(ssmcontacts_mixins.CfnContactChannelMixinProps(
            channel_address="channelAddress",
            channel_name="channelName",
            channel_type="channelType",
            contact_id="contactId",
            defer_activation=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnContactChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMContacts::ContactChannel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f39aaa9dcf2c829256bacf14d93811cb203bfbbc6fea0b1d88f4a745b17b1ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1776384d28f67a572ca2f0a47319d3fa13fb4fbaabdc56109bc23c716a6d610a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29f0bffc8326eb23ec33f25a5686c434abd90c8178718870cb3b9823c5895ae0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContactChannelMixinProps:
        return typing.cast(CfnContactChannelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias": "alias",
        "display_name": "displayName",
        "plan": "plan",
        "tags": "tags",
        "type": "type",
    },
)
class CfnContactMixinProps:
    def __init__(
        self,
        *,
        alias: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        plan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContactPropsMixin.StageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnContactPropsMixin.

        :param alias: The unique and identifiable alias of the contact or escalation plan.
        :param display_name: The full name of the contact or escalation plan.
        :param plan: A list of stages. A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.
        :param tags: 
        :param type: The type of contact. - ``PERSONAL`` : A single, individual contact. - ``ESCALATION`` : An escalation plan. - ``ONCALL_SCHEDULE`` : An on-call schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
            
            cfn_contact_mixin_props = ssmcontacts_mixins.CfnContactMixinProps(
                alias="alias",
                display_name="displayName",
                plan=[ssmcontacts_mixins.CfnContactPropsMixin.StageProperty(
                    duration_in_minutes=123,
                    rotation_ids=["rotationIds"],
                    targets=[ssmcontacts_mixins.CfnContactPropsMixin.TargetsProperty(
                        channel_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77f46c188043829ad79c882df15864fa2755ca2c9c30456ec18e99f74d3ecb65)
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias is not None:
            self._values["alias"] = alias
        if display_name is not None:
            self._values["display_name"] = display_name
        if plan is not None:
            self._values["plan"] = plan
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''The unique and identifiable alias of the contact or escalation plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-alias
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The full name of the contact or escalation plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plan(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.StageProperty"]]]]:
        '''A list of stages.

        A contact has an engagement plan with stages that contact specified contact channels. An escalation plan uses stages that contact specified contacts.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-plan
        '''
        result = self._values.get("plan")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.StageProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of contact.

        - ``PERSONAL`` : A single, individual contact.
        - ``ESCALATION`` : An escalation plan.
        - ``ONCALL_SCHEDULE`` : An on-call schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html#cfn-ssmcontacts-contact-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContactPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactPropsMixin",
):
    '''The ``AWS::SSMContacts::Contact`` resource specifies a contact or escalation plan.

    Incident Manager contacts are a subset of actions and data types that you can use for managing responder engagement and interaction.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html
    :cloudformationResource: AWS::SSMContacts::Contact
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
        
        cfn_contact_props_mixin = ssmcontacts_mixins.CfnContactPropsMixin(ssmcontacts_mixins.CfnContactMixinProps(
            alias="alias",
            display_name="displayName",
            plan=[ssmcontacts_mixins.CfnContactPropsMixin.StageProperty(
                duration_in_minutes=123,
                rotation_ids=["rotationIds"],
                targets=[ssmcontacts_mixins.CfnContactPropsMixin.TargetsProperty(
                    channel_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )]
            )],
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
        props: typing.Union[CfnContactMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMContacts::Contact``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367d18fd47ae3aa73d7d7d084f2f09bad94da1bc208b4a862d1899fd8adf2749)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5e61154e94305c307a8cada2d2887cf31fc4ee1346ebea1ef052293355468cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdce4b3f6e47110bf1b67ee31e79694004bdf35a05371c7c285a394d1d0d18d6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContactMixinProps:
        return typing.cast(CfnContactMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactPropsMixin.ChannelTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_id": "channelId",
            "retry_interval_in_minutes": "retryIntervalInMinutes",
        },
    )
    class ChannelTargetInfoProperty:
        def __init__(
            self,
            *,
            channel_id: typing.Optional[builtins.str] = None,
            retry_interval_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the contact channel that Incident Manager uses to engage the contact.

            :param channel_id: The Amazon Resource Name (ARN) of the contact channel.
            :param retry_interval_in_minutes: The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                channel_target_info_property = ssmcontacts_mixins.CfnContactPropsMixin.ChannelTargetInfoProperty(
                    channel_id="channelId",
                    retry_interval_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3ed6712cc8bfe304c366b1286e737834c8ae329ee0fb893ecfd25999287d7763)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument retry_interval_in_minutes", value=retry_interval_in_minutes, expected_type=type_hints["retry_interval_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_id is not None:
                self._values["channel_id"] = channel_id
            if retry_interval_in_minutes is not None:
                self._values["retry_interval_in_minutes"] = retry_interval_in_minutes

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the contact channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html#cfn-ssmcontacts-contact-channeltargetinfo-channelid
            '''
            result = self._values.get("channel_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retry_interval_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-channeltargetinfo.html#cfn-ssmcontacts-contact-channeltargetinfo-retryintervalinminutes
            '''
            result = self._values.get("retry_interval_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactPropsMixin.ContactTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_id": "contactId", "is_essential": "isEssential"},
    )
    class ContactTargetInfoProperty:
        def __init__(
            self,
            *,
            contact_id: typing.Optional[builtins.str] = None,
            is_essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The contact that Incident Manager is engaging during an incident.

            :param contact_id: The Amazon Resource Name (ARN) of the contact.
            :param is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                contact_target_info_property = ssmcontacts_mixins.CfnContactPropsMixin.ContactTargetInfoProperty(
                    contact_id="contactId",
                    is_essential=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cb82aede4b2b201fb5f0d356e0214dce0d3effbf020b1b0be1b8327e1e447a3)
                check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
                check_type(argname="argument is_essential", value=is_essential, expected_type=type_hints["is_essential"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_id is not None:
                self._values["contact_id"] = contact_id
            if is_essential is not None:
                self._values["is_essential"] = is_essential

        @builtins.property
        def contact_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html#cfn-ssmcontacts-contact-contacttargetinfo-contactid
            '''
            result = self._values.get("contact_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_essential(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-contacttargetinfo.html#cfn-ssmcontacts-contact-contacttargetinfo-isessential
            '''
            result = self._values.get("is_essential")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContactTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactPropsMixin.StageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_in_minutes": "durationInMinutes",
            "rotation_ids": "rotationIds",
            "targets": "targets",
        },
    )
    class StageProperty:
        def __init__(
            self,
            *,
            duration_in_minutes: typing.Optional[jsii.Number] = None,
            rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContactPropsMixin.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The ``Stage`` property type specifies a set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.

            :param duration_in_minutes: The time to wait until beginning the next stage. The duration can only be set to 0 if a target is specified.
            :param rotation_ids: The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.
            :param targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                stage_property = ssmcontacts_mixins.CfnContactPropsMixin.StageProperty(
                    duration_in_minutes=123,
                    rotation_ids=["rotationIds"],
                    targets=[ssmcontacts_mixins.CfnContactPropsMixin.TargetsProperty(
                        channel_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7aad603734e5c186510a00d872178066875f019c3e58266048eb800c72ee2103)
                check_type(argname="argument duration_in_minutes", value=duration_in_minutes, expected_type=type_hints["duration_in_minutes"])
                check_type(argname="argument rotation_ids", value=rotation_ids, expected_type=type_hints["rotation_ids"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_minutes is not None:
                self._values["duration_in_minutes"] = duration_in_minutes
            if rotation_ids is not None:
                self._values["rotation_ids"] = rotation_ids
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def duration_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The time to wait until beginning the next stage.

            The duration can only be set to 0 if a target is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-durationinminutes
            '''
            result = self._values.get("duration_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def rotation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-rotationids
            '''
            result = self._values.get("rotation_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.TargetsProperty"]]]]:
            '''The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-stage.html#cfn-ssmcontacts-contact-stage-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.TargetsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnContactPropsMixin.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_target_info": "channelTargetInfo",
            "contact_target_info": "contactTargetInfo",
        },
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            channel_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContactPropsMixin.ChannelTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            contact_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnContactPropsMixin.ContactTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The contact or contact channel that's being engaged.

            :param channel_target_info: Information about the contact channel that Incident Manager engages.
            :param contact_target_info: The contact that Incident Manager is engaging during an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                targets_property = ssmcontacts_mixins.CfnContactPropsMixin.TargetsProperty(
                    channel_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts_mixins.CfnContactPropsMixin.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c33de781abe58215dbdc8952e30e86a1e771ec8b9eb65525e2a404ffb3995c06)
                check_type(argname="argument channel_target_info", value=channel_target_info, expected_type=type_hints["channel_target_info"])
                check_type(argname="argument contact_target_info", value=contact_target_info, expected_type=type_hints["contact_target_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_target_info is not None:
                self._values["channel_target_info"] = channel_target_info
            if contact_target_info is not None:
                self._values["contact_target_info"] = contact_target_info

        @builtins.property
        def channel_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.ChannelTargetInfoProperty"]]:
            '''Information about the contact channel that Incident Manager engages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html#cfn-ssmcontacts-contact-targets-channeltargetinfo
            '''
            result = self._values.get("channel_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.ChannelTargetInfoProperty"]], result)

        @builtins.property
        def contact_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.ContactTargetInfoProperty"]]:
            '''The contact that Incident Manager is engaging during an incident.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-contact-targets.html#cfn-ssmcontacts-contact-targets-contacttargetinfo
            '''
            result = self._values.get("contact_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnContactPropsMixin.ContactTargetInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnPlanMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_id": "contactId",
        "rotation_ids": "rotationIds",
        "stages": "stages",
    },
)
class CfnPlanMixinProps:
    def __init__(
        self,
        *,
        contact_id: typing.Optional[builtins.str] = None,
        rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        stages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.StageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnPlanPropsMixin.

        :param contact_id: The Amazon Resource Name (ARN) of the contact.
        :param rotation_ids: The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.
        :param stages: A list of stages that the escalation plan or engagement plan uses to engage contacts and contact methods.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
            
            cfn_plan_mixin_props = ssmcontacts_mixins.CfnPlanMixinProps(
                contact_id="contactId",
                rotation_ids=["rotationIds"],
                stages=[ssmcontacts_mixins.CfnPlanPropsMixin.StageProperty(
                    duration_in_minutes=123,
                    targets=[ssmcontacts_mixins.CfnPlanPropsMixin.TargetsProperty(
                        channel_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fddeaee51fd62472b07ea362c4938b0c41b4d67e56907925ff487cdfea358325)
            check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
            check_type(argname="argument rotation_ids", value=rotation_ids, expected_type=type_hints["rotation_ids"])
            check_type(argname="argument stages", value=stages, expected_type=type_hints["stages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_id is not None:
            self._values["contact_id"] = contact_id
        if rotation_ids is not None:
            self._values["rotation_ids"] = rotation_ids
        if stages is not None:
            self._values["stages"] = stages

    @builtins.property
    def contact_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the contact.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-contactid
        '''
        result = self._values.get("contact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rotation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the on-call rotations associated with the plan.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-rotationids
        '''
        result = self._values.get("rotation_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stages(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.StageProperty"]]]]:
        '''A list of stages that the escalation plan or engagement plan uses to engage contacts and contact methods.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html#cfn-ssmcontacts-plan-stages
        '''
        result = self._values.get("stages")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.StageProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlanMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPlanPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnPlanPropsMixin",
):
    '''Information about the stages and on-call rotation teams associated with an escalation plan or engagement plan.

    .. epigraph::

       *Template example* : We recommend creating all Incident Manager ``Contacts`` resources using a single AWS CloudFormation template. For a demonstration, see the examples for `AWS::SSMContacts::Contacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-plan.html
    :cloudformationResource: AWS::SSMContacts::Plan
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
        
        cfn_plan_props_mixin = ssmcontacts_mixins.CfnPlanPropsMixin(ssmcontacts_mixins.CfnPlanMixinProps(
            contact_id="contactId",
            rotation_ids=["rotationIds"],
            stages=[ssmcontacts_mixins.CfnPlanPropsMixin.StageProperty(
                duration_in_minutes=123,
                targets=[ssmcontacts_mixins.CfnPlanPropsMixin.TargetsProperty(
                    channel_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )]
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMContacts::Plan``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f74a72c163a498b0e8a5c3f89fc973ce06f57e83307dbbe696878d07dfba3e00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68ca089157c166e0ae529d0d98d759dd15f112ba2d5b1b1a4cc6a2aa75ec3547)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4457c5b7b626aaef9bfccc23b4ca7426e16a5776d7936cb7fd070e4267e33777)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPlanMixinProps:
        return typing.cast(CfnPlanMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnPlanPropsMixin.ChannelTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_id": "channelId",
            "retry_interval_in_minutes": "retryIntervalInMinutes",
        },
    )
    class ChannelTargetInfoProperty:
        def __init__(
            self,
            *,
            channel_id: typing.Optional[builtins.str] = None,
            retry_interval_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the contact channel that Incident Manager uses to engage the contact.

            :param channel_id: The Amazon Resource Name (ARN) of the contact channel.
            :param retry_interval_in_minutes: The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-channeltargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                channel_target_info_property = ssmcontacts_mixins.CfnPlanPropsMixin.ChannelTargetInfoProperty(
                    channel_id="channelId",
                    retry_interval_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef515567fcaba716f93eb958132e75f0901ff80d8d8cd145bb05502abace0b1d)
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
                check_type(argname="argument retry_interval_in_minutes", value=retry_interval_in_minutes, expected_type=type_hints["retry_interval_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_id is not None:
                self._values["channel_id"] = channel_id
            if retry_interval_in_minutes is not None:
                self._values["retry_interval_in_minutes"] = retry_interval_in_minutes

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the contact channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-channeltargetinfo.html#cfn-ssmcontacts-plan-channeltargetinfo-channelid
            '''
            result = self._values.get("channel_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retry_interval_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The number of minutes to wait before retrying to send engagement if the engagement initially failed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-channeltargetinfo.html#cfn-ssmcontacts-plan-channeltargetinfo-retryintervalinminutes
            '''
            result = self._values.get("retry_interval_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnPlanPropsMixin.ContactTargetInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_id": "contactId", "is_essential": "isEssential"},
    )
    class ContactTargetInfoProperty:
        def __init__(
            self,
            *,
            contact_id: typing.Optional[builtins.str] = None,
            is_essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The contact that Incident Manager is engaging during an incident.

            :param contact_id: The Amazon Resource Name (ARN) of the contact.
            :param is_essential: A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-contacttargetinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                contact_target_info_property = ssmcontacts_mixins.CfnPlanPropsMixin.ContactTargetInfoProperty(
                    contact_id="contactId",
                    is_essential=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__125d43f3b378727d8d799b080433dccb8aa407041cc6b1032a061270fa3ce0dc)
                check_type(argname="argument contact_id", value=contact_id, expected_type=type_hints["contact_id"])
                check_type(argname="argument is_essential", value=is_essential, expected_type=type_hints["is_essential"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_id is not None:
                self._values["contact_id"] = contact_id
            if is_essential is not None:
                self._values["is_essential"] = is_essential

        @builtins.property
        def contact_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-contacttargetinfo.html#cfn-ssmcontacts-plan-contacttargetinfo-contactid
            '''
            result = self._values.get("contact_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def is_essential(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value determining if the contact's acknowledgement stops the progress of stages in the plan.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-contacttargetinfo.html#cfn-ssmcontacts-plan-contacttargetinfo-isessential
            '''
            result = self._values.get("is_essential")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContactTargetInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnPlanPropsMixin.StageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "duration_in_minutes": "durationInMinutes",
            "targets": "targets",
        },
    )
    class StageProperty:
        def __init__(
            self,
            *,
            duration_in_minutes: typing.Optional[jsii.Number] = None,
            targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.TargetsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A set amount of time that an escalation plan or engagement plan engages the specified contacts or contact methods.

            :param duration_in_minutes: The time to wait until beginning the next stage. The duration can only be set to 0 if a target is specified.
            :param targets: The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-stage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                stage_property = ssmcontacts_mixins.CfnPlanPropsMixin.StageProperty(
                    duration_in_minutes=123,
                    targets=[ssmcontacts_mixins.CfnPlanPropsMixin.TargetsProperty(
                        channel_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ChannelTargetInfoProperty(
                            channel_id="channelId",
                            retry_interval_in_minutes=123
                        ),
                        contact_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ContactTargetInfoProperty(
                            contact_id="contactId",
                            is_essential=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6b2c6cb090eb2b0e14a84fa110a4f7ab37581d3b69c992f74e10dc4a5415a32d)
                check_type(argname="argument duration_in_minutes", value=duration_in_minutes, expected_type=type_hints["duration_in_minutes"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if duration_in_minutes is not None:
                self._values["duration_in_minutes"] = duration_in_minutes
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def duration_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The time to wait until beginning the next stage.

            The duration can only be set to 0 if a target is specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-stage.html#cfn-ssmcontacts-plan-stage-durationinminutes
            '''
            result = self._values.get("duration_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.TargetsProperty"]]]]:
            '''The contacts or contact methods that the escalation plan or engagement plan is engaging.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-stage.html#cfn-ssmcontacts-plan-stage-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.TargetsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnPlanPropsMixin.TargetsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel_target_info": "channelTargetInfo",
            "contact_target_info": "contactTargetInfo",
        },
    )
    class TargetsProperty:
        def __init__(
            self,
            *,
            channel_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ChannelTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            contact_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPlanPropsMixin.ContactTargetInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The contact or contact channel that's being engaged.

            :param channel_target_info: Information about the contact channel that Incident Manager engages.
            :param contact_target_info: Information about the contact that Incident Manager engages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-targets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                targets_property = ssmcontacts_mixins.CfnPlanPropsMixin.TargetsProperty(
                    channel_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ChannelTargetInfoProperty(
                        channel_id="channelId",
                        retry_interval_in_minutes=123
                    ),
                    contact_target_info=ssmcontacts_mixins.CfnPlanPropsMixin.ContactTargetInfoProperty(
                        contact_id="contactId",
                        is_essential=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22537a1127dea50eb77daf6365f9bb118c3817fdb7df5a73935f752becca6f91)
                check_type(argname="argument channel_target_info", value=channel_target_info, expected_type=type_hints["channel_target_info"])
                check_type(argname="argument contact_target_info", value=contact_target_info, expected_type=type_hints["contact_target_info"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel_target_info is not None:
                self._values["channel_target_info"] = channel_target_info
            if contact_target_info is not None:
                self._values["contact_target_info"] = contact_target_info

        @builtins.property
        def channel_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ChannelTargetInfoProperty"]]:
            '''Information about the contact channel that Incident Manager engages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-targets.html#cfn-ssmcontacts-plan-targets-channeltargetinfo
            '''
            result = self._values.get("channel_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ChannelTargetInfoProperty"]], result)

        @builtins.property
        def contact_target_info(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ContactTargetInfoProperty"]]:
            '''Information about the contact that Incident Manager engages.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-plan-targets.html#cfn-ssmcontacts-plan-targets-contacttargetinfo
            '''
            result = self._values.get("contact_target_info")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPlanPropsMixin.ContactTargetInfoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_ids": "contactIds",
        "name": "name",
        "recurrence": "recurrence",
        "start_time": "startTime",
        "tags": "tags",
        "time_zone_id": "timeZoneId",
    },
)
class CfnRotationMixinProps:
    def __init__(
        self,
        *,
        contact_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        recurrence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationPropsMixin.RecurrenceSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        start_time: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_zone_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRotationPropsMixin.

        :param contact_ids: The Amazon Resource Names (ARNs) of the contacts to add to the rotation. .. epigraph:: Only the ``PERSONAL`` contact type is supported. The contact types ``ESCALATION`` and ``ONCALL_SCHEDULE`` are not supported for this operation. The order in which you list the contacts is their shift order in the rotation schedule.
        :param name: The name for the rotation.
        :param recurrence: Information about the rule that specifies when shift team members rotate.
        :param start_time: The date and time the rotation goes into effect.
        :param tags: Optional metadata to assign to the rotation. Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For more information, see `Tagging Incident Manager resources <https://docs.aws.amazon.com/incident-manager/latest/userguide/tagging.html>`_ in the *Incident Manager User Guide* .
        :param time_zone_id: The time zone to base the rotation’s activity on, in Internet Assigned Numbers Authority (IANA) format. For example: "America/Los_Angeles", "UTC", or "Asia/Seoul". For more information, see the `Time Zone Database <https://docs.aws.amazon.com/https://www.iana.org/time-zones>`_ on the IANA website. .. epigraph:: Designators for time zones that don’t support Daylight Savings Time rules, such as Pacific Standard Time (PST), are not supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
            
            cfn_rotation_mixin_props = ssmcontacts_mixins.CfnRotationMixinProps(
                contact_ids=["contactIds"],
                name="name",
                recurrence=ssmcontacts_mixins.CfnRotationPropsMixin.RecurrenceSettingsProperty(
                    daily_settings=["dailySettings"],
                    monthly_settings=[ssmcontacts_mixins.CfnRotationPropsMixin.MonthlySettingProperty(
                        day_of_month=123,
                        hand_off_time="handOffTime"
                    )],
                    number_of_on_calls=123,
                    recurrence_multiplier=123,
                    shift_coverages=[ssmcontacts_mixins.CfnRotationPropsMixin.ShiftCoverageProperty(
                        coverage_times=[ssmcontacts_mixins.CfnRotationPropsMixin.CoverageTimeProperty(
                            end_time="endTime",
                            start_time="startTime"
                        )],
                        day_of_week="dayOfWeek"
                    )],
                    weekly_settings=[ssmcontacts_mixins.CfnRotationPropsMixin.WeeklySettingProperty(
                        day_of_week="dayOfWeek",
                        hand_off_time="handOffTime"
                    )]
                ),
                start_time="startTime",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_zone_id="timeZoneId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0379a8e26ef9df8ecf0c165062e2639d5d3e23a5903daca59d3e98338ba21626)
            check_type(argname="argument contact_ids", value=contact_ids, expected_type=type_hints["contact_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_zone_id", value=time_zone_id, expected_type=type_hints["time_zone_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_ids is not None:
            self._values["contact_ids"] = contact_ids
        if name is not None:
            self._values["name"] = name
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if start_time is not None:
            self._values["start_time"] = start_time
        if tags is not None:
            self._values["tags"] = tags
        if time_zone_id is not None:
            self._values["time_zone_id"] = time_zone_id

    @builtins.property
    def contact_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARNs) of the contacts to add to the rotation.

        .. epigraph::

           Only the ``PERSONAL`` contact type is supported. The contact types ``ESCALATION`` and ``ONCALL_SCHEDULE`` are not supported for this operation.

        The order in which you list the contacts is their shift order in the rotation schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-contactids
        '''
        result = self._values.get("contact_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the rotation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.RecurrenceSettingsProperty"]]:
        '''Information about the rule that specifies when shift team members rotate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-recurrence
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.RecurrenceSettingsProperty"]], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The date and time the rotation goes into effect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-starttime
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Optional metadata to assign to the rotation.

        Tags enable you to categorize a resource in different ways, such as by purpose, owner, or environment. For more information, see `Tagging Incident Manager resources <https://docs.aws.amazon.com/incident-manager/latest/userguide/tagging.html>`_ in the *Incident Manager User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_zone_id(self) -> typing.Optional[builtins.str]:
        '''The time zone to base the rotation’s activity on, in Internet Assigned Numbers Authority (IANA) format.

        For example: "America/Los_Angeles", "UTC", or "Asia/Seoul". For more information, see the `Time Zone Database <https://docs.aws.amazon.com/https://www.iana.org/time-zones>`_ on the IANA website.
        .. epigraph::

           Designators for time zones that don’t support Daylight Savings Time rules, such as Pacific Standard Time (PST), are not supported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html#cfn-ssmcontacts-rotation-timezoneid
        '''
        result = self._values.get("time_zone_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRotationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRotationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationPropsMixin",
):
    '''Specifies a rotation in an on-call schedule.

    .. epigraph::

       *Template example* : We recommend creating all Incident Manager ``Contacts`` resources using a single AWS CloudFormation template. For a demonstration, see the examples for `AWS::SSMContacts::Contacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-contact.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssmcontacts-rotation.html
    :cloudformationResource: AWS::SSMContacts::Rotation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
        
        cfn_rotation_props_mixin = ssmcontacts_mixins.CfnRotationPropsMixin(ssmcontacts_mixins.CfnRotationMixinProps(
            contact_ids=["contactIds"],
            name="name",
            recurrence=ssmcontacts_mixins.CfnRotationPropsMixin.RecurrenceSettingsProperty(
                daily_settings=["dailySettings"],
                monthly_settings=[ssmcontacts_mixins.CfnRotationPropsMixin.MonthlySettingProperty(
                    day_of_month=123,
                    hand_off_time="handOffTime"
                )],
                number_of_on_calls=123,
                recurrence_multiplier=123,
                shift_coverages=[ssmcontacts_mixins.CfnRotationPropsMixin.ShiftCoverageProperty(
                    coverage_times=[ssmcontacts_mixins.CfnRotationPropsMixin.CoverageTimeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    day_of_week="dayOfWeek"
                )],
                weekly_settings=[ssmcontacts_mixins.CfnRotationPropsMixin.WeeklySettingProperty(
                    day_of_week="dayOfWeek",
                    hand_off_time="handOffTime"
                )]
            ),
            start_time="startTime",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_zone_id="timeZoneId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRotationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSMContacts::Rotation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff302d59e1f2863b20f90c351d8728d6d910864aa661a48b792d5ee90d4a355)
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
            type_hints = typing.get_type_hints(_typecheckingstub__762fdec096441bc4b0272e410def12c545b8cb50adc47201f57d06ffa8931eda)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307471384c5163c2257bcc72195ebc73321260d18d35e980154c2712bae628ae)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRotationMixinProps:
        return typing.cast(CfnRotationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationPropsMixin.CoverageTimeProperty",
        jsii_struct_bases=[],
        name_mapping={"end_time": "endTime", "start_time": "startTime"},
    )
    class CoverageTimeProperty:
        def __init__(
            self,
            *,
            end_time: typing.Optional[builtins.str] = None,
            start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about when an on-call shift begins and ends.

            :param end_time: Information about when an on-call rotation shift ends.
            :param start_time: Information about when an on-call rotation shift begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-coveragetime.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                coverage_time_property = ssmcontacts_mixins.CfnRotationPropsMixin.CoverageTimeProperty(
                    end_time="endTime",
                    start_time="startTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c4331f1ffc205358943ed256aaae940b080de7413b89df60305e43c3287a7974)
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if end_time is not None:
                self._values["end_time"] = end_time
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def end_time(self) -> typing.Optional[builtins.str]:
            '''Information about when an on-call rotation shift ends.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-coveragetime.html#cfn-ssmcontacts-rotation-coveragetime-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def start_time(self) -> typing.Optional[builtins.str]:
            '''Information about when an on-call rotation shift begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-coveragetime.html#cfn-ssmcontacts-rotation-coveragetime-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoverageTimeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationPropsMixin.MonthlySettingProperty",
        jsii_struct_bases=[],
        name_mapping={"day_of_month": "dayOfMonth", "hand_off_time": "handOffTime"},
    )
    class MonthlySettingProperty:
        def __init__(
            self,
            *,
            day_of_month: typing.Optional[jsii.Number] = None,
            hand_off_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about on-call rotations that recur monthly.

            :param day_of_month: The day of the month when monthly recurring on-call rotations begin.
            :param hand_off_time: The time of day when a monthly recurring on-call shift rotation begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-monthlysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                monthly_setting_property = ssmcontacts_mixins.CfnRotationPropsMixin.MonthlySettingProperty(
                    day_of_month=123,
                    hand_off_time="handOffTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e965c9f1395d5789f75f790824f61fea2b4bba5f4118878874602c12c305af1)
                check_type(argname="argument day_of_month", value=day_of_month, expected_type=type_hints["day_of_month"])
                check_type(argname="argument hand_off_time", value=hand_off_time, expected_type=type_hints["hand_off_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day_of_month is not None:
                self._values["day_of_month"] = day_of_month
            if hand_off_time is not None:
                self._values["hand_off_time"] = hand_off_time

        @builtins.property
        def day_of_month(self) -> typing.Optional[jsii.Number]:
            '''The day of the month when monthly recurring on-call rotations begin.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-monthlysetting.html#cfn-ssmcontacts-rotation-monthlysetting-dayofmonth
            '''
            result = self._values.get("day_of_month")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def hand_off_time(self) -> typing.Optional[builtins.str]:
            '''The time of day when a monthly recurring on-call shift rotation begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-monthlysetting.html#cfn-ssmcontacts-rotation-monthlysetting-handofftime
            '''
            result = self._values.get("hand_off_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonthlySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationPropsMixin.RecurrenceSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "daily_settings": "dailySettings",
            "monthly_settings": "monthlySettings",
            "number_of_on_calls": "numberOfOnCalls",
            "recurrence_multiplier": "recurrenceMultiplier",
            "shift_coverages": "shiftCoverages",
            "weekly_settings": "weeklySettings",
        },
    )
    class RecurrenceSettingsProperty:
        def __init__(
            self,
            *,
            daily_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
            monthly_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationPropsMixin.MonthlySettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            number_of_on_calls: typing.Optional[jsii.Number] = None,
            recurrence_multiplier: typing.Optional[jsii.Number] = None,
            shift_coverages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationPropsMixin.ShiftCoverageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            weekly_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationPropsMixin.WeeklySettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about when an on-call rotation is in effect and how long the rotation period lasts.

            :param daily_settings: Information about on-call rotations that recur daily.
            :param monthly_settings: Information about on-call rotations that recur monthly.
            :param number_of_on_calls: The number of contacts, or shift team members designated to be on call concurrently during a shift. For example, in an on-call schedule that contains ten contacts, a value of ``2`` designates that two of them are on call at any given time.
            :param recurrence_multiplier: The number of days, weeks, or months a single rotation lasts.
            :param shift_coverages: Information about the days of the week included in on-call rotation coverage.
            :param weekly_settings: Information about on-call rotations that recur weekly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                recurrence_settings_property = ssmcontacts_mixins.CfnRotationPropsMixin.RecurrenceSettingsProperty(
                    daily_settings=["dailySettings"],
                    monthly_settings=[ssmcontacts_mixins.CfnRotationPropsMixin.MonthlySettingProperty(
                        day_of_month=123,
                        hand_off_time="handOffTime"
                    )],
                    number_of_on_calls=123,
                    recurrence_multiplier=123,
                    shift_coverages=[ssmcontacts_mixins.CfnRotationPropsMixin.ShiftCoverageProperty(
                        coverage_times=[ssmcontacts_mixins.CfnRotationPropsMixin.CoverageTimeProperty(
                            end_time="endTime",
                            start_time="startTime"
                        )],
                        day_of_week="dayOfWeek"
                    )],
                    weekly_settings=[ssmcontacts_mixins.CfnRotationPropsMixin.WeeklySettingProperty(
                        day_of_week="dayOfWeek",
                        hand_off_time="handOffTime"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6bcee625c082e13461df9abe2e600c3a8304d2d2f79e66de95e15f6f489d0d16)
                check_type(argname="argument daily_settings", value=daily_settings, expected_type=type_hints["daily_settings"])
                check_type(argname="argument monthly_settings", value=monthly_settings, expected_type=type_hints["monthly_settings"])
                check_type(argname="argument number_of_on_calls", value=number_of_on_calls, expected_type=type_hints["number_of_on_calls"])
                check_type(argname="argument recurrence_multiplier", value=recurrence_multiplier, expected_type=type_hints["recurrence_multiplier"])
                check_type(argname="argument shift_coverages", value=shift_coverages, expected_type=type_hints["shift_coverages"])
                check_type(argname="argument weekly_settings", value=weekly_settings, expected_type=type_hints["weekly_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if daily_settings is not None:
                self._values["daily_settings"] = daily_settings
            if monthly_settings is not None:
                self._values["monthly_settings"] = monthly_settings
            if number_of_on_calls is not None:
                self._values["number_of_on_calls"] = number_of_on_calls
            if recurrence_multiplier is not None:
                self._values["recurrence_multiplier"] = recurrence_multiplier
            if shift_coverages is not None:
                self._values["shift_coverages"] = shift_coverages
            if weekly_settings is not None:
                self._values["weekly_settings"] = weekly_settings

        @builtins.property
        def daily_settings(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Information about on-call rotations that recur daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-dailysettings
            '''
            result = self._values.get("daily_settings")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def monthly_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.MonthlySettingProperty"]]]]:
            '''Information about on-call rotations that recur monthly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-monthlysettings
            '''
            result = self._values.get("monthly_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.MonthlySettingProperty"]]]], result)

        @builtins.property
        def number_of_on_calls(self) -> typing.Optional[jsii.Number]:
            '''The number of contacts, or shift team members designated to be on call concurrently during a shift.

            For example, in an on-call schedule that contains ten contacts, a value of ``2`` designates that two of them are on call at any given time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-numberofoncalls
            '''
            result = self._values.get("number_of_on_calls")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def recurrence_multiplier(self) -> typing.Optional[jsii.Number]:
            '''The number of days, weeks, or months a single rotation lasts.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-recurrencemultiplier
            '''
            result = self._values.get("recurrence_multiplier")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def shift_coverages(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.ShiftCoverageProperty"]]]]:
            '''Information about the days of the week included in on-call rotation coverage.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-shiftcoverages
            '''
            result = self._values.get("shift_coverages")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.ShiftCoverageProperty"]]]], result)

        @builtins.property
        def weekly_settings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.WeeklySettingProperty"]]]]:
            '''Information about on-call rotations that recur weekly.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-recurrencesettings.html#cfn-ssmcontacts-rotation-recurrencesettings-weeklysettings
            '''
            result = self._values.get("weekly_settings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.WeeklySettingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecurrenceSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationPropsMixin.ShiftCoverageProperty",
        jsii_struct_bases=[],
        name_mapping={"coverage_times": "coverageTimes", "day_of_week": "dayOfWeek"},
    )
    class ShiftCoverageProperty:
        def __init__(
            self,
            *,
            coverage_times: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRotationPropsMixin.CoverageTimeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            day_of_week: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the days of the week that the on-call rotation coverage includes.

            :param coverage_times: The start and end times of the shift.
            :param day_of_week: A list of days on which the schedule is active.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-shiftcoverage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                shift_coverage_property = ssmcontacts_mixins.CfnRotationPropsMixin.ShiftCoverageProperty(
                    coverage_times=[ssmcontacts_mixins.CfnRotationPropsMixin.CoverageTimeProperty(
                        end_time="endTime",
                        start_time="startTime"
                    )],
                    day_of_week="dayOfWeek"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5ecd3a9eca39fd1e9031d0f60d322fef62ac0491db2832466c6068b7d44fd55)
                check_type(argname="argument coverage_times", value=coverage_times, expected_type=type_hints["coverage_times"])
                check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if coverage_times is not None:
                self._values["coverage_times"] = coverage_times
            if day_of_week is not None:
                self._values["day_of_week"] = day_of_week

        @builtins.property
        def coverage_times(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.CoverageTimeProperty"]]]]:
            '''The start and end times of the shift.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-shiftcoverage.html#cfn-ssmcontacts-rotation-shiftcoverage-coveragetimes
            '''
            result = self._values.get("coverage_times")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRotationPropsMixin.CoverageTimeProperty"]]]], result)

        @builtins.property
        def day_of_week(self) -> typing.Optional[builtins.str]:
            '''A list of days on which the schedule is active.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-shiftcoverage.html#cfn-ssmcontacts-rotation-shiftcoverage-dayofweek
            '''
            result = self._values.get("day_of_week")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShiftCoverageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_ssmcontacts.mixins.CfnRotationPropsMixin.WeeklySettingProperty",
        jsii_struct_bases=[],
        name_mapping={"day_of_week": "dayOfWeek", "hand_off_time": "handOffTime"},
    )
    class WeeklySettingProperty:
        def __init__(
            self,
            *,
            day_of_week: typing.Optional[builtins.str] = None,
            hand_off_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about rotations that recur weekly.

            :param day_of_week: The day of the week when weekly recurring on-call shift rotations begins.
            :param hand_off_time: The time of day when a weekly recurring on-call shift rotation begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-weeklysetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_ssmcontacts import mixins as ssmcontacts_mixins
                
                weekly_setting_property = ssmcontacts_mixins.CfnRotationPropsMixin.WeeklySettingProperty(
                    day_of_week="dayOfWeek",
                    hand_off_time="handOffTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c429b17b6b4bfa5f28847be7f5ff90638a0bee0308e393df8f1665e2be38652)
                check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
                check_type(argname="argument hand_off_time", value=hand_off_time, expected_type=type_hints["hand_off_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day_of_week is not None:
                self._values["day_of_week"] = day_of_week
            if hand_off_time is not None:
                self._values["hand_off_time"] = hand_off_time

        @builtins.property
        def day_of_week(self) -> typing.Optional[builtins.str]:
            '''The day of the week when weekly recurring on-call shift rotations begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-weeklysetting.html#cfn-ssmcontacts-rotation-weeklysetting-dayofweek
            '''
            result = self._values.get("day_of_week")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hand_off_time(self) -> typing.Optional[builtins.str]:
            '''The time of day when a weekly recurring on-call shift rotation begins.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ssmcontacts-rotation-weeklysetting.html#cfn-ssmcontacts-rotation-weeklysetting-handofftime
            '''
            result = self._values.get("hand_off_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeeklySettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnContactChannelMixinProps",
    "CfnContactChannelPropsMixin",
    "CfnContactMixinProps",
    "CfnContactPropsMixin",
    "CfnPlanMixinProps",
    "CfnPlanPropsMixin",
    "CfnRotationMixinProps",
    "CfnRotationPropsMixin",
]

publication.publish()

def _typecheckingstub__7e203018f319daceea7c187f662dc35b2145478a4dba0fb4624cee97b049f14a(
    *,
    channel_address: typing.Optional[builtins.str] = None,
    channel_name: typing.Optional[builtins.str] = None,
    channel_type: typing.Optional[builtins.str] = None,
    contact_id: typing.Optional[builtins.str] = None,
    defer_activation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f39aaa9dcf2c829256bacf14d93811cb203bfbbc6fea0b1d88f4a745b17b1ea(
    props: typing.Union[CfnContactChannelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1776384d28f67a572ca2f0a47319d3fa13fb4fbaabdc56109bc23c716a6d610a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29f0bffc8326eb23ec33f25a5686c434abd90c8178718870cb3b9823c5895ae0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77f46c188043829ad79c882df15864fa2755ca2c9c30456ec18e99f74d3ecb65(
    *,
    alias: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    plan: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContactPropsMixin.StageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__367d18fd47ae3aa73d7d7d084f2f09bad94da1bc208b4a862d1899fd8adf2749(
    props: typing.Union[CfnContactMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e61154e94305c307a8cada2d2887cf31fc4ee1346ebea1ef052293355468cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdce4b3f6e47110bf1b67ee31e79694004bdf35a05371c7c285a394d1d0d18d6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ed6712cc8bfe304c366b1286e737834c8ae329ee0fb893ecfd25999287d7763(
    *,
    channel_id: typing.Optional[builtins.str] = None,
    retry_interval_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb82aede4b2b201fb5f0d356e0214dce0d3effbf020b1b0be1b8327e1e447a3(
    *,
    contact_id: typing.Optional[builtins.str] = None,
    is_essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aad603734e5c186510a00d872178066875f019c3e58266048eb800c72ee2103(
    *,
    duration_in_minutes: typing.Optional[jsii.Number] = None,
    rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContactPropsMixin.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33de781abe58215dbdc8952e30e86a1e771ec8b9eb65525e2a404ffb3995c06(
    *,
    channel_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContactPropsMixin.ChannelTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contact_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnContactPropsMixin.ContactTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fddeaee51fd62472b07ea362c4938b0c41b4d67e56907925ff487cdfea358325(
    *,
    contact_id: typing.Optional[builtins.str] = None,
    rotation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    stages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.StageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f74a72c163a498b0e8a5c3f89fc973ce06f57e83307dbbe696878d07dfba3e00(
    props: typing.Union[CfnPlanMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ca089157c166e0ae529d0d98d759dd15f112ba2d5b1b1a4cc6a2aa75ec3547(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4457c5b7b626aaef9bfccc23b4ca7426e16a5776d7936cb7fd070e4267e33777(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef515567fcaba716f93eb958132e75f0901ff80d8d8cd145bb05502abace0b1d(
    *,
    channel_id: typing.Optional[builtins.str] = None,
    retry_interval_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125d43f3b378727d8d799b080433dccb8aa407041cc6b1032a061270fa3ce0dc(
    *,
    contact_id: typing.Optional[builtins.str] = None,
    is_essential: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2c6cb090eb2b0e14a84fa110a4f7ab37581d3b69c992f74e10dc4a5415a32d(
    *,
    duration_in_minutes: typing.Optional[jsii.Number] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.TargetsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22537a1127dea50eb77daf6365f9bb118c3817fdb7df5a73935f752becca6f91(
    *,
    channel_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ChannelTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    contact_target_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPlanPropsMixin.ContactTargetInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0379a8e26ef9df8ecf0c165062e2639d5d3e23a5903daca59d3e98338ba21626(
    *,
    contact_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    recurrence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationPropsMixin.RecurrenceSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_time: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ff302d59e1f2863b20f90c351d8728d6d910864aa661a48b792d5ee90d4a355(
    props: typing.Union[CfnRotationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762fdec096441bc4b0272e410def12c545b8cb50adc47201f57d06ffa8931eda(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307471384c5163c2257bcc72195ebc73321260d18d35e980154c2712bae628ae(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4331f1ffc205358943ed256aaae940b080de7413b89df60305e43c3287a7974(
    *,
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e965c9f1395d5789f75f790824f61fea2b4bba5f4118878874602c12c305af1(
    *,
    day_of_month: typing.Optional[jsii.Number] = None,
    hand_off_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bcee625c082e13461df9abe2e600c3a8304d2d2f79e66de95e15f6f489d0d16(
    *,
    daily_settings: typing.Optional[typing.Sequence[builtins.str]] = None,
    monthly_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationPropsMixin.MonthlySettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    number_of_on_calls: typing.Optional[jsii.Number] = None,
    recurrence_multiplier: typing.Optional[jsii.Number] = None,
    shift_coverages: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationPropsMixin.ShiftCoverageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    weekly_settings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationPropsMixin.WeeklySettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5ecd3a9eca39fd1e9031d0f60d322fef62ac0491db2832466c6068b7d44fd55(
    *,
    coverage_times: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRotationPropsMixin.CoverageTimeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    day_of_week: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c429b17b6b4bfa5f28847be7f5ff90638a0bee0308e393df8f1665e2be38652(
    *,
    day_of_week: typing.Optional[builtins.str] = None,
    hand_off_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
