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
    jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnAccessorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "accessor_type": "accessorType",
        "network_type": "networkType",
        "tags": "tags",
    },
)
class CfnAccessorMixinProps:
    def __init__(
        self,
        *,
        accessor_type: typing.Optional[builtins.str] = None,
        network_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessorPropsMixin.

        :param accessor_type: The type of the accessor. .. epigraph:: Currently, accessor type is restricted to ``BILLING_TOKEN`` .
        :param network_type: The blockchain network that the ``Accessor`` token is created for. .. epigraph:: We recommend using the appropriate ``networkType`` value for the blockchain network that you are creating the ``Accessor`` token for. You cannot use the value ``ETHEREUM_MAINNET_AND_GOERLI`` to specify a ``networkType`` for your Accessor token. The default value of ``ETHEREUM_MAINNET_AND_GOERLI`` is only applied: - when the ``CreateAccessor`` action does not set a ``networkType`` . - to all existing ``Accessor`` tokens that were created before the ``networkType`` property was introduced.
        :param tags: The tags assigned to the Accessor. For more information about tags, see `Tagging Resources <https://docs.aws.amazon.com/managed-blockchain/latest/ethereum-dev/tagging-resources.html>`_ in the *Amazon Managed Blockchain Ethereum Developer Guide* , or `Tagging Resources <https://docs.aws.amazon.com/managed-blockchain/latest/hyperledger-fabric-dev/tagging-resources.html>`_ in the *Amazon Managed Blockchain Hyperledger Fabric Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-accessor.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
            
            cfn_accessor_mixin_props = managedblockchain_mixins.CfnAccessorMixinProps(
                accessor_type="accessorType",
                network_type="networkType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9095f52471372b517d22ca9c66146a2a3e39ee9d24b585749dcc37e48aa36dab)
            check_type(argname="argument accessor_type", value=accessor_type, expected_type=type_hints["accessor_type"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if accessor_type is not None:
            self._values["accessor_type"] = accessor_type
        if network_type is not None:
            self._values["network_type"] = network_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def accessor_type(self) -> typing.Optional[builtins.str]:
        '''The type of the accessor.

        .. epigraph::

           Currently, accessor type is restricted to ``BILLING_TOKEN`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-accessor.html#cfn-managedblockchain-accessor-accessortype
        '''
        result = self._values.get("accessor_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The blockchain network that the ``Accessor`` token is created for.

        .. epigraph::

           We recommend using the appropriate ``networkType`` value for the blockchain network that you are creating the ``Accessor`` token for. You cannot use the value ``ETHEREUM_MAINNET_AND_GOERLI`` to specify a ``networkType`` for your Accessor token.

           The default value of ``ETHEREUM_MAINNET_AND_GOERLI`` is only applied:

           - when the ``CreateAccessor`` action does not set a ``networkType`` .
           - to all existing ``Accessor`` tokens that were created before the ``networkType`` property was introduced.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-accessor.html#cfn-managedblockchain-accessor-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags assigned to the Accessor.

        For more information about tags, see `Tagging Resources <https://docs.aws.amazon.com/managed-blockchain/latest/ethereum-dev/tagging-resources.html>`_ in the *Amazon Managed Blockchain Ethereum Developer Guide* , or `Tagging Resources <https://docs.aws.amazon.com/managed-blockchain/latest/hyperledger-fabric-dev/tagging-resources.html>`_ in the *Amazon Managed Blockchain Hyperledger Fabric Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-accessor.html#cfn-managedblockchain-accessor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnAccessorPropsMixin",
):
    '''Creates a new accessor for use with Amazon Managed Blockchain service that supports token based access.

    The accessor contains information required for token based access.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-accessor.html
    :cloudformationResource: AWS::ManagedBlockchain::Accessor
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
        
        cfn_accessor_props_mixin = managedblockchain_mixins.CfnAccessorPropsMixin(managedblockchain_mixins.CfnAccessorMixinProps(
            accessor_type="accessorType",
            network_type="networkType",
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
        props: typing.Union[CfnAccessorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ManagedBlockchain::Accessor``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb8174fa7d25f1d601827d6647f6e6202c44cba9e22b2da1153dec35b3fb6698)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66e241c996eda7a59bc5c7af09e9e561ab22d42281739b73fdba783833341c4b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33827a8568fe25107d74568bbb52fece7be4e8c977e68f58220aee673a043286)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessorMixinProps:
        return typing.cast(CfnAccessorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "invitation_id": "invitationId",
        "member_configuration": "memberConfiguration",
        "network_configuration": "networkConfiguration",
        "network_id": "networkId",
    },
)
class CfnMemberMixinProps:
    def __init__(
        self,
        *,
        invitation_id: typing.Optional[builtins.str] = None,
        member_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.MemberConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnMemberPropsMixin.

        :param invitation_id: The unique identifier of the invitation to join the network sent to the account that creates the member.
        :param member_configuration: Configuration properties of the member.
        :param network_configuration: Configuration properties of the network to which the member belongs.
        :param network_id: The unique identifier of the network to which the member belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
            
            cfn_member_mixin_props = managedblockchain_mixins.CfnMemberMixinProps(
                invitation_id="invitationId",
                member_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberConfigurationProperty(
                    description="description",
                    member_framework_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFrameworkConfigurationProperty(
                        member_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFabricConfigurationProperty(
                            admin_password="adminPassword",
                            admin_username="adminUsername"
                        )
                    ),
                    name="name"
                ),
                network_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkConfigurationProperty(
                    description="description",
                    framework="framework",
                    framework_version="frameworkVersion",
                    name="name",
                    network_framework_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty(
                        network_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFabricConfigurationProperty(
                            edition="edition"
                        )
                    ),
                    voting_policy=managedblockchain_mixins.CfnMemberPropsMixin.VotingPolicyProperty(
                        approval_threshold_policy=managedblockchain_mixins.CfnMemberPropsMixin.ApprovalThresholdPolicyProperty(
                            proposal_duration_in_hours=123,
                            threshold_comparator="thresholdComparator",
                            threshold_percentage=123
                        )
                    )
                ),
                network_id="networkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86e55600fed9cda6efada1e92c719646fa1a51148c013b1a4d4aea96f1226b98)
            check_type(argname="argument invitation_id", value=invitation_id, expected_type=type_hints["invitation_id"])
            check_type(argname="argument member_configuration", value=member_configuration, expected_type=type_hints["member_configuration"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if invitation_id is not None:
            self._values["invitation_id"] = invitation_id
        if member_configuration is not None:
            self._values["member_configuration"] = member_configuration
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if network_id is not None:
            self._values["network_id"] = network_id

    @builtins.property
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the invitation to join the network sent to the account that creates the member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-invitationid
        '''
        result = self._values.get("invitation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.MemberConfigurationProperty"]]:
        '''Configuration properties of the member.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-memberconfiguration
        '''
        result = self._values.get("member_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.MemberConfigurationProperty"]], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.NetworkConfigurationProperty"]]:
        '''Configuration properties of the network to which the member belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.NetworkConfigurationProperty"]], result)

    @builtins.property
    def network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the network to which the member belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkid
        '''
        result = self._values.get("network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnMemberPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin",
):
    '''Creates a member within a Managed Blockchain network.

    Applies only to Hyperledger Fabric.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html
    :cloudformationResource: AWS::ManagedBlockchain::Member
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
        
        cfn_member_props_mixin = managedblockchain_mixins.CfnMemberPropsMixin(managedblockchain_mixins.CfnMemberMixinProps(
            invitation_id="invitationId",
            member_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberConfigurationProperty(
                description="description",
                member_framework_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFrameworkConfigurationProperty(
                    member_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFabricConfigurationProperty(
                        admin_password="adminPassword",
                        admin_username="adminUsername"
                    )
                ),
                name="name"
            ),
            network_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkConfigurationProperty(
                description="description",
                framework="framework",
                framework_version="frameworkVersion",
                name="name",
                network_framework_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty(
                    network_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFabricConfigurationProperty(
                        edition="edition"
                    )
                ),
                voting_policy=managedblockchain_mixins.CfnMemberPropsMixin.VotingPolicyProperty(
                    approval_threshold_policy=managedblockchain_mixins.CfnMemberPropsMixin.ApprovalThresholdPolicyProperty(
                        proposal_duration_in_hours=123,
                        threshold_comparator="thresholdComparator",
                        threshold_percentage=123
                    )
                )
            ),
            network_id="networkId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnMemberMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ManagedBlockchain::Member``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__782579f858bce5b204f267c84c72d6122954ed5a8067abd93ed16890d377effe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ada91c3c090637e018197089ced05384365b4d37cd99eaa3d85044c646c495ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc70235676b3470e9e69865753f3b9673cd8b49b14674341dc9830c8f12b5fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnMemberMixinProps:
        return typing.cast(CfnMemberMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.ApprovalThresholdPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "proposal_duration_in_hours": "proposalDurationInHours",
            "threshold_comparator": "thresholdComparator",
            "threshold_percentage": "thresholdPercentage",
        },
    )
    class ApprovalThresholdPolicyProperty:
        def __init__(
            self,
            *,
            proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
            threshold_comparator: typing.Optional[builtins.str] = None,
            threshold_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A policy type that defines the voting rules for the network.

            The rules decide if a proposal is approved. Approval may be based on criteria such as the percentage of ``YES`` votes and the duration of the proposal. The policy applies to all proposals and is specified when the network is created.

            Applies only to Hyperledger Fabric.

            :param proposal_duration_in_hours: The duration from the time that a proposal is created until it expires. If members cast neither the required number of ``YES`` votes to approve the proposal nor the number of ``NO`` votes required to reject it before the duration expires, the proposal is ``EXPIRED`` and ``ProposalActions`` aren't carried out.
            :param threshold_comparator: Determines whether the vote percentage must be greater than the ``ThresholdPercentage`` or must be greater than or equal to the ``ThresholdPercentage`` to be approved.
            :param threshold_percentage: The percentage of votes among all members that must be ``YES`` for a proposal to be approved. For example, a ``ThresholdPercentage`` value of ``50`` indicates 50%. The ``ThresholdComparator`` determines the precise comparison. If a ``ThresholdPercentage`` value of ``50`` is specified on a network with 10 members, along with a ``ThresholdComparator`` value of ``GREATER_THAN`` , this indicates that 6 ``YES`` votes are required for the proposal to be approved.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                approval_threshold_policy_property = managedblockchain_mixins.CfnMemberPropsMixin.ApprovalThresholdPolicyProperty(
                    proposal_duration_in_hours=123,
                    threshold_comparator="thresholdComparator",
                    threshold_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c873e9c3b6f0301c10c348f20eef81bb362c52ff43f8946ab099f21c4208a4f)
                check_type(argname="argument proposal_duration_in_hours", value=proposal_duration_in_hours, expected_type=type_hints["proposal_duration_in_hours"])
                check_type(argname="argument threshold_comparator", value=threshold_comparator, expected_type=type_hints["threshold_comparator"])
                check_type(argname="argument threshold_percentage", value=threshold_percentage, expected_type=type_hints["threshold_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if proposal_duration_in_hours is not None:
                self._values["proposal_duration_in_hours"] = proposal_duration_in_hours
            if threshold_comparator is not None:
                self._values["threshold_comparator"] = threshold_comparator
            if threshold_percentage is not None:
                self._values["threshold_percentage"] = threshold_percentage

        @builtins.property
        def proposal_duration_in_hours(self) -> typing.Optional[jsii.Number]:
            '''The duration from the time that a proposal is created until it expires.

            If members cast neither the required number of ``YES`` votes to approve the proposal nor the number of ``NO`` votes required to reject it before the duration expires, the proposal is ``EXPIRED`` and ``ProposalActions`` aren't carried out.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-proposaldurationinhours
            '''
            result = self._values.get("proposal_duration_in_hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def threshold_comparator(self) -> typing.Optional[builtins.str]:
            '''Determines whether the vote percentage must be greater than the ``ThresholdPercentage`` or must be greater than or equal to the ``ThresholdPercentage`` to be approved.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-thresholdcomparator
            '''
            result = self._values.get("threshold_comparator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of votes among all members that must be ``YES`` for a proposal to be approved.

            For example, a ``ThresholdPercentage`` value of ``50`` indicates 50%. The ``ThresholdComparator`` determines the precise comparison. If a ``ThresholdPercentage`` value of ``50`` is specified on a network with 10 members, along with a ``ThresholdComparator`` value of ``GREATER_THAN`` , this indicates that 6 ``YES`` votes are required for the proposal to be approved.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-thresholdpercentage
            '''
            result = self._values.get("threshold_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApprovalThresholdPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.MemberConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "member_framework_configuration": "memberFrameworkConfiguration",
            "name": "name",
        },
    )
    class MemberConfigurationProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            member_framework_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.MemberFrameworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration properties of the member.

            Applies only to Hyperledger Fabric.

            :param description: An optional description of the member.
            :param member_framework_configuration: Configuration properties of the blockchain framework relevant to the member.
            :param name: The name of the member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                member_configuration_property = managedblockchain_mixins.CfnMemberPropsMixin.MemberConfigurationProperty(
                    description="description",
                    member_framework_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFrameworkConfigurationProperty(
                        member_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFabricConfigurationProperty(
                            admin_password="adminPassword",
                            admin_username="adminUsername"
                        )
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ac148603f30cf099b5a87cbb20123947c126e3bf54857857d50d2b428b3c131)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument member_framework_configuration", value=member_framework_configuration, expected_type=type_hints["member_framework_configuration"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if member_framework_configuration is not None:
                self._values["member_framework_configuration"] = member_framework_configuration
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''An optional description of the member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def member_framework_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.MemberFrameworkConfigurationProperty"]]:
            '''Configuration properties of the blockchain framework relevant to the member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-memberframeworkconfiguration
            '''
            result = self._values.get("member_framework_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.MemberFrameworkConfigurationProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the member.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.MemberFabricConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "admin_password": "adminPassword",
            "admin_username": "adminUsername",
        },
    )
    class MemberFabricConfigurationProperty:
        def __init__(
            self,
            *,
            admin_password: typing.Optional[builtins.str] = None,
            admin_username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network that is using the Hyperledger Fabric framework.

            :param admin_password: The password for the member's initial administrative user. The ``AdminPassword`` must be at least 8 characters long and no more than 32 characters. It must contain at least one uppercase letter, one lowercase letter, and one digit. It cannot have a single quotation mark (‘), a double quotation marks (“), a forward slash(/), a backward slash(),
            :param admin_username: The user name for the member's initial administrative user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                member_fabric_configuration_property = managedblockchain_mixins.CfnMemberPropsMixin.MemberFabricConfigurationProperty(
                    admin_password="adminPassword",
                    admin_username="adminUsername"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__46d772b1661616e564797722d59c5b2e526971408f4f1ab4934e27c2b107926b)
                check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
                check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if admin_password is not None:
                self._values["admin_password"] = admin_password
            if admin_username is not None:
                self._values["admin_username"] = admin_username

        @builtins.property
        def admin_password(self) -> typing.Optional[builtins.str]:
            '''The password for the member's initial administrative user.

            The ``AdminPassword`` must be at least 8 characters long and no more than 32 characters. It must contain at least one uppercase letter, one lowercase letter, and one digit. It cannot have a single quotation mark (‘), a double quotation marks (“), a forward slash(/), a backward slash(),

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html#cfn-managedblockchain-member-memberfabricconfiguration-adminpassword
            :: , or a space.
            '''
            result = self._values.get("admin_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def admin_username(self) -> typing.Optional[builtins.str]:
            '''The user name for the member's initial administrative user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html#cfn-managedblockchain-member-memberfabricconfiguration-adminusername
            '''
            result = self._values.get("admin_username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberFabricConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.MemberFrameworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"member_fabric_configuration": "memberFabricConfiguration"},
    )
    class MemberFrameworkConfigurationProperty:
        def __init__(
            self,
            *,
            member_fabric_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.MemberFabricConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration properties relevant to a member for the blockchain framework that the Managed Blockchain network uses.

            :param member_fabric_configuration: Configuration properties for Hyperledger Fabric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberframeworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                member_framework_configuration_property = managedblockchain_mixins.CfnMemberPropsMixin.MemberFrameworkConfigurationProperty(
                    member_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.MemberFabricConfigurationProperty(
                        admin_password="adminPassword",
                        admin_username="adminUsername"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d5cf41fdcd4739249abae2db2961290263b4d4229059ff749a882404dd7d47aa)
                check_type(argname="argument member_fabric_configuration", value=member_fabric_configuration, expected_type=type_hints["member_fabric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if member_fabric_configuration is not None:
                self._values["member_fabric_configuration"] = member_fabric_configuration

        @builtins.property
        def member_fabric_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.MemberFabricConfigurationProperty"]]:
            '''Configuration properties for Hyperledger Fabric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberframeworkconfiguration.html#cfn-managedblockchain-member-memberframeworkconfiguration-memberfabricconfiguration
            '''
            result = self._values.get("member_fabric_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.MemberFabricConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberFrameworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "description": "description",
            "framework": "framework",
            "framework_version": "frameworkVersion",
            "name": "name",
            "network_framework_configuration": "networkFrameworkConfiguration",
            "voting_policy": "votingPolicy",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            description: typing.Optional[builtins.str] = None,
            framework: typing.Optional[builtins.str] = None,
            framework_version: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            network_framework_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            voting_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.VotingPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration properties of the network to which the member belongs.

            :param description: Attributes of the blockchain framework for the network.
            :param framework: The blockchain framework that the network uses.
            :param framework_version: The version of the blockchain framework that the network uses.
            :param name: The name of the network.
            :param network_framework_configuration: Configuration properties relevant to the network for the blockchain framework that the network uses.
            :param voting_policy: The voting rules that the network uses to decide if a proposal is accepted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                network_configuration_property = managedblockchain_mixins.CfnMemberPropsMixin.NetworkConfigurationProperty(
                    description="description",
                    framework="framework",
                    framework_version="frameworkVersion",
                    name="name",
                    network_framework_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty(
                        network_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFabricConfigurationProperty(
                            edition="edition"
                        )
                    ),
                    voting_policy=managedblockchain_mixins.CfnMemberPropsMixin.VotingPolicyProperty(
                        approval_threshold_policy=managedblockchain_mixins.CfnMemberPropsMixin.ApprovalThresholdPolicyProperty(
                            proposal_duration_in_hours=123,
                            threshold_comparator="thresholdComparator",
                            threshold_percentage=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5413870afc4b6145e94cd1ae53416236f03a8729def27b7ca15b4fd51ab093f7)
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
                check_type(argname="argument framework_version", value=framework_version, expected_type=type_hints["framework_version"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument network_framework_configuration", value=network_framework_configuration, expected_type=type_hints["network_framework_configuration"])
                check_type(argname="argument voting_policy", value=voting_policy, expected_type=type_hints["voting_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if description is not None:
                self._values["description"] = description
            if framework is not None:
                self._values["framework"] = framework
            if framework_version is not None:
                self._values["framework_version"] = framework_version
            if name is not None:
                self._values["name"] = name
            if network_framework_configuration is not None:
                self._values["network_framework_configuration"] = network_framework_configuration
            if voting_policy is not None:
                self._values["voting_policy"] = voting_policy

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''Attributes of the blockchain framework for the network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def framework(self) -> typing.Optional[builtins.str]:
            '''The blockchain framework that the network uses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-framework
            '''
            result = self._values.get("framework")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def framework_version(self) -> typing.Optional[builtins.str]:
            '''The version of the blockchain framework that the network uses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-frameworkversion
            '''
            result = self._values.get("framework_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the network.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_framework_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty"]]:
            '''Configuration properties relevant to the network for the blockchain framework that the network uses.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-networkframeworkconfiguration
            '''
            result = self._values.get("network_framework_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty"]], result)

        @builtins.property
        def voting_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.VotingPolicyProperty"]]:
            '''The voting rules that the network uses to decide if a proposal is accepted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-votingpolicy
            '''
            result = self._values.get("voting_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.VotingPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.NetworkFabricConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"edition": "edition"},
    )
    class NetworkFabricConfigurationProperty:
        def __init__(self, *, edition: typing.Optional[builtins.str] = None) -> None:
            '''Hyperledger Fabric configuration properties for the network.

            :param edition: The edition of Amazon Managed Blockchain that the network uses. Valid values are ``standard`` and ``starter`` . For more information, see `Amazon Managed Blockchain Pricing <https://docs.aws.amazon.com/managed-blockchain/pricing/>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkfabricconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                network_fabric_configuration_property = managedblockchain_mixins.CfnMemberPropsMixin.NetworkFabricConfigurationProperty(
                    edition="edition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fc3899cc29b6752ed2999ad91be65c6bfd382e39ca4ee57dff6d8537fc2da5c)
                check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if edition is not None:
                self._values["edition"] = edition

        @builtins.property
        def edition(self) -> typing.Optional[builtins.str]:
            '''The edition of Amazon Managed Blockchain that the network uses.

            Valid values are ``standard`` and ``starter`` . For more information, see `Amazon Managed Blockchain Pricing <https://docs.aws.amazon.com/managed-blockchain/pricing/>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkfabricconfiguration.html#cfn-managedblockchain-member-networkfabricconfiguration-edition
            '''
            result = self._values.get("edition")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFabricConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"network_fabric_configuration": "networkFabricConfiguration"},
    )
    class NetworkFrameworkConfigurationProperty:
        def __init__(
            self,
            *,
            network_fabric_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.NetworkFabricConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration properties relevant to the network for the blockchain framework that the network uses.

            :param network_fabric_configuration: Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network that is using the Hyperledger Fabric framework.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkframeworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                network_framework_configuration_property = managedblockchain_mixins.CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty(
                    network_fabric_configuration=managedblockchain_mixins.CfnMemberPropsMixin.NetworkFabricConfigurationProperty(
                        edition="edition"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__96019a4c4a3c12ff1124a80aa1f6738df80197e131c80d267f49b89316ace479)
                check_type(argname="argument network_fabric_configuration", value=network_fabric_configuration, expected_type=type_hints["network_fabric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_fabric_configuration is not None:
                self._values["network_fabric_configuration"] = network_fabric_configuration

        @builtins.property
        def network_fabric_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.NetworkFabricConfigurationProperty"]]:
            '''Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network that is using the Hyperledger Fabric framework.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkframeworkconfiguration.html#cfn-managedblockchain-member-networkframeworkconfiguration-networkfabricconfiguration
            '''
            result = self._values.get("network_fabric_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.NetworkFabricConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFrameworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnMemberPropsMixin.VotingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"approval_threshold_policy": "approvalThresholdPolicy"},
    )
    class VotingPolicyProperty:
        def __init__(
            self,
            *,
            approval_threshold_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnMemberPropsMixin.ApprovalThresholdPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The voting rules for the network to decide if a proposal is accepted.

            Applies only to Hyperledger Fabric.

            :param approval_threshold_policy: Defines the rules for the network for voting on proposals, such as the percentage of ``YES`` votes required for the proposal to be approved and the duration of the proposal. The policy applies to all proposals and is specified when the network is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-votingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                voting_policy_property = managedblockchain_mixins.CfnMemberPropsMixin.VotingPolicyProperty(
                    approval_threshold_policy=managedblockchain_mixins.CfnMemberPropsMixin.ApprovalThresholdPolicyProperty(
                        proposal_duration_in_hours=123,
                        threshold_comparator="thresholdComparator",
                        threshold_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9db38f409331e773252aa61ab310aa94d958c38f6a71489efd3b4142c2c20260)
                check_type(argname="argument approval_threshold_policy", value=approval_threshold_policy, expected_type=type_hints["approval_threshold_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approval_threshold_policy is not None:
                self._values["approval_threshold_policy"] = approval_threshold_policy

        @builtins.property
        def approval_threshold_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.ApprovalThresholdPolicyProperty"]]:
            '''Defines the rules for the network for voting on proposals, such as the percentage of ``YES`` votes required for the proposal to be approved and the duration of the proposal.

            The policy applies to all proposals and is specified when the network is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-votingpolicy.html#cfn-managedblockchain-member-votingpolicy-approvalthresholdpolicy
            '''
            result = self._values.get("approval_threshold_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnMemberPropsMixin.ApprovalThresholdPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VotingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnNodeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "member_id": "memberId",
        "network_id": "networkId",
        "node_configuration": "nodeConfiguration",
    },
)
class CfnNodeMixinProps:
    def __init__(
        self,
        *,
        member_id: typing.Optional[builtins.str] = None,
        network_id: typing.Optional[builtins.str] = None,
        node_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodePropsMixin.NodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnNodePropsMixin.

        :param member_id: The unique identifier of the member to which the node belongs. Applies only to Hyperledger Fabric.
        :param network_id: The unique identifier of the network for the node. Ethereum public networks have the following ``NetworkId`` s: - ``n-ethereum-mainnet``
        :param node_configuration: Configuration properties of a peer node.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
            
            cfn_node_mixin_props = managedblockchain_mixins.CfnNodeMixinProps(
                member_id="memberId",
                network_id="networkId",
                node_configuration=managedblockchain_mixins.CfnNodePropsMixin.NodeConfigurationProperty(
                    availability_zone="availabilityZone",
                    instance_type="instanceType"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1686f95dd7a2e8adb59261b16eae5a63e32ac4403571bf6665be0dbcad368c6a)
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument node_configuration", value=node_configuration, expected_type=type_hints["node_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if member_id is not None:
            self._values["member_id"] = member_id
        if network_id is not None:
            self._values["network_id"] = network_id
        if node_configuration is not None:
            self._values["node_configuration"] = node_configuration

    @builtins.property
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the member to which the node belongs.

        Applies only to Hyperledger Fabric.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the network for the node.

        Ethereum public networks have the following ``NetworkId`` s:

        - ``n-ethereum-mainnet``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-networkid
        '''
        result = self._values.get("network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodePropsMixin.NodeConfigurationProperty"]]:
        '''Configuration properties of a peer node.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-nodeconfiguration
        '''
        result = self._values.get("node_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodePropsMixin.NodeConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNodeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNodePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnNodePropsMixin",
):
    '''Creates a node on the specified blockchain network.

    Applies to Hyperledger Fabric and Ethereum.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html
    :cloudformationResource: AWS::ManagedBlockchain::Node
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
        
        cfn_node_props_mixin = managedblockchain_mixins.CfnNodePropsMixin(managedblockchain_mixins.CfnNodeMixinProps(
            member_id="memberId",
            network_id="networkId",
            node_configuration=managedblockchain_mixins.CfnNodePropsMixin.NodeConfigurationProperty(
                availability_zone="availabilityZone",
                instance_type="instanceType"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNodeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ManagedBlockchain::Node``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66de73982844751c394c15355ce6ae53dac5e80be3a7c63872d830ac153cd0e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b999807ce842d97acdb60df4cb345483aad6fcc8523524365260c9a2c40884b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de1792a323eba0c392f48323fe1a505b75b10bc200c7256cd156065acfb610c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNodeMixinProps:
        return typing.cast(CfnNodeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_managedblockchain.mixins.CfnNodePropsMixin.NodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "instance_type": "instanceType",
        },
    )
    class NodeConfigurationProperty:
        def __init__(
            self,
            *,
            availability_zone: typing.Optional[builtins.str] = None,
            instance_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration properties of a peer node within a membership.

            :param availability_zone: The Availability Zone in which the node exists. Required for Ethereum nodes.
            :param instance_type: The Amazon Managed Blockchain instance type for the node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_managedblockchain import mixins as managedblockchain_mixins
                
                node_configuration_property = managedblockchain_mixins.CfnNodePropsMixin.NodeConfigurationProperty(
                    availability_zone="availabilityZone",
                    instance_type="instanceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a7316d8317f8490a423588c823f66567fd43763fe2a08d7404c3b349e24f168)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if availability_zone is not None:
                self._values["availability_zone"] = availability_zone
            if instance_type is not None:
                self._values["instance_type"] = instance_type

        @builtins.property
        def availability_zone(self) -> typing.Optional[builtins.str]:
            '''The Availability Zone in which the node exists.

            Required for Ethereum nodes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html#cfn-managedblockchain-node-nodeconfiguration-availabilityzone
            '''
            result = self._values.get("availability_zone")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The Amazon Managed Blockchain instance type for the node.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html#cfn-managedblockchain-node-nodeconfiguration-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccessorMixinProps",
    "CfnAccessorPropsMixin",
    "CfnMemberMixinProps",
    "CfnMemberPropsMixin",
    "CfnNodeMixinProps",
    "CfnNodePropsMixin",
]

publication.publish()

def _typecheckingstub__9095f52471372b517d22ca9c66146a2a3e39ee9d24b585749dcc37e48aa36dab(
    *,
    accessor_type: typing.Optional[builtins.str] = None,
    network_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb8174fa7d25f1d601827d6647f6e6202c44cba9e22b2da1153dec35b3fb6698(
    props: typing.Union[CfnAccessorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e241c996eda7a59bc5c7af09e9e561ab22d42281739b73fdba783833341c4b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33827a8568fe25107d74568bbb52fece7be4e8c977e68f58220aee673a043286(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e55600fed9cda6efada1e92c719646fa1a51148c013b1a4d4aea96f1226b98(
    *,
    invitation_id: typing.Optional[builtins.str] = None,
    member_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782579f858bce5b204f267c84c72d6122954ed5a8067abd93ed16890d377effe(
    props: typing.Union[CfnMemberMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada91c3c090637e018197089ced05384365b4d37cd99eaa3d85044c646c495ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc70235676b3470e9e69865753f3b9673cd8b49b14674341dc9830c8f12b5fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c873e9c3b6f0301c10c348f20eef81bb362c52ff43f8946ab099f21c4208a4f(
    *,
    proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
    threshold_comparator: typing.Optional[builtins.str] = None,
    threshold_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac148603f30cf099b5a87cbb20123947c126e3bf54857857d50d2b428b3c131(
    *,
    description: typing.Optional[builtins.str] = None,
    member_framework_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.MemberFrameworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d772b1661616e564797722d59c5b2e526971408f4f1ab4934e27c2b107926b(
    *,
    admin_password: typing.Optional[builtins.str] = None,
    admin_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5cf41fdcd4739249abae2db2961290263b4d4229059ff749a882404dd7d47aa(
    *,
    member_fabric_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.MemberFabricConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5413870afc4b6145e94cd1ae53416236f03a8729def27b7ca15b4fd51ab093f7(
    *,
    description: typing.Optional[builtins.str] = None,
    framework: typing.Optional[builtins.str] = None,
    framework_version: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    network_framework_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.NetworkFrameworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    voting_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.VotingPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc3899cc29b6752ed2999ad91be65c6bfd382e39ca4ee57dff6d8537fc2da5c(
    *,
    edition: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96019a4c4a3c12ff1124a80aa1f6738df80197e131c80d267f49b89316ace479(
    *,
    network_fabric_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.NetworkFabricConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9db38f409331e773252aa61ab310aa94d958c38f6a71489efd3b4142c2c20260(
    *,
    approval_threshold_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnMemberPropsMixin.ApprovalThresholdPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1686f95dd7a2e8adb59261b16eae5a63e32ac4403571bf6665be0dbcad368c6a(
    *,
    member_id: typing.Optional[builtins.str] = None,
    network_id: typing.Optional[builtins.str] = None,
    node_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodePropsMixin.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66de73982844751c394c15355ce6ae53dac5e80be3a7c63872d830ac153cd0e8(
    props: typing.Union[CfnNodeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b999807ce842d97acdb60df4cb345483aad6fcc8523524365260c9a2c40884b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de1792a323eba0c392f48323fe1a505b75b10bc200c7256cd156065acfb610c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7316d8317f8490a423588c823f66567fd43763fe2a08d7404c3b349e24f168(
    *,
    availability_zone: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
