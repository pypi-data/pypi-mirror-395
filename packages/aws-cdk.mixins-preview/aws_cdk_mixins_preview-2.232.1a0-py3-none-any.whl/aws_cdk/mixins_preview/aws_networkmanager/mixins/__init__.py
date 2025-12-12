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
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "edge_location": "edgeLocation",
        "network_function_group_name": "networkFunctionGroupName",
        "options": "options",
        "proposed_network_function_group_change": "proposedNetworkFunctionGroupChange",
        "proposed_segment_change": "proposedSegmentChange",
        "tags": "tags",
        "transport_attachment_id": "transportAttachmentId",
    },
)
class CfnConnectAttachmentMixinProps:
    def __init__(
        self,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        edge_location: typing.Optional[builtins.str] = None,
        network_function_group_name: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transport_attachment_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConnectAttachmentPropsMixin.

        :param core_network_id: The ID of the core network where the Connect attachment is located.
        :param edge_location: The Region where the edge is located.
        :param network_function_group_name: The name of the network function group.
        :param options: Options for connecting an attachment.
        :param proposed_network_function_group_change: Describes proposed changes to a network function group.
        :param proposed_segment_change: Describes a proposed segment change. In some cases, the segment change must first be evaluated and accepted.
        :param tags: The tags associated with the Connect attachment.
        :param transport_attachment_id: The ID of the transport attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_connect_attachment_mixin_props = networkmanager_mixins.CfnConnectAttachmentMixinProps(
                core_network_id="coreNetworkId",
                edge_location="edgeLocation",
                network_function_group_name="networkFunctionGroupName",
                options=networkmanager_mixins.CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty(
                    protocol="protocol"
                ),
                proposed_network_function_group_change=networkmanager_mixins.CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                proposed_segment_change=networkmanager_mixins.CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transport_attachment_id="transportAttachmentId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__376547195bc8d656deb703636f9f64f8708038db64c41d180e9d47bbeabd5b23)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument edge_location", value=edge_location, expected_type=type_hints["edge_location"])
            check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument proposed_network_function_group_change", value=proposed_network_function_group_change, expected_type=type_hints["proposed_network_function_group_change"])
            check_type(argname="argument proposed_segment_change", value=proposed_segment_change, expected_type=type_hints["proposed_segment_change"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transport_attachment_id", value=transport_attachment_id, expected_type=type_hints["transport_attachment_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_network_id is not None:
            self._values["core_network_id"] = core_network_id
        if edge_location is not None:
            self._values["edge_location"] = edge_location
        if network_function_group_name is not None:
            self._values["network_function_group_name"] = network_function_group_name
        if options is not None:
            self._values["options"] = options
        if proposed_network_function_group_change is not None:
            self._values["proposed_network_function_group_change"] = proposed_network_function_group_change
        if proposed_segment_change is not None:
            self._values["proposed_segment_change"] = proposed_segment_change
        if tags is not None:
            self._values["tags"] = tags
        if transport_attachment_id is not None:
            self._values["transport_attachment_id"] = transport_attachment_id

    @builtins.property
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the core network where the Connect attachment is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_location(self) -> typing.Optional[builtins.str]:
        '''The Region where the edge is located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-edgelocation
        '''
        result = self._values.get("edge_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_function_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-networkfunctiongroupname
        '''
        result = self._values.get("network_function_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty"]]:
        '''Options for connecting an attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty"]], result)

    @builtins.property
    def proposed_network_function_group_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]]:
        '''Describes proposed changes to a network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-proposednetworkfunctiongroupchange
        '''
        result = self._values.get("proposed_network_function_group_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]], result)

    @builtins.property
    def proposed_segment_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty"]]:
        '''Describes a proposed segment change.

        In some cases, the segment change must first be evaluated and accepted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-proposedsegmentchange
        '''
        result = self._values.get("proposed_segment_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the Connect attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transport_attachment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the transport attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html#cfn-networkmanager-connectattachment-transportattachmentid
        '''
        result = self._values.get("transport_attachment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectAttachmentPropsMixin",
):
    '''Creates a core network Connect attachment from a specified core network attachment.

    A core network Connect attachment is a GRE-based tunnel attachment that you can use to establish a connection between a core network and an appliance. A core network Connect attachment uses an existing VPC attachment as the underlying transport mechanism.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectattachment.html
    :cloudformationResource: AWS::NetworkManager::ConnectAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_connect_attachment_props_mixin = networkmanager_mixins.CfnConnectAttachmentPropsMixin(networkmanager_mixins.CfnConnectAttachmentMixinProps(
            core_network_id="coreNetworkId",
            edge_location="edgeLocation",
            network_function_group_name="networkFunctionGroupName",
            options=networkmanager_mixins.CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty(
                protocol="protocol"
            ),
            proposed_network_function_group_change=networkmanager_mixins.CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                attachment_policy_rule_number=123,
                network_function_group_name="networkFunctionGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            proposed_segment_change=networkmanager_mixins.CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty(
                attachment_policy_rule_number=123,
                segment_name="segmentName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transport_attachment_id="transportAttachmentId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::ConnectAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f31091868ce62203d18ad90f9674adc56f24a457f6e01dfa451b58edaf95e00f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48517be6f9e12e0b0cfe781a245fa554f488c2c2366fb5d64bbf38fa2242df9c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de9c3e7021c2ca30a57a90dc0b9e5b49bbb362c20ef2b8426120fefb4bb9a62b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectAttachmentMixinProps:
        return typing.cast(CfnConnectAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"protocol": "protocol"},
    )
    class ConnectAttachmentOptionsProperty:
        def __init__(self, *, protocol: typing.Optional[builtins.str] = None) -> None:
            '''Describes a core network Connect attachment options.

            :param protocol: The protocol used for the attachment connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-connectattachmentoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                connect_attachment_options_property = networkmanager_mixins.CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty(
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__51c1670bc365d5eeca9a16039a1586f3c4416712005d4e4bb530c13028cbd917)
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for the attachment connection.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-connectattachmentoptions.html#cfn-networkmanager-connectattachment-connectattachmentoptions-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectAttachmentOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "network_function_group_name": "networkFunctionGroupName",
            "tags": "tags",
        },
    )
    class ProposedNetworkFunctionGroupChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            network_function_group_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes proposed changes to a network function group.

            :param attachment_policy_rule_number: The proposed new attachment policy rule number for the network function group.
            :param network_function_group_name: The proposed name change for the network function group name.
            :param tags: The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposednetworkfunctiongroupchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_network_function_group_change_property = networkmanager_mixins.CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a69f674d193ada46eb8b214446a112c4ee0b7ef2d7c7ec46601ee718ceaa38a)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if network_function_group_name is not None:
                self._values["network_function_group_name"] = network_function_group_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The proposed new attachment policy rule number for the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-connectattachment-proposednetworkfunctiongroupchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def network_function_group_name(self) -> typing.Optional[builtins.str]:
            '''The proposed name change for the network function group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-connectattachment-proposednetworkfunctiongroupchange-networkfunctiongroupname
            '''
            result = self._values.get("network_function_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-connectattachment-proposednetworkfunctiongroupchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedNetworkFunctionGroupChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_segment_change_property = networkmanager_mixins.CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32fa32c3f8ce99ce4e71d16aea47b36578079c4649aa034b755b3012dec48348)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html#cfn-networkmanager-connectattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html#cfn-networkmanager-connectattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectattachment-proposedsegmentchange.html#cfn-networkmanager-connectattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectPeerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bgp_options": "bgpOptions",
        "connect_attachment_id": "connectAttachmentId",
        "core_network_address": "coreNetworkAddress",
        "inside_cidr_blocks": "insideCidrBlocks",
        "peer_address": "peerAddress",
        "subnet_arn": "subnetArn",
        "tags": "tags",
    },
)
class CfnConnectPeerMixinProps:
    def __init__(
        self,
        *,
        bgp_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectPeerPropsMixin.BgpOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        connect_attachment_id: typing.Optional[builtins.str] = None,
        core_network_address: typing.Optional[builtins.str] = None,
        inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        peer_address: typing.Optional[builtins.str] = None,
        subnet_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConnectPeerPropsMixin.

        :param bgp_options: Describes the BGP options.
        :param connect_attachment_id: The ID of the attachment to connect.
        :param core_network_address: The IP address of a core network.
        :param inside_cidr_blocks: The inside IP addresses used for a Connect peer configuration.
        :param peer_address: The IP address of the Connect peer.
        :param subnet_arn: The subnet ARN of the Connect peer.
        :param tags: The list of key-value tags associated with the Connect peer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_connect_peer_mixin_props = networkmanager_mixins.CfnConnectPeerMixinProps(
                bgp_options=networkmanager_mixins.CfnConnectPeerPropsMixin.BgpOptionsProperty(
                    peer_asn=123
                ),
                connect_attachment_id="connectAttachmentId",
                core_network_address="coreNetworkAddress",
                inside_cidr_blocks=["insideCidrBlocks"],
                peer_address="peerAddress",
                subnet_arn="subnetArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcbf63e0d7abd3f7f9f915aac3a0ca1f700e793200e41dd3cb569fd1c44098a7)
            check_type(argname="argument bgp_options", value=bgp_options, expected_type=type_hints["bgp_options"])
            check_type(argname="argument connect_attachment_id", value=connect_attachment_id, expected_type=type_hints["connect_attachment_id"])
            check_type(argname="argument core_network_address", value=core_network_address, expected_type=type_hints["core_network_address"])
            check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
            check_type(argname="argument subnet_arn", value=subnet_arn, expected_type=type_hints["subnet_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bgp_options is not None:
            self._values["bgp_options"] = bgp_options
        if connect_attachment_id is not None:
            self._values["connect_attachment_id"] = connect_attachment_id
        if core_network_address is not None:
            self._values["core_network_address"] = core_network_address
        if inside_cidr_blocks is not None:
            self._values["inside_cidr_blocks"] = inside_cidr_blocks
        if peer_address is not None:
            self._values["peer_address"] = peer_address
        if subnet_arn is not None:
            self._values["subnet_arn"] = subnet_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bgp_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectPeerPropsMixin.BgpOptionsProperty"]]:
        '''Describes the BGP options.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-bgpoptions
        '''
        result = self._values.get("bgp_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectPeerPropsMixin.BgpOptionsProperty"]], result)

    @builtins.property
    def connect_attachment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the attachment to connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-connectattachmentid
        '''
        result = self._values.get("connect_attachment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def core_network_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of a core network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-corenetworkaddress
        '''
        result = self._values.get("core_network_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The inside IP addresses used for a Connect peer configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-insidecidrblocks
        '''
        result = self._values.get("inside_cidr_blocks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def peer_address(self) -> typing.Optional[builtins.str]:
        '''The IP address of the Connect peer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-peeraddress
        '''
        result = self._values.get("peer_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_arn(self) -> typing.Optional[builtins.str]:
        '''The subnet ARN of the Connect peer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-subnetarn
        '''
        result = self._values.get("subnet_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value tags associated with the Connect peer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html#cfn-networkmanager-connectpeer-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectPeerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectPeerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectPeerPropsMixin",
):
    '''Creates a core network Connect peer for a specified core network connect attachment between a core network and an appliance.

    The peer address and transit gateway address must be the same IP address family (IPv4 or IPv6).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-connectpeer.html
    :cloudformationResource: AWS::NetworkManager::ConnectPeer
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_connect_peer_props_mixin = networkmanager_mixins.CfnConnectPeerPropsMixin(networkmanager_mixins.CfnConnectPeerMixinProps(
            bgp_options=networkmanager_mixins.CfnConnectPeerPropsMixin.BgpOptionsProperty(
                peer_asn=123
            ),
            connect_attachment_id="connectAttachmentId",
            core_network_address="coreNetworkAddress",
            inside_cidr_blocks=["insideCidrBlocks"],
            peer_address="peerAddress",
            subnet_arn="subnetArn",
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
        props: typing.Union[CfnConnectPeerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::ConnectPeer``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acd551b1ee80fed1cb8c1581d83647b2e1b4b4aaba1be9182ae5e215fce5bafa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__644d295199ed993d3673f03ccddb031c5866c6e8fc8e097c85c40464aabc5042)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a686f3eb0eed1eeba51e7fa7c47b3d0ba2a8ce230aa7c8d24177933fc8fff33)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectPeerMixinProps:
        return typing.cast(CfnConnectPeerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectPeerPropsMixin.BgpOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"peer_asn": "peerAsn"},
    )
    class BgpOptionsProperty:
        def __init__(self, *, peer_asn: typing.Optional[jsii.Number] = None) -> None:
            '''Describes the BGP options.

            :param peer_asn: The Peer ASN of the BGP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-bgpoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                bgp_options_property = networkmanager_mixins.CfnConnectPeerPropsMixin.BgpOptionsProperty(
                    peer_asn=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9445c0dbfc7ac72dcb4bfa3aed0af5dc50ba655499e60b77ab60714a7df434ad)
                check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if peer_asn is not None:
                self._values["peer_asn"] = peer_asn

        @builtins.property
        def peer_asn(self) -> typing.Optional[jsii.Number]:
            '''The Peer ASN of the BGP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-bgpoptions.html#cfn-networkmanager-connectpeer-bgpoptions-peerasn
            '''
            result = self._values.get("peer_asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BgpOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "core_network_address": "coreNetworkAddress",
            "core_network_asn": "coreNetworkAsn",
            "peer_address": "peerAddress",
            "peer_asn": "peerAsn",
        },
    )
    class ConnectPeerBgpConfigurationProperty:
        def __init__(
            self,
            *,
            core_network_address: typing.Optional[builtins.str] = None,
            core_network_asn: typing.Optional[jsii.Number] = None,
            peer_address: typing.Optional[builtins.str] = None,
            peer_asn: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a core network BGP configuration.

            :param core_network_address: The address of a core network.
            :param core_network_asn: The ASN of the Coret Network.
            :param peer_address: The address of a core network Connect peer.
            :param peer_asn: The ASN of the Connect peer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                connect_peer_bgp_configuration_property = networkmanager_mixins.CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty(
                    core_network_address="coreNetworkAddress",
                    core_network_asn=123,
                    peer_address="peerAddress",
                    peer_asn=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a8931d722114054cbaf69dfe95cd00f5a878306210501f505721dcd84c396f1)
                check_type(argname="argument core_network_address", value=core_network_address, expected_type=type_hints["core_network_address"])
                check_type(argname="argument core_network_asn", value=core_network_asn, expected_type=type_hints["core_network_asn"])
                check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
                check_type(argname="argument peer_asn", value=peer_asn, expected_type=type_hints["peer_asn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if core_network_address is not None:
                self._values["core_network_address"] = core_network_address
            if core_network_asn is not None:
                self._values["core_network_asn"] = core_network_asn
            if peer_address is not None:
                self._values["peer_address"] = peer_address
            if peer_asn is not None:
                self._values["peer_asn"] = peer_asn

        @builtins.property
        def core_network_address(self) -> typing.Optional[builtins.str]:
            '''The address of a core network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-corenetworkaddress
            '''
            result = self._values.get("core_network_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def core_network_asn(self) -> typing.Optional[jsii.Number]:
            '''The ASN of the Coret Network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-corenetworkasn
            '''
            result = self._values.get("core_network_asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def peer_address(self) -> typing.Optional[builtins.str]:
            '''The address of a core network Connect peer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-peeraddress
            '''
            result = self._values.get("peer_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def peer_asn(self) -> typing.Optional[jsii.Number]:
            '''The ASN of the Connect peer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerbgpconfiguration.html#cfn-networkmanager-connectpeer-connectpeerbgpconfiguration-peerasn
            '''
            result = self._values.get("peer_asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectPeerBgpConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnConnectPeerPropsMixin.ConnectPeerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bgp_configurations": "bgpConfigurations",
            "core_network_address": "coreNetworkAddress",
            "inside_cidr_blocks": "insideCidrBlocks",
            "peer_address": "peerAddress",
            "protocol": "protocol",
        },
    )
    class ConnectPeerConfigurationProperty:
        def __init__(
            self,
            *,
            bgp_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            core_network_address: typing.Optional[builtins.str] = None,
            inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
            peer_address: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a core network Connect peer configuration.

            :param bgp_configurations: The Connect peer BGP configurations.
            :param core_network_address: The IP address of a core network.
            :param inside_cidr_blocks: The inside IP addresses used for a Connect peer configuration.
            :param peer_address: The IP address of the Connect peer.
            :param protocol: The protocol used for a Connect peer configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                connect_peer_configuration_property = networkmanager_mixins.CfnConnectPeerPropsMixin.ConnectPeerConfigurationProperty(
                    bgp_configurations=[networkmanager_mixins.CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty(
                        core_network_address="coreNetworkAddress",
                        core_network_asn=123,
                        peer_address="peerAddress",
                        peer_asn=123
                    )],
                    core_network_address="coreNetworkAddress",
                    inside_cidr_blocks=["insideCidrBlocks"],
                    peer_address="peerAddress",
                    protocol="protocol"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__299e869edf1b3f4d09daa032df2c8debc3e8b4603f1162c277718650d9f5fb2f)
                check_type(argname="argument bgp_configurations", value=bgp_configurations, expected_type=type_hints["bgp_configurations"])
                check_type(argname="argument core_network_address", value=core_network_address, expected_type=type_hints["core_network_address"])
                check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
                check_type(argname="argument peer_address", value=peer_address, expected_type=type_hints["peer_address"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bgp_configurations is not None:
                self._values["bgp_configurations"] = bgp_configurations
            if core_network_address is not None:
                self._values["core_network_address"] = core_network_address
            if inside_cidr_blocks is not None:
                self._values["inside_cidr_blocks"] = inside_cidr_blocks
            if peer_address is not None:
                self._values["peer_address"] = peer_address
            if protocol is not None:
                self._values["protocol"] = protocol

        @builtins.property
        def bgp_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty"]]]]:
            '''The Connect peer BGP configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-bgpconfigurations
            '''
            result = self._values.get("bgp_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty"]]]], result)

        @builtins.property
        def core_network_address(self) -> typing.Optional[builtins.str]:
            '''The IP address of a core network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-corenetworkaddress
            '''
            result = self._values.get("core_network_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The inside IP addresses used for a Connect peer configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-insidecidrblocks
            '''
            result = self._values.get("inside_cidr_blocks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def peer_address(self) -> typing.Optional[builtins.str]:
            '''The IP address of the Connect peer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-peeraddress
            '''
            result = self._values.get("peer_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used for a Connect peer configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-connectpeer-connectpeerconfiguration.html#cfn-networkmanager-connectpeer-connectpeerconfiguration-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectPeerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCoreNetworkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "global_network_id": "globalNetworkId",
        "policy_document": "policyDocument",
        "tags": "tags",
    },
)
class CfnCoreNetworkMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        global_network_id: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCoreNetworkPropsMixin.

        :param description: The description of a core network.
        :param global_network_id: The ID of the global network that your core network is a part of.
        :param policy_document: Describes a core network policy. For more information, see `Core network policies <https://docs.aws.amazon.com/network-manager/latest/cloudwan/cloudwan-policy-change-sets.html>`_ . If you update the policy document, CloudFormation will apply the core network change set generated from the updated policy document, and then set it as the LIVE policy.
        :param tags: The list of key-value tags associated with a core network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            # policy_document: Any
            
            cfn_core_network_mixin_props = networkmanager_mixins.CfnCoreNetworkMixinProps(
                description="description",
                global_network_id="globalNetworkId",
                policy_document=policy_document,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6bd70b108158ccd1c98098b78081dfe96c42293e062f8c4e13b9c7736d726b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of a core network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network that your core network is a part of.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''Describes a core network policy. For more information, see `Core network policies <https://docs.aws.amazon.com/network-manager/latest/cloudwan/cloudwan-policy-change-sets.html>`_ .

        If you update the policy document, CloudFormation will apply the core network change set generated from the updated policy document, and then set it as the LIVE policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value tags associated with a core network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html#cfn-networkmanager-corenetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCoreNetworkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCoreNetworkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCoreNetworkPropsMixin",
):
    '''Describes a core network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-corenetwork.html
    :cloudformationResource: AWS::NetworkManager::CoreNetwork
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        # policy_document: Any
        
        cfn_core_network_props_mixin = networkmanager_mixins.CfnCoreNetworkPropsMixin(networkmanager_mixins.CfnCoreNetworkMixinProps(
            description="description",
            global_network_id="globalNetworkId",
            policy_document=policy_document,
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
        props: typing.Union[CfnCoreNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::CoreNetwork``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1695bb1e30476c48bb7aa47b1dfc40925df157e13550f682a15253a98aa4ac43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b0f5ae7d0c1e08784122369fe4fedb88623a39cded518b2283edeaca8f6462b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7b7a8a33475c90d1331900f850c8a43c25a8bad2294c9aa3edcba44f1bdf6bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCoreNetworkMixinProps:
        return typing.cast(CfnCoreNetworkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCoreNetworkPropsMixin.CoreNetworkEdgeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asn": "asn",
            "edge_location": "edgeLocation",
            "inside_cidr_blocks": "insideCidrBlocks",
        },
    )
    class CoreNetworkEdgeProperty:
        def __init__(
            self,
            *,
            asn: typing.Optional[jsii.Number] = None,
            edge_location: typing.Optional[builtins.str] = None,
            inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a core network edge.

            :param asn: The ASN of a core network edge.
            :param edge_location: The Region where a core network edge is located.
            :param inside_cidr_blocks: The inside IP addresses used for core network edges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                core_network_edge_property = networkmanager_mixins.CfnCoreNetworkPropsMixin.CoreNetworkEdgeProperty(
                    asn=123,
                    edge_location="edgeLocation",
                    inside_cidr_blocks=["insideCidrBlocks"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85ad1c44e741e7d1abf85b5e555a2e9420bc603bae2a2e105eaa02b7db4c7d11)
                check_type(argname="argument asn", value=asn, expected_type=type_hints["asn"])
                check_type(argname="argument edge_location", value=edge_location, expected_type=type_hints["edge_location"])
                check_type(argname="argument inside_cidr_blocks", value=inside_cidr_blocks, expected_type=type_hints["inside_cidr_blocks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asn is not None:
                self._values["asn"] = asn
            if edge_location is not None:
                self._values["edge_location"] = edge_location
            if inside_cidr_blocks is not None:
                self._values["inside_cidr_blocks"] = inside_cidr_blocks

        @builtins.property
        def asn(self) -> typing.Optional[jsii.Number]:
            '''The ASN of a core network edge.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html#cfn-networkmanager-corenetwork-corenetworkedge-asn
            '''
            result = self._values.get("asn")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def edge_location(self) -> typing.Optional[builtins.str]:
            '''The Region where a core network edge is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html#cfn-networkmanager-corenetwork-corenetworkedge-edgelocation
            '''
            result = self._values.get("edge_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def inside_cidr_blocks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The inside IP addresses used for core network edges.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworkedge.html#cfn-networkmanager-corenetwork-corenetworkedge-insidecidrblocks
            '''
            result = self._values.get("inside_cidr_blocks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreNetworkEdgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCoreNetworkPropsMixin.CoreNetworkNetworkFunctionGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "edge_locations": "edgeLocations",
            "name": "name",
            "segments": "segments",
        },
    )
    class CoreNetworkNetworkFunctionGroupProperty:
        def __init__(
            self,
            *,
            edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            segments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCoreNetworkPropsMixin.SegmentsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a network function group.

            :param edge_locations: The core network edge locations.
            :param name: The name of the network function group.
            :param segments: The segments associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworknetworkfunctiongroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                core_network_network_function_group_property = networkmanager_mixins.CfnCoreNetworkPropsMixin.CoreNetworkNetworkFunctionGroupProperty(
                    edge_locations=["edgeLocations"],
                    name="name",
                    segments=networkmanager_mixins.CfnCoreNetworkPropsMixin.SegmentsProperty(
                        send_to=["sendTo"],
                        send_via=["sendVia"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__443a898604abe535a2a8930d4f014536adaff1cacedb66771b63c0b3ef7627de)
                check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument segments", value=segments, expected_type=type_hints["segments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if edge_locations is not None:
                self._values["edge_locations"] = edge_locations
            if name is not None:
                self._values["name"] = name
            if segments is not None:
                self._values["segments"] = segments

        @builtins.property
        def edge_locations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The core network edge locations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworknetworkfunctiongroup.html#cfn-networkmanager-corenetwork-corenetworknetworkfunctiongroup-edgelocations
            '''
            result = self._values.get("edge_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworknetworkfunctiongroup.html#cfn-networkmanager-corenetwork-corenetworknetworkfunctiongroup-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def segments(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreNetworkPropsMixin.SegmentsProperty"]]:
            '''The segments associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworknetworkfunctiongroup.html#cfn-networkmanager-corenetwork-corenetworknetworkfunctiongroup-segments
            '''
            result = self._values.get("segments")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCoreNetworkPropsMixin.SegmentsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreNetworkNetworkFunctionGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCoreNetworkPropsMixin.CoreNetworkSegmentProperty",
        jsii_struct_bases=[],
        name_mapping={
            "edge_locations": "edgeLocations",
            "name": "name",
            "shared_segments": "sharedSegments",
        },
    )
    class CoreNetworkSegmentProperty:
        def __init__(
            self,
            *,
            edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
            name: typing.Optional[builtins.str] = None,
            shared_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a core network segment, which are dedicated routes.

            Only attachments within this segment can communicate with each other.

            :param edge_locations: The Regions where the edges are located.
            :param name: The name of a core network segment.
            :param shared_segments: The shared segments of a core network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                core_network_segment_property = networkmanager_mixins.CfnCoreNetworkPropsMixin.CoreNetworkSegmentProperty(
                    edge_locations=["edgeLocations"],
                    name="name",
                    shared_segments=["sharedSegments"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__849d8bb2d896ee58dec98fea77a986026ee3ce92b0bcedf7c972f6c9fba233b9)
                check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument shared_segments", value=shared_segments, expected_type=type_hints["shared_segments"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if edge_locations is not None:
                self._values["edge_locations"] = edge_locations
            if name is not None:
                self._values["name"] = name
            if shared_segments is not None:
                self._values["shared_segments"] = shared_segments

        @builtins.property
        def edge_locations(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Regions where the edges are located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html#cfn-networkmanager-corenetwork-corenetworksegment-edgelocations
            '''
            result = self._values.get("edge_locations")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a core network segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html#cfn-networkmanager-corenetwork-corenetworksegment-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def shared_segments(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The shared segments of a core network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-corenetworksegment.html#cfn-networkmanager-corenetwork-corenetworksegment-sharedsegments
            '''
            result = self._values.get("shared_segments")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CoreNetworkSegmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCoreNetworkPropsMixin.SegmentsProperty",
        jsii_struct_bases=[],
        name_mapping={"send_to": "sendTo", "send_via": "sendVia"},
    )
    class SegmentsProperty:
        def __init__(
            self,
            *,
            send_to: typing.Optional[typing.Sequence[builtins.str]] = None,
            send_via: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param send_to: 
            :param send_via: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-segments.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                segments_property = networkmanager_mixins.CfnCoreNetworkPropsMixin.SegmentsProperty(
                    send_to=["sendTo"],
                    send_via=["sendVia"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c8db760f1a7c3fd4830803825adf94bea1dc1a2d69481cd501df93c9f50f6c2f)
                check_type(argname="argument send_to", value=send_to, expected_type=type_hints["send_to"])
                check_type(argname="argument send_via", value=send_via, expected_type=type_hints["send_via"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if send_to is not None:
                self._values["send_to"] = send_to
            if send_via is not None:
                self._values["send_via"] = send_via

        @builtins.property
        def send_to(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-segments.html#cfn-networkmanager-corenetwork-segments-sendto
            '''
            result = self._values.get("send_to")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def send_via(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-corenetwork-segments.html#cfn-networkmanager-corenetwork-segments-sendvia
            '''
            result = self._values.get("send_via")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SegmentsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCustomerGatewayAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_gateway_arn": "customerGatewayArn",
        "device_id": "deviceId",
        "global_network_id": "globalNetworkId",
        "link_id": "linkId",
    },
)
class CfnCustomerGatewayAssociationMixinProps:
    def __init__(
        self,
        *,
        customer_gateway_arn: typing.Optional[builtins.str] = None,
        device_id: typing.Optional[builtins.str] = None,
        global_network_id: typing.Optional[builtins.str] = None,
        link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCustomerGatewayAssociationPropsMixin.

        :param customer_gateway_arn: The Amazon Resource Name (ARN) of the customer gateway.
        :param device_id: The ID of the device.
        :param global_network_id: The ID of the global network.
        :param link_id: The ID of the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_customer_gateway_association_mixin_props = networkmanager_mixins.CfnCustomerGatewayAssociationMixinProps(
                customer_gateway_arn="customerGatewayArn",
                device_id="deviceId",
                global_network_id="globalNetworkId",
                link_id="linkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ed9a64ae116bb65e4a7df06553437f5324ff57df2ec09659242657c42087740)
            check_type(argname="argument customer_gateway_arn", value=customer_gateway_arn, expected_type=type_hints["customer_gateway_arn"])
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument link_id", value=link_id, expected_type=type_hints["link_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if customer_gateway_arn is not None:
            self._values["customer_gateway_arn"] = customer_gateway_arn
        if device_id is not None:
            self._values["device_id"] = device_id
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if link_id is not None:
            self._values["link_id"] = link_id

    @builtins.property
    def customer_gateway_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the customer gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-customergatewayarn
        '''
        result = self._values.get("customer_gateway_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def device_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-deviceid
        '''
        result = self._values.get("device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html#cfn-networkmanager-customergatewayassociation-linkid
        '''
        result = self._values.get("link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCustomerGatewayAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCustomerGatewayAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnCustomerGatewayAssociationPropsMixin",
):
    '''Specifies an association between a customer gateway, a device, and optionally, a link.

    If you specify a link, it must be associated with the specified device. The customer gateway must be connected to a VPN attachment on a transit gateway that's registered in your global network.

    You cannot associate a customer gateway with more than one device and link.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-customergatewayassociation.html
    :cloudformationResource: AWS::NetworkManager::CustomerGatewayAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_customer_gateway_association_props_mixin = networkmanager_mixins.CfnCustomerGatewayAssociationPropsMixin(networkmanager_mixins.CfnCustomerGatewayAssociationMixinProps(
            customer_gateway_arn="customerGatewayArn",
            device_id="deviceId",
            global_network_id="globalNetworkId",
            link_id="linkId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCustomerGatewayAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::CustomerGatewayAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a6a7b302178654dbad33a39d58101b207b9459e49f254c0f3c1bfe69efddb7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e0c5dd139a29bd344958e2067a62656c9d6ee79ae20fe3f3ffeb2ede9fe8e5b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4d568553a213de861be46b4af9f3337f7f76ca182015105e826804323befe73)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCustomerGatewayAssociationMixinProps:
        return typing.cast(CfnCustomerGatewayAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDeviceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_location": "awsLocation",
        "description": "description",
        "global_network_id": "globalNetworkId",
        "location": "location",
        "model": "model",
        "serial_number": "serialNumber",
        "site_id": "siteId",
        "tags": "tags",
        "type": "type",
        "vendor": "vendor",
    },
)
class CfnDeviceMixinProps:
    def __init__(
        self,
        *,
        aws_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDevicePropsMixin.AWSLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        global_network_id: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDevicePropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        model: typing.Optional[builtins.str] = None,
        serial_number: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        vendor: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDevicePropsMixin.

        :param aws_location: The AWS location of the device.
        :param description: A description of the device. Constraints: Maximum length of 256 characters.
        :param global_network_id: The ID of the global network.
        :param location: The site location.
        :param model: The model of the device. Constraints: Maximum length of 128 characters.
        :param serial_number: The serial number of the device. Constraints: Maximum length of 128 characters.
        :param site_id: The site ID.
        :param tags: The tags for the device.
        :param type: The device type.
        :param vendor: The vendor of the device. Constraints: Maximum length of 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_device_mixin_props = networkmanager_mixins.CfnDeviceMixinProps(
                aws_location=networkmanager_mixins.CfnDevicePropsMixin.AWSLocationProperty(
                    subnet_arn="subnetArn",
                    zone="zone"
                ),
                description="description",
                global_network_id="globalNetworkId",
                location=networkmanager_mixins.CfnDevicePropsMixin.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                ),
                model="model",
                serial_number="serialNumber",
                site_id="siteId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type",
                vendor="vendor"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f07472a7614181033710cbfa2896482428060d7fda3f2edd3fbd0191cf91d94)
            check_type(argname="argument aws_location", value=aws_location, expected_type=type_hints["aws_location"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
            check_type(argname="argument site_id", value=site_id, expected_type=type_hints["site_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vendor", value=vendor, expected_type=type_hints["vendor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_location is not None:
            self._values["aws_location"] = aws_location
        if description is not None:
            self._values["description"] = description
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if location is not None:
            self._values["location"] = location
        if model is not None:
            self._values["model"] = model
        if serial_number is not None:
            self._values["serial_number"] = serial_number
        if site_id is not None:
            self._values["site_id"] = site_id
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if vendor is not None:
            self._values["vendor"] = vendor

    @builtins.property
    def aws_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDevicePropsMixin.AWSLocationProperty"]]:
        '''The AWS location of the device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-awslocation
        '''
        result = self._values.get("aws_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDevicePropsMixin.AWSLocationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the device.

        Constraints: Maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDevicePropsMixin.LocationProperty"]]:
        '''The site location.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDevicePropsMixin.LocationProperty"]], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''The model of the device.

        Constraints: Maximum length of 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-model
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def serial_number(self) -> typing.Optional[builtins.str]:
        '''The serial number of the device.

        Constraints: Maximum length of 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-serialnumber
        '''
        result = self._values.get("serial_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_id(self) -> typing.Optional[builtins.str]:
        '''The site ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-siteid
        '''
        result = self._values.get("site_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The device type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vendor(self) -> typing.Optional[builtins.str]:
        '''The vendor of the device.

        Constraints: Maximum length of 128 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html#cfn-networkmanager-device-vendor
        '''
        result = self._values.get("vendor")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeviceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDevicePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDevicePropsMixin",
):
    '''Specifies a device.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-device.html
    :cloudformationResource: AWS::NetworkManager::Device
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_device_props_mixin = networkmanager_mixins.CfnDevicePropsMixin(networkmanager_mixins.CfnDeviceMixinProps(
            aws_location=networkmanager_mixins.CfnDevicePropsMixin.AWSLocationProperty(
                subnet_arn="subnetArn",
                zone="zone"
            ),
            description="description",
            global_network_id="globalNetworkId",
            location=networkmanager_mixins.CfnDevicePropsMixin.LocationProperty(
                address="address",
                latitude="latitude",
                longitude="longitude"
            ),
            model="model",
            serial_number="serialNumber",
            site_id="siteId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type",
            vendor="vendor"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDeviceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::Device``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9fc2c1090985ba1f0bd043a0da4e65f36d1b891118fe6da0f35546a38cbf0c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bed08d6d1017593e8d6599868554bfbff0424269d9d3288fd1d146f8e2203a4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f5a2693cd376b701156906d2ca87857bf63e037291d1053582d775adc484aee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDeviceMixinProps:
        return typing.cast(CfnDeviceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDevicePropsMixin.AWSLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_arn": "subnetArn", "zone": "zone"},
    )
    class AWSLocationProperty:
        def __init__(
            self,
            *,
            subnet_arn: typing.Optional[builtins.str] = None,
            zone: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a location in AWS .

            :param subnet_arn: The Amazon Resource Name (ARN) of the subnet that the device is located in.
            :param zone: The Zone that the device is located in. Specify the ID of an Availability Zone, Local Zone, Wavelength Zone, or an Outpost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-awslocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                a_wSLocation_property = networkmanager_mixins.CfnDevicePropsMixin.AWSLocationProperty(
                    subnet_arn="subnetArn",
                    zone="zone"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99130f8abb45860d969816d5b76518688b93013289e448bf9d13a83cfb0086d0)
                check_type(argname="argument subnet_arn", value=subnet_arn, expected_type=type_hints["subnet_arn"])
                check_type(argname="argument zone", value=zone, expected_type=type_hints["zone"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if subnet_arn is not None:
                self._values["subnet_arn"] = subnet_arn
            if zone is not None:
                self._values["zone"] = zone

        @builtins.property
        def subnet_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the subnet that the device is located in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-awslocation.html#cfn-networkmanager-device-awslocation-subnetarn
            '''
            result = self._values.get("subnet_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def zone(self) -> typing.Optional[builtins.str]:
            '''The Zone that the device is located in.

            Specify the ID of an Availability Zone, Local Zone, Wavelength Zone, or an Outpost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-awslocation.html#cfn-networkmanager-device-awslocation-zone
            '''
            result = self._values.get("zone")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDevicePropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a location.

            :param address: The physical address.
            :param latitude: The latitude.
            :param longitude: The longitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                location_property = networkmanager_mixins.CfnDevicePropsMixin.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e69c563a0ecd65ce0560c4827b5585e0fb528c701509594703118b6fdb61f8ba)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The physical address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            '''The latitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            '''The longitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-device-location.html#cfn-networkmanager-device-location-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDirectConnectGatewayAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "direct_connect_gateway_arn": "directConnectGatewayArn",
        "edge_locations": "edgeLocations",
        "proposed_network_function_group_change": "proposedNetworkFunctionGroupChange",
        "proposed_segment_change": "proposedSegmentChange",
        "tags": "tags",
    },
)
class CfnDirectConnectGatewayAttachmentMixinProps:
    def __init__(
        self,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        direct_connect_gateway_arn: typing.Optional[builtins.str] = None,
        edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDirectConnectGatewayAttachmentPropsMixin.

        :param core_network_id: The ID of a core network for the Direct Connect Gateway attachment.
        :param direct_connect_gateway_arn: The Direct Connect gateway attachment ARN.
        :param edge_locations: The Regions where the edges are located.
        :param proposed_network_function_group_change: Describes proposed changes to a network function group.
        :param proposed_segment_change: Describes a proposed segment change. In some cases, the segment change must first be evaluated and accepted.
        :param tags: Tags for the attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_direct_connect_gateway_attachment_mixin_props = networkmanager_mixins.CfnDirectConnectGatewayAttachmentMixinProps(
                core_network_id="coreNetworkId",
                direct_connect_gateway_arn="directConnectGatewayArn",
                edge_locations=["edgeLocations"],
                proposed_network_function_group_change=networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                proposed_segment_change=networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52670004739b84bc51aa660afeb2710189c1db5cf4c447f519cdd1fa837ca43f)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument direct_connect_gateway_arn", value=direct_connect_gateway_arn, expected_type=type_hints["direct_connect_gateway_arn"])
            check_type(argname="argument edge_locations", value=edge_locations, expected_type=type_hints["edge_locations"])
            check_type(argname="argument proposed_network_function_group_change", value=proposed_network_function_group_change, expected_type=type_hints["proposed_network_function_group_change"])
            check_type(argname="argument proposed_segment_change", value=proposed_segment_change, expected_type=type_hints["proposed_segment_change"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_network_id is not None:
            self._values["core_network_id"] = core_network_id
        if direct_connect_gateway_arn is not None:
            self._values["direct_connect_gateway_arn"] = direct_connect_gateway_arn
        if edge_locations is not None:
            self._values["edge_locations"] = edge_locations
        if proposed_network_function_group_change is not None:
            self._values["proposed_network_function_group_change"] = proposed_network_function_group_change
        if proposed_segment_change is not None:
            self._values["proposed_segment_change"] = proposed_segment_change
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a core network for the Direct Connect Gateway attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html#cfn-networkmanager-directconnectgatewayattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def direct_connect_gateway_arn(self) -> typing.Optional[builtins.str]:
        '''The Direct Connect gateway attachment ARN.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html#cfn-networkmanager-directconnectgatewayattachment-directconnectgatewayarn
        '''
        result = self._values.get("direct_connect_gateway_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def edge_locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Regions where the edges are located.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html#cfn-networkmanager-directconnectgatewayattachment-edgelocations
        '''
        result = self._values.get("edge_locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def proposed_network_function_group_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]]:
        '''Describes proposed changes to a network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html#cfn-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange
        '''
        result = self._values.get("proposed_network_function_group_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]], result)

    @builtins.property
    def proposed_segment_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty"]]:
        '''Describes a proposed segment change.

        In some cases, the segment change must first be evaluated and accepted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html#cfn-networkmanager-directconnectgatewayattachment-proposedsegmentchange
        '''
        result = self._values.get("proposed_segment_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags for the attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html#cfn-networkmanager-directconnectgatewayattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectConnectGatewayAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDirectConnectGatewayAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDirectConnectGatewayAttachmentPropsMixin",
):
    '''Creates an AWS Direct Connect gateway attachment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-directconnectgatewayattachment.html
    :cloudformationResource: AWS::NetworkManager::DirectConnectGatewayAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_direct_connect_gateway_attachment_props_mixin = networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin(networkmanager_mixins.CfnDirectConnectGatewayAttachmentMixinProps(
            core_network_id="coreNetworkId",
            direct_connect_gateway_arn="directConnectGatewayArn",
            edge_locations=["edgeLocations"],
            proposed_network_function_group_change=networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                attachment_policy_rule_number=123,
                network_function_group_name="networkFunctionGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            proposed_segment_change=networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty(
                attachment_policy_rule_number=123,
                segment_name="segmentName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
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
        props: typing.Union[CfnDirectConnectGatewayAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::DirectConnectGatewayAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126b3b3ccb453bc4733d220c6e76f4cae594c5afd2cae601825b77ac2e49d7d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a603a1fdf7c0f19139a1cfc6f2b435dc00b8573938a662ac9a270dc847a61ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__920ee8fcc4aac74a1b3214921391dd7d3916720196acc8a8f496e97c0dada2c5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDirectConnectGatewayAttachmentMixinProps:
        return typing.cast(CfnDirectConnectGatewayAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "network_function_group_name": "networkFunctionGroupName",
            "tags": "tags",
        },
    )
    class ProposedNetworkFunctionGroupChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            network_function_group_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes proposed changes to a network function group.

            :param attachment_policy_rule_number: The proposed new attachment policy rule number for the network function group.
            :param network_function_group_name: The proposed name change for the network function group name.
            :param tags: The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_network_function_group_change_property = networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f426bac1c5e3541c23f472d2dddf506778e4bb9b6aa8e04c297c57d8e813cc2e)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if network_function_group_name is not None:
                self._values["network_function_group_name"] = network_function_group_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The proposed new attachment policy rule number for the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def network_function_group_name(self) -> typing.Optional[builtins.str]:
            '''The proposed name change for the network function group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange-networkfunctiongroupname
            '''
            result = self._values.get("network_function_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-directconnectgatewayattachment-proposednetworkfunctiongroupchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedNetworkFunctionGroupChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_segment_change_property = networkmanager_mixins.CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a89fedcd1b2c3385f58b47055514049bacbcee3fb09f88cdba48085563c65c22)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposedsegmentchange.html#cfn-networkmanager-directconnectgatewayattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposedsegmentchange.html#cfn-networkmanager-directconnectgatewayattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-directconnectgatewayattachment-proposedsegmentchange.html#cfn-networkmanager-directconnectgatewayattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnGlobalNetworkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "created_at": "createdAt",
        "description": "description",
        "state": "state",
        "tags": "tags",
    },
)
class CfnGlobalNetworkMixinProps:
    def __init__(
        self,
        *,
        created_at: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGlobalNetworkPropsMixin.

        :param created_at: The date and time that the global network was created.
        :param description: A description of the global network. Constraints: Maximum length of 256 characters.
        :param state: The state of the global network.
        :param tags: The tags for the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_global_network_mixin_props = networkmanager_mixins.CfnGlobalNetworkMixinProps(
                created_at="createdAt",
                description="description",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad600e63a37fdf52115193d81a97b7c3b4dcf7889870c917362901e1c8d9a69b)
            check_type(argname="argument created_at", value=created_at, expected_type=type_hints["created_at"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if created_at is not None:
            self._values["created_at"] = created_at
        if description is not None:
            self._values["description"] = description
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def created_at(self) -> typing.Optional[builtins.str]:
        '''The date and time that the global network was created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-createdat
        '''
        result = self._values.get("created_at")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the global network.

        Constraints: Maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html#cfn-networkmanager-globalnetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGlobalNetworkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGlobalNetworkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnGlobalNetworkPropsMixin",
):
    '''Creates a new, empty global network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-globalnetwork.html
    :cloudformationResource: AWS::NetworkManager::GlobalNetwork
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_global_network_props_mixin = networkmanager_mixins.CfnGlobalNetworkPropsMixin(networkmanager_mixins.CfnGlobalNetworkMixinProps(
            created_at="createdAt",
            description="description",
            state="state",
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
        props: typing.Union[CfnGlobalNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::GlobalNetwork``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c803538d229ce3793a3380ed5174621a8cf816b0a21f4191484ed9b725acf4b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c502eae070a2f6d5226747ebe85bc7f9befe695947742a731801f16071a23667)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fa21671c5d98c1bde78f90589a20fdafbf52b72e3f2bf35175c981e20ad2fa7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGlobalNetworkMixinProps:
        return typing.cast(CfnGlobalNetworkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnLinkAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "device_id": "deviceId",
        "global_network_id": "globalNetworkId",
        "link_id": "linkId",
    },
)
class CfnLinkAssociationMixinProps:
    def __init__(
        self,
        *,
        device_id: typing.Optional[builtins.str] = None,
        global_network_id: typing.Optional[builtins.str] = None,
        link_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLinkAssociationPropsMixin.

        :param device_id: The device ID for the link association.
        :param global_network_id: The ID of the global network.
        :param link_id: The ID of the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_link_association_mixin_props = networkmanager_mixins.CfnLinkAssociationMixinProps(
                device_id="deviceId",
                global_network_id="globalNetworkId",
                link_id="linkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21aa55d4825078e8aca0a155d1ab20c880267d01587d0ef807f9f302020421af)
            check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument link_id", value=link_id, expected_type=type_hints["link_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if device_id is not None:
            self._values["device_id"] = device_id
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if link_id is not None:
            self._values["link_id"] = link_id

    @builtins.property
    def device_id(self) -> typing.Optional[builtins.str]:
        '''The device ID for the link association.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-deviceid
        '''
        result = self._values.get("device_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def link_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html#cfn-networkmanager-linkassociation-linkid
        '''
        result = self._values.get("link_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLinkAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnLinkAssociationPropsMixin",
):
    '''Describes the association between a device and a link.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-linkassociation.html
    :cloudformationResource: AWS::NetworkManager::LinkAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_link_association_props_mixin = networkmanager_mixins.CfnLinkAssociationPropsMixin(networkmanager_mixins.CfnLinkAssociationMixinProps(
            device_id="deviceId",
            global_network_id="globalNetworkId",
            link_id="linkId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnLinkAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::LinkAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7a1f701951f666f3c902c08d2646e83c6bc5d24d03862cb559313f3d3a09757)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e2a4c24d8e76b6bcff3715d36e6b827b775314452a0c1d8fd7b8c5e7bd2c5ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6b41ed281d0f16aab2dc401885b1889005f735e61109dba38ad5df71682798f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLinkAssociationMixinProps:
        return typing.cast(CfnLinkAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnLinkMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bandwidth": "bandwidth",
        "description": "description",
        "global_network_id": "globalNetworkId",
        "provider": "provider",
        "site_id": "siteId",
        "tags": "tags",
        "type": "type",
    },
)
class CfnLinkMixinProps:
    def __init__(
        self,
        *,
        bandwidth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnLinkPropsMixin.BandwidthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        global_network_id: typing.Optional[builtins.str] = None,
        provider: typing.Optional[builtins.str] = None,
        site_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnLinkPropsMixin.

        :param bandwidth: The bandwidth for the link.
        :param description: A description of the link. Constraints: Maximum length of 256 characters.
        :param global_network_id: The ID of the global network.
        :param provider: The provider of the link. Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^
        :param site_id: The ID of the site.
        :param tags: The tags for the link.
        :param type: The type of the link. Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_link_mixin_props = networkmanager_mixins.CfnLinkMixinProps(
                bandwidth=networkmanager_mixins.CfnLinkPropsMixin.BandwidthProperty(
                    download_speed=123,
                    upload_speed=123
                ),
                description="description",
                global_network_id="globalNetworkId",
                provider="provider",
                site_id="siteId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2e6efcb610e2788c67fef0cae70ddc651781cd68f88a3ea79fc21fa6d47afaa)
            check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument site_id", value=site_id, expected_type=type_hints["site_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bandwidth is not None:
            self._values["bandwidth"] = bandwidth
        if description is not None:
            self._values["description"] = description
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if provider is not None:
            self._values["provider"] = provider
        if site_id is not None:
            self._values["site_id"] = site_id
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def bandwidth(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.BandwidthProperty"]]:
        '''The bandwidth for the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-bandwidth
        '''
        result = self._values.get("bandwidth")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnLinkPropsMixin.BandwidthProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the link.

        Constraints: Maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provider(self) -> typing.Optional[builtins.str]:
        '''The provider of the link.

        Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-provider
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def site_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the site.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-siteid
        '''
        result = self._values.get("site_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the link.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the link.

        Constraints: Maximum length of 128 characters. Cannot include the following characters: | \\ ^

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html#cfn-networkmanager-link-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLinkMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLinkPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnLinkPropsMixin",
):
    '''Specifies a link for a site.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-link.html
    :cloudformationResource: AWS::NetworkManager::Link
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_link_props_mixin = networkmanager_mixins.CfnLinkPropsMixin(networkmanager_mixins.CfnLinkMixinProps(
            bandwidth=networkmanager_mixins.CfnLinkPropsMixin.BandwidthProperty(
                download_speed=123,
                upload_speed=123
            ),
            description="description",
            global_network_id="globalNetworkId",
            provider="provider",
            site_id="siteId",
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
        props: typing.Union[CfnLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::Link``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89542d48303651711c3b8db8d64e86217b8e4975dcbcd61c06abd92d40cc8024)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd0ca68acbc7a4eb4dbb9517bdbd8e395436fe41764cbe21db14431c523acf32)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d36aaff86281e984eb745e06bc3346128e26434cba02234d652811d7eaa14611)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLinkMixinProps:
        return typing.cast(CfnLinkMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnLinkPropsMixin.BandwidthProperty",
        jsii_struct_bases=[],
        name_mapping={
            "download_speed": "downloadSpeed",
            "upload_speed": "uploadSpeed",
        },
    )
    class BandwidthProperty:
        def __init__(
            self,
            *,
            download_speed: typing.Optional[jsii.Number] = None,
            upload_speed: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes bandwidth information.

            :param download_speed: Download speed in Mbps.
            :param upload_speed: Upload speed in Mbps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                bandwidth_property = networkmanager_mixins.CfnLinkPropsMixin.BandwidthProperty(
                    download_speed=123,
                    upload_speed=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ddb7784934d5c0ad890e4f1480e67fb6af2f1bc0462f6d694ba7b8840a953145)
                check_type(argname="argument download_speed", value=download_speed, expected_type=type_hints["download_speed"])
                check_type(argname="argument upload_speed", value=upload_speed, expected_type=type_hints["upload_speed"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if download_speed is not None:
                self._values["download_speed"] = download_speed
            if upload_speed is not None:
                self._values["upload_speed"] = upload_speed

        @builtins.property
        def download_speed(self) -> typing.Optional[jsii.Number]:
            '''Download speed in Mbps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-downloadspeed
            '''
            result = self._values.get("download_speed")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def upload_speed(self) -> typing.Optional[jsii.Number]:
            '''Upload speed in Mbps.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-link-bandwidth.html#cfn-networkmanager-link-bandwidth-uploadspeed
            '''
            result = self._values.get("upload_speed")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BandwidthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSiteMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "global_network_id": "globalNetworkId",
        "location": "location",
        "tags": "tags",
    },
)
class CfnSiteMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        global_network_id: typing.Optional[builtins.str] = None,
        location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSitePropsMixin.LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSitePropsMixin.

        :param description: A description of your site. Constraints: Maximum length of 256 characters.
        :param global_network_id: The ID of the global network.
        :param location: The site location. This information is used for visualization in the Network Manager console. If you specify the address, the latitude and longitude are automatically calculated. - ``Address`` : The physical address of the site. - ``Latitude`` : The latitude of the site. - ``Longitude`` : The longitude of the site.
        :param tags: The tags for the site.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_site_mixin_props = networkmanager_mixins.CfnSiteMixinProps(
                description="description",
                global_network_id="globalNetworkId",
                location=networkmanager_mixins.CfnSitePropsMixin.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e95ae010650cacfa301924214c8d140177a71c747ae867b62239982b7c6f1737)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if location is not None:
            self._values["location"] = location
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of your site.

        Constraints: Maximum length of 256 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSitePropsMixin.LocationProperty"]]:
        '''The site location.

        This information is used for visualization in the Network Manager console. If you specify the address, the latitude and longitude are automatically calculated.

        - ``Address`` : The physical address of the site.
        - ``Latitude`` : The latitude of the site.
        - ``Longitude`` : The longitude of the site.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-location
        '''
        result = self._values.get("location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSitePropsMixin.LocationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags for the site.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html#cfn-networkmanager-site-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSiteMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSitePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSitePropsMixin",
):
    '''Creates a new site in a global network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-site.html
    :cloudformationResource: AWS::NetworkManager::Site
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_site_props_mixin = networkmanager_mixins.CfnSitePropsMixin(networkmanager_mixins.CfnSiteMixinProps(
            description="description",
            global_network_id="globalNetworkId",
            location=networkmanager_mixins.CfnSitePropsMixin.LocationProperty(
                address="address",
                latitude="latitude",
                longitude="longitude"
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
        props: typing.Union[CfnSiteMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::Site``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfab8962168a725dc833ca7e6a85e9e217f7088d1664a6bcbcb4fb091e12ae40)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30eabb95e4766446c66f0dca8a4d67d2079d34c115ac6617c9fe2d998a5ff937)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70052d39bcde4427a4e5fe4a8c785e178e70e599d29e73a732baae362ea4cae7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSiteMixinProps:
        return typing.cast(CfnSiteMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSitePropsMixin.LocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address": "address",
            "latitude": "latitude",
            "longitude": "longitude",
        },
    )
    class LocationProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[builtins.str] = None,
            latitude: typing.Optional[builtins.str] = None,
            longitude: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a location.

            :param address: The physical address.
            :param latitude: The latitude.
            :param longitude: The longitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                location_property = networkmanager_mixins.CfnSitePropsMixin.LocationProperty(
                    address="address",
                    latitude="latitude",
                    longitude="longitude"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aaa2a86cf9b0f23d1b9cef5287c5cfa576eabd415f313d35271ddb77db87bdd4)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument latitude", value=latitude, expected_type=type_hints["latitude"])
                check_type(argname="argument longitude", value=longitude, expected_type=type_hints["longitude"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if latitude is not None:
                self._values["latitude"] = latitude
            if longitude is not None:
                self._values["longitude"] = longitude

        @builtins.property
        def address(self) -> typing.Optional[builtins.str]:
            '''The physical address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def latitude(self) -> typing.Optional[builtins.str]:
            '''The latitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-latitude
            '''
            result = self._values.get("latitude")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def longitude(self) -> typing.Optional[builtins.str]:
            '''The longitude.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-site-location.html#cfn-networkmanager-site-location-longitude
            '''
            result = self._values.get("longitude")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSiteToSiteVpnAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "network_function_group_name": "networkFunctionGroupName",
        "proposed_network_function_group_change": "proposedNetworkFunctionGroupChange",
        "proposed_segment_change": "proposedSegmentChange",
        "tags": "tags",
        "vpn_connection_arn": "vpnConnectionArn",
    },
)
class CfnSiteToSiteVpnAttachmentMixinProps:
    def __init__(
        self,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        network_function_group_name: typing.Optional[builtins.str] = None,
        proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpn_connection_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSiteToSiteVpnAttachmentPropsMixin.

        :param core_network_id: The ID of a core network where you're creating a site-to-site VPN attachment.
        :param network_function_group_name: The name of the network function group.
        :param proposed_network_function_group_change: Describes proposed changes to a network function group.
        :param proposed_segment_change: Describes a proposed segment change. In some cases, the segment change must first be evaluated and accepted.
        :param tags: The tags associated with the Site-to-Site VPN attachment.
        :param vpn_connection_arn: The ARN of the site-to-site VPN attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_site_to_site_vpn_attachment_mixin_props = networkmanager_mixins.CfnSiteToSiteVpnAttachmentMixinProps(
                core_network_id="coreNetworkId",
                network_function_group_name="networkFunctionGroupName",
                proposed_network_function_group_change=networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                proposed_segment_change=networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpn_connection_arn="vpnConnectionArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf7d975e0e2efb14ca9df466d7d0e265a53dab2963a43d722f159087ac8f6c9)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
            check_type(argname="argument proposed_network_function_group_change", value=proposed_network_function_group_change, expected_type=type_hints["proposed_network_function_group_change"])
            check_type(argname="argument proposed_segment_change", value=proposed_segment_change, expected_type=type_hints["proposed_segment_change"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpn_connection_arn", value=vpn_connection_arn, expected_type=type_hints["vpn_connection_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_network_id is not None:
            self._values["core_network_id"] = core_network_id
        if network_function_group_name is not None:
            self._values["network_function_group_name"] = network_function_group_name
        if proposed_network_function_group_change is not None:
            self._values["proposed_network_function_group_change"] = proposed_network_function_group_change
        if proposed_segment_change is not None:
            self._values["proposed_segment_change"] = proposed_segment_change
        if tags is not None:
            self._values["tags"] = tags
        if vpn_connection_arn is not None:
            self._values["vpn_connection_arn"] = vpn_connection_arn

    @builtins.property
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of a core network where you're creating a site-to-site VPN attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_function_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-networkfunctiongroupname
        '''
        result = self._values.get("network_function_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proposed_network_function_group_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]]:
        '''Describes proposed changes to a network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange
        '''
        result = self._values.get("proposed_network_function_group_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]], result)

    @builtins.property
    def proposed_segment_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty"]]:
        '''Describes a proposed segment change.

        In some cases, the segment change must first be evaluated and accepted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange
        '''
        result = self._values.get("proposed_segment_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the Site-to-Site VPN attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpn_connection_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the site-to-site VPN attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html#cfn-networkmanager-sitetositevpnattachment-vpnconnectionarn
        '''
        result = self._values.get("vpn_connection_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSiteToSiteVpnAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSiteToSiteVpnAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSiteToSiteVpnAttachmentPropsMixin",
):
    '''Creates an Amazon Web Services site-to-site VPN attachment on an edge location of a core network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-sitetositevpnattachment.html
    :cloudformationResource: AWS::NetworkManager::SiteToSiteVpnAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_site_to_site_vpn_attachment_props_mixin = networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin(networkmanager_mixins.CfnSiteToSiteVpnAttachmentMixinProps(
            core_network_id="coreNetworkId",
            network_function_group_name="networkFunctionGroupName",
            proposed_network_function_group_change=networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                attachment_policy_rule_number=123,
                network_function_group_name="networkFunctionGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            proposed_segment_change=networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty(
                attachment_policy_rule_number=123,
                segment_name="segmentName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpn_connection_arn="vpnConnectionArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSiteToSiteVpnAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::SiteToSiteVpnAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2f02ec74bb0c76ece8302b265c8ff46f231b6e334e4e312dfbb64fb22e0c2c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5044449ffcb4e8b66a796414bbdc5b5a687abec847f8d61fc02cb514e0867c0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ae85bf5951b0cf88ed79a1d9556246a1875cd2e30f99c9383aab5f0ca4a4319)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSiteToSiteVpnAttachmentMixinProps:
        return typing.cast(CfnSiteToSiteVpnAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "network_function_group_name": "networkFunctionGroupName",
            "tags": "tags",
        },
    )
    class ProposedNetworkFunctionGroupChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            network_function_group_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes proposed changes to a network function group.

            :param attachment_policy_rule_number: The proposed new attachment policy rule number for the network function group.
            :param network_function_group_name: The proposed name change for the network function group name.
            :param tags: The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_network_function_group_change_property = networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1f241520fd1ba67f5d2dd51284e6bd92b71c7171b5523c5c10a1c90da769edd)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if network_function_group_name is not None:
                self._values["network_function_group_name"] = network_function_group_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The proposed new attachment policy rule number for the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def network_function_group_name(self) -> typing.Optional[builtins.str]:
            '''The proposed name change for the network function group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange-networkfunctiongroupname
            '''
            result = self._values.get("network_function_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-sitetositevpnattachment-proposednetworkfunctiongroupchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedNetworkFunctionGroupChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_segment_change_property = networkmanager_mixins.CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f0a2f2c2a993a76be6983477394d21344bdf590380b206e31efe21808571fd5)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-sitetositevpnattachment-proposedsegmentchange.html#cfn-networkmanager-sitetositevpnattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayPeeringMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "tags": "tags",
        "transit_gateway_arn": "transitGatewayArn",
    },
)
class CfnTransitGatewayPeeringMixinProps:
    def __init__(
        self,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_gateway_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTransitGatewayPeeringPropsMixin.

        :param core_network_id: The ID of the core network.
        :param tags: The list of key-value tags associated with the peering.
        :param transit_gateway_arn: The ARN of the transit gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewaypeering.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_transit_gateway_peering_mixin_props = networkmanager_mixins.CfnTransitGatewayPeeringMixinProps(
                core_network_id="coreNetworkId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_gateway_arn="transitGatewayArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3b7a1e922b09da25c0871ea37e1d3454d8fd8e9d35b08a2826167bab01c8f4)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_gateway_arn", value=transit_gateway_arn, expected_type=type_hints["transit_gateway_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_network_id is not None:
            self._values["core_network_id"] = core_network_id
        if tags is not None:
            self._values["tags"] = tags
        if transit_gateway_arn is not None:
            self._values["transit_gateway_arn"] = transit_gateway_arn

    @builtins.property
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the core network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewaypeering.html#cfn-networkmanager-transitgatewaypeering-corenetworkid
        '''
        result = self._values.get("core_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value tags associated with the peering.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewaypeering.html#cfn-networkmanager-transitgatewaypeering-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transit_gateway_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the transit gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewaypeering.html#cfn-networkmanager-transitgatewaypeering-transitgatewayarn
        '''
        result = self._values.get("transit_gateway_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransitGatewayPeeringMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTransitGatewayPeeringPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayPeeringPropsMixin",
):
    '''Creates a transit gateway peering connection.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewaypeering.html
    :cloudformationResource: AWS::NetworkManager::TransitGatewayPeering
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_transit_gateway_peering_props_mixin = networkmanager_mixins.CfnTransitGatewayPeeringPropsMixin(networkmanager_mixins.CfnTransitGatewayPeeringMixinProps(
            core_network_id="coreNetworkId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_gateway_arn="transitGatewayArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTransitGatewayPeeringMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::TransitGatewayPeering``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99632e08facde9f7d27f166627bebe51624cd03c1c74f9ee40fa7154ae272b18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db65e143cd8e3c4f4cbb6b18e16b747cbc921b7fbcaced11c9c71815d4a643e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e43ce646a4e977bfc8a48a51c3c799d745d263fd1e879532a0e7005f3507addb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTransitGatewayPeeringMixinProps:
        return typing.cast(CfnTransitGatewayPeeringMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayRegistrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "global_network_id": "globalNetworkId",
        "transit_gateway_arn": "transitGatewayArn",
    },
)
class CfnTransitGatewayRegistrationMixinProps:
    def __init__(
        self,
        *,
        global_network_id: typing.Optional[builtins.str] = None,
        transit_gateway_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTransitGatewayRegistrationPropsMixin.

        :param global_network_id: The ID of the global network.
        :param transit_gateway_arn: The Amazon Resource Name (ARN) of the transit gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_transit_gateway_registration_mixin_props = networkmanager_mixins.CfnTransitGatewayRegistrationMixinProps(
                global_network_id="globalNetworkId",
                transit_gateway_arn="transitGatewayArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b249146e714c2a906a2ec02f6110874a417c5e9ead233b73a5453db310d66927)
            check_type(argname="argument global_network_id", value=global_network_id, expected_type=type_hints["global_network_id"])
            check_type(argname="argument transit_gateway_arn", value=transit_gateway_arn, expected_type=type_hints["transit_gateway_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if global_network_id is not None:
            self._values["global_network_id"] = global_network_id
        if transit_gateway_arn is not None:
            self._values["transit_gateway_arn"] = transit_gateway_arn

    @builtins.property
    def global_network_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the global network.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-globalnetworkid
        '''
        result = self._values.get("global_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transit_gateway_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the transit gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html#cfn-networkmanager-transitgatewayregistration-transitgatewayarn
        '''
        result = self._values.get("transit_gateway_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransitGatewayRegistrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTransitGatewayRegistrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayRegistrationPropsMixin",
):
    '''Registers a transit gateway in your global network.

    Not all Regions support transit gateways for global networks. For a list of the supported Regions, see `Region Availability <https://docs.aws.amazon.com/network-manager/latest/tgwnm/what-are-global-networks.html#nm-available-regions>`_ in the *AWS Transit Gateways for Global Networks User Guide* . The transit gateway can be in any of the supported AWS Regions, but it must be owned by the same AWS account that owns the global network. You cannot register a transit gateway in more than one global network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayregistration.html
    :cloudformationResource: AWS::NetworkManager::TransitGatewayRegistration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_transit_gateway_registration_props_mixin = networkmanager_mixins.CfnTransitGatewayRegistrationPropsMixin(networkmanager_mixins.CfnTransitGatewayRegistrationMixinProps(
            global_network_id="globalNetworkId",
            transit_gateway_arn="transitGatewayArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTransitGatewayRegistrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::TransitGatewayRegistration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e423db62cf56af63d32eacc0f04655423ed738fb251cc4ab9368d04d44e2df5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15daa6fbbb5aabb0feaed4446ad3b0c811b521655336d6c7efc48cd1b8c08cd8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c144b412c3e4e9d83758ab5663d4065f11977ce9b13f0982af5e98e52f2e0d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTransitGatewayRegistrationMixinProps:
        return typing.cast(CfnTransitGatewayRegistrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayRouteTableAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "network_function_group_name": "networkFunctionGroupName",
        "peering_id": "peeringId",
        "proposed_network_function_group_change": "proposedNetworkFunctionGroupChange",
        "proposed_segment_change": "proposedSegmentChange",
        "tags": "tags",
        "transit_gateway_route_table_arn": "transitGatewayRouteTableArn",
    },
)
class CfnTransitGatewayRouteTableAttachmentMixinProps:
    def __init__(
        self,
        *,
        network_function_group_name: typing.Optional[builtins.str] = None,
        peering_id: typing.Optional[builtins.str] = None,
        proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        transit_gateway_route_table_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTransitGatewayRouteTableAttachmentPropsMixin.

        :param network_function_group_name: The name of the network function group.
        :param peering_id: The ID of the transit gateway peering.
        :param proposed_network_function_group_change: Describes proposed changes to a network function group.
        :param proposed_segment_change: This property is read-only. Values can't be assigned to it.
        :param tags: The list of key-value pairs associated with the transit gateway route table attachment.
        :param transit_gateway_route_table_arn: The ARN of the transit gateway attachment route table. For example, ``"TransitGatewayRouteTableArn": "arn:aws:ec2:us-west-2:123456789012:transit-gateway-route-table/tgw-rtb-9876543210123456"`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_transit_gateway_route_table_attachment_mixin_props = networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentMixinProps(
                network_function_group_name="networkFunctionGroupName",
                peering_id="peeringId",
                proposed_network_function_group_change=networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                proposed_segment_change=networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                transit_gateway_route_table_arn="transitGatewayRouteTableArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e696b957c68c36c024c1df0c6c40059819dfe11d1f5de8ce6694abf98072da)
            check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
            check_type(argname="argument peering_id", value=peering_id, expected_type=type_hints["peering_id"])
            check_type(argname="argument proposed_network_function_group_change", value=proposed_network_function_group_change, expected_type=type_hints["proposed_network_function_group_change"])
            check_type(argname="argument proposed_segment_change", value=proposed_segment_change, expected_type=type_hints["proposed_segment_change"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument transit_gateway_route_table_arn", value=transit_gateway_route_table_arn, expected_type=type_hints["transit_gateway_route_table_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if network_function_group_name is not None:
            self._values["network_function_group_name"] = network_function_group_name
        if peering_id is not None:
            self._values["peering_id"] = peering_id
        if proposed_network_function_group_change is not None:
            self._values["proposed_network_function_group_change"] = proposed_network_function_group_change
        if proposed_segment_change is not None:
            self._values["proposed_segment_change"] = proposed_segment_change
        if tags is not None:
            self._values["tags"] = tags
        if transit_gateway_route_table_arn is not None:
            self._values["transit_gateway_route_table_arn"] = transit_gateway_route_table_arn

    @builtins.property
    def network_function_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html#cfn-networkmanager-transitgatewayroutetableattachment-networkfunctiongroupname
        '''
        result = self._values.get("network_function_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def peering_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the transit gateway peering.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html#cfn-networkmanager-transitgatewayroutetableattachment-peeringid
        '''
        result = self._values.get("peering_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proposed_network_function_group_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]]:
        '''Describes proposed changes to a network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html#cfn-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange
        '''
        result = self._values.get("proposed_network_function_group_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]], result)

    @builtins.property
    def proposed_segment_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty"]]:
        '''This property is read-only.

        Values can't be assigned to it.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html#cfn-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange
        '''
        result = self._values.get("proposed_segment_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The list of key-value pairs associated with the transit gateway route table attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html#cfn-networkmanager-transitgatewayroutetableattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def transit_gateway_route_table_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the transit gateway attachment route table.

        For example, ``"TransitGatewayRouteTableArn": "arn:aws:ec2:us-west-2:123456789012:transit-gateway-route-table/tgw-rtb-9876543210123456"`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html#cfn-networkmanager-transitgatewayroutetableattachment-transitgatewayroutetablearn
        '''
        result = self._values.get("transit_gateway_route_table_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTransitGatewayRouteTableAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTransitGatewayRouteTableAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin",
):
    '''Creates a transit gateway route table attachment.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-transitgatewayroutetableattachment.html
    :cloudformationResource: AWS::NetworkManager::TransitGatewayRouteTableAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_transit_gateway_route_table_attachment_props_mixin = networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin(networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentMixinProps(
            network_function_group_name="networkFunctionGroupName",
            peering_id="peeringId",
            proposed_network_function_group_change=networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                attachment_policy_rule_number=123,
                network_function_group_name="networkFunctionGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            proposed_segment_change=networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty(
                attachment_policy_rule_number=123,
                segment_name="segmentName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            transit_gateway_route_table_arn="transitGatewayRouteTableArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTransitGatewayRouteTableAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::TransitGatewayRouteTableAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9991f8f86f4db4d08e41a1372b6860065f93dca7c6509917b0ce359fdcceb8b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be7f8351eab2a66668cfcd6d68395bc0e3bac424aeee3dd1d89354421182f89d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12a20a538681ecd79bbeb9c64635d9094f01b7c10559f9e4d5d3af66a4f2b1a1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTransitGatewayRouteTableAttachmentMixinProps:
        return typing.cast(CfnTransitGatewayRouteTableAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "network_function_group_name": "networkFunctionGroupName",
            "tags": "tags",
        },
    )
    class ProposedNetworkFunctionGroupChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            network_function_group_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes proposed changes to a network function group.

            :param attachment_policy_rule_number: The proposed new attachment policy rule number for the network function group.
            :param network_function_group_name: The proposed name change for the network function group name.
            :param tags: The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_network_function_group_change_property = networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfa1345f50416445b0f5afd6344d7d7c3c2d18e8265916167acd5fe15c79a379)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if network_function_group_name is not None:
                self._values["network_function_group_name"] = network_function_group_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The proposed new attachment policy rule number for the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def network_function_group_name(self) -> typing.Optional[builtins.str]:
            '''The proposed name change for the network function group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange-networkfunctiongroupname
            '''
            result = self._values.get("network_function_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-transitgatewayroutetableattachment-proposednetworkfunctiongroupchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedNetworkFunctionGroupChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_segment_change_property = networkmanager_mixins.CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b184447653104aeb50cf6dd4eb6f679e050eabf227bbc7ed6de14c22a4a2077)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange.html#cfn-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange.html#cfn-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange.html#cfn-networkmanager-transitgatewayroutetableattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnVpcAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "core_network_id": "coreNetworkId",
        "options": "options",
        "proposed_network_function_group_change": "proposedNetworkFunctionGroupChange",
        "proposed_segment_change": "proposedSegmentChange",
        "subnet_arns": "subnetArns",
        "tags": "tags",
        "vpc_arn": "vpcArn",
    },
)
class CfnVpcAttachmentMixinProps:
    def __init__(
        self,
        *,
        core_network_id: typing.Optional[builtins.str] = None,
        options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVpcAttachmentPropsMixin.VpcOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVpcAttachmentPropsMixin.

        :param core_network_id: The core network ID.
        :param options: Options for creating the VPC attachment.
        :param proposed_network_function_group_change: Describes proposed changes to a network function group.
        :param proposed_segment_change: Describes a proposed segment change. In some cases, the segment change must first be evaluated and accepted.
        :param subnet_arns: The subnet ARNs.
        :param tags: The tags associated with the VPC attachment.
        :param vpc_arn: The ARN of the VPC attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
            
            cfn_vpc_attachment_mixin_props = networkmanager_mixins.CfnVpcAttachmentMixinProps(
                core_network_id="coreNetworkId",
                options=networkmanager_mixins.CfnVpcAttachmentPropsMixin.VpcOptionsProperty(
                    appliance_mode_support=False,
                    dns_support=False,
                    ipv6_support=False,
                    security_group_referencing_support=False
                ),
                proposed_network_function_group_change=networkmanager_mixins.CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                proposed_segment_change=networkmanager_mixins.CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                ),
                subnet_arns=["subnetArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_arn="vpcArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b54918d70411a2cf9e7988d6be35d5b581245f38de34800c5d8db7f1a777e2)
            check_type(argname="argument core_network_id", value=core_network_id, expected_type=type_hints["core_network_id"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument proposed_network_function_group_change", value=proposed_network_function_group_change, expected_type=type_hints["proposed_network_function_group_change"])
            check_type(argname="argument proposed_segment_change", value=proposed_segment_change, expected_type=type_hints["proposed_segment_change"])
            check_type(argname="argument subnet_arns", value=subnet_arns, expected_type=type_hints["subnet_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_arn", value=vpc_arn, expected_type=type_hints["vpc_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if core_network_id is not None:
            self._values["core_network_id"] = core_network_id
        if options is not None:
            self._values["options"] = options
        if proposed_network_function_group_change is not None:
            self._values["proposed_network_function_group_change"] = proposed_network_function_group_change
        if proposed_segment_change is not None:
            self._values["proposed_segment_change"] = proposed_segment_change
        if subnet_arns is not None:
            self._values["subnet_arns"] = subnet_arns
        if tags is not None:
            self._values["tags"] = tags
        if vpc_arn is not None:
            self._values["vpc_arn"] = vpc_arn

    @builtins.property
    def core_network_id(self) -> typing.Optional[builtins.str]:
        '''The core network ID.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-corenetworkid
        '''
        result = self._values.get("core_network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcAttachmentPropsMixin.VpcOptionsProperty"]]:
        '''Options for creating the VPC attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcAttachmentPropsMixin.VpcOptionsProperty"]], result)

    @builtins.property
    def proposed_network_function_group_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]]:
        '''Describes proposed changes to a network function group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-proposednetworkfunctiongroupchange
        '''
        result = self._values.get("proposed_network_function_group_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty"]], result)

    @builtins.property
    def proposed_segment_change(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty"]]:
        '''Describes a proposed segment change.

        In some cases, the segment change must first be evaluated and accepted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-proposedsegmentchange
        '''
        result = self._values.get("proposed_segment_change")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty"]], result)

    @builtins.property
    def subnet_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The subnet ARNs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-subnetarns
        '''
        result = self._values.get("subnet_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the VPC attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def vpc_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the VPC attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html#cfn-networkmanager-vpcattachment-vpcarn
        '''
        result = self._values.get("vpc_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVpcAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVpcAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnVpcAttachmentPropsMixin",
):
    '''Creates a VPC attachment on an edge location of a core network.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmanager-vpcattachment.html
    :cloudformationResource: AWS::NetworkManager::VpcAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
        
        cfn_vpc_attachment_props_mixin = networkmanager_mixins.CfnVpcAttachmentPropsMixin(networkmanager_mixins.CfnVpcAttachmentMixinProps(
            core_network_id="coreNetworkId",
            options=networkmanager_mixins.CfnVpcAttachmentPropsMixin.VpcOptionsProperty(
                appliance_mode_support=False,
                dns_support=False,
                ipv6_support=False,
                security_group_referencing_support=False
            ),
            proposed_network_function_group_change=networkmanager_mixins.CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                attachment_policy_rule_number=123,
                network_function_group_name="networkFunctionGroupName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            proposed_segment_change=networkmanager_mixins.CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty(
                attachment_policy_rule_number=123,
                segment_name="segmentName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            ),
            subnet_arns=["subnetArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_arn="vpcArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVpcAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::NetworkManager::VpcAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7bf24edf1a0b472751b243fb73acd17dad2a5704025a8ba0114faaacb0f74a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcbe59da0e8d67c6ac770b65aee41f077ebf1fde416a36f0b796e8d39c92f5bc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47f438107b05e4e42516bf098a4880b11c4ad4002f19bea4724f6fe7b8028f9d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVpcAttachmentMixinProps:
        return typing.cast(CfnVpcAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "network_function_group_name": "networkFunctionGroupName",
            "tags": "tags",
        },
    )
    class ProposedNetworkFunctionGroupChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            network_function_group_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes proposed changes to a network function group.

            :param attachment_policy_rule_number: The proposed new attachment policy rule number for the network function group.
            :param network_function_group_name: The proposed name change for the network function group name.
            :param tags: The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposednetworkfunctiongroupchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_network_function_group_change_property = networkmanager_mixins.CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty(
                    attachment_policy_rule_number=123,
                    network_function_group_name="networkFunctionGroupName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e239ed7d0e2dea79fad9c6ac568f9974869b7525dbd068b3a659d2b613f8b91d)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument network_function_group_name", value=network_function_group_name, expected_type=type_hints["network_function_group_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if network_function_group_name is not None:
                self._values["network_function_group_name"] = network_function_group_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The proposed new attachment policy rule number for the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-vpcattachment-proposednetworkfunctiongroupchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def network_function_group_name(self) -> typing.Optional[builtins.str]:
            '''The proposed name change for the network function group name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-vpcattachment-proposednetworkfunctiongroupchange-networkfunctiongroupname
            '''
            result = self._values.get("network_function_group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of proposed changes to the key-value tags associated with the network function group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposednetworkfunctiongroupchange.html#cfn-networkmanager-vpcattachment-proposednetworkfunctiongroupchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedNetworkFunctionGroupChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attachment_policy_rule_number": "attachmentPolicyRuleNumber",
            "segment_name": "segmentName",
            "tags": "tags",
        },
    )
    class ProposedSegmentChangeProperty:
        def __init__(
            self,
            *,
            attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
            segment_name: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a proposed segment change.

            In some cases, the segment change must first be evaluated and accepted.

            :param attachment_policy_rule_number: The rule number in the policy document that applies to this change.
            :param segment_name: The name of the segment to change.
            :param tags: The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                proposed_segment_change_property = networkmanager_mixins.CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty(
                    attachment_policy_rule_number=123,
                    segment_name="segmentName",
                    tags=[CfnTag(
                        key="key",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cb2bc2ed4a2ad23c2c557114a61076185c899156745f6325a3301165b8d512bc)
                check_type(argname="argument attachment_policy_rule_number", value=attachment_policy_rule_number, expected_type=type_hints["attachment_policy_rule_number"])
                check_type(argname="argument segment_name", value=segment_name, expected_type=type_hints["segment_name"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attachment_policy_rule_number is not None:
                self._values["attachment_policy_rule_number"] = attachment_policy_rule_number
            if segment_name is not None:
                self._values["segment_name"] = segment_name
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def attachment_policy_rule_number(self) -> typing.Optional[jsii.Number]:
            '''The rule number in the policy document that applies to this change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html#cfn-networkmanager-vpcattachment-proposedsegmentchange-attachmentpolicyrulenumber
            '''
            result = self._values.get("attachment_policy_rule_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def segment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the segment to change.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html#cfn-networkmanager-vpcattachment-proposedsegmentchange-segmentname
            '''
            result = self._values.get("segment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
            '''The list of key-value tags that changed for the segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-proposedsegmentchange.html#cfn-networkmanager-vpcattachment-proposedsegmentchange-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProposedSegmentChangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_networkmanager.mixins.CfnVpcAttachmentPropsMixin.VpcOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "appliance_mode_support": "applianceModeSupport",
            "dns_support": "dnsSupport",
            "ipv6_support": "ipv6Support",
            "security_group_referencing_support": "securityGroupReferencingSupport",
        },
    )
    class VpcOptionsProperty:
        def __init__(
            self,
            *,
            appliance_mode_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            dns_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ipv6_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            security_group_referencing_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Describes the VPC options.

            :param appliance_mode_support: Indicates whether appliance mode is supported. If enabled, traffic flow between a source and destination use the same Availability Zone for the VPC attachment for the lifetime of that flow. The default value is ``false`` . Default: - false
            :param dns_support: Indicates whether DNS is supported. Default: - true
            :param ipv6_support: Indicates whether IPv6 is supported. Default: - false
            :param security_group_referencing_support: Indicates whether security group referencing is enabled for this VPC attachment. The default is ``true`` . However, at the core network policy-level the default is set to ``false`` . Default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_networkmanager import mixins as networkmanager_mixins
                
                vpc_options_property = networkmanager_mixins.CfnVpcAttachmentPropsMixin.VpcOptionsProperty(
                    appliance_mode_support=False,
                    dns_support=False,
                    ipv6_support=False,
                    security_group_referencing_support=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72ef10f2e89601d5366f728cecb626e17564063f382b9a890d64961d91a07f01)
                check_type(argname="argument appliance_mode_support", value=appliance_mode_support, expected_type=type_hints["appliance_mode_support"])
                check_type(argname="argument dns_support", value=dns_support, expected_type=type_hints["dns_support"])
                check_type(argname="argument ipv6_support", value=ipv6_support, expected_type=type_hints["ipv6_support"])
                check_type(argname="argument security_group_referencing_support", value=security_group_referencing_support, expected_type=type_hints["security_group_referencing_support"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if appliance_mode_support is not None:
                self._values["appliance_mode_support"] = appliance_mode_support
            if dns_support is not None:
                self._values["dns_support"] = dns_support
            if ipv6_support is not None:
                self._values["ipv6_support"] = ipv6_support
            if security_group_referencing_support is not None:
                self._values["security_group_referencing_support"] = security_group_referencing_support

        @builtins.property
        def appliance_mode_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether appliance mode is supported.

            If enabled, traffic flow between a source and destination use the same Availability Zone for the VPC attachment for the lifetime of that flow. The default value is ``false`` .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html#cfn-networkmanager-vpcattachment-vpcoptions-appliancemodesupport
            '''
            result = self._values.get("appliance_mode_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def dns_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether DNS is supported.

            :default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html#cfn-networkmanager-vpcattachment-vpcoptions-dnssupport
            '''
            result = self._values.get("dns_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ipv6_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether IPv6 is supported.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html#cfn-networkmanager-vpcattachment-vpcoptions-ipv6support
            '''
            result = self._values.get("ipv6_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def security_group_referencing_support(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates whether security group referencing is enabled for this VPC attachment.

            The default is ``true`` . However, at the core network policy-level the default is set to ``false`` .

            :default: - true

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkmanager-vpcattachment-vpcoptions.html#cfn-networkmanager-vpcattachment-vpcoptions-securitygroupreferencingsupport
            '''
            result = self._values.get("security_group_referencing_support")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConnectAttachmentMixinProps",
    "CfnConnectAttachmentPropsMixin",
    "CfnConnectPeerMixinProps",
    "CfnConnectPeerPropsMixin",
    "CfnCoreNetworkMixinProps",
    "CfnCoreNetworkPropsMixin",
    "CfnCustomerGatewayAssociationMixinProps",
    "CfnCustomerGatewayAssociationPropsMixin",
    "CfnDeviceMixinProps",
    "CfnDevicePropsMixin",
    "CfnDirectConnectGatewayAttachmentMixinProps",
    "CfnDirectConnectGatewayAttachmentPropsMixin",
    "CfnGlobalNetworkMixinProps",
    "CfnGlobalNetworkPropsMixin",
    "CfnLinkAssociationMixinProps",
    "CfnLinkAssociationPropsMixin",
    "CfnLinkMixinProps",
    "CfnLinkPropsMixin",
    "CfnSiteMixinProps",
    "CfnSitePropsMixin",
    "CfnSiteToSiteVpnAttachmentMixinProps",
    "CfnSiteToSiteVpnAttachmentPropsMixin",
    "CfnTransitGatewayPeeringMixinProps",
    "CfnTransitGatewayPeeringPropsMixin",
    "CfnTransitGatewayRegistrationMixinProps",
    "CfnTransitGatewayRegistrationPropsMixin",
    "CfnTransitGatewayRouteTableAttachmentMixinProps",
    "CfnTransitGatewayRouteTableAttachmentPropsMixin",
    "CfnVpcAttachmentMixinProps",
    "CfnVpcAttachmentPropsMixin",
]

publication.publish()

def _typecheckingstub__376547195bc8d656deb703636f9f64f8708038db64c41d180e9d47bbeabd5b23(
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    edge_location: typing.Optional[builtins.str] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectAttachmentPropsMixin.ConnectAttachmentOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectAttachmentPropsMixin.ProposedSegmentChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transport_attachment_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31091868ce62203d18ad90f9674adc56f24a457f6e01dfa451b58edaf95e00f(
    props: typing.Union[CfnConnectAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48517be6f9e12e0b0cfe781a245fa554f488c2c2366fb5d64bbf38fa2242df9c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de9c3e7021c2ca30a57a90dc0b9e5b49bbb362c20ef2b8426120fefb4bb9a62b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51c1670bc365d5eeca9a16039a1586f3c4416712005d4e4bb530c13028cbd917(
    *,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a69f674d193ada46eb8b214446a112c4ee0b7ef2d7c7ec46601ee718ceaa38a(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32fa32c3f8ce99ce4e71d16aea47b36578079c4649aa034b755b3012dec48348(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcbf63e0d7abd3f7f9f915aac3a0ca1f700e793200e41dd3cb569fd1c44098a7(
    *,
    bgp_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectPeerPropsMixin.BgpOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    connect_attachment_id: typing.Optional[builtins.str] = None,
    core_network_address: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_address: typing.Optional[builtins.str] = None,
    subnet_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acd551b1ee80fed1cb8c1581d83647b2e1b4b4aaba1be9182ae5e215fce5bafa(
    props: typing.Union[CfnConnectPeerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644d295199ed993d3673f03ccddb031c5866c6e8fc8e097c85c40464aabc5042(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a686f3eb0eed1eeba51e7fa7c47b3d0ba2a8ce230aa7c8d24177933fc8fff33(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9445c0dbfc7ac72dcb4bfa3aed0af5dc50ba655499e60b77ab60714a7df434ad(
    *,
    peer_asn: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8931d722114054cbaf69dfe95cd00f5a878306210501f505721dcd84c396f1(
    *,
    core_network_address: typing.Optional[builtins.str] = None,
    core_network_asn: typing.Optional[jsii.Number] = None,
    peer_address: typing.Optional[builtins.str] = None,
    peer_asn: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__299e869edf1b3f4d09daa032df2c8debc3e8b4603f1162c277718650d9f5fb2f(
    *,
    bgp_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectPeerPropsMixin.ConnectPeerBgpConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    core_network_address: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
    peer_address: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6bd70b108158ccd1c98098b78081dfe96c42293e062f8c4e13b9c7736d726b(
    *,
    description: typing.Optional[builtins.str] = None,
    global_network_id: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1695bb1e30476c48bb7aa47b1dfc40925df157e13550f682a15253a98aa4ac43(
    props: typing.Union[CfnCoreNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0f5ae7d0c1e08784122369fe4fedb88623a39cded518b2283edeaca8f6462b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7b7a8a33475c90d1331900f850c8a43c25a8bad2294c9aa3edcba44f1bdf6bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ad1c44e741e7d1abf85b5e555a2e9420bc603bae2a2e105eaa02b7db4c7d11(
    *,
    asn: typing.Optional[jsii.Number] = None,
    edge_location: typing.Optional[builtins.str] = None,
    inside_cidr_blocks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__443a898604abe535a2a8930d4f014536adaff1cacedb66771b63c0b3ef7627de(
    *,
    edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    segments: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCoreNetworkPropsMixin.SegmentsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849d8bb2d896ee58dec98fea77a986026ee3ce92b0bcedf7c972f6c9fba233b9(
    *,
    edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    shared_segments: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8db760f1a7c3fd4830803825adf94bea1dc1a2d69481cd501df93c9f50f6c2f(
    *,
    send_to: typing.Optional[typing.Sequence[builtins.str]] = None,
    send_via: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ed9a64ae116bb65e4a7df06553437f5324ff57df2ec09659242657c42087740(
    *,
    customer_gateway_arn: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    global_network_id: typing.Optional[builtins.str] = None,
    link_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a6a7b302178654dbad33a39d58101b207b9459e49f254c0f3c1bfe69efddb7(
    props: typing.Union[CfnCustomerGatewayAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e0c5dd139a29bd344958e2067a62656c9d6ee79ae20fe3f3ffeb2ede9fe8e5b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d568553a213de861be46b4af9f3337f7f76ca182015105e826804323befe73(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f07472a7614181033710cbfa2896482428060d7fda3f2edd3fbd0191cf91d94(
    *,
    aws_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDevicePropsMixin.AWSLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    global_network_id: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDevicePropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    model: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    site_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    vendor: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9fc2c1090985ba1f0bd043a0da4e65f36d1b891118fe6da0f35546a38cbf0c(
    props: typing.Union[CfnDeviceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bed08d6d1017593e8d6599868554bfbff0424269d9d3288fd1d146f8e2203a4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f5a2693cd376b701156906d2ca87857bf63e037291d1053582d775adc484aee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99130f8abb45860d969816d5b76518688b93013289e448bf9d13a83cfb0086d0(
    *,
    subnet_arn: typing.Optional[builtins.str] = None,
    zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69c563a0ecd65ce0560c4827b5585e0fb528c701509594703118b6fdb61f8ba(
    *,
    address: typing.Optional[builtins.str] = None,
    latitude: typing.Optional[builtins.str] = None,
    longitude: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52670004739b84bc51aa660afeb2710189c1db5cf4c447f519cdd1fa837ca43f(
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    direct_connect_gateway_arn: typing.Optional[builtins.str] = None,
    edge_locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectConnectGatewayAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDirectConnectGatewayAttachmentPropsMixin.ProposedSegmentChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126b3b3ccb453bc4733d220c6e76f4cae594c5afd2cae601825b77ac2e49d7d7(
    props: typing.Union[CfnDirectConnectGatewayAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a603a1fdf7c0f19139a1cfc6f2b435dc00b8573938a662ac9a270dc847a61ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__920ee8fcc4aac74a1b3214921391dd7d3916720196acc8a8f496e97c0dada2c5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f426bac1c5e3541c23f472d2dddf506778e4bb9b6aa8e04c297c57d8e813cc2e(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89fedcd1b2c3385f58b47055514049bacbcee3fb09f88cdba48085563c65c22(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad600e63a37fdf52115193d81a97b7c3b4dcf7889870c917362901e1c8d9a69b(
    *,
    created_at: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c803538d229ce3793a3380ed5174621a8cf816b0a21f4191484ed9b725acf4b(
    props: typing.Union[CfnGlobalNetworkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c502eae070a2f6d5226747ebe85bc7f9befe695947742a731801f16071a23667(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa21671c5d98c1bde78f90589a20fdafbf52b72e3f2bf35175c981e20ad2fa7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21aa55d4825078e8aca0a155d1ab20c880267d01587d0ef807f9f302020421af(
    *,
    device_id: typing.Optional[builtins.str] = None,
    global_network_id: typing.Optional[builtins.str] = None,
    link_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7a1f701951f666f3c902c08d2646e83c6bc5d24d03862cb559313f3d3a09757(
    props: typing.Union[CfnLinkAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e2a4c24d8e76b6bcff3715d36e6b827b775314452a0c1d8fd7b8c5e7bd2c5ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b41ed281d0f16aab2dc401885b1889005f735e61109dba38ad5df71682798f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e6efcb610e2788c67fef0cae70ddc651781cd68f88a3ea79fc21fa6d47afaa(
    *,
    bandwidth: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnLinkPropsMixin.BandwidthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    global_network_id: typing.Optional[builtins.str] = None,
    provider: typing.Optional[builtins.str] = None,
    site_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89542d48303651711c3b8db8d64e86217b8e4975dcbcd61c06abd92d40cc8024(
    props: typing.Union[CfnLinkMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0ca68acbc7a4eb4dbb9517bdbd8e395436fe41764cbe21db14431c523acf32(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d36aaff86281e984eb745e06bc3346128e26434cba02234d652811d7eaa14611(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb7784934d5c0ad890e4f1480e67fb6af2f1bc0462f6d694ba7b8840a953145(
    *,
    download_speed: typing.Optional[jsii.Number] = None,
    upload_speed: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e95ae010650cacfa301924214c8d140177a71c747ae867b62239982b7c6f1737(
    *,
    description: typing.Optional[builtins.str] = None,
    global_network_id: typing.Optional[builtins.str] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSitePropsMixin.LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfab8962168a725dc833ca7e6a85e9e217f7088d1664a6bcbcb4fb091e12ae40(
    props: typing.Union[CfnSiteMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30eabb95e4766446c66f0dca8a4d67d2079d34c115ac6617c9fe2d998a5ff937(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70052d39bcde4427a4e5fe4a8c785e178e70e599d29e73a732baae362ea4cae7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaa2a86cf9b0f23d1b9cef5287c5cfa576eabd415f313d35271ddb77db87bdd4(
    *,
    address: typing.Optional[builtins.str] = None,
    latitude: typing.Optional[builtins.str] = None,
    longitude: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf7d975e0e2efb14ca9df466d7d0e265a53dab2963a43d722f159087ac8f6c9(
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSiteToSiteVpnAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSiteToSiteVpnAttachmentPropsMixin.ProposedSegmentChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpn_connection_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f02ec74bb0c76ece8302b265c8ff46f231b6e334e4e312dfbb64fb22e0c2c4(
    props: typing.Union[CfnSiteToSiteVpnAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5044449ffcb4e8b66a796414bbdc5b5a687abec847f8d61fc02cb514e0867c0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ae85bf5951b0cf88ed79a1d9556246a1875cd2e30f99c9383aab5f0ca4a4319(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f241520fd1ba67f5d2dd51284e6bd92b71c7171b5523c5c10a1c90da769edd(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f0a2f2c2a993a76be6983477394d21344bdf590380b206e31efe21808571fd5(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3b7a1e922b09da25c0871ea37e1d3454d8fd8e9d35b08a2826167bab01c8f4(
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_gateway_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99632e08facde9f7d27f166627bebe51624cd03c1c74f9ee40fa7154ae272b18(
    props: typing.Union[CfnTransitGatewayPeeringMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db65e143cd8e3c4f4cbb6b18e16b747cbc921b7fbcaced11c9c71815d4a643e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e43ce646a4e977bfc8a48a51c3c799d745d263fd1e879532a0e7005f3507addb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b249146e714c2a906a2ec02f6110874a417c5e9ead233b73a5453db310d66927(
    *,
    global_network_id: typing.Optional[builtins.str] = None,
    transit_gateway_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e423db62cf56af63d32eacc0f04655423ed738fb251cc4ab9368d04d44e2df5f(
    props: typing.Union[CfnTransitGatewayRegistrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15daa6fbbb5aabb0feaed4446ad3b0c811b521655336d6c7efc48cd1b8c08cd8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c144b412c3e4e9d83758ab5663d4065f11977ce9b13f0982af5e98e52f2e0d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e696b957c68c36c024c1df0c6c40059819dfe11d1f5de8ce6694abf98072da(
    *,
    network_function_group_name: typing.Optional[builtins.str] = None,
    peering_id: typing.Optional[builtins.str] = None,
    proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTransitGatewayRouteTableAttachmentPropsMixin.ProposedSegmentChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    transit_gateway_route_table_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9991f8f86f4db4d08e41a1372b6860065f93dca7c6509917b0ce359fdcceb8b4(
    props: typing.Union[CfnTransitGatewayRouteTableAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7f8351eab2a66668cfcd6d68395bc0e3bac424aeee3dd1d89354421182f89d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12a20a538681ecd79bbeb9c64635d9094f01b7c10559f9e4d5d3af66a4f2b1a1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa1345f50416445b0f5afd6344d7d7c3c2d18e8265916167acd5fe15c79a379(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b184447653104aeb50cf6dd4eb6f679e050eabf227bbc7ed6de14c22a4a2077(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b54918d70411a2cf9e7988d6be35d5b581245f38de34800c5d8db7f1a777e2(
    *,
    core_network_id: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVpcAttachmentPropsMixin.VpcOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_network_function_group_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVpcAttachmentPropsMixin.ProposedNetworkFunctionGroupChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    proposed_segment_change: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVpcAttachmentPropsMixin.ProposedSegmentChangeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnet_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7bf24edf1a0b472751b243fb73acd17dad2a5704025a8ba0114faaacb0f74a(
    props: typing.Union[CfnVpcAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbe59da0e8d67c6ac770b65aee41f077ebf1fde416a36f0b796e8d39c92f5bc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f438107b05e4e42516bf098a4880b11c4ad4002f19bea4724f6fe7b8028f9d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e239ed7d0e2dea79fad9c6ac568f9974869b7525dbd068b3a659d2b613f8b91d(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    network_function_group_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb2bc2ed4a2ad23c2c557114a61076185c899156745f6325a3301165b8d512bc(
    *,
    attachment_policy_rule_number: typing.Optional[jsii.Number] = None,
    segment_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ef10f2e89601d5366f728cecb626e17564063f382b9a890d64961d91a07f01(
    *,
    appliance_mode_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    dns_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ipv6_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    security_group_referencing_support: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
