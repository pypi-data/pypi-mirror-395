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
    jsii_type="@aws-cdk/mixins-preview.aws_systemsmanagersap.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "application_type": "applicationType",
        "components_info": "componentsInfo",
        "credentials": "credentials",
        "database_arn": "databaseArn",
        "instances": "instances",
        "sap_instance_number": "sapInstanceNumber",
        "sid": "sid",
        "tags": "tags",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[builtins.str] = None,
        application_type: typing.Optional[builtins.str] = None,
        components_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.ComponentInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CredentialProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        database_arn: typing.Optional[builtins.str] = None,
        instances: typing.Optional[typing.Sequence[builtins.str]] = None,
        sap_instance_number: typing.Optional[builtins.str] = None,
        sid: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_id: The ID of the application.
        :param application_type: The type of the application.
        :param components_info: This is an optional parameter for component details to which the SAP ABAP application is attached, such as Web Dispatcher.
        :param credentials: The credentials of the SAP application.
        :param database_arn: The Amazon Resource Name (ARN) of the database.
        :param instances: The Amazon EC2 instances on which your SAP application is running.
        :param sap_instance_number: The SAP instance number of the application.
        :param sid: The System ID of the application.
        :param tags: The tags on the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_systemsmanagersap import mixins as systemsmanagersap_mixins
            
            cfn_application_mixin_props = systemsmanagersap_mixins.CfnApplicationMixinProps(
                application_id="applicationId",
                application_type="applicationType",
                components_info=[systemsmanagersap_mixins.CfnApplicationPropsMixin.ComponentInfoProperty(
                    component_type="componentType",
                    ec2_instance_id="ec2InstanceId",
                    sid="sid"
                )],
                credentials=[systemsmanagersap_mixins.CfnApplicationPropsMixin.CredentialProperty(
                    credential_type="credentialType",
                    database_name="databaseName",
                    secret_id="secretId"
                )],
                database_arn="databaseArn",
                instances=["instances"],
                sap_instance_number="sapInstanceNumber",
                sid="sid",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84a5dd3fad7a0141d07d35291dfa94da4150574a5c09d2e236879b80673c02ef)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument application_type", value=application_type, expected_type=type_hints["application_type"])
            check_type(argname="argument components_info", value=components_info, expected_type=type_hints["components_info"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument database_arn", value=database_arn, expected_type=type_hints["database_arn"])
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument sap_instance_number", value=sap_instance_number, expected_type=type_hints["sap_instance_number"])
            check_type(argname="argument sid", value=sid, expected_type=type_hints["sid"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if application_type is not None:
            self._values["application_type"] = application_type
        if components_info is not None:
            self._values["components_info"] = components_info
        if credentials is not None:
            self._values["credentials"] = credentials
        if database_arn is not None:
            self._values["database_arn"] = database_arn
        if instances is not None:
            self._values["instances"] = instances
        if sap_instance_number is not None:
            self._values["sap_instance_number"] = sap_instance_number
        if sid is not None:
            self._values["sid"] = sid
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-applicationid
        '''
        result = self._values.get("application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_type(self) -> typing.Optional[builtins.str]:
        '''The type of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-applicationtype
        '''
        result = self._values.get("application_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def components_info(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentInfoProperty"]]]]:
        '''This is an optional parameter for component details to which the SAP ABAP application is attached, such as Web Dispatcher.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-componentsinfo
        '''
        result = self._values.get("components_info")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.ComponentInfoProperty"]]]], result)

    @builtins.property
    def credentials(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CredentialProperty"]]]]:
        '''The credentials of the SAP application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-credentials
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CredentialProperty"]]]], result)

    @builtins.property
    def database_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-databasearn
        '''
        result = self._values.get("database_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instances(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon EC2 instances on which your SAP application is running.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-instances
        '''
        result = self._values.get("instances")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sap_instance_number(self) -> typing.Optional[builtins.str]:
        '''The SAP instance number of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-sapinstancenumber
        '''
        result = self._values.get("sap_instance_number")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sid(self) -> typing.Optional[builtins.str]:
        '''The System ID of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-sid
        '''
        result = self._values.get("sid")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags on the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html#cfn-systemsmanagersap-application-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_systemsmanagersap.mixins.CfnApplicationPropsMixin",
):
    '''An SAP application registered with AWS Systems Manager for SAP.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-systemsmanagersap-application.html
    :cloudformationResource: AWS::SystemsManagerSAP::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_systemsmanagersap import mixins as systemsmanagersap_mixins
        
        cfn_application_props_mixin = systemsmanagersap_mixins.CfnApplicationPropsMixin(systemsmanagersap_mixins.CfnApplicationMixinProps(
            application_id="applicationId",
            application_type="applicationType",
            components_info=[systemsmanagersap_mixins.CfnApplicationPropsMixin.ComponentInfoProperty(
                component_type="componentType",
                ec2_instance_id="ec2InstanceId",
                sid="sid"
            )],
            credentials=[systemsmanagersap_mixins.CfnApplicationPropsMixin.CredentialProperty(
                credential_type="credentialType",
                database_name="databaseName",
                secret_id="secretId"
            )],
            database_arn="databaseArn",
            instances=["instances"],
            sap_instance_number="sapInstanceNumber",
            sid="sid",
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
        '''Create a mixin to apply properties to ``AWS::SystemsManagerSAP::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0346506a5330ad47b7a7bfaf5139f0a34390b251f4b336b67bf6758c9b7babc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e3a8666885e38273a4e6ec10b41cab88ad5981cfad201671a0109b7ef0a3a79)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675b74584dba8908b5ae78b4a685025445f39c0b1250f1acad48def561ddb729)
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
        jsii_type="@aws-cdk/mixins-preview.aws_systemsmanagersap.mixins.CfnApplicationPropsMixin.ComponentInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_type": "componentType",
            "ec2_instance_id": "ec2InstanceId",
            "sid": "sid",
        },
    )
    class ComponentInfoProperty:
        def __init__(
            self,
            *,
            component_type: typing.Optional[builtins.str] = None,
            ec2_instance_id: typing.Optional[builtins.str] = None,
            sid: typing.Optional[builtins.str] = None,
        ) -> None:
            '''This is information about the component of your SAP application, such as Web Dispatcher.

            :param component_type: This string is the type of the component. Accepted value is ``WD`` .
            :param ec2_instance_id: This is the Amazon EC2 instance on which your SAP component is running. Accepted values are alphanumeric.
            :param sid: This string is the SAP System ID of the component. Accepted values are alphanumeric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-componentinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_systemsmanagersap import mixins as systemsmanagersap_mixins
                
                component_info_property = systemsmanagersap_mixins.CfnApplicationPropsMixin.ComponentInfoProperty(
                    component_type="componentType",
                    ec2_instance_id="ec2InstanceId",
                    sid="sid"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb8350c7f0500589d891965ccd10734a40c43085f446ff5f655bc9983ed4b544)
                check_type(argname="argument component_type", value=component_type, expected_type=type_hints["component_type"])
                check_type(argname="argument ec2_instance_id", value=ec2_instance_id, expected_type=type_hints["ec2_instance_id"])
                check_type(argname="argument sid", value=sid, expected_type=type_hints["sid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_type is not None:
                self._values["component_type"] = component_type
            if ec2_instance_id is not None:
                self._values["ec2_instance_id"] = ec2_instance_id
            if sid is not None:
                self._values["sid"] = sid

        @builtins.property
        def component_type(self) -> typing.Optional[builtins.str]:
            '''This string is the type of the component.

            Accepted value is ``WD`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-componentinfo.html#cfn-systemsmanagersap-application-componentinfo-componenttype
            '''
            result = self._values.get("component_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ec2_instance_id(self) -> typing.Optional[builtins.str]:
            '''This is the Amazon EC2 instance on which your SAP component is running.

            Accepted values are alphanumeric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-componentinfo.html#cfn-systemsmanagersap-application-componentinfo-ec2instanceid
            '''
            result = self._values.get("ec2_instance_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sid(self) -> typing.Optional[builtins.str]:
            '''This string is the SAP System ID of the component.

            Accepted values are alphanumeric.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-componentinfo.html#cfn-systemsmanagersap-application-componentinfo-sid
            '''
            result = self._values.get("sid")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_systemsmanagersap.mixins.CfnApplicationPropsMixin.CredentialProperty",
        jsii_struct_bases=[],
        name_mapping={
            "credential_type": "credentialType",
            "database_name": "databaseName",
            "secret_id": "secretId",
        },
    )
    class CredentialProperty:
        def __init__(
            self,
            *,
            credential_type: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The credentials of your SAP application.

            :param credential_type: The type of the application credentials.
            :param database_name: The name of the SAP HANA database.
            :param secret_id: The secret ID created in AWS Secrets Manager to store the credentials of the SAP application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_systemsmanagersap import mixins as systemsmanagersap_mixins
                
                credential_property = systemsmanagersap_mixins.CfnApplicationPropsMixin.CredentialProperty(
                    credential_type="credentialType",
                    database_name="databaseName",
                    secret_id="secretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e97b65f8b91a80ddf2c9c54f65d58cd0b10604f7b3a52c7c227e3a5bbaaa8a59)
                check_type(argname="argument credential_type", value=credential_type, expected_type=type_hints["credential_type"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if credential_type is not None:
                self._values["credential_type"] = credential_type
            if database_name is not None:
                self._values["database_name"] = database_name
            if secret_id is not None:
                self._values["secret_id"] = secret_id

        @builtins.property
        def credential_type(self) -> typing.Optional[builtins.str]:
            '''The type of the application credentials.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html#cfn-systemsmanagersap-application-credential-credentialtype
            '''
            result = self._values.get("credential_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the SAP HANA database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html#cfn-systemsmanagersap-application-credential-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_id(self) -> typing.Optional[builtins.str]:
            '''The secret ID created in AWS Secrets Manager to store the credentials of the SAP application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-systemsmanagersap-application-credential.html#cfn-systemsmanagersap-application-credential-secretid
            '''
            result = self._values.get("secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CredentialProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationPropsMixin",
]

publication.publish()

def _typecheckingstub__84a5dd3fad7a0141d07d35291dfa94da4150574a5c09d2e236879b80673c02ef(
    *,
    application_id: typing.Optional[builtins.str] = None,
    application_type: typing.Optional[builtins.str] = None,
    components_info: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.ComponentInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    credentials: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CredentialProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    database_arn: typing.Optional[builtins.str] = None,
    instances: typing.Optional[typing.Sequence[builtins.str]] = None,
    sap_instance_number: typing.Optional[builtins.str] = None,
    sid: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0346506a5330ad47b7a7bfaf5139f0a34390b251f4b336b67bf6758c9b7babc9(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3a8666885e38273a4e6ec10b41cab88ad5981cfad201671a0109b7ef0a3a79(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675b74584dba8908b5ae78b4a685025445f39c0b1250f1acad48def561ddb729(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb8350c7f0500589d891965ccd10734a40c43085f446ff5f655bc9983ed4b544(
    *,
    component_type: typing.Optional[builtins.str] = None,
    ec2_instance_id: typing.Optional[builtins.str] = None,
    sid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97b65f8b91a80ddf2c9c54f65d58cd0b10604f7b3a52c7c227e3a5bbaaa8a59(
    *,
    credential_type: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
