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
    jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnApprovalTeamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "approval_strategy": "approvalStrategy",
        "approvers": "approvers",
        "description": "description",
        "name": "name",
        "policies": "policies",
        "tags": "tags",
    },
)
class CfnApprovalTeamMixinProps:
    def __init__(
        self,
        *,
        approval_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApprovalTeamPropsMixin.ApprovalStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        approvers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApprovalTeamPropsMixin.ApproverProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApprovalTeamPropsMixin.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApprovalTeamPropsMixin.

        :param approval_strategy: Contains details for how an approval team grants approval.
        :param approvers: Contains details for an approver.
        :param description: Description for the team.
        :param name: Name of the team.
        :param policies: Contains details for a policy. Policies define what operations a team that define the permissions for team resources.
        :param tags: Tags that you have added to the specified resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
            
            cfn_approval_team_mixin_props = mpa_mixins.CfnApprovalTeamMixinProps(
                approval_strategy=mpa_mixins.CfnApprovalTeamPropsMixin.ApprovalStrategyProperty(
                    mof_n=mpa_mixins.CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty(
                        min_approvals_required=123
                    )
                ),
                approvers=[mpa_mixins.CfnApprovalTeamPropsMixin.ApproverProperty(
                    approver_id="approverId",
                    primary_identity_id="primaryIdentityId",
                    primary_identity_source_arn="primaryIdentitySourceArn",
                    primary_identity_status="primaryIdentityStatus",
                    response_time="responseTime"
                )],
                description="description",
                name="name",
                policies=[mpa_mixins.CfnApprovalTeamPropsMixin.PolicyProperty(
                    policy_arn="policyArn"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85447318a42c48ef36bfb03a9db3df6a37fe571e3f26b68e41fb6f3dacd70a2c)
            check_type(argname="argument approval_strategy", value=approval_strategy, expected_type=type_hints["approval_strategy"])
            check_type(argname="argument approvers", value=approvers, expected_type=type_hints["approvers"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if approval_strategy is not None:
            self._values["approval_strategy"] = approval_strategy
        if approvers is not None:
            self._values["approvers"] = approvers
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def approval_strategy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.ApprovalStrategyProperty"]]:
        '''Contains details for how an approval team grants approval.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html#cfn-mpa-approvalteam-approvalstrategy
        '''
        result = self._values.get("approval_strategy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.ApprovalStrategyProperty"]], result)

    @builtins.property
    def approvers(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.ApproverProperty"]]]]:
        '''Contains details for an approver.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html#cfn-mpa-approvalteam-approvers
        '''
        result = self._values.get("approvers")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.ApproverProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Description for the team.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html#cfn-mpa-approvalteam-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the team.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html#cfn-mpa-approvalteam-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.PolicyProperty"]]]]:
        '''Contains details for a policy.

        Policies define what operations a team that define the permissions for team resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html#cfn-mpa-approvalteam-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.PolicyProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags that you have added to the specified resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html#cfn-mpa-approvalteam-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApprovalTeamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApprovalTeamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnApprovalTeamPropsMixin",
):
    '''Creates a new approval team.

    For more information, see `Approval team <https://docs.aws.amazon.com/mpa/latest/userguide/mpa-concepts.html>`_ in the *Multi-party approval User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-approvalteam.html
    :cloudformationResource: AWS::MPA::ApprovalTeam
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
        
        cfn_approval_team_props_mixin = mpa_mixins.CfnApprovalTeamPropsMixin(mpa_mixins.CfnApprovalTeamMixinProps(
            approval_strategy=mpa_mixins.CfnApprovalTeamPropsMixin.ApprovalStrategyProperty(
                mof_n=mpa_mixins.CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty(
                    min_approvals_required=123
                )
            ),
            approvers=[mpa_mixins.CfnApprovalTeamPropsMixin.ApproverProperty(
                approver_id="approverId",
                primary_identity_id="primaryIdentityId",
                primary_identity_source_arn="primaryIdentitySourceArn",
                primary_identity_status="primaryIdentityStatus",
                response_time="responseTime"
            )],
            description="description",
            name="name",
            policies=[mpa_mixins.CfnApprovalTeamPropsMixin.PolicyProperty(
                policy_arn="policyArn"
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
        props: typing.Union[CfnApprovalTeamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MPA::ApprovalTeam``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__938d6f33e69704a33e363ec1d3cb49cdfa4390ee2893ebaaf24daa59a4321ec6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__949b9a9f38e122318efdc1e2cb3849a4a0e29db8cd049227207b3328770588cd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db4b1bff74be45bd9dfa79e39d9de8ee06eaf20952cdfbdf53f5563bccc55b6e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApprovalTeamMixinProps:
        return typing.cast(CfnApprovalTeamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnApprovalTeamPropsMixin.ApprovalStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"mof_n": "mofN"},
    )
    class ApprovalStrategyProperty:
        def __init__(
            self,
            *,
            mof_n: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Strategy for how an approval team grants approval.

            :param mof_n: Minimum number of approvals (M) required for a total number of approvers (N).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approvalstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
                
                approval_strategy_property = mpa_mixins.CfnApprovalTeamPropsMixin.ApprovalStrategyProperty(
                    mof_n=mpa_mixins.CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty(
                        min_approvals_required=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e545b81fefb9d4cf13af506b46369a22d927b515e3f760772ce315c96a12fdb1)
                check_type(argname="argument mof_n", value=mof_n, expected_type=type_hints["mof_n"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mof_n is not None:
                self._values["mof_n"] = mof_n

        @builtins.property
        def mof_n(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty"]]:
            '''Minimum number of approvals (M) required for a total number of approvers (N).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approvalstrategy.html#cfn-mpa-approvalteam-approvalstrategy-mofn
            '''
            result = self._values.get("mof_n")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApprovalStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnApprovalTeamPropsMixin.ApproverProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approver_id": "approverId",
            "primary_identity_id": "primaryIdentityId",
            "primary_identity_source_arn": "primaryIdentitySourceArn",
            "primary_identity_status": "primaryIdentityStatus",
            "response_time": "responseTime",
        },
    )
    class ApproverProperty:
        def __init__(
            self,
            *,
            approver_id: typing.Optional[builtins.str] = None,
            primary_identity_id: typing.Optional[builtins.str] = None,
            primary_identity_source_arn: typing.Optional[builtins.str] = None,
            primary_identity_status: typing.Optional[builtins.str] = None,
            response_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details for an approver.

            :param approver_id: ID for the approver.
            :param primary_identity_id: ID for the user.
            :param primary_identity_source_arn: Amazon Resource Name (ARN) for the identity source. The identity source manages the user authentication for approvers.
            :param primary_identity_status: Status for the identity source. For example, if an approver has accepted a team invitation with a user authentication method managed by the identity source.
            :param response_time: Timestamp when the approver responded to an approval team invitation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approver.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
                
                approver_property = mpa_mixins.CfnApprovalTeamPropsMixin.ApproverProperty(
                    approver_id="approverId",
                    primary_identity_id="primaryIdentityId",
                    primary_identity_source_arn="primaryIdentitySourceArn",
                    primary_identity_status="primaryIdentityStatus",
                    response_time="responseTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2a91aa5114bd654b1a180d3e8a2de6b5634d8ec626e97dc24759efdc55bd71d5)
                check_type(argname="argument approver_id", value=approver_id, expected_type=type_hints["approver_id"])
                check_type(argname="argument primary_identity_id", value=primary_identity_id, expected_type=type_hints["primary_identity_id"])
                check_type(argname="argument primary_identity_source_arn", value=primary_identity_source_arn, expected_type=type_hints["primary_identity_source_arn"])
                check_type(argname="argument primary_identity_status", value=primary_identity_status, expected_type=type_hints["primary_identity_status"])
                check_type(argname="argument response_time", value=response_time, expected_type=type_hints["response_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approver_id is not None:
                self._values["approver_id"] = approver_id
            if primary_identity_id is not None:
                self._values["primary_identity_id"] = primary_identity_id
            if primary_identity_source_arn is not None:
                self._values["primary_identity_source_arn"] = primary_identity_source_arn
            if primary_identity_status is not None:
                self._values["primary_identity_status"] = primary_identity_status
            if response_time is not None:
                self._values["response_time"] = response_time

        @builtins.property
        def approver_id(self) -> typing.Optional[builtins.str]:
            '''ID for the approver.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approver.html#cfn-mpa-approvalteam-approver-approverid
            '''
            result = self._values.get("approver_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_identity_id(self) -> typing.Optional[builtins.str]:
            '''ID for the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approver.html#cfn-mpa-approvalteam-approver-primaryidentityid
            '''
            result = self._values.get("primary_identity_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_identity_source_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) for the identity source.

            The identity source manages the user authentication for approvers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approver.html#cfn-mpa-approvalteam-approver-primaryidentitysourcearn
            '''
            result = self._values.get("primary_identity_source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def primary_identity_status(self) -> typing.Optional[builtins.str]:
            '''Status for the identity source.

            For example, if an approver has accepted a team invitation with a user authentication method managed by the identity source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approver.html#cfn-mpa-approvalteam-approver-primaryidentitystatus
            '''
            result = self._values.get("primary_identity_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def response_time(self) -> typing.Optional[builtins.str]:
            '''Timestamp when the approver responded to an approval team invitation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-approver.html#cfn-mpa-approvalteam-approver-responsetime
            '''
            result = self._values.get("response_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApproverProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"min_approvals_required": "minApprovalsRequired"},
    )
    class MofNApprovalStrategyProperty:
        def __init__(
            self,
            *,
            min_approvals_required: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Strategy for how an approval team grants approval.

            :param min_approvals_required: Minimum number of approvals (M) required for a total number of approvers (N).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-mofnapprovalstrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
                
                mof_nApproval_strategy_property = mpa_mixins.CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty(
                    min_approvals_required=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d1189663d5a6147421d80bf57d9b7091620f5564fae76e285dfe1df1decf76c1)
                check_type(argname="argument min_approvals_required", value=min_approvals_required, expected_type=type_hints["min_approvals_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if min_approvals_required is not None:
                self._values["min_approvals_required"] = min_approvals_required

        @builtins.property
        def min_approvals_required(self) -> typing.Optional[jsii.Number]:
            '''Minimum number of approvals (M) required for a total number of approvers (N).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-mofnapprovalstrategy.html#cfn-mpa-approvalteam-mofnapprovalstrategy-minapprovalsrequired
            '''
            result = self._values.get("min_approvals_required")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MofNApprovalStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnApprovalTeamPropsMixin.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"policy_arn": "policyArn"},
    )
    class PolicyProperty:
        def __init__(self, *, policy_arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains details for a policy.

            Policies define what operations a team that define the permissions for team resources.

            :param policy_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
                
                policy_property = mpa_mixins.CfnApprovalTeamPropsMixin.PolicyProperty(
                    policy_arn="policyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e97970208d4d53357ac2672071a63f266fff63e7872acd3d886e8b8aafc999a)
                check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_arn is not None:
                self._values["policy_arn"] = policy_arn

        @builtins.property
        def policy_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-approvalteam-policy.html#cfn-mpa-approvalteam-policy-policyarn
            '''
            result = self._values.get("policy_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnIdentitySourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_source_parameters": "identitySourceParameters",
        "tags": "tags",
    },
)
class CfnIdentitySourceMixinProps:
    def __init__(
        self,
        *,
        identity_source_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnIdentitySourcePropsMixin.

        :param identity_source_parameters: A ``IdentitySourceParameters`` object. Contains details for the resource that provides identities to the identity source. For example, an IAM Identity Center instance.
        :param tags: Tags that you have added to the specified resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-identitysource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
            
            cfn_identity_source_mixin_props = mpa_mixins.CfnIdentitySourceMixinProps(
                identity_source_parameters=mpa_mixins.CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty(
                    iam_identity_center=mpa_mixins.CfnIdentitySourcePropsMixin.IamIdentityCenterProperty(
                        approval_portal_url="approvalPortalUrl",
                        instance_arn="instanceArn",
                        region="region"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28de594395387221c03932543e7f44b46aef6e5de7a2a5bb80f872c30080cdf0)
            check_type(argname="argument identity_source_parameters", value=identity_source_parameters, expected_type=type_hints["identity_source_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if identity_source_parameters is not None:
            self._values["identity_source_parameters"] = identity_source_parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def identity_source_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty"]]:
        '''A ``IdentitySourceParameters`` object.

        Contains details for the resource that provides identities to the identity source. For example, an IAM Identity Center instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-identitysource.html#cfn-mpa-identitysource-identitysourceparameters
        '''
        result = self._values.get("identity_source_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Tags that you have added to the specified resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-identitysource.html#cfn-mpa-identitysource-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentitySourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentitySourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnIdentitySourcePropsMixin",
):
    '''Creates a new identity source.

    For more information, see `Identity Source <https://docs.aws.amazon.com/mpa/latest/userguide/mpa-concepts.html>`_ in the *Multi-party approval User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mpa-identitysource.html
    :cloudformationResource: AWS::MPA::IdentitySource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
        
        cfn_identity_source_props_mixin = mpa_mixins.CfnIdentitySourcePropsMixin(mpa_mixins.CfnIdentitySourceMixinProps(
            identity_source_parameters=mpa_mixins.CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty(
                iam_identity_center=mpa_mixins.CfnIdentitySourcePropsMixin.IamIdentityCenterProperty(
                    approval_portal_url="approvalPortalUrl",
                    instance_arn="instanceArn",
                    region="region"
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
        props: typing.Union[CfnIdentitySourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::MPA::IdentitySource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc2e2b6b16458e5928ea786d95e66e997eb18b7d459e901168ed80368d40c8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaff0dd4652adf8a5d62afd1214369d860f3231c1aea3830b3a112a3dff7f556)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d3480c7b709d33708431083229730059f276ebb62d1765fff0390762ba67d42)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentitySourceMixinProps:
        return typing.cast(CfnIdentitySourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnIdentitySourcePropsMixin.IamIdentityCenterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "approval_portal_url": "approvalPortalUrl",
            "instance_arn": "instanceArn",
            "region": "region",
        },
    )
    class IamIdentityCenterProperty:
        def __init__(
            self,
            *,
            approval_portal_url: typing.Optional[builtins.str] = None,
            instance_arn: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''AWS IAM Identity Center credentials.

            For more information see, `AWS IAM Identity Center <https://docs.aws.amazon.com/identity-center/>`_ .

            :param approval_portal_url: URL for the approval portal associated with the IAM Identity Center instance.
            :param instance_arn: Amazon Resource Name (ARN) for the IAM Identity Center instance.
            :param region: AWS Region where the IAM Identity Center instance is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-identitysource-iamidentitycenter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
                
                iam_identity_center_property = mpa_mixins.CfnIdentitySourcePropsMixin.IamIdentityCenterProperty(
                    approval_portal_url="approvalPortalUrl",
                    instance_arn="instanceArn",
                    region="region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3914f1294660809547e0b4f5ee60c39788f7f6669533cf084efeceab1f429b2b)
                check_type(argname="argument approval_portal_url", value=approval_portal_url, expected_type=type_hints["approval_portal_url"])
                check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approval_portal_url is not None:
                self._values["approval_portal_url"] = approval_portal_url
            if instance_arn is not None:
                self._values["instance_arn"] = instance_arn
            if region is not None:
                self._values["region"] = region

        @builtins.property
        def approval_portal_url(self) -> typing.Optional[builtins.str]:
            '''URL for the approval portal associated with the IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-identitysource-iamidentitycenter.html#cfn-mpa-identitysource-iamidentitycenter-approvalportalurl
            '''
            result = self._values.get("approval_portal_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) for the IAM Identity Center instance.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-identitysource-iamidentitycenter.html#cfn-mpa-identitysource-iamidentitycenter-instancearn
            '''
            result = self._values.get("instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''AWS Region where the IAM Identity Center instance is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-identitysource-iamidentitycenter.html#cfn-mpa-identitysource-iamidentitycenter-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamIdentityCenterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_mpa.mixins.CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"iam_identity_center": "iamIdentityCenter"},
    )
    class IdentitySourceParametersProperty:
        def __init__(
            self,
            *,
            iam_identity_center: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentitySourcePropsMixin.IamIdentityCenterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains details for the resource that provides identities to the identity source.

            For example, an IAM Identity Center instance.

            :param iam_identity_center: AWS IAM Identity Center credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-identitysource-identitysourceparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_mpa import mixins as mpa_mixins
                
                identity_source_parameters_property = mpa_mixins.CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty(
                    iam_identity_center=mpa_mixins.CfnIdentitySourcePropsMixin.IamIdentityCenterProperty(
                        approval_portal_url="approvalPortalUrl",
                        instance_arn="instanceArn",
                        region="region"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00fc7bc24019e539cc97f7f53a99c1353d749273663fcebb8ac55876bdd85eab)
                check_type(argname="argument iam_identity_center", value=iam_identity_center, expected_type=type_hints["iam_identity_center"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam_identity_center is not None:
                self._values["iam_identity_center"] = iam_identity_center

        @builtins.property
        def iam_identity_center(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.IamIdentityCenterProperty"]]:
            '''AWS IAM Identity Center credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mpa-identitysource-identitysourceparameters.html#cfn-mpa-identitysource-identitysourceparameters-iamidentitycenter
            '''
            result = self._values.get("iam_identity_center")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentitySourcePropsMixin.IamIdentityCenterProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentitySourceParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApprovalTeamMixinProps",
    "CfnApprovalTeamPropsMixin",
    "CfnIdentitySourceMixinProps",
    "CfnIdentitySourcePropsMixin",
]

publication.publish()

def _typecheckingstub__85447318a42c48ef36bfb03a9db3df6a37fe571e3f26b68e41fb6f3dacd70a2c(
    *,
    approval_strategy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApprovalTeamPropsMixin.ApprovalStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    approvers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApprovalTeamPropsMixin.ApproverProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApprovalTeamPropsMixin.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__938d6f33e69704a33e363ec1d3cb49cdfa4390ee2893ebaaf24daa59a4321ec6(
    props: typing.Union[CfnApprovalTeamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949b9a9f38e122318efdc1e2cb3849a4a0e29db8cd049227207b3328770588cd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db4b1bff74be45bd9dfa79e39d9de8ee06eaf20952cdfbdf53f5563bccc55b6e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e545b81fefb9d4cf13af506b46369a22d927b515e3f760772ce315c96a12fdb1(
    *,
    mof_n: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApprovalTeamPropsMixin.MofNApprovalStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a91aa5114bd654b1a180d3e8a2de6b5634d8ec626e97dc24759efdc55bd71d5(
    *,
    approver_id: typing.Optional[builtins.str] = None,
    primary_identity_id: typing.Optional[builtins.str] = None,
    primary_identity_source_arn: typing.Optional[builtins.str] = None,
    primary_identity_status: typing.Optional[builtins.str] = None,
    response_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1189663d5a6147421d80bf57d9b7091620f5564fae76e285dfe1df1decf76c1(
    *,
    min_approvals_required: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e97970208d4d53357ac2672071a63f266fff63e7872acd3d886e8b8aafc999a(
    *,
    policy_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28de594395387221c03932543e7f44b46aef6e5de7a2a5bb80f872c30080cdf0(
    *,
    identity_source_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.IdentitySourceParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc2e2b6b16458e5928ea786d95e66e997eb18b7d459e901168ed80368d40c8f(
    props: typing.Union[CfnIdentitySourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaff0dd4652adf8a5d62afd1214369d860f3231c1aea3830b3a112a3dff7f556(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d3480c7b709d33708431083229730059f276ebb62d1765fff0390762ba67d42(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3914f1294660809547e0b4f5ee60c39788f7f6669533cf084efeceab1f429b2b(
    *,
    approval_portal_url: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00fc7bc24019e539cc97f7f53a99c1353d749273663fcebb8ac55876bdd85eab(
    *,
    iam_identity_center: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentitySourcePropsMixin.IamIdentityCenterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
