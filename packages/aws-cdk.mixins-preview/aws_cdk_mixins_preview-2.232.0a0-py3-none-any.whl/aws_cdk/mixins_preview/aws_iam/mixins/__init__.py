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
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnAccessKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={"serial": "serial", "status": "status", "user_name": "userName"},
)
class CfnAccessKeyMixinProps:
    def __init__(
        self,
        *,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAccessKeyPropsMixin.

        :param serial: This value is specific to CloudFormation and can only be *incremented* . Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.
        :param status: The status of the access key. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
        :param user_name: The name of the IAM user that the new key will belong to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-accesskey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_access_key_mixin_props = iam_mixins.CfnAccessKeyMixinProps(
                serial=123,
                status="status",
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667fb2d6c96b48768dd9b15d5927d81bd02803cc90d2a71e9064118a3a8c80f8)
            check_type(argname="argument serial", value=serial, expected_type=type_hints["serial"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if serial is not None:
            self._values["serial"] = serial
        if status is not None:
            self._values["status"] = status
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        '''This value is specific to CloudFormation and can only be *incremented* .

        Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-accesskey.html#cfn-iam-accesskey-serial
        '''
        result = self._values.get("serial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the access key.

        ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-accesskey.html#cfn-iam-accesskey-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM user that the new key will belong to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-accesskey.html#cfn-iam-accesskey-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccessKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnAccessKeyPropsMixin",
):
    '''Creates a new AWS secret access key and corresponding AWS access key ID for the specified user.

    The default status for new keys is ``Active`` .

    For information about quotas on the number of keys you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       To ensure the security of your AWS account , the secret access key is accessible only during key and user creation. You must save the key (for example, in a text file) if you want to be able to access it again. If a secret key is lost, you can rotate access keys by increasing the value of the ``serial`` property.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-accesskey.html
    :cloudformationResource: AWS::IAM::AccessKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_access_key_props_mixin = iam_mixins.CfnAccessKeyPropsMixin(iam_mixins.CfnAccessKeyMixinProps(
            serial=123,
            status="status",
            user_name="userName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccessKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::AccessKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07916fa3109989a36f3a892df0eb08aec93ef8fcdde52bc1269773a33771765a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__89a586a279a8f93d02f0c531685b044e395e465a7491e930f58eef13995c99b0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d6ac2bc1f33507cf035f2decf8c2a9f18b224d9420e1e0d95677f579d9145c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccessKeyMixinProps:
        return typing.cast(CfnAccessKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "managed_policy_arns": "managedPolicyArns",
        "path": "path",
        "policies": "policies",
    },
)
class CfnGroupMixinProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnGroupPropsMixin.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnGroupPropsMixin.

        :param group_name: The name of the group to create. Do not include the path in this value. The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the group name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param managed_policy_arns: The Amazon Resource Name (ARN) of the IAM policy you want to attach. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM group. To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ . .. epigraph:: The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_group_mixin_props = iam_mixins.CfnGroupMixinProps(
                group_name="groupName",
                managed_policy_arns=["managedPolicyArns"],
                path="path",
                policies=[iam_mixins.CfnGroupPropsMixin.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6341b4217cfcb11835888db05678654be3f5a9bb73f5a0fcedcbb61b6226e500)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None:
            self._values["path"] = path
        if policies is not None:
            self._values["policies"] = policies

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to create. Do not include the path in this value.

        The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the group name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-group.html#cfn-iam-group-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-group.html#cfn-iam-group-managedpolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-group.html#cfn-iam-group-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.PolicyProperty"]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM group.

        To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ .
        .. epigraph::

           The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-group.html#cfn-iam-group-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnGroupPropsMixin.PolicyProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnGroupPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "policy_document": "policyDocument",
        "policy_name": "policyName",
    },
)
class CfnGroupPolicyMixinProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
        policy_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnGroupPolicyPropsMixin.

        :param group_name: The name of the group to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.
        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ) - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-grouppolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_group_policy_mixin_props = iam_mixins.CfnGroupPolicyMixinProps(
                group_name="groupName",
                policy_document=policy_document,
                policy_name="policyName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837a056370eb6710c1cb2b9ccabcd0346e68e4ab54057752a96d3adbb57f6888)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-grouppolicy.html#cfn-iam-grouppolicy-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` )
        - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-grouppolicy.html#cfn-iam-grouppolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-grouppolicy.html#cfn-iam-grouppolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnGroupPolicyPropsMixin",
):
    '''Adds or updates an inline policy document that is embedded in the specified IAM group.

    A group can also have managed policies attached to it. To attach a managed policy to a group, use ```AWS::IAM::Group`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html>`_ . To create a new managed policy, use ```AWS::IAM::ManagedPolicy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html>`_ . For information about policies, see `Managed policies and inline policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    For information about the maximum number of inline policies that you can embed in a group, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-grouppolicy.html
    :cloudformationResource: AWS::IAM::GroupPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_group_policy_props_mixin = iam_mixins.CfnGroupPolicyPropsMixin(iam_mixins.CfnGroupPolicyMixinProps(
            group_name="groupName",
            policy_document=policy_document,
            policy_name="policyName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnGroupPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::GroupPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d3a83f4a758dc739104e052eb3e3b42c87bad2e761665a8ee01ec4f6efa4fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6999a40dd0a3f157698d3d5b23ed440893ff488bc288a20376ea058e8a10708)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba625031af088706b427d35d2bfb07581ca5268cb63e6c5e7235e189b8f3a75e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnGroupPolicyMixinProps:
        return typing.cast(CfnGroupPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnGroupPropsMixin",
):
    '''Creates a new group.

    For information about the number of groups you can create, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-group.html
    :cloudformationResource: AWS::IAM::Group
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_group_props_mixin = iam_mixins.CfnGroupPropsMixin(iam_mixins.CfnGroupMixinProps(
            group_name="groupName",
            managed_policy_arns=["managedPolicyArns"],
            path="path",
            policies=[iam_mixins.CfnGroupPropsMixin.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )]
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
        '''Create a mixin to apply properties to ``AWS::IAM::Group``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77e89a1600a26aca07b0f22e60962a2da9f29dbd772a9a0a343bf4e0d43046c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b858c5ef3a5debdf950a379e2682d25b3b35b142cb62c18649f30868a08afee)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__261a8d0eaa1b8c112ac487d955a6db62f112a6578f860bcdfbd26047eca63dcc)
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

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnGroupPropsMixin.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The policy document.
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
                
                # policy_document: Any
                
                policy_property = iam_mixins.CfnGroupPropsMixin.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__864da8deb879ce026dd3b82315320ff3830029d42093034ef06e7be49bad1d84)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_document is not None:
                self._values["policy_document"] = policy_document
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The policy document.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group-policy.html#cfn-iam-group-policy-policydocument
            '''
            result = self._values.get("policy_document")
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The friendly name (not ARN) identifying the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group-policy.html#cfn-iam-group-policy-policyname
            '''
            result = self._values.get("policy_name")
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
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnInstanceProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_profile_name": "instanceProfileName",
        "path": "path",
        "roles": "roles",
    },
)
class CfnInstanceProfileMixinProps:
    def __init__(
        self,
        *,
        instance_profile_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnInstanceProfilePropsMixin.

        :param instance_profile_name: The name of the instance profile to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param path: The path to the instance profile. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param roles: The name of the role to associate with the instance profile. Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_instance_profile_mixin_props = iam_mixins.CfnInstanceProfileMixinProps(
                instance_profile_name="instanceProfileName",
                path="path",
                roles=["roles"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6884b55f7939fd1fcf475cdc70ed0e420c7a629eb5dd51c07aaae550108248)
            check_type(argname="argument instance_profile_name", value=instance_profile_name, expected_type=type_hints["instance_profile_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_profile_name is not None:
            self._values["instance_profile_name"] = instance_profile_name
        if path is not None:
            self._values["path"] = path
        if roles is not None:
            self._values["roles"] = roles

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance profile to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        '''
        result = self._values.get("instance_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the instance profile.

        For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the role to associate with the instance profile.

        Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnInstanceProfilePropsMixin",
):
    '''Creates a new instance profile. For information about instance profiles, see `Using instance profiles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html>`_ .

    For information about the number of instance profiles you can create, see `IAM object quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
    :cloudformationResource: AWS::IAM::InstanceProfile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_instance_profile_props_mixin = iam_mixins.CfnInstanceProfilePropsMixin(iam_mixins.CfnInstanceProfileMixinProps(
            instance_profile_name="instanceProfileName",
            path="path",
            roles=["roles"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::InstanceProfile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__390090c2cdca8076013d5a76b382bc6435e8736be7138cd4cc5c3e5121d2b6f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__081bb370a7d202808ce1125b2b53afc55ba126142df63d135254ada26514bd9b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d30690369ff9bce316cb37b2d8d7852b72abb87ad38b4cfb3740881ccce8a5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceProfileMixinProps:
        return typing.cast(CfnInstanceProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnManagedPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "groups": "groups",
        "managed_policy_name": "managedPolicyName",
        "path": "path",
        "policy_document": "policyDocument",
        "roles": "roles",
        "users": "users",
    },
)
class CfnManagedPolicyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        policy_document: typing.Any = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnManagedPolicyPropsMixin.

        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param groups: The name (friendly name, not ARN) of the group to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param managed_policy_name: The friendly name of the policy. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: You cannot use an asterisk (*) in the path name. Default: - "/"
        :param policy_document: The JSON policy document that you want to use as the content for the new policy. You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ . To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* . The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ) - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )
        :param roles: The name (friendly name, not ARN) of the role to attach the policy to. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name (friendly name, not ARN) of the IAM user to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_managed_policy_mixin_props = iam_mixins.CfnManagedPolicyMixinProps(
                description="description",
                groups=["groups"],
                managed_policy_name="managedPolicyName",
                path="path",
                policy_document=policy_document,
                roles=["roles"],
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3524be4c27fd6acf63e3d44693b4bfd6652afb7288c1d0bae300df39d2fb3af)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if groups is not None:
            self._values["groups"] = groups
        if managed_policy_name is not None:
            self._values["managed_policy_name"] = managed_policy_name
        if path is not None:
            self._values["path"] = path
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A friendly description of the policy.

        Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables."

        The policy description is immutable. After a value is assigned, it cannot be changed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the group to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the policy.

        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        '''
        result = self._values.get("managed_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           You cannot use an asterisk (*) in the path name.

        :default: - "/"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The JSON policy document that you want to use as the content for the new policy.

        You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ .

        To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* .

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` )
        - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the role to attach the policy to.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the IAM user to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnManagedPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnManagedPolicyPropsMixin",
):
    '''Creates a new managed policy for your AWS account .

    This operation creates a policy version with a version identifier of ``v1`` and sets v1 as the policy's default version. For more information about policy versions, see `Versioning for managed policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`_ in the *IAM User Guide* .

    As a best practice, you can validate your IAM policies. To learn more, see `Validating IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_policy-validator.html>`_ in the *IAM User Guide* .

    For more information about managed policies in general, see `Managed policies and inline policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
    :cloudformationResource: AWS::IAM::ManagedPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_managed_policy_props_mixin = iam_mixins.CfnManagedPolicyPropsMixin(iam_mixins.CfnManagedPolicyMixinProps(
            description="description",
            groups=["groups"],
            managed_policy_name="managedPolicyName",
            path="path",
            policy_document=policy_document,
            roles=["roles"],
            users=["users"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnManagedPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::ManagedPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a84943610be47cc0cffebe3d2f864698d827edcd744212b05c589d7a72b91bd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc0cd3838e3e8172eaea32b78073426bc2002a1c0baff8a5ae96c8e0ceec0434)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e78de50c8c117b2faf0b0e1b0a9b8c53e59bc3259b9c681fc6f73b12cbd124)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnManagedPolicyMixinProps:
        return typing.cast(CfnManagedPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnOIDCProviderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "client_id_list": "clientIdList",
        "tags": "tags",
        "thumbprint_list": "thumbprintList",
        "url": "url",
    },
)
class CfnOIDCProviderMixinProps:
    def __init__(
        self,
        *,
        client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        thumbprint_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnOIDCProviderPropsMixin.

        :param client_id_list: A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param tags: A list of tags that are attached to the specified IAM OIDC provider. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        :param thumbprint_list: A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ . This property is optional. If it is not included, IAM will retrieve and use the top intermediate certificate authority (CA) thumbprint of the OpenID Connect identity provider server certificate.
        :param url: The URL that the IAM OIDC provider resource object is associated with. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_oIDCProvider_mixin_props = iam_mixins.CfnOIDCProviderMixinProps(
                client_id_list=["clientIdList"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                thumbprint_list=["thumbprintList"],
                url="url"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b265bbf0cc0a691f2d8f7405a5fe74d27cc56a0bd1699b63a6455bed8ef367)
            check_type(argname="argument client_id_list", value=client_id_list, expected_type=type_hints["client_id_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument thumbprint_list", value=thumbprint_list, expected_type=type_hints["thumbprint_list"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_id_list is not None:
            self._values["client_id_list"] = client_id_list
        if tags is not None:
            self._values["tags"] = tags
        if thumbprint_list is not None:
            self._values["thumbprint_list"] = thumbprint_list
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def client_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-clientidlist
        '''
        result = self._values.get("client_id_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that are attached to the specified IAM OIDC provider.

        The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def thumbprint_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        This property is optional. If it is not included, IAM will retrieve and use the top intermediate certificate authority (CA) thumbprint of the OpenID Connect identity provider server certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-thumbprintlist
        '''
        result = self._values.get("thumbprint_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL that the IAM OIDC provider resource object is associated with.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOIDCProviderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnOIDCProviderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnOIDCProviderPropsMixin",
):
    '''Creates or updates an IAM entity to describe an identity provider (IdP) that supports `OpenID Connect (OIDC) <https://docs.aws.amazon.com/http://openid.net/connect/>`_ .

    The OIDC provider that you create with this operation can be used as a principal in a role's trust policy. Such a policy establishes a trust relationship between AWS and the OIDC provider.

    When you create the IAM OIDC provider, you specify the following:

    - The URL of the OIDC identity provider (IdP) to trust
    - A list of client IDs (also known as audiences) that identify the application or applications that are allowed to authenticate using the OIDC provider
    - A list of tags that are attached to the specified IAM OIDC provider
    - A list of thumbprints of one or more server certificates that the IdP uses

    You get all of this information from the OIDC IdP that you want to use to access AWS .

    When you update the IAM OIDC provider, you specify the following:

    - The URL of the OIDC identity provider (IdP) to trust
    - A list of client IDs (also known as audiences) that replaces the existing list of client IDs associated with the OIDC IdP
    - A list of tags that replaces the existing list of tags attached to the specified IAM OIDC provider
    - A list of thumbprints that replaces the existing list of server certificates thumbprints that the IdP uses

    .. epigraph::

       The trust for the OIDC provider is derived from the IAM provider that this operation creates. Therefore, it is best to limit access to the `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ operation to highly privileged users.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html
    :cloudformationResource: AWS::IAM::OIDCProvider
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_oIDCProvider_props_mixin = iam_mixins.CfnOIDCProviderPropsMixin(iam_mixins.CfnOIDCProviderMixinProps(
            client_id_list=["clientIdList"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            thumbprint_list=["thumbprintList"],
            url="url"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnOIDCProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::OIDCProvider``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9f793a34480fc75de979bb4189dd08e44888c3dd12f643d907d9c31bef1ff5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14db8b303f0d78d942464f08ef50368eb114424f5251a2203cbaaef8e855c5e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__152f42bdb6756442608b1e051426e5847636af9c3cbaeaaafe60a6fc77d31950)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnOIDCProviderMixinProps:
        return typing.cast(CfnOIDCProviderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "roles": "roles",
        "users": "users",
    },
)
class CfnPolicyMixinProps:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        policy_document: typing.Any = None,
        policy_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnPolicyPropsMixin.

        :param groups: The name of the group to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.
        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ) - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param roles: The name of the role to associate the policy with. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name of the user to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_policy_mixin_props = iam_mixins.CfnPolicyMixinProps(
                groups=["groups"],
                policy_document=policy_document,
                policy_name="policyName",
                roles=["roles"],
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f655b82f9f8a8ec7551016bc2cbe1ad396184561fe01463aed29234d80d68a2)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the group to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` )
        - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the role to associate the policy with.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the user to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnPolicyPropsMixin",
):
    '''Adds or updates an inline policy document that is embedded in the specified IAM group, user or role.

    An IAM user can also have a managed policy attached to it. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    The Groups, Roles, and Users properties are optional. However, you must specify at least one of these properties.

    For information about policy documents, see `Creating IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html>`_ in the *IAM User Guide* .

    For information about limits on the number of inline policies that you can embed in an identity, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
    .. epigraph::

       This resource does not support `drift detection <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html>`_ . The following inline policy resource types support drift detection:

       - ```AWS::IAM::GroupPolicy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-grouppolicy.html>`_
       - ```AWS::IAM::RolePolicy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html>`_
       - ```AWS::IAM::UserPolicy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-userpolicy.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
    :cloudformationResource: AWS::IAM::Policy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_policy_props_mixin = iam_mixins.CfnPolicyPropsMixin(iam_mixins.CfnPolicyMixinProps(
            groups=["groups"],
            policy_document=policy_document,
            policy_name="policyName",
            roles=["roles"],
            users=["users"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::Policy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23ebf00b12c9fbf58506dbb43a06ee39402e9df79b5331141cd60944f11ef58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0abff2b1f74e686b74e548a58f4c63fcdd1c7c6d37ec291796401a20b4beda23)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6734f6b7a0eb6934a1a1c9088ab4ef286fae382568415c93ef5953a174165465)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPolicyMixinProps:
        return typing.cast(CfnPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnRoleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role_policy_document": "assumeRolePolicyDocument",
        "description": "description",
        "managed_policy_arns": "managedPolicyArns",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "role_name": "roleName",
        "tags": "tags",
    },
)
class CfnRoleMixinProps:
    def __init__(
        self,
        *,
        assume_role_policy_document: typing.Any = None,
        description: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_session_duration: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRolePropsMixin.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        role_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRolePropsMixin.

        :param assume_role_policy_document: The trust policy that is associated with this role. Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .
        :param description: A description of the role that you provide.
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param max_session_duration: The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours. Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .
        :param path: The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. Default: - "/"
        :param permissions_boundary: The ARN of the policy used to set the permissions boundary for the role. For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM role. When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ . A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* . For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* . .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param role_name: A name for the IAM role, up to 64 characters in length. For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* . This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1". If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the role name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param tags: A list of tags that are attached to the role. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # assume_role_policy_document: Any
            # policy_document: Any
            
            cfn_role_mixin_props = iam_mixins.CfnRoleMixinProps(
                assume_role_policy_document=assume_role_policy_document,
                description="description",
                managed_policy_arns=["managedPolicyArns"],
                max_session_duration=123,
                path="path",
                permissions_boundary="permissionsBoundary",
                policies=[iam_mixins.CfnRolePropsMixin.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )],
                role_name="roleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fe5a414314e1714619916d29c1278900a88d9e7301bad1bda1363f8cb89662)
            check_type(argname="argument assume_role_policy_document", value=assume_role_policy_document, expected_type=type_hints["assume_role_policy_document"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assume_role_policy_document is not None:
            self._values["assume_role_policy_document"] = assume_role_policy_document
        if description is not None:
            self._values["description"] = description
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if role_name is not None:
            self._values["role_name"] = role_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        '''The trust policy that is associated with this role.

        Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        '''
        result = self._values.get("assume_role_policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role that you provide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managedpolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        '''The maximum session duration (in seconds) that you want to set for the specified role.

        If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours.

        Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :default: - "/"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the policy used to set the permissions boundary for the role.

        For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRolePropsMixin.PolicyProperty"]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM role.

        When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ .

        A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

        For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRolePropsMixin.PolicyProperty"]]]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role, up to 64 characters in length.

        For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* .

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1".

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the role name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that are attached to the role.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnRolePolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "role_name": "roleName",
    },
)
class CfnRolePolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        policy_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRolePolicyPropsMixin.

        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ) - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param role_name: The name of the role to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_role_policy_mixin_props = iam_mixins.CfnRolePolicyMixinProps(
                policy_document=policy_document,
                policy_name="policyName",
                role_name="roleName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd037386f28fd04dae74c903c15e3af633dac66fbfa4b51b427ff11cad486501)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` )
        - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html#cfn-iam-rolepolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html#cfn-iam-rolepolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the role to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html#cfn-iam-rolepolicy-rolename
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRolePolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRolePolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnRolePolicyPropsMixin",
):
    '''Adds or updates an inline policy document that is embedded in the specified IAM role.

    When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role, using ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ . You can update a role's trust policy using ```UpdateAssumeRolePolicy`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_UpdateAssumeRolePolicy.html>`_ . For information about roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ in the *IAM User Guide* .

    A role can also have a managed policy attached to it. To attach a managed policy to a role, use ```AWS::IAM::Role`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html>`_ . To create a new managed policy, use ```AWS::IAM::ManagedPolicy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html>`_ . For information about policies, see `Managed policies and inline policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    For information about the maximum number of inline policies that you can embed with a role, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-rolepolicy.html
    :cloudformationResource: AWS::IAM::RolePolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_role_policy_props_mixin = iam_mixins.CfnRolePolicyPropsMixin(iam_mixins.CfnRolePolicyMixinProps(
            policy_document=policy_document,
            policy_name="policyName",
            role_name="roleName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRolePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::RolePolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd6f6b43538cb8b8670aa60e414a056e3ee644c12a6c64b428b4d2d807ab14c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37ce4b10eb7416c2f0f598bcf5365c2307db3a13ae7a8944f62c349590fec2ff)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c093f24e631319954cdb64208be7ff7e919167e958ad6aaa5bcc8e1d7bcb95)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRolePolicyMixinProps:
        return typing.cast(CfnRolePolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnRolePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnRolePropsMixin",
):
    '''Creates a new role for your AWS account .

    For more information about roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html>`_ in the *IAM User Guide* . For information about quotas for role names and the number of roles you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    :cloudformationResource: AWS::IAM::Role
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # assume_role_policy_document: Any
        # policy_document: Any
        
        cfn_role_props_mixin = iam_mixins.CfnRolePropsMixin(iam_mixins.CfnRoleMixinProps(
            assume_role_policy_document=assume_role_policy_document,
            description="description",
            managed_policy_arns=["managedPolicyArns"],
            max_session_duration=123,
            path="path",
            permissions_boundary="permissionsBoundary",
            policies=[iam_mixins.CfnRolePropsMixin.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )],
            role_name="roleName",
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
        props: typing.Union[CfnRoleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::Role``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02affbee49162438343b52598a1b37e34c1c7fa883f04c0a2dd4273fb561513)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fdef70c482053898554d9bb4e3d6ee43a7d3b508ea906ee8f7935833d7a308a3)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c7bbc2ff7f5e6574f68a7a682bc9314e983bf8b5cd5fb55b5a7bdf6cff11c2d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRoleMixinProps:
        return typing.cast(CfnRoleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnRolePropsMixin.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, refer to `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The entire contents of the policy that defines permissions. For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
                
                # policy_document: Any
                
                policy_property = iam_mixins.CfnRolePropsMixin.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70d42a5b06521c8ff7e02a033c136a54907f481b8278c26c8ae439012f0bc853)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_document is not None:
                self._values["policy_document"] = policy_document
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The entire contents of the policy that defines permissions.

            For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html#cfn-iam-role-policy-policydocument
            '''
            result = self._values.get("policy_document")
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The friendly name (not ARN) identifying the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-role-policy.html#cfn-iam-role-policy-policyname
            '''
            result = self._values.get("policy_name")
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
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnSAMLProviderMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "add_private_key": "addPrivateKey",
        "assertion_encryption_mode": "assertionEncryptionMode",
        "name": "name",
        "private_key_list": "privateKeyList",
        "remove_private_key": "removePrivateKey",
        "saml_metadata_document": "samlMetadataDocument",
        "tags": "tags",
    },
)
class CfnSAMLProviderMixinProps:
    def __init__(
        self,
        *,
        add_private_key: typing.Optional[builtins.str] = None,
        assertion_encryption_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        private_key_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        remove_private_key: typing.Optional[builtins.str] = None,
        saml_metadata_document: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSAMLProviderPropsMixin.

        :param add_private_key: Specifies the new private key from your external identity provider. The private key must be a .pem file that uses AES-GCM or AES-CBC encryption algorithm to decrypt SAML assertions.
        :param assertion_encryption_mode: Specifies the encryption setting for the SAML provider.
        :param name: The name of the provider to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param private_key_list: The private key metadata for the SAML provider.
        :param remove_private_key: The Key ID of the private key to remove.
        :param saml_metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP. For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*
        :param tags: A list of tags that you want to attach to the new IAM SAML provider. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_sAMLProvider_mixin_props = iam_mixins.CfnSAMLProviderMixinProps(
                add_private_key="addPrivateKey",
                assertion_encryption_mode="assertionEncryptionMode",
                name="name",
                private_key_list=[iam_mixins.CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty(
                    key_id="keyId",
                    timestamp="timestamp"
                )],
                remove_private_key="removePrivateKey",
                saml_metadata_document="samlMetadataDocument",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec2b5a7aec047b3c3c150d76f3cca4a001e01269ff445a202768e53812decc9)
            check_type(argname="argument add_private_key", value=add_private_key, expected_type=type_hints["add_private_key"])
            check_type(argname="argument assertion_encryption_mode", value=assertion_encryption_mode, expected_type=type_hints["assertion_encryption_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument private_key_list", value=private_key_list, expected_type=type_hints["private_key_list"])
            check_type(argname="argument remove_private_key", value=remove_private_key, expected_type=type_hints["remove_private_key"])
            check_type(argname="argument saml_metadata_document", value=saml_metadata_document, expected_type=type_hints["saml_metadata_document"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_private_key is not None:
            self._values["add_private_key"] = add_private_key
        if assertion_encryption_mode is not None:
            self._values["assertion_encryption_mode"] = assertion_encryption_mode
        if name is not None:
            self._values["name"] = name
        if private_key_list is not None:
            self._values["private_key_list"] = private_key_list
        if remove_private_key is not None:
            self._values["remove_private_key"] = remove_private_key
        if saml_metadata_document is not None:
            self._values["saml_metadata_document"] = saml_metadata_document
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def add_private_key(self) -> typing.Optional[builtins.str]:
        '''Specifies the new private key from your external identity provider.

        The private key must be a .pem file that uses AES-GCM or AES-CBC encryption algorithm to decrypt SAML assertions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-addprivatekey
        '''
        result = self._values.get("add_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assertion_encryption_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies the encryption setting for the SAML provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-assertionencryptionmode
        '''
        result = self._values.get("assertion_encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the provider to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty"]]]]:
        '''The private key metadata for the SAML provider.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-privatekeylist
        '''
        result = self._values.get("private_key_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty"]]]], result)

    @builtins.property
    def remove_private_key(self) -> typing.Optional[builtins.str]:
        '''The Key ID of the private key to remove.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-removeprivatekey
        '''
        result = self._values.get("remove_private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def saml_metadata_document(self) -> typing.Optional[builtins.str]:
        '''An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.

        For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-samlmetadatadocument
        '''
        result = self._values.get("saml_metadata_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the new IAM SAML provider.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSAMLProviderMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSAMLProviderPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnSAMLProviderPropsMixin",
):
    '''Creates an IAM resource that describes an identity provider (IdP) that supports SAML 2.0.

    The SAML provider resource that you create with this operation can be used as a principal in an IAM role's trust policy. Such a policy can enable federated users who sign in using the SAML IdP to assume the role. You can create an IAM role that supports Web-based single sign-on (SSO) to the AWS Management Console or one that supports API access to AWS .

    When you create the SAML provider resource, you upload a SAML metadata document that you get from your IdP. That document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that the IdP sends. You must generate the metadata document using the identity management software that is used as your organization's IdP.
    .. epigraph::

       This operation requires `Signature Version 4 <https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`_ .

    For more information, see `Enabling SAML 2.0 federated users to access the AWS Management Console <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-saml.html>`_ and `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html
    :cloudformationResource: AWS::IAM::SAMLProvider
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_sAMLProvider_props_mixin = iam_mixins.CfnSAMLProviderPropsMixin(iam_mixins.CfnSAMLProviderMixinProps(
            add_private_key="addPrivateKey",
            assertion_encryption_mode="assertionEncryptionMode",
            name="name",
            private_key_list=[iam_mixins.CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty(
                key_id="keyId",
                timestamp="timestamp"
            )],
            remove_private_key="removePrivateKey",
            saml_metadata_document="samlMetadataDocument",
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
        props: typing.Union[CfnSAMLProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::SAMLProvider``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc486a0022f6cfe1bab76035c3dc9a3236a6237e53f1fc32dc3ee12bf1f5fe6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ced242a2067981f4f4af2c45ca61b8d5331fe1edc35539337cb0daedf33e748e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2723cc84aaf6d3f40f5048734082e87ffc51b40fb1d29c78324d747f6d2209e8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSAMLProviderMixinProps:
        return typing.cast(CfnSAMLProviderMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty",
        jsii_struct_bases=[],
        name_mapping={"key_id": "keyId", "timestamp": "timestamp"},
    )
    class SAMLPrivateKeyProperty:
        def __init__(
            self,
            *,
            key_id: typing.Optional[builtins.str] = None,
            timestamp: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains the private keys for the SAML provider.

            This data type is used as a response element in the `GetSAMLProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_GetSAMLProvider.html>`_ operation.

            :param key_id: The unique identifier for the SAML private key.
            :param timestamp: The date and time, in `ISO 8601 date-time <https://docs.aws.amazon.com/http://www.iso.org/iso/iso8601>`_ format, when the private key was uploaded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-samlprovider-samlprivatekey.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
                
                s_aMLPrivate_key_property = iam_mixins.CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty(
                    key_id="keyId",
                    timestamp="timestamp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd8097571e82d554193680a8548df8d7e34a2a72e0f1385787b9c759090dff9c)
                check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
                check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_id is not None:
                self._values["key_id"] = key_id
            if timestamp is not None:
                self._values["timestamp"] = timestamp

        @builtins.property
        def key_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the SAML private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-samlprovider-samlprivatekey.html#cfn-iam-samlprovider-samlprivatekey-keyid
            '''
            result = self._values.get("key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timestamp(self) -> typing.Optional[builtins.str]:
            '''The date and time, in `ISO 8601 date-time <https://docs.aws.amazon.com/http://www.iso.org/iso/iso8601>`_ format, when the private key was uploaded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-samlprovider-samlprivatekey.html#cfn-iam-samlprovider-samlprivatekey-timestamp
            '''
            result = self._values.get("timestamp")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SAMLPrivateKeyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnServerCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_body": "certificateBody",
        "certificate_chain": "certificateChain",
        "path": "path",
        "private_key": "privateKey",
        "server_certificate_name": "serverCertificateName",
        "tags": "tags",
    },
)
class CfnServerCertificateMixinProps:
    def __init__(
        self,
        *,
        certificate_body: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        server_certificate_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServerCertificatePropsMixin.

        :param certificate_body: The contents of the public key certificate.
        :param certificate_chain: The contents of the public key certificate chain.
        :param path: The path for the server certificate. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).
        :param private_key: The contents of the private key in PEM-encoded format. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ) - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )
        :param server_certificate_name: The name for the server certificate. Do not include the path in this value. The name of the certificate cannot contain any spaces. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that are attached to the server certificate. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_server_certificate_mixin_props = iam_mixins.CfnServerCertificateMixinProps(
                certificate_body="certificateBody",
                certificate_chain="certificateChain",
                path="path",
                private_key="privateKey",
                server_certificate_name="serverCertificateName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df438f7b5bbf807e75e1f4f55e218eb43a6b8d39ce84958c7cf7e9200e16198)
            check_type(argname="argument certificate_body", value=certificate_body, expected_type=type_hints["certificate_body"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument server_certificate_name", value=server_certificate_name, expected_type=type_hints["server_certificate_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_body is not None:
            self._values["certificate_body"] = certificate_body
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if path is not None:
            self._values["path"] = path
        if private_key is not None:
            self._values["private_key"] = private_key
        if server_certificate_name is not None:
            self._values["server_certificate_name"] = server_certificate_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_body(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatebody
        '''
        result = self._values.get("certificate_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate chain.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the server certificate.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The contents of the private key in PEM-encoded format.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` )
        - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name for the server certificate.

        Do not include the path in this value. The name of the certificate cannot contain any spaces.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-servercertificatename
        '''
        result = self._values.get("server_certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that are attached to the server certificate.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServerCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnServerCertificatePropsMixin",
):
    '''Uploads a server certificate entity for the AWS account .

    The server certificate entity includes a public key certificate, a private key, and an optional certificate chain, which should all be PEM-encoded.

    We recommend that you use `Certificate Manager <https://docs.aws.amazon.com/acm/>`_ to provision, manage, and deploy your server certificates. With ACM you can request a certificate, deploy it to AWS resources, and let ACM handle certificate renewals for you. Certificates provided by ACM are free. For more information about using ACM, see the `Certificate Manager User Guide <https://docs.aws.amazon.com/acm/latest/userguide/>`_ .

    For more information about working with server certificates, see `Working with server certificates <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`_ in the *IAM User Guide* . This topic includes a list of AWS services that can use the server certificates that you manage with IAM.

    For information about the number of server certificates you can upload, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       Because the body of the public key certificate, private key, and the certificate chain can be large, you should use POST rather than GET when calling ``UploadServerCertificate`` . For information about setting up signatures and authorization through the API, see `Signing AWS API requests <https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html>`_ in the *AWS General Reference* . For general information about using the Query API with IAM, see `Calling the API by making HTTP query requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/programming.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html
    :cloudformationResource: AWS::IAM::ServerCertificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_server_certificate_props_mixin = iam_mixins.CfnServerCertificatePropsMixin(iam_mixins.CfnServerCertificateMixinProps(
            certificate_body="certificateBody",
            certificate_chain="certificateChain",
            path="path",
            private_key="privateKey",
            server_certificate_name="serverCertificateName",
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
        props: typing.Union[CfnServerCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::ServerCertificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__799173fb948634e8b331c3cbe1106373b9c262c3d349ea4efcbe3df02722ec7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c65534e25e57a5966e23550839366c509b080a1ec028a14ef6cf7eccb9e0d36)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebfbb94e5b451f13e78320a473f95e1079b542498633b26d2c5d6517ae0f8af0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServerCertificateMixinProps:
        return typing.cast(CfnServerCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnServiceLinkedRoleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_service_name": "awsServiceName",
        "custom_suffix": "customSuffix",
        "description": "description",
    },
)
class CfnServiceLinkedRoleMixinProps:
    def __init__(
        self,
        *,
        aws_service_name: typing.Optional[builtins.str] = None,
        custom_suffix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServiceLinkedRolePropsMixin.

        :param aws_service_name: The service principal for the AWS service to which this role is attached. You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` . Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.
        :param custom_suffix: A string that you provide, which is combined with the service-provided prefix to form the complete role name. If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix. Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.
        :param description: The description of the role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_service_linked_role_mixin_props = iam_mixins.CfnServiceLinkedRoleMixinProps(
                aws_service_name="awsServiceName",
                custom_suffix="customSuffix",
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b2d9bbe41688a27c3c879d5dcccaca85d57416db49db10480c56b04a43985de)
            check_type(argname="argument aws_service_name", value=aws_service_name, expected_type=type_hints["aws_service_name"])
            check_type(argname="argument custom_suffix", value=custom_suffix, expected_type=type_hints["custom_suffix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if aws_service_name is not None:
            self._values["aws_service_name"] = aws_service_name
        if custom_suffix is not None:
            self._values["custom_suffix"] = custom_suffix
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def aws_service_name(self) -> typing.Optional[builtins.str]:
        '''The service principal for the AWS service to which this role is attached.

        You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` .

        Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        '''
        result = self._values.get("aws_service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_suffix(self) -> typing.Optional[builtins.str]:
        '''A string that you provide, which is combined with the service-provided prefix to form the complete role name.

        If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix.

        Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        '''
        result = self._values.get("custom_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the role.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceLinkedRoleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceLinkedRolePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnServiceLinkedRolePropsMixin",
):
    '''Creates an IAM role that is linked to a specific AWS service.

    The service controls the attached policies and when the role can be deleted. This helps ensure that the service is not broken by an unexpectedly changed or deleted role, which could put your AWS resources into an unknown state. Allowing the service to control the role helps improve service stability and proper cleanup when a service and its role are no longer needed. For more information, see `Using service-linked roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html>`_ in the *IAM User Guide* .

    To attach a policy to this service-linked role, you must make the request using the AWS service that depends on this role.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
    :cloudformationResource: AWS::IAM::ServiceLinkedRole
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_service_linked_role_props_mixin = iam_mixins.CfnServiceLinkedRolePropsMixin(iam_mixins.CfnServiceLinkedRoleMixinProps(
            aws_service_name="awsServiceName",
            custom_suffix="customSuffix",
            description="description"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServiceLinkedRoleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::ServiceLinkedRole``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a619830adaa8c7fdc85d9d257c495fe59015c7ddd85511e6cc8246ef47c6f63f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc92e4ad0c03458a5ff51c8af9a199ec2f7efc397a1a428808f67ef84b2d843c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc19c8bb5588b0d0e7b9f209fb656ff4ed382a8b0e534b9e049c91693aaf94a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceLinkedRoleMixinProps:
        return typing.cast(CfnServiceLinkedRoleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "login_profile": "loginProfile",
        "managed_policy_arns": "managedPolicyArns",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "tags": "tags",
        "user_name": "userName",
    },
)
class CfnUserMixinProps:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.LoginProfileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.PolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPropsMixin.

        :param groups: A list of group names to which you want to add the user.
        :param login_profile: Creates a password for the specified IAM user. A password allows an IAM user to access AWS services through the AWS Management Console . You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console . For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path for the user name. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the managed policy that is used to set the permissions boundary for the user. A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* . For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM user. To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ . .. epigraph:: The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        :param tags: A list of tags that you want to attach to the new user. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param user_name: The name of the user to create. Do not include the path in this value. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john". If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_user_mixin_props = iam_mixins.CfnUserMixinProps(
                groups=["groups"],
                login_profile=iam_mixins.CfnUserPropsMixin.LoginProfileProperty(
                    password="password",
                    password_reset_required=False
                ),
                managed_policy_arns=["managedPolicyArns"],
                path="path",
                permissions_boundary="permissionsBoundary",
                policies=[iam_mixins.CfnUserPropsMixin.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bed884fc96ed26199ad09b5a2b0bb41c987e71f362770d6bc23b3fbc4740ed35)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument login_profile", value=login_profile, expected_type=type_hints["login_profile"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if login_profile is not None:
            self._values["login_profile"] = login_profile
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of group names to which you want to add the user.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_profile(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.LoginProfileProperty"]]:
        '''Creates a password for the specified IAM user.

        A password allows an IAM user to access AWS services through the AWS Management Console .

        You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console .

        For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-loginprofile
        '''
        result = self._values.get("login_profile")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.LoginProfileProperty"]], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-managedpolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the managed policy that is used to set the permissions boundary for the user.

        A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.PolicyProperty"]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM user.

        To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ .
        .. epigraph::

           The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.PolicyProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the new user.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user to create. Do not include the path in this value.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john".

        If you don't specify a name, CloudFormation generates a unique physical ID and uses that ID for the user name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html#cfn-iam-user-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserPolicyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "user_name": "userName",
    },
)
class CfnUserPolicyMixinProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any = None,
        policy_name: typing.Optional[builtins.str] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPolicyPropsMixin.

        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ) - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param user_name: The name of the user to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-userpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            # policy_document: Any
            
            cfn_user_policy_mixin_props = iam_mixins.CfnUserPolicyMixinProps(
                policy_document=policy_document,
                policy_name="policyName",
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5797d4e4553de15de703e7a1de61c7da91b17a6a91e96081311360d9162f1d09)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if policy_document is not None:
            self._values["policy_document"] = policy_document
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` )
        - The special characters tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` )

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-userpolicy.html#cfn-iam-userpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-userpolicy.html#cfn-iam-userpolicy-policyname
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-userpolicy.html#cfn-iam-userpolicy-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserPolicyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPolicyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserPolicyPropsMixin",
):
    '''Adds or updates an inline policy document that is embedded in the specified IAM user.

    An IAM user can also have a managed policy attached to it. To attach a managed policy to a user, use ```AWS::IAM::User`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html>`_ . To create a new managed policy, use ```AWS::IAM::ManagedPolicy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html>`_ . For information about policies, see `Managed policies and inline policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    For information about the maximum number of inline policies that you can embed in a user, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-userpolicy.html
    :cloudformationResource: AWS::IAM::UserPolicy
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_user_policy_props_mixin = iam_mixins.CfnUserPolicyPropsMixin(iam_mixins.CfnUserPolicyMixinProps(
            policy_document=policy_document,
            policy_name="policyName",
            user_name="userName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::UserPolicy``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183b6032aa76b0dbc7e5cf7c63bdc30558671d49b4d658c86cb84573eaa574f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a902eda93f069e0252e6154bfb10beb0bae01dbb09483fa88fc7e5209898576e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caeb33fd770b1096efe2c36b23e3741912c8a7d2439fd3d8bd232e549bc7d75d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserPolicyMixinProps:
        return typing.cast(CfnUserPolicyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnUserPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserPropsMixin",
):
    '''Creates a new IAM user for your AWS account .

    For information about quotas for the number of IAM users you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-user.html
    :cloudformationResource: AWS::IAM::User
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        # policy_document: Any
        
        cfn_user_props_mixin = iam_mixins.CfnUserPropsMixin(iam_mixins.CfnUserMixinProps(
            groups=["groups"],
            login_profile=iam_mixins.CfnUserPropsMixin.LoginProfileProperty(
                password="password",
                password_reset_required=False
            ),
            managed_policy_arns=["managedPolicyArns"],
            path="path",
            permissions_boundary="permissionsBoundary",
            policies=[iam_mixins.CfnUserPropsMixin.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_name="userName"
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
        '''Create a mixin to apply properties to ``AWS::IAM::User``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61716a0a11640f7413e711068de215653671edc0eafa20c0e3c383a998f638cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8fa034c1c7bff6c3435075b71d7f406ccb42c2f3eeb988042936933dae4e6641)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b426f9ced1c827796d50677bf6e843a7732642b29834db562ae691f87db3acbf)
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
        jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserPropsMixin.LoginProfileProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "password_reset_required": "passwordResetRequired",
        },
    )
    class LoginProfileProperty:
        def __init__(
            self,
            *,
            password: typing.Optional[builtins.str] = None,
            password_reset_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Creates a password for the specified user, giving the user the ability to access AWS services through the AWS Management Console .

            For more information about managing passwords, see `Managing Passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

            :param password: The user's password.
            :param password_reset_required: Specifies whether the user is required to set a new password on next sign-in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
                
                login_profile_property = iam_mixins.CfnUserPropsMixin.LoginProfileProperty(
                    password="password",
                    password_reset_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b47bbe102fdd47ee6361a08c35e7fb49752e36e2efc475e18946c17bb8b40e20)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument password_reset_required", value=password_reset_required, expected_type=type_hints["password_reset_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if password is not None:
                self._values["password"] = password
            if password_reset_required is not None:
                self._values["password_reset_required"] = password_reset_required

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The user's password.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def password_reset_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies whether the user is required to set a new password on next sign-in.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-passwordresetrequired
            '''
            result = self._values.get("password_reset_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoginProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserPropsMixin.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any = None,
            policy_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, refer to `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The entire contents of the policy that defines permissions. For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
                
                # policy_document: Any
                
                policy_property = iam_mixins.CfnUserPropsMixin.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b143da8664673d41797acb77498e368f5bdab27afa197a082cb0561bbddee1cb)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_document is not None:
                self._values["policy_document"] = policy_document
            if policy_name is not None:
                self._values["policy_name"] = policy_name

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The entire contents of the policy that defines permissions.

            For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-policy.html#cfn-iam-user-policy-policydocument
            '''
            result = self._values.get("policy_document")
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> typing.Optional[builtins.str]:
            '''The friendly name (not ARN) identifying the policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-policy.html#cfn-iam-user-policy-policyname
            '''
            result = self._values.get("policy_name")
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
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserToGroupAdditionMixinProps",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "users": "users"},
)
class CfnUserToGroupAdditionMixinProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnUserToGroupAdditionPropsMixin.

        :param group_name: The name of the group to update. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param users: A list of the names of the users that you want to add to the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-usertogroupaddition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_user_to_group_addition_mixin_props = iam_mixins.CfnUserToGroupAdditionMixinProps(
                group_name="groupName",
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc936f8b24d800842432735b2233894dedf974f461b68b7482652b0f9a4b785c)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to update.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-usertogroupaddition.html#cfn-iam-usertogroupaddition-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the names of the users that you want to add to the group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-usertogroupaddition.html#cfn-iam-usertogroupaddition-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserToGroupAdditionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserToGroupAdditionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnUserToGroupAdditionPropsMixin",
):
    '''Adds the specified user to the specified group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-usertogroupaddition.html
    :cloudformationResource: AWS::IAM::UserToGroupAddition
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_user_to_group_addition_props_mixin = iam_mixins.CfnUserToGroupAdditionPropsMixin(iam_mixins.CfnUserToGroupAdditionMixinProps(
            group_name="groupName",
            users=["users"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserToGroupAdditionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::UserToGroupAddition``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab3dd899dcbf283443fc87da96ee452c233da7464bbffff248dc83eb413f1e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d96fd1123ddb3b34def7fdaae5b06790c62a32a7b3628e9d04875bd05a21c89d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cecb3cbdc05f31a346da0f50c7d0737dc7d78a2c94543fd72fe2b559b2a03442)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserToGroupAdditionMixinProps:
        return typing.cast(CfnUserToGroupAdditionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnVirtualMFADeviceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "tags": "tags",
        "users": "users",
        "virtual_mfa_device_name": "virtualMfaDeviceName",
    },
)
class CfnVirtualMFADeviceMixinProps:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
        virtual_mfa_device_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVirtualMFADevicePropsMixin.

        :param path: The path for the virtual MFA device. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param tags: A list of tags that you want to attach to the new IAM virtual MFA device. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param users: The IAM user associated with this virtual MFA device.
        :param virtual_mfa_device_name: The name of the virtual MFA device, which must be unique. Use with path to uniquely identify a virtual MFA device. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
            
            cfn_virtual_mFADevice_mixin_props = iam_mixins.CfnVirtualMFADeviceMixinProps(
                path="path",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                users=["users"],
                virtual_mfa_device_name="virtualMfaDeviceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea55aba130d69e6fae91b2760122d527939c9efe0928adfc6c13234d4a4f5b61)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument virtual_mfa_device_name", value=virtual_mfa_device_name, expected_type=type_hints["virtual_mfa_device_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if tags is not None:
            self._values["tags"] = tags
        if users is not None:
            self._values["users"] = users
        if virtual_mfa_device_name is not None:
            self._values["virtual_mfa_device_name"] = virtual_mfa_device_name

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the virtual MFA device.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\u0021`` ) through the DEL character ( ``\\u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of tags that you want to attach to the new IAM virtual MFA device.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IAM user associated with this virtual MFA device.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def virtual_mfa_device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual MFA device, which must be unique.

        Use with path to uniquely identify a virtual MFA device.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-virtualmfadevicename
        '''
        result = self._values.get("virtual_mfa_device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualMFADeviceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVirtualMFADevicePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_iam.mixins.CfnVirtualMFADevicePropsMixin",
):
    '''Creates a new virtual MFA device for the AWS account .

    After creating the virtual MFA, use `EnableMFADevice <https://docs.aws.amazon.com/IAM/latest/APIReference/API_EnableMFADevice.html>`_ to attach the MFA device to an IAM user. For more information about creating and working with virtual MFA devices, see `Using a virtual MFA device <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_VirtualMFA.html>`_ in the *IAM User Guide* .

    For information about the maximum number of MFA devices you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       The seed information contained in the QR code and the Base32 string should be treated like any other secret access information. In other words, protect the seed information as you would your AWS access keys or your passwords. After you provision your virtual device, you should ensure that the information is destroyed following secure procedures.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html
    :cloudformationResource: AWS::IAM::VirtualMFADevice
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_iam import mixins as iam_mixins
        
        cfn_virtual_mFADevice_props_mixin = iam_mixins.CfnVirtualMFADevicePropsMixin(iam_mixins.CfnVirtualMFADeviceMixinProps(
            path="path",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            users=["users"],
            virtual_mfa_device_name="virtualMfaDeviceName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVirtualMFADeviceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::IAM::VirtualMFADevice``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6e5f0961474d3675a283f158820f60c2880e9851f7bba2d0cedca048924869)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f5a7b5aeaf0ad4be2201e4730a8f88168b8c1e9ffd20d4b78d25a7e3f69b335)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9021ec6773d8c2d1581283b0a85ff73198f1f2b5fb7b9e5bad6e008aefe924d7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVirtualMFADeviceMixinProps:
        return typing.cast(CfnVirtualMFADeviceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAccessKeyMixinProps",
    "CfnAccessKeyPropsMixin",
    "CfnGroupMixinProps",
    "CfnGroupPolicyMixinProps",
    "CfnGroupPolicyPropsMixin",
    "CfnGroupPropsMixin",
    "CfnInstanceProfileMixinProps",
    "CfnInstanceProfilePropsMixin",
    "CfnManagedPolicyMixinProps",
    "CfnManagedPolicyPropsMixin",
    "CfnOIDCProviderMixinProps",
    "CfnOIDCProviderPropsMixin",
    "CfnPolicyMixinProps",
    "CfnPolicyPropsMixin",
    "CfnRoleMixinProps",
    "CfnRolePolicyMixinProps",
    "CfnRolePolicyPropsMixin",
    "CfnRolePropsMixin",
    "CfnSAMLProviderMixinProps",
    "CfnSAMLProviderPropsMixin",
    "CfnServerCertificateMixinProps",
    "CfnServerCertificatePropsMixin",
    "CfnServiceLinkedRoleMixinProps",
    "CfnServiceLinkedRolePropsMixin",
    "CfnUserMixinProps",
    "CfnUserPolicyMixinProps",
    "CfnUserPolicyPropsMixin",
    "CfnUserPropsMixin",
    "CfnUserToGroupAdditionMixinProps",
    "CfnUserToGroupAdditionPropsMixin",
    "CfnVirtualMFADeviceMixinProps",
    "CfnVirtualMFADevicePropsMixin",
]

publication.publish()

def _typecheckingstub__667fb2d6c96b48768dd9b15d5927d81bd02803cc90d2a71e9064118a3a8c80f8(
    *,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07916fa3109989a36f3a892df0eb08aec93ef8fcdde52bc1269773a33771765a(
    props: typing.Union[CfnAccessKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a586a279a8f93d02f0c531685b044e395e465a7491e930f58eef13995c99b0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d6ac2bc1f33507cf035f2decf8c2a9f18b224d9420e1e0d95677f579d9145c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6341b4217cfcb11835888db05678654be3f5a9bb73f5a0fcedcbb61b6226e500(
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnGroupPropsMixin.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837a056370eb6710c1cb2b9ccabcd0346e68e4ab54057752a96d3adbb57f6888(
    *,
    group_name: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d3a83f4a758dc739104e052eb3e3b42c87bad2e761665a8ee01ec4f6efa4fb(
    props: typing.Union[CfnGroupPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6999a40dd0a3f157698d3d5b23ed440893ff488bc288a20376ea058e8a10708(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba625031af088706b427d35d2bfb07581ca5268cb63e6c5e7235e189b8f3a75e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e89a1600a26aca07b0f22e60962a2da9f29dbd772a9a0a343bf4e0d43046c8(
    props: typing.Union[CfnGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b858c5ef3a5debdf950a379e2682d25b3b35b142cb62c18649f30868a08afee(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__261a8d0eaa1b8c112ac487d955a6db62f112a6578f860bcdfbd26047eca63dcc(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864da8deb879ce026dd3b82315320ff3830029d42093034ef06e7be49bad1d84(
    *,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6884b55f7939fd1fcf475cdc70ed0e420c7a629eb5dd51c07aaae550108248(
    *,
    instance_profile_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__390090c2cdca8076013d5a76b382bc6435e8736be7138cd4cc5c3e5121d2b6f4(
    props: typing.Union[CfnInstanceProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081bb370a7d202808ce1125b2b53afc55ba126142df63d135254ada26514bd9b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d30690369ff9bce316cb37b2d8d7852b72abb87ad38b4cfb3740881ccce8a5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3524be4c27fd6acf63e3d44693b4bfd6652afb7288c1d0bae300df39d2fb3af(
    *,
    description: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    policy_document: typing.Any = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84943610be47cc0cffebe3d2f864698d827edcd744212b05c589d7a72b91bd0(
    props: typing.Union[CfnManagedPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0cd3838e3e8172eaea32b78073426bc2002a1c0baff8a5ae96c8e0ceec0434(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e78de50c8c117b2faf0b0e1b0a9b8c53e59bc3259b9c681fc6f73b12cbd124(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b265bbf0cc0a691f2d8f7405a5fe74d27cc56a0bd1699b63a6455bed8ef367(
    *,
    client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    thumbprint_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9f793a34480fc75de979bb4189dd08e44888c3dd12f643d907d9c31bef1ff5(
    props: typing.Union[CfnOIDCProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14db8b303f0d78d942464f08ef50368eb114424f5251a2203cbaaef8e855c5e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__152f42bdb6756442608b1e051426e5847636af9c3cbaeaaafe60a6fc77d31950(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f655b82f9f8a8ec7551016bc2cbe1ad396184561fe01463aed29234d80d68a2(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23ebf00b12c9fbf58506dbb43a06ee39402e9df79b5331141cd60944f11ef58(
    props: typing.Union[CfnPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abff2b1f74e686b74e548a58f4c63fcdd1c7c6d37ec291796401a20b4beda23(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6734f6b7a0eb6934a1a1c9088ab4ef286fae382568415c93ef5953a174165465(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fe5a414314e1714619916d29c1278900a88d9e7301bad1bda1363f8cb89662(
    *,
    assume_role_policy_document: typing.Any = None,
    description: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_session_duration: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRolePropsMixin.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    role_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd037386f28fd04dae74c903c15e3af633dac66fbfa4b51b427ff11cad486501(
    *,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd6f6b43538cb8b8670aa60e414a056e3ee644c12a6c64b428b4d2d807ab14c7(
    props: typing.Union[CfnRolePolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37ce4b10eb7416c2f0f598bcf5365c2307db3a13ae7a8944f62c349590fec2ff(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c093f24e631319954cdb64208be7ff7e919167e958ad6aaa5bcc8e1d7bcb95(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02affbee49162438343b52598a1b37e34c1c7fa883f04c0a2dd4273fb561513(
    props: typing.Union[CfnRoleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdef70c482053898554d9bb4e3d6ee43a7d3b508ea906ee8f7935833d7a308a3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c7bbc2ff7f5e6574f68a7a682bc9314e983bf8b5cd5fb55b5a7bdf6cff11c2d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d42a5b06521c8ff7e02a033c136a54907f481b8278c26c8ae439012f0bc853(
    *,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec2b5a7aec047b3c3c150d76f3cca4a001e01269ff445a202768e53812decc9(
    *,
    add_private_key: typing.Optional[builtins.str] = None,
    assertion_encryption_mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    private_key_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSAMLProviderPropsMixin.SAMLPrivateKeyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    remove_private_key: typing.Optional[builtins.str] = None,
    saml_metadata_document: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc486a0022f6cfe1bab76035c3dc9a3236a6237e53f1fc32dc3ee12bf1f5fe6c(
    props: typing.Union[CfnSAMLProviderMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced242a2067981f4f4af2c45ca61b8d5331fe1edc35539337cb0daedf33e748e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2723cc84aaf6d3f40f5048734082e87ffc51b40fb1d29c78324d747f6d2209e8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8097571e82d554193680a8548df8d7e34a2a72e0f1385787b9c759090dff9c(
    *,
    key_id: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df438f7b5bbf807e75e1f4f55e218eb43a6b8d39ce84958c7cf7e9200e16198(
    *,
    certificate_body: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    server_certificate_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__799173fb948634e8b331c3cbe1106373b9c262c3d349ea4efcbe3df02722ec7a(
    props: typing.Union[CfnServerCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c65534e25e57a5966e23550839366c509b080a1ec028a14ef6cf7eccb9e0d36(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebfbb94e5b451f13e78320a473f95e1079b542498633b26d2c5d6517ae0f8af0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b2d9bbe41688a27c3c879d5dcccaca85d57416db49db10480c56b04a43985de(
    *,
    aws_service_name: typing.Optional[builtins.str] = None,
    custom_suffix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a619830adaa8c7fdc85d9d257c495fe59015c7ddd85511e6cc8246ef47c6f63f(
    props: typing.Union[CfnServiceLinkedRoleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc92e4ad0c03458a5ff51c8af9a199ec2f7efc397a1a428808f67ef84b2d843c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc19c8bb5588b0d0e7b9f209fb656ff4ed382a8b0e534b9e049c91693aaf94a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bed884fc96ed26199ad09b5a2b0bb41c987e71f362770d6bc23b3fbc4740ed35(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.PolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5797d4e4553de15de703e7a1de61c7da91b17a6a91e96081311360d9162f1d09(
    *,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183b6032aa76b0dbc7e5cf7c63bdc30558671d49b4d658c86cb84573eaa574f2(
    props: typing.Union[CfnUserPolicyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a902eda93f069e0252e6154bfb10beb0bae01dbb09483fa88fc7e5209898576e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caeb33fd770b1096efe2c36b23e3741912c8a7d2439fd3d8bd232e549bc7d75d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61716a0a11640f7413e711068de215653671edc0eafa20c0e3c383a998f638cd(
    props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa034c1c7bff6c3435075b71d7f406ccb42c2f3eeb988042936933dae4e6641(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b426f9ced1c827796d50677bf6e843a7732642b29834db562ae691f87db3acbf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b47bbe102fdd47ee6361a08c35e7fb49752e36e2efc475e18946c17bb8b40e20(
    *,
    password: typing.Optional[builtins.str] = None,
    password_reset_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b143da8664673d41797acb77498e368f5bdab27afa197a082cb0561bbddee1cb(
    *,
    policy_document: typing.Any = None,
    policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc936f8b24d800842432735b2233894dedf974f461b68b7482652b0f9a4b785c(
    *,
    group_name: typing.Optional[builtins.str] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab3dd899dcbf283443fc87da96ee452c233da7464bbffff248dc83eb413f1e3(
    props: typing.Union[CfnUserToGroupAdditionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96fd1123ddb3b34def7fdaae5b06790c62a32a7b3628e9d04875bd05a21c89d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cecb3cbdc05f31a346da0f50c7d0737dc7d78a2c94543fd72fe2b559b2a03442(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea55aba130d69e6fae91b2760122d527939c9efe0928adfc6c13234d4a4f5b61(
    *,
    path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
    virtual_mfa_device_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6e5f0961474d3675a283f158820f60c2880e9851f7bba2d0cedca048924869(
    props: typing.Union[CfnVirtualMFADeviceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f5a7b5aeaf0ad4be2201e4730a8f88168b8c1e9ffd20d4b78d25a7e3f69b335(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9021ec6773d8c2d1581283b0a85ff73198f1f2b5fb7b9e5bad6e008aefe924d7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
