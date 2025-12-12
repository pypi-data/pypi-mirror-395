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
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnChallengeMixinProps",
    jsii_struct_bases=[],
    name_mapping={"connector_arn": "connectorArn", "tags": "tags"},
)
class CfnChallengeMixinProps:
    def __init__(
        self,
        *,
        connector_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnChallengePropsMixin.

        :param connector_arn: The Amazon Resource Name (ARN) of the connector.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-challenge.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
            
            cfn_challenge_mixin_props = pcaconnectorscep_mixins.CfnChallengeMixinProps(
                connector_arn="connectorArn",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a6a6c83728c439ecd86d251ecd848d030930ee192e16f977d13f790ecf8097)
            check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector_arn is not None:
            self._values["connector_arn"] = connector_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connector_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-challenge.html#cfn-pcaconnectorscep-challenge-connectorarn
        '''
        result = self._values.get("connector_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-challenge.html#cfn-pcaconnectorscep-challenge-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChallengeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnChallengePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnChallengePropsMixin",
):
    '''For general-purpose connectors.

    Creates a *challenge password* for the specified connector. The SCEP protocol uses a challenge password to authenticate a request before issuing a certificate from a certificate authority (CA). Your SCEP clients include the challenge password as part of their certificate request to Connector for SCEP. To retrieve the connector Amazon Resource Names (ARNs) for the connectors in your account, call `ListConnectors <https://docs.aws.amazon.com/pca-connector-scep/latest/APIReference/API_ListConnectors.html>`_ .

    To create additional challenge passwords for the connector, call ``CreateChallenge`` again. We recommend frequently rotating your challenge passwords.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-challenge.html
    :cloudformationResource: AWS::PCAConnectorSCEP::Challenge
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
        
        cfn_challenge_props_mixin = pcaconnectorscep_mixins.CfnChallengePropsMixin(pcaconnectorscep_mixins.CfnChallengeMixinProps(
            connector_arn="connectorArn",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnChallengeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCAConnectorSCEP::Challenge``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3a194483d75c42ee2571856865db6a799663d347d10bf7d1634e05af6d42ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__861d051a8a4d189c8be9a08ff97e5b35e6734b856bfad44311bc13e8bf24690b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__657c957e2c78da99c7792a3c212dc617e7ff6ddec2f2307a252e994f9fa3f054)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnChallengeMixinProps:
        return typing.cast(CfnChallengeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnConnectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "mobile_device_management": "mobileDeviceManagement",
        "tags": "tags",
    },
)
class CfnConnectorMixinProps:
    def __init__(
        self,
        *,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        mobile_device_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.MobileDeviceManagementProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnConnectorPropsMixin.

        :param certificate_authority_arn: The Amazon Resource Name (ARN) of the certificate authority associated with the connector.
        :param mobile_device_management: Contains settings relevant to the mobile device management system that you chose for the connector. If you didn't configure ``MobileDeviceManagement`` , then the connector is for general-purpose use and this object is empty.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
            
            cfn_connector_mixin_props = pcaconnectorscep_mixins.CfnConnectorMixinProps(
                certificate_authority_arn="certificateAuthorityArn",
                mobile_device_management=pcaconnectorscep_mixins.CfnConnectorPropsMixin.MobileDeviceManagementProperty(
                    intune=pcaconnectorscep_mixins.CfnConnectorPropsMixin.IntuneConfigurationProperty(
                        azure_application_id="azureApplicationId",
                        domain="domain"
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b6c25c183846a2ea35071715cb7900ed002cd6d56c2baa40251a898a350bad)
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument mobile_device_management", value=mobile_device_management, expected_type=type_hints["mobile_device_management"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if mobile_device_management is not None:
            self._values["mobile_device_management"] = mobile_device_management
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the certificate authority associated with the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-connector.html#cfn-pcaconnectorscep-connector-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mobile_device_management(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.MobileDeviceManagementProperty"]]:
        '''Contains settings relevant to the mobile device management system that you chose for the connector.

        If you didn't configure ``MobileDeviceManagement`` , then the connector is for general-purpose use and this object is empty.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-connector.html#cfn-pcaconnectorscep-connector-mobiledevicemanagement
        '''
        result = self._values.get("mobile_device_management")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.MobileDeviceManagementProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-connector.html#cfn-pcaconnectorscep-connector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConnectorMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnConnectorPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnConnectorPropsMixin",
):
    '''Connector for SCEP is a service that links AWS Private Certificate Authority to your SCEP-enabled devices.

    The connector brokers the exchange of certificates from AWS Private CA to your SCEP-enabled devices and mobile device management systems. The connector is a complex type that contains the connector's configuration settings.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorscep-connector.html
    :cloudformationResource: AWS::PCAConnectorSCEP::Connector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
        
        cfn_connector_props_mixin = pcaconnectorscep_mixins.CfnConnectorPropsMixin(pcaconnectorscep_mixins.CfnConnectorMixinProps(
            certificate_authority_arn="certificateAuthorityArn",
            mobile_device_management=pcaconnectorscep_mixins.CfnConnectorPropsMixin.MobileDeviceManagementProperty(
                intune=pcaconnectorscep_mixins.CfnConnectorPropsMixin.IntuneConfigurationProperty(
                    azure_application_id="azureApplicationId",
                    domain="domain"
                )
            ),
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCAConnectorSCEP::Connector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72117bd7c1bf73abd9e85644ab948055b0bff7096128a6cc512b3aff7aa22483)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f26a43c239eb124826491568aa49d43bfd142d859c0e7f54b11c4af5cc84f20a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fdebd748157657e22f0c09a982709a6db9bbba540acbd57f864b683b6ce12c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnConnectorMixinProps:
        return typing.cast(CfnConnectorMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnConnectorPropsMixin.IntuneConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "azure_application_id": "azureApplicationId",
            "domain": "domain",
        },
    )
    class IntuneConfigurationProperty:
        def __init__(
            self,
            *,
            azure_application_id: typing.Optional[builtins.str] = None,
            domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configuration details for use with Microsoft Intune.

            For information about using Connector for SCEP for Microsoft Intune, see `Using Connector for SCEP for Microsoft Intune <https://docs.aws.amazon.com/privateca/latest/userguide/scep-connector.htmlconnector-for-scep-intune.html>`_ .

            When you use Connector for SCEP for Microsoft Intune, certain functionalities are enabled by accessing Microsoft Intune through the Microsoft API. Your use of the Connector for SCEP and accompanying AWS services doesn't remove your need to have a valid license for your use of the Microsoft Intune service. You should also review the `Microsoft Intune® App Protection Policies <https://docs.aws.amazon.com/https://learn.microsoft.com/en-us/mem/intune/apps/app-protection-policy>`_ .

            :param azure_application_id: The directory (tenant) ID from your Microsoft Entra ID app registration.
            :param domain: The primary domain from your Microsoft Entra ID app registration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-intuneconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
                
                intune_configuration_property = pcaconnectorscep_mixins.CfnConnectorPropsMixin.IntuneConfigurationProperty(
                    azure_application_id="azureApplicationId",
                    domain="domain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e02ad8798e727cbdd2fe1421822989f41d8b2bd3222dd85734bb76a8c5fd2042)
                check_type(argname="argument azure_application_id", value=azure_application_id, expected_type=type_hints["azure_application_id"])
                check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if azure_application_id is not None:
                self._values["azure_application_id"] = azure_application_id
            if domain is not None:
                self._values["domain"] = domain

        @builtins.property
        def azure_application_id(self) -> typing.Optional[builtins.str]:
            '''The directory (tenant) ID from your Microsoft Entra ID app registration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-intuneconfiguration.html#cfn-pcaconnectorscep-connector-intuneconfiguration-azureapplicationid
            '''
            result = self._values.get("azure_application_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain(self) -> typing.Optional[builtins.str]:
            '''The primary domain from your Microsoft Entra ID app registration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-intuneconfiguration.html#cfn-pcaconnectorscep-connector-intuneconfiguration-domain
            '''
            result = self._values.get("domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IntuneConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnConnectorPropsMixin.MobileDeviceManagementProperty",
        jsii_struct_bases=[],
        name_mapping={"intune": "intune"},
    )
    class MobileDeviceManagementProperty:
        def __init__(
            self,
            *,
            intune: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.IntuneConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''If you don't supply a value, by default Connector for SCEP creates a connector for general-purpose use.

            A general-purpose connector is designed to work with clients or endpoints that support the SCEP protocol, except Connector for SCEP for Microsoft Intune. For information about considerations and limitations with using Connector for SCEP, see `Considerations and Limitations <https://docs.aws.amazon.com/privateca/latest/userguide/scep-connector.htmlc4scep-considerations-limitations.html>`_ .

            If you provide an ``IntuneConfiguration`` , Connector for SCEP creates a connector for use with Microsoft Intune, and you manage the challenge passwords using Microsoft Intune. For more information, see `Using Connector for SCEP for Microsoft Intune <https://docs.aws.amazon.com/privateca/latest/userguide/scep-connector.htmlconnector-for-scep-intune.html>`_ .

            :param intune: Configuration settings for use with Microsoft Intune. For information about using Connector for SCEP for Microsoft Intune, see `Using Connector for SCEP for Microsoft Intune <https://docs.aws.amazon.com/privateca/latest/userguide/scep-connector.htmlconnector-for-scep-intune.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-mobiledevicemanagement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
                
                mobile_device_management_property = pcaconnectorscep_mixins.CfnConnectorPropsMixin.MobileDeviceManagementProperty(
                    intune=pcaconnectorscep_mixins.CfnConnectorPropsMixin.IntuneConfigurationProperty(
                        azure_application_id="azureApplicationId",
                        domain="domain"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__380ad513c0addd320535de2511cb3c486c0b48b5c80c0921e9941b69b4f56e7b)
                check_type(argname="argument intune", value=intune, expected_type=type_hints["intune"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if intune is not None:
                self._values["intune"] = intune

        @builtins.property
        def intune(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.IntuneConfigurationProperty"]]:
            '''Configuration settings for use with Microsoft Intune.

            For information about using Connector for SCEP for Microsoft Intune, see `Using Connector for SCEP for Microsoft Intune <https://docs.aws.amazon.com/privateca/latest/userguide/scep-connector.htmlconnector-for-scep-intune.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-mobiledevicemanagement.html#cfn-pcaconnectorscep-connector-mobiledevicemanagement-intune
            '''
            result = self._values.get("intune")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.IntuneConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MobileDeviceManagementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorscep.mixins.CfnConnectorPropsMixin.OpenIdConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audience": "audience",
            "issuer": "issuer",
            "subject": "subject",
        },
    )
    class OpenIdConfigurationProperty:
        def __init__(
            self,
            *,
            audience: typing.Optional[builtins.str] = None,
            issuer: typing.Optional[builtins.str] = None,
            subject: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains OpenID Connect (OIDC) parameters for use with Microsoft Intune.

            For more information about using Connector for SCEP for Microsoft Intune, see `Using Connector for SCEP for Microsoft Intune <https://docs.aws.amazon.com/privateca/latest/userguide/scep-connector.htmlconnector-for-scep-intune.html>`_ .

            :param audience: The audience value to copy into your Microsoft Entra app registration's OIDC.
            :param issuer: The issuer value to copy into your Microsoft Entra app registration's OIDC.
            :param subject: The subject value to copy into your Microsoft Entra app registration's OIDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-openidconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorscep import mixins as pcaconnectorscep_mixins
                
                open_id_configuration_property = pcaconnectorscep_mixins.CfnConnectorPropsMixin.OpenIdConfigurationProperty(
                    audience="audience",
                    issuer="issuer",
                    subject="subject"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e380269285af456b193e03e919ef1f8461749d6074a7813d710e349f9c42eb7)
                check_type(argname="argument audience", value=audience, expected_type=type_hints["audience"])
                check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audience is not None:
                self._values["audience"] = audience
            if issuer is not None:
                self._values["issuer"] = issuer
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def audience(self) -> typing.Optional[builtins.str]:
            '''The audience value to copy into your Microsoft Entra app registration's OIDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-openidconfiguration.html#cfn-pcaconnectorscep-connector-openidconfiguration-audience
            '''
            result = self._values.get("audience")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def issuer(self) -> typing.Optional[builtins.str]:
            '''The issuer value to copy into your Microsoft Entra app registration's OIDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-openidconfiguration.html#cfn-pcaconnectorscep-connector-openidconfiguration-issuer
            '''
            result = self._values.get("issuer")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def subject(self) -> typing.Optional[builtins.str]:
            '''The subject value to copy into your Microsoft Entra app registration's OIDC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorscep-connector-openidconfiguration.html#cfn-pcaconnectorscep-connector-openidconfiguration-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenIdConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnChallengeMixinProps",
    "CfnChallengePropsMixin",
    "CfnConnectorMixinProps",
    "CfnConnectorPropsMixin",
]

publication.publish()

def _typecheckingstub__07a6a6c83728c439ecd86d251ecd848d030930ee192e16f977d13f790ecf8097(
    *,
    connector_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3a194483d75c42ee2571856865db6a799663d347d10bf7d1634e05af6d42ee(
    props: typing.Union[CfnChallengeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861d051a8a4d189c8be9a08ff97e5b35e6734b856bfad44311bc13e8bf24690b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__657c957e2c78da99c7792a3c212dc617e7ff6ddec2f2307a252e994f9fa3f054(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b6c25c183846a2ea35071715cb7900ed002cd6d56c2baa40251a898a350bad(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    mobile_device_management: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.MobileDeviceManagementProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72117bd7c1bf73abd9e85644ab948055b0bff7096128a6cc512b3aff7aa22483(
    props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26a43c239eb124826491568aa49d43bfd142d859c0e7f54b11c4af5cc84f20a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fdebd748157657e22f0c09a982709a6db9bbba540acbd57f864b683b6ce12c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02ad8798e727cbdd2fe1421822989f41d8b2bd3222dd85734bb76a8c5fd2042(
    *,
    azure_application_id: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380ad513c0addd320535de2511cb3c486c0b48b5c80c0921e9941b69b4f56e7b(
    *,
    intune: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.IntuneConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e380269285af456b193e03e919ef1f8461749d6074a7813d710e349f9c42eb7(
    *,
    audience: typing.Optional[builtins.str] = None,
    issuer: typing.Optional[builtins.str] = None,
    subject: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
