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
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnAgentStatusMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_order": "displayOrder",
        "instance_arn": "instanceArn",
        "name": "name",
        "reset_order_number": "resetOrderNumber",
        "state": "state",
        "tags": "tags",
        "type": "type",
    },
)
class CfnAgentStatusMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_order: typing.Optional[jsii.Number] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        reset_order_number: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAgentStatusPropsMixin.

        :param description: The description of the agent status.
        :param display_order: The display order of the agent status.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the agent status.
        :param reset_order_number: A number indicating the reset order of the agent status.
        :param state: The state of the agent status.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "Tags": {"key1":"value1", "key2":"value2"} }.
        :param type: The type of agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_agent_status_mixin_props = connect_mixins.CfnAgentStatusMixinProps(
                description="description",
                display_order=123,
                instance_arn="instanceArn",
                name="name",
                reset_order_number=False,
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea87d5b9a3520e3997f9bdcbdb5f1a1985957369a1ded042005be20b5ac83975)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_order", value=display_order, expected_type=type_hints["display_order"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reset_order_number", value=reset_order_number, expected_type=type_hints["reset_order_number"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_order is not None:
            self._values["display_order"] = display_order
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if reset_order_number is not None:
            self._values["reset_order_number"] = reset_order_number
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_order(self) -> typing.Optional[jsii.Number]:
        '''The display order of the agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-displayorder
        '''
        result = self._values.get("display_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reset_order_number(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A number indicating the reset order of the agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-resetordernumber
        '''
        result = self._values.get("reset_order_number")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of agent status.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html#cfn-connect-agentstatus-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgentStatusMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAgentStatusPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnAgentStatusPropsMixin",
):
    '''Contains information about an agent status.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-agentstatus.html
    :cloudformationResource: AWS::Connect::AgentStatus
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_agent_status_props_mixin = connect_mixins.CfnAgentStatusPropsMixin(connect_mixins.CfnAgentStatusMixinProps(
            description="description",
            display_order=123,
            instance_arn="instanceArn",
            name="name",
            reset_order_number=False,
            state="state",
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
        props: typing.Union[CfnAgentStatusMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::AgentStatus``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d94da73055421bbe8d6dc80e2ddc486d769afef107b48f9e8b31dec21710c1c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__94bbb605322f13161516a5cc98d30baaa6cc215456eab587d6eb0a4bbf431d08)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__818ffdc8dcfafcab85a92cb412f67a0c7a8d2c05d64d9a4d713b3501790fdccd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAgentStatusMixinProps:
        return typing.cast(CfnAgentStatusMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnApprovedOriginMixinProps",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId", "origin": "origin"},
)
class CfnApprovedOriginMixinProps:
    def __init__(
        self,
        *,
        instance_id: typing.Optional[builtins.str] = None,
        origin: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApprovedOriginPropsMixin.

        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param origin: Domain name to be added to the allow-list of the instance. *Maximum* : ``267``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_approved_origin_mixin_props = connect_mixins.CfnApprovedOriginMixinProps(
                instance_id="instanceId",
                origin="origin"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a2d0c80425bb697834f55c94edf804ecf51e0e5d0ac9d126c8680082b69c51)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if origin is not None:
            self._values["origin"] = origin

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html#cfn-connect-approvedorigin-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''Domain name to be added to the allow-list of the instance.

        *Maximum* : ``267``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html#cfn-connect-approvedorigin-origin
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApprovedOriginMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApprovedOriginPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnApprovedOriginPropsMixin",
):
    '''The approved origin for the instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-approvedorigin.html
    :cloudformationResource: AWS::Connect::ApprovedOrigin
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_approved_origin_props_mixin = connect_mixins.CfnApprovedOriginPropsMixin(connect_mixins.CfnApprovedOriginMixinProps(
            instance_id="instanceId",
            origin="origin"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApprovedOriginMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::ApprovedOrigin``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae73093cb19dd7adfdbd99349842306d8f5ebecc58c523e3ecef0aabee2ec46)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d9107fd6e8213d4adfa090cf2790928070adbf6ea333e0fb94dd1443613b51e4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1d44d18ff3cf050d4adfc3a887ffc2d6bb373063ce2963d7944a91bae5c483f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApprovedOriginMixinProps:
        return typing.cast(CfnApprovedOriginMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnContactFlowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "state": "state",
        "tags": "tags",
        "type": "type",
    },
)
class CfnContactFlowMixinProps:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnContactFlowPropsMixin.

        :param content: The content of the flow. For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .
        :param description: The description of the flow.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow.
        :param state: The state of the flow.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The type of the flow. For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_contact_flow_mixin_props = connect_mixins.CfnContactFlowMixinProps(
                content="content",
                description="description",
                instance_arn="instanceArn",
                name="name",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41759aacb7bb794ee58e68bdfb26a185f76b460decaab3039d0bbeb3441deb14)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''The content of the flow.

        For more information, see `Amazon Connect Flow language <https://docs.aws.amazon.com/connect/latest/adminguide/flow-language.html>`_ in the *Amazon Connect Administrator Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the flow.

        For descriptions of the available types, see `Choose a flow type <https://docs.aws.amazon.com/connect/latest/adminguide/create-contact-flow.html#contact-flow-types>`_ in the *Amazon Connect Administrator Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html#cfn-connect-contactflow-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnContactFlowModuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "content": "content",
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "state": "state",
        "tags": "tags",
    },
)
class CfnContactFlowModuleMixinProps:
    def __init__(
        self,
        *,
        content: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnContactFlowModulePropsMixin.

        :param content: The content of the flow module.
        :param description: The description of the flow module.
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the flow module.
        :param state: The state of the flow module.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_contact_flow_module_mixin_props = connect_mixins.CfnContactFlowModuleMixinProps(
                content="content",
                description="description",
                instance_arn="instanceArn",
                name="name",
                state="state",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e09de24bff9dd984d2843d8fe81291715576b5e5fe7733a182bf329f73fbf8)
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if content is not None:
            self._values["content"] = content
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def content(self) -> typing.Optional[builtins.str]:
        '''The content of the flow module.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-content
        '''
        result = self._values.get("content")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow module.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the flow module.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the flow module.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html#cfn-connect-contactflowmodule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowModuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContactFlowModulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnContactFlowModulePropsMixin",
):
    '''Specifies a flow module for an Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowmodule.html
    :cloudformationResource: AWS::Connect::ContactFlowModule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_contact_flow_module_props_mixin = connect_mixins.CfnContactFlowModulePropsMixin(connect_mixins.CfnContactFlowModuleMixinProps(
            content="content",
            description="description",
            instance_arn="instanceArn",
            name="name",
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
        props: typing.Union[CfnContactFlowModuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::ContactFlowModule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856b04157f23dca41234f30f2a48a49efbd1917305fa14957e78937b4f3da23f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__48c5407498e15accd0afcba452b2e107ee1355b6f433eba3e9a7675f79eea99a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c15af3a811f191acde3a0a847036ec37933b825096d531db66bfc21af3bcfb8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContactFlowModuleMixinProps:
        return typing.cast(CfnContactFlowModuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnContactFlowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnContactFlowPropsMixin",
):
    '''Specifies a flow for an Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflow.html
    :cloudformationResource: AWS::Connect::ContactFlow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_contact_flow_props_mixin = connect_mixins.CfnContactFlowPropsMixin(connect_mixins.CfnContactFlowMixinProps(
            content="content",
            description="description",
            instance_arn="instanceArn",
            name="name",
            state="state",
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
        props: typing.Union[CfnContactFlowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::ContactFlow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb860e205ffae32cda0499e7e2480d6e59f1fc08932f24c8c0c909369db1e72)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0571c9f7340f88b0f867862a3fddc44bedb43f92f4b9d587c06b0d01faa4c03f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2ba308e10303a206edc42f7e05118b80d357e8b3704dc85835a3f897a7b8e5a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContactFlowMixinProps:
        return typing.cast(CfnContactFlowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnContactFlowVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"contact_flow_id": "contactFlowId", "description": "description"},
)
class CfnContactFlowVersionMixinProps:
    def __init__(
        self,
        *,
        contact_flow_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnContactFlowVersionPropsMixin.

        :param contact_flow_id: The identifier of the flow.
        :param description: The description of the flow version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_contact_flow_version_mixin_props = connect_mixins.CfnContactFlowVersionMixinProps(
                contact_flow_id="contactFlowId",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4d88913c68a3331275d7304dfb60c2fb634dce2ca6f40afc61850e4187a38f)
            check_type(argname="argument contact_flow_id", value=contact_flow_id, expected_type=type_hints["contact_flow_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_flow_id is not None:
            self._values["contact_flow_id"] = contact_flow_id
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def contact_flow_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowversion.html#cfn-connect-contactflowversion-contactflowid
        '''
        result = self._values.get("contact_flow_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowversion.html#cfn-connect-contactflowversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactFlowVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnContactFlowVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnContactFlowVersionPropsMixin",
):
    '''Creates a version for the specified customer-managed flow within the specified instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-contactflowversion.html
    :cloudformationResource: AWS::Connect::ContactFlowVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_contact_flow_version_props_mixin = connect_mixins.CfnContactFlowVersionPropsMixin(connect_mixins.CfnContactFlowVersionMixinProps(
            contact_flow_id="contactFlowId",
            description="description"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnContactFlowVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::ContactFlowVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48fc78b8d432b27e2b1b3a2439590d5500195880739b12108fdac35c8e3fcb34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e150925111c26d1d8b06149db34a3f1e19e99bbe27e4388a2e53a431501a0bba)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99d237675626041fb362c2c0d446abcc2364bf7ffd5ca7b818a2e3def41722c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnContactFlowVersionMixinProps:
        return typing.cast(CfnContactFlowVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTableAttributeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_table_arn": "dataTableArn",
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "primary": "primary",
        "validation": "validation",
        "value_type": "valueType",
    },
)
class CfnDataTableAttributeMixinProps:
    def __init__(
        self,
        *,
        data_table_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        primary: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataTableAttributePropsMixin.ValidationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataTableAttributePropsMixin.

        :param data_table_arn: 
        :param description: 
        :param instance_arn: 
        :param name: 
        :param primary: 
        :param validation: 
        :param value_type: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_data_table_attribute_mixin_props = connect_mixins.CfnDataTableAttributeMixinProps(
                data_table_arn="dataTableArn",
                description="description",
                instance_arn="instanceArn",
                name="name",
                primary=False,
                validation=connect_mixins.CfnDataTableAttributePropsMixin.ValidationProperty(
                    enum=connect_mixins.CfnDataTableAttributePropsMixin.EnumProperty(
                        strict=False,
                        values=["values"]
                    ),
                    exclusive_maximum=123,
                    exclusive_minimum=123,
                    maximum=123,
                    max_length=123,
                    max_values=123,
                    minimum=123,
                    min_length=123,
                    min_values=123,
                    multiple_of=123
                ),
                value_type="valueType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__284d49a335428429a1419a0e1912fa44ca1a18d86d912f39f94905a2bdb1e978)
            check_type(argname="argument data_table_arn", value=data_table_arn, expected_type=type_hints["data_table_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument primary", value=primary, expected_type=type_hints["primary"])
            check_type(argname="argument validation", value=validation, expected_type=type_hints["validation"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_table_arn is not None:
            self._values["data_table_arn"] = data_table_arn
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if primary is not None:
            self._values["primary"] = primary
        if validation is not None:
            self._values["validation"] = validation
        if value_type is not None:
            self._values["value_type"] = value_type

    @builtins.property
    def data_table_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-datatablearn
        '''
        result = self._values.get("data_table_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def primary(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-primary
        '''
        result = self._values.get("primary")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def validation(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataTableAttributePropsMixin.ValidationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-validation
        '''
        result = self._values.get("validation")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataTableAttributePropsMixin.ValidationProperty"]], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html#cfn-connect-datatableattribute-valuetype
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataTableAttributeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataTableAttributePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTableAttributePropsMixin",
):
    '''Resource Type definition for AWS::Connect::DataTableAttribute.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatableattribute.html
    :cloudformationResource: AWS::Connect::DataTableAttribute
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_data_table_attribute_props_mixin = connect_mixins.CfnDataTableAttributePropsMixin(connect_mixins.CfnDataTableAttributeMixinProps(
            data_table_arn="dataTableArn",
            description="description",
            instance_arn="instanceArn",
            name="name",
            primary=False,
            validation=connect_mixins.CfnDataTableAttributePropsMixin.ValidationProperty(
                enum=connect_mixins.CfnDataTableAttributePropsMixin.EnumProperty(
                    strict=False,
                    values=["values"]
                ),
                exclusive_maximum=123,
                exclusive_minimum=123,
                maximum=123,
                max_length=123,
                max_values=123,
                minimum=123,
                min_length=123,
                min_values=123,
                multiple_of=123
            ),
            value_type="valueType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataTableAttributeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::DataTableAttribute``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5cf6be2f3340bfaece66b9bdc8ed3d5670d11f05a0c240aa6bbf6967b28a88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9c0ff5343398cd48c3f7f094586d676c3c7107b009deb2ca9dcb24b6d55f319)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6757f37e089bf9d085b24c5f6d51e4859f8e6167e1e9b560c082945b98935df)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataTableAttributeMixinProps:
        return typing.cast(CfnDataTableAttributeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTableAttributePropsMixin.EnumProperty",
        jsii_struct_bases=[],
        name_mapping={"strict": "strict", "values": "values"},
    )
    class EnumProperty:
        def __init__(
            self,
            *,
            strict: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param strict: 
            :param values: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-enum.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                enum_property = connect_mixins.CfnDataTableAttributePropsMixin.EnumProperty(
                    strict=False,
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da8e521f54b6d88b5ee32cf529654278a28aa0360392319fd989f147340e6cad)
                check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if strict is not None:
                self._values["strict"] = strict
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def strict(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-enum.html#cfn-connect-datatableattribute-enum-strict
            '''
            result = self._values.get("strict")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-enum.html#cfn-connect-datatableattribute-enum-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnumProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTableAttributePropsMixin.LockVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"attribute": "attribute", "data_table": "dataTable"},
    )
    class LockVersionProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[builtins.str] = None,
            data_table: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param attribute: 
            :param data_table: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-lockversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                lock_version_property = connect_mixins.CfnDataTableAttributePropsMixin.LockVersionProperty(
                    attribute="attribute",
                    data_table="dataTable"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__554a300ab85c6d2c38395a005f3111e85693158d83a62c449a44c1952e4f67b3)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument data_table", value=data_table, expected_type=type_hints["data_table"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if data_table is not None:
                self._values["data_table"] = data_table

        @builtins.property
        def attribute(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-lockversion.html#cfn-connect-datatableattribute-lockversion-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_table(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-lockversion.html#cfn-connect-datatableattribute-lockversion-datatable
            '''
            result = self._values.get("data_table")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LockVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTableAttributePropsMixin.ValidationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enum": "enum",
            "exclusive_maximum": "exclusiveMaximum",
            "exclusive_minimum": "exclusiveMinimum",
            "maximum": "maximum",
            "max_length": "maxLength",
            "max_values": "maxValues",
            "minimum": "minimum",
            "min_length": "minLength",
            "min_values": "minValues",
            "multiple_of": "multipleOf",
        },
    )
    class ValidationProperty:
        def __init__(
            self,
            *,
            enum: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataTableAttributePropsMixin.EnumProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            exclusive_maximum: typing.Optional[jsii.Number] = None,
            exclusive_minimum: typing.Optional[jsii.Number] = None,
            maximum: typing.Optional[jsii.Number] = None,
            max_length: typing.Optional[jsii.Number] = None,
            max_values: typing.Optional[jsii.Number] = None,
            minimum: typing.Optional[jsii.Number] = None,
            min_length: typing.Optional[jsii.Number] = None,
            min_values: typing.Optional[jsii.Number] = None,
            multiple_of: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param enum: 
            :param exclusive_maximum: 
            :param exclusive_minimum: 
            :param maximum: 
            :param max_length: 
            :param max_values: 
            :param minimum: 
            :param min_length: 
            :param min_values: 
            :param multiple_of: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                validation_property = connect_mixins.CfnDataTableAttributePropsMixin.ValidationProperty(
                    enum=connect_mixins.CfnDataTableAttributePropsMixin.EnumProperty(
                        strict=False,
                        values=["values"]
                    ),
                    exclusive_maximum=123,
                    exclusive_minimum=123,
                    maximum=123,
                    max_length=123,
                    max_values=123,
                    minimum=123,
                    min_length=123,
                    min_values=123,
                    multiple_of=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__71d13337c88d4e88c1acb2a387d79e5a830e8efc9d99c48d3f33688c5915b313)
                check_type(argname="argument enum", value=enum, expected_type=type_hints["enum"])
                check_type(argname="argument exclusive_maximum", value=exclusive_maximum, expected_type=type_hints["exclusive_maximum"])
                check_type(argname="argument exclusive_minimum", value=exclusive_minimum, expected_type=type_hints["exclusive_minimum"])
                check_type(argname="argument maximum", value=maximum, expected_type=type_hints["maximum"])
                check_type(argname="argument max_length", value=max_length, expected_type=type_hints["max_length"])
                check_type(argname="argument max_values", value=max_values, expected_type=type_hints["max_values"])
                check_type(argname="argument minimum", value=minimum, expected_type=type_hints["minimum"])
                check_type(argname="argument min_length", value=min_length, expected_type=type_hints["min_length"])
                check_type(argname="argument min_values", value=min_values, expected_type=type_hints["min_values"])
                check_type(argname="argument multiple_of", value=multiple_of, expected_type=type_hints["multiple_of"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enum is not None:
                self._values["enum"] = enum
            if exclusive_maximum is not None:
                self._values["exclusive_maximum"] = exclusive_maximum
            if exclusive_minimum is not None:
                self._values["exclusive_minimum"] = exclusive_minimum
            if maximum is not None:
                self._values["maximum"] = maximum
            if max_length is not None:
                self._values["max_length"] = max_length
            if max_values is not None:
                self._values["max_values"] = max_values
            if minimum is not None:
                self._values["minimum"] = minimum
            if min_length is not None:
                self._values["min_length"] = min_length
            if min_values is not None:
                self._values["min_values"] = min_values
            if multiple_of is not None:
                self._values["multiple_of"] = multiple_of

        @builtins.property
        def enum(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataTableAttributePropsMixin.EnumProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-enum
            '''
            result = self._values.get("enum")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataTableAttributePropsMixin.EnumProperty"]], result)

        @builtins.property
        def exclusive_maximum(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-exclusivemaximum
            '''
            result = self._values.get("exclusive_maximum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def exclusive_minimum(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-exclusiveminimum
            '''
            result = self._values.get("exclusive_minimum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def maximum(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-maximum
            '''
            result = self._values.get("maximum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_length(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-maxlength
            '''
            result = self._values.get("max_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_values(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-maxvalues
            '''
            result = self._values.get("max_values")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minimum(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-minimum
            '''
            result = self._values.get("minimum")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_length(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-minlength
            '''
            result = self._values.get("min_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_values(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-minvalues
            '''
            result = self._values.get("min_values")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def multiple_of(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatableattribute-validation.html#cfn-connect-datatableattribute-validation-multipleof
            '''
            result = self._values.get("multiple_of")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTableMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "status": "status",
        "tags": "tags",
        "time_zone": "timeZone",
        "value_lock_level": "valueLockLevel",
    },
)
class CfnDataTableMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
        value_lock_level: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataTablePropsMixin.

        :param description: The description of the Data Table.
        :param instance_arn: The identifier of the Amazon Connect instance.
        :param name: The name of the Data Table.
        :param status: The status of the Data Table.
        :param tags: One or more tags.
        :param time_zone: The time zone of the Data Table.
        :param value_lock_level: The value lock level of the Data Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_data_table_mixin_props = connect_mixins.CfnDataTableMixinProps(
                description="description",
                instance_arn="instanceArn",
                name="name",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_zone="timeZone",
                value_lock_level="valueLockLevel"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6ff5f5f586e687f18973cf961e747c5f49ffab67f65f71cf2b29e3adef9087)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument value_lock_level", value=value_lock_level, expected_type=type_hints["value_lock_level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if time_zone is not None:
            self._values["time_zone"] = time_zone
        if value_lock_level is not None:
            self._values["value_lock_level"] = value_lock_level

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Data Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Data Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the Data Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''One or more tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone of the Data Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-timezone
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value_lock_level(self) -> typing.Optional[builtins.str]:
        '''The value lock level of the Data Table.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html#cfn-connect-datatable-valuelocklevel
        '''
        result = self._values.get("value_lock_level")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataTableMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataTablePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTablePropsMixin",
):
    '''Resource Type definition for AWS::Connect::DataTable.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-datatable.html
    :cloudformationResource: AWS::Connect::DataTable
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_data_table_props_mixin = connect_mixins.CfnDataTablePropsMixin(connect_mixins.CfnDataTableMixinProps(
            description="description",
            instance_arn="instanceArn",
            name="name",
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_zone="timeZone",
            value_lock_level="valueLockLevel"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataTableMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::DataTable``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3daeafe37708f1eea8f6cb7b284f92614dda4403c5dc317ebfef29a1b4dfec3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ed11b1d4b0d10bce1f92972d6a04bb3f03be8cee16393770bcab08da7ca2927)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df1a4649af02f29698d3f882f3f8b7a20633aaa8485553edcfbb5834f67292a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataTableMixinProps:
        return typing.cast(CfnDataTableMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnDataTablePropsMixin.LockVersionProperty",
        jsii_struct_bases=[],
        name_mapping={"data_table": "dataTable"},
    )
    class LockVersionProperty:
        def __init__(self, *, data_table: typing.Optional[builtins.str] = None) -> None:
            '''The lock version of the Data Table.

            :param data_table: The data table for the lock version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatable-lockversion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                lock_version_property = connect_mixins.CfnDataTablePropsMixin.LockVersionProperty(
                    data_table="dataTable"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11f1a58e8beee0f65e84fe4f9689eda54e3f4634945e55ff4cda30601b2301e6)
                check_type(argname="argument data_table", value=data_table, expected_type=type_hints["data_table"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_table is not None:
                self._values["data_table"] = data_table

        @builtins.property
        def data_table(self) -> typing.Optional[builtins.str]:
            '''The data table for the lock version.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-datatable-lockversion.html#cfn-connect-datatable-lockversion-datatable
            '''
            result = self._values.get("data_table")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LockVersionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEmailAddressMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alias_configurations": "aliasConfigurations",
        "description": "description",
        "display_name": "displayName",
        "email_address": "emailAddress",
        "instance_arn": "instanceArn",
        "tags": "tags",
    },
)
class CfnEmailAddressMixinProps:
    def __init__(
        self,
        *,
        alias_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEmailAddressPropsMixin.AliasConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        email_address: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEmailAddressPropsMixin.

        :param alias_configurations: A list of alias configurations for this email address, showing which email addresses forward to this primary address. Each configuration contains the email address ID of an alias that forwards emails to this address.
        :param description: The description of the email address.
        :param display_name: The display name of email address.
        :param email_address: The email address, including the domain.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_email_address_mixin_props = connect_mixins.CfnEmailAddressMixinProps(
                alias_configurations=[connect_mixins.CfnEmailAddressPropsMixin.AliasConfigurationProperty(
                    email_address_arn="emailAddressArn"
                )],
                description="description",
                display_name="displayName",
                email_address="emailAddress",
                instance_arn="instanceArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__333d0036ebf9196aac54461fc944192183701c4485bb4982caaebf0d9363ae7b)
            check_type(argname="argument alias_configurations", value=alias_configurations, expected_type=type_hints["alias_configurations"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias_configurations is not None:
            self._values["alias_configurations"] = alias_configurations
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if email_address is not None:
            self._values["email_address"] = email_address
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def alias_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailAddressPropsMixin.AliasConfigurationProperty"]]]]:
        '''A list of alias configurations for this email address, showing which email addresses forward to this primary address.

        Each configuration contains the email address ID of an alias that forwards emails to this address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html#cfn-connect-emailaddress-aliasconfigurations
        '''
        result = self._values.get("alias_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEmailAddressPropsMixin.AliasConfigurationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the email address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html#cfn-connect-emailaddress-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name of email address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html#cfn-connect-emailaddress-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def email_address(self) -> typing.Optional[builtins.str]:
        '''The email address, including the domain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html#cfn-connect-emailaddress-emailaddress
        '''
        result = self._values.get("email_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html#cfn-connect-emailaddress-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html#cfn-connect-emailaddress-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailAddressMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEmailAddressPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEmailAddressPropsMixin",
):
    '''Create new email address in the specified Amazon Connect instance.

    For more information about email addresses, see `Create email addresses <https://docs.aws.amazon.com/connect/latest/adminguide/create-email-address1.html>`_ in the Amazon Connect Administrator Guide.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-emailaddress.html
    :cloudformationResource: AWS::Connect::EmailAddress
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_email_address_props_mixin = connect_mixins.CfnEmailAddressPropsMixin(connect_mixins.CfnEmailAddressMixinProps(
            alias_configurations=[connect_mixins.CfnEmailAddressPropsMixin.AliasConfigurationProperty(
                email_address_arn="emailAddressArn"
            )],
            description="description",
            display_name="displayName",
            email_address="emailAddress",
            instance_arn="instanceArn",
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
        props: typing.Union[CfnEmailAddressMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::EmailAddress``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc5b683c4d4e0c4859b83a930537fd7f7db1ed3058d2d8844a2db90cc4b98bf2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d4176ac3179bcbbfd5eea60c5891d84869764278dcc38737e92896a3076f983)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e735cd549c668955b733b37a9eb29b75a7110d1a3c187e1e45ff38a2251b870)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEmailAddressMixinProps:
        return typing.cast(CfnEmailAddressMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEmailAddressPropsMixin.AliasConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"email_address_arn": "emailAddressArn"},
    )
    class AliasConfigurationProperty:
        def __init__(
            self,
            *,
            email_address_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information of an email alias.

            :param email_address_arn: The identifier of the email address alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-emailaddress-aliasconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                alias_configuration_property = connect_mixins.CfnEmailAddressPropsMixin.AliasConfigurationProperty(
                    email_address_arn="emailAddressArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a3cb19a07a28971b989a7e63c3729fabba3fb08980f037205852dacf5fbec33)
                check_type(argname="argument email_address_arn", value=email_address_arn, expected_type=type_hints["email_address_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_address_arn is not None:
                self._values["email_address_arn"] = email_address_arn

        @builtins.property
        def email_address_arn(self) -> typing.Optional[builtins.str]:
            '''The identifier of the email address alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-emailaddress-aliasconfiguration.html#cfn-connect-emailaddress-aliasconfiguration-emailaddressarn
            '''
            result = self._values.get("email_address_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AliasConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "auto_evaluation_configuration": "autoEvaluationConfiguration",
        "description": "description",
        "instance_arn": "instanceArn",
        "items": "items",
        "language_configuration": "languageConfiguration",
        "scoring_strategy": "scoringStrategy",
        "status": "status",
        "tags": "tags",
        "target_configuration": "targetConfiguration",
        "title": "title",
    },
)
class CfnEvaluationFormMixinProps:
    def __init__(
        self,
        *,
        auto_evaluation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        language_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scoring_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.ScoringStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnEvaluationFormPropsMixin.

        :param auto_evaluation_configuration: The automatic evaluation configuration of an evaluation form.
        :param description: The description of the evaluation form. *Length Constraints* : Minimum length of 0. Maximum length of 1024.
        :param instance_arn: The identifier of the Amazon Connect instance.
        :param items: Items that are part of the evaluation form. The total number of sections and questions must not exceed 100 each. Questions must be contained in a section. *Minimum size* : 1 *Maximum size* : 100
        :param language_configuration: 
        :param scoring_strategy: A scoring strategy of the evaluation form.
        :param status: The status of the evaluation form. *Allowed values* : ``DRAFT`` | ``ACTIVE`` Default: - "DRAFT"
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        :param target_configuration: 
        :param title: A title of the evaluation form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            # evaluation_form_section_property_: connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty
            
            cfn_evaluation_form_mixin_props = connect_mixins.CfnEvaluationFormMixinProps(
                auto_evaluation_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty(
                    enabled=False
                ),
                description="description",
                instance_arn="instanceArn",
                items=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty(
                    section=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty(
                        instructions="instructions",
                        items=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty(
                            question=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty(
                                enablement=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                                    action="action",
                                    condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                                        operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                                            expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                                comparator="comparator",
                                                source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                                    ref_id="refId",
                                                    type="type"
                                                ),
                                                values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                                    ref_id="refId",
                                                    type="type"
                                                )]
                                            )
                                        )],
                                        operator="operator"
                                    ),
                                    default_action="defaultAction"
                                ),
                                instructions="instructions",
                                not_applicable_enabled=False,
                                question_type="questionType",
                                question_type_properties=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                                    multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            ),
                                            default_option_ref_ids=["defaultOptionRefIds"],
                                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                                rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                                    category="category",
                                                    condition="condition",
                                                    option_ref_ids=["optionRefIds"]
                                                )
                                            )]
                                        ),
                                        display_as="displayAs",
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                                            ref_id="refId",
                                            text="text"
                                        )]
                                    ),
                                    numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            ),
                                            property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                                label="label"
                                            )
                                        ),
                                        max_value=123,
                                        min_value=123,
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                                            automatic_fail=False,
                                            automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                                target_section="targetSection"
                                            ),
                                            max_value=123,
                                            min_value=123,
                                            score=123
                                        )]
                                    ),
                                    single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            ),
                                            default_option_ref_id="defaultOptionRefId",
                                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                                rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                                    category="category",
                                                    condition="condition",
                                                    option_ref_id="optionRefId"
                                                )
                                            )]
                                        ),
                                        display_as="displayAs",
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                                            automatic_fail=False,
                                            automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                                target_section="targetSection"
                                            ),
                                            ref_id="refId",
                                            score=123,
                                            text="text"
                                        )]
                                    ),
                                    text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            )
                                        )
                                    )
                                ),
                                ref_id="refId",
                                title="title",
                                weight=123
                            ),
                            section=evaluation_form_section_property_
                        )],
                        ref_id="refId",
                        title="title",
                        weight=123
                    )
                )],
                language_configuration=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty(
                    form_language="formLanguage"
                ),
                scoring_strategy=connect_mixins.CfnEvaluationFormPropsMixin.ScoringStrategyProperty(
                    mode="mode",
                    status="status"
                ),
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_configuration=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty(
                    contact_interaction_type="contactInteractionType"
                ),
                title="title"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__741d59b1f8ff8308e9793e7581026c1643be954ee87377493e259fabf972dcf7)
            check_type(argname="argument auto_evaluation_configuration", value=auto_evaluation_configuration, expected_type=type_hints["auto_evaluation_configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument items", value=items, expected_type=type_hints["items"])
            check_type(argname="argument language_configuration", value=language_configuration, expected_type=type_hints["language_configuration"])
            check_type(argname="argument scoring_strategy", value=scoring_strategy, expected_type=type_hints["scoring_strategy"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_configuration", value=target_configuration, expected_type=type_hints["target_configuration"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_evaluation_configuration is not None:
            self._values["auto_evaluation_configuration"] = auto_evaluation_configuration
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if items is not None:
            self._values["items"] = items
        if language_configuration is not None:
            self._values["language_configuration"] = language_configuration
        if scoring_strategy is not None:
            self._values["scoring_strategy"] = scoring_strategy
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if target_configuration is not None:
            self._values["target_configuration"] = target_configuration
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def auto_evaluation_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty"]]:
        '''The automatic evaluation configuration of an evaluation form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-autoevaluationconfiguration
        '''
        result = self._values.get("auto_evaluation_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the evaluation form.

        *Length Constraints* : Minimum length of 0. Maximum length of 1024.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def items(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty"]]]]:
        '''Items that are part of the evaluation form.

        The total number of sections and questions must not exceed 100 each. Questions must be contained in a section.

        *Minimum size* : 1

        *Maximum size* : 100

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-items
        '''
        result = self._values.get("items")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty"]]]], result)

    @builtins.property
    def language_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-languageconfiguration
        '''
        result = self._values.get("language_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty"]], result)

    @builtins.property
    def scoring_strategy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.ScoringStrategyProperty"]]:
        '''A scoring strategy of the evaluation form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-scoringstrategy
        '''
        result = self._values.get("scoring_strategy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.ScoringStrategyProperty"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the evaluation form.

        *Allowed values* : ``DRAFT`` | ``ACTIVE``

        :default: - "DRAFT"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-targetconfiguration
        '''
        result = self._values.get("target_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty"]], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        '''A title of the evaluation form.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html#cfn-connect-evaluationform-title
        '''
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEvaluationFormMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEvaluationFormPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin",
):
    '''Creates an evaluation form for the specified Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-evaluationform.html
    :cloudformationResource: AWS::Connect::EvaluationForm
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        # evaluation_form_section_property_: connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty
        
        cfn_evaluation_form_props_mixin = connect_mixins.CfnEvaluationFormPropsMixin(connect_mixins.CfnEvaluationFormMixinProps(
            auto_evaluation_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty(
                enabled=False
            ),
            description="description",
            instance_arn="instanceArn",
            items=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty(
                section=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty(
                    instructions="instructions",
                    items=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty(
                        question=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty(
                            enablement=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                                action="action",
                                condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                                    operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                                        expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                            comparator="comparator",
                                            source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                                ref_id="refId",
                                                type="type"
                                            ),
                                            values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                                ref_id="refId",
                                                type="type"
                                            )]
                                        )
                                    )],
                                    operator="operator"
                                ),
                                default_action="defaultAction"
                            ),
                            instructions="instructions",
                            not_applicable_enabled=False,
                            question_type="questionType",
                            question_type_properties=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                                multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        ),
                                        default_option_ref_ids=["defaultOptionRefIds"],
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                            rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                                category="category",
                                                condition="condition",
                                                option_ref_ids=["optionRefIds"]
                                            )
                                        )]
                                    ),
                                    display_as="displayAs",
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                                        ref_id="refId",
                                        text="text"
                                    )]
                                ),
                                numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        ),
                                        property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                            label="label"
                                        )
                                    ),
                                    max_value=123,
                                    min_value=123,
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                                        automatic_fail=False,
                                        automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                            target_section="targetSection"
                                        ),
                                        max_value=123,
                                        min_value=123,
                                        score=123
                                    )]
                                ),
                                single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        ),
                                        default_option_ref_id="defaultOptionRefId",
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                            rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                                category="category",
                                                condition="condition",
                                                option_ref_id="optionRefId"
                                            )
                                        )]
                                    ),
                                    display_as="displayAs",
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                                        automatic_fail=False,
                                        automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                            target_section="targetSection"
                                        ),
                                        ref_id="refId",
                                        score=123,
                                        text="text"
                                    )]
                                ),
                                text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        )
                                    )
                                )
                            ),
                            ref_id="refId",
                            title="title",
                            weight=123
                        ),
                        section=evaluation_form_section_property_
                    )],
                    ref_id="refId",
                    title="title",
                    weight=123
                )
            )],
            language_configuration=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty(
                form_language="formLanguage"
            ),
            scoring_strategy=connect_mixins.CfnEvaluationFormPropsMixin.ScoringStrategyProperty(
                mode="mode",
                status="status"
            ),
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_configuration=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty(
                contact_interaction_type="contactInteractionType"
            ),
            title="title"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnEvaluationFormMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::EvaluationForm``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ecf2cca2098b0182240ff981fa486afa1ba8122613906811842512b4af33f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87acea13f1ca0569900470beacceed7711aa7d26c08c67cfe77e234412d9428b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2bcf60337ba05daff300eb986b06f8a4cd10b350e30646e9fcebeb5070dcc36)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEvaluationFormMixinProps:
        return typing.cast(CfnEvaluationFormMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AutoEvaluationConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Configuration information about automated evaluations.

            :param enabled: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-autoevaluationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                auto_evaluation_configuration_property = connect_mixins.CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4fef8bbf0c55eb4b3d298166f4b531564fa6b0f1f60d13f1fe2b23696976f94)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-autoevaluationconfiguration.html#cfn-connect-evaluationform-autoevaluationconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoEvaluationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"target_section": "targetSection"},
    )
    class AutomaticFailConfigurationProperty:
        def __init__(
            self,
            *,
            target_section: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about automatic fail configuration for an evaluation form.

            :param target_section: The referenceId of the target section for auto failure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-automaticfailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                automatic_fail_configuration_property = connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                    target_section="targetSection"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__678457b89d206c0f98eb6a07687b6906c7df47b285a03cf47418fb3eb3e5a8d2)
                check_type(argname="argument target_section", value=target_section, expected_type=type_hints["target_section"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if target_section is not None:
                self._values["target_section"] = target_section

        @builtins.property
        def target_section(self) -> typing.Optional[builtins.str]:
            '''The referenceId of the target section for auto failure.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-automaticfailconfiguration.html#cfn-connect-evaluationform-automaticfailconfiguration-targetsection
            '''
            result = self._values.get("target_section")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutomaticFailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty",
        jsii_struct_bases=[],
        name_mapping={"section": "section"},
    )
    class EvaluationFormBaseItemProperty:
        def __init__(
            self,
            *,
            section: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An item at the root level.

            All items must be sections.

            :param section: A subsection or inner section of an item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformbaseitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # evaluation_form_section_property_: connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty
                
                evaluation_form_base_item_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty(
                    section=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty(
                        instructions="instructions",
                        items=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty(
                            question=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty(
                                enablement=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                                    action="action",
                                    condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                                        operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                                            expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                                comparator="comparator",
                                                source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                                    ref_id="refId",
                                                    type="type"
                                                ),
                                                values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                                    ref_id="refId",
                                                    type="type"
                                                )]
                                            )
                                        )],
                                        operator="operator"
                                    ),
                                    default_action="defaultAction"
                                ),
                                instructions="instructions",
                                not_applicable_enabled=False,
                                question_type="questionType",
                                question_type_properties=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                                    multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            ),
                                            default_option_ref_ids=["defaultOptionRefIds"],
                                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                                rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                                    category="category",
                                                    condition="condition",
                                                    option_ref_ids=["optionRefIds"]
                                                )
                                            )]
                                        ),
                                        display_as="displayAs",
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                                            ref_id="refId",
                                            text="text"
                                        )]
                                    ),
                                    numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            ),
                                            property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                                label="label"
                                            )
                                        ),
                                        max_value=123,
                                        min_value=123,
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                                            automatic_fail=False,
                                            automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                                target_section="targetSection"
                                            ),
                                            max_value=123,
                                            min_value=123,
                                            score=123
                                        )]
                                    ),
                                    single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            ),
                                            default_option_ref_id="defaultOptionRefId",
                                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                                rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                                    category="category",
                                                    condition="condition",
                                                    option_ref_id="optionRefId"
                                                )
                                            )]
                                        ),
                                        display_as="displayAs",
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                                            automatic_fail=False,
                                            automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                                target_section="targetSection"
                                            ),
                                            ref_id="refId",
                                            score=123,
                                            text="text"
                                        )]
                                    ),
                                    text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                                source_type="sourceType"
                                            )
                                        )
                                    )
                                ),
                                ref_id="refId",
                                title="title",
                                weight=123
                            ),
                            section=evaluation_form_section_property_
                        )],
                        ref_id="refId",
                        title="title",
                        weight=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05d6eab10fb5ba01e9f9341bed34f4b5fbe70cf0aaa083ba286bce6f87579809)
                check_type(argname="argument section", value=section, expected_type=type_hints["section"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if section is not None:
                self._values["section"] = section

        @builtins.property
        def section(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty"]]:
            '''A subsection or inner section of an item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformbaseitem.html#cfn-connect-evaluationform-evaluationformbaseitem-section
            '''
            result = self._values.get("section")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormBaseItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression"},
    )
    class EvaluationFormItemEnablementConditionOperandProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An operand of the enablement condition.

            :param expression: An expression of the enablement condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementconditionoperand.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_item_enablement_condition_operand_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                    expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                        comparator="comparator",
                        source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                            ref_id="refId",
                            type="type"
                        ),
                        values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                            ref_id="refId",
                            type="type"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9fbc943951aeea6b57ec68919599f2ee796f4ce88186311e2cd73a25beb9de4a)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression

        @builtins.property
        def expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty"]]:
            '''An expression of the enablement condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementconditionoperand.html#cfn-connect-evaluationform-evaluationformitemenablementconditionoperand-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemEnablementConditionOperandProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"operands": "operands", "operator": "operator"},
    )
    class EvaluationFormItemEnablementConditionProperty:
        def __init__(
            self,
            *,
            operands: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            operator: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A condition for item enablement.

            :param operands: Operands of the enablement condition.
            :param operator: The operator to be used to be applied to operands if more than one provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_item_enablement_condition_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                    operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                        expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                            comparator="comparator",
                            source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                ref_id="refId",
                                type="type"
                            ),
                            values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                ref_id="refId",
                                type="type"
                            )]
                        )
                    )],
                    operator="operator"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a8a244223e0066b4a781c530a165a2f14acf2a76e962eaeb6253bab2fb5d807)
                check_type(argname="argument operands", value=operands, expected_type=type_hints["operands"])
                check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if operands is not None:
                self._values["operands"] = operands
            if operator is not None:
                self._values["operator"] = operator

        @builtins.property
        def operands(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty"]]]]:
            '''Operands of the enablement condition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementcondition.html#cfn-connect-evaluationform-evaluationformitemenablementcondition-operands
            '''
            result = self._values.get("operands")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty"]]]], result)

        @builtins.property
        def operator(self) -> typing.Optional[builtins.str]:
            '''The operator to be used to be applied to operands if more than one provided.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementcondition.html#cfn-connect-evaluationform-evaluationformitemenablementcondition-operator
            '''
            result = self._values.get("operator")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemEnablementConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "condition": "condition",
            "default_action": "defaultAction",
        },
    )
    class EvaluationFormItemEnablementConfigurationProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_action: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An item enablement configuration.

            :param action: An enablement action that if condition is satisfied.
            :param condition: A condition for item enablement configuration.
            :param default_action: An enablement action that if condition is not satisfied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_item_enablement_configuration_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                    action="action",
                    condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                        operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                            expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                comparator="comparator",
                                source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                    ref_id="refId",
                                    type="type"
                                ),
                                values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                    ref_id="refId",
                                    type="type"
                                )]
                            )
                        )],
                        operator="operator"
                    ),
                    default_action="defaultAction"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__380b8409fbde3191a6de09d7c1f3d7d7287c0f322711799c66779e0d8c83ead4)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if condition is not None:
                self._values["condition"] = condition
            if default_action is not None:
                self._values["default_action"] = default_action

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''An enablement action that if condition is satisfied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementconfiguration.html#cfn-connect-evaluationform-evaluationformitemenablementconfiguration-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty"]]:
            '''A condition for item enablement configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementconfiguration.html#cfn-connect-evaluationform-evaluationformitemenablementconfiguration-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty"]], result)

        @builtins.property
        def default_action(self) -> typing.Optional[builtins.str]:
            '''An enablement action that if condition is not satisfied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementconfiguration.html#cfn-connect-evaluationform-evaluationformitemenablementconfiguration-defaultaction
            '''
            result = self._values.get("default_action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemEnablementConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "comparator": "comparator",
            "source": "source",
            "values": "values",
        },
    )
    class EvaluationFormItemEnablementExpressionProperty:
        def __init__(
            self,
            *,
            comparator: typing.Optional[builtins.str] = None,
            source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''An expression that defines a basic building block of conditional enablement.

            :param comparator: A comparator to be used against list of values.
            :param source: A source item of enablement expression.
            :param values: A list of values from source item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_item_enablement_expression_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                    comparator="comparator",
                    source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                        ref_id="refId",
                        type="type"
                    ),
                    values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                        ref_id="refId",
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f76e6958a1d309b95d0185a94d5f9a9a9f1544c74c696a59b5f01f5bcafe51e6)
                check_type(argname="argument comparator", value=comparator, expected_type=type_hints["comparator"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if comparator is not None:
                self._values["comparator"] = comparator
            if source is not None:
                self._values["source"] = source
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def comparator(self) -> typing.Optional[builtins.str]:
            '''A comparator to be used against list of values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementexpression.html#cfn-connect-evaluationform-evaluationformitemenablementexpression-comparator
            '''
            result = self._values.get("comparator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty"]]:
            '''A source item of enablement expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementexpression.html#cfn-connect-evaluationform-evaluationformitemenablementexpression-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty"]], result)

        @builtins.property
        def values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty"]]]]:
            '''A list of values from source item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementexpression.html#cfn-connect-evaluationform-evaluationformitemenablementexpression-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemEnablementExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"ref_id": "refId", "type": "type"},
    )
    class EvaluationFormItemEnablementSourceProperty:
        def __init__(
            self,
            *,
            ref_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An enablement expression source item.

            :param ref_id: A referenceId of the source item.
            :param type: A type of source item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_item_enablement_source_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                    ref_id="refId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07405088fbad04d37acc0fd2e251407fd6a93c1a9395ef3144adc95710e0a36a)
                check_type(argname="argument ref_id", value=ref_id, expected_type=type_hints["ref_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ref_id is not None:
                self._values["ref_id"] = ref_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def ref_id(self) -> typing.Optional[builtins.str]:
            '''A referenceId of the source item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementsource.html#cfn-connect-evaluationform-evaluationformitemenablementsource-refid
            '''
            result = self._values.get("ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''A type of source item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementsource.html#cfn-connect-evaluationform-evaluationformitemenablementsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemEnablementSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty",
        jsii_struct_bases=[],
        name_mapping={"ref_id": "refId", "type": "type"},
    )
    class EvaluationFormItemEnablementSourceValueProperty:
        def __init__(
            self,
            *,
            ref_id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An enablement expression source value.

            :param ref_id: A referenceId of the source value.
            :param type: A type of source item value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementsourcevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_item_enablement_source_value_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                    ref_id="refId",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5524544ac0c995d807fbf32c810a11be5f2e2ff96a29aabe3370ed3e62b73ec0)
                check_type(argname="argument ref_id", value=ref_id, expected_type=type_hints["ref_id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ref_id is not None:
                self._values["ref_id"] = ref_id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def ref_id(self) -> typing.Optional[builtins.str]:
            '''A referenceId of the source value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementsourcevalue.html#cfn-connect-evaluationform-evaluationformitemenablementsourcevalue-refid
            '''
            result = self._values.get("ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''A type of source item value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitemenablementsourcevalue.html#cfn-connect-evaluationform-evaluationformitemenablementsourcevalue-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemEnablementSourceValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty",
        jsii_struct_bases=[],
        name_mapping={"question": "question", "section": "section"},
    )
    class EvaluationFormItemProperty:
        def __init__(
            self,
            *,
            question: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            section: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Items that are part of the evaluation form.

            The total number of sections and questions must not exceed 100 each. Questions must be contained in a section.

            :param question: The information of the question.
            :param section: The information of the section.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # evaluation_form_item_property_: connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty
                
                evaluation_form_item_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty(
                    question=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty(
                        enablement=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                            action="action",
                            condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                                operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                                    expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                        comparator="comparator",
                                        source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                            ref_id="refId",
                                            type="type"
                                        ),
                                        values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                            ref_id="refId",
                                            type="type"
                                        )]
                                    )
                                )],
                                operator="operator"
                            ),
                            default_action="defaultAction"
                        ),
                        instructions="instructions",
                        not_applicable_enabled=False,
                        question_type="questionType",
                        question_type_properties=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                            multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                                automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                        source_type="sourceType"
                                    ),
                                    default_option_ref_ids=["defaultOptionRefIds"],
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                        rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                            category="category",
                                            condition="condition",
                                            option_ref_ids=["optionRefIds"]
                                        )
                                    )]
                                ),
                                display_as="displayAs",
                                options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                                    ref_id="refId",
                                    text="text"
                                )]
                            ),
                            numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                                automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                        source_type="sourceType"
                                    ),
                                    property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                        label="label"
                                    )
                                ),
                                max_value=123,
                                min_value=123,
                                options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                                    automatic_fail=False,
                                    automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                        target_section="targetSection"
                                    ),
                                    max_value=123,
                                    min_value=123,
                                    score=123
                                )]
                            ),
                            single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                                automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                        source_type="sourceType"
                                    ),
                                    default_option_ref_id="defaultOptionRefId",
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                        rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                            category="category",
                                            condition="condition",
                                            option_ref_id="optionRefId"
                                        )
                                    )]
                                ),
                                display_as="displayAs",
                                options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                                    automatic_fail=False,
                                    automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                        target_section="targetSection"
                                    ),
                                    ref_id="refId",
                                    score=123,
                                    text="text"
                                )]
                            ),
                            text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                                automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                        source_type="sourceType"
                                    )
                                )
                            )
                        ),
                        ref_id="refId",
                        title="title",
                        weight=123
                    ),
                    section=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty(
                        instructions="instructions",
                        items=[evaluation_form_item_property_],
                        ref_id="refId",
                        title="title",
                        weight=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d55db0b4fa12da4530f844e0e2c05aad9e53b5e87422a6294022465147fdf0ad)
                check_type(argname="argument question", value=question, expected_type=type_hints["question"])
                check_type(argname="argument section", value=section, expected_type=type_hints["section"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if question is not None:
                self._values["question"] = question
            if section is not None:
                self._values["section"] = section

        @builtins.property
        def question(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty"]]:
            '''The information of the question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitem.html#cfn-connect-evaluationform-evaluationformitem-question
            '''
            result = self._values.get("question")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty"]], result)

        @builtins.property
        def section(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty"]]:
            '''The information of the section.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformitem.html#cfn-connect-evaluationform-evaluationformitem-section
            '''
            result = self._values.get("section")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"form_language": "formLanguage"},
    )
    class EvaluationFormLanguageConfigurationProperty:
        def __init__(
            self,
            *,
            form_language: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param form_language: The language of the form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformlanguageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_language_configuration_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty(
                    form_language="formLanguage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ae8a6ebd71bb4304d21e53c024d1ba425e25c989281ac07d1f98488300ca394e)
                check_type(argname="argument form_language", value=form_language, expected_type=type_hints["form_language"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if form_language is not None:
                self._values["form_language"] = form_language

        @builtins.property
        def form_language(self) -> typing.Optional[builtins.str]:
            '''The language of the form.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformlanguageconfiguration.html#cfn-connect-evaluationform-evaluationformlanguageconfiguration-formlanguage
            '''
            result = self._values.get("form_language")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormLanguageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_category": "ruleCategory"},
    )
    class EvaluationFormMultiSelectQuestionAutomationOptionProperty:
        def __init__(
            self,
            *,
            rule_category: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param rule_category: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionautomationoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_multi_select_question_automation_option_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                    rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                        category="category",
                        condition="condition",
                        option_ref_ids=["optionRefIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aeb90133d764129efac6e4162540af82714ef9037fdd90cef1fea317b1b73b85)
                check_type(argname="argument rule_category", value=rule_category, expected_type=type_hints["rule_category"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_category is not None:
                self._values["rule_category"] = rule_category

        @builtins.property
        def rule_category(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionautomationoption.html#cfn-connect-evaluationform-evaluationformmultiselectquestionautomationoption-rulecategory
            '''
            result = self._values.get("rule_category")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormMultiSelectQuestionAutomationOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_source": "answerSource",
            "default_option_ref_ids": "defaultOptionRefIds",
            "options": "options",
        },
    )
    class EvaluationFormMultiSelectQuestionAutomationProperty:
        def __init__(
            self,
            *,
            answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_option_ref_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param answer_source: A question automation answer.
            :param default_option_ref_ids: The list of reference id.
            :param options: The answer options for the automation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_multi_select_question_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                        source_type="sourceType"
                    ),
                    default_option_ref_ids=["defaultOptionRefIds"],
                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                        rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                            category="category",
                            condition="condition",
                            option_ref_ids=["optionRefIds"]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1870c0e6901b3a3c1410ccbbea461ec0879143c534cabdf71a3089a90b020a7)
                check_type(argname="argument answer_source", value=answer_source, expected_type=type_hints["answer_source"])
                check_type(argname="argument default_option_ref_ids", value=default_option_ref_ids, expected_type=type_hints["default_option_ref_ids"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_source is not None:
                self._values["answer_source"] = answer_source
            if default_option_ref_ids is not None:
                self._values["default_option_ref_ids"] = default_option_ref_ids
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def answer_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]]:
            '''A question automation answer.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionautomation.html#cfn-connect-evaluationform-evaluationformmultiselectquestionautomation-answersource
            '''
            result = self._values.get("answer_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]], result)

        @builtins.property
        def default_option_ref_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of reference id.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionautomation.html#cfn-connect-evaluationform-evaluationformmultiselectquestionautomation-defaultoptionrefids
            '''
            result = self._values.get("default_option_ref_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty"]]]]:
            '''The answer options for the automation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionautomation.html#cfn-connect-evaluationform-evaluationformmultiselectquestionautomation-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormMultiSelectQuestionAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"ref_id": "refId", "text": "text"},
    )
    class EvaluationFormMultiSelectQuestionOptionProperty:
        def __init__(
            self,
            *,
            ref_id: typing.Optional[builtins.str] = None,
            text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param ref_id: The identifier to reference the item.
            :param text: The title of the option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_multi_select_question_option_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                    ref_id="refId",
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d0dd058600358960283f7f8943697287d6775157393c48e80e756e63353c22c9)
                check_type(argname="argument ref_id", value=ref_id, expected_type=type_hints["ref_id"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ref_id is not None:
                self._values["ref_id"] = ref_id
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def ref_id(self) -> typing.Optional[builtins.str]:
            '''The identifier to reference the item.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionoption.html#cfn-connect-evaluationform-evaluationformmultiselectquestionoption-refid
            '''
            result = self._values.get("ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The title of the option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionoption.html#cfn-connect-evaluationform-evaluationformmultiselectquestionoption-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormMultiSelectQuestionOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automation": "automation",
            "display_as": "displayAs",
            "options": "options",
        },
    )
    class EvaluationFormMultiSelectQuestionPropertiesProperty:
        def __init__(
            self,
            *,
            automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            display_as: typing.Optional[builtins.str] = None,
            options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param automation: 
            :param display_as: The display mode of the multi-select question.
            :param options: The list of options for the question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_multi_select_question_properties_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                            source_type="sourceType"
                        ),
                        default_option_ref_ids=["defaultOptionRefIds"],
                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                            rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                category="category",
                                condition="condition",
                                option_ref_ids=["optionRefIds"]
                            )
                        )]
                    ),
                    display_as="displayAs",
                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                        ref_id="refId",
                        text="text"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7da1df8884df4bc93a61bbed26859f223ae9d1db4a8ce78ef36549f282097d2)
                check_type(argname="argument automation", value=automation, expected_type=type_hints["automation"])
                check_type(argname="argument display_as", value=display_as, expected_type=type_hints["display_as"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automation is not None:
                self._values["automation"] = automation
            if display_as is not None:
                self._values["display_as"] = display_as
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def automation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionproperties.html#cfn-connect-evaluationform-evaluationformmultiselectquestionproperties-automation
            '''
            result = self._values.get("automation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty"]], result)

        @builtins.property
        def display_as(self) -> typing.Optional[builtins.str]:
            '''The display mode of the multi-select question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionproperties.html#cfn-connect-evaluationform-evaluationformmultiselectquestionproperties-displayas
            '''
            result = self._values.get("display_as")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty"]]]]:
            '''The list of options for the question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformmultiselectquestionproperties.html#cfn-connect-evaluationform-evaluationformmultiselectquestionproperties-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormMultiSelectQuestionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_source": "answerSource",
            "property_value": "propertyValue",
        },
    )
    class EvaluationFormNumericQuestionAutomationProperty:
        def __init__(
            self,
            *,
            answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            property_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the automation configuration in numeric questions.

            :param answer_source: A source of automation answer for numeric question.
            :param property_value: The property value of the automation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_numeric_question_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                        source_type="sourceType"
                    ),
                    property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                        label="label"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dae32fe31e05073d0d27f79249546e709b771c758a5da5102449099b82759584)
                check_type(argname="argument answer_source", value=answer_source, expected_type=type_hints["answer_source"])
                check_type(argname="argument property_value", value=property_value, expected_type=type_hints["property_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_source is not None:
                self._values["answer_source"] = answer_source
            if property_value is not None:
                self._values["property_value"] = property_value

        @builtins.property
        def answer_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]]:
            '''A source of automation answer for numeric question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionautomation.html#cfn-connect-evaluationform-evaluationformnumericquestionautomation-answersource
            '''
            result = self._values.get("answer_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]], result)

        @builtins.property
        def property_value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty"]]:
            '''The property value of the automation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionautomation.html#cfn-connect-evaluationform-evaluationformnumericquestionautomation-propertyvalue
            '''
            result = self._values.get("property_value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormNumericQuestionAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatic_fail": "automaticFail",
            "automatic_fail_configuration": "automaticFailConfiguration",
            "max_value": "maxValue",
            "min_value": "minValue",
            "score": "score",
        },
    )
    class EvaluationFormNumericQuestionOptionProperty:
        def __init__(
            self,
            *,
            automatic_fail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            automatic_fail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_value: typing.Optional[jsii.Number] = None,
            min_value: typing.Optional[jsii.Number] = None,
            score: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about the option range used for scoring in numeric questions.

            :param automatic_fail: The flag to mark the option as automatic fail. If an automatic fail answer is provided, the overall evaluation gets a score of 0.
            :param automatic_fail_configuration: A configuration for automatic fail.
            :param max_value: The maximum answer value of the range option.
            :param min_value: The minimum answer value of the range option.
            :param score: The score assigned to answer values within the range option. *Minimum* : 0 *Maximum* : 10

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_numeric_question_option_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                    automatic_fail=False,
                    automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                        target_section="targetSection"
                    ),
                    max_value=123,
                    min_value=123,
                    score=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad7f2ab1045f6a68ef08faccd738ae59f5badbe2fd0b02c15736fa8bed82a6ae)
                check_type(argname="argument automatic_fail", value=automatic_fail, expected_type=type_hints["automatic_fail"])
                check_type(argname="argument automatic_fail_configuration", value=automatic_fail_configuration, expected_type=type_hints["automatic_fail_configuration"])
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
                check_type(argname="argument score", value=score, expected_type=type_hints["score"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic_fail is not None:
                self._values["automatic_fail"] = automatic_fail
            if automatic_fail_configuration is not None:
                self._values["automatic_fail_configuration"] = automatic_fail_configuration
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value
            if score is not None:
                self._values["score"] = score

        @builtins.property
        def automatic_fail(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag to mark the option as automatic fail.

            If an automatic fail answer is provided, the overall evaluation gets a score of 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionoption.html#cfn-connect-evaluationform-evaluationformnumericquestionoption-automaticfail
            '''
            result = self._values.get("automatic_fail")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def automatic_fail_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty"]]:
            '''A configuration for automatic fail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionoption.html#cfn-connect-evaluationform-evaluationformnumericquestionoption-automaticfailconfiguration
            '''
            result = self._values.get("automatic_fail_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty"]], result)

        @builtins.property
        def max_value(self) -> typing.Optional[jsii.Number]:
            '''The maximum answer value of the range option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionoption.html#cfn-connect-evaluationform-evaluationformnumericquestionoption-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_value(self) -> typing.Optional[jsii.Number]:
            '''The minimum answer value of the range option.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionoption.html#cfn-connect-evaluationform-evaluationformnumericquestionoption-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def score(self) -> typing.Optional[jsii.Number]:
            '''The score assigned to answer values within the range option.

            *Minimum* : 0

            *Maximum* : 10

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionoption.html#cfn-connect-evaluationform-evaluationformnumericquestionoption-score
            '''
            result = self._values.get("score")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormNumericQuestionOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automation": "automation",
            "max_value": "maxValue",
            "min_value": "minValue",
            "options": "options",
        },
    )
    class EvaluationFormNumericQuestionPropertiesProperty:
        def __init__(
            self,
            *,
            automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_value: typing.Optional[jsii.Number] = None,
            min_value: typing.Optional[jsii.Number] = None,
            options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about properties for a numeric question in an evaluation form.

            :param automation: The automation properties of the numeric question.
            :param max_value: The maximum answer value.
            :param min_value: The minimum answer value.
            :param options: The scoring options of the numeric question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_numeric_question_properties_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                            source_type="sourceType"
                        ),
                        property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                            label="label"
                        )
                    ),
                    max_value=123,
                    min_value=123,
                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                        automatic_fail=False,
                        automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                            target_section="targetSection"
                        ),
                        max_value=123,
                        min_value=123,
                        score=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1eb664a04aa51c540168b259d2013e559cdd46a7f2a16811f871406c98b0b3ca)
                check_type(argname="argument automation", value=automation, expected_type=type_hints["automation"])
                check_type(argname="argument max_value", value=max_value, expected_type=type_hints["max_value"])
                check_type(argname="argument min_value", value=min_value, expected_type=type_hints["min_value"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automation is not None:
                self._values["automation"] = automation
            if max_value is not None:
                self._values["max_value"] = max_value
            if min_value is not None:
                self._values["min_value"] = min_value
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def automation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty"]]:
            '''The automation properties of the numeric question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionproperties.html#cfn-connect-evaluationform-evaluationformnumericquestionproperties-automation
            '''
            result = self._values.get("automation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty"]], result)

        @builtins.property
        def max_value(self) -> typing.Optional[jsii.Number]:
            '''The maximum answer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionproperties.html#cfn-connect-evaluationform-evaluationformnumericquestionproperties-maxvalue
            '''
            result = self._values.get("max_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_value(self) -> typing.Optional[jsii.Number]:
            '''The minimum answer value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionproperties.html#cfn-connect-evaluationform-evaluationformnumericquestionproperties-minvalue
            '''
            result = self._values.get("min_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty"]]]]:
            '''The scoring options of the numeric question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformnumericquestionproperties.html#cfn-connect-evaluationform-evaluationformnumericquestionproperties-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormNumericQuestionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"source_type": "sourceType"},
    )
    class EvaluationFormQuestionAutomationAnswerSourceProperty:
        def __init__(
            self,
            *,
            source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A question automation answer.

            :param source_type: The automation answer source type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestionautomationanswersource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_question_automation_answer_source_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                    source_type="sourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f07ebab658961b74162e3bf99a3a6b50e87497f6075fe1ad7de96c729f0454b6)
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_type is not None:
                self._values["source_type"] = source_type

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''The automation answer source type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestionautomationanswersource.html#cfn-connect-evaluationform-evaluationformquestionautomationanswersource-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormQuestionAutomationAnswerSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enablement": "enablement",
            "instructions": "instructions",
            "not_applicable_enabled": "notApplicableEnabled",
            "question_type": "questionType",
            "question_type_properties": "questionTypeProperties",
            "ref_id": "refId",
            "title": "title",
            "weight": "weight",
        },
    )
    class EvaluationFormQuestionProperty:
        def __init__(
            self,
            *,
            enablement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instructions: typing.Optional[builtins.str] = None,
            not_applicable_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            question_type: typing.Optional[builtins.str] = None,
            question_type_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ref_id: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about a question from an evaluation form.

            :param enablement: A question conditional enablement.
            :param instructions: The instructions of the section. *Length Constraints* : Minimum length of 0. Maximum length of 1024.
            :param not_applicable_enabled: The flag to enable not applicable answers to the question.
            :param question_type: The type of the question. *Allowed values* : ``NUMERIC`` | ``SINGLESELECT`` | ``TEXT``
            :param question_type_properties: The properties of the type of question. Text questions do not have to define question type properties.
            :param ref_id: The identifier of the question. An identifier must be unique within the evaluation form. *Length Constraints* : Minimum length of 1. Maximum length of 40.
            :param title: The title of the question. *Length Constraints* : Minimum length of 1. Maximum length of 350.
            :param weight: The scoring weight of the section. *Minimum* : 0 *Maximum* : 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_question_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty(
                    enablement=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                        action="action",
                        condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                            operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                                expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                    comparator="comparator",
                                    source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                        ref_id="refId",
                                        type="type"
                                    ),
                                    values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                        ref_id="refId",
                                        type="type"
                                    )]
                                )
                            )],
                            operator="operator"
                        ),
                        default_action="defaultAction"
                    ),
                    instructions="instructions",
                    not_applicable_enabled=False,
                    question_type="questionType",
                    question_type_properties=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                        multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                            automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                                answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                    source_type="sourceType"
                                ),
                                default_option_ref_ids=["defaultOptionRefIds"],
                                options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                    rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                        category="category",
                                        condition="condition",
                                        option_ref_ids=["optionRefIds"]
                                    )
                                )]
                            ),
                            display_as="displayAs",
                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                                ref_id="refId",
                                text="text"
                            )]
                        ),
                        numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                            automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                                answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                    source_type="sourceType"
                                ),
                                property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                    label="label"
                                )
                            ),
                            max_value=123,
                            min_value=123,
                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                                automatic_fail=False,
                                automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                    target_section="targetSection"
                                ),
                                max_value=123,
                                min_value=123,
                                score=123
                            )]
                        ),
                        single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                            automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                                answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                    source_type="sourceType"
                                ),
                                default_option_ref_id="defaultOptionRefId",
                                options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                    rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                        category="category",
                                        condition="condition",
                                        option_ref_id="optionRefId"
                                    )
                                )]
                            ),
                            display_as="displayAs",
                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                                automatic_fail=False,
                                automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                    target_section="targetSection"
                                ),
                                ref_id="refId",
                                score=123,
                                text="text"
                            )]
                        ),
                        text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                            automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                                answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                    source_type="sourceType"
                                )
                            )
                        )
                    ),
                    ref_id="refId",
                    title="title",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60011c01c9c884476d3f0bc32d78dbb6f0e244b358a140a19d0e130c8ee29452)
                check_type(argname="argument enablement", value=enablement, expected_type=type_hints["enablement"])
                check_type(argname="argument instructions", value=instructions, expected_type=type_hints["instructions"])
                check_type(argname="argument not_applicable_enabled", value=not_applicable_enabled, expected_type=type_hints["not_applicable_enabled"])
                check_type(argname="argument question_type", value=question_type, expected_type=type_hints["question_type"])
                check_type(argname="argument question_type_properties", value=question_type_properties, expected_type=type_hints["question_type_properties"])
                check_type(argname="argument ref_id", value=ref_id, expected_type=type_hints["ref_id"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enablement is not None:
                self._values["enablement"] = enablement
            if instructions is not None:
                self._values["instructions"] = instructions
            if not_applicable_enabled is not None:
                self._values["not_applicable_enabled"] = not_applicable_enabled
            if question_type is not None:
                self._values["question_type"] = question_type
            if question_type_properties is not None:
                self._values["question_type_properties"] = question_type_properties
            if ref_id is not None:
                self._values["ref_id"] = ref_id
            if title is not None:
                self._values["title"] = title
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def enablement(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty"]]:
            '''A question conditional enablement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-enablement
            '''
            result = self._values.get("enablement")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty"]], result)

        @builtins.property
        def instructions(self) -> typing.Optional[builtins.str]:
            '''The instructions of the section.

            *Length Constraints* : Minimum length of 0. Maximum length of 1024.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-instructions
            '''
            result = self._values.get("instructions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def not_applicable_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag to enable not applicable answers to the question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-notapplicableenabled
            '''
            result = self._values.get("not_applicable_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def question_type(self) -> typing.Optional[builtins.str]:
            '''The type of the question.

            *Allowed values* : ``NUMERIC`` | ``SINGLESELECT`` | ``TEXT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-questiontype
            '''
            result = self._values.get("question_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def question_type_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty"]]:
            '''The properties of the type of question.

            Text questions do not have to define question type properties.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-questiontypeproperties
            '''
            result = self._values.get("question_type_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty"]], result)

        @builtins.property
        def ref_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the question. An identifier must be unique within the evaluation form.

            *Length Constraints* : Minimum length of 1. Maximum length of 40.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-refid
            '''
            result = self._values.get("ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title of the question.

            *Length Constraints* : Minimum length of 1. Maximum length of 350.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The scoring weight of the section.

            *Minimum* : 0

            *Maximum* : 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestion.html#cfn-connect-evaluationform-evaluationformquestion-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormQuestionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "multi_select": "multiSelect",
            "numeric": "numeric",
            "single_select": "singleSelect",
            "text": "text",
        },
    )
    class EvaluationFormQuestionTypePropertiesProperty:
        def __init__(
            self,
            *,
            multi_select: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            numeric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            single_select: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about properties for a question in an evaluation form.

            The question type properties must be either for a numeric question or a single select question.

            :param multi_select: 
            :param numeric: The properties of the numeric question.
            :param single_select: The properties of the numeric question.
            :param text: The properties of the text question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestiontypeproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_question_type_properties_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                    multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                source_type="sourceType"
                            ),
                            default_option_ref_ids=["defaultOptionRefIds"],
                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                    category="category",
                                    condition="condition",
                                    option_ref_ids=["optionRefIds"]
                                )
                            )]
                        ),
                        display_as="displayAs",
                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                            ref_id="refId",
                            text="text"
                        )]
                    ),
                    numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                source_type="sourceType"
                            ),
                            property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                label="label"
                            )
                        ),
                        max_value=123,
                        min_value=123,
                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                            automatic_fail=False,
                            automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                target_section="targetSection"
                            ),
                            max_value=123,
                            min_value=123,
                            score=123
                        )]
                    ),
                    single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                source_type="sourceType"
                            ),
                            default_option_ref_id="defaultOptionRefId",
                            options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                    category="category",
                                    condition="condition",
                                    option_ref_id="optionRefId"
                                )
                            )]
                        ),
                        display_as="displayAs",
                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                            automatic_fail=False,
                            automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                target_section="targetSection"
                            ),
                            ref_id="refId",
                            score=123,
                            text="text"
                        )]
                    ),
                    text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                        automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                            answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                source_type="sourceType"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__95d0c10c451bd9906345fd25bde24ba0ba058ce36ff85480225fc0d41f7ae4a4)
                check_type(argname="argument multi_select", value=multi_select, expected_type=type_hints["multi_select"])
                check_type(argname="argument numeric", value=numeric, expected_type=type_hints["numeric"])
                check_type(argname="argument single_select", value=single_select, expected_type=type_hints["single_select"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multi_select is not None:
                self._values["multi_select"] = multi_select
            if numeric is not None:
                self._values["numeric"] = numeric
            if single_select is not None:
                self._values["single_select"] = single_select
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def multi_select(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestiontypeproperties.html#cfn-connect-evaluationform-evaluationformquestiontypeproperties-multiselect
            '''
            result = self._values.get("multi_select")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty"]], result)

        @builtins.property
        def numeric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty"]]:
            '''The properties of the numeric question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestiontypeproperties.html#cfn-connect-evaluationform-evaluationformquestiontypeproperties-numeric
            '''
            result = self._values.get("numeric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty"]], result)

        @builtins.property
        def single_select(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty"]]:
            '''The properties of the numeric question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestiontypeproperties.html#cfn-connect-evaluationform-evaluationformquestiontypeproperties-singleselect
            '''
            result = self._values.get("single_select")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty"]], result)

        @builtins.property
        def text(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty"]]:
            '''The properties of the text question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformquestiontypeproperties.html#cfn-connect-evaluationform-evaluationformquestiontypeproperties-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormQuestionTypePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "instructions": "instructions",
            "items": "items",
            "ref_id": "refId",
            "title": "title",
            "weight": "weight",
        },
    )
    class EvaluationFormSectionProperty:
        def __init__(
            self,
            *,
            instructions: typing.Optional[builtins.str] = None,
            items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormItemProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ref_id: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Information about a section from an evaluation form.

            A section can contain sections and/or questions. Evaluation forms can only contain sections and subsections (two level nesting).

            :param instructions: The instructions of the section.
            :param items: The items of the section. *Minimum* : 1
            :param ref_id: The identifier of the section. An identifier must be unique within the evaluation form. *Length Constraints* : Minimum length of 1. Maximum length of 40.
            :param title: The title of the section. *Length Constraints* : Minimum length of 1. Maximum length of 128.
            :param weight: The scoring weight of the section. *Minimum* : 0 *Maximum* : 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # evaluation_form_section_property_: connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty
                
                evaluation_form_section_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty(
                    instructions="instructions",
                    items=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemProperty(
                        question=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty(
                            enablement=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty(
                                action="action",
                                condition=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty(
                                    operands=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty(
                                        expression=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty(
                                            comparator="comparator",
                                            source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty(
                                                ref_id="refId",
                                                type="type"
                                            ),
                                            values=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty(
                                                ref_id="refId",
                                                type="type"
                                            )]
                                        )
                                    )],
                                    operator="operator"
                                ),
                                default_action="defaultAction"
                            ),
                            instructions="instructions",
                            not_applicable_enabled=False,
                            question_type="questionType",
                            question_type_properties=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty(
                                multi_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        ),
                                        default_option_ref_ids=["defaultOptionRefIds"],
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty(
                                            rule_category=connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                                                category="category",
                                                condition="condition",
                                                option_ref_ids=["optionRefIds"]
                                            )
                                        )]
                                    ),
                                    display_as="displayAs",
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty(
                                        ref_id="refId",
                                        text="text"
                                    )]
                                ),
                                numeric=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        ),
                                        property_value=connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                                            label="label"
                                        )
                                    ),
                                    max_value=123,
                                    min_value=123,
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty(
                                        automatic_fail=False,
                                        automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                            target_section="targetSection"
                                        ),
                                        max_value=123,
                                        min_value=123,
                                        score=123
                                    )]
                                ),
                                single_select=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        ),
                                        default_option_ref_id="defaultOptionRefId",
                                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                                            rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                                category="category",
                                                condition="condition",
                                                option_ref_id="optionRefId"
                                            )
                                        )]
                                    ),
                                    display_as="displayAs",
                                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                                        automatic_fail=False,
                                        automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                                            target_section="targetSection"
                                        ),
                                        ref_id="refId",
                                        score=123,
                                        text="text"
                                    )]
                                ),
                                text=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                                            source_type="sourceType"
                                        )
                                    )
                                )
                            ),
                            ref_id="refId",
                            title="title",
                            weight=123
                        ),
                        section=evaluation_form_section_property_
                    )],
                    ref_id="refId",
                    title="title",
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e02e8660f59c45996c30278920e8e901a052ded70fcf383aa214bb1bf4a4807)
                check_type(argname="argument instructions", value=instructions, expected_type=type_hints["instructions"])
                check_type(argname="argument items", value=items, expected_type=type_hints["items"])
                check_type(argname="argument ref_id", value=ref_id, expected_type=type_hints["ref_id"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if instructions is not None:
                self._values["instructions"] = instructions
            if items is not None:
                self._values["items"] = items
            if ref_id is not None:
                self._values["ref_id"] = ref_id
            if title is not None:
                self._values["title"] = title
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def instructions(self) -> typing.Optional[builtins.str]:
            '''The instructions of the section.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsection.html#cfn-connect-evaluationform-evaluationformsection-instructions
            '''
            result = self._values.get("instructions")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def items(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemProperty"]]]]:
            '''The items of the section.

            *Minimum* : 1

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsection.html#cfn-connect-evaluationform-evaluationformsection-items
            '''
            result = self._values.get("items")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormItemProperty"]]]], result)

        @builtins.property
        def ref_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the section. An identifier must be unique within the evaluation form.

            *Length Constraints* : Minimum length of 1. Maximum length of 40.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsection.html#cfn-connect-evaluationform-evaluationformsection-refid
            '''
            result = self._values.get("ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''The title of the section.

            *Length Constraints* : Minimum length of 1. Maximum length of 128.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsection.html#cfn-connect-evaluationform-evaluationformsection-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''The scoring weight of the section.

            *Minimum* : 0

            *Maximum* : 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsection.html#cfn-connect-evaluationform-evaluationformsection-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormSectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_category": "ruleCategory"},
    )
    class EvaluationFormSingleSelectQuestionAutomationOptionProperty:
        def __init__(
            self,
            *,
            rule_category: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The automation options of the single select question.

            :param rule_category: The automation option based on a rule category for the single select question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionautomationoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_single_select_question_automation_option_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                    rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                        category="category",
                        condition="condition",
                        option_ref_id="optionRefId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee54669b7aad28c0aca7d77599bd4d8a027ea8f7df44bfad63478e4b91102169)
                check_type(argname="argument rule_category", value=rule_category, expected_type=type_hints["rule_category"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_category is not None:
                self._values["rule_category"] = rule_category

        @builtins.property
        def rule_category(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty"]]:
            '''The automation option based on a rule category for the single select question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionautomationoption.html#cfn-connect-evaluationform-evaluationformsingleselectquestionautomationoption-rulecategory
            '''
            result = self._values.get("rule_category")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormSingleSelectQuestionAutomationOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "answer_source": "answerSource",
            "default_option_ref_id": "defaultOptionRefId",
            "options": "options",
        },
    )
    class EvaluationFormSingleSelectQuestionAutomationProperty:
        def __init__(
            self,
            *,
            answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            default_option_ref_id: typing.Optional[builtins.str] = None,
            options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about the automation configuration in single select questions.

            Automation options are evaluated in order, and the first matched option is applied. If no automation option matches, and there is a default option, then the default option is applied.

            :param answer_source: Automation answer source.
            :param default_option_ref_id: The identifier of the default answer option, when none of the automation options match the criteria. *Length Constraints* : Minimum length of 1. Maximum length of 40.
            :param options: The automation options of the single select question. *Minimum* : 1 *Maximum* : 20

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_single_select_question_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                        source_type="sourceType"
                    ),
                    default_option_ref_id="defaultOptionRefId",
                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                        rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                            category="category",
                            condition="condition",
                            option_ref_id="optionRefId"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b15a5da33e2cc89a44939968f80922b9a8840e650b4baef882f06053209a9637)
                check_type(argname="argument answer_source", value=answer_source, expected_type=type_hints["answer_source"])
                check_type(argname="argument default_option_ref_id", value=default_option_ref_id, expected_type=type_hints["default_option_ref_id"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_source is not None:
                self._values["answer_source"] = answer_source
            if default_option_ref_id is not None:
                self._values["default_option_ref_id"] = default_option_ref_id
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def answer_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]]:
            '''Automation answer source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionautomation.html#cfn-connect-evaluationform-evaluationformsingleselectquestionautomation-answersource
            '''
            result = self._values.get("answer_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]], result)

        @builtins.property
        def default_option_ref_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the default answer option, when none of the automation options match the criteria.

            *Length Constraints* : Minimum length of 1. Maximum length of 40.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionautomation.html#cfn-connect-evaluationform-evaluationformsingleselectquestionautomation-defaultoptionrefid
            '''
            result = self._values.get("default_option_ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty"]]]]:
            '''The automation options of the single select question.

            *Minimum* : 1

            *Maximum* : 20

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionautomation.html#cfn-connect-evaluationform-evaluationformsingleselectquestionautomation-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormSingleSelectQuestionAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatic_fail": "automaticFail",
            "automatic_fail_configuration": "automaticFailConfiguration",
            "ref_id": "refId",
            "score": "score",
            "text": "text",
        },
    )
    class EvaluationFormSingleSelectQuestionOptionProperty:
        def __init__(
            self,
            *,
            automatic_fail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            automatic_fail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ref_id: typing.Optional[builtins.str] = None,
            score: typing.Optional[jsii.Number] = None,
            text: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the automation configuration in single select questions.

            :param automatic_fail: The flag to mark the option as automatic fail. If an automatic fail answer is provided, the overall evaluation gets a score of 0.
            :param automatic_fail_configuration: Whether automatic fail is configured on a single select question.
            :param ref_id: The identifier of the answer option. An identifier must be unique within the question. *Length Constraints* : Minimum length of 1. Maximum length of 40.
            :param score: The score assigned to the answer option. *Minimum* : 0 *Maximum* : 10
            :param text: The title of the answer option. *Length Constraints* : Minimum length of 1. Maximum length of 128.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_single_select_question_option_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                    automatic_fail=False,
                    automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                        target_section="targetSection"
                    ),
                    ref_id="refId",
                    score=123,
                    text="text"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__06a5c100d1b31f46f3c94798ff520248d8a5d2697da096cf72a26581450128ff)
                check_type(argname="argument automatic_fail", value=automatic_fail, expected_type=type_hints["automatic_fail"])
                check_type(argname="argument automatic_fail_configuration", value=automatic_fail_configuration, expected_type=type_hints["automatic_fail_configuration"])
                check_type(argname="argument ref_id", value=ref_id, expected_type=type_hints["ref_id"])
                check_type(argname="argument score", value=score, expected_type=type_hints["score"])
                check_type(argname="argument text", value=text, expected_type=type_hints["text"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic_fail is not None:
                self._values["automatic_fail"] = automatic_fail
            if automatic_fail_configuration is not None:
                self._values["automatic_fail_configuration"] = automatic_fail_configuration
            if ref_id is not None:
                self._values["ref_id"] = ref_id
            if score is not None:
                self._values["score"] = score
            if text is not None:
                self._values["text"] = text

        @builtins.property
        def automatic_fail(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The flag to mark the option as automatic fail.

            If an automatic fail answer is provided, the overall evaluation gets a score of 0.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionoption.html#cfn-connect-evaluationform-evaluationformsingleselectquestionoption-automaticfail
            '''
            result = self._values.get("automatic_fail")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def automatic_fail_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty"]]:
            '''Whether automatic fail is configured on a single select question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionoption.html#cfn-connect-evaluationform-evaluationformsingleselectquestionoption-automaticfailconfiguration
            '''
            result = self._values.get("automatic_fail_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty"]], result)

        @builtins.property
        def ref_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the answer option. An identifier must be unique within the question.

            *Length Constraints* : Minimum length of 1. Maximum length of 40.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionoption.html#cfn-connect-evaluationform-evaluationformsingleselectquestionoption-refid
            '''
            result = self._values.get("ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def score(self) -> typing.Optional[jsii.Number]:
            '''The score assigned to the answer option.

            *Minimum* : 0

            *Maximum* : 10

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionoption.html#cfn-connect-evaluationform-evaluationformsingleselectquestionoption-score
            '''
            result = self._values.get("score")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def text(self) -> typing.Optional[builtins.str]:
            '''The title of the answer option.

            *Length Constraints* : Minimum length of 1. Maximum length of 128.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionoption.html#cfn-connect-evaluationform-evaluationformsingleselectquestionoption-text
            '''
            result = self._values.get("text")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormSingleSelectQuestionOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automation": "automation",
            "display_as": "displayAs",
            "options": "options",
        },
    )
    class EvaluationFormSingleSelectQuestionPropertiesProperty:
        def __init__(
            self,
            *,
            automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            display_as: typing.Optional[builtins.str] = None,
            options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about the options in single select questions.

            :param automation: The display mode of the single select question.
            :param display_as: The display mode of the single select question. *Allowed values* : ``DROPDOWN`` | ``RADIO``
            :param options: The answer options of the single select question. *Minimum* : 2 *Maximum* : 256

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_single_select_question_properties_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty(
                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty(
                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                            source_type="sourceType"
                        ),
                        default_option_ref_id="defaultOptionRefId",
                        options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty(
                            rule_category=connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                                category="category",
                                condition="condition",
                                option_ref_id="optionRefId"
                            )
                        )]
                    ),
                    display_as="displayAs",
                    options=[connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty(
                        automatic_fail=False,
                        automatic_fail_configuration=connect_mixins.CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty(
                            target_section="targetSection"
                        ),
                        ref_id="refId",
                        score=123,
                        text="text"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__99591f4b221d52fd992ea091e13eb9b0b814737e38aa313619e4f5386274f161)
                check_type(argname="argument automation", value=automation, expected_type=type_hints["automation"])
                check_type(argname="argument display_as", value=display_as, expected_type=type_hints["display_as"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automation is not None:
                self._values["automation"] = automation
            if display_as is not None:
                self._values["display_as"] = display_as
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def automation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty"]]:
            '''The display mode of the single select question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionproperties.html#cfn-connect-evaluationform-evaluationformsingleselectquestionproperties-automation
            '''
            result = self._values.get("automation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty"]], result)

        @builtins.property
        def display_as(self) -> typing.Optional[builtins.str]:
            '''The display mode of the single select question.

            *Allowed values* : ``DROPDOWN`` | ``RADIO``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionproperties.html#cfn-connect-evaluationform-evaluationformsingleselectquestionproperties-displayas
            '''
            result = self._values.get("display_as")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty"]]]]:
            '''The answer options of the single select question.

            *Minimum* : 2

            *Maximum* : 256

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformsingleselectquestionproperties.html#cfn-connect-evaluationform-evaluationformsingleselectquestionproperties-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormSingleSelectQuestionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_interaction_type": "contactInteractionType"},
    )
    class EvaluationFormTargetConfigurationProperty:
        def __init__(
            self,
            *,
            contact_interaction_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param contact_interaction_type: The interaction type of a contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformtargetconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_target_configuration_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty(
                    contact_interaction_type="contactInteractionType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6fc750340d378de9f9ea6bfd9096b4023bd09128e3dabedc11c2f1f0fd672ad3)
                check_type(argname="argument contact_interaction_type", value=contact_interaction_type, expected_type=type_hints["contact_interaction_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_interaction_type is not None:
                self._values["contact_interaction_type"] = contact_interaction_type

        @builtins.property
        def contact_interaction_type(self) -> typing.Optional[builtins.str]:
            '''The interaction type of a contact.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformtargetconfiguration.html#cfn-connect-evaluationform-evaluationformtargetconfiguration-contactinteractiontype
            '''
            result = self._values.get("contact_interaction_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormTargetConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={"answer_source": "answerSource"},
    )
    class EvaluationFormTextQuestionAutomationProperty:
        def __init__(
            self,
            *,
            answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the automation configuration in text questions.

            :param answer_source: Automation answer source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformtextquestionautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_text_question_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                    answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                        source_type="sourceType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f85964724dd0591b615e6e23a435e93ca12d64e59ba11c8ad1936660a72a90e3)
                check_type(argname="argument answer_source", value=answer_source, expected_type=type_hints["answer_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if answer_source is not None:
                self._values["answer_source"] = answer_source

        @builtins.property
        def answer_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]]:
            '''Automation answer source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformtextquestionautomation.html#cfn-connect-evaluationform-evaluationformtextquestionautomation-answersource
            '''
            result = self._values.get("answer_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormTextQuestionAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"automation": "automation"},
    )
    class EvaluationFormTextQuestionPropertiesProperty:
        def __init__(
            self,
            *,
            automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about properties for a text question in an evaluation form.

            :param automation: The automation properties of the text question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformtextquestionproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                evaluation_form_text_question_properties_property = connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty(
                    automation=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty(
                        answer_source=connect_mixins.CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty(
                            source_type="sourceType"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c45024df85ab30660109d97088bdfe33658214e2ca0b8d00a1c9448f3d47d350)
                check_type(argname="argument automation", value=automation, expected_type=type_hints["automation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automation is not None:
                self._values["automation"] = automation

        @builtins.property
        def automation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty"]]:
            '''The automation properties of the text question.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-evaluationformtextquestionproperties.html#cfn-connect-evaluationform-evaluationformtextquestionproperties-automation
            '''
            result = self._values.get("automation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluationFormTextQuestionPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "category": "category",
            "condition": "condition",
            "option_ref_ids": "optionRefIds",
        },
    )
    class MultiSelectQuestionRuleCategoryAutomationProperty:
        def __init__(
            self,
            *,
            category: typing.Optional[builtins.str] = None,
            condition: typing.Optional[builtins.str] = None,
            option_ref_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''
            :param category: The category name as defined in Rules.
            :param condition: The automation condition applied on contact categories.
            :param option_ref_ids: The list of reference id.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-multiselectquestionrulecategoryautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                multi_select_question_rule_category_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty(
                    category="category",
                    condition="condition",
                    option_ref_ids=["optionRefIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eaa6b190bd17cd9731062798a98c48c465526742485c8603effcd5c1bca0a19a)
                check_type(argname="argument category", value=category, expected_type=type_hints["category"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument option_ref_ids", value=option_ref_ids, expected_type=type_hints["option_ref_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if category is not None:
                self._values["category"] = category
            if condition is not None:
                self._values["condition"] = condition
            if option_ref_ids is not None:
                self._values["option_ref_ids"] = option_ref_ids

        @builtins.property
        def category(self) -> typing.Optional[builtins.str]:
            '''The category name as defined in Rules.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-multiselectquestionrulecategoryautomation.html#cfn-connect-evaluationform-multiselectquestionrulecategoryautomation-category
            '''
            result = self._values.get("category")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The automation condition applied on contact categories.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-multiselectquestionrulecategoryautomation.html#cfn-connect-evaluationform-multiselectquestionrulecategoryautomation-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def option_ref_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of reference id.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-multiselectquestionrulecategoryautomation.html#cfn-connect-evaluationform-multiselectquestionrulecategoryautomation-optionrefids
            '''
            result = self._values.get("option_ref_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MultiSelectQuestionRuleCategoryAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={"label": "label"},
    )
    class NumericQuestionPropertyValueAutomationProperty:
        def __init__(self, *, label: typing.Optional[builtins.str] = None) -> None:
            '''Information about the property value used in automation of a numeric questions.

            :param label: The property label of the automation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-numericquestionpropertyvalueautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                numeric_question_property_value_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty(
                    label="label"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05f8857fe52cd33ed7be2916236ce779e89a4f895d4b62df11455f82cae80818)
                check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if label is not None:
                self._values["label"] = label

        @builtins.property
        def label(self) -> typing.Optional[builtins.str]:
            '''The property label of the automation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-numericquestionpropertyvalueautomation.html#cfn-connect-evaluationform-numericquestionpropertyvalueautomation-label
            '''
            result = self._values.get("label")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NumericQuestionPropertyValueAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.ScoringStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode", "status": "status"},
    )
    class ScoringStrategyProperty:
        def __init__(
            self,
            *,
            mode: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A scoring strategy of the evaluation form.

            :param mode: The scoring mode of the evaluation form. *Allowed values* : ``QUESTION_ONLY`` | ``SECTION_ONLY``
            :param status: The scoring status of the evaluation form. *Allowed values* : ``ENABLED`` | ``DISABLED``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-scoringstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                scoring_strategy_property = connect_mixins.CfnEvaluationFormPropsMixin.ScoringStrategyProperty(
                    mode="mode",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ac6a9ec50b96f9eea9eda688062bb92565562ef8433be01496ab5f343a3a3fa)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''The scoring mode of the evaluation form.

            *Allowed values* : ``QUESTION_ONLY`` | ``SECTION_ONLY``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-scoringstrategy.html#cfn-connect-evaluationform-scoringstrategy-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The scoring status of the evaluation form.

            *Allowed values* : ``ENABLED`` | ``DISABLED``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-scoringstrategy.html#cfn-connect-evaluationform-scoringstrategy-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScoringStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "category": "category",
            "condition": "condition",
            "option_ref_id": "optionRefId",
        },
    )
    class SingleSelectQuestionRuleCategoryAutomationProperty:
        def __init__(
            self,
            *,
            category: typing.Optional[builtins.str] = None,
            condition: typing.Optional[builtins.str] = None,
            option_ref_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the automation option based on a rule category for a single select question.

            *Length Constraints* : Minimum length of 1. Maximum length of 50.

            :param category: The category name, as defined in Rules. *Minimum* : 1 *Maximum* : 50
            :param condition: The condition to apply for the automation option. If the condition is PRESENT, then the option is applied when the contact data includes the category. Similarly, if the condition is NOT_PRESENT, then the option is applied when the contact data does not include the category. *Allowed values* : ``PRESENT`` | ``NOT_PRESENT`` *Maximum* : 50
            :param option_ref_id: The identifier of the answer option. An identifier must be unique within the question. *Length Constraints* : Minimum length of 1. Maximum length of 40.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-singleselectquestionrulecategoryautomation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                single_select_question_rule_category_automation_property = connect_mixins.CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty(
                    category="category",
                    condition="condition",
                    option_ref_id="optionRefId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5527a748c7efd5f3e38660a02dc4a52f540dec1d50fdd7b2c3d695ff0e670dc)
                check_type(argname="argument category", value=category, expected_type=type_hints["category"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument option_ref_id", value=option_ref_id, expected_type=type_hints["option_ref_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if category is not None:
                self._values["category"] = category
            if condition is not None:
                self._values["condition"] = condition
            if option_ref_id is not None:
                self._values["option_ref_id"] = option_ref_id

        @builtins.property
        def category(self) -> typing.Optional[builtins.str]:
            '''The category name, as defined in Rules.

            *Minimum* : 1

            *Maximum* : 50

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-singleselectquestionrulecategoryautomation.html#cfn-connect-evaluationform-singleselectquestionrulecategoryautomation-category
            '''
            result = self._values.get("category")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The condition to apply for the automation option.

            If the condition is PRESENT, then the option is applied when the contact data includes the category. Similarly, if the condition is NOT_PRESENT, then the option is applied when the contact data does not include the category.

            *Allowed values* : ``PRESENT`` | ``NOT_PRESENT``

            *Maximum* : 50

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-singleselectquestionrulecategoryautomation.html#cfn-connect-evaluationform-singleselectquestionrulecategoryautomation-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def option_ref_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the answer option. An identifier must be unique within the question.

            *Length Constraints* : Minimum length of 1. Maximum length of 40.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-evaluationform-singleselectquestionrulecategoryautomation.html#cfn-connect-evaluationform-singleselectquestionrulecategoryautomation-optionrefid
            '''
            result = self._values.get("option_ref_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SingleSelectQuestionRuleCategoryAutomationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "config": "config",
        "description": "description",
        "hours_of_operation_overrides": "hoursOfOperationOverrides",
        "instance_arn": "instanceArn",
        "name": "name",
        "tags": "tags",
        "time_zone": "timeZone",
    },
)
class CfnHoursOfOperationMixinProps:
    def __init__(
        self,
        *,
        config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        hours_of_operation_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnHoursOfOperationPropsMixin.

        :param config: Configuration information for the hours of operation.
        :param description: The description for the hours of operation.
        :param hours_of_operation_overrides: One or more hours of operation overrides assigned to an hour of operation.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name for the hours of operation.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "Tags": {"key1":"value1", "key2":"value2"} }.
        :param time_zone: The time zone for the hours of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_hours_of_operation_mixin_props = connect_mixins.CfnHoursOfOperationMixinProps(
                config=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty(
                    day="day",
                    end_time=connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )],
                description="description",
                hours_of_operation_overrides=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty(
                    effective_from="effectiveFrom",
                    effective_till="effectiveTill",
                    hours_of_operation_override_id="hoursOfOperationOverrideId",
                    override_config=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty(
                        day="day",
                        end_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                            hours=123,
                            minutes=123
                        ),
                        start_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                            hours=123,
                            minutes=123
                        )
                    )],
                    override_description="overrideDescription",
                    override_name="overrideName"
                )],
                instance_arn="instanceArn",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                time_zone="timeZone"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e1f49dfdaae143884e84b0d07cb37c6d84c46913121fc1951b29611c585143a)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hours_of_operation_overrides", value=hours_of_operation_overrides, expected_type=type_hints["hours_of_operation_overrides"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if config is not None:
            self._values["config"] = config
        if description is not None:
            self._values["description"] = description
        if hours_of_operation_overrides is not None:
            self._values["hours_of_operation_overrides"] = hours_of_operation_overrides
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty"]]]]:
        '''Configuration information for the hours of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the hours of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hours_of_operation_overrides(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty"]]]]:
        '''One or more hours of operation overrides assigned to an hour of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-hoursofoperationoverrides
        '''
        result = self._values.get("hours_of_operation_overrides")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty"]]]], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the hours of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''The time zone for the hours of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html#cfn-connect-hoursofoperation-timezone
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHoursOfOperationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnHoursOfOperationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationPropsMixin",
):
    '''Specifies hours of operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-hoursofoperation.html
    :cloudformationResource: AWS::Connect::HoursOfOperation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_hours_of_operation_props_mixin = connect_mixins.CfnHoursOfOperationPropsMixin(connect_mixins.CfnHoursOfOperationMixinProps(
            config=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty(
                day="day",
                end_time=connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                ),
                start_time=connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            )],
            description="description",
            hours_of_operation_overrides=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty(
                effective_from="effectiveFrom",
                effective_till="effectiveTill",
                hours_of_operation_override_id="hoursOfOperationOverrideId",
                override_config=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty(
                    day="day",
                    end_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )],
                override_description="overrideDescription",
                override_name="overrideName"
            )],
            instance_arn="instanceArn",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            time_zone="timeZone"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnHoursOfOperationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::HoursOfOperation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfc158957dfc051d6783578a7c4abb8c3adcb93752c450cce52b16637d6a48b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__03556557bc7df6a7b2f7c80a484b1ee78f28b50b38f849c108b8c6e5feb1f6f7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f3a5b03a89fb5ab09f3727bdae5a6b365f5e695f8b66efba087533d78c0255)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnHoursOfOperationMixinProps:
        return typing.cast(CfnHoursOfOperationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "end_time": "endTime", "start_time": "startTime"},
    )
    class HoursOfOperationConfigProperty:
        def __init__(
            self,
            *,
            day: typing.Optional[builtins.str] = None,
            end_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the hours of operation.

            :param day: The day that the hours of operation applies to.
            :param end_time: The end time that your contact center closes.
            :param start_time: The start time that your contact center opens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                hours_of_operation_config_property = connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty(
                    day="day",
                    end_time=connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e33b3645a9288ef8fd63991d2566cb47df5a1fc0b98399c7ca1cfed12dd38368)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day is not None:
                self._values["day"] = day
            if end_time is not None:
                self._values["end_time"] = end_time
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def day(self) -> typing.Optional[builtins.str]:
            '''The day that the hours of operation applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-day
            '''
            result = self._values.get("day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def end_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty"]]:
            '''The end time that your contact center closes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty"]], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty"]]:
            '''The start time that your contact center opens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationconfig.html#cfn-connect-hoursofoperation-hoursofoperationconfig-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"day": "day", "end_time": "endTime", "start_time": "startTime"},
    )
    class HoursOfOperationOverrideConfigProperty:
        def __init__(
            self,
            *,
            day: typing.Optional[builtins.str] = None,
            end_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the hours of operation override config: day, start time, and end time.

            :param day: The day that the hours of operation override applies to.
            :param end_time: The end time that your contact center closes if overrides are applied.
            :param start_time: The start time when your contact center opens if overrides are applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverrideconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                hours_of_operation_override_config_property = connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty(
                    day="day",
                    end_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                        hours=123,
                        minutes=123
                    ),
                    start_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                        hours=123,
                        minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1cd95bed655e54b8d50feb6347b5e0a40e6b4343211f2fd3d0ec82dcfb96ea6)
                check_type(argname="argument day", value=day, expected_type=type_hints["day"])
                check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
                check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if day is not None:
                self._values["day"] = day
            if end_time is not None:
                self._values["end_time"] = end_time
            if start_time is not None:
                self._values["start_time"] = start_time

        @builtins.property
        def day(self) -> typing.Optional[builtins.str]:
            '''The day that the hours of operation override applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverrideconfig.html#cfn-connect-hoursofoperation-hoursofoperationoverrideconfig-day
            '''
            result = self._values.get("day")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def end_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty"]]:
            '''The end time that your contact center closes if overrides are applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverrideconfig.html#cfn-connect-hoursofoperation-hoursofoperationoverrideconfig-endtime
            '''
            result = self._values.get("end_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty"]], result)

        @builtins.property
        def start_time(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty"]]:
            '''The start time when your contact center opens if overrides are applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverrideconfig.html#cfn-connect-hoursofoperation-hoursofoperationoverrideconfig-starttime
            '''
            result = self._values.get("start_time")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationOverrideConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={
            "effective_from": "effectiveFrom",
            "effective_till": "effectiveTill",
            "hours_of_operation_override_id": "hoursOfOperationOverrideId",
            "override_config": "overrideConfig",
            "override_description": "overrideDescription",
            "override_name": "overrideName",
        },
    )
    class HoursOfOperationOverrideProperty:
        def __init__(
            self,
            *,
            effective_from: typing.Optional[builtins.str] = None,
            effective_till: typing.Optional[builtins.str] = None,
            hours_of_operation_override_id: typing.Optional[builtins.str] = None,
            override_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            override_description: typing.Optional[builtins.str] = None,
            override_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the hours of operations override.

            :param effective_from: The date from which the hours of operation override would be effective.
            :param effective_till: The date until the hours of operation override is effective.
            :param hours_of_operation_override_id: The identifier for the hours of operation override.
            :param override_config: Configuration information for the hours of operation override: day, start time, and end time.
            :param override_description: The description of the hours of operation override.
            :param override_name: The name of the hours of operation override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                hours_of_operation_override_property = connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty(
                    effective_from="effectiveFrom",
                    effective_till="effectiveTill",
                    hours_of_operation_override_id="hoursOfOperationOverrideId",
                    override_config=[connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty(
                        day="day",
                        end_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                            hours=123,
                            minutes=123
                        ),
                        start_time=connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                            hours=123,
                            minutes=123
                        )
                    )],
                    override_description="overrideDescription",
                    override_name="overrideName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7142e5d1c379872a023937f048f08602914be4773e511011a79a0c19612aa3d8)
                check_type(argname="argument effective_from", value=effective_from, expected_type=type_hints["effective_from"])
                check_type(argname="argument effective_till", value=effective_till, expected_type=type_hints["effective_till"])
                check_type(argname="argument hours_of_operation_override_id", value=hours_of_operation_override_id, expected_type=type_hints["hours_of_operation_override_id"])
                check_type(argname="argument override_config", value=override_config, expected_type=type_hints["override_config"])
                check_type(argname="argument override_description", value=override_description, expected_type=type_hints["override_description"])
                check_type(argname="argument override_name", value=override_name, expected_type=type_hints["override_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if effective_from is not None:
                self._values["effective_from"] = effective_from
            if effective_till is not None:
                self._values["effective_till"] = effective_till
            if hours_of_operation_override_id is not None:
                self._values["hours_of_operation_override_id"] = hours_of_operation_override_id
            if override_config is not None:
                self._values["override_config"] = override_config
            if override_description is not None:
                self._values["override_description"] = override_description
            if override_name is not None:
                self._values["override_name"] = override_name

        @builtins.property
        def effective_from(self) -> typing.Optional[builtins.str]:
            '''The date from which the hours of operation override would be effective.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html#cfn-connect-hoursofoperation-hoursofoperationoverride-effectivefrom
            '''
            result = self._values.get("effective_from")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def effective_till(self) -> typing.Optional[builtins.str]:
            '''The date until the hours of operation override is effective.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html#cfn-connect-hoursofoperation-hoursofoperationoverride-effectivetill
            '''
            result = self._values.get("effective_till")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hours_of_operation_override_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the hours of operation override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html#cfn-connect-hoursofoperation-hoursofoperationoverride-hoursofoperationoverrideid
            '''
            result = self._values.get("hours_of_operation_override_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def override_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty"]]]]:
            '''Configuration information for the hours of operation override: day, start time, and end time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html#cfn-connect-hoursofoperation-hoursofoperationoverride-overrideconfig
            '''
            result = self._values.get("override_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty"]]]], result)

        @builtins.property
        def override_description(self) -> typing.Optional[builtins.str]:
            '''The description of the hours of operation override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html#cfn-connect-hoursofoperation-hoursofoperationoverride-overridedescription
            '''
            result = self._values.get("override_description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def override_name(self) -> typing.Optional[builtins.str]:
            '''The name of the hours of operation override.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationoverride.html#cfn-connect-hoursofoperation-hoursofoperationoverride-overridename
            '''
            result = self._values.get("override_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty",
        jsii_struct_bases=[],
        name_mapping={"hours": "hours", "minutes": "minutes"},
    )
    class HoursOfOperationTimeSliceProperty:
        def __init__(
            self,
            *,
            hours: typing.Optional[jsii.Number] = None,
            minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The start time or end time for an hours of operation.

            :param hours: The hours.
            :param minutes: The minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                hours_of_operation_time_slice_property = connect_mixins.CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0c44bbac4d6a4774e2d0fbd02a0dbff1ef2150c5acc4ac687b4694e26ab1479)
                check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hours is not None:
                self._values["hours"] = hours
            if minutes is not None:
                self._values["minutes"] = minutes

        @builtins.property
        def hours(self) -> typing.Optional[jsii.Number]:
            '''The hours.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html#cfn-connect-hoursofoperation-hoursofoperationtimeslice-hours
            '''
            result = self._values.get("hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minutes(self) -> typing.Optional[jsii.Number]:
            '''The minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-hoursofoperationtimeslice.html#cfn-connect-hoursofoperation-hoursofoperationtimeslice-minutes
            '''
            result = self._values.get("minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HoursOfOperationTimeSliceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty",
        jsii_struct_bases=[],
        name_mapping={"hours": "hours", "minutes": "minutes"},
    )
    class OverrideTimeSliceProperty:
        def __init__(
            self,
            *,
            hours: typing.Optional[jsii.Number] = None,
            minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The start time or end time for an hours of operation override.

            :param hours: The hours.
            :param minutes: The minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-overridetimeslice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                override_time_slice_property = connect_mixins.CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty(
                    hours=123,
                    minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90489a4984583c862b32af63f926e1992b834774d64540b3798a347da24c26e0)
                check_type(argname="argument hours", value=hours, expected_type=type_hints["hours"])
                check_type(argname="argument minutes", value=minutes, expected_type=type_hints["minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hours is not None:
                self._values["hours"] = hours
            if minutes is not None:
                self._values["minutes"] = minutes

        @builtins.property
        def hours(self) -> typing.Optional[jsii.Number]:
            '''The hours.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-overridetimeslice.html#cfn-connect-hoursofoperation-overridetimeslice-hours
            '''
            result = self._values.get("hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def minutes(self) -> typing.Optional[jsii.Number]:
            '''The minutes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-hoursofoperation-overridetimeslice.html#cfn-connect-hoursofoperation-overridetimeslice-minutes
            '''
            result = self._values.get("minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OverrideTimeSliceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnInstanceAmazonConnectFlowLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceAmazonConnectFlowLogs",
):
    '''Builder for CfnInstanceLogsMixin to generate AMAZON_CONNECT_FLOW_LOGS for CfnInstance.

    :cloudformationResource: AWS::Connect::Instance
    :logType: AMAZON_CONNECT_FLOW_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_instance_amazon_connect_flow_logs = connect_mixins.CfnInstanceAmazonConnectFlowLogs()
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
    ) -> "CfnInstanceLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f524ccabc53801fb94975d482b7fb463124eafc4ebc48d654cc483de43692a36)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnInstanceLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnInstanceLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cbfb8169091793561b0df8b00000e4d9789d334697519c2e5aa85a2f3db6c86)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnInstanceLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnInstanceLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281d7ec173b2cc2ed2c930ba3c1422994f3ed06b15e2ba86daed5a450ab57641)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnInstanceLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceLogsMixin",
):
    '''*This is a preview release for Amazon Connect . It is subject to change.*.

    Initiates an Amazon Connect instance with all the supported channels enabled. It does not attach any storage, such as Amazon Simple Storage Service (Amazon S3) or Amazon Kinesis.

    Amazon Connect enforces a limit on the total number of instances that you can create or delete in 30 days. If you exceed this limit, you will get an error message indicating there has been an excessive number of attempts at creating or deleting instances. You must wait 30 days before you can restart creating and deleting instances in your account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
    :cloudformationResource: AWS::Connect::Instance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_instance_logs_mixin = connect_mixins.CfnInstanceLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Connect::Instance``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__002079279089e239349300b2d0a5903bac7ff1cab918690857c88e0aa1736826)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71c6a4401f1403f580f5c334f43bdc35c02991656897c5d9e7fcc1e7e2454623)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__283f9ad56fd54ee160928c8754f580036fea700d360077b5a1d81ad66d8622c7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AMAZON_CONNECT_FLOW_LOGS")
    def AMAZON_CONNECT_FLOW_LOGS(cls) -> CfnInstanceAmazonConnectFlowLogs:
        return typing.cast(CfnInstanceAmazonConnectFlowLogs, jsii.sget(cls, "AMAZON_CONNECT_FLOW_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "directory_id": "directoryId",
        "identity_management_type": "identityManagementType",
        "instance_alias": "instanceAlias",
        "tags": "tags",
    },
)
class CfnInstanceMixinProps:
    def __init__(
        self,
        *,
        attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstancePropsMixin.AttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        directory_id: typing.Optional[builtins.str] = None,
        identity_management_type: typing.Optional[builtins.str] = None,
        instance_alias: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInstancePropsMixin.

        :param attributes: A toggle for an individual feature at the instance level.
        :param directory_id: The identifier for the directory.
        :param identity_management_type: The identity management type.
        :param instance_alias: The alias of instance. ``InstanceAlias`` is only required when ``IdentityManagementType`` is ``CONNECT_MANAGED`` or ``SAML`` . ``InstanceAlias`` is not required when ``IdentityManagementType`` is ``EXISTING_DIRECTORY`` .
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_instance_mixin_props = connect_mixins.CfnInstanceMixinProps(
                attributes=connect_mixins.CfnInstancePropsMixin.AttributesProperty(
                    auto_resolve_best_voices=False,
                    contactflow_logs=False,
                    contact_lens=False,
                    early_media=False,
                    enhanced_chat_monitoring=False,
                    enhanced_contact_monitoring=False,
                    high_volume_out_bound=False,
                    inbound_calls=False,
                    multi_party_chat_conference=False,
                    multi_party_conference=False,
                    outbound_calls=False,
                    use_custom_tts_voices=False
                ),
                directory_id="directoryId",
                identity_management_type="identityManagementType",
                instance_alias="instanceAlias",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81d555e5cc0a05587e5cd9ae0866bc70ec9582678ae52f139da50eb3936166e)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument identity_management_type", value=identity_management_type, expected_type=type_hints["identity_management_type"])
            check_type(argname="argument instance_alias", value=instance_alias, expected_type=type_hints["instance_alias"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attributes is not None:
            self._values["attributes"] = attributes
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if identity_management_type is not None:
            self._values["identity_management_type"] = identity_management_type
        if instance_alias is not None:
            self._values["instance_alias"] = instance_alias
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.AttributesProperty"]]:
        '''A toggle for an individual feature at the instance level.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstancePropsMixin.AttributesProperty"]], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for the directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_management_type(self) -> typing.Optional[builtins.str]:
        '''The identity management type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-identitymanagementtype
        '''
        result = self._values.get("identity_management_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_alias(self) -> typing.Optional[builtins.str]:
        '''The alias of instance.

        ``InstanceAlias`` is only required when ``IdentityManagementType`` is ``CONNECT_MANAGED`` or ``SAML`` . ``InstanceAlias`` is not required when ``IdentityManagementType`` is ``EXISTING_DIRECTORY`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-instancealias
        '''
        result = self._values.get("instance_alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html#cfn-connect-instance-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstancePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstancePropsMixin",
):
    '''*This is a preview release for Amazon Connect . It is subject to change.*.

    Initiates an Amazon Connect instance with all the supported channels enabled. It does not attach any storage, such as Amazon Simple Storage Service (Amazon S3) or Amazon Kinesis.

    Amazon Connect enforces a limit on the total number of instances that you can create or delete in 30 days. If you exceed this limit, you will get an error message indicating there has been an excessive number of attempts at creating or deleting instances. You must wait 30 days before you can restart creating and deleting instances in your account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instance.html
    :cloudformationResource: AWS::Connect::Instance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_instance_props_mixin = connect_mixins.CfnInstancePropsMixin(connect_mixins.CfnInstanceMixinProps(
            attributes=connect_mixins.CfnInstancePropsMixin.AttributesProperty(
                auto_resolve_best_voices=False,
                contactflow_logs=False,
                contact_lens=False,
                early_media=False,
                enhanced_chat_monitoring=False,
                enhanced_contact_monitoring=False,
                high_volume_out_bound=False,
                inbound_calls=False,
                multi_party_chat_conference=False,
                multi_party_conference=False,
                outbound_calls=False,
                use_custom_tts_voices=False
            ),
            directory_id="directoryId",
            identity_management_type="identityManagementType",
            instance_alias="instanceAlias",
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
        props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::Instance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e89a33b79dad3c75d654636a9ed87967e6913593bd745b5aa201b6ccbfa2703)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a5f6cae604e6ca38ccfb94dac8b06a4aa72b61788c359d829f06cdb40ef85de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1920d211b1ee24c1b0c3c112ea6f5773c0f9fbc74795ff2dffcc508ae7a1db25)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceMixinProps:
        return typing.cast(CfnInstanceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstancePropsMixin.AttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_resolve_best_voices": "autoResolveBestVoices",
            "contactflow_logs": "contactflowLogs",
            "contact_lens": "contactLens",
            "early_media": "earlyMedia",
            "enhanced_chat_monitoring": "enhancedChatMonitoring",
            "enhanced_contact_monitoring": "enhancedContactMonitoring",
            "high_volume_out_bound": "highVolumeOutBound",
            "inbound_calls": "inboundCalls",
            "multi_party_chat_conference": "multiPartyChatConference",
            "multi_party_conference": "multiPartyConference",
            "outbound_calls": "outboundCalls",
            "use_custom_tts_voices": "useCustomTtsVoices",
        },
    )
    class AttributesProperty:
        def __init__(
            self,
            *,
            auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            contactflow_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            contact_lens: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            early_media: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enhanced_chat_monitoring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            enhanced_contact_monitoring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            high_volume_out_bound: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            inbound_calls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            multi_party_chat_conference: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            multi_party_conference: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            outbound_calls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''*This is a preview release for Amazon Connect .

            It is subject to change.*

            :param auto_resolve_best_voices: Boolean flag which enables AUTO_RESOLVE_BEST_VOICES on an instance.
            :param contactflow_logs: Boolean flag which enables CONTACTFLOW_LOGS on an instance.
            :param contact_lens: Boolean flag which enables CONTACT_LENS on an instance.
            :param early_media: Boolean flag which enables EARLY_MEDIA on an instance.
            :param enhanced_chat_monitoring: Boolean flag which enables ENHANCED_CHAT_MONITORING on an instance.
            :param enhanced_contact_monitoring: Boolean flag which enables ENHANCED_CONTACT_MONITORING on an instance.
            :param high_volume_out_bound: Boolean flag which enables HIGH_VOLUME_OUTBOUND on an instance.
            :param inbound_calls: Mandatory element which enables inbound calls on new instance.
            :param multi_party_chat_conference: Boolean flag which enables MULTI_PARTY_CHAT_CONFERENCE on an instance.
            :param multi_party_conference: Boolean flag which enables MULTI_PARTY_CONFERENCE on an instance.
            :param outbound_calls: Mandatory element which enables outbound calls on new instance.
            :param use_custom_tts_voices: Boolean flag which enables USE_CUSTOM_TTS_VOICES on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                attributes_property = connect_mixins.CfnInstancePropsMixin.AttributesProperty(
                    auto_resolve_best_voices=False,
                    contactflow_logs=False,
                    contact_lens=False,
                    early_media=False,
                    enhanced_chat_monitoring=False,
                    enhanced_contact_monitoring=False,
                    high_volume_out_bound=False,
                    inbound_calls=False,
                    multi_party_chat_conference=False,
                    multi_party_conference=False,
                    outbound_calls=False,
                    use_custom_tts_voices=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ffe62479f9a266bee0c3989950e29ad208de7e4d516f97732e77d312875f48ec)
                check_type(argname="argument auto_resolve_best_voices", value=auto_resolve_best_voices, expected_type=type_hints["auto_resolve_best_voices"])
                check_type(argname="argument contactflow_logs", value=contactflow_logs, expected_type=type_hints["contactflow_logs"])
                check_type(argname="argument contact_lens", value=contact_lens, expected_type=type_hints["contact_lens"])
                check_type(argname="argument early_media", value=early_media, expected_type=type_hints["early_media"])
                check_type(argname="argument enhanced_chat_monitoring", value=enhanced_chat_monitoring, expected_type=type_hints["enhanced_chat_monitoring"])
                check_type(argname="argument enhanced_contact_monitoring", value=enhanced_contact_monitoring, expected_type=type_hints["enhanced_contact_monitoring"])
                check_type(argname="argument high_volume_out_bound", value=high_volume_out_bound, expected_type=type_hints["high_volume_out_bound"])
                check_type(argname="argument inbound_calls", value=inbound_calls, expected_type=type_hints["inbound_calls"])
                check_type(argname="argument multi_party_chat_conference", value=multi_party_chat_conference, expected_type=type_hints["multi_party_chat_conference"])
                check_type(argname="argument multi_party_conference", value=multi_party_conference, expected_type=type_hints["multi_party_conference"])
                check_type(argname="argument outbound_calls", value=outbound_calls, expected_type=type_hints["outbound_calls"])
                check_type(argname="argument use_custom_tts_voices", value=use_custom_tts_voices, expected_type=type_hints["use_custom_tts_voices"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_resolve_best_voices is not None:
                self._values["auto_resolve_best_voices"] = auto_resolve_best_voices
            if contactflow_logs is not None:
                self._values["contactflow_logs"] = contactflow_logs
            if contact_lens is not None:
                self._values["contact_lens"] = contact_lens
            if early_media is not None:
                self._values["early_media"] = early_media
            if enhanced_chat_monitoring is not None:
                self._values["enhanced_chat_monitoring"] = enhanced_chat_monitoring
            if enhanced_contact_monitoring is not None:
                self._values["enhanced_contact_monitoring"] = enhanced_contact_monitoring
            if high_volume_out_bound is not None:
                self._values["high_volume_out_bound"] = high_volume_out_bound
            if inbound_calls is not None:
                self._values["inbound_calls"] = inbound_calls
            if multi_party_chat_conference is not None:
                self._values["multi_party_chat_conference"] = multi_party_chat_conference
            if multi_party_conference is not None:
                self._values["multi_party_conference"] = multi_party_conference
            if outbound_calls is not None:
                self._values["outbound_calls"] = outbound_calls
            if use_custom_tts_voices is not None:
                self._values["use_custom_tts_voices"] = use_custom_tts_voices

        @builtins.property
        def auto_resolve_best_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables AUTO_RESOLVE_BEST_VOICES on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-autoresolvebestvoices
            '''
            result = self._values.get("auto_resolve_best_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def contactflow_logs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables CONTACTFLOW_LOGS on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactflowlogs
            '''
            result = self._values.get("contactflow_logs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def contact_lens(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables CONTACT_LENS on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-contactlens
            '''
            result = self._values.get("contact_lens")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def early_media(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables EARLY_MEDIA on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-earlymedia
            '''
            result = self._values.get("early_media")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enhanced_chat_monitoring(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables ENHANCED_CHAT_MONITORING on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-enhancedchatmonitoring
            '''
            result = self._values.get("enhanced_chat_monitoring")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def enhanced_contact_monitoring(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables ENHANCED_CONTACT_MONITORING on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-enhancedcontactmonitoring
            '''
            result = self._values.get("enhanced_contact_monitoring")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def high_volume_out_bound(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables HIGH_VOLUME_OUTBOUND on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-highvolumeoutbound
            '''
            result = self._values.get("high_volume_out_bound")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def inbound_calls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Mandatory element which enables inbound calls on new instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-inboundcalls
            '''
            result = self._values.get("inbound_calls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def multi_party_chat_conference(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables MULTI_PARTY_CHAT_CONFERENCE on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-multipartychatconference
            '''
            result = self._values.get("multi_party_chat_conference")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def multi_party_conference(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables MULTI_PARTY_CONFERENCE on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-multipartyconference
            '''
            result = self._values.get("multi_party_conference")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def outbound_calls(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Mandatory element which enables outbound calls on new instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-outboundcalls
            '''
            result = self._values.get("outbound_calls")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_custom_tts_voices(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean flag which enables USE_CUSTOM_TTS_VOICES on an instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instance-attributes.html#cfn-connect-instance-attributes-usecustomttsvoices
            '''
            result = self._values.get("use_custom_tts_voices")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "kinesis_firehose_config": "kinesisFirehoseConfig",
        "kinesis_stream_config": "kinesisStreamConfig",
        "kinesis_video_stream_config": "kinesisVideoStreamConfig",
        "resource_type": "resourceType",
        "s3_config": "s3Config",
        "storage_type": "storageType",
    },
)
class CfnInstanceStorageConfigMixinProps:
    def __init__(
        self,
        *,
        instance_arn: typing.Optional[builtins.str] = None,
        kinesis_firehose_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_stream_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kinesis_video_stream_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceStorageConfigPropsMixin.S3ConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInstanceStorageConfigPropsMixin.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param kinesis_firehose_config: The configuration of the Kinesis Firehose delivery stream.
        :param kinesis_stream_config: The configuration of the Kinesis data stream.
        :param kinesis_video_stream_config: The configuration of the Kinesis video stream.
        :param resource_type: A valid resource type. Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``
        :param s3_config: The S3 bucket configuration.
        :param storage_type: A valid storage type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_instance_storage_config_mixin_props = connect_mixins.CfnInstanceStorageConfigMixinProps(
                instance_arn="instanceArn",
                kinesis_firehose_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                ),
                kinesis_stream_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                ),
                kinesis_video_stream_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty(
                    encryption_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    ),
                    prefix="prefix",
                    retention_period_hours=123
                ),
                resource_type="resourceType",
                s3_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    encryption_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                ),
                storage_type="storageType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49be8be49fc7e60bc6603c25a10b13bb9152432b01b00975bb9c7255a04a2647)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument kinesis_firehose_config", value=kinesis_firehose_config, expected_type=type_hints["kinesis_firehose_config"])
            check_type(argname="argument kinesis_stream_config", value=kinesis_stream_config, expected_type=type_hints["kinesis_stream_config"])
            check_type(argname="argument kinesis_video_stream_config", value=kinesis_video_stream_config, expected_type=type_hints["kinesis_video_stream_config"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument s3_config", value=s3_config, expected_type=type_hints["s3_config"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if kinesis_firehose_config is not None:
            self._values["kinesis_firehose_config"] = kinesis_firehose_config
        if kinesis_stream_config is not None:
            self._values["kinesis_stream_config"] = kinesis_stream_config
        if kinesis_video_stream_config is not None:
            self._values["kinesis_video_stream_config"] = kinesis_video_stream_config
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if s3_config is not None:
            self._values["s3_config"] = s3_config
        if storage_type is not None:
            self._values["storage_type"] = storage_type

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis_firehose_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty"]]:
        '''The configuration of the Kinesis Firehose delivery stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig
        '''
        result = self._values.get("kinesis_firehose_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty"]], result)

    @builtins.property
    def kinesis_stream_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty"]]:
        '''The configuration of the Kinesis data stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig
        '''
        result = self._values.get("kinesis_stream_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty"]], result)

    @builtins.property
    def kinesis_video_stream_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty"]]:
        '''The configuration of the Kinesis video stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig
        '''
        result = self._values.get("kinesis_video_stream_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty"]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''A valid resource type.

        Following are the valid resource types: ``CHAT_TRANSCRIPTS`` | ``CALL_RECORDINGS`` | ``SCHEDULED_REPORTS`` | ``MEDIA_STREAMS`` | ``CONTACT_TRACE_RECORDS`` | ``AGENT_EVENTS``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.S3ConfigProperty"]]:
        '''The S3 bucket configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-s3config
        '''
        result = self._values.get("s3_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.S3ConfigProperty"]], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''A valid storage type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html#cfn-connect-instancestorageconfig-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceStorageConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceStorageConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigPropsMixin",
):
    '''The storage configuration for the instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-instancestorageconfig.html
    :cloudformationResource: AWS::Connect::InstanceStorageConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_instance_storage_config_props_mixin = connect_mixins.CfnInstanceStorageConfigPropsMixin(connect_mixins.CfnInstanceStorageConfigMixinProps(
            instance_arn="instanceArn",
            kinesis_firehose_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty(
                firehose_arn="firehoseArn"
            ),
            kinesis_stream_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty(
                stream_arn="streamArn"
            ),
            kinesis_video_stream_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty(
                encryption_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                ),
                prefix="prefix",
                retention_period_hours=123
            ),
            resource_type="resourceType",
            s3_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.S3ConfigProperty(
                bucket_name="bucketName",
                bucket_prefix="bucketPrefix",
                encryption_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            ),
            storage_type="storageType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceStorageConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::InstanceStorageConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caed2c11b928c1ea98a54262d071e9af00f2658bea49ff2098900b320e9f10c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b13492084d545024a8c3532f3ae93cf9b0e7674d50ea89c2ce61f2e0ab70d307)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2592945ee9cd3b2ab27b6312c38695c34a8e4f6be93f94fd1539e9a538b961c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceStorageConfigMixinProps:
        return typing.cast(CfnInstanceStorageConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"encryption_type": "encryptionType", "key_id": "keyId"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            encryption_type: typing.Optional[builtins.str] = None,
            key_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The encryption configuration.

            :param encryption_type: The type of encryption.
            :param key_id: The full ARN of the encryption key. .. epigraph:: Be sure to provide the full ARN of the encryption key, not just the ID. Amazon Connect supports only KMS keys with the default key spec of ```SYMMETRIC_DEFAULT`` <https://docs.aws.amazon.com/kms/latest/developerguide/asymmetric-key-specs.html#key-spec-symmetric-default>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                encryption_config_property = connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                    encryption_type="encryptionType",
                    key_id="keyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8a14003fb5038a988d306ec31fc28aea979735b3b815d4407327a564e094556)
                check_type(argname="argument encryption_type", value=encryption_type, expected_type=type_hints["encryption_type"])
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_type is not None:
                self._values["encryption_type"] = encryption_type
            if key_id is not None:
                self._values["key_id"] = key_id

        @builtins.property
        def encryption_type(self) -> typing.Optional[builtins.str]:
            '''The type of encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html#cfn-connect-instancestorageconfig-encryptionconfig-encryptiontype
            '''
            result = self._values.get("encryption_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_id(self) -> typing.Optional[builtins.str]:
            '''The full ARN of the encryption key.

            .. epigraph::

               Be sure to provide the full ARN of the encryption key, not just the ID.

               Amazon Connect supports only KMS keys with the default key spec of ```SYMMETRIC_DEFAULT`` <https://docs.aws.amazon.com/kms/latest/developerguide/asymmetric-key-specs.html#key-spec-symmetric-default>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-encryptionconfig.html#cfn-connect-instancestorageconfig-encryptionconfig-keyid
            '''
            result = self._values.get("key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"firehose_arn": "firehoseArn"},
    )
    class KinesisFirehoseConfigProperty:
        def __init__(
            self,
            *,
            firehose_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration information of a Kinesis Data Firehose delivery stream.

            :param firehose_arn: The Amazon Resource Name (ARN) of the delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisfirehoseconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                kinesis_firehose_config_property = connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty(
                    firehose_arn="firehoseArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d6d3410c16e53dd14a6ba32c400347efbcb2d1d668ab0a1ef58eec1debc0b87)
                check_type(argname="argument firehose_arn", value=firehose_arn, expected_type=type_hints["firehose_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if firehose_arn is not None:
                self._values["firehose_arn"] = firehose_arn

        @builtins.property
        def firehose_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisfirehoseconfig.html#cfn-connect-instancestorageconfig-kinesisfirehoseconfig-firehosearn
            '''
            result = self._values.get("firehose_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"stream_arn": "streamArn"},
    )
    class KinesisStreamConfigProperty:
        def __init__(self, *, stream_arn: typing.Optional[builtins.str] = None) -> None:
            '''Configuration information of a Kinesis data stream.

            :param stream_arn: The Amazon Resource Name (ARN) of the data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisstreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                kinesis_stream_config_property = connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty(
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7378e4d0364b03e9a42f2978c8e38e6d7f3e426a050dfb5cbb726b4e1ed7f6d4)
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the data stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisstreamconfig.html#cfn-connect-instancestorageconfig-kinesisstreamconfig-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "encryption_config": "encryptionConfig",
            "prefix": "prefix",
            "retention_period_hours": "retentionPeriodHours",
        },
    )
    class KinesisVideoStreamConfigProperty:
        def __init__(
            self,
            *,
            encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            prefix: typing.Optional[builtins.str] = None,
            retention_period_hours: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Configuration information of a Kinesis video stream.

            :param encryption_config: The encryption configuration.
            :param prefix: The prefix of the video stream.
            :param retention_period_hours: The number of hours data is retained in the stream. Kinesis Video Streams retains the data in a data store that is associated with the stream. The default value is 0, indicating that the stream does not persist data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                kinesis_video_stream_config_property = connect_mixins.CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty(
                    encryption_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    ),
                    prefix="prefix",
                    retention_period_hours=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1abcf8b63206f586fb8d9d21908f64c252929d1059c89f453593a76fac966957)
                check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument retention_period_hours", value=retention_period_hours, expected_type=type_hints["retention_period_hours"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encryption_config is not None:
                self._values["encryption_config"] = encryption_config
            if prefix is not None:
                self._values["prefix"] = prefix
            if retention_period_hours is not None:
                self._values["retention_period_hours"] = retention_period_hours

        @builtins.property
        def encryption_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty"]]:
            '''The encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty"]], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix of the video stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_period_hours(self) -> typing.Optional[jsii.Number]:
            '''The number of hours data is retained in the stream.

            Kinesis Video Streams retains the data in a data store that is associated with the stream.

            The default value is 0, indicating that the stream does not persist data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-kinesisvideostreamconfig.html#cfn-connect-instancestorageconfig-kinesisvideostreamconfig-retentionperiodhours
            '''
            result = self._values.get("retention_period_hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisVideoStreamConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnInstanceStorageConfigPropsMixin.S3ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "bucket_prefix": "bucketPrefix",
            "encryption_config": "encryptionConfig",
        },
    )
    class S3ConfigProperty:
        def __init__(
            self,
            *,
            bucket_name: typing.Optional[builtins.str] = None,
            bucket_prefix: typing.Optional[builtins.str] = None,
            encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about the Amazon Simple Storage Service (Amazon S3) storage type.

            :param bucket_name: The S3 bucket name.
            :param bucket_prefix: The S3 bucket prefix.
            :param encryption_config: The Amazon S3 encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                s3_config_property = connect_mixins.CfnInstanceStorageConfigPropsMixin.S3ConfigProperty(
                    bucket_name="bucketName",
                    bucket_prefix="bucketPrefix",
                    encryption_config=connect_mixins.CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty(
                        encryption_type="encryptionType",
                        key_id="keyId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b19039f27bc824feabc24feb7d612741db9d231423b3843a87346ecbd672ee2)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument bucket_prefix", value=bucket_prefix, expected_type=type_hints["bucket_prefix"])
                check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_name is not None:
                self._values["bucket_name"] = bucket_name
            if bucket_prefix is not None:
                self._values["bucket_prefix"] = bucket_prefix
            if encryption_config is not None:
                self._values["encryption_config"] = encryption_config

        @builtins.property
        def bucket_name(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-bucketname
            '''
            result = self._values.get("bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket prefix.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-bucketprefix
            '''
            result = self._values.get("bucket_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty"]]:
            '''The Amazon S3 encryption configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-instancestorageconfig-s3config.html#cfn-connect-instancestorageconfig-s3config-encryptionconfig
            '''
            result = self._values.get("encryption_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnIntegrationAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_id": "instanceId",
        "integration_arn": "integrationArn",
        "integration_type": "integrationType",
    },
)
class CfnIntegrationAssociationMixinProps:
    def __init__(
        self,
        *,
        instance_id: typing.Optional[builtins.str] = None,
        integration_arn: typing.Optional[builtins.str] = None,
        integration_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIntegrationAssociationPropsMixin.

        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param integration_arn: ARN of the integration being associated with the instance. *Minimum* : ``1`` *Maximum* : ``140``
        :param integration_type: Specifies the integration type to be associated with the instance. *Allowed Values* : ``LEX_BOT`` | ``LAMBDA_FUNCTION``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_integration_association_mixin_props = connect_mixins.CfnIntegrationAssociationMixinProps(
                instance_id="instanceId",
                integration_arn="integrationArn",
                integration_type="integrationType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d6234f1b8cd3382d0829ce424ec867997a2292ed8c50e173d838fc50bf0e8a)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument integration_arn", value=integration_arn, expected_type=type_hints["integration_arn"])
            check_type(argname="argument integration_type", value=integration_type, expected_type=type_hints["integration_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if integration_arn is not None:
            self._values["integration_arn"] = integration_arn
        if integration_type is not None:
            self._values["integration_type"] = integration_type

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_arn(self) -> typing.Optional[builtins.str]:
        '''ARN of the integration being associated with the instance.

        *Minimum* : ``1``

        *Maximum* : ``140``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-integrationarn
        '''
        result = self._values.get("integration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_type(self) -> typing.Optional[builtins.str]:
        '''Specifies the integration type to be associated with the instance.

        *Allowed Values* : ``LEX_BOT`` | ``LAMBDA_FUNCTION``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html#cfn-connect-integrationassociation-integrationtype
        '''
        result = self._values.get("integration_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIntegrationAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIntegrationAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnIntegrationAssociationPropsMixin",
):
    '''Specifies the association of an AWS resource such as Lex bot (both v1 and v2) and Lambda function with an Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-integrationassociation.html
    :cloudformationResource: AWS::Connect::IntegrationAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_integration_association_props_mixin = connect_mixins.CfnIntegrationAssociationPropsMixin(connect_mixins.CfnIntegrationAssociationMixinProps(
            instance_id="instanceId",
            integration_arn="integrationArn",
            integration_type="integrationType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnIntegrationAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::IntegrationAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326d8daff01b4f6af2f10cff06807155fef39148dff17e600b94bc2189c0ca0d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e4fd4046df6275b2a93e573885bcc436a5f6c916e2188e965d61c1d4656fc0fc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c7f6023e54366affb403306667930bd68d77e5a3e9bdc36a84547d7da3d084)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIntegrationAssociationMixinProps:
        return typing.cast(CfnIntegrationAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPhoneNumberMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "country_code": "countryCode",
        "description": "description",
        "prefix": "prefix",
        "source_phone_number_arn": "sourcePhoneNumberArn",
        "tags": "tags",
        "target_arn": "targetArn",
        "type": "type",
    },
)
class CfnPhoneNumberMixinProps:
    def __init__(
        self,
        *,
        country_code: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        prefix: typing.Optional[builtins.str] = None,
        source_phone_number_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPhoneNumberPropsMixin.

        :param country_code: The ISO country code.
        :param description: The description of the phone number.
        :param prefix: The prefix of the phone number. If provided, it must contain ``+`` as part of the country code. *Pattern* : ``^\\\\+[0-9]{1,15}``
        :param source_phone_number_arn: The claimed phone number ARN that was previously imported from the external service, such as AWS End User Messaging. If it is from AWS End User Messaging, it looks like the ARN of the phone number that was imported from AWS End User Messaging.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        :param target_arn: The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.
        :param type: The type of phone number.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_phone_number_mixin_props = connect_mixins.CfnPhoneNumberMixinProps(
                country_code="countryCode",
                description="description",
                prefix="prefix",
                source_phone_number_arn="sourcePhoneNumberArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arn="targetArn",
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e05114daef5981fdb19b4b5d2d306c934b15a5bee6ae8e31e3846be5cf31ab29)
            check_type(argname="argument country_code", value=country_code, expected_type=type_hints["country_code"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument source_phone_number_arn", value=source_phone_number_arn, expected_type=type_hints["source_phone_number_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if country_code is not None:
            self._values["country_code"] = country_code
        if description is not None:
            self._values["description"] = description
        if prefix is not None:
            self._values["prefix"] = prefix
        if source_phone_number_arn is not None:
            self._values["source_phone_number_arn"] = source_phone_number_arn
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def country_code(self) -> typing.Optional[builtins.str]:
        '''The ISO country code.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-countrycode
        '''
        result = self._values.get("country_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the phone number.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix of the phone number. If provided, it must contain ``+`` as part of the country code.

        *Pattern* : ``^\\\\+[0-9]{1,15}``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-prefix
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_phone_number_arn(self) -> typing.Optional[builtins.str]:
        '''The claimed phone number ARN that was previously imported from the external service, such as AWS End User Messaging.

        If it is from AWS End User Messaging, it looks like the ARN of the phone number that was imported from AWS End User Messaging.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-sourcephonenumberarn
        '''
        result = self._values.get("source_phone_number_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for Amazon Connect instances or traffic distribution group that phone numbers are claimed to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-targetarn
        '''
        result = self._values.get("target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of phone number.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html#cfn-connect-phonenumber-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPhoneNumberMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPhoneNumberPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPhoneNumberPropsMixin",
):
    '''Claims a phone number to the specified Amazon Connect instance or traffic distribution group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-phonenumber.html
    :cloudformationResource: AWS::Connect::PhoneNumber
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_phone_number_props_mixin = connect_mixins.CfnPhoneNumberPropsMixin(connect_mixins.CfnPhoneNumberMixinProps(
            country_code="countryCode",
            description="description",
            prefix="prefix",
            source_phone_number_arn="sourcePhoneNumberArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_arn="targetArn",
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPhoneNumberMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::PhoneNumber``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69682a1a0ee9423911b1548ba54a4b551074037b38c3383ec9cc17604238ab5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__762d1ca975a679483e492982fc3ba458893cc127472f5f75da965a13b34719d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7959b9d200821617dd17e71181bf15303211acb075e997f1766d6202122599ac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPhoneNumberMixinProps:
        return typing.cast(CfnPhoneNumberMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPredefinedAttributeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_configuration": "attributeConfiguration",
        "instance_arn": "instanceArn",
        "name": "name",
        "purposes": "purposes",
        "values": "values",
    },
)
class CfnPredefinedAttributeMixinProps:
    def __init__(
        self,
        *,
        attribute_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        purposes: typing.Optional[typing.Sequence[builtins.str]] = None,
        values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPredefinedAttributePropsMixin.ValuesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPredefinedAttributePropsMixin.

        :param attribute_configuration: Custom metadata that is associated to predefined attributes to control behavior in upstream services, such as controlling how a predefined attribute should be displayed in the Amazon Connect admin website.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the predefined attribute.
        :param purposes: Values that enable you to categorize your predefined attributes. You can use them in custom UI elements across the Amazon Connect admin website.
        :param values: The values of a predefined attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_predefined_attribute_mixin_props = connect_mixins.CfnPredefinedAttributeMixinProps(
                attribute_configuration=connect_mixins.CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty(
                    enable_value_validation_on_association=False,
                    is_read_only=False
                ),
                instance_arn="instanceArn",
                name="name",
                purposes=["purposes"],
                values=connect_mixins.CfnPredefinedAttributePropsMixin.ValuesProperty(
                    string_list=["stringList"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22af6c1aaf951525be21f8474aa83609b5b1c40d6741c38a433420528cd827c4)
            check_type(argname="argument attribute_configuration", value=attribute_configuration, expected_type=type_hints["attribute_configuration"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument purposes", value=purposes, expected_type=type_hints["purposes"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_configuration is not None:
            self._values["attribute_configuration"] = attribute_configuration
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if purposes is not None:
            self._values["purposes"] = purposes
        if values is not None:
            self._values["values"] = values

    @builtins.property
    def attribute_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty"]]:
        '''Custom metadata that is associated to predefined attributes to control behavior in upstream services, such as controlling how a predefined attribute should be displayed in the Amazon Connect admin website.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html#cfn-connect-predefinedattribute-attributeconfiguration
        '''
        result = self._values.get("attribute_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty"]], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html#cfn-connect-predefinedattribute-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the predefined attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html#cfn-connect-predefinedattribute-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def purposes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Values that enable you to categorize your predefined attributes.

        You can use them in custom UI elements across the Amazon Connect admin website.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html#cfn-connect-predefinedattribute-purposes
        '''
        result = self._values.get("purposes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def values(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPredefinedAttributePropsMixin.ValuesProperty"]]:
        '''The values of a predefined attribute.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html#cfn-connect-predefinedattribute-values
        '''
        result = self._values.get("values")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPredefinedAttributePropsMixin.ValuesProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPredefinedAttributeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPredefinedAttributePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPredefinedAttributePropsMixin",
):
    '''Textual or numeric value that describes an attribute.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-predefinedattribute.html
    :cloudformationResource: AWS::Connect::PredefinedAttribute
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_predefined_attribute_props_mixin = connect_mixins.CfnPredefinedAttributePropsMixin(connect_mixins.CfnPredefinedAttributeMixinProps(
            attribute_configuration=connect_mixins.CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty(
                enable_value_validation_on_association=False,
                is_read_only=False
            ),
            instance_arn="instanceArn",
            name="name",
            purposes=["purposes"],
            values=connect_mixins.CfnPredefinedAttributePropsMixin.ValuesProperty(
                string_list=["stringList"]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPredefinedAttributeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::PredefinedAttribute``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50bee6780b5b34043175433cdeada2df6caba4f07908853822e64b95a5cb1804)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15d5e76c2a25cdfb82b92cff7bc7ce41d8d22ec3d227c8aab2d9dd2f90954930)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__714839b7bf128b53357fd7213541c87025918720ecc9fbe4726a6e15e3ff334a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPredefinedAttributeMixinProps:
        return typing.cast(CfnPredefinedAttributeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_value_validation_on_association": "enableValueValidationOnAssociation",
            "is_read_only": "isReadOnly",
        },
    )
    class AttributeConfigurationProperty:
        def __init__(
            self,
            *,
            enable_value_validation_on_association: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            is_read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Custom metadata associated to a Predefined attribute that controls how the attribute behaves when used by upstream services.

            :param enable_value_validation_on_association: Enables customers to enforce strict validation on the specific values that this predefined attribute can hold.
            :param is_read_only: Allows the predefined attribute to show up and be managed in the Amazon Connect UI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-predefinedattribute-attributeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                attribute_configuration_property = connect_mixins.CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty(
                    enable_value_validation_on_association=False,
                    is_read_only=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b67c47cbca611d28ef23f7b234081488133a8108d0fc74197b0b93bb0d5cb77a)
                check_type(argname="argument enable_value_validation_on_association", value=enable_value_validation_on_association, expected_type=type_hints["enable_value_validation_on_association"])
                check_type(argname="argument is_read_only", value=is_read_only, expected_type=type_hints["is_read_only"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_value_validation_on_association is not None:
                self._values["enable_value_validation_on_association"] = enable_value_validation_on_association
            if is_read_only is not None:
                self._values["is_read_only"] = is_read_only

        @builtins.property
        def enable_value_validation_on_association(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables customers to enforce strict validation on the specific values that this predefined attribute can hold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-predefinedattribute-attributeconfiguration.html#cfn-connect-predefinedattribute-attributeconfiguration-enablevaluevalidationonassociation
            '''
            result = self._values.get("enable_value_validation_on_association")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def is_read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows the predefined attribute to show up and be managed in the Amazon Connect UI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-predefinedattribute-attributeconfiguration.html#cfn-connect-predefinedattribute-attributeconfiguration-isreadonly
            '''
            result = self._values.get("is_read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPredefinedAttributePropsMixin.ValuesProperty",
        jsii_struct_bases=[],
        name_mapping={"string_list": "stringList"},
    )
    class ValuesProperty:
        def __init__(
            self,
            *,
            string_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The values of a predefined attribute.

            :param string_list: Predefined attribute values of type string list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-predefinedattribute-values.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                values_property = connect_mixins.CfnPredefinedAttributePropsMixin.ValuesProperty(
                    string_list=["stringList"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f5608dd66bdaad22d2338c6bd4c9964e499f681aab7e2e0daaae17b22f70d0f)
                check_type(argname="argument string_list", value=string_list, expected_type=type_hints["string_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if string_list is not None:
                self._values["string_list"] = string_list

        @builtins.property
        def string_list(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Predefined attribute values of type string list.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-predefinedattribute-values.html#cfn-connect-predefinedattribute-values-stringlist
            '''
            result = self._values.get("string_list")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValuesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPromptMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "s3_uri": "s3Uri",
        "tags": "tags",
    },
)
class CfnPromptMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        s3_uri: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPromptPropsMixin.

        :param description: The description of the prompt.
        :param instance_arn: The identifier of the Amazon Connect instance.
        :param name: The name of the prompt.
        :param s3_uri: The URI for the S3 bucket where the prompt is stored. This property is required when you create a prompt.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_prompt_mixin_props = connect_mixins.CfnPromptMixinProps(
                description="description",
                instance_arn="instanceArn",
                name="name",
                s3_uri="s3Uri",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4098b1cda862652bff9e159070722b5d0832330a97be0763f0aa3f2c325508c5)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument s3_uri", value=s3_uri, expected_type=type_hints["s3_uri"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if s3_uri is not None:
            self._values["s3_uri"] = s3_uri
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html#cfn-connect-prompt-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html#cfn-connect-prompt-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html#cfn-connect-prompt-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_uri(self) -> typing.Optional[builtins.str]:
        '''The URI for the S3 bucket where the prompt is stored.

        This property is required when you create a prompt.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html#cfn-connect-prompt-s3uri
        '''
        result = self._values.get("s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html#cfn-connect-prompt-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPromptMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPromptPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnPromptPropsMixin",
):
    '''Creates a prompt for the specified Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-prompt.html
    :cloudformationResource: AWS::Connect::Prompt
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_prompt_props_mixin = connect_mixins.CfnPromptPropsMixin(connect_mixins.CfnPromptMixinProps(
            description="description",
            instance_arn="instanceArn",
            name="name",
            s3_uri="s3Uri",
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
        props: typing.Union[CfnPromptMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::Prompt``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aafbe36e72a86a8b3b7fd62a16c3e80c73d11b38254963e371ecc77760ea227f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6dafe59880cb651cacb6f796a7aec73ee7cc98e3d798d4bb50b30d1d1e52f14)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92da6224e86699311dc3ff5e77be33c3f03201ea468d2886335d74252ce35ada)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPromptMixinProps:
        return typing.cast(CfnPromptMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQueueMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "hours_of_operation_arn": "hoursOfOperationArn",
        "instance_arn": "instanceArn",
        "max_contacts": "maxContacts",
        "name": "name",
        "outbound_caller_config": "outboundCallerConfig",
        "outbound_email_config": "outboundEmailConfig",
        "quick_connect_arns": "quickConnectArns",
        "status": "status",
        "tags": "tags",
    },
)
class CfnQueueMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        hours_of_operation_arn: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        max_contacts: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        outbound_caller_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.OutboundCallerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outbound_email_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQueuePropsMixin.OutboundEmailConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        quick_connect_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnQueuePropsMixin.

        :param description: The description of the queue.
        :param hours_of_operation_arn: The Amazon Resource Name (ARN) of the hours of operation.
        :param instance_arn: The identifier of the Amazon Connect instance.
        :param max_contacts: The maximum number of contacts that can be in the queue before it is considered full.
        :param name: The name of the queue.
        :param outbound_caller_config: The outbound caller ID name, number, and outbound whisper flow.
        :param outbound_email_config: The outbound email address ID for a specified queue.
        :param quick_connect_arns: The Amazon Resource Names (ARN) of the of the quick connects available to agents who are working the queue.
        :param status: The status of the queue.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_queue_mixin_props = connect_mixins.CfnQueueMixinProps(
                description="description",
                hours_of_operation_arn="hoursOfOperationArn",
                instance_arn="instanceArn",
                max_contacts=123,
                name="name",
                outbound_caller_config=connect_mixins.CfnQueuePropsMixin.OutboundCallerConfigProperty(
                    outbound_caller_id_name="outboundCallerIdName",
                    outbound_caller_id_number_arn="outboundCallerIdNumberArn",
                    outbound_flow_arn="outboundFlowArn"
                ),
                outbound_email_config=connect_mixins.CfnQueuePropsMixin.OutboundEmailConfigProperty(
                    outbound_email_address_id="outboundEmailAddressId"
                ),
                quick_connect_arns=["quickConnectArns"],
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2ee9c47eb4e64a55a58d6b1e31a2b775f04cc55c2818fa386143c8ed555c33a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument hours_of_operation_arn", value=hours_of_operation_arn, expected_type=type_hints["hours_of_operation_arn"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument max_contacts", value=max_contacts, expected_type=type_hints["max_contacts"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outbound_caller_config", value=outbound_caller_config, expected_type=type_hints["outbound_caller_config"])
            check_type(argname="argument outbound_email_config", value=outbound_email_config, expected_type=type_hints["outbound_email_config"])
            check_type(argname="argument quick_connect_arns", value=quick_connect_arns, expected_type=type_hints["quick_connect_arns"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if hours_of_operation_arn is not None:
            self._values["hours_of_operation_arn"] = hours_of_operation_arn
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if max_contacts is not None:
            self._values["max_contacts"] = max_contacts
        if name is not None:
            self._values["name"] = name
        if outbound_caller_config is not None:
            self._values["outbound_caller_config"] = outbound_caller_config
        if outbound_email_config is not None:
            self._values["outbound_email_config"] = outbound_email_config
        if quick_connect_arns is not None:
            self._values["quick_connect_arns"] = quick_connect_arns
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hours_of_operation_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the hours of operation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-hoursofoperationarn
        '''
        result = self._values.get("hours_of_operation_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_contacts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of contacts that can be in the queue before it is considered full.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-maxcontacts
        '''
        result = self._values.get("max_contacts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_caller_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.OutboundCallerConfigProperty"]]:
        '''The outbound caller ID name, number, and outbound whisper flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-outboundcallerconfig
        '''
        result = self._values.get("outbound_caller_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.OutboundCallerConfigProperty"]], result)

    @builtins.property
    def outbound_email_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.OutboundEmailConfigProperty"]]:
        '''The outbound email address ID for a specified queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-outboundemailconfig
        '''
        result = self._values.get("outbound_email_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQueuePropsMixin.OutboundEmailConfigProperty"]], result)

    @builtins.property
    def quick_connect_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Names (ARN) of the of the quick connects available to agents who are working the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-quickconnectarns
        '''
        result = self._values.get("quick_connect_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the queue.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html#cfn-connect-queue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQueueMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQueuePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQueuePropsMixin",
):
    '''Contains information about a queue.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-queue.html
    :cloudformationResource: AWS::Connect::Queue
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_queue_props_mixin = connect_mixins.CfnQueuePropsMixin(connect_mixins.CfnQueueMixinProps(
            description="description",
            hours_of_operation_arn="hoursOfOperationArn",
            instance_arn="instanceArn",
            max_contacts=123,
            name="name",
            outbound_caller_config=connect_mixins.CfnQueuePropsMixin.OutboundCallerConfigProperty(
                outbound_caller_id_name="outboundCallerIdName",
                outbound_caller_id_number_arn="outboundCallerIdNumberArn",
                outbound_flow_arn="outboundFlowArn"
            ),
            outbound_email_config=connect_mixins.CfnQueuePropsMixin.OutboundEmailConfigProperty(
                outbound_email_address_id="outboundEmailAddressId"
            ),
            quick_connect_arns=["quickConnectArns"],
            status="status",
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
        props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::Queue``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46b62bedf99e60fb0a5c1e7859b5a2ac251a768a701cf76dc622c9b4e64cb7be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5661c6ff214de690bc733dd53e2a4b68938155dd05eedf22306075b928e38920)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b1d57a18285983ab02b162630d50a7c1ac03335e33544cb1ba899d51b8345d3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQueueMixinProps:
        return typing.cast(CfnQueueMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQueuePropsMixin.OutboundCallerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "outbound_caller_id_name": "outboundCallerIdName",
            "outbound_caller_id_number_arn": "outboundCallerIdNumberArn",
            "outbound_flow_arn": "outboundFlowArn",
        },
    )
    class OutboundCallerConfigProperty:
        def __init__(
            self,
            *,
            outbound_caller_id_name: typing.Optional[builtins.str] = None,
            outbound_caller_id_number_arn: typing.Optional[builtins.str] = None,
            outbound_flow_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The outbound caller ID name, number, and outbound whisper flow.

            :param outbound_caller_id_name: The caller ID name.
            :param outbound_caller_id_number_arn: The Amazon Resource Name (ARN) of the outbound caller ID number. .. epigraph:: Only use the phone number ARN format that doesn't contain ``instance`` in the path, for example, ``arn:aws:connect:us-east-1:1234567890:phone-number/uuid`` . This is the same ARN format that is returned when you create a phone number using CloudFormation , or when you call the `ListPhoneNumbersV2 <https://docs.aws.amazon.com/connect/latest/APIReference/API_ListPhoneNumbersV2.html>`_ API.
            :param outbound_flow_arn: The Amazon Resource Name (ARN) of the outbound flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-queue-outboundcallerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                outbound_caller_config_property = connect_mixins.CfnQueuePropsMixin.OutboundCallerConfigProperty(
                    outbound_caller_id_name="outboundCallerIdName",
                    outbound_caller_id_number_arn="outboundCallerIdNumberArn",
                    outbound_flow_arn="outboundFlowArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b805fc08c1922ddf61c172b2134a5e1c8c836b0d2d482e61c619c4af41f4e3b)
                check_type(argname="argument outbound_caller_id_name", value=outbound_caller_id_name, expected_type=type_hints["outbound_caller_id_name"])
                check_type(argname="argument outbound_caller_id_number_arn", value=outbound_caller_id_number_arn, expected_type=type_hints["outbound_caller_id_number_arn"])
                check_type(argname="argument outbound_flow_arn", value=outbound_flow_arn, expected_type=type_hints["outbound_flow_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if outbound_caller_id_name is not None:
                self._values["outbound_caller_id_name"] = outbound_caller_id_name
            if outbound_caller_id_number_arn is not None:
                self._values["outbound_caller_id_number_arn"] = outbound_caller_id_number_arn
            if outbound_flow_arn is not None:
                self._values["outbound_flow_arn"] = outbound_flow_arn

        @builtins.property
        def outbound_caller_id_name(self) -> typing.Optional[builtins.str]:
            '''The caller ID name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-queue-outboundcallerconfig.html#cfn-connect-queue-outboundcallerconfig-outboundcalleridname
            '''
            result = self._values.get("outbound_caller_id_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def outbound_caller_id_number_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the outbound caller ID number.

            .. epigraph::

               Only use the phone number ARN format that doesn't contain ``instance`` in the path, for example, ``arn:aws:connect:us-east-1:1234567890:phone-number/uuid`` . This is the same ARN format that is returned when you create a phone number using CloudFormation , or when you call the `ListPhoneNumbersV2 <https://docs.aws.amazon.com/connect/latest/APIReference/API_ListPhoneNumbersV2.html>`_ API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-queue-outboundcallerconfig.html#cfn-connect-queue-outboundcallerconfig-outboundcalleridnumberarn
            '''
            result = self._values.get("outbound_caller_id_number_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def outbound_flow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the outbound flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-queue-outboundcallerconfig.html#cfn-connect-queue-outboundcallerconfig-outboundflowarn
            '''
            result = self._values.get("outbound_flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutboundCallerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQueuePropsMixin.OutboundEmailConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"outbound_email_address_id": "outboundEmailAddressId"},
    )
    class OutboundEmailConfigProperty:
        def __init__(
            self,
            *,
            outbound_email_address_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The outbound email address ID.

            :param outbound_email_address_id: The identifier of the email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-queue-outboundemailconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                outbound_email_config_property = connect_mixins.CfnQueuePropsMixin.OutboundEmailConfigProperty(
                    outbound_email_address_id="outboundEmailAddressId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c60dfc236da5b03bd69d7949f5be5303791262a120076a0ce5fa611a5b537733)
                check_type(argname="argument outbound_email_address_id", value=outbound_email_address_id, expected_type=type_hints["outbound_email_address_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if outbound_email_address_id is not None:
                self._values["outbound_email_address_id"] = outbound_email_address_id

        @builtins.property
        def outbound_email_address_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-queue-outboundemailconfig.html#cfn-connect-queue-outboundemailconfig-outboundemailaddressid
            '''
            result = self._values.get("outbound_email_address_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutboundEmailConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQuickConnectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "quick_connect_config": "quickConnectConfig",
        "tags": "tags",
    },
)
class CfnQuickConnectMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        quick_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickConnectPropsMixin.QuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnQuickConnectPropsMixin.

        :param description: The description of the quick connect.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the quick connect.
        :param quick_connect_config: Contains information about the quick connect.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_quick_connect_mixin_props = connect_mixins.CfnQuickConnectMixinProps(
                description="description",
                instance_arn="instanceArn",
                name="name",
                quick_connect_config=connect_mixins.CfnQuickConnectPropsMixin.QuickConnectConfigProperty(
                    phone_config=connect_mixins.CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty(
                        phone_number="phoneNumber"
                    ),
                    queue_config=connect_mixins.CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        queue_arn="queueArn"
                    ),
                    quick_connect_type="quickConnectType",
                    user_config=connect_mixins.CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        user_arn="userArn"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e6358f65464ec035e10d81ad457b17a1b5469b32917915fb6441eb14dcfa65)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument quick_connect_config", value=quick_connect_config, expected_type=type_hints["quick_connect_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if quick_connect_config is not None:
            self._values["quick_connect_config"] = quick_connect_config
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the quick connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the quick connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quick_connect_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.QuickConnectConfigProperty"]]:
        '''Contains information about the quick connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-quickconnectconfig
        '''
        result = self._values.get("quick_connect_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.QuickConnectConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html#cfn-connect-quickconnect-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnQuickConnectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnQuickConnectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQuickConnectPropsMixin",
):
    '''Specifies a quick connect for an Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-quickconnect.html
    :cloudformationResource: AWS::Connect::QuickConnect
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_quick_connect_props_mixin = connect_mixins.CfnQuickConnectPropsMixin(connect_mixins.CfnQuickConnectMixinProps(
            description="description",
            instance_arn="instanceArn",
            name="name",
            quick_connect_config=connect_mixins.CfnQuickConnectPropsMixin.QuickConnectConfigProperty(
                phone_config=connect_mixins.CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                ),
                queue_config=connect_mixins.CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                ),
                quick_connect_type="quickConnectType",
                user_config=connect_mixins.CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
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
        props: typing.Union[CfnQuickConnectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::QuickConnect``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa26570c7730135267b75206428c37c384cc96240e79fffe84267bb57ec94027)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1079c3745993e8134d80dfb0dca662c5973630c46ba739184c498ac018af5f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31762183ad741337b0c06d64bf5c62c17c284e63871078a0274191331dab743)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnQuickConnectMixinProps:
        return typing.cast(CfnQuickConnectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"phone_number": "phoneNumber"},
    )
    class PhoneNumberQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a phone number for a quick connect.

            :param phone_number: The phone number in E.164 format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-phonenumberquickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                phone_number_quick_connect_config_property = connect_mixins.CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty(
                    phone_number="phoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__191f6b3e5b6e04ee28533b8cf9547fa9160344b482901b9e26aff925ccdd23b3)
                check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if phone_number is not None:
                self._values["phone_number"] = phone_number

        @builtins.property
        def phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number in E.164 format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-phonenumberquickconnectconfig.html#cfn-connect-quickconnect-phonenumberquickconnectconfig-phonenumber
            '''
            result = self._values.get("phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PhoneNumberQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_flow_arn": "contactFlowArn", "queue_arn": "queueArn"},
    )
    class QueueQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: typing.Optional[builtins.str] = None,
            queue_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a queue for a quick connect.

            The flow must be of type Transfer to Queue.

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param queue_arn: The Amazon Resource Name (ARN) of the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                queue_quick_connect_config_property = connect_mixins.CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    queue_arn="queueArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__16c80250e7ce579fcded6a27e608e519a0820c2f51996660b6268c21337718c8)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_flow_arn is not None:
                self._values["contact_flow_arn"] = contact_flow_arn
            if queue_arn is not None:
                self._values["queue_arn"] = queue_arn

        @builtins.property
        def contact_flow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html#cfn-connect-quickconnect-queuequickconnectconfig-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def queue_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-queuequickconnectconfig.html#cfn-connect-quickconnect-queuequickconnectconfig-queuearn
            '''
            result = self._values.get("queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QueueQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQuickConnectPropsMixin.QuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "phone_config": "phoneConfig",
            "queue_config": "queueConfig",
            "quick_connect_type": "quickConnectType",
            "user_config": "userConfig",
        },
    )
    class QuickConnectConfigProperty:
        def __init__(
            self,
            *,
            phone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            queue_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            quick_connect_type: typing.Optional[builtins.str] = None,
            user_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains configuration settings for a quick connect.

            :param phone_config: The phone configuration. This is required only if QuickConnectType is PHONE_NUMBER.
            :param queue_config: The queue configuration. This is required only if QuickConnectType is QUEUE.
            :param quick_connect_type: The type of quick connect. In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).
            :param user_config: The user configuration. This is required only if QuickConnectType is USER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                quick_connect_config_property = connect_mixins.CfnQuickConnectPropsMixin.QuickConnectConfigProperty(
                    phone_config=connect_mixins.CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty(
                        phone_number="phoneNumber"
                    ),
                    queue_config=connect_mixins.CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        queue_arn="queueArn"
                    ),
                    quick_connect_type="quickConnectType",
                    user_config=connect_mixins.CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty(
                        contact_flow_arn="contactFlowArn",
                        user_arn="userArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3484d15311805a5c3571ca053fc3eb5dcc4a057a4e3f616915beb10d3119c5b)
                check_type(argname="argument phone_config", value=phone_config, expected_type=type_hints["phone_config"])
                check_type(argname="argument queue_config", value=queue_config, expected_type=type_hints["queue_config"])
                check_type(argname="argument quick_connect_type", value=quick_connect_type, expected_type=type_hints["quick_connect_type"])
                check_type(argname="argument user_config", value=user_config, expected_type=type_hints["user_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if phone_config is not None:
                self._values["phone_config"] = phone_config
            if queue_config is not None:
                self._values["queue_config"] = queue_config
            if quick_connect_type is not None:
                self._values["quick_connect_type"] = quick_connect_type
            if user_config is not None:
                self._values["user_config"] = user_config

        @builtins.property
        def phone_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty"]]:
            '''The phone configuration.

            This is required only if QuickConnectType is PHONE_NUMBER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-phoneconfig
            '''
            result = self._values.get("phone_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty"]], result)

        @builtins.property
        def queue_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty"]]:
            '''The queue configuration.

            This is required only if QuickConnectType is QUEUE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-queueconfig
            '''
            result = self._values.get("queue_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty"]], result)

        @builtins.property
        def quick_connect_type(self) -> typing.Optional[builtins.str]:
            '''The type of quick connect.

            In the Amazon Connect console, when you create a quick connect, you are prompted to assign one of the following types: Agent (USER), External (PHONE_NUMBER), or Queue (QUEUE).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-quickconnecttype
            '''
            result = self._values.get("quick_connect_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty"]]:
            '''The user configuration.

            This is required only if QuickConnectType is USER.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-quickconnectconfig.html#cfn-connect-quickconnect-quickconnectconfig-userconfig
            '''
            result = self._values.get("user_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"contact_flow_arn": "contactFlowArn", "user_arn": "userArn"},
    )
    class UserQuickConnectConfigProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: typing.Optional[builtins.str] = None,
            user_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the quick connect configuration settings for a user.

            The contact flow must be of type Transfer to Agent.

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param user_arn: The Amazon Resource Name (ARN) of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                user_quick_connect_config_property = connect_mixins.CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty(
                    contact_flow_arn="contactFlowArn",
                    user_arn="userArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b0f26beb30eb410d21be62ce83243ec0c0869344d2bdfec1544d8037a24c9126)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_flow_arn is not None:
                self._values["contact_flow_arn"] = contact_flow_arn
            if user_arn is not None:
                self._values["user_arn"] = user_arn

        @builtins.property
        def contact_flow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html#cfn-connect-quickconnect-userquickconnectconfig-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-quickconnect-userquickconnectconfig.html#cfn-connect-quickconnect-userquickconnectconfig-userarn
            '''
            result = self._values.get("user_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserQuickConnectConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "agent_availability_timer": "agentAvailabilityTimer",
        "default_outbound_queue_arn": "defaultOutboundQueueArn",
        "description": "description",
        "instance_arn": "instanceArn",
        "manual_assignment_queue_configs": "manualAssignmentQueueConfigs",
        "media_concurrencies": "mediaConcurrencies",
        "name": "name",
        "queue_configs": "queueConfigs",
        "tags": "tags",
    },
)
class CfnRoutingProfileMixinProps:
    def __init__(
        self,
        *,
        agent_availability_timer: typing.Optional[builtins.str] = None,
        default_outbound_queue_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        manual_assignment_queue_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        media_concurrencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutingProfilePropsMixin.MediaConcurrencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        queue_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRoutingProfilePropsMixin.

        :param agent_availability_timer: Whether agents with this routing profile will have their routing order calculated based on *time since their last inbound contact* or *longest idle time* .
        :param default_outbound_queue_arn: The Amazon Resource Name (ARN) of the default outbound queue for the routing profile.
        :param description: The description of the routing profile.
        :param instance_arn: The identifier of the Amazon Connect instance.
        :param manual_assignment_queue_configs: Contains information about the queue and channel for manual assignment behaviour can be enabled.
        :param media_concurrencies: The channels agents can handle in the Contact Control Panel (CCP) for this routing profile.
        :param name: The name of the routing profile.
        :param queue_configs: The inbound queues associated with the routing profile. If no queue is added, the agent can make only outbound calls.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_routing_profile_mixin_props = connect_mixins.CfnRoutingProfileMixinProps(
                agent_availability_timer="agentAvailabilityTimer",
                default_outbound_queue_arn="defaultOutboundQueueArn",
                description="description",
                instance_arn="instanceArn",
                manual_assignment_queue_configs=[connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty(
                    queue_reference=connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                        channel="channel",
                        queue_arn="queueArn"
                    )
                )],
                media_concurrencies=[connect_mixins.CfnRoutingProfilePropsMixin.MediaConcurrencyProperty(
                    channel="channel",
                    concurrency=123,
                    cross_channel_behavior=connect_mixins.CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty(
                        behavior_type="behaviorType"
                    )
                )],
                name="name",
                queue_configs=[connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty(
                    delay=123,
                    priority=123,
                    queue_reference=connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                        channel="channel",
                        queue_arn="queueArn"
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52d8fc6715ebef6888e1788df00bd48b9de2d35e6e5b4e25d5c266e47e634286)
            check_type(argname="argument agent_availability_timer", value=agent_availability_timer, expected_type=type_hints["agent_availability_timer"])
            check_type(argname="argument default_outbound_queue_arn", value=default_outbound_queue_arn, expected_type=type_hints["default_outbound_queue_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument manual_assignment_queue_configs", value=manual_assignment_queue_configs, expected_type=type_hints["manual_assignment_queue_configs"])
            check_type(argname="argument media_concurrencies", value=media_concurrencies, expected_type=type_hints["media_concurrencies"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument queue_configs", value=queue_configs, expected_type=type_hints["queue_configs"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if agent_availability_timer is not None:
            self._values["agent_availability_timer"] = agent_availability_timer
        if default_outbound_queue_arn is not None:
            self._values["default_outbound_queue_arn"] = default_outbound_queue_arn
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if manual_assignment_queue_configs is not None:
            self._values["manual_assignment_queue_configs"] = manual_assignment_queue_configs
        if media_concurrencies is not None:
            self._values["media_concurrencies"] = media_concurrencies
        if name is not None:
            self._values["name"] = name
        if queue_configs is not None:
            self._values["queue_configs"] = queue_configs
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def agent_availability_timer(self) -> typing.Optional[builtins.str]:
        '''Whether agents with this routing profile will have their routing order calculated based on *time since their last inbound contact* or *longest idle time* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-agentavailabilitytimer
        '''
        result = self._values.get("agent_availability_timer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_outbound_queue_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the default outbound queue for the routing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-defaultoutboundqueuearn
        '''
        result = self._values.get("default_outbound_queue_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the routing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def manual_assignment_queue_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty"]]]]:
        '''Contains information about the queue and channel for manual assignment behaviour can be enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-manualassignmentqueueconfigs
        '''
        result = self._values.get("manual_assignment_queue_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty"]]]], result)

    @builtins.property
    def media_concurrencies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.MediaConcurrencyProperty"]]]]:
        '''The channels agents can handle in the Contact Control Panel (CCP) for this routing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-mediaconcurrencies
        '''
        result = self._values.get("media_concurrencies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.MediaConcurrencyProperty"]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the routing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def queue_configs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty"]]]]:
        '''The inbound queues associated with the routing profile.

        If no queue is added, the agent can make only outbound calls.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-queueconfigs
        '''
        result = self._values.get("queue_configs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html#cfn-connect-routingprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoutingProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRoutingProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfilePropsMixin",
):
    '''Creates a new routing profile.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-routingprofile.html
    :cloudformationResource: AWS::Connect::RoutingProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_routing_profile_props_mixin = connect_mixins.CfnRoutingProfilePropsMixin(connect_mixins.CfnRoutingProfileMixinProps(
            agent_availability_timer="agentAvailabilityTimer",
            default_outbound_queue_arn="defaultOutboundQueueArn",
            description="description",
            instance_arn="instanceArn",
            manual_assignment_queue_configs=[connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty(
                queue_reference=connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                    channel="channel",
                    queue_arn="queueArn"
                )
            )],
            media_concurrencies=[connect_mixins.CfnRoutingProfilePropsMixin.MediaConcurrencyProperty(
                channel="channel",
                concurrency=123,
                cross_channel_behavior=connect_mixins.CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty(
                    behavior_type="behaviorType"
                )
            )],
            name="name",
            queue_configs=[connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty(
                delay=123,
                priority=123,
                queue_reference=connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                    channel="channel",
                    queue_arn="queueArn"
                )
            )],
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
        props: typing.Union[CfnRoutingProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::RoutingProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a3cca3d6dc4feeb2de2b6df1e78847ebee6f591bf0dec7e143ce91de2cc6d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd063ef9cf3223322923db5eb378e731ea7c7e2f13a7e9f40e00bcdb30dcc0ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1f22ded1cb974e1f8ecd129ad632306e51af40622e69343eaabf3019b90474)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRoutingProfileMixinProps:
        return typing.cast(CfnRoutingProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty",
        jsii_struct_bases=[],
        name_mapping={"behavior_type": "behaviorType"},
    )
    class CrossChannelBehaviorProperty:
        def __init__(
            self,
            *,
            behavior_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the cross-channel routing behavior that allows an agent working on a contact in one channel to be offered a contact from a different channel.

            :param behavior_type: Specifies the other channels that can be routed to an agent handling their current channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-crosschannelbehavior.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                cross_channel_behavior_property = connect_mixins.CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty(
                    behavior_type="behaviorType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1767ecb7fb7c7a037524035bf5990d0d9f520fa77a7d79ffc14cb6f65d7e6ea)
                check_type(argname="argument behavior_type", value=behavior_type, expected_type=type_hints["behavior_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior_type is not None:
                self._values["behavior_type"] = behavior_type

        @builtins.property
        def behavior_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the other channels that can be routed to an agent handling their current channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-crosschannelbehavior.html#cfn-connect-routingprofile-crosschannelbehavior-behaviortype
            '''
            result = self._values.get("behavior_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrossChannelBehaviorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfilePropsMixin.MediaConcurrencyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "channel": "channel",
            "concurrency": "concurrency",
            "cross_channel_behavior": "crossChannelBehavior",
        },
    )
    class MediaConcurrencyProperty:
        def __init__(
            self,
            *,
            channel: typing.Optional[builtins.str] = None,
            concurrency: typing.Optional[jsii.Number] = None,
            cross_channel_behavior: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about which channels are supported, and how many contacts an agent can have on a channel simultaneously.

            :param channel: The channels that agents can handle in the Contact Control Panel (CCP).
            :param concurrency: The number of contacts an agent can have on a channel simultaneously. Valid Range for ``VOICE`` : Minimum value of 1. Maximum value of 1. Valid Range for ``CHAT`` : Minimum value of 1. Maximum value of 10. Valid Range for ``TASK`` : Minimum value of 1. Maximum value of 10.
            :param cross_channel_behavior: Defines the cross-channel routing behavior for each channel that is enabled for this Routing Profile. For example, this allows you to offer an agent a different contact from another channel when they are currently working with a contact from a Voice channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-mediaconcurrency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                media_concurrency_property = connect_mixins.CfnRoutingProfilePropsMixin.MediaConcurrencyProperty(
                    channel="channel",
                    concurrency=123,
                    cross_channel_behavior=connect_mixins.CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty(
                        behavior_type="behaviorType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd115c31c6efd9516419cac7f6c0ea9a88650756ab71b029e75e06af156ca49e)
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
                check_type(argname="argument cross_channel_behavior", value=cross_channel_behavior, expected_type=type_hints["cross_channel_behavior"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel is not None:
                self._values["channel"] = channel
            if concurrency is not None:
                self._values["concurrency"] = concurrency
            if cross_channel_behavior is not None:
                self._values["cross_channel_behavior"] = cross_channel_behavior

        @builtins.property
        def channel(self) -> typing.Optional[builtins.str]:
            '''The channels that agents can handle in the Contact Control Panel (CCP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-mediaconcurrency.html#cfn-connect-routingprofile-mediaconcurrency-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def concurrency(self) -> typing.Optional[jsii.Number]:
            '''The number of contacts an agent can have on a channel simultaneously.

            Valid Range for ``VOICE`` : Minimum value of 1. Maximum value of 1.

            Valid Range for ``CHAT`` : Minimum value of 1. Maximum value of 10.

            Valid Range for ``TASK`` : Minimum value of 1. Maximum value of 10.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-mediaconcurrency.html#cfn-connect-routingprofile-mediaconcurrency-concurrency
            '''
            result = self._values.get("concurrency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def cross_channel_behavior(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty"]]:
            '''Defines the cross-channel routing behavior for each channel that is enabled for this Routing Profile.

            For example, this allows you to offer an agent a different contact from another channel when they are currently working with a contact from a Voice channel.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-mediaconcurrency.html#cfn-connect-routingprofile-mediaconcurrency-crosschannelbehavior
            '''
            result = self._values.get("cross_channel_behavior")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MediaConcurrencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"queue_reference": "queueReference"},
    )
    class RoutingProfileManualAssignmentQueueConfigProperty:
        def __init__(
            self,
            *,
            queue_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the queue and channel for manual assignment behaviour can be enabled.

            :param queue_reference: Contains information about a queue resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilemanualassignmentqueueconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                routing_profile_manual_assignment_queue_config_property = connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty(
                    queue_reference=connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                        channel="channel",
                        queue_arn="queueArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a26af61ae429d1eaa98a76439f321eca5831c7f100b47d023eb1f8bbbb8a960a)
                check_type(argname="argument queue_reference", value=queue_reference, expected_type=type_hints["queue_reference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if queue_reference is not None:
                self._values["queue_reference"] = queue_reference

        @builtins.property
        def queue_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty"]]:
            '''Contains information about a queue resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilemanualassignmentqueueconfig.html#cfn-connect-routingprofile-routingprofilemanualassignmentqueueconfig-queuereference
            '''
            result = self._values.get("queue_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingProfileManualAssignmentQueueConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delay": "delay",
            "priority": "priority",
            "queue_reference": "queueReference",
        },
    )
    class RoutingProfileQueueConfigProperty:
        def __init__(
            self,
            *,
            delay: typing.Optional[jsii.Number] = None,
            priority: typing.Optional[jsii.Number] = None,
            queue_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about the queue and channel for which priority and delay can be set.

            :param delay: The delay, in seconds, a contact should be in the queue before they are routed to an available agent. For more information, see `Queues: priority and delay <https://docs.aws.amazon.com/connect/latest/adminguide/concepts-routing-profiles-priority.html>`_ in the *Amazon Connect Administrator Guide* .
            :param priority: The order in which contacts are to be handled for the queue. For more information, see `Queues: priority and delay <https://docs.aws.amazon.com/connect/latest/adminguide/concepts-routing-profiles-priority.html>`_ .
            :param queue_reference: Contains information about a queue resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeueconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                routing_profile_queue_config_property = connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty(
                    delay=123,
                    priority=123,
                    queue_reference=connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                        channel="channel",
                        queue_arn="queueArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__460e3ffd2f931c382dcbb1dc7336c3581d480ad7b5b30fdff6be76113c352daf)
                check_type(argname="argument delay", value=delay, expected_type=type_hints["delay"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument queue_reference", value=queue_reference, expected_type=type_hints["queue_reference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delay is not None:
                self._values["delay"] = delay
            if priority is not None:
                self._values["priority"] = priority
            if queue_reference is not None:
                self._values["queue_reference"] = queue_reference

        @builtins.property
        def delay(self) -> typing.Optional[jsii.Number]:
            '''The delay, in seconds, a contact should be in the queue before they are routed to an available agent.

            For more information, see `Queues: priority and delay <https://docs.aws.amazon.com/connect/latest/adminguide/concepts-routing-profiles-priority.html>`_ in the *Amazon Connect Administrator Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeueconfig.html#cfn-connect-routingprofile-routingprofilequeueconfig-delay
            '''
            result = self._values.get("delay")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''The order in which contacts are to be handled for the queue.

            For more information, see `Queues: priority and delay <https://docs.aws.amazon.com/connect/latest/adminguide/concepts-routing-profiles-priority.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeueconfig.html#cfn-connect-routingprofile-routingprofilequeueconfig-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def queue_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty"]]:
            '''Contains information about a queue resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeueconfig.html#cfn-connect-routingprofile-routingprofilequeueconfig-queuereference
            '''
            result = self._values.get("queue_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingProfileQueueConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"channel": "channel", "queue_arn": "queueArn"},
    )
    class RoutingProfileQueueReferenceProperty:
        def __init__(
            self,
            *,
            channel: typing.Optional[builtins.str] = None,
            queue_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the channel and queue identifier for a routing profile.

            :param channel: The channels agents can handle in the Contact Control Panel (CCP) for this routing profile.
            :param queue_arn: The Amazon Resource Name (ARN) of the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeuereference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                routing_profile_queue_reference_property = connect_mixins.CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty(
                    channel="channel",
                    queue_arn="queueArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__73235db8dea6526e26ebe89a54e5f6943f990d50ed847f6f4779687cacd50d1f)
                check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
                check_type(argname="argument queue_arn", value=queue_arn, expected_type=type_hints["queue_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if channel is not None:
                self._values["channel"] = channel
            if queue_arn is not None:
                self._values["queue_arn"] = queue_arn

        @builtins.property
        def channel(self) -> typing.Optional[builtins.str]:
            '''The channels agents can handle in the Contact Control Panel (CCP) for this routing profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeuereference.html#cfn-connect-routingprofile-routingprofilequeuereference-channel
            '''
            result = self._values.get("channel")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def queue_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the queue.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-routingprofile-routingprofilequeuereference.html#cfn-connect-routingprofile-routingprofilequeuereference-queuearn
            '''
            result = self._values.get("queue_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoutingProfileQueueReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRuleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "function": "function",
        "instance_arn": "instanceArn",
        "name": "name",
        "publish_status": "publishStatus",
        "tags": "tags",
        "trigger_event_source": "triggerEventSource",
    },
)
class CfnRuleMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.ActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        function: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        publish_status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        trigger_event_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.RuleTriggerEventSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRulePropsMixin.

        :param actions: A list of actions to be run when the rule is triggered.
        :param function: The conditions of the rule.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the rule.
        :param publish_status: The publish status of the rule. *Allowed values* : ``DRAFT`` | ``PUBLISHED``
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        :param trigger_event_source: The event source to trigger the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            # assign_contact_category_actions: Any
            # empty_value: Any
            # end_associated_tasks_actions: Any
            
            cfn_rule_mixin_props = connect_mixins.CfnRuleMixinProps(
                actions=connect_mixins.CfnRulePropsMixin.ActionsProperty(
                    assign_contact_category_actions=[assign_contact_category_actions],
                    create_case_actions=[connect_mixins.CfnRulePropsMixin.CreateCaseActionProperty(
                        fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                            id="id",
                            value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                                boolean_value=False,
                                double_value=123,
                                empty_value=empty_value,
                                string_value="stringValue"
                            )
                        )],
                        template_id="templateId"
                    )],
                    end_associated_tasks_actions=[end_associated_tasks_actions],
                    event_bridge_actions=[connect_mixins.CfnRulePropsMixin.EventBridgeActionProperty(
                        name="name"
                    )],
                    send_notification_actions=[connect_mixins.CfnRulePropsMixin.SendNotificationActionProperty(
                        content="content",
                        content_type="contentType",
                        delivery_method="deliveryMethod",
                        recipient=connect_mixins.CfnRulePropsMixin.NotificationRecipientTypeProperty(
                            user_arns=["userArns"],
                            user_tags={
                                "user_tags_key": "userTags"
                            }
                        ),
                        subject="subject"
                    )],
                    submit_auto_evaluation_actions=[connect_mixins.CfnRulePropsMixin.SubmitAutoEvaluationActionProperty(
                        evaluation_form_arn="evaluationFormArn"
                    )],
                    task_actions=[connect_mixins.CfnRulePropsMixin.TaskActionProperty(
                        contact_flow_arn="contactFlowArn",
                        description="description",
                        name="name",
                        references={
                            "references_key": connect_mixins.CfnRulePropsMixin.ReferenceProperty(
                                type="type",
                                value="value"
                            )
                        }
                    )],
                    update_case_actions=[connect_mixins.CfnRulePropsMixin.UpdateCaseActionProperty(
                        fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                            id="id",
                            value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                                boolean_value=False,
                                double_value=123,
                                empty_value=empty_value,
                                string_value="stringValue"
                            )
                        )]
                    )]
                ),
                function="function",
                instance_arn="instanceArn",
                name="name",
                publish_status="publishStatus",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                trigger_event_source=connect_mixins.CfnRulePropsMixin.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
                    integration_association_arn="integrationAssociationArn"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45290cb986518bf26ef612edf30f89d238a47e8b38d0ecc3f53461d7e0b6bf01)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument function", value=function, expected_type=type_hints["function"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument publish_status", value=publish_status, expected_type=type_hints["publish_status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument trigger_event_source", value=trigger_event_source, expected_type=type_hints["trigger_event_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if function is not None:
            self._values["function"] = function
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if publish_status is not None:
            self._values["publish_status"] = publish_status
        if tags is not None:
            self._values["tags"] = tags
        if trigger_event_source is not None:
            self._values["trigger_event_source"] = trigger_event_source

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ActionsProperty"]]:
        '''A list of actions to be run when the rule is triggered.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ActionsProperty"]], result)

    @builtins.property
    def function(self) -> typing.Optional[builtins.str]:
        '''The conditions of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-function
        '''
        result = self._values.get("function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_status(self) -> typing.Optional[builtins.str]:
        '''The publish status of the rule.

        *Allowed values* : ``DRAFT`` | ``PUBLISHED``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-publishstatus
        '''
        result = self._values.get("publish_status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def trigger_event_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.RuleTriggerEventSourceProperty"]]:
        '''The event source to trigger the rule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html#cfn-connect-rule-triggereventsource
        '''
        result = self._values.get("trigger_event_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.RuleTriggerEventSourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin",
):
    '''Creates a rule for the specified Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-rule.html
    :cloudformationResource: AWS::Connect::Rule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        # assign_contact_category_actions: Any
        # empty_value: Any
        # end_associated_tasks_actions: Any
        
        cfn_rule_props_mixin = connect_mixins.CfnRulePropsMixin(connect_mixins.CfnRuleMixinProps(
            actions=connect_mixins.CfnRulePropsMixin.ActionsProperty(
                assign_contact_category_actions=[assign_contact_category_actions],
                create_case_actions=[connect_mixins.CfnRulePropsMixin.CreateCaseActionProperty(
                    fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                        id="id",
                        value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                            boolean_value=False,
                            double_value=123,
                            empty_value=empty_value,
                            string_value="stringValue"
                        )
                    )],
                    template_id="templateId"
                )],
                end_associated_tasks_actions=[end_associated_tasks_actions],
                event_bridge_actions=[connect_mixins.CfnRulePropsMixin.EventBridgeActionProperty(
                    name="name"
                )],
                send_notification_actions=[connect_mixins.CfnRulePropsMixin.SendNotificationActionProperty(
                    content="content",
                    content_type="contentType",
                    delivery_method="deliveryMethod",
                    recipient=connect_mixins.CfnRulePropsMixin.NotificationRecipientTypeProperty(
                        user_arns=["userArns"],
                        user_tags={
                            "user_tags_key": "userTags"
                        }
                    ),
                    subject="subject"
                )],
                submit_auto_evaluation_actions=[connect_mixins.CfnRulePropsMixin.SubmitAutoEvaluationActionProperty(
                    evaluation_form_arn="evaluationFormArn"
                )],
                task_actions=[connect_mixins.CfnRulePropsMixin.TaskActionProperty(
                    contact_flow_arn="contactFlowArn",
                    description="description",
                    name="name",
                    references={
                        "references_key": connect_mixins.CfnRulePropsMixin.ReferenceProperty(
                            type="type",
                            value="value"
                        )
                    }
                )],
                update_case_actions=[connect_mixins.CfnRulePropsMixin.UpdateCaseActionProperty(
                    fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                        id="id",
                        value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                            boolean_value=False,
                            double_value=123,
                            empty_value=empty_value,
                            string_value="stringValue"
                        )
                    )]
                )]
            ),
            function="function",
            instance_arn="instanceArn",
            name="name",
            publish_status="publishStatus",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            trigger_event_source=connect_mixins.CfnRulePropsMixin.RuleTriggerEventSourceProperty(
                event_source_name="eventSourceName",
                integration_association_arn="integrationAssociationArn"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::Rule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c55e92831284bf7ec63e128e53f1430c9623bbb2bb69cc617409e295115bb7aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__845b3a39a7a9d75fbbaa0b29aadffb0a0b51838dd5e5e943b61caf7ac9a339ef)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b5f6b06bce6ecbf1d59d8f93885db0c9735633e9b27ee1b842ab55fa4561042)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRuleMixinProps:
        return typing.cast(CfnRuleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.ActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assign_contact_category_actions": "assignContactCategoryActions",
            "create_case_actions": "createCaseActions",
            "end_associated_tasks_actions": "endAssociatedTasksActions",
            "event_bridge_actions": "eventBridgeActions",
            "send_notification_actions": "sendNotificationActions",
            "submit_auto_evaluation_actions": "submitAutoEvaluationActions",
            "task_actions": "taskActions",
            "update_case_actions": "updateCaseActions",
        },
    )
    class ActionsProperty:
        def __init__(
            self,
            *,
            assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
            create_case_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.CreateCaseActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            end_associated_tasks_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
            event_bridge_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.EventBridgeActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            send_notification_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.SendNotificationActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            submit_auto_evaluation_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.SubmitAutoEvaluationActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            task_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.TaskActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            update_case_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.UpdateCaseActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''A list of actions to be run when the rule is triggered.

            :param assign_contact_category_actions: Information about the contact category action. The syntax can be empty, for example, ``{}`` .
            :param create_case_actions: This action will create a case when a rule is triggered.
            :param end_associated_tasks_actions: This action will end associated tasks when a rule is triggered.
            :param event_bridge_actions: Information about the EventBridge action.
            :param send_notification_actions: Information about the send notification action.
            :param submit_auto_evaluation_actions: This action will submit an auto contact evaluation when a rule is triggered.
            :param task_actions: Information about the task action. This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``
            :param update_case_actions: This action will update a case when a rule is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # assign_contact_category_actions: Any
                # empty_value: Any
                # end_associated_tasks_actions: Any
                
                actions_property = connect_mixins.CfnRulePropsMixin.ActionsProperty(
                    assign_contact_category_actions=[assign_contact_category_actions],
                    create_case_actions=[connect_mixins.CfnRulePropsMixin.CreateCaseActionProperty(
                        fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                            id="id",
                            value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                                boolean_value=False,
                                double_value=123,
                                empty_value=empty_value,
                                string_value="stringValue"
                            )
                        )],
                        template_id="templateId"
                    )],
                    end_associated_tasks_actions=[end_associated_tasks_actions],
                    event_bridge_actions=[connect_mixins.CfnRulePropsMixin.EventBridgeActionProperty(
                        name="name"
                    )],
                    send_notification_actions=[connect_mixins.CfnRulePropsMixin.SendNotificationActionProperty(
                        content="content",
                        content_type="contentType",
                        delivery_method="deliveryMethod",
                        recipient=connect_mixins.CfnRulePropsMixin.NotificationRecipientTypeProperty(
                            user_arns=["userArns"],
                            user_tags={
                                "user_tags_key": "userTags"
                            }
                        ),
                        subject="subject"
                    )],
                    submit_auto_evaluation_actions=[connect_mixins.CfnRulePropsMixin.SubmitAutoEvaluationActionProperty(
                        evaluation_form_arn="evaluationFormArn"
                    )],
                    task_actions=[connect_mixins.CfnRulePropsMixin.TaskActionProperty(
                        contact_flow_arn="contactFlowArn",
                        description="description",
                        name="name",
                        references={
                            "references_key": connect_mixins.CfnRulePropsMixin.ReferenceProperty(
                                type="type",
                                value="value"
                            )
                        }
                    )],
                    update_case_actions=[connect_mixins.CfnRulePropsMixin.UpdateCaseActionProperty(
                        fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                            id="id",
                            value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                                boolean_value=False,
                                double_value=123,
                                empty_value=empty_value,
                                string_value="stringValue"
                            )
                        )]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7933b63d1220183bcaf569fc44f15da19cbce19ff7c14a114b275c9e298ac18)
                check_type(argname="argument assign_contact_category_actions", value=assign_contact_category_actions, expected_type=type_hints["assign_contact_category_actions"])
                check_type(argname="argument create_case_actions", value=create_case_actions, expected_type=type_hints["create_case_actions"])
                check_type(argname="argument end_associated_tasks_actions", value=end_associated_tasks_actions, expected_type=type_hints["end_associated_tasks_actions"])
                check_type(argname="argument event_bridge_actions", value=event_bridge_actions, expected_type=type_hints["event_bridge_actions"])
                check_type(argname="argument send_notification_actions", value=send_notification_actions, expected_type=type_hints["send_notification_actions"])
                check_type(argname="argument submit_auto_evaluation_actions", value=submit_auto_evaluation_actions, expected_type=type_hints["submit_auto_evaluation_actions"])
                check_type(argname="argument task_actions", value=task_actions, expected_type=type_hints["task_actions"])
                check_type(argname="argument update_case_actions", value=update_case_actions, expected_type=type_hints["update_case_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_contact_category_actions is not None:
                self._values["assign_contact_category_actions"] = assign_contact_category_actions
            if create_case_actions is not None:
                self._values["create_case_actions"] = create_case_actions
            if end_associated_tasks_actions is not None:
                self._values["end_associated_tasks_actions"] = end_associated_tasks_actions
            if event_bridge_actions is not None:
                self._values["event_bridge_actions"] = event_bridge_actions
            if send_notification_actions is not None:
                self._values["send_notification_actions"] = send_notification_actions
            if submit_auto_evaluation_actions is not None:
                self._values["submit_auto_evaluation_actions"] = submit_auto_evaluation_actions
            if task_actions is not None:
                self._values["task_actions"] = task_actions
            if update_case_actions is not None:
                self._values["update_case_actions"] = update_case_actions

        @builtins.property
        def assign_contact_category_actions(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
            '''Information about the contact category action.

            The syntax can be empty, for example, ``{}`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-assigncontactcategoryactions
            '''
            result = self._values.get("assign_contact_category_actions")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def create_case_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.CreateCaseActionProperty"]]]]:
            '''This action will create a case when a rule is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-createcaseactions
            '''
            result = self._values.get("create_case_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.CreateCaseActionProperty"]]]], result)

        @builtins.property
        def end_associated_tasks_actions(
            self,
        ) -> typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]]:
            '''This action will end associated tasks when a rule is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-endassociatedtasksactions
            '''
            result = self._values.get("end_associated_tasks_actions")
            return typing.cast(typing.Optional[typing.Union[typing.List[typing.Any], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def event_bridge_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.EventBridgeActionProperty"]]]]:
            '''Information about the EventBridge action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-eventbridgeactions
            '''
            result = self._values.get("event_bridge_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.EventBridgeActionProperty"]]]], result)

        @builtins.property
        def send_notification_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.SendNotificationActionProperty"]]]]:
            '''Information about the send notification action.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-sendnotificationactions
            '''
            result = self._values.get("send_notification_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.SendNotificationActionProperty"]]]], result)

        @builtins.property
        def submit_auto_evaluation_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.SubmitAutoEvaluationActionProperty"]]]]:
            '''This action will submit an auto contact evaluation when a rule is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-submitautoevaluationactions
            '''
            result = self._values.get("submit_auto_evaluation_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.SubmitAutoEvaluationActionProperty"]]]], result)

        @builtins.property
        def task_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.TaskActionProperty"]]]]:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-taskactions
            '''
            result = self._values.get("task_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.TaskActionProperty"]]]], result)

        @builtins.property
        def update_case_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.UpdateCaseActionProperty"]]]]:
            '''This action will update a case when a rule is triggered.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-actions.html#cfn-connect-rule-actions-updatecaseactions
            '''
            result = self._values.get("update_case_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.UpdateCaseActionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.CreateCaseActionProperty",
        jsii_struct_bases=[],
        name_mapping={"fields": "fields", "template_id": "templateId"},
    )
    class CreateCaseActionProperty:
        def __init__(
            self,
            *,
            fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            template_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param fields: An array of case fields.
            :param template_id: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-createcaseaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # empty_value: Any
                
                create_case_action_property = connect_mixins.CfnRulePropsMixin.CreateCaseActionProperty(
                    fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                        id="id",
                        value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                            boolean_value=False,
                            double_value=123,
                            empty_value=empty_value,
                            string_value="stringValue"
                        )
                    )],
                    template_id="templateId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3af10753c689192700f95c6de519951fe3ffc589638b8241bc85ae23c2f0311b)
                check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
                check_type(argname="argument template_id", value=template_id, expected_type=type_hints["template_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fields is not None:
                self._values["fields"] = fields
            if template_id is not None:
                self._values["template_id"] = template_id

        @builtins.property
        def fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FieldProperty"]]]]:
            '''An array of case fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-createcaseaction.html#cfn-connect-rule-createcaseaction-fields
            '''
            result = self._values.get("fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FieldProperty"]]]], result)

        @builtins.property
        def template_id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-createcaseaction.html#cfn-connect-rule-createcaseaction-templateid
            '''
            result = self._values.get("template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CreateCaseActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.EventBridgeActionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class EventBridgeActionProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The EventBridge action definition.

            :param name: The name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-eventbridgeaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                event_bridge_action_property = connect_mixins.CfnRulePropsMixin.EventBridgeActionProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83cee4bc9047627089a42e5b8d718eb215d6e4ff84f3d84e7d1f1a5024932954)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-eventbridgeaction.html#cfn-connect-rule-eventbridgeaction-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventBridgeActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "value": "value"},
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.FieldValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param id: 
            :param value: Object for case field values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # empty_value: Any
                
                field_property = connect_mixins.CfnRulePropsMixin.FieldProperty(
                    id="id",
                    value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                        boolean_value=False,
                        double_value=123,
                        empty_value=empty_value,
                        string_value="stringValue"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aca4f4db6ef266b638244212e51f9c99589cf5f543e928a1d60e11bd8dc1c5ce)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-field.html#cfn-connect-rule-field-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FieldValueProperty"]]:
            '''Object for case field values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-field.html#cfn-connect-rule-field-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FieldValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.FieldValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "boolean_value": "booleanValue",
            "double_value": "doubleValue",
            "empty_value": "emptyValue",
            "string_value": "stringValue",
        },
    )
    class FieldValueProperty:
        def __init__(
            self,
            *,
            boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            double_value: typing.Optional[jsii.Number] = None,
            empty_value: typing.Any = None,
            string_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Object for case field values.

            :param boolean_value: 
            :param double_value: 
            :param empty_value: 
            :param string_value: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-fieldvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # empty_value: Any
                
                field_value_property = connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                    boolean_value=False,
                    double_value=123,
                    empty_value=empty_value,
                    string_value="stringValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__725dc24ab18352a277ba03517438ce0deb2604be8bed69f09c0a2099cd5df66a)
                check_type(argname="argument boolean_value", value=boolean_value, expected_type=type_hints["boolean_value"])
                check_type(argname="argument double_value", value=double_value, expected_type=type_hints["double_value"])
                check_type(argname="argument empty_value", value=empty_value, expected_type=type_hints["empty_value"])
                check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if boolean_value is not None:
                self._values["boolean_value"] = boolean_value
            if double_value is not None:
                self._values["double_value"] = double_value
            if empty_value is not None:
                self._values["empty_value"] = empty_value
            if string_value is not None:
                self._values["string_value"] = string_value

        @builtins.property
        def boolean_value(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-fieldvalue.html#cfn-connect-rule-fieldvalue-booleanvalue
            '''
            result = self._values.get("boolean_value")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def double_value(self) -> typing.Optional[jsii.Number]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-fieldvalue.html#cfn-connect-rule-fieldvalue-doublevalue
            '''
            result = self._values.get("double_value")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def empty_value(self) -> typing.Any:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-fieldvalue.html#cfn-connect-rule-fieldvalue-emptyvalue
            '''
            result = self._values.get("empty_value")
            return typing.cast(typing.Any, result)

        @builtins.property
        def string_value(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-fieldvalue.html#cfn-connect-rule-fieldvalue-stringvalue
            '''
            result = self._values.get("string_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.NotificationRecipientTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"user_arns": "userArns", "user_tags": "userTags"},
    )
    class NotificationRecipientTypeProperty:
        def __init__(
            self,
            *,
            user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            user_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The type of notification recipient.

            :param user_arns: The Amazon Resource Name (ARN) of the user account.
            :param user_tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                notification_recipient_type_property = connect_mixins.CfnRulePropsMixin.NotificationRecipientTypeProperty(
                    user_arns=["userArns"],
                    user_tags={
                        "user_tags_key": "userTags"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__685661a93ed658b0e1cad593aae9b097c1ae9691984bd2d651a619ff40d544cf)
                check_type(argname="argument user_arns", value=user_arns, expected_type=type_hints["user_arns"])
                check_type(argname="argument user_tags", value=user_tags, expected_type=type_hints["user_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if user_arns is not None:
                self._values["user_arns"] = user_arns
            if user_tags is not None:
                self._values["user_tags"] = user_tags

        @builtins.property
        def user_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Name (ARN) of the user account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-userarns
            '''
            result = self._values.get("user_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def user_tags(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''The tags used to organize, track, or control access for this resource.

            For example, { "tags": {"key1":"value1", "key2":"value2"} }. Amazon Connect users with the specified tags will be notified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-notificationrecipienttype.html#cfn-connect-rule-notificationrecipienttype-usertags
            '''
            result = self._values.get("user_tags")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationRecipientTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.ReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ReferenceProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. (Supports variable injection in the ``Value`` field.)

            :param type: The type of the reference. ``DATE`` must be of type Epoch timestamp. *Allowed values* : ``URL`` | ``ATTACHMENT`` | ``NUMBER`` | ``STRING`` | ``DATE`` | ``EMAIL``
            :param value: A valid value for the reference. For example, for a URL reference, a formatted URL that is displayed to an agent in the Contact Control Panel (CCP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                reference_property = connect_mixins.CfnRulePropsMixin.ReferenceProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4bfd9c3e1210a0c032100188a9089e96585c49a29e58f2d2b544e4774e62619)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the reference. ``DATE`` must be of type Epoch timestamp.

            *Allowed values* : ``URL`` | ``ATTACHMENT`` | ``NUMBER`` | ``STRING`` | ``DATE`` | ``EMAIL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html#cfn-connect-rule-reference-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A valid value for the reference.

            For example, for a URL reference, a formatted URL that is displayed to an agent in the Contact Control Panel (CCP).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-reference.html#cfn-connect-rule-reference-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.RuleTriggerEventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "event_source_name": "eventSourceName",
            "integration_association_arn": "integrationAssociationArn",
        },
    )
    class RuleTriggerEventSourceProperty:
        def __init__(
            self,
            *,
            event_source_name: typing.Optional[builtins.str] = None,
            integration_association_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The name of the event source.

            :param event_source_name: The name of the event source.
            :param integration_association_arn: The Amazon Resource Name (ARN) of the integration association. ``IntegrationAssociationArn`` is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                rule_trigger_event_source_property = connect_mixins.CfnRulePropsMixin.RuleTriggerEventSourceProperty(
                    event_source_name="eventSourceName",
                    integration_association_arn="integrationAssociationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f70d491880d95d3f26cd5a022fbeef1266b4c9302f402b08562ec4484fac61f0)
                check_type(argname="argument event_source_name", value=event_source_name, expected_type=type_hints["event_source_name"])
                check_type(argname="argument integration_association_arn", value=integration_association_arn, expected_type=type_hints["integration_association_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if event_source_name is not None:
                self._values["event_source_name"] = event_source_name
            if integration_association_arn is not None:
                self._values["integration_association_arn"] = integration_association_arn

        @builtins.property
        def event_source_name(self) -> typing.Optional[builtins.str]:
            '''The name of the event source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html#cfn-connect-rule-ruletriggereventsource-eventsourcename
            '''
            result = self._values.get("event_source_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def integration_association_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the integration association.

            ``IntegrationAssociationArn`` is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-ruletriggereventsource.html#cfn-connect-rule-ruletriggereventsource-integrationassociationarn
            '''
            result = self._values.get("integration_association_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleTriggerEventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.SendNotificationActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "content": "content",
            "content_type": "contentType",
            "delivery_method": "deliveryMethod",
            "recipient": "recipient",
            "subject": "subject",
        },
    )
    class SendNotificationActionProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[builtins.str] = None,
            content_type: typing.Optional[builtins.str] = None,
            delivery_method: typing.Optional[builtins.str] = None,
            recipient: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.NotificationRecipientTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the send notification action.

            :param content: Notification content. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param content_type: Content type format. *Allowed value* : ``PLAIN_TEXT``
            :param delivery_method: Notification delivery method. *Allowed value* : ``EMAIL``
            :param recipient: Notification recipient.
            :param subject: The subject of the email if the delivery method is ``EMAIL`` . Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                send_notification_action_property = connect_mixins.CfnRulePropsMixin.SendNotificationActionProperty(
                    content="content",
                    content_type="contentType",
                    delivery_method="deliveryMethod",
                    recipient=connect_mixins.CfnRulePropsMixin.NotificationRecipientTypeProperty(
                        user_arns=["userArns"],
                        user_tags={
                            "user_tags_key": "userTags"
                        }
                    ),
                    subject="subject"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8a1391e60b81f17a6cd5dc212b91a93966e57a542965457cb52948d51b7419f)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
                check_type(argname="argument delivery_method", value=delivery_method, expected_type=type_hints["delivery_method"])
                check_type(argname="argument recipient", value=recipient, expected_type=type_hints["recipient"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if content_type is not None:
                self._values["content_type"] = content_type
            if delivery_method is not None:
                self._values["delivery_method"] = delivery_method
            if recipient is not None:
                self._values["recipient"] = recipient
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''Notification content.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def content_type(self) -> typing.Optional[builtins.str]:
            '''Content type format.

            *Allowed value* : ``PLAIN_TEXT``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-contenttype
            '''
            result = self._values.get("content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def delivery_method(self) -> typing.Optional[builtins.str]:
            '''Notification delivery method.

            *Allowed value* : ``EMAIL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-deliverymethod
            '''
            result = self._values.get("delivery_method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recipient(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.NotificationRecipientTypeProperty"]]:
            '''Notification recipient.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-recipient
            '''
            result = self._values.get("recipient")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.NotificationRecipientTypeProperty"]], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The subject of the email if the delivery method is ``EMAIL`` .

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-sendnotificationaction.html#cfn-connect-rule-sendnotificationaction-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SendNotificationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.SubmitAutoEvaluationActionProperty",
        jsii_struct_bases=[],
        name_mapping={"evaluation_form_arn": "evaluationFormArn"},
    )
    class SubmitAutoEvaluationActionProperty:
        def __init__(
            self,
            *,
            evaluation_form_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param evaluation_form_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-submitautoevaluationaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                submit_auto_evaluation_action_property = connect_mixins.CfnRulePropsMixin.SubmitAutoEvaluationActionProperty(
                    evaluation_form_arn="evaluationFormArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bee3e2861ceea772eb80b0ebb32633583a0ae8d5fd662c39edc643b9f8386f01)
                check_type(argname="argument evaluation_form_arn", value=evaluation_form_arn, expected_type=type_hints["evaluation_form_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if evaluation_form_arn is not None:
                self._values["evaluation_form_arn"] = evaluation_form_arn

        @builtins.property
        def evaluation_form_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-submitautoevaluationaction.html#cfn-connect-rule-submitautoevaluationaction-evaluationformarn
            '''
            result = self._values.get("evaluation_form_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubmitAutoEvaluationActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.TaskActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "contact_flow_arn": "contactFlowArn",
            "description": "description",
            "name": "name",
            "references": "references",
        },
    )
    class TaskActionProperty:
        def __init__(
            self,
            *,
            contact_flow_arn: typing.Optional[builtins.str] = None,
            description: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.ReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Information about the task action.

            This field is required if ``TriggerEventSource`` is one of the following values: ``OnZendeskTicketCreate`` | ``OnZendeskTicketStatusUpdate`` | ``OnSalesforceCaseCreate``

            :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param description: The description. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param name: The name. Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .
            :param references: Information about the reference when the ``referenceType`` is ``URL`` . Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                task_action_property = connect_mixins.CfnRulePropsMixin.TaskActionProperty(
                    contact_flow_arn="contactFlowArn",
                    description="description",
                    name="name",
                    references={
                        "references_key": connect_mixins.CfnRulePropsMixin.ReferenceProperty(
                            type="type",
                            value="value"
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4d62de805df4fdff5f5837c8c4e9d9b97e0beaa813df631cbba95e8fb0095991)
                check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument references", value=references, expected_type=type_hints["references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contact_flow_arn is not None:
                self._values["contact_flow_arn"] = contact_flow_arn
            if description is not None:
                self._values["description"] = description
            if name is not None:
                self._values["name"] = name
            if references is not None:
                self._values["references"] = references

        @builtins.property
        def contact_flow_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the flow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-contactflowarn
            '''
            result = self._values.get("contact_flow_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name.

            Supports variable injection. For more information, see `JSONPath reference <https://docs.aws.amazon.com/connect/latest/adminguide/contact-lens-variable-injection.html>`_ in the *Amazon Connect Administrators Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ReferenceProperty"]]]]:
            '''Information about the reference when the ``referenceType`` is ``URL`` .

            Otherwise, null. ``URL`` is the only accepted type. (Supports variable injection in the ``Value`` field.)

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-taskaction.html#cfn-connect-rule-taskaction-references
            '''
            result = self._values.get("references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.ReferenceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaskActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnRulePropsMixin.UpdateCaseActionProperty",
        jsii_struct_bases=[],
        name_mapping={"fields": "fields"},
    )
    class UpdateCaseActionProperty:
        def __init__(
            self,
            *,
            fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulePropsMixin.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''
            :param fields: An array of case fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-updatecaseaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                # empty_value: Any
                
                update_case_action_property = connect_mixins.CfnRulePropsMixin.UpdateCaseActionProperty(
                    fields=[connect_mixins.CfnRulePropsMixin.FieldProperty(
                        id="id",
                        value=connect_mixins.CfnRulePropsMixin.FieldValueProperty(
                            boolean_value=False,
                            double_value=123,
                            empty_value=empty_value,
                            string_value="stringValue"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__523448360bca58d27a51d620dbcdd332b59f6eb98e756d85d4b785eff6e2aab7)
                check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fields is not None:
                self._values["fields"] = fields

        @builtins.property
        def fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FieldProperty"]]]]:
            '''An array of case fields.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-rule-updatecaseaction.html#cfn-connect-rule-updatecaseaction-fields
            '''
            result = self._values.get("fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulePropsMixin.FieldProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateCaseActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"instance_id": "instanceId", "key": "key"},
)
class CfnSecurityKeyMixinProps:
    def __init__(
        self,
        *,
        instance_id: typing.Optional[builtins.str] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSecurityKeyPropsMixin.

        :param instance_id: The Amazon Resource Name (ARN) of the instance. *Minimum* : ``1`` *Maximum* : ``100``
        :param key: A valid security key in PEM format. For example:. ``"-----BEGIN PUBLIC KEY-----\\ [a lot of characters] ----END PUBLIC KEY-----"`` *Minimum* : ``1`` *Maximum* : ``1024``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_security_key_mixin_props = connect_mixins.CfnSecurityKeyMixinProps(
                instance_id="instanceId",
                key="key"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a691082a031b56a67ddfcbbba4df7fe2310fb3012ba413a2d790791fa2065a9)
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        *Minimum* : ``1``

        *Maximum* : ``100``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html#cfn-connect-securitykey-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''A valid security key in PEM format. For example:.

        ``"-----BEGIN PUBLIC KEY-----\\ [a lot of characters] ----END PUBLIC KEY-----"``

        *Minimum* : ``1``

        *Maximum* : ``1024``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html#cfn-connect-securitykey-key
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityKeyPropsMixin",
):
    '''The security key for the instance.

    .. epigraph::

       Only two security keys are allowed per Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securitykey.html
    :cloudformationResource: AWS::Connect::SecurityKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_security_key_props_mixin = connect_mixins.CfnSecurityKeyPropsMixin(connect_mixins.CfnSecurityKeyMixinProps(
            instance_id="instanceId",
            key="key"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSecurityKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::SecurityKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55d832d4b8979677c58e4e60054fc177f8f1c745d9f8c7ad73c07b31a2d71b5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc8e15b985a2ff49f532bd9c83c596c94fa1eb2e7d2aa3d580901670810f892)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3173f8a09281de1ac5175f9007803d639f5e35d343af03fa344753c7c2fd8647)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityKeyMixinProps:
        return typing.cast(CfnSecurityKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_access_control_hierarchy_group_id": "allowedAccessControlHierarchyGroupId",
        "allowed_access_control_tags": "allowedAccessControlTags",
        "applications": "applications",
        "description": "description",
        "granular_access_control_configuration": "granularAccessControlConfiguration",
        "hierarchy_restricted_resources": "hierarchyRestrictedResources",
        "instance_arn": "instanceArn",
        "permissions": "permissions",
        "security_profile_name": "securityProfileName",
        "tag_restricted_resources": "tagRestrictedResources",
        "tags": "tags",
    },
)
class CfnSecurityProfileMixinProps:
    def __init__(
        self,
        *,
        allowed_access_control_hierarchy_group_id: typing.Optional[builtins.str] = None,
        allowed_access_control_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        applications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityProfilePropsMixin.ApplicationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        granular_access_control_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        hierarchy_restricted_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        security_profile_name: typing.Optional[builtins.str] = None,
        tag_restricted_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSecurityProfilePropsMixin.

        :param allowed_access_control_hierarchy_group_id: The identifier of the hierarchy group that a security profile uses to restrict access to resources in Amazon Connect.
        :param allowed_access_control_tags: The list of tags that a security profile uses to restrict access to resources in Amazon Connect.
        :param applications: A list of third-party applications that the security profile will give access to.
        :param description: The description of the security profile.
        :param granular_access_control_configuration: 
        :param hierarchy_restricted_resources: The list of resources that a security profile applies hierarchy restrictions to in Amazon Connect. Following are acceptable ResourceNames: ``User`` .
        :param instance_arn: The identifier of the Amazon Connect instance.
        :param permissions: Permissions assigned to the security profile. For a list of valid permissions, see `List of security profile permissions <https://docs.aws.amazon.com/connect/latest/adminguide/security-profile-list.html>`_ .
        :param security_profile_name: The name for the security profile.
        :param tag_restricted_resources: The list of resources that a security profile applies tag restrictions to in Amazon Connect.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_security_profile_mixin_props = connect_mixins.CfnSecurityProfileMixinProps(
                allowed_access_control_hierarchy_group_id="allowedAccessControlHierarchyGroupId",
                allowed_access_control_tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                applications=[connect_mixins.CfnSecurityProfilePropsMixin.ApplicationProperty(
                    application_permissions=["applicationPermissions"],
                    namespace="namespace"
                )],
                description="description",
                granular_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty(
                    data_table_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty(
                        primary_attribute_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty(
                            primary_attribute_values=[connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty(
                                access_type="accessType",
                                attribute_name="attributeName",
                                values=["values"]
                            )]
                        )
                    )
                ),
                hierarchy_restricted_resources=["hierarchyRestrictedResources"],
                instance_arn="instanceArn",
                permissions=["permissions"],
                security_profile_name="securityProfileName",
                tag_restricted_resources=["tagRestrictedResources"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8741bb5c41219d2c1a527ea8eeb43262286744d3b49203f9b8f54239d14d611a)
            check_type(argname="argument allowed_access_control_hierarchy_group_id", value=allowed_access_control_hierarchy_group_id, expected_type=type_hints["allowed_access_control_hierarchy_group_id"])
            check_type(argname="argument allowed_access_control_tags", value=allowed_access_control_tags, expected_type=type_hints["allowed_access_control_tags"])
            check_type(argname="argument applications", value=applications, expected_type=type_hints["applications"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument granular_access_control_configuration", value=granular_access_control_configuration, expected_type=type_hints["granular_access_control_configuration"])
            check_type(argname="argument hierarchy_restricted_resources", value=hierarchy_restricted_resources, expected_type=type_hints["hierarchy_restricted_resources"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument security_profile_name", value=security_profile_name, expected_type=type_hints["security_profile_name"])
            check_type(argname="argument tag_restricted_resources", value=tag_restricted_resources, expected_type=type_hints["tag_restricted_resources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_access_control_hierarchy_group_id is not None:
            self._values["allowed_access_control_hierarchy_group_id"] = allowed_access_control_hierarchy_group_id
        if allowed_access_control_tags is not None:
            self._values["allowed_access_control_tags"] = allowed_access_control_tags
        if applications is not None:
            self._values["applications"] = applications
        if description is not None:
            self._values["description"] = description
        if granular_access_control_configuration is not None:
            self._values["granular_access_control_configuration"] = granular_access_control_configuration
        if hierarchy_restricted_resources is not None:
            self._values["hierarchy_restricted_resources"] = hierarchy_restricted_resources
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if permissions is not None:
            self._values["permissions"] = permissions
        if security_profile_name is not None:
            self._values["security_profile_name"] = security_profile_name
        if tag_restricted_resources is not None:
            self._values["tag_restricted_resources"] = tag_restricted_resources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def allowed_access_control_hierarchy_group_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The identifier of the hierarchy group that a security profile uses to restrict access to resources in Amazon Connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-allowedaccesscontrolhierarchygroupid
        '''
        result = self._values.get("allowed_access_control_hierarchy_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def allowed_access_control_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]]:
        '''The list of tags that a security profile uses to restrict access to resources in Amazon Connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-allowedaccesscontroltags
        '''
        result = self._values.get("allowed_access_control_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_ceddda9d.CfnTag]]]], result)

    @builtins.property
    def applications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.ApplicationProperty"]]]]:
        '''A list of third-party applications that the security profile will give access to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-applications
        '''
        result = self._values.get("applications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.ApplicationProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the security profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def granular_access_control_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-granularaccesscontrolconfiguration
        '''
        result = self._values.get("granular_access_control_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty"]], result)

    @builtins.property
    def hierarchy_restricted_resources(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resources that a security profile applies hierarchy restrictions to in Amazon Connect.

        Following are acceptable ResourceNames: ``User`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-hierarchyrestrictedresources
        '''
        result = self._values.get("hierarchy_restricted_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Permissions assigned to the security profile.

        For a list of valid permissions, see `List of security profile permissions <https://docs.aws.amazon.com/connect/latest/adminguide/security-profile-list.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-permissions
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def security_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name for the security profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-securityprofilename
        '''
        result = self._values.get("security_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_restricted_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resources that a security profile applies tag restrictions to in Amazon Connect.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-tagrestrictedresources
        '''
        result = self._values.get("tag_restricted_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "Tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html#cfn-connect-securityprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSecurityProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSecurityProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfilePropsMixin",
):
    '''Creates a security profile.

    For information about security profiles, see `Security Profiles <https://docs.aws.amazon.com/connect/latest/adminguide/connect-security-profiles.html>`_ in the *Amazon Connect Administrator Guide* . For a mapping of the API name and user interface name of the security profile permissions, see `List of security profile permissions <https://docs.aws.amazon.com/connect/latest/adminguide/security-profile-list.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-securityprofile.html
    :cloudformationResource: AWS::Connect::SecurityProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_security_profile_props_mixin = connect_mixins.CfnSecurityProfilePropsMixin(connect_mixins.CfnSecurityProfileMixinProps(
            allowed_access_control_hierarchy_group_id="allowedAccessControlHierarchyGroupId",
            allowed_access_control_tags=[CfnTag(
                key="key",
                value="value"
            )],
            applications=[connect_mixins.CfnSecurityProfilePropsMixin.ApplicationProperty(
                application_permissions=["applicationPermissions"],
                namespace="namespace"
            )],
            description="description",
            granular_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty(
                data_table_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty(
                    primary_attribute_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty(
                        primary_attribute_values=[connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty(
                            access_type="accessType",
                            attribute_name="attributeName",
                            values=["values"]
                        )]
                    )
                )
            ),
            hierarchy_restricted_resources=["hierarchyRestrictedResources"],
            instance_arn="instanceArn",
            permissions=["permissions"],
            security_profile_name="securityProfileName",
            tag_restricted_resources=["tagRestrictedResources"],
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
        props: typing.Union[CfnSecurityProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::SecurityProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db9c0ab7fceae7e82f6cd38fd66d9d2ff1facb1ad03630a9f7b96135755b721)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c6f8078c97ae6678c700d3478ca7dbcb52860a75036387973a672393c6e4f4b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731a654d650f2d5e06044b1b926138faea9dd897644cc4515c758c887e695cc3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSecurityProfileMixinProps:
        return typing.cast(CfnSecurityProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfilePropsMixin.ApplicationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_permissions": "applicationPermissions",
            "namespace": "namespace",
        },
    )
    class ApplicationProperty:
        def __init__(
            self,
            *,
            application_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This API is in preview release for Amazon Connect and is subject to change.

            A third-party application's metadata.

            :param application_permissions: The permissions that the agent is granted on the application. Only the ``ACCESS`` permission is supported.
            :param namespace: Namespace of the application that you want to give access to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-application.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                application_property = connect_mixins.CfnSecurityProfilePropsMixin.ApplicationProperty(
                    application_permissions=["applicationPermissions"],
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e350e330c9a978caa94b8096526a4fab2e32192a00da7c976967948da89ae619)
                check_type(argname="argument application_permissions", value=application_permissions, expected_type=type_hints["application_permissions"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_permissions is not None:
                self._values["application_permissions"] = application_permissions
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def application_permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The permissions that the agent is granted on the application.

            Only the ``ACCESS`` permission is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-application.html#cfn-connect-securityprofile-application-applicationpermissions
            '''
            result = self._values.get("application_permissions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''Namespace of the application that you want to give access to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-application.html#cfn-connect-securityprofile-application-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "primary_attribute_access_control_configuration": "primaryAttributeAccessControlConfiguration",
        },
    )
    class DataTableAccessControlConfigurationProperty:
        def __init__(
            self,
            *,
            primary_attribute_access_control_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the access control configuration for data tables.

            :param primary_attribute_access_control_configuration: Contains the configuration for record-based access control.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-datatableaccesscontrolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                data_table_access_control_configuration_property = connect_mixins.CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty(
                    primary_attribute_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty(
                        primary_attribute_values=[connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty(
                            access_type="accessType",
                            attribute_name="attributeName",
                            values=["values"]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aa9e504081e076390fdde648274bf823a9c98c6c2f8e4e445069efe3c7e7401e)
                check_type(argname="argument primary_attribute_access_control_configuration", value=primary_attribute_access_control_configuration, expected_type=type_hints["primary_attribute_access_control_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if primary_attribute_access_control_configuration is not None:
                self._values["primary_attribute_access_control_configuration"] = primary_attribute_access_control_configuration

        @builtins.property
        def primary_attribute_access_control_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty"]]:
            '''Contains the configuration for record-based access control.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-datatableaccesscontrolconfiguration.html#cfn-connect-securityprofile-datatableaccesscontrolconfiguration-primaryattributeaccesscontrolconfiguration
            '''
            result = self._values.get("primary_attribute_access_control_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataTableAccessControlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_table_access_control_configuration": "dataTableAccessControlConfiguration",
        },
    )
    class GranularAccessControlConfigurationProperty:
        def __init__(
            self,
            *,
            data_table_access_control_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param data_table_access_control_configuration: Defines the access control configuration for data tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-granularaccesscontrolconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                granular_access_control_configuration_property = connect_mixins.CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty(
                    data_table_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty(
                        primary_attribute_access_control_configuration=connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty(
                            primary_attribute_values=[connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty(
                                access_type="accessType",
                                attribute_name="attributeName",
                                values=["values"]
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db4b66ee1ee9161fea501ebd2604cb136ca7ff79f3bd08712caa3617e0c49b8f)
                check_type(argname="argument data_table_access_control_configuration", value=data_table_access_control_configuration, expected_type=type_hints["data_table_access_control_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_table_access_control_configuration is not None:
                self._values["data_table_access_control_configuration"] = data_table_access_control_configuration

        @builtins.property
        def data_table_access_control_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty"]]:
            '''Defines the access control configuration for data tables.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-granularaccesscontrolconfiguration.html#cfn-connect-securityprofile-granularaccesscontrolconfiguration-datatableaccesscontrolconfiguration
            '''
            result = self._values.get("data_table_access_control_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GranularAccessControlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty",
        jsii_struct_bases=[],
        name_mapping={"primary_attribute_values": "primaryAttributeValues"},
    )
    class PrimaryAttributeAccessControlConfigurationItemProperty:
        def __init__(
            self,
            *,
            primary_attribute_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains the configuration for record-based access control.

            :param primary_attribute_values: An array of PrimaryAttributeValue objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-primaryattributeaccesscontrolconfigurationitem.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                primary_attribute_access_control_configuration_item_property = connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty(
                    primary_attribute_values=[connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty(
                        access_type="accessType",
                        attribute_name="attributeName",
                        values=["values"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86f9b0aa95d3409687f8645e81d33bb085cdfae6adfbb738e02c5cd1f0fb0ad0)
                check_type(argname="argument primary_attribute_values", value=primary_attribute_values, expected_type=type_hints["primary_attribute_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if primary_attribute_values is not None:
                self._values["primary_attribute_values"] = primary_attribute_values

        @builtins.property
        def primary_attribute_values(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty"]]]]:
            '''An array of PrimaryAttributeValue objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-primaryattributeaccesscontrolconfigurationitem.html#cfn-connect-securityprofile-primaryattributeaccesscontrolconfigurationitem-primaryattributevalues
            '''
            result = self._values.get("primary_attribute_values")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryAttributeAccessControlConfigurationItemProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_type": "accessType",
            "attribute_name": "attributeName",
            "values": "values",
        },
    )
    class PrimaryAttributeValueProperty:
        def __init__(
            self,
            *,
            access_type: typing.Optional[builtins.str] = None,
            attribute_name: typing.Optional[builtins.str] = None,
            values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object defining the access control for a specific attribute and its values.

            :param access_type: Specifies the type of access granted. Currently, only "ALLOW" is supported
            :param attribute_name: The name of the primary attribute.
            :param values: An array of allowed primary values for the specified primary attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-primaryattributevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                primary_attribute_value_property = connect_mixins.CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty(
                    access_type="accessType",
                    attribute_name="attributeName",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c341c3f92fe9661253958dbdd13ba1f855372de88a7a0719cb164cae4223b01)
                check_type(argname="argument access_type", value=access_type, expected_type=type_hints["access_type"])
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_type is not None:
                self._values["access_type"] = access_type
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if values is not None:
                self._values["values"] = values

        @builtins.property
        def access_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of access granted.

            Currently, only "ALLOW" is supported

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-primaryattributevalue.html#cfn-connect-securityprofile-primaryattributevalue-accesstype
            '''
            result = self._values.get("access_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of the primary attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-primaryattributevalue.html#cfn-connect-securityprofile-primaryattributevalue-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of allowed primary values for the specified primary attribute.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-securityprofile-primaryattributevalue.html#cfn-connect-securityprofile-primaryattributevalue-values
            '''
            result = self._values.get("values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrimaryAttributeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_token": "clientToken",
        "constraints": "constraints",
        "contact_flow_arn": "contactFlowArn",
        "defaults": "defaults",
        "description": "description",
        "fields": "fields",
        "instance_arn": "instanceArn",
        "name": "name",
        "self_assign_contact_flow_arn": "selfAssignContactFlowArn",
        "status": "status",
        "tags": "tags",
    },
)
class CfnTaskTemplateMixinProps:
    def __init__(
        self,
        *,
        client_token: typing.Optional[builtins.str] = None,
        constraints: typing.Any = None,
        contact_flow_arn: typing.Optional[builtins.str] = None,
        defaults: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.DefaultFieldValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.FieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        self_assign_contact_flow_arn: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTaskTemplatePropsMixin.

        :param client_token: A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.
        :param constraints: Constraints that are applicable to the fields listed. The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.
        :param contact_flow_arn: The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template. ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .
        :param defaults: The default values for fields when a task is created by referencing this template.
        :param description: The description of the task template.
        :param fields: Fields that are part of the template. A template requires at least one field that has type ``Name`` .
        :param instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param name: The name of the task template.
        :param self_assign_contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param status: The status of the task template.
        :param tags: The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            # constraints: Any
            
            cfn_task_template_mixin_props = connect_mixins.CfnTaskTemplateMixinProps(
                client_token="clientToken",
                constraints=constraints,
                contact_flow_arn="contactFlowArn",
                defaults=[connect_mixins.CfnTaskTemplatePropsMixin.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    )
                )],
                description="description",
                fields=[connect_mixins.CfnTaskTemplatePropsMixin.FieldProperty(
                    description="description",
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    ),
                    single_select_options=["singleSelectOptions"],
                    type="type"
                )],
                instance_arn="instanceArn",
                name="name",
                self_assign_contact_flow_arn="selfAssignContactFlowArn",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fffbb0723f3425ee0abb5a58cdc0eb6980e0f37a057f6339282db32cb3928f95)
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
            check_type(argname="argument contact_flow_arn", value=contact_flow_arn, expected_type=type_hints["contact_flow_arn"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument fields", value=fields, expected_type=type_hints["fields"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument self_assign_contact_flow_arn", value=self_assign_contact_flow_arn, expected_type=type_hints["self_assign_contact_flow_arn"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_token is not None:
            self._values["client_token"] = client_token
        if constraints is not None:
            self._values["constraints"] = constraints
        if contact_flow_arn is not None:
            self._values["contact_flow_arn"] = contact_flow_arn
        if defaults is not None:
            self._values["defaults"] = defaults
        if description is not None:
            self._values["description"] = description
        if fields is not None:
            self._values["fields"] = fields
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if self_assign_contact_flow_arn is not None:
            self._values["self_assign_contact_flow_arn"] = self_assign_contact_flow_arn
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''A unique, case-sensitive identifier that you provide to ensure the idempotency of the request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-clienttoken
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def constraints(self) -> typing.Any:
        '''Constraints that are applicable to the fields listed.

        The values can be represented in either JSON or YAML format. For an example of the JSON configuration, see *Examples* at the bottom of this page.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-constraints
        '''
        result = self._values.get("constraints")
        return typing.cast(typing.Any, result)

    @builtins.property
    def contact_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow that runs by default when a task is created by referencing this template.

        ``ContactFlowArn`` is not required when there is a field with ``fieldType`` = ``QUICK_CONNECT`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-contactflowarn
        '''
        result = self._values.get("contact_flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def defaults(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.DefaultFieldValueProperty"]]]]:
        '''The default values for fields when a task is created by referencing this template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-defaults
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.DefaultFieldValueProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the task template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fields(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldProperty"]]]]:
        '''Fields that are part of the template.

        A template requires at least one field that has type ``Name`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-fields
        '''
        result = self._values.get("fields")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldProperty"]]]], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the task template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_assign_contact_flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-selfassigncontactflowarn
        '''
        result = self._values.get("self_assign_contact_flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the task template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html#cfn-connect-tasktemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTaskTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTaskTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin",
):
    '''Specifies a task template for a Amazon Connect instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-tasktemplate.html
    :cloudformationResource: AWS::Connect::TaskTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        # constraints: Any
        
        cfn_task_template_props_mixin = connect_mixins.CfnTaskTemplatePropsMixin(connect_mixins.CfnTaskTemplateMixinProps(
            client_token="clientToken",
            constraints=constraints,
            contact_flow_arn="contactFlowArn",
            defaults=[connect_mixins.CfnTaskTemplatePropsMixin.DefaultFieldValueProperty(
                default_value="defaultValue",
                id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                    name="name"
                )
            )],
            description="description",
            fields=[connect_mixins.CfnTaskTemplatePropsMixin.FieldProperty(
                description="description",
                id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                    name="name"
                ),
                single_select_options=["singleSelectOptions"],
                type="type"
            )],
            instance_arn="instanceArn",
            name="name",
            self_assign_contact_flow_arn="selfAssignContactFlowArn",
            status="status",
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
        props: typing.Union[CfnTaskTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::TaskTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edd5b28ec4fd2a594ffb8a8e1f7ca35a6005d224466f664cfa93e14fc6c08b2c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5c2e67329c6b663bc5ee835621b867283f07a26a45b70e24d1935c67d032f0f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__425700ea564e1b8d83ba7ee24d00d41eb120f93ebcc28132eccee0d426ee8492)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTaskTemplateMixinProps:
        return typing.cast(CfnTaskTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.ConstraintsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "invisible_fields": "invisibleFields",
            "read_only_fields": "readOnlyFields",
            "required_fields": "requiredFields",
        },
    )
    class ConstraintsProperty:
        def __init__(
            self,
            *,
            invisible_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            read_only_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            required_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes constraints that apply to the template fields.

            :param invisible_fields: Lists the fields that are invisible to agents.
            :param read_only_fields: Lists the fields that are read-only to agents, and cannot be edited.
            :param required_fields: Lists the fields that are required to be filled by agents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                constraints_property = connect_mixins.CfnTaskTemplatePropsMixin.ConstraintsProperty(
                    invisible_fields=[connect_mixins.CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty(
                        id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                            name="name"
                        )
                    )],
                    read_only_fields=[connect_mixins.CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty(
                        id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                            name="name"
                        )
                    )],
                    required_fields=[connect_mixins.CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty(
                        id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                            name="name"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f3c3d756aa44adcf1938b9028f9ed0ce6bb85b348388b2c0a41d5302b49828cd)
                check_type(argname="argument invisible_fields", value=invisible_fields, expected_type=type_hints["invisible_fields"])
                check_type(argname="argument read_only_fields", value=read_only_fields, expected_type=type_hints["read_only_fields"])
                check_type(argname="argument required_fields", value=required_fields, expected_type=type_hints["required_fields"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if invisible_fields is not None:
                self._values["invisible_fields"] = invisible_fields
            if read_only_fields is not None:
                self._values["read_only_fields"] = read_only_fields
            if required_fields is not None:
                self._values["required_fields"] = required_fields

        @builtins.property
        def invisible_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty"]]]]:
            '''Lists the fields that are invisible to agents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-invisiblefields
            '''
            result = self._values.get("invisible_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty"]]]], result)

        @builtins.property
        def read_only_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty"]]]]:
            '''Lists the fields that are read-only to agents, and cannot be edited.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-readonlyfields
            '''
            result = self._values.get("read_only_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty"]]]], result)

        @builtins.property
        def required_fields(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty"]]]]:
            '''Lists the fields that are required to be filled by agents.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-constraints.html#cfn-connect-tasktemplate-constraints-requiredfields
            '''
            result = self._values.get("required_fields")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConstraintsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.DefaultFieldValueProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue", "id": "id"},
    )
    class DefaultFieldValueProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes a default field and its corresponding value.

            :param default_value: Default value for the field.
            :param id: Identifier of a field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                default_field_value_property = connect_mixins.CfnTaskTemplatePropsMixin.DefaultFieldValueProperty(
                    default_value="defaultValue",
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__640a0f7f8b2dc14bd603a5d3a3dded2c13a1d63d0c30a5e0873fd45f73dd7ce8)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''Default value for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]]:
            '''Identifier of a field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-defaultfieldvalue.html#cfn-connect-tasktemplate-defaultfieldvalue-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultFieldValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class FieldIdentifierProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''The identifier of the task template field.

            :param name: The name of the task template field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-fieldidentifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                field_identifier_property = connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4bebf6090bd1b96e0e738185bbd17ac531398eb008e4fa4afce833793dc62861)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the task template field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-fieldidentifier.html#cfn-connect-tasktemplate-fieldidentifier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldIdentifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.FieldProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "id": "id",
            "single_select_options": "singleSelectOptions",
            "type": "type",
        },
    )
    class FieldProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a single task template field.

            :param description: The description of the field.
            :param id: The unique identifier for the field.
            :param single_select_options: A list of options for a single select field.
            :param type: Indicates the type of field. Following are the valid field types: ``NAME`` ``DESCRIPTION`` | ``SCHEDULED_TIME`` | ``QUICK_CONNECT`` | ``URL`` | ``NUMBER`` | ``TEXT`` | ``TEXT_AREA`` | ``DATE_TIME`` | ``BOOLEAN`` | ``SINGLE_SELECT`` | ``EMAIL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                field_property = connect_mixins.CfnTaskTemplatePropsMixin.FieldProperty(
                    description="description",
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    ),
                    single_select_options=["singleSelectOptions"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__66d52b5df896b87e3bff67b3cea897fae5551f59f339998b98a1d138359178d2)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument single_select_options", value=single_select_options, expected_type=type_hints["single_select_options"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if id is not None:
                self._values["id"] = id
            if single_select_options is not None:
                self._values["single_select_options"] = single_select_options
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]]:
            '''The unique identifier for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]], result)

        @builtins.property
        def single_select_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of options for a single select field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-singleselectoptions
            '''
            result = self._values.get("single_select_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Indicates the type of field.

            Following are the valid field types: ``NAME`` ``DESCRIPTION`` | ``SCHEDULED_TIME`` | ``QUICK_CONNECT`` | ``URL`` | ``NUMBER`` | ``TEXT`` | ``TEXT_AREA`` | ``DATE_TIME`` | ``BOOLEAN`` | ``SINGLE_SELECT`` | ``EMAIL``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-field.html#cfn-connect-tasktemplate-field-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class InvisibleFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A field that is invisible to an agent.

            :param id: Identifier of the invisible field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                invisible_field_info_property = connect_mixins.CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty(
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8961e1b4434aecef4dd770af578f72195b0710998cd87f8e519f8597b073b47d)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]]:
            '''Identifier of the invisible field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-invisiblefieldinfo.html#cfn-connect-tasktemplate-invisiblefieldinfo-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InvisibleFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class ReadOnlyFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Indicates a field that is read-only to an agent.

            :param id: Identifier of the read-only field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                read_only_field_info_property = connect_mixins.CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty(
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ffa9bfe62e583eae81b77013a630dbc1cf7dec35c4ce7efbaef756dbe4af419)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]]:
            '''Identifier of the read-only field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-readonlyfieldinfo.html#cfn-connect-tasktemplate-readonlyfieldinfo-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadOnlyFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class RequiredFieldInfoProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTaskTemplatePropsMixin.FieldIdentifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about a required field.

            :param id: The unique identifier for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                required_field_info_property = connect_mixins.CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty(
                    id=connect_mixins.CfnTaskTemplatePropsMixin.FieldIdentifierProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a7c8fb0c8eb87e15701479f2f93243e5f9bee3f43bb23e7792cdb1655bb55f0)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]]:
            '''The unique identifier for the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-tasktemplate-requiredfieldinfo.html#cfn-connect-tasktemplate-requiredfieldinfo-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTaskTemplatePropsMixin.FieldIdentifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequiredFieldInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTrafficDistributionGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "tags": "tags",
    },
)
class CfnTrafficDistributionGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTrafficDistributionGroupPropsMixin.

        :param description: The description of the traffic distribution group.
        :param instance_arn: The Amazon Resource Name (ARN).
        :param name: The name of the traffic distribution group.
        :param tags: The tags used to organize, track, or control access for this resource. For example, {"tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-trafficdistributiongroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_traffic_distribution_group_mixin_props = connect_mixins.CfnTrafficDistributionGroupMixinProps(
                description="description",
                instance_arn="instanceArn",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11363e3b01378326a043d2ef1414ab7ba339453d9579003194d67df5123f86a)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the traffic distribution group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-trafficdistributiongroup.html#cfn-connect-trafficdistributiongroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-trafficdistributiongroup.html#cfn-connect-trafficdistributiongroup-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the traffic distribution group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-trafficdistributiongroup.html#cfn-connect-trafficdistributiongroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, {"tags": {"key1":"value1", "key2":"value2"} }.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-trafficdistributiongroup.html#cfn-connect-trafficdistributiongroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrafficDistributionGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrafficDistributionGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnTrafficDistributionGroupPropsMixin",
):
    '''Information about a traffic distribution group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-trafficdistributiongroup.html
    :cloudformationResource: AWS::Connect::TrafficDistributionGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_traffic_distribution_group_props_mixin = connect_mixins.CfnTrafficDistributionGroupPropsMixin(connect_mixins.CfnTrafficDistributionGroupMixinProps(
            description="description",
            instance_arn="instanceArn",
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
        props: typing.Union[CfnTrafficDistributionGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::TrafficDistributionGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3dd694b2b87268524857e2ec09362241db50b48b9b2aff03652767dc0d0ee82)
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
            type_hints = typing.get_type_hints(_typecheckingstub__120b783baec79bf0399d29ea94ef3928b4f08a592462630ccc6b350f4f1f257f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b96425e9fa1408b9f5c87c3c7d892dcb41c11062780d1081063d0b8d98dabf9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrafficDistributionGroupMixinProps:
        return typing.cast(CfnTrafficDistributionGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "name": "name",
        "parent_group_arn": "parentGroupArn",
        "tags": "tags",
    },
)
class CfnUserHierarchyGroupMixinProps:
    def __init__(
        self,
        *,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        parent_group_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnUserHierarchyGroupPropsMixin.

        :param instance_arn: The Amazon Resource Name (ARN) of the user hierarchy group.
        :param name: The name of the user hierarchy group.
        :param parent_group_arn: The Amazon Resource Name (ARN) of the parent group.
        :param tags: An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_user_hierarchy_group_mixin_props = connect_mixins.CfnUserHierarchyGroupMixinProps(
                instance_arn="instanceArn",
                name="name",
                parent_group_arn="parentGroupArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b83fd73ae5bba166ac452b4050780f3e4b6b0ca05f404362e040d4a8a48078)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parent_group_arn", value=parent_group_arn, expected_type=type_hints["parent_group_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if parent_group_arn is not None:
            self._values["parent_group_arn"] = parent_group_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user hierarchy group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the user hierarchy group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parent_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the parent group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-parentgrouparn
        '''
        result = self._values.get("parent_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html#cfn-connect-userhierarchygroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserHierarchyGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserHierarchyGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyGroupPropsMixin",
):
    '''Specifies a new user hierarchy group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchygroup.html
    :cloudformationResource: AWS::Connect::UserHierarchyGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_user_hierarchy_group_props_mixin = connect_mixins.CfnUserHierarchyGroupPropsMixin(connect_mixins.CfnUserHierarchyGroupMixinProps(
            instance_arn="instanceArn",
            name="name",
            parent_group_arn="parentGroupArn",
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
        props: typing.Union[CfnUserHierarchyGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::UserHierarchyGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__680733510943706d81fdeb4265c63fb91b5105765312c45fdfe173d4ff2d4edd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__86a62523ecf1d21f493826c831f3fbc97ba964a2d2b2d315b3e50183c8d66724)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac29ed3ff1d940eebd19380d4578f2f92b1eb8f63c7d293a893b4f8f50e5e123)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserHierarchyGroupMixinProps:
        return typing.cast(CfnUserHierarchyGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructureMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "user_hierarchy_structure": "userHierarchyStructure",
    },
)
class CfnUserHierarchyStructureMixinProps:
    def __init__(
        self,
        *,
        instance_arn: typing.Optional[builtins.str] = None,
        user_hierarchy_structure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnUserHierarchyStructurePropsMixin.

        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param user_hierarchy_structure: Contains information about a hierarchy structure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchystructure.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_user_hierarchy_structure_mixin_props = connect_mixins.CfnUserHierarchyStructureMixinProps(
                instance_arn="instanceArn",
                user_hierarchy_structure=connect_mixins.CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty(
                    level_five=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFiveProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_four=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFourProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_one=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelOneProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_three=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelThreeProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_two=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelTwoProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0303262d5d1b6ffd2599ad3ae7307fff1d0db0cdc484aac23db76a93484fed80)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument user_hierarchy_structure", value=user_hierarchy_structure, expected_type=type_hints["user_hierarchy_structure"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if user_hierarchy_structure is not None:
            self._values["user_hierarchy_structure"] = user_hierarchy_structure

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchystructure.html#cfn-connect-userhierarchystructure-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_hierarchy_structure(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty"]]:
        '''Contains information about a hierarchy structure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchystructure.html#cfn-connect-userhierarchystructure-userhierarchystructure
        '''
        result = self._values.get("user_hierarchy_structure")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserHierarchyStructureMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserHierarchyStructurePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin",
):
    '''Contains information about a hierarchy structure.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-userhierarchystructure.html
    :cloudformationResource: AWS::Connect::UserHierarchyStructure
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_user_hierarchy_structure_props_mixin = connect_mixins.CfnUserHierarchyStructurePropsMixin(connect_mixins.CfnUserHierarchyStructureMixinProps(
            instance_arn="instanceArn",
            user_hierarchy_structure=connect_mixins.CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty(
                level_five=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFiveProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                ),
                level_four=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFourProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                ),
                level_one=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelOneProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                ),
                level_three=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelThreeProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                ),
                level_two=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelTwoProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserHierarchyStructureMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::UserHierarchyStructure``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27bea220dc18416f5d2a822206d7a9c672debf2335b764672e8744fa7c192411)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b906a6ddf59ee363b57ccb7af361cb9fa32c9b36ca3841a0b848cc5eda553986)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2bf15c042cad6ff2ee813b9ff0e793a7c1872db9ebc5c644fba20775f4dc13)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserHierarchyStructureMixinProps:
        return typing.cast(CfnUserHierarchyStructureMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin.LevelFiveProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hierarchy_level_arn": "hierarchyLevelArn",
            "hierarchy_level_id": "hierarchyLevelId",
            "name": "name",
        },
    )
    class LevelFiveProperty:
        def __init__(
            self,
            *,
            hierarchy_level_arn: typing.Optional[builtins.str] = None,
            hierarchy_level_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The update for level five.

            :param hierarchy_level_arn: The Amazon Resource Name (ARN) of the hierarchy level.
            :param hierarchy_level_id: The identifier of the hierarchy level.
            :param name: The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfive.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                level_five_property = connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFiveProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__894dddf1a74864d0487df23149a2c90472705eae27af745a6634fb15bd15cbe6)
                check_type(argname="argument hierarchy_level_arn", value=hierarchy_level_arn, expected_type=type_hints["hierarchy_level_arn"])
                check_type(argname="argument hierarchy_level_id", value=hierarchy_level_id, expected_type=type_hints["hierarchy_level_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hierarchy_level_arn is not None:
                self._values["hierarchy_level_arn"] = hierarchy_level_arn
            if hierarchy_level_id is not None:
                self._values["hierarchy_level_id"] = hierarchy_level_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def hierarchy_level_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfive.html#cfn-connect-userhierarchystructure-levelfive-hierarchylevelarn
            '''
            result = self._values.get("hierarchy_level_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_level_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfive.html#cfn-connect-userhierarchystructure-levelfive-hierarchylevelid
            '''
            result = self._values.get("hierarchy_level_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfive.html#cfn-connect-userhierarchystructure-levelfive-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LevelFiveProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin.LevelFourProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hierarchy_level_arn": "hierarchyLevelArn",
            "hierarchy_level_id": "hierarchyLevelId",
            "name": "name",
        },
    )
    class LevelFourProperty:
        def __init__(
            self,
            *,
            hierarchy_level_arn: typing.Optional[builtins.str] = None,
            hierarchy_level_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The update for level four.

            :param hierarchy_level_arn: The Amazon Resource Name (ARN) of the hierarchy level.
            :param hierarchy_level_id: The identifier of the hierarchy level.
            :param name: The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfour.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                level_four_property = connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFourProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63eccffd3a2ff99c082ae978132b9be73c667ee0e75140ea57174d1f3c6b423a)
                check_type(argname="argument hierarchy_level_arn", value=hierarchy_level_arn, expected_type=type_hints["hierarchy_level_arn"])
                check_type(argname="argument hierarchy_level_id", value=hierarchy_level_id, expected_type=type_hints["hierarchy_level_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hierarchy_level_arn is not None:
                self._values["hierarchy_level_arn"] = hierarchy_level_arn
            if hierarchy_level_id is not None:
                self._values["hierarchy_level_id"] = hierarchy_level_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def hierarchy_level_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfour.html#cfn-connect-userhierarchystructure-levelfour-hierarchylevelarn
            '''
            result = self._values.get("hierarchy_level_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_level_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfour.html#cfn-connect-userhierarchystructure-levelfour-hierarchylevelid
            '''
            result = self._values.get("hierarchy_level_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelfour.html#cfn-connect-userhierarchystructure-levelfour-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LevelFourProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin.LevelOneProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hierarchy_level_arn": "hierarchyLevelArn",
            "hierarchy_level_id": "hierarchyLevelId",
            "name": "name",
        },
    )
    class LevelOneProperty:
        def __init__(
            self,
            *,
            hierarchy_level_arn: typing.Optional[builtins.str] = None,
            hierarchy_level_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about level one.

            :param hierarchy_level_arn: The Amazon Resource Name (ARN) of the hierarchy level.
            :param hierarchy_level_id: The identifier of the hierarchy level.
            :param name: The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelone.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                level_one_property = connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelOneProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__665f77eca2c33953ecb563963e5bd8523a0b4e7d61991d48c29ba99e7dfacd37)
                check_type(argname="argument hierarchy_level_arn", value=hierarchy_level_arn, expected_type=type_hints["hierarchy_level_arn"])
                check_type(argname="argument hierarchy_level_id", value=hierarchy_level_id, expected_type=type_hints["hierarchy_level_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hierarchy_level_arn is not None:
                self._values["hierarchy_level_arn"] = hierarchy_level_arn
            if hierarchy_level_id is not None:
                self._values["hierarchy_level_id"] = hierarchy_level_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def hierarchy_level_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelone.html#cfn-connect-userhierarchystructure-levelone-hierarchylevelarn
            '''
            result = self._values.get("hierarchy_level_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_level_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelone.html#cfn-connect-userhierarchystructure-levelone-hierarchylevelid
            '''
            result = self._values.get("hierarchy_level_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelone.html#cfn-connect-userhierarchystructure-levelone-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LevelOneProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin.LevelThreeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hierarchy_level_arn": "hierarchyLevelArn",
            "hierarchy_level_id": "hierarchyLevelId",
            "name": "name",
        },
    )
    class LevelThreeProperty:
        def __init__(
            self,
            *,
            hierarchy_level_arn: typing.Optional[builtins.str] = None,
            hierarchy_level_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The update for level three.

            :param hierarchy_level_arn: The Amazon Resource Name (ARN) of the hierarchy level.
            :param hierarchy_level_id: The identifier of the hierarchy level.
            :param name: The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelthree.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                level_three_property = connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelThreeProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84f5e2c62bc09d2d63067d150de7954f63fc5cc9efd83bf2782030381280dd39)
                check_type(argname="argument hierarchy_level_arn", value=hierarchy_level_arn, expected_type=type_hints["hierarchy_level_arn"])
                check_type(argname="argument hierarchy_level_id", value=hierarchy_level_id, expected_type=type_hints["hierarchy_level_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hierarchy_level_arn is not None:
                self._values["hierarchy_level_arn"] = hierarchy_level_arn
            if hierarchy_level_id is not None:
                self._values["hierarchy_level_id"] = hierarchy_level_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def hierarchy_level_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelthree.html#cfn-connect-userhierarchystructure-levelthree-hierarchylevelarn
            '''
            result = self._values.get("hierarchy_level_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_level_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelthree.html#cfn-connect-userhierarchystructure-levelthree-hierarchylevelid
            '''
            result = self._values.get("hierarchy_level_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-levelthree.html#cfn-connect-userhierarchystructure-levelthree-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LevelThreeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin.LevelTwoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hierarchy_level_arn": "hierarchyLevelArn",
            "hierarchy_level_id": "hierarchyLevelId",
            "name": "name",
        },
    )
    class LevelTwoProperty:
        def __init__(
            self,
            *,
            hierarchy_level_arn: typing.Optional[builtins.str] = None,
            hierarchy_level_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The update for level two.

            :param hierarchy_level_arn: The Amazon Resource Name (ARN) of the hierarchy level.
            :param hierarchy_level_id: The identifier of the hierarchy level.
            :param name: The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-leveltwo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                level_two_property = connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelTwoProperty(
                    hierarchy_level_arn="hierarchyLevelArn",
                    hierarchy_level_id="hierarchyLevelId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a7fb4a1039c8d4aa9d8c76dad4a59e529f6f4fe1267220c8b937e41876b97b2)
                check_type(argname="argument hierarchy_level_arn", value=hierarchy_level_arn, expected_type=type_hints["hierarchy_level_arn"])
                check_type(argname="argument hierarchy_level_id", value=hierarchy_level_id, expected_type=type_hints["hierarchy_level_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hierarchy_level_arn is not None:
                self._values["hierarchy_level_arn"] = hierarchy_level_arn
            if hierarchy_level_id is not None:
                self._values["hierarchy_level_id"] = hierarchy_level_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def hierarchy_level_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-leveltwo.html#cfn-connect-userhierarchystructure-leveltwo-hierarchylevelarn
            '''
            result = self._values.get("hierarchy_level_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_level_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-leveltwo.html#cfn-connect-userhierarchystructure-leveltwo-hierarchylevelid
            '''
            result = self._values.get("hierarchy_level_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the hierarchy level.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-leveltwo.html#cfn-connect-userhierarchystructure-leveltwo-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LevelTwoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty",
        jsii_struct_bases=[],
        name_mapping={
            "level_five": "levelFive",
            "level_four": "levelFour",
            "level_one": "levelOne",
            "level_three": "levelThree",
            "level_two": "levelTwo",
        },
    )
    class UserHierarchyStructureProperty:
        def __init__(
            self,
            *,
            level_five: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserHierarchyStructurePropsMixin.LevelFiveProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            level_four: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserHierarchyStructurePropsMixin.LevelFourProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            level_one: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserHierarchyStructurePropsMixin.LevelOneProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            level_three: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserHierarchyStructurePropsMixin.LevelThreeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            level_two: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserHierarchyStructurePropsMixin.LevelTwoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about a hierarchy structure.

            :param level_five: Information about level five.
            :param level_four: The update for level four.
            :param level_one: The update for level one.
            :param level_three: The update for level three.
            :param level_two: The update for level two.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-userhierarchystructure.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                user_hierarchy_structure_property = connect_mixins.CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty(
                    level_five=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFiveProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_four=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelFourProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_one=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelOneProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_three=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelThreeProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    ),
                    level_two=connect_mixins.CfnUserHierarchyStructurePropsMixin.LevelTwoProperty(
                        hierarchy_level_arn="hierarchyLevelArn",
                        hierarchy_level_id="hierarchyLevelId",
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a41862f6dabdcbb7d82dda5669c9977f41eef4565ed6bcbb4f7592f3db7d2104)
                check_type(argname="argument level_five", value=level_five, expected_type=type_hints["level_five"])
                check_type(argname="argument level_four", value=level_four, expected_type=type_hints["level_four"])
                check_type(argname="argument level_one", value=level_one, expected_type=type_hints["level_one"])
                check_type(argname="argument level_three", value=level_three, expected_type=type_hints["level_three"])
                check_type(argname="argument level_two", value=level_two, expected_type=type_hints["level_two"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if level_five is not None:
                self._values["level_five"] = level_five
            if level_four is not None:
                self._values["level_four"] = level_four
            if level_one is not None:
                self._values["level_one"] = level_one
            if level_three is not None:
                self._values["level_three"] = level_three
            if level_two is not None:
                self._values["level_two"] = level_two

        @builtins.property
        def level_five(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelFiveProperty"]]:
            '''Information about level five.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-userhierarchystructure.html#cfn-connect-userhierarchystructure-userhierarchystructure-levelfive
            '''
            result = self._values.get("level_five")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelFiveProperty"]], result)

        @builtins.property
        def level_four(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelFourProperty"]]:
            '''The update for level four.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-userhierarchystructure.html#cfn-connect-userhierarchystructure-userhierarchystructure-levelfour
            '''
            result = self._values.get("level_four")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelFourProperty"]], result)

        @builtins.property
        def level_one(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelOneProperty"]]:
            '''The update for level one.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-userhierarchystructure.html#cfn-connect-userhierarchystructure-userhierarchystructure-levelone
            '''
            result = self._values.get("level_one")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelOneProperty"]], result)

        @builtins.property
        def level_three(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelThreeProperty"]]:
            '''The update for level three.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-userhierarchystructure.html#cfn-connect-userhierarchystructure-userhierarchystructure-levelthree
            '''
            result = self._values.get("level_three")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelThreeProperty"]], result)

        @builtins.property
        def level_two(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelTwoProperty"]]:
            '''The update for level two.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-userhierarchystructure-userhierarchystructure.html#cfn-connect-userhierarchystructure-userhierarchystructure-leveltwo
            '''
            result = self._values.get("level_two")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserHierarchyStructurePropsMixin.LevelTwoProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserHierarchyStructureProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "directory_user_id": "directoryUserId",
        "hierarchy_group_arn": "hierarchyGroupArn",
        "identity_info": "identityInfo",
        "instance_arn": "instanceArn",
        "password": "password",
        "phone_config": "phoneConfig",
        "routing_profile_arn": "routingProfileArn",
        "security_profile_arns": "securityProfileArns",
        "tags": "tags",
        "username": "username",
        "user_proficiencies": "userProficiencies",
    },
)
class CfnUserMixinProps:
    def __init__(
        self,
        *,
        directory_user_id: typing.Optional[builtins.str] = None,
        hierarchy_group_arn: typing.Optional[builtins.str] = None,
        identity_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.UserIdentityInfoProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        password: typing.Optional[builtins.str] = None,
        phone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.UserPhoneConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        routing_profile_arn: typing.Optional[builtins.str] = None,
        security_profile_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        username: typing.Optional[builtins.str] = None,
        user_proficiencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.UserProficiencyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnUserPropsMixin.

        :param directory_user_id: The identifier of the user account in the directory used for identity management.
        :param hierarchy_group_arn: The Amazon Resource Name (ARN) of the user's hierarchy group.
        :param identity_info: Information about the user identity.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param password: The user's password.
        :param phone_config: Information about the phone configuration for the user.
        :param routing_profile_arn: The Amazon Resource Name (ARN) of the user's routing profile.
        :param security_profile_arns: The Amazon Resource Name (ARN) of the user's security profile.
        :param tags: The tags.
        :param username: The user name assigned to the user account.
        :param user_proficiencies: One or more predefined attributes assigned to a user, with a numeric value that indicates how their level of skill in a specified area.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_user_mixin_props = connect_mixins.CfnUserMixinProps(
                directory_user_id="directoryUserId",
                hierarchy_group_arn="hierarchyGroupArn",
                identity_info=connect_mixins.CfnUserPropsMixin.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                ),
                instance_arn="instanceArn",
                password="password",
                phone_config=connect_mixins.CfnUserPropsMixin.UserPhoneConfigProperty(
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber",
                    persistent_connection=False,
                    phone_type="phoneType"
                ),
                routing_profile_arn="routingProfileArn",
                security_profile_arns=["securityProfileArns"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                username="username",
                user_proficiencies=[connect_mixins.CfnUserPropsMixin.UserProficiencyProperty(
                    attribute_name="attributeName",
                    attribute_value="attributeValue",
                    level=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8354d75e03f378bbba4eae38aad427a4b4fd927e2393bd1e7d9c6f2f713ec3ab)
            check_type(argname="argument directory_user_id", value=directory_user_id, expected_type=type_hints["directory_user_id"])
            check_type(argname="argument hierarchy_group_arn", value=hierarchy_group_arn, expected_type=type_hints["hierarchy_group_arn"])
            check_type(argname="argument identity_info", value=identity_info, expected_type=type_hints["identity_info"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument phone_config", value=phone_config, expected_type=type_hints["phone_config"])
            check_type(argname="argument routing_profile_arn", value=routing_profile_arn, expected_type=type_hints["routing_profile_arn"])
            check_type(argname="argument security_profile_arns", value=security_profile_arns, expected_type=type_hints["security_profile_arns"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument user_proficiencies", value=user_proficiencies, expected_type=type_hints["user_proficiencies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if directory_user_id is not None:
            self._values["directory_user_id"] = directory_user_id
        if hierarchy_group_arn is not None:
            self._values["hierarchy_group_arn"] = hierarchy_group_arn
        if identity_info is not None:
            self._values["identity_info"] = identity_info
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if password is not None:
            self._values["password"] = password
        if phone_config is not None:
            self._values["phone_config"] = phone_config
        if routing_profile_arn is not None:
            self._values["routing_profile_arn"] = routing_profile_arn
        if security_profile_arns is not None:
            self._values["security_profile_arns"] = security_profile_arns
        if tags is not None:
            self._values["tags"] = tags
        if username is not None:
            self._values["username"] = username
        if user_proficiencies is not None:
            self._values["user_proficiencies"] = user_proficiencies

    @builtins.property
    def directory_user_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the user account in the directory used for identity management.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-directoryuserid
        '''
        result = self._values.get("directory_user_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hierarchy_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's hierarchy group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-hierarchygrouparn
        '''
        result = self._values.get("hierarchy_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.UserIdentityInfoProperty"]]:
        '''Information about the user identity.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-identityinfo
        '''
        result = self._values.get("identity_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.UserIdentityInfoProperty"]], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The user's password.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-password
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def phone_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.UserPhoneConfigProperty"]]:
        '''Information about the phone configuration for the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-phoneconfig
        '''
        result = self._values.get("phone_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.UserPhoneConfigProperty"]], result)

    @builtins.property
    def routing_profile_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the user's routing profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-routingprofilearn
        '''
        result = self._values.get("routing_profile_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_profile_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) of the user's security profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-securityprofilearns
        '''
        result = self._values.get("security_profile_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The user name assigned to the user account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_proficiencies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.UserProficiencyProperty"]]]]:
        '''One or more predefined attributes assigned to a user, with a numeric value that indicates how their level of skill in a specified area.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html#cfn-connect-user-userproficiencies
        '''
        result = self._values.get("user_proficiencies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.UserProficiencyProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserPropsMixin",
):
    '''Specifies a user account for an Amazon Connect instance.

    For information about how to create user accounts using the Amazon Connect console, see `Add Users <https://docs.aws.amazon.com/connect/latest/adminguide/user-management.html>`_ in the *Amazon Connect Administrator Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-user.html
    :cloudformationResource: AWS::Connect::User
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_user_props_mixin = connect_mixins.CfnUserPropsMixin(connect_mixins.CfnUserMixinProps(
            directory_user_id="directoryUserId",
            hierarchy_group_arn="hierarchyGroupArn",
            identity_info=connect_mixins.CfnUserPropsMixin.UserIdentityInfoProperty(
                email="email",
                first_name="firstName",
                last_name="lastName",
                mobile="mobile",
                secondary_email="secondaryEmail"
            ),
            instance_arn="instanceArn",
            password="password",
            phone_config=connect_mixins.CfnUserPropsMixin.UserPhoneConfigProperty(
                after_contact_work_time_limit=123,
                auto_accept=False,
                desk_phone_number="deskPhoneNumber",
                persistent_connection=False,
                phone_type="phoneType"
            ),
            routing_profile_arn="routingProfileArn",
            security_profile_arns=["securityProfileArns"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            username="username",
            user_proficiencies=[connect_mixins.CfnUserPropsMixin.UserProficiencyProperty(
                attribute_name="attributeName",
                attribute_value="attributeValue",
                level=123
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::User``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ac895919ab5609ec24d17b15e30adb0001218a20bd2fa71e8a6639315ac794f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd41e5094eb5003250e11727c21bf851de5683f9eebdd1d7bd6a0ebe92fe2331)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d668e5761bc180f7d4df14a49ed2410c795bf970068c1855f55eecdf4e98b2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserMixinProps:
        return typing.cast(CfnUserMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserPropsMixin.UserIdentityInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "email": "email",
            "first_name": "firstName",
            "last_name": "lastName",
            "mobile": "mobile",
            "secondary_email": "secondaryEmail",
        },
    )
    class UserIdentityInfoProperty:
        def __init__(
            self,
            *,
            email: typing.Optional[builtins.str] = None,
            first_name: typing.Optional[builtins.str] = None,
            last_name: typing.Optional[builtins.str] = None,
            mobile: typing.Optional[builtins.str] = None,
            secondary_email: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the identity of a user.

            .. epigraph::

               For Amazon Connect instances that are created with the ``EXISTING_DIRECTORY`` identity management type, ``FirstName`` , ``LastName`` , and ``Email`` cannot be updated from within Amazon Connect because they are managed by the directory. > The ``FirstName`` and ``LastName`` length constraints below apply only to instances using SAML for identity management. If you are using Amazon Connect for identity management, the length constraints are 1-255 for ``FirstName`` , and 1-256 for ``LastName`` .

            :param email: The email address. If you are using SAML for identity management and include this parameter, an error is returned.
            :param first_name: The first name. This is required if you are using Amazon Connect or SAML for identity management. Inputs must be in Unicode Normalization Form C (NFC). Text containing characters in a non-NFC form (for example, decomposed characters or combining marks) are not accepted.
            :param last_name: The last name. This is required if you are using Amazon Connect or SAML for identity management. Inputs must be in Unicode Normalization Form C (NFC). Text containing characters in a non-NFC form (for example, decomposed characters or combining marks) are not accepted.
            :param mobile: The user's mobile number.
            :param secondary_email: The user's secondary email address. If you provide a secondary email, the user receives email notifications -- other than password reset notifications -- to this email address instead of to their primary email address. *Pattern* : ``(?=^.{0,265}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                user_identity_info_property = connect_mixins.CfnUserPropsMixin.UserIdentityInfoProperty(
                    email="email",
                    first_name="firstName",
                    last_name="lastName",
                    mobile="mobile",
                    secondary_email="secondaryEmail"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a806844c3261a05d5432359d8a139d6a4042f72003dd4f8dfe1f43ea1ea69a2)
                check_type(argname="argument email", value=email, expected_type=type_hints["email"])
                check_type(argname="argument first_name", value=first_name, expected_type=type_hints["first_name"])
                check_type(argname="argument last_name", value=last_name, expected_type=type_hints["last_name"])
                check_type(argname="argument mobile", value=mobile, expected_type=type_hints["mobile"])
                check_type(argname="argument secondary_email", value=secondary_email, expected_type=type_hints["secondary_email"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email is not None:
                self._values["email"] = email
            if first_name is not None:
                self._values["first_name"] = first_name
            if last_name is not None:
                self._values["last_name"] = last_name
            if mobile is not None:
                self._values["mobile"] = mobile
            if secondary_email is not None:
                self._values["secondary_email"] = secondary_email

        @builtins.property
        def email(self) -> typing.Optional[builtins.str]:
            '''The email address.

            If you are using SAML for identity management and include this parameter, an error is returned.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-email
            '''
            result = self._values.get("email")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def first_name(self) -> typing.Optional[builtins.str]:
            '''The first name.

            This is required if you are using Amazon Connect or SAML for identity management. Inputs must be in Unicode Normalization Form C (NFC). Text containing characters in a non-NFC form (for example, decomposed characters or combining marks) are not accepted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-firstname
            '''
            result = self._values.get("first_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_name(self) -> typing.Optional[builtins.str]:
            '''The last name.

            This is required if you are using Amazon Connect or SAML for identity management. Inputs must be in Unicode Normalization Form C (NFC). Text containing characters in a non-NFC form (for example, decomposed characters or combining marks) are not accepted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-lastname
            '''
            result = self._values.get("last_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mobile(self) -> typing.Optional[builtins.str]:
            '''The user's mobile number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-mobile
            '''
            result = self._values.get("mobile")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secondary_email(self) -> typing.Optional[builtins.str]:
            '''The user's secondary email address.

            If you provide a secondary email, the user receives email notifications -- other than password reset notifications -- to this email address instead of to their primary email address.

            *Pattern* : ``(?=^.{0,265}$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,63}``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-useridentityinfo.html#cfn-connect-user-useridentityinfo-secondaryemail
            '''
            result = self._values.get("secondary_email")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserIdentityInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserPropsMixin.UserPhoneConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "after_contact_work_time_limit": "afterContactWorkTimeLimit",
            "auto_accept": "autoAccept",
            "desk_phone_number": "deskPhoneNumber",
            "persistent_connection": "persistentConnection",
            "phone_type": "phoneType",
        },
    )
    class UserPhoneConfigProperty:
        def __init__(
            self,
            *,
            after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
            auto_accept: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            desk_phone_number: typing.Optional[builtins.str] = None,
            persistent_connection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            phone_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the phone configuration settings for a user.

            :param after_contact_work_time_limit: The After Call Work (ACW) timeout setting, in seconds. This parameter has a minimum value of 0 and a maximum value of 2,000,000 seconds (24 days). Enter 0 if you don't want to allocate a specific amount of ACW time. It essentially means an indefinite amount of time. When the conversation ends, ACW starts; the agent must choose Close contact to end ACW. .. epigraph:: When returned by a ``SearchUsers`` call, ``AfterContactWorkTimeLimit`` is returned in milliseconds.
            :param auto_accept: The Auto accept setting.
            :param desk_phone_number: The phone number for the user's desk phone.
            :param persistent_connection: The persistent connection setting for the user.
            :param phone_type: The phone type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                user_phone_config_property = connect_mixins.CfnUserPropsMixin.UserPhoneConfigProperty(
                    after_contact_work_time_limit=123,
                    auto_accept=False,
                    desk_phone_number="deskPhoneNumber",
                    persistent_connection=False,
                    phone_type="phoneType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59355ef26c844c31f4376c354ec6a8e9434e7a27298937ce9efe6a9f198e816f)
                check_type(argname="argument after_contact_work_time_limit", value=after_contact_work_time_limit, expected_type=type_hints["after_contact_work_time_limit"])
                check_type(argname="argument auto_accept", value=auto_accept, expected_type=type_hints["auto_accept"])
                check_type(argname="argument desk_phone_number", value=desk_phone_number, expected_type=type_hints["desk_phone_number"])
                check_type(argname="argument persistent_connection", value=persistent_connection, expected_type=type_hints["persistent_connection"])
                check_type(argname="argument phone_type", value=phone_type, expected_type=type_hints["phone_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if after_contact_work_time_limit is not None:
                self._values["after_contact_work_time_limit"] = after_contact_work_time_limit
            if auto_accept is not None:
                self._values["auto_accept"] = auto_accept
            if desk_phone_number is not None:
                self._values["desk_phone_number"] = desk_phone_number
            if persistent_connection is not None:
                self._values["persistent_connection"] = persistent_connection
            if phone_type is not None:
                self._values["phone_type"] = phone_type

        @builtins.property
        def after_contact_work_time_limit(self) -> typing.Optional[jsii.Number]:
            '''The After Call Work (ACW) timeout setting, in seconds.

            This parameter has a minimum value of 0 and a maximum value of 2,000,000 seconds (24 days). Enter 0 if you don't want to allocate a specific amount of ACW time. It essentially means an indefinite amount of time. When the conversation ends, ACW starts; the agent must choose Close contact to end ACW.
            .. epigraph::

               When returned by a ``SearchUsers`` call, ``AfterContactWorkTimeLimit`` is returned in milliseconds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-aftercontactworktimelimit
            '''
            result = self._values.get("after_contact_work_time_limit")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def auto_accept(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The Auto accept setting.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-autoaccept
            '''
            result = self._values.get("auto_accept")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def desk_phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number for the user's desk phone.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-deskphonenumber
            '''
            result = self._values.get("desk_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def persistent_connection(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The persistent connection setting for the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-persistentconnection
            '''
            result = self._values.get("persistent_connection")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def phone_type(self) -> typing.Optional[builtins.str]:
            '''The phone type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userphoneconfig.html#cfn-connect-user-userphoneconfig-phonetype
            '''
            result = self._values.get("phone_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserPhoneConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnUserPropsMixin.UserProficiencyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_value": "attributeValue",
            "level": "level",
        },
    )
    class UserProficiencyProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            attribute_value: typing.Optional[builtins.str] = None,
            level: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''.. epigraph::

   A predefined attribute must be created before using ``UserProficiencies`` in the Cloudformation *User* template.

            For more information, see `Predefined attributes <https://docs.aws.amazon.com/connect/latest/adminguide/predefined-attributes.html>`_ .

            Proficiency of a user.

            :param attribute_name: The name of user’s proficiency. You must use a predefined attribute name that is present in the Amazon Connect instance.
            :param attribute_value: The value of user’s proficiency. You must use a predefined attribute value that is present in the Amazon Connect instance.
            :param level: The level of the proficiency. The valid values are 1, 2, 3, 4 and 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userproficiency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
                
                user_proficiency_property = connect_mixins.CfnUserPropsMixin.UserProficiencyProperty(
                    attribute_name="attributeName",
                    attribute_value="attributeValue",
                    level=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5005c7eecec31b3d3a332f97200f7063d00557f0440005d963522d01779ebdc)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_value", value=attribute_value, expected_type=type_hints["attribute_value"])
                check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if attribute_value is not None:
                self._values["attribute_value"] = attribute_value
            if level is not None:
                self._values["level"] = level

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''The name of user’s proficiency.

            You must use a predefined attribute name that is present in the Amazon Connect instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userproficiency.html#cfn-connect-user-userproficiency-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_value(self) -> typing.Optional[builtins.str]:
            '''The value of user’s proficiency.

            You must use a predefined attribute value that is present in the Amazon Connect instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userproficiency.html#cfn-connect-user-userproficiency-attributevalue
            '''
            result = self._values.get("attribute_value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def level(self) -> typing.Optional[jsii.Number]:
            '''The level of the proficiency.

            The valid values are 1, 2, 3, 4 and 5.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connect-user-userproficiency.html#cfn-connect-user-userproficiency-level
            '''
            result = self._values.get("level")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProficiencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnViewMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "tags": "tags",
        "template": "template",
    },
)
class CfnViewMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template: typing.Any = None,
    ) -> None:
        '''Properties for CfnViewPropsMixin.

        :param actions: A list of actions possible from the view.
        :param description: The description of the view.
        :param instance_arn: The Amazon Resource Name (ARN) of the instance.
        :param name: The name of the view.
        :param tags: The tags associated with the view resource (not specific to view version).
        :param template: The view template representing the structure of the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            # template: Any
            
            cfn_view_mixin_props = connect_mixins.CfnViewMixinProps(
                actions=["actions"],
                description="description",
                instance_arn="instanceArn",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template=template
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18f523fffe05d1b1a1aca5533b511f70aa3ac3ce4e2f194a5c52d1f6b72d1844)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of actions possible from the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html#cfn-connect-view-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html#cfn-connect-view-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html#cfn-connect-view-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html#cfn-connect-view-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags associated with the view resource (not specific to view version).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html#cfn-connect-view-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def template(self) -> typing.Any:
        '''The view template representing the structure of the view.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html#cfn-connect-view-template
        '''
        result = self._values.get("template")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnViewMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnViewPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnViewPropsMixin",
):
    '''Creates a customer-managed view in the published state within the specified instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-view.html
    :cloudformationResource: AWS::Connect::View
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        # template: Any
        
        cfn_view_props_mixin = connect_mixins.CfnViewPropsMixin(connect_mixins.CfnViewMixinProps(
            actions=["actions"],
            description="description",
            instance_arn="instanceArn",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template=template
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnViewMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::View``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3a6c27af462ccfe0d263ae79292a609408167a24251171157f892b0b1f10e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb2c0a835fa139cda25516eeee3b68d4d271971182bb4d177143d8f638bc170e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dfc3c59224aa32cddf7ae4c81d215c89509bc6644289c4d4fcfe7f7cc591a76)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnViewMixinProps:
        return typing.cast(CfnViewMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnViewVersionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "version_description": "versionDescription",
        "view_arn": "viewArn",
        "view_content_sha256": "viewContentSha256",
    },
)
class CfnViewVersionMixinProps:
    def __init__(
        self,
        *,
        version_description: typing.Optional[builtins.str] = None,
        view_arn: typing.Optional[builtins.str] = None,
        view_content_sha256: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnViewVersionPropsMixin.

        :param version_description: The description of the view version.
        :param view_arn: The unqualified Amazon Resource Name (ARN) of the view. For example: ``arn:<partition>:connect:<region>:<accountId>:instance/00000000-0000-0000-0000-000000000000/view/00000000-0000-0000-0000-000000000000``
        :param view_content_sha256: Indicates the checksum value of the latest published view content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-viewversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
            
            cfn_view_version_mixin_props = connect_mixins.CfnViewVersionMixinProps(
                version_description="versionDescription",
                view_arn="viewArn",
                view_content_sha256="viewContentSha256"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7887539e2ba635d3573fa00ddd30c8c3a64b135711bd09827a8a63bd20cd9131)
            check_type(argname="argument version_description", value=version_description, expected_type=type_hints["version_description"])
            check_type(argname="argument view_arn", value=view_arn, expected_type=type_hints["view_arn"])
            check_type(argname="argument view_content_sha256", value=view_content_sha256, expected_type=type_hints["view_content_sha256"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if version_description is not None:
            self._values["version_description"] = version_description
        if view_arn is not None:
            self._values["view_arn"] = view_arn
        if view_content_sha256 is not None:
            self._values["view_content_sha256"] = view_content_sha256

    @builtins.property
    def version_description(self) -> typing.Optional[builtins.str]:
        '''The description of the view version.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-viewversion.html#cfn-connect-viewversion-versiondescription
        '''
        result = self._values.get("version_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view_arn(self) -> typing.Optional[builtins.str]:
        '''The unqualified Amazon Resource Name (ARN) of the view.

        For example:

        ``arn:<partition>:connect:<region>:<accountId>:instance/00000000-0000-0000-0000-000000000000/view/00000000-0000-0000-0000-000000000000``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-viewversion.html#cfn-connect-viewversion-viewarn
        '''
        result = self._values.get("view_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def view_content_sha256(self) -> typing.Optional[builtins.str]:
        '''Indicates the checksum value of the latest published view content.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-viewversion.html#cfn-connect-viewversion-viewcontentsha256
        '''
        result = self._values.get("view_content_sha256")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnViewVersionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnViewVersionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_connect.mixins.CfnViewVersionPropsMixin",
):
    '''Creates a version for the specified customer-managed view within the specified instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connect-viewversion.html
    :cloudformationResource: AWS::Connect::ViewVersion
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_connect import mixins as connect_mixins
        
        cfn_view_version_props_mixin = connect_mixins.CfnViewVersionPropsMixin(connect_mixins.CfnViewVersionMixinProps(
            version_description="versionDescription",
            view_arn="viewArn",
            view_content_sha256="viewContentSha256"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnViewVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Connect::ViewVersion``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0b77ca0a940ebdbac2d94fec01efdc693c0761e3e2b573086606f295375b14c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5eed45c6b649031d8a8457258d6ebb9ca6783db9f0f508964f9345a49a831e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8371be47fdea0ede98f102d126902d48061ab7de97d1a1005845622a45d17ba8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnViewVersionMixinProps:
        return typing.cast(CfnViewVersionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAgentStatusMixinProps",
    "CfnAgentStatusPropsMixin",
    "CfnApprovedOriginMixinProps",
    "CfnApprovedOriginPropsMixin",
    "CfnContactFlowMixinProps",
    "CfnContactFlowModuleMixinProps",
    "CfnContactFlowModulePropsMixin",
    "CfnContactFlowPropsMixin",
    "CfnContactFlowVersionMixinProps",
    "CfnContactFlowVersionPropsMixin",
    "CfnDataTableAttributeMixinProps",
    "CfnDataTableAttributePropsMixin",
    "CfnDataTableMixinProps",
    "CfnDataTablePropsMixin",
    "CfnEmailAddressMixinProps",
    "CfnEmailAddressPropsMixin",
    "CfnEvaluationFormMixinProps",
    "CfnEvaluationFormPropsMixin",
    "CfnHoursOfOperationMixinProps",
    "CfnHoursOfOperationPropsMixin",
    "CfnInstanceAmazonConnectFlowLogs",
    "CfnInstanceLogsMixin",
    "CfnInstanceMixinProps",
    "CfnInstancePropsMixin",
    "CfnInstanceStorageConfigMixinProps",
    "CfnInstanceStorageConfigPropsMixin",
    "CfnIntegrationAssociationMixinProps",
    "CfnIntegrationAssociationPropsMixin",
    "CfnPhoneNumberMixinProps",
    "CfnPhoneNumberPropsMixin",
    "CfnPredefinedAttributeMixinProps",
    "CfnPredefinedAttributePropsMixin",
    "CfnPromptMixinProps",
    "CfnPromptPropsMixin",
    "CfnQueueMixinProps",
    "CfnQueuePropsMixin",
    "CfnQuickConnectMixinProps",
    "CfnQuickConnectPropsMixin",
    "CfnRoutingProfileMixinProps",
    "CfnRoutingProfilePropsMixin",
    "CfnRuleMixinProps",
    "CfnRulePropsMixin",
    "CfnSecurityKeyMixinProps",
    "CfnSecurityKeyPropsMixin",
    "CfnSecurityProfileMixinProps",
    "CfnSecurityProfilePropsMixin",
    "CfnTaskTemplateMixinProps",
    "CfnTaskTemplatePropsMixin",
    "CfnTrafficDistributionGroupMixinProps",
    "CfnTrafficDistributionGroupPropsMixin",
    "CfnUserHierarchyGroupMixinProps",
    "CfnUserHierarchyGroupPropsMixin",
    "CfnUserHierarchyStructureMixinProps",
    "CfnUserHierarchyStructurePropsMixin",
    "CfnUserMixinProps",
    "CfnUserPropsMixin",
    "CfnViewMixinProps",
    "CfnViewPropsMixin",
    "CfnViewVersionMixinProps",
    "CfnViewVersionPropsMixin",
]

publication.publish()

def _typecheckingstub__ea87d5b9a3520e3997f9bdcbdb5f1a1985957369a1ded042005be20b5ac83975(
    *,
    description: typing.Optional[builtins.str] = None,
    display_order: typing.Optional[jsii.Number] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    reset_order_number: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94da73055421bbe8d6dc80e2ddc486d769afef107b48f9e8b31dec21710c1c8(
    props: typing.Union[CfnAgentStatusMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94bbb605322f13161516a5cc98d30baaa6cc215456eab587d6eb0a4bbf431d08(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818ffdc8dcfafcab85a92cb412f67a0c7a8d2c05d64d9a4d713b3501790fdccd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a2d0c80425bb697834f55c94edf804ecf51e0e5d0ac9d126c8680082b69c51(
    *,
    instance_id: typing.Optional[builtins.str] = None,
    origin: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae73093cb19dd7adfdbd99349842306d8f5ebecc58c523e3ecef0aabee2ec46(
    props: typing.Union[CfnApprovedOriginMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9107fd6e8213d4adfa090cf2790928070adbf6ea333e0fb94dd1443613b51e4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1d44d18ff3cf050d4adfc3a887ffc2d6bb373063ce2963d7944a91bae5c483f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41759aacb7bb794ee58e68bdfb26a185f76b460decaab3039d0bbeb3441deb14(
    *,
    content: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e09de24bff9dd984d2843d8fe81291715576b5e5fe7733a182bf329f73fbf8(
    *,
    content: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856b04157f23dca41234f30f2a48a49efbd1917305fa14957e78937b4f3da23f(
    props: typing.Union[CfnContactFlowModuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c5407498e15accd0afcba452b2e107ee1355b6f433eba3e9a7675f79eea99a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c15af3a811f191acde3a0a847036ec37933b825096d531db66bfc21af3bcfb8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb860e205ffae32cda0499e7e2480d6e59f1fc08932f24c8c0c909369db1e72(
    props: typing.Union[CfnContactFlowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0571c9f7340f88b0f867862a3fddc44bedb43f92f4b9d587c06b0d01faa4c03f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2ba308e10303a206edc42f7e05118b80d357e8b3704dc85835a3f897a7b8e5a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4d88913c68a3331275d7304dfb60c2fb634dce2ca6f40afc61850e4187a38f(
    *,
    contact_flow_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48fc78b8d432b27e2b1b3a2439590d5500195880739b12108fdac35c8e3fcb34(
    props: typing.Union[CfnContactFlowVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e150925111c26d1d8b06149db34a3f1e19e99bbe27e4388a2e53a431501a0bba(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99d237675626041fb362c2c0d446abcc2364bf7ffd5ca7b818a2e3def41722c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284d49a335428429a1419a0e1912fa44ca1a18d86d912f39f94905a2bdb1e978(
    *,
    data_table_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    primary: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    validation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataTableAttributePropsMixin.ValidationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5cf6be2f3340bfaece66b9bdc8ed3d5670d11f05a0c240aa6bbf6967b28a88(
    props: typing.Union[CfnDataTableAttributeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c0ff5343398cd48c3f7f094586d676c3c7107b009deb2ca9dcb24b6d55f319(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6757f37e089bf9d085b24c5f6d51e4859f8e6167e1e9b560c082945b98935df(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8e521f54b6d88b5ee32cf529654278a28aa0360392319fd989f147340e6cad(
    *,
    strict: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__554a300ab85c6d2c38395a005f3111e85693158d83a62c449a44c1952e4f67b3(
    *,
    attribute: typing.Optional[builtins.str] = None,
    data_table: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d13337c88d4e88c1acb2a387d79e5a830e8efc9d99c48d3f33688c5915b313(
    *,
    enum: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataTableAttributePropsMixin.EnumProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    exclusive_maximum: typing.Optional[jsii.Number] = None,
    exclusive_minimum: typing.Optional[jsii.Number] = None,
    maximum: typing.Optional[jsii.Number] = None,
    max_length: typing.Optional[jsii.Number] = None,
    max_values: typing.Optional[jsii.Number] = None,
    minimum: typing.Optional[jsii.Number] = None,
    min_length: typing.Optional[jsii.Number] = None,
    min_values: typing.Optional[jsii.Number] = None,
    multiple_of: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6ff5f5f586e687f18973cf961e747c5f49ffab67f65f71cf2b29e3adef9087(
    *,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
    value_lock_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3daeafe37708f1eea8f6cb7b284f92614dda4403c5dc317ebfef29a1b4dfec3d(
    props: typing.Union[CfnDataTableMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ed11b1d4b0d10bce1f92972d6a04bb3f03be8cee16393770bcab08da7ca2927(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df1a4649af02f29698d3f882f3f8b7a20633aaa8485553edcfbb5834f67292a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f1a58e8beee0f65e84fe4f9689eda54e3f4634945e55ff4cda30601b2301e6(
    *,
    data_table: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333d0036ebf9196aac54461fc944192183701c4485bb4982caaebf0d9363ae7b(
    *,
    alias_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEmailAddressPropsMixin.AliasConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    email_address: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc5b683c4d4e0c4859b83a930537fd7f7db1ed3058d2d8844a2db90cc4b98bf2(
    props: typing.Union[CfnEmailAddressMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d4176ac3179bcbbfd5eea60c5891d84869764278dcc38737e92896a3076f983(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e735cd549c668955b733b37a9eb29b75a7110d1a3c187e1e45ff38a2251b870(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a3cb19a07a28971b989a7e63c3729fabba3fb08980f037205852dacf5fbec33(
    *,
    email_address_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__741d59b1f8ff8308e9793e7581026c1643be954ee87377493e259fabf972dcf7(
    *,
    auto_evaluation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.AutoEvaluationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormBaseItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    language_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormLanguageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scoring_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.ScoringStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormTargetConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ecf2cca2098b0182240ff981fa486afa1ba8122613906811842512b4af33f6(
    props: typing.Union[CfnEvaluationFormMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87acea13f1ca0569900470beacceed7711aa7d26c08c67cfe77e234412d9428b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bcf60337ba05daff300eb986b06f8a4cd10b350e30646e9fcebeb5070dcc36(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fef8bbf0c55eb4b3d298166f4b531564fa6b0f1f60d13f1fe2b23696976f94(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678457b89d206c0f98eb6a07687b6906c7df47b285a03cf47418fb3eb3e5a8d2(
    *,
    target_section: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d6eab10fb5ba01e9f9341bed34f4b5fbe70cf0aaa083ba286bce6f87579809(
    *,
    section: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fbc943951aeea6b57ec68919599f2ee796f4ce88186311e2cd73a25beb9de4a(
    *,
    expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a8a244223e0066b4a781c530a165a2f14acf2a76e962eaeb6253bab2fb5d807(
    *,
    operands: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionOperandProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    operator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380b8409fbde3191a6de09d7c1f3d7d7287c0f322711799c66779e0d8c83ead4(
    *,
    action: typing.Optional[builtins.str] = None,
    condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConditionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76e6958a1d309b95d0185a94d5f9a9a9f1544c74c696a59b5f01f5bcafe51e6(
    *,
    comparator: typing.Optional[builtins.str] = None,
    source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementSourceValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07405088fbad04d37acc0fd2e251407fd6a93c1a9395ef3144adc95710e0a36a(
    *,
    ref_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5524544ac0c995d807fbf32c810a11be5f2e2ff96a29aabe3370ed3e62b73ec0(
    *,
    ref_id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55db0b4fa12da4530f844e0e2c05aad9e53b5e87422a6294022465147fdf0ad(
    *,
    question: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormQuestionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    section: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormSectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae8a6ebd71bb4304d21e53c024d1ba425e25c989281ac07d1f98488300ca394e(
    *,
    form_language: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeb90133d764129efac6e4162540af82714ef9037fdd90cef1fea317b1b73b85(
    *,
    rule_category: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.MultiSelectQuestionRuleCategoryAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1870c0e6901b3a3c1410ccbbea461ec0879143c534cabdf71a3089a90b020a7(
    *,
    answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_option_ref_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0dd058600358960283f7f8943697287d6775157393c48e80e756e63353c22c9(
    *,
    ref_id: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7da1df8884df4bc93a61bbed26859f223ae9d1db4a8ce78ef36549f282097d2(
    *,
    automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    display_as: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dae32fe31e05073d0d27f79249546e709b771c758a5da5102449099b82759584(
    *,
    answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    property_value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.NumericQuestionPropertyValueAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad7f2ab1045f6a68ef08faccd738ae59f5badbe2fd0b02c15736fa8bed82a6ae(
    *,
    automatic_fail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    automatic_fail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_value: typing.Optional[jsii.Number] = None,
    min_value: typing.Optional[jsii.Number] = None,
    score: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb664a04aa51c540168b259d2013e559cdd46a7f2a16811f871406c98b0b3ca(
    *,
    automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_value: typing.Optional[jsii.Number] = None,
    min_value: typing.Optional[jsii.Number] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f07ebab658961b74162e3bf99a3a6b50e87497f6075fe1ad7de96c729f0454b6(
    *,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60011c01c9c884476d3f0bc32d78dbb6f0e244b358a140a19d0e130c8ee29452(
    *,
    enablement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemEnablementConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instructions: typing.Optional[builtins.str] = None,
    not_applicable_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    question_type: typing.Optional[builtins.str] = None,
    question_type_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormQuestionTypePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ref_id: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d0c10c451bd9906345fd25bde24ba0ba058ce36ff85480225fc0d41f7ae4a4(
    *,
    multi_select: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormMultiSelectQuestionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    numeric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormNumericQuestionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    single_select: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    text: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e02e8660f59c45996c30278920e8e901a052ded70fcf383aa214bb1bf4a4807(
    *,
    instructions: typing.Optional[builtins.str] = None,
    items: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormItemProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ref_id: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee54669b7aad28c0aca7d77599bd4d8a027ea8f7df44bfad63478e4b91102169(
    *,
    rule_category: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.SingleSelectQuestionRuleCategoryAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b15a5da33e2cc89a44939968f80922b9a8840e650b4baef882f06053209a9637(
    *,
    answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    default_option_ref_id: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a5c100d1b31f46f3c94798ff520248d8a5d2697da096cf72a26581450128ff(
    *,
    automatic_fail: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    automatic_fail_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.AutomaticFailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ref_id: typing.Optional[builtins.str] = None,
    score: typing.Optional[jsii.Number] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99591f4b221d52fd992ea091e13eb9b0b814737e38aa313619e4f5386274f161(
    *,
    automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    display_as: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormSingleSelectQuestionOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc750340d378de9f9ea6bfd9096b4023bd09128e3dabedc11c2f1f0fd672ad3(
    *,
    contact_interaction_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85964724dd0591b615e6e23a435e93ca12d64e59ba11c8ad1936660a72a90e3(
    *,
    answer_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormQuestionAutomationAnswerSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c45024df85ab30660109d97088bdfe33658214e2ca0b8d00a1c9448f3d47d350(
    *,
    automation: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnEvaluationFormPropsMixin.EvaluationFormTextQuestionAutomationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa6b190bd17cd9731062798a98c48c465526742485c8603effcd5c1bca0a19a(
    *,
    category: typing.Optional[builtins.str] = None,
    condition: typing.Optional[builtins.str] = None,
    option_ref_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f8857fe52cd33ed7be2916236ce779e89a4f895d4b62df11455f82cae80818(
    *,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac6a9ec50b96f9eea9eda688062bb92565562ef8433be01496ab5f343a3a3fa(
    *,
    mode: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5527a748c7efd5f3e38660a02dc4a52f540dec1d50fdd7b2c3d695ff0e670dc(
    *,
    category: typing.Optional[builtins.str] = None,
    condition: typing.Optional[builtins.str] = None,
    option_ref_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e1f49dfdaae143884e84b0d07cb37c6d84c46913121fc1951b29611c585143a(
    *,
    config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.HoursOfOperationConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    hours_of_operation_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfc158957dfc051d6783578a7c4abb8c3adcb93752c450cce52b16637d6a48b(
    props: typing.Union[CfnHoursOfOperationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03556557bc7df6a7b2f7c80a484b1ee78f28b50b38f849c108b8c6e5feb1f6f7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f3a5b03a89fb5ab09f3727bdae5a6b365f5e695f8b66efba087533d78c0255(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e33b3645a9288ef8fd63991d2566cb47df5a1fc0b98399c7ca1cfed12dd38368(
    *,
    day: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.HoursOfOperationTimeSliceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cd95bed655e54b8d50feb6347b5e0a40e6b4343211f2fd3d0ec82dcfb96ea6(
    *,
    day: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    start_time: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.OverrideTimeSliceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7142e5d1c379872a023937f048f08602914be4773e511011a79a0c19612aa3d8(
    *,
    effective_from: typing.Optional[builtins.str] = None,
    effective_till: typing.Optional[builtins.str] = None,
    hours_of_operation_override_id: typing.Optional[builtins.str] = None,
    override_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnHoursOfOperationPropsMixin.HoursOfOperationOverrideConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    override_description: typing.Optional[builtins.str] = None,
    override_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c44bbac4d6a4774e2d0fbd02a0dbff1ef2150c5acc4ac687b4694e26ab1479(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90489a4984583c862b32af63f926e1992b834774d64540b3798a347da24c26e0(
    *,
    hours: typing.Optional[jsii.Number] = None,
    minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f524ccabc53801fb94975d482b7fb463124eafc4ebc48d654cc483de43692a36(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cbfb8169091793561b0df8b00000e4d9789d334697519c2e5aa85a2f3db6c86(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281d7ec173b2cc2ed2c930ba3c1422994f3ed06b15e2ba86daed5a450ab57641(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__002079279089e239349300b2d0a5903bac7ff1cab918690857c88e0aa1736826(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c6a4401f1403f580f5c334f43bdc35c02991656897c5d9e7fcc1e7e2454623(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__283f9ad56fd54ee160928c8754f580036fea700d360077b5a1d81ad66d8622c7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81d555e5cc0a05587e5cd9ae0866bc70ec9582678ae52f139da50eb3936166e(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstancePropsMixin.AttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    directory_id: typing.Optional[builtins.str] = None,
    identity_management_type: typing.Optional[builtins.str] = None,
    instance_alias: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e89a33b79dad3c75d654636a9ed87967e6913593bd745b5aa201b6ccbfa2703(
    props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a5f6cae604e6ca38ccfb94dac8b06a4aa72b61788c359d829f06cdb40ef85de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1920d211b1ee24c1b0c3c112ea6f5773c0f9fbc74795ff2dffcc508ae7a1db25(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffe62479f9a266bee0c3989950e29ad208de7e4d516f97732e77d312875f48ec(
    *,
    auto_resolve_best_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    contactflow_logs: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    contact_lens: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    early_media: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enhanced_chat_monitoring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enhanced_contact_monitoring: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    high_volume_out_bound: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    inbound_calls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    multi_party_chat_conference: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    multi_party_conference: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    outbound_calls: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_custom_tts_voices: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49be8be49fc7e60bc6603c25a10b13bb9152432b01b00975bb9c7255a04a2647(
    *,
    instance_arn: typing.Optional[builtins.str] = None,
    kinesis_firehose_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceStorageConfigPropsMixin.KinesisFirehoseConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_stream_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceStorageConfigPropsMixin.KinesisStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_video_stream_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceStorageConfigPropsMixin.KinesisVideoStreamConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    s3_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceStorageConfigPropsMixin.S3ConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caed2c11b928c1ea98a54262d071e9af00f2658bea49ff2098900b320e9f10c7(
    props: typing.Union[CfnInstanceStorageConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13492084d545024a8c3532f3ae93cf9b0e7674d50ea89c2ce61f2e0ab70d307(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2592945ee9cd3b2ab27b6312c38695c34a8e4f6be93f94fd1539e9a538b961c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8a14003fb5038a988d306ec31fc28aea979735b3b815d4407327a564e094556(
    *,
    encryption_type: typing.Optional[builtins.str] = None,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6d3410c16e53dd14a6ba32c400347efbcb2d1d668ab0a1ef58eec1debc0b87(
    *,
    firehose_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7378e4d0364b03e9a42f2978c8e38e6d7f3e426a050dfb5cbb726b4e1ed7f6d4(
    *,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abcf8b63206f586fb8d9d21908f64c252929d1059c89f453593a76fac966957(
    *,
    encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    prefix: typing.Optional[builtins.str] = None,
    retention_period_hours: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b19039f27bc824feabc24feb7d612741db9d231423b3843a87346ecbd672ee2(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    bucket_prefix: typing.Optional[builtins.str] = None,
    encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceStorageConfigPropsMixin.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d6234f1b8cd3382d0829ce424ec867997a2292ed8c50e173d838fc50bf0e8a(
    *,
    instance_id: typing.Optional[builtins.str] = None,
    integration_arn: typing.Optional[builtins.str] = None,
    integration_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326d8daff01b4f6af2f10cff06807155fef39148dff17e600b94bc2189c0ca0d(
    props: typing.Union[CfnIntegrationAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4fd4046df6275b2a93e573885bcc436a5f6c916e2188e965d61c1d4656fc0fc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c7f6023e54366affb403306667930bd68d77e5a3e9bdc36a84547d7da3d084(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e05114daef5981fdb19b4b5d2d306c934b15a5bee6ae8e31e3846be5cf31ab29(
    *,
    country_code: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    source_phone_number_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69682a1a0ee9423911b1548ba54a4b551074037b38c3383ec9cc17604238ab5a(
    props: typing.Union[CfnPhoneNumberMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__762d1ca975a679483e492982fc3ba458893cc127472f5f75da965a13b34719d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7959b9d200821617dd17e71181bf15303211acb075e997f1766d6202122599ac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22af6c1aaf951525be21f8474aa83609b5b1c40d6741c38a433420528cd827c4(
    *,
    attribute_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPredefinedAttributePropsMixin.AttributeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    purposes: typing.Optional[typing.Sequence[builtins.str]] = None,
    values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPredefinedAttributePropsMixin.ValuesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50bee6780b5b34043175433cdeada2df6caba4f07908853822e64b95a5cb1804(
    props: typing.Union[CfnPredefinedAttributeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d5e76c2a25cdfb82b92cff7bc7ce41d8d22ec3d227c8aab2d9dd2f90954930(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__714839b7bf128b53357fd7213541c87025918720ecc9fbe4726a6e15e3ff334a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b67c47cbca611d28ef23f7b234081488133a8108d0fc74197b0b93bb0d5cb77a(
    *,
    enable_value_validation_on_association: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    is_read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5608dd66bdaad22d2338c6bd4c9964e499f681aab7e2e0daaae17b22f70d0f(
    *,
    string_list: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4098b1cda862652bff9e159070722b5d0832330a97be0763f0aa3f2c325508c5(
    *,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    s3_uri: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aafbe36e72a86a8b3b7fd62a16c3e80c73d11b38254963e371ecc77760ea227f(
    props: typing.Union[CfnPromptMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6dafe59880cb651cacb6f796a7aec73ee7cc98e3d798d4bb50b30d1d1e52f14(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92da6224e86699311dc3ff5e77be33c3f03201ea468d2886335d74252ce35ada(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2ee9c47eb4e64a55a58d6b1e31a2b775f04cc55c2818fa386143c8ed555c33a(
    *,
    description: typing.Optional[builtins.str] = None,
    hours_of_operation_arn: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    max_contacts: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    outbound_caller_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.OutboundCallerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outbound_email_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQueuePropsMixin.OutboundEmailConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    quick_connect_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46b62bedf99e60fb0a5c1e7859b5a2ac251a768a701cf76dc622c9b4e64cb7be(
    props: typing.Union[CfnQueueMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5661c6ff214de690bc733dd53e2a4b68938155dd05eedf22306075b928e38920(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b1d57a18285983ab02b162630d50a7c1ac03335e33544cb1ba899d51b8345d3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b805fc08c1922ddf61c172b2134a5e1c8c836b0d2d482e61c619c4af41f4e3b(
    *,
    outbound_caller_id_name: typing.Optional[builtins.str] = None,
    outbound_caller_id_number_arn: typing.Optional[builtins.str] = None,
    outbound_flow_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60dfc236da5b03bd69d7949f5be5303791262a120076a0ce5fa611a5b537733(
    *,
    outbound_email_address_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e6358f65464ec035e10d81ad457b17a1b5469b32917915fb6441eb14dcfa65(
    *,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    quick_connect_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickConnectPropsMixin.QuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa26570c7730135267b75206428c37c384cc96240e79fffe84267bb57ec94027(
    props: typing.Union[CfnQuickConnectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1079c3745993e8134d80dfb0dca662c5973630c46ba739184c498ac018af5f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31762183ad741337b0c06d64bf5c62c17c284e63871078a0274191331dab743(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__191f6b3e5b6e04ee28533b8cf9547fa9160344b482901b9e26aff925ccdd23b3(
    *,
    phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c80250e7ce579fcded6a27e608e519a0820c2f51996660b6268c21337718c8(
    *,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    queue_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3484d15311805a5c3571ca053fc3eb5dcc4a057a4e3f616915beb10d3119c5b(
    *,
    phone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickConnectPropsMixin.PhoneNumberQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    queue_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickConnectPropsMixin.QueueQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    quick_connect_type: typing.Optional[builtins.str] = None,
    user_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnQuickConnectPropsMixin.UserQuickConnectConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0f26beb30eb410d21be62ce83243ec0c0869344d2bdfec1544d8037a24c9126(
    *,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    user_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52d8fc6715ebef6888e1788df00bd48b9de2d35e6e5b4e25d5c266e47e634286(
    *,
    agent_availability_timer: typing.Optional[builtins.str] = None,
    default_outbound_queue_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    manual_assignment_queue_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutingProfilePropsMixin.RoutingProfileManualAssignmentQueueConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    media_concurrencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutingProfilePropsMixin.MediaConcurrencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    queue_configs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutingProfilePropsMixin.RoutingProfileQueueConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a3cca3d6dc4feeb2de2b6df1e78847ebee6f591bf0dec7e143ce91de2cc6d3(
    props: typing.Union[CfnRoutingProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd063ef9cf3223322923db5eb378e731ea7c7e2f13a7e9f40e00bcdb30dcc0ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1f22ded1cb974e1f8ecd129ad632306e51af40622e69343eaabf3019b90474(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1767ecb7fb7c7a037524035bf5990d0d9f520fa77a7d79ffc14cb6f65d7e6ea(
    *,
    behavior_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd115c31c6efd9516419cac7f6c0ea9a88650756ab71b029e75e06af156ca49e(
    *,
    channel: typing.Optional[builtins.str] = None,
    concurrency: typing.Optional[jsii.Number] = None,
    cross_channel_behavior: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutingProfilePropsMixin.CrossChannelBehaviorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a26af61ae429d1eaa98a76439f321eca5831c7f100b47d023eb1f8bbbb8a960a(
    *,
    queue_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460e3ffd2f931c382dcbb1dc7336c3581d480ad7b5b30fdff6be76113c352daf(
    *,
    delay: typing.Optional[jsii.Number] = None,
    priority: typing.Optional[jsii.Number] = None,
    queue_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRoutingProfilePropsMixin.RoutingProfileQueueReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73235db8dea6526e26ebe89a54e5f6943f990d50ed847f6f4779687cacd50d1f(
    *,
    channel: typing.Optional[builtins.str] = None,
    queue_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45290cb986518bf26ef612edf30f89d238a47e8b38d0ecc3f53461d7e0b6bf01(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.ActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    function: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    publish_status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    trigger_event_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.RuleTriggerEventSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c55e92831284bf7ec63e128e53f1430c9623bbb2bb69cc617409e295115bb7aa(
    props: typing.Union[CfnRuleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__845b3a39a7a9d75fbbaa0b29aadffb0a0b51838dd5e5e943b61caf7ac9a339ef(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b5f6b06bce6ecbf1d59d8f93885db0c9735633e9b27ee1b842ab55fa4561042(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7933b63d1220183bcaf569fc44f15da19cbce19ff7c14a114b275c9e298ac18(
    *,
    assign_contact_category_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    create_case_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.CreateCaseActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    end_associated_tasks_actions: typing.Optional[typing.Union[typing.Sequence[typing.Any], _aws_cdk_ceddda9d.IResolvable]] = None,
    event_bridge_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.EventBridgeActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    send_notification_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.SendNotificationActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    submit_auto_evaluation_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.SubmitAutoEvaluationActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    task_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.TaskActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    update_case_actions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.UpdateCaseActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af10753c689192700f95c6de519951fe3ffc589638b8241bc85ae23c2f0311b(
    *,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    template_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83cee4bc9047627089a42e5b8d718eb215d6e4ff84f3d84e7d1f1a5024932954(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca4f4db6ef266b638244212e51f9c99589cf5f543e928a1d60e11bd8dc1c5ce(
    *,
    id: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.FieldValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725dc24ab18352a277ba03517438ce0deb2604be8bed69f09c0a2099cd5df66a(
    *,
    boolean_value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    double_value: typing.Optional[jsii.Number] = None,
    empty_value: typing.Any = None,
    string_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685661a93ed658b0e1cad593aae9b097c1ae9691984bd2d651a619ff40d544cf(
    *,
    user_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_tags: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4bfd9c3e1210a0c032100188a9089e96585c49a29e58f2d2b544e4774e62619(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70d491880d95d3f26cd5a022fbeef1266b4c9302f402b08562ec4484fac61f0(
    *,
    event_source_name: typing.Optional[builtins.str] = None,
    integration_association_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a1391e60b81f17a6cd5dc212b91a93966e57a542965457cb52948d51b7419f(
    *,
    content: typing.Optional[builtins.str] = None,
    content_type: typing.Optional[builtins.str] = None,
    delivery_method: typing.Optional[builtins.str] = None,
    recipient: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.NotificationRecipientTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee3e2861ceea772eb80b0ebb32633583a0ae8d5fd662c39edc643b9f8386f01(
    *,
    evaluation_form_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d62de805df4fdff5f5837c8c4e9d9b97e0beaa813df631cbba95e8fb0095991(
    *,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.ReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523448360bca58d27a51d620dbcdd332b59f6eb98e756d85d4b785eff6e2aab7(
    *,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulePropsMixin.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a691082a031b56a67ddfcbbba4df7fe2310fb3012ba413a2d790791fa2065a9(
    *,
    instance_id: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55d832d4b8979677c58e4e60054fc177f8f1c745d9f8c7ad73c07b31a2d71b5a(
    props: typing.Union[CfnSecurityKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc8e15b985a2ff49f532bd9c83c596c94fa1eb2e7d2aa3d580901670810f892(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3173f8a09281de1ac5175f9007803d639f5e35d343af03fa344753c7c2fd8647(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8741bb5c41219d2c1a527ea8eeb43262286744d3b49203f9b8f54239d14d611a(
    *,
    allowed_access_control_hierarchy_group_id: typing.Optional[builtins.str] = None,
    allowed_access_control_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    applications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityProfilePropsMixin.ApplicationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    granular_access_control_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityProfilePropsMixin.GranularAccessControlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    hierarchy_restricted_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_profile_name: typing.Optional[builtins.str] = None,
    tag_restricted_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db9c0ab7fceae7e82f6cd38fd66d9d2ff1facb1ad03630a9f7b96135755b721(
    props: typing.Union[CfnSecurityProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c6f8078c97ae6678c700d3478ca7dbcb52860a75036387973a672393c6e4f4b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731a654d650f2d5e06044b1b926138faea9dd897644cc4515c758c887e695cc3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e350e330c9a978caa94b8096526a4fab2e32192a00da7c976967948da89ae619(
    *,
    application_permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9e504081e076390fdde648274bf823a9c98c6c2f8e4e445069efe3c7e7401e(
    *,
    primary_attribute_access_control_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityProfilePropsMixin.PrimaryAttributeAccessControlConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4b66ee1ee9161fea501ebd2604cb136ca7ff79f3bd08712caa3617e0c49b8f(
    *,
    data_table_access_control_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityProfilePropsMixin.DataTableAccessControlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86f9b0aa95d3409687f8645e81d33bb085cdfae6adfbb738e02c5cd1f0fb0ad0(
    *,
    primary_attribute_values: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSecurityProfilePropsMixin.PrimaryAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c341c3f92fe9661253958dbdd13ba1f855372de88a7a0719cb164cae4223b01(
    *,
    access_type: typing.Optional[builtins.str] = None,
    attribute_name: typing.Optional[builtins.str] = None,
    values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fffbb0723f3425ee0abb5a58cdc0eb6980e0f37a057f6339282db32cb3928f95(
    *,
    client_token: typing.Optional[builtins.str] = None,
    constraints: typing.Any = None,
    contact_flow_arn: typing.Optional[builtins.str] = None,
    defaults: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.DefaultFieldValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.FieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    self_assign_contact_flow_arn: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edd5b28ec4fd2a594ffb8a8e1f7ca35a6005d224466f664cfa93e14fc6c08b2c(
    props: typing.Union[CfnTaskTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5c2e67329c6b663bc5ee835621b867283f07a26a45b70e24d1935c67d032f0f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__425700ea564e1b8d83ba7ee24d00d41eb120f93ebcc28132eccee0d426ee8492(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c3d756aa44adcf1938b9028f9ed0ce6bb85b348388b2c0a41d5302b49828cd(
    *,
    invisible_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.InvisibleFieldInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    read_only_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.ReadOnlyFieldInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    required_fields: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.RequiredFieldInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640a0f7f8b2dc14bd603a5d3a3dded2c13a1d63d0c30a5e0873fd45f73dd7ce8(
    *,
    default_value: typing.Optional[builtins.str] = None,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bebf6090bd1b96e0e738185bbd17ac531398eb008e4fa4afce833793dc62861(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66d52b5df896b87e3bff67b3cea897fae5551f59f339998b98a1d138359178d2(
    *,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    single_select_options: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8961e1b4434aecef4dd770af578f72195b0710998cd87f8e519f8597b073b47d(
    *,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ffa9bfe62e583eae81b77013a630dbc1cf7dec35c4ce7efbaef756dbe4af419(
    *,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7c8fb0c8eb87e15701479f2f93243e5f9bee3f43bb23e7792cdb1655bb55f0(
    *,
    id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTaskTemplatePropsMixin.FieldIdentifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d11363e3b01378326a043d2ef1414ab7ba339453d9579003194d67df5123f86a(
    *,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3dd694b2b87268524857e2ec09362241db50b48b9b2aff03652767dc0d0ee82(
    props: typing.Union[CfnTrafficDistributionGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__120b783baec79bf0399d29ea94ef3928b4f08a592462630ccc6b350f4f1f257f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b96425e9fa1408b9f5c87c3c7d892dcb41c11062780d1081063d0b8d98dabf9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b83fd73ae5bba166ac452b4050780f3e4b6b0ca05f404362e040d4a8a48078(
    *,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_group_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680733510943706d81fdeb4265c63fb91b5105765312c45fdfe173d4ff2d4edd(
    props: typing.Union[CfnUserHierarchyGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86a62523ecf1d21f493826c831f3fbc97ba964a2d2b2d315b3e50183c8d66724(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac29ed3ff1d940eebd19380d4578f2f92b1eb8f63c7d293a893b4f8f50e5e123(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0303262d5d1b6ffd2599ad3ae7307fff1d0db0cdc484aac23db76a93484fed80(
    *,
    instance_arn: typing.Optional[builtins.str] = None,
    user_hierarchy_structure: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserHierarchyStructurePropsMixin.UserHierarchyStructureProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27bea220dc18416f5d2a822206d7a9c672debf2335b764672e8744fa7c192411(
    props: typing.Union[CfnUserHierarchyStructureMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b906a6ddf59ee363b57ccb7af361cb9fa32c9b36ca3841a0b848cc5eda553986(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2bf15c042cad6ff2ee813b9ff0e793a7c1872db9ebc5c644fba20775f4dc13(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__894dddf1a74864d0487df23149a2c90472705eae27af745a6634fb15bd15cbe6(
    *,
    hierarchy_level_arn: typing.Optional[builtins.str] = None,
    hierarchy_level_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63eccffd3a2ff99c082ae978132b9be73c667ee0e75140ea57174d1f3c6b423a(
    *,
    hierarchy_level_arn: typing.Optional[builtins.str] = None,
    hierarchy_level_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665f77eca2c33953ecb563963e5bd8523a0b4e7d61991d48c29ba99e7dfacd37(
    *,
    hierarchy_level_arn: typing.Optional[builtins.str] = None,
    hierarchy_level_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84f5e2c62bc09d2d63067d150de7954f63fc5cc9efd83bf2782030381280dd39(
    *,
    hierarchy_level_arn: typing.Optional[builtins.str] = None,
    hierarchy_level_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7fb4a1039c8d4aa9d8c76dad4a59e529f6f4fe1267220c8b937e41876b97b2(
    *,
    hierarchy_level_arn: typing.Optional[builtins.str] = None,
    hierarchy_level_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a41862f6dabdcbb7d82dda5669c9977f41eef4565ed6bcbb4f7592f3db7d2104(
    *,
    level_five: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserHierarchyStructurePropsMixin.LevelFiveProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    level_four: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserHierarchyStructurePropsMixin.LevelFourProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    level_one: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserHierarchyStructurePropsMixin.LevelOneProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    level_three: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserHierarchyStructurePropsMixin.LevelThreeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    level_two: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserHierarchyStructurePropsMixin.LevelTwoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8354d75e03f378bbba4eae38aad427a4b4fd927e2393bd1e7d9c6f2f713ec3ab(
    *,
    directory_user_id: typing.Optional[builtins.str] = None,
    hierarchy_group_arn: typing.Optional[builtins.str] = None,
    identity_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.UserIdentityInfoProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    phone_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.UserPhoneConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    routing_profile_arn: typing.Optional[builtins.str] = None,
    security_profile_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    username: typing.Optional[builtins.str] = None,
    user_proficiencies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.UserProficiencyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ac895919ab5609ec24d17b15e30adb0001218a20bd2fa71e8a6639315ac794f(
    props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd41e5094eb5003250e11727c21bf851de5683f9eebdd1d7bd6a0ebe92fe2331(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d668e5761bc180f7d4df14a49ed2410c795bf970068c1855f55eecdf4e98b2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a806844c3261a05d5432359d8a139d6a4042f72003dd4f8dfe1f43ea1ea69a2(
    *,
    email: typing.Optional[builtins.str] = None,
    first_name: typing.Optional[builtins.str] = None,
    last_name: typing.Optional[builtins.str] = None,
    mobile: typing.Optional[builtins.str] = None,
    secondary_email: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59355ef26c844c31f4376c354ec6a8e9434e7a27298937ce9efe6a9f198e816f(
    *,
    after_contact_work_time_limit: typing.Optional[jsii.Number] = None,
    auto_accept: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    desk_phone_number: typing.Optional[builtins.str] = None,
    persistent_connection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    phone_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5005c7eecec31b3d3a332f97200f7063d00557f0440005d963522d01779ebdc(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_value: typing.Optional[builtins.str] = None,
    level: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18f523fffe05d1b1a1aca5533b511f70aa3ac3ce4e2f194a5c52d1f6b72d1844(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3a6c27af462ccfe0d263ae79292a609408167a24251171157f892b0b1f10e5(
    props: typing.Union[CfnViewMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2c0a835fa139cda25516eeee3b68d4d271971182bb4d177143d8f638bc170e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dfc3c59224aa32cddf7ae4c81d215c89509bc6644289c4d4fcfe7f7cc591a76(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7887539e2ba635d3573fa00ddd30c8c3a64b135711bd09827a8a63bd20cd9131(
    *,
    version_description: typing.Optional[builtins.str] = None,
    view_arn: typing.Optional[builtins.str] = None,
    view_content_sha256: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0b77ca0a940ebdbac2d94fec01efdc693c0761e3e2b573086606f295375b14c(
    props: typing.Union[CfnViewVersionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5eed45c6b649031d8a8457258d6ebb9ca6783db9f0f508964f9345a49a831e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8371be47fdea0ede98f102d126902d48061ab7de97d1a1005845622a45d17ba8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
