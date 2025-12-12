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
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnApplicationAssignmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_arn": "applicationArn",
        "principal_id": "principalId",
        "principal_type": "principalType",
    },
)
class CfnApplicationAssignmentMixinProps:
    def __init__(
        self,
        *,
        application_arn: typing.Optional[builtins.str] = None,
        principal_id: typing.Optional[builtins.str] = None,
        principal_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnApplicationAssignmentPropsMixin.

        :param application_arn: The ARN of the application that has principals assigned.
        :param principal_id: The unique identifier of the principal assigned to the application.
        :param principal_type: The type of the principal assigned to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-applicationassignment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
            
            cfn_application_assignment_mixin_props = sso_mixins.CfnApplicationAssignmentMixinProps(
                application_arn="applicationArn",
                principal_id="principalId",
                principal_type="principalType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd019052d7107729c161da0352e4b7c0b48715610cc415ffc7f937c09613d3fc)
            check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_arn is not None:
            self._values["application_arn"] = application_arn
        if principal_id is not None:
            self._values["principal_id"] = principal_id
        if principal_type is not None:
            self._values["principal_type"] = principal_type

    @builtins.property
    def application_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the application that has principals assigned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-applicationassignment.html#cfn-sso-applicationassignment-applicationarn
        '''
        result = self._values.get("application_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the principal assigned to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-applicationassignment.html#cfn-sso-applicationassignment-principalid
        '''
        result = self._values.get("principal_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_type(self) -> typing.Optional[builtins.str]:
        '''The type of the principal assigned to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-applicationassignment.html#cfn-sso-applicationassignment-principaltype
        '''
        result = self._values.get("principal_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationAssignmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationAssignmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnApplicationAssignmentPropsMixin",
):
    '''A structure that describes an assignment of a principal to an application.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-applicationassignment.html
    :cloudformationResource: AWS::SSO::ApplicationAssignment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
        
        cfn_application_assignment_props_mixin = sso_mixins.CfnApplicationAssignmentPropsMixin(sso_mixins.CfnApplicationAssignmentMixinProps(
            application_arn="applicationArn",
            principal_id="principalId",
            principal_type="principalType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationAssignmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSO::ApplicationAssignment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be76bf2d7dc468608b3035a97c7cecb1b22c2c078506e4197c959e97444c0ed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e57bf186bb6bf2f036cf35050d5ea6d8680306005dae70465353bb5d47f9516a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113a3efc2352acb0de2cfae2bff292bfb2b05084ec7d5fb63031845e2412d768)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationAssignmentMixinProps:
        return typing.cast(CfnApplicationAssignmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_provider_arn": "applicationProviderArn",
        "description": "description",
        "instance_arn": "instanceArn",
        "name": "name",
        "portal_options": "portalOptions",
        "status": "status",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_provider_arn: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        instance_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        portal_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.PortalOptionsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_provider_arn: The ARN of the application provider for this application.
        :param description: The description of the application.
        :param instance_arn: The ARN of the instance of IAM Identity Center that is configured with this application.
        :param name: The name of the application.
        :param portal_options: A structure that describes the options for the access portal associated with this application.
        :param status: The current status of the application in this instance of IAM Identity Center.
        :param tags: Specifies tags to be attached to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
            
            cfn_application_mixin_props = sso_mixins.CfnApplicationMixinProps(
                application_provider_arn="applicationProviderArn",
                description="description",
                instance_arn="instanceArn",
                name="name",
                portal_options=sso_mixins.CfnApplicationPropsMixin.PortalOptionsConfigurationProperty(
                    sign_in_options=sso_mixins.CfnApplicationPropsMixin.SignInOptionsProperty(
                        application_url="applicationUrl",
                        origin="origin"
                    ),
                    visibility="visibility"
                ),
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74c478664936b133a4b7cb4c980eb0bb1d9715837b4c7084bf3bbde7b9889a4)
            check_type(argname="argument application_provider_arn", value=application_provider_arn, expected_type=type_hints["application_provider_arn"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument portal_options", value=portal_options, expected_type=type_hints["portal_options"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_provider_arn is not None:
            self._values["application_provider_arn"] = application_provider_arn
        if description is not None:
            self._values["description"] = description
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if name is not None:
            self._values["name"] = name
        if portal_options is not None:
            self._values["portal_options"] = portal_options
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_provider_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the application provider for this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-applicationproviderarn
        '''
        result = self._values.get("application_provider_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the instance of IAM Identity Center that is configured with this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def portal_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PortalOptionsConfigurationProperty"]]:
        '''A structure that describes the options for the access portal associated with this application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-portaloptions
        '''
        result = self._values.get("portal_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.PortalOptionsConfigurationProperty"]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The current status of the application in this instance of IAM Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies tags to be attached to the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html#cfn-sso-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnApplicationPropsMixin",
):
    '''Creates an OAuth 2.0 customer managed application in IAM Identity Center for the given application provider.

    .. epigraph::

       This API does not support creating SAML 2.0 customer managed applications or AWS managed applications. To learn how to create an AWS managed application, see the application user guide. You can create a SAML 2.0 customer managed application in the AWS Management Console only. See `Setting up customer managed SAML 2.0 applications <https://docs.aws.amazon.com/singlesignon/latest/userguide/customermanagedapps-saml2-setup.html>`_ . For more information on these application types, see `AWS managed applications <https://docs.aws.amazon.com/singlesignon/latest/userguide/awsapps.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-application.html
    :cloudformationResource: AWS::SSO::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
        
        cfn_application_props_mixin = sso_mixins.CfnApplicationPropsMixin(sso_mixins.CfnApplicationMixinProps(
            application_provider_arn="applicationProviderArn",
            description="description",
            instance_arn="instanceArn",
            name="name",
            portal_options=sso_mixins.CfnApplicationPropsMixin.PortalOptionsConfigurationProperty(
                sign_in_options=sso_mixins.CfnApplicationPropsMixin.SignInOptionsProperty(
                    application_url="applicationUrl",
                    origin="origin"
                ),
                visibility="visibility"
            ),
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
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSO::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11abf81294a3e3dbf2c006b34cc6fa6327a089ffc978b6633faf0168c5ec4560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__736b6fd4155b6669276183943c08f74d655529e2eee6583c51cd11477a50ba75)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5633e1c4f675927ee31abcbb6d8f2ebf45acb5e43e258a25967aff29663f13f0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnApplicationPropsMixin.PortalOptionsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"sign_in_options": "signInOptions", "visibility": "visibility"},
    )
    class PortalOptionsConfigurationProperty:
        def __init__(
            self,
            *,
            sign_in_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.SignInOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            visibility: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that describes the options for the portal associated with an application.

            :param sign_in_options: A structure that describes the sign-in options for the access portal.
            :param visibility: Indicates whether this application is visible in the access portal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-application-portaloptionsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                portal_options_configuration_property = sso_mixins.CfnApplicationPropsMixin.PortalOptionsConfigurationProperty(
                    sign_in_options=sso_mixins.CfnApplicationPropsMixin.SignInOptionsProperty(
                        application_url="applicationUrl",
                        origin="origin"
                    ),
                    visibility="visibility"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__856a127b64a095fb9ea6035b8026536276a497fef3bf10c5f2ce40aa8626ecd0)
                check_type(argname="argument sign_in_options", value=sign_in_options, expected_type=type_hints["sign_in_options"])
                check_type(argname="argument visibility", value=visibility, expected_type=type_hints["visibility"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sign_in_options is not None:
                self._values["sign_in_options"] = sign_in_options
            if visibility is not None:
                self._values["visibility"] = visibility

        @builtins.property
        def sign_in_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SignInOptionsProperty"]]:
            '''A structure that describes the sign-in options for the access portal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-application-portaloptionsconfiguration.html#cfn-sso-application-portaloptionsconfiguration-signinoptions
            '''
            result = self._values.get("sign_in_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.SignInOptionsProperty"]], result)

        @builtins.property
        def visibility(self) -> typing.Optional[builtins.str]:
            '''Indicates whether this application is visible in the access portal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-application-portaloptionsconfiguration.html#cfn-sso-application-portaloptionsconfiguration-visibility
            '''
            result = self._values.get("visibility")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortalOptionsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnApplicationPropsMixin.SignInOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"application_url": "applicationUrl", "origin": "origin"},
    )
    class SignInOptionsProperty:
        def __init__(
            self,
            *,
            application_url: typing.Optional[builtins.str] = None,
            origin: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that describes the sign-in options for an application portal.

            :param application_url: The URL that accepts authentication requests for an application. This is a required parameter if the ``Origin`` parameter is ``APPLICATION`` .
            :param origin: This determines how IAM Identity Center navigates the user to the target application. It can be one of the following values: - ``APPLICATION`` : IAM Identity Center redirects the customer to the configured ``ApplicationUrl`` . - ``IDENTITY_CENTER`` : IAM Identity Center uses SAML identity-provider initiated authentication to sign the customer directly into a SAML-based application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-application-signinoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                sign_in_options_property = sso_mixins.CfnApplicationPropsMixin.SignInOptionsProperty(
                    application_url="applicationUrl",
                    origin="origin"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cbaa22d331a376b97e1e4d0bb27373c429293a8adb165b66f6b0d4608c8037a0)
                check_type(argname="argument application_url", value=application_url, expected_type=type_hints["application_url"])
                check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_url is not None:
                self._values["application_url"] = application_url
            if origin is not None:
                self._values["origin"] = origin

        @builtins.property
        def application_url(self) -> typing.Optional[builtins.str]:
            '''The URL that accepts authentication requests for an application.

            This is a required parameter if the ``Origin`` parameter is ``APPLICATION`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-application-signinoptions.html#cfn-sso-application-signinoptions-applicationurl
            '''
            result = self._values.get("application_url")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def origin(self) -> typing.Optional[builtins.str]:
            '''This determines how IAM Identity Center navigates the user to the target application.

            It can be one of the following values:

            - ``APPLICATION`` : IAM Identity Center redirects the customer to the configured ``ApplicationUrl`` .
            - ``IDENTITY_CENTER`` : IAM Identity Center uses SAML identity-provider initiated authentication to sign the customer directly into a SAML-based application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-application-signinoptions.html#cfn-sso-application-signinoptions-origin
            '''
            result = self._values.get("origin")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SignInOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnAssignmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_arn": "instanceArn",
        "permission_set_arn": "permissionSetArn",
        "principal_id": "principalId",
        "principal_type": "principalType",
        "target_id": "targetId",
        "target_type": "targetType",
    },
)
class CfnAssignmentMixinProps:
    def __init__(
        self,
        *,
        instance_arn: typing.Optional[builtins.str] = None,
        permission_set_arn: typing.Optional[builtins.str] = None,
        principal_id: typing.Optional[builtins.str] = None,
        principal_type: typing.Optional[builtins.str] = None,
        target_id: typing.Optional[builtins.str] = None,
        target_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAssignmentPropsMixin.

        :param instance_arn: The ARN of the IAM Identity Center instance under which the operation will be executed. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param permission_set_arn: The ARN of the permission set.
        :param principal_id: An identifier for an object in IAM Identity Center, such as a user or group. PrincipalIds are GUIDs (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6). For more information about PrincipalIds in IAM Identity Center, see the `IAM Identity Center Identity Store API Reference <https://docs.aws.amazon.com//singlesignon/latest/IdentityStoreAPIReference/welcome.html>`_ .
        :param principal_type: The entity type for which the assignment will be created.
        :param target_id: TargetID is an AWS account identifier, (For example, 123456789012).
        :param target_type: The entity type for which the assignment will be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
            
            cfn_assignment_mixin_props = sso_mixins.CfnAssignmentMixinProps(
                instance_arn="instanceArn",
                permission_set_arn="permissionSetArn",
                principal_id="principalId",
                principal_type="principalType",
                target_id="targetId",
                target_type="targetType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e43dba2e58e3da11a375f0f8a05d1559ffdb5f4281d3ffd3c58502ee30695a)
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument permission_set_arn", value=permission_set_arn, expected_type=type_hints["permission_set_arn"])
            check_type(argname="argument principal_id", value=principal_id, expected_type=type_hints["principal_id"])
            check_type(argname="argument principal_type", value=principal_type, expected_type=type_hints["principal_type"])
            check_type(argname="argument target_id", value=target_id, expected_type=type_hints["target_id"])
            check_type(argname="argument target_type", value=target_type, expected_type=type_hints["target_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if permission_set_arn is not None:
            self._values["permission_set_arn"] = permission_set_arn
        if principal_id is not None:
            self._values["principal_id"] = principal_id
        if principal_type is not None:
            self._values["principal_type"] = principal_type
        if target_id is not None:
            self._values["target_id"] = target_id
        if target_type is not None:
            self._values["target_type"] = target_type

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permission_set_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the permission set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-permissionsetarn
        '''
        result = self._values.get("permission_set_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_id(self) -> typing.Optional[builtins.str]:
        '''An identifier for an object in IAM Identity Center, such as a user or group.

        PrincipalIds are GUIDs (For example, f81d4fae-7dec-11d0-a765-00a0c91e6bf6). For more information about PrincipalIds in IAM Identity Center, see the `IAM Identity Center Identity Store API Reference <https://docs.aws.amazon.com//singlesignon/latest/IdentityStoreAPIReference/welcome.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principalid
        '''
        result = self._values.get("principal_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal_type(self) -> typing.Optional[builtins.str]:
        '''The entity type for which the assignment will be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-principaltype
        '''
        result = self._values.get("principal_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_id(self) -> typing.Optional[builtins.str]:
        '''TargetID is an AWS account identifier, (For example, 123456789012).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targetid
        '''
        result = self._values.get("target_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_type(self) -> typing.Optional[builtins.str]:
        '''The entity type for which the assignment will be created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html#cfn-sso-assignment-targettype
        '''
        result = self._values.get("target_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssignmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAssignmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnAssignmentPropsMixin",
):
    '''Assigns access to a Principal for a specified AWS account using a specified permission set.

    .. epigraph::

       The term *principal* here refers to a user or group that is defined in IAM Identity Center .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html
    :cloudformationResource: AWS::SSO::Assignment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
        
        cfn_assignment_props_mixin = sso_mixins.CfnAssignmentPropsMixin(sso_mixins.CfnAssignmentMixinProps(
            instance_arn="instanceArn",
            permission_set_arn="permissionSetArn",
            principal_id="principalId",
            principal_type="principalType",
            target_id="targetId",
            target_type="targetType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAssignmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSO::Assignment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afaff995987cf802ac6395e41f6d5c1a7d700c087ea175da9b9f3bc419f44942)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a262a6b2d24fabdfd3e09d05fd9851a9f57e4eb6e6d7f43c50f17bb51842fc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ab1b5ca6b3cb1c2e5bb4004fc7224374231bc59be2a4723ac5cde00065fea16)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAssignmentMixinProps:
        return typing.cast(CfnAssignmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstanceAccessControlAttributeConfigurationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_control_attributes": "accessControlAttributes",
        "instance_access_control_attribute_configuration": "instanceAccessControlAttributeConfiguration",
        "instance_arn": "instanceArn",
    },
)
class CfnInstanceAccessControlAttributeConfigurationMixinProps:
    def __init__(
        self,
        *,
        access_control_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        instance_access_control_attribute_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnInstanceAccessControlAttributeConfigurationPropsMixin.

        :param access_control_attributes: Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance.
        :param instance_access_control_attribute_configuration: (deprecated) The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes. We recomend that you use AccessControlAttributes property instead.
        :param instance_arn: The ARN of the IAM Identity Center instance under which the operation will be executed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
            
            cfn_instance_access_control_attribute_configuration_mixin_props = sso_mixins.CfnInstanceAccessControlAttributeConfigurationMixinProps(
                access_control_attributes=[sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty(
                    key="key",
                    value=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                        source=["source"]
                    )
                )],
                instance_access_control_attribute_configuration=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty(
                    access_control_attributes=[sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty(
                        key="key",
                        value=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                            source=["source"]
                        )
                    )]
                ),
                instance_arn="instanceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64059a91aa855429917801a59d1bf29901816bc3fdfcdcb4bf84719d25948cbf)
            check_type(argname="argument access_control_attributes", value=access_control_attributes, expected_type=type_hints["access_control_attributes"])
            check_type(argname="argument instance_access_control_attribute_configuration", value=instance_access_control_attribute_configuration, expected_type=type_hints["instance_access_control_attribute_configuration"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_control_attributes is not None:
            self._values["access_control_attributes"] = access_control_attributes
        if instance_access_control_attribute_configuration is not None:
            self._values["instance_access_control_attribute_configuration"] = instance_access_control_attribute_configuration
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn

    @builtins.property
    def access_control_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty"]]]]:
        '''Lists the attributes that are configured for ABAC in the specified IAM Identity Center instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html#cfn-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributes
        '''
        result = self._values.get("access_control_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty"]]]], result)

    @builtins.property
    def instance_access_control_attribute_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty"]]:
        '''(deprecated) The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes.

        We recomend that you use  AccessControlAttributes property instead.

        :deprecated: this property has been deprecated

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html#cfn-sso-instanceaccesscontrolattributeconfiguration-instanceaccesscontrolattributeconfiguration
        :stability: deprecated
        '''
        result = self._values.get("instance_access_control_attribute_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty"]], result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html#cfn-sso-instanceaccesscontrolattributeconfiguration-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceAccessControlAttributeConfigurationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnInstanceAccessControlAttributeConfigurationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin",
):
    '''Enables the attribute-based access control (ABAC) feature for the specified IAM Identity Center instance.

    You can also specify new attributes to add to your ABAC configuration during the enabling process. For more information about ABAC, see `Attribute-Based Access Control <https://docs.aws.amazon.com//singlesignon/latest/userguide/abac.html>`_ in the *IAM Identity Center User Guide* .
    .. epigraph::

       The ``InstanceAccessControlAttributeConfiguration`` property has been deprecated but is still supported for backwards compatibility purposes. We recommend that you use the ``AccessControlAttributes`` property instead.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instanceaccesscontrolattributeconfiguration.html
    :cloudformationResource: AWS::SSO::InstanceAccessControlAttributeConfiguration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
        
        cfn_instance_access_control_attribute_configuration_props_mixin = sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin(sso_mixins.CfnInstanceAccessControlAttributeConfigurationMixinProps(
            access_control_attributes=[sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty(
                key="key",
                value=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                    source=["source"]
                )
            )],
            instance_access_control_attribute_configuration=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty(
                access_control_attributes=[sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty(
                    key="key",
                    value=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                        source=["source"]
                    )
                )]
            ),
            instance_arn="instanceArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnInstanceAccessControlAttributeConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSO::InstanceAccessControlAttributeConfiguration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab5b8fc24229ea66b03cde556be83261818cb9f2a65595d0f2741805119068c8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__659a5f96736b755fbc5b61c317f03ae23babdd6ef5635f9abcb4599e29d4c99b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a252c90861e97465002a3c73f55bc35f32419f737ac52a7ce6f857ecb5d2d85)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnInstanceAccessControlAttributeConfigurationMixinProps:
        return typing.cast(CfnInstanceAccessControlAttributeConfigurationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class AccessControlAttributeProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''These are IAM Identity Center identity store attributes that you can configure for use in attributes-based access control (ABAC).

            You can create permissions policies that determine who can access your AWS resources based upon the configured attribute values. When you enable ABAC and specify ``AccessControlAttributes`` , IAM Identity Center passes the attribute values of the authenticated user into IAM for use in policy evaluation.

            :param key: The name of the attribute associated with your identities in your identity source. This is used to map a specified attribute in your identity source with an attribute in IAM Identity Center .
            :param value: The value used for mapping a specified attribute to an identity source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                access_control_attribute_property = sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty(
                    key="key",
                    value=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                        source=["source"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe2b43fde08426054b3087464c07ac2c554b9368f477a680002405074ca45e91)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name of the attribute associated with your identities in your identity source.

            This is used to map a specified attribute in your identity source with an attribute in IAM Identity Center .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattribute.html#cfn-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattribute-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty"]]:
            '''The value used for mapping a specified attribute to an identity source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattribute.html#cfn-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessControlAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source"},
    )
    class AccessControlAttributeValueProperty:
        def __init__(
            self,
            *,
            source: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The value used for mapping a specified attribute to an identity source.

            :param source: The identity source to use when mapping a specified attribute to IAM Identity Center .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributevalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                access_control_attribute_value_property = sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                    source=["source"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e292b34137c572db9ec7fad2142888423eb345da16eb5338d921a814688d7057)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def source(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The identity source to use when mapping a specified attribute to IAM Identity Center .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributevalue.html#cfn-sso-instanceaccesscontrolattributeconfiguration-accesscontrolattributevalue-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessControlAttributeValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"access_control_attributes": "accessControlAttributes"},
    )
    class InstanceAccessControlAttributeConfigurationProperty:
        def __init__(
            self,
            *,
            access_control_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The InstanceAccessControlAttributeConfiguration property has been deprecated but is still supported for backwards compatibility purposes.

            We recomend that you use  AccessControlAttributes property instead.

            :param access_control_attributes: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-instanceaccesscontrolattributeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                instance_access_control_attribute_configuration_property = sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty(
                    access_control_attributes=[sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty(
                        key="key",
                        value=sso_mixins.CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty(
                            source=["source"]
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4ff604df46463fdb79e5e64b38c10add6da472a8438c113c06deb154fc72a57)
                check_type(argname="argument access_control_attributes", value=access_control_attributes, expected_type=type_hints["access_control_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_control_attributes is not None:
                self._values["access_control_attributes"] = access_control_attributes

        @builtins.property
        def access_control_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty"]]]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-instanceaccesscontrolattributeconfiguration-instanceaccesscontrolattributeconfiguration.html#cfn-sso-instanceaccesscontrolattributeconfiguration-instanceaccesscontrolattributeconfiguration-accesscontrolattributes
            '''
            result = self._values.get("access_control_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InstanceAccessControlAttributeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstanceMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags"},
)
class CfnInstanceMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnInstancePropsMixin.

        :param name: The name of the Identity Center instance.
        :param tags: Specifies tags to be attached to the instance of IAM Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
            
            cfn_instance_mixin_props = sso_mixins.CfnInstanceMixinProps(
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f98ad37f13eec0fce3062f844b6e41e8db556c2703a836087a1ed7573c0a062)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the Identity Center instance.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instance.html#cfn-sso-instance-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Specifies tags to be attached to the instance of IAM Identity Center.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instance.html#cfn-sso-instance-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnInstancePropsMixin",
):
    '''Creates an instance of IAM Identity Center for a standalone AWS account that is not managed by AWS Organizations or a member AWS account in an organization.

    You can create only one instance per account and across all AWS Regions .

    The CreateInstance request is rejected if the following apply:

    - The instance is created within the organization management account.
    - An instance already exists in the same account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-instance.html
    :cloudformationResource: AWS::SSO::Instance
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
        
        cfn_instance_props_mixin = sso_mixins.CfnInstancePropsMixin(sso_mixins.CfnInstanceMixinProps(
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
        props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSO::Instance``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e451232d79af32b37a336fbc85b839df609bb288559daae5769b3875fb4fd5ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dc7b7b7ad43e679b13aef2f24e28f1c862facaebc64bf59bb97847dd04326cf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10804232e254a555dbd6f4c3e534cae35c4ad82a79254655237ad3daa6cd0f3)
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
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnPermissionSetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "customer_managed_policy_references": "customerManagedPolicyReferences",
        "description": "description",
        "inline_policy": "inlinePolicy",
        "instance_arn": "instanceArn",
        "managed_policies": "managedPolicies",
        "name": "name",
        "permissions_boundary": "permissionsBoundary",
        "relay_state_type": "relayStateType",
        "session_duration": "sessionDuration",
        "tags": "tags",
    },
)
class CfnPermissionSetMixinProps:
    def __init__(
        self,
        *,
        customer_managed_policy_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        inline_policy: typing.Any = None,
        instance_arn: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionSetPropsMixin.PermissionsBoundaryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        relay_state_type: typing.Optional[builtins.str] = None,
        session_duration: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPermissionSetPropsMixin.

        :param customer_managed_policy_references: Specifies the names and paths of the customer managed policies that you have attached to your permission set.
        :param description: The description of the ``PermissionSet`` .
        :param inline_policy: The inline policy that is attached to the permission set. .. epigraph:: For ``Length Constraints`` , if a valid ARN is provided for a permission set, it is possible for an empty inline policy to be returned.
        :param instance_arn: The ARN of the IAM Identity Center instance under which the operation will be executed. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param managed_policies: A structure that stores a list of managed policy ARNs that describe the associated AWS managed policy.
        :param name: The name of the permission set.
        :param permissions_boundary: Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary. Specify either ``CustomerManagedPolicyReference`` to use the name and path of a customer managed policy, or ``ManagedPolicyArn`` to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* . .. epigraph:: Policies used as permissions boundaries don't provide permissions. You must also attach an IAM policy to the role. To learn how the effective permissions for a role are evaluated, see `IAM JSON policy evaluation logic <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`_ in the *IAM User Guide* .
        :param relay_state_type: Used to redirect users within the application during the federation authentication process.
        :param session_duration: The length of time that the application user sessions are valid for in the ISO-8601 standard.
        :param tags: The tags to attach to the new ``PermissionSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
            
            # inline_policy: Any
            
            cfn_permission_set_mixin_props = sso_mixins.CfnPermissionSetMixinProps(
                customer_managed_policy_references=[sso_mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty(
                    name="name",
                    path="path"
                )],
                description="description",
                inline_policy=inline_policy,
                instance_arn="instanceArn",
                managed_policies=["managedPolicies"],
                name="name",
                permissions_boundary=sso_mixins.CfnPermissionSetPropsMixin.PermissionsBoundaryProperty(
                    customer_managed_policy_reference=sso_mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty(
                        name="name",
                        path="path"
                    ),
                    managed_policy_arn="managedPolicyArn"
                ),
                relay_state_type="relayStateType",
                session_duration="sessionDuration",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a03d6019e674558b52ef1b19a00dacce58fb98f534f1844fe55f18b2ac9ea2)
            check_type(argname="argument customer_managed_policy_references", value=customer_managed_policy_references, expected_type=type_hints["customer_managed_policy_references"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inline_policy", value=inline_policy, expected_type=type_hints["inline_policy"])
            check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument relay_state_type", value=relay_state_type, expected_type=type_hints["relay_state_type"])
            check_type(argname="argument session_duration", value=session_duration, expected_type=type_hints["session_duration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if customer_managed_policy_references is not None:
            self._values["customer_managed_policy_references"] = customer_managed_policy_references
        if description is not None:
            self._values["description"] = description
        if inline_policy is not None:
            self._values["inline_policy"] = inline_policy
        if instance_arn is not None:
            self._values["instance_arn"] = instance_arn
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if name is not None:
            self._values["name"] = name
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if relay_state_type is not None:
            self._values["relay_state_type"] = relay_state_type
        if session_duration is not None:
            self._values["session_duration"] = session_duration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def customer_managed_policy_references(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty"]]]]:
        '''Specifies the names and paths of the customer managed policies that you have attached to your permission set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-customermanagedpolicyreferences
        '''
        result = self._values.get("customer_managed_policy_references")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty"]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ``PermissionSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_policy(self) -> typing.Any:
        '''The inline policy that is attached to the permission set.

        .. epigraph::

           For ``Length Constraints`` , if a valid ARN is provided for a permission set, it is possible for an empty inline policy to be returned.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-inlinepolicy
        '''
        result = self._values.get("inline_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def instance_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM Identity Center instance under which the operation will be executed.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-instancearn
        '''
        result = self._values.get("instance_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A structure that stores a list of managed policy ARNs that describe the associated AWS managed policy.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-managedpolicies
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the permission set.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionSetPropsMixin.PermissionsBoundaryProperty"]]:
        '''Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary.

        Specify either ``CustomerManagedPolicyReference`` to use the name and path of a customer managed policy, or ``ManagedPolicyArn`` to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
        .. epigraph::

           Policies used as permissions boundaries don't provide permissions. You must also attach an IAM policy to the role. To learn how the effective permissions for a role are evaluated, see `IAM JSON policy evaluation logic <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`_ in the *IAM User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionSetPropsMixin.PermissionsBoundaryProperty"]], result)

    @builtins.property
    def relay_state_type(self) -> typing.Optional[builtins.str]:
        '''Used to redirect users within the application during the federation authentication process.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-relaystatetype
        '''
        result = self._values.get("relay_state_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_duration(self) -> typing.Optional[builtins.str]:
        '''The length of time that the application user sessions are valid for in the ISO-8601 standard.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-sessionduration
        '''
        result = self._values.get("session_duration")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to attach to the new ``PermissionSet`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html#cfn-sso-permissionset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionSetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPermissionSetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnPermissionSetPropsMixin",
):
    '''Specifies a permission set within a specified IAM Identity Center instance.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-permissionset.html
    :cloudformationResource: AWS::SSO::PermissionSet
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
        
        # inline_policy: Any
        
        cfn_permission_set_props_mixin = sso_mixins.CfnPermissionSetPropsMixin(sso_mixins.CfnPermissionSetMixinProps(
            customer_managed_policy_references=[sso_mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty(
                name="name",
                path="path"
            )],
            description="description",
            inline_policy=inline_policy,
            instance_arn="instanceArn",
            managed_policies=["managedPolicies"],
            name="name",
            permissions_boundary=sso_mixins.CfnPermissionSetPropsMixin.PermissionsBoundaryProperty(
                customer_managed_policy_reference=sso_mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty(
                    name="name",
                    path="path"
                ),
                managed_policy_arn="managedPolicyArn"
            ),
            relay_state_type="relayStateType",
            session_duration="sessionDuration",
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
        props: typing.Union[CfnPermissionSetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::SSO::PermissionSet``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a6c23ef716564317364a6f3e8cc8bb88a6c82ed74049ffcd9f27714e8c376d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdbb3b1edde0efa984a440f80d84f5f2a3cb2181612d4ad3105e1c74a208416c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f81be4254278e2a42ff56f38a04a11a2285440c457792274d529a19469e70b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPermissionSetMixinProps:
        return typing.cast(CfnPermissionSetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "path": "path"},
    )
    class CustomerManagedPolicyReferenceProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the name and path of a customer managed policy.

            You must have an IAM policy that matches the name and path in each AWS account where you want to deploy your permission set.

            :param name: The name of the IAM policy that you have configured in each account where you want to deploy your permission set.
            :param path: The path to the IAM policy that you have configured in each account where you want to deploy your permission set. The default is ``/`` . For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-permissionset-customermanagedpolicyreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                customer_managed_policy_reference_property = sso_mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty(
                    name="name",
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f44e02aef58c381c961c86b9846449c79d58a8e7d825dbec7c5a85e095b28d05)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the IAM policy that you have configured in each account where you want to deploy your permission set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-permissionset-customermanagedpolicyreference.html#cfn-sso-permissionset-customermanagedpolicyreference-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The path to the IAM policy that you have configured in each account where you want to deploy your permission set.

            The default is ``/`` . For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-permissionset-customermanagedpolicyreference.html#cfn-sso-permissionset-customermanagedpolicyreference-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomerManagedPolicyReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_sso.mixins.CfnPermissionSetPropsMixin.PermissionsBoundaryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "customer_managed_policy_reference": "customerManagedPolicyReference",
            "managed_policy_arn": "managedPolicyArn",
        },
    )
    class PermissionsBoundaryProperty:
        def __init__(
            self,
            *,
            customer_managed_policy_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            managed_policy_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of the AWS managed or customer managed policy that you want to set as a permissions boundary.

            Specify either ``CustomerManagedPolicyReference`` to use the name and path of a customer managed policy, or ``ManagedPolicyArn`` to use the ARN of an AWS managed policy. A permissions boundary represents the maximum permissions that any policy can grant your role. For more information, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
            .. epigraph::

               Policies used as permissions boundaries don't provide permissions. You must also attach an IAM policy to the role. To learn how the effective permissions for a role are evaluated, see `IAM JSON policy evaluation logic <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html>`_ in the *IAM User Guide* .

            :param customer_managed_policy_reference: Specifies the name and path of a customer managed policy. You must have an IAM policy that matches the name and path in each AWS account where you want to deploy your permission set.
            :param managed_policy_arn: The AWS managed policy ARN that you want to attach to a permission set as a permissions boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-permissionset-permissionsboundary.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_sso import mixins as sso_mixins
                
                permissions_boundary_property = sso_mixins.CfnPermissionSetPropsMixin.PermissionsBoundaryProperty(
                    customer_managed_policy_reference=sso_mixins.CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty(
                        name="name",
                        path="path"
                    ),
                    managed_policy_arn="managedPolicyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c5c00abbe2a62dce2d576696ee7de8d7fe829432b5b10309fa287fd053160ff)
                check_type(argname="argument customer_managed_policy_reference", value=customer_managed_policy_reference, expected_type=type_hints["customer_managed_policy_reference"])
                check_type(argname="argument managed_policy_arn", value=managed_policy_arn, expected_type=type_hints["managed_policy_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if customer_managed_policy_reference is not None:
                self._values["customer_managed_policy_reference"] = customer_managed_policy_reference
            if managed_policy_arn is not None:
                self._values["managed_policy_arn"] = managed_policy_arn

        @builtins.property
        def customer_managed_policy_reference(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty"]]:
            '''Specifies the name and path of a customer managed policy.

            You must have an IAM policy that matches the name and path in each AWS account where you want to deploy your permission set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-permissionset-permissionsboundary.html#cfn-sso-permissionset-permissionsboundary-customermanagedpolicyreference
            '''
            result = self._values.get("customer_managed_policy_reference")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty"]], result)

        @builtins.property
        def managed_policy_arn(self) -> typing.Optional[builtins.str]:
            '''The AWS managed policy ARN that you want to attach to a permission set as a permissions boundary.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sso-permissionset-permissionsboundary.html#cfn-sso-permissionset-permissionsboundary-managedpolicyarn
            '''
            result = self._values.get("managed_policy_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PermissionsBoundaryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationAssignmentMixinProps",
    "CfnApplicationAssignmentPropsMixin",
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
    "CfnAssignmentMixinProps",
    "CfnAssignmentPropsMixin",
    "CfnInstanceAccessControlAttributeConfigurationMixinProps",
    "CfnInstanceAccessControlAttributeConfigurationPropsMixin",
    "CfnInstanceMixinProps",
    "CfnInstancePropsMixin",
    "CfnPermissionSetMixinProps",
    "CfnPermissionSetPropsMixin",
]

publication.publish()

def _typecheckingstub__cd019052d7107729c161da0352e4b7c0b48715610cc415ffc7f937c09613d3fc(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    principal_id: typing.Optional[builtins.str] = None,
    principal_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be76bf2d7dc468608b3035a97c7cecb1b22c2c078506e4197c959e97444c0ed(
    props: typing.Union[CfnApplicationAssignmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e57bf186bb6bf2f036cf35050d5ea6d8680306005dae70465353bb5d47f9516a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113a3efc2352acb0de2cfae2bff292bfb2b05084ec7d5fb63031845e2412d768(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74c478664936b133a4b7cb4c980eb0bb1d9715837b4c7084bf3bbde7b9889a4(
    *,
    application_provider_arn: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    portal_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.PortalOptionsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11abf81294a3e3dbf2c006b34cc6fa6327a089ffc978b6633faf0168c5ec4560(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736b6fd4155b6669276183943c08f74d655529e2eee6583c51cd11477a50ba75(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5633e1c4f675927ee31abcbb6d8f2ebf45acb5e43e258a25967aff29663f13f0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856a127b64a095fb9ea6035b8026536276a497fef3bf10c5f2ce40aa8626ecd0(
    *,
    sign_in_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.SignInOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    visibility: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbaa22d331a376b97e1e4d0bb27373c429293a8adb165b66f6b0d4608c8037a0(
    *,
    application_url: typing.Optional[builtins.str] = None,
    origin: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e43dba2e58e3da11a375f0f8a05d1559ffdb5f4281d3ffd3c58502ee30695a(
    *,
    instance_arn: typing.Optional[builtins.str] = None,
    permission_set_arn: typing.Optional[builtins.str] = None,
    principal_id: typing.Optional[builtins.str] = None,
    principal_type: typing.Optional[builtins.str] = None,
    target_id: typing.Optional[builtins.str] = None,
    target_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afaff995987cf802ac6395e41f6d5c1a7d700c087ea175da9b9f3bc419f44942(
    props: typing.Union[CfnAssignmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a262a6b2d24fabdfd3e09d05fd9851a9f57e4eb6e6d7f43c50f17bb51842fc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ab1b5ca6b3cb1c2e5bb4004fc7224374231bc59be2a4723ac5cde00065fea16(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64059a91aa855429917801a59d1bf29901816bc3fdfcdcb4bf84719d25948cbf(
    *,
    access_control_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    instance_access_control_attribute_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceAccessControlAttributeConfigurationPropsMixin.InstanceAccessControlAttributeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab5b8fc24229ea66b03cde556be83261818cb9f2a65595d0f2741805119068c8(
    props: typing.Union[CfnInstanceAccessControlAttributeConfigurationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659a5f96736b755fbc5b61c317f03ae23babdd6ef5635f9abcb4599e29d4c99b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a252c90861e97465002a3c73f55bc35f32419f737ac52a7ce6f857ecb5d2d85(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2b43fde08426054b3087464c07ac2c554b9368f477a680002405074ca45e91(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeValueProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e292b34137c572db9ec7fad2142888423eb345da16eb5338d921a814688d7057(
    *,
    source: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ff604df46463fdb79e5e64b38c10add6da472a8438c113c06deb154fc72a57(
    *,
    access_control_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnInstanceAccessControlAttributeConfigurationPropsMixin.AccessControlAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f98ad37f13eec0fce3062f844b6e41e8db556c2703a836087a1ed7573c0a062(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e451232d79af32b37a336fbc85b839df609bb288559daae5769b3875fb4fd5ae(
    props: typing.Union[CfnInstanceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc7b7b7ad43e679b13aef2f24e28f1c862facaebc64bf59bb97847dd04326cf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10804232e254a555dbd6f4c3e534cae35c4ad82a79254655237ad3daa6cd0f3(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a03d6019e674558b52ef1b19a00dacce58fb98f534f1844fe55f18b2ac9ea2(
    *,
    customer_managed_policy_references: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    inline_policy: typing.Any = None,
    instance_arn: typing.Optional[builtins.str] = None,
    managed_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionSetPropsMixin.PermissionsBoundaryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    relay_state_type: typing.Optional[builtins.str] = None,
    session_duration: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a6c23ef716564317364a6f3e8cc8bb88a6c82ed74049ffcd9f27714e8c376d9(
    props: typing.Union[CfnPermissionSetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdbb3b1edde0efa984a440f80d84f5f2a3cb2181612d4ad3105e1c74a208416c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f81be4254278e2a42ff56f38a04a11a2285440c457792274d529a19469e70b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f44e02aef58c381c961c86b9846449c79d58a8e7d825dbec7c5a85e095b28d05(
    *,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c5c00abbe2a62dce2d576696ee7de8d7fe829432b5b10309fa287fd053160ff(
    *,
    customer_managed_policy_reference: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionSetPropsMixin.CustomerManagedPolicyReferenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    managed_policy_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
