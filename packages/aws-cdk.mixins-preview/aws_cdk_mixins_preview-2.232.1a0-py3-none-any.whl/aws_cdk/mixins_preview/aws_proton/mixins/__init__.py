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
    jsii_type="@aws-cdk/mixins-preview.aws_proton.mixins.CfnEnvironmentAccountConnectionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "codebuild_role_arn": "codebuildRoleArn",
        "component_role_arn": "componentRoleArn",
        "environment_account_id": "environmentAccountId",
        "environment_name": "environmentName",
        "management_account_id": "managementAccountId",
        "role_arn": "roleArn",
        "tags": "tags",
    },
)
class CfnEnvironmentAccountConnectionMixinProps:
    def __init__(
        self,
        *,
        codebuild_role_arn: typing.Optional[builtins.str] = None,
        component_role_arn: typing.Optional[builtins.str] = None,
        environment_account_id: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        management_account_id: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentAccountConnectionPropsMixin.

        :param codebuild_role_arn: The Amazon Resource Name (ARN) of an IAM service role in the environment account. AWS Proton uses this role to provision infrastructure resources using CodeBuild-based provisioning in the associated environment account.
        :param component_role_arn: The Amazon Resource Name (ARN) of the IAM service role that AWS Proton uses when provisioning directly defined components in the associated environment account. It determines the scope of infrastructure that a component can provision in the account. The environment account connection must have a ``componentRoleArn`` to allow directly defined components to be associated with any environments running in the account. For more information about components, see `AWS Proton components <https://docs.aws.amazon.com/proton/latest/userguide/ag-components.html>`_ in the *AWS Proton User Guide* .
        :param environment_account_id: The environment account that's connected to the environment account connection.
        :param environment_name: The name of the environment that's associated with the environment account connection.
        :param management_account_id: The ID of the management account that's connected to the environment account connection.
        :param role_arn: The IAM service role that's associated with the environment account connection.
        :param tags: An optional list of metadata items that you can associate with the AWS Proton environment account connection. A tag is a key-value pair. For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_proton import mixins as proton_mixins
            
            cfn_environment_account_connection_mixin_props = proton_mixins.CfnEnvironmentAccountConnectionMixinProps(
                codebuild_role_arn="codebuildRoleArn",
                component_role_arn="componentRoleArn",
                environment_account_id="environmentAccountId",
                environment_name="environmentName",
                management_account_id="managementAccountId",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bad7a0a01888a9ef8abd512be03e6aff455caa999d3f55324a70c0b74b8d23)
            check_type(argname="argument codebuild_role_arn", value=codebuild_role_arn, expected_type=type_hints["codebuild_role_arn"])
            check_type(argname="argument component_role_arn", value=component_role_arn, expected_type=type_hints["component_role_arn"])
            check_type(argname="argument environment_account_id", value=environment_account_id, expected_type=type_hints["environment_account_id"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument management_account_id", value=management_account_id, expected_type=type_hints["management_account_id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if codebuild_role_arn is not None:
            self._values["codebuild_role_arn"] = codebuild_role_arn
        if component_role_arn is not None:
            self._values["component_role_arn"] = component_role_arn
        if environment_account_id is not None:
            self._values["environment_account_id"] = environment_account_id
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if management_account_id is not None:
            self._values["management_account_id"] = management_account_id
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def codebuild_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an IAM service role in the environment account.

        AWS Proton uses this role to provision infrastructure resources using CodeBuild-based provisioning in the associated environment account.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-codebuildrolearn
        '''
        result = self._values.get("codebuild_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def component_role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM service role that AWS Proton uses when provisioning directly defined components in the associated environment account.

        It determines the scope of infrastructure that a component can provision in the account.

        The environment account connection must have a ``componentRoleArn`` to allow directly defined components to be associated with any environments running in the account.

        For more information about components, see `AWS Proton components <https://docs.aws.amazon.com/proton/latest/userguide/ag-components.html>`_ in the *AWS Proton User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-componentrolearn
        '''
        result = self._values.get("component_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_account_id(self) -> typing.Optional[builtins.str]:
        '''The environment account that's connected to the environment account connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-environmentaccountid
        '''
        result = self._values.get("environment_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment that's associated with the environment account connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def management_account_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the management account that's connected to the environment account connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-managementaccountid
        '''
        result = self._values.get("management_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM service role that's associated with the environment account connection.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional list of metadata items that you can associate with the AWS Proton environment account connection.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html#cfn-proton-environmentaccountconnection-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentAccountConnectionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentAccountConnectionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_proton.mixins.CfnEnvironmentAccountConnectionPropsMixin",
):
    '''Detailed data of an AWS Proton environment account connection resource.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmentaccountconnection.html
    :cloudformationResource: AWS::Proton::EnvironmentAccountConnection
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_proton import mixins as proton_mixins
        
        cfn_environment_account_connection_props_mixin = proton_mixins.CfnEnvironmentAccountConnectionPropsMixin(proton_mixins.CfnEnvironmentAccountConnectionMixinProps(
            codebuild_role_arn="codebuildRoleArn",
            component_role_arn="componentRoleArn",
            environment_account_id="environmentAccountId",
            environment_name="environmentName",
            management_account_id="managementAccountId",
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
        props: typing.Union[CfnEnvironmentAccountConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Proton::EnvironmentAccountConnection``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adaa50747598bed57dd9eefd66e70bfa06ae09cc5bd8b9669970a62c5f31fb60)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a54529df88e5ebb973e097f2c30c5a0224416eabdab94240bd69ba118d0672c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01adc060b3872017ab6549522e0fce7a839fdd297ceb8c2ff7f3ebc4570bc0e1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentAccountConnectionMixinProps:
        return typing.cast(CfnEnvironmentAccountConnectionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_proton.mixins.CfnEnvironmentTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "encryption_key": "encryptionKey",
        "name": "name",
        "provisioning": "provisioning",
        "tags": "tags",
    },
)
class CfnEnvironmentTemplateMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnEnvironmentTemplatePropsMixin.

        :param description: A description of the environment template.
        :param display_name: The name of the environment template as displayed in the developer interface.
        :param encryption_key: The customer provided encryption key for the environment template.
        :param name: The name of the environment template.
        :param provisioning: When included, indicates that the environment template is for customer provisioned and managed infrastructure.
        :param tags: An optional list of metadata items that you can associate with the AWS Proton environment template. A tag is a key-value pair. For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_proton import mixins as proton_mixins
            
            cfn_environment_template_mixin_props = proton_mixins.CfnEnvironmentTemplateMixinProps(
                description="description",
                display_name="displayName",
                encryption_key="encryptionKey",
                name="name",
                provisioning="provisioning",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae59a0bc7c134269d5ea18ee588893301330c04c154da644f4a24c898952369b)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument provisioning", value=provisioning, expected_type=type_hints["provisioning"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if name is not None:
            self._values["name"] = name
        if provisioning is not None:
            self._values["provisioning"] = provisioning
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment template as displayed in the developer interface.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer provided encryption key for the environment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the environment template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def provisioning(self) -> typing.Optional[builtins.str]:
        '''When included, indicates that the environment template is for customer provisioned and managed infrastructure.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-provisioning
        '''
        result = self._values.get("provisioning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An optional list of metadata items that you can associate with the AWS Proton environment template.

        A tag is a key-value pair.

        For more information, see `AWS Proton resources and tagging <https://docs.aws.amazon.com/proton/latest/userguide/resources.html>`_ in the *AWS Proton User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html#cfn-proton-environmenttemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnEnvironmentTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_proton.mixins.CfnEnvironmentTemplatePropsMixin",
):
    '''Create an environment template for AWS Proton .

    For more information, see `Environment Templates <https://docs.aws.amazon.com/proton/latest/userguide/ag-templates.html>`_ in the *AWS Proton User Guide* .

    You can create an environment template in one of the two following ways:

    - Register and publish a *standard* environment template that instructs AWS Proton to deploy and manage environment infrastructure.
    - Register and publish a *customer managed* environment template that connects AWS Proton to your existing provisioned infrastructure that you manage. AWS Proton *doesn't* manage your existing provisioned infrastructure. To create an environment template for customer provisioned and managed infrastructure, include the ``provisioning`` parameter and set the value to ``CUSTOMER_MANAGED`` . For more information, see `Register and publish an environment template <https://docs.aws.amazon.com/proton/latest/userguide/template-create.html>`_ in the *AWS Proton User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-environmenttemplate.html
    :cloudformationResource: AWS::Proton::EnvironmentTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_proton import mixins as proton_mixins
        
        cfn_environment_template_props_mixin = proton_mixins.CfnEnvironmentTemplatePropsMixin(proton_mixins.CfnEnvironmentTemplateMixinProps(
            description="description",
            display_name="displayName",
            encryption_key="encryptionKey",
            name="name",
            provisioning="provisioning",
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
        props: typing.Union[CfnEnvironmentTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Proton::EnvironmentTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc41b84fce408427d89c48ecb6274b52b73b77168bd4eb221f4f08595c9ee3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66b7f5c2eccd9165ba39586adc24f6c1fa0e033d044262fbe8000aaeb42eeba5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__372958998a09bc5a5465fff8fd41583ddcd40203f5727fdd129950a7d0a66024)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnEnvironmentTemplateMixinProps:
        return typing.cast(CfnEnvironmentTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_proton.mixins.CfnServiceTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "display_name": "displayName",
        "encryption_key": "encryptionKey",
        "name": "name",
        "pipeline_provisioning": "pipelineProvisioning",
        "tags": "tags",
    },
)
class CfnServiceTemplateMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        pipeline_provisioning: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServiceTemplatePropsMixin.

        :param description: A description of the service template.
        :param display_name: The service template name as displayed in the developer interface.
        :param encryption_key: The customer provided service template encryption key that's used to encrypt data.
        :param name: The name of the service template.
        :param pipeline_provisioning: If ``pipelineProvisioning`` is ``true`` , a service pipeline is included in the service template. Otherwise, a service pipeline *isn't* included in the service template.
        :param tags: An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_proton import mixins as proton_mixins
            
            cfn_service_template_mixin_props = proton_mixins.CfnServiceTemplateMixinProps(
                description="description",
                display_name="displayName",
                encryption_key="encryptionKey",
                name="name",
                pipeline_provisioning="pipelineProvisioning",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3beab2a5f0d97fc368cfa763c1c91d80b915c74e6d9dd1e23bbff4d9d920fd68)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument pipeline_provisioning", value=pipeline_provisioning, expected_type=type_hints["pipeline_provisioning"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if display_name is not None:
            self._values["display_name"] = display_name
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if name is not None:
            self._values["name"] = name
        if pipeline_provisioning is not None:
            self._values["pipeline_provisioning"] = pipeline_provisioning
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''The service template name as displayed in the developer interface.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-displayname
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[builtins.str]:
        '''The customer provided service template encryption key that's used to encrypt data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-encryptionkey
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_provisioning(self) -> typing.Optional[builtins.str]:
        '''If ``pipelineProvisioning`` is ``true`` , a service pipeline is included in the service template.

        Otherwise, a service pipeline *isn't* included in the service template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-pipelineprovisioning
        '''
        result = self._values.get("pipeline_provisioning")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An object that includes the template bundle S3 bucket path and name for the new version of a service template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html#cfn-proton-servicetemplate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServiceTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_proton.mixins.CfnServiceTemplatePropsMixin",
):
    '''Create a service template.

    The administrator creates a service template to define standardized infrastructure and an optional CI/CD service pipeline. Developers, in turn, select the service template from AWS Proton . If the selected service template includes a service pipeline definition, they provide a link to their source code repository. AWS Proton then deploys and manages the infrastructure defined by the selected service template. For more information, see `AWS Proton templates <https://docs.aws.amazon.com/proton/latest/userguide/ag-templates.html>`_ in the *AWS Proton User Guide* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-proton-servicetemplate.html
    :cloudformationResource: AWS::Proton::ServiceTemplate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_proton import mixins as proton_mixins
        
        cfn_service_template_props_mixin = proton_mixins.CfnServiceTemplatePropsMixin(proton_mixins.CfnServiceTemplateMixinProps(
            description="description",
            display_name="displayName",
            encryption_key="encryptionKey",
            name="name",
            pipeline_provisioning="pipelineProvisioning",
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
        props: typing.Union[CfnServiceTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Proton::ServiceTemplate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c9764910d696a0ae6410f65b43a02a077a5b8d3a88542b3c4eb69d7aa0d6958)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5fbd63d8330c73a35084e3610c6f02c01f3fd91c6947c08ca2d7a5916ba41f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59006280abd3752d5597016dca430ef94c9cf08fa13a624ca0aae84084268e60)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServiceTemplateMixinProps:
        return typing.cast(CfnServiceTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnEnvironmentAccountConnectionMixinProps",
    "CfnEnvironmentAccountConnectionPropsMixin",
    "CfnEnvironmentTemplateMixinProps",
    "CfnEnvironmentTemplatePropsMixin",
    "CfnServiceTemplateMixinProps",
    "CfnServiceTemplatePropsMixin",
]

publication.publish()

def _typecheckingstub__a1bad7a0a01888a9ef8abd512be03e6aff455caa999d3f55324a70c0b74b8d23(
    *,
    codebuild_role_arn: typing.Optional[builtins.str] = None,
    component_role_arn: typing.Optional[builtins.str] = None,
    environment_account_id: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    management_account_id: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adaa50747598bed57dd9eefd66e70bfa06ae09cc5bd8b9669970a62c5f31fb60(
    props: typing.Union[CfnEnvironmentAccountConnectionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a54529df88e5ebb973e097f2c30c5a0224416eabdab94240bd69ba118d0672c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01adc060b3872017ab6549522e0fce7a839fdd297ceb8c2ff7f3ebc4570bc0e1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae59a0bc7c134269d5ea18ee588893301330c04c154da644f4a24c898952369b(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc41b84fce408427d89c48ecb6274b52b73b77168bd4eb221f4f08595c9ee3f(
    props: typing.Union[CfnEnvironmentTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b7f5c2eccd9165ba39586adc24f6c1fa0e033d044262fbe8000aaeb42eeba5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__372958998a09bc5a5465fff8fd41583ddcd40203f5727fdd129950a7d0a66024(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3beab2a5f0d97fc368cfa763c1c91d80b915c74e6d9dd1e23bbff4d9d920fd68(
    *,
    description: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    pipeline_provisioning: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c9764910d696a0ae6410f65b43a02a077a5b8d3a88542b3c4eb69d7aa0d6958(
    props: typing.Union[CfnServiceTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5fbd63d8330c73a35084e3610c6f02c01f3fd91c6947c08ca2d7a5916ba41f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59006280abd3752d5597016dca430ef94c9cf08fa13a624ca0aae84084268e60(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
