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
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityActivationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_chain": "certificateChain",
        "status": "status",
    },
)
class CfnCertificateAuthorityActivationMixinProps:
    def __init__(
        self,
        *,
        certificate: typing.Optional[builtins.str] = None,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCertificateAuthorityActivationPropsMixin.

        :param certificate: The Base64 PEM-encoded certificate authority certificate.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) of your private CA.
        :param certificate_chain: The Base64 PEM-encoded certificate chain that chains up to the root CA certificate that you used to sign your private CA certificate.
        :param status: Status of your private CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
            
            cfn_certificate_authority_activation_mixin_props = acmpca_mixins.CfnCertificateAuthorityActivationMixinProps(
                certificate="certificate",
                certificate_authority_arn="certificateAuthorityArn",
                certificate_chain="certificateChain",
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf9dbfa8af5910b9821e9dc872e374ebc7d7e0f92617d0b86526de83ff593c3)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The Base64 PEM-encoded certificate authority certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of your private CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The Base64 PEM-encoded certificate chain that chains up to the root CA certificate that you used to sign your private CA certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Status of your private CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html#cfn-acmpca-certificateauthorityactivation-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityActivationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCertificateAuthorityActivationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityActivationPropsMixin",
):
    '''The ``AWS::ACMPCA::CertificateAuthorityActivation`` resource creates and installs a CA certificate on a CA.

    If no status is specified, the ``AWS::ACMPCA::CertificateAuthorityActivation`` resource status defaults to ACTIVE. Once the CA has a CA certificate installed, you can use the resource to toggle the CA status field between ``ACTIVE`` and ``DISABLED`` .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthorityactivation.html
    :cloudformationResource: AWS::ACMPCA::CertificateAuthorityActivation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
        
        cfn_certificate_authority_activation_props_mixin = acmpca_mixins.CfnCertificateAuthorityActivationPropsMixin(acmpca_mixins.CfnCertificateAuthorityActivationMixinProps(
            certificate="certificate",
            certificate_authority_arn="certificateAuthorityArn",
            certificate_chain="certificateChain",
            status="status"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCertificateAuthorityActivationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ACMPCA::CertificateAuthorityActivation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4acc1e0b7336eefbc5d0133b3f5477772a2bbff37d7fd2296f1dee7533fa32d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae333ce3f4c74b66e4960302c2090c605006bdc42896bad534beaeaad864c04a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78287dd4c2e73c9adf438d23116764b167aaef5b67f0ca4e64637bc3b99d23f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCertificateAuthorityActivationMixinProps:
        return typing.cast(CfnCertificateAuthorityActivationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "csr_extensions": "csrExtensions",
        "key_algorithm": "keyAlgorithm",
        "key_storage_security_standard": "keyStorageSecurityStandard",
        "revocation_configuration": "revocationConfiguration",
        "signing_algorithm": "signingAlgorithm",
        "subject": "subject",
        "tags": "tags",
        "type": "type",
        "usage_mode": "usageMode",
    },
)
class CfnCertificateAuthorityMixinProps:
    def __init__(
        self,
        *,
        csr_extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        key_algorithm: typing.Optional[builtins.str] = None,
        key_storage_security_standard: typing.Optional[builtins.str] = None,
        revocation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        signing_algorithm: typing.Optional[builtins.str] = None,
        subject: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        usage_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCertificateAuthorityPropsMixin.

        :param csr_extensions: Specifies information to be added to the extension section of the certificate signing request (CSR).
        :param key_algorithm: Type of the public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate. When you create a subordinate CA, you must use a key algorithm supported by the parent CA.
        :param key_storage_security_standard: Specifies a cryptographic key management compliance standard for handling and protecting CA keys. Default: FIPS_140_2_LEVEL_3_OR_HIGHER .. epigraph:: Some AWS Regions don't support the default value. When you create a CA in these Regions, you must use ``CCPC_LEVEL_1_OR_HIGHER`` for the ``KeyStorageSecurityStandard`` parameter. If you don't, the operation returns an ``InvalidArgsException`` with this message: "A certificate authority cannot be created in this region with the specified security standard." For information about security standard support in different AWS Regions, see `Storage and security compliance of AWS Private CA private keys <https://docs.aws.amazon.com/privateca/latest/userguide/data-protection.html#private-keys>`_ .
        :param revocation_configuration: Information about the Online Certificate Status Protocol (OCSP) configuration or certificate revocation list (CRL) created and maintained by your private CA.
        :param signing_algorithm: Name of the algorithm your private CA uses to sign certificate requests. This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign certificates when they are issued.
        :param subject: Structure that contains X.500 distinguished name information for your private CA.
        :param tags: Key-value pairs that will be attached to the new private CA. You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see `Controlling Access Using IAM Tags <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html>`_ .
        :param type: Type of your private CA.
        :param usage_mode: Specifies whether the CA issues general-purpose certificates that typically require a revocation mechanism, or short-lived certificates that may optionally omit revocation because they expire quickly. Short-lived certificate validity is limited to seven days. The default value is GENERAL_PURPOSE.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
            
            cfn_certificate_authority_mixin_props = acmpca_mixins.CfnCertificateAuthorityMixinProps(
                csr_extensions=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty(
                    key_usage=acmpca_mixins.CfnCertificateAuthorityPropsMixin.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_information_access=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty(
                        access_location=acmpca_mixins.CfnCertificateAuthorityPropsMixin.GeneralNameProperty(
                            directory_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        ),
                        access_method=acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessMethodProperty(
                            access_method_type="accessMethodType",
                            custom_object_identifier="customObjectIdentifier"
                        )
                    )]
                ),
                key_algorithm="keyAlgorithm",
                key_storage_security_standard="keyStorageSecurityStandard",
                revocation_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty(
                    crl_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty(
                        crl_distribution_point_extension_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty(
                            omit_extension=False
                        ),
                        crl_type="crlType",
                        custom_cname="customCname",
                        custom_path="customPath",
                        enabled=False,
                        expiration_in_days=123,
                        s3_bucket_name="s3BucketName",
                        s3_object_acl="s3ObjectAcl"
                    ),
                    ocsp_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty(
                        enabled=False,
                        ocsp_custom_cname="ocspCustomCname"
                    )
                ),
                signing_algorithm="signingAlgorithm",
                subject=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type",
                usage_mode="usageMode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a77a7dfaa4b57460f4186d70378987e5878b6f8a02976ed22505743eb48390d)
            check_type(argname="argument csr_extensions", value=csr_extensions, expected_type=type_hints["csr_extensions"])
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument key_storage_security_standard", value=key_storage_security_standard, expected_type=type_hints["key_storage_security_standard"])
            check_type(argname="argument revocation_configuration", value=revocation_configuration, expected_type=type_hints["revocation_configuration"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument usage_mode", value=usage_mode, expected_type=type_hints["usage_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if csr_extensions is not None:
            self._values["csr_extensions"] = csr_extensions
        if key_algorithm is not None:
            self._values["key_algorithm"] = key_algorithm
        if key_storage_security_standard is not None:
            self._values["key_storage_security_standard"] = key_storage_security_standard
        if revocation_configuration is not None:
            self._values["revocation_configuration"] = revocation_configuration
        if signing_algorithm is not None:
            self._values["signing_algorithm"] = signing_algorithm
        if subject is not None:
            self._values["subject"] = subject
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if usage_mode is not None:
            self._values["usage_mode"] = usage_mode

    @builtins.property
    def csr_extensions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty"]]:
        '''Specifies information to be added to the extension section of the certificate signing request (CSR).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-csrextensions
        '''
        result = self._values.get("csr_extensions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty"]], result)

    @builtins.property
    def key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Type of the public key algorithm and size, in bits, of the key pair that your CA creates when it issues a certificate.

        When you create a subordinate CA, you must use a key algorithm supported by the parent CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keyalgorithm
        '''
        result = self._values.get("key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_storage_security_standard(self) -> typing.Optional[builtins.str]:
        '''Specifies a cryptographic key management compliance standard for handling and protecting CA keys.

        Default: FIPS_140_2_LEVEL_3_OR_HIGHER
        .. epigraph::

           Some AWS Regions don't support the default value. When you create a CA in these Regions, you must use ``CCPC_LEVEL_1_OR_HIGHER`` for the ``KeyStorageSecurityStandard`` parameter. If you don't, the operation returns an ``InvalidArgsException`` with this message: "A certificate authority cannot be created in this region with the specified security standard."

           For information about security standard support in different AWS Regions, see `Storage and security compliance of AWS Private CA private keys <https://docs.aws.amazon.com/privateca/latest/userguide/data-protection.html#private-keys>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-keystoragesecuritystandard
        '''
        result = self._values.get("key_storage_security_standard")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def revocation_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty"]]:
        '''Information about the Online Certificate Status Protocol (OCSP) configuration or certificate revocation list (CRL) created and maintained by your private CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-revocationconfiguration
        '''
        result = self._values.get("revocation_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty"]], result)

    @builtins.property
    def signing_algorithm(self) -> typing.Optional[builtins.str]:
        '''Name of the algorithm your private CA uses to sign certificate requests.

        This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign certificates when they are issued.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-signingalgorithm
        '''
        result = self._values.get("signing_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.SubjectProperty"]]:
        '''Structure that contains X.500 distinguished name information for your private CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-subject
        '''
        result = self._values.get("subject")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.SubjectProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that will be attached to the new private CA.

        You can associate up to 50 tags with a private CA. For information using tags with IAM to manage permissions, see `Controlling Access Using IAM Tags <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Type of your private CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def usage_mode(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the CA issues general-purpose certificates that typically require a revocation mechanism, or short-lived certificates that may optionally omit revocation because they expire quickly.

        Short-lived certificate validity is limited to seven days.

        The default value is GENERAL_PURPOSE.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html#cfn-acmpca-certificateauthority-usagemode
        '''
        result = self._values.get("usage_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateAuthorityMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCertificateAuthorityPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin",
):
    '''Use the ``AWS::ACMPCA::CertificateAuthority`` resource to create a private CA.

    Once the CA exists, you can use the ``AWS::ACMPCA::Certificate`` resource to issue a new CA certificate. Alternatively, you can issue a CA certificate using an on-premises CA, and then use the ``AWS::ACMPCA::CertificateAuthorityActivation`` resource to import the new CA certificate and activate the CA.
    .. epigraph::

       Before removing a ``AWS::ACMPCA::CertificateAuthority`` resource from the CloudFormation stack, disable the affected CA. Otherwise, the action will fail. You can disable the CA by removing its associated ``AWS::ACMPCA::CertificateAuthorityActivation`` resource from CloudFormation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificateauthority.html
    :cloudformationResource: AWS::ACMPCA::CertificateAuthority
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
        
        cfn_certificate_authority_props_mixin = acmpca_mixins.CfnCertificateAuthorityPropsMixin(acmpca_mixins.CfnCertificateAuthorityMixinProps(
            csr_extensions=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty(
                key_usage=acmpca_mixins.CfnCertificateAuthorityPropsMixin.KeyUsageProperty(
                    crl_sign=False,
                    data_encipherment=False,
                    decipher_only=False,
                    digital_signature=False,
                    encipher_only=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    key_encipherment=False,
                    non_repudiation=False
                ),
                subject_information_access=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty(
                    access_location=acmpca_mixins.CfnCertificateAuthorityPropsMixin.GeneralNameProperty(
                        directory_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    ),
                    access_method=acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessMethodProperty(
                        access_method_type="accessMethodType",
                        custom_object_identifier="customObjectIdentifier"
                    )
                )]
            ),
            key_algorithm="keyAlgorithm",
            key_storage_security_standard="keyStorageSecurityStandard",
            revocation_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty(
                crl_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty(
                    crl_distribution_point_extension_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty(
                        omit_extension=False
                    ),
                    crl_type="crlType",
                    custom_cname="customCname",
                    custom_path="customPath",
                    enabled=False,
                    expiration_in_days=123,
                    s3_bucket_name="s3BucketName",
                    s3_object_acl="s3ObjectAcl"
                ),
                ocsp_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty(
                    enabled=False,
                    ocsp_custom_cname="ocspCustomCname"
                )
            ),
            signing_algorithm="signingAlgorithm",
            subject=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                common_name="commonName",
                country="country",
                custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                    object_identifier="objectIdentifier",
                    value="value"
                )],
                distinguished_name_qualifier="distinguishedNameQualifier",
                generation_qualifier="generationQualifier",
                given_name="givenName",
                initials="initials",
                locality="locality",
                organization="organization",
                organizational_unit="organizationalUnit",
                pseudonym="pseudonym",
                serial_number="serialNumber",
                state="state",
                surname="surname",
                title="title"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type",
            usage_mode="usageMode"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCertificateAuthorityMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ACMPCA::CertificateAuthority``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b409b4e92d242217582e134a83287e6e2393d92e8fe1bff0ac717568710a5381)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ef9833d9d84b12e48eea999e394bc89efe7998b2beecf2dd2a4712a73d8d1df)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fed528f8137b7fe1b044d37929e52755769a342efd52c24a6a78a5c359fdb398)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCertificateAuthorityMixinProps:
        return typing.cast(CfnCertificateAuthorityMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_location": "accessLocation",
            "access_method": "accessMethod",
        },
    )
    class AccessDescriptionProperty:
        def __init__(
            self,
            *,
            access_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.GeneralNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            access_method: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.AccessMethodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides access information used by the ``authorityInfoAccess`` and ``subjectInfoAccess`` extensions described in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ .

            :param access_location: The location of ``AccessDescription`` information.
            :param access_method: The type and format of ``AccessDescription`` information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                access_description_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty(
                    access_location=acmpca_mixins.CfnCertificateAuthorityPropsMixin.GeneralNameProperty(
                        directory_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    ),
                    access_method=acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessMethodProperty(
                        access_method_type="accessMethodType",
                        custom_object_identifier="customObjectIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7992c9e6f1198106308b4e4c67cc64ad122a4c11245fae91c83342fdc0b4309)
                check_type(argname="argument access_location", value=access_location, expected_type=type_hints["access_location"])
                check_type(argname="argument access_method", value=access_method, expected_type=type_hints["access_method"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_location is not None:
                self._values["access_location"] = access_location
            if access_method is not None:
                self._values["access_method"] = access_method

        @builtins.property
        def access_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.GeneralNameProperty"]]:
            '''The location of ``AccessDescription`` information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html#cfn-acmpca-certificateauthority-accessdescription-accesslocation
            '''
            result = self._values.get("access_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.GeneralNameProperty"]], result)

        @builtins.property
        def access_method(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.AccessMethodProperty"]]:
            '''The type and format of ``AccessDescription`` information.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessdescription.html#cfn-acmpca-certificateauthority-accessdescription-accessmethod
            '''
            result = self._values.get("access_method")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.AccessMethodProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessDescriptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.AccessMethodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "access_method_type": "accessMethodType",
            "custom_object_identifier": "customObjectIdentifier",
        },
    )
    class AccessMethodProperty:
        def __init__(
            self,
            *,
            access_method_type: typing.Optional[builtins.str] = None,
            custom_object_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the type and format of extension access.

            Only one of ``CustomObjectIdentifier`` or ``AccessMethodType`` may be provided. Providing both results in ``InvalidArgsException`` .

            :param access_method_type: Specifies the ``AccessMethod`` .
            :param custom_object_identifier: An object identifier (OID) specifying the ``AccessMethod`` . The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                access_method_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessMethodProperty(
                    access_method_type="accessMethodType",
                    custom_object_identifier="customObjectIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__782ee5f838c15a764ed3396c9e761126b184826c05c19f5119f12acd10b4f435)
                check_type(argname="argument access_method_type", value=access_method_type, expected_type=type_hints["access_method_type"])
                check_type(argname="argument custom_object_identifier", value=custom_object_identifier, expected_type=type_hints["custom_object_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_method_type is not None:
                self._values["access_method_type"] = access_method_type
            if custom_object_identifier is not None:
                self._values["custom_object_identifier"] = custom_object_identifier

        @builtins.property
        def access_method_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the ``AccessMethod`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html#cfn-acmpca-certificateauthority-accessmethod-accessmethodtype
            '''
            result = self._values.get("access_method_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_object_identifier(self) -> typing.Optional[builtins.str]:
            '''An object identifier (OID) specifying the ``AccessMethod`` .

            The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-accessmethod.html#cfn-acmpca-certificateauthority-accessmethod-customobjectidentifier
            '''
            result = self._values.get("custom_object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AccessMethodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_distribution_point_extension_configuration": "crlDistributionPointExtensionConfiguration",
            "crl_type": "crlType",
            "custom_cname": "customCname",
            "custom_path": "customPath",
            "enabled": "enabled",
            "expiration_in_days": "expirationInDays",
            "s3_bucket_name": "s3BucketName",
            "s3_object_acl": "s3ObjectAcl",
        },
    )
    class CrlConfigurationProperty:
        def __init__(
            self,
            *,
            crl_distribution_point_extension_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            crl_type: typing.Optional[builtins.str] = None,
            custom_cname: typing.Optional[builtins.str] = None,
            custom_path: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            expiration_in_days: typing.Optional[jsii.Number] = None,
            s3_bucket_name: typing.Optional[builtins.str] = None,
            s3_object_acl: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains configuration information for a certificate revocation list (CRL).

            Your private certificate authority (CA) creates base CRLs. Delta CRLs are not supported. You can enable CRLs for your new or an existing private CA by setting the *Enabled* parameter to ``true`` . Your private CA writes CRLs to an S3 bucket that you specify in the *S3BucketName* parameter. You can hide the name of your bucket by specifying a value for the *CustomCname* parameter. Your private CA by default copies the CNAME or the S3 bucket name to the *CRL Distribution Points* extension of each certificate it issues. If you want to configure this default behavior to be something different, you can set the *CrlDistributionPointExtensionConfiguration* parameter. Your S3 bucket policy must give write permission to AWS Private CA.

            AWS Private CA assets that are stored in Amazon S3 can be protected with encryption. For more information, see `Encrypting Your CRLs <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#crl-encryption>`_ .

            Your private CA uses the value in the *ExpirationInDays* parameter to calculate the *nextUpdate* field in the CRL. The CRL is refreshed prior to a certificate's expiration date or when a certificate is revoked. When a certificate is revoked, it appears in the CRL until the certificate expires, and then in one additional CRL after expiration, and it always appears in the audit report.

            A CRL is typically updated approximately 30 minutes after a certificate is revoked. If for any reason a CRL update fails, AWS Private CA makes further attempts every 15 minutes.

            CRLs contain the following fields:

            - *Version* : The current version number defined in RFC 5280 is V2. The integer value is 0x1.
            - *Signature Algorithm* : The name of the algorithm used to sign the CRL.
            - *Issuer* : The X.500 distinguished name of your private CA that issued the CRL.
            - *Last Update* : The issue date and time of this CRL.
            - *Next Update* : The day and time by which the next CRL will be issued.
            - *Revoked Certificates* : List of revoked certificates. Each list item contains the following information.
            - *Serial Number* : The serial number, in hexadecimal format, of the revoked certificate.
            - *Revocation Date* : Date and time the certificate was revoked.
            - *CRL Entry Extensions* : Optional extensions for the CRL entry.
            - *X509v3 CRL Reason Code* : Reason the certificate was revoked.
            - *CRL Extensions* : Optional extensions for the CRL.
            - *X509v3 Authority Key Identifier* : Identifies the public key associated with the private key used to sign the certificate.
            - *X509v3 CRL Number:* : Decimal sequence number for the CRL.
            - *Signature Algorithm* : Algorithm used by your private CA to sign the CRL.
            - *Signature Value* : Signature computed over the CRL.

            Certificate revocation lists created by AWS Private CA are DER-encoded. You can use the following OpenSSL command to list a CRL.

            ``openssl crl -inform DER -text -in *crl_path* -noout``

            For more information, see `Planning a certificate revocation list (CRL) <https://docs.aws.amazon.com/privateca/latest/userguide/crl-planning.html>`_ in the *AWS Private Certificate Authority User Guide*

            :param crl_distribution_point_extension_configuration: Configures the default behavior of the CRL Distribution Point extension for certificates issued by your CA. If this field is not provided, then the CRL Distribution Point extension will be present and contain the default CRL URL.
            :param crl_type: Specifies the type of CRL. This setting determines the maximum number of certificates that the certificate authority can issue and revoke. For more information, see `AWS Private CA quotas <https://docs.aws.amazon.com/general/latest/gr/pca.html#limits_pca>`_ . - ``COMPLETE`` - The default setting. AWS Private CA maintains a single CRL file for all unexpired certificates issued by a CA that have been revoked for any reason. Each certificate that AWS Private CA issues is bound to a specific CRL through the CRL distribution point (CDP) defined in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ . - ``PARTITIONED`` - Compared to complete CRLs, partitioned CRLs dramatically increase the number of certificates your private CA can issue. .. epigraph:: When using partitioned CRLs, you must validate that the CRL's associated issuing distribution point (IDP) URI matches the certiﬁcate's CDP URI to ensure the right CRL has been fetched. AWS Private CA marks the IDP extension as critical, which your client must be able to process.
            :param custom_cname: Name inserted into the certificate *CRL Distribution Points* extension that enables the use of an alias for the CRL distribution point. Use this value if you don't want the name of your S3 bucket to be public. .. epigraph:: The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".
            :param custom_path: Designates a custom file path in S3 for CRL(s). For example, ``http://<CustomName>/<CustomPath>/<CrlPartition_GUID>.crl`` .
            :param enabled: Boolean value that specifies whether certificate revocation lists (CRLs) are enabled. You can use this value to enable certificate revocation for a new CA when you call the ``CreateCertificateAuthority`` operation or for an existing CA when you call the ``UpdateCertificateAuthority`` operation.
            :param expiration_in_days: Validity period of the CRL in days.
            :param s3_bucket_name: Name of the S3 bucket that contains the CRL. If you do not provide a value for the *CustomCname* argument, the name of your S3 bucket is placed into the *CRL Distribution Points* extension of the issued certificate. You can change the name of your bucket by calling the `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ operation. You must specify a `bucket policy <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-policies>`_ that allows AWS Private CA to write the CRL to your bucket. .. epigraph:: The ``S3BucketName`` parameter must conform to the `S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
            :param s3_object_acl: Determines whether the CRL will be publicly readable or privately held in the CRL Amazon S3 bucket. If you choose PUBLIC_READ, the CRL will be accessible over the public internet. If you choose BUCKET_OWNER_FULL_CONTROL, only the owner of the CRL S3 bucket can access the CRL, and your PKI clients may need an alternative method of access. If no value is specified, the default is PUBLIC_READ. *Note:* This default can cause CA creation to fail in some circumstances. If you have have enabled the Block Public Access (BPA) feature in your S3 account, then you must specify the value of this parameter as ``BUCKET_OWNER_FULL_CONTROL`` , and not doing so results in an error. If you have disabled BPA in S3, then you can specify either ``BUCKET_OWNER_FULL_CONTROL`` or ``PUBLIC_READ`` as the value. For more information, see `Blocking public access to the S3 bucket <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-bpa>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                crl_configuration_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty(
                    crl_distribution_point_extension_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty(
                        omit_extension=False
                    ),
                    crl_type="crlType",
                    custom_cname="customCname",
                    custom_path="customPath",
                    enabled=False,
                    expiration_in_days=123,
                    s3_bucket_name="s3BucketName",
                    s3_object_acl="s3ObjectAcl"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__967dfb0f153d649ebd2b778f2341d704c360fd34087f8ba08e7b4dff6adf1aea)
                check_type(argname="argument crl_distribution_point_extension_configuration", value=crl_distribution_point_extension_configuration, expected_type=type_hints["crl_distribution_point_extension_configuration"])
                check_type(argname="argument crl_type", value=crl_type, expected_type=type_hints["crl_type"])
                check_type(argname="argument custom_cname", value=custom_cname, expected_type=type_hints["custom_cname"])
                check_type(argname="argument custom_path", value=custom_path, expected_type=type_hints["custom_path"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument expiration_in_days", value=expiration_in_days, expected_type=type_hints["expiration_in_days"])
                check_type(argname="argument s3_bucket_name", value=s3_bucket_name, expected_type=type_hints["s3_bucket_name"])
                check_type(argname="argument s3_object_acl", value=s3_object_acl, expected_type=type_hints["s3_object_acl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_distribution_point_extension_configuration is not None:
                self._values["crl_distribution_point_extension_configuration"] = crl_distribution_point_extension_configuration
            if crl_type is not None:
                self._values["crl_type"] = crl_type
            if custom_cname is not None:
                self._values["custom_cname"] = custom_cname
            if custom_path is not None:
                self._values["custom_path"] = custom_path
            if enabled is not None:
                self._values["enabled"] = enabled
            if expiration_in_days is not None:
                self._values["expiration_in_days"] = expiration_in_days
            if s3_bucket_name is not None:
                self._values["s3_bucket_name"] = s3_bucket_name
            if s3_object_acl is not None:
                self._values["s3_object_acl"] = s3_object_acl

        @builtins.property
        def crl_distribution_point_extension_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty"]]:
            '''Configures the default behavior of the CRL Distribution Point extension for certificates issued by your CA.

            If this field is not provided, then the CRL Distribution Point extension will be present and contain the default CRL URL.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-crldistributionpointextensionconfiguration
            '''
            result = self._values.get("crl_distribution_point_extension_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty"]], result)

        @builtins.property
        def crl_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of CRL.

            This setting determines the maximum number of certificates that the certificate authority can issue and revoke. For more information, see `AWS Private CA quotas <https://docs.aws.amazon.com/general/latest/gr/pca.html#limits_pca>`_ .

            - ``COMPLETE`` - The default setting. AWS Private CA maintains a single CRL file for all unexpired certificates issued by a CA that have been revoked for any reason. Each certificate that AWS Private CA issues is bound to a specific CRL through the CRL distribution point (CDP) defined in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ .
            - ``PARTITIONED`` - Compared to complete CRLs, partitioned CRLs dramatically increase the number of certificates your private CA can issue.

            .. epigraph::

               When using partitioned CRLs, you must validate that the CRL's associated issuing distribution point (IDP) URI matches the certiﬁcate's CDP URI to ensure the right CRL has been fetched. AWS Private CA marks the IDP extension as critical, which your client must be able to process.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-crltype
            '''
            result = self._values.get("crl_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_cname(self) -> typing.Optional[builtins.str]:
            '''Name inserted into the certificate *CRL Distribution Points* extension that enables the use of an alias for the CRL distribution point.

            Use this value if you don't want the name of your S3 bucket to be public.
            .. epigraph::

               The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-customcname
            '''
            result = self._values.get("custom_cname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_path(self) -> typing.Optional[builtins.str]:
            '''Designates a custom file path in S3 for CRL(s).

            For example, ``http://<CustomName>/<CustomPath>/<CrlPartition_GUID>.crl`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-custompath
            '''
            result = self._values.get("custom_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Boolean value that specifies whether certificate revocation lists (CRLs) are enabled.

            You can use this value to enable certificate revocation for a new CA when you call the ``CreateCertificateAuthority`` operation or for an existing CA when you call the ``UpdateCertificateAuthority`` operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def expiration_in_days(self) -> typing.Optional[jsii.Number]:
            '''Validity period of the CRL in days.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-expirationindays
            '''
            result = self._values.get("expiration_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def s3_bucket_name(self) -> typing.Optional[builtins.str]:
            '''Name of the S3 bucket that contains the CRL.

            If you do not provide a value for the *CustomCname* argument, the name of your S3 bucket is placed into the *CRL Distribution Points* extension of the issued certificate. You can change the name of your bucket by calling the `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ operation. You must specify a `bucket policy <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-policies>`_ that allows AWS Private CA to write the CRL to your bucket.
            .. epigraph::

               The ``S3BucketName`` parameter must conform to the `S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3bucketname
            '''
            result = self._values.get("s3_bucket_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_object_acl(self) -> typing.Optional[builtins.str]:
            '''Determines whether the CRL will be publicly readable or privately held in the CRL Amazon S3 bucket.

            If you choose PUBLIC_READ, the CRL will be accessible over the public internet. If you choose BUCKET_OWNER_FULL_CONTROL, only the owner of the CRL S3 bucket can access the CRL, and your PKI clients may need an alternative method of access.

            If no value is specified, the default is PUBLIC_READ.

            *Note:* This default can cause CA creation to fail in some circumstances. If you have have enabled the Block Public Access (BPA) feature in your S3 account, then you must specify the value of this parameter as ``BUCKET_OWNER_FULL_CONTROL`` , and not doing so results in an error. If you have disabled BPA in S3, then you can specify either ``BUCKET_OWNER_FULL_CONTROL`` or ``PUBLIC_READ`` as the value.

            For more information, see `Blocking public access to the S3 bucket <https://docs.aws.amazon.com/privateca/latest/userguide/PcaCreateCa.html#s3-bpa>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crlconfiguration.html#cfn-acmpca-certificateauthority-crlconfiguration-s3objectacl
            '''
            result = self._values.get("s3_object_acl")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrlConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"omit_extension": "omitExtension"},
    )
    class CrlDistributionPointExtensionConfigurationProperty:
        def __init__(
            self,
            *,
            omit_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Contains configuration information for the default behavior of the CRL Distribution Point (CDP) extension in certificates issued by your CA.

            This extension contains a link to download the CRL, so you can check whether a certificate has been revoked. To choose whether you want this extension omitted or not in certificates issued by your CA, you can set the *OmitExtension* parameter.

            :param omit_extension: Configures whether the CRL Distribution Point extension should be populated with the default URL to the CRL. If set to ``true`` , then the CDP extension will not be present in any certificates issued by that CA unless otherwise specified through CSR or API passthrough. .. epigraph:: Only set this if you have another way to distribute the CRL Distribution Points for certificates issued by your CA, such as the Matter Distributed Compliance Ledger. This configuration cannot be enabled with a custom CNAME set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crldistributionpointextensionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                crl_distribution_point_extension_configuration_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty(
                    omit_extension=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5607361104159196c91cb191e7e28592c0ae4a0e23fe166b4cca7296fa38d45)
                check_type(argname="argument omit_extension", value=omit_extension, expected_type=type_hints["omit_extension"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if omit_extension is not None:
                self._values["omit_extension"] = omit_extension

        @builtins.property
        def omit_extension(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Configures whether the CRL Distribution Point extension should be populated with the default URL to the CRL.

            If set to ``true`` , then the CDP extension will not be present in any certificates issued by that CA unless otherwise specified through CSR or API passthrough.
            .. epigraph::

               Only set this if you have another way to distribute the CRL Distribution Points for certificates issued by your CA, such as the Matter Distributed Compliance Ledger.

               This configuration cannot be enabled with a custom CNAME set.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-crldistributionpointextensionconfiguration.html#cfn-acmpca-certificateauthority-crldistributionpointextensionconfiguration-omitextension
            '''
            result = self._values.get("omit_extension")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CrlDistributionPointExtensionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key_usage": "keyUsage",
            "subject_information_access": "subjectInformationAccess",
        },
    )
    class CsrExtensionsProperty:
        def __init__(
            self,
            *,
            key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_information_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Describes the certificate extensions to be added to the certificate signing request (CSR).

            :param key_usage: Indicates the purpose of the certificate and of the key contained in the certificate.
            :param subject_information_access: For CA certificates, provides a path to additional information pertaining to the CA, such as revocation and policy. For more information, see `Subject Information Access <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.2.2>`_ in RFC 5280.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                csr_extensions_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty(
                    key_usage=acmpca_mixins.CfnCertificateAuthorityPropsMixin.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_information_access=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty(
                        access_location=acmpca_mixins.CfnCertificateAuthorityPropsMixin.GeneralNameProperty(
                            directory_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        ),
                        access_method=acmpca_mixins.CfnCertificateAuthorityPropsMixin.AccessMethodProperty(
                            access_method_type="accessMethodType",
                            custom_object_identifier="customObjectIdentifier"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7541f697f70cd36aa3de411eef934fc157dc15545a65d7ccdf4e24abc559eb52)
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
                check_type(argname="argument subject_information_access", value=subject_information_access, expected_type=type_hints["subject_information_access"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_usage is not None:
                self._values["key_usage"] = key_usage
            if subject_information_access is not None:
                self._values["subject_information_access"] = subject_information_access

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.KeyUsageProperty"]]:
            '''Indicates the purpose of the certificate and of the key contained in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html#cfn-acmpca-certificateauthority-csrextensions-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.KeyUsageProperty"]], result)

        @builtins.property
        def subject_information_access(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty"]]]]:
            '''For CA certificates, provides a path to additional information pertaining to the CA, such as revocation and policy.

            For more information, see `Subject Information Access <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.2.2>`_ in RFC 5280.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-csrextensions.html#cfn-acmpca-certificateauthority-csrextensions-subjectinformationaccess
            '''
            result = self._values.get("subject_information_access")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsrExtensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"object_identifier": "objectIdentifier", "value": "value"},
    )
    class CustomAttributeProperty:
        def __init__(
            self,
            *,
            object_identifier: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the X.500 relative distinguished name (RDN).

            :param object_identifier: Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).
            :param value: Specifies the attribute value of relative distinguished name (RDN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-customattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                custom_attribute_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                    object_identifier="objectIdentifier",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b90f6eee84dc75e8a2ba80cd3ff4791447912a759e6d3258ff2773716d69e2ef)
                check_type(argname="argument object_identifier", value=object_identifier, expected_type=type_hints["object_identifier"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_identifier is not None:
                self._values["object_identifier"] = object_identifier
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def object_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-customattribute.html#cfn-acmpca-certificateauthority-customattribute-objectidentifier
            '''
            result = self._values.get("object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specifies the attribute value of relative distinguished name (RDN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-customattribute.html#cfn-acmpca-certificateauthority-customattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty",
        jsii_struct_bases=[],
        name_mapping={"name_assigner": "nameAssigner", "party_name": "partyName"},
    )
    class EdiPartyNameProperty:
        def __init__(
            self,
            *,
            name_assigner: typing.Optional[builtins.str] = None,
            party_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an Electronic Data Interchange (EDI) entity as described in as defined in `Subject Alternative Name <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ in RFC 5280.

            :param name_assigner: Specifies the name assigner.
            :param party_name: Specifies the party name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                edi_party_name_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty(
                    name_assigner="nameAssigner",
                    party_name="partyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f79a0fbafc36191cfda515db5e6c05321c3016e8e103cc74610150052db35b81)
                check_type(argname="argument name_assigner", value=name_assigner, expected_type=type_hints["name_assigner"])
                check_type(argname="argument party_name", value=party_name, expected_type=type_hints["party_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name_assigner is not None:
                self._values["name_assigner"] = name_assigner
            if party_name is not None:
                self._values["party_name"] = party_name

        @builtins.property
        def name_assigner(self) -> typing.Optional[builtins.str]:
            '''Specifies the name assigner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html#cfn-acmpca-certificateauthority-edipartyname-nameassigner
            '''
            result = self._values.get("name_assigner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def party_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the party name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-edipartyname.html#cfn-acmpca-certificateauthority-edipartyname-partyname
            '''
            result = self._values.get("party_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiPartyNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.GeneralNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "dns_name": "dnsName",
            "edi_party_name": "ediPartyName",
            "ip_address": "ipAddress",
            "other_name": "otherName",
            "registered_id": "registeredId",
            "rfc822_name": "rfc822Name",
            "uniform_resource_identifier": "uniformResourceIdentifier",
        },
    )
    class GeneralNameProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dns_name: typing.Optional[builtins.str] = None,
            edi_party_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            other_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.OtherNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            registered_id: typing.Optional[builtins.str] = None,
            rfc822_name: typing.Optional[builtins.str] = None,
            uniform_resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an ASN.1 X.400 ``GeneralName`` as defined in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ . Only one of the following naming options should be provided. Providing more than one option results in an ``InvalidArgsException`` error.

            :param directory_name: Contains information about the certificate subject. The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.
            :param dns_name: Represents ``GeneralName`` as a DNS name.
            :param edi_party_name: Represents ``GeneralName`` as an ``EdiPartyName`` object.
            :param ip_address: Represents ``GeneralName`` as an IPv4 or IPv6 address.
            :param other_name: Represents ``GeneralName`` using an ``OtherName`` object.
            :param registered_id: Represents ``GeneralName`` as an object identifier (OID).
            :param rfc822_name: Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.
            :param uniform_resource_identifier: Represents ``GeneralName`` as a URI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                general_name_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.GeneralNameProperty(
                    directory_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    ),
                    dns_name="dnsName",
                    edi_party_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty(
                        name_assigner="nameAssigner",
                        party_name="partyName"
                    ),
                    ip_address="ipAddress",
                    other_name=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty(
                        type_id="typeId",
                        value="value"
                    ),
                    registered_id="registeredId",
                    rfc822_name="rfc822Name",
                    uniform_resource_identifier="uniformResourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe2299b488a143d9fe92d473443cb79f8ecb1cf679258faf7003343cccc08975)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
                check_type(argname="argument edi_party_name", value=edi_party_name, expected_type=type_hints["edi_party_name"])
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument other_name", value=other_name, expected_type=type_hints["other_name"])
                check_type(argname="argument registered_id", value=registered_id, expected_type=type_hints["registered_id"])
                check_type(argname="argument rfc822_name", value=rfc822_name, expected_type=type_hints["rfc822_name"])
                check_type(argname="argument uniform_resource_identifier", value=uniform_resource_identifier, expected_type=type_hints["uniform_resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if edi_party_name is not None:
                self._values["edi_party_name"] = edi_party_name
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if other_name is not None:
                self._values["other_name"] = other_name
            if registered_id is not None:
                self._values["registered_id"] = registered_id
            if rfc822_name is not None:
                self._values["rfc822_name"] = rfc822_name
            if uniform_resource_identifier is not None:
                self._values["uniform_resource_identifier"] = uniform_resource_identifier

        @builtins.property
        def directory_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.SubjectProperty"]]:
            '''Contains information about the certificate subject.

            The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.SubjectProperty"]], result)

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a DNS name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-dnsname
            '''
            result = self._values.get("dns_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def edi_party_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty"]]:
            '''Represents ``GeneralName`` as an ``EdiPartyName`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-edipartyname
            '''
            result = self._values.get("edi_party_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty"]], result)

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an IPv4 or IPv6 address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def other_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.OtherNameProperty"]]:
            '''Represents ``GeneralName`` using an ``OtherName`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-othername
            '''
            result = self._values.get("other_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.OtherNameProperty"]], result)

        @builtins.property
        def registered_id(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an object identifier (OID).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-registeredid
            '''
            result = self._values.get("registered_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rfc822_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-rfc822name
            '''
            result = self._values.get("rfc822_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a URI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-generalname.html#cfn-acmpca-certificateauthority-generalname-uniformresourceidentifier
            '''
            result = self._values.get("uniform_resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_sign": "crlSign",
            "data_encipherment": "dataEncipherment",
            "decipher_only": "decipherOnly",
            "digital_signature": "digitalSignature",
            "encipher_only": "encipherOnly",
            "key_agreement": "keyAgreement",
            "key_cert_sign": "keyCertSign",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Defines one or more purposes for which the key contained in the certificate can be used.

            Default value for each option is false.

            :param crl_sign: Key can be used to sign CRLs. Default: - false
            :param data_encipherment: Key can be used to decipher data. Default: - false
            :param decipher_only: Key can be used only to decipher data. Default: - false
            :param digital_signature: Key can be used for digital signing. Default: - false
            :param encipher_only: Key can be used only to encipher data. Default: - false
            :param key_agreement: Key can be used in a key-agreement protocol. Default: - false
            :param key_cert_sign: Key can be used to sign certificates. Default: - false
            :param key_encipherment: Key can be used to encipher data. Default: - false
            :param non_repudiation: Key can be used for non-repudiation. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                key_usage_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.KeyUsageProperty(
                    crl_sign=False,
                    data_encipherment=False,
                    decipher_only=False,
                    digital_signature=False,
                    encipher_only=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    key_encipherment=False,
                    non_repudiation=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6f2b6b4a4d1b3d7eba5010cc5f45b4e010daabe3f82704339fe206a969ac7312)
                check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
                check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
                check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
                check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
                check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
                check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
                check_type(argname="argument key_cert_sign", value=key_cert_sign, expected_type=type_hints["key_cert_sign"])
                check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
                check_type(argname="argument non_repudiation", value=non_repudiation, expected_type=type_hints["non_repudiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_sign is not None:
                self._values["crl_sign"] = crl_sign
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if decipher_only is not None:
                self._values["decipher_only"] = decipher_only
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if encipher_only is not None:
                self._values["encipher_only"] = encipher_only
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_cert_sign is not None:
                self._values["key_cert_sign"] = key_cert_sign
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def crl_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to sign CRLs.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-crlsign
            '''
            result = self._values.get("crl_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to decipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-dataencipherment
            '''
            result = self._values.get("data_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def decipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used only to decipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-decipheronly
            '''
            result = self._values.get("decipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used for digital signing.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-digitalsignature
            '''
            result = self._values.get("digital_signature")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used only to encipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-encipheronly
            '''
            result = self._values.get("encipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used in a key-agreement protocol.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keyagreement
            '''
            result = self._values.get("key_agreement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_cert_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to sign certificates.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keycertsign
            '''
            result = self._values.get("key_cert_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to encipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-keyencipherment
            '''
            result = self._values.get("key_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used for non-repudiation.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-keyusage.html#cfn-acmpca-certificateauthority-keyusage-nonrepudiation
            '''
            result = self._values.get("non_repudiation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled", "ocsp_custom_cname": "ocspCustomCname"},
    )
    class OcspConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            ocsp_custom_cname: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information to enable and configure Online Certificate Status Protocol (OCSP) for validating certificate revocation status.

            :param enabled: Flag enabling use of the Online Certificate Status Protocol (OCSP) for validating certificate revocation status.
            :param ocsp_custom_cname: By default, AWS Private CA injects an Amazon domain into certificates being validated by the Online Certificate Status Protocol (OCSP). A customer can alternatively use this object to define a CNAME specifying a customized OCSP domain. .. epigraph:: The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-ocspconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                ocsp_configuration_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty(
                    enabled=False,
                    ocsp_custom_cname="ocspCustomCname"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a679d493bc7bb1fefbc08f2cb7790180a8977ad8d789359801e0c8247c3c537)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument ocsp_custom_cname", value=ocsp_custom_cname, expected_type=type_hints["ocsp_custom_cname"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if ocsp_custom_cname is not None:
                self._values["ocsp_custom_cname"] = ocsp_custom_cname

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Flag enabling use of the Online Certificate Status Protocol (OCSP) for validating certificate revocation status.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-ocspconfiguration.html#cfn-acmpca-certificateauthority-ocspconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def ocsp_custom_cname(self) -> typing.Optional[builtins.str]:
            '''By default, AWS Private CA injects an Amazon domain into certificates being validated by the Online Certificate Status Protocol (OCSP).

            A customer can alternatively use this object to define a CNAME specifying a customized OCSP domain.
            .. epigraph::

               The content of a Canonical Name (CNAME) record must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in URIs. Additionally, the value of the CNAME must not include a protocol prefix such as "http://" or "https://".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-ocspconfiguration.html#cfn-acmpca-certificateauthority-ocspconfiguration-ocspcustomcname
            '''
            result = self._values.get("ocsp_custom_cname")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OcspConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty",
        jsii_struct_bases=[],
        name_mapping={"type_id": "typeId", "value": "value"},
    )
    class OtherNameProperty:
        def __init__(
            self,
            *,
            type_id: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a custom ASN.1 X.400 ``GeneralName`` using an object identifier (OID) and value. The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :param type_id: Specifies an OID.
            :param value: Specifies an OID value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                other_name_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.OtherNameProperty(
                    type_id="typeId",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bdec9bc050eb1acd991c5c5a06553a5cee257ab6e7ba59ef19e7e09b8ff6b668)
                check_type(argname="argument type_id", value=type_id, expected_type=type_hints["type_id"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type_id is not None:
                self._values["type_id"] = type_id
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type_id(self) -> typing.Optional[builtins.str]:
            '''Specifies an OID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html#cfn-acmpca-certificateauthority-othername-typeid
            '''
            result = self._values.get("type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specifies an OID value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-othername.html#cfn-acmpca-certificateauthority-othername-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtherNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_configuration": "crlConfiguration",
            "ocsp_configuration": "ocspConfiguration",
        },
    )
    class RevocationConfigurationProperty:
        def __init__(
            self,
            *,
            crl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ocsp_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Certificate revocation information used by the `CreateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_CreateCertificateAuthority.html>`_ and `UpdateCertificateAuthority <https://docs.aws.amazon.com/privateca/latest/APIReference/API_UpdateCertificateAuthority.html>`_ actions. Your private certificate authority (CA) can configure Online Certificate Status Protocol (OCSP) support and/or maintain a certificate revocation list (CRL). OCSP returns validation information about certificates as requested by clients, and a CRL contains an updated list of certificates revoked by your CA. For more information, see `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ in the *AWS Private CA API Reference* and `Setting up a certificate revocation method <https://docs.aws.amazon.com/privateca/latest/userguide/revocation-setup.html>`_ in the *AWS Private CA User Guide* .

            The following requirements and constraints apply to revocation configurations.

            - A configuration disabling CRLs or OCSP must contain only the ``Enabled=False`` parameter, and will fail if other parameters such as ``CustomCname`` or ``ExpirationInDays`` are included.
            - In a CRL configuration, the ``S3BucketName`` parameter must conform to the `Amazon S3 bucket naming rules <https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html>`_ .
            - A configuration containing a custom Canonical Name (CNAME) parameter for CRLs or OCSP must conform to `RFC2396 <https://docs.aws.amazon.com/https://www.ietf.org/rfc/rfc2396.txt>`_ restrictions on the use of special characters in a CNAME.
            - In a CRL or OCSP configuration, the value of a CNAME parameter must not include a protocol prefix such as "http://" or "https://".
            - To revoke a certificate, delete the resource from your template, and call the AWS Private CA `RevokeCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_RevokeCertificate.html>`_ API and specify the resource's certificate authority ARN.

            :param crl_configuration: Configuration of the certificate revocation list (CRL), if any, maintained by your private CA.
            :param ocsp_configuration: Configuration of Online Certificate Status Protocol (OCSP) support, if any, maintained by your private CA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                revocation_configuration_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty(
                    crl_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty(
                        crl_distribution_point_extension_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty(
                            omit_extension=False
                        ),
                        crl_type="crlType",
                        custom_cname="customCname",
                        custom_path="customPath",
                        enabled=False,
                        expiration_in_days=123,
                        s3_bucket_name="s3BucketName",
                        s3_object_acl="s3ObjectAcl"
                    ),
                    ocsp_configuration=acmpca_mixins.CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty(
                        enabled=False,
                        ocsp_custom_cname="ocspCustomCname"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9445ab5edcd58d1fab896ba2f3beb27bee2b4987158248a97ada7deb44b62ff8)
                check_type(argname="argument crl_configuration", value=crl_configuration, expected_type=type_hints["crl_configuration"])
                check_type(argname="argument ocsp_configuration", value=ocsp_configuration, expected_type=type_hints["ocsp_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_configuration is not None:
                self._values["crl_configuration"] = crl_configuration
            if ocsp_configuration is not None:
                self._values["ocsp_configuration"] = ocsp_configuration

        @builtins.property
        def crl_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty"]]:
            '''Configuration of the certificate revocation list (CRL), if any, maintained by your private CA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-crlconfiguration
            '''
            result = self._values.get("crl_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty"]], result)

        @builtins.property
        def ocsp_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty"]]:
            '''Configuration of Online Certificate Status Protocol (OCSP) support, if any, maintained by your private CA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-revocationconfiguration.html#cfn-acmpca-certificateauthority-revocationconfiguration-ocspconfiguration
            '''
            result = self._values.get("ocsp_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RevocationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "custom_attributes": "customAttributes",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificateAuthorityPropsMixin.CustomAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''ASN1 subject for the certificate authority.

            :param common_name: Fully qualified domain name (FQDN) associated with the certificate subject.
            :param country: Two-digit code that specifies the country in which the certificate subject located.
            :param custom_attributes: Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ . .. epigraph:: Custom attributes cannot be used in combination with standard attributes.
            :param distinguished_name_qualifier: Disambiguating information for the certificate subject.
            :param generation_qualifier: Typically a qualifier appended to the name of an individual. Examples include Jr. for junior, Sr. for senior, and III for third.
            :param given_name: First name.
            :param initials: Concatenation that typically contains the first letter of the GivenName, the first letter of the middle name if one exists, and the first letter of the SurName.
            :param locality: The locality (such as a city or town) in which the certificate subject is located.
            :param organization: Legal name of the organization with which the certificate subject is affiliated.
            :param organizational_unit: A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.
            :param pseudonym: Typically a shortened version of a longer GivenName. For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.
            :param serial_number: The certificate serial number.
            :param state: State in which the subject of the certificate is located.
            :param surname: Family name.
            :param title: A personal title such as Mr.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                subject_property = acmpca_mixins.CfnCertificateAuthorityPropsMixin.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca_mixins.CfnCertificateAuthorityPropsMixin.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b8ea4ff185f94eb7fe81c26a6cd6307c5777ecd02d25a45ca20bea4e3d87e49)
                check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument distinguished_name_qualifier", value=distinguished_name_qualifier, expected_type=type_hints["distinguished_name_qualifier"])
                check_type(argname="argument generation_qualifier", value=generation_qualifier, expected_type=type_hints["generation_qualifier"])
                check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
                check_type(argname="argument initials", value=initials, expected_type=type_hints["initials"])
                check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
                check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
                check_type(argname="argument pseudonym", value=pseudonym, expected_type=type_hints["pseudonym"])
                check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            '''Fully qualified domain name (FQDN) associated with the certificate subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-commonname
            '''
            result = self._values.get("common_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            '''Two-digit code that specifies the country in which the certificate subject located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CustomAttributeProperty"]]]]:
            '''Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            .. epigraph::

               Custom attributes cannot be used in combination with standard attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificateAuthorityPropsMixin.CustomAttributeProperty"]]]], result)

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            '''Disambiguating information for the certificate subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-distinguishednamequalifier
            '''
            result = self._values.get("distinguished_name_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            '''Typically a qualifier appended to the name of an individual.

            Examples include Jr. for junior, Sr. for senior, and III for third.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-generationqualifier
            '''
            result = self._values.get("generation_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            '''First name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-givenname
            '''
            result = self._values.get("given_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            '''Concatenation that typically contains the first letter of the GivenName, the first letter of the middle name if one exists, and the first letter of the SurName.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-initials
            '''
            result = self._values.get("initials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            '''The locality (such as a city or town) in which the certificate subject is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-locality
            '''
            result = self._values.get("locality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            '''Legal name of the organization with which the certificate subject is affiliated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organization
            '''
            result = self._values.get("organization")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            '''A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-organizationalunit
            '''
            result = self._values.get("organizational_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            '''Typically a shortened version of a longer GivenName.

            For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-pseudonym
            '''
            result = self._values.get("pseudonym")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            '''The certificate serial number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-serialnumber
            '''
            result = self._values.get("serial_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''State in which the subject of the certificate is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            '''Family name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-surname
            '''
            result = self._values.get("surname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''A personal title such as Mr.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificateauthority-subject.html#cfn-acmpca-certificateauthority-subject-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "api_passthrough": "apiPassthrough",
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_signing_request": "certificateSigningRequest",
        "signing_algorithm": "signingAlgorithm",
        "template_arn": "templateArn",
        "validity": "validity",
        "validity_not_before": "validityNotBefore",
    },
)
class CfnCertificateMixinProps:
    def __init__(
        self,
        *,
        api_passthrough: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.ApiPassthroughProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        certificate_signing_request: typing.Optional[builtins.str] = None,
        signing_algorithm: typing.Optional[builtins.str] = None,
        template_arn: typing.Optional[builtins.str] = None,
        validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.ValidityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        validity_not_before: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.ValidityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnCertificatePropsMixin.

        :param api_passthrough: Specifies X.509 certificate information to be included in the issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.
        :param certificate_authority_arn: The Amazon Resource Name (ARN) for the private CA issues the certificate.
        :param certificate_signing_request: The certificate signing request (CSR) for the certificate.
        :param signing_algorithm: The name of the algorithm that will be used to sign the certificate to be issued. This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign a CSR in the ``CreateCertificateAuthority`` action. .. epigraph:: The specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.
        :param template_arn: Specifies a custom configuration template to use when issuing a certificate. If this parameter is not provided, AWS Private CA defaults to the ``EndEntityCertificate/V1`` template. For more information about AWS Private CA templates, see `Using Templates <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html>`_ .
        :param validity: The period of time during which the certificate will be valid.
        :param validity_not_before: Information describing the start of the validity period of the certificate. This parameter sets the “Not Before" date for the certificate. By default, when issuing a certificate, AWS Private CA sets the "Not Before" date to the issuance time minus 60 minutes. This compensates for clock inconsistencies across computer systems. The ``ValidityNotBefore`` parameter can be used to customize the “Not Before” value. Unlike the ``Validity`` parameter, the ``ValidityNotBefore`` parameter is optional. The ``ValidityNotBefore`` value is expressed as an explicit date and time, using the ``Validity`` type value ``ABSOLUTE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
            
            cfn_certificate_mixin_props = acmpca_mixins.CfnCertificateMixinProps(
                api_passthrough=acmpca_mixins.CfnCertificatePropsMixin.ApiPassthroughProperty(
                    extensions=acmpca_mixins.CfnCertificatePropsMixin.ExtensionsProperty(
                        certificate_policies=[acmpca_mixins.CfnCertificatePropsMixin.PolicyInformationProperty(
                            cert_policy_id="certPolicyId",
                            policy_qualifiers=[acmpca_mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty(
                                policy_qualifier_id="policyQualifierId",
                                qualifier=acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                                    cps_uri="cpsUri"
                                )
                            )]
                        )],
                        custom_extensions=[acmpca_mixins.CfnCertificatePropsMixin.CustomExtensionProperty(
                            critical=False,
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        extended_key_usage=[acmpca_mixins.CfnCertificatePropsMixin.ExtendedKeyUsageProperty(
                            extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                            extended_key_usage_type="extendedKeyUsageType"
                        )],
                        key_usage=acmpca_mixins.CfnCertificatePropsMixin.KeyUsageProperty(
                            crl_sign=False,
                            data_encipherment=False,
                            decipher_only=False,
                            digital_signature=False,
                            encipher_only=False,
                            key_agreement=False,
                            key_cert_sign=False,
                            key_encipherment=False,
                            non_repudiation=False
                        ),
                        subject_alternative_names=[acmpca_mixins.CfnCertificatePropsMixin.GeneralNameProperty(
                            directory_name=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca_mixins.CfnCertificatePropsMixin.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca_mixins.CfnCertificatePropsMixin.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        )]
                    ),
                    subject=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    )
                ),
                certificate_authority_arn="certificateAuthorityArn",
                certificate_signing_request="certificateSigningRequest",
                signing_algorithm="signingAlgorithm",
                template_arn="templateArn",
                validity=acmpca_mixins.CfnCertificatePropsMixin.ValidityProperty(
                    type="type",
                    value=123
                ),
                validity_not_before=acmpca_mixins.CfnCertificatePropsMixin.ValidityProperty(
                    type="type",
                    value=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b2aa01a0efb1d981bda21f6cf09c7f9544005051db8d0bedd624ce4163858e)
            check_type(argname="argument api_passthrough", value=api_passthrough, expected_type=type_hints["api_passthrough"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument certificate_signing_request", value=certificate_signing_request, expected_type=type_hints["certificate_signing_request"])
            check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            check_type(argname="argument template_arn", value=template_arn, expected_type=type_hints["template_arn"])
            check_type(argname="argument validity", value=validity, expected_type=type_hints["validity"])
            check_type(argname="argument validity_not_before", value=validity_not_before, expected_type=type_hints["validity_not_before"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_passthrough is not None:
            self._values["api_passthrough"] = api_passthrough
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if certificate_signing_request is not None:
            self._values["certificate_signing_request"] = certificate_signing_request
        if signing_algorithm is not None:
            self._values["signing_algorithm"] = signing_algorithm
        if template_arn is not None:
            self._values["template_arn"] = template_arn
        if validity is not None:
            self._values["validity"] = validity
        if validity_not_before is not None:
            self._values["validity_not_before"] = validity_not_before

    @builtins.property
    def api_passthrough(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ApiPassthroughProperty"]]:
        '''Specifies X.509 certificate information to be included in the issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-apipassthrough
        '''
        result = self._values.get("api_passthrough")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ApiPassthroughProperty"]], result)

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) for the private CA issues the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_signing_request(self) -> typing.Optional[builtins.str]:
        '''The certificate signing request (CSR) for the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-certificatesigningrequest
        '''
        result = self._values.get("certificate_signing_request")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def signing_algorithm(self) -> typing.Optional[builtins.str]:
        '''The name of the algorithm that will be used to sign the certificate to be issued.

        This parameter should not be confused with the ``SigningAlgorithm`` parameter used to sign a CSR in the ``CreateCertificateAuthority`` action.
        .. epigraph::

           The specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-signingalgorithm
        '''
        result = self._values.get("signing_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies a custom configuration template to use when issuing a certificate.

        If this parameter is not provided, AWS Private CA defaults to the ``EndEntityCertificate/V1`` template. For more information about AWS Private CA templates, see `Using Templates <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-templatearn
        '''
        result = self._values.get("template_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ValidityProperty"]]:
        '''The period of time during which the certificate will be valid.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validity
        '''
        result = self._values.get("validity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ValidityProperty"]], result)

    @builtins.property
    def validity_not_before(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ValidityProperty"]]:
        '''Information describing the start of the validity period of the certificate.

        This parameter sets the “Not Before" date for the certificate.

        By default, when issuing a certificate, AWS Private CA sets the "Not Before" date to the issuance time minus 60 minutes. This compensates for clock inconsistencies across computer systems. The ``ValidityNotBefore`` parameter can be used to customize the “Not Before” value.

        Unlike the ``Validity`` parameter, the ``ValidityNotBefore`` parameter is optional.

        The ``ValidityNotBefore`` value is expressed as an explicit date and time, using the ``Validity`` type value ``ABSOLUTE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html#cfn-acmpca-certificate-validitynotbefore
        '''
        result = self._values.get("validity_not_before")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ValidityProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCertificateMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnCertificatePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin",
):
    '''The ``AWS::ACMPCA::Certificate`` resource is used to issue a certificate using your private certificate authority.

    For more information, see the `IssueCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_IssueCertificate.html>`_ action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-certificate.html
    :cloudformationResource: AWS::ACMPCA::Certificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
        
        cfn_certificate_props_mixin = acmpca_mixins.CfnCertificatePropsMixin(acmpca_mixins.CfnCertificateMixinProps(
            api_passthrough=acmpca_mixins.CfnCertificatePropsMixin.ApiPassthroughProperty(
                extensions=acmpca_mixins.CfnCertificatePropsMixin.ExtensionsProperty(
                    certificate_policies=[acmpca_mixins.CfnCertificatePropsMixin.PolicyInformationProperty(
                        cert_policy_id="certPolicyId",
                        policy_qualifiers=[acmpca_mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty(
                            policy_qualifier_id="policyQualifierId",
                            qualifier=acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                                cps_uri="cpsUri"
                            )
                        )]
                    )],
                    custom_extensions=[acmpca_mixins.CfnCertificatePropsMixin.CustomExtensionProperty(
                        critical=False,
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    extended_key_usage=[acmpca_mixins.CfnCertificatePropsMixin.ExtendedKeyUsageProperty(
                        extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                        extended_key_usage_type="extendedKeyUsageType"
                    )],
                    key_usage=acmpca_mixins.CfnCertificatePropsMixin.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_alternative_names=[acmpca_mixins.CfnCertificatePropsMixin.GeneralNameProperty(
                        directory_name=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca_mixins.CfnCertificatePropsMixin.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca_mixins.CfnCertificatePropsMixin.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    )]
                ),
                subject=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                )
            ),
            certificate_authority_arn="certificateAuthorityArn",
            certificate_signing_request="certificateSigningRequest",
            signing_algorithm="signingAlgorithm",
            template_arn="templateArn",
            validity=acmpca_mixins.CfnCertificatePropsMixin.ValidityProperty(
                type="type",
                value=123
            ),
            validity_not_before=acmpca_mixins.CfnCertificatePropsMixin.ValidityProperty(
                type="type",
                value=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ACMPCA::Certificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad98aa5ffc29494da6343a840ce4f26e4fa9a635e1ecf44e1ae5a1bea2bd8bd4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b0c5928c375d66f606b11c2e88d6477cfd1f8737f8177f214def5b4841256f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37bdd78c283ce1dd2f7c66b24785f693e88a2fec67f60b075a3c25653b080e44)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnCertificateMixinProps:
        return typing.cast(CfnCertificateMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.ApiPassthroughProperty",
        jsii_struct_bases=[],
        name_mapping={"extensions": "extensions", "subject": "subject"},
    )
    class ApiPassthroughProperty:
        def __init__(
            self,
            *,
            extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.ExtensionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains X.509 certificate information to be placed in an issued certificate. An ``APIPassthrough`` or ``APICSRPassthrough`` template variant must be selected, or else this parameter is ignored.

            If conflicting or duplicate certificate information is supplied from other sources, AWS Private CA applies `order of operation rules <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html#template-order-of-operations>`_ to determine what information is used.

            :param extensions: Specifies X.509 extension information for a certificate.
            :param subject: Contains information about the certificate subject. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                api_passthrough_property = acmpca_mixins.CfnCertificatePropsMixin.ApiPassthroughProperty(
                    extensions=acmpca_mixins.CfnCertificatePropsMixin.ExtensionsProperty(
                        certificate_policies=[acmpca_mixins.CfnCertificatePropsMixin.PolicyInformationProperty(
                            cert_policy_id="certPolicyId",
                            policy_qualifiers=[acmpca_mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty(
                                policy_qualifier_id="policyQualifierId",
                                qualifier=acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                                    cps_uri="cpsUri"
                                )
                            )]
                        )],
                        custom_extensions=[acmpca_mixins.CfnCertificatePropsMixin.CustomExtensionProperty(
                            critical=False,
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        extended_key_usage=[acmpca_mixins.CfnCertificatePropsMixin.ExtendedKeyUsageProperty(
                            extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                            extended_key_usage_type="extendedKeyUsageType"
                        )],
                        key_usage=acmpca_mixins.CfnCertificatePropsMixin.KeyUsageProperty(
                            crl_sign=False,
                            data_encipherment=False,
                            decipher_only=False,
                            digital_signature=False,
                            encipher_only=False,
                            key_agreement=False,
                            key_cert_sign=False,
                            key_encipherment=False,
                            non_repudiation=False
                        ),
                        subject_alternative_names=[acmpca_mixins.CfnCertificatePropsMixin.GeneralNameProperty(
                            directory_name=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                                common_name="commonName",
                                country="country",
                                custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                                    object_identifier="objectIdentifier",
                                    value="value"
                                )],
                                distinguished_name_qualifier="distinguishedNameQualifier",
                                generation_qualifier="generationQualifier",
                                given_name="givenName",
                                initials="initials",
                                locality="locality",
                                organization="organization",
                                organizational_unit="organizationalUnit",
                                pseudonym="pseudonym",
                                serial_number="serialNumber",
                                state="state",
                                surname="surname",
                                title="title"
                            ),
                            dns_name="dnsName",
                            edi_party_name=acmpca_mixins.CfnCertificatePropsMixin.EdiPartyNameProperty(
                                name_assigner="nameAssigner",
                                party_name="partyName"
                            ),
                            ip_address="ipAddress",
                            other_name=acmpca_mixins.CfnCertificatePropsMixin.OtherNameProperty(
                                type_id="typeId",
                                value="value"
                            ),
                            registered_id="registeredId",
                            rfc822_name="rfc822Name",
                            uniform_resource_identifier="uniformResourceIdentifier"
                        )]
                    ),
                    subject=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98bfed5bfc1d347ba82e966d471846ea6f479a344cc425c1665d4cb585084ed1)
                check_type(argname="argument extensions", value=extensions, expected_type=type_hints["extensions"])
                check_type(argname="argument subject", value=subject, expected_type=type_hints["subject"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if extensions is not None:
                self._values["extensions"] = extensions
            if subject is not None:
                self._values["subject"] = subject

        @builtins.property
        def extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ExtensionsProperty"]]:
            '''Specifies X.509 extension information for a certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html#cfn-acmpca-certificate-apipassthrough-extensions
            '''
            result = self._values.get("extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ExtensionsProperty"]], result)

        @builtins.property
        def subject(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.SubjectProperty"]]:
            '''Contains information about the certificate subject.

            The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-apipassthrough.html#cfn-acmpca-certificate-apipassthrough-subject
            '''
            result = self._values.get("subject")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.SubjectProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApiPassthroughProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.CustomAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"object_identifier": "objectIdentifier", "value": "value"},
    )
    class CustomAttributeProperty:
        def __init__(
            self,
            *,
            object_identifier: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the X.500 relative distinguished name (RDN).

            :param object_identifier: Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).
            :param value: Specifies the attribute value of relative distinguished name (RDN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                custom_attribute_property = acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                    object_identifier="objectIdentifier",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4ac75c5153c7364402cdf080ec0444a2e7a2f8e6d8a5fc231cebb56fd034751)
                check_type(argname="argument object_identifier", value=object_identifier, expected_type=type_hints["object_identifier"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if object_identifier is not None:
                self._values["object_identifier"] = object_identifier
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def object_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies the object identifier (OID) of the attribute type of the relative distinguished name (RDN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customattribute.html#cfn-acmpca-certificate-customattribute-objectidentifier
            '''
            result = self._values.get("object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specifies the attribute value of relative distinguished name (RDN).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customattribute.html#cfn-acmpca-certificate-customattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.CustomExtensionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "critical": "critical",
            "object_identifier": "objectIdentifier",
            "value": "value",
        },
    )
    class CustomExtensionProperty:
        def __init__(
            self,
            *,
            critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            object_identifier: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the X.509 extension information for a certificate.

            Extensions present in ``CustomExtensions`` follow the ``ApiPassthrough`` `template rules <https://docs.aws.amazon.com/privateca/latest/userguide/UsingTemplates.html#template-order-of-operations>`_ .

            :param critical: Specifies the critical flag of the X.509 extension.
            :param object_identifier: Specifies the object identifier (OID) of the X.509 extension. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.
            :param value: Specifies the base64-encoded value of the X.509 extension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                custom_extension_property = acmpca_mixins.CfnCertificatePropsMixin.CustomExtensionProperty(
                    critical=False,
                    object_identifier="objectIdentifier",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03d8729f120d68ecf0dd00bda6df43f1d9e4154206d9080f9ced5b5c8bebf5fa)
                check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
                check_type(argname="argument object_identifier", value=object_identifier, expected_type=type_hints["object_identifier"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if critical is not None:
                self._values["critical"] = critical
            if object_identifier is not None:
                self._values["object_identifier"] = object_identifier
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def critical(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Specifies the critical flag of the X.509 extension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html#cfn-acmpca-certificate-customextension-critical
            '''
            result = self._values.get("critical")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def object_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies the object identifier (OID) of the X.509 extension. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html#cfn-acmpca-certificate-customextension-objectidentifier
            '''
            result = self._values.get("object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specifies the base64-encoded value of the X.509 extension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-customextension.html#cfn-acmpca-certificate-customextension-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomExtensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.EdiPartyNameProperty",
        jsii_struct_bases=[],
        name_mapping={"name_assigner": "nameAssigner", "party_name": "partyName"},
    )
    class EdiPartyNameProperty:
        def __init__(
            self,
            *,
            name_assigner: typing.Optional[builtins.str] = None,
            party_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an Electronic Data Interchange (EDI) entity as described in as defined in `Subject Alternative Name <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ in RFC 5280.

            :param name_assigner: Specifies the name assigner.
            :param party_name: Specifies the party name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                edi_party_name_property = acmpca_mixins.CfnCertificatePropsMixin.EdiPartyNameProperty(
                    name_assigner="nameAssigner",
                    party_name="partyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6dab4aefd4e414c78ac40fe49ccb15d02c93d1bc5cb4c98ce53c28cffe392d4)
                check_type(argname="argument name_assigner", value=name_assigner, expected_type=type_hints["name_assigner"])
                check_type(argname="argument party_name", value=party_name, expected_type=type_hints["party_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name_assigner is not None:
                self._values["name_assigner"] = name_assigner
            if party_name is not None:
                self._values["party_name"] = party_name

        @builtins.property
        def name_assigner(self) -> typing.Optional[builtins.str]:
            '''Specifies the name assigner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html#cfn-acmpca-certificate-edipartyname-nameassigner
            '''
            result = self._values.get("name_assigner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def party_name(self) -> typing.Optional[builtins.str]:
            '''Specifies the party name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-edipartyname.html#cfn-acmpca-certificate-edipartyname-partyname
            '''
            result = self._values.get("party_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EdiPartyNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.ExtendedKeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "extended_key_usage_object_identifier": "extendedKeyUsageObjectIdentifier",
            "extended_key_usage_type": "extendedKeyUsageType",
        },
    )
    class ExtendedKeyUsageProperty:
        def __init__(
            self,
            *,
            extended_key_usage_object_identifier: typing.Optional[builtins.str] = None,
            extended_key_usage_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies additional purposes for which the certified public key may be used other than basic purposes indicated in the ``KeyUsage`` extension.

            :param extended_key_usage_object_identifier: Specifies a custom ``ExtendedKeyUsage`` with an object identifier (OID).
            :param extended_key_usage_type: Specifies a standard ``ExtendedKeyUsage`` as defined as in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                extended_key_usage_property = acmpca_mixins.CfnCertificatePropsMixin.ExtendedKeyUsageProperty(
                    extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                    extended_key_usage_type="extendedKeyUsageType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__40cc3aca4a6c2b95c0c64ae256537b0d183eb75c8ec0e25fa59fc4b1a4552224)
                check_type(argname="argument extended_key_usage_object_identifier", value=extended_key_usage_object_identifier, expected_type=type_hints["extended_key_usage_object_identifier"])
                check_type(argname="argument extended_key_usage_type", value=extended_key_usage_type, expected_type=type_hints["extended_key_usage_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if extended_key_usage_object_identifier is not None:
                self._values["extended_key_usage_object_identifier"] = extended_key_usage_object_identifier
            if extended_key_usage_type is not None:
                self._values["extended_key_usage_type"] = extended_key_usage_type

        @builtins.property
        def extended_key_usage_object_identifier(self) -> typing.Optional[builtins.str]:
            '''Specifies a custom ``ExtendedKeyUsage`` with an object identifier (OID).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html#cfn-acmpca-certificate-extendedkeyusage-extendedkeyusageobjectidentifier
            '''
            result = self._values.get("extended_key_usage_object_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def extended_key_usage_type(self) -> typing.Optional[builtins.str]:
            '''Specifies a standard ``ExtendedKeyUsage`` as defined as in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.12>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extendedkeyusage.html#cfn-acmpca-certificate-extendedkeyusage-extendedkeyusagetype
            '''
            result = self._values.get("extended_key_usage_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtendedKeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.ExtensionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "certificate_policies": "certificatePolicies",
            "custom_extensions": "customExtensions",
            "extended_key_usage": "extendedKeyUsage",
            "key_usage": "keyUsage",
            "subject_alternative_names": "subjectAlternativeNames",
        },
    )
    class ExtensionsProperty:
        def __init__(
            self,
            *,
            certificate_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.PolicyInformationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            custom_extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.CustomExtensionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            extended_key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.ExtendedKeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.KeyUsageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.GeneralNameProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains X.509 extension information for a certificate.

            :param certificate_policies: Contains a sequence of one or more policy information terms, each of which consists of an object identifier (OID) and optional qualifiers. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ . In an end-entity certificate, these terms indicate the policy under which the certificate was issued and the purposes for which it may be used. In a CA certificate, these terms limit the set of policies for certification paths that include this certificate.
            :param custom_extensions: Contains a sequence of one or more X.509 extensions, each of which consists of an object identifier (OID), a base64-encoded value, and the critical flag. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.
            :param extended_key_usage: Specifies additional purposes for which the certified public key may be used other than basic purposes indicated in the ``KeyUsage`` extension.
            :param key_usage: Defines one or more purposes for which the key contained in the certificate can be used. Default value for each option is false.
            :param subject_alternative_names: The subject alternative name extension allows identities to be bound to the subject of the certificate. These identities may be included in addition to or in place of the identity in the subject field of the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                extensions_property = acmpca_mixins.CfnCertificatePropsMixin.ExtensionsProperty(
                    certificate_policies=[acmpca_mixins.CfnCertificatePropsMixin.PolicyInformationProperty(
                        cert_policy_id="certPolicyId",
                        policy_qualifiers=[acmpca_mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty(
                            policy_qualifier_id="policyQualifierId",
                            qualifier=acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                                cps_uri="cpsUri"
                            )
                        )]
                    )],
                    custom_extensions=[acmpca_mixins.CfnCertificatePropsMixin.CustomExtensionProperty(
                        critical=False,
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    extended_key_usage=[acmpca_mixins.CfnCertificatePropsMixin.ExtendedKeyUsageProperty(
                        extended_key_usage_object_identifier="extendedKeyUsageObjectIdentifier",
                        extended_key_usage_type="extendedKeyUsageType"
                    )],
                    key_usage=acmpca_mixins.CfnCertificatePropsMixin.KeyUsageProperty(
                        crl_sign=False,
                        data_encipherment=False,
                        decipher_only=False,
                        digital_signature=False,
                        encipher_only=False,
                        key_agreement=False,
                        key_cert_sign=False,
                        key_encipherment=False,
                        non_repudiation=False
                    ),
                    subject_alternative_names=[acmpca_mixins.CfnCertificatePropsMixin.GeneralNameProperty(
                        directory_name=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                            common_name="commonName",
                            country="country",
                            custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                                object_identifier="objectIdentifier",
                                value="value"
                            )],
                            distinguished_name_qualifier="distinguishedNameQualifier",
                            generation_qualifier="generationQualifier",
                            given_name="givenName",
                            initials="initials",
                            locality="locality",
                            organization="organization",
                            organizational_unit="organizationalUnit",
                            pseudonym="pseudonym",
                            serial_number="serialNumber",
                            state="state",
                            surname="surname",
                            title="title"
                        ),
                        dns_name="dnsName",
                        edi_party_name=acmpca_mixins.CfnCertificatePropsMixin.EdiPartyNameProperty(
                            name_assigner="nameAssigner",
                            party_name="partyName"
                        ),
                        ip_address="ipAddress",
                        other_name=acmpca_mixins.CfnCertificatePropsMixin.OtherNameProperty(
                            type_id="typeId",
                            value="value"
                        ),
                        registered_id="registeredId",
                        rfc822_name="rfc822Name",
                        uniform_resource_identifier="uniformResourceIdentifier"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72ab952e881b5da71e8f9c1c22b5244144bd7edd18d53b7d0feac6636a16c5cb)
                check_type(argname="argument certificate_policies", value=certificate_policies, expected_type=type_hints["certificate_policies"])
                check_type(argname="argument custom_extensions", value=custom_extensions, expected_type=type_hints["custom_extensions"])
                check_type(argname="argument extended_key_usage", value=extended_key_usage, expected_type=type_hints["extended_key_usage"])
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
                check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if certificate_policies is not None:
                self._values["certificate_policies"] = certificate_policies
            if custom_extensions is not None:
                self._values["custom_extensions"] = custom_extensions
            if extended_key_usage is not None:
                self._values["extended_key_usage"] = extended_key_usage
            if key_usage is not None:
                self._values["key_usage"] = key_usage
            if subject_alternative_names is not None:
                self._values["subject_alternative_names"] = subject_alternative_names

        @builtins.property
        def certificate_policies(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.PolicyInformationProperty"]]]]:
            '''Contains a sequence of one or more policy information terms, each of which consists of an object identifier (OID) and optional qualifiers.

            For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            In an end-entity certificate, these terms indicate the policy under which the certificate was issued and the purposes for which it may be used. In a CA certificate, these terms limit the set of policies for certification paths that include this certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-certificatepolicies
            '''
            result = self._values.get("certificate_policies")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.PolicyInformationProperty"]]]], result)

        @builtins.property
        def custom_extensions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.CustomExtensionProperty"]]]]:
            '''Contains a sequence of one or more X.509 extensions, each of which consists of an object identifier (OID), a base64-encoded value, and the critical flag. For more information, see the `Global OID reference database. <https://docs.aws.amazon.com/https://oidref.com/2.5.29>`_.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-customextensions
            '''
            result = self._values.get("custom_extensions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.CustomExtensionProperty"]]]], result)

        @builtins.property
        def extended_key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ExtendedKeyUsageProperty"]]]]:
            '''Specifies additional purposes for which the certified public key may be used other than basic purposes indicated in the ``KeyUsage`` extension.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-extendedkeyusage
            '''
            result = self._values.get("extended_key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.ExtendedKeyUsageProperty"]]]], result)

        @builtins.property
        def key_usage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.KeyUsageProperty"]]:
            '''Defines one or more purposes for which the key contained in the certificate can be used.

            Default value for each option is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.KeyUsageProperty"]], result)

        @builtins.property
        def subject_alternative_names(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.GeneralNameProperty"]]]]:
            '''The subject alternative name extension allows identities to be bound to the subject of the certificate.

            These identities may be included in addition to or in place of the identity in the subject field of the certificate.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-extensions.html#cfn-acmpca-certificate-extensions-subjectalternativenames
            '''
            result = self._values.get("subject_alternative_names")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.GeneralNameProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExtensionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.GeneralNameProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_name": "directoryName",
            "dns_name": "dnsName",
            "edi_party_name": "ediPartyName",
            "ip_address": "ipAddress",
            "other_name": "otherName",
            "registered_id": "registeredId",
            "rfc822_name": "rfc822Name",
            "uniform_resource_identifier": "uniformResourceIdentifier",
        },
    )
    class GeneralNameProperty:
        def __init__(
            self,
            *,
            directory_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.SubjectProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dns_name: typing.Optional[builtins.str] = None,
            edi_party_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.EdiPartyNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address: typing.Optional[builtins.str] = None,
            other_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.OtherNameProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            registered_id: typing.Optional[builtins.str] = None,
            rfc822_name: typing.Optional[builtins.str] = None,
            uniform_resource_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes an ASN.1 X.400 ``GeneralName`` as defined in `RFC 5280 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280>`_ . Only one of the following naming options should be provided. Providing more than one option results in an ``InvalidArgsException`` error.

            :param directory_name: Contains information about the certificate subject. The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.
            :param dns_name: Represents ``GeneralName`` as a DNS name.
            :param edi_party_name: Represents ``GeneralName`` as an ``EdiPartyName`` object.
            :param ip_address: Represents ``GeneralName`` as an IPv4 or IPv6 address.
            :param other_name: Represents ``GeneralName`` using an ``OtherName`` object.
            :param registered_id: Represents ``GeneralName`` as an object identifier (OID).
            :param rfc822_name: Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.
            :param uniform_resource_identifier: Represents ``GeneralName`` as a URI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                general_name_property = acmpca_mixins.CfnCertificatePropsMixin.GeneralNameProperty(
                    directory_name=acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                        common_name="commonName",
                        country="country",
                        custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                            object_identifier="objectIdentifier",
                            value="value"
                        )],
                        distinguished_name_qualifier="distinguishedNameQualifier",
                        generation_qualifier="generationQualifier",
                        given_name="givenName",
                        initials="initials",
                        locality="locality",
                        organization="organization",
                        organizational_unit="organizationalUnit",
                        pseudonym="pseudonym",
                        serial_number="serialNumber",
                        state="state",
                        surname="surname",
                        title="title"
                    ),
                    dns_name="dnsName",
                    edi_party_name=acmpca_mixins.CfnCertificatePropsMixin.EdiPartyNameProperty(
                        name_assigner="nameAssigner",
                        party_name="partyName"
                    ),
                    ip_address="ipAddress",
                    other_name=acmpca_mixins.CfnCertificatePropsMixin.OtherNameProperty(
                        type_id="typeId",
                        value="value"
                    ),
                    registered_id="registeredId",
                    rfc822_name="rfc822Name",
                    uniform_resource_identifier="uniformResourceIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03d20a57c567bdd27764bca4df52417b5fac623980db3e755dde53ac608ca318)
                check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
                check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
                check_type(argname="argument edi_party_name", value=edi_party_name, expected_type=type_hints["edi_party_name"])
                check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
                check_type(argname="argument other_name", value=other_name, expected_type=type_hints["other_name"])
                check_type(argname="argument registered_id", value=registered_id, expected_type=type_hints["registered_id"])
                check_type(argname="argument rfc822_name", value=rfc822_name, expected_type=type_hints["rfc822_name"])
                check_type(argname="argument uniform_resource_identifier", value=uniform_resource_identifier, expected_type=type_hints["uniform_resource_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_name is not None:
                self._values["directory_name"] = directory_name
            if dns_name is not None:
                self._values["dns_name"] = dns_name
            if edi_party_name is not None:
                self._values["edi_party_name"] = edi_party_name
            if ip_address is not None:
                self._values["ip_address"] = ip_address
            if other_name is not None:
                self._values["other_name"] = other_name
            if registered_id is not None:
                self._values["registered_id"] = registered_id
            if rfc822_name is not None:
                self._values["rfc822_name"] = rfc822_name
            if uniform_resource_identifier is not None:
                self._values["uniform_resource_identifier"] = uniform_resource_identifier

        @builtins.property
        def directory_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.SubjectProperty"]]:
            '''Contains information about the certificate subject.

            The certificate can be one issued by your private certificate authority (CA) or it can be your private CA certificate. The Subject field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The Subject must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate. The DN must be unique for each entity, but your private CA can issue more than one certificate with the same DN to the same entity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-directoryname
            '''
            result = self._values.get("directory_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.SubjectProperty"]], result)

        @builtins.property
        def dns_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a DNS name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-dnsname
            '''
            result = self._values.get("dns_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def edi_party_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.EdiPartyNameProperty"]]:
            '''Represents ``GeneralName`` as an ``EdiPartyName`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-edipartyname
            '''
            result = self._values.get("edi_party_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.EdiPartyNameProperty"]], result)

        @builtins.property
        def ip_address(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an IPv4 or IPv6 address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-ipaddress
            '''
            result = self._values.get("ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def other_name(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.OtherNameProperty"]]:
            '''Represents ``GeneralName`` using an ``OtherName`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-othername
            '''
            result = self._values.get("other_name")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.OtherNameProperty"]], result)

        @builtins.property
        def registered_id(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an object identifier (OID).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-registeredid
            '''
            result = self._values.get("registered_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def rfc822_name(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as an `RFC 822 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc822>`_ email address.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-rfc822name
            '''
            result = self._values.get("rfc822_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def uniform_resource_identifier(self) -> typing.Optional[builtins.str]:
            '''Represents ``GeneralName`` as a URI.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-generalname.html#cfn-acmpca-certificate-generalname-uniformresourceidentifier
            '''
            result = self._values.get("uniform_resource_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GeneralNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.KeyUsageProperty",
        jsii_struct_bases=[],
        name_mapping={
            "crl_sign": "crlSign",
            "data_encipherment": "dataEncipherment",
            "decipher_only": "decipherOnly",
            "digital_signature": "digitalSignature",
            "encipher_only": "encipherOnly",
            "key_agreement": "keyAgreement",
            "key_cert_sign": "keyCertSign",
            "key_encipherment": "keyEncipherment",
            "non_repudiation": "nonRepudiation",
        },
    )
    class KeyUsageProperty:
        def __init__(
            self,
            *,
            crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Defines one or more purposes for which the key contained in the certificate can be used.

            Default value for each option is false.

            :param crl_sign: Key can be used to sign CRLs. Default: - false
            :param data_encipherment: Key can be used to decipher data. Default: - false
            :param decipher_only: Key can be used only to decipher data. Default: - false
            :param digital_signature: Key can be used for digital signing. Default: - false
            :param encipher_only: Key can be used only to encipher data. Default: - false
            :param key_agreement: Key can be used in a key-agreement protocol. Default: - false
            :param key_cert_sign: Key can be used to sign certificates. Default: - false
            :param key_encipherment: Key can be used to encipher data. Default: - false
            :param non_repudiation: Key can be used for non-repudiation. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                key_usage_property = acmpca_mixins.CfnCertificatePropsMixin.KeyUsageProperty(
                    crl_sign=False,
                    data_encipherment=False,
                    decipher_only=False,
                    digital_signature=False,
                    encipher_only=False,
                    key_agreement=False,
                    key_cert_sign=False,
                    key_encipherment=False,
                    non_repudiation=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a5a22f58704b045d5ec98993b08e2a77d4e21db93b3558bcdb1e8656935a83e7)
                check_type(argname="argument crl_sign", value=crl_sign, expected_type=type_hints["crl_sign"])
                check_type(argname="argument data_encipherment", value=data_encipherment, expected_type=type_hints["data_encipherment"])
                check_type(argname="argument decipher_only", value=decipher_only, expected_type=type_hints["decipher_only"])
                check_type(argname="argument digital_signature", value=digital_signature, expected_type=type_hints["digital_signature"])
                check_type(argname="argument encipher_only", value=encipher_only, expected_type=type_hints["encipher_only"])
                check_type(argname="argument key_agreement", value=key_agreement, expected_type=type_hints["key_agreement"])
                check_type(argname="argument key_cert_sign", value=key_cert_sign, expected_type=type_hints["key_cert_sign"])
                check_type(argname="argument key_encipherment", value=key_encipherment, expected_type=type_hints["key_encipherment"])
                check_type(argname="argument non_repudiation", value=non_repudiation, expected_type=type_hints["non_repudiation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if crl_sign is not None:
                self._values["crl_sign"] = crl_sign
            if data_encipherment is not None:
                self._values["data_encipherment"] = data_encipherment
            if decipher_only is not None:
                self._values["decipher_only"] = decipher_only
            if digital_signature is not None:
                self._values["digital_signature"] = digital_signature
            if encipher_only is not None:
                self._values["encipher_only"] = encipher_only
            if key_agreement is not None:
                self._values["key_agreement"] = key_agreement
            if key_cert_sign is not None:
                self._values["key_cert_sign"] = key_cert_sign
            if key_encipherment is not None:
                self._values["key_encipherment"] = key_encipherment
            if non_repudiation is not None:
                self._values["non_repudiation"] = non_repudiation

        @builtins.property
        def crl_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to sign CRLs.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-crlsign
            '''
            result = self._values.get("crl_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to decipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-dataencipherment
            '''
            result = self._values.get("data_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def decipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used only to decipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-decipheronly
            '''
            result = self._values.get("decipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def digital_signature(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used for digital signing.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-digitalsignature
            '''
            result = self._values.get("digital_signature")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encipher_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used only to encipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-encipheronly
            '''
            result = self._values.get("encipher_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_agreement(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used in a key-agreement protocol.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keyagreement
            '''
            result = self._values.get("key_agreement")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_cert_sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to sign certificates.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keycertsign
            '''
            result = self._values.get("key_cert_sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def key_encipherment(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used to encipher data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-keyencipherment
            '''
            result = self._values.get("key_encipherment")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def non_repudiation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Key can be used for non-repudiation.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-keyusage.html#cfn-acmpca-certificate-keyusage-nonrepudiation
            '''
            result = self._values.get("non_repudiation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyUsageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.OtherNameProperty",
        jsii_struct_bases=[],
        name_mapping={"type_id": "typeId", "value": "value"},
    )
    class OtherNameProperty:
        def __init__(
            self,
            *,
            type_id: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a custom ASN.1 X.400 ``GeneralName`` using an object identifier (OID) and value. The OID must satisfy the regular expression shown below. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :param type_id: Specifies an OID.
            :param value: Specifies an OID value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                other_name_property = acmpca_mixins.CfnCertificatePropsMixin.OtherNameProperty(
                    type_id="typeId",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0554e8dc9895d271e74953b5a6fdd1c54d9bfd89eed420767bd0db7eefa39d16)
                check_type(argname="argument type_id", value=type_id, expected_type=type_hints["type_id"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type_id is not None:
                self._values["type_id"] = type_id
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type_id(self) -> typing.Optional[builtins.str]:
            '''Specifies an OID.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html#cfn-acmpca-certificate-othername-typeid
            '''
            result = self._values.get("type_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Specifies an OID value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-othername.html#cfn-acmpca-certificate-othername-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OtherNameProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.PolicyInformationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cert_policy_id": "certPolicyId",
            "policy_qualifiers": "policyQualifiers",
        },
    )
    class PolicyInformationProperty:
        def __init__(
            self,
            *,
            cert_policy_id: typing.Optional[builtins.str] = None,
            policy_qualifiers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.PolicyQualifierInfoProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines the X.509 ``CertificatePolicies`` extension.

            :param cert_policy_id: Specifies the object identifier (OID) of the certificate policy under which the certificate was issued. For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .
            :param policy_qualifiers: Modifies the given ``CertPolicyId`` with a qualifier. AWS Private CA supports the certification practice statement (CPS) qualifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                policy_information_property = acmpca_mixins.CfnCertificatePropsMixin.PolicyInformationProperty(
                    cert_policy_id="certPolicyId",
                    policy_qualifiers=[acmpca_mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty(
                        policy_qualifier_id="policyQualifierId",
                        qualifier=acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                            cps_uri="cpsUri"
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b99b31b0888daa7926f2c6eecb517a63139a9bbe2ce406b190af2b368a7ef96b)
                check_type(argname="argument cert_policy_id", value=cert_policy_id, expected_type=type_hints["cert_policy_id"])
                check_type(argname="argument policy_qualifiers", value=policy_qualifiers, expected_type=type_hints["policy_qualifiers"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cert_policy_id is not None:
                self._values["cert_policy_id"] = cert_policy_id
            if policy_qualifiers is not None:
                self._values["policy_qualifiers"] = policy_qualifiers

        @builtins.property
        def cert_policy_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the object identifier (OID) of the certificate policy under which the certificate was issued.

            For more information, see NIST's definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html#cfn-acmpca-certificate-policyinformation-certpolicyid
            '''
            result = self._values.get("cert_policy_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_qualifiers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.PolicyQualifierInfoProperty"]]]]:
            '''Modifies the given ``CertPolicyId`` with a qualifier.

            AWS Private CA supports the certification practice statement (CPS) qualifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyinformation.html#cfn-acmpca-certificate-policyinformation-policyqualifiers
            '''
            result = self._values.get("policy_qualifiers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.PolicyQualifierInfoProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyInformationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_qualifier_id": "policyQualifierId",
            "qualifier": "qualifier",
        },
    )
    class PolicyQualifierInfoProperty:
        def __init__(
            self,
            *,
            policy_qualifier_id: typing.Optional[builtins.str] = None,
            qualifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.QualifierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Modifies the ``CertPolicyId`` of a ``PolicyInformation`` object with a qualifier.

            AWS Private CA supports the certification practice statement (CPS) qualifier.

            :param policy_qualifier_id: Identifies the qualifier modifying a ``CertPolicyId`` .
            :param qualifier: Defines the qualifier type. AWS Private CA supports the use of a URI for a CPS qualifier in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                policy_qualifier_info_property = acmpca_mixins.CfnCertificatePropsMixin.PolicyQualifierInfoProperty(
                    policy_qualifier_id="policyQualifierId",
                    qualifier=acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                        cps_uri="cpsUri"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1fcb27af89b7c2eba37cb7bbb250795786f9127fb8eaff885ef5d44d69b1acf2)
                check_type(argname="argument policy_qualifier_id", value=policy_qualifier_id, expected_type=type_hints["policy_qualifier_id"])
                check_type(argname="argument qualifier", value=qualifier, expected_type=type_hints["qualifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if policy_qualifier_id is not None:
                self._values["policy_qualifier_id"] = policy_qualifier_id
            if qualifier is not None:
                self._values["qualifier"] = qualifier

        @builtins.property
        def policy_qualifier_id(self) -> typing.Optional[builtins.str]:
            '''Identifies the qualifier modifying a ``CertPolicyId`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html#cfn-acmpca-certificate-policyqualifierinfo-policyqualifierid
            '''
            result = self._values.get("policy_qualifier_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def qualifier(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.QualifierProperty"]]:
            '''Defines the qualifier type.

            AWS Private CA supports the use of a URI for a CPS qualifier in this field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-policyqualifierinfo.html#cfn-acmpca-certificate-policyqualifierinfo-qualifier
            '''
            result = self._values.get("qualifier")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.QualifierProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyQualifierInfoProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.QualifierProperty",
        jsii_struct_bases=[],
        name_mapping={"cps_uri": "cpsUri"},
    )
    class QualifierProperty:
        def __init__(self, *, cps_uri: typing.Optional[builtins.str] = None) -> None:
            '''Defines a ``PolicyInformation`` qualifier.

            AWS Private CA supports the `certification practice statement (CPS) qualifier <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc5280#section-4.2.1.4>`_ defined in RFC 5280.

            :param cps_uri: Contains a pointer to a certification practice statement (CPS) published by the CA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-qualifier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                qualifier_property = acmpca_mixins.CfnCertificatePropsMixin.QualifierProperty(
                    cps_uri="cpsUri"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26fe45ada088b088b33106d1ffc0689334ffc78fe27f2b684349cf96a12b06b1)
                check_type(argname="argument cps_uri", value=cps_uri, expected_type=type_hints["cps_uri"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cps_uri is not None:
                self._values["cps_uri"] = cps_uri

        @builtins.property
        def cps_uri(self) -> typing.Optional[builtins.str]:
            '''Contains a pointer to a certification practice statement (CPS) published by the CA.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-qualifier.html#cfn-acmpca-certificate-qualifier-cpsuri
            '''
            result = self._values.get("cps_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "QualifierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.SubjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "common_name": "commonName",
            "country": "country",
            "custom_attributes": "customAttributes",
            "distinguished_name_qualifier": "distinguishedNameQualifier",
            "generation_qualifier": "generationQualifier",
            "given_name": "givenName",
            "initials": "initials",
            "locality": "locality",
            "organization": "organization",
            "organizational_unit": "organizationalUnit",
            "pseudonym": "pseudonym",
            "serial_number": "serialNumber",
            "state": "state",
            "surname": "surname",
            "title": "title",
        },
    )
    class SubjectProperty:
        def __init__(
            self,
            *,
            common_name: typing.Optional[builtins.str] = None,
            country: typing.Optional[builtins.str] = None,
            custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.CustomAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            distinguished_name_qualifier: typing.Optional[builtins.str] = None,
            generation_qualifier: typing.Optional[builtins.str] = None,
            given_name: typing.Optional[builtins.str] = None,
            initials: typing.Optional[builtins.str] = None,
            locality: typing.Optional[builtins.str] = None,
            organization: typing.Optional[builtins.str] = None,
            organizational_unit: typing.Optional[builtins.str] = None,
            pseudonym: typing.Optional[builtins.str] = None,
            serial_number: typing.Optional[builtins.str] = None,
            state: typing.Optional[builtins.str] = None,
            surname: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about the certificate subject.

            The ``Subject`` field in the certificate identifies the entity that owns or controls the public key in the certificate. The entity can be a user, computer, device, or service. The ``Subject`` must contain an X.500 distinguished name (DN). A DN is a sequence of relative distinguished names (RDNs). The RDNs are separated by commas in the certificate.

            :param common_name: For CA and end-entity certificates in a private PKI, the common name (CN) can be any string within the length limit. Note: In publicly trusted certificates, the common name must be a fully qualified domain name (FQDN) associated with the certificate subject.
            :param country: Two-digit code that specifies the country in which the certificate subject located.
            :param custom_attributes: Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ . .. epigraph:: Custom attributes cannot be used in combination with standard attributes.
            :param distinguished_name_qualifier: Disambiguating information for the certificate subject.
            :param generation_qualifier: Typically a qualifier appended to the name of an individual. Examples include Jr. for junior, Sr. for senior, and III for third.
            :param given_name: First name.
            :param initials: Concatenation that typically contains the first letter of the *GivenName* , the first letter of the middle name if one exists, and the first letter of the *Surname* .
            :param locality: The locality (such as a city or town) in which the certificate subject is located.
            :param organization: Legal name of the organization with which the certificate subject is affiliated.
            :param organizational_unit: A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.
            :param pseudonym: Typically a shortened version of a longer *GivenName* . For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.
            :param serial_number: The certificate serial number.
            :param state: State in which the subject of the certificate is located.
            :param surname: Family name. In the US and the UK, for example, the surname of an individual is ordered last. In Asian cultures the surname is typically ordered first.
            :param title: A title such as Mr. or Ms., which is pre-pended to the name to refer formally to the certificate subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                subject_property = acmpca_mixins.CfnCertificatePropsMixin.SubjectProperty(
                    common_name="commonName",
                    country="country",
                    custom_attributes=[acmpca_mixins.CfnCertificatePropsMixin.CustomAttributeProperty(
                        object_identifier="objectIdentifier",
                        value="value"
                    )],
                    distinguished_name_qualifier="distinguishedNameQualifier",
                    generation_qualifier="generationQualifier",
                    given_name="givenName",
                    initials="initials",
                    locality="locality",
                    organization="organization",
                    organizational_unit="organizationalUnit",
                    pseudonym="pseudonym",
                    serial_number="serialNumber",
                    state="state",
                    surname="surname",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb1c1a736d9342ed3dc813070ed52ed1552792c8b34ca61cb4a59fbbc2411fb3)
                check_type(argname="argument common_name", value=common_name, expected_type=type_hints["common_name"])
                check_type(argname="argument country", value=country, expected_type=type_hints["country"])
                check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
                check_type(argname="argument distinguished_name_qualifier", value=distinguished_name_qualifier, expected_type=type_hints["distinguished_name_qualifier"])
                check_type(argname="argument generation_qualifier", value=generation_qualifier, expected_type=type_hints["generation_qualifier"])
                check_type(argname="argument given_name", value=given_name, expected_type=type_hints["given_name"])
                check_type(argname="argument initials", value=initials, expected_type=type_hints["initials"])
                check_type(argname="argument locality", value=locality, expected_type=type_hints["locality"])
                check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
                check_type(argname="argument organizational_unit", value=organizational_unit, expected_type=type_hints["organizational_unit"])
                check_type(argname="argument pseudonym", value=pseudonym, expected_type=type_hints["pseudonym"])
                check_type(argname="argument serial_number", value=serial_number, expected_type=type_hints["serial_number"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
                check_type(argname="argument surname", value=surname, expected_type=type_hints["surname"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if common_name is not None:
                self._values["common_name"] = common_name
            if country is not None:
                self._values["country"] = country
            if custom_attributes is not None:
                self._values["custom_attributes"] = custom_attributes
            if distinguished_name_qualifier is not None:
                self._values["distinguished_name_qualifier"] = distinguished_name_qualifier
            if generation_qualifier is not None:
                self._values["generation_qualifier"] = generation_qualifier
            if given_name is not None:
                self._values["given_name"] = given_name
            if initials is not None:
                self._values["initials"] = initials
            if locality is not None:
                self._values["locality"] = locality
            if organization is not None:
                self._values["organization"] = organization
            if organizational_unit is not None:
                self._values["organizational_unit"] = organizational_unit
            if pseudonym is not None:
                self._values["pseudonym"] = pseudonym
            if serial_number is not None:
                self._values["serial_number"] = serial_number
            if state is not None:
                self._values["state"] = state
            if surname is not None:
                self._values["surname"] = surname
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def common_name(self) -> typing.Optional[builtins.str]:
            '''For CA and end-entity certificates in a private PKI, the common name (CN) can be any string within the length limit.

            Note: In publicly trusted certificates, the common name must be a fully qualified domain name (FQDN) associated with the certificate subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-commonname
            '''
            result = self._values.get("common_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def country(self) -> typing.Optional[builtins.str]:
            '''Two-digit code that specifies the country in which the certificate subject located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-country
            '''
            result = self._values.get("country")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def custom_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.CustomAttributeProperty"]]]]:
            '''Contains a sequence of one or more X.500 relative distinguished names (RDNs), each of which consists of an object identifier (OID) and a value. For more information, see NIST’s definition of `Object Identifier (OID) <https://docs.aws.amazon.com/https://csrc.nist.gov/glossary/term/Object_Identifier>`_ .

            .. epigraph::

               Custom attributes cannot be used in combination with standard attributes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-customattributes
            '''
            result = self._values.get("custom_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.CustomAttributeProperty"]]]], result)

        @builtins.property
        def distinguished_name_qualifier(self) -> typing.Optional[builtins.str]:
            '''Disambiguating information for the certificate subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-distinguishednamequalifier
            '''
            result = self._values.get("distinguished_name_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def generation_qualifier(self) -> typing.Optional[builtins.str]:
            '''Typically a qualifier appended to the name of an individual.

            Examples include Jr. for junior, Sr. for senior, and III for third.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-generationqualifier
            '''
            result = self._values.get("generation_qualifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def given_name(self) -> typing.Optional[builtins.str]:
            '''First name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-givenname
            '''
            result = self._values.get("given_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def initials(self) -> typing.Optional[builtins.str]:
            '''Concatenation that typically contains the first letter of the *GivenName* , the first letter of the middle name if one exists, and the first letter of the *Surname* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-initials
            '''
            result = self._values.get("initials")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locality(self) -> typing.Optional[builtins.str]:
            '''The locality (such as a city or town) in which the certificate subject is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-locality
            '''
            result = self._values.get("locality")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organization(self) -> typing.Optional[builtins.str]:
            '''Legal name of the organization with which the certificate subject is affiliated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-organization
            '''
            result = self._values.get("organization")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit(self) -> typing.Optional[builtins.str]:
            '''A subdivision or unit of the organization (such as sales or finance) with which the certificate subject is affiliated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-organizationalunit
            '''
            result = self._values.get("organizational_unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pseudonym(self) -> typing.Optional[builtins.str]:
            '''Typically a shortened version of a longer *GivenName* .

            For example, Jonathan is often shortened to John. Elizabeth is often shortened to Beth, Liz, or Eliza.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-pseudonym
            '''
            result = self._values.get("pseudonym")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def serial_number(self) -> typing.Optional[builtins.str]:
            '''The certificate serial number.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-serialnumber
            '''
            result = self._values.get("serial_number")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''State in which the subject of the certificate is located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def surname(self) -> typing.Optional[builtins.str]:
            '''Family name.

            In the US and the UK, for example, the surname of an individual is ordered last. In Asian cultures the surname is typically ordered first.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-surname
            '''
            result = self._values.get("surname")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''A title such as Mr.

            or Ms., which is pre-pended to the name to refer formally to the certificate subject.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-subject.html#cfn-acmpca-certificate-subject-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnCertificatePropsMixin.ValidityProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ValidityProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Length of time for which the certificate issued by your private certificate authority (CA), or by the private CA itself, is valid in days, months, or years.

            You can issue a certificate by calling the ``IssueCertificate`` operation.

            :param type: Specifies whether the ``Value`` parameter represents days, months, or years.
            :param value: A long integer interpreted according to the value of ``Type`` , below.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
                
                validity_property = acmpca_mixins.CfnCertificatePropsMixin.ValidityProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb3521f44fd13d3e3f96a152cf1a752cf909a3e00621751114a48ff5761a6db8)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the ``Value`` parameter represents days, months, or years.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''A long integer interpreted according to the value of ``Type`` , below.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-acmpca-certificate-validity.html#cfn-acmpca-certificate-validity-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnPermissionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "certificate_authority_arn": "certificateAuthorityArn",
        "principal": "principal",
        "source_account": "sourceAccount",
    },
)
class CfnPermissionMixinProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        principal: typing.Optional[builtins.str] = None,
        source_account: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnPermissionPropsMixin.

        :param actions: The private CA actions that can be performed by the designated AWS service. Supported actions are ``IssueCertificate`` , ``GetCertificate`` , and ``ListPermissions`` .
        :param certificate_authority_arn: The Amazon Resource Number (ARN) of the private CA from which the permission was issued.
        :param principal: The AWS service or entity that holds the permission. At this time, the only valid principal is ``acm.amazonaws.com`` .
        :param source_account: The ID of the account that assigned the permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
            
            cfn_permission_mixin_props = acmpca_mixins.CfnPermissionMixinProps(
                actions=["actions"],
                certificate_authority_arn="certificateAuthorityArn",
                principal="principal",
                source_account="sourceAccount"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7952727bf88a60fc9d96368bbef3d142142b483809bafecd24f19e4715bf6b1a)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument source_account", value=source_account, expected_type=type_hints["source_account"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if principal is not None:
            self._values["principal"] = principal
        if source_account is not None:
            self._values["source_account"] = source_account

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The private CA actions that can be performed by the designated AWS service.

        Supported actions are ``IssueCertificate`` , ``GetCertificate`` , and ``ListPermissions`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Number (ARN) of the private CA from which the permission was issued.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def principal(self) -> typing.Optional[builtins.str]:
        '''The AWS service or entity that holds the permission.

        At this time, the only valid principal is ``acm.amazonaws.com`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_account(self) -> typing.Optional[builtins.str]:
        '''The ID of the account that assigned the permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html#cfn-acmpca-permission-sourceaccount
        '''
        result = self._values.get("source_account")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPermissionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_acmpca.mixins.CfnPermissionPropsMixin",
):
    '''Grants permissions to the Certificate Manager ( ACM ) service principal ( ``acm.amazonaws.com`` ) to perform `IssueCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_IssueCertificate.html>`_ , `GetCertificate <https://docs.aws.amazon.com/privateca/latest/APIReference/API_GetCertificate.html>`_ , and `ListPermissions <https://docs.aws.amazon.com/privateca/latest/APIReference/API_ListPermissions.html>`_ actions on a CA. These actions are needed for the ACM principal to renew private PKI certificates requested through ACM and residing in the same AWS account as the CA.

    **About permissions** - If the private CA and the certificates it issues reside in the same account, you can use ``AWS::ACMPCA::Permission`` to grant permissions for ACM to carry out automatic certificate renewals.

    - For automatic certificate renewal to succeed, the ACM service principal needs permissions to create, retrieve, and list permissions.
    - If the private CA and the ACM certificates reside in different accounts, then permissions cannot be used to enable automatic renewals. Instead, the ACM certificate owner must set up a resource-based policy to enable cross-account issuance and renewals. For more information, see `Using a Resource Based Policy with AWS Private CA <https://docs.aws.amazon.com/privateca/latest/userguide/pca-rbp.html>`_ .

    .. epigraph::

       To update an ``AWS::ACMPCA::Permission`` resource, you must first delete the existing permission resource from the CloudFormation stack and then create a new permission resource with updated properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-acmpca-permission.html
    :cloudformationResource: AWS::ACMPCA::Permission
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_acmpca import mixins as acmpca_mixins
        
        cfn_permission_props_mixin = acmpca_mixins.CfnPermissionPropsMixin(acmpca_mixins.CfnPermissionMixinProps(
            actions=["actions"],
            certificate_authority_arn="certificateAuthorityArn",
            principal="principal",
            source_account="sourceAccount"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::ACMPCA::Permission``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c24f3cdae88103a5361499c4fbae96cc3c7efeaeae86b1c6aa5f6171e88fc94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eea39dbc4fc2300593b5adffdaa5e6cfbf06a1b0997cb20b19e23dac9f6d4f48)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f510a95a4303d24b69cdbbdb8789151a7ceda649e4fa9b9dfe49dc146a3644d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPermissionMixinProps:
        return typing.cast(CfnPermissionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnCertificateAuthorityActivationMixinProps",
    "CfnCertificateAuthorityActivationPropsMixin",
    "CfnCertificateAuthorityMixinProps",
    "CfnCertificateAuthorityPropsMixin",
    "CfnCertificateMixinProps",
    "CfnCertificatePropsMixin",
    "CfnPermissionMixinProps",
    "CfnPermissionPropsMixin",
]

publication.publish()

def _typecheckingstub__dbf9dbfa8af5910b9821e9dc872e374ebc7d7e0f92617d0b86526de83ff593c3(
    *,
    certificate: typing.Optional[builtins.str] = None,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4acc1e0b7336eefbc5d0133b3f5477772a2bbff37d7fd2296f1dee7533fa32d(
    props: typing.Union[CfnCertificateAuthorityActivationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae333ce3f4c74b66e4960302c2090c605006bdc42896bad534beaeaad864c04a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78287dd4c2e73c9adf438d23116764b167aaef5b67f0ca4e64637bc3b99d23f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a77a7dfaa4b57460f4186d70378987e5878b6f8a02976ed22505743eb48390d(
    *,
    csr_extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.CsrExtensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_algorithm: typing.Optional[builtins.str] = None,
    key_storage_security_standard: typing.Optional[builtins.str] = None,
    revocation_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.RevocationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    signing_algorithm: typing.Optional[builtins.str] = None,
    subject: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    usage_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b409b4e92d242217582e134a83287e6e2393d92e8fe1bff0ac717568710a5381(
    props: typing.Union[CfnCertificateAuthorityMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ef9833d9d84b12e48eea999e394bc89efe7998b2beecf2dd2a4712a73d8d1df(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fed528f8137b7fe1b044d37929e52755769a342efd52c24a6a78a5c359fdb398(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7992c9e6f1198106308b4e4c67cc64ad122a4c11245fae91c83342fdc0b4309(
    *,
    access_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.GeneralNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    access_method: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.AccessMethodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__782ee5f838c15a764ed3396c9e761126b184826c05c19f5119f12acd10b4f435(
    *,
    access_method_type: typing.Optional[builtins.str] = None,
    custom_object_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967dfb0f153d649ebd2b778f2341d704c360fd34087f8ba08e7b4dff6adf1aea(
    *,
    crl_distribution_point_extension_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.CrlDistributionPointExtensionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    crl_type: typing.Optional[builtins.str] = None,
    custom_cname: typing.Optional[builtins.str] = None,
    custom_path: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    expiration_in_days: typing.Optional[jsii.Number] = None,
    s3_bucket_name: typing.Optional[builtins.str] = None,
    s3_object_acl: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5607361104159196c91cb191e7e28592c0ae4a0e23fe166b4cca7296fa38d45(
    *,
    omit_extension: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7541f697f70cd36aa3de411eef934fc157dc15545a65d7ccdf4e24abc559eb52(
    *,
    key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_information_access: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.AccessDescriptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90f6eee84dc75e8a2ba80cd3ff4791447912a759e6d3258ff2773716d69e2ef(
    *,
    object_identifier: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79a0fbafc36191cfda515db5e6c05321c3016e8e103cc74610150052db35b81(
    *,
    name_assigner: typing.Optional[builtins.str] = None,
    party_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2299b488a143d9fe92d473443cb79f8ecb1cf679258faf7003343cccc08975(
    *,
    directory_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dns_name: typing.Optional[builtins.str] = None,
    edi_party_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.EdiPartyNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    other_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.OtherNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    registered_id: typing.Optional[builtins.str] = None,
    rfc822_name: typing.Optional[builtins.str] = None,
    uniform_resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f2b6b4a4d1b3d7eba5010cc5f45b4e010daabe3f82704339fe206a969ac7312(
    *,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a679d493bc7bb1fefbc08f2cb7790180a8977ad8d789359801e0c8247c3c537(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ocsp_custom_cname: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdec9bc050eb1acd991c5c5a06553a5cee257ab6e7ba59ef19e7e09b8ff6b668(
    *,
    type_id: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9445ab5edcd58d1fab896ba2f3beb27bee2b4987158248a97ada7deb44b62ff8(
    *,
    crl_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.CrlConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ocsp_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.OcspConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b8ea4ff185f94eb7fe81c26a6cd6307c5777ecd02d25a45ca20bea4e3d87e49(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificateAuthorityPropsMixin.CustomAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    distinguished_name_qualifier: typing.Optional[builtins.str] = None,
    generation_qualifier: typing.Optional[builtins.str] = None,
    given_name: typing.Optional[builtins.str] = None,
    initials: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    pseudonym: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b2aa01a0efb1d981bda21f6cf09c7f9544005051db8d0bedd624ce4163858e(
    *,
    api_passthrough: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.ApiPassthroughProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    certificate_signing_request: typing.Optional[builtins.str] = None,
    signing_algorithm: typing.Optional[builtins.str] = None,
    template_arn: typing.Optional[builtins.str] = None,
    validity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.ValidityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    validity_not_before: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.ValidityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad98aa5ffc29494da6343a840ce4f26e4fa9a635e1ecf44e1ae5a1bea2bd8bd4(
    props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0c5928c375d66f606b11c2e88d6477cfd1f8737f8177f214def5b4841256f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37bdd78c283ce1dd2f7c66b24785f693e88a2fec67f60b075a3c25653b080e44(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bfed5bfc1d347ba82e966d471846ea6f479a344cc425c1665d4cb585084ed1(
    *,
    extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.ExtensionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4ac75c5153c7364402cdf080ec0444a2e7a2f8e6d8a5fc231cebb56fd034751(
    *,
    object_identifier: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d8729f120d68ecf0dd00bda6df43f1d9e4154206d9080f9ced5b5c8bebf5fa(
    *,
    critical: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    object_identifier: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6dab4aefd4e414c78ac40fe49ccb15d02c93d1bc5cb4c98ce53c28cffe392d4(
    *,
    name_assigner: typing.Optional[builtins.str] = None,
    party_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cc3aca4a6c2b95c0c64ae256537b0d183eb75c8ec0e25fa59fc4b1a4552224(
    *,
    extended_key_usage_object_identifier: typing.Optional[builtins.str] = None,
    extended_key_usage_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ab952e881b5da71e8f9c1c22b5244144bd7edd18d53b7d0feac6636a16c5cb(
    *,
    certificate_policies: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.PolicyInformationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    custom_extensions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.CustomExtensionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    extended_key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.ExtendedKeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    key_usage: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.KeyUsageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    subject_alternative_names: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.GeneralNameProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d20a57c567bdd27764bca4df52417b5fac623980db3e755dde53ac608ca318(
    *,
    directory_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.SubjectProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dns_name: typing.Optional[builtins.str] = None,
    edi_party_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.EdiPartyNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    other_name: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.OtherNameProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    registered_id: typing.Optional[builtins.str] = None,
    rfc822_name: typing.Optional[builtins.str] = None,
    uniform_resource_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5a22f58704b045d5ec98993b08e2a77d4e21db93b3558bcdb1e8656935a83e7(
    *,
    crl_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    decipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    digital_signature: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encipher_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_agreement: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_cert_sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_encipherment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    non_repudiation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0554e8dc9895d271e74953b5a6fdd1c54d9bfd89eed420767bd0db7eefa39d16(
    *,
    type_id: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b99b31b0888daa7926f2c6eecb517a63139a9bbe2ce406b190af2b368a7ef96b(
    *,
    cert_policy_id: typing.Optional[builtins.str] = None,
    policy_qualifiers: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.PolicyQualifierInfoProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fcb27af89b7c2eba37cb7bbb250795786f9127fb8eaff885ef5d44d69b1acf2(
    *,
    policy_qualifier_id: typing.Optional[builtins.str] = None,
    qualifier: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.QualifierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fe45ada088b088b33106d1ffc0689334ffc78fe27f2b684349cf96a12b06b1(
    *,
    cps_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1c1a736d9342ed3dc813070ed52ed1552792c8b34ca61cb4a59fbbc2411fb3(
    *,
    common_name: typing.Optional[builtins.str] = None,
    country: typing.Optional[builtins.str] = None,
    custom_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.CustomAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    distinguished_name_qualifier: typing.Optional[builtins.str] = None,
    generation_qualifier: typing.Optional[builtins.str] = None,
    given_name: typing.Optional[builtins.str] = None,
    initials: typing.Optional[builtins.str] = None,
    locality: typing.Optional[builtins.str] = None,
    organization: typing.Optional[builtins.str] = None,
    organizational_unit: typing.Optional[builtins.str] = None,
    pseudonym: typing.Optional[builtins.str] = None,
    serial_number: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    surname: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3521f44fd13d3e3f96a152cf1a752cf909a3e00621751114a48ff5761a6db8(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7952727bf88a60fc9d96368bbef3d142142b483809bafecd24f19e4715bf6b1a(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    principal: typing.Optional[builtins.str] = None,
    source_account: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c24f3cdae88103a5361499c4fbae96cc3c7efeaeae86b1c6aa5f6171e88fc94(
    props: typing.Union[CfnPermissionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea39dbc4fc2300593b5adffdaa5e6cfbf06a1b0997cb20b19e23dac9f6d4f48(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f510a95a4303d24b69cdbbdb8789151a7ceda649e4fa9b9dfe49dc146a3644d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
