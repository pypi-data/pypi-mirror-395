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
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAccessEntryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_policies": "accessPolicies",
        "cluster_name": "clusterName",
        "kubernetes_groups": "kubernetesGroups",
        "principal_arn": "principalArn",
        "tags": "tags",
        "type": "type",
        "username": "username",
    },
)
class CfnAccessEntryMixinProps:
    def __init__(
        self,
        *,
        access_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessEntryPropsMixin.AccessPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        kubernetes_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        principal_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAccessEntryPropsMixin.

        :param access_policies: The access policies to associate to the access entry.
        :param cluster_name: The name of your cluster.
        :param kubernetes_groups: The value for ``name`` that you've specified for ``kind: Group`` as a ``subject`` in a Kubernetes ``RoleBinding`` or ``ClusterRoleBinding`` object. Amazon EKS doesn't confirm that the value for ``name`` exists in any bindings on your cluster. You can specify one or more names. Kubernetes authorizes the ``principalArn`` of the access entry to access any cluster objects that you've specified in a Kubernetes ``Role`` or ``ClusterRole`` object that is also specified in a binding's ``roleRef`` . For more information about creating Kubernetes ``RoleBinding`` , ``ClusterRoleBinding`` , ``Role`` , or ``ClusterRole`` objects, see `Using RBAC Authorization in the Kubernetes documentation <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/access-authn-authz/rbac/>`_ . If you want Amazon EKS to authorize the ``principalArn`` (instead of, or in addition to Kubernetes authorizing the ``principalArn`` ), you can associate one or more access policies to the access entry using ``AssociateAccessPolicy`` . If you associate any access policies, the ``principalARN`` has all permissions assigned in the associated access policies and all permissions in any Kubernetes ``Role`` or ``ClusterRole`` objects that the group names are bound to.
        :param principal_arn: The ARN of the IAM principal for the ``AccessEntry`` . You can specify one ARN for each access entry. You can't specify the same ARN in more than one access entry. This value can't be changed after access entry creation. The valid principals differ depending on the type of the access entry in the ``type`` field. For ``STANDARD`` access entries, you can use every IAM principal type. For nodes ( ``EC2`` (for EKS Auto Mode), ``EC2_LINUX`` , ``EC2_WINDOWS`` , ``FARGATE_LINUX`` , and ``HYBRID_LINUX`` ), the only valid ARN is IAM roles. You can't use the STS session principal type with access entries because this is a temporary principal for each session and not a permanent identity that can be assigned permissions. `IAM best practices <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#bp-users-federation-idp>`_ recommend using IAM roles with temporary credentials, rather than IAM users with long-term credentials.
        :param tags: Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.
        :param type: The type of the new access entry. Valid values are ``STANDARD`` , ``FARGATE_LINUX`` , ``EC2_LINUX`` , ``EC2_WINDOWS`` , ``EC2`` (for EKS Auto Mode), ``HYBRID_LINUX`` , and ``HYPERPOD_LINUX`` . If the ``principalArn`` is for an IAM role that's used for self-managed Amazon EC2 nodes, specify ``EC2_LINUX`` or ``EC2_WINDOWS`` . Amazon EKS grants the necessary permissions to the node for you. If the ``principalArn`` is for any other purpose, specify ``STANDARD`` . If you don't specify a value, Amazon EKS sets the value to ``STANDARD`` . If you have the access mode of the cluster set to ``API_AND_CONFIG_MAP`` , it's unnecessary to create access entries for IAM roles used with Fargate profiles or managed Amazon EC2 nodes, because Amazon EKS creates entries in the ``aws-auth`` ``ConfigMap`` for the roles. You can't change this value once you've created the access entry. If you set the value to ``EC2_LINUX`` or ``EC2_WINDOWS`` , you can't specify values for ``kubernetesGroups`` , or associate an ``AccessPolicy`` to the access entry.
        :param username: The username to authenticate to Kubernetes with. We recommend not specifying a username and letting Amazon EKS specify it for you. For more information about the value Amazon EKS specifies for you, or constraints before specifying your own username, see `Creating access entries <https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html#creating-access-entries>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_access_entry_mixin_props = eks_mixins.CfnAccessEntryMixinProps(
                access_policies=[eks_mixins.CfnAccessEntryPropsMixin.AccessPolicyProperty(
                    access_scope=eks_mixins.CfnAccessEntryPropsMixin.AccessScopeProperty(
                        namespaces=["namespaces"],
                        type="type"
                    ),
                    policy_arn="policyArn"
                )],
                cluster_name="clusterName",
                kubernetes_groups=["kubernetesGroups"],
                principal_arn="principalArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type",
                username="username"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1156c03c75ecb82707ffe98344bf14beccd767b3baea0ea988b41a4bcae836e0)
            check_type(argname="argument access_policies", value=access_policies, expected_type=type_hints["access_policies"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument kubernetes_groups", value=kubernetes_groups, expected_type=type_hints["kubernetes_groups"])
            check_type(argname="argument principal_arn", value=principal_arn, expected_type=type_hints["principal_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_policies is not None:
            self._values["access_policies"] = access_policies
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if kubernetes_groups is not None:
            self._values["kubernetes_groups"] = kubernetes_groups
        if principal_arn is not None:
            self._values["principal_arn"] = principal_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def access_policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessEntryPropsMixin.AccessPolicyProperty"]]]]:
        '''The access policies to associate to the access entry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-accesspolicies
        '''
        result = self._values.get("access_policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessEntryPropsMixin.AccessPolicyProperty"]]]], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of your cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kubernetes_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The value for ``name`` that you've specified for ``kind: Group`` as a ``subject`` in a Kubernetes ``RoleBinding`` or ``ClusterRoleBinding`` object.

        Amazon EKS doesn't confirm that the value for ``name`` exists in any bindings on your cluster. You can specify one or more names.

        Kubernetes authorizes the ``principalArn`` of the access entry to access any cluster objects that you've specified in a Kubernetes ``Role`` or ``ClusterRole`` object that is also specified in a binding's ``roleRef`` . For more information about creating Kubernetes ``RoleBinding`` , ``ClusterRoleBinding`` , ``Role`` , or ``ClusterRole`` objects, see `Using RBAC Authorization in the Kubernetes documentation <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/access-authn-authz/rbac/>`_ .

        If you want Amazon EKS to authorize the ``principalArn`` (instead of, or in addition to Kubernetes authorizing the ``principalArn`` ), you can associate one or more access policies to the access entry using ``AssociateAccessPolicy`` . If you associate any access policies, the ``principalARN`` has all permissions assigned in the associated access policies and all permissions in any Kubernetes ``Role`` or ``ClusterRole`` objects that the group names are bound to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-kubernetesgroups
        '''
        result = self._values.get("kubernetes_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principal_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM principal for the ``AccessEntry`` .

        You can specify one ARN for each access entry. You can't specify the same ARN in more than one access entry. This value can't be changed after access entry creation.

        The valid principals differ depending on the type of the access entry in the ``type`` field. For ``STANDARD`` access entries, you can use every IAM principal type. For nodes ( ``EC2`` (for EKS Auto Mode), ``EC2_LINUX`` , ``EC2_WINDOWS`` , ``FARGATE_LINUX`` , and ``HYBRID_LINUX`` ), the only valid ARN is IAM roles. You can't use the STS session principal type with access entries because this is a temporary principal for each session and not a permanent identity that can be assigned permissions.

        `IAM best practices <https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#bp-users-federation-idp>`_ recommend using IAM roles with temporary credentials, rather than IAM users with long-term credentials.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-principalarn
        '''
        result = self._values.get("principal_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that assists with categorization and organization.

        Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the new access entry.

        Valid values are ``STANDARD`` , ``FARGATE_LINUX`` , ``EC2_LINUX`` , ``EC2_WINDOWS`` , ``EC2`` (for EKS Auto Mode), ``HYBRID_LINUX`` , and ``HYPERPOD_LINUX`` .

        If the ``principalArn`` is for an IAM role that's used for self-managed Amazon EC2 nodes, specify ``EC2_LINUX`` or ``EC2_WINDOWS`` . Amazon EKS grants the necessary permissions to the node for you. If the ``principalArn`` is for any other purpose, specify ``STANDARD`` . If you don't specify a value, Amazon EKS sets the value to ``STANDARD`` . If you have the access mode of the cluster set to ``API_AND_CONFIG_MAP`` , it's unnecessary to create access entries for IAM roles used with Fargate profiles or managed Amazon EC2 nodes, because Amazon EKS creates entries in the ``aws-auth`` ``ConfigMap`` for the roles. You can't change this value once you've created the access entry.

        If you set the value to ``EC2_LINUX`` or ``EC2_WINDOWS`` , you can't specify values for ``kubernetesGroups`` , or associate an ``AccessPolicy`` to the access entry.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to authenticate to Kubernetes with.

        We recommend not specifying a username and letting Amazon EKS specify it for you. For more information about the value Amazon EKS specifies for you, or constraints before specifying your own username, see `Creating access entries <https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html#creating-access-entries>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html#cfn-eks-accessentry-username
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessEntryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessEntryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAccessEntryPropsMixin",
):
    '''Creates an access entry.

    An access entry allows an IAM principal to access your cluster. Access entries can replace the need to maintain entries in the ``aws-auth`` ``ConfigMap`` for authentication. You have the following options for authorizing an IAM principal to access Kubernetes objects on your cluster: Kubernetes role-based access control (RBAC), Amazon EKS, or both. Kubernetes RBAC authorization requires you to create and manage Kubernetes ``Role`` , ``ClusterRole`` , ``RoleBinding`` , and ``ClusterRoleBinding`` objects, in addition to managing access entries. If you use Amazon EKS authorization exclusively, you don't need to create and manage Kubernetes ``Role`` , ``ClusterRole`` , ``RoleBinding`` , and ``ClusterRoleBinding`` objects.

    For more information about access entries, see `Access entries <https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html>`_ in the *Amazon EKS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-accessentry.html
    :cloudformationResource: AWS::EKS::AccessEntry
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_access_entry_props_mixin = eks_mixins.CfnAccessEntryPropsMixin(eks_mixins.CfnAccessEntryMixinProps(
            access_policies=[eks_mixins.CfnAccessEntryPropsMixin.AccessPolicyProperty(
                access_scope=eks_mixins.CfnAccessEntryPropsMixin.AccessScopeProperty(
                    namespaces=["namespaces"],
                    type="type"
                ),
                policy_arn="policyArn"
            )],
            cluster_name="clusterName",
            kubernetes_groups=["kubernetesGroups"],
            principal_arn="principalArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type",
            username="username"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessEntryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::AccessEntry``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c97100c52aa262a44ac10663be49f670302b96d3e21036cac880569e887988)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28cae9fd0a4b7082ffdbd82b73b8cfbe63d188243a9e032bbaee7a61d60e05fd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c88f3c23ab18e4daeef256e5a6e7a31f80180d57f13ca5bc322f991df587888)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessEntryMixinProps:
        return typing.cast(CfnAccessEntryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAccessEntryPropsMixin.AccessPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"access_scope": "accessScope", "policy_arn": "policyArn"},
    )
    class AccessPolicyProperty:
        def __init__(
            self,
            *,
            access_scope: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccessEntryPropsMixin.AccessScopeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            policy_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An access policy includes permissions that allow Amazon EKS to authorize an IAM principal to work with Kubernetes objects on your cluster.

            The policies are managed by Amazon EKS, but they're not IAM policies. You can't view the permissions in the policies using the API. The permissions for many of the policies are similar to the Kubernetes ``cluster-admin`` , ``admin`` , ``edit`` , and ``view`` cluster roles. For more information about these cluster roles, see `User-facing roles <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/access-authn-authz/rbac/#user-facing-roles>`_ in the Kubernetes documentation. To view the contents of the policies, see `Access policy permissions <https://docs.aws.amazon.com/eks/latest/userguide/access-policies.html#access-policy-permissions>`_ in the *Amazon EKS User Guide* .

            :param access_scope: The scope of an ``AccessPolicy`` that's associated to an ``AccessEntry`` .
            :param policy_arn: The ARN of the access policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-accessentry-accesspolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                access_policy_property = eks_mixins.CfnAccessEntryPropsMixin.AccessPolicyProperty(
                    access_scope=eks_mixins.CfnAccessEntryPropsMixin.AccessScopeProperty(
                        namespaces=["namespaces"],
                        type="type"
                    ),
                    policy_arn="policyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__073f9428d5f81408532a02358f7aebf2621f9688b56530abcdae78fe8db0c005)
                check_type(argname="argument access_scope", value=access_scope, expected_type=type_hints["access_scope"])
                check_type(argname="argument policy_arn", value=policy_arn, expected_type=type_hints["policy_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_scope is not None:
                self._values["access_scope"] = access_scope
            if policy_arn is not None:
                self._values["policy_arn"] = policy_arn

        @builtins.property
        def access_scope(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessEntryPropsMixin.AccessScopeProperty"]]:
            '''The scope of an ``AccessPolicy`` that's associated to an ``AccessEntry`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-accessentry-accesspolicy.html#cfn-eks-accessentry-accesspolicy-accessscope
            '''
            result = self._values.get("access_scope")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccessEntryPropsMixin.AccessScopeProperty"]], result)

        @builtins.property
        def policy_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the access policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-accessentry-accesspolicy.html#cfn-eks-accessentry-accesspolicy-policyarn
            '''
            result = self._values.get("policy_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAccessEntryPropsMixin.AccessScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"namespaces": "namespaces", "type": "type"},
    )
    class AccessScopeProperty:
        def __init__(
            self,
            *,
            namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The scope of an ``AccessPolicy`` that's associated to an ``AccessEntry`` .

            :param namespaces: A Kubernetes ``namespace`` that an access policy is scoped to. A value is required if you specified ``namespace`` for ``Type`` .
            :param type: The scope type of an access policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-accessentry-accessscope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                access_scope_property = eks_mixins.CfnAccessEntryPropsMixin.AccessScopeProperty(
                    namespaces=["namespaces"],
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ad647e620ef50a99475aae64b02046734b44aaaa0524fa3325feeecdb408f17)
                check_type(argname="argument namespaces", value=namespaces, expected_type=type_hints["namespaces"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if namespaces is not None:
                self._values["namespaces"] = namespaces
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def namespaces(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A Kubernetes ``namespace`` that an access policy is scoped to.

            A value is required if you specified ``namespace`` for ``Type`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-accessentry-accessscope.html#cfn-eks-accessentry-accessscope-namespaces
            '''
            result = self._values.get("namespaces")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The scope type of an access policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-accessentry-accessscope.html#cfn-eks-accessentry-accessscope-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAddonMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "addon_name": "addonName",
        "addon_version": "addonVersion",
        "cluster_name": "clusterName",
        "configuration_values": "configurationValues",
        "namespace_config": "namespaceConfig",
        "pod_identity_associations": "podIdentityAssociations",
        "preserve_on_delete": "preserveOnDelete",
        "resolve_conflicts": "resolveConflicts",
        "service_account_role_arn": "serviceAccountRoleArn",
        "tags": "tags",
    },
)
class CfnAddonMixinProps:
    def __init__(
        self,
        *,
        addon_name: typing.Optional[builtins.str] = None,
        addon_version: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        configuration_values: typing.Optional[builtins.str] = None,
        namespace_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAddonPropsMixin.NamespaceConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        pod_identity_associations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAddonPropsMixin.PodIdentityAssociationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        preserve_on_delete: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resolve_conflicts: typing.Optional[builtins.str] = None,
        service_account_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAddonPropsMixin.

        :param addon_name: The name of the add-on.
        :param addon_version: The version of the add-on.
        :param cluster_name: The name of your cluster.
        :param configuration_values: The configuration values that you provided.
        :param namespace_config: The namespace configuration for the addon. This specifies the Kubernetes namespace where the addon is installed.
        :param pod_identity_associations: An array of EKS Pod Identity associations owned by the add-on. Each association maps a role to a service account in a namespace in the cluster. For more information, see `Attach an IAM Role to an Amazon EKS add-on using EKS Pod Identity <https://docs.aws.amazon.com/eks/latest/userguide/add-ons-iam.html>`_ in the *Amazon EKS User Guide* .
        :param preserve_on_delete: Specifying this option preserves the add-on software on your cluster but Amazon EKS stops managing any settings for the add-on. If an IAM account is associated with the add-on, it isn't removed.
        :param resolve_conflicts: How to resolve field value conflicts for an Amazon EKS add-on. Conflicts are handled based on the value you choose: - *None* – If the self-managed version of the add-on is installed on your cluster, Amazon EKS doesn't change the value. Creation of the add-on might fail. - *Overwrite* – If the self-managed version of the add-on is installed on your cluster and the Amazon EKS default value is different than the existing value, Amazon EKS changes the value to the Amazon EKS default value. - *Preserve* – This is similar to the NONE option. If the self-managed version of the add-on is installed on your cluster Amazon EKS doesn't change the add-on resource properties. Creation of the add-on might fail if conflicts are detected. This option works differently during the update operation. For more information, see ```UpdateAddon`` <https://docs.aws.amazon.com/eks/latest/APIReference/API_UpdateAddon.html>`_ . If you don't currently have the self-managed version of the add-on installed on your cluster, the Amazon EKS add-on is installed. Amazon EKS sets all values to default values, regardless of the option that you specify.
        :param service_account_role_arn: The Amazon Resource Name (ARN) of an existing IAM role to bind to the add-on's service account. The role must be assigned the IAM permissions required by the add-on. If you don't specify an existing IAM role, then the add-on uses the permissions assigned to the node IAM role. For more information, see `Amazon EKS node IAM role <https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html>`_ in the *Amazon EKS User Guide* . .. epigraph:: To specify an existing IAM role, you must have an IAM OpenID Connect (OIDC) provider created for your cluster. For more information, see `Enabling IAM roles for service accounts on your cluster <https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html>`_ in the *Amazon EKS User Guide* .
        :param tags: The metadata that you apply to the add-on to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Add-on tags do not propagate to any other resources associated with the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_addon_mixin_props = eks_mixins.CfnAddonMixinProps(
                addon_name="addonName",
                addon_version="addonVersion",
                cluster_name="clusterName",
                configuration_values="configurationValues",
                namespace_config=eks_mixins.CfnAddonPropsMixin.NamespaceConfigProperty(
                    namespace="namespace"
                ),
                pod_identity_associations=[eks_mixins.CfnAddonPropsMixin.PodIdentityAssociationProperty(
                    role_arn="roleArn",
                    service_account="serviceAccount"
                )],
                preserve_on_delete=False,
                resolve_conflicts="resolveConflicts",
                service_account_role_arn="serviceAccountRoleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce74297a0466688dc1bd80c3534de7e1052034a4be658f0f106a8e1fec3e7a40)
            check_type(argname="argument addon_name", value=addon_name, expected_type=type_hints["addon_name"])
            check_type(argname="argument addon_version", value=addon_version, expected_type=type_hints["addon_version"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument configuration_values", value=configuration_values, expected_type=type_hints["configuration_values"])
            check_type(argname="argument namespace_config", value=namespace_config, expected_type=type_hints["namespace_config"])
            check_type(argname="argument pod_identity_associations", value=pod_identity_associations, expected_type=type_hints["pod_identity_associations"])
            check_type(argname="argument preserve_on_delete", value=preserve_on_delete, expected_type=type_hints["preserve_on_delete"])
            check_type(argname="argument resolve_conflicts", value=resolve_conflicts, expected_type=type_hints["resolve_conflicts"])
            check_type(argname="argument service_account_role_arn", value=service_account_role_arn, expected_type=type_hints["service_account_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if addon_name is not None:
            self._values["addon_name"] = addon_name
        if addon_version is not None:
            self._values["addon_version"] = addon_version
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if configuration_values is not None:
            self._values["configuration_values"] = configuration_values
        if namespace_config is not None:
            self._values["namespace_config"] = namespace_config
        if pod_identity_associations is not None:
            self._values["pod_identity_associations"] = pod_identity_associations
        if preserve_on_delete is not None:
            self._values["preserve_on_delete"] = preserve_on_delete
        if resolve_conflicts is not None:
            self._values["resolve_conflicts"] = resolve_conflicts
        if service_account_role_arn is not None:
            self._values["service_account_role_arn"] = service_account_role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def addon_name(self) -> typing.Optional[builtins.str]:
        '''The name of the add-on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-addonname
        '''
        result = self._values.get("addon_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def addon_version(self) -> typing.Optional[builtins.str]:
        '''The version of the add-on.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-addonversion
        '''
        result = self._values.get("addon_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of your cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration_values(self) -> typing.Optional[builtins.str]:
        '''The configuration values that you provided.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-configurationvalues
        '''
        result = self._values.get("configuration_values")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAddonPropsMixin.NamespaceConfigProperty"]]:
        '''The namespace configuration for the addon.

        This specifies the Kubernetes namespace where the addon is installed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-namespaceconfig
        '''
        result = self._values.get("namespace_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAddonPropsMixin.NamespaceConfigProperty"]], result)

    @builtins.property
    def pod_identity_associations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAddonPropsMixin.PodIdentityAssociationProperty"]]]]:
        '''An array of EKS Pod Identity associations owned by the add-on.

        Each association maps a role to a service account in a namespace in the cluster.

        For more information, see `Attach an IAM Role to an Amazon EKS add-on using EKS Pod Identity <https://docs.aws.amazon.com/eks/latest/userguide/add-ons-iam.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-podidentityassociations
        '''
        result = self._values.get("pod_identity_associations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAddonPropsMixin.PodIdentityAssociationProperty"]]]], result)

    @builtins.property
    def preserve_on_delete(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifying this option preserves the add-on software on your cluster but Amazon EKS stops managing any settings for the add-on.

        If an IAM account is associated with the add-on, it isn't removed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-preserveondelete
        '''
        result = self._values.get("preserve_on_delete")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resolve_conflicts(self) -> typing.Optional[builtins.str]:
        '''How to resolve field value conflicts for an Amazon EKS add-on.

        Conflicts are handled based on the value you choose:

        - *None* – If the self-managed version of the add-on is installed on your cluster, Amazon EKS doesn't change the value. Creation of the add-on might fail.
        - *Overwrite* – If the self-managed version of the add-on is installed on your cluster and the Amazon EKS default value is different than the existing value, Amazon EKS changes the value to the Amazon EKS default value.
        - *Preserve* – This is similar to the NONE option. If the self-managed version of the add-on is installed on your cluster Amazon EKS doesn't change the add-on resource properties. Creation of the add-on might fail if conflicts are detected. This option works differently during the update operation. For more information, see ```UpdateAddon`` <https://docs.aws.amazon.com/eks/latest/APIReference/API_UpdateAddon.html>`_ .

        If you don't currently have the self-managed version of the add-on installed on your cluster, the Amazon EKS add-on is installed. Amazon EKS sets all values to default values, regardless of the option that you specify.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-resolveconflicts
        '''
        result = self._values.get("resolve_conflicts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an existing IAM role to bind to the add-on's service account.

        The role must be assigned the IAM permissions required by the add-on. If you don't specify an existing IAM role, then the add-on uses the permissions assigned to the node IAM role. For more information, see `Amazon EKS node IAM role <https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html>`_ in the *Amazon EKS User Guide* .
        .. epigraph::

           To specify an existing IAM role, you must have an IAM OpenID Connect (OIDC) provider created for your cluster. For more information, see `Enabling IAM roles for service accounts on your cluster <https://docs.aws.amazon.com/eks/latest/userguide/enable-iam-roles-for-service-accounts.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-serviceaccountrolearn
        '''
        result = self._values.get("service_account_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The metadata that you apply to the add-on to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Add-on tags do not propagate to any other resources associated with the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html#cfn-eks-addon-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAddonMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAddonPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAddonPropsMixin",
):
    '''Creates an Amazon EKS add-on.

    Amazon EKS add-ons help to automate the provisioning and lifecycle management of common operational software for Amazon EKS clusters. For more information, see `Amazon EKS add-ons <https://docs.aws.amazon.com/eks/latest/userguide/eks-add-ons.html>`_ in the *Amazon EKS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-addon.html
    :cloudformationResource: AWS::EKS::Addon
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_addon_props_mixin = eks_mixins.CfnAddonPropsMixin(eks_mixins.CfnAddonMixinProps(
            addon_name="addonName",
            addon_version="addonVersion",
            cluster_name="clusterName",
            configuration_values="configurationValues",
            namespace_config=eks_mixins.CfnAddonPropsMixin.NamespaceConfigProperty(
                namespace="namespace"
            ),
            pod_identity_associations=[eks_mixins.CfnAddonPropsMixin.PodIdentityAssociationProperty(
                role_arn="roleArn",
                service_account="serviceAccount"
            )],
            preserve_on_delete=False,
            resolve_conflicts="resolveConflicts",
            service_account_role_arn="serviceAccountRoleArn",
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
        props: typing.Union[CfnAddonMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::Addon``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc6db2e2c2b167fd1439ef52ccc426a4e56936e8e5890a4447a24562abe50d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01d25519d08c4bb7ce5a80ed901db03403a7b35925984f8e707cf49e0228f2bb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ac0c66e104e010dc5a0d93f70a23497ce51693044accfd23818dd9cf8471a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAddonMixinProps:
        return typing.cast(CfnAddonMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAddonPropsMixin.NamespaceConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"namespace": "namespace"},
    )
    class NamespaceConfigProperty:
        def __init__(self, *, namespace: typing.Optional[builtins.str] = None) -> None:
            '''The custom namespace configuration to use with the add-on.

            :param namespace: The custom namespace for creating the add-on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-addon-namespaceconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                namespace_config_property = eks_mixins.CfnAddonPropsMixin.NamespaceConfigProperty(
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7eda9fe54e66a6780045bc879d8510e4e7caa9a76b87c5538fbd2ff6e0a9e6d9)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The custom namespace for creating the add-on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-addon-namespaceconfig.html#cfn-eks-addon-namespaceconfig-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NamespaceConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnAddonPropsMixin.PodIdentityAssociationProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "service_account": "serviceAccount"},
    )
    class PodIdentityAssociationProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            service_account: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances.

            :param role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the Pods that use this service account.
            :param service_account: The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-addon-podidentityassociation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                pod_identity_association_property = eks_mixins.CfnAddonPropsMixin.PodIdentityAssociationProperty(
                    role_arn="roleArn",
                    service_account="serviceAccount"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__063b63afba958fb4c24a7358a691b11c722c8dee025b3096694e8736092950ce)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if service_account is not None:
                self._values["service_account"] = service_account

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role to associate with the service account.

            The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the Pods that use this service account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-addon-podidentityassociation.html#cfn-eks-addon-podidentityassociation-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_account(self) -> typing.Optional[builtins.str]:
            '''The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-addon-podidentityassociation.html#cfn-eks-addon-podidentityassociation-serviceaccount
            '''
            result = self._values.get("service_account")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PodIdentityAssociationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "capability_name": "capabilityName",
        "cluster_name": "clusterName",
        "configuration": "configuration",
        "delete_propagation_policy": "deletePropagationPolicy",
        "role_arn": "roleArn",
        "tags": "tags",
        "type": "type",
    },
)
class CfnCapabilityMixinProps:
    def __init__(
        self,
        *,
        capability_name: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.CapabilityConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        delete_propagation_policy: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCapabilityPropsMixin.

        :param capability_name: A unique name for the capability. The name must be unique within your cluster and can contain alphanumeric characters, hyphens, and underscores.
        :param cluster_name: The name of the EKS cluster where you want to create the capability.
        :param configuration: Configuration settings for a capability. The structure of this object varies depending on the capability type.
        :param delete_propagation_policy: Specifies how Kubernetes resources managed by the capability should be handled when the capability is deleted. Currently, the only supported value is RETAIN which retains all Kubernetes resources managed by the capability when the capability is deleted.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that the capability uses to interact with AWS services. This role must have a trust policy that allows the EKS service principal to assume it, and it must have the necessary permissions for the capability type you're creating.
        :param tags: An array of key-value pairs to apply to this resource.
        :param type: The type of capability to create. Valid values are: ACK (AWS Controllers for Kubernetes, which lets you manage AWS resources directly from Kubernetes), ARGOCD (Argo CD for GitOps-based continuous delivery), or KRO (Kube Resource Orchestrator for composing and managing custom Kubernetes resources).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_capability_mixin_props = eks_mixins.CfnCapabilityMixinProps(
                capability_name="capabilityName",
                cluster_name="clusterName",
                configuration=eks_mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty(
                    argo_cd=eks_mixins.CfnCapabilityPropsMixin.ArgoCdProperty(
                        aws_idc=eks_mixins.CfnCapabilityPropsMixin.AwsIdcProperty(
                            idc_instance_arn="idcInstanceArn",
                            idc_managed_application_arn="idcManagedApplicationArn",
                            idc_region="idcRegion"
                        ),
                        namespace="namespace",
                        network_access=eks_mixins.CfnCapabilityPropsMixin.NetworkAccessProperty(
                            vpce_ids=["vpceIds"]
                        ),
                        rbac_role_mappings=[eks_mixins.CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty(
                            identities=[eks_mixins.CfnCapabilityPropsMixin.SsoIdentityProperty(
                                id="id",
                                type="type"
                            )],
                            role="role"
                        )],
                        server_url="serverUrl"
                    )
                ),
                delete_propagation_policy="deletePropagationPolicy",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d01108725c81e0073efea146d54ea809de3889302fb72866c9b72e76295b5d9)
            check_type(argname="argument capability_name", value=capability_name, expected_type=type_hints["capability_name"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument delete_propagation_policy", value=delete_propagation_policy, expected_type=type_hints["delete_propagation_policy"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if capability_name is not None:
            self._values["capability_name"] = capability_name
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if configuration is not None:
            self._values["configuration"] = configuration
        if delete_propagation_policy is not None:
            self._values["delete_propagation_policy"] = delete_propagation_policy
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def capability_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the capability.

        The name must be unique within your cluster and can contain alphanumeric characters, hyphens, and underscores.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-capabilityname
        '''
        result = self._values.get("capability_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the EKS cluster where you want to create the capability.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.CapabilityConfigurationProperty"]]:
        '''Configuration settings for a capability.

        The structure of this object varies depending on the capability type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.CapabilityConfigurationProperty"]], result)

    @builtins.property
    def delete_propagation_policy(self) -> typing.Optional[builtins.str]:
        '''Specifies how Kubernetes resources managed by the capability should be handled when the capability is deleted.

        Currently, the only supported value is RETAIN which retains all Kubernetes resources managed by the capability when the capability is deleted.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-deletepropagationpolicy
        '''
        result = self._values.get("delete_propagation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that the capability uses to interact with AWS services.

        This role must have a trust policy that allows the EKS service principal to assume it, and it must have the necessary permissions for the capability type you're creating.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of capability to create.

        Valid values are: ACK (AWS Controllers for Kubernetes, which lets you manage AWS resources directly from Kubernetes), ARGOCD (Argo CD for GitOps-based continuous delivery), or KRO (Kube Resource Orchestrator for composing and managing custom Kubernetes resources).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html#cfn-eks-capability-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCapabilityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCapabilityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin",
):
    '''Resource Type definition for EKS Capability.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-capability.html
    :cloudformationResource: AWS::EKS::Capability
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_capability_props_mixin = eks_mixins.CfnCapabilityPropsMixin(eks_mixins.CfnCapabilityMixinProps(
            capability_name="capabilityName",
            cluster_name="clusterName",
            configuration=eks_mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty(
                argo_cd=eks_mixins.CfnCapabilityPropsMixin.ArgoCdProperty(
                    aws_idc=eks_mixins.CfnCapabilityPropsMixin.AwsIdcProperty(
                        idc_instance_arn="idcInstanceArn",
                        idc_managed_application_arn="idcManagedApplicationArn",
                        idc_region="idcRegion"
                    ),
                    namespace="namespace",
                    network_access=eks_mixins.CfnCapabilityPropsMixin.NetworkAccessProperty(
                        vpce_ids=["vpceIds"]
                    ),
                    rbac_role_mappings=[eks_mixins.CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty(
                        identities=[eks_mixins.CfnCapabilityPropsMixin.SsoIdentityProperty(
                            id="id",
                            type="type"
                        )],
                        role="role"
                    )],
                    server_url="serverUrl"
                )
            ),
            delete_propagation_policy="deletePropagationPolicy",
            role_arn="roleArn",
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
        props: typing.Union[CfnCapabilityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::Capability``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eed663ca5d7f84d7dc9ac5906b2fcdb893198e3b67c5eaa1f1ffc93e23942655)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5be9e16455e0c413d2bade4270b60add2e7013ede22b7ad2106b7198d5f74beb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd3e101b1ce07af649131bfaf29c6003f7c2f8480f78f9958cce4f7fa1059139)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCapabilityMixinProps:
        return typing.cast(CfnCapabilityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin.ArgoCdProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aws_idc": "awsIdc",
            "namespace": "namespace",
            "network_access": "networkAccess",
            "rbac_role_mappings": "rbacRoleMappings",
            "server_url": "serverUrl",
        },
    )
    class ArgoCdProperty:
        def __init__(
            self,
            *,
            aws_idc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.AwsIdcProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            namespace: typing.Optional[builtins.str] = None,
            network_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.NetworkAccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rbac_role_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            server_url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for an Argo CD capability.

            This includes the Kubernetes namespace, IAM Identity Center integration, RBAC role mappings, and network access configuration.

            :param aws_idc: Configuration for integrating Argo CD with IAM Identity Center. This allows you to use your organization's identity provider for authentication to Argo CD.
            :param namespace: The Kubernetes namespace where Argo CD resources will be created. If not specified, the default namespace is used.
            :param network_access: Configuration for network access to the Argo CD capability's managed API server endpoint. By default, the Argo CD server is accessible via a public endpoint. You can optionally specify one or more VPC endpoint IDs to enable private connectivity from your VPCs.
            :param rbac_role_mappings: A list of role mappings that define which IAM Identity Center users or groups have which Argo CD roles. Each mapping associates an Argo CD role (ADMIN, EDITOR, or VIEWER) with one or more IAM Identity Center identities.
            :param server_url: The URL of the Argo CD server. Use this URL to access the Argo CD web interface and API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocd.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                argo_cd_property = eks_mixins.CfnCapabilityPropsMixin.ArgoCdProperty(
                    aws_idc=eks_mixins.CfnCapabilityPropsMixin.AwsIdcProperty(
                        idc_instance_arn="idcInstanceArn",
                        idc_managed_application_arn="idcManagedApplicationArn",
                        idc_region="idcRegion"
                    ),
                    namespace="namespace",
                    network_access=eks_mixins.CfnCapabilityPropsMixin.NetworkAccessProperty(
                        vpce_ids=["vpceIds"]
                    ),
                    rbac_role_mappings=[eks_mixins.CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty(
                        identities=[eks_mixins.CfnCapabilityPropsMixin.SsoIdentityProperty(
                            id="id",
                            type="type"
                        )],
                        role="role"
                    )],
                    server_url="serverUrl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3c56d64eaa4a8e40468dfd88cf78066cd65db34b295bcf031db97bcb65d4151b)
                check_type(argname="argument aws_idc", value=aws_idc, expected_type=type_hints["aws_idc"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument network_access", value=network_access, expected_type=type_hints["network_access"])
                check_type(argname="argument rbac_role_mappings", value=rbac_role_mappings, expected_type=type_hints["rbac_role_mappings"])
                check_type(argname="argument server_url", value=server_url, expected_type=type_hints["server_url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_idc is not None:
                self._values["aws_idc"] = aws_idc
            if namespace is not None:
                self._values["namespace"] = namespace
            if network_access is not None:
                self._values["network_access"] = network_access
            if rbac_role_mappings is not None:
                self._values["rbac_role_mappings"] = rbac_role_mappings
            if server_url is not None:
                self._values["server_url"] = server_url

        @builtins.property
        def aws_idc(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.AwsIdcProperty"]]:
            '''Configuration for integrating Argo CD with IAM Identity Center.

            This allows you to use your organization's identity provider for authentication to Argo CD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocd.html#cfn-eks-capability-argocd-awsidc
            '''
            result = self._values.get("aws_idc")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.AwsIdcProperty"]], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The Kubernetes namespace where Argo CD resources will be created.

            If not specified, the default namespace is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocd.html#cfn-eks-capability-argocd-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.NetworkAccessProperty"]]:
            '''Configuration for network access to the Argo CD capability's managed API server endpoint.

            By default, the Argo CD server is accessible via a public endpoint. You can optionally specify one or more VPC endpoint IDs to enable private connectivity from your VPCs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocd.html#cfn-eks-capability-argocd-networkaccess
            '''
            result = self._values.get("network_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.NetworkAccessProperty"]], result)

        @builtins.property
        def rbac_role_mappings(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty"]]]]:
            '''A list of role mappings that define which IAM Identity Center users or groups have which Argo CD roles.

            Each mapping associates an Argo CD role (ADMIN, EDITOR, or VIEWER) with one or more IAM Identity Center identities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocd.html#cfn-eks-capability-argocd-rbacrolemappings
            '''
            result = self._values.get("rbac_role_mappings")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty"]]]], result)

        @builtins.property
        def server_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the Argo CD server.

            Use this URL to access the Argo CD web interface and API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocd.html#cfn-eks-capability-argocd-serverurl
            '''
            result = self._values.get("server_url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArgoCdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"identities": "identities", "role": "role"},
    )
    class ArgoCdRoleMappingProperty:
        def __init__(
            self,
            *,
            identities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.SsoIdentityProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A mapping between an Argo CD role and IAM Identity Center identities.

            This defines which users or groups have specific permissions in Argo CD.

            :param identities: A list of IAM Identity Center identities (users or groups) that should be assigned this Argo CD role.
            :param role: The Argo CD role to assign. Valid values are: ADMIN (full administrative access to Argo CD), EDITOR (edit access to Argo CD resources), or VIEWER (read-only access to Argo CD resources).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocdrolemapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                argo_cd_role_mapping_property = eks_mixins.CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty(
                    identities=[eks_mixins.CfnCapabilityPropsMixin.SsoIdentityProperty(
                        id="id",
                        type="type"
                    )],
                    role="role"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__011c506d5b317d0194c59e8916f995eddef76a2fb217ee6bbdf5c1c6e8903aae)
                check_type(argname="argument identities", value=identities, expected_type=type_hints["identities"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if identities is not None:
                self._values["identities"] = identities
            if role is not None:
                self._values["role"] = role

        @builtins.property
        def identities(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.SsoIdentityProperty"]]]]:
            '''A list of IAM Identity Center identities (users or groups) that should be assigned this Argo CD role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocdrolemapping.html#cfn-eks-capability-argocdrolemapping-identities
            '''
            result = self._values.get("identities")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.SsoIdentityProperty"]]]], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''The Argo CD role to assign.

            Valid values are: ADMIN (full administrative access to Argo CD), EDITOR (edit access to Argo CD resources), or VIEWER (read-only access to Argo CD resources).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-argocdrolemapping.html#cfn-eks-capability-argocdrolemapping-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ArgoCdRoleMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin.AwsIdcProperty",
        jsii_struct_bases=[],
        name_mapping={
            "idc_instance_arn": "idcInstanceArn",
            "idc_managed_application_arn": "idcManagedApplicationArn",
            "idc_region": "idcRegion",
        },
    )
    class AwsIdcProperty:
        def __init__(
            self,
            *,
            idc_instance_arn: typing.Optional[builtins.str] = None,
            idc_managed_application_arn: typing.Optional[builtins.str] = None,
            idc_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for integrating Argo CD with IAM Identity Center.

            This allows you to use your organization's identity provider for authentication to Argo CD.

            :param idc_instance_arn: The ARN of the IAM Identity Center instance to use for authentication.
            :param idc_managed_application_arn: The ARN of the managed application created in IAM Identity Center for this Argo CD capability. This application is automatically created and managed by EKS.
            :param idc_region: The Region where your IAM Identity Center instance is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-awsidc.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                aws_idc_property = eks_mixins.CfnCapabilityPropsMixin.AwsIdcProperty(
                    idc_instance_arn="idcInstanceArn",
                    idc_managed_application_arn="idcManagedApplicationArn",
                    idc_region="idcRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c3d17311c70b31316d9e3457d61e651e50be01af9711468bfc9e3a1a2b28590b)
                check_type(argname="argument idc_instance_arn", value=idc_instance_arn, expected_type=type_hints["idc_instance_arn"])
                check_type(argname="argument idc_managed_application_arn", value=idc_managed_application_arn, expected_type=type_hints["idc_managed_application_arn"])
                check_type(argname="argument idc_region", value=idc_region, expected_type=type_hints["idc_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if idc_instance_arn is not None:
                self._values["idc_instance_arn"] = idc_instance_arn
            if idc_managed_application_arn is not None:
                self._values["idc_managed_application_arn"] = idc_managed_application_arn
            if idc_region is not None:
                self._values["idc_region"] = idc_region

        @builtins.property
        def idc_instance_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM Identity Center instance to use for authentication.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-awsidc.html#cfn-eks-capability-awsidc-idcinstancearn
            '''
            result = self._values.get("idc_instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def idc_managed_application_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the managed application created in IAM Identity Center for this Argo CD capability.

            This application is automatically created and managed by EKS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-awsidc.html#cfn-eks-capability-awsidc-idcmanagedapplicationarn
            '''
            result = self._values.get("idc_managed_application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def idc_region(self) -> typing.Optional[builtins.str]:
            '''The Region where your IAM Identity Center instance is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-awsidc.html#cfn-eks-capability-awsidc-idcregion
            '''
            result = self._values.get("idc_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AwsIdcProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"argo_cd": "argoCd"},
    )
    class CapabilityConfigurationProperty:
        def __init__(
            self,
            *,
            argo_cd: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCapabilityPropsMixin.ArgoCdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration settings for a capability.

            The structure of this object varies depending on the capability type.

            :param argo_cd: Configuration settings for an Argo CD capability. This includes the Kubernetes namespace, IAM Identity Center integration, RBAC role mappings, and network access configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-capabilityconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                capability_configuration_property = eks_mixins.CfnCapabilityPropsMixin.CapabilityConfigurationProperty(
                    argo_cd=eks_mixins.CfnCapabilityPropsMixin.ArgoCdProperty(
                        aws_idc=eks_mixins.CfnCapabilityPropsMixin.AwsIdcProperty(
                            idc_instance_arn="idcInstanceArn",
                            idc_managed_application_arn="idcManagedApplicationArn",
                            idc_region="idcRegion"
                        ),
                        namespace="namespace",
                        network_access=eks_mixins.CfnCapabilityPropsMixin.NetworkAccessProperty(
                            vpce_ids=["vpceIds"]
                        ),
                        rbac_role_mappings=[eks_mixins.CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty(
                            identities=[eks_mixins.CfnCapabilityPropsMixin.SsoIdentityProperty(
                                id="id",
                                type="type"
                            )],
                            role="role"
                        )],
                        server_url="serverUrl"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c67107c054132e3fed460785cb46c34120f2f60fc3f627f302ff33ff6819f8d4)
                check_type(argname="argument argo_cd", value=argo_cd, expected_type=type_hints["argo_cd"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if argo_cd is not None:
                self._values["argo_cd"] = argo_cd

        @builtins.property
        def argo_cd(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.ArgoCdProperty"]]:
            '''Configuration settings for an Argo CD capability.

            This includes the Kubernetes namespace, IAM Identity Center integration, RBAC role mappings, and network access configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-capabilityconfiguration.html#cfn-eks-capability-capabilityconfiguration-argocd
            '''
            result = self._values.get("argo_cd")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCapabilityPropsMixin.ArgoCdProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CapabilityConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin.NetworkAccessProperty",
        jsii_struct_bases=[],
        name_mapping={"vpce_ids": "vpceIds"},
    )
    class NetworkAccessProperty:
        def __init__(
            self,
            *,
            vpce_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration for network access to the Argo CD capability's managed API server endpoint.

            By default, the Argo CD server is accessible via a public endpoint. You can optionally specify one or more VPC endpoint IDs to enable private connectivity from your VPCs.

            :param vpce_ids: A list of VPC endpoint IDs to associate with the managed Argo CD API server endpoint. Each VPC endpoint provides private connectivity from a specific VPC to the Argo CD server. You can specify multiple VPC endpoint IDs to enable access from multiple VPCs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-networkaccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                network_access_property = eks_mixins.CfnCapabilityPropsMixin.NetworkAccessProperty(
                    vpce_ids=["vpceIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e857e219ccae5b0318790e68957cfe2e482a32892a6b9e4cb16fb76aed41122)
                check_type(argname="argument vpce_ids", value=vpce_ids, expected_type=type_hints["vpce_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpce_ids is not None:
                self._values["vpce_ids"] = vpce_ids

        @builtins.property
        def vpce_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of VPC endpoint IDs to associate with the managed Argo CD API server endpoint.

            Each VPC endpoint provides private connectivity from a specific VPC to the Argo CD server. You can specify multiple VPC endpoint IDs to enable access from multiple VPCs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-networkaccess.html#cfn-eks-capability-networkaccess-vpceids
            '''
            result = self._values.get("vpce_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnCapabilityPropsMixin.SsoIdentityProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "type": "type"},
    )
    class SsoIdentityProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An IAM Identity Center identity (user or group) that can be assigned permissions in a capability.

            :param id: The unique identifier of the IAM Identity Center user or group.
            :param type: The type of identity. Valid values are SSO_USER or SSO_GROUP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-ssoidentity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                sso_identity_property = eks_mixins.CfnCapabilityPropsMixin.SsoIdentityProperty(
                    id="id",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efc6fd1effc9db0da3c216e90c4b17d69a9e3c569869d4cf49c86a204fe1b0a0)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the IAM Identity Center user or group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-ssoidentity.html#cfn-eks-capability-ssoidentity-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of identity.

            Valid values are SSO_USER or SSO_GROUP.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-capability-ssoidentity.html#cfn-eks-capability-ssoidentity-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SsoIdentityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnClusterAutoModeBlockStorageLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterAutoModeBlockStorageLogs",
):
    '''Builder for CfnClusterLogsMixin to generate AUTO_MODE_BLOCK_STORAGE_LOGS for CfnCluster.

    :cloudformationResource: AWS::EKS::Cluster
    :logType: AUTO_MODE_BLOCK_STORAGE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_cluster_auto_mode_block_storage_logs = eks_mixins.CfnClusterAutoModeBlockStorageLogs()
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
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aecdb0debcd07a97068a632ba35400026d2754a7df3e68d4f5dbf7e5026bf749)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eec0074381fcadfacfde7bedc383fc9f44c33c1c62397dc0fe13a58f455c973)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b12ae579e035fede9e9de8239ea591e7bc334c56c39ab067d49debd6201328)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnClusterAutoModeComputeLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterAutoModeComputeLogs",
):
    '''Builder for CfnClusterLogsMixin to generate AUTO_MODE_COMPUTE_LOGS for CfnCluster.

    :cloudformationResource: AWS::EKS::Cluster
    :logType: AUTO_MODE_COMPUTE_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_cluster_auto_mode_compute_logs = eks_mixins.CfnClusterAutoModeComputeLogs()
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
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c9a24d16d5427cd3848a5af518bbfe333b1db6f812ff8443aa0d839079052c)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a288934057859cc20cf92adbfd789937358a18ea3ae4d73ed37310c176e55d)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2932241cd1a057c81bfc0a6c89beb78d5f9d1a99794d17dfb833e64113c843)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnClusterAutoModeIpamLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterAutoModeIpamLogs",
):
    '''Builder for CfnClusterLogsMixin to generate AUTO_MODE_IPAM_LOGS for CfnCluster.

    :cloudformationResource: AWS::EKS::Cluster
    :logType: AUTO_MODE_IPAM_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_cluster_auto_mode_ipam_logs = eks_mixins.CfnClusterAutoModeIpamLogs()
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
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e40f6ce14578d4d7e545d2bec39260439f2d6ecb8bf8ee7074a22534594eed9)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0582fdfef130b417ce8f731492aad637555f45cb40977a735a2c0a7279f1136)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff225116c19cb7efcfb1e90dae8557fa0ae2445d614dc75be2727537c5411ac)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toS3", [bucket]))


class CfnClusterAutoModeLoadBalancingLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterAutoModeLoadBalancingLogs",
):
    '''Builder for CfnClusterLogsMixin to generate AUTO_MODE_LOAD_BALANCING_LOGS for CfnCluster.

    :cloudformationResource: AWS::EKS::Cluster
    :logType: AUTO_MODE_LOAD_BALANCING_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_cluster_auto_mode_load_balancing_logs = eks_mixins.CfnClusterAutoModeLoadBalancingLogs()
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
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e52d3a745ee872d211b863a8daa91da493e51e2eaad811818bbfb2c30b4253b)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0dc46ca63c84c4d09de0a9c422860eab9a1040b651d2e4487e42962b083426e)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> "CfnClusterLogsMixin":
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__287d15fdf0dcfd50d1b16077d3ba322ecd4ecc450fa176ee06aee2f13bb2d811)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast("CfnClusterLogsMixin", jsii.invoke(self, "toS3", [bucket]))


@jsii.implements(_IMixin_11e4b965)
class CfnClusterLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterLogsMixin",
):
    '''Creates an Amazon EKS control plane.

    The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as ``etcd`` and the API server. The control plane runs in an account managed by AWS , and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

    The cluster control plane is provisioned across multiple Availability Zones and fronted by an ELB Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support ``kubectl exec`` , ``logs`` , and ``proxy`` data flows).

    Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

    You can use the ``endpointPublicAccess`` and ``endpointPrivateAccess`` parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ``ipFamily`` for the cluster. For more information, see `Amazon EKS Cluster Endpoint Access Control <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .

    You can use the ``logging`` parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see `Amazon EKS Cluster Control Plane Logs <https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html>`_ in the **Amazon EKS User Guide** .
    .. epigraph::

       CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see `CloudWatch Pricing <https://docs.aws.amazon.com/cloudwatch/pricing/>`_ .

    In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see `Allowing users to access your cluster <https://docs.aws.amazon.com/eks/latest/userguide/cluster-auth.html>`_ and `Launching Amazon EKS nodes <https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html>`_ in the *Amazon EKS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
    :cloudformationResource: AWS::EKS::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_cluster_logs_mixin = eks_mixins.CfnClusterLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::EKS::Cluster``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d54377ef74f8513cd0d834d49d8ffcbe02caa072dfb89bea1d46f40f056f74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d51028fbb5aacfbaf51b7c7834ba4699ede78ce14522f0639499cedaa98a6df)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dc79894f0f72f4ce665ae05d23fd826cf1ac150e1cf0dca53780d2bdbbe6f9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTO_MODE_BLOCK_STORAGE_LOGS")
    def AUTO_MODE_BLOCK_STORAGE_LOGS(cls) -> CfnClusterAutoModeBlockStorageLogs:
        return typing.cast(CfnClusterAutoModeBlockStorageLogs, jsii.sget(cls, "AUTO_MODE_BLOCK_STORAGE_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTO_MODE_COMPUTE_LOGS")
    def AUTO_MODE_COMPUTE_LOGS(cls) -> CfnClusterAutoModeComputeLogs:
        return typing.cast(CfnClusterAutoModeComputeLogs, jsii.sget(cls, "AUTO_MODE_COMPUTE_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTO_MODE_IPAM_LOGS")
    def AUTO_MODE_IPAM_LOGS(cls) -> CfnClusterAutoModeIpamLogs:
        return typing.cast(CfnClusterAutoModeIpamLogs, jsii.sget(cls, "AUTO_MODE_IPAM_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTO_MODE_LOAD_BALANCING_LOGS")
    def AUTO_MODE_LOAD_BALANCING_LOGS(cls) -> CfnClusterAutoModeLoadBalancingLogs:
        return typing.cast(CfnClusterAutoModeLoadBalancingLogs, jsii.sget(cls, "AUTO_MODE_LOAD_BALANCING_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_config": "accessConfig",
        "bootstrap_self_managed_addons": "bootstrapSelfManagedAddons",
        "compute_config": "computeConfig",
        "control_plane_scaling_config": "controlPlaneScalingConfig",
        "deletion_protection": "deletionProtection",
        "encryption_config": "encryptionConfig",
        "force": "force",
        "kubernetes_network_config": "kubernetesNetworkConfig",
        "logging": "logging",
        "name": "name",
        "outpost_config": "outpostConfig",
        "remote_network_config": "remoteNetworkConfig",
        "resources_vpc_config": "resourcesVpcConfig",
        "role_arn": "roleArn",
        "storage_config": "storageConfig",
        "tags": "tags",
        "upgrade_policy": "upgradePolicy",
        "version": "version",
        "zonal_shift_config": "zonalShiftConfig",
    },
)
class CfnClusterMixinProps:
    def __init__(
        self,
        *,
        access_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.AccessConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        bootstrap_self_managed_addons: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        compute_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ComputeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        control_plane_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ControlPlaneScalingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.EncryptionConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        force: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kubernetes_network_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.KubernetesNetworkConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.LoggingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        outpost_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.OutpostConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        remote_network_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.RemoteNetworkConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resources_vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ResourcesVpcConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        storage_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.StorageConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        upgrade_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.UpgradePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
        zonal_shift_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ZonalShiftConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnClusterPropsMixin.

        :param access_config: The access configuration for the cluster.
        :param bootstrap_self_managed_addons: If you set this value to ``False`` when creating a cluster, the default networking add-ons will not be installed. The default networking add-ons include ``vpc-cni`` , ``coredns`` , and ``kube-proxy`` . Use this option when you plan to install third-party alternative add-ons or self-manage the default networking add-ons.
        :param compute_config: Indicates the current configuration of the compute capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the *Amazon EKS User Guide* .
        :param control_plane_scaling_config: The control plane scaling tier configuration. For more information, see EKS Provisioned Control Plane in the Amazon EKS User Guide.
        :param deletion_protection: The current deletion protection setting for the cluster. When ``true`` , deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When ``false`` , the cluster can be deleted normally. This setting only applies to clusters in an active state.
        :param encryption_config: The encryption configuration for the cluster.
        :param force: Set this value to ``true`` to override upgrade-blocking readiness checks when updating a cluster. Default: - false
        :param kubernetes_network_config: The Kubernetes network configuration for the cluster.
        :param logging: The logging configuration for your cluster.
        :param name: The unique name to give to your cluster. The name can contain only alphanumeric characters (case-sensitive) and hyphens. It must start with an alphanumeric character and can't be longer than 100 characters. The name must be unique within the AWS Region and AWS account that you're creating the cluster in. Note that underscores can't be used in CloudFormation .
        :param outpost_config: An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost. This object isn't available for clusters on the AWS cloud.
        :param remote_network_config: The configuration in the cluster for EKS Hybrid Nodes. You can add, change, or remove this configuration after the cluster is created.
        :param resources_vpc_config: The VPC configuration that's used by the cluster control plane. Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see `Cluster VPC Considerations <https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html>`_ and `Cluster Security Group Considerations <https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html>`_ in the *Amazon EKS User Guide* . You must specify at least two subnets. You can specify up to five security groups, but we recommend that you use a dedicated security group for your cluster control plane.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. For more information, see `Amazon EKS Service IAM Role <https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html>`_ in the **Amazon EKS User Guide** .
        :param storage_config: Indicates the current configuration of the block storage capability on your EKS Auto Mode cluster. For example, if the capability is enabled or disabled. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account. For more information, see EKS Auto Mode block storage capability in the *Amazon EKS User Guide* .
        :param tags: The metadata that you apply to the cluster to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Cluster tags don't propagate to any other resources associated with the cluster. .. epigraph:: You must have the ``eks:TagResource`` and ``eks:UntagResource`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.
        :param upgrade_policy: This value indicates if extended support is enabled or disabled for the cluster. `Learn more about EKS Extended Support in the *Amazon EKS User Guide* . <https://docs.aws.amazon.com/eks/latest/userguide/extended-support-control.html>`_
        :param version: The desired Kubernetes version for your cluster. If you don't specify a value here, the default version available in Amazon EKS is used. .. epigraph:: The default version might not be the latest version available.
        :param zonal_shift_config: The configuration for zonal shift for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_cluster_mixin_props = eks_mixins.CfnClusterMixinProps(
                access_config=eks_mixins.CfnClusterPropsMixin.AccessConfigProperty(
                    authentication_mode="authenticationMode",
                    bootstrap_cluster_creator_admin_permissions=False
                ),
                bootstrap_self_managed_addons=False,
                compute_config=eks_mixins.CfnClusterPropsMixin.ComputeConfigProperty(
                    enabled=False,
                    node_pools=["nodePools"],
                    node_role_arn="nodeRoleArn"
                ),
                control_plane_scaling_config=eks_mixins.CfnClusterPropsMixin.ControlPlaneScalingConfigProperty(
                    tier="tier"
                ),
                deletion_protection=False,
                encryption_config=[eks_mixins.CfnClusterPropsMixin.EncryptionConfigProperty(
                    provider=eks_mixins.CfnClusterPropsMixin.ProviderProperty(
                        key_arn="keyArn"
                    ),
                    resources=["resources"]
                )],
                force=False,
                kubernetes_network_config=eks_mixins.CfnClusterPropsMixin.KubernetesNetworkConfigProperty(
                    elastic_load_balancing=eks_mixins.CfnClusterPropsMixin.ElasticLoadBalancingProperty(
                        enabled=False
                    ),
                    ip_family="ipFamily",
                    service_ipv4_cidr="serviceIpv4Cidr",
                    service_ipv6_cidr="serviceIpv6Cidr"
                ),
                logging=eks_mixins.CfnClusterPropsMixin.LoggingProperty(
                    cluster_logging=eks_mixins.CfnClusterPropsMixin.ClusterLoggingProperty(
                        enabled_types=[eks_mixins.CfnClusterPropsMixin.LoggingTypeConfigProperty(
                            type="type"
                        )]
                    )
                ),
                name="name",
                outpost_config=eks_mixins.CfnClusterPropsMixin.OutpostConfigProperty(
                    control_plane_instance_type="controlPlaneInstanceType",
                    control_plane_placement=eks_mixins.CfnClusterPropsMixin.ControlPlanePlacementProperty(
                        group_name="groupName"
                    ),
                    outpost_arns=["outpostArns"]
                ),
                remote_network_config=eks_mixins.CfnClusterPropsMixin.RemoteNetworkConfigProperty(
                    remote_node_networks=[eks_mixins.CfnClusterPropsMixin.RemoteNodeNetworkProperty(
                        cidrs=["cidrs"]
                    )],
                    remote_pod_networks=[eks_mixins.CfnClusterPropsMixin.RemotePodNetworkProperty(
                        cidrs=["cidrs"]
                    )]
                ),
                resources_vpc_config=eks_mixins.CfnClusterPropsMixin.ResourcesVpcConfigProperty(
                    endpoint_private_access=False,
                    endpoint_public_access=False,
                    public_access_cidrs=["publicAccessCidrs"],
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                ),
                role_arn="roleArn",
                storage_config=eks_mixins.CfnClusterPropsMixin.StorageConfigProperty(
                    block_storage=eks_mixins.CfnClusterPropsMixin.BlockStorageProperty(
                        enabled=False
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                upgrade_policy=eks_mixins.CfnClusterPropsMixin.UpgradePolicyProperty(
                    support_type="supportType"
                ),
                version="version",
                zonal_shift_config=eks_mixins.CfnClusterPropsMixin.ZonalShiftConfigProperty(
                    enabled=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c08513e242c1780e7ecbdd194d599fee79f6b17677a2d80d72e204e233b222)
            check_type(argname="argument access_config", value=access_config, expected_type=type_hints["access_config"])
            check_type(argname="argument bootstrap_self_managed_addons", value=bootstrap_self_managed_addons, expected_type=type_hints["bootstrap_self_managed_addons"])
            check_type(argname="argument compute_config", value=compute_config, expected_type=type_hints["compute_config"])
            check_type(argname="argument control_plane_scaling_config", value=control_plane_scaling_config, expected_type=type_hints["control_plane_scaling_config"])
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument kubernetes_network_config", value=kubernetes_network_config, expected_type=type_hints["kubernetes_network_config"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outpost_config", value=outpost_config, expected_type=type_hints["outpost_config"])
            check_type(argname="argument remote_network_config", value=remote_network_config, expected_type=type_hints["remote_network_config"])
            check_type(argname="argument resources_vpc_config", value=resources_vpc_config, expected_type=type_hints["resources_vpc_config"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument storage_config", value=storage_config, expected_type=type_hints["storage_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument upgrade_policy", value=upgrade_policy, expected_type=type_hints["upgrade_policy"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument zonal_shift_config", value=zonal_shift_config, expected_type=type_hints["zonal_shift_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_config is not None:
            self._values["access_config"] = access_config
        if bootstrap_self_managed_addons is not None:
            self._values["bootstrap_self_managed_addons"] = bootstrap_self_managed_addons
        if compute_config is not None:
            self._values["compute_config"] = compute_config
        if control_plane_scaling_config is not None:
            self._values["control_plane_scaling_config"] = control_plane_scaling_config
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if force is not None:
            self._values["force"] = force
        if kubernetes_network_config is not None:
            self._values["kubernetes_network_config"] = kubernetes_network_config
        if logging is not None:
            self._values["logging"] = logging
        if name is not None:
            self._values["name"] = name
        if outpost_config is not None:
            self._values["outpost_config"] = outpost_config
        if remote_network_config is not None:
            self._values["remote_network_config"] = remote_network_config
        if resources_vpc_config is not None:
            self._values["resources_vpc_config"] = resources_vpc_config
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if storage_config is not None:
            self._values["storage_config"] = storage_config
        if tags is not None:
            self._values["tags"] = tags
        if upgrade_policy is not None:
            self._values["upgrade_policy"] = upgrade_policy
        if version is not None:
            self._values["version"] = version
        if zonal_shift_config is not None:
            self._values["zonal_shift_config"] = zonal_shift_config

    @builtins.property
    def access_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AccessConfigProperty"]]:
        '''The access configuration for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-accessconfig
        '''
        result = self._values.get("access_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.AccessConfigProperty"]], result)

    @builtins.property
    def bootstrap_self_managed_addons(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''If you set this value to ``False`` when creating a cluster, the default networking add-ons will not be installed.

        The default networking add-ons include ``vpc-cni`` , ``coredns`` , and ``kube-proxy`` .

        Use this option when you plan to install third-party alternative add-ons or self-manage the default networking add-ons.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-bootstrapselfmanagedaddons
        '''
        result = self._values.get("bootstrap_self_managed_addons")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def compute_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ComputeConfigProperty"]]:
        '''Indicates the current configuration of the compute capability on your EKS Auto Mode cluster.

        For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-computeconfig
        '''
        result = self._values.get("compute_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ComputeConfigProperty"]], result)

    @builtins.property
    def control_plane_scaling_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ControlPlaneScalingConfigProperty"]]:
        '''The control plane scaling tier configuration.

        For more information, see EKS Provisioned Control Plane in the Amazon EKS User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-controlplanescalingconfig
        '''
        result = self._values.get("control_plane_scaling_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ControlPlaneScalingConfigProperty"]], result)

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The current deletion protection setting for the cluster.

        When ``true`` , deletion protection is enabled and the cluster cannot be deleted until protection is disabled. When ``false`` , the cluster can be deleted normally. This setting only applies to clusters in an active state.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionConfigProperty"]]]]:
        '''The encryption configuration for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.EncryptionConfigProperty"]]]], result)

    @builtins.property
    def force(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Set this value to ``true`` to override upgrade-blocking readiness checks when updating a cluster.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-force
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kubernetes_network_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.KubernetesNetworkConfigProperty"]]:
        '''The Kubernetes network configuration for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-kubernetesnetworkconfig
        '''
        result = self._values.get("kubernetes_network_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.KubernetesNetworkConfigProperty"]], result)

    @builtins.property
    def logging(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingProperty"]]:
        '''The logging configuration for your cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-logging
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name to give to your cluster.

        The name can contain only alphanumeric characters (case-sensitive) and hyphens. It must start with an alphanumeric character and can't be longer than 100 characters. The name must be unique within the AWS Region and AWS account that you're creating the cluster in. Note that underscores can't be used in CloudFormation .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outpost_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OutpostConfigProperty"]]:
        '''An object representing the configuration of your local Amazon EKS cluster on an AWS Outpost.

        This object isn't available for clusters on the AWS cloud.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-outpostconfig
        '''
        result = self._values.get("outpost_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.OutpostConfigProperty"]], result)

    @builtins.property
    def remote_network_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RemoteNetworkConfigProperty"]]:
        '''The configuration in the cluster for EKS Hybrid Nodes.

        You can add, change, or remove this configuration after the cluster is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-remotenetworkconfig
        '''
        result = self._values.get("remote_network_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RemoteNetworkConfigProperty"]], result)

    @builtins.property
    def resources_vpc_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ResourcesVpcConfigProperty"]]:
        '''The VPC configuration that's used by the cluster control plane.

        Amazon EKS VPC resources have specific requirements to work properly with Kubernetes. For more information, see `Cluster VPC Considerations <https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html>`_ and `Cluster Security Group Considerations <https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html>`_ in the *Amazon EKS User Guide* . You must specify at least two subnets. You can specify up to five security groups, but we recommend that you use a dedicated security group for your cluster control plane.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        '''
        result = self._values.get("resources_vpc_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ResourcesVpcConfigProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        For more information, see `Amazon EKS Service IAM Role <https://docs.aws.amazon.com/eks/latest/userguide/service_IAM_role.html>`_ in the **Amazon EKS User Guide** .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.StorageConfigProperty"]]:
        '''Indicates the current configuration of the block storage capability on your EKS Auto Mode cluster.

        For example, if the capability is enabled or disabled. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account. For more information, see EKS Auto Mode block storage capability in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-storageconfig
        '''
        result = self._values.get("storage_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.StorageConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The metadata that you apply to the cluster to assist with categorization and organization.

        Each tag consists of a key and an optional value, both of which you define. Cluster tags don't propagate to any other resources associated with the cluster.
        .. epigraph::

           You must have the ``eks:TagResource`` and ``eks:UntagResource`` permissions for your `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ to manage the CloudFormation stack. If you don't have these permissions, there might be unexpected behavior with stack-level tags propagating to the resource during resource creation and update.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def upgrade_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.UpgradePolicyProperty"]]:
        '''This value indicates if extended support is enabled or disabled for the cluster.

        `Learn more about EKS Extended Support in the *Amazon EKS User Guide* . <https://docs.aws.amazon.com/eks/latest/userguide/extended-support-control.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-upgradepolicy
        '''
        result = self._values.get("upgrade_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.UpgradePolicyProperty"]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The desired Kubernetes version for your cluster.

        If you don't specify a value here, the default version available in Amazon EKS is used.
        .. epigraph::

           The default version might not be the latest version available.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def zonal_shift_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ZonalShiftConfigProperty"]]:
        '''The configuration for zonal shift for the cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-zonalshiftconfig
        '''
        result = self._values.get("zonal_shift_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ZonalShiftConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnClusterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin",
):
    '''Creates an Amazon EKS control plane.

    The Amazon EKS control plane consists of control plane instances that run the Kubernetes software, such as ``etcd`` and the API server. The control plane runs in an account managed by AWS , and the Kubernetes API is exposed by the Amazon EKS API server endpoint. Each Amazon EKS cluster control plane is single tenant and unique. It runs on its own set of Amazon EC2 instances.

    The cluster control plane is provisioned across multiple Availability Zones and fronted by an ELB Network Load Balancer. Amazon EKS also provisions elastic network interfaces in your VPC subnets to provide connectivity from the control plane instances to the nodes (for example, to support ``kubectl exec`` , ``logs`` , and ``proxy`` data flows).

    Amazon EKS nodes run in your AWS account and connect to your cluster's control plane over the Kubernetes API server endpoint and a certificate file that is created for your cluster.

    You can use the ``endpointPublicAccess`` and ``endpointPrivateAccess`` parameters to enable or disable public and private access to your cluster's Kubernetes API server endpoint. By default, public access is enabled, and private access is disabled. The endpoint domain name and IP address family depends on the value of the ``ipFamily`` for the cluster. For more information, see `Amazon EKS Cluster Endpoint Access Control <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .

    You can use the ``logging`` parameter to enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs. By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see `Amazon EKS Cluster Control Plane Logs <https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html>`_ in the **Amazon EKS User Guide** .
    .. epigraph::

       CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see `CloudWatch Pricing <https://docs.aws.amazon.com/cloudwatch/pricing/>`_ .

    In most cases, it takes several minutes to create a cluster. After you create an Amazon EKS cluster, you must configure your Kubernetes tooling to communicate with the API server and launch nodes into your cluster. For more information, see `Allowing users to access your cluster <https://docs.aws.amazon.com/eks/latest/userguide/cluster-auth.html>`_ and `Launching Amazon EKS nodes <https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html>`_ in the *Amazon EKS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
    :cloudformationResource: AWS::EKS::Cluster
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_cluster_props_mixin = eks_mixins.CfnClusterPropsMixin(eks_mixins.CfnClusterMixinProps(
            access_config=eks_mixins.CfnClusterPropsMixin.AccessConfigProperty(
                authentication_mode="authenticationMode",
                bootstrap_cluster_creator_admin_permissions=False
            ),
            bootstrap_self_managed_addons=False,
            compute_config=eks_mixins.CfnClusterPropsMixin.ComputeConfigProperty(
                enabled=False,
                node_pools=["nodePools"],
                node_role_arn="nodeRoleArn"
            ),
            control_plane_scaling_config=eks_mixins.CfnClusterPropsMixin.ControlPlaneScalingConfigProperty(
                tier="tier"
            ),
            deletion_protection=False,
            encryption_config=[eks_mixins.CfnClusterPropsMixin.EncryptionConfigProperty(
                provider=eks_mixins.CfnClusterPropsMixin.ProviderProperty(
                    key_arn="keyArn"
                ),
                resources=["resources"]
            )],
            force=False,
            kubernetes_network_config=eks_mixins.CfnClusterPropsMixin.KubernetesNetworkConfigProperty(
                elastic_load_balancing=eks_mixins.CfnClusterPropsMixin.ElasticLoadBalancingProperty(
                    enabled=False
                ),
                ip_family="ipFamily",
                service_ipv4_cidr="serviceIpv4Cidr",
                service_ipv6_cidr="serviceIpv6Cidr"
            ),
            logging=eks_mixins.CfnClusterPropsMixin.LoggingProperty(
                cluster_logging=eks_mixins.CfnClusterPropsMixin.ClusterLoggingProperty(
                    enabled_types=[eks_mixins.CfnClusterPropsMixin.LoggingTypeConfigProperty(
                        type="type"
                    )]
                )
            ),
            name="name",
            outpost_config=eks_mixins.CfnClusterPropsMixin.OutpostConfigProperty(
                control_plane_instance_type="controlPlaneInstanceType",
                control_plane_placement=eks_mixins.CfnClusterPropsMixin.ControlPlanePlacementProperty(
                    group_name="groupName"
                ),
                outpost_arns=["outpostArns"]
            ),
            remote_network_config=eks_mixins.CfnClusterPropsMixin.RemoteNetworkConfigProperty(
                remote_node_networks=[eks_mixins.CfnClusterPropsMixin.RemoteNodeNetworkProperty(
                    cidrs=["cidrs"]
                )],
                remote_pod_networks=[eks_mixins.CfnClusterPropsMixin.RemotePodNetworkProperty(
                    cidrs=["cidrs"]
                )]
            ),
            resources_vpc_config=eks_mixins.CfnClusterPropsMixin.ResourcesVpcConfigProperty(
                endpoint_private_access=False,
                endpoint_public_access=False,
                public_access_cidrs=["publicAccessCidrs"],
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            ),
            role_arn="roleArn",
            storage_config=eks_mixins.CfnClusterPropsMixin.StorageConfigProperty(
                block_storage=eks_mixins.CfnClusterPropsMixin.BlockStorageProperty(
                    enabled=False
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            upgrade_policy=eks_mixins.CfnClusterPropsMixin.UpgradePolicyProperty(
                support_type="supportType"
            ),
            version="version",
            zonal_shift_config=eks_mixins.CfnClusterPropsMixin.ZonalShiftConfigProperty(
                enabled=False
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::Cluster``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b37fd968c8c81d6eab3abc583f2cc13f2d4cc77a30f570a1ee7a8354bde2039)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e29f4b7e3ba272edc9da7f534cc78f2904390fa15e47d1b513cea011f148eecc)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76738ce397597402ee937c79a408cc9c796c6eedef089e7aaf508418a464657)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnClusterMixinProps:
        return typing.cast(CfnClusterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.AccessConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "authentication_mode": "authenticationMode",
            "bootstrap_cluster_creator_admin_permissions": "bootstrapClusterCreatorAdminPermissions",
        },
    )
    class AccessConfigProperty:
        def __init__(
            self,
            *,
            authentication_mode: typing.Optional[builtins.str] = None,
            bootstrap_cluster_creator_admin_permissions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The access configuration for the cluster.

            :param authentication_mode: The desired authentication mode for the cluster. If you create a cluster by using the EKS API, AWS SDKs, or AWS CloudFormation , the default is ``CONFIG_MAP`` . If you create the cluster by using the AWS Management Console , the default value is ``API_AND_CONFIG_MAP`` .
            :param bootstrap_cluster_creator_admin_permissions: Specifies whether or not the cluster creator IAM principal was set as a cluster admin access entry during cluster creation time. The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-accessconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                access_config_property = eks_mixins.CfnClusterPropsMixin.AccessConfigProperty(
                    authentication_mode="authenticationMode",
                    bootstrap_cluster_creator_admin_permissions=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7abb00b84ce3203f8a120fb117cb95adbf035bdc2617143258d8cc3caaf885af)
                check_type(argname="argument authentication_mode", value=authentication_mode, expected_type=type_hints["authentication_mode"])
                check_type(argname="argument bootstrap_cluster_creator_admin_permissions", value=bootstrap_cluster_creator_admin_permissions, expected_type=type_hints["bootstrap_cluster_creator_admin_permissions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if authentication_mode is not None:
                self._values["authentication_mode"] = authentication_mode
            if bootstrap_cluster_creator_admin_permissions is not None:
                self._values["bootstrap_cluster_creator_admin_permissions"] = bootstrap_cluster_creator_admin_permissions

        @builtins.property
        def authentication_mode(self) -> typing.Optional[builtins.str]:
            '''The desired authentication mode for the cluster.

            If you create a cluster by using the EKS API, AWS SDKs, or AWS CloudFormation , the default is ``CONFIG_MAP`` . If you create the cluster by using the AWS Management Console , the default value is ``API_AND_CONFIG_MAP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-accessconfig.html#cfn-eks-cluster-accessconfig-authenticationmode
            '''
            result = self._values.get("authentication_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bootstrap_cluster_creator_admin_permissions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether or not the cluster creator IAM principal was set as a cluster admin access entry during cluster creation time.

            The default value is ``true`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-accessconfig.html#cfn-eks-cluster-accessconfig-bootstrapclustercreatoradminpermissions
            '''
            result = self._values.get("bootstrap_cluster_creator_admin_permissions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.BlockStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class BlockStorageProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Indicates the current configuration of the block storage capability on your EKS Auto Mode cluster.

            For example, if the capability is enabled or disabled. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account. For more information, see EKS Auto Mode block storage capability in the *Amazon EKS User Guide* .

            :param enabled: Indicates if the block storage capability is enabled on your EKS Auto Mode cluster. If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-blockstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                block_storage_property = eks_mixins.CfnClusterPropsMixin.BlockStorageProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f81d66301d0f7dfb9b17059e69aa3a836a29ca841aba02247f516aadd867223)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates if the block storage capability is enabled on your EKS Auto Mode cluster.

            If the block storage capability is enabled, EKS Auto Mode will create and delete EBS volumes in your AWS account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-blockstorage.html#cfn-eks-cluster-blockstorage-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BlockStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ClusterLoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled_types": "enabledTypes"},
    )
    class ClusterLoggingProperty:
        def __init__(
            self,
            *,
            enabled_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.LoggingTypeConfigProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The cluster control plane logging configuration for your cluster.

            .. epigraph::

               When updating a resource, you must include this ``ClusterLogging`` property if the previous CloudFormation template of the resource had it.

            :param enabled_types: The enabled control plane logs for your cluster. All log types are disabled if the array is empty. .. epigraph:: When updating a resource, you must include this ``EnabledTypes`` property if the previous CloudFormation template of the resource had it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-clusterlogging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                cluster_logging_property = eks_mixins.CfnClusterPropsMixin.ClusterLoggingProperty(
                    enabled_types=[eks_mixins.CfnClusterPropsMixin.LoggingTypeConfigProperty(
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97d51fb21d9b8ef39d179ee88e5a4127483fddaef6b1d07dfd652e175110c857)
                check_type(argname="argument enabled_types", value=enabled_types, expected_type=type_hints["enabled_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled_types is not None:
                self._values["enabled_types"] = enabled_types

        @builtins.property
        def enabled_types(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingTypeConfigProperty"]]]]:
            '''The enabled control plane logs for your cluster. All log types are disabled if the array is empty.

            .. epigraph::

               When updating a resource, you must include this ``EnabledTypes`` property if the previous CloudFormation template of the resource had it.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-clusterlogging.html#cfn-eks-cluster-clusterlogging-enabledtypes
            '''
            result = self._values.get("enabled_types")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.LoggingTypeConfigProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClusterLoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ComputeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "node_pools": "nodePools",
            "node_role_arn": "nodeRoleArn",
        },
    )
    class ComputeConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            node_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
            node_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Indicates the current configuration of the compute capability on your EKS Auto Mode cluster.

            For example, if the capability is enabled or disabled. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account. For more information, see EKS Auto Mode compute capability in the *Amazon EKS User Guide* .

            :param enabled: Request to enable or disable the compute capability on your EKS Auto Mode cluster. If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account.
            :param node_pools: Configuration for node pools that defines the compute resources for your EKS Auto Mode cluster. For more information, see EKS Auto Mode Node Pools in the *Amazon EKS User Guide* .
            :param node_role_arn: The ARN of the IAM Role EKS will assign to EC2 Managed Instances in your EKS Auto Mode cluster. This value cannot be changed after the compute capability of EKS Auto Mode is enabled. For more information, see the IAM Reference in the *Amazon EKS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-computeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                compute_config_property = eks_mixins.CfnClusterPropsMixin.ComputeConfigProperty(
                    enabled=False,
                    node_pools=["nodePools"],
                    node_role_arn="nodeRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__feb86e2e5ea2041c2e25ae62cb6f90c1322d826206dd4e6facde8381ddc2913d)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument node_pools", value=node_pools, expected_type=type_hints["node_pools"])
                check_type(argname="argument node_role_arn", value=node_role_arn, expected_type=type_hints["node_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if node_pools is not None:
                self._values["node_pools"] = node_pools
            if node_role_arn is not None:
                self._values["node_role_arn"] = node_role_arn

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Request to enable or disable the compute capability on your EKS Auto Mode cluster.

            If the compute capability is enabled, EKS Auto Mode will create and delete EC2 Managed Instances in your AWS account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-computeconfig.html#cfn-eks-cluster-computeconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def node_pools(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Configuration for node pools that defines the compute resources for your EKS Auto Mode cluster.

            For more information, see EKS Auto Mode Node Pools in the *Amazon EKS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-computeconfig.html#cfn-eks-cluster-computeconfig-nodepools
            '''
            result = self._values.get("node_pools")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def node_role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM Role EKS will assign to EC2 Managed Instances in your EKS Auto Mode cluster.

            This value cannot be changed after the compute capability of EKS Auto Mode is enabled. For more information, see the IAM Reference in the *Amazon EKS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-computeconfig.html#cfn-eks-cluster-computeconfig-noderolearn
            '''
            result = self._values.get("node_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ControlPlanePlacementProperty",
        jsii_struct_bases=[],
        name_mapping={"group_name": "groupName"},
    )
    class ControlPlanePlacementProperty:
        def __init__(self, *, group_name: typing.Optional[builtins.str] = None) -> None:
            '''The placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost.

            For more information, see `Capacity considerations <https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-capacity-considerations.html>`_ in the *Amazon EKS User Guide* .

            :param group_name: The name of the placement group for the Kubernetes control plane instances. This property is only used for a local cluster on an AWS Outpost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-controlplaneplacement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                control_plane_placement_property = eks_mixins.CfnClusterPropsMixin.ControlPlanePlacementProperty(
                    group_name="groupName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad1e2ee49a3b025004a061fb537c45bf5814cf3a952eeb89b5ef85dce6941c69)
                check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if group_name is not None:
                self._values["group_name"] = group_name

        @builtins.property
        def group_name(self) -> typing.Optional[builtins.str]:
            '''The name of the placement group for the Kubernetes control plane instances.

            This property is only used for a local cluster on an AWS Outpost.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-controlplaneplacement.html#cfn-eks-cluster-controlplaneplacement-groupname
            '''
            result = self._values.get("group_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ControlPlanePlacementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ControlPlaneScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"tier": "tier"},
    )
    class ControlPlaneScalingConfigProperty:
        def __init__(self, *, tier: typing.Optional[builtins.str] = None) -> None:
            '''The control plane scaling tier configuration.

            For more information, see EKS Provisioned Control Plane in the Amazon EKS User Guide.

            :param tier: The control plane scaling tier configuration. Available options are ``standard`` , ``tier-xl`` , ``tier-2xl`` , or ``tier-4xl`` . For more information, see EKS Provisioned Control Plane in the Amazon EKS User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-controlplanescalingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                control_plane_scaling_config_property = eks_mixins.CfnClusterPropsMixin.ControlPlaneScalingConfigProperty(
                    tier="tier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ea548bfe5e1d0b226f0a90c93137fedc65b590bd26a02dab110d29ddeabf3c37)
                check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tier is not None:
                self._values["tier"] = tier

        @builtins.property
        def tier(self) -> typing.Optional[builtins.str]:
            '''The control plane scaling tier configuration.

            Available options are ``standard`` , ``tier-xl`` , ``tier-2xl`` , or ``tier-4xl`` . For more information, see EKS Provisioned Control Plane in the Amazon EKS User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-controlplanescalingconfig.html#cfn-eks-cluster-controlplanescalingconfig-tier
            '''
            result = self._values.get("tier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ControlPlaneScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ElasticLoadBalancingProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ElasticLoadBalancingProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Indicates the current configuration of the load balancing capability on your EKS Auto Mode cluster.

            For example, if the capability is enabled or disabled. For more information, see EKS Auto Mode load balancing capability in the *Amazon EKS User Guide* .

            :param enabled: Indicates if the load balancing capability is enabled on your EKS Auto Mode cluster. If the load balancing capability is enabled, EKS Auto Mode will create and delete load balancers in your AWS account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-elasticloadbalancing.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                elastic_load_balancing_property = eks_mixins.CfnClusterPropsMixin.ElasticLoadBalancingProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__787515c03fb09a0cccc860d57909fd312861c9d80bef1dcc5fb81fd32a284ab2)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Indicates if the load balancing capability is enabled on your EKS Auto Mode cluster.

            If the load balancing capability is enabled, EKS Auto Mode will create and delete load balancers in your AWS account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-elasticloadbalancing.html#cfn-eks-cluster-elasticloadbalancing-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ElasticLoadBalancingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"provider": "provider", "resources": "resources"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ProviderProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The encryption configuration for the cluster.

            :param provider: The encryption provider for the cluster.
            :param resources: Specifies the resources to be encrypted. The only supported value is ``secrets`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                encryption_config_property = eks_mixins.CfnClusterPropsMixin.EncryptionConfigProperty(
                    provider=eks_mixins.CfnClusterPropsMixin.ProviderProperty(
                        key_arn="keyArn"
                    ),
                    resources=["resources"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10c1778da436313b56ddded82e658928b7e15f2f3f560c0ba5855067f5b0685f)
                check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provider is not None:
                self._values["provider"] = provider
            if resources is not None:
                self._values["resources"] = resources

        @builtins.property
        def provider(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ProviderProperty"]]:
            '''The encryption provider for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-provider
            '''
            result = self._values.get("provider")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ProviderProperty"]], result)

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specifies the resources to be encrypted.

            The only supported value is ``secrets`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.KubernetesNetworkConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "elastic_load_balancing": "elasticLoadBalancing",
            "ip_family": "ipFamily",
            "service_ipv4_cidr": "serviceIpv4Cidr",
            "service_ipv6_cidr": "serviceIpv6Cidr",
        },
    )
    class KubernetesNetworkConfigProperty:
        def __init__(
            self,
            *,
            elastic_load_balancing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ElasticLoadBalancingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_family: typing.Optional[builtins.str] = None,
            service_ipv4_cidr: typing.Optional[builtins.str] = None,
            service_ipv6_cidr: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Kubernetes network configuration for the cluster.

            :param elastic_load_balancing: Request to enable or disable the load balancing capability on your EKS Auto Mode cluster. For more information, see EKS Auto Mode load balancing capability in the *Amazon EKS User Guide* .
            :param ip_family: Specify which IP family is used to assign Kubernetes pod and service IP addresses. If you don't specify a value, ``ipv4`` is used by default. You can only specify an IP family when you create a cluster and can't change this value once the cluster is created. If you specify ``ipv6`` , the VPC and subnets that you specify for cluster creation must have both ``IPv4`` and ``IPv6`` CIDR blocks assigned to them. You can't specify ``ipv6`` for clusters in China Regions. You can only specify ``ipv6`` for ``1.21`` and later clusters that use version ``1.10.1`` or later of the Amazon VPC CNI add-on. If you specify ``ipv6`` , then ensure that your VPC meets the requirements listed in the considerations listed in `Assigning IPv6 addresses to pods and services <https://docs.aws.amazon.com/eks/latest/userguide/cni-ipv6.html>`_ in the *Amazon EKS User Guide* . Kubernetes assigns services ``IPv6`` addresses from the unique local address range ``(fc00::/7)`` . You can't specify a custom ``IPv6`` CIDR block. Pod addresses are assigned from the subnet's ``IPv6`` CIDR.
            :param service_ipv4_cidr: Don't specify a value if you select ``ipv6`` for *ipFamily* . The CIDR block to assign Kubernetes service IP addresses from. If you don't specify a block, Kubernetes assigns addresses from either the ``10.100.0.0/16`` or ``172.20.0.0/16`` CIDR blocks. We recommend that you specify a block that does not overlap with resources in other networks that are peered or connected to your VPC. The block must meet the following requirements: - Within one of the following private IP address blocks: ``10.0.0.0/8`` , ``172.16.0.0/12`` , or ``192.168.0.0/16`` . - Doesn't overlap with any CIDR block assigned to the VPC that you selected for VPC. - Between ``/24`` and ``/12`` . .. epigraph:: You can only specify a custom CIDR block when you create a cluster. You can't change this value after the cluster is created.
            :param service_ipv6_cidr: The CIDR block that Kubernetes pod and service IP addresses are assigned from if you created a 1.21 or later cluster with version 1.10.1 or later of the Amazon VPC CNI add-on and specified ``ipv6`` for *ipFamily* when you created the cluster. Kubernetes assigns service addresses from the unique local address range ( ``fc00::/7`` ) because you can't specify a custom IPv6 CIDR block when you create the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-kubernetesnetworkconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                kubernetes_network_config_property = eks_mixins.CfnClusterPropsMixin.KubernetesNetworkConfigProperty(
                    elastic_load_balancing=eks_mixins.CfnClusterPropsMixin.ElasticLoadBalancingProperty(
                        enabled=False
                    ),
                    ip_family="ipFamily",
                    service_ipv4_cidr="serviceIpv4Cidr",
                    service_ipv6_cidr="serviceIpv6Cidr"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__006ca85255d20e7e283d1b5d958978dd9d4b7902b1d260f8626f697e35806bb8)
                check_type(argname="argument elastic_load_balancing", value=elastic_load_balancing, expected_type=type_hints["elastic_load_balancing"])
                check_type(argname="argument ip_family", value=ip_family, expected_type=type_hints["ip_family"])
                check_type(argname="argument service_ipv4_cidr", value=service_ipv4_cidr, expected_type=type_hints["service_ipv4_cidr"])
                check_type(argname="argument service_ipv6_cidr", value=service_ipv6_cidr, expected_type=type_hints["service_ipv6_cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if elastic_load_balancing is not None:
                self._values["elastic_load_balancing"] = elastic_load_balancing
            if ip_family is not None:
                self._values["ip_family"] = ip_family
            if service_ipv4_cidr is not None:
                self._values["service_ipv4_cidr"] = service_ipv4_cidr
            if service_ipv6_cidr is not None:
                self._values["service_ipv6_cidr"] = service_ipv6_cidr

        @builtins.property
        def elastic_load_balancing(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ElasticLoadBalancingProperty"]]:
            '''Request to enable or disable the load balancing capability on your EKS Auto Mode cluster.

            For more information, see EKS Auto Mode load balancing capability in the *Amazon EKS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-kubernetesnetworkconfig.html#cfn-eks-cluster-kubernetesnetworkconfig-elasticloadbalancing
            '''
            result = self._values.get("elastic_load_balancing")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ElasticLoadBalancingProperty"]], result)

        @builtins.property
        def ip_family(self) -> typing.Optional[builtins.str]:
            '''Specify which IP family is used to assign Kubernetes pod and service IP addresses.

            If you don't specify a value, ``ipv4`` is used by default. You can only specify an IP family when you create a cluster and can't change this value once the cluster is created. If you specify ``ipv6`` , the VPC and subnets that you specify for cluster creation must have both ``IPv4`` and ``IPv6`` CIDR blocks assigned to them. You can't specify ``ipv6`` for clusters in China Regions.

            You can only specify ``ipv6`` for ``1.21`` and later clusters that use version ``1.10.1`` or later of the Amazon VPC CNI add-on. If you specify ``ipv6`` , then ensure that your VPC meets the requirements listed in the considerations listed in `Assigning IPv6 addresses to pods and services <https://docs.aws.amazon.com/eks/latest/userguide/cni-ipv6.html>`_ in the *Amazon EKS User Guide* . Kubernetes assigns services ``IPv6`` addresses from the unique local address range ``(fc00::/7)`` . You can't specify a custom ``IPv6`` CIDR block. Pod addresses are assigned from the subnet's ``IPv6`` CIDR.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-kubernetesnetworkconfig.html#cfn-eks-cluster-kubernetesnetworkconfig-ipfamily
            '''
            result = self._values.get("ip_family")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_ipv4_cidr(self) -> typing.Optional[builtins.str]:
            '''Don't specify a value if you select ``ipv6`` for *ipFamily* .

            The CIDR block to assign Kubernetes service IP addresses from. If you don't specify a block, Kubernetes assigns addresses from either the ``10.100.0.0/16`` or ``172.20.0.0/16`` CIDR blocks. We recommend that you specify a block that does not overlap with resources in other networks that are peered or connected to your VPC. The block must meet the following requirements:

            - Within one of the following private IP address blocks: ``10.0.0.0/8`` , ``172.16.0.0/12`` , or ``192.168.0.0/16`` .
            - Doesn't overlap with any CIDR block assigned to the VPC that you selected for VPC.
            - Between ``/24`` and ``/12`` .

            .. epigraph::

               You can only specify a custom CIDR block when you create a cluster. You can't change this value after the cluster is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-kubernetesnetworkconfig.html#cfn-eks-cluster-kubernetesnetworkconfig-serviceipv4cidr
            '''
            result = self._values.get("service_ipv4_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def service_ipv6_cidr(self) -> typing.Optional[builtins.str]:
            '''The CIDR block that Kubernetes pod and service IP addresses are assigned from if you created a 1.21 or later cluster with version 1.10.1 or later of the Amazon VPC CNI add-on and specified ``ipv6`` for *ipFamily* when you created the cluster. Kubernetes assigns service addresses from the unique local address range ( ``fc00::/7`` ) because you can't specify a custom IPv6 CIDR block when you create the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-kubernetesnetworkconfig.html#cfn-eks-cluster-kubernetesnetworkconfig-serviceipv6cidr
            '''
            result = self._values.get("service_ipv6_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KubernetesNetworkConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.LoggingProperty",
        jsii_struct_bases=[],
        name_mapping={"cluster_logging": "clusterLogging"},
    )
    class LoggingProperty:
        def __init__(
            self,
            *,
            cluster_logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ClusterLoggingProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Enable or disable exporting the Kubernetes control plane logs for your cluster to CloudWatch Logs.

            By default, cluster control plane logs aren't exported to CloudWatch Logs. For more information, see `Amazon EKS Cluster control plane logs <https://docs.aws.amazon.com/eks/latest/userguide/control-plane-logs.html>`_ in the **Amazon EKS User Guide** .
            .. epigraph::

               When updating a resource, you must include this ``Logging`` property if the previous CloudFormation template of the resource had it. > CloudWatch Logs ingestion, archive storage, and data scanning rates apply to exported control plane logs. For more information, see `CloudWatch Pricing <https://docs.aws.amazon.com/cloudwatch/pricing/>`_ .

            :param cluster_logging: The cluster control plane logging configuration for your cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-logging.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                logging_property = eks_mixins.CfnClusterPropsMixin.LoggingProperty(
                    cluster_logging=eks_mixins.CfnClusterPropsMixin.ClusterLoggingProperty(
                        enabled_types=[eks_mixins.CfnClusterPropsMixin.LoggingTypeConfigProperty(
                            type="type"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc1db75ec99d84675799be45d3b59aa2294cf650265a9392cbf18dc2182bda71)
                check_type(argname="argument cluster_logging", value=cluster_logging, expected_type=type_hints["cluster_logging"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cluster_logging is not None:
                self._values["cluster_logging"] = cluster_logging

        @builtins.property
        def cluster_logging(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ClusterLoggingProperty"]]:
            '''The cluster control plane logging configuration for your cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-logging.html#cfn-eks-cluster-logging-clusterlogging
            '''
            result = self._values.get("cluster_logging")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ClusterLoggingProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.LoggingTypeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type"},
    )
    class LoggingTypeConfigProperty:
        def __init__(self, *, type: typing.Optional[builtins.str] = None) -> None:
            '''The enabled logging type.

            For a list of the valid logging types, see the ```types`` property of ``LogSetup`` <https://docs.aws.amazon.com/eks/latest/APIReference/API_LogSetup.html#AmazonEKS-Type-LogSetup-types>`_ in the *Amazon EKS API Reference* .

            :param type: The name of the log type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-loggingtypeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                logging_type_config_property = eks_mixins.CfnClusterPropsMixin.LoggingTypeConfigProperty(
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18e0cba62f31c9c7109b9c6ac1e1f6c5783d897ef6758ce1a6a18d6d84baec88)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The name of the log type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-loggingtypeconfig.html#cfn-eks-cluster-loggingtypeconfig-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingTypeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.OutpostConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "control_plane_instance_type": "controlPlaneInstanceType",
            "control_plane_placement": "controlPlanePlacement",
            "outpost_arns": "outpostArns",
        },
    )
    class OutpostConfigProperty:
        def __init__(
            self,
            *,
            control_plane_instance_type: typing.Optional[builtins.str] = None,
            control_plane_placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.ControlPlanePlacementProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            outpost_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The configuration of your local Amazon EKS cluster on an AWS Outpost.

            Before creating a cluster on an Outpost, review `Creating a local cluster on an Outpost <https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-local-cluster-create.html>`_ in the *Amazon EKS User Guide* . This API isn't available for Amazon EKS clusters on the AWS cloud.

            :param control_plane_instance_type: The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts. Choose an instance type based on the number of nodes that your cluster will have. For more information, see `Capacity considerations <https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-capacity-considerations.html>`_ in the *Amazon EKS User Guide* . The instance type that you specify is used for all Kubernetes control plane instances. The instance type can't be changed after cluster creation. The control plane is not automatically scaled by Amazon EKS.
            :param control_plane_placement: An object representing the placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost. For more information, see `Capacity considerations <https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-capacity-considerations.html>`_ in the *Amazon EKS User Guide* .
            :param outpost_arns: The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts. Only a single Outpost ARN is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-outpostconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                outpost_config_property = eks_mixins.CfnClusterPropsMixin.OutpostConfigProperty(
                    control_plane_instance_type="controlPlaneInstanceType",
                    control_plane_placement=eks_mixins.CfnClusterPropsMixin.ControlPlanePlacementProperty(
                        group_name="groupName"
                    ),
                    outpost_arns=["outpostArns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2508ff07f331eafb9fe64eb2285d86d9f3f39befd121b3b00c893ef069acc7ba)
                check_type(argname="argument control_plane_instance_type", value=control_plane_instance_type, expected_type=type_hints["control_plane_instance_type"])
                check_type(argname="argument control_plane_placement", value=control_plane_placement, expected_type=type_hints["control_plane_placement"])
                check_type(argname="argument outpost_arns", value=outpost_arns, expected_type=type_hints["outpost_arns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if control_plane_instance_type is not None:
                self._values["control_plane_instance_type"] = control_plane_instance_type
            if control_plane_placement is not None:
                self._values["control_plane_placement"] = control_plane_placement
            if outpost_arns is not None:
                self._values["outpost_arns"] = outpost_arns

        @builtins.property
        def control_plane_instance_type(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 instance type that you want to use for your local Amazon EKS cluster on Outposts.

            Choose an instance type based on the number of nodes that your cluster will have. For more information, see `Capacity considerations <https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-capacity-considerations.html>`_ in the *Amazon EKS User Guide* .

            The instance type that you specify is used for all Kubernetes control plane instances. The instance type can't be changed after cluster creation. The control plane is not automatically scaled by Amazon EKS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-outpostconfig.html#cfn-eks-cluster-outpostconfig-controlplaneinstancetype
            '''
            result = self._values.get("control_plane_instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def control_plane_placement(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ControlPlanePlacementProperty"]]:
            '''An object representing the placement configuration for all the control plane instances of your local Amazon EKS cluster on an AWS Outpost.

            For more information, see `Capacity considerations <https://docs.aws.amazon.com/eks/latest/userguide/eks-outposts-capacity-considerations.html>`_ in the *Amazon EKS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-outpostconfig.html#cfn-eks-cluster-outpostconfig-controlplaneplacement
            '''
            result = self._values.get("control_plane_placement")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.ControlPlanePlacementProperty"]], result)

        @builtins.property
        def outpost_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ARN of the Outpost that you want to use for your local Amazon EKS cluster on Outposts.

            Only a single Outpost ARN is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-outpostconfig.html#cfn-eks-cluster-outpostconfig-outpostarns
            '''
            result = self._values.get("outpost_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutpostConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn"},
    )
    class ProviderProperty:
        def __init__(self, *, key_arn: typing.Optional[builtins.str] = None) -> None:
            '''Identifies the AWS Key Management Service ( AWS  ) key used to encrypt the secrets.

            :param key_arn: Amazon Resource Name (ARN) or alias of the KMS key. The KMS key must be symmetric and created in the same AWS Region as the cluster. If the KMS key was created in a different account, the `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ must have access to the KMS key. For more information, see `Allowing users in other accounts to use a KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                provider_property = eks_mixins.CfnClusterPropsMixin.ProviderProperty(
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9adcb48ec0b0f285ab8c15a1a41cab9f7172f201b5458d767757cc65caa98de)
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) or alias of the KMS key.

            The KMS key must be symmetric and created in the same AWS Region as the cluster. If the KMS key was created in a different account, the `IAM principal <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html>`_ must have access to the KMS key. For more information, see `Allowing users in other accounts to use a KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-modifying-external-accounts.html>`_ in the *AWS Key Management Service Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html#cfn-eks-cluster-provider-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.RemoteNetworkConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "remote_node_networks": "remoteNodeNetworks",
            "remote_pod_networks": "remotePodNetworks",
        },
    )
    class RemoteNetworkConfigProperty:
        def __init__(
            self,
            *,
            remote_node_networks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.RemoteNodeNetworkProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            remote_pod_networks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.RemotePodNetworkProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration in the cluster for EKS Hybrid Nodes.

            You can add, change, or remove this configuration after the cluster is created.

            :param remote_node_networks: The list of network CIDRs that can contain hybrid nodes. These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator. Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ). It must satisfy the following requirements: - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported. - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range. - Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway , AWS Site-to-Site VPN , or AWS Direct Connect . - Each host must allow outbound connection to the EKS cluster control plane on TCP ports ``443`` and ``10250`` . - Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations. - Each host must allow TCP and UDP network connectivity to and from other hosts that are running ``CoreDNS`` on UDP port ``53`` for service and pod DNS names.
            :param remote_pod_networks: The list of network CIDRs that can contain pods that run Kubernetes webhooks on hybrid nodes. These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations. Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ). It must satisfy the following requirements: - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported. - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotenetworkconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                remote_network_config_property = eks_mixins.CfnClusterPropsMixin.RemoteNetworkConfigProperty(
                    remote_node_networks=[eks_mixins.CfnClusterPropsMixin.RemoteNodeNetworkProperty(
                        cidrs=["cidrs"]
                    )],
                    remote_pod_networks=[eks_mixins.CfnClusterPropsMixin.RemotePodNetworkProperty(
                        cidrs=["cidrs"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e4d136219f8ecf9b184f86a7d9e2cedf0924d156be0ab7345bef5cc84535002c)
                check_type(argname="argument remote_node_networks", value=remote_node_networks, expected_type=type_hints["remote_node_networks"])
                check_type(argname="argument remote_pod_networks", value=remote_pod_networks, expected_type=type_hints["remote_pod_networks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if remote_node_networks is not None:
                self._values["remote_node_networks"] = remote_node_networks
            if remote_pod_networks is not None:
                self._values["remote_pod_networks"] = remote_pod_networks

        @builtins.property
        def remote_node_networks(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RemoteNodeNetworkProperty"]]]]:
            '''The list of network CIDRs that can contain hybrid nodes.

            These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator.

            Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ).

            It must satisfy the following requirements:

            - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.
            - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.
            - Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway , AWS Site-to-Site VPN , or AWS Direct Connect .
            - Each host must allow outbound connection to the EKS cluster control plane on TCP ports ``443`` and ``10250`` .
            - Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations.
            - Each host must allow TCP and UDP network connectivity to and from other hosts that are running ``CoreDNS`` on UDP port ``53`` for service and pod DNS names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotenetworkconfig.html#cfn-eks-cluster-remotenetworkconfig-remotenodenetworks
            '''
            result = self._values.get("remote_node_networks")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RemoteNodeNetworkProperty"]]]], result)

        @builtins.property
        def remote_pod_networks(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RemotePodNetworkProperty"]]]]:
            '''The list of network CIDRs that can contain pods that run Kubernetes webhooks on hybrid nodes.

            These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations.

            Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ).

            It must satisfy the following requirements:

            - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.
            - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotenetworkconfig.html#cfn-eks-cluster-remotenetworkconfig-remotepodnetworks
            '''
            result = self._values.get("remote_pod_networks")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.RemotePodNetworkProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemoteNetworkConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.RemoteNodeNetworkProperty",
        jsii_struct_bases=[],
        name_mapping={"cidrs": "cidrs"},
    )
    class RemoteNodeNetworkProperty:
        def __init__(
            self,
            *,
            cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A network CIDR that can contain hybrid nodes.

            These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator.

            Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ).

            It must satisfy the following requirements:

            - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.
            - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.
            - Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway , AWS Site-to-Site VPN , or AWS Direct Connect .
            - Each host must allow outbound connection to the EKS cluster control plane on TCP ports ``443`` and ``10250`` .
            - Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations.
            - Each host must allow TCP and UDP network connectivity to and from other hosts that are running ``CoreDNS`` on UDP port ``53`` for service and pod DNS names.

            :param cidrs: A network CIDR that can contain hybrid nodes. These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator. Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ). It must satisfy the following requirements: - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported. - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range. - Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway , AWS Site-to-Site VPN , or AWS Direct Connect . - Each host must allow outbound connection to the EKS cluster control plane on TCP ports ``443`` and ``10250`` . - Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations. - Each host must allow TCP and UDP network connectivity to and from other hosts that are running ``CoreDNS`` on UDP port ``53`` for service and pod DNS names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotenodenetwork.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                remote_node_network_property = eks_mixins.CfnClusterPropsMixin.RemoteNodeNetworkProperty(
                    cidrs=["cidrs"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e3d61b80182ab467ad7ea941dec542b3dabb0ea7db3699123bfbea5b042dcf1)
                check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidrs is not None:
                self._values["cidrs"] = cidrs

        @builtins.property
        def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A network CIDR that can contain hybrid nodes.

            These CIDR blocks define the expected IP address range of the hybrid nodes that join the cluster. These blocks are typically determined by your network administrator.

            Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ).

            It must satisfy the following requirements:

            - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.
            - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.
            - Each block must have a route to the VPC that uses the VPC CIDR blocks, not public IPs or Elastic IPs. There are many options including AWS Transit Gateway , AWS Site-to-Site VPN , or AWS Direct Connect .
            - Each host must allow outbound connection to the EKS cluster control plane on TCP ports ``443`` and ``10250`` .
            - Each host must allow inbound connection from the EKS cluster control plane on TCP port 10250 for logs, exec and port-forward operations.
            - Each host must allow TCP and UDP network connectivity to and from other hosts that are running ``CoreDNS`` on UDP port ``53`` for service and pod DNS names.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotenodenetwork.html#cfn-eks-cluster-remotenodenetwork-cidrs
            '''
            result = self._values.get("cidrs")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemoteNodeNetworkProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.RemotePodNetworkProperty",
        jsii_struct_bases=[],
        name_mapping={"cidrs": "cidrs"},
    )
    class RemotePodNetworkProperty:
        def __init__(
            self,
            *,
            cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A network CIDR that can contain pods that run Kubernetes webhooks on hybrid nodes.

            These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations.

            Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ).

            It must satisfy the following requirements:

            - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.
            - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

            :param cidrs: A network CIDR that can contain pods that run Kubernetes webhooks on hybrid nodes. These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations. Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ). It must satisfy the following requirements: - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported. - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotepodnetwork.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                remote_pod_network_property = eks_mixins.CfnClusterPropsMixin.RemotePodNetworkProperty(
                    cidrs=["cidrs"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc816bb9e439bd0298cff03e6952b6a9de99b103244c311c2cd1d92b9cacc146)
                check_type(argname="argument cidrs", value=cidrs, expected_type=type_hints["cidrs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cidrs is not None:
                self._values["cidrs"] = cidrs

        @builtins.property
        def cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A network CIDR that can contain pods that run Kubernetes webhooks on hybrid nodes.

            These CIDR blocks are determined by configuring your Container Network Interface (CNI) plugin. We recommend the Calico CNI or Cilium CNI. Note that the Amazon VPC CNI plugin for Kubernetes isn't available for on-premises and edge locations.

            Enter one or more IPv4 CIDR blocks in decimal dotted-quad notation (for example, ``10.2.0.0/16`` ).

            It must satisfy the following requirements:

            - Each block must be within an ``IPv4`` RFC-1918 network range. Minimum allowed size is /32, maximum allowed size is /8. Publicly-routable addresses aren't supported.
            - Each block cannot overlap with the range of the VPC CIDR blocks for your EKS resources, or the block of the Kubernetes service IP range.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-remotepodnetwork.html#cfn-eks-cluster-remotepodnetwork-cidrs
            '''
            result = self._values.get("cidrs")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemotePodNetworkProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ResourcesVpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint_private_access": "endpointPrivateAccess",
            "endpoint_public_access": "endpointPublicAccess",
            "public_access_cidrs": "publicAccessCidrs",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class ResourcesVpcConfigProperty:
        def __init__(
            self,
            *,
            endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object representing the VPC configuration to use for an Amazon EKS cluster.

            .. epigraph::

               When updating a resource, you must include these properties if the previous CloudFormation template of the resource had them:

               - ``EndpointPublicAccess``
               - ``EndpointPrivateAccess``
               - ``PublicAccessCidrs``

            :param endpoint_private_access: Set this value to ``true`` to enable private access for your cluster's Kubernetes API server endpoint. If you enable private access, Kubernetes API requests from within your cluster's VPC use the private VPC endpoint. The default value for this parameter is ``false`` , which disables private access for your Kubernetes API server. If you disable private access and you have nodes or AWS Fargate pods in the cluster, then ensure that ``publicAccessCidrs`` includes the necessary CIDR blocks for communication with the nodes or Fargate pods. For more information, see `Cluster API server endpoint <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .
            :param endpoint_public_access: Set this value to ``false`` to disable public access to your cluster's Kubernetes API server endpoint. If you disable public access, your cluster's Kubernetes API server can only receive requests from within the cluster VPC. The default value for this parameter is ``true`` , which enables public access for your Kubernetes API server. The endpoint domain name and IP address family depends on the value of the ``ipFamily`` for the cluster. For more information, see `Cluster API server endpoint <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .
            :param public_access_cidrs: The CIDR blocks that are allowed access to your cluster's public Kubernetes API server endpoint. Communication to the endpoint from addresses outside of the CIDR blocks that you specify is denied. The default value is ``0.0.0.0/0`` and additionally ``::/0`` for dual-stack ``IPv6`` clusters. If you've disabled private endpoint access, make sure that you specify the necessary CIDR blocks for every node and AWS Fargate ``Pod`` in the cluster. For more information, see `Cluster API server endpoint <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** . Note that the public endpoints are dual-stack for only ``IPv6`` clusters that are made after October 2024. You can't add ``IPv6`` CIDR blocks to ``IPv4`` clusters or ``IPv6`` clusters that were made before October 2024.
            :param security_group_ids: Specify one or more security groups for the cross-account elastic network interfaces that Amazon EKS creates to use that allow communication between your nodes and the Kubernetes control plane. If you don't specify any security groups, then familiarize yourself with the difference between Amazon EKS defaults for clusters deployed with Kubernetes. For more information, see `Amazon EKS security group considerations <https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html>`_ in the **Amazon EKS User Guide** .
            :param subnet_ids: Specify subnets for your Amazon EKS nodes. Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your nodes and the Kubernetes control plane.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                resources_vpc_config_property = eks_mixins.CfnClusterPropsMixin.ResourcesVpcConfigProperty(
                    endpoint_private_access=False,
                    endpoint_public_access=False,
                    public_access_cidrs=["publicAccessCidrs"],
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff54a8f2aa57b7979791f97f83b9b2e701f9a505fc200fbd84e51462b788a32c)
                check_type(argname="argument endpoint_private_access", value=endpoint_private_access, expected_type=type_hints["endpoint_private_access"])
                check_type(argname="argument endpoint_public_access", value=endpoint_public_access, expected_type=type_hints["endpoint_public_access"])
                check_type(argname="argument public_access_cidrs", value=public_access_cidrs, expected_type=type_hints["public_access_cidrs"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint_private_access is not None:
                self._values["endpoint_private_access"] = endpoint_private_access
            if endpoint_public_access is not None:
                self._values["endpoint_public_access"] = endpoint_public_access
            if public_access_cidrs is not None:
                self._values["public_access_cidrs"] = public_access_cidrs
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def endpoint_private_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this value to ``true`` to enable private access for your cluster's Kubernetes API server endpoint.

            If you enable private access, Kubernetes API requests from within your cluster's VPC use the private VPC endpoint. The default value for this parameter is ``false`` , which disables private access for your Kubernetes API server. If you disable private access and you have nodes or AWS Fargate pods in the cluster, then ensure that ``publicAccessCidrs`` includes the necessary CIDR blocks for communication with the nodes or Fargate pods. For more information, see `Cluster API server endpoint <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-endpointprivateaccess
            '''
            result = self._values.get("endpoint_private_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def endpoint_public_access(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Set this value to ``false`` to disable public access to your cluster's Kubernetes API server endpoint.

            If you disable public access, your cluster's Kubernetes API server can only receive requests from within the cluster VPC. The default value for this parameter is ``true`` , which enables public access for your Kubernetes API server. The endpoint domain name and IP address family depends on the value of the ``ipFamily`` for the cluster. For more information, see `Cluster API server endpoint <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-endpointpublicaccess
            '''
            result = self._values.get("endpoint_public_access")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def public_access_cidrs(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The CIDR blocks that are allowed access to your cluster's public Kubernetes API server endpoint.

            Communication to the endpoint from addresses outside of the CIDR blocks that you specify is denied. The default value is ``0.0.0.0/0`` and additionally ``::/0`` for dual-stack ``IPv6`` clusters. If you've disabled private endpoint access, make sure that you specify the necessary CIDR blocks for every node and AWS Fargate ``Pod`` in the cluster. For more information, see `Cluster API server endpoint <https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html>`_ in the **Amazon EKS User Guide** .

            Note that the public endpoints are dual-stack for only ``IPv6`` clusters that are made after October 2024. You can't add ``IPv6`` CIDR blocks to ``IPv4`` clusters or ``IPv6`` clusters that were made before October 2024.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-publicaccesscidrs
            '''
            result = self._values.get("public_access_cidrs")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify one or more security groups for the cross-account elastic network interfaces that Amazon EKS creates to use that allow communication between your nodes and the Kubernetes control plane.

            If you don't specify any security groups, then familiarize yourself with the difference between Amazon EKS defaults for clusters deployed with Kubernetes. For more information, see `Amazon EKS security group considerations <https://docs.aws.amazon.com/eks/latest/userguide/sec-group-reqs.html>`_ in the **Amazon EKS User Guide** .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Specify subnets for your Amazon EKS nodes.

            Amazon EKS creates cross-account elastic network interfaces in these subnets to allow communication between your nodes and the Kubernetes control plane.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcesVpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.StorageConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"block_storage": "blockStorage"},
    )
    class StorageConfigProperty:
        def __init__(
            self,
            *,
            block_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnClusterPropsMixin.BlockStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Request to update the configuration of the storage capability of your EKS Auto Mode cluster.

            For example, enable the capability. For more information, see EKS Auto Mode block storage capability in the *Amazon EKS User Guide* .

            :param block_storage: Request to configure EBS Block Storage settings for your EKS Auto Mode cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-storageconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                storage_config_property = eks_mixins.CfnClusterPropsMixin.StorageConfigProperty(
                    block_storage=eks_mixins.CfnClusterPropsMixin.BlockStorageProperty(
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2672805e847c16309ec5d16e0d482794ecee22e86cbba45b2e06b9b08902fcd3)
                check_type(argname="argument block_storage", value=block_storage, expected_type=type_hints["block_storage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if block_storage is not None:
                self._values["block_storage"] = block_storage

        @builtins.property
        def block_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BlockStorageProperty"]]:
            '''Request to configure EBS Block Storage settings for your EKS Auto Mode cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-storageconfig.html#cfn-eks-cluster-storageconfig-blockstorage
            '''
            result = self._values.get("block_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnClusterPropsMixin.BlockStorageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.UpgradePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"support_type": "supportType"},
    )
    class UpgradePolicyProperty:
        def __init__(
            self,
            *,
            support_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The support policy to use for the cluster.

            Extended support allows you to remain on specific Kubernetes versions for longer. Clusters in extended support have higher costs. The default value is ``EXTENDED`` . Use ``STANDARD`` to disable extended support.

            `Learn more about EKS Extended Support in the *Amazon EKS User Guide* . <https://docs.aws.amazon.com/eks/latest/userguide/extended-support-control.html>`_

            :param support_type: If the cluster is set to ``EXTENDED`` , it will enter extended support at the end of standard support. If the cluster is set to ``STANDARD`` , it will be automatically upgraded at the end of standard support. `Learn more about EKS Extended Support in the *Amazon EKS User Guide* . <https://docs.aws.amazon.com/eks/latest/userguide/extended-support-control.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-upgradepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                upgrade_policy_property = eks_mixins.CfnClusterPropsMixin.UpgradePolicyProperty(
                    support_type="supportType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c7bc1112e38b98cb6957135de8248c808db40f04a551ed17e13f5b0c1f9ee91c)
                check_type(argname="argument support_type", value=support_type, expected_type=type_hints["support_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if support_type is not None:
                self._values["support_type"] = support_type

        @builtins.property
        def support_type(self) -> typing.Optional[builtins.str]:
            '''If the cluster is set to ``EXTENDED`` , it will enter extended support at the end of standard support.

            If the cluster is set to ``STANDARD`` , it will be automatically upgraded at the end of standard support.

            `Learn more about EKS Extended Support in the *Amazon EKS User Guide* . <https://docs.aws.amazon.com/eks/latest/userguide/extended-support-control.html>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-upgradepolicy.html#cfn-eks-cluster-upgradepolicy-supporttype
            '''
            result = self._values.get("support_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpgradePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnClusterPropsMixin.ZonalShiftConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class ZonalShiftConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The configuration for zonal shift for the cluster.

            :param enabled: If zonal shift is enabled, AWS configures zonal autoshift for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-zonalshiftconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                zonal_shift_config_property = eks_mixins.CfnClusterPropsMixin.ZonalShiftConfigProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a3ec0199823bd491402bb518d9a047262a685cd120ad4990e161969ba471adfc)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''If zonal shift is enabled, AWS configures zonal autoshift for the cluster.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-zonalshiftconfig.html#cfn-eks-cluster-zonalshiftconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ZonalShiftConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnFargateProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "fargate_profile_name": "fargateProfileName",
        "pod_execution_role_arn": "podExecutionRoleArn",
        "selectors": "selectors",
        "subnets": "subnets",
        "tags": "tags",
    },
)
class CfnFargateProfileMixinProps:
    def __init__(
        self,
        *,
        cluster_name: typing.Optional[builtins.str] = None,
        fargate_profile_name: typing.Optional[builtins.str] = None,
        pod_execution_role_arn: typing.Optional[builtins.str] = None,
        selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFargateProfilePropsMixin.SelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFargateProfilePropsMixin.

        :param cluster_name: The name of your cluster.
        :param fargate_profile_name: The name of the Fargate profile.
        :param pod_execution_role_arn: The Amazon Resource Name (ARN) of the ``Pod`` execution role to use for a ``Pod`` that matches the selectors in the Fargate profile. The ``Pod`` execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. For more information, see ```Pod`` execution role <https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html>`_ in the *Amazon EKS User Guide* .
        :param selectors: The selectors to match for a ``Pod`` to use this Fargate profile. Each selector must have an associated Kubernetes ``namespace`` . Optionally, you can also specify ``labels`` for a ``namespace`` . You may specify up to five selectors in a Fargate profile.
        :param subnets: The IDs of subnets to launch a ``Pod`` into. A ``Pod`` running on Fargate isn't assigned a public IP address, so only private subnets (with no direct route to an Internet Gateway) are accepted for this parameter.
        :param tags: Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_fargate_profile_mixin_props = eks_mixins.CfnFargateProfileMixinProps(
                cluster_name="clusterName",
                fargate_profile_name="fargateProfileName",
                pod_execution_role_arn="podExecutionRoleArn",
                selectors=[eks_mixins.CfnFargateProfilePropsMixin.SelectorProperty(
                    labels=[eks_mixins.CfnFargateProfilePropsMixin.LabelProperty(
                        key="key",
                        value="value"
                    )],
                    namespace="namespace"
                )],
                subnets=["subnets"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69481e0b841a3d9c17b27989469dc34033e57273a809f69ab44fc1eefa4b4348)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument fargate_profile_name", value=fargate_profile_name, expected_type=type_hints["fargate_profile_name"])
            check_type(argname="argument pod_execution_role_arn", value=pod_execution_role_arn, expected_type=type_hints["pod_execution_role_arn"])
            check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if fargate_profile_name is not None:
            self._values["fargate_profile_name"] = fargate_profile_name
        if pod_execution_role_arn is not None:
            self._values["pod_execution_role_arn"] = pod_execution_role_arn
        if selectors is not None:
            self._values["selectors"] = selectors
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of your cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html#cfn-eks-fargateprofile-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def fargate_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Fargate profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html#cfn-eks-fargateprofile-fargateprofilename
        '''
        result = self._values.get("fargate_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pod_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the ``Pod`` execution role to use for a ``Pod`` that matches the selectors in the Fargate profile.

        The ``Pod`` execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. For more information, see ```Pod`` execution role <https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html#cfn-eks-fargateprofile-podexecutionrolearn
        '''
        result = self._values.get("pod_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selectors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFargateProfilePropsMixin.SelectorProperty"]]]]:
        '''The selectors to match for a ``Pod`` to use this Fargate profile.

        Each selector must have an associated Kubernetes ``namespace`` . Optionally, you can also specify ``labels`` for a ``namespace`` . You may specify up to five selectors in a Fargate profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html#cfn-eks-fargateprofile-selectors
        '''
        result = self._values.get("selectors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFargateProfilePropsMixin.SelectorProperty"]]]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of subnets to launch a ``Pod`` into.

        A ``Pod`` running on Fargate isn't assigned a public IP address, so only private subnets (with no direct route to an Internet Gateway) are accepted for this parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html#cfn-eks-fargateprofile-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that assists with categorization and organization.

        Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html#cfn-eks-fargateprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFargateProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFargateProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnFargateProfilePropsMixin",
):
    '''Creates an AWS Fargate profile for your Amazon EKS cluster.

    You must have at least one Fargate profile in a cluster to be able to run pods on Fargate.

    The Fargate profile allows an administrator to declare which pods run on Fargate and specify which pods run on which Fargate profile. This declaration is done through the profile's selectors. Each profile can have up to five selectors that contain a namespace and labels. A namespace is required for every selector. The label field consists of multiple optional key-value pairs. Pods that match the selectors are scheduled on Fargate. If a to-be-scheduled pod matches any of the selectors in the Fargate profile, then that pod is run on Fargate.

    When you create a Fargate profile, you must specify a pod execution role to use with the pods that are scheduled with the profile. This role is added to the cluster's Kubernetes `Role Based Access Control <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/access-authn-authz/rbac/>`_ (RBAC) for authorization so that the ``kubelet`` that is running on the Fargate infrastructure can register with your Amazon EKS cluster so that it can appear in your cluster as a node. The pod execution role also provides IAM permissions to the Fargate infrastructure to allow read access to Amazon ECR image repositories. For more information, see `Pod Execution Role <https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html>`_ in the *Amazon EKS User Guide* .

    Fargate profiles are immutable. However, you can create a new updated profile to replace an existing profile and then delete the original after the updated profile has finished creating.

    If any Fargate profiles in a cluster are in the ``DELETING`` status, you must wait for that Fargate profile to finish deleting before you can create any other profiles in that cluster.

    For more information, see `AWS Fargate profile <https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html>`_ in the *Amazon EKS User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-fargateprofile.html
    :cloudformationResource: AWS::EKS::FargateProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_fargate_profile_props_mixin = eks_mixins.CfnFargateProfilePropsMixin(eks_mixins.CfnFargateProfileMixinProps(
            cluster_name="clusterName",
            fargate_profile_name="fargateProfileName",
            pod_execution_role_arn="podExecutionRoleArn",
            selectors=[eks_mixins.CfnFargateProfilePropsMixin.SelectorProperty(
                labels=[eks_mixins.CfnFargateProfilePropsMixin.LabelProperty(
                    key="key",
                    value="value"
                )],
                namespace="namespace"
            )],
            subnets=["subnets"],
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
        props: typing.Union[CfnFargateProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::FargateProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90a889cc8d94b56a4a9f0f9221227024ec07e5682428bf5807c94d06f7f7bfad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a17af886f6e21c9b6d9587e1349af00ddbe1c366e9672652a4eaa16bef2719d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203e371936b1258c35ef14837b516e03c504270b1da3c192ec7fe9f5e42675dd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFargateProfileMixinProps:
        return typing.cast(CfnFargateProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnFargateProfilePropsMixin.LabelProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class LabelProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair.

            :param key: Enter a key.
            :param value: Enter a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-fargateprofile-label.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                label_property = eks_mixins.CfnFargateProfilePropsMixin.LabelProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f7a1717305e0734af3f97f4f620db242aed66a4fbe7185ba434f7ddf79a042e)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''Enter a key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-fargateprofile-label.html#cfn-eks-fargateprofile-label-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Enter a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-fargateprofile-label.html#cfn-eks-fargateprofile-label-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LabelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnFargateProfilePropsMixin.SelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"labels": "labels", "namespace": "namespace"},
    )
    class SelectorProperty:
        def __init__(
            self,
            *,
            labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFargateProfilePropsMixin.LabelProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            namespace: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing an AWS Fargate profile selector.

            :param labels: The Kubernetes labels that the selector should match. A pod must contain all of the labels that are specified in the selector for it to be considered a match.
            :param namespace: The Kubernetes ``namespace`` that the selector should match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-fargateprofile-selector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                selector_property = eks_mixins.CfnFargateProfilePropsMixin.SelectorProperty(
                    labels=[eks_mixins.CfnFargateProfilePropsMixin.LabelProperty(
                        key="key",
                        value="value"
                    )],
                    namespace="namespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9dc9dfe7583f0ae8fda51695f520444f8dd30c07ef6699cbea8f7e5ab78864c8)
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if labels is not None:
                self._values["labels"] = labels
            if namespace is not None:
                self._values["namespace"] = namespace

        @builtins.property
        def labels(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFargateProfilePropsMixin.LabelProperty"]]]]:
            '''The Kubernetes labels that the selector should match.

            A pod must contain all of the labels that are specified in the selector for it to be considered a match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-fargateprofile-selector.html#cfn-eks-fargateprofile-selector-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFargateProfilePropsMixin.LabelProperty"]]]], result)

        @builtins.property
        def namespace(self) -> typing.Optional[builtins.str]:
            '''The Kubernetes ``namespace`` that the selector should match.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-fargateprofile-selector.html#cfn-eks-fargateprofile-selector-namespace
            '''
            result = self._values.get("namespace")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnIdentityProviderConfigMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "identity_provider_config_name": "identityProviderConfigName",
        "oidc": "oidc",
        "tags": "tags",
        "type": "type",
    },
)
class CfnIdentityProviderConfigMixinProps:
    def __init__(
        self,
        *,
        cluster_name: typing.Optional[builtins.str] = None,
        identity_provider_config_name: typing.Optional[builtins.str] = None,
        oidc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnIdentityProviderConfigPropsMixin.

        :param cluster_name: The name of your cluster.
        :param identity_provider_config_name: The name of the configuration.
        :param oidc: An object representing an OpenID Connect (OIDC) identity provider configuration.
        :param tags: Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.
        :param type: The type of the identity provider configuration. The only type available is ``oidc`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_identity_provider_config_mixin_props = eks_mixins.CfnIdentityProviderConfigMixinProps(
                cluster_name="clusterName",
                identity_provider_config_name="identityProviderConfigName",
                oidc=eks_mixins.CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty(
                    client_id="clientId",
                    groups_claim="groupsClaim",
                    groups_prefix="groupsPrefix",
                    issuer_url="issuerUrl",
                    required_claims=[eks_mixins.CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty(
                        key="key",
                        value="value"
                    )],
                    username_claim="usernameClaim",
                    username_prefix="usernamePrefix"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a6402788bc38ad1d5a84e9c63aff7b138a92de2030f890d4ab223aa66855d31)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument identity_provider_config_name", value=identity_provider_config_name, expected_type=type_hints["identity_provider_config_name"])
            check_type(argname="argument oidc", value=oidc, expected_type=type_hints["oidc"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if identity_provider_config_name is not None:
            self._values["identity_provider_config_name"] = identity_provider_config_name
        if oidc is not None:
            self._values["oidc"] = oidc
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of your cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html#cfn-eks-identityproviderconfig-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_config_name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html#cfn-eks-identityproviderconfig-identityproviderconfigname
        '''
        result = self._values.get("identity_provider_config_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oidc(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty"]]:
        '''An object representing an OpenID Connect (OIDC) identity provider configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html#cfn-eks-identityproviderconfig-oidc
        '''
        result = self._values.get("oidc")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that assists with categorization and organization.

        Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html#cfn-eks-identityproviderconfig-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of the identity provider configuration.

        The only type available is ``oidc`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html#cfn-eks-identityproviderconfig-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIdentityProviderConfigMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnIdentityProviderConfigPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnIdentityProviderConfigPropsMixin",
):
    '''Associates an identity provider configuration to a cluster.

    If you want to authenticate identities using an identity provider, you can create an identity provider configuration and associate it to your cluster. After configuring authentication to your cluster you can create Kubernetes ``Role`` and ``ClusterRole`` objects, assign permissions to them, and then bind them to the identities using Kubernetes ``RoleBinding`` and ``ClusterRoleBinding`` objects. For more information see `Using RBAC Authorization <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/access-authn-authz/rbac/>`_ in the Kubernetes documentation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-identityproviderconfig.html
    :cloudformationResource: AWS::EKS::IdentityProviderConfig
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_identity_provider_config_props_mixin = eks_mixins.CfnIdentityProviderConfigPropsMixin(eks_mixins.CfnIdentityProviderConfigMixinProps(
            cluster_name="clusterName",
            identity_provider_config_name="identityProviderConfigName",
            oidc=eks_mixins.CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty(
                client_id="clientId",
                groups_claim="groupsClaim",
                groups_prefix="groupsPrefix",
                issuer_url="issuerUrl",
                required_claims=[eks_mixins.CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty(
                    key="key",
                    value="value"
                )],
                username_claim="usernameClaim",
                username_prefix="usernamePrefix"
            ),
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
        props: typing.Union[CfnIdentityProviderConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::IdentityProviderConfig``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d53085b7b9d247eefafca01eb37636813543ac25ada04595ec6258d326504aa5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5944ef352bbf891a3af900b5824e7ef4a962bb7ebe249ae16445d463d5deb4f1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f17805bf32093c5d618b2185f7f1df66931c8fae6b8cbb8b088a391259a66e6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnIdentityProviderConfigMixinProps:
        return typing.cast(CfnIdentityProviderConfigMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "client_id": "clientId",
            "groups_claim": "groupsClaim",
            "groups_prefix": "groupsPrefix",
            "issuer_url": "issuerUrl",
            "required_claims": "requiredClaims",
            "username_claim": "usernameClaim",
            "username_prefix": "usernamePrefix",
        },
    )
    class OidcIdentityProviderConfigProperty:
        def __init__(
            self,
            *,
            client_id: typing.Optional[builtins.str] = None,
            groups_claim: typing.Optional[builtins.str] = None,
            groups_prefix: typing.Optional[builtins.str] = None,
            issuer_url: typing.Optional[builtins.str] = None,
            required_claims: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            username_claim: typing.Optional[builtins.str] = None,
            username_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing the configuration for an OpenID Connect (OIDC) identity provider.

            :param client_id: This is also known as *audience* . The ID of the client application that makes authentication requests to the OIDC identity provider.
            :param groups_claim: The JSON web token (JWT) claim that the provider uses to return your groups.
            :param groups_prefix: The prefix that is prepended to group claims to prevent clashes with existing names (such as ``system:`` groups). For example, the value ``oidc:`` creates group names like ``oidc:engineering`` and ``oidc:infra`` . The prefix can't contain ``system:``
            :param issuer_url: The URL of the OIDC identity provider that allows the API server to discover public signing keys for verifying tokens.
            :param required_claims: The key-value pairs that describe required claims in the identity token. If set, each claim is verified to be present in the token with a matching value.
            :param username_claim: The JSON Web token (JWT) claim that is used as the username.
            :param username_prefix: The prefix that is prepended to username claims to prevent clashes with existing names. The prefix can't contain ``system:``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                oidc_identity_provider_config_property = eks_mixins.CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty(
                    client_id="clientId",
                    groups_claim="groupsClaim",
                    groups_prefix="groupsPrefix",
                    issuer_url="issuerUrl",
                    required_claims=[eks_mixins.CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty(
                        key="key",
                        value="value"
                    )],
                    username_claim="usernameClaim",
                    username_prefix="usernamePrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d102f688d559941f7c3e0651b380e8bb3cedbc43a7f0ad690f9da3cabdb622bc)
                check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
                check_type(argname="argument groups_claim", value=groups_claim, expected_type=type_hints["groups_claim"])
                check_type(argname="argument groups_prefix", value=groups_prefix, expected_type=type_hints["groups_prefix"])
                check_type(argname="argument issuer_url", value=issuer_url, expected_type=type_hints["issuer_url"])
                check_type(argname="argument required_claims", value=required_claims, expected_type=type_hints["required_claims"])
                check_type(argname="argument username_claim", value=username_claim, expected_type=type_hints["username_claim"])
                check_type(argname="argument username_prefix", value=username_prefix, expected_type=type_hints["username_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_id is not None:
                self._values["client_id"] = client_id
            if groups_claim is not None:
                self._values["groups_claim"] = groups_claim
            if groups_prefix is not None:
                self._values["groups_prefix"] = groups_prefix
            if issuer_url is not None:
                self._values["issuer_url"] = issuer_url
            if required_claims is not None:
                self._values["required_claims"] = required_claims
            if username_claim is not None:
                self._values["username_claim"] = username_claim
            if username_prefix is not None:
                self._values["username_prefix"] = username_prefix

        @builtins.property
        def client_id(self) -> typing.Optional[builtins.str]:
            '''This is also known as *audience* .

            The ID of the client application that makes authentication requests to the OIDC identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-clientid
            '''
            result = self._values.get("client_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def groups_claim(self) -> typing.Optional[builtins.str]:
            '''The JSON web token (JWT) claim that the provider uses to return your groups.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-groupsclaim
            '''
            result = self._values.get("groups_claim")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def groups_prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix that is prepended to group claims to prevent clashes with existing names (such as ``system:`` groups).

            For example, the value ``oidc:`` creates group names like ``oidc:engineering`` and ``oidc:infra`` . The prefix can't contain ``system:``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-groupsprefix
            '''
            result = self._values.get("groups_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def issuer_url(self) -> typing.Optional[builtins.str]:
            '''The URL of the OIDC identity provider that allows the API server to discover public signing keys for verifying tokens.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-issuerurl
            '''
            result = self._values.get("issuer_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def required_claims(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty"]]]]:
            '''The key-value pairs that describe required claims in the identity token.

            If set, each claim is verified to be present in the token with a matching value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-requiredclaims
            '''
            result = self._values.get("required_claims")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty"]]]], result)

        @builtins.property
        def username_claim(self) -> typing.Optional[builtins.str]:
            '''The JSON Web token (JWT) claim that is used as the username.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-usernameclaim
            '''
            result = self._values.get("username_claim")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username_prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix that is prepended to username claims to prevent clashes with existing names.

            The prefix can't contain ``system:``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-oidcidentityproviderconfig.html#cfn-eks-identityproviderconfig-oidcidentityproviderconfig-usernameprefix
            '''
            result = self._values.get("username_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OidcIdentityProviderConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class RequiredClaimProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair that describes a required claim in the identity token.

            If set, each claim is verified to be present in the token with a matching value.

            :param key: The key to match from the token.
            :param value: The value for the key from the token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-requiredclaim.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                required_claim_property = eks_mixins.CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__690ee63e94cf912b8cfc99e4e8b0f97305d508cec2a2514c913555907869490c)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key to match from the token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-requiredclaim.html#cfn-eks-identityproviderconfig-requiredclaim-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the key from the token.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-identityproviderconfig-requiredclaim.html#cfn-eks-identityproviderconfig-requiredclaim-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RequiredClaimProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "ami_type": "amiType",
        "capacity_type": "capacityType",
        "cluster_name": "clusterName",
        "disk_size": "diskSize",
        "force_update_enabled": "forceUpdateEnabled",
        "instance_types": "instanceTypes",
        "labels": "labels",
        "launch_template": "launchTemplate",
        "nodegroup_name": "nodegroupName",
        "node_repair_config": "nodeRepairConfig",
        "node_role": "nodeRole",
        "release_version": "releaseVersion",
        "remote_access": "remoteAccess",
        "scaling_config": "scalingConfig",
        "subnets": "subnets",
        "tags": "tags",
        "taints": "taints",
        "update_config": "updateConfig",
        "version": "version",
    },
)
class CfnNodegroupMixinProps:
    def __init__(
        self,
        *,
        ami_type: typing.Optional[builtins.str] = None,
        capacity_type: typing.Optional[builtins.str] = None,
        cluster_name: typing.Optional[builtins.str] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        labels: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        nodegroup_name: typing.Optional[builtins.str] = None,
        node_repair_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.NodeRepairConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        node_role: typing.Optional[builtins.str] = None,
        release_version: typing.Optional[builtins.str] = None,
        remote_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.RemoteAccessProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.ScalingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        taints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.TaintProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        update_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.UpdateConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnNodegroupPropsMixin.

        :param ami_type: The AMI type for your node group. If you specify ``launchTemplate`` , and your launch template uses a custom AMI, then don't specify ``amiType`` , or the node group deployment will fail. If your launch template uses a Windows custom AMI, then add ``eks:kube-proxy-windows`` to your Windows nodes ``rolearn`` in the ``aws-auth`` ``ConfigMap`` . For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param capacity_type: The capacity type of your managed node group.
        :param cluster_name: The name of your cluster.
        :param disk_size: The root device disk size (in GiB) for your node group instances. The default disk size is 20 GiB for Linux and Bottlerocket. The default disk size is 50 GiB for Windows. If you specify ``launchTemplate`` , then don't specify ``diskSize`` , or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param force_update_enabled: Force the update if any ``Pod`` on the existing node group can't be drained due to a ``Pod`` disruption budget issue. If an update fails because all Pods can't be drained, you can force the update after it fails to terminate the old node whether or not any ``Pod`` is running on the node. Default: - false
        :param instance_types: Specify the instance types for a node group. If you specify a GPU instance type, make sure to also specify an applicable GPU AMI type with the ``amiType`` parameter. If you specify ``launchTemplate`` , then you can specify zero or one instance type in your launch template *or* you can specify 0-20 instance types for ``instanceTypes`` . If however, you specify an instance type in your launch template *and* specify any ``instanceTypes`` , the node group deployment will fail. If you don't specify an instance type in a launch template or for ``instanceTypes`` , then ``t3.medium`` is used, by default. If you specify ``Spot`` for ``capacityType`` , then we recommend specifying multiple values for ``instanceTypes`` . For more information, see `Managed node group capacity types <https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html#managed-node-group-capacity-types>`_ and `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param labels: The Kubernetes ``labels`` applied to the nodes in the node group. .. epigraph:: Only ``labels`` that are applied with the Amazon EKS API are shown here. There may be other Kubernetes ``labels`` applied to the nodes in this group.
        :param launch_template: An object representing a node group's launch template specification. When using this object, don't directly specify ``instanceTypes`` , ``diskSize`` , or ``remoteAccess`` . You cannot later specify a different launch template ID or name than what was used to create the node group. Make sure that the launch template meets the requirements in ``launchTemplateSpecification`` . Also refer to `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param nodegroup_name: The unique name to give your node group.
        :param node_repair_config: The node auto repair configuration for the node group.
        :param node_role: The Amazon Resource Name (ARN) of the IAM role to associate with your node group. The Amazon EKS worker node ``kubelet`` daemon makes calls to AWS APIs on your behalf. Nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch nodes and register them into a cluster, you must create an IAM role for those nodes to use when they are launched. For more information, see `Amazon EKS node IAM role <https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html>`_ in the **Amazon EKS User Guide** . If you specify ``launchTemplate`` , then don't specify ``[IamInstanceProfile](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_IamInstanceProfile.html)`` in your launch template, or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param release_version: The AMI version of the Amazon EKS optimized AMI to use with your node group (for example, ``1.14.7- *YYYYMMDD*`` ). By default, the latest available AMI version for the node group's current Kubernetes version is used. For more information, see `Amazon EKS optimized Linux AMI Versions <https://docs.aws.amazon.com/eks/latest/userguide/eks-linux-ami-versions.html>`_ in the *Amazon EKS User Guide* . .. epigraph:: Changing this value triggers an update of the node group if one is available. You can't update other properties at the same time as updating ``Release Version`` .
        :param remote_access: The remote access configuration to use with your node group. For Linux, the protocol is SSH. For Windows, the protocol is RDP. If you specify ``launchTemplate`` , then don't specify ``remoteAccess`` , or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param scaling_config: The scaling configuration details for the Auto Scaling group that is created for your node group.
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. If you specify ``launchTemplate`` , then don't specify ``[SubnetId](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkInterface.html)`` in your launch template, or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        :param tags: Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.
        :param taints: The Kubernetes taints to be applied to the nodes in the node group when they are created. Effect is one of ``No_Schedule`` , ``Prefer_No_Schedule`` , or ``No_Execute`` . Kubernetes taints can be used together with tolerations to control how workloads are scheduled to your nodes. For more information, see `Node taints on managed node groups <https://docs.aws.amazon.com/eks/latest/userguide/node-taints-managed-node-groups.html>`_ .
        :param update_config: The node group update configuration.
        :param version: The Kubernetes version to use for your managed nodes. By default, the Kubernetes version of the cluster is used, and this is the only accepted specified value. If you specify ``launchTemplate`` , and your launch template uses a custom AMI, then don't specify ``version`` , or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Launch template support <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* . .. epigraph:: You can't update other properties at the same time as updating ``Version`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_nodegroup_mixin_props = eks_mixins.CfnNodegroupMixinProps(
                ami_type="amiType",
                capacity_type="capacityType",
                cluster_name="clusterName",
                disk_size=123,
                force_update_enabled=False,
                instance_types=["instanceTypes"],
                labels={
                    "labels_key": "labels"
                },
                launch_template=eks_mixins.CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty(
                    id="id",
                    name="name",
                    version="version"
                ),
                nodegroup_name="nodegroupName",
                node_repair_config=eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigProperty(
                    enabled=False,
                    max_parallel_nodes_repaired_count=123,
                    max_parallel_nodes_repaired_percentage=123,
                    max_unhealthy_node_threshold_count=123,
                    max_unhealthy_node_threshold_percentage=123,
                    node_repair_config_overrides=[eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty(
                        min_repair_wait_time_mins=123,
                        node_monitoring_condition="nodeMonitoringCondition",
                        node_unhealthy_reason="nodeUnhealthyReason",
                        repair_action="repairAction"
                    )]
                ),
                node_role="nodeRole",
                release_version="releaseVersion",
                remote_access=eks_mixins.CfnNodegroupPropsMixin.RemoteAccessProperty(
                    ec2_ssh_key="ec2SshKey",
                    source_security_groups=["sourceSecurityGroups"]
                ),
                scaling_config=eks_mixins.CfnNodegroupPropsMixin.ScalingConfigProperty(
                    desired_size=123,
                    max_size=123,
                    min_size=123
                ),
                subnets=["subnets"],
                tags={
                    "tags_key": "tags"
                },
                taints=[eks_mixins.CfnNodegroupPropsMixin.TaintProperty(
                    effect="effect",
                    key="key",
                    value="value"
                )],
                update_config=eks_mixins.CfnNodegroupPropsMixin.UpdateConfigProperty(
                    max_unavailable=123,
                    max_unavailable_percentage=123,
                    update_strategy="updateStrategy"
                ),
                version="version"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef0a142ce443af7b00b26ddf05201b2966ad1ea05e9b8dc03d472336f7e08e55)
            check_type(argname="argument ami_type", value=ami_type, expected_type=type_hints["ami_type"])
            check_type(argname="argument capacity_type", value=capacity_type, expected_type=type_hints["capacity_type"])
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument disk_size", value=disk_size, expected_type=type_hints["disk_size"])
            check_type(argname="argument force_update_enabled", value=force_update_enabled, expected_type=type_hints["force_update_enabled"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument nodegroup_name", value=nodegroup_name, expected_type=type_hints["nodegroup_name"])
            check_type(argname="argument node_repair_config", value=node_repair_config, expected_type=type_hints["node_repair_config"])
            check_type(argname="argument node_role", value=node_role, expected_type=type_hints["node_role"])
            check_type(argname="argument release_version", value=release_version, expected_type=type_hints["release_version"])
            check_type(argname="argument remote_access", value=remote_access, expected_type=type_hints["remote_access"])
            check_type(argname="argument scaling_config", value=scaling_config, expected_type=type_hints["scaling_config"])
            check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument taints", value=taints, expected_type=type_hints["taints"])
            check_type(argname="argument update_config", value=update_config, expected_type=type_hints["update_config"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ami_type is not None:
            self._values["ami_type"] = ami_type
        if capacity_type is not None:
            self._values["capacity_type"] = capacity_type
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if force_update_enabled is not None:
            self._values["force_update_enabled"] = force_update_enabled
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if labels is not None:
            self._values["labels"] = labels
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if nodegroup_name is not None:
            self._values["nodegroup_name"] = nodegroup_name
        if node_repair_config is not None:
            self._values["node_repair_config"] = node_repair_config
        if node_role is not None:
            self._values["node_role"] = node_role
        if release_version is not None:
            self._values["release_version"] = release_version
        if remote_access is not None:
            self._values["remote_access"] = remote_access
        if scaling_config is not None:
            self._values["scaling_config"] = scaling_config
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags
        if taints is not None:
            self._values["taints"] = taints
        if update_config is not None:
            self._values["update_config"] = update_config
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def ami_type(self) -> typing.Optional[builtins.str]:
        '''The AMI type for your node group.

        If you specify ``launchTemplate`` , and your launch template uses a custom AMI, then don't specify ``amiType`` , or the node group deployment will fail. If your launch template uses a Windows custom AMI, then add ``eks:kube-proxy-windows`` to your Windows nodes ``rolearn`` in the ``aws-auth`` ``ConfigMap`` . For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        '''
        result = self._values.get("ami_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def capacity_type(self) -> typing.Optional[builtins.str]:
        '''The capacity type of your managed node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-capacitytype
        '''
        result = self._values.get("capacity_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of your cluster.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        '''The root device disk size (in GiB) for your node group instances.

        The default disk size is 20 GiB for Linux and Bottlerocket. The default disk size is 50 GiB for Windows. If you specify ``launchTemplate`` , then don't specify ``diskSize`` , or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        '''
        result = self._values.get("disk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def force_update_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Force the update if any ``Pod`` on the existing node group can't be drained due to a ``Pod`` disruption budget issue.

        If an update fails because all Pods can't be drained, you can force the update after it fails to terminate the old node whether or not any ``Pod`` is running on the node.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        '''
        result = self._values.get("force_update_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specify the instance types for a node group.

        If you specify a GPU instance type, make sure to also specify an applicable GPU AMI type with the ``amiType`` parameter. If you specify ``launchTemplate`` , then you can specify zero or one instance type in your launch template *or* you can specify 0-20 instance types for ``instanceTypes`` . If however, you specify an instance type in your launch template *and* specify any ``instanceTypes`` , the node group deployment will fail. If you don't specify an instance type in a launch template or for ``instanceTypes`` , then ``t3.medium`` is used, by default. If you specify ``Spot`` for ``capacityType`` , then we recommend specifying multiple values for ``instanceTypes`` . For more information, see `Managed node group capacity types <https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html#managed-node-group-capacity-types>`_ and `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def labels(
        self,
    ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
        '''The Kubernetes ``labels`` applied to the nodes in the node group.

        .. epigraph::

           Only ``labels`` that are applied with the Amazon EKS API are shown here. There may be other Kubernetes ``labels`` applied to the nodes in this group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty"]]:
        '''An object representing a node group's launch template specification.

        When using this object, don't directly specify ``instanceTypes`` , ``diskSize`` , or ``remoteAccess`` . You cannot later specify a different launch template ID or name than what was used to create the node group.

        Make sure that the launch template meets the requirements in ``launchTemplateSpecification`` . Also refer to `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-launchtemplate
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty"]], result)

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[builtins.str]:
        '''The unique name to give your node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        '''
        result = self._values.get("nodegroup_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_repair_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.NodeRepairConfigProperty"]]:
        '''The node auto repair configuration for the node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderepairconfig
        '''
        result = self._values.get("node_repair_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.NodeRepairConfigProperty"]], result)

    @builtins.property
    def node_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role to associate with your node group.

        The Amazon EKS worker node ``kubelet`` daemon makes calls to AWS APIs on your behalf. Nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch nodes and register them into a cluster, you must create an IAM role for those nodes to use when they are launched. For more information, see `Amazon EKS node IAM role <https://docs.aws.amazon.com/eks/latest/userguide/create-node-role.html>`_ in the **Amazon EKS User Guide** . If you specify ``launchTemplate`` , then don't specify ``[IamInstanceProfile](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_IamInstanceProfile.html)`` in your launch template, or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        '''
        result = self._values.get("node_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def release_version(self) -> typing.Optional[builtins.str]:
        '''The AMI version of the Amazon EKS optimized AMI to use with your node group (for example, ``1.14.7- *YYYYMMDD*`` ). By default, the latest available AMI version for the node group's current Kubernetes version is used. For more information, see `Amazon EKS optimized Linux AMI Versions <https://docs.aws.amazon.com/eks/latest/userguide/eks-linux-ami-versions.html>`_ in the *Amazon EKS User Guide* .

        .. epigraph::

           Changing this value triggers an update of the node group if one is available. You can't update other properties at the same time as updating ``Release Version`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        '''
        result = self._values.get("release_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_access(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.RemoteAccessProperty"]]:
        '''The remote access configuration to use with your node group.

        For Linux, the protocol is SSH. For Windows, the protocol is RDP. If you specify ``launchTemplate`` , then don't specify ``remoteAccess`` , or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        '''
        result = self._values.get("remote_access")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.RemoteAccessProperty"]], result)

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.ScalingConfigProperty"]]:
        '''The scaling configuration details for the Auto Scaling group that is created for your node group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        '''
        result = self._values.get("scaling_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.ScalingConfigProperty"]], result)

    @builtins.property
    def subnets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The subnets to use for the Auto Scaling group that is created for your node group.

        If you specify ``launchTemplate`` , then don't specify ``[SubnetId](https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkInterface.html)`` in your launch template, or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        '''
        result = self._values.get("subnets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata that assists with categorization and organization.

        Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def taints(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.TaintProperty"]]]]:
        '''The Kubernetes taints to be applied to the nodes in the node group when they are created.

        Effect is one of ``No_Schedule`` , ``Prefer_No_Schedule`` , or ``No_Execute`` . Kubernetes taints can be used together with tolerations to control how workloads are scheduled to your nodes. For more information, see `Node taints on managed node groups <https://docs.aws.amazon.com/eks/latest/userguide/node-taints-managed-node-groups.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-taints
        '''
        result = self._values.get("taints")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.TaintProperty"]]]], result)

    @builtins.property
    def update_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.UpdateConfigProperty"]]:
        '''The node group update configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-updateconfig
        '''
        result = self._values.get("update_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.UpdateConfigProperty"]], result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''The Kubernetes version to use for your managed nodes.

        By default, the Kubernetes version of the cluster is used, and this is the only accepted specified value. If you specify ``launchTemplate`` , and your launch template uses a custom AMI, then don't specify ``version`` , or the node group deployment will fail. For more information about using launch templates with Amazon EKS, see `Launch template support <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .
        .. epigraph::

           You can't update other properties at the same time as updating ``Version`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNodegroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnNodegroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin",
):
    '''Creates a managed node group for an Amazon EKS cluster.

    You can only create a node group for your cluster that is equal to the current Kubernetes version for the cluster. All node groups are created with the latest AMI release version for the respective minor Kubernetes version of the cluster, unless you deploy a custom AMI using a launch template.

    For later updates, you will only be able to update a node group using a launch template only if it was originally deployed with a launch template. Additionally, the launch template ID or name must match what was used when the node group was created. You can update the launch template version with necessary changes. For more information about using launch templates, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ .

    An Amazon EKS managed node group is an Amazon EC2 Amazon EC2 Auto Scaling group and associated Amazon EC2 instances that are managed by AWS for an Amazon EKS cluster. For more information, see `Managed node groups <https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html>`_ in the *Amazon EKS User Guide* .
    .. epigraph::

       Windows AMI types are only supported for commercial AWS Regions that support Windows on Amazon EKS.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
    :cloudformationResource: AWS::EKS::Nodegroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_nodegroup_props_mixin = eks_mixins.CfnNodegroupPropsMixin(eks_mixins.CfnNodegroupMixinProps(
            ami_type="amiType",
            capacity_type="capacityType",
            cluster_name="clusterName",
            disk_size=123,
            force_update_enabled=False,
            instance_types=["instanceTypes"],
            labels={
                "labels_key": "labels"
            },
            launch_template=eks_mixins.CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty(
                id="id",
                name="name",
                version="version"
            ),
            nodegroup_name="nodegroupName",
            node_repair_config=eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigProperty(
                enabled=False,
                max_parallel_nodes_repaired_count=123,
                max_parallel_nodes_repaired_percentage=123,
                max_unhealthy_node_threshold_count=123,
                max_unhealthy_node_threshold_percentage=123,
                node_repair_config_overrides=[eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty(
                    min_repair_wait_time_mins=123,
                    node_monitoring_condition="nodeMonitoringCondition",
                    node_unhealthy_reason="nodeUnhealthyReason",
                    repair_action="repairAction"
                )]
            ),
            node_role="nodeRole",
            release_version="releaseVersion",
            remote_access=eks_mixins.CfnNodegroupPropsMixin.RemoteAccessProperty(
                ec2_ssh_key="ec2SshKey",
                source_security_groups=["sourceSecurityGroups"]
            ),
            scaling_config=eks_mixins.CfnNodegroupPropsMixin.ScalingConfigProperty(
                desired_size=123,
                max_size=123,
                min_size=123
            ),
            subnets=["subnets"],
            tags={
                "tags_key": "tags"
            },
            taints=[eks_mixins.CfnNodegroupPropsMixin.TaintProperty(
                effect="effect",
                key="key",
                value="value"
            )],
            update_config=eks_mixins.CfnNodegroupPropsMixin.UpdateConfigProperty(
                max_unavailable=123,
                max_unavailable_percentage=123,
                update_strategy="updateStrategy"
            ),
            version="version"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnNodegroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::Nodegroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__057f2cd808c02688415746571246536821a421b1731e4c8f3b7b67e8b81caba6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__858afb7a10cb7ff45e75e3d382eb242e0106bee45b3dcebed15c0584a8afc0ee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96c5d60afe31328fd8c735be89968b32c65cb341759062b1e80b7936a556fea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnNodegroupMixinProps:
        return typing.cast(CfnNodegroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "name": "name", "version": "version"},
    )
    class LaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object representing a node group launch template specification.

            The launch template can't include ```SubnetId`` <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateNetworkInterface.html>`_ , ```IamInstanceProfile`` <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_IamInstanceProfile.html>`_ , ```RequestSpotInstances`` <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RequestSpotInstances.html>`_ , ```HibernationOptions`` <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_HibernationOptionsRequest.html>`_ , or ```TerminateInstances`` <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_TerminateInstances.html>`_ , or the node group deployment or update will fail. For more information about launch templates, see ```CreateLaunchTemplate`` <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_CreateLaunchTemplate.html>`_ in the Amazon EC2 API Reference. For more information about using launch templates with Amazon EKS, see `Customizing managed nodes with launch templates <https://docs.aws.amazon.com/eks/latest/userguide/launch-templates.html>`_ in the *Amazon EKS User Guide* .

            You must specify either the launch template ID or the launch template name in the request, but not both.

            :param id: The ID of the launch template. You must specify either the launch template ID or the launch template name in the request, but not both. After node group creation, you cannot use a different ID.
            :param name: The name of the launch template. You must specify either the launch template name or the launch template ID in the request, but not both. After node group creation, you cannot use a different name.
            :param version: The version number of the launch template to use. If no version is specified, then the template's default version is used. You can use a different version for node group updates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-launchtemplatespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                launch_template_specification_property = eks_mixins.CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty(
                    id="id",
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b36cee528d1052c7ce04005d1159a427b1f69fe4f0fdf645e6c8a14720e0b6ac)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The ID of the launch template.

            You must specify either the launch template ID or the launch template name in the request, but not both. After node group creation, you cannot use a different ID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-launchtemplatespecification.html#cfn-eks-nodegroup-launchtemplatespecification-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch template.

            You must specify either the launch template name or the launch template ID in the request, but not both. After node group creation, you cannot use a different name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-launchtemplatespecification.html#cfn-eks-nodegroup-launchtemplatespecification-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version number of the launch template to use.

            If no version is specified, then the template's default version is used. You can use a different version for node group updates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-launchtemplatespecification.html#cfn-eks-nodegroup-launchtemplatespecification-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "min_repair_wait_time_mins": "minRepairWaitTimeMins",
            "node_monitoring_condition": "nodeMonitoringCondition",
            "node_unhealthy_reason": "nodeUnhealthyReason",
            "repair_action": "repairAction",
        },
    )
    class NodeRepairConfigOverridesProperty:
        def __init__(
            self,
            *,
            min_repair_wait_time_mins: typing.Optional[jsii.Number] = None,
            node_monitoring_condition: typing.Optional[builtins.str] = None,
            node_unhealthy_reason: typing.Optional[builtins.str] = None,
            repair_action: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specify granular overrides for specific repair actions.

            These overrides control the repair action and the repair delay time before a node is considered eligible for repair. If you use this, you must specify all the values.

            :param min_repair_wait_time_mins: Specify the minimum time in minutes to wait before attempting to repair a node with this specific NodeMonitoringCondition and NodeUnhealthyReason.
            :param node_monitoring_condition: Specify an unhealthy condition reported by the node monitoring agent that this override would apply to.
            :param node_unhealthy_reason: Specify a reason reported by the node monitoring agent that this override would apply to.
            :param repair_action: Specify the repair action to take for nodes when all of the specified conditions are met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfigoverrides.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                node_repair_config_overrides_property = eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty(
                    min_repair_wait_time_mins=123,
                    node_monitoring_condition="nodeMonitoringCondition",
                    node_unhealthy_reason="nodeUnhealthyReason",
                    repair_action="repairAction"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a94836a82f4b000716de195407d972d5c627c6a1a6570ac2cbb0015d6c599263)
                check_type(argname="argument min_repair_wait_time_mins", value=min_repair_wait_time_mins, expected_type=type_hints["min_repair_wait_time_mins"])
                check_type(argname="argument node_monitoring_condition", value=node_monitoring_condition, expected_type=type_hints["node_monitoring_condition"])
                check_type(argname="argument node_unhealthy_reason", value=node_unhealthy_reason, expected_type=type_hints["node_unhealthy_reason"])
                check_type(argname="argument repair_action", value=repair_action, expected_type=type_hints["repair_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if min_repair_wait_time_mins is not None:
                self._values["min_repair_wait_time_mins"] = min_repair_wait_time_mins
            if node_monitoring_condition is not None:
                self._values["node_monitoring_condition"] = node_monitoring_condition
            if node_unhealthy_reason is not None:
                self._values["node_unhealthy_reason"] = node_unhealthy_reason
            if repair_action is not None:
                self._values["repair_action"] = repair_action

        @builtins.property
        def min_repair_wait_time_mins(self) -> typing.Optional[jsii.Number]:
            '''Specify the minimum time in minutes to wait before attempting to repair a node with this specific NodeMonitoringCondition and NodeUnhealthyReason.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfigoverrides.html#cfn-eks-nodegroup-noderepairconfigoverrides-minrepairwaittimemins
            '''
            result = self._values.get("min_repair_wait_time_mins")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def node_monitoring_condition(self) -> typing.Optional[builtins.str]:
            '''Specify an unhealthy condition reported by the node monitoring agent that this override would apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfigoverrides.html#cfn-eks-nodegroup-noderepairconfigoverrides-nodemonitoringcondition
            '''
            result = self._values.get("node_monitoring_condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def node_unhealthy_reason(self) -> typing.Optional[builtins.str]:
            '''Specify a reason reported by the node monitoring agent that this override would apply to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfigoverrides.html#cfn-eks-nodegroup-noderepairconfigoverrides-nodeunhealthyreason
            '''
            result = self._values.get("node_unhealthy_reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def repair_action(self) -> typing.Optional[builtins.str]:
            '''Specify the repair action to take for nodes when all of the specified conditions are met.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfigoverrides.html#cfn-eks-nodegroup-noderepairconfigoverrides-repairaction
            '''
            result = self._values.get("repair_action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeRepairConfigOverridesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.NodeRepairConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "max_parallel_nodes_repaired_count": "maxParallelNodesRepairedCount",
            "max_parallel_nodes_repaired_percentage": "maxParallelNodesRepairedPercentage",
            "max_unhealthy_node_threshold_count": "maxUnhealthyNodeThresholdCount",
            "max_unhealthy_node_threshold_percentage": "maxUnhealthyNodeThresholdPercentage",
            "node_repair_config_overrides": "nodeRepairConfigOverrides",
        },
    )
    class NodeRepairConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            max_parallel_nodes_repaired_count: typing.Optional[jsii.Number] = None,
            max_parallel_nodes_repaired_percentage: typing.Optional[jsii.Number] = None,
            max_unhealthy_node_threshold_count: typing.Optional[jsii.Number] = None,
            max_unhealthy_node_threshold_percentage: typing.Optional[jsii.Number] = None,
            node_repair_config_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The node auto repair configuration for the node group.

            :param enabled: Specifies whether to enable node auto repair for the node group. Node auto repair is disabled by default.
            :param max_parallel_nodes_repaired_count: Specify the maximum number of nodes that can be repaired concurrently or in parallel, expressed as a count of unhealthy nodes. This gives you finer-grained control over the pace of node replacements. When using this, you cannot also set MaxParallelNodesRepairedPercentage at the same time.
            :param max_parallel_nodes_repaired_percentage: Specify the maximum number of nodes that can be repaired concurrently or in parallel, expressed as a percentage of unhealthy nodes. This gives you finer-grained control over the pace of node replacements. When using this, you cannot also set MaxParallelNodesRepairedCount at the same time.
            :param max_unhealthy_node_threshold_count: Specify a count threshold of unhealthy nodes, above which node auto repair actions will stop. When using this, you cannot also set MaxUnhealthyNodeThresholdPercentage at the same time.
            :param max_unhealthy_node_threshold_percentage: Specify a percentage threshold of unhealthy nodes, above which node auto repair actions will stop. When using this, you cannot also set MaxUnhealthyNodeThresholdCount at the same time.
            :param node_repair_config_overrides: Specify granular overrides for specific repair actions. These overrides control the repair action and the repair delay time before a node is considered eligible for repair. If you use this, you must specify all the values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                node_repair_config_property = eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigProperty(
                    enabled=False,
                    max_parallel_nodes_repaired_count=123,
                    max_parallel_nodes_repaired_percentage=123,
                    max_unhealthy_node_threshold_count=123,
                    max_unhealthy_node_threshold_percentage=123,
                    node_repair_config_overrides=[eks_mixins.CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty(
                        min_repair_wait_time_mins=123,
                        node_monitoring_condition="nodeMonitoringCondition",
                        node_unhealthy_reason="nodeUnhealthyReason",
                        repair_action="repairAction"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c4bca4634996e40c842517ab9ef6a98a5e23339d8a099c7aaca9095eb09ef24)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument max_parallel_nodes_repaired_count", value=max_parallel_nodes_repaired_count, expected_type=type_hints["max_parallel_nodes_repaired_count"])
                check_type(argname="argument max_parallel_nodes_repaired_percentage", value=max_parallel_nodes_repaired_percentage, expected_type=type_hints["max_parallel_nodes_repaired_percentage"])
                check_type(argname="argument max_unhealthy_node_threshold_count", value=max_unhealthy_node_threshold_count, expected_type=type_hints["max_unhealthy_node_threshold_count"])
                check_type(argname="argument max_unhealthy_node_threshold_percentage", value=max_unhealthy_node_threshold_percentage, expected_type=type_hints["max_unhealthy_node_threshold_percentage"])
                check_type(argname="argument node_repair_config_overrides", value=node_repair_config_overrides, expected_type=type_hints["node_repair_config_overrides"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_parallel_nodes_repaired_count is not None:
                self._values["max_parallel_nodes_repaired_count"] = max_parallel_nodes_repaired_count
            if max_parallel_nodes_repaired_percentage is not None:
                self._values["max_parallel_nodes_repaired_percentage"] = max_parallel_nodes_repaired_percentage
            if max_unhealthy_node_threshold_count is not None:
                self._values["max_unhealthy_node_threshold_count"] = max_unhealthy_node_threshold_count
            if max_unhealthy_node_threshold_percentage is not None:
                self._values["max_unhealthy_node_threshold_percentage"] = max_unhealthy_node_threshold_percentage
            if node_repair_config_overrides is not None:
                self._values["node_repair_config_overrides"] = node_repair_config_overrides

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether to enable node auto repair for the node group.

            Node auto repair is disabled by default.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html#cfn-eks-nodegroup-noderepairconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def max_parallel_nodes_repaired_count(self) -> typing.Optional[jsii.Number]:
            '''Specify the maximum number of nodes that can be repaired concurrently or in parallel, expressed as a count of unhealthy nodes.

            This gives you finer-grained control over the pace of node replacements. When using this, you cannot also set MaxParallelNodesRepairedPercentage at the same time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html#cfn-eks-nodegroup-noderepairconfig-maxparallelnodesrepairedcount
            '''
            result = self._values.get("max_parallel_nodes_repaired_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_parallel_nodes_repaired_percentage(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''Specify the maximum number of nodes that can be repaired concurrently or in parallel, expressed as a percentage of unhealthy nodes.

            This gives you finer-grained control over the pace of node replacements. When using this, you cannot also set MaxParallelNodesRepairedCount at the same time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html#cfn-eks-nodegroup-noderepairconfig-maxparallelnodesrepairedpercentage
            '''
            result = self._values.get("max_parallel_nodes_repaired_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_unhealthy_node_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''Specify a count threshold of unhealthy nodes, above which node auto repair actions will stop.

            When using this, you cannot also set MaxUnhealthyNodeThresholdPercentage at the same time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html#cfn-eks-nodegroup-noderepairconfig-maxunhealthynodethresholdcount
            '''
            result = self._values.get("max_unhealthy_node_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_unhealthy_node_threshold_percentage(
            self,
        ) -> typing.Optional[jsii.Number]:
            '''Specify a percentage threshold of unhealthy nodes, above which node auto repair actions will stop.

            When using this, you cannot also set MaxUnhealthyNodeThresholdCount at the same time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html#cfn-eks-nodegroup-noderepairconfig-maxunhealthynodethresholdpercentage
            '''
            result = self._values.get("max_unhealthy_node_threshold_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def node_repair_config_overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty"]]]]:
            '''Specify granular overrides for specific repair actions.

            These overrides control the repair action and the repair delay time before a node is considered eligible for repair. If you use this, you must specify all the values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-noderepairconfig.html#cfn-eks-nodegroup-noderepairconfig-noderepairconfigoverrides
            '''
            result = self._values.get("node_repair_config_overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeRepairConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.RemoteAccessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ec2_ssh_key": "ec2SshKey",
            "source_security_groups": "sourceSecurityGroups",
        },
    )
    class RemoteAccessProperty:
        def __init__(
            self,
            *,
            ec2_ssh_key: typing.Optional[builtins.str] = None,
            source_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object representing the remote access configuration for the managed node group.

            :param ec2_ssh_key: The Amazon EC2 SSH key name that provides access for SSH communication with the nodes in the managed node group. For more information, see `Amazon EC2 key pairs and Linux instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_ in the *Amazon Elastic Compute Cloud User Guide for Linux Instances* . For Windows, an Amazon EC2 SSH key is used to obtain the RDP password. For more information, see `Amazon EC2 key pairs and Windows instances <https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-key-pairs.html>`_ in the *Amazon Elastic Compute Cloud User Guide for Windows Instances* .
            :param source_security_groups: The security group IDs that are allowed SSH access (port 22) to the nodes. For Windows, the port is 3389. If you specify an Amazon EC2 SSH key but don't specify a source security group when you create a managed node group, then the port on the nodes is opened to the internet ( ``0.0.0.0/0`` ). For more information, see `Security Groups for Your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                remote_access_property = eks_mixins.CfnNodegroupPropsMixin.RemoteAccessProperty(
                    ec2_ssh_key="ec2SshKey",
                    source_security_groups=["sourceSecurityGroups"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5edc1eb0f53df48c00447fc31c0e68d112367c02d295fb991dbd452f7478bd1f)
                check_type(argname="argument ec2_ssh_key", value=ec2_ssh_key, expected_type=type_hints["ec2_ssh_key"])
                check_type(argname="argument source_security_groups", value=source_security_groups, expected_type=type_hints["source_security_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ec2_ssh_key is not None:
                self._values["ec2_ssh_key"] = ec2_ssh_key
            if source_security_groups is not None:
                self._values["source_security_groups"] = source_security_groups

        @builtins.property
        def ec2_ssh_key(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 SSH key name that provides access for SSH communication with the nodes in the managed node group.

            For more information, see `Amazon EC2 key pairs and Linux instances <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html>`_ in the *Amazon Elastic Compute Cloud User Guide for Linux Instances* . For Windows, an Amazon EC2 SSH key is used to obtain the RDP password. For more information, see `Amazon EC2 key pairs and Windows instances <https://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/ec2-key-pairs.html>`_ in the *Amazon Elastic Compute Cloud User Guide for Windows Instances* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-ec2sshkey
            '''
            result = self._values.get("ec2_ssh_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_security_groups(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security group IDs that are allowed SSH access (port 22) to the nodes.

            For Windows, the port is 3389. If you specify an Amazon EC2 SSH key but don't specify a source security group when you create a managed node group, then the port on the nodes is opened to the internet ( ``0.0.0.0/0`` ). For more information, see `Security Groups for Your VPC <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon Virtual Private Cloud User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-sourcesecuritygroups
            '''
            result = self._values.get("source_security_groups")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemoteAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.ScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_size": "desiredSize",
            "max_size": "maxSize",
            "min_size": "minSize",
        },
    )
    class ScalingConfigProperty:
        def __init__(
            self,
            *,
            desired_size: typing.Optional[jsii.Number] = None,
            max_size: typing.Optional[jsii.Number] = None,
            min_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object representing the scaling configuration details for the Amazon EC2 Auto Scaling group that is associated with your node group.

            When creating a node group, you must specify all or none of the properties. When updating a node group, you can specify any or none of the properties.

            :param desired_size: The current number of nodes that the managed node group should maintain. .. epigraph:: If you use the Kubernetes `Cluster Autoscaler <https://docs.aws.amazon.com/https://github.com/kubernetes/autoscaler#kubernetes-autoscaler>`_ , you shouldn't change the ``desiredSize`` value directly, as this can cause the Cluster Autoscaler to suddenly scale up or scale down. Whenever this parameter changes, the number of worker nodes in the node group is updated to the specified size. If this parameter is given a value that is smaller than the current number of running worker nodes, the necessary number of worker nodes are terminated to match the given value. When using CloudFormation, no action occurs if you remove this parameter from your CFN template. This parameter can be different from ``minSize`` in some cases, such as when starting with extra hosts for testing. This parameter can also be different when you want to start with an estimated number of needed hosts, but let the Cluster Autoscaler reduce the number if there are too many. When the Cluster Autoscaler is used, the ``desiredSize`` parameter is altered by the Cluster Autoscaler (but can be out-of-date for short periods of time). the Cluster Autoscaler doesn't scale a managed node group lower than ``minSize`` or higher than ``maxSize`` .
            :param max_size: The maximum number of nodes that the managed node group can scale out to. For information about the maximum number that you can specify, see `Amazon EKS service quotas <https://docs.aws.amazon.com/eks/latest/userguide/service-quotas.html>`_ in the *Amazon EKS User Guide* .
            :param min_size: The minimum number of nodes that the managed node group can scale in to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                scaling_config_property = eks_mixins.CfnNodegroupPropsMixin.ScalingConfigProperty(
                    desired_size=123,
                    max_size=123,
                    min_size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8727d4084fa5ce10c520a48a963a3668d23b7c25df1ff9d7ffd2e9b898d15ae)
                check_type(argname="argument desired_size", value=desired_size, expected_type=type_hints["desired_size"])
                check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
                check_type(argname="argument min_size", value=min_size, expected_type=type_hints["min_size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if desired_size is not None:
                self._values["desired_size"] = desired_size
            if max_size is not None:
                self._values["max_size"] = max_size
            if min_size is not None:
                self._values["min_size"] = min_size

        @builtins.property
        def desired_size(self) -> typing.Optional[jsii.Number]:
            '''The current number of nodes that the managed node group should maintain.

            .. epigraph::

               If you use the Kubernetes `Cluster Autoscaler <https://docs.aws.amazon.com/https://github.com/kubernetes/autoscaler#kubernetes-autoscaler>`_ , you shouldn't change the ``desiredSize`` value directly, as this can cause the Cluster Autoscaler to suddenly scale up or scale down.

            Whenever this parameter changes, the number of worker nodes in the node group is updated to the specified size. If this parameter is given a value that is smaller than the current number of running worker nodes, the necessary number of worker nodes are terminated to match the given value. When using CloudFormation, no action occurs if you remove this parameter from your CFN template.

            This parameter can be different from ``minSize`` in some cases, such as when starting with extra hosts for testing. This parameter can also be different when you want to start with an estimated number of needed hosts, but let the Cluster Autoscaler reduce the number if there are too many. When the Cluster Autoscaler is used, the ``desiredSize`` parameter is altered by the Cluster Autoscaler (but can be out-of-date for short periods of time). the Cluster Autoscaler doesn't scale a managed node group lower than ``minSize`` or higher than ``maxSize`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-desiredsize
            '''
            result = self._values.get("desired_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of nodes that the managed node group can scale out to.

            For information about the maximum number that you can specify, see `Amazon EKS service quotas <https://docs.aws.amazon.com/eks/latest/userguide/service-quotas.html>`_ in the *Amazon EKS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-maxsize
            '''
            result = self._values.get("max_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_size(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of nodes that the managed node group can scale in to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-minsize
            '''
            result = self._values.get("min_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.TaintProperty",
        jsii_struct_bases=[],
        name_mapping={"effect": "effect", "key": "key", "value": "value"},
    )
    class TaintProperty:
        def __init__(
            self,
            *,
            effect: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A property that allows a node to repel a ``Pod`` .

            For more information, see `Node taints on managed node groups <https://docs.aws.amazon.com/eks/latest/userguide/node-taints-managed-node-groups.html>`_ in the *Amazon EKS User Guide* .

            :param effect: The effect of the taint.
            :param key: The key of the taint.
            :param value: The value of the taint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-taint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                taint_property = eks_mixins.CfnNodegroupPropsMixin.TaintProperty(
                    effect="effect",
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__712dbc410ae98ac8d544a9e6cf4839d71a0a357a350df69df951a804bd44d263)
                check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if effect is not None:
                self._values["effect"] = effect
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def effect(self) -> typing.Optional[builtins.str]:
            '''The effect of the taint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-taint.html#cfn-eks-nodegroup-taint-effect
            '''
            result = self._values.get("effect")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key of the taint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-taint.html#cfn-eks-nodegroup-taint-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the taint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-taint.html#cfn-eks-nodegroup-taint-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TaintProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnNodegroupPropsMixin.UpdateConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_unavailable": "maxUnavailable",
            "max_unavailable_percentage": "maxUnavailablePercentage",
            "update_strategy": "updateStrategy",
        },
    )
    class UpdateConfigProperty:
        def __init__(
            self,
            *,
            max_unavailable: typing.Optional[jsii.Number] = None,
            max_unavailable_percentage: typing.Optional[jsii.Number] = None,
            update_strategy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The update configuration for the node group.

            :param max_unavailable: The maximum number of nodes unavailable at once during a version update. Nodes are updated in parallel. This value or ``maxUnavailablePercentage`` is required to have a value.The maximum number is 100.
            :param max_unavailable_percentage: The maximum percentage of nodes unavailable during a version update. This percentage of nodes are updated in parallel, up to 100 nodes at once. This value or ``maxUnavailable`` is required to have a value.
            :param update_strategy: The configuration for the behavior to follow during a node group version update of this managed node group. You choose between two possible strategies for replacing nodes during an ```UpdateNodegroupVersion`` <https://docs.aws.amazon.com/eks/latest/APIReference/API_UpdateNodegroupVersion.html>`_ action. An Amazon EKS managed node group updates by replacing nodes with new nodes of newer AMI versions in parallel. The *update strategy* changes the managed node update behavior of the managed node group for each quantity. The *default* strategy has guardrails to protect you from misconfiguration and launches the new instances first, before terminating the old instances. The *minimal* strategy removes the guardrails and terminates the old instances before launching the new instances. This minimal strategy is useful in scenarios where you are constrained to resources or costs (for example, with hardware accelerators such as GPUs).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-updateconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
                
                update_config_property = eks_mixins.CfnNodegroupPropsMixin.UpdateConfigProperty(
                    max_unavailable=123,
                    max_unavailable_percentage=123,
                    update_strategy="updateStrategy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eeefc9f8994774a62d4a08efb5f2c485724aa74f8560295369ad32358fe2faf7)
                check_type(argname="argument max_unavailable", value=max_unavailable, expected_type=type_hints["max_unavailable"])
                check_type(argname="argument max_unavailable_percentage", value=max_unavailable_percentage, expected_type=type_hints["max_unavailable_percentage"])
                check_type(argname="argument update_strategy", value=update_strategy, expected_type=type_hints["update_strategy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_unavailable is not None:
                self._values["max_unavailable"] = max_unavailable
            if max_unavailable_percentage is not None:
                self._values["max_unavailable_percentage"] = max_unavailable_percentage
            if update_strategy is not None:
                self._values["update_strategy"] = update_strategy

        @builtins.property
        def max_unavailable(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of nodes unavailable at once during a version update.

            Nodes are updated in parallel. This value or ``maxUnavailablePercentage`` is required to have a value.The maximum number is 100.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-updateconfig.html#cfn-eks-nodegroup-updateconfig-maxunavailable
            '''
            result = self._values.get("max_unavailable")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_unavailable_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage of nodes unavailable during a version update.

            This percentage of nodes are updated in parallel, up to 100 nodes at once. This value or ``maxUnavailable`` is required to have a value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-updateconfig.html#cfn-eks-nodegroup-updateconfig-maxunavailablepercentage
            '''
            result = self._values.get("max_unavailable_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def update_strategy(self) -> typing.Optional[builtins.str]:
            '''The configuration for the behavior to follow during a node group version update of this managed node group.

            You choose between two possible strategies for replacing nodes during an ```UpdateNodegroupVersion`` <https://docs.aws.amazon.com/eks/latest/APIReference/API_UpdateNodegroupVersion.html>`_ action.

            An Amazon EKS managed node group updates by replacing nodes with new nodes of newer AMI versions in parallel. The *update strategy* changes the managed node update behavior of the managed node group for each quantity. The *default* strategy has guardrails to protect you from misconfiguration and launches the new instances first, before terminating the old instances. The *minimal* strategy removes the guardrails and terminates the old instances before launching the new instances. This minimal strategy is useful in scenarios where you are constrained to resources or costs (for example, with hardware accelerators such as GPUs).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-updateconfig.html#cfn-eks-nodegroup-updateconfig-updatestrategy
            '''
            result = self._values.get("update_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdateConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnPodIdentityAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "disable_session_tags": "disableSessionTags",
        "namespace": "namespace",
        "role_arn": "roleArn",
        "service_account": "serviceAccount",
        "tags": "tags",
        "target_role_arn": "targetRoleArn",
    },
)
class CfnPodIdentityAssociationMixinProps:
    def __init__(
        self,
        *,
        cluster_name: typing.Optional[builtins.str] = None,
        disable_session_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        namespace: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPodIdentityAssociationPropsMixin.

        :param cluster_name: The name of the cluster that the association is in.
        :param disable_session_tags: The state of the automatic sessions tags. The value of *true* disables these tags. EKS Pod Identity adds a pre-defined set of session tags when it assumes the role. You can use these tags to author a single role that can work across resources by allowing access to AWS resources based on matching tags. By default, EKS Pod Identity attaches six tags, including tags for cluster name, namespace, and service account name. For the list of tags added by EKS Pod Identity, see `List of session tags added by EKS Pod Identity <https://docs.aws.amazon.com/eks/latest/userguide/pod-id-abac.html#pod-id-abac-tags>`_ in the *Amazon EKS User Guide* .
        :param namespace: The name of the Kubernetes namespace inside the cluster to create the association in. The service account and the Pods that use the service account must be in this namespace.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role to associate with the service account. The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the Pods that use this service account.
        :param service_account: The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.
        :param tags: Metadata that assists with categorization and organization. Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources. The following basic restrictions apply to tags: - Maximum number of tags per resource – 50 - For each resource, each tag key must be unique, and each tag key can have only one value. - Maximum key length – 128 Unicode characters in UTF-8 - Maximum value length – 256 Unicode characters in UTF-8 - If your tagging schema is used across multiple services and resources, remember that other services may have restrictions on allowed characters. Generally allowed characters are: letters, numbers, and spaces representable in UTF-8, and the following characters: + - = . _ : /
        :param target_role_arn: The Amazon Resource Name (ARN) of the target IAM role to associate with the service account. This role is assumed by using the EKS Pod Identity association role, then the credentials for this role are injected into the Pod.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
            
            cfn_pod_identity_association_mixin_props = eks_mixins.CfnPodIdentityAssociationMixinProps(
                cluster_name="clusterName",
                disable_session_tags=False,
                namespace="namespace",
                role_arn="roleArn",
                service_account="serviceAccount",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_role_arn="targetRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb5898782698aebfa9c055c02192df0552b4a7d7519cd2249c867204e93d6236)
            check_type(argname="argument cluster_name", value=cluster_name, expected_type=type_hints["cluster_name"])
            check_type(argname="argument disable_session_tags", value=disable_session_tags, expected_type=type_hints["disable_session_tags"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_role_arn", value=target_role_arn, expected_type=type_hints["target_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if disable_session_tags is not None:
            self._values["disable_session_tags"] = disable_session_tags
        if namespace is not None:
            self._values["namespace"] = namespace
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if service_account is not None:
            self._values["service_account"] = service_account
        if tags is not None:
            self._values["tags"] = tags
        if target_role_arn is not None:
            self._values["target_role_arn"] = target_role_arn

    @builtins.property
    def cluster_name(self) -> typing.Optional[builtins.str]:
        '''The name of the cluster that the association is in.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-clustername
        '''
        result = self._values.get("cluster_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_session_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''The state of the automatic sessions tags. The value of *true* disables these tags.

        EKS Pod Identity adds a pre-defined set of session tags when it assumes the role. You can use these tags to author a single role that can work across resources by allowing access to AWS resources based on matching tags. By default, EKS Pod Identity attaches six tags, including tags for cluster name, namespace, and service account name. For the list of tags added by EKS Pod Identity, see `List of session tags added by EKS Pod Identity <https://docs.aws.amazon.com/eks/latest/userguide/pod-id-abac.html#pod-id-abac-tags>`_ in the *Amazon EKS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-disablesessiontags
        '''
        result = self._values.get("disable_session_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The name of the Kubernetes namespace inside the cluster to create the association in.

        The service account and the Pods that use the service account must be in this namespace.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-namespace
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role to associate with the service account.

        The EKS Pod Identity agent manages credentials to assume this role for applications in the containers in the Pods that use this service account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''The name of the Kubernetes service account inside the cluster to associate the IAM credentials with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-serviceaccount
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata that assists with categorization and organization.

        Each tag consists of a key and an optional value. You define both. Tags don't propagate to any other cluster or AWS resources.

        The following basic restrictions apply to tags:

        - Maximum number of tags per resource – 50
        - For each resource, each tag key must be unique, and each tag key can have only one value.
        - Maximum key length – 128 Unicode characters in UTF-8
        - Maximum value length – 256 Unicode characters in UTF-8
        - If your tagging schema is used across multiple services and resources, remember that other services may have restrictions on allowed characters. Generally allowed characters are: letters, numbers, and spaces representable in UTF-8, and the following characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-tags
        ::

        .

        - Tag keys and values are case-sensitive.
        - Do not use ``aws:`` , ``AWS:`` , or any upper or lowercase combination of such as a prefix for either keys or values as it is reserved for AWS use. You cannot edit or delete tag keys or values with this prefix. Tags with this prefix do not count against your tags per resource limit.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the target IAM role to associate with the service account.

        This role is assumed by using the EKS Pod Identity association role, then the credentials for this role are injected into the Pod.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html#cfn-eks-podidentityassociation-targetrolearn
        '''
        result = self._values.get("target_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPodIdentityAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPodIdentityAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_eks.mixins.CfnPodIdentityAssociationPropsMixin",
):
    '''Amazon EKS Pod Identity associations provide the ability to manage credentials for your applications, similar to the way that Amazon EC2 instance profiles provide credentials to Amazon EC2 instances.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-podidentityassociation.html
    :cloudformationResource: AWS::EKS::PodIdentityAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_eks import mixins as eks_mixins
        
        cfn_pod_identity_association_props_mixin = eks_mixins.CfnPodIdentityAssociationPropsMixin(eks_mixins.CfnPodIdentityAssociationMixinProps(
            cluster_name="clusterName",
            disable_session_tags=False,
            namespace="namespace",
            role_arn="roleArn",
            service_account="serviceAccount",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_role_arn="targetRoleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPodIdentityAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::EKS::PodIdentityAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc6ef39db082ca55da9ac28bdfe0ca2bb09eb2b5222ad338344c892ad20e779d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70629ec0511c50d1dd7a804bc59f5c26ffc451559abb8619095e49201b1c42eb)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf607ba52abd329900a6c5bb0642eeb876b16274e01445a5e4a39dd060b007e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPodIdentityAssociationMixinProps:
        return typing.cast(CfnPodIdentityAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAccessEntryMixinProps",
    "CfnAccessEntryPropsMixin",
    "CfnAddonMixinProps",
    "CfnAddonPropsMixin",
    "CfnCapabilityMixinProps",
    "CfnCapabilityPropsMixin",
    "CfnClusterAutoModeBlockStorageLogs",
    "CfnClusterAutoModeComputeLogs",
    "CfnClusterAutoModeIpamLogs",
    "CfnClusterAutoModeLoadBalancingLogs",
    "CfnClusterLogsMixin",
    "CfnClusterMixinProps",
    "CfnClusterPropsMixin",
    "CfnFargateProfileMixinProps",
    "CfnFargateProfilePropsMixin",
    "CfnIdentityProviderConfigMixinProps",
    "CfnIdentityProviderConfigPropsMixin",
    "CfnNodegroupMixinProps",
    "CfnNodegroupPropsMixin",
    "CfnPodIdentityAssociationMixinProps",
    "CfnPodIdentityAssociationPropsMixin",
]

publication.publish()

def _typecheckingstub__1156c03c75ecb82707ffe98344bf14beccd767b3baea0ea988b41a4bcae836e0(
    *,
    access_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessEntryPropsMixin.AccessPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    kubernetes_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c97100c52aa262a44ac10663be49f670302b96d3e21036cac880569e887988(
    props: typing.Union[CfnAccessEntryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cae9fd0a4b7082ffdbd82b73b8cfbe63d188243a9e032bbaee7a61d60e05fd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c88f3c23ab18e4daeef256e5a6e7a31f80180d57f13ca5bc322f991df587888(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073f9428d5f81408532a02358f7aebf2621f9688b56530abcdae78fe8db0c005(
    *,
    access_scope: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccessEntryPropsMixin.AccessScopeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad647e620ef50a99475aae64b02046734b44aaaa0524fa3325feeecdb408f17(
    *,
    namespaces: typing.Optional[typing.Sequence[builtins.str]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce74297a0466688dc1bd80c3534de7e1052034a4be658f0f106a8e1fec3e7a40(
    *,
    addon_name: typing.Optional[builtins.str] = None,
    addon_version: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    configuration_values: typing.Optional[builtins.str] = None,
    namespace_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAddonPropsMixin.NamespaceConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    pod_identity_associations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAddonPropsMixin.PodIdentityAssociationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    preserve_on_delete: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resolve_conflicts: typing.Optional[builtins.str] = None,
    service_account_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc6db2e2c2b167fd1439ef52ccc426a4e56936e8e5890a4447a24562abe50d9(
    props: typing.Union[CfnAddonMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01d25519d08c4bb7ce5a80ed901db03403a7b35925984f8e707cf49e0228f2bb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ac0c66e104e010dc5a0d93f70a23497ce51693044accfd23818dd9cf8471a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eda9fe54e66a6780045bc879d8510e4e7caa9a76b87c5538fbd2ff6e0a9e6d9(
    *,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063b63afba958fb4c24a7358a691b11c722c8dee025b3096694e8736092950ce(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d01108725c81e0073efea146d54ea809de3889302fb72866c9b72e76295b5d9(
    *,
    capability_name: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.CapabilityConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delete_propagation_policy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eed663ca5d7f84d7dc9ac5906b2fcdb893198e3b67c5eaa1f1ffc93e23942655(
    props: typing.Union[CfnCapabilityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be9e16455e0c413d2bade4270b60add2e7013ede22b7ad2106b7198d5f74beb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd3e101b1ce07af649131bfaf29c6003f7c2f8480f78f9958cce4f7fa1059139(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c56d64eaa4a8e40468dfd88cf78066cd65db34b295bcf031db97bcb65d4151b(
    *,
    aws_idc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.AwsIdcProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
    network_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.NetworkAccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rbac_role_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.ArgoCdRoleMappingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    server_url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__011c506d5b317d0194c59e8916f995eddef76a2fb217ee6bbdf5c1c6e8903aae(
    *,
    identities: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.SsoIdentityProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d17311c70b31316d9e3457d61e651e50be01af9711468bfc9e3a1a2b28590b(
    *,
    idc_instance_arn: typing.Optional[builtins.str] = None,
    idc_managed_application_arn: typing.Optional[builtins.str] = None,
    idc_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c67107c054132e3fed460785cb46c34120f2f60fc3f627f302ff33ff6819f8d4(
    *,
    argo_cd: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCapabilityPropsMixin.ArgoCdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e857e219ccae5b0318790e68957cfe2e482a32892a6b9e4cb16fb76aed41122(
    *,
    vpce_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efc6fd1effc9db0da3c216e90c4b17d69a9e3c569869d4cf49c86a204fe1b0a0(
    *,
    id: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aecdb0debcd07a97068a632ba35400026d2754a7df3e68d4f5dbf7e5026bf749(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eec0074381fcadfacfde7bedc383fc9f44c33c1c62397dc0fe13a58f455c973(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7b12ae579e035fede9e9de8239ea591e7bc334c56c39ab067d49debd6201328(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c9a24d16d5427cd3848a5af518bbfe333b1db6f812ff8443aa0d839079052c(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a288934057859cc20cf92adbfd789937358a18ea3ae4d73ed37310c176e55d(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2932241cd1a057c81bfc0a6c89beb78d5f9d1a99794d17dfb833e64113c843(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e40f6ce14578d4d7e545d2bec39260439f2d6ecb8bf8ee7074a22534594eed9(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0582fdfef130b417ce8f731492aad637555f45cb40977a735a2c0a7279f1136(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff225116c19cb7efcfb1e90dae8557fa0ae2445d614dc75be2727537c5411ac(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e52d3a745ee872d211b863a8daa91da493e51e2eaad811818bbfb2c30b4253b(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dc46ca63c84c4d09de0a9c422860eab9a1040b651d2e4487e42962b083426e(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__287d15fdf0dcfd50d1b16077d3ba322ecd4ecc450fa176ee06aee2f13bb2d811(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d54377ef74f8513cd0d834d49d8ffcbe02caa072dfb89bea1d46f40f056f74(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d51028fbb5aacfbaf51b7c7834ba4699ede78ce14522f0639499cedaa98a6df(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dc79894f0f72f4ce665ae05d23fd826cf1ac150e1cf0dca53780d2bdbbe6f9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c08513e242c1780e7ecbdd194d599fee79f6b17677a2d80d72e204e233b222(
    *,
    access_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.AccessConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bootstrap_self_managed_addons: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    compute_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ComputeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    control_plane_scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ControlPlaneScalingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encryption_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.EncryptionConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    force: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kubernetes_network_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.KubernetesNetworkConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.LoggingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    outpost_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.OutpostConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    remote_network_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.RemoteNetworkConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resources_vpc_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ResourcesVpcConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    storage_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.StorageConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    upgrade_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.UpgradePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
    zonal_shift_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ZonalShiftConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b37fd968c8c81d6eab3abc583f2cc13f2d4cc77a30f570a1ee7a8354bde2039(
    props: typing.Union[CfnClusterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29f4b7e3ba272edc9da7f534cc78f2904390fa15e47d1b513cea011f148eecc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76738ce397597402ee937c79a408cc9c796c6eedef089e7aaf508418a464657(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abb00b84ce3203f8a120fb117cb95adbf035bdc2617143258d8cc3caaf885af(
    *,
    authentication_mode: typing.Optional[builtins.str] = None,
    bootstrap_cluster_creator_admin_permissions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f81d66301d0f7dfb9b17059e69aa3a836a29ca841aba02247f516aadd867223(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d51fb21d9b8ef39d179ee88e5a4127483fddaef6b1d07dfd652e175110c857(
    *,
    enabled_types: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.LoggingTypeConfigProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb86e2e5ea2041c2e25ae62cb6f90c1322d826206dd4e6facde8381ddc2913d(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    node_pools: typing.Optional[typing.Sequence[builtins.str]] = None,
    node_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1e2ee49a3b025004a061fb537c45bf5814cf3a952eeb89b5ef85dce6941c69(
    *,
    group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea548bfe5e1d0b226f0a90c93137fedc65b590bd26a02dab110d29ddeabf3c37(
    *,
    tier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787515c03fb09a0cccc860d57909fd312861c9d80bef1dcc5fb81fd32a284ab2(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10c1778da436313b56ddded82e658928b7e15f2f3f560c0ba5855067f5b0685f(
    *,
    provider: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ProviderProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006ca85255d20e7e283d1b5d958978dd9d4b7902b1d260f8626f697e35806bb8(
    *,
    elastic_load_balancing: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ElasticLoadBalancingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_family: typing.Optional[builtins.str] = None,
    service_ipv4_cidr: typing.Optional[builtins.str] = None,
    service_ipv6_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1db75ec99d84675799be45d3b59aa2294cf650265a9392cbf18dc2182bda71(
    *,
    cluster_logging: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ClusterLoggingProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e0cba62f31c9c7109b9c6ac1e1f6c5783d897ef6758ce1a6a18d6d84baec88(
    *,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2508ff07f331eafb9fe64eb2285d86d9f3f39befd121b3b00c893ef069acc7ba(
    *,
    control_plane_instance_type: typing.Optional[builtins.str] = None,
    control_plane_placement: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.ControlPlanePlacementProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outpost_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9adcb48ec0b0f285ab8c15a1a41cab9f7172f201b5458d767757cc65caa98de(
    *,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4d136219f8ecf9b184f86a7d9e2cedf0924d156be0ab7345bef5cc84535002c(
    *,
    remote_node_networks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.RemoteNodeNetworkProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    remote_pod_networks: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.RemotePodNetworkProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e3d61b80182ab467ad7ea941dec542b3dabb0ea7db3699123bfbea5b042dcf1(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc816bb9e439bd0298cff03e6952b6a9de99b103244c311c2cd1d92b9cacc146(
    *,
    cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff54a8f2aa57b7979791f97f83b9b2e701f9a505fc200fbd84e51462b788a32c(
    *,
    endpoint_private_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    endpoint_public_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    public_access_cidrs: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2672805e847c16309ec5d16e0d482794ecee22e86cbba45b2e06b9b08902fcd3(
    *,
    block_storage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnClusterPropsMixin.BlockStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bc1112e38b98cb6957135de8248c808db40f04a551ed17e13f5b0c1f9ee91c(
    *,
    support_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ec0199823bd491402bb518d9a047262a685cd120ad4990e161969ba471adfc(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69481e0b841a3d9c17b27989469dc34033e57273a809f69ab44fc1eefa4b4348(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
    fargate_profile_name: typing.Optional[builtins.str] = None,
    pod_execution_role_arn: typing.Optional[builtins.str] = None,
    selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFargateProfilePropsMixin.SelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90a889cc8d94b56a4a9f0f9221227024ec07e5682428bf5807c94d06f7f7bfad(
    props: typing.Union[CfnFargateProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a17af886f6e21c9b6d9587e1349af00ddbe1c366e9672652a4eaa16bef2719d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203e371936b1258c35ef14837b516e03c504270b1da3c192ec7fe9f5e42675dd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f7a1717305e0734af3f97f4f620db242aed66a4fbe7185ba434f7ddf79a042e(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc9dfe7583f0ae8fda51695f520444f8dd30c07ef6699cbea8f7e5ab78864c8(
    *,
    labels: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFargateProfilePropsMixin.LabelProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a6402788bc38ad1d5a84e9c63aff7b138a92de2030f890d4ab223aa66855d31(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
    identity_provider_config_name: typing.Optional[builtins.str] = None,
    oidc: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityProviderConfigPropsMixin.OidcIdentityProviderConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d53085b7b9d247eefafca01eb37636813543ac25ada04595ec6258d326504aa5(
    props: typing.Union[CfnIdentityProviderConfigMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5944ef352bbf891a3af900b5824e7ef4a962bb7ebe249ae16445d463d5deb4f1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f17805bf32093c5d618b2185f7f1df66931c8fae6b8cbb8b088a391259a66e6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d102f688d559941f7c3e0651b380e8bb3cedbc43a7f0ad690f9da3cabdb622bc(
    *,
    client_id: typing.Optional[builtins.str] = None,
    groups_claim: typing.Optional[builtins.str] = None,
    groups_prefix: typing.Optional[builtins.str] = None,
    issuer_url: typing.Optional[builtins.str] = None,
    required_claims: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnIdentityProviderConfigPropsMixin.RequiredClaimProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    username_claim: typing.Optional[builtins.str] = None,
    username_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690ee63e94cf912b8cfc99e4e8b0f97305d508cec2a2514c913555907869490c(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef0a142ce443af7b00b26ddf05201b2966ad1ea05e9b8dc03d472336f7e08e55(
    *,
    ami_type: typing.Optional[builtins.str] = None,
    capacity_type: typing.Optional[builtins.str] = None,
    cluster_name: typing.Optional[builtins.str] = None,
    disk_size: typing.Optional[jsii.Number] = None,
    force_update_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    labels: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.LaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    nodegroup_name: typing.Optional[builtins.str] = None,
    node_repair_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.NodeRepairConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    node_role: typing.Optional[builtins.str] = None,
    release_version: typing.Optional[builtins.str] = None,
    remote_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.RemoteAccessProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scaling_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.ScalingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subnets: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    taints: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.TaintProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    update_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.UpdateConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__057f2cd808c02688415746571246536821a421b1731e4c8f3b7b67e8b81caba6(
    props: typing.Union[CfnNodegroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858afb7a10cb7ff45e75e3d382eb242e0106bee45b3dcebed15c0584a8afc0ee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96c5d60afe31328fd8c735be89968b32c65cb341759062b1e80b7936a556fea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36cee528d1052c7ce04005d1159a427b1f69fe4f0fdf645e6c8a14720e0b6ac(
    *,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94836a82f4b000716de195407d972d5c627c6a1a6570ac2cbb0015d6c599263(
    *,
    min_repair_wait_time_mins: typing.Optional[jsii.Number] = None,
    node_monitoring_condition: typing.Optional[builtins.str] = None,
    node_unhealthy_reason: typing.Optional[builtins.str] = None,
    repair_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c4bca4634996e40c842517ab9ef6a98a5e23339d8a099c7aaca9095eb09ef24(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    max_parallel_nodes_repaired_count: typing.Optional[jsii.Number] = None,
    max_parallel_nodes_repaired_percentage: typing.Optional[jsii.Number] = None,
    max_unhealthy_node_threshold_count: typing.Optional[jsii.Number] = None,
    max_unhealthy_node_threshold_percentage: typing.Optional[jsii.Number] = None,
    node_repair_config_overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnNodegroupPropsMixin.NodeRepairConfigOverridesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5edc1eb0f53df48c00447fc31c0e68d112367c02d295fb991dbd452f7478bd1f(
    *,
    ec2_ssh_key: typing.Optional[builtins.str] = None,
    source_security_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8727d4084fa5ce10c520a48a963a3668d23b7c25df1ff9d7ffd2e9b898d15ae(
    *,
    desired_size: typing.Optional[jsii.Number] = None,
    max_size: typing.Optional[jsii.Number] = None,
    min_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712dbc410ae98ac8d544a9e6cf4839d71a0a357a350df69df951a804bd44d263(
    *,
    effect: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeefc9f8994774a62d4a08efb5f2c485724aa74f8560295369ad32358fe2faf7(
    *,
    max_unavailable: typing.Optional[jsii.Number] = None,
    max_unavailable_percentage: typing.Optional[jsii.Number] = None,
    update_strategy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb5898782698aebfa9c055c02192df0552b4a7d7519cd2249c867204e93d6236(
    *,
    cluster_name: typing.Optional[builtins.str] = None,
    disable_session_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    namespace: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    service_account: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc6ef39db082ca55da9ac28bdfe0ca2bb09eb2b5222ad338344c892ad20e779d(
    props: typing.Union[CfnPodIdentityAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70629ec0511c50d1dd7a804bc59f5c26ffc451559abb8619095e49201b1c42eb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf607ba52abd329900a6c5bb0642eeb876b16274e01445a5e4a39dd060b007e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
