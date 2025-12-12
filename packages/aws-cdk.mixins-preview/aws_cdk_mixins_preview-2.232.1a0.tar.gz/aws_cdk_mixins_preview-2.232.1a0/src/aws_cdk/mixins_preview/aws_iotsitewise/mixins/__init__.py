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
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policy_identity": "accessPolicyIdentity",
        "access_policy_permission": "accessPolicyPermission",
        "access_policy_resource": "accessPolicyResource",
    },
)
class CfnAccessPolicyMixinProps:
    def __init__(
        self,
        *,
        access_policy_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        access_policy_permission: typing.Optional[builtins.str] = None,
        access_policy_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccessPolicyPropsMixin.

        :param access_policy_identity: The identity for this access policy. Choose an IAM Identity Center user, an IAM Identity Center group, or an IAM user.
        :param access_policy_permission: The permission level for this access policy. Note that a project ``ADMINISTRATOR`` is also known as a project owner.
        :param access_policy_resource: The AWS IoT SiteWise Monitor resource for this access policy. Choose either a portal or a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_access_policy_mixin_props = iotsitewise_mixins.CfnAccessPolicyMixinProps(
                access_policy_identity=iotsitewise_mixins.CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty(
                    iam_role=iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamRoleProperty(
                        arn="arn"
                    ),
                    iam_user=iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamUserProperty(
                        arn="arn"
                    ),
                    user=iotsitewise_mixins.CfnAccessPolicyPropsMixin.UserProperty(
                        id="id"
                    )
                ),
                access_policy_permission="accessPolicyPermission",
                access_policy_resource=iotsitewise_mixins.CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty(
                    portal=iotsitewise_mixins.CfnAccessPolicyPropsMixin.PortalProperty(
                        id="id"
                    ),
                    project=iotsitewise_mixins.CfnAccessPolicyPropsMixin.ProjectProperty(
                        id="id"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60ba3197eb03e24ac1b4baad565e4034d9540b6e2237fdb4048a77f508bfdbc2)
            check_type(argname="argument access_policy_identity", value=access_policy_identity, expected_type=type_hints["access_policy_identity"])
            check_type(argname="argument access_policy_permission", value=access_policy_permission, expected_type=type_hints["access_policy_permission"])
            check_type(argname="argument access_policy_resource", value=access_policy_resource, expected_type=type_hints["access_policy_resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policy_identity is not None:
            self._values["access_policy_identity"] = access_policy_identity
        if access_policy_permission is not None:
            self._values["access_policy_permission"] = access_policy_permission
        if access_policy_resource is not None:
            self._values["access_policy_resource"] = access_policy_resource

    @builtins.property
    def access_policy_identity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty"]]:
        '''The identity for this access policy.

        Choose an IAM Identity Center user, an IAM Identity Center group, or an IAM user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity
        '''
        result = self._values.get("access_policy_identity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty"]], result)

    @builtins.property
    def access_policy_permission(self) -> typing.Optional[builtins.str]:
        '''The permission level for this access policy.

        Note that a project ``ADMINISTRATOR`` is also known as a project owner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicypermission
        '''
        result = self._values.get("access_policy_permission")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def access_policy_resource(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty"]]:
        '''The AWS IoT SiteWise Monitor resource for this access policy.

        Choose either a portal or a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html#cfn-iotsitewise-accesspolicy-accesspolicyresource
        '''
        result = self._values.get("access_policy_resource")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin",
):
    '''.. epigraph::

   The AWS IoT SiteWise Monitor feature will no longer be open to new customers starting November 7, 2025 .

    If you would like to use the AWS IoT SiteWise Monitor feature, sign up prior to that date. Existing customers can continue to use the service as normal. For more information, see `AWS IoT SiteWise Monitor availability change <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/iotsitewise-monitor-availability-change.html>`_ .

    Creates an access policy that grants the specified identity (IAM Identity Center user, IAM Identity Center group, or IAM user) access to the specified AWS IoT SiteWise Monitor portal or project resource.
    .. epigraph::

       Support for access policies that use an SSO Group as the identity is not supported at this time.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-accesspolicy.html
    :cloudformationResource: AWS::IoTSiteWise::AccessPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_access_policy_props_mixin = iotsitewise_mixins.CfnAccessPolicyPropsMixin(iotsitewise_mixins.CfnAccessPolicyMixinProps(
            access_policy_identity=iotsitewise_mixins.CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty(
                iam_role=iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamRoleProperty(
                    arn="arn"
                ),
                iam_user=iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamUserProperty(
                    arn="arn"
                ),
                user=iotsitewise_mixins.CfnAccessPolicyPropsMixin.UserProperty(
                    id="id"
                )
            ),
            access_policy_permission="accessPolicyPermission",
            access_policy_resource=iotsitewise_mixins.CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty(
                portal=iotsitewise_mixins.CfnAccessPolicyPropsMixin.PortalProperty(
                    id="id"
                ),
                project=iotsitewise_mixins.CfnAccessPolicyPropsMixin.ProjectProperty(
                    id="id"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::AccessPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee19fcb7fe6f7ecdf032765d85996bf45e8d87930cad57a525a2c3985330716)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67b891abe155649965105dfcfc834de4c98af6156bc6bb0449243f52684c678c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f2d78c380b9ddf50fb8ebe5fa8124ebbf3adaad0539cf183d68f13a2c3ef55)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessPolicyMixinProps:
        return typing.cast(CfnAccessPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty",
        jsii_struct_bases=[],
        name_mapping={"iam_role": "iamRole", "iam_user": "iamUser", "user": "user"},
    )
    class AccessPolicyIdentityProperty:
        def __init__(
            self,
            *,
            iam_role: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.IamRoleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            iam_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.IamUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.UserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The identity (IAM Identity Center user, IAM Identity Center group, or IAM user) to which this access policy applies.

            :param iam_role: An IAM role identity.
            :param iam_user: An IAM user identity.
            :param user: An IAM Identity Center user identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                access_policy_identity_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty(
                    iam_role=iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamRoleProperty(
                        arn="arn"
                    ),
                    iam_user=iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamUserProperty(
                        arn="arn"
                    ),
                    user=iotsitewise_mixins.CfnAccessPolicyPropsMixin.UserProperty(
                        id="id"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3633858c7b39ce6eef7bcd631db9354135fe807cd00da82f2cf58bf4d42eaa6)
                check_type(argname="argument iam_role", value=iam_role, expected_type=type_hints["iam_role"])
                check_type(argname="argument iam_user", value=iam_user, expected_type=type_hints["iam_user"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iam_role is not None:
                self._values["iam_role"] = iam_role
            if iam_user is not None:
                self._values["iam_user"] = iam_user
            if user is not None:
                self._values["user"] = user

        @builtins.property
        def iam_role(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.IamRoleProperty"]]:
            '''An IAM role identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity-iamrole
            '''
            result = self._values.get("iam_role")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.IamRoleProperty"]], result)

        @builtins.property
        def iam_user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.IamUserProperty"]]:
            '''An IAM user identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity-iamuser
            '''
            result = self._values.get("iam_user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.IamUserProperty"]], result)

        @builtins.property
        def user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.UserProperty"]]:
            '''An IAM Identity Center user identity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyidentity.html#cfn-iotsitewise-accesspolicy-accesspolicyidentity-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.UserProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPolicyIdentityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"portal": "portal", "project": "project"},
    )
    class AccessPolicyResourceProperty:
        def __init__(
            self,
            *,
            portal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.PortalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            project: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessPolicyPropsMixin.ProjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The AWS IoT SiteWise Monitor resource for this access policy.

            Choose either a portal or a project.

            :param portal: Identifies an AWS IoT SiteWise Monitor portal.
            :param project: Identifies a specific AWS IoT SiteWise Monitor project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                access_policy_resource_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty(
                    portal=iotsitewise_mixins.CfnAccessPolicyPropsMixin.PortalProperty(
                        id="id"
                    ),
                    project=iotsitewise_mixins.CfnAccessPolicyPropsMixin.ProjectProperty(
                        id="id"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3b08471238b1145803210592f37ace7196d6d0e7d4cf78fbac74f21613409ea)
                check_type(argname="argument portal", value=portal, expected_type=type_hints["portal"])
                check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if portal is not None:
                self._values["portal"] = portal
            if project is not None:
                self._values["project"] = project

        @builtins.property
        def portal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.PortalProperty"]]:
            '''Identifies an AWS IoT SiteWise Monitor portal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyresource.html#cfn-iotsitewise-accesspolicy-accesspolicyresource-portal
            '''
            result = self._values.get("portal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.PortalProperty"]], result)

        @builtins.property
        def project(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.ProjectProperty"]]:
            '''Identifies a specific AWS IoT SiteWise Monitor project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-accesspolicyresource.html#cfn-iotsitewise-accesspolicy-accesspolicyresource-project
            '''
            result = self._values.get("project")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessPolicyPropsMixin.ProjectProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPolicyResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.IamRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class IamRoleProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains information about an AWS Identity and Access Management role.

            For more information, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *IAM User Guide* .

            :param arn: The ARN of the IAM role. For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamrole.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                iam_role_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamRoleProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ed9e460349e8698ba4c9e17d2265ad865f0212635971a46a42e50360c3a6b500)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role.

            For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamrole.html#cfn-iotsitewise-accesspolicy-iamrole-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.IamUserProperty",
        jsii_struct_bases=[],
        name_mapping={"arn": "arn"},
    )
    class IamUserProperty:
        def __init__(self, *, arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains information about an AWS Identity and Access Management user.

            :param arn: The ARN of the IAM user. For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* . .. epigraph:: If you delete the IAM user, access policies that contain this identity include an empty ``arn`` . You can delete the access policy for the IAM user that no longer exists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                iam_user_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.IamUserProperty(
                    arn="arn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e3684d26436a9383d739e5e81d799713b24dd05622c74ead3984ac9eb8ac72a2)
                check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if arn is not None:
                self._values["arn"] = arn

        @builtins.property
        def arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM user. For more information, see `IAM ARNs <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

            .. epigraph::

               If you delete the IAM user, access policies that contain this identity include an empty ``arn`` . You can delete the access policy for the IAM user that no longer exists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-iamuser.html#cfn-iotsitewise-accesspolicy-iamuser-arn
            '''
            result = self._values.get("arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IamUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.PortalProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class PortalProperty:
        def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
            '''Identifies an AWS IoT SiteWise Monitor portal.

            :param id: The ID of the portal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-portal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                portal_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.PortalProperty(
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e15d639e4c17daf8a21256e9f0ce77c4e7fbbf05a202c51f4553c37b0f4bce69)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the portal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-portal.html#cfn-iotsitewise-accesspolicy-portal-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.ProjectProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class ProjectProperty:
        def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
            '''Identifies a specific AWS IoT SiteWise Monitor project.

            :param id: The ID of the project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-project.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                project_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.ProjectProperty(
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86aa039711c0d511d5d709f3cf3d093dbde20dfb349a76ad10dfbaa2828c41e3)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the project.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-project.html#cfn-iotsitewise-accesspolicy-project-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAccessPolicyPropsMixin.UserProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id"},
    )
    class UserProperty:
        def __init__(self, *, id: typing.Optional[builtins.str] = None) -> None:
            '''Contains information for a user identity in an access policy.

            :param id: The IAM Identity Center ID of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-user.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                user_property = iotsitewise_mixins.CfnAccessPolicyPropsMixin.UserProperty(
                    id="id"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b0131dc793dcc13e38b4bf9e06013d51e579ec7c4e33ca6ed8c3be08b37da3d)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The IAM Identity Center ID of the user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-accesspolicy-user.html#cfn-iotsitewise-accesspolicy-user-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_description": "assetDescription",
        "asset_external_id": "assetExternalId",
        "asset_hierarchies": "assetHierarchies",
        "asset_model_id": "assetModelId",
        "asset_name": "assetName",
        "asset_properties": "assetProperties",
        "tags": "tags",
    },
)
class CfnAssetMixinProps:
    def __init__(
        self,
        *,
        asset_description: typing.Optional[builtins.str] = None,
        asset_external_id: typing.Optional[builtins.str] = None,
        asset_hierarchies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetPropsMixin.AssetHierarchyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        asset_model_id: typing.Optional[builtins.str] = None,
        asset_name: typing.Optional[builtins.str] = None,
        asset_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetPropsMixin.AssetPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAssetPropsMixin.

        :param asset_description: The ID of the asset, in UUID format.
        :param asset_external_id: The external ID of the asset model composite model. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_hierarchies: A list of asset hierarchies that each contain a ``hierarchyId`` . A hierarchy specifies allowed parent/child asset relationships.
        :param asset_model_id: The ID of the asset model from which to create the asset. This can be either the actual ID in UUID format, or else ``externalId:`` followed by the external ID, if it has one. For more information, see `Referencing objects with external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-id-references>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_name: A friendly name for the asset.
        :param asset_properties: The list of asset properties for the asset. This object doesn't include properties that you define in composite models. You can find composite model properties in the ``assetCompositeModels`` object.
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_asset_mixin_props = iotsitewise_mixins.CfnAssetMixinProps(
                asset_description="assetDescription",
                asset_external_id="assetExternalId",
                asset_hierarchies=[iotsitewise_mixins.CfnAssetPropsMixin.AssetHierarchyProperty(
                    child_asset_id="childAssetId",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId"
                )],
                asset_model_id="assetModelId",
                asset_name="assetName",
                asset_properties=[iotsitewise_mixins.CfnAssetPropsMixin.AssetPropertyProperty(
                    alias="alias",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    notification_state="notificationState",
                    unit="unit"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19b35f584fa63fb70614867d69366ba08a0d97df2408336a30bab6953d4951a)
            check_type(argname="argument asset_description", value=asset_description, expected_type=type_hints["asset_description"])
            check_type(argname="argument asset_external_id", value=asset_external_id, expected_type=type_hints["asset_external_id"])
            check_type(argname="argument asset_hierarchies", value=asset_hierarchies, expected_type=type_hints["asset_hierarchies"])
            check_type(argname="argument asset_model_id", value=asset_model_id, expected_type=type_hints["asset_model_id"])
            check_type(argname="argument asset_name", value=asset_name, expected_type=type_hints["asset_name"])
            check_type(argname="argument asset_properties", value=asset_properties, expected_type=type_hints["asset_properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_description is not None:
            self._values["asset_description"] = asset_description
        if asset_external_id is not None:
            self._values["asset_external_id"] = asset_external_id
        if asset_hierarchies is not None:
            self._values["asset_hierarchies"] = asset_hierarchies
        if asset_model_id is not None:
            self._values["asset_model_id"] = asset_model_id
        if asset_name is not None:
            self._values["asset_name"] = asset_name
        if asset_properties is not None:
            self._values["asset_properties"] = asset_properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_description(self) -> typing.Optional[builtins.str]:
        '''The ID of the asset, in UUID format.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetdescription
        '''
        result = self._values.get("asset_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_external_id(self) -> typing.Optional[builtins.str]:
        '''The external ID of the asset model composite model.

        For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetexternalid
        '''
        result = self._values.get("asset_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetPropsMixin.AssetHierarchyProperty"]]]]:
        '''A list of asset hierarchies that each contain a ``hierarchyId`` .

        A hierarchy specifies allowed parent/child asset relationships.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assethierarchies
        '''
        result = self._values.get("asset_hierarchies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetPropsMixin.AssetHierarchyProperty"]]]], result)

    @builtins.property
    def asset_model_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the asset model from which to create the asset.

        This can be either the actual ID in UUID format, or else ``externalId:`` followed by the external ID, if it has one. For more information, see `Referencing objects with external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-id-references>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetmodelid
        '''
        result = self._values.get("asset_model_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the asset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetname
        '''
        result = self._values.get("asset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetPropsMixin.AssetPropertyProperty"]]]]:
        '''The list of asset properties for the asset.

        This object doesn't include properties that you define in composite models. You can find composite model properties in the ``assetCompositeModels`` object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-assetproperties
        '''
        result = self._values.get("asset_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetPropsMixin.AssetPropertyProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html#cfn-iotsitewise-asset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_model_composite_models": "assetModelCompositeModels",
        "asset_model_description": "assetModelDescription",
        "asset_model_external_id": "assetModelExternalId",
        "asset_model_hierarchies": "assetModelHierarchies",
        "asset_model_name": "assetModelName",
        "asset_model_properties": "assetModelProperties",
        "asset_model_type": "assetModelType",
        "enforced_asset_model_interface_relationships": "enforcedAssetModelInterfaceRelationships",
        "tags": "tags",
    },
)
class CfnAssetModelMixinProps:
    def __init__(
        self,
        *,
        asset_model_composite_models: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.AssetModelCompositeModelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        asset_model_description: typing.Optional[builtins.str] = None,
        asset_model_external_id: typing.Optional[builtins.str] = None,
        asset_model_hierarchies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.AssetModelHierarchyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        asset_model_name: typing.Optional[builtins.str] = None,
        asset_model_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.AssetModelPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        asset_model_type: typing.Optional[builtins.str] = None,
        enforced_asset_model_interface_relationships: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAssetModelPropsMixin.

        :param asset_model_composite_models: The composite models that are part of this asset model. It groups properties (such as attributes, measurements, transforms, and metrics) and child composite models that model parts of your industrial equipment. Each composite model has a type that defines the properties that the composite model supports. Use composite models to define alarms on this asset model. .. epigraph:: When creating custom composite models, you need to use `CreateAssetModelCompositeModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_CreateAssetModelCompositeModel.html>`_ . For more information, see `Creating custom composite models (Components) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-custom-composite-models.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_model_description: A description for the asset model.
        :param asset_model_external_id: The external ID of the asset model. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_model_hierarchies: The hierarchy definitions of the asset model. Each hierarchy specifies an asset model whose assets can be children of any other assets created from this asset model. For more information, see `Asset hierarchies <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* . You can specify up to 10 hierarchies per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_model_name: A unique name for the asset model.
        :param asset_model_properties: The property definitions of the asset model. For more information, see `Asset properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html>`_ in the *AWS IoT SiteWise User Guide* . You can specify up to 200 properties per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param asset_model_type: The type of asset model. - *ASSET_MODEL* – (default) An asset model that you can use to create assets. Can't be included as a component in another asset model. - *COMPONENT_MODEL* – A reusable component that you can include in the composite models of other asset models. You can't create assets directly from this type of asset model. - *INTERFACE* – An interface is a type of model that defines a standard structure that can be applied to different asset models.
        :param enforced_asset_model_interface_relationships: a list of asset model and interface relationships.
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_asset_model_mixin_props = iotsitewise_mixins.CfnAssetModelMixinProps(
                asset_model_composite_models=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelCompositeModelProperty(
                    composed_asset_model_id="composedAssetModelId",
                    composite_model_properties=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty(
                        data_type="dataType",
                        data_type_spec="dataTypeSpec",
                        external_id="externalId",
                        id="id",
                        logical_id="logicalId",
                        name="name",
                        type=iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                            attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                                default_value="defaultValue"
                            ),
                            metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                                expression="expression",
                                variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                        hierarchy_external_id="hierarchyExternalId",
                                        hierarchy_id="hierarchyId",
                                        hierarchy_logical_id="hierarchyLogicalId",
                                        property_external_id="propertyExternalId",
                                        property_id="propertyId",
                                        property_logical_id="propertyLogicalId",
                                        property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                            name="name"
                                        )]
                                    )
                                )],
                                window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                                    tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                        interval="interval",
                                        offset="offset"
                                    )
                                )
                            ),
                            transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                                expression="expression",
                                variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                        hierarchy_external_id="hierarchyExternalId",
                                        hierarchy_id="hierarchyId",
                                        hierarchy_logical_id="hierarchyLogicalId",
                                        property_external_id="propertyExternalId",
                                        property_id="propertyId",
                                        property_logical_id="propertyLogicalId",
                                        property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                            name="name"
                                        )]
                                    )
                                )]
                            ),
                            type_name="typeName"
                        ),
                        unit="unit"
                    )],
                    description="description",
                    external_id="externalId",
                    id="id",
                    name="name",
                    parent_asset_model_composite_model_external_id="parentAssetModelCompositeModelExternalId",
                    path=["path"],
                    type="type"
                )],
                asset_model_description="assetModelDescription",
                asset_model_external_id="assetModelExternalId",
                asset_model_hierarchies=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelHierarchyProperty(
                    child_asset_model_id="childAssetModelId",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    name="name"
                )],
                asset_model_name="assetModelName",
                asset_model_properties=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty(
                    data_type="dataType",
                    data_type_spec="dataTypeSpec",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    name="name",
                    type=iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                        attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                            default_value="defaultValue"
                        ),
                        metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                            expression="expression",
                            variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                    hierarchy_external_id="hierarchyExternalId",
                                    hierarchy_id="hierarchyId",
                                    hierarchy_logical_id="hierarchyLogicalId",
                                    property_external_id="propertyExternalId",
                                    property_id="propertyId",
                                    property_logical_id="propertyLogicalId",
                                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                        name="name"
                                    )]
                                )
                            )],
                            window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                                tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                    interval="interval",
                                    offset="offset"
                                )
                            )
                        ),
                        transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                            expression="expression",
                            variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                    hierarchy_external_id="hierarchyExternalId",
                                    hierarchy_id="hierarchyId",
                                    hierarchy_logical_id="hierarchyLogicalId",
                                    property_external_id="propertyExternalId",
                                    property_id="propertyId",
                                    property_logical_id="propertyLogicalId",
                                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                        name="name"
                                    )]
                                )
                            )]
                        ),
                        type_name="typeName"
                    ),
                    unit="unit"
                )],
                asset_model_type="assetModelType",
                enforced_asset_model_interface_relationships=[iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty(
                    interface_asset_model_id="interfaceAssetModelId",
                    property_mappings=[iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty(
                        asset_model_property_external_id="assetModelPropertyExternalId",
                        asset_model_property_logical_id="assetModelPropertyLogicalId",
                        interface_asset_model_property_external_id="interfaceAssetModelPropertyExternalId"
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aec01792f61cb9eb8d8bb3da9ff3a7175dbd936e61662af47a9cbba2c554114a)
            check_type(argname="argument asset_model_composite_models", value=asset_model_composite_models, expected_type=type_hints["asset_model_composite_models"])
            check_type(argname="argument asset_model_description", value=asset_model_description, expected_type=type_hints["asset_model_description"])
            check_type(argname="argument asset_model_external_id", value=asset_model_external_id, expected_type=type_hints["asset_model_external_id"])
            check_type(argname="argument asset_model_hierarchies", value=asset_model_hierarchies, expected_type=type_hints["asset_model_hierarchies"])
            check_type(argname="argument asset_model_name", value=asset_model_name, expected_type=type_hints["asset_model_name"])
            check_type(argname="argument asset_model_properties", value=asset_model_properties, expected_type=type_hints["asset_model_properties"])
            check_type(argname="argument asset_model_type", value=asset_model_type, expected_type=type_hints["asset_model_type"])
            check_type(argname="argument enforced_asset_model_interface_relationships", value=enforced_asset_model_interface_relationships, expected_type=type_hints["enforced_asset_model_interface_relationships"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_model_composite_models is not None:
            self._values["asset_model_composite_models"] = asset_model_composite_models
        if asset_model_description is not None:
            self._values["asset_model_description"] = asset_model_description
        if asset_model_external_id is not None:
            self._values["asset_model_external_id"] = asset_model_external_id
        if asset_model_hierarchies is not None:
            self._values["asset_model_hierarchies"] = asset_model_hierarchies
        if asset_model_name is not None:
            self._values["asset_model_name"] = asset_model_name
        if asset_model_properties is not None:
            self._values["asset_model_properties"] = asset_model_properties
        if asset_model_type is not None:
            self._values["asset_model_type"] = asset_model_type
        if enforced_asset_model_interface_relationships is not None:
            self._values["enforced_asset_model_interface_relationships"] = enforced_asset_model_interface_relationships
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_model_composite_models(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelCompositeModelProperty"]]]]:
        '''The composite models that are part of this asset model.

        It groups properties (such as attributes, measurements, transforms, and metrics) and child composite models that model parts of your industrial equipment. Each composite model has a type that defines the properties that the composite model supports. Use composite models to define alarms on this asset model.
        .. epigraph::

           When creating custom composite models, you need to use `CreateAssetModelCompositeModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_CreateAssetModelCompositeModel.html>`_ . For more information, see `Creating custom composite models (Components) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-custom-composite-models.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodels
        '''
        result = self._values.get("asset_model_composite_models")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelCompositeModelProperty"]]]], result)

    @builtins.property
    def asset_model_description(self) -> typing.Optional[builtins.str]:
        '''A description for the asset model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodeldescription
        '''
        result = self._values.get("asset_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_model_external_id(self) -> typing.Optional[builtins.str]:
        '''The external ID of the asset model.

        For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelexternalid
        '''
        result = self._values.get("asset_model_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_model_hierarchies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelHierarchyProperty"]]]]:
        '''The hierarchy definitions of the asset model.

        Each hierarchy specifies an asset model whose assets can be children of any other assets created from this asset model. For more information, see `Asset hierarchies <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

        You can specify up to 10 hierarchies per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelhierarchies
        '''
        result = self._values.get("asset_model_hierarchies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelHierarchyProperty"]]]], result)

    @builtins.property
    def asset_model_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the asset model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelname
        '''
        result = self._values.get("asset_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_model_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelPropertyProperty"]]]]:
        '''The property definitions of the asset model.

        For more information, see `Asset properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html>`_ in the *AWS IoT SiteWise User Guide* .

        You can specify up to 200 properties per asset model. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodelproperties
        '''
        result = self._values.get("asset_model_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelPropertyProperty"]]]], result)

    @builtins.property
    def asset_model_type(self) -> typing.Optional[builtins.str]:
        '''The type of asset model.

        - *ASSET_MODEL* – (default) An asset model that you can use to create assets. Can't be included as a component in another asset model.
        - *COMPONENT_MODEL* – A reusable component that you can include in the composite models of other asset models. You can't create assets directly from this type of asset model.
        - *INTERFACE* – An interface is a type of model that defines a standard structure that can be applied to different asset models.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-assetmodeltype
        '''
        result = self._values.get("asset_model_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforced_asset_model_interface_relationships(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty"]]]]:
        '''a list of asset model and interface relationships.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-enforcedassetmodelinterfacerelationships
        '''
        result = self._values.get("enforced_asset_model_interface_relationships")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html#cfn-iotsitewise-assetmodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssetModelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssetModelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin",
):
    '''Creates an asset model from specified property and hierarchy definitions.

    You create assets from asset models. With asset models, you can easily create assets of the same type that have standardized definitions. Each asset created from a model inherits the asset model's property and hierarchy definitions. For more information, see `Defining asset models <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/define-models.html>`_ in the *AWS IoT SiteWise User Guide* .

    You can create three types of asset models, ``ASSET_MODEL`` , ``COMPONENT_MODEL`` , or an ``INTERFACE`` .

    - *ASSET_MODEL* – (default) An asset model that you can use to create assets. Can't be included as a component in another asset model.
    - *COMPONENT_MODEL* – A reusable component that you can include in the composite models of other asset models. You can't create assets directly from this type of asset model.
    - *INTERFACE* – An interface is a type of model that defines a standard structure that can be applied to different asset models.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-assetmodel.html
    :cloudformationResource: AWS::IoTSiteWise::AssetModel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_asset_model_props_mixin = iotsitewise_mixins.CfnAssetModelPropsMixin(iotsitewise_mixins.CfnAssetModelMixinProps(
            asset_model_composite_models=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelCompositeModelProperty(
                composed_asset_model_id="composedAssetModelId",
                composite_model_properties=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty(
                    data_type="dataType",
                    data_type_spec="dataTypeSpec",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    name="name",
                    type=iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                        attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                            default_value="defaultValue"
                        ),
                        metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                            expression="expression",
                            variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                    hierarchy_external_id="hierarchyExternalId",
                                    hierarchy_id="hierarchyId",
                                    hierarchy_logical_id="hierarchyLogicalId",
                                    property_external_id="propertyExternalId",
                                    property_id="propertyId",
                                    property_logical_id="propertyLogicalId",
                                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                        name="name"
                                    )]
                                )
                            )],
                            window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                                tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                    interval="interval",
                                    offset="offset"
                                )
                            )
                        ),
                        transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                            expression="expression",
                            variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                    hierarchy_external_id="hierarchyExternalId",
                                    hierarchy_id="hierarchyId",
                                    hierarchy_logical_id="hierarchyLogicalId",
                                    property_external_id="propertyExternalId",
                                    property_id="propertyId",
                                    property_logical_id="propertyLogicalId",
                                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                        name="name"
                                    )]
                                )
                            )]
                        ),
                        type_name="typeName"
                    ),
                    unit="unit"
                )],
                description="description",
                external_id="externalId",
                id="id",
                name="name",
                parent_asset_model_composite_model_external_id="parentAssetModelCompositeModelExternalId",
                path=["path"],
                type="type"
            )],
            asset_model_description="assetModelDescription",
            asset_model_external_id="assetModelExternalId",
            asset_model_hierarchies=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelHierarchyProperty(
                child_asset_model_id="childAssetModelId",
                external_id="externalId",
                id="id",
                logical_id="logicalId",
                name="name"
            )],
            asset_model_name="assetModelName",
            asset_model_properties=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty(
                data_type="dataType",
                data_type_spec="dataTypeSpec",
                external_id="externalId",
                id="id",
                logical_id="logicalId",
                name="name",
                type=iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                    attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                        default_value="defaultValue"
                    ),
                    metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                        expression="expression",
                        variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                hierarchy_external_id="hierarchyExternalId",
                                hierarchy_id="hierarchyId",
                                hierarchy_logical_id="hierarchyLogicalId",
                                property_external_id="propertyExternalId",
                                property_id="propertyId",
                                property_logical_id="propertyLogicalId",
                                property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                    name="name"
                                )]
                            )
                        )],
                        window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                            tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                interval="interval",
                                offset="offset"
                            )
                        )
                    ),
                    transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                        expression="expression",
                        variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                hierarchy_external_id="hierarchyExternalId",
                                hierarchy_id="hierarchyId",
                                hierarchy_logical_id="hierarchyLogicalId",
                                property_external_id="propertyExternalId",
                                property_id="propertyId",
                                property_logical_id="propertyLogicalId",
                                property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                    name="name"
                                )]
                            )
                        )]
                    ),
                    type_name="typeName"
                ),
                unit="unit"
            )],
            asset_model_type="assetModelType",
            enforced_asset_model_interface_relationships=[iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty(
                interface_asset_model_id="interfaceAssetModelId",
                property_mappings=[iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty(
                    asset_model_property_external_id="assetModelPropertyExternalId",
                    asset_model_property_logical_id="assetModelPropertyLogicalId",
                    interface_asset_model_property_external_id="interfaceAssetModelPropertyExternalId"
                )]
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
        props: typing.Union[CfnAssetModelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::AssetModel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03848ea7301b041003f3f7926bb1f8acf7aa285754b17a42b10eafd646c2e4ff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11d9a3fb9b84ef29adaa2102a33cd31291f2e5e13c0caa4ddb11c85e5a365e2b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0178d116fa4d6a18e7c0f91d47f8f50e00283a0a319a720ae220ceeda0de369c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssetModelMixinProps:
        return typing.cast(CfnAssetModelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.AssetModelCompositeModelProperty",
        jsii_struct_bases=[],
        name_mapping={
            "composed_asset_model_id": "composedAssetModelId",
            "composite_model_properties": "compositeModelProperties",
            "description": "description",
            "external_id": "externalId",
            "id": "id",
            "name": "name",
            "parent_asset_model_composite_model_external_id": "parentAssetModelCompositeModelExternalId",
            "path": "path",
            "type": "type",
        },
    )
    class AssetModelCompositeModelProperty:
        def __init__(
            self,
            *,
            composed_asset_model_id: typing.Optional[builtins.str] = None,
            composite_model_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.AssetModelPropertyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            description: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            parent_asset_model_composite_model_external_id: typing.Optional[builtins.str] = None,
            path: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a composite model in an asset model.

            This object contains the asset property definitions that you define in the composite model.

            :param composed_asset_model_id: The ID of a component model which is reused to create this composite model.
            :param composite_model_properties: The asset property definitions for this composite model.
            :param description: The description of the composite model. .. epigraph:: If the composite model is a ``component-model-based`` composite model, the description is inherited from the ``COMPONENT_MODEL`` asset model and cannot be changed.
            :param external_id: The external ID of a composite model on this asset model. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* . .. epigraph:: One of ``ExternalId`` or ``Path`` must be specified.
            :param id: The ID of the asset model composite model. .. epigraph:: This is a return value and can't be set.
            :param name: The name of the composite model.
            :param parent_asset_model_composite_model_external_id: The external ID of the parent composite model. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            :param path: The structured path to the property from the root of the asset using property names. Path is used as the ID if the asset model is a derived composite model. .. epigraph:: One of ``ExternalId`` or ``Path`` must be specified.
            :param type: The type of the composite model. For alarm composite models, this type is ``AWS/ALARM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_model_composite_model_property = iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelCompositeModelProperty(
                    composed_asset_model_id="composedAssetModelId",
                    composite_model_properties=[iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty(
                        data_type="dataType",
                        data_type_spec="dataTypeSpec",
                        external_id="externalId",
                        id="id",
                        logical_id="logicalId",
                        name="name",
                        type=iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                            attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                                default_value="defaultValue"
                            ),
                            metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                                expression="expression",
                                variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                        hierarchy_external_id="hierarchyExternalId",
                                        hierarchy_id="hierarchyId",
                                        hierarchy_logical_id="hierarchyLogicalId",
                                        property_external_id="propertyExternalId",
                                        property_id="propertyId",
                                        property_logical_id="propertyLogicalId",
                                        property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                            name="name"
                                        )]
                                    )
                                )],
                                window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                                    tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                        interval="interval",
                                        offset="offset"
                                    )
                                )
                            ),
                            transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                                expression="expression",
                                variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                    name="name",
                                    value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                        hierarchy_external_id="hierarchyExternalId",
                                        hierarchy_id="hierarchyId",
                                        hierarchy_logical_id="hierarchyLogicalId",
                                        property_external_id="propertyExternalId",
                                        property_id="propertyId",
                                        property_logical_id="propertyLogicalId",
                                        property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                            name="name"
                                        )]
                                    )
                                )]
                            ),
                            type_name="typeName"
                        ),
                        unit="unit"
                    )],
                    description="description",
                    external_id="externalId",
                    id="id",
                    name="name",
                    parent_asset_model_composite_model_external_id="parentAssetModelCompositeModelExternalId",
                    path=["path"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a323731b49f95fc9d33b7bb9a49e5767e711b51410172e929430c142020ca6f0)
                check_type(argname="argument composed_asset_model_id", value=composed_asset_model_id, expected_type=type_hints["composed_asset_model_id"])
                check_type(argname="argument composite_model_properties", value=composite_model_properties, expected_type=type_hints["composite_model_properties"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument parent_asset_model_composite_model_external_id", value=parent_asset_model_composite_model_external_id, expected_type=type_hints["parent_asset_model_composite_model_external_id"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if composed_asset_model_id is not None:
                self._values["composed_asset_model_id"] = composed_asset_model_id
            if composite_model_properties is not None:
                self._values["composite_model_properties"] = composite_model_properties
            if description is not None:
                self._values["description"] = description
            if external_id is not None:
                self._values["external_id"] = external_id
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name
            if parent_asset_model_composite_model_external_id is not None:
                self._values["parent_asset_model_composite_model_external_id"] = parent_asset_model_composite_model_external_id
            if path is not None:
                self._values["path"] = path
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def composed_asset_model_id(self) -> typing.Optional[builtins.str]:
            '''The ID of a component model which is reused to create this composite model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-composedassetmodelid
            '''
            result = self._values.get("composed_asset_model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def composite_model_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelPropertyProperty"]]]]:
            '''The asset property definitions for this composite model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-compositemodelproperties
            '''
            result = self._values.get("composite_model_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AssetModelPropertyProperty"]]]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description of the composite model.

            .. epigraph::

               If the composite model is a ``component-model-based`` composite model, the description is inherited from the ``COMPONENT_MODEL`` asset model and cannot be changed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of a composite model on this asset model.

            For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            .. epigraph::

               One of ``ExternalId`` or ``Path`` must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset model composite model.

            .. epigraph::

               This is a return value and can't be set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the composite model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parent_asset_model_composite_model_external_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The external ID of the parent composite model.

            For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-parentassetmodelcompositemodelexternalid
            '''
            result = self._values.get("parent_asset_model_composite_model_external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The structured path to the property from the root of the asset using property names.

            Path is used as the ID if the asset model is a derived composite model.
            .. epigraph::

               One of ``ExternalId`` or ``Path`` must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the composite model.

            For alarm composite models, this type is ``AWS/ALARM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelcompositemodel.html#cfn-iotsitewise-assetmodel-assetmodelcompositemodel-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelCompositeModelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.AssetModelHierarchyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_asset_model_id": "childAssetModelId",
            "external_id": "externalId",
            "id": "id",
            "logical_id": "logicalId",
            "name": "name",
        },
    )
    class AssetModelHierarchyProperty:
        def __init__(
            self,
            *,
            child_asset_model_id: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            logical_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an asset hierarchy that contains a hierarchy's name, ID, and child asset model ID that specifies the type of asset that can be in this hierarchy.

            :param child_asset_model_id: The ID of the asset model, in UUID format. All assets in this hierarchy must be instances of the ``childAssetModelId`` asset model. AWS IoT SiteWise will always return the actual asset model ID for this value. However, when you are specifying this value as part of a call to `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ , you may provide either the asset model ID or else ``externalId:`` followed by the asset model's external ID. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            :param external_id: The external ID (if any) provided in the `CreateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_CreateAssetModel.html>`_ or `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ operation. You can assign an external ID by specifying this value as part of a call to `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ . However, you can't change the external ID if one is already assigned. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* . .. epigraph:: One of ``ExternalId`` or ``LogicalId`` must be specified.
            :param id: The ID of the asset model hierarchy. This ID is a ``hierarchyId`` . .. epigraph:: This is a return value and can't be set. - If you are callling `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ to create a *new* hierarchy: You can specify its ID here, if desired. AWS IoT SiteWise automatically generates a unique ID for you, so this parameter is never required. However, if you prefer to supply your own ID instead, you can specify it here in UUID format. If you specify your own ID, it must be globally unique. - If you are calling UpdateAssetModel to modify an *existing* hierarchy: This can be either the actual ID in UUID format, or else ``externalId:`` followed by the external ID, if it has one. For more information, see `Referencing objects with external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-id-references>`_ in the *AWS IoT SiteWise User Guide* .
            :param logical_id: The ``LogicalID`` of the asset model hierarchy. This ID is a ``hierarchyLogicalId`` . .. epigraph:: One of ``ExternalId`` or ``LogicalId`` must be specified.
            :param name: The name of the asset model hierarchy that you specify by using the `CreateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_CreateAssetModel.html>`_ or `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_model_hierarchy_property = iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelHierarchyProperty(
                    child_asset_model_id="childAssetModelId",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__86e5aad55f1fc50d6fdc90b86bf2e070c2f4c5d4d4e6e84070b7d15d565d840c)
                check_type(argname="argument child_asset_model_id", value=child_asset_model_id, expected_type=type_hints["child_asset_model_id"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if child_asset_model_id is not None:
                self._values["child_asset_model_id"] = child_asset_model_id
            if external_id is not None:
                self._values["external_id"] = external_id
            if id is not None:
                self._values["id"] = id
            if logical_id is not None:
                self._values["logical_id"] = logical_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def child_asset_model_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset model, in UUID format.

            All assets in this hierarchy must be instances of the ``childAssetModelId`` asset model. AWS IoT SiteWise will always return the actual asset model ID for this value. However, when you are specifying this value as part of a call to `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ , you may provide either the asset model ID or else ``externalId:`` followed by the asset model's external ID. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-childassetmodelid
            '''
            result = self._values.get("child_asset_model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID (if any) provided in the `CreateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_CreateAssetModel.html>`_ or `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ operation. You can assign an external ID by specifying this value as part of a call to `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ . However, you can't change the external ID if one is already assigned. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            .. epigraph::

               One of ``ExternalId`` or ``LogicalId`` must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset model hierarchy. This ID is a ``hierarchyId`` .

            .. epigraph::

               This is a return value and can't be set.

            - If you are callling `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ to create a *new* hierarchy: You can specify its ID here, if desired. AWS IoT SiteWise automatically generates a unique ID for you, so this parameter is never required. However, if you prefer to supply your own ID instead, you can specify it here in UUID format. If you specify your own ID, it must be globally unique.
            - If you are calling UpdateAssetModel to modify an *existing* hierarchy: This can be either the actual ID in UUID format, or else ``externalId:`` followed by the external ID, if it has one. For more information, see `Referencing objects with external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-id-references>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_id(self) -> typing.Optional[builtins.str]:
            '''The ``LogicalID`` of the asset model hierarchy. This ID is a ``hierarchyLogicalId`` .

            .. epigraph::

               One of ``ExternalId`` or ``LogicalId`` must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-logicalid
            '''
            result = self._values.get("logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the asset model hierarchy that you specify by using the `CreateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_CreateAssetModel.html>`_ or `UpdateAssetModel <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_UpdateAssetModel.html>`_ API operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelhierarchy.html#cfn-iotsitewise-assetmodel-assetmodelhierarchy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelHierarchyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_type": "dataType",
            "data_type_spec": "dataTypeSpec",
            "external_id": "externalId",
            "id": "id",
            "logical_id": "logicalId",
            "name": "name",
            "type": "type",
            "unit": "unit",
        },
    )
    class AssetModelPropertyProperty:
        def __init__(
            self,
            *,
            data_type: typing.Optional[builtins.str] = None,
            data_type_spec: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            logical_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.PropertyTypeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an asset model property.

            :param data_type: The data type of the asset model property. If you specify ``STRUCT`` , you must also specify ``dataTypeSpec`` to identify the type of the structure for this property.
            :param data_type_spec: The data type of the structure for this property. This parameter exists on properties that have the ``STRUCT`` data type.
            :param external_id: The external ID of the asset property. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* . .. epigraph:: One of ``ExternalId`` or ``LogicalId`` must be specified.
            :param id: The ID of the property. .. epigraph:: This is a return value and can't be set.
            :param logical_id: The ``LogicalID`` of the asset model property. .. epigraph:: One of ``ExternalId`` or ``LogicalId`` must be specified.
            :param name: The name of the asset model property.
            :param type: Contains a property type, which can be one of ``attribute`` , ``measurement`` , ``metric`` , or ``transform`` .
            :param unit: The unit of the asset model property, such as ``Newtons`` or ``RPM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_model_property_property = iotsitewise_mixins.CfnAssetModelPropsMixin.AssetModelPropertyProperty(
                    data_type="dataType",
                    data_type_spec="dataTypeSpec",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    name="name",
                    type=iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                        attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                            default_value="defaultValue"
                        ),
                        metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                            expression="expression",
                            variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                    hierarchy_external_id="hierarchyExternalId",
                                    hierarchy_id="hierarchyId",
                                    hierarchy_logical_id="hierarchyLogicalId",
                                    property_external_id="propertyExternalId",
                                    property_id="propertyId",
                                    property_logical_id="propertyLogicalId",
                                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                        name="name"
                                    )]
                                )
                            )],
                            window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                                tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                    interval="interval",
                                    offset="offset"
                                )
                            )
                        ),
                        transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                            expression="expression",
                            variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                                name="name",
                                value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                    hierarchy_external_id="hierarchyExternalId",
                                    hierarchy_id="hierarchyId",
                                    hierarchy_logical_id="hierarchyLogicalId",
                                    property_external_id="propertyExternalId",
                                    property_id="propertyId",
                                    property_logical_id="propertyLogicalId",
                                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                        name="name"
                                    )]
                                )
                            )]
                        ),
                        type_name="typeName"
                    ),
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__24c2297ac18add804df77cc24025c4e967eab3aa8f1a1ca94ac6d33926c98422)
                check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
                check_type(argname="argument data_type_spec", value=data_type_spec, expected_type=type_hints["data_type_spec"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_type is not None:
                self._values["data_type"] = data_type
            if data_type_spec is not None:
                self._values["data_type_spec"] = data_type_spec
            if external_id is not None:
                self._values["external_id"] = external_id
            if id is not None:
                self._values["id"] = id
            if logical_id is not None:
                self._values["logical_id"] = logical_id
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def data_type(self) -> typing.Optional[builtins.str]:
            '''The data type of the asset model property.

            If you specify ``STRUCT`` , you must also specify ``dataTypeSpec`` to identify the type of the structure for this property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-datatype
            '''
            result = self._values.get("data_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_type_spec(self) -> typing.Optional[builtins.str]:
            '''The data type of the structure for this property.

            This parameter exists on properties that have the ``STRUCT`` data type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-datatypespec
            '''
            result = self._values.get("data_type_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of the asset property.

            For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            .. epigraph::

               One of ``ExternalId`` or ``LogicalId`` must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the property.

            .. epigraph::

               This is a return value and can't be set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_id(self) -> typing.Optional[builtins.str]:
            '''The ``LogicalID`` of the asset model property.

            .. epigraph::

               One of ``ExternalId`` or ``LogicalId`` must be specified.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-logicalid
            '''
            result = self._values.get("logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the asset model property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.PropertyTypeProperty"]]:
            '''Contains a property type, which can be one of ``attribute`` , ``measurement`` , ``metric`` , or ``transform`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.PropertyTypeProperty"]], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit of the asset model property, such as ``Newtons`` or ``RPM`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-assetmodelproperty.html#cfn-iotsitewise-assetmodel-assetmodelproperty-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.AttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"default_value": "defaultValue"},
    )
    class AttributeProperty:
        def __init__(
            self,
            *,
            default_value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains an asset attribute property.

            For more information, see `Attributes <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html#attributes>`_ in the *AWS IoT SiteWise User Guide* .

            :param default_value: The default value of the asset model property attribute. All assets that you create from the asset model contain this attribute value. You can update an attribute's value after you create an asset. For more information, see `Updating attribute values <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/update-attribute-values.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-attribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                attribute_property = iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                    default_value="defaultValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0724e3693b16652c412c1720ac26bebf81113b22b527e6313f4fe1f402ceb845)
                check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_value is not None:
                self._values["default_value"] = default_value

        @builtins.property
        def default_value(self) -> typing.Optional[builtins.str]:
            '''The default value of the asset model property attribute.

            All assets that you create from the asset model contain this attribute value. You can update an attribute's value after you create an asset. For more information, see `Updating attribute values <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/update-attribute-values.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-attribute.html#cfn-iotsitewise-assetmodel-attribute-defaultvalue
            '''
            result = self._values.get("default_value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asset_model_property_external_id": "assetModelPropertyExternalId",
            "asset_model_property_logical_id": "assetModelPropertyLogicalId",
            "interface_asset_model_property_external_id": "interfaceAssetModelPropertyExternalId",
        },
    )
    class EnforcedAssetModelInterfacePropertyMappingProperty:
        def __init__(
            self,
            *,
            asset_model_property_external_id: typing.Optional[builtins.str] = None,
            asset_model_property_logical_id: typing.Optional[builtins.str] = None,
            interface_asset_model_property_external_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about applied interface property and asset model property.

            :param asset_model_property_external_id: The external ID of the linked asset model property.
            :param asset_model_property_logical_id: The logical ID of the linked asset model property.
            :param interface_asset_model_property_external_id: The external ID of the applied interface property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                enforced_asset_model_interface_property_mapping_property = iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty(
                    asset_model_property_external_id="assetModelPropertyExternalId",
                    asset_model_property_logical_id="assetModelPropertyLogicalId",
                    interface_asset_model_property_external_id="interfaceAssetModelPropertyExternalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a7888f86aeb21200298f28694fba2f1c73644a3d2d1aedc32b72996855fa152f)
                check_type(argname="argument asset_model_property_external_id", value=asset_model_property_external_id, expected_type=type_hints["asset_model_property_external_id"])
                check_type(argname="argument asset_model_property_logical_id", value=asset_model_property_logical_id, expected_type=type_hints["asset_model_property_logical_id"])
                check_type(argname="argument interface_asset_model_property_external_id", value=interface_asset_model_property_external_id, expected_type=type_hints["interface_asset_model_property_external_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_model_property_external_id is not None:
                self._values["asset_model_property_external_id"] = asset_model_property_external_id
            if asset_model_property_logical_id is not None:
                self._values["asset_model_property_logical_id"] = asset_model_property_logical_id
            if interface_asset_model_property_external_id is not None:
                self._values["interface_asset_model_property_external_id"] = interface_asset_model_property_external_id

        @builtins.property
        def asset_model_property_external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of the linked asset model property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping.html#cfn-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping-assetmodelpropertyexternalid
            '''
            result = self._values.get("asset_model_property_external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def asset_model_property_logical_id(self) -> typing.Optional[builtins.str]:
            '''The logical ID of the linked asset model property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping.html#cfn-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping-assetmodelpropertylogicalid
            '''
            result = self._values.get("asset_model_property_logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def interface_asset_model_property_external_id(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The external ID of the applied interface property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping.html#cfn-iotsitewise-assetmodel-enforcedassetmodelinterfacepropertymapping-interfaceassetmodelpropertyexternalid
            '''
            result = self._values.get("interface_asset_model_property_external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnforcedAssetModelInterfacePropertyMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty",
        jsii_struct_bases=[],
        name_mapping={
            "interface_asset_model_id": "interfaceAssetModelId",
            "property_mappings": "propertyMappings",
        },
    )
    class EnforcedAssetModelInterfaceRelationshipProperty:
        def __init__(
            self,
            *,
            interface_asset_model_id: typing.Optional[builtins.str] = None,
            property_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information about applied interface hierarchy and asset model hierarchy.

            :param interface_asset_model_id: The ID of the asset model that has the interface applied to it.
            :param property_mappings: A list of property mappings between the interface asset model and the asset model where the interface is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacerelationship.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                enforced_asset_model_interface_relationship_property = iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty(
                    interface_asset_model_id="interfaceAssetModelId",
                    property_mappings=[iotsitewise_mixins.CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty(
                        asset_model_property_external_id="assetModelPropertyExternalId",
                        asset_model_property_logical_id="assetModelPropertyLogicalId",
                        interface_asset_model_property_external_id="interfaceAssetModelPropertyExternalId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff3043c6e7b68bc121ebc6e8528c0392375786157417455fec6c944c960b18f9)
                check_type(argname="argument interface_asset_model_id", value=interface_asset_model_id, expected_type=type_hints["interface_asset_model_id"])
                check_type(argname="argument property_mappings", value=property_mappings, expected_type=type_hints["property_mappings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interface_asset_model_id is not None:
                self._values["interface_asset_model_id"] = interface_asset_model_id
            if property_mappings is not None:
                self._values["property_mappings"] = property_mappings

        @builtins.property
        def interface_asset_model_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset model that has the interface applied to it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacerelationship.html#cfn-iotsitewise-assetmodel-enforcedassetmodelinterfacerelationship-interfaceassetmodelid
            '''
            result = self._values.get("interface_asset_model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty"]]]]:
            '''A list of property mappings between the interface asset model and the asset model where the interface is applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-enforcedassetmodelinterfacerelationship.html#cfn-iotsitewise-assetmodel-enforcedassetmodelinterfacerelationship-propertymappings
            '''
            result = self._values.get("property_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnforcedAssetModelInterfaceRelationshipProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ExpressionVariableProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.VariableValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains expression variable information.

            :param name: The friendly name of the variable to be used in the expression.
            :param value: The variable that identifies an asset property from which to use values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                expression_variable_property = iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                    name="name",
                    value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                        hierarchy_external_id="hierarchyExternalId",
                        hierarchy_id="hierarchyId",
                        hierarchy_logical_id="hierarchyLogicalId",
                        property_external_id="propertyExternalId",
                        property_id="propertyId",
                        property_logical_id="propertyLogicalId",
                        property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                            name="name"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d9c8da0b975dd29e1ac642001998703f4dcc8c15e9bf05203079cd8a19300883)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The friendly name of the variable to be used in the expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html#cfn-iotsitewise-assetmodel-expressionvariable-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.VariableValueProperty"]]:
            '''The variable that identifies an asset property from which to use values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-expressionvariable.html#cfn-iotsitewise-assetmodel-expressionvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.VariableValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpressionVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.MetricProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "variables": "variables",
            "window": "window",
        },
    )
    class MetricProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.ExpressionVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.MetricWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains an asset metric property.

            With metrics, you can calculate aggregate functions, such as an average, maximum, or minimum, as specified through an expression. A metric maps several values to a single value (such as a sum).

            The maximum number of dependent/cascading variables used in any one metric calculation is 10. Therefore, a *root* metric can have up to 10 cascading metrics in its computational dependency tree. Additionally, a metric can only have a data type of ``DOUBLE`` and consume properties with data types of ``INTEGER`` or ``DOUBLE`` .

            For more information, see `Metrics <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html#metrics>`_ in the *AWS IoT SiteWise User Guide* .

            :param expression: The mathematical expression that defines the metric aggregation function. You can specify up to 10 variables per expression. You can specify up to 10 functions per expression. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param variables: The list of variables used in the expression.
            :param window: The window (time interval) over which AWS IoT SiteWise computes the metric's aggregation expression. AWS IoT SiteWise computes one data point per ``window`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                metric_property = iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                    expression="expression",
                    variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                        name="name",
                        value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                            hierarchy_external_id="hierarchyExternalId",
                            hierarchy_id="hierarchyId",
                            hierarchy_logical_id="hierarchyLogicalId",
                            property_external_id="propertyExternalId",
                            property_id="propertyId",
                            property_logical_id="propertyLogicalId",
                            property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                name="name"
                            )]
                        )
                    )],
                    window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                        tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                            interval="interval",
                            offset="offset"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b07089c907e8797833da848d36c129da00f8d686b46f28db24edfa8ddb6f9c55)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
                check_type(argname="argument window", value=window, expected_type=type_hints["window"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if variables is not None:
                self._values["variables"] = variables
            if window is not None:
                self._values["window"] = window

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The mathematical expression that defines the metric aggregation function.

            You can specify up to 10 variables per expression. You can specify up to 10 functions per expression.

            For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.ExpressionVariableProperty"]]]]:
            '''The list of variables used in the expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.ExpressionVariableProperty"]]]], result)

        @builtins.property
        def window(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.MetricWindowProperty"]]:
            '''The window (time interval) over which AWS IoT SiteWise computes the metric's aggregation expression.

            AWS IoT SiteWise computes one data point per ``window`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metric.html#cfn-iotsitewise-assetmodel-metric-window
            '''
            result = self._values.get("window")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.MetricWindowProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.MetricWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"tumbling": "tumbling"},
    )
    class MetricWindowProperty:
        def __init__(
            self,
            *,
            tumbling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.TumblingWindowProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains a time interval window used for data aggregate computations (for example, average, sum, count, and so on).

            :param tumbling: The tumbling time interval window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metricwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                metric_window_property = iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                    tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                        interval="interval",
                        offset="offset"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b44ddee2b61caf8d0989ff10881efb65ee5d6927daf7c3810dac1269fe9f37a)
                check_type(argname="argument tumbling", value=tumbling, expected_type=type_hints["tumbling"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tumbling is not None:
                self._values["tumbling"] = tumbling

        @builtins.property
        def tumbling(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.TumblingWindowProperty"]]:
            '''The tumbling time interval window.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-metricwindow.html#cfn-iotsitewise-assetmodel-metricwindow-tumbling
            '''
            result = self._values.get("tumbling")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.TumblingWindowProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetricWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class PropertyPathDefinitionProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''Represents one level between a composite model and the root of the asset model.

            :param name: The name of the path segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertypathdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                property_path_definition_property = iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78ac092b6ca433f8fd73170ab9841eccaf9332745dce487813f88d9a1052ef1d)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the path segment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertypathdefinition.html#cfn-iotsitewise-assetmodel-propertypathdefinition-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyPathDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.PropertyTypeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute": "attribute",
            "metric": "metric",
            "transform": "transform",
            "type_name": "typeName",
        },
    )
    class PropertyTypeProperty:
        def __init__(
            self,
            *,
            attribute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.AttributeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.MetricProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.TransformProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains a property type, which can be one of ``attribute`` , ``measurement`` , ``metric`` , or ``transform`` .

            :param attribute: Specifies an asset attribute property. An attribute generally contains static information, such as the serial number of an `IIoT <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Internet_of_things#Industrial_applications>`_ wind turbine.
            :param metric: Specifies an asset metric property. A metric contains a mathematical expression that uses aggregate functions to process all input data points over a time interval and output a single data point, such as to calculate the average hourly temperature.
            :param transform: Specifies an asset transform property. A transform contains a mathematical expression that maps a property's data points from one form to another, such as a unit conversion from Celsius to Fahrenheit.
            :param type_name: The type of property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                property_type_property = iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyTypeProperty(
                    attribute=iotsitewise_mixins.CfnAssetModelPropsMixin.AttributeProperty(
                        default_value="defaultValue"
                    ),
                    metric=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricProperty(
                        expression="expression",
                        variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                hierarchy_external_id="hierarchyExternalId",
                                hierarchy_id="hierarchyId",
                                hierarchy_logical_id="hierarchyLogicalId",
                                property_external_id="propertyExternalId",
                                property_id="propertyId",
                                property_logical_id="propertyLogicalId",
                                property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                    name="name"
                                )]
                            )
                        )],
                        window=iotsitewise_mixins.CfnAssetModelPropsMixin.MetricWindowProperty(
                            tumbling=iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                                interval="interval",
                                offset="offset"
                            )
                        )
                    ),
                    transform=iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                        expression="expression",
                        variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                            name="name",
                            value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                                hierarchy_external_id="hierarchyExternalId",
                                hierarchy_id="hierarchyId",
                                hierarchy_logical_id="hierarchyLogicalId",
                                property_external_id="propertyExternalId",
                                property_id="propertyId",
                                property_logical_id="propertyLogicalId",
                                property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                    name="name"
                                )]
                            )
                        )]
                    ),
                    type_name="typeName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa1425c9072cde93d5f33638362cfe23804d02af310d22c6c04c1428bfd7edcc)
                check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
                check_type(argname="argument metric", value=metric, expected_type=type_hints["metric"])
                check_type(argname="argument transform", value=transform, expected_type=type_hints["transform"])
                check_type(argname="argument type_name", value=type_name, expected_type=type_hints["type_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute is not None:
                self._values["attribute"] = attribute
            if metric is not None:
                self._values["metric"] = metric
            if transform is not None:
                self._values["transform"] = transform
            if type_name is not None:
                self._values["type_name"] = type_name

        @builtins.property
        def attribute(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AttributeProperty"]]:
            '''Specifies an asset attribute property.

            An attribute generally contains static information, such as the serial number of an `IIoT <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Internet_of_things#Industrial_applications>`_ wind turbine.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-attribute
            '''
            result = self._values.get("attribute")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.AttributeProperty"]], result)

        @builtins.property
        def metric(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.MetricProperty"]]:
            '''Specifies an asset metric property.

            A metric contains a mathematical expression that uses aggregate functions to process all input data points over a time interval and output a single data point, such as to calculate the average hourly temperature.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-metric
            '''
            result = self._values.get("metric")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.MetricProperty"]], result)

        @builtins.property
        def transform(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.TransformProperty"]]:
            '''Specifies an asset transform property.

            A transform contains a mathematical expression that maps a property's data points from one form to another, such as a unit conversion from Celsius to Fahrenheit.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-transform
            '''
            result = self._values.get("transform")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.TransformProperty"]], result)

        @builtins.property
        def type_name(self) -> typing.Optional[builtins.str]:
            '''The type of property type, which can be one of ``Attribute`` , ``Measurement`` , ``Metric`` , or ``Transform`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-propertytype.html#cfn-iotsitewise-assetmodel-propertytype-typename
            '''
            result = self._values.get("type_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertyTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.TransformProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "variables": "variables"},
    )
    class TransformProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.ExpressionVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains an asset transform property.

            A transform is a one-to-one mapping of a property's data points from one form to another. For example, you can use a transform to convert a Celsius data stream to Fahrenheit by applying the transformation expression to each data point of the Celsius stream. A transform can only have a data type of ``DOUBLE`` and consume properties with data types of ``INTEGER`` or ``DOUBLE`` .

            For more information, see `Transforms <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-properties.html#transforms>`_ in the *AWS IoT SiteWise User Guide* .

            :param expression: The mathematical expression that defines the transformation function. You can specify up to 10 variables per expression. You can specify up to 10 functions per expression. For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param variables: The list of variables used in the expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                transform_property = iotsitewise_mixins.CfnAssetModelPropsMixin.TransformProperty(
                    expression="expression",
                    variables=[iotsitewise_mixins.CfnAssetModelPropsMixin.ExpressionVariableProperty(
                        name="name",
                        value=iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                            hierarchy_external_id="hierarchyExternalId",
                            hierarchy_id="hierarchyId",
                            hierarchy_logical_id="hierarchyLogicalId",
                            property_external_id="propertyExternalId",
                            property_id="propertyId",
                            property_logical_id="propertyLogicalId",
                            property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                                name="name"
                            )]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c972e66e1fbe917365587c44ea9e1522a725575d1a05bb8dbe0657ee15b990ae)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument variables", value=variables, expected_type=type_hints["variables"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if variables is not None:
                self._values["variables"] = variables

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The mathematical expression that defines the transformation function.

            You can specify up to 10 variables per expression. You can specify up to 10 functions per expression.

            For more information, see `Quotas <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/quotas.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html#cfn-iotsitewise-assetmodel-transform-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.ExpressionVariableProperty"]]]]:
            '''The list of variables used in the expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-transform.html#cfn-iotsitewise-assetmodel-transform-variables
            '''
            result = self._values.get("variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.ExpressionVariableProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TransformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.TumblingWindowProperty",
        jsii_struct_bases=[],
        name_mapping={"interval": "interval", "offset": "offset"},
    )
    class TumblingWindowProperty:
        def __init__(
            self,
            *,
            interval: typing.Optional[builtins.str] = None,
            offset: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains a tumbling window, which is a repeating fixed-sized, non-overlapping, and contiguous time window.

            You can use this window in metrics to aggregate data from properties and other assets.

            You can use ``m`` , ``h`` , ``d`` , and ``w`` when you specify an interval or offset. Note that ``m`` represents minutes, ``h`` represents hours, ``d`` represents days, and ``w`` represents weeks. You can also use ``s`` to represent seconds in ``offset`` .

            The ``interval`` and ``offset`` parameters support the `ISO 8601 format <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/ISO_8601>`_ . For example, ``PT5S`` represents 5 seconds, ``PT5M`` represents 5 minutes, and ``PT5H`` represents 5 hours.

            :param interval: The time interval for the tumbling window. The interval time must be between 1 minute and 1 week. AWS IoT SiteWise computes the ``1w`` interval the end of Sunday at midnight each week (UTC), the ``1d`` interval at the end of each day at midnight (UTC), the ``1h`` interval at the end of each hour, and so on. When AWS IoT SiteWise aggregates data points for metric computations, the start of each interval is exclusive and the end of each interval is inclusive. AWS IoT SiteWise places the computed data point at the end of the interval.
            :param offset: The offset for the tumbling window. The ``offset`` parameter accepts the following:. - The offset time. For example, if you specify ``18h`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways: - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric. - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day. - The ISO 8601 format. For example, if you specify ``PT18H`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways: - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric. - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day. - The 24-hour clock. For example, if you specify ``00:03:00`` for ``offset`` , ``5m`` for ``interval`` , and you create the metric at 2 PM (UTC), you get the first aggregation result at 2:03 PM (UTC). You get the second aggregation result at 2:08 PM (UTC). - The offset time zone. For example, if you specify ``2021-07-23T18:00-08`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways: - If you create the metric before or at 6 PM (PST), you get the first aggregation result at 6 PM (PST) on the day when you create the metric. - If you create the metric after 6 PM (PST), you get the first aggregation result at 6 PM (PST) the next day.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                tumbling_window_property = iotsitewise_mixins.CfnAssetModelPropsMixin.TumblingWindowProperty(
                    interval="interval",
                    offset="offset"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e64a9d184207666a72082862697e9685e593a66c078eb8373f740186599be9f)
                check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
                check_type(argname="argument offset", value=offset, expected_type=type_hints["offset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if interval is not None:
                self._values["interval"] = interval
            if offset is not None:
                self._values["offset"] = offset

        @builtins.property
        def interval(self) -> typing.Optional[builtins.str]:
            '''The time interval for the tumbling window. The interval time must be between 1 minute and 1 week.

            AWS IoT SiteWise computes the ``1w`` interval the end of Sunday at midnight each week (UTC), the ``1d`` interval at the end of each day at midnight (UTC), the ``1h`` interval at the end of each hour, and so on.

            When AWS IoT SiteWise aggregates data points for metric computations, the start of each interval is exclusive and the end of each interval is inclusive. AWS IoT SiteWise places the computed data point at the end of the interval.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html#cfn-iotsitewise-assetmodel-tumblingwindow-interval
            '''
            result = self._values.get("interval")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def offset(self) -> typing.Optional[builtins.str]:
            '''The offset for the tumbling window. The ``offset`` parameter accepts the following:.

            - The offset time.

            For example, if you specify ``18h`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways:

            - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric.
            - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day.
            - The ISO 8601 format.

            For example, if you specify ``PT18H`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways:

            - If you create the metric before or at 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) on the day when you create the metric.
            - If you create the metric after 6 PM (UTC), you get the first aggregation result at 6 PM (UTC) the next day.
            - The 24-hour clock.

            For example, if you specify ``00:03:00`` for ``offset`` , ``5m`` for ``interval`` , and you create the metric at 2 PM (UTC), you get the first aggregation result at 2:03 PM (UTC). You get the second aggregation result at 2:08 PM (UTC).

            - The offset time zone.

            For example, if you specify ``2021-07-23T18:00-08`` for ``offset`` and ``1d`` for ``interval`` , AWS IoT SiteWise aggregates data in one of the following ways:

            - If you create the metric before or at 6 PM (PST), you get the first aggregation result at 6 PM (PST) on the day when you create the metric.
            - If you create the metric after 6 PM (PST), you get the first aggregation result at 6 PM (PST) the next day.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-tumblingwindow.html#cfn-iotsitewise-assetmodel-tumblingwindow-offset
            '''
            result = self._values.get("offset")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TumblingWindowProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetModelPropsMixin.VariableValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hierarchy_external_id": "hierarchyExternalId",
            "hierarchy_id": "hierarchyId",
            "hierarchy_logical_id": "hierarchyLogicalId",
            "property_external_id": "propertyExternalId",
            "property_id": "propertyId",
            "property_logical_id": "propertyLogicalId",
            "property_path": "propertyPath",
        },
    )
    class VariableValueProperty:
        def __init__(
            self,
            *,
            hierarchy_external_id: typing.Optional[builtins.str] = None,
            hierarchy_id: typing.Optional[builtins.str] = None,
            hierarchy_logical_id: typing.Optional[builtins.str] = None,
            property_external_id: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
            property_logical_id: typing.Optional[builtins.str] = None,
            property_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAssetModelPropsMixin.PropertyPathDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Identifies a property value used in an expression.

            :param hierarchy_external_id: The external ID of the hierarchy being referenced. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            :param hierarchy_id: The ID of the hierarchy to query for the property ID. You can use the hierarchy's name instead of the hierarchy's ID. If the hierarchy has an external ID, you can specify ``externalId:`` followed by the external ID. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* . You use a hierarchy ID instead of a model ID because you can have several hierarchies using the same model and therefore the same ``propertyId`` . For example, you might have separately grouped assets that come from the same asset model. For more information, see `Asset hierarchies <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param hierarchy_logical_id: The ``LogicalID`` of the hierarchy to query for the ``PropertyLogicalID`` . You use a ``hierarchyLogicalID`` instead of a model ID because you can have several hierarchies using the same model and therefore the same property. For example, you might have separately grouped assets that come from the same asset model. For more information, see `Defining relationships between asset models (hierarchies) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param property_external_id: The external ID of the property being referenced. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            :param property_id: The ID of the property to use as the variable. You can use the property ``name`` if it's from the same asset model. If the property has an external ID, you can specify ``externalId:`` followed by the external ID. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* . .. epigraph:: This is a return value and can't be set.
            :param property_logical_id: The ``LogicalID`` of the property that is being referenced.
            :param property_path: The path of the property. Each step of the path is the name of the step. See the following example: ``PropertyPath: Name: AssetModelName Name: Composite1 Name: NestedComposite``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                variable_value_property = iotsitewise_mixins.CfnAssetModelPropsMixin.VariableValueProperty(
                    hierarchy_external_id="hierarchyExternalId",
                    hierarchy_id="hierarchyId",
                    hierarchy_logical_id="hierarchyLogicalId",
                    property_external_id="propertyExternalId",
                    property_id="propertyId",
                    property_logical_id="propertyLogicalId",
                    property_path=[iotsitewise_mixins.CfnAssetModelPropsMixin.PropertyPathDefinitionProperty(
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fad675896dbae731730632b6365b4d627e68db8784987d5472971c879725de68)
                check_type(argname="argument hierarchy_external_id", value=hierarchy_external_id, expected_type=type_hints["hierarchy_external_id"])
                check_type(argname="argument hierarchy_id", value=hierarchy_id, expected_type=type_hints["hierarchy_id"])
                check_type(argname="argument hierarchy_logical_id", value=hierarchy_logical_id, expected_type=type_hints["hierarchy_logical_id"])
                check_type(argname="argument property_external_id", value=property_external_id, expected_type=type_hints["property_external_id"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
                check_type(argname="argument property_logical_id", value=property_logical_id, expected_type=type_hints["property_logical_id"])
                check_type(argname="argument property_path", value=property_path, expected_type=type_hints["property_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if hierarchy_external_id is not None:
                self._values["hierarchy_external_id"] = hierarchy_external_id
            if hierarchy_id is not None:
                self._values["hierarchy_id"] = hierarchy_id
            if hierarchy_logical_id is not None:
                self._values["hierarchy_logical_id"] = hierarchy_logical_id
            if property_external_id is not None:
                self._values["property_external_id"] = property_external_id
            if property_id is not None:
                self._values["property_id"] = property_id
            if property_logical_id is not None:
                self._values["property_logical_id"] = property_logical_id
            if property_path is not None:
                self._values["property_path"] = property_path

        @builtins.property
        def hierarchy_external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of the hierarchy being referenced.

            For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-hierarchyexternalid
            '''
            result = self._values.get("hierarchy_external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hierarchy to query for the property ID.

            You can use the hierarchy's name instead of the hierarchy's ID. If the hierarchy has an external ID, you can specify ``externalId:`` followed by the external ID. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            You use a hierarchy ID instead of a model ID because you can have several hierarchies using the same model and therefore the same ``propertyId`` . For example, you might have separately grouped assets that come from the same asset model. For more information, see `Asset hierarchies <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-hierarchyid
            '''
            result = self._values.get("hierarchy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hierarchy_logical_id(self) -> typing.Optional[builtins.str]:
            '''The ``LogicalID`` of the hierarchy to query for the ``PropertyLogicalID`` .

            You use a ``hierarchyLogicalID`` instead of a model ID because you can have several hierarchies using the same model and therefore the same property. For example, you might have separately grouped assets that come from the same asset model. For more information, see `Defining relationships between asset models (hierarchies) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/asset-hierarchies.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-hierarchylogicalid
            '''
            result = self._values.get("hierarchy_logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of the property being referenced.

            For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-propertyexternalid
            '''
            result = self._values.get("property_external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the property to use as the variable.

            You can use the property ``name`` if it's from the same asset model. If the property has an external ID, you can specify ``externalId:`` followed by the external ID. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            .. epigraph::

               This is a return value and can't be set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_logical_id(self) -> typing.Optional[builtins.str]:
            '''The ``LogicalID`` of the property that is being referenced.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-propertylogicalid
            '''
            result = self._values.get("property_logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.PropertyPathDefinitionProperty"]]]]:
            '''The path of the property.

            Each step of the path is the name of the step. See the following example:

            ``PropertyPath: Name: AssetModelName Name: Composite1 Name: NestedComposite``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-assetmodel-variablevalue.html#cfn-iotsitewise-assetmodel-variablevalue-propertypath
            '''
            result = self._values.get("property_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAssetModelPropsMixin.PropertyPathDefinitionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VariableValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnAssetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetPropsMixin",
):
    '''Creates an asset from an existing asset model.

    For more information, see `Creating assets <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-assets.html>`_ in the *AWS IoT SiteWise User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-asset.html
    :cloudformationResource: AWS::IoTSiteWise::Asset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_asset_props_mixin = iotsitewise_mixins.CfnAssetPropsMixin(iotsitewise_mixins.CfnAssetMixinProps(
            asset_description="assetDescription",
            asset_external_id="assetExternalId",
            asset_hierarchies=[iotsitewise_mixins.CfnAssetPropsMixin.AssetHierarchyProperty(
                child_asset_id="childAssetId",
                external_id="externalId",
                id="id",
                logical_id="logicalId"
            )],
            asset_model_id="assetModelId",
            asset_name="assetName",
            asset_properties=[iotsitewise_mixins.CfnAssetPropsMixin.AssetPropertyProperty(
                alias="alias",
                external_id="externalId",
                id="id",
                logical_id="logicalId",
                notification_state="notificationState",
                unit="unit"
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
        props: typing.Union[CfnAssetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::Asset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e67f68deb0bfbe05f1019ab5997304c5755c2a146896fa04a762508db186604)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ca71fb8e4955facfc28b5495be55e909286fc0b26a462d001eb38ab4bf88991)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93080cac718b60e9b1394c30d673ecae46d26a13fbbc10297dce0e03affb1574)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssetMixinProps:
        return typing.cast(CfnAssetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetPropsMixin.AssetHierarchyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "child_asset_id": "childAssetId",
            "external_id": "externalId",
            "id": "id",
            "logical_id": "logicalId",
        },
    )
    class AssetHierarchyProperty:
        def __init__(
            self,
            *,
            child_asset_id: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            logical_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an asset hierarchy that contains a hierarchy's name and ID.

            :param child_asset_id: The Id of the child asset.
            :param external_id: The external ID of the hierarchy, if it has one. When you update an asset hierarchy, you may assign an external ID if it doesn't already have one. You can't change the external ID of an asset hierarchy that already has one. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            :param id: The ID of the hierarchy. This ID is a ``hierarchyId`` . .. epigraph:: This is a return value and can't be set.
            :param logical_id: The ID of the hierarchy. This ID is a ``hierarchyId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_hierarchy_property = iotsitewise_mixins.CfnAssetPropsMixin.AssetHierarchyProperty(
                    child_asset_id="childAssetId",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__373a15009838ac88d6a4d0c0616900c3522339370495a8c3fb5cbe47fd472849)
                check_type(argname="argument child_asset_id", value=child_asset_id, expected_type=type_hints["child_asset_id"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if child_asset_id is not None:
                self._values["child_asset_id"] = child_asset_id
            if external_id is not None:
                self._values["external_id"] = external_id
            if id is not None:
                self._values["id"] = id
            if logical_id is not None:
                self._values["logical_id"] = logical_id

        @builtins.property
        def child_asset_id(self) -> typing.Optional[builtins.str]:
            '''The Id of the child asset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-childassetid
            '''
            result = self._values.get("child_asset_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of the hierarchy, if it has one.

            When you update an asset hierarchy, you may assign an external ID if it doesn't already have one. You can't change the external ID of an asset hierarchy that already has one. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hierarchy. This ID is a ``hierarchyId`` .

            .. epigraph::

               This is a return value and can't be set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hierarchy.

            This ID is a ``hierarchyId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assethierarchy.html#cfn-iotsitewise-asset-assethierarchy-logicalid
            '''
            result = self._values.get("logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetHierarchyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnAssetPropsMixin.AssetPropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alias": "alias",
            "external_id": "externalId",
            "id": "id",
            "logical_id": "logicalId",
            "notification_state": "notificationState",
            "unit": "unit",
        },
    )
    class AssetPropertyProperty:
        def __init__(
            self,
            *,
            alias: typing.Optional[builtins.str] = None,
            external_id: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            logical_id: typing.Optional[builtins.str] = None,
            notification_state: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains asset property information.

            :param alias: The alias that identifies the property, such as an OPC-UA server data stream path (for example, ``/company/windfarm/3/turbine/7/temperature`` ). For more information, see `Mapping industrial data streams to asset properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/connect-data-streams.html>`_ in the *AWS IoT SiteWise User Guide* .
            :param external_id: The external ID of the property. For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .
            :param id: The ID of the asset property. .. epigraph:: This is a return value and can't be set.
            :param logical_id: The ``LogicalID`` of the asset property.
            :param notification_state: The MQTT notification state (enabled or disabled) for this asset property. When the notification state is enabled, AWS IoT SiteWise publishes property value updates to a unique MQTT topic. For more information, see `Interacting with other services <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/interact-with-other-services.html>`_ in the *AWS IoT SiteWise User Guide* . If you omit this parameter, the notification state is set to ``DISABLED`` .
            :param unit: The unit (such as ``Newtons`` or ``RPM`` ) of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_property_property = iotsitewise_mixins.CfnAssetPropsMixin.AssetPropertyProperty(
                    alias="alias",
                    external_id="externalId",
                    id="id",
                    logical_id="logicalId",
                    notification_state="notificationState",
                    unit="unit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4a04950ecc067e02a227e9dec9ce11fd3bdd7f64875fdabd7cc4fb6625b4af2)
                check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
                check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument logical_id", value=logical_id, expected_type=type_hints["logical_id"])
                check_type(argname="argument notification_state", value=notification_state, expected_type=type_hints["notification_state"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alias is not None:
                self._values["alias"] = alias
            if external_id is not None:
                self._values["external_id"] = external_id
            if id is not None:
                self._values["id"] = id
            if logical_id is not None:
                self._values["logical_id"] = logical_id
            if notification_state is not None:
                self._values["notification_state"] = notification_state
            if unit is not None:
                self._values["unit"] = unit

        @builtins.property
        def alias(self) -> typing.Optional[builtins.str]:
            '''The alias that identifies the property, such as an OPC-UA server data stream path (for example, ``/company/windfarm/3/turbine/7/temperature`` ).

            For more information, see `Mapping industrial data streams to asset properties <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/connect-data-streams.html>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-alias
            '''
            result = self._values.get("alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def external_id(self) -> typing.Optional[builtins.str]:
            '''The external ID of the property.

            For more information, see `Using external IDs <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/object-ids.html#external-ids>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-externalid
            '''
            result = self._values.get("external_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset property.

            .. epigraph::

               This is a return value and can't be set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logical_id(self) -> typing.Optional[builtins.str]:
            '''The ``LogicalID`` of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-logicalid
            '''
            result = self._values.get("logical_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_state(self) -> typing.Optional[builtins.str]:
            '''The MQTT notification state (enabled or disabled) for this asset property.

            When the notification state is enabled, AWS IoT SiteWise publishes property value updates to a unique MQTT topic. For more information, see `Interacting with other services <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/interact-with-other-services.html>`_ in the *AWS IoT SiteWise User Guide* .

            If you omit this parameter, the notification state is set to ``DISABLED`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-notificationstate
            '''
            result = self._values.get("notification_state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''The unit (such as ``Newtons`` or ``RPM`` ) of the asset property.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-asset-assetproperty.html#cfn-iotsitewise-asset-assetproperty-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "computation_model_configuration": "computationModelConfiguration",
        "computation_model_data_binding": "computationModelDataBinding",
        "computation_model_description": "computationModelDescription",
        "computation_model_name": "computationModelName",
        "tags": "tags",
    },
)
class CfnComputationModelMixinProps:
    def __init__(
        self,
        *,
        computation_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputationModelPropsMixin.ComputationModelConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        computation_model_data_binding: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        computation_model_description: typing.Optional[builtins.str] = None,
        computation_model_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnComputationModelPropsMixin.

        :param computation_model_configuration: The configuration for the computation model.
        :param computation_model_data_binding: The data binding for the computation model. Key is a variable name defined in configuration. Value is a ``ComputationModelDataBindingValue`` referenced by the variable.
        :param computation_model_description: The description of the computation model.
        :param computation_model_name: The name of the computation model.
        :param tags: A list of key-value pairs that contain metadata for the asset. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            # computation_model_data_binding_value_property_: iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty
            
            cfn_computation_model_mixin_props = iotsitewise_mixins.CfnComputationModelMixinProps(
                computation_model_configuration=iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelConfigurationProperty(
                    anomaly_detection=iotsitewise_mixins.CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty(
                        input_properties="inputProperties",
                        result_property="resultProperty"
                    )
                ),
                computation_model_data_binding={
                    "computation_model_data_binding_key": iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty(
                        asset_model_property=iotsitewise_mixins.CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty(
                            asset_model_id="assetModelId",
                            property_id="propertyId"
                        ),
                        asset_property=iotsitewise_mixins.CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty(
                            asset_id="assetId",
                            property_id="propertyId"
                        ),
                        list=[computation_model_data_binding_value_property_]
                    )
                },
                computation_model_description="computationModelDescription",
                computation_model_name="computationModelName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02ea665cd064f65ce4d47f7ee1effcaf3b4e8b36ec9e2afd540b0982702c082)
            check_type(argname="argument computation_model_configuration", value=computation_model_configuration, expected_type=type_hints["computation_model_configuration"])
            check_type(argname="argument computation_model_data_binding", value=computation_model_data_binding, expected_type=type_hints["computation_model_data_binding"])
            check_type(argname="argument computation_model_description", value=computation_model_description, expected_type=type_hints["computation_model_description"])
            check_type(argname="argument computation_model_name", value=computation_model_name, expected_type=type_hints["computation_model_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if computation_model_configuration is not None:
            self._values["computation_model_configuration"] = computation_model_configuration
        if computation_model_data_binding is not None:
            self._values["computation_model_data_binding"] = computation_model_data_binding
        if computation_model_description is not None:
            self._values["computation_model_description"] = computation_model_description
        if computation_model_name is not None:
            self._values["computation_model_name"] = computation_model_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def computation_model_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.ComputationModelConfigurationProperty"]]:
        '''The configuration for the computation model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html#cfn-iotsitewise-computationmodel-computationmodelconfiguration
        '''
        result = self._values.get("computation_model_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.ComputationModelConfigurationProperty"]], result)

    @builtins.property
    def computation_model_data_binding(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty"]]]]:
        '''The data binding for the computation model.

        Key is a variable name defined in configuration. Value is a ``ComputationModelDataBindingValue`` referenced by the variable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html#cfn-iotsitewise-computationmodel-computationmodeldatabinding
        '''
        result = self._values.get("computation_model_data_binding")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty"]]]], result)

    @builtins.property
    def computation_model_description(self) -> typing.Optional[builtins.str]:
        '''The description of the computation model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html#cfn-iotsitewise-computationmodel-computationmodeldescription
        '''
        result = self._values.get("computation_model_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def computation_model_name(self) -> typing.Optional[builtins.str]:
        '''The name of the computation model.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html#cfn-iotsitewise-computationmodel-computationmodelname
        '''
        result = self._values.get("computation_model_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the asset.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html#cfn-iotsitewise-computationmodel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComputationModelMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnComputationModelPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelPropsMixin",
):
    '''Create a computation model with a configuration and data binding.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-computationmodel.html
    :cloudformationResource: AWS::IoTSiteWise::ComputationModel
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        # computation_model_data_binding_value_property_: iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty
        
        cfn_computation_model_props_mixin = iotsitewise_mixins.CfnComputationModelPropsMixin(iotsitewise_mixins.CfnComputationModelMixinProps(
            computation_model_configuration=iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelConfigurationProperty(
                anomaly_detection=iotsitewise_mixins.CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty(
                    input_properties="inputProperties",
                    result_property="resultProperty"
                )
            ),
            computation_model_data_binding={
                "computation_model_data_binding_key": iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty(
                    asset_model_property=iotsitewise_mixins.CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty(
                        asset_model_id="assetModelId",
                        property_id="propertyId"
                    ),
                    asset_property=iotsitewise_mixins.CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty(
                        asset_id="assetId",
                        property_id="propertyId"
                    ),
                    list=[computation_model_data_binding_value_property_]
                )
            },
            computation_model_description="computationModelDescription",
            computation_model_name="computationModelName",
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
        props: typing.Union[CfnComputationModelMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::ComputationModel``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2078012b63cdc9f9080294534acffdc1fa3cbeee50f08a32448d358de1cf78d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec036da5a481ab4d90433311c42492ea577402d6441b5022a53d1766c5973122)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61377acff0a2e93329775ff41714a31ada59cc40e4a323704c168d95b27c307a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnComputationModelMixinProps:
        return typing.cast(CfnComputationModelMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_properties": "inputProperties",
            "result_property": "resultProperty",
        },
    )
    class AnomalyDetectionComputationModelConfigurationProperty:
        def __init__(
            self,
            *,
            input_properties: typing.Optional[builtins.str] = None,
            result_property: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the configuration for anomaly detection computation models.

            :param input_properties: The list of input properties for the anomaly detection model.
            :param result_property: The property where the anomaly detection results will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-anomalydetectioncomputationmodelconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                anomaly_detection_computation_model_configuration_property = iotsitewise_mixins.CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty(
                    input_properties="inputProperties",
                    result_property="resultProperty"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22b9aedc70fcf70e3783490c5cf31ee4e5eee99cd86661ab076fd7417fd95800)
                check_type(argname="argument input_properties", value=input_properties, expected_type=type_hints["input_properties"])
                check_type(argname="argument result_property", value=result_property, expected_type=type_hints["result_property"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_properties is not None:
                self._values["input_properties"] = input_properties
            if result_property is not None:
                self._values["result_property"] = result_property

        @builtins.property
        def input_properties(self) -> typing.Optional[builtins.str]:
            '''The list of input properties for the anomaly detection model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-anomalydetectioncomputationmodelconfiguration.html#cfn-iotsitewise-computationmodel-anomalydetectioncomputationmodelconfiguration-inputproperties
            '''
            result = self._values.get("input_properties")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def result_property(self) -> typing.Optional[builtins.str]:
            '''The property where the anomaly detection results will be stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-anomalydetectioncomputationmodelconfiguration.html#cfn-iotsitewise-computationmodel-anomalydetectioncomputationmodelconfiguration-resultproperty
            '''
            result = self._values.get("result_property")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AnomalyDetectionComputationModelConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty",
        jsii_struct_bases=[],
        name_mapping={"asset_model_id": "assetModelId", "property_id": "propertyId"},
    )
    class AssetModelPropertyBindingValueProperty:
        def __init__(
            self,
            *,
            asset_model_id: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an ``assetModelProperty`` binding value.

            :param asset_model_id: The ID of the asset model, in UUID format.
            :param property_id: The ID of the asset model property used in data binding value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-assetmodelpropertybindingvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_model_property_binding_value_property = iotsitewise_mixins.CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty(
                    asset_model_id="assetModelId",
                    property_id="propertyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e306ecad84c22ba508efbb8a9a66ad3c69f5286f7f41aa1b91cfb6de11938001)
                check_type(argname="argument asset_model_id", value=asset_model_id, expected_type=type_hints["asset_model_id"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_model_id is not None:
                self._values["asset_model_id"] = asset_model_id
            if property_id is not None:
                self._values["property_id"] = property_id

        @builtins.property
        def asset_model_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset model, in UUID format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-assetmodelpropertybindingvalue.html#cfn-iotsitewise-computationmodel-assetmodelpropertybindingvalue-assetmodelid
            '''
            result = self._values.get("asset_model_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset model property used in data binding value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-assetmodelpropertybindingvalue.html#cfn-iotsitewise-computationmodel-assetmodelpropertybindingvalue-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetModelPropertyBindingValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty",
        jsii_struct_bases=[],
        name_mapping={"asset_id": "assetId", "property_id": "propertyId"},
    )
    class AssetPropertyBindingValueProperty:
        def __init__(
            self,
            *,
            asset_id: typing.Optional[builtins.str] = None,
            property_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a data binding value referencing a specific asset property.

            It's used to bind computation model variables to actual asset property values for processing.

            :param asset_id: The ID of the asset containing the property. This identifies the specific asset instance's property value used in the computation model.
            :param property_id: The ID of the property within the asset. This identifies the specific property's value used in the computation model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-assetpropertybindingvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                asset_property_binding_value_property = iotsitewise_mixins.CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty(
                    asset_id="assetId",
                    property_id="propertyId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__77830f864b1a25badf7b788c0e1c82b96dc4b1bfac921e3395f8e96a1ab5b512)
                check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
                check_type(argname="argument property_id", value=property_id, expected_type=type_hints["property_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_id is not None:
                self._values["asset_id"] = asset_id
            if property_id is not None:
                self._values["property_id"] = property_id

        @builtins.property
        def asset_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the asset containing the property.

            This identifies the specific asset instance's property value used in the computation model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-assetpropertybindingvalue.html#cfn-iotsitewise-computationmodel-assetpropertybindingvalue-assetid
            '''
            result = self._values.get("asset_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def property_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the property within the asset.

            This identifies the specific property's value used in the computation model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-assetpropertybindingvalue.html#cfn-iotsitewise-computationmodel-assetpropertybindingvalue-propertyid
            '''
            result = self._values.get("property_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssetPropertyBindingValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelPropsMixin.ComputationModelConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"anomaly_detection": "anomalyDetection"},
    )
    class ComputationModelConfigurationProperty:
        def __init__(
            self,
            *,
            anomaly_detection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for the computation model.

            :param anomaly_detection: The configuration for the anomaly detection type of computation model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-computationmodelconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                computation_model_configuration_property = iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelConfigurationProperty(
                    anomaly_detection=iotsitewise_mixins.CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty(
                        input_properties="inputProperties",
                        result_property="resultProperty"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0ae9439abc990b52def1ed50c748b11a8e8434950628dc29aac11caf966994b1)
                check_type(argname="argument anomaly_detection", value=anomaly_detection, expected_type=type_hints["anomaly_detection"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if anomaly_detection is not None:
                self._values["anomaly_detection"] = anomaly_detection

        @builtins.property
        def anomaly_detection(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty"]]:
            '''The configuration for the anomaly detection type of computation model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-computationmodelconfiguration.html#cfn-iotsitewise-computationmodel-computationmodelconfiguration-anomalydetection
            '''
            result = self._values.get("anomaly_detection")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputationModelConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty",
        jsii_struct_bases=[],
        name_mapping={
            "asset_model_property": "assetModelProperty",
            "asset_property": "assetProperty",
            "list": "list",
        },
    )
    class ComputationModelDataBindingValueProperty:
        def __init__(
            self,
            *,
            asset_model_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            asset_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains computation model data binding value information, which can be one of ``assetModelProperty`` , ``list`` .

            :param asset_model_property: Specifies an asset model property data binding value.
            :param asset_property: The asset property value used for computation model data binding.
            :param list: Specifies a list of data binding value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-computationmodeldatabindingvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                # computation_model_data_binding_value_property_: iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty
                
                computation_model_data_binding_value_property = iotsitewise_mixins.CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty(
                    asset_model_property=iotsitewise_mixins.CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty(
                        asset_model_id="assetModelId",
                        property_id="propertyId"
                    ),
                    asset_property=iotsitewise_mixins.CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty(
                        asset_id="assetId",
                        property_id="propertyId"
                    ),
                    list=[computation_model_data_binding_value_property_]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__311dff77549a1a3d04ed8c991736a061de4fc6d066e5e1e43a2ed21e3fb35b32)
                check_type(argname="argument asset_model_property", value=asset_model_property, expected_type=type_hints["asset_model_property"])
                check_type(argname="argument asset_property", value=asset_property, expected_type=type_hints["asset_property"])
                check_type(argname="argument list", value=list, expected_type=type_hints["list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if asset_model_property is not None:
                self._values["asset_model_property"] = asset_model_property
            if asset_property is not None:
                self._values["asset_property"] = asset_property
            if list is not None:
                self._values["list"] = list

        @builtins.property
        def asset_model_property(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty"]]:
            '''Specifies an asset model property data binding value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-computationmodeldatabindingvalue.html#cfn-iotsitewise-computationmodel-computationmodeldatabindingvalue-assetmodelproperty
            '''
            result = self._values.get("asset_model_property")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty"]], result)

        @builtins.property
        def asset_property(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty"]]:
            '''The asset property value used for computation model data binding.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-computationmodeldatabindingvalue.html#cfn-iotsitewise-computationmodel-computationmodeldatabindingvalue-assetproperty
            '''
            result = self._values.get("asset_property")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty"]], result)

        @builtins.property
        def list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty"]]]]:
            '''Specifies a list of data binding value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-computationmodel-computationmodeldatabindingvalue.html#cfn-iotsitewise-computationmodel-computationmodeldatabindingvalue-list
            '''
            result = self._values.get("list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputationModelDataBindingValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDashboardMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_definition": "dashboardDefinition",
        "dashboard_description": "dashboardDescription",
        "dashboard_name": "dashboardName",
        "project_id": "projectId",
        "tags": "tags",
    },
)
class CfnDashboardMixinProps:
    def __init__(
        self,
        *,
        dashboard_definition: typing.Optional[builtins.str] = None,
        dashboard_description: typing.Optional[builtins.str] = None,
        dashboard_name: typing.Optional[builtins.str] = None,
        project_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDashboardPropsMixin.

        :param dashboard_definition: The dashboard definition specified in a JSON literal. - AWS IoT SiteWise Monitor (Classic) see `Create dashboards ( AWS CLI ) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-using-aws-cli.html>`_ - AWS IoT SiteWise Monitor (AI-aware) see `Create dashboards ( AWS CLI ) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-ai-dashboard-cli.html>`_ in the *AWS IoT SiteWise User Guide*
        :param dashboard_description: A description for the dashboard.
        :param dashboard_name: A friendly name for the dashboard.
        :param project_id: The ID of the project in which to create the dashboard.
        :param tags: A list of key-value pairs that contain metadata for the dashboard. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_dashboard_mixin_props = iotsitewise_mixins.CfnDashboardMixinProps(
                dashboard_definition="dashboardDefinition",
                dashboard_description="dashboardDescription",
                dashboard_name="dashboardName",
                project_id="projectId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__779982b4818869a3996bf93486f539d38611f61e3dbb16e4f3637f89e487e734)
            check_type(argname="argument dashboard_definition", value=dashboard_definition, expected_type=type_hints["dashboard_definition"])
            check_type(argname="argument dashboard_description", value=dashboard_description, expected_type=type_hints["dashboard_description"])
            check_type(argname="argument dashboard_name", value=dashboard_name, expected_type=type_hints["dashboard_name"])
            check_type(argname="argument project_id", value=project_id, expected_type=type_hints["project_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_definition is not None:
            self._values["dashboard_definition"] = dashboard_definition
        if dashboard_description is not None:
            self._values["dashboard_description"] = dashboard_description
        if dashboard_name is not None:
            self._values["dashboard_name"] = dashboard_name
        if project_id is not None:
            self._values["project_id"] = project_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dashboard_definition(self) -> typing.Optional[builtins.str]:
        '''The dashboard definition specified in a JSON literal.

        - AWS IoT SiteWise Monitor (Classic) see `Create dashboards ( AWS CLI ) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-using-aws-cli.html>`_
        - AWS IoT SiteWise Monitor (AI-aware) see `Create dashboards ( AWS CLI ) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/create-dashboards-ai-dashboard-cli.html>`_

        in the *AWS IoT SiteWise User Guide*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboarddefinition
        '''
        result = self._values.get("dashboard_definition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dashboard_description(self) -> typing.Optional[builtins.str]:
        '''A description for the dashboard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboarddescription
        '''
        result = self._values.get("dashboard_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dashboard_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the dashboard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-dashboardname
        '''
        result = self._values.get("dashboard_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the project in which to create the dashboard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-projectid
        '''
        result = self._values.get("project_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the dashboard.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html#cfn-iotsitewise-dashboard-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDashboardMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDashboardPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDashboardPropsMixin",
):
    '''.. epigraph::

   The AWS IoT SiteWise Monitor feature will no longer be open to new customers starting November 7, 2025 .

    If you would like to use the AWS IoT SiteWise Monitor feature, sign up prior to that date. Existing customers can continue to use the service as normal. For more information, see `AWS IoT SiteWise Monitor availability change <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/iotsitewise-monitor-availability-change.html>`_ .

    Creates a dashboard in an AWS IoT SiteWise Monitor project.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dashboard.html
    :cloudformationResource: AWS::IoTSiteWise::Dashboard
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_dashboard_props_mixin = iotsitewise_mixins.CfnDashboardPropsMixin(iotsitewise_mixins.CfnDashboardMixinProps(
            dashboard_definition="dashboardDefinition",
            dashboard_description="dashboardDescription",
            dashboard_name="dashboardName",
            project_id="projectId",
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
        props: typing.Union[CfnDashboardMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::Dashboard``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d493037726f626dd33244d11175341ae7b725867fb3c03903b0f0097f6507e8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f611cf18f640531e3cd4dd03e7036c14220d84a27e4ca157c76da2771e43569e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d255bec8fc335a9ced1a828b5d0da01606d2b2efd89a34fbcaec6c543196ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDashboardMixinProps:
        return typing.cast(CfnDashboardMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDatasetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_description": "datasetDescription",
        "dataset_name": "datasetName",
        "dataset_source": "datasetSource",
        "tags": "tags",
    },
)
class CfnDatasetMixinProps:
    def __init__(
        self,
        *,
        dataset_description: typing.Optional[builtins.str] = None,
        dataset_name: typing.Optional[builtins.str] = None,
        dataset_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatasetSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatasetPropsMixin.

        :param dataset_description: A description about the dataset, and its functionality.
        :param dataset_name: The name of the dataset.
        :param dataset_source: The data source for the dataset.
        :param tags: A list of key-value pairs that contain metadata for the access policy. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_dataset_mixin_props = iotsitewise_mixins.CfnDatasetMixinProps(
                dataset_description="datasetDescription",
                dataset_name="datasetName",
                dataset_source=iotsitewise_mixins.CfnDatasetPropsMixin.DatasetSourceProperty(
                    source_detail=iotsitewise_mixins.CfnDatasetPropsMixin.SourceDetailProperty(
                        kendra=iotsitewise_mixins.CfnDatasetPropsMixin.KendraSourceDetailProperty(
                            knowledge_base_arn="knowledgeBaseArn",
                            role_arn="roleArn"
                        )
                    ),
                    source_format="sourceFormat",
                    source_type="sourceType"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__887d927bb2a9b0d4ebaf0d7478aa4e948fcfecd2fc0ff742ca9b35872f574301)
            check_type(argname="argument dataset_description", value=dataset_description, expected_type=type_hints["dataset_description"])
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument dataset_source", value=dataset_source, expected_type=type_hints["dataset_source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_description is not None:
            self._values["dataset_description"] = dataset_description
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if dataset_source is not None:
            self._values["dataset_source"] = dataset_source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataset_description(self) -> typing.Optional[builtins.str]:
        '''A description about the dataset, and its functionality.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dataset.html#cfn-iotsitewise-dataset-datasetdescription
        '''
        result = self._values.get("dataset_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dataset.html#cfn-iotsitewise-dataset-datasetname
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataset_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetSourceProperty"]]:
        '''The data source for the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dataset.html#cfn-iotsitewise-dataset-datasetsource
        '''
        result = self._values.get("dataset_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetSourceProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the access policy.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dataset.html#cfn-iotsitewise-dataset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatasetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDatasetPropsMixin",
):
    '''Creates a dataset to connect an external datasource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-dataset.html
    :cloudformationResource: AWS::IoTSiteWise::Dataset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_dataset_props_mixin = iotsitewise_mixins.CfnDatasetPropsMixin(iotsitewise_mixins.CfnDatasetMixinProps(
            dataset_description="datasetDescription",
            dataset_name="datasetName",
            dataset_source=iotsitewise_mixins.CfnDatasetPropsMixin.DatasetSourceProperty(
                source_detail=iotsitewise_mixins.CfnDatasetPropsMixin.SourceDetailProperty(
                    kendra=iotsitewise_mixins.CfnDatasetPropsMixin.KendraSourceDetailProperty(
                        knowledge_base_arn="knowledgeBaseArn",
                        role_arn="roleArn"
                    )
                ),
                source_format="sourceFormat",
                source_type="sourceType"
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
        props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::Dataset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02958fe39016b80d1ccb64f4c578b9ec7d3734646548a1dcea741e35d3686d6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ad9e2259ed9ac4d232c951c38239a0b3d6110e81fcf32da8adf3e3becac67ad)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7dc9c3fd73b87b87e150dc22b3a28834adf3ea76a1140322c2cb2c7cf7cc4de)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatasetMixinProps:
        return typing.cast(CfnDatasetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDatasetPropsMixin.DatasetSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source_detail": "sourceDetail",
            "source_format": "sourceFormat",
            "source_type": "sourceType",
        },
    )
    class DatasetSourceProperty:
        def __init__(
            self,
            *,
            source_detail: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.SourceDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            source_format: typing.Optional[builtins.str] = None,
            source_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The data source for the dataset.

            :param source_detail: The details of the dataset source associated with the dataset.
            :param source_format: The format of the dataset source associated with the dataset.
            :param source_type: The type of data source for the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-datasetsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                dataset_source_property = iotsitewise_mixins.CfnDatasetPropsMixin.DatasetSourceProperty(
                    source_detail=iotsitewise_mixins.CfnDatasetPropsMixin.SourceDetailProperty(
                        kendra=iotsitewise_mixins.CfnDatasetPropsMixin.KendraSourceDetailProperty(
                            knowledge_base_arn="knowledgeBaseArn",
                            role_arn="roleArn"
                        )
                    ),
                    source_format="sourceFormat",
                    source_type="sourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a69d8e5e7aeb520066483dbd7a5a67f61051ab9e4ed90310ddda77fbcd4b094b)
                check_type(argname="argument source_detail", value=source_detail, expected_type=type_hints["source_detail"])
                check_type(argname="argument source_format", value=source_format, expected_type=type_hints["source_format"])
                check_type(argname="argument source_type", value=source_type, expected_type=type_hints["source_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_detail is not None:
                self._values["source_detail"] = source_detail
            if source_format is not None:
                self._values["source_format"] = source_format
            if source_type is not None:
                self._values["source_type"] = source_type

        @builtins.property
        def source_detail(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.SourceDetailProperty"]]:
            '''The details of the dataset source associated with the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-datasetsource.html#cfn-iotsitewise-dataset-datasetsource-sourcedetail
            '''
            result = self._values.get("source_detail")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.SourceDetailProperty"]], result)

        @builtins.property
        def source_format(self) -> typing.Optional[builtins.str]:
            '''The format of the dataset source associated with the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-datasetsource.html#cfn-iotsitewise-dataset-datasetsource-sourceformat
            '''
            result = self._values.get("source_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_type(self) -> typing.Optional[builtins.str]:
            '''The type of data source for the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-datasetsource.html#cfn-iotsitewise-dataset-datasetsource-sourcetype
            '''
            result = self._values.get("source_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDatasetPropsMixin.KendraSourceDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"knowledge_base_arn": "knowledgeBaseArn", "role_arn": "roleArn"},
    )
    class KendraSourceDetailProperty:
        def __init__(
            self,
            *,
            knowledge_base_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The source details for the Kendra dataset source.

            :param knowledge_base_arn: The ``knowledgeBaseArn`` details for the Kendra dataset source.
            :param role_arn: The ``roleARN`` details for the Kendra dataset source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-kendrasourcedetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                kendra_source_detail_property = iotsitewise_mixins.CfnDatasetPropsMixin.KendraSourceDetailProperty(
                    knowledge_base_arn="knowledgeBaseArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57e36e03be816067243e362049c04c676adb39d20b8683d89f650816f2c74955)
                check_type(argname="argument knowledge_base_arn", value=knowledge_base_arn, expected_type=type_hints["knowledge_base_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if knowledge_base_arn is not None:
                self._values["knowledge_base_arn"] = knowledge_base_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def knowledge_base_arn(self) -> typing.Optional[builtins.str]:
            '''The ``knowledgeBaseArn`` details for the Kendra dataset source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-kendrasourcedetail.html#cfn-iotsitewise-dataset-kendrasourcedetail-knowledgebasearn
            '''
            result = self._values.get("knowledge_base_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ``roleARN`` details for the Kendra dataset source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-kendrasourcedetail.html#cfn-iotsitewise-dataset-kendrasourcedetail-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KendraSourceDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnDatasetPropsMixin.SourceDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"kendra": "kendra"},
    )
    class SourceDetailProperty:
        def __init__(
            self,
            *,
            kendra: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.KendraSourceDetailProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The details of the dataset source associated with the dataset.

            :param kendra: Contains details about the Kendra dataset source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-sourcedetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                source_detail_property = iotsitewise_mixins.CfnDatasetPropsMixin.SourceDetailProperty(
                    kendra=iotsitewise_mixins.CfnDatasetPropsMixin.KendraSourceDetailProperty(
                        knowledge_base_arn="knowledgeBaseArn",
                        role_arn="roleArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ad275725c1332e72ca82de0af82ad4a838d0bdd1c5effdc127d2b2c30f8f940)
                check_type(argname="argument kendra", value=kendra, expected_type=type_hints["kendra"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kendra is not None:
                self._values["kendra"] = kendra

        @builtins.property
        def kendra(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.KendraSourceDetailProperty"]]:
            '''Contains details about the Kendra dataset source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-dataset-sourcedetail.html#cfn-iotsitewise-dataset-sourcedetail-kendra
            '''
            result = self._values.get("kendra")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.KendraSourceDetailProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "gateway_capability_summaries": "gatewayCapabilitySummaries",
        "gateway_name": "gatewayName",
        "gateway_platform": "gatewayPlatform",
        "gateway_version": "gatewayVersion",
        "tags": "tags",
    },
)
class CfnGatewayMixinProps:
    def __init__(
        self,
        *,
        gateway_capability_summaries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        gateway_name: typing.Optional[builtins.str] = None,
        gateway_platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.GatewayPlatformProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        gateway_version: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnGatewayPropsMixin.

        :param gateway_capability_summaries: A list of gateway capability summaries that each contain a namespace and status. Each gateway capability defines data sources for the gateway. To retrieve a capability configuration's definition, use `DescribeGatewayCapabilityConfiguration <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_DescribeGatewayCapabilityConfiguration.html>`_ .
        :param gateway_name: A unique name for the gateway.
        :param gateway_platform: The gateway's platform. You can only specify one platform in a gateway.
        :param gateway_version: The version of the gateway. A value of ``3`` indicates an MQTT-enabled, V3 gateway, while ``2`` indicates a Classic streams, V2 gateway.
        :param tags: A list of key-value pairs that contain metadata for the gateway. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_gateway_mixin_props = iotsitewise_mixins.CfnGatewayMixinProps(
                gateway_capability_summaries=[iotsitewise_mixins.CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty(
                    capability_configuration="capabilityConfiguration",
                    capability_namespace="capabilityNamespace"
                )],
                gateway_name="gatewayName",
                gateway_platform=iotsitewise_mixins.CfnGatewayPropsMixin.GatewayPlatformProperty(
                    greengrass=iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassProperty(
                        group_arn="groupArn"
                    ),
                    greengrass_v2=iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassV2Property(
                        core_device_operating_system="coreDeviceOperatingSystem",
                        core_device_thing_name="coreDeviceThingName"
                    ),
                    siemens_ie=iotsitewise_mixins.CfnGatewayPropsMixin.SiemensIEProperty(
                        iot_core_thing_name="iotCoreThingName"
                    )
                ),
                gateway_version="gatewayVersion",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae07484d64a9107e9bbbcb5cadb345d581ac7c545f0fb5cd0d910356e9de449)
            check_type(argname="argument gateway_capability_summaries", value=gateway_capability_summaries, expected_type=type_hints["gateway_capability_summaries"])
            check_type(argname="argument gateway_name", value=gateway_name, expected_type=type_hints["gateway_name"])
            check_type(argname="argument gateway_platform", value=gateway_platform, expected_type=type_hints["gateway_platform"])
            check_type(argname="argument gateway_version", value=gateway_version, expected_type=type_hints["gateway_version"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if gateway_capability_summaries is not None:
            self._values["gateway_capability_summaries"] = gateway_capability_summaries
        if gateway_name is not None:
            self._values["gateway_name"] = gateway_name
        if gateway_platform is not None:
            self._values["gateway_platform"] = gateway_platform
        if gateway_version is not None:
            self._values["gateway_version"] = gateway_version
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def gateway_capability_summaries(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty"]]]]:
        '''A list of gateway capability summaries that each contain a namespace and status.

        Each gateway capability defines data sources for the gateway. To retrieve a capability configuration's definition, use `DescribeGatewayCapabilityConfiguration <https://docs.aws.amazon.com/iot-sitewise/latest/APIReference/API_DescribeGatewayCapabilityConfiguration.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewaycapabilitysummaries
        '''
        result = self._values.get("gateway_capability_summaries")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty"]]]], result)

    @builtins.property
    def gateway_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayname
        '''
        result = self._values.get("gateway_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gateway_platform(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayPlatformProperty"]]:
        '''The gateway's platform.

        You can only specify one platform in a gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayplatform
        '''
        result = self._values.get("gateway_platform")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GatewayPlatformProperty"]], result)

    @builtins.property
    def gateway_version(self) -> typing.Optional[builtins.str]:
        '''The version of the gateway.

        A value of ``3`` indicates an MQTT-enabled, V3 gateway, while ``2`` indicates a Classic streams, V2 gateway.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-gatewayversion
        '''
        result = self._values.get("gateway_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the gateway.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html#cfn-iotsitewise-gateway-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGatewayMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGatewayPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayPropsMixin",
):
    '''Creates a gateway, which is a virtual or edge device that delivers industrial data streams from local servers to AWS IoT SiteWise .

    For more information, see `Ingesting data using a gateway <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/gateway-connector.html>`_ in the *AWS IoT SiteWise User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-gateway.html
    :cloudformationResource: AWS::IoTSiteWise::Gateway
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_gateway_props_mixin = iotsitewise_mixins.CfnGatewayPropsMixin(iotsitewise_mixins.CfnGatewayMixinProps(
            gateway_capability_summaries=[iotsitewise_mixins.CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty(
                capability_configuration="capabilityConfiguration",
                capability_namespace="capabilityNamespace"
            )],
            gateway_name="gatewayName",
            gateway_platform=iotsitewise_mixins.CfnGatewayPropsMixin.GatewayPlatformProperty(
                greengrass=iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassProperty(
                    group_arn="groupArn"
                ),
                greengrass_v2=iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassV2Property(
                    core_device_operating_system="coreDeviceOperatingSystem",
                    core_device_thing_name="coreDeviceThingName"
                ),
                siemens_ie=iotsitewise_mixins.CfnGatewayPropsMixin.SiemensIEProperty(
                    iot_core_thing_name="iotCoreThingName"
                )
            ),
            gateway_version="gatewayVersion",
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
        props: typing.Union[CfnGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::Gateway``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5bd5ace143e5558bb5683d5c11573b409a50d7f8d9114c4fa42bb5c6b8daa2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cbf305ce8d3e09c8ec950ce55f32c9a089a7da9e495ef728f3ef24b756c5f56)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae4a9719a9f1bc3c9af4d7b3319cdc37f313a1bc8887e7839bf47a80eeba34f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGatewayMixinProps:
        return typing.cast(CfnGatewayMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "capability_configuration": "capabilityConfiguration",
            "capability_namespace": "capabilityNamespace",
        },
    )
    class GatewayCapabilitySummaryProperty:
        def __init__(
            self,
            *,
            capability_configuration: typing.Optional[builtins.str] = None,
            capability_namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains a summary of a gateway capability configuration.

            :param capability_configuration: The JSON document that defines the configuration for the gateway capability. For more information, see `Configuring data sources (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/configure-sources.html#configure-source-cli>`_ in the *AWS IoT SiteWise User Guide* .
            :param capability_namespace: The namespace of the capability configuration. For example, if you configure OPC UA sources for an MQTT-enabled gateway, your OPC-UA capability configuration has the namespace ``iotsitewise:opcuacollector:3`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                gateway_capability_summary_property = iotsitewise_mixins.CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty(
                    capability_configuration="capabilityConfiguration",
                    capability_namespace="capabilityNamespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4683e676cfe0db9a6f08e081f63571f80351804c0d2b6c335bba0e5890c1742)
                check_type(argname="argument capability_configuration", value=capability_configuration, expected_type=type_hints["capability_configuration"])
                check_type(argname="argument capability_namespace", value=capability_namespace, expected_type=type_hints["capability_namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if capability_configuration is not None:
                self._values["capability_configuration"] = capability_configuration
            if capability_namespace is not None:
                self._values["capability_namespace"] = capability_namespace

        @builtins.property
        def capability_configuration(self) -> typing.Optional[builtins.str]:
            '''The JSON document that defines the configuration for the gateway capability.

            For more information, see `Configuring data sources (CLI) <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/configure-sources.html#configure-source-cli>`_ in the *AWS IoT SiteWise User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html#cfn-iotsitewise-gateway-gatewaycapabilitysummary-capabilityconfiguration
            '''
            result = self._values.get("capability_configuration")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def capability_namespace(self) -> typing.Optional[builtins.str]:
            '''The namespace of the capability configuration.

            For example, if you configure OPC UA sources for an MQTT-enabled gateway, your OPC-UA capability configuration has the namespace ``iotsitewise:opcuacollector:3`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewaycapabilitysummary.html#cfn-iotsitewise-gateway-gatewaycapabilitysummary-capabilitynamespace
            '''
            result = self._values.get("capability_namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayCapabilitySummaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayPropsMixin.GatewayPlatformProperty",
        jsii_struct_bases=[],
        name_mapping={
            "greengrass": "greengrass",
            "greengrass_v2": "greengrassV2",
            "siemens_ie": "siemensIe",
        },
    )
    class GatewayPlatformProperty:
        def __init__(
            self,
            *,
            greengrass: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.GreengrassProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            greengrass_v2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.GreengrassV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            siemens_ie: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGatewayPropsMixin.SiemensIEProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The gateway's platform configuration. You can only specify one platform type in a gateway.

            (Legacy only) For Greengrass V1 gateways, specify the ``greengrass`` parameter with a valid Greengrass group ARN.

            For Greengrass V2 gateways, specify the ``greengrassV2`` parameter with a valid core device thing name. If creating a V3 gateway ( ``gatewayVersion=3`` ), you must also specify the ``coreDeviceOperatingSystem`` .

            For Siemens Industrial Edge gateways, specify the ``siemensIE`` parameter with a valid IoT Core thing name.

            :param greengrass: 
            :param greengrass_v2: A gateway that runs on AWS IoT Greengrass V2 .
            :param siemens_ie: An AWS IoT SiteWise Edge gateway that runs on a Siemens Industrial Edge Device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                gateway_platform_property = iotsitewise_mixins.CfnGatewayPropsMixin.GatewayPlatformProperty(
                    greengrass=iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassProperty(
                        group_arn="groupArn"
                    ),
                    greengrass_v2=iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassV2Property(
                        core_device_operating_system="coreDeviceOperatingSystem",
                        core_device_thing_name="coreDeviceThingName"
                    ),
                    siemens_ie=iotsitewise_mixins.CfnGatewayPropsMixin.SiemensIEProperty(
                        iot_core_thing_name="iotCoreThingName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6104f7501aea12898788cc70d47ddf797353c7f8f4a1b2952b337006fa2aa9a5)
                check_type(argname="argument greengrass", value=greengrass, expected_type=type_hints["greengrass"])
                check_type(argname="argument greengrass_v2", value=greengrass_v2, expected_type=type_hints["greengrass_v2"])
                check_type(argname="argument siemens_ie", value=siemens_ie, expected_type=type_hints["siemens_ie"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if greengrass is not None:
                self._values["greengrass"] = greengrass
            if greengrass_v2 is not None:
                self._values["greengrass_v2"] = greengrass_v2
            if siemens_ie is not None:
                self._values["siemens_ie"] = siemens_ie

        @builtins.property
        def greengrass(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GreengrassProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html#cfn-iotsitewise-gateway-gatewayplatform-greengrass
            '''
            result = self._values.get("greengrass")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GreengrassProperty"]], result)

        @builtins.property
        def greengrass_v2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GreengrassV2Property"]]:
            '''A gateway that runs on AWS IoT Greengrass V2 .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html#cfn-iotsitewise-gateway-gatewayplatform-greengrassv2
            '''
            result = self._values.get("greengrass_v2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.GreengrassV2Property"]], result)

        @builtins.property
        def siemens_ie(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.SiemensIEProperty"]]:
            '''An AWS IoT SiteWise Edge gateway that runs on a Siemens Industrial Edge Device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-gatewayplatform.html#cfn-iotsitewise-gateway-gatewayplatform-siemensie
            '''
            result = self._values.get("siemens_ie")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGatewayPropsMixin.SiemensIEProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GatewayPlatformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayPropsMixin.GreengrassProperty",
        jsii_struct_bases=[],
        name_mapping={"group_arn": "groupArn"},
    )
    class GreengrassProperty:
        def __init__(self, *, group_arn: typing.Optional[builtins.str] = None) -> None:
            '''
            :param group_arn: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrass.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                greengrass_property = iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassProperty(
                    group_arn="groupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__02689eee67f71fcf45b7daa598b1f97a6e7b8775912eb7580d898bd54e3bac06)
                check_type(argname="argument group_arn", value=group_arn, expected_type=type_hints["group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_arn is not None:
                self._values["group_arn"] = group_arn

        @builtins.property
        def group_arn(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrass.html#cfn-iotsitewise-gateway-greengrass-grouparn
            '''
            result = self._values.get("group_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreengrassProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayPropsMixin.GreengrassV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "core_device_operating_system": "coreDeviceOperatingSystem",
            "core_device_thing_name": "coreDeviceThingName",
        },
    )
    class GreengrassV2Property:
        def __init__(
            self,
            *,
            core_device_operating_system: typing.Optional[builtins.str] = None,
            core_device_thing_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details for a gateway that runs on AWS IoT Greengrass V2 .

            To create a gateway that runs on AWS IoT Greengrass V2 , you must deploy the IoT SiteWise Edge component to your gateway device. Your `Greengrass device role <https://docs.aws.amazon.com/greengrass/v2/developerguide/device-service-role.html>`_ must use the ``AWSIoTSiteWiseEdgeAccess`` policy. For more information, see `Using AWS IoT SiteWise at the edge <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/sw-gateways.html>`_ in the *AWS IoT SiteWise User Guide* .

            :param core_device_operating_system: The operating system of the core device in AWS IoT Greengrass V2.
            :param core_device_thing_name: The name of the AWS IoT thing for your AWS IoT Greengrass V2 core device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrassv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                greengrass_v2_property = iotsitewise_mixins.CfnGatewayPropsMixin.GreengrassV2Property(
                    core_device_operating_system="coreDeviceOperatingSystem",
                    core_device_thing_name="coreDeviceThingName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7bb0dc9c0b02ee2cfa59047535727c60c0c42dbff8cd251aa93a8d9888446097)
                check_type(argname="argument core_device_operating_system", value=core_device_operating_system, expected_type=type_hints["core_device_operating_system"])
                check_type(argname="argument core_device_thing_name", value=core_device_thing_name, expected_type=type_hints["core_device_thing_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if core_device_operating_system is not None:
                self._values["core_device_operating_system"] = core_device_operating_system
            if core_device_thing_name is not None:
                self._values["core_device_thing_name"] = core_device_thing_name

        @builtins.property
        def core_device_operating_system(self) -> typing.Optional[builtins.str]:
            '''The operating system of the core device in AWS IoT Greengrass V2.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrassv2.html#cfn-iotsitewise-gateway-greengrassv2-coredeviceoperatingsystem
            '''
            result = self._values.get("core_device_operating_system")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def core_device_thing_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS IoT thing for your AWS IoT Greengrass V2 core device.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-greengrassv2.html#cfn-iotsitewise-gateway-greengrassv2-coredevicethingname
            '''
            result = self._values.get("core_device_thing_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GreengrassV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnGatewayPropsMixin.SiemensIEProperty",
        jsii_struct_bases=[],
        name_mapping={"iot_core_thing_name": "iotCoreThingName"},
    )
    class SiemensIEProperty:
        def __init__(
            self,
            *,
            iot_core_thing_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains details for a AWS IoT SiteWise Edge gateway that runs on a Siemens Industrial Edge Device.

            :param iot_core_thing_name: The name of the AWS IoT Thing for your AWS IoT SiteWise Edge gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-siemensie.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                siemens_iEProperty = iotsitewise_mixins.CfnGatewayPropsMixin.SiemensIEProperty(
                    iot_core_thing_name="iotCoreThingName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4caa984f38500b273e01689fa304d82c98239f95c087f8017a19e8fa78454e9b)
                check_type(argname="argument iot_core_thing_name", value=iot_core_thing_name, expected_type=type_hints["iot_core_thing_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iot_core_thing_name is not None:
                self._values["iot_core_thing_name"] = iot_core_thing_name

        @builtins.property
        def iot_core_thing_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS IoT Thing for your AWS IoT SiteWise Edge gateway.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-gateway-siemensie.html#cfn-iotsitewise-gateway-siemensie-iotcorethingname
            '''
            result = self._values.get("iot_core_thing_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SiemensIEProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnPortalMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "alarms": "alarms",
        "notification_sender_email": "notificationSenderEmail",
        "portal_auth_mode": "portalAuthMode",
        "portal_contact_email": "portalContactEmail",
        "portal_description": "portalDescription",
        "portal_name": "portalName",
        "portal_type": "portalType",
        "portal_type_configuration": "portalTypeConfiguration",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnPortalMixinProps:
    def __init__(
        self,
        *,
        alarms: typing.Any = None,
        notification_sender_email: typing.Optional[builtins.str] = None,
        portal_auth_mode: typing.Optional[builtins.str] = None,
        portal_contact_email: typing.Optional[builtins.str] = None,
        portal_description: typing.Optional[builtins.str] = None,
        portal_name: typing.Optional[builtins.str] = None,
        portal_type: typing.Optional[builtins.str] = None,
        portal_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPortalPropsMixin.PortalTypeEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPortalPropsMixin.

        :param alarms: Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .
        :param notification_sender_email: The email address that sends alarm notifications. .. epigraph:: If you use the `AWS IoT Events managed Lambda function <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ to manage your emails, you must `verify the sender email address in Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html>`_ .
        :param portal_auth_mode: The service to use to authenticate users to the portal. Choose from the following options:. - ``SSO`` – The portal uses AWS IAM Identity Center to authenticate users and manage user permissions. Before you can create a portal that uses IAM Identity Center, you must enable IAM Identity Center. For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* . This option is only available in AWS Regions other than the China Regions. - ``IAM`` – The portal uses AWS Identity and Access Management to authenticate users and manage user permissions. You can't change this value after you create a portal. Default: ``SSO``
        :param portal_contact_email: The AWS administrator's contact email address.
        :param portal_description: A description for the portal.
        :param portal_name: A friendly name for the portal.
        :param portal_type: Define the type of portal. The value for AWS IoT SiteWise Monitor (Classic) is ``SITEWISE_PORTAL_V1`` . The value for AWS IoT SiteWise Monitor (AI-aware) is ``SITEWISE_PORTAL_V2`` .
        :param portal_type_configuration: Map to associate detail of configuration related with a PortalType.
        :param role_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf. For more information, see `Using service roles for AWS IoT SiteWise Monitor <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-service-role.html>`_ in the *AWS IoT SiteWise User Guide* .
        :param tags: A list of key-value pairs that contain metadata for the portal. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            # alarms: Any
            
            cfn_portal_mixin_props = iotsitewise_mixins.CfnPortalMixinProps(
                alarms=alarms,
                notification_sender_email="notificationSenderEmail",
                portal_auth_mode="portalAuthMode",
                portal_contact_email="portalContactEmail",
                portal_description="portalDescription",
                portal_name="portalName",
                portal_type="portalType",
                portal_type_configuration={
                    "portal_type_configuration_key": iotsitewise_mixins.CfnPortalPropsMixin.PortalTypeEntryProperty(
                        portal_tools=["portalTools"]
                    )
                },
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b669e2fb033eedf92e0452c81c64627cc0226b41aea4132ddc0195c6565fcb14)
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument notification_sender_email", value=notification_sender_email, expected_type=type_hints["notification_sender_email"])
            check_type(argname="argument portal_auth_mode", value=portal_auth_mode, expected_type=type_hints["portal_auth_mode"])
            check_type(argname="argument portal_contact_email", value=portal_contact_email, expected_type=type_hints["portal_contact_email"])
            check_type(argname="argument portal_description", value=portal_description, expected_type=type_hints["portal_description"])
            check_type(argname="argument portal_name", value=portal_name, expected_type=type_hints["portal_name"])
            check_type(argname="argument portal_type", value=portal_type, expected_type=type_hints["portal_type"])
            check_type(argname="argument portal_type_configuration", value=portal_type_configuration, expected_type=type_hints["portal_type_configuration"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alarms is not None:
            self._values["alarms"] = alarms
        if notification_sender_email is not None:
            self._values["notification_sender_email"] = notification_sender_email
        if portal_auth_mode is not None:
            self._values["portal_auth_mode"] = portal_auth_mode
        if portal_contact_email is not None:
            self._values["portal_contact_email"] = portal_contact_email
        if portal_description is not None:
            self._values["portal_description"] = portal_description
        if portal_name is not None:
            self._values["portal_name"] = portal_name
        if portal_type is not None:
            self._values["portal_type"] = portal_type
        if portal_type_configuration is not None:
            self._values["portal_type_configuration"] = portal_type_configuration
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def alarms(self) -> typing.Any:
        '''Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal.

        You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-alarms
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Any, result)

    @builtins.property
    def notification_sender_email(self) -> typing.Optional[builtins.str]:
        '''The email address that sends alarm notifications.

        .. epigraph::

           If you use the `AWS IoT Events managed Lambda function <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ to manage your emails, you must `verify the sender email address in Amazon SES <https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-notificationsenderemail
        '''
        result = self._values.get("notification_sender_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_auth_mode(self) -> typing.Optional[builtins.str]:
        '''The service to use to authenticate users to the portal. Choose from the following options:.

        - ``SSO`` – The portal uses AWS IAM Identity Center to authenticate users and manage user permissions. Before you can create a portal that uses IAM Identity Center, you must enable IAM Identity Center. For more information, see `Enabling IAM Identity Center <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-get-started.html#mon-gs-sso>`_ in the *AWS IoT SiteWise User Guide* . This option is only available in AWS Regions other than the China Regions.
        - ``IAM`` – The portal uses AWS Identity and Access Management to authenticate users and manage user permissions.

        You can't change this value after you create a portal.

        Default: ``SSO``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalauthmode
        '''
        result = self._values.get("portal_auth_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_contact_email(self) -> typing.Optional[builtins.str]:
        '''The AWS administrator's contact email address.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalcontactemail
        '''
        result = self._values.get("portal_contact_email")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_description(self) -> typing.Optional[builtins.str]:
        '''A description for the portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portaldescription
        '''
        result = self._values.get("portal_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the portal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portalname
        '''
        result = self._values.get("portal_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_type(self) -> typing.Optional[builtins.str]:
        '''Define the type of portal.

        The value for AWS IoT SiteWise Monitor (Classic) is ``SITEWISE_PORTAL_V1`` . The value for AWS IoT SiteWise Monitor (AI-aware) is ``SITEWISE_PORTAL_V2`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portaltype
        '''
        result = self._values.get("portal_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_type_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPortalPropsMixin.PortalTypeEntryProperty"]]]]:
        '''Map to associate detail of configuration related with a PortalType.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-portaltypeconfiguration
        '''
        result = self._values.get("portal_type_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPortalPropsMixin.PortalTypeEntryProperty"]]]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of a service role that allows the portal's users to access your AWS IoT SiteWise resources on your behalf. For more information, see `Using service roles for AWS IoT SiteWise Monitor <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/monitor-service-role.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the portal.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html#cfn-iotsitewise-portal-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPortalMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPortalPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnPortalPropsMixin",
):
    '''.. epigraph::

   The AWS IoT SiteWise Monitor feature will no longer be open to new customers starting November 7, 2025 .

    If you would like to use the AWS IoT SiteWise Monitor feature, sign up prior to that date. Existing customers can continue to use the service as normal. For more information, see `AWS IoT SiteWise Monitor availability change <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/iotsitewise-monitor-availability-change.html>`_ .

    Creates a portal, which can contain projects and dashboards. AWS IoT SiteWise Monitor uses IAM Identity Center or IAM to authenticate portal users and manage user permissions.
    .. epigraph::

       Before you can sign in to a new portal, you must add at least one identity to that portal. For more information, see `Adding or removing portal administrators <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/administer-portals.html#portal-change-admins>`_ in the *AWS IoT SiteWise User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-portal.html
    :cloudformationResource: AWS::IoTSiteWise::Portal
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        # alarms: Any
        
        cfn_portal_props_mixin = iotsitewise_mixins.CfnPortalPropsMixin(iotsitewise_mixins.CfnPortalMixinProps(
            alarms=alarms,
            notification_sender_email="notificationSenderEmail",
            portal_auth_mode="portalAuthMode",
            portal_contact_email="portalContactEmail",
            portal_description="portalDescription",
            portal_name="portalName",
            portal_type="portalType",
            portal_type_configuration={
                "portal_type_configuration_key": iotsitewise_mixins.CfnPortalPropsMixin.PortalTypeEntryProperty(
                    portal_tools=["portalTools"]
                )
            },
            role_arn="roleArn",
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
        props: typing.Union[CfnPortalMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::Portal``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfb12d05184b7c3305880c91b5cfa25293ab7d0689017b967385b1be9692172c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1f68a5961e58721e333074f737add6368e2d35429ed635ba8754cd2a8bceeb91)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b86336d610ce09d9d8da335fd96bee966fb92d6946151fead06abc62c5b892)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPortalMixinProps:
        return typing.cast(CfnPortalMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnPortalPropsMixin.AlarmsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alarm_role_arn": "alarmRoleArn",
            "notification_lambda_arn": "notificationLambdaArn",
        },
    )
    class AlarmsProperty:
        def __init__(
            self,
            *,
            alarm_role_arn: typing.Optional[builtins.str] = None,
            notification_lambda_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal.

            You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range. For more information, see `Monitoring with alarms <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/monitor-alarms.html>`_ in the *AWS IoT SiteWise Application Guide* .

            :param alarm_role_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the IAM role that allows the alarm to perform actions and access AWS resources and services, such as AWS IoT Events .
            :param notification_lambda_arn: The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the Lambda function that manages alarm notifications. For more information, see `Managing alarm notifications <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ in the *AWS IoT Events Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-alarms.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                alarms_property = iotsitewise_mixins.CfnPortalPropsMixin.AlarmsProperty(
                    alarm_role_arn="alarmRoleArn",
                    notification_lambda_arn="notificationLambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1ae5b91fef5bdaf2a24cafeee3833a216dc8bed3cae676c1b5bf691a42242a60)
                check_type(argname="argument alarm_role_arn", value=alarm_role_arn, expected_type=type_hints["alarm_role_arn"])
                check_type(argname="argument notification_lambda_arn", value=notification_lambda_arn, expected_type=type_hints["notification_lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_role_arn is not None:
                self._values["alarm_role_arn"] = alarm_role_arn
            if notification_lambda_arn is not None:
                self._values["notification_lambda_arn"] = notification_lambda_arn

        @builtins.property
        def alarm_role_arn(self) -> typing.Optional[builtins.str]:
            '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the IAM role that allows the alarm to perform actions and access AWS resources and services, such as AWS IoT Events .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-alarms.html#cfn-iotsitewise-portal-alarms-alarmrolearn
            '''
            result = self._values.get("alarm_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def notification_lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The `ARN <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ of the Lambda function that manages alarm notifications. For more information, see `Managing alarm notifications <https://docs.aws.amazon.com/iotevents/latest/developerguide/lambda-support.html>`_ in the *AWS IoT Events Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-alarms.html#cfn-iotsitewise-portal-alarms-notificationlambdaarn
            '''
            result = self._values.get("notification_lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AlarmsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnPortalPropsMixin.PortalTypeEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"portal_tools": "portalTools"},
    )
    class PortalTypeEntryProperty:
        def __init__(
            self,
            *,
            portal_tools: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Container associated a certain PortalType.

            :param portal_tools: The array of tools associated with the specified portal type. The possible values are ``ASSISTANT`` and ``DASHBOARD`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-portaltypeentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
                
                portal_type_entry_property = iotsitewise_mixins.CfnPortalPropsMixin.PortalTypeEntryProperty(
                    portal_tools=["portalTools"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a367187b245851aa52aa7f073d200b23f3cba34282390705927e55aa61f6037)
                check_type(argname="argument portal_tools", value=portal_tools, expected_type=type_hints["portal_tools"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if portal_tools is not None:
                self._values["portal_tools"] = portal_tools

        @builtins.property
        def portal_tools(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of tools associated with the specified portal type.

            The possible values are ``ASSISTANT`` and ``DASHBOARD`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotsitewise-portal-portaltypeentry.html#cfn-iotsitewise-portal-portaltypeentry-portaltools
            '''
            result = self._values.get("portal_tools")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortalTypeEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "asset_ids": "assetIds",
        "portal_id": "portalId",
        "project_description": "projectDescription",
        "project_name": "projectName",
        "tags": "tags",
    },
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        asset_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        portal_id: typing.Optional[builtins.str] = None,
        project_description: typing.Optional[builtins.str] = None,
        project_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param asset_ids: A list that contains the IDs of each asset associated with the project.
        :param portal_id: The ID of the portal in which to create the project.
        :param project_description: A description for the project.
        :param project_name: A friendly name for the project.
        :param tags: A list of key-value pairs that contain metadata for the project. For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
            
            cfn_project_mixin_props = iotsitewise_mixins.CfnProjectMixinProps(
                asset_ids=["assetIds"],
                portal_id="portalId",
                project_description="projectDescription",
                project_name="projectName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5b4ea8e2cf11cbfc0bd74ee1269db67546f69c510e2ba1628eaedfe0b8e633)
            check_type(argname="argument asset_ids", value=asset_ids, expected_type=type_hints["asset_ids"])
            check_type(argname="argument portal_id", value=portal_id, expected_type=type_hints["portal_id"])
            check_type(argname="argument project_description", value=project_description, expected_type=type_hints["project_description"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_ids is not None:
            self._values["asset_ids"] = asset_ids
        if portal_id is not None:
            self._values["portal_id"] = portal_id
        if project_description is not None:
            self._values["project_description"] = project_description
        if project_name is not None:
            self._values["project_name"] = project_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def asset_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list that contains the IDs of each asset associated with the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-assetids
        '''
        result = self._values.get("asset_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def portal_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the portal in which to create the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-portalid
        '''
        result = self._values.get("portal_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_description(self) -> typing.Optional[builtins.str]:
        '''A description for the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-projectdescription
        '''
        result = self._values.get("project_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name for the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-projectname
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of key-value pairs that contain metadata for the project.

        For more information, see `Tagging your AWS IoT SiteWise resources <https://docs.aws.amazon.com/iot-sitewise/latest/userguide/tag-resources.html>`_ in the *AWS IoT SiteWise User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html#cfn-iotsitewise-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iotsitewise.mixins.CfnProjectPropsMixin",
):
    '''.. epigraph::

   The AWS IoT SiteWise Monitor feature will no longer be open to new customers starting November 7, 2025 .

    If you would like to use the AWS IoT SiteWise Monitor feature, sign up prior to that date. Existing customers can continue to use the service as normal. For more information, see `AWS IoT SiteWise Monitor availability change <https://docs.aws.amazon.com/iot-sitewise/latest/appguide/iotsitewise-monitor-availability-change.html>`_ .

    Creates a project in the specified portal.
    .. epigraph::

       Make sure that the project name and description don't contain confidential information.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotsitewise-project.html
    :cloudformationResource: AWS::IoTSiteWise::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iotsitewise import mixins as iotsitewise_mixins
        
        cfn_project_props_mixin = iotsitewise_mixins.CfnProjectPropsMixin(iotsitewise_mixins.CfnProjectMixinProps(
            asset_ids=["assetIds"],
            portal_id="portalId",
            project_description="projectDescription",
            project_name="projectName",
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
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IoTSiteWise::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d270bf9b141f1509332165fd62343299036acc1c0ced3a8eb8915b61ea05df9f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9268177c19e6d52c802791f94937702f7c6e373ac483d8c512c1c2e6044ae6b7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24e693cfee71638be0e4aaf213799a3cceaa649faf92bbb30caee8b99149aacb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAccessPolicyMixinProps",
    "CfnAccessPolicyPropsMixin",
    "CfnAssetMixinProps",
    "CfnAssetModelMixinProps",
    "CfnAssetModelPropsMixin",
    "CfnAssetPropsMixin",
    "CfnComputationModelMixinProps",
    "CfnComputationModelPropsMixin",
    "CfnDashboardMixinProps",
    "CfnDashboardPropsMixin",
    "CfnDatasetMixinProps",
    "CfnDatasetPropsMixin",
    "CfnGatewayMixinProps",
    "CfnGatewayPropsMixin",
    "CfnPortalMixinProps",
    "CfnPortalPropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectPropsMixin",
]

publication.publish()

def _typecheckingstub__60ba3197eb03e24ac1b4baad565e4034d9540b6e2237fdb4048a77f508bfdbc2(
    *,
    access_policy_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.AccessPolicyIdentityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    access_policy_permission: typing.Optional[builtins.str] = None,
    access_policy_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.AccessPolicyResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee19fcb7fe6f7ecdf032765d85996bf45e8d87930cad57a525a2c3985330716(
    props: typing.Union[CfnAccessPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b891abe155649965105dfcfc834de4c98af6156bc6bb0449243f52684c678c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f2d78c380b9ddf50fb8ebe5fa8124ebbf3adaad0539cf183d68f13a2c3ef55(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3633858c7b39ce6eef7bcd631db9354135fe807cd00da82f2cf58bf4d42eaa6(
    *,
    iam_role: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.IamRoleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    iam_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.IamUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.UserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b08471238b1145803210592f37ace7196d6d0e7d4cf78fbac74f21613409ea(
    *,
    portal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.PortalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    project: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessPolicyPropsMixin.ProjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9e460349e8698ba4c9e17d2265ad865f0212635971a46a42e50360c3a6b500(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3684d26436a9383d739e5e81d799713b24dd05622c74ead3984ac9eb8ac72a2(
    *,
    arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15d639e4c17daf8a21256e9f0ce77c4e7fbbf05a202c51f4553c37b0f4bce69(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86aa039711c0d511d5d709f3cf3d093dbde20dfb349a76ad10dfbaa2828c41e3(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b0131dc793dcc13e38b4bf9e06013d51e579ec7c4e33ca6ed8c3be08b37da3d(
    *,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19b35f584fa63fb70614867d69366ba08a0d97df2408336a30bab6953d4951a(
    *,
    asset_description: typing.Optional[builtins.str] = None,
    asset_external_id: typing.Optional[builtins.str] = None,
    asset_hierarchies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetPropsMixin.AssetHierarchyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    asset_model_id: typing.Optional[builtins.str] = None,
    asset_name: typing.Optional[builtins.str] = None,
    asset_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetPropsMixin.AssetPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aec01792f61cb9eb8d8bb3da9ff3a7175dbd936e61662af47a9cbba2c554114a(
    *,
    asset_model_composite_models: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.AssetModelCompositeModelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    asset_model_description: typing.Optional[builtins.str] = None,
    asset_model_external_id: typing.Optional[builtins.str] = None,
    asset_model_hierarchies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.AssetModelHierarchyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    asset_model_name: typing.Optional[builtins.str] = None,
    asset_model_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.AssetModelPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    asset_model_type: typing.Optional[builtins.str] = None,
    enforced_asset_model_interface_relationships: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.EnforcedAssetModelInterfaceRelationshipProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03848ea7301b041003f3f7926bb1f8acf7aa285754b17a42b10eafd646c2e4ff(
    props: typing.Union[CfnAssetModelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d9a3fb9b84ef29adaa2102a33cd31291f2e5e13c0caa4ddb11c85e5a365e2b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0178d116fa4d6a18e7c0f91d47f8f50e00283a0a319a720ae220ceeda0de369c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a323731b49f95fc9d33b7bb9a49e5767e711b51410172e929430c142020ca6f0(
    *,
    composed_asset_model_id: typing.Optional[builtins.str] = None,
    composite_model_properties: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.AssetModelPropertyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    parent_asset_model_composite_model_external_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86e5aad55f1fc50d6fdc90b86bf2e070c2f4c5d4d4e6e84070b7d15d565d840c(
    *,
    child_asset_model_id: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logical_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24c2297ac18add804df77cc24025c4e967eab3aa8f1a1ca94ac6d33926c98422(
    *,
    data_type: typing.Optional[builtins.str] = None,
    data_type_spec: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logical_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.PropertyTypeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0724e3693b16652c412c1720ac26bebf81113b22b527e6313f4fe1f402ceb845(
    *,
    default_value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7888f86aeb21200298f28694fba2f1c73644a3d2d1aedc32b72996855fa152f(
    *,
    asset_model_property_external_id: typing.Optional[builtins.str] = None,
    asset_model_property_logical_id: typing.Optional[builtins.str] = None,
    interface_asset_model_property_external_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff3043c6e7b68bc121ebc6e8528c0392375786157417455fec6c944c960b18f9(
    *,
    interface_asset_model_id: typing.Optional[builtins.str] = None,
    property_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.EnforcedAssetModelInterfacePropertyMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9c8da0b975dd29e1ac642001998703f4dcc8c15e9bf05203079cd8a19300883(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.VariableValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07089c907e8797833da848d36c129da00f8d686b46f28db24edfa8ddb6f9c55(
    *,
    expression: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.ExpressionVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    window: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.MetricWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b44ddee2b61caf8d0989ff10881efb65ee5d6927daf7c3810dac1269fe9f37a(
    *,
    tumbling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.TumblingWindowProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78ac092b6ca433f8fd73170ab9841eccaf9332745dce487813f88d9a1052ef1d(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1425c9072cde93d5f33638362cfe23804d02af310d22c6c04c1428bfd7edcc(
    *,
    attribute: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.AttributeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metric: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.MetricProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.TransformProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c972e66e1fbe917365587c44ea9e1522a725575d1a05bb8dbe0657ee15b990ae(
    *,
    expression: typing.Optional[builtins.str] = None,
    variables: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.ExpressionVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e64a9d184207666a72082862697e9685e593a66c078eb8373f740186599be9f(
    *,
    interval: typing.Optional[builtins.str] = None,
    offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad675896dbae731730632b6365b4d627e68db8784987d5472971c879725de68(
    *,
    hierarchy_external_id: typing.Optional[builtins.str] = None,
    hierarchy_id: typing.Optional[builtins.str] = None,
    hierarchy_logical_id: typing.Optional[builtins.str] = None,
    property_external_id: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
    property_logical_id: typing.Optional[builtins.str] = None,
    property_path: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAssetModelPropsMixin.PropertyPathDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e67f68deb0bfbe05f1019ab5997304c5755c2a146896fa04a762508db186604(
    props: typing.Union[CfnAssetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ca71fb8e4955facfc28b5495be55e909286fc0b26a462d001eb38ab4bf88991(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93080cac718b60e9b1394c30d673ecae46d26a13fbbc10297dce0e03affb1574(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373a15009838ac88d6a4d0c0616900c3522339370495a8c3fb5cbe47fd472849(
    *,
    child_asset_id: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logical_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a04950ecc067e02a227e9dec9ce11fd3bdd7f64875fdabd7cc4fb6625b4af2(
    *,
    alias: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    logical_id: typing.Optional[builtins.str] = None,
    notification_state: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02ea665cd064f65ce4d47f7ee1effcaf3b4e8b36ec9e2afd540b0982702c082(
    *,
    computation_model_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputationModelPropsMixin.ComputationModelConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    computation_model_data_binding: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    computation_model_description: typing.Optional[builtins.str] = None,
    computation_model_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2078012b63cdc9f9080294534acffdc1fa3cbeee50f08a32448d358de1cf78d(
    props: typing.Union[CfnComputationModelMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec036da5a481ab4d90433311c42492ea577402d6441b5022a53d1766c5973122(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61377acff0a2e93329775ff41714a31ada59cc40e4a323704c168d95b27c307a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22b9aedc70fcf70e3783490c5cf31ee4e5eee99cd86661ab076fd7417fd95800(
    *,
    input_properties: typing.Optional[builtins.str] = None,
    result_property: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e306ecad84c22ba508efbb8a9a66ad3c69f5286f7f41aa1b91cfb6de11938001(
    *,
    asset_model_id: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77830f864b1a25badf7b788c0e1c82b96dc4b1bfac921e3395f8e96a1ab5b512(
    *,
    asset_id: typing.Optional[builtins.str] = None,
    property_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae9439abc990b52def1ed50c748b11a8e8434950628dc29aac11caf966994b1(
    *,
    anomaly_detection: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputationModelPropsMixin.AnomalyDetectionComputationModelConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__311dff77549a1a3d04ed8c991736a061de4fc6d066e5e1e43a2ed21e3fb35b32(
    *,
    asset_model_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputationModelPropsMixin.AssetModelPropertyBindingValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    asset_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputationModelPropsMixin.AssetPropertyBindingValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnComputationModelPropsMixin.ComputationModelDataBindingValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779982b4818869a3996bf93486f539d38611f61e3dbb16e4f3637f89e487e734(
    *,
    dashboard_definition: typing.Optional[builtins.str] = None,
    dashboard_description: typing.Optional[builtins.str] = None,
    dashboard_name: typing.Optional[builtins.str] = None,
    project_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d493037726f626dd33244d11175341ae7b725867fb3c03903b0f0097f6507e8a(
    props: typing.Union[CfnDashboardMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f611cf18f640531e3cd4dd03e7036c14220d84a27e4ca157c76da2771e43569e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d255bec8fc335a9ced1a828b5d0da01606d2b2efd89a34fbcaec6c543196ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__887d927bb2a9b0d4ebaf0d7478aa4e948fcfecd2fc0ff742ca9b35872f574301(
    *,
    dataset_description: typing.Optional[builtins.str] = None,
    dataset_name: typing.Optional[builtins.str] = None,
    dataset_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatasetSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02958fe39016b80d1ccb64f4c578b9ec7d3734646548a1dcea741e35d3686d6f(
    props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ad9e2259ed9ac4d232c951c38239a0b3d6110e81fcf32da8adf3e3becac67ad(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dc9c3fd73b87b87e150dc22b3a28834adf3ea76a1140322c2cb2c7cf7cc4de(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a69d8e5e7aeb520066483dbd7a5a67f61051ab9e4ed90310ddda77fbcd4b094b(
    *,
    source_detail: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.SourceDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source_format: typing.Optional[builtins.str] = None,
    source_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e36e03be816067243e362049c04c676adb39d20b8683d89f650816f2c74955(
    *,
    knowledge_base_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad275725c1332e72ca82de0af82ad4a838d0bdd1c5effdc127d2b2c30f8f940(
    *,
    kendra: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.KendraSourceDetailProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae07484d64a9107e9bbbcb5cadb345d581ac7c545f0fb5cd0d910356e9de449(
    *,
    gateway_capability_summaries: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.GatewayCapabilitySummaryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    gateway_name: typing.Optional[builtins.str] = None,
    gateway_platform: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.GatewayPlatformProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    gateway_version: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5bd5ace143e5558bb5683d5c11573b409a50d7f8d9114c4fa42bb5c6b8daa2(
    props: typing.Union[CfnGatewayMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cbf305ce8d3e09c8ec950ce55f32c9a089a7da9e495ef728f3ef24b756c5f56(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae4a9719a9f1bc3c9af4d7b3319cdc37f313a1bc8887e7839bf47a80eeba34f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4683e676cfe0db9a6f08e081f63571f80351804c0d2b6c335bba0e5890c1742(
    *,
    capability_configuration: typing.Optional[builtins.str] = None,
    capability_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6104f7501aea12898788cc70d47ddf797353c7f8f4a1b2952b337006fa2aa9a5(
    *,
    greengrass: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.GreengrassProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    greengrass_v2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.GreengrassV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    siemens_ie: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGatewayPropsMixin.SiemensIEProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02689eee67f71fcf45b7daa598b1f97a6e7b8775912eb7580d898bd54e3bac06(
    *,
    group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb0dc9c0b02ee2cfa59047535727c60c0c42dbff8cd251aa93a8d9888446097(
    *,
    core_device_operating_system: typing.Optional[builtins.str] = None,
    core_device_thing_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4caa984f38500b273e01689fa304d82c98239f95c087f8017a19e8fa78454e9b(
    *,
    iot_core_thing_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669e2fb033eedf92e0452c81c64627cc0226b41aea4132ddc0195c6565fcb14(
    *,
    alarms: typing.Any = None,
    notification_sender_email: typing.Optional[builtins.str] = None,
    portal_auth_mode: typing.Optional[builtins.str] = None,
    portal_contact_email: typing.Optional[builtins.str] = None,
    portal_description: typing.Optional[builtins.str] = None,
    portal_name: typing.Optional[builtins.str] = None,
    portal_type: typing.Optional[builtins.str] = None,
    portal_type_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPortalPropsMixin.PortalTypeEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfb12d05184b7c3305880c91b5cfa25293ab7d0689017b967385b1be9692172c(
    props: typing.Union[CfnPortalMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f68a5961e58721e333074f737add6368e2d35429ed635ba8754cd2a8bceeb91(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b86336d610ce09d9d8da335fd96bee966fb92d6946151fead06abc62c5b892(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ae5b91fef5bdaf2a24cafeee3833a216dc8bed3cae676c1b5bf691a42242a60(
    *,
    alarm_role_arn: typing.Optional[builtins.str] = None,
    notification_lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a367187b245851aa52aa7f073d200b23f3cba34282390705927e55aa61f6037(
    *,
    portal_tools: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5b4ea8e2cf11cbfc0bd74ee1269db67546f69c510e2ba1628eaedfe0b8e633(
    *,
    asset_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    portal_id: typing.Optional[builtins.str] = None,
    project_description: typing.Optional[builtins.str] = None,
    project_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d270bf9b141f1509332165fd62343299036acc1c0ced3a8eb8915b61ea05df9f(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9268177c19e6d52c802791f94937702f7c6e373ac483d8c512c1c2e6044ae6b7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24e693cfee71638be0e4aaf213799a3cceaa649faf92bbb30caee8b99149aacb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
