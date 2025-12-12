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
    jsii_type="@aws-cdk/mixins-preview.aws_identitystore.mixins.CfnGroupMembershipMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_id": "groupId",
        "identity_store_id": "identityStoreId",
        "member_id": "memberId",
    },
)
class CfnGroupMembershipMixinProps:
    def __init__(
        self,
        *,
        group_id: typing.Optional[builtins.str] = None,
        identity_store_id: typing.Optional[builtins.str] = None,
        member_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupMembershipPropsMixin.MemberIdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGroupMembershipPropsMixin.

        :param group_id: The identifier for a group in the identity store.
        :param identity_store_id: The globally unique identifier for the identity store.
        :param member_id: An object containing the identifier of a group member. Setting the ``MemberId`` 's ``UserId`` field to a specific User's ID indicates that user is a member of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_identitystore import mixins as identitystore_mixins
            
            cfn_group_membership_mixin_props = identitystore_mixins.CfnGroupMembershipMixinProps(
                group_id="groupId",
                identity_store_id="identityStoreId",
                member_id=identitystore_mixins.CfnGroupMembershipPropsMixin.MemberIdProperty(
                    user_id="userId"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9d9bbeffb17017218b7373de30d7d39deb380f8d551a835b13bf969a51859b)
            check_type(argname="argument group_id", value=group_id, expected_type=type_hints["group_id"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_id is not None:
            self._values["group_id"] = group_id
        if identity_store_id is not None:
            self._values["identity_store_id"] = identity_store_id
        if member_id is not None:
            self._values["member_id"] = member_id

    @builtins.property
    def group_id(self) -> typing.Optional[builtins.str]:
        '''The identifier for a group in the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html#cfn-identitystore-groupmembership-groupid
        '''
        result = self._values.get("group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_store_id(self) -> typing.Optional[builtins.str]:
        '''The globally unique identifier for the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html#cfn-identitystore-groupmembership-identitystoreid
        '''
        result = self._values.get("identity_store_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def member_id(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupMembershipPropsMixin.MemberIdProperty"]]:
        '''An object containing the identifier of a group member.

        Setting the ``MemberId`` 's ``UserId`` field to a specific User's ID indicates that user is a member of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html#cfn-identitystore-groupmembership-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupMembershipPropsMixin.MemberIdProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMembershipMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupMembershipPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_identitystore.mixins.CfnGroupMembershipPropsMixin",
):
    '''Creates a relationship between a member and a group.

    The following identifiers must be specified: ``GroupId`` , ``IdentityStoreId`` , and ``MemberId`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-groupmembership.html
    :cloudformationResource: AWS::IdentityStore::GroupMembership
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_identitystore import mixins as identitystore_mixins
        
        cfn_group_membership_props_mixin = identitystore_mixins.CfnGroupMembershipPropsMixin(identitystore_mixins.CfnGroupMembershipMixinProps(
            group_id="groupId",
            identity_store_id="identityStoreId",
            member_id=identitystore_mixins.CfnGroupMembershipPropsMixin.MemberIdProperty(
                user_id="userId"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupMembershipMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IdentityStore::GroupMembership``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__213f3a07e7df6b6c2bf74b058fe5902ba3de029350de91b8542d95067465b7a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f040f901c0c46053c34a3d88feeba93ce8ebfae385e2ad2f7718d348e33e3faf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1a9509c95a8a4e79d9e7880a6287d6568c2fe077167f17a5372c11b2b41c048)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupMembershipMixinProps:
        return typing.cast(CfnGroupMembershipMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_identitystore.mixins.CfnGroupMembershipPropsMixin.MemberIdProperty",
        jsii_struct_bases=[],
        name_mapping={"user_id": "userId"},
    )
    class MemberIdProperty:
        def __init__(self, *, user_id: typing.Optional[builtins.str] = None) -> None:
            '''An object that contains the identifier of a group member.

            Setting the ``UserID`` field to the specific identifier for a user indicates that the user is a member of the group.

            :param user_id: An object containing the identifiers of resources that can be members.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-identitystore-groupmembership-memberid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_identitystore import mixins as identitystore_mixins
                
                member_id_property = identitystore_mixins.CfnGroupMembershipPropsMixin.MemberIdProperty(
                    user_id="userId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__00d644df589abb6c224ca10d4511e8886175ec207f9ff6062dfe822303105381)
                check_type(argname="argument user_id", value=user_id, expected_type=type_hints["user_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if user_id is not None:
                self._values["user_id"] = user_id

        @builtins.property
        def user_id(self) -> typing.Optional[builtins.str]:
            '''An object containing the identifiers of resources that can be members.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-identitystore-groupmembership-memberid.html#cfn-identitystore-groupmembership-memberid-userid
            '''
            result = self._values.get("user_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberIdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_identitystore.mixins.CfnGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "identity_store_id": "identityStoreId",
    },
)
class CfnGroupMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        identity_store_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGroupPropsMixin.

        :param description: A string containing the description of the group.
        :param display_name: The display name value for the group. The length limit is 1,024 characters. This value can consist of letters, accented characters, symbols, numbers, punctuation, tab, new line, carriage return, space, and nonbreaking space in this attribute. This value is specified at the time the group is created and stored as an attribute of the group object in the identity store. Prefix search supports a maximum of 1,000 characters for the string.
        :param identity_store_id: The globally unique identifier for the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_identitystore import mixins as identitystore_mixins
            
            cfn_group_mixin_props = identitystore_mixins.CfnGroupMixinProps(
                description="description",
                display_name="displayName",
                identity_store_id="identityStoreId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c0c8f49ac78ad1a96667797dff0871aeae2d0122972c76a9714e476ae96f5b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument identity_store_id", value=identity_store_id, expected_type=type_hints["identity_store_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if identity_store_id is not None:
            self._values["identity_store_id"] = identity_store_id

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A string containing the description of the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html#cfn-identitystore-group-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The display name value for the group.

        The length limit is 1,024 characters. This value can consist of letters, accented characters, symbols, numbers, punctuation, tab, new line, carriage return, space, and nonbreaking space in this attribute. This value is specified at the time the group is created and stored as an attribute of the group object in the identity store.

        Prefix search supports a maximum of 1,000 characters for the string.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html#cfn-identitystore-group-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_store_id(self) -> typing.Optional[builtins.str]:
        '''The globally unique identifier for the identity store.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html#cfn-identitystore-group-identitystoreid
        '''
        result = self._values.get("identity_store_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_identitystore.mixins.CfnGroupPropsMixin",
):
    '''A group object, which contains a specified group’s metadata and attributes.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-identitystore-group.html
    :cloudformationResource: AWS::IdentityStore::Group
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_identitystore import mixins as identitystore_mixins
        
        cfn_group_props_mixin = identitystore_mixins.CfnGroupPropsMixin(identitystore_mixins.CfnGroupMixinProps(
            description="description",
            display_name="displayName",
            identity_store_id="identityStoreId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IdentityStore::Group``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41277a77b6f557fdc342fd13a66f6b9f545076ea2fee14aa41cc06bf4e0a11e5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b591d7e791da3cf2def7b100b3628b6f92bfaa082135126bd7cf297a4f292f7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c173af8c9218a0e83341cdc7997aafb2c8075ca79e47b010c95d4d663ea811)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupMixinProps:
        return typing.cast(CfnGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnGroupMembershipMixinProps",
    "CfnGroupMembershipPropsMixin",
    "CfnGroupMixinProps",
    "CfnGroupPropsMixin",
]

publication.publish()

def _typecheckingstub__3b9d9bbeffb17017218b7373de30d7d39deb380f8d551a835b13bf969a51859b(
    *,
    group_id: typing.Optional[builtins.str] = None,
    identity_store_id: typing.Optional[builtins.str] = None,
    member_id: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupMembershipPropsMixin.MemberIdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__213f3a07e7df6b6c2bf74b058fe5902ba3de029350de91b8542d95067465b7a3(
    props: typing.Union[CfnGroupMembershipMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f040f901c0c46053c34a3d88feeba93ce8ebfae385e2ad2f7718d348e33e3faf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1a9509c95a8a4e79d9e7880a6287d6568c2fe077167f17a5372c11b2b41c048(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d644df589abb6c224ca10d4511e8886175ec207f9ff6062dfe822303105381(
    *,
    user_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c0c8f49ac78ad1a96667797dff0871aeae2d0122972c76a9714e476ae96f5b(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    identity_store_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41277a77b6f557fdc342fd13a66f6b9f545076ea2fee14aa41cc06bf4e0a11e5(
    props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b591d7e791da3cf2def7b100b3628b6f92bfaa082135126bd7cf297a4f292f7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c173af8c9218a0e83341cdc7997aafb2c8075ca79e47b010c95d4d663ea811(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
