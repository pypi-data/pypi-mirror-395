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
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnConnectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "directory_id": "directoryId",
        "tags": "tags",
        "vpc_information": "vpcInformation",
    },
)
class CfnConnectorMixinProps:
    def __init__(
        self,
        *,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        directory_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        vpc_information: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.VpcInformationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnConnectorPropsMixin.

        :param certificate_authority_arn: The Amazon Resource Name (ARN) of the certificate authority being used.
        :param directory_id: The identifier of the Active Directory.
        :param tags: Metadata assigned to a connector consisting of a key-value pair.
        :param vpc_information: Information of the VPC and security group(s) used with the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
            
            cfn_connector_mixin_props = pcaconnectorad_mixins.CfnConnectorMixinProps(
                certificate_authority_arn="certificateAuthorityArn",
                directory_id="directoryId",
                tags={
                    "tags_key": "tags"
                },
                vpc_information=pcaconnectorad_mixins.CfnConnectorPropsMixin.VpcInformationProperty(
                    ip_address_type="ipAddressType",
                    security_group_ids=["securityGroupIds"]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a03772b5f6a0c471823b3e7c865d4af3ec9ce3714cf27c609f875f585fd67d8c)
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_information", value=vpc_information, expected_type=type_hints["vpc_information"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if tags is not None:
            self._values["tags"] = tags
        if vpc_information is not None:
            self._values["vpc_information"] = vpc_information

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the certificate authority being used.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-connector.html#cfn-pcaconnectorad-connector-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Active Directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-connector.html#cfn-pcaconnectorad-connector-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata assigned to a connector consisting of a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-connector.html#cfn-pcaconnectorad-connector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def vpc_information(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.VpcInformationProperty"]]:
        '''Information of the VPC and security group(s) used with the connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-connector.html#cfn-pcaconnectorad-connector-vpcinformation
        '''
        result = self._values.get("vpc_information")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.VpcInformationProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnConnectorPropsMixin",
):
    '''Creates a connector between AWS Private CA and an Active Directory.

    You must specify the private CA, directory ID, and security groups.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-connector.html
    :cloudformationResource: AWS::PCAConnectorAD::Connector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
        
        cfn_connector_props_mixin = pcaconnectorad_mixins.CfnConnectorPropsMixin(pcaconnectorad_mixins.CfnConnectorMixinProps(
            certificate_authority_arn="certificateAuthorityArn",
            directory_id="directoryId",
            tags={
                "tags_key": "tags"
            },
            vpc_information=pcaconnectorad_mixins.CfnConnectorPropsMixin.VpcInformationProperty(
                ip_address_type="ipAddressType",
                security_group_ids=["securityGroupIds"]
            )
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
        '''Create a mixin to apply properties to ``AWS::PCAConnectorAD::Connector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36fa959ddb848f03b7e2169020349fb2483ab07d9b9e65720030f0b5168fe99d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e12d7cdec7d4104d3a55e226e33b4f276994c9ea0d4ecb755f9502d6bd6befa1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd95ce69fc5764a16050950406d13ea3ba6d5c602d2a771a3085184f412a353c)
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
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnConnectorPropsMixin.VpcInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ip_address_type": "ipAddressType",
            "security_group_ids": "securityGroupIds",
        },
    )
    class VpcInformationProperty:
        def __init__(
            self,
            *,
            ip_address_type: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about your VPC and security groups used with the connector.

            :param ip_address_type: The VPC IP address type.
            :param security_group_ids: The security groups used with the connector. You can use a maximum of 4 security groups with a connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-connector-vpcinformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                vpc_information_property = pcaconnectorad_mixins.CfnConnectorPropsMixin.VpcInformationProperty(
                    ip_address_type="ipAddressType",
                    security_group_ids=["securityGroupIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9010df8c182f607bf2bb7c301ba546c2d01a01e4277d8cdd7babc0f8ee936264)
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The VPC IP address type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-connector-vpcinformation.html#cfn-pcaconnectorad-connector-vpcinformation-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security groups used with the connector.

            You can use a maximum of 4 security groups with a connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-connector-vpcinformation.html#cfn-pcaconnectorad-connector-vpcinformation-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnDirectoryRegistrationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"directory_id": "directoryId", "tags": "tags"},
)
class CfnDirectoryRegistrationMixinProps:
    def __init__(
        self,
        *,
        directory_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDirectoryRegistrationPropsMixin.

        :param directory_id: The identifier of the Active Directory.
        :param tags: Metadata assigned to a directory registration consisting of a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-directoryregistration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
            
            cfn_directory_registration_mixin_props = pcaconnectorad_mixins.CfnDirectoryRegistrationMixinProps(
                directory_id="directoryId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb53457a7657b9d094a099dbf5a8732235e33c6ab197e3fa6b4277737f6bd7ae)
            check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if directory_id is not None:
            self._values["directory_id"] = directory_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def directory_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of the Active Directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-directoryregistration.html#cfn-pcaconnectorad-directoryregistration-directoryid
        '''
        result = self._values.get("directory_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata assigned to a directory registration consisting of a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-directoryregistration.html#cfn-pcaconnectorad-directoryregistration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDirectoryRegistrationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDirectoryRegistrationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnDirectoryRegistrationPropsMixin",
):
    '''Creates a directory registration that authorizes communication between AWS Private CA and an Active Directory.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-directoryregistration.html
    :cloudformationResource: AWS::PCAConnectorAD::DirectoryRegistration
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
        
        cfn_directory_registration_props_mixin = pcaconnectorad_mixins.CfnDirectoryRegistrationPropsMixin(pcaconnectorad_mixins.CfnDirectoryRegistrationMixinProps(
            directory_id="directoryId",
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDirectoryRegistrationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCAConnectorAD::DirectoryRegistration``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__022094408102afcf55c5b49df1f4d78186a7bd40804b01942ee22ce0ce14b4b6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4f95bc21e4799d9562cbed48671413c771ef6556283c4ef5409e9f8a999ce18)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34866a2523e8f8c9c75b7ec8a4d6e0764e9eeebbfa6c1c79a92a8e2f1c3aea0a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDirectoryRegistrationMixinProps:
        return typing.cast(CfnDirectoryRegistrationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnServicePrincipalNameMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_arn": "connectorArn",
        "directory_registration_arn": "directoryRegistrationArn",
    },
)
class CfnServicePrincipalNameMixinProps:
    def __init__(
        self,
        *,
        connector_arn: typing.Optional[builtins.str] = None,
        directory_registration_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnServicePrincipalNamePropsMixin.

        :param connector_arn: The Amazon Resource Name (ARN) that was returned when you called `CreateConnector.html <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateConnector.html>`_ .
        :param directory_registration_arn: The Amazon Resource Name (ARN) that was returned when you called `CreateDirectoryRegistration <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateDirectoryRegistration.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-serviceprincipalname.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
            
            cfn_service_principal_name_mixin_props = pcaconnectorad_mixins.CfnServicePrincipalNameMixinProps(
                connector_arn="connectorArn",
                directory_registration_arn="directoryRegistrationArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f04fb46542cd265bd4ec409134f949452ed30092ee59a1aee1a089ccee0627e)
            check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
            check_type(argname="argument directory_registration_arn", value=directory_registration_arn, expected_type=type_hints["directory_registration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector_arn is not None:
            self._values["connector_arn"] = connector_arn
        if directory_registration_arn is not None:
            self._values["directory_registration_arn"] = directory_registration_arn

    @builtins.property
    def connector_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that was returned when you called `CreateConnector.html <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateConnector.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-serviceprincipalname.html#cfn-pcaconnectorad-serviceprincipalname-connectorarn
        '''
        result = self._values.get("connector_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def directory_registration_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that was returned when you called `CreateDirectoryRegistration <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateDirectoryRegistration.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-serviceprincipalname.html#cfn-pcaconnectorad-serviceprincipalname-directoryregistrationarn
        '''
        result = self._values.get("directory_registration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServicePrincipalNameMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServicePrincipalNamePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnServicePrincipalNamePropsMixin",
):
    '''Creates a service principal name (SPN) for the service account in Active Directory.

    Kerberos authentication uses SPNs to associate a service instance with a service sign-in account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-serviceprincipalname.html
    :cloudformationResource: AWS::PCAConnectorAD::ServicePrincipalName
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
        
        cfn_service_principal_name_props_mixin = pcaconnectorad_mixins.CfnServicePrincipalNamePropsMixin(pcaconnectorad_mixins.CfnServicePrincipalNameMixinProps(
            connector_arn="connectorArn",
            directory_registration_arn="directoryRegistrationArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServicePrincipalNameMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCAConnectorAD::ServicePrincipalName``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f3bdb69bc52c82947e4308f5be4a7b5fce6b919b2960f1d3229f22fcdfb6b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c160b8ec1ab84cbef79c7baab892562f707f8dc2302475405ae0b08e3f97aa7a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8d32b9fae37db4a5b392d69c6bd3dff7e122d0ef0b193334aa96c67ffccfcc7)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServicePrincipalNameMixinProps:
        return typing.cast(CfnServicePrincipalNameMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplateGroupAccessControlEntryMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_rights": "accessRights",
        "group_display_name": "groupDisplayName",
        "group_security_identifier": "groupSecurityIdentifier",
        "template_arn": "templateArn",
    },
)
class CfnTemplateGroupAccessControlEntryMixinProps:
    def __init__(
        self,
        *,
        access_rights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        group_display_name: typing.Optional[builtins.str] = None,
        group_security_identifier: typing.Optional[builtins.str] = None,
        template_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnTemplateGroupAccessControlEntryPropsMixin.

        :param access_rights: Permissions to allow or deny an Active Directory group to enroll or autoenroll certificates issued against a template.
        :param group_display_name: Name of the Active Directory group. This name does not need to match the group name in Active Directory.
        :param group_security_identifier: Security identifier (SID) of the group object from Active Directory. The SID starts with "S-".
        :param template_arn: The Amazon Resource Name (ARN) that was returned when you called `CreateTemplate <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateTemplate.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-templategroupaccesscontrolentry.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
            
            cfn_template_group_access_control_entry_mixin_props = pcaconnectorad_mixins.CfnTemplateGroupAccessControlEntryMixinProps(
                access_rights=pcaconnectorad_mixins.CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty(
                    auto_enroll="autoEnroll",
                    enroll="enroll"
                ),
                group_display_name="groupDisplayName",
                group_security_identifier="groupSecurityIdentifier",
                template_arn="templateArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0a5be10a66495b6a37132fb0eec5c9caeb53d1f4610733177239afdca09e47)
            check_type(argname="argument access_rights", value=access_rights, expected_type=type_hints["access_rights"])
            check_type(argname="argument group_display_name", value=group_display_name, expected_type=type_hints["group_display_name"])
            check_type(argname="argument group_security_identifier", value=group_security_identifier, expected_type=type_hints["group_security_identifier"])
            check_type(argname="argument template_arn", value=template_arn, expected_type=type_hints["template_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_rights is not None:
            self._values["access_rights"] = access_rights
        if group_display_name is not None:
            self._values["group_display_name"] = group_display_name
        if group_security_identifier is not None:
            self._values["group_security_identifier"] = group_security_identifier
        if template_arn is not None:
            self._values["template_arn"] = template_arn

    @builtins.property
    def access_rights(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty"]]:
        '''Permissions to allow or deny an Active Directory group to enroll or autoenroll certificates issued against a template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-templategroupaccesscontrolentry.html#cfn-pcaconnectorad-templategroupaccesscontrolentry-accessrights
        '''
        result = self._values.get("access_rights")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty"]], result)

    @builtins.property
    def group_display_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Active Directory group.

        This name does not need to match the group name in Active Directory.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-templategroupaccesscontrolentry.html#cfn-pcaconnectorad-templategroupaccesscontrolentry-groupdisplayname
        '''
        result = self._values.get("group_display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def group_security_identifier(self) -> typing.Optional[builtins.str]:
        '''Security identifier (SID) of the group object from Active Directory.

        The SID starts with "S-".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-templategroupaccesscontrolentry.html#cfn-pcaconnectorad-templategroupaccesscontrolentry-groupsecurityidentifier
        '''
        result = self._values.get("group_security_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that was returned when you called `CreateTemplate <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateTemplate.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-templategroupaccesscontrolentry.html#cfn-pcaconnectorad-templategroupaccesscontrolentry-templatearn
        '''
        result = self._values.get("template_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTemplateGroupAccessControlEntryMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTemplateGroupAccessControlEntryPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplateGroupAccessControlEntryPropsMixin",
):
    '''Create a group access control entry.

    Allow or deny Active Directory groups from enrolling and/or autoenrolling with the template based on the group security identifiers (SIDs).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-templategroupaccesscontrolentry.html
    :cloudformationResource: AWS::PCAConnectorAD::TemplateGroupAccessControlEntry
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
        
        cfn_template_group_access_control_entry_props_mixin = pcaconnectorad_mixins.CfnTemplateGroupAccessControlEntryPropsMixin(pcaconnectorad_mixins.CfnTemplateGroupAccessControlEntryMixinProps(
            access_rights=pcaconnectorad_mixins.CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty(
                auto_enroll="autoEnroll",
                enroll="enroll"
            ),
            group_display_name="groupDisplayName",
            group_security_identifier="groupSecurityIdentifier",
            template_arn="templateArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTemplateGroupAccessControlEntryMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCAConnectorAD::TemplateGroupAccessControlEntry``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d478aad196f28995118d38b56f55d6fae7335562dc1c79a5fa576d3990cd6841)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31dc11851dc7a807bf879bc7f2e8dcd6da026b98d6ae98e87fd86925d06e1ec5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336bb226dbb1bdfb7d4b5c1a0ddf6a1f58da4077e50f3aff91fa8fe1aa7da851)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTemplateGroupAccessControlEntryMixinProps:
        return typing.cast(CfnTemplateGroupAccessControlEntryMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty",
        jsii_struct_bases=[],
        name_mapping={"auto_enroll": "autoEnroll", "enroll": "enroll"},
    )
    class AccessRightsProperty:
        def __init__(
            self,
            *,
            auto_enroll: typing.Optional[builtins.str] = None,
            enroll: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Allow or deny permissions for an Active Directory group to enroll or autoenroll certificates for a template.

            :param auto_enroll: Allow or deny an Active Directory group from autoenrolling certificates issued against a template. The Active Directory group must be allowed to enroll to allow autoenrollment
            :param enroll: Allow or deny an Active Directory group from enrolling certificates issued against a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-templategroupaccesscontrolentry-accessrights.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                access_rights_property = pcaconnectorad_mixins.CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty(
                    auto_enroll="autoEnroll",
                    enroll="enroll"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__af0ed257143715f3f880e01f1917aeb24bc58d7017842e00e337da4f2e0383c9)
                check_type(argname="argument auto_enroll", value=auto_enroll, expected_type=type_hints["auto_enroll"])
                check_type(argname="argument enroll", value=enroll, expected_type=type_hints["enroll"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_enroll is not None:
                self._values["auto_enroll"] = auto_enroll
            if enroll is not None:
                self._values["enroll"] = enroll

        @builtins.property
        def auto_enroll(self) -> typing.Optional[builtins.str]:
            '''Allow or deny an Active Directory group from autoenrolling certificates issued against a template.

            The Active Directory group must be allowed to enroll to allow autoenrollment

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-templategroupaccesscontrolentry-accessrights.html#cfn-pcaconnectorad-templategroupaccesscontrolentry-accessrights-autoenroll
            '''
            result = self._values.get("auto_enroll")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enroll(self) -> typing.Optional[builtins.str]:
            '''Allow or deny an Active Directory group from enrolling certificates issued against a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-templategroupaccesscontrolentry-accessrights.html#cfn-pcaconnectorad-templategroupaccesscontrolentry-accessrights-enroll
            '''
            result = self._values.get("enroll")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessRightsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "connector_arn": "connectorArn",
        "definition": "definition",
        "name": "name",
        "reenroll_all_certificate_holders": "reenrollAllCertificateHolders",
        "tags": "tags",
    },
)
class CfnTemplateMixinProps:
    def __init__(
        self,
        *,
        connector_arn: typing.Optional[builtins.str] = None,
        definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.TemplateDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        reenroll_all_certificate_holders: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for CfnTemplatePropsMixin.

        :param connector_arn: The Amazon Resource Name (ARN) that was returned when you called `CreateConnector <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateConnector.html>`_ .
        :param definition: Template configuration to define the information included in certificates. Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.
        :param name: Name of the templates. Template names must be unique.
        :param reenroll_all_certificate_holders: This setting allows the major version of a template to be increased automatically. All members of Active Directory groups that are allowed to enroll with a template will receive a new certificate issued using that template.
        :param tags: Metadata assigned to a template consisting of a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
            
            cfn_template_mixin_props = pcaconnectorad_mixins.CfnTemplateMixinProps(
                connector_arn="connectorArn",
                definition=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateDefinitionProperty(
                    template_v2=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV2Property(
                        certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                            renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            ),
                            validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            )
                        ),
                        enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV2Property(
                            enable_key_reuse_on_nt_token_keyset_storage_full=False,
                            include_symmetric_algorithms=False,
                            no_security_extension=False,
                            remove_invalid_certificate_from_personal_store=False,
                            user_interaction_required=False
                        ),
                        extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV2Property(
                            application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                                critical=False,
                                policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                    policy_object_identifier="policyObjectIdentifier",
                                    policy_type="policyType"
                                )]
                            ),
                            key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                                critical=False,
                                usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                    data_encipherment=False,
                                    digital_signature=False,
                                    key_agreement=False,
                                    key_encipherment=False,
                                    non_repudiation=False
                                )
                            )
                        ),
                        general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV2Property(
                            auto_enrollment=False,
                            machine_type=False
                        ),
                        private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV2Property(
                            crypto_providers=["cryptoProviders"],
                            key_spec="keySpec",
                            minimal_key_length=123
                        ),
                        private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV2Property(
                            client_version="clientVersion",
                            exportable_key=False,
                            strong_key_protection_required=False
                        ),
                        subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV2Property(
                            require_common_name=False,
                            require_directory_path=False,
                            require_dns_as_cn=False,
                            require_email=False,
                            san_require_directory_guid=False,
                            san_require_dns=False,
                            san_require_domain_dns=False,
                            san_require_email=False,
                            san_require_spn=False,
                            san_require_upn=False
                        ),
                        superseded_templates=["supersededTemplates"]
                    ),
                    template_v3=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV3Property(
                        certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                            renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            ),
                            validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            )
                        ),
                        enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV3Property(
                            enable_key_reuse_on_nt_token_keyset_storage_full=False,
                            include_symmetric_algorithms=False,
                            no_security_extension=False,
                            remove_invalid_certificate_from_personal_store=False,
                            user_interaction_required=False
                        ),
                        extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV3Property(
                            application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                                critical=False,
                                policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                    policy_object_identifier="policyObjectIdentifier",
                                    policy_type="policyType"
                                )]
                            ),
                            key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                                critical=False,
                                usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                    data_encipherment=False,
                                    digital_signature=False,
                                    key_agreement=False,
                                    key_encipherment=False,
                                    non_repudiation=False
                                )
                            )
                        ),
                        general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV3Property(
                            auto_enrollment=False,
                            machine_type=False
                        ),
                        hash_algorithm="hashAlgorithm",
                        private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV3Property(
                            algorithm="algorithm",
                            crypto_providers=["cryptoProviders"],
                            key_spec="keySpec",
                            key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                                property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                    decrypt=False,
                                    key_agreement=False,
                                    sign=False
                                ),
                                property_type="propertyType"
                            ),
                            minimal_key_length=123
                        ),
                        private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV3Property(
                            client_version="clientVersion",
                            exportable_key=False,
                            require_alternate_signature_algorithm=False,
                            strong_key_protection_required=False
                        ),
                        subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV3Property(
                            require_common_name=False,
                            require_directory_path=False,
                            require_dns_as_cn=False,
                            require_email=False,
                            san_require_directory_guid=False,
                            san_require_dns=False,
                            san_require_domain_dns=False,
                            san_require_email=False,
                            san_require_spn=False,
                            san_require_upn=False
                        ),
                        superseded_templates=["supersededTemplates"]
                    ),
                    template_v4=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV4Property(
                        certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                            renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            ),
                            validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            )
                        ),
                        enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV4Property(
                            enable_key_reuse_on_nt_token_keyset_storage_full=False,
                            include_symmetric_algorithms=False,
                            no_security_extension=False,
                            remove_invalid_certificate_from_personal_store=False,
                            user_interaction_required=False
                        ),
                        extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV4Property(
                            application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                                critical=False,
                                policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                    policy_object_identifier="policyObjectIdentifier",
                                    policy_type="policyType"
                                )]
                            ),
                            key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                                critical=False,
                                usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                    data_encipherment=False,
                                    digital_signature=False,
                                    key_agreement=False,
                                    key_encipherment=False,
                                    non_repudiation=False
                                )
                            )
                        ),
                        general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV4Property(
                            auto_enrollment=False,
                            machine_type=False
                        ),
                        hash_algorithm="hashAlgorithm",
                        private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV4Property(
                            algorithm="algorithm",
                            crypto_providers=["cryptoProviders"],
                            key_spec="keySpec",
                            key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                                property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                    decrypt=False,
                                    key_agreement=False,
                                    sign=False
                                ),
                                property_type="propertyType"
                            ),
                            minimal_key_length=123
                        ),
                        private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV4Property(
                            client_version="clientVersion",
                            exportable_key=False,
                            require_alternate_signature_algorithm=False,
                            require_same_key_renewal=False,
                            strong_key_protection_required=False,
                            use_legacy_provider=False
                        ),
                        subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV4Property(
                            require_common_name=False,
                            require_directory_path=False,
                            require_dns_as_cn=False,
                            require_email=False,
                            san_require_directory_guid=False,
                            san_require_dns=False,
                            san_require_domain_dns=False,
                            san_require_email=False,
                            san_require_spn=False,
                            san_require_upn=False
                        ),
                        superseded_templates=["supersededTemplates"]
                    )
                ),
                name="name",
                reenroll_all_certificate_holders=False,
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ed2bb0c68d534f3ccc76ba96205528c4c89758a8e8d61bf380d3cb0f857440b)
            check_type(argname="argument connector_arn", value=connector_arn, expected_type=type_hints["connector_arn"])
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reenroll_all_certificate_holders", value=reenroll_all_certificate_holders, expected_type=type_hints["reenroll_all_certificate_holders"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connector_arn is not None:
            self._values["connector_arn"] = connector_arn
        if definition is not None:
            self._values["definition"] = definition
        if name is not None:
            self._values["name"] = name
        if reenroll_all_certificate_holders is not None:
            self._values["reenroll_all_certificate_holders"] = reenroll_all_certificate_holders
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connector_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) that was returned when you called `CreateConnector <https://docs.aws.amazon.com/pca-connector-ad/latest/APIReference/API_CreateConnector.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html#cfn-pcaconnectorad-template-connectorarn
        '''
        result = self._values.get("connector_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def definition(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateDefinitionProperty"]]:
        '''Template configuration to define the information included in certificates.

        Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html#cfn-pcaconnectorad-template-definition
        '''
        result = self._values.get("definition")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateDefinitionProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Name of the templates.

        Template names must be unique.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html#cfn-pcaconnectorad-template-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reenroll_all_certificate_holders(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''This setting allows the major version of a template to be increased automatically.

        All members of Active Directory groups that are allowed to enroll with a template will receive a new certificate issued using that template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html#cfn-pcaconnectorad-template-reenrollallcertificateholders
        '''
        result = self._values.get("reenroll_all_certificate_holders")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Metadata assigned to a template consisting of a key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html#cfn-pcaconnectorad-template-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTemplateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTemplatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin",
):
    '''Creates an Active Directory compatible certificate template.

    The connectors issues certificates using these templates based on the requester’s Active Directory group membership.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-pcaconnectorad-template.html
    :cloudformationResource: AWS::PCAConnectorAD::Template
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
        
        cfn_template_props_mixin = pcaconnectorad_mixins.CfnTemplatePropsMixin(pcaconnectorad_mixins.CfnTemplateMixinProps(
            connector_arn="connectorArn",
            definition=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateDefinitionProperty(
                template_v2=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV2Property(
                    certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                        renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        ),
                        validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        )
                    ),
                    enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV2Property(
                        enable_key_reuse_on_nt_token_keyset_storage_full=False,
                        include_symmetric_algorithms=False,
                        no_security_extension=False,
                        remove_invalid_certificate_from_personal_store=False,
                        user_interaction_required=False
                    ),
                    extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV2Property(
                        application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                            critical=False,
                            policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                policy_object_identifier="policyObjectIdentifier",
                                policy_type="policyType"
                            )]
                        ),
                        key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                            critical=False,
                            usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                data_encipherment=False,
                                digital_signature=False,
                                key_agreement=False,
                                key_encipherment=False,
                                non_repudiation=False
                            )
                        )
                    ),
                    general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV2Property(
                        auto_enrollment=False,
                        machine_type=False
                    ),
                    private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV2Property(
                        crypto_providers=["cryptoProviders"],
                        key_spec="keySpec",
                        minimal_key_length=123
                    ),
                    private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV2Property(
                        client_version="clientVersion",
                        exportable_key=False,
                        strong_key_protection_required=False
                    ),
                    subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV2Property(
                        require_common_name=False,
                        require_directory_path=False,
                        require_dns_as_cn=False,
                        require_email=False,
                        san_require_directory_guid=False,
                        san_require_dns=False,
                        san_require_domain_dns=False,
                        san_require_email=False,
                        san_require_spn=False,
                        san_require_upn=False
                    ),
                    superseded_templates=["supersededTemplates"]
                ),
                template_v3=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV3Property(
                    certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                        renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        ),
                        validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        )
                    ),
                    enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV3Property(
                        enable_key_reuse_on_nt_token_keyset_storage_full=False,
                        include_symmetric_algorithms=False,
                        no_security_extension=False,
                        remove_invalid_certificate_from_personal_store=False,
                        user_interaction_required=False
                    ),
                    extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV3Property(
                        application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                            critical=False,
                            policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                policy_object_identifier="policyObjectIdentifier",
                                policy_type="policyType"
                            )]
                        ),
                        key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                            critical=False,
                            usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                data_encipherment=False,
                                digital_signature=False,
                                key_agreement=False,
                                key_encipherment=False,
                                non_repudiation=False
                            )
                        )
                    ),
                    general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV3Property(
                        auto_enrollment=False,
                        machine_type=False
                    ),
                    hash_algorithm="hashAlgorithm",
                    private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV3Property(
                        algorithm="algorithm",
                        crypto_providers=["cryptoProviders"],
                        key_spec="keySpec",
                        key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                            property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                decrypt=False,
                                key_agreement=False,
                                sign=False
                            ),
                            property_type="propertyType"
                        ),
                        minimal_key_length=123
                    ),
                    private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV3Property(
                        client_version="clientVersion",
                        exportable_key=False,
                        require_alternate_signature_algorithm=False,
                        strong_key_protection_required=False
                    ),
                    subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV3Property(
                        require_common_name=False,
                        require_directory_path=False,
                        require_dns_as_cn=False,
                        require_email=False,
                        san_require_directory_guid=False,
                        san_require_dns=False,
                        san_require_domain_dns=False,
                        san_require_email=False,
                        san_require_spn=False,
                        san_require_upn=False
                    ),
                    superseded_templates=["supersededTemplates"]
                ),
                template_v4=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV4Property(
                    certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                        renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        ),
                        validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        )
                    ),
                    enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV4Property(
                        enable_key_reuse_on_nt_token_keyset_storage_full=False,
                        include_symmetric_algorithms=False,
                        no_security_extension=False,
                        remove_invalid_certificate_from_personal_store=False,
                        user_interaction_required=False
                    ),
                    extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV4Property(
                        application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                            critical=False,
                            policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                policy_object_identifier="policyObjectIdentifier",
                                policy_type="policyType"
                            )]
                        ),
                        key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                            critical=False,
                            usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                data_encipherment=False,
                                digital_signature=False,
                                key_agreement=False,
                                key_encipherment=False,
                                non_repudiation=False
                            )
                        )
                    ),
                    general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV4Property(
                        auto_enrollment=False,
                        machine_type=False
                    ),
                    hash_algorithm="hashAlgorithm",
                    private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV4Property(
                        algorithm="algorithm",
                        crypto_providers=["cryptoProviders"],
                        key_spec="keySpec",
                        key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                            property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                decrypt=False,
                                key_agreement=False,
                                sign=False
                            ),
                            property_type="propertyType"
                        ),
                        minimal_key_length=123
                    ),
                    private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV4Property(
                        client_version="clientVersion",
                        exportable_key=False,
                        require_alternate_signature_algorithm=False,
                        require_same_key_renewal=False,
                        strong_key_protection_required=False,
                        use_legacy_provider=False
                    ),
                    subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV4Property(
                        require_common_name=False,
                        require_directory_path=False,
                        require_dns_as_cn=False,
                        require_email=False,
                        san_require_directory_guid=False,
                        san_require_dns=False,
                        san_require_domain_dns=False,
                        san_require_email=False,
                        san_require_spn=False,
                        san_require_upn=False
                    ),
                    superseded_templates=["supersededTemplates"]
                )
            ),
            name="name",
            reenroll_all_certificate_holders=False,
            tags={
                "tags_key": "tags"
            }
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PCAConnectorAD::Template``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5581ecc0fa3254b75efdbfab8ae0f1982a0ed629d4e056bde6dd13c429ef8b9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af7629f9a526847b0e24578e5063a4532b800fdf2a5e97bca78b27a8cbf8cd3a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0be3b92e47f4a93a0a53223ef55153683ff0095e7d0e20e3e53db5c8785dc9db)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTemplateMixinProps:
        return typing.cast(CfnTemplateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={"critical": "critical", "policies": "policies"},
    )
    class ApplicationPoliciesProperty:
        def __init__(
            self,
            *,
            critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ApplicationPolicyProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Application policies describe what the certificate can be used for.

            :param critical: Marks the application policy extension as critical.
            :param policies: Application policies describe what the certificate can be used for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-applicationpolicies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                application_policies_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                    critical=False,
                    policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                        policy_object_identifier="policyObjectIdentifier",
                        policy_type="policyType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__421eedf2444494e475029c36650ce1ec8a17434b0ef692117fc5ecfcac604ca0)
                check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
                check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if critical is not None:
                self._values["critical"] = critical
            if policies is not None:
                self._values["policies"] = policies

        @builtins.property
        def critical(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Marks the application policy extension as critical.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-applicationpolicies.html#cfn-pcaconnectorad-template-applicationpolicies-critical
            '''
            result = self._values.get("critical")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPolicyProperty"]]]]:
            '''Application policies describe what the certificate can be used for.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-applicationpolicies.html#cfn-pcaconnectorad-template-applicationpolicies-policies
            '''
            result = self._values.get("policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPolicyProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationPoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_object_identifier": "policyObjectIdentifier",
            "policy_type": "policyType",
        },
    )
    class ApplicationPolicyProperty:
        def __init__(
            self,
            *,
            policy_object_identifier: typing.Optional[builtins.str] = None,
            policy_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Application policies describe what the certificate can be used for.

            :param policy_object_identifier: The object identifier (OID) of an application policy.
            :param policy_type: The type of application policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-applicationpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                application_policy_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                    policy_object_identifier="policyObjectIdentifier",
                    policy_type="policyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__84ec73bbf7c78872678b79c3a9ed1c47d8af9b7b7d6569be75ec6cf6f9d1de0f)
                check_type(argname="argument policy_object_identifier", value=policy_object_identifier, expected_type=type_hints["policy_object_identifier"])
                check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_object_identifier is not None:
                self._values["policy_object_identifier"] = policy_object_identifier
            if policy_type is not None:
                self._values["policy_type"] = policy_type

        @builtins.property
        def policy_object_identifier(self) -> typing.Optional[builtins.str]:
            '''The object identifier (OID) of an application policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-applicationpolicy.html#cfn-pcaconnectorad-template-applicationpolicy-policyobjectidentifier
            '''
            result = self._values.get("policy_object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_type(self) -> typing.Optional[builtins.str]:
            '''The type of application policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-applicationpolicy.html#cfn-pcaconnectorad-template-applicationpolicy-policytype
            '''
            result = self._values.get("policy_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.CertificateValidityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "renewal_period": "renewalPeriod",
            "validity_period": "validityPeriod",
        },
    )
    class CertificateValidityProperty:
        def __init__(
            self,
            *,
            renewal_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ValidityPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            validity_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ValidityPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information describing the end of the validity period of the certificate.

            This parameter sets the “Not After” date for the certificate. Certificate validity is the period of time during which a certificate is valid. Validity can be expressed as an explicit date and time when the certificate expires, or as a span of time after issuance, stated in days, months, or years. For more information, see Validity in RFC 5280. This value is unaffected when ValidityNotBefore is also specified. For example, if Validity is set to 20 days in the future, the certificate will expire 20 days from issuance time regardless of the ValidityNotBefore value.

            :param renewal_period: Renewal period is the period of time before certificate expiration when a new certificate will be requested.
            :param validity_period: Information describing the end of the validity period of the certificate. This parameter sets the “Not After” date for the certificate. Certificate validity is the period of time during which a certificate is valid. Validity can be expressed as an explicit date and time when the certificate expires, or as a span of time after issuance, stated in days, months, or years. For more information, see Validity in RFC 5280. This value is unaffected when ValidityNotBefore is also specified. For example, if Validity is set to 20 days in the future, the certificate will expire 20 days from issuance time regardless of the ValidityNotBefore value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-certificatevalidity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                certificate_validity_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                    renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                        period=123,
                        period_type="periodType"
                    ),
                    validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                        period=123,
                        period_type="periodType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6441e65cbc02035f1c2ab5c2e1d9433a1cefd3b2d6c59f6cab7c78e59884b97)
                check_type(argname="argument renewal_period", value=renewal_period, expected_type=type_hints["renewal_period"])
                check_type(argname="argument validity_period", value=validity_period, expected_type=type_hints["validity_period"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if renewal_period is not None:
                self._values["renewal_period"] = renewal_period
            if validity_period is not None:
                self._values["validity_period"] = validity_period

        @builtins.property
        def renewal_period(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ValidityPeriodProperty"]]:
            '''Renewal period is the period of time before certificate expiration when a new certificate will be requested.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-certificatevalidity.html#cfn-pcaconnectorad-template-certificatevalidity-renewalperiod
            '''
            result = self._values.get("renewal_period")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ValidityPeriodProperty"]], result)

        @builtins.property
        def validity_period(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ValidityPeriodProperty"]]:
            '''Information describing the end of the validity period of the certificate.

            This parameter sets the “Not After” date for the certificate. Certificate validity is the period of time during which a certificate is valid. Validity can be expressed as an explicit date and time when the certificate expires, or as a span of time after issuance, stated in days, months, or years. For more information, see Validity in RFC 5280. This value is unaffected when ValidityNotBefore is also specified. For example, if Validity is set to 20 days in the future, the certificate will expire 20 days from issuance time regardless of the ValidityNotBefore value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-certificatevalidity.html#cfn-pcaconnectorad-template-certificatevalidity-validityperiod
            '''
            result = self._values.get("validity_period")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ValidityPeriodProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CertificateValidityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.EnrollmentFlagsV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "enable_key_reuse_on_nt_token_keyset_storage_full": "enableKeyReuseOnNtTokenKeysetStorageFull",
            "include_symmetric_algorithms": "includeSymmetricAlgorithms",
            "no_security_extension": "noSecurityExtension",
            "remove_invalid_certificate_from_personal_store": "removeInvalidCertificateFromPersonalStore",
            "user_interaction_required": "userInteractionRequired",
        },
    )
    class EnrollmentFlagsV2Property:
        def __init__(
            self,
            *,
            enable_key_reuse_on_nt_token_keyset_storage_full: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_symmetric_algorithms: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            no_security_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_invalid_certificate_from_personal_store: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            user_interaction_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Template configurations for v2 template schema.

            :param enable_key_reuse_on_nt_token_keyset_storage_full: Allow renewal using the same key.
            :param include_symmetric_algorithms: Include symmetric algorithms allowed by the subject.
            :param no_security_extension: This flag instructs the CA to not include the security extension szOID_NTDS_CA_SECURITY_EXT (OID:1.3.6.1.4.1.311.25.2), as specified in [MS-WCCE] sections 2.2.2.7.7.4 and 3.2.2.6.2.1.4.5.9, in the issued certificate. This addresses a Windows Kerberos elevation-of-privilege vulnerability.
            :param remove_invalid_certificate_from_personal_store: Delete expired or revoked certificates instead of archiving them.
            :param user_interaction_required: Require user interaction when the subject is enrolled and the private key associated with the certificate is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                enrollment_flags_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV2Property(
                    enable_key_reuse_on_nt_token_keyset_storage_full=False,
                    include_symmetric_algorithms=False,
                    no_security_extension=False,
                    remove_invalid_certificate_from_personal_store=False,
                    user_interaction_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8a16acae7fc8f25e49ce81ec532403608b99e93526172df20b51cae46490953)
                check_type(argname="argument enable_key_reuse_on_nt_token_keyset_storage_full", value=enable_key_reuse_on_nt_token_keyset_storage_full, expected_type=type_hints["enable_key_reuse_on_nt_token_keyset_storage_full"])
                check_type(argname="argument include_symmetric_algorithms", value=include_symmetric_algorithms, expected_type=type_hints["include_symmetric_algorithms"])
                check_type(argname="argument no_security_extension", value=no_security_extension, expected_type=type_hints["no_security_extension"])
                check_type(argname="argument remove_invalid_certificate_from_personal_store", value=remove_invalid_certificate_from_personal_store, expected_type=type_hints["remove_invalid_certificate_from_personal_store"])
                check_type(argname="argument user_interaction_required", value=user_interaction_required, expected_type=type_hints["user_interaction_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_key_reuse_on_nt_token_keyset_storage_full is not None:
                self._values["enable_key_reuse_on_nt_token_keyset_storage_full"] = enable_key_reuse_on_nt_token_keyset_storage_full
            if include_symmetric_algorithms is not None:
                self._values["include_symmetric_algorithms"] = include_symmetric_algorithms
            if no_security_extension is not None:
                self._values["no_security_extension"] = no_security_extension
            if remove_invalid_certificate_from_personal_store is not None:
                self._values["remove_invalid_certificate_from_personal_store"] = remove_invalid_certificate_from_personal_store
            if user_interaction_required is not None:
                self._values["user_interaction_required"] = user_interaction_required

        @builtins.property
        def enable_key_reuse_on_nt_token_keyset_storage_full(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allow renewal using the same key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv2.html#cfn-pcaconnectorad-template-enrollmentflagsv2-enablekeyreuseonnttokenkeysetstoragefull
            '''
            result = self._values.get("enable_key_reuse_on_nt_token_keyset_storage_full")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_symmetric_algorithms(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include symmetric algorithms allowed by the subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv2.html#cfn-pcaconnectorad-template-enrollmentflagsv2-includesymmetricalgorithms
            '''
            result = self._values.get("include_symmetric_algorithms")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def no_security_extension(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This flag instructs the CA to not include the security extension szOID_NTDS_CA_SECURITY_EXT (OID:1.3.6.1.4.1.311.25.2), as specified in [MS-WCCE] sections 2.2.2.7.7.4 and 3.2.2.6.2.1.4.5.9, in the issued certificate. This addresses a Windows Kerberos elevation-of-privilege vulnerability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv2.html#cfn-pcaconnectorad-template-enrollmentflagsv2-nosecurityextension
            '''
            result = self._values.get("no_security_extension")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_invalid_certificate_from_personal_store(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Delete expired or revoked certificates instead of archiving them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv2.html#cfn-pcaconnectorad-template-enrollmentflagsv2-removeinvalidcertificatefrompersonalstore
            '''
            result = self._values.get("remove_invalid_certificate_from_personal_store")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def user_interaction_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Require user interaction when the subject is enrolled and the private key associated with the certificate is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv2.html#cfn-pcaconnectorad-template-enrollmentflagsv2-userinteractionrequired
            '''
            result = self._values.get("user_interaction_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnrollmentFlagsV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.EnrollmentFlagsV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "enable_key_reuse_on_nt_token_keyset_storage_full": "enableKeyReuseOnNtTokenKeysetStorageFull",
            "include_symmetric_algorithms": "includeSymmetricAlgorithms",
            "no_security_extension": "noSecurityExtension",
            "remove_invalid_certificate_from_personal_store": "removeInvalidCertificateFromPersonalStore",
            "user_interaction_required": "userInteractionRequired",
        },
    )
    class EnrollmentFlagsV3Property:
        def __init__(
            self,
            *,
            enable_key_reuse_on_nt_token_keyset_storage_full: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_symmetric_algorithms: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            no_security_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_invalid_certificate_from_personal_store: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            user_interaction_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Template configurations for v3 template schema.

            :param enable_key_reuse_on_nt_token_keyset_storage_full: Allow renewal using the same key.
            :param include_symmetric_algorithms: Include symmetric algorithms allowed by the subject.
            :param no_security_extension: This flag instructs the CA to not include the security extension szOID_NTDS_CA_SECURITY_EXT (OID:1.3.6.1.4.1.311.25.2), as specified in [MS-WCCE] sections 2.2.2.7.7.4 and 3.2.2.6.2.1.4.5.9, in the issued certificate. This addresses a Windows Kerberos elevation-of-privilege vulnerability.
            :param remove_invalid_certificate_from_personal_store: Delete expired or revoked certificates instead of archiving them.
            :param user_interaction_required: Require user interaction when the subject is enrolled and the private key associated with the certificate is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                enrollment_flags_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV3Property(
                    enable_key_reuse_on_nt_token_keyset_storage_full=False,
                    include_symmetric_algorithms=False,
                    no_security_extension=False,
                    remove_invalid_certificate_from_personal_store=False,
                    user_interaction_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04a05473aa4b4ad821c6a08e810f6206ee138e6418d6400c318ed78d76d6ad76)
                check_type(argname="argument enable_key_reuse_on_nt_token_keyset_storage_full", value=enable_key_reuse_on_nt_token_keyset_storage_full, expected_type=type_hints["enable_key_reuse_on_nt_token_keyset_storage_full"])
                check_type(argname="argument include_symmetric_algorithms", value=include_symmetric_algorithms, expected_type=type_hints["include_symmetric_algorithms"])
                check_type(argname="argument no_security_extension", value=no_security_extension, expected_type=type_hints["no_security_extension"])
                check_type(argname="argument remove_invalid_certificate_from_personal_store", value=remove_invalid_certificate_from_personal_store, expected_type=type_hints["remove_invalid_certificate_from_personal_store"])
                check_type(argname="argument user_interaction_required", value=user_interaction_required, expected_type=type_hints["user_interaction_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_key_reuse_on_nt_token_keyset_storage_full is not None:
                self._values["enable_key_reuse_on_nt_token_keyset_storage_full"] = enable_key_reuse_on_nt_token_keyset_storage_full
            if include_symmetric_algorithms is not None:
                self._values["include_symmetric_algorithms"] = include_symmetric_algorithms
            if no_security_extension is not None:
                self._values["no_security_extension"] = no_security_extension
            if remove_invalid_certificate_from_personal_store is not None:
                self._values["remove_invalid_certificate_from_personal_store"] = remove_invalid_certificate_from_personal_store
            if user_interaction_required is not None:
                self._values["user_interaction_required"] = user_interaction_required

        @builtins.property
        def enable_key_reuse_on_nt_token_keyset_storage_full(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allow renewal using the same key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv3.html#cfn-pcaconnectorad-template-enrollmentflagsv3-enablekeyreuseonnttokenkeysetstoragefull
            '''
            result = self._values.get("enable_key_reuse_on_nt_token_keyset_storage_full")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_symmetric_algorithms(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include symmetric algorithms allowed by the subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv3.html#cfn-pcaconnectorad-template-enrollmentflagsv3-includesymmetricalgorithms
            '''
            result = self._values.get("include_symmetric_algorithms")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def no_security_extension(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This flag instructs the CA to not include the security extension szOID_NTDS_CA_SECURITY_EXT (OID:1.3.6.1.4.1.311.25.2), as specified in [MS-WCCE] sections 2.2.2.7.7.4 and 3.2.2.6.2.1.4.5.9, in the issued certificate. This addresses a Windows Kerberos elevation-of-privilege vulnerability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv3.html#cfn-pcaconnectorad-template-enrollmentflagsv3-nosecurityextension
            '''
            result = self._values.get("no_security_extension")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_invalid_certificate_from_personal_store(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Delete expired or revoked certificates instead of archiving them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv3.html#cfn-pcaconnectorad-template-enrollmentflagsv3-removeinvalidcertificatefrompersonalstore
            '''
            result = self._values.get("remove_invalid_certificate_from_personal_store")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def user_interaction_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Require user interaction when the subject is enrolled and the private key associated with the certificate is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv3.html#cfn-pcaconnectorad-template-enrollmentflagsv3-userinteractionrequired
            '''
            result = self._values.get("user_interaction_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnrollmentFlagsV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.EnrollmentFlagsV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "enable_key_reuse_on_nt_token_keyset_storage_full": "enableKeyReuseOnNtTokenKeysetStorageFull",
            "include_symmetric_algorithms": "includeSymmetricAlgorithms",
            "no_security_extension": "noSecurityExtension",
            "remove_invalid_certificate_from_personal_store": "removeInvalidCertificateFromPersonalStore",
            "user_interaction_required": "userInteractionRequired",
        },
    )
    class EnrollmentFlagsV4Property:
        def __init__(
            self,
            *,
            enable_key_reuse_on_nt_token_keyset_storage_full: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            include_symmetric_algorithms: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            no_security_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            remove_invalid_certificate_from_personal_store: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            user_interaction_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Template configurations for v4 template schema.

            :param enable_key_reuse_on_nt_token_keyset_storage_full: Allow renewal using the same key.
            :param include_symmetric_algorithms: Include symmetric algorithms allowed by the subject.
            :param no_security_extension: This flag instructs the CA to not include the security extension szOID_NTDS_CA_SECURITY_EXT (OID:1.3.6.1.4.1.311.25.2), as specified in [MS-WCCE] sections 2.2.2.7.7.4 and 3.2.2.6.2.1.4.5.9, in the issued certificate. This addresses a Windows Kerberos elevation-of-privilege vulnerability.
            :param remove_invalid_certificate_from_personal_store: Delete expired or revoked certificates instead of archiving them.
            :param user_interaction_required: Require user interaction when the subject is enrolled and the private key associated with the certificate is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                enrollment_flags_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV4Property(
                    enable_key_reuse_on_nt_token_keyset_storage_full=False,
                    include_symmetric_algorithms=False,
                    no_security_extension=False,
                    remove_invalid_certificate_from_personal_store=False,
                    user_interaction_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a882390b3abf90505f807072eac64f4d440a60e84d26abfd92b85fb89e2f878c)
                check_type(argname="argument enable_key_reuse_on_nt_token_keyset_storage_full", value=enable_key_reuse_on_nt_token_keyset_storage_full, expected_type=type_hints["enable_key_reuse_on_nt_token_keyset_storage_full"])
                check_type(argname="argument include_symmetric_algorithms", value=include_symmetric_algorithms, expected_type=type_hints["include_symmetric_algorithms"])
                check_type(argname="argument no_security_extension", value=no_security_extension, expected_type=type_hints["no_security_extension"])
                check_type(argname="argument remove_invalid_certificate_from_personal_store", value=remove_invalid_certificate_from_personal_store, expected_type=type_hints["remove_invalid_certificate_from_personal_store"])
                check_type(argname="argument user_interaction_required", value=user_interaction_required, expected_type=type_hints["user_interaction_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_key_reuse_on_nt_token_keyset_storage_full is not None:
                self._values["enable_key_reuse_on_nt_token_keyset_storage_full"] = enable_key_reuse_on_nt_token_keyset_storage_full
            if include_symmetric_algorithms is not None:
                self._values["include_symmetric_algorithms"] = include_symmetric_algorithms
            if no_security_extension is not None:
                self._values["no_security_extension"] = no_security_extension
            if remove_invalid_certificate_from_personal_store is not None:
                self._values["remove_invalid_certificate_from_personal_store"] = remove_invalid_certificate_from_personal_store
            if user_interaction_required is not None:
                self._values["user_interaction_required"] = user_interaction_required

        @builtins.property
        def enable_key_reuse_on_nt_token_keyset_storage_full(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allow renewal using the same key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv4.html#cfn-pcaconnectorad-template-enrollmentflagsv4-enablekeyreuseonnttokenkeysetstoragefull
            '''
            result = self._values.get("enable_key_reuse_on_nt_token_keyset_storage_full")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def include_symmetric_algorithms(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include symmetric algorithms allowed by the subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv4.html#cfn-pcaconnectorad-template-enrollmentflagsv4-includesymmetricalgorithms
            '''
            result = self._values.get("include_symmetric_algorithms")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def no_security_extension(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''This flag instructs the CA to not include the security extension szOID_NTDS_CA_SECURITY_EXT (OID:1.3.6.1.4.1.311.25.2), as specified in [MS-WCCE] sections 2.2.2.7.7.4 and 3.2.2.6.2.1.4.5.9, in the issued certificate. This addresses a Windows Kerberos elevation-of-privilege vulnerability.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv4.html#cfn-pcaconnectorad-template-enrollmentflagsv4-nosecurityextension
            '''
            result = self._values.get("no_security_extension")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def remove_invalid_certificate_from_personal_store(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Delete expired or revoked certificates instead of archiving them.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv4.html#cfn-pcaconnectorad-template-enrollmentflagsv4-removeinvalidcertificatefrompersonalstore
            '''
            result = self._values.get("remove_invalid_certificate_from_personal_store")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def user_interaction_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Require user interaction when the subject is enrolled and the private key associated with the certificate is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-enrollmentflagsv4.html#cfn-pcaconnectorad-template-enrollmentflagsv4-userinteractionrequired
            '''
            result = self._values.get("user_interaction_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnrollmentFlagsV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.ExtensionsV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "application_policies": "applicationPolicies",
            "key_usage": "keyUsage",
        },
    )
    class ExtensionsV2Property:
        def __init__(
            self,
            *,
            application_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ApplicationPoliciesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Certificate extensions for v2 template schema.

            :param application_policies: Application policies specify what the certificate is used for and its purpose.
            :param key_usage: The key usage extension defines the purpose (e.g., encipherment, signature, certificate signing) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                extensions_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV2Property(
                    application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                        critical=False,
                        policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                            policy_object_identifier="policyObjectIdentifier",
                            policy_type="policyType"
                        )]
                    ),
                    key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                        critical=False,
                        usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                            data_encipherment=False,
                            digital_signature=False,
                            key_agreement=False,
                            key_encipherment=False,
                            non_repudiation=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f16c8826291cefe02834bc61491b65e66eeaba8d366751f1d2a52968eb187d5)
                check_type(argname="argument application_policies", value=application_policies, expected_type=type_hints["application_policies"])
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_policies is not None:
                self._values["application_policies"] = application_policies
            if key_usage is not None:
                self._values["key_usage"] = key_usage

        @builtins.property
        def application_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPoliciesProperty"]]:
            '''Application policies specify what the certificate is used for and its purpose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv2.html#cfn-pcaconnectorad-template-extensionsv2-applicationpolicies
            '''
            result = self._values.get("application_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPoliciesProperty"]], result)

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageProperty"]]:
            '''The key usage extension defines the purpose (e.g., encipherment, signature, certificate signing) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv2.html#cfn-pcaconnectorad-template-extensionsv2-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtensionsV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.ExtensionsV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "application_policies": "applicationPolicies",
            "key_usage": "keyUsage",
        },
    )
    class ExtensionsV3Property:
        def __init__(
            self,
            *,
            application_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ApplicationPoliciesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Certificate extensions for v3 template schema.

            :param application_policies: Application policies specify what the certificate is used for and its purpose.
            :param key_usage: The key usage extension defines the purpose (e.g., encipherment, signature, certificate signing) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                extensions_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV3Property(
                    application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                        critical=False,
                        policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                            policy_object_identifier="policyObjectIdentifier",
                            policy_type="policyType"
                        )]
                    ),
                    key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                        critical=False,
                        usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                            data_encipherment=False,
                            digital_signature=False,
                            key_agreement=False,
                            key_encipherment=False,
                            non_repudiation=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__618276d35b1aa9ee1d946b69a649a37f1470a6e86e36fdb16e45f0f4072883e6)
                check_type(argname="argument application_policies", value=application_policies, expected_type=type_hints["application_policies"])
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_policies is not None:
                self._values["application_policies"] = application_policies
            if key_usage is not None:
                self._values["key_usage"] = key_usage

        @builtins.property
        def application_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPoliciesProperty"]]:
            '''Application policies specify what the certificate is used for and its purpose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv3.html#cfn-pcaconnectorad-template-extensionsv3-applicationpolicies
            '''
            result = self._values.get("application_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPoliciesProperty"]], result)

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageProperty"]]:
            '''The key usage extension defines the purpose (e.g., encipherment, signature, certificate signing) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv3.html#cfn-pcaconnectorad-template-extensionsv3-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtensionsV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.ExtensionsV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "application_policies": "applicationPolicies",
            "key_usage": "keyUsage",
        },
    )
    class ExtensionsV4Property:
        def __init__(
            self,
            *,
            application_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ApplicationPoliciesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Certificate extensions for v4 template schema.

            :param application_policies: Application policies specify what the certificate is used for and its purpose.
            :param key_usage: The key usage extension defines the purpose (e.g., encipherment, signature) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                extensions_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV4Property(
                    application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                        critical=False,
                        policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                            policy_object_identifier="policyObjectIdentifier",
                            policy_type="policyType"
                        )]
                    ),
                    key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                        critical=False,
                        usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                            data_encipherment=False,
                            digital_signature=False,
                            key_agreement=False,
                            key_encipherment=False,
                            non_repudiation=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__168a7553510eeb9e93f4f37e6699219139a777014c1465c7e85ef836b8109a17)
                check_type(argname="argument application_policies", value=application_policies, expected_type=type_hints["application_policies"])
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_policies is not None:
                self._values["application_policies"] = application_policies
            if key_usage is not None:
                self._values["key_usage"] = key_usage

        @builtins.property
        def application_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPoliciesProperty"]]:
            '''Application policies specify what the certificate is used for and its purpose.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv4.html#cfn-pcaconnectorad-template-extensionsv4-applicationpolicies
            '''
            result = self._values.get("application_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ApplicationPoliciesProperty"]], result)

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageProperty"]]:
            '''The key usage extension defines the purpose (e.g., encipherment, signature) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-extensionsv4.html#cfn-pcaconnectorad-template-extensionsv4-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtensionsV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.GeneralFlagsV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "auto_enrollment": "autoEnrollment",
            "machine_type": "machineType",
        },
    )
    class GeneralFlagsV2Property:
        def __init__(
            self,
            *,
            auto_enrollment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            machine_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''General flags for v2 template schema that defines if the template is for a machine or a user and if the template can be issued using autoenrollment.

            :param auto_enrollment: Allows certificate issuance using autoenrollment. Set to TRUE to allow autoenrollment.
            :param machine_type: Defines if the template is for machines or users. Set to TRUE if the template is for machines. Set to FALSE if the template is for users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                general_flags_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV2Property(
                    auto_enrollment=False,
                    machine_type=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fbf500eb5a9acf6f7f591fbb021ae9e93995350cb4131b385b564ca56f788c6)
                check_type(argname="argument auto_enrollment", value=auto_enrollment, expected_type=type_hints["auto_enrollment"])
                check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_enrollment is not None:
                self._values["auto_enrollment"] = auto_enrollment
            if machine_type is not None:
                self._values["machine_type"] = machine_type

        @builtins.property
        def auto_enrollment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows certificate issuance using autoenrollment.

            Set to TRUE to allow autoenrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv2.html#cfn-pcaconnectorad-template-generalflagsv2-autoenrollment
            '''
            result = self._values.get("auto_enrollment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def machine_type(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Defines if the template is for machines or users.

            Set to TRUE if the template is for machines. Set to FALSE if the template is for users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv2.html#cfn-pcaconnectorad-template-generalflagsv2-machinetype
            '''
            result = self._values.get("machine_type")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralFlagsV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.GeneralFlagsV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "auto_enrollment": "autoEnrollment",
            "machine_type": "machineType",
        },
    )
    class GeneralFlagsV3Property:
        def __init__(
            self,
            *,
            auto_enrollment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            machine_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''General flags for v3 template schema that defines if the template is for a machine or a user and if the template can be issued using autoenrollment.

            :param auto_enrollment: Allows certificate issuance using autoenrollment. Set to TRUE to allow autoenrollment.
            :param machine_type: Defines if the template is for machines or users. Set to TRUE if the template is for machines. Set to FALSE if the template is for users

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                general_flags_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV3Property(
                    auto_enrollment=False,
                    machine_type=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f985359454d1d7cafdcb84e10b187c3f16caffd1a18b2f8f747cce6102fd716a)
                check_type(argname="argument auto_enrollment", value=auto_enrollment, expected_type=type_hints["auto_enrollment"])
                check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_enrollment is not None:
                self._values["auto_enrollment"] = auto_enrollment
            if machine_type is not None:
                self._values["machine_type"] = machine_type

        @builtins.property
        def auto_enrollment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows certificate issuance using autoenrollment.

            Set to TRUE to allow autoenrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv3.html#cfn-pcaconnectorad-template-generalflagsv3-autoenrollment
            '''
            result = self._values.get("auto_enrollment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def machine_type(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Defines if the template is for machines or users.

            Set to TRUE if the template is for machines. Set to FALSE if the template is for users

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv3.html#cfn-pcaconnectorad-template-generalflagsv3-machinetype
            '''
            result = self._values.get("machine_type")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralFlagsV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.GeneralFlagsV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "auto_enrollment": "autoEnrollment",
            "machine_type": "machineType",
        },
    )
    class GeneralFlagsV4Property:
        def __init__(
            self,
            *,
            auto_enrollment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            machine_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''General flags for v4 template schema that defines if the template is for a machine or a user and if the template can be issued using autoenrollment.

            :param auto_enrollment: Allows certificate issuance using autoenrollment. Set to TRUE to allow autoenrollment.
            :param machine_type: Defines if the template is for machines or users. Set to TRUE if the template is for machines. Set to FALSE if the template is for users

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                general_flags_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV4Property(
                    auto_enrollment=False,
                    machine_type=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__daac8f6943ae523f3afefe014b3319e7e2c248c54f086d371313e2b61b03c86a)
                check_type(argname="argument auto_enrollment", value=auto_enrollment, expected_type=type_hints["auto_enrollment"])
                check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_enrollment is not None:
                self._values["auto_enrollment"] = auto_enrollment
            if machine_type is not None:
                self._values["machine_type"] = machine_type

        @builtins.property
        def auto_enrollment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows certificate issuance using autoenrollment.

            Set to TRUE to allow autoenrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv4.html#cfn-pcaconnectorad-template-generalflagsv4-autoenrollment
            '''
            result = self._values.get("auto_enrollment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def machine_type(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Defines if the template is for machines or users.

            Set to TRUE if the template is for machines. Set to FALSE if the template is for users

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-generalflagsv4.html#cfn-pcaconnectorad-template-generalflagsv4-machinetype
            '''
            result = self._values.get("machine_type")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralFlagsV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_encipherment": "dataEncipherment",
            "digital_signature": "digitalSignature",
            "key_agreement": "keyAgreement",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageFlagsProperty:
        def __init__(
            self,
            *,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The key usage flags represent the purpose (e.g., encipherment, signature) of the key contained in the certificate.

            :param data_encipherment: DataEncipherment is asserted when the subject public key is used for directly enciphering raw user data without the use of an intermediate symmetric cipher.
            :param digital_signature: The digitalSignature is asserted when the subject public key is used for verifying digital signatures.
            :param key_agreement: KeyAgreement is asserted when the subject public key is used for key agreement.
            :param key_encipherment: KeyEncipherment is asserted when the subject public key is used for enciphering private or secret keys, i.e., for key transport.
            :param non_repudiation: NonRepudiation is asserted when the subject public key is used to verify digital signatures.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageflags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                key_usage_flags_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                    data_encipherment=False,
                    digital_signature=False,
                    key_agreement=False,
                    key_encipherment=False,
                    non_repudiation=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d5a6a2efed46832d2692314708bab7f2f9402cf3938d592ba03a4a6ba9fe69b)
                check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
                check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
                check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
                check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
                check_type(argname="argument non_repudiation", value=non_repudiation, expected_type=type_hints["non_repudiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''DataEncipherment is asserted when the subject public key is used for directly enciphering raw user data without the use of an intermediate symmetric cipher.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageflags.html#cfn-pcaconnectorad-template-keyusageflags-dataencipherment
            '''
            result = self._values.get("data_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''The digitalSignature is asserted when the subject public key is used for verifying digital signatures.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageflags.html#cfn-pcaconnectorad-template-keyusageflags-digitalsignature
            '''
            result = self._values.get("digital_signature")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''KeyAgreement is asserted when the subject public key is used for key agreement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageflags.html#cfn-pcaconnectorad-template-keyusageflags-keyagreement
            '''
            result = self._values.get("key_agreement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''KeyEncipherment is asserted when the subject public key is used for enciphering private or secret keys, i.e., for key transport.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageflags.html#cfn-pcaconnectorad-template-keyusageflags-keyencipherment
            '''
            result = self._values.get("key_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''NonRepudiation is asserted when the subject public key is used to verify digital signatures.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageflags.html#cfn-pcaconnectorad-template-keyusageflags-nonrepudiation
            '''
            result = self._values.get("non_repudiation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageFlagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={"critical": "critical", "usage_flags": "usageFlags"},
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            usage_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsageFlagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The key usage extension defines the purpose (e.g., encipherment, signature) of the key contained in the certificate.

            :param critical: Sets the key usage extension to critical.
            :param usage_flags: The key usage flags represent the purpose (e.g., encipherment, signature) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                key_usage_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                    critical=False,
                    usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                        data_encipherment=False,
                        digital_signature=False,
                        key_agreement=False,
                        key_encipherment=False,
                        non_repudiation=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3d8954507ea8dbfc13f11e2865fcb898693d349ddfca0c3bdc2fd547919c3161)
                check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
                check_type(argname="argument usage_flags", value=usage_flags, expected_type=type_hints["usage_flags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if critical is not None:
                self._values["critical"] = critical
            if usage_flags is not None:
                self._values["usage_flags"] = usage_flags

        @builtins.property
        def critical(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Sets the key usage extension to critical.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusage.html#cfn-pcaconnectorad-template-keyusage-critical
            '''
            result = self._values.get("critical")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def usage_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageFlagsProperty"]]:
            '''The key usage flags represent the purpose (e.g., encipherment, signature) of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusage.html#cfn-pcaconnectorad-template-keyusage-usageflags
            '''
            result = self._values.get("usage_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsageFlagsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decrypt": "decrypt",
            "key_agreement": "keyAgreement",
            "sign": "sign",
        },
    )
    class KeyUsagePropertyFlagsProperty:
        def __init__(
            self,
            *,
            decrypt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Specifies key usage.

            :param decrypt: Allows key for encryption and decryption.
            :param key_agreement: Allows key exchange without encryption.
            :param sign: Allow key use for digital signature.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusagepropertyflags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                key_usage_property_flags_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                    decrypt=False,
                    key_agreement=False,
                    sign=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92ccde75a6ff24689da8b849c1cd0eda203e64dac75c35a30f0137badb4076df)
                check_type(argname="argument decrypt", value=decrypt, expected_type=type_hints["decrypt"])
                check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
                check_type(argname="argument sign", value=sign, expected_type=type_hints["sign"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decrypt is not None:
                self._values["decrypt"] = decrypt
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if sign is not None:
                self._values["sign"] = sign

        @builtins.property
        def decrypt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows key for encryption and decryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusagepropertyflags.html#cfn-pcaconnectorad-template-keyusagepropertyflags-decrypt
            '''
            result = self._values.get("decrypt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows key exchange without encryption.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusagepropertyflags.html#cfn-pcaconnectorad-template-keyusagepropertyflags-keyagreement
            '''
            result = self._values.get("key_agreement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allow key use for digital signature.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusagepropertyflags.html#cfn-pcaconnectorad-template-keyusagepropertyflags-sign
            '''
            result = self._values.get("sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsagePropertyFlagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "property_flags": "propertyFlags",
            "property_type": "propertyType",
        },
    )
    class KeyUsagePropertyProperty:
        def __init__(
            self,
            *,
            property_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            property_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The key usage property defines the purpose of the private key contained in the certificate.

            You can specify specific purposes using property flags or all by using property type ALL.

            :param property_flags: You can specify key usage for encryption, key agreement, and signature. You can use property flags or property type but not both.
            :param property_type: You can specify all key usages using property type ALL. You can use property type or property flags but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                key_usage_property_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                    property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                        decrypt=False,
                        key_agreement=False,
                        sign=False
                    ),
                    property_type="propertyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ee80703166df61ed3d4e49a839f7a394aab4133474d2ef6ca8eaac875f34fa7)
                check_type(argname="argument property_flags", value=property_flags, expected_type=type_hints["property_flags"])
                check_type(argname="argument property_type", value=property_type, expected_type=type_hints["property_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if property_flags is not None:
                self._values["property_flags"] = property_flags
            if property_type is not None:
                self._values["property_type"] = property_type

        @builtins.property
        def property_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty"]]:
            '''You can specify key usage for encryption, key agreement, and signature.

            You can use property flags or property type but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageproperty.html#cfn-pcaconnectorad-template-keyusageproperty-propertyflags
            '''
            result = self._values.get("property_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty"]], result)

        @builtins.property
        def property_type(self) -> typing.Optional[builtins.str]:
            '''You can specify all key usages using property type ALL.

            You can use property type or property flags but not both.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-keyusageproperty.html#cfn-pcaconnectorad-template-keyusageproperty-propertytype
            '''
            result = self._values.get("property_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsagePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "crypto_providers": "cryptoProviders",
            "key_spec": "keySpec",
            "minimal_key_length": "minimalKeyLength",
        },
    )
    class PrivateKeyAttributesV2Property:
        def __init__(
            self,
            *,
            crypto_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
            key_spec: typing.Optional[builtins.str] = None,
            minimal_key_length: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the attributes of the private key.

            :param crypto_providers: Defines the cryptographic providers used to generate the private key.
            :param key_spec: Defines the purpose of the private key. Set it to "KEY_EXCHANGE" or "SIGNATURE" value.
            :param minimal_key_length: Set the minimum key length of the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                private_key_attributes_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV2Property(
                    crypto_providers=["cryptoProviders"],
                    key_spec="keySpec",
                    minimal_key_length=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8bd8738d00183ac8ec3b4030504415a7e1bf05f60ee45141d9020a8fd6e8309)
                check_type(argname="argument crypto_providers", value=crypto_providers, expected_type=type_hints["crypto_providers"])
                check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
                check_type(argname="argument minimal_key_length", value=minimal_key_length, expected_type=type_hints["minimal_key_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crypto_providers is not None:
                self._values["crypto_providers"] = crypto_providers
            if key_spec is not None:
                self._values["key_spec"] = key_spec
            if minimal_key_length is not None:
                self._values["minimal_key_length"] = minimal_key_length

        @builtins.property
        def crypto_providers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Defines the cryptographic providers used to generate the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv2.html#cfn-pcaconnectorad-template-privatekeyattributesv2-cryptoproviders
            '''
            result = self._values.get("crypto_providers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def key_spec(self) -> typing.Optional[builtins.str]:
            '''Defines the purpose of the private key.

            Set it to "KEY_EXCHANGE" or "SIGNATURE" value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv2.html#cfn-pcaconnectorad-template-privatekeyattributesv2-keyspec
            '''
            result = self._values.get("key_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def minimal_key_length(self) -> typing.Optional[jsii.Number]:
            '''Set the minimum key length of the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv2.html#cfn-pcaconnectorad-template-privatekeyattributesv2-minimalkeylength
            '''
            result = self._values.get("minimal_key_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateKeyAttributesV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "crypto_providers": "cryptoProviders",
            "key_spec": "keySpec",
            "key_usage_property": "keyUsageProperty",
            "minimal_key_length": "minimalKeyLength",
        },
    )
    class PrivateKeyAttributesV3Property:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            crypto_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
            key_spec: typing.Optional[builtins.str] = None,
            key_usage_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsagePropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimal_key_length: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the attributes of the private key.

            :param algorithm: Defines the algorithm used to generate the private key.
            :param crypto_providers: Defines the cryptographic providers used to generate the private key.
            :param key_spec: Defines the purpose of the private key. Set it to "KEY_EXCHANGE" or "SIGNATURE" value.
            :param key_usage_property: The key usage property defines the purpose of the private key contained in the certificate. You can specify specific purposes using property flags or all by using property type ALL.
            :param minimal_key_length: Set the minimum key length of the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                private_key_attributes_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV3Property(
                    algorithm="algorithm",
                    crypto_providers=["cryptoProviders"],
                    key_spec="keySpec",
                    key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                        property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                            decrypt=False,
                            key_agreement=False,
                            sign=False
                        ),
                        property_type="propertyType"
                    ),
                    minimal_key_length=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f454b49bf57d445d91d36d92137f5e13fdf72094847f4ef5f4988d5882c0501)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument crypto_providers", value=crypto_providers, expected_type=type_hints["crypto_providers"])
                check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
                check_type(argname="argument key_usage_property", value=key_usage_property, expected_type=type_hints["key_usage_property"])
                check_type(argname="argument minimal_key_length", value=minimal_key_length, expected_type=type_hints["minimal_key_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if crypto_providers is not None:
                self._values["crypto_providers"] = crypto_providers
            if key_spec is not None:
                self._values["key_spec"] = key_spec
            if key_usage_property is not None:
                self._values["key_usage_property"] = key_usage_property
            if minimal_key_length is not None:
                self._values["minimal_key_length"] = minimal_key_length

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''Defines the algorithm used to generate the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv3.html#cfn-pcaconnectorad-template-privatekeyattributesv3-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def crypto_providers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Defines the cryptographic providers used to generate the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv3.html#cfn-pcaconnectorad-template-privatekeyattributesv3-cryptoproviders
            '''
            result = self._values.get("crypto_providers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def key_spec(self) -> typing.Optional[builtins.str]:
            '''Defines the purpose of the private key.

            Set it to "KEY_EXCHANGE" or "SIGNATURE" value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv3.html#cfn-pcaconnectorad-template-privatekeyattributesv3-keyspec
            '''
            result = self._values.get("key_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_usage_property(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsagePropertyProperty"]]:
            '''The key usage property defines the purpose of the private key contained in the certificate.

            You can specify specific purposes using property flags or all by using property type ALL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv3.html#cfn-pcaconnectorad-template-privatekeyattributesv3-keyusageproperty
            '''
            result = self._values.get("key_usage_property")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsagePropertyProperty"]], result)

        @builtins.property
        def minimal_key_length(self) -> typing.Optional[jsii.Number]:
            '''Set the minimum key length of the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv3.html#cfn-pcaconnectorad-template-privatekeyattributesv3-minimalkeylength
            '''
            result = self._values.get("minimal_key_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateKeyAttributesV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "crypto_providers": "cryptoProviders",
            "key_spec": "keySpec",
            "key_usage_property": "keyUsageProperty",
            "minimal_key_length": "minimalKeyLength",
        },
    )
    class PrivateKeyAttributesV4Property:
        def __init__(
            self,
            *,
            algorithm: typing.Optional[builtins.str] = None,
            crypto_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
            key_spec: typing.Optional[builtins.str] = None,
            key_usage_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.KeyUsagePropertyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimal_key_length: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines the attributes of the private key.

            :param algorithm: Defines the algorithm used to generate the private key.
            :param crypto_providers: Defines the cryptographic providers used to generate the private key.
            :param key_spec: Defines the purpose of the private key. Set it to "KEY_EXCHANGE" or "SIGNATURE" value.
            :param key_usage_property: The key usage property defines the purpose of the private key contained in the certificate. You can specify specific purposes using property flags or all by using property type ALL.
            :param minimal_key_length: Set the minimum key length of the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                private_key_attributes_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV4Property(
                    algorithm="algorithm",
                    crypto_providers=["cryptoProviders"],
                    key_spec="keySpec",
                    key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                        property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                            decrypt=False,
                            key_agreement=False,
                            sign=False
                        ),
                        property_type="propertyType"
                    ),
                    minimal_key_length=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__380c7979b66173afd9bf75e7b7aec1dfb63e3215a5c1ebdd4798b40654165d95)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument crypto_providers", value=crypto_providers, expected_type=type_hints["crypto_providers"])
                check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
                check_type(argname="argument key_usage_property", value=key_usage_property, expected_type=type_hints["key_usage_property"])
                check_type(argname="argument minimal_key_length", value=minimal_key_length, expected_type=type_hints["minimal_key_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if crypto_providers is not None:
                self._values["crypto_providers"] = crypto_providers
            if key_spec is not None:
                self._values["key_spec"] = key_spec
            if key_usage_property is not None:
                self._values["key_usage_property"] = key_usage_property
            if minimal_key_length is not None:
                self._values["minimal_key_length"] = minimal_key_length

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''Defines the algorithm used to generate the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv4.html#cfn-pcaconnectorad-template-privatekeyattributesv4-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def crypto_providers(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Defines the cryptographic providers used to generate the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv4.html#cfn-pcaconnectorad-template-privatekeyattributesv4-cryptoproviders
            '''
            result = self._values.get("crypto_providers")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def key_spec(self) -> typing.Optional[builtins.str]:
            '''Defines the purpose of the private key.

            Set it to "KEY_EXCHANGE" or "SIGNATURE" value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv4.html#cfn-pcaconnectorad-template-privatekeyattributesv4-keyspec
            '''
            result = self._values.get("key_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_usage_property(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsagePropertyProperty"]]:
            '''The key usage property defines the purpose of the private key contained in the certificate.

            You can specify specific purposes using property flags or all by using property type ALL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv4.html#cfn-pcaconnectorad-template-privatekeyattributesv4-keyusageproperty
            '''
            result = self._values.get("key_usage_property")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.KeyUsagePropertyProperty"]], result)

        @builtins.property
        def minimal_key_length(self) -> typing.Optional[jsii.Number]:
            '''Set the minimum key length of the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyattributesv4.html#cfn-pcaconnectorad-template-privatekeyattributesv4-minimalkeylength
            '''
            result = self._values.get("minimal_key_length")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateKeyAttributesV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "client_version": "clientVersion",
            "exportable_key": "exportableKey",
            "strong_key_protection_required": "strongKeyProtectionRequired",
        },
    )
    class PrivateKeyFlagsV2Property:
        def __init__(
            self,
            *,
            client_version: typing.Optional[builtins.str] = None,
            exportable_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            strong_key_protection_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Private key flags for v2 templates specify the client compatibility, if the private key can be exported, and if user input is required when using a private key.

            :param client_version: Defines the minimum client compatibility.
            :param exportable_key: Allows the private key to be exported.
            :param strong_key_protection_required: Require user input when using the private key for enrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                private_key_flags_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV2Property(
                    client_version="clientVersion",
                    exportable_key=False,
                    strong_key_protection_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a35dcbd6f1ab4ecb527cece3ede1aae5bb37edc1cca3190634160d9b09390b4d)
                check_type(argname="argument client_version", value=client_version, expected_type=type_hints["client_version"])
                check_type(argname="argument exportable_key", value=exportable_key, expected_type=type_hints["exportable_key"])
                check_type(argname="argument strong_key_protection_required", value=strong_key_protection_required, expected_type=type_hints["strong_key_protection_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_version is not None:
                self._values["client_version"] = client_version
            if exportable_key is not None:
                self._values["exportable_key"] = exportable_key
            if strong_key_protection_required is not None:
                self._values["strong_key_protection_required"] = strong_key_protection_required

        @builtins.property
        def client_version(self) -> typing.Optional[builtins.str]:
            '''Defines the minimum client compatibility.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv2.html#cfn-pcaconnectorad-template-privatekeyflagsv2-clientversion
            '''
            result = self._values.get("client_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exportable_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows the private key to be exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv2.html#cfn-pcaconnectorad-template-privatekeyflagsv2-exportablekey
            '''
            result = self._values.get("exportable_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def strong_key_protection_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Require user input when using the private key for enrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv2.html#cfn-pcaconnectorad-template-privatekeyflagsv2-strongkeyprotectionrequired
            '''
            result = self._values.get("strong_key_protection_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateKeyFlagsV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "client_version": "clientVersion",
            "exportable_key": "exportableKey",
            "require_alternate_signature_algorithm": "requireAlternateSignatureAlgorithm",
            "strong_key_protection_required": "strongKeyProtectionRequired",
        },
    )
    class PrivateKeyFlagsV3Property:
        def __init__(
            self,
            *,
            client_version: typing.Optional[builtins.str] = None,
            exportable_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_alternate_signature_algorithm: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            strong_key_protection_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Private key flags for v3 templates specify the client compatibility, if the private key can be exported, if user input is required when using a private key, and if an alternate signature algorithm should be used.

            :param client_version: Defines the minimum client compatibility.
            :param exportable_key: Allows the private key to be exported.
            :param require_alternate_signature_algorithm: Reguires the PKCS #1 v2.1 signature format for certificates. You should verify that your CA, objects, and applications can accept this signature format.
            :param strong_key_protection_required: Requirer user input when using the private key for enrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                private_key_flags_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV3Property(
                    client_version="clientVersion",
                    exportable_key=False,
                    require_alternate_signature_algorithm=False,
                    strong_key_protection_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ad22943c153b2434fe0109c30b2ff6157350b51efa03e41d577e8e5a3a02209)
                check_type(argname="argument client_version", value=client_version, expected_type=type_hints["client_version"])
                check_type(argname="argument exportable_key", value=exportable_key, expected_type=type_hints["exportable_key"])
                check_type(argname="argument require_alternate_signature_algorithm", value=require_alternate_signature_algorithm, expected_type=type_hints["require_alternate_signature_algorithm"])
                check_type(argname="argument strong_key_protection_required", value=strong_key_protection_required, expected_type=type_hints["strong_key_protection_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_version is not None:
                self._values["client_version"] = client_version
            if exportable_key is not None:
                self._values["exportable_key"] = exportable_key
            if require_alternate_signature_algorithm is not None:
                self._values["require_alternate_signature_algorithm"] = require_alternate_signature_algorithm
            if strong_key_protection_required is not None:
                self._values["strong_key_protection_required"] = strong_key_protection_required

        @builtins.property
        def client_version(self) -> typing.Optional[builtins.str]:
            '''Defines the minimum client compatibility.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv3.html#cfn-pcaconnectorad-template-privatekeyflagsv3-clientversion
            '''
            result = self._values.get("client_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exportable_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows the private key to be exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv3.html#cfn-pcaconnectorad-template-privatekeyflagsv3-exportablekey
            '''
            result = self._values.get("exportable_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_alternate_signature_algorithm(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Reguires the PKCS #1 v2.1 signature format for certificates. You should verify that your CA, objects, and applications can accept this signature format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv3.html#cfn-pcaconnectorad-template-privatekeyflagsv3-requirealternatesignaturealgorithm
            '''
            result = self._values.get("require_alternate_signature_algorithm")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def strong_key_protection_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Requirer user input when using the private key for enrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv3.html#cfn-pcaconnectorad-template-privatekeyflagsv3-strongkeyprotectionrequired
            '''
            result = self._values.get("strong_key_protection_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateKeyFlagsV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "client_version": "clientVersion",
            "exportable_key": "exportableKey",
            "require_alternate_signature_algorithm": "requireAlternateSignatureAlgorithm",
            "require_same_key_renewal": "requireSameKeyRenewal",
            "strong_key_protection_required": "strongKeyProtectionRequired",
            "use_legacy_provider": "useLegacyProvider",
        },
    )
    class PrivateKeyFlagsV4Property:
        def __init__(
            self,
            *,
            client_version: typing.Optional[builtins.str] = None,
            exportable_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_alternate_signature_algorithm: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_same_key_renewal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            strong_key_protection_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            use_legacy_provider: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Private key flags for v4 templates specify the client compatibility, if the private key can be exported, if user input is required when using a private key, if an alternate signature algorithm should be used, and if certificates are renewed using the same private key.

            :param client_version: Defines the minimum client compatibility.
            :param exportable_key: Allows the private key to be exported.
            :param require_alternate_signature_algorithm: Requires the PKCS #1 v2.1 signature format for certificates. You should verify that your CA, objects, and applications can accept this signature format.
            :param require_same_key_renewal: Renew certificate using the same private key.
            :param strong_key_protection_required: Require user input when using the private key for enrollment.
            :param use_legacy_provider: Specifies the cryptographic service provider category used to generate private keys. Set to TRUE to use Legacy Cryptographic Service Providers and FALSE to use Key Storage Providers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                private_key_flags_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV4Property(
                    client_version="clientVersion",
                    exportable_key=False,
                    require_alternate_signature_algorithm=False,
                    require_same_key_renewal=False,
                    strong_key_protection_required=False,
                    use_legacy_provider=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64c10735713efb0e7cb52e0d60b784864fd81df9c79647e90877f8921b5f1d38)
                check_type(argname="argument client_version", value=client_version, expected_type=type_hints["client_version"])
                check_type(argname="argument exportable_key", value=exportable_key, expected_type=type_hints["exportable_key"])
                check_type(argname="argument require_alternate_signature_algorithm", value=require_alternate_signature_algorithm, expected_type=type_hints["require_alternate_signature_algorithm"])
                check_type(argname="argument require_same_key_renewal", value=require_same_key_renewal, expected_type=type_hints["require_same_key_renewal"])
                check_type(argname="argument strong_key_protection_required", value=strong_key_protection_required, expected_type=type_hints["strong_key_protection_required"])
                check_type(argname="argument use_legacy_provider", value=use_legacy_provider, expected_type=type_hints["use_legacy_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_version is not None:
                self._values["client_version"] = client_version
            if exportable_key is not None:
                self._values["exportable_key"] = exportable_key
            if require_alternate_signature_algorithm is not None:
                self._values["require_alternate_signature_algorithm"] = require_alternate_signature_algorithm
            if require_same_key_renewal is not None:
                self._values["require_same_key_renewal"] = require_same_key_renewal
            if strong_key_protection_required is not None:
                self._values["strong_key_protection_required"] = strong_key_protection_required
            if use_legacy_provider is not None:
                self._values["use_legacy_provider"] = use_legacy_provider

        @builtins.property
        def client_version(self) -> typing.Optional[builtins.str]:
            '''Defines the minimum client compatibility.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html#cfn-pcaconnectorad-template-privatekeyflagsv4-clientversion
            '''
            result = self._values.get("client_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exportable_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Allows the private key to be exported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html#cfn-pcaconnectorad-template-privatekeyflagsv4-exportablekey
            '''
            result = self._values.get("exportable_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_alternate_signature_algorithm(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Requires the PKCS #1 v2.1 signature format for certificates. You should verify that your CA, objects, and applications can accept this signature format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html#cfn-pcaconnectorad-template-privatekeyflagsv4-requirealternatesignaturealgorithm
            '''
            result = self._values.get("require_alternate_signature_algorithm")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_same_key_renewal(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Renew certificate using the same private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html#cfn-pcaconnectorad-template-privatekeyflagsv4-requiresamekeyrenewal
            '''
            result = self._values.get("require_same_key_renewal")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def strong_key_protection_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Require user input when using the private key for enrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html#cfn-pcaconnectorad-template-privatekeyflagsv4-strongkeyprotectionrequired
            '''
            result = self._values.get("strong_key_protection_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def use_legacy_provider(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the cryptographic service provider category used to generate private keys.

            Set to TRUE to use Legacy Cryptographic Service Providers and FALSE to use Key Storage Providers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-privatekeyflagsv4.html#cfn-pcaconnectorad-template-privatekeyflagsv4-uselegacyprovider
            '''
            result = self._values.get("use_legacy_provider")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateKeyFlagsV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.SubjectNameFlagsV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "require_common_name": "requireCommonName",
            "require_directory_path": "requireDirectoryPath",
            "require_dns_as_cn": "requireDnsAsCn",
            "require_email": "requireEmail",
            "san_require_directory_guid": "sanRequireDirectoryGuid",
            "san_require_dns": "sanRequireDns",
            "san_require_domain_dns": "sanRequireDomainDns",
            "san_require_email": "sanRequireEmail",
            "san_require_spn": "sanRequireSpn",
            "san_require_upn": "sanRequireUpn",
        },
    )
    class SubjectNameFlagsV2Property:
        def __init__(
            self,
            *,
            require_common_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_directory_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_dns_as_cn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_directory_guid: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_domain_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_spn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_upn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information to include in the subject name and alternate subject name of the certificate.

            The subject name can be common name, directory path, DNS as common name, or left blank. You can optionally include email to the subject name for user templates. If you leave the subject name blank then you must set a subject alternate name. The subject alternate name (SAN) can include globally unique identifier (GUID), DNS, domain DNS, email, service principal name (SPN), and user principal name (UPN). You can leave the SAN blank. If you leave the SAN blank, then you must set a subject name.

            :param require_common_name: Include the common name in the subject name.
            :param require_directory_path: Include the directory path in the subject name.
            :param require_dns_as_cn: Include the DNS as common name in the subject name.
            :param require_email: Include the subject's email in the subject name.
            :param san_require_directory_guid: Include the globally unique identifier (GUID) in the subject alternate name.
            :param san_require_dns: Include the DNS in the subject alternate name.
            :param san_require_domain_dns: Include the domain DNS in the subject alternate name.
            :param san_require_email: Include the subject's email in the subject alternate name.
            :param san_require_spn: Include the service principal name (SPN) in the subject alternate name.
            :param san_require_upn: Include the user principal name (UPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                subject_name_flags_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV2Property(
                    require_common_name=False,
                    require_directory_path=False,
                    require_dns_as_cn=False,
                    require_email=False,
                    san_require_directory_guid=False,
                    san_require_dns=False,
                    san_require_domain_dns=False,
                    san_require_email=False,
                    san_require_spn=False,
                    san_require_upn=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c453755889eaa4fe7a699647915ad7751f995c1ca0a7122c6cc6e85976bc3904)
                check_type(argname="argument require_common_name", value=require_common_name, expected_type=type_hints["require_common_name"])
                check_type(argname="argument require_directory_path", value=require_directory_path, expected_type=type_hints["require_directory_path"])
                check_type(argname="argument require_dns_as_cn", value=require_dns_as_cn, expected_type=type_hints["require_dns_as_cn"])
                check_type(argname="argument require_email", value=require_email, expected_type=type_hints["require_email"])
                check_type(argname="argument san_require_directory_guid", value=san_require_directory_guid, expected_type=type_hints["san_require_directory_guid"])
                check_type(argname="argument san_require_dns", value=san_require_dns, expected_type=type_hints["san_require_dns"])
                check_type(argname="argument san_require_domain_dns", value=san_require_domain_dns, expected_type=type_hints["san_require_domain_dns"])
                check_type(argname="argument san_require_email", value=san_require_email, expected_type=type_hints["san_require_email"])
                check_type(argname="argument san_require_spn", value=san_require_spn, expected_type=type_hints["san_require_spn"])
                check_type(argname="argument san_require_upn", value=san_require_upn, expected_type=type_hints["san_require_upn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if require_common_name is not None:
                self._values["require_common_name"] = require_common_name
            if require_directory_path is not None:
                self._values["require_directory_path"] = require_directory_path
            if require_dns_as_cn is not None:
                self._values["require_dns_as_cn"] = require_dns_as_cn
            if require_email is not None:
                self._values["require_email"] = require_email
            if san_require_directory_guid is not None:
                self._values["san_require_directory_guid"] = san_require_directory_guid
            if san_require_dns is not None:
                self._values["san_require_dns"] = san_require_dns
            if san_require_domain_dns is not None:
                self._values["san_require_domain_dns"] = san_require_domain_dns
            if san_require_email is not None:
                self._values["san_require_email"] = san_require_email
            if san_require_spn is not None:
                self._values["san_require_spn"] = san_require_spn
            if san_require_upn is not None:
                self._values["san_require_upn"] = san_require_upn

        @builtins.property
        def require_common_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the common name in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-requirecommonname
            '''
            result = self._values.get("require_common_name")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_directory_path(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the directory path in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-requiredirectorypath
            '''
            result = self._values.get("require_directory_path")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_dns_as_cn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the DNS as common name in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-requirednsascn
            '''
            result = self._values.get("require_dns_as_cn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_email(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the subject's email in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-requireemail
            '''
            result = self._values.get("require_email")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_directory_guid(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the globally unique identifier (GUID) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-sanrequiredirectoryguid
            '''
            result = self._values.get("san_require_directory_guid")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_dns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the DNS in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-sanrequiredns
            '''
            result = self._values.get("san_require_dns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_domain_dns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the domain DNS in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-sanrequiredomaindns
            '''
            result = self._values.get("san_require_domain_dns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_email(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the subject's email in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-sanrequireemail
            '''
            result = self._values.get("san_require_email")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_spn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the service principal name (SPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-sanrequirespn
            '''
            result = self._values.get("san_require_spn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_upn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the user principal name (UPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv2.html#cfn-pcaconnectorad-template-subjectnameflagsv2-sanrequireupn
            '''
            result = self._values.get("san_require_upn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectNameFlagsV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.SubjectNameFlagsV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "require_common_name": "requireCommonName",
            "require_directory_path": "requireDirectoryPath",
            "require_dns_as_cn": "requireDnsAsCn",
            "require_email": "requireEmail",
            "san_require_directory_guid": "sanRequireDirectoryGuid",
            "san_require_dns": "sanRequireDns",
            "san_require_domain_dns": "sanRequireDomainDns",
            "san_require_email": "sanRequireEmail",
            "san_require_spn": "sanRequireSpn",
            "san_require_upn": "sanRequireUpn",
        },
    )
    class SubjectNameFlagsV3Property:
        def __init__(
            self,
            *,
            require_common_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_directory_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_dns_as_cn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_directory_guid: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_domain_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_spn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_upn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information to include in the subject name and alternate subject name of the certificate.

            The subject name can be common name, directory path, DNS as common name, or left blank. You can optionally include email to the subject name for user templates. If you leave the subject name blank then you must set a subject alternate name. The subject alternate name (SAN) can include globally unique identifier (GUID), DNS, domain DNS, email, service principal name (SPN), and user principal name (UPN). You can leave the SAN blank. If you leave the SAN blank, then you must set a subject name.

            :param require_common_name: Include the common name in the subject name.
            :param require_directory_path: Include the directory path in the subject name.
            :param require_dns_as_cn: Include the DNS as common name in the subject name.
            :param require_email: Include the subject's email in the subject name.
            :param san_require_directory_guid: Include the globally unique identifier (GUID) in the subject alternate name.
            :param san_require_dns: Include the DNS in the subject alternate name.
            :param san_require_domain_dns: Include the domain DNS in the subject alternate name.
            :param san_require_email: Include the subject's email in the subject alternate name.
            :param san_require_spn: Include the service principal name (SPN) in the subject alternate name.
            :param san_require_upn: Include the user principal name (UPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                subject_name_flags_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV3Property(
                    require_common_name=False,
                    require_directory_path=False,
                    require_dns_as_cn=False,
                    require_email=False,
                    san_require_directory_guid=False,
                    san_require_dns=False,
                    san_require_domain_dns=False,
                    san_require_email=False,
                    san_require_spn=False,
                    san_require_upn=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__694941c5b547122e3465e292a3f0aa46c95b68dee22258aa5b4edeb3b554e708)
                check_type(argname="argument require_common_name", value=require_common_name, expected_type=type_hints["require_common_name"])
                check_type(argname="argument require_directory_path", value=require_directory_path, expected_type=type_hints["require_directory_path"])
                check_type(argname="argument require_dns_as_cn", value=require_dns_as_cn, expected_type=type_hints["require_dns_as_cn"])
                check_type(argname="argument require_email", value=require_email, expected_type=type_hints["require_email"])
                check_type(argname="argument san_require_directory_guid", value=san_require_directory_guid, expected_type=type_hints["san_require_directory_guid"])
                check_type(argname="argument san_require_dns", value=san_require_dns, expected_type=type_hints["san_require_dns"])
                check_type(argname="argument san_require_domain_dns", value=san_require_domain_dns, expected_type=type_hints["san_require_domain_dns"])
                check_type(argname="argument san_require_email", value=san_require_email, expected_type=type_hints["san_require_email"])
                check_type(argname="argument san_require_spn", value=san_require_spn, expected_type=type_hints["san_require_spn"])
                check_type(argname="argument san_require_upn", value=san_require_upn, expected_type=type_hints["san_require_upn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if require_common_name is not None:
                self._values["require_common_name"] = require_common_name
            if require_directory_path is not None:
                self._values["require_directory_path"] = require_directory_path
            if require_dns_as_cn is not None:
                self._values["require_dns_as_cn"] = require_dns_as_cn
            if require_email is not None:
                self._values["require_email"] = require_email
            if san_require_directory_guid is not None:
                self._values["san_require_directory_guid"] = san_require_directory_guid
            if san_require_dns is not None:
                self._values["san_require_dns"] = san_require_dns
            if san_require_domain_dns is not None:
                self._values["san_require_domain_dns"] = san_require_domain_dns
            if san_require_email is not None:
                self._values["san_require_email"] = san_require_email
            if san_require_spn is not None:
                self._values["san_require_spn"] = san_require_spn
            if san_require_upn is not None:
                self._values["san_require_upn"] = san_require_upn

        @builtins.property
        def require_common_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the common name in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-requirecommonname
            '''
            result = self._values.get("require_common_name")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_directory_path(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the directory path in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-requiredirectorypath
            '''
            result = self._values.get("require_directory_path")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_dns_as_cn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the DNS as common name in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-requirednsascn
            '''
            result = self._values.get("require_dns_as_cn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_email(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the subject's email in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-requireemail
            '''
            result = self._values.get("require_email")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_directory_guid(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the globally unique identifier (GUID) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-sanrequiredirectoryguid
            '''
            result = self._values.get("san_require_directory_guid")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_dns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the DNS in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-sanrequiredns
            '''
            result = self._values.get("san_require_dns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_domain_dns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the domain DNS in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-sanrequiredomaindns
            '''
            result = self._values.get("san_require_domain_dns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_email(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the subject's email in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-sanrequireemail
            '''
            result = self._values.get("san_require_email")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_spn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the service principal name (SPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-sanrequirespn
            '''
            result = self._values.get("san_require_spn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_upn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the user principal name (UPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv3.html#cfn-pcaconnectorad-template-subjectnameflagsv3-sanrequireupn
            '''
            result = self._values.get("san_require_upn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectNameFlagsV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.SubjectNameFlagsV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "require_common_name": "requireCommonName",
            "require_directory_path": "requireDirectoryPath",
            "require_dns_as_cn": "requireDnsAsCn",
            "require_email": "requireEmail",
            "san_require_directory_guid": "sanRequireDirectoryGuid",
            "san_require_dns": "sanRequireDns",
            "san_require_domain_dns": "sanRequireDomainDns",
            "san_require_email": "sanRequireEmail",
            "san_require_spn": "sanRequireSpn",
            "san_require_upn": "sanRequireUpn",
        },
    )
    class SubjectNameFlagsV4Property:
        def __init__(
            self,
            *,
            require_common_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_directory_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_dns_as_cn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_directory_guid: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_domain_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_spn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            san_require_upn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Information to include in the subject name and alternate subject name of the certificate.

            The subject name can be common name, directory path, DNS as common name, or left blank. You can optionally include email to the subject name for user templates. If you leave the subject name blank then you must set a subject alternate name. The subject alternate name (SAN) can include globally unique identifier (GUID), DNS, domain DNS, email, service principal name (SPN), and user principal name (UPN). You can leave the SAN blank. If you leave the SAN blank, then you must set a subject name.

            :param require_common_name: Include the common name in the subject name.
            :param require_directory_path: Include the directory path in the subject name.
            :param require_dns_as_cn: Include the DNS as common name in the subject name.
            :param require_email: Include the subject's email in the subject name.
            :param san_require_directory_guid: Include the globally unique identifier (GUID) in the subject alternate name.
            :param san_require_dns: Include the DNS in the subject alternate name.
            :param san_require_domain_dns: Include the domain DNS in the subject alternate name.
            :param san_require_email: Include the subject's email in the subject alternate name.
            :param san_require_spn: Include the service principal name (SPN) in the subject alternate name.
            :param san_require_upn: Include the user principal name (UPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                subject_name_flags_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV4Property(
                    require_common_name=False,
                    require_directory_path=False,
                    require_dns_as_cn=False,
                    require_email=False,
                    san_require_directory_guid=False,
                    san_require_dns=False,
                    san_require_domain_dns=False,
                    san_require_email=False,
                    san_require_spn=False,
                    san_require_upn=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6da9e5f6eba88f30e600b17a15cdb12510ae4ba090e5f5fbbf645eb3d22b7a89)
                check_type(argname="argument require_common_name", value=require_common_name, expected_type=type_hints["require_common_name"])
                check_type(argname="argument require_directory_path", value=require_directory_path, expected_type=type_hints["require_directory_path"])
                check_type(argname="argument require_dns_as_cn", value=require_dns_as_cn, expected_type=type_hints["require_dns_as_cn"])
                check_type(argname="argument require_email", value=require_email, expected_type=type_hints["require_email"])
                check_type(argname="argument san_require_directory_guid", value=san_require_directory_guid, expected_type=type_hints["san_require_directory_guid"])
                check_type(argname="argument san_require_dns", value=san_require_dns, expected_type=type_hints["san_require_dns"])
                check_type(argname="argument san_require_domain_dns", value=san_require_domain_dns, expected_type=type_hints["san_require_domain_dns"])
                check_type(argname="argument san_require_email", value=san_require_email, expected_type=type_hints["san_require_email"])
                check_type(argname="argument san_require_spn", value=san_require_spn, expected_type=type_hints["san_require_spn"])
                check_type(argname="argument san_require_upn", value=san_require_upn, expected_type=type_hints["san_require_upn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if require_common_name is not None:
                self._values["require_common_name"] = require_common_name
            if require_directory_path is not None:
                self._values["require_directory_path"] = require_directory_path
            if require_dns_as_cn is not None:
                self._values["require_dns_as_cn"] = require_dns_as_cn
            if require_email is not None:
                self._values["require_email"] = require_email
            if san_require_directory_guid is not None:
                self._values["san_require_directory_guid"] = san_require_directory_guid
            if san_require_dns is not None:
                self._values["san_require_dns"] = san_require_dns
            if san_require_domain_dns is not None:
                self._values["san_require_domain_dns"] = san_require_domain_dns
            if san_require_email is not None:
                self._values["san_require_email"] = san_require_email
            if san_require_spn is not None:
                self._values["san_require_spn"] = san_require_spn
            if san_require_upn is not None:
                self._values["san_require_upn"] = san_require_upn

        @builtins.property
        def require_common_name(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the common name in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-requirecommonname
            '''
            result = self._values.get("require_common_name")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_directory_path(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the directory path in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-requiredirectorypath
            '''
            result = self._values.get("require_directory_path")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_dns_as_cn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the DNS as common name in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-requirednsascn
            '''
            result = self._values.get("require_dns_as_cn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def require_email(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the subject's email in the subject name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-requireemail
            '''
            result = self._values.get("require_email")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_directory_guid(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the globally unique identifier (GUID) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-sanrequiredirectoryguid
            '''
            result = self._values.get("san_require_directory_guid")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_dns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the DNS in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-sanrequiredns
            '''
            result = self._values.get("san_require_dns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_domain_dns(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the domain DNS in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-sanrequiredomaindns
            '''
            result = self._values.get("san_require_domain_dns")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_email(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the subject's email in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-sanrequireemail
            '''
            result = self._values.get("san_require_email")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_spn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the service principal name (SPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-sanrequirespn
            '''
            result = self._values.get("san_require_spn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def san_require_upn(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Include the user principal name (UPN) in the subject alternate name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-subjectnameflagsv4.html#cfn-pcaconnectorad-template-subjectnameflagsv4-sanrequireupn
            '''
            result = self._values.get("san_require_upn")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectNameFlagsV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.TemplateDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "template_v2": "templateV2",
            "template_v3": "templateV3",
            "template_v4": "templateV4",
        },
    )
    class TemplateDefinitionProperty:
        def __init__(
            self,
            *,
            template_v2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.TemplateV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            template_v3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.TemplateV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            template_v4: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.TemplateV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Template configuration to define the information included in certificates.

            Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.

            :param template_v2: Template configuration to define the information included in certificates. Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.
            :param template_v3: Template configuration to define the information included in certificates. Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.
            :param template_v4: Template configuration to define the information included in certificates. Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatedefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                template_definition_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateDefinitionProperty(
                    template_v2=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV2Property(
                        certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                            renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            ),
                            validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            )
                        ),
                        enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV2Property(
                            enable_key_reuse_on_nt_token_keyset_storage_full=False,
                            include_symmetric_algorithms=False,
                            no_security_extension=False,
                            remove_invalid_certificate_from_personal_store=False,
                            user_interaction_required=False
                        ),
                        extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV2Property(
                            application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                                critical=False,
                                policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                    policy_object_identifier="policyObjectIdentifier",
                                    policy_type="policyType"
                                )]
                            ),
                            key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                                critical=False,
                                usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                    data_encipherment=False,
                                    digital_signature=False,
                                    key_agreement=False,
                                    key_encipherment=False,
                                    non_repudiation=False
                                )
                            )
                        ),
                        general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV2Property(
                            auto_enrollment=False,
                            machine_type=False
                        ),
                        private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV2Property(
                            crypto_providers=["cryptoProviders"],
                            key_spec="keySpec",
                            minimal_key_length=123
                        ),
                        private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV2Property(
                            client_version="clientVersion",
                            exportable_key=False,
                            strong_key_protection_required=False
                        ),
                        subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV2Property(
                            require_common_name=False,
                            require_directory_path=False,
                            require_dns_as_cn=False,
                            require_email=False,
                            san_require_directory_guid=False,
                            san_require_dns=False,
                            san_require_domain_dns=False,
                            san_require_email=False,
                            san_require_spn=False,
                            san_require_upn=False
                        ),
                        superseded_templates=["supersededTemplates"]
                    ),
                    template_v3=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV3Property(
                        certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                            renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            ),
                            validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            )
                        ),
                        enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV3Property(
                            enable_key_reuse_on_nt_token_keyset_storage_full=False,
                            include_symmetric_algorithms=False,
                            no_security_extension=False,
                            remove_invalid_certificate_from_personal_store=False,
                            user_interaction_required=False
                        ),
                        extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV3Property(
                            application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                                critical=False,
                                policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                    policy_object_identifier="policyObjectIdentifier",
                                    policy_type="policyType"
                                )]
                            ),
                            key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                                critical=False,
                                usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                    data_encipherment=False,
                                    digital_signature=False,
                                    key_agreement=False,
                                    key_encipherment=False,
                                    non_repudiation=False
                                )
                            )
                        ),
                        general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV3Property(
                            auto_enrollment=False,
                            machine_type=False
                        ),
                        hash_algorithm="hashAlgorithm",
                        private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV3Property(
                            algorithm="algorithm",
                            crypto_providers=["cryptoProviders"],
                            key_spec="keySpec",
                            key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                                property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                    decrypt=False,
                                    key_agreement=False,
                                    sign=False
                                ),
                                property_type="propertyType"
                            ),
                            minimal_key_length=123
                        ),
                        private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV3Property(
                            client_version="clientVersion",
                            exportable_key=False,
                            require_alternate_signature_algorithm=False,
                            strong_key_protection_required=False
                        ),
                        subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV3Property(
                            require_common_name=False,
                            require_directory_path=False,
                            require_dns_as_cn=False,
                            require_email=False,
                            san_require_directory_guid=False,
                            san_require_dns=False,
                            san_require_domain_dns=False,
                            san_require_email=False,
                            san_require_spn=False,
                            san_require_upn=False
                        ),
                        superseded_templates=["supersededTemplates"]
                    ),
                    template_v4=pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV4Property(
                        certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                            renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            ),
                            validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                                period=123,
                                period_type="periodType"
                            )
                        ),
                        enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV4Property(
                            enable_key_reuse_on_nt_token_keyset_storage_full=False,
                            include_symmetric_algorithms=False,
                            no_security_extension=False,
                            remove_invalid_certificate_from_personal_store=False,
                            user_interaction_required=False
                        ),
                        extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV4Property(
                            application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                                critical=False,
                                policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                    policy_object_identifier="policyObjectIdentifier",
                                    policy_type="policyType"
                                )]
                            ),
                            key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                                critical=False,
                                usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                    data_encipherment=False,
                                    digital_signature=False,
                                    key_agreement=False,
                                    key_encipherment=False,
                                    non_repudiation=False
                                )
                            )
                        ),
                        general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV4Property(
                            auto_enrollment=False,
                            machine_type=False
                        ),
                        hash_algorithm="hashAlgorithm",
                        private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV4Property(
                            algorithm="algorithm",
                            crypto_providers=["cryptoProviders"],
                            key_spec="keySpec",
                            key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                                property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                    decrypt=False,
                                    key_agreement=False,
                                    sign=False
                                ),
                                property_type="propertyType"
                            ),
                            minimal_key_length=123
                        ),
                        private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV4Property(
                            client_version="clientVersion",
                            exportable_key=False,
                            require_alternate_signature_algorithm=False,
                            require_same_key_renewal=False,
                            strong_key_protection_required=False,
                            use_legacy_provider=False
                        ),
                        subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV4Property(
                            require_common_name=False,
                            require_directory_path=False,
                            require_dns_as_cn=False,
                            require_email=False,
                            san_require_directory_guid=False,
                            san_require_dns=False,
                            san_require_domain_dns=False,
                            san_require_email=False,
                            san_require_spn=False,
                            san_require_upn=False
                        ),
                        superseded_templates=["supersededTemplates"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2688bfc145892d31555199d49aa02e203684f31a77a509b08b26c88d51131630)
                check_type(argname="argument template_v2", value=template_v2, expected_type=type_hints["template_v2"])
                check_type(argname="argument template_v3", value=template_v3, expected_type=type_hints["template_v3"])
                check_type(argname="argument template_v4", value=template_v4, expected_type=type_hints["template_v4"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if template_v2 is not None:
                self._values["template_v2"] = template_v2
            if template_v3 is not None:
                self._values["template_v3"] = template_v3
            if template_v4 is not None:
                self._values["template_v4"] = template_v4

        @builtins.property
        def template_v2(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateV2Property"]]:
            '''Template configuration to define the information included in certificates.

            Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatedefinition.html#cfn-pcaconnectorad-template-templatedefinition-templatev2
            '''
            result = self._values.get("template_v2")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateV2Property"]], result)

        @builtins.property
        def template_v3(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateV3Property"]]:
            '''Template configuration to define the information included in certificates.

            Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatedefinition.html#cfn-pcaconnectorad-template-templatedefinition-templatev3
            '''
            result = self._values.get("template_v3")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateV3Property"]], result)

        @builtins.property
        def template_v4(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateV4Property"]]:
            '''Template configuration to define the information included in certificates.

            Define certificate validity and renewal periods, certificate request handling and enrollment options, key usage extensions, application policies, and cryptography settings.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatedefinition.html#cfn-pcaconnectorad-template-templatedefinition-templatev4
            '''
            result = self._values.get("template_v4")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.TemplateV4Property"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.TemplateV2Property",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_validity": "certificateValidity",
            "enrollment_flags": "enrollmentFlags",
            "extensions": "extensions",
            "general_flags": "generalFlags",
            "private_key_attributes": "privateKeyAttributes",
            "private_key_flags": "privateKeyFlags",
            "subject_name_flags": "subjectNameFlags",
            "superseded_templates": "supersededTemplates",
        },
    )
    class TemplateV2Property:
        def __init__(
            self,
            *,
            certificate_validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.CertificateValidityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enrollment_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.EnrollmentFlagsV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ExtensionsV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            general_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.GeneralFlagsV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            private_key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.PrivateKeyAttributesV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            private_key_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.PrivateKeyFlagsV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_name_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.SubjectNameFlagsV2Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            superseded_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''v2 template schema that uses Legacy Cryptographic Providers.

            :param certificate_validity: Certificate validity describes the validity and renewal periods of a certificate.
            :param enrollment_flags: Enrollment flags describe the enrollment settings for certificates such as using the existing private key and deleting expired or revoked certificates.
            :param extensions: Extensions describe the key usage extensions and application policies for a template.
            :param general_flags: General flags describe whether the template is used for computers or users and if the template can be used with autoenrollment.
            :param private_key_attributes: Private key attributes allow you to specify the minimal key length, key spec, and cryptographic providers for the private key of a certificate for v2 templates. V2 templates allow you to use Legacy Cryptographic Service Providers.
            :param private_key_flags: Private key flags for v2 templates specify the client compatibility, if the private key can be exported, and if user input is required when using a private key.
            :param subject_name_flags: Subject name flags describe the subject name and subject alternate name that is included in a certificate.
            :param superseded_templates: List of templates in Active Directory that are superseded by this template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                template_v2_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV2Property(
                    certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                        renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        ),
                        validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        )
                    ),
                    enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV2Property(
                        enable_key_reuse_on_nt_token_keyset_storage_full=False,
                        include_symmetric_algorithms=False,
                        no_security_extension=False,
                        remove_invalid_certificate_from_personal_store=False,
                        user_interaction_required=False
                    ),
                    extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV2Property(
                        application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                            critical=False,
                            policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                policy_object_identifier="policyObjectIdentifier",
                                policy_type="policyType"
                            )]
                        ),
                        key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                            critical=False,
                            usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                data_encipherment=False,
                                digital_signature=False,
                                key_agreement=False,
                                key_encipherment=False,
                                non_repudiation=False
                            )
                        )
                    ),
                    general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV2Property(
                        auto_enrollment=False,
                        machine_type=False
                    ),
                    private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV2Property(
                        crypto_providers=["cryptoProviders"],
                        key_spec="keySpec",
                        minimal_key_length=123
                    ),
                    private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV2Property(
                        client_version="clientVersion",
                        exportable_key=False,
                        strong_key_protection_required=False
                    ),
                    subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV2Property(
                        require_common_name=False,
                        require_directory_path=False,
                        require_dns_as_cn=False,
                        require_email=False,
                        san_require_directory_guid=False,
                        san_require_dns=False,
                        san_require_domain_dns=False,
                        san_require_email=False,
                        san_require_spn=False,
                        san_require_upn=False
                    ),
                    superseded_templates=["supersededTemplates"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4b7293a76d58fd2beb7557a6c8e2eb9633b0300e054719df51eebf91818729f0)
                check_type(argname="argument certificate_validity", value=certificate_validity, expected_type=type_hints["certificate_validity"])
                check_type(argname="argument enrollment_flags", value=enrollment_flags, expected_type=type_hints["enrollment_flags"])
                check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
                check_type(argname="argument general_flags", value=general_flags, expected_type=type_hints["general_flags"])
                check_type(argname="argument private_key_attributes", value=private_key_attributes, expected_type=type_hints["private_key_attributes"])
                check_type(argname="argument private_key_flags", value=private_key_flags, expected_type=type_hints["private_key_flags"])
                check_type(argname="argument subject_name_flags", value=subject_name_flags, expected_type=type_hints["subject_name_flags"])
                check_type(argname="argument superseded_templates", value=superseded_templates, expected_type=type_hints["superseded_templates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_validity is not None:
                self._values["certificate_validity"] = certificate_validity
            if enrollment_flags is not None:
                self._values["enrollment_flags"] = enrollment_flags
            if extensions is not None:
                self._values["extensions"] = extensions
            if general_flags is not None:
                self._values["general_flags"] = general_flags
            if private_key_attributes is not None:
                self._values["private_key_attributes"] = private_key_attributes
            if private_key_flags is not None:
                self._values["private_key_flags"] = private_key_flags
            if subject_name_flags is not None:
                self._values["subject_name_flags"] = subject_name_flags
            if superseded_templates is not None:
                self._values["superseded_templates"] = superseded_templates

        @builtins.property
        def certificate_validity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.CertificateValidityProperty"]]:
            '''Certificate validity describes the validity and renewal periods of a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-certificatevalidity
            '''
            result = self._values.get("certificate_validity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.CertificateValidityProperty"]], result)

        @builtins.property
        def enrollment_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.EnrollmentFlagsV2Property"]]:
            '''Enrollment flags describe the enrollment settings for certificates such as using the existing private key and deleting expired or revoked certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-enrollmentflags
            '''
            result = self._values.get("enrollment_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.EnrollmentFlagsV2Property"]], result)

        @builtins.property
        def extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ExtensionsV2Property"]]:
            '''Extensions describe the key usage extensions and application policies for a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-extensions
            '''
            result = self._values.get("extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ExtensionsV2Property"]], result)

        @builtins.property
        def general_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.GeneralFlagsV2Property"]]:
            '''General flags describe whether the template is used for computers or users and if the template can be used with autoenrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-generalflags
            '''
            result = self._values.get("general_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.GeneralFlagsV2Property"]], result)

        @builtins.property
        def private_key_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyAttributesV2Property"]]:
            '''Private key attributes allow you to specify the minimal key length, key spec, and cryptographic providers for the private key of a certificate for v2 templates.

            V2 templates allow you to use Legacy Cryptographic Service Providers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-privatekeyattributes
            '''
            result = self._values.get("private_key_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyAttributesV2Property"]], result)

        @builtins.property
        def private_key_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyFlagsV2Property"]]:
            '''Private key flags for v2 templates specify the client compatibility, if the private key can be exported, and if user input is required when using a private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-privatekeyflags
            '''
            result = self._values.get("private_key_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyFlagsV2Property"]], result)

        @builtins.property
        def subject_name_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.SubjectNameFlagsV2Property"]]:
            '''Subject name flags describe the subject name and subject alternate name that is included in a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-subjectnameflags
            '''
            result = self._values.get("subject_name_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.SubjectNameFlagsV2Property"]], result)

        @builtins.property
        def superseded_templates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of templates in Active Directory that are superseded by this template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev2.html#cfn-pcaconnectorad-template-templatev2-supersededtemplates
            '''
            result = self._values.get("superseded_templates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateV2Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.TemplateV3Property",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_validity": "certificateValidity",
            "enrollment_flags": "enrollmentFlags",
            "extensions": "extensions",
            "general_flags": "generalFlags",
            "hash_algorithm": "hashAlgorithm",
            "private_key_attributes": "privateKeyAttributes",
            "private_key_flags": "privateKeyFlags",
            "subject_name_flags": "subjectNameFlags",
            "superseded_templates": "supersededTemplates",
        },
    )
    class TemplateV3Property:
        def __init__(
            self,
            *,
            certificate_validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.CertificateValidityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enrollment_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.EnrollmentFlagsV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ExtensionsV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            general_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.GeneralFlagsV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            hash_algorithm: typing.Optional[builtins.str] = None,
            private_key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.PrivateKeyAttributesV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            private_key_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.PrivateKeyFlagsV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_name_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.SubjectNameFlagsV3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            superseded_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''v3 template schema that uses Key Storage Providers.

            :param certificate_validity: Certificate validity describes the validity and renewal periods of a certificate.
            :param enrollment_flags: Enrollment flags describe the enrollment settings for certificates such as using the existing private key and deleting expired or revoked certificates.
            :param extensions: Extensions describe the key usage extensions and application policies for a template.
            :param general_flags: General flags describe whether the template is used for computers or users and if the template can be used with autoenrollment.
            :param hash_algorithm: Specifies the hash algorithm used to hash the private key.
            :param private_key_attributes: Private key attributes allow you to specify the algorithm, minimal key length, key spec, key usage, and cryptographic providers for the private key of a certificate for v3 templates. V3 templates allow you to use Key Storage Providers.
            :param private_key_flags: Private key flags for v3 templates specify the client compatibility, if the private key can be exported, if user input is required when using a private key, and if an alternate signature algorithm should be used.
            :param subject_name_flags: Subject name flags describe the subject name and subject alternate name that is included in a certificate.
            :param superseded_templates: List of templates in Active Directory that are superseded by this template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                template_v3_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV3Property(
                    certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                        renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        ),
                        validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        )
                    ),
                    enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV3Property(
                        enable_key_reuse_on_nt_token_keyset_storage_full=False,
                        include_symmetric_algorithms=False,
                        no_security_extension=False,
                        remove_invalid_certificate_from_personal_store=False,
                        user_interaction_required=False
                    ),
                    extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV3Property(
                        application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                            critical=False,
                            policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                policy_object_identifier="policyObjectIdentifier",
                                policy_type="policyType"
                            )]
                        ),
                        key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                            critical=False,
                            usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                data_encipherment=False,
                                digital_signature=False,
                                key_agreement=False,
                                key_encipherment=False,
                                non_repudiation=False
                            )
                        )
                    ),
                    general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV3Property(
                        auto_enrollment=False,
                        machine_type=False
                    ),
                    hash_algorithm="hashAlgorithm",
                    private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV3Property(
                        algorithm="algorithm",
                        crypto_providers=["cryptoProviders"],
                        key_spec="keySpec",
                        key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                            property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                decrypt=False,
                                key_agreement=False,
                                sign=False
                            ),
                            property_type="propertyType"
                        ),
                        minimal_key_length=123
                    ),
                    private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV3Property(
                        client_version="clientVersion",
                        exportable_key=False,
                        require_alternate_signature_algorithm=False,
                        strong_key_protection_required=False
                    ),
                    subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV3Property(
                        require_common_name=False,
                        require_directory_path=False,
                        require_dns_as_cn=False,
                        require_email=False,
                        san_require_directory_guid=False,
                        san_require_dns=False,
                        san_require_domain_dns=False,
                        san_require_email=False,
                        san_require_spn=False,
                        san_require_upn=False
                    ),
                    superseded_templates=["supersededTemplates"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dab39b87f80eaed839e53392bd2177d0094c3c6069202c6f150ef850242ce8d9)
                check_type(argname="argument certificate_validity", value=certificate_validity, expected_type=type_hints["certificate_validity"])
                check_type(argname="argument enrollment_flags", value=enrollment_flags, expected_type=type_hints["enrollment_flags"])
                check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
                check_type(argname="argument general_flags", value=general_flags, expected_type=type_hints["general_flags"])
                check_type(argname="argument hash_algorithm", value=hash_algorithm, expected_type=type_hints["hash_algorithm"])
                check_type(argname="argument private_key_attributes", value=private_key_attributes, expected_type=type_hints["private_key_attributes"])
                check_type(argname="argument private_key_flags", value=private_key_flags, expected_type=type_hints["private_key_flags"])
                check_type(argname="argument subject_name_flags", value=subject_name_flags, expected_type=type_hints["subject_name_flags"])
                check_type(argname="argument superseded_templates", value=superseded_templates, expected_type=type_hints["superseded_templates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_validity is not None:
                self._values["certificate_validity"] = certificate_validity
            if enrollment_flags is not None:
                self._values["enrollment_flags"] = enrollment_flags
            if extensions is not None:
                self._values["extensions"] = extensions
            if general_flags is not None:
                self._values["general_flags"] = general_flags
            if hash_algorithm is not None:
                self._values["hash_algorithm"] = hash_algorithm
            if private_key_attributes is not None:
                self._values["private_key_attributes"] = private_key_attributes
            if private_key_flags is not None:
                self._values["private_key_flags"] = private_key_flags
            if subject_name_flags is not None:
                self._values["subject_name_flags"] = subject_name_flags
            if superseded_templates is not None:
                self._values["superseded_templates"] = superseded_templates

        @builtins.property
        def certificate_validity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.CertificateValidityProperty"]]:
            '''Certificate validity describes the validity and renewal periods of a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-certificatevalidity
            '''
            result = self._values.get("certificate_validity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.CertificateValidityProperty"]], result)

        @builtins.property
        def enrollment_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.EnrollmentFlagsV3Property"]]:
            '''Enrollment flags describe the enrollment settings for certificates such as using the existing private key and deleting expired or revoked certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-enrollmentflags
            '''
            result = self._values.get("enrollment_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.EnrollmentFlagsV3Property"]], result)

        @builtins.property
        def extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ExtensionsV3Property"]]:
            '''Extensions describe the key usage extensions and application policies for a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-extensions
            '''
            result = self._values.get("extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ExtensionsV3Property"]], result)

        @builtins.property
        def general_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.GeneralFlagsV3Property"]]:
            '''General flags describe whether the template is used for computers or users and if the template can be used with autoenrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-generalflags
            '''
            result = self._values.get("general_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.GeneralFlagsV3Property"]], result)

        @builtins.property
        def hash_algorithm(self) -> typing.Optional[builtins.str]:
            '''Specifies the hash algorithm used to hash the private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-hashalgorithm
            '''
            result = self._values.get("hash_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_key_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyAttributesV3Property"]]:
            '''Private key attributes allow you to specify the algorithm, minimal key length, key spec, key usage, and cryptographic providers for the private key of a certificate for v3 templates.

            V3 templates allow you to use Key Storage Providers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-privatekeyattributes
            '''
            result = self._values.get("private_key_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyAttributesV3Property"]], result)

        @builtins.property
        def private_key_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyFlagsV3Property"]]:
            '''Private key flags for v3 templates specify the client compatibility, if the private key can be exported, if user input is required when using a private key, and if an alternate signature algorithm should be used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-privatekeyflags
            '''
            result = self._values.get("private_key_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyFlagsV3Property"]], result)

        @builtins.property
        def subject_name_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.SubjectNameFlagsV3Property"]]:
            '''Subject name flags describe the subject name and subject alternate name that is included in a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-subjectnameflags
            '''
            result = self._values.get("subject_name_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.SubjectNameFlagsV3Property"]], result)

        @builtins.property
        def superseded_templates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of templates in Active Directory that are superseded by this template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev3.html#cfn-pcaconnectorad-template-templatev3-supersededtemplates
            '''
            result = self._values.get("superseded_templates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateV3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.TemplateV4Property",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_validity": "certificateValidity",
            "enrollment_flags": "enrollmentFlags",
            "extensions": "extensions",
            "general_flags": "generalFlags",
            "hash_algorithm": "hashAlgorithm",
            "private_key_attributes": "privateKeyAttributes",
            "private_key_flags": "privateKeyFlags",
            "subject_name_flags": "subjectNameFlags",
            "superseded_templates": "supersededTemplates",
        },
    )
    class TemplateV4Property:
        def __init__(
            self,
            *,
            certificate_validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.CertificateValidityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enrollment_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.EnrollmentFlagsV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.ExtensionsV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            general_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.GeneralFlagsV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            hash_algorithm: typing.Optional[builtins.str] = None,
            private_key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.PrivateKeyAttributesV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            private_key_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.PrivateKeyFlagsV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_name_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTemplatePropsMixin.SubjectNameFlagsV4Property", typing.Dict[builtins.str, typing.Any]]]] = None,
            superseded_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''v4 template schema that can use either Legacy Cryptographic Providers or Key Storage Providers.

            :param certificate_validity: Certificate validity describes the validity and renewal periods of a certificate.
            :param enrollment_flags: Enrollment flags describe the enrollment settings for certificates using the existing private key and deleting expired or revoked certificates.
            :param extensions: Extensions describe the key usage extensions and application policies for a template.
            :param general_flags: General flags describe whether the template is used for computers or users and if the template can be used with autoenrollment.
            :param hash_algorithm: Specifies the hash algorithm used to hash the private key. Hash algorithm can only be specified when using Key Storage Providers.
            :param private_key_attributes: Private key attributes allow you to specify the minimal key length, key spec, key usage, and cryptographic providers for the private key of a certificate for v4 templates. V4 templates allow you to use either Key Storage Providers or Legacy Cryptographic Service Providers. You specify the cryptography provider category in private key flags.
            :param private_key_flags: Private key flags for v4 templates specify the client compatibility, if the private key can be exported, if user input is required when using a private key, if an alternate signature algorithm should be used, and if certificates are renewed using the same private key.
            :param subject_name_flags: Subject name flags describe the subject name and subject alternate name that is included in a certificate.
            :param superseded_templates: List of templates in Active Directory that are superseded by this template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                template_v4_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.TemplateV4Property(
                    certificate_validity=pcaconnectorad_mixins.CfnTemplatePropsMixin.CertificateValidityProperty(
                        renewal_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        ),
                        validity_period=pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                            period=123,
                            period_type="periodType"
                        )
                    ),
                    enrollment_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.EnrollmentFlagsV4Property(
                        enable_key_reuse_on_nt_token_keyset_storage_full=False,
                        include_symmetric_algorithms=False,
                        no_security_extension=False,
                        remove_invalid_certificate_from_personal_store=False,
                        user_interaction_required=False
                    ),
                    extensions=pcaconnectorad_mixins.CfnTemplatePropsMixin.ExtensionsV4Property(
                        application_policies=pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPoliciesProperty(
                            critical=False,
                            policies=[pcaconnectorad_mixins.CfnTemplatePropsMixin.ApplicationPolicyProperty(
                                policy_object_identifier="policyObjectIdentifier",
                                policy_type="policyType"
                            )]
                        ),
                        key_usage=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageProperty(
                            critical=False,
                            usage_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsageFlagsProperty(
                                data_encipherment=False,
                                digital_signature=False,
                                key_agreement=False,
                                key_encipherment=False,
                                non_repudiation=False
                            )
                        )
                    ),
                    general_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.GeneralFlagsV4Property(
                        auto_enrollment=False,
                        machine_type=False
                    ),
                    hash_algorithm="hashAlgorithm",
                    private_key_attributes=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyAttributesV4Property(
                        algorithm="algorithm",
                        crypto_providers=["cryptoProviders"],
                        key_spec="keySpec",
                        key_usage_property=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyProperty(
                            property_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty(
                                decrypt=False,
                                key_agreement=False,
                                sign=False
                            ),
                            property_type="propertyType"
                        ),
                        minimal_key_length=123
                    ),
                    private_key_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.PrivateKeyFlagsV4Property(
                        client_version="clientVersion",
                        exportable_key=False,
                        require_alternate_signature_algorithm=False,
                        require_same_key_renewal=False,
                        strong_key_protection_required=False,
                        use_legacy_provider=False
                    ),
                    subject_name_flags=pcaconnectorad_mixins.CfnTemplatePropsMixin.SubjectNameFlagsV4Property(
                        require_common_name=False,
                        require_directory_path=False,
                        require_dns_as_cn=False,
                        require_email=False,
                        san_require_directory_guid=False,
                        san_require_dns=False,
                        san_require_domain_dns=False,
                        san_require_email=False,
                        san_require_spn=False,
                        san_require_upn=False
                    ),
                    superseded_templates=["supersededTemplates"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec4844f70f3ddcd3427e8bfbe6d26043947800a4d9ce085e214e761c24fed186)
                check_type(argname="argument certificate_validity", value=certificate_validity, expected_type=type_hints["certificate_validity"])
                check_type(argname="argument enrollment_flags", value=enrollment_flags, expected_type=type_hints["enrollment_flags"])
                check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
                check_type(argname="argument general_flags", value=general_flags, expected_type=type_hints["general_flags"])
                check_type(argname="argument hash_algorithm", value=hash_algorithm, expected_type=type_hints["hash_algorithm"])
                check_type(argname="argument private_key_attributes", value=private_key_attributes, expected_type=type_hints["private_key_attributes"])
                check_type(argname="argument private_key_flags", value=private_key_flags, expected_type=type_hints["private_key_flags"])
                check_type(argname="argument subject_name_flags", value=subject_name_flags, expected_type=type_hints["subject_name_flags"])
                check_type(argname="argument superseded_templates", value=superseded_templates, expected_type=type_hints["superseded_templates"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_validity is not None:
                self._values["certificate_validity"] = certificate_validity
            if enrollment_flags is not None:
                self._values["enrollment_flags"] = enrollment_flags
            if extensions is not None:
                self._values["extensions"] = extensions
            if general_flags is not None:
                self._values["general_flags"] = general_flags
            if hash_algorithm is not None:
                self._values["hash_algorithm"] = hash_algorithm
            if private_key_attributes is not None:
                self._values["private_key_attributes"] = private_key_attributes
            if private_key_flags is not None:
                self._values["private_key_flags"] = private_key_flags
            if subject_name_flags is not None:
                self._values["subject_name_flags"] = subject_name_flags
            if superseded_templates is not None:
                self._values["superseded_templates"] = superseded_templates

        @builtins.property
        def certificate_validity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.CertificateValidityProperty"]]:
            '''Certificate validity describes the validity and renewal periods of a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-certificatevalidity
            '''
            result = self._values.get("certificate_validity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.CertificateValidityProperty"]], result)

        @builtins.property
        def enrollment_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.EnrollmentFlagsV4Property"]]:
            '''Enrollment flags describe the enrollment settings for certificates using the existing private key and deleting expired or revoked certificates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-enrollmentflags
            '''
            result = self._values.get("enrollment_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.EnrollmentFlagsV4Property"]], result)

        @builtins.property
        def extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ExtensionsV4Property"]]:
            '''Extensions describe the key usage extensions and application policies for a template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-extensions
            '''
            result = self._values.get("extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.ExtensionsV4Property"]], result)

        @builtins.property
        def general_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.GeneralFlagsV4Property"]]:
            '''General flags describe whether the template is used for computers or users and if the template can be used with autoenrollment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-generalflags
            '''
            result = self._values.get("general_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.GeneralFlagsV4Property"]], result)

        @builtins.property
        def hash_algorithm(self) -> typing.Optional[builtins.str]:
            '''Specifies the hash algorithm used to hash the private key.

            Hash algorithm can only be specified when using Key Storage Providers.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-hashalgorithm
            '''
            result = self._values.get("hash_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def private_key_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyAttributesV4Property"]]:
            '''Private key attributes allow you to specify the minimal key length, key spec, key usage, and cryptographic providers for the private key of a certificate for v4 templates.

            V4 templates allow you to use either Key Storage Providers or Legacy Cryptographic Service Providers. You specify the cryptography provider category in private key flags.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-privatekeyattributes
            '''
            result = self._values.get("private_key_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyAttributesV4Property"]], result)

        @builtins.property
        def private_key_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyFlagsV4Property"]]:
            '''Private key flags for v4 templates specify the client compatibility, if the private key can be exported, if user input is required when using a private key, if an alternate signature algorithm should be used, and if certificates are renewed using the same private key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-privatekeyflags
            '''
            result = self._values.get("private_key_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.PrivateKeyFlagsV4Property"]], result)

        @builtins.property
        def subject_name_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.SubjectNameFlagsV4Property"]]:
            '''Subject name flags describe the subject name and subject alternate name that is included in a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-subjectnameflags
            '''
            result = self._values.get("subject_name_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTemplatePropsMixin.SubjectNameFlagsV4Property"]], result)

        @builtins.property
        def superseded_templates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of templates in Active Directory that are superseded by this template.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-templatev4.html#cfn-pcaconnectorad-template-templatev4-supersededtemplates
            '''
            result = self._values.get("superseded_templates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateV4Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_pcaconnectorad.mixins.CfnTemplatePropsMixin.ValidityPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"period": "period", "period_type": "periodType"},
    )
    class ValidityPeriodProperty:
        def __init__(
            self,
            *,
            period: typing.Optional[jsii.Number] = None,
            period_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information describing the end of the validity period of the certificate.

            This parameter sets the “Not After” date for the certificate. Certificate validity is the period of time during which a certificate is valid. Validity can be expressed as an explicit date and time when the certificate expires, or as a span of time after issuance, stated in hours, days, months, or years. For more information, see Validity in RFC 5280. This value is unaffected when ValidityNotBefore is also specified. For example, if Validity is set to 20 days in the future, the certificate will expire 20 days from issuance time regardless of the ValidityNotBefore value.

            :param period: The numeric value for the validity period.
            :param period_type: The unit of time. You can select hours, days, weeks, months, and years.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-validityperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_pcaconnectorad import mixins as pcaconnectorad_mixins
                
                validity_period_property = pcaconnectorad_mixins.CfnTemplatePropsMixin.ValidityPeriodProperty(
                    period=123,
                    period_type="periodType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e706810bb142d0f17db205edab7b429e46fb5a4631578c5feb63f5e27354b65a)
                check_type(argname="argument period", value=period, expected_type=type_hints["period"])
                check_type(argname="argument period_type", value=period_type, expected_type=type_hints["period_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if period is not None:
                self._values["period"] = period
            if period_type is not None:
                self._values["period_type"] = period_type

        @builtins.property
        def period(self) -> typing.Optional[jsii.Number]:
            '''The numeric value for the validity period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-validityperiod.html#cfn-pcaconnectorad-template-validityperiod-period
            '''
            result = self._values.get("period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def period_type(self) -> typing.Optional[builtins.str]:
            '''The unit of time.

            You can select hours, days, weeks, months, and years.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pcaconnectorad-template-validityperiod.html#cfn-pcaconnectorad-template-validityperiod-periodtype
            '''
            result = self._values.get("period_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnConnectorMixinProps",
    "CfnConnectorPropsMixin",
    "CfnDirectoryRegistrationMixinProps",
    "CfnDirectoryRegistrationPropsMixin",
    "CfnServicePrincipalNameMixinProps",
    "CfnServicePrincipalNamePropsMixin",
    "CfnTemplateGroupAccessControlEntryMixinProps",
    "CfnTemplateGroupAccessControlEntryPropsMixin",
    "CfnTemplateMixinProps",
    "CfnTemplatePropsMixin",
]

publication.publish()

def _typecheckingstub__a03772b5f6a0c471823b3e7c865d4af3ec9ce3714cf27c609f875f585fd67d8c(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    directory_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    vpc_information: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.VpcInformationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36fa959ddb848f03b7e2169020349fb2483ab07d9b9e65720030f0b5168fe99d(
    props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12d7cdec7d4104d3a55e226e33b4f276994c9ea0d4ecb755f9502d6bd6befa1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd95ce69fc5764a16050950406d13ea3ba6d5c602d2a771a3085184f412a353c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9010df8c182f607bf2bb7c301ba546c2d01a01e4277d8cdd7babc0f8ee936264(
    *,
    ip_address_type: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb53457a7657b9d094a099dbf5a8732235e33c6ab197e3fa6b4277737f6bd7ae(
    *,
    directory_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__022094408102afcf55c5b49df1f4d78186a7bd40804b01942ee22ce0ce14b4b6(
    props: typing.Union[CfnDirectoryRegistrationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f95bc21e4799d9562cbed48671413c771ef6556283c4ef5409e9f8a999ce18(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34866a2523e8f8c9c75b7ec8a4d6e0764e9eeebbfa6c1c79a92a8e2f1c3aea0a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f04fb46542cd265bd4ec409134f949452ed30092ee59a1aee1a089ccee0627e(
    *,
    connector_arn: typing.Optional[builtins.str] = None,
    directory_registration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f3bdb69bc52c82947e4308f5be4a7b5fce6b919b2960f1d3229f22fcdfb6b7(
    props: typing.Union[CfnServicePrincipalNameMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c160b8ec1ab84cbef79c7baab892562f707f8dc2302475405ae0b08e3f97aa7a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8d32b9fae37db4a5b392d69c6bd3dff7e122d0ef0b193334aa96c67ffccfcc7(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0a5be10a66495b6a37132fb0eec5c9caeb53d1f4610733177239afdca09e47(
    *,
    access_rights: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplateGroupAccessControlEntryPropsMixin.AccessRightsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    group_display_name: typing.Optional[builtins.str] = None,
    group_security_identifier: typing.Optional[builtins.str] = None,
    template_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d478aad196f28995118d38b56f55d6fae7335562dc1c79a5fa576d3990cd6841(
    props: typing.Union[CfnTemplateGroupAccessControlEntryMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31dc11851dc7a807bf879bc7f2e8dcd6da026b98d6ae98e87fd86925d06e1ec5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__336bb226dbb1bdfb7d4b5c1a0ddf6a1f58da4077e50f3aff91fa8fe1aa7da851(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0ed257143715f3f880e01f1917aeb24bc58d7017842e00e337da4f2e0383c9(
    *,
    auto_enroll: typing.Optional[builtins.str] = None,
    enroll: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ed2bb0c68d534f3ccc76ba96205528c4c89758a8e8d61bf380d3cb0f857440b(
    *,
    connector_arn: typing.Optional[builtins.str] = None,
    definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.TemplateDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    reenroll_all_certificate_holders: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5581ecc0fa3254b75efdbfab8ae0f1982a0ed629d4e056bde6dd13c429ef8b9(
    props: typing.Union[CfnTemplateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7629f9a526847b0e24578e5063a4532b800fdf2a5e97bca78b27a8cbf8cd3a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0be3b92e47f4a93a0a53223ef55153683ff0095e7d0e20e3e53db5c8785dc9db(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__421eedf2444494e475029c36650ce1ec8a17434b0ef692117fc5ecfcac604ca0(
    *,
    critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ApplicationPolicyProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ec73bbf7c78872678b79c3a9ed1c47d8af9b7b7d6569be75ec6cf6f9d1de0f(
    *,
    policy_object_identifier: typing.Optional[builtins.str] = None,
    policy_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6441e65cbc02035f1c2ab5c2e1d9433a1cefd3b2d6c59f6cab7c78e59884b97(
    *,
    renewal_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    validity_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ValidityPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a16acae7fc8f25e49ce81ec532403608b99e93526172df20b51cae46490953(
    *,
    enable_key_reuse_on_nt_token_keyset_storage_full: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_symmetric_algorithms: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    no_security_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_invalid_certificate_from_personal_store: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_interaction_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a05473aa4b4ad821c6a08e810f6206ee138e6418d6400c318ed78d76d6ad76(
    *,
    enable_key_reuse_on_nt_token_keyset_storage_full: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_symmetric_algorithms: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    no_security_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_invalid_certificate_from_personal_store: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_interaction_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a882390b3abf90505f807072eac64f4d440a60e84d26abfd92b85fb89e2f878c(
    *,
    enable_key_reuse_on_nt_token_keyset_storage_full: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    include_symmetric_algorithms: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    no_security_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    remove_invalid_certificate_from_personal_store: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    user_interaction_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f16c8826291cefe02834bc61491b65e66eeaba8d366751f1d2a52968eb187d5(
    *,
    application_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ApplicationPoliciesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__618276d35b1aa9ee1d946b69a649a37f1470a6e86e36fdb16e45f0f4072883e6(
    *,
    application_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ApplicationPoliciesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__168a7553510eeb9e93f4f37e6699219139a777014c1465c7e85ef836b8109a17(
    *,
    application_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ApplicationPoliciesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbf500eb5a9acf6f7f591fbb021ae9e93995350cb4131b385b564ca56f788c6(
    *,
    auto_enrollment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    machine_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f985359454d1d7cafdcb84e10b187c3f16caffd1a18b2f8f747cce6102fd716a(
    *,
    auto_enrollment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    machine_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daac8f6943ae523f3afefe014b3319e7e2c248c54f086d371313e2b61b03c86a(
    *,
    auto_enrollment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    machine_type: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5a6a2efed46832d2692314708bab7f2f9402cf3938d592ba03a4a6ba9fe69b(
    *,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8954507ea8dbfc13f11e2865fcb898693d349ddfca0c3bdc2fd547919c3161(
    *,
    critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    usage_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsageFlagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ccde75a6ff24689da8b849c1cd0eda203e64dac75c35a30f0137badb4076df(
    *,
    decrypt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ee80703166df61ed3d4e49a839f7a394aab4133474d2ef6ca8eaac875f34fa7(
    *,
    property_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsagePropertyFlagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    property_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8bd8738d00183ac8ec3b4030504415a7e1bf05f60ee45141d9020a8fd6e8309(
    *,
    crypto_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_spec: typing.Optional[builtins.str] = None,
    minimal_key_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f454b49bf57d445d91d36d92137f5e13fdf72094847f4ef5f4988d5882c0501(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    crypto_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_spec: typing.Optional[builtins.str] = None,
    key_usage_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsagePropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimal_key_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380c7979b66173afd9bf75e7b7aec1dfb63e3215a5c1ebdd4798b40654165d95(
    *,
    algorithm: typing.Optional[builtins.str] = None,
    crypto_providers: typing.Optional[typing.Sequence[builtins.str]] = None,
    key_spec: typing.Optional[builtins.str] = None,
    key_usage_property: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.KeyUsagePropertyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimal_key_length: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a35dcbd6f1ab4ecb527cece3ede1aae5bb37edc1cca3190634160d9b09390b4d(
    *,
    client_version: typing.Optional[builtins.str] = None,
    exportable_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    strong_key_protection_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ad22943c153b2434fe0109c30b2ff6157350b51efa03e41d577e8e5a3a02209(
    *,
    client_version: typing.Optional[builtins.str] = None,
    exportable_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_alternate_signature_algorithm: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    strong_key_protection_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c10735713efb0e7cb52e0d60b784864fd81df9c79647e90877f8921b5f1d38(
    *,
    client_version: typing.Optional[builtins.str] = None,
    exportable_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_alternate_signature_algorithm: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_same_key_renewal: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    strong_key_protection_required: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    use_legacy_provider: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c453755889eaa4fe7a699647915ad7751f995c1ca0a7122c6cc6e85976bc3904(
    *,
    require_common_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_directory_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_dns_as_cn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_directory_guid: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_domain_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_spn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_upn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694941c5b547122e3465e292a3f0aa46c95b68dee22258aa5b4edeb3b554e708(
    *,
    require_common_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_directory_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_dns_as_cn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_directory_guid: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_domain_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_spn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_upn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6da9e5f6eba88f30e600b17a15cdb12510ae4ba090e5f5fbbf645eb3d22b7a89(
    *,
    require_common_name: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_directory_path: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_dns_as_cn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_directory_guid: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_domain_dns: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_email: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_spn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    san_require_upn: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2688bfc145892d31555199d49aa02e203684f31a77a509b08b26c88d51131630(
    *,
    template_v2: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.TemplateV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_v3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.TemplateV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_v4: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.TemplateV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b7293a76d58fd2beb7557a6c8e2eb9633b0300e054719df51eebf91818729f0(
    *,
    certificate_validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.CertificateValidityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enrollment_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.EnrollmentFlagsV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ExtensionsV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    general_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.GeneralFlagsV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.PrivateKeyAttributesV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_key_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.PrivateKeyFlagsV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_name_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.SubjectNameFlagsV2Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    superseded_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dab39b87f80eaed839e53392bd2177d0094c3c6069202c6f150ef850242ce8d9(
    *,
    certificate_validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.CertificateValidityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enrollment_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.EnrollmentFlagsV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ExtensionsV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    general_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.GeneralFlagsV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    hash_algorithm: typing.Optional[builtins.str] = None,
    private_key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.PrivateKeyAttributesV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_key_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.PrivateKeyFlagsV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_name_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.SubjectNameFlagsV3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    superseded_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4844f70f3ddcd3427e8bfbe6d26043947800a4d9ce085e214e761c24fed186(
    *,
    certificate_validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.CertificateValidityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enrollment_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.EnrollmentFlagsV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.ExtensionsV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    general_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.GeneralFlagsV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    hash_algorithm: typing.Optional[builtins.str] = None,
    private_key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.PrivateKeyAttributesV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    private_key_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.PrivateKeyFlagsV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_name_flags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTemplatePropsMixin.SubjectNameFlagsV4Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    superseded_templates: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e706810bb142d0f17db205edab7b429e46fb5a4631578c5feb63f5e27354b65a(
    *,
    period: typing.Optional[jsii.Number] = None,
    period_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
