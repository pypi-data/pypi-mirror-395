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
    jsii_type="@aws-cdk/mixins-preview.aws_certificatemanager.mixins.CfnAccountMixinProps",
    jsii_struct_bases=[],
    name_mapping={"expiry_events_configuration": "expiryEventsConfiguration"},
)
class CfnAccountMixinProps:
    def __init__(
        self,
        *,
        expiry_events_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAccountPropsMixin.ExpiryEventsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAccountPropsMixin.

        :param expiry_events_configuration: Object containing expiration events options associated with an AWS account . For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_certificatemanager import mixins as certificatemanager_mixins
            
            cfn_account_mixin_props = certificatemanager_mixins.CfnAccountMixinProps(
                expiry_events_configuration=certificatemanager_mixins.CfnAccountPropsMixin.ExpiryEventsConfigurationProperty(
                    days_before_expiry=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5021daa81844fb97d05ae20e3e5446ee97c7bfa83b6b4d3bf6185303d853da)
            check_type(argname="argument expiry_events_configuration", value=expiry_events_configuration, expected_type=type_hints["expiry_events_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if expiry_events_configuration is not None:
            self._values["expiry_events_configuration"] = expiry_events_configuration

    @builtins.property
    def expiry_events_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccountPropsMixin.ExpiryEventsConfigurationProperty"]]:
        '''Object containing expiration events options associated with an AWS account .

        For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html#cfn-certificatemanager-account-expiryeventsconfiguration
        '''
        result = self._values.get("expiry_events_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAccountPropsMixin.ExpiryEventsConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccountMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAccountPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_certificatemanager.mixins.CfnAccountPropsMixin",
):
    '''The ``AWS::CertificateManager::Account`` resource defines the expiry event configuration that determines the number of days prior to expiry when ACM starts generating EventBridge events.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-account.html
    :cloudformationResource: AWS::CertificateManager::Account
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_certificatemanager import mixins as certificatemanager_mixins
        
        cfn_account_props_mixin = certificatemanager_mixins.CfnAccountPropsMixin(certificatemanager_mixins.CfnAccountMixinProps(
            expiry_events_configuration=certificatemanager_mixins.CfnAccountPropsMixin.ExpiryEventsConfigurationProperty(
                days_before_expiry=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CertificateManager::Account``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb0d62c722383d62a390c1d842806592de7e685d15548ff0ed082d1c1738486)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c831530f38e8c253eaccb5593f8fff585c3861d88caffa249ace641325fd5b78)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843149febfcfd4efc6013a59365bc53562bcc4614c5db7a644aa29dccffa4bac)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAccountMixinProps:
        return typing.cast(CfnAccountMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_certificatemanager.mixins.CfnAccountPropsMixin.ExpiryEventsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"days_before_expiry": "daysBeforeExpiry"},
    )
    class ExpiryEventsConfigurationProperty:
        def __init__(
            self,
            *,
            days_before_expiry: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Object containing expiration events options associated with an AWS account .

            For more information, see `ExpiryEventsConfiguration <https://docs.aws.amazon.com/acm/latest/APIReference/API_ExpiryEventsConfiguration.html>`_ in the API reference.

            :param days_before_expiry: This option specifies the number of days prior to certificate expiration when ACM starts generating ``EventBridge`` events. ACM sends one event per day per certificate until the certificate expires. By default, accounts receive events starting 45 days before certificate expiration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-account-expiryeventsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_certificatemanager import mixins as certificatemanager_mixins
                
                expiry_events_configuration_property = certificatemanager_mixins.CfnAccountPropsMixin.ExpiryEventsConfigurationProperty(
                    days_before_expiry=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ed1081d5995edbffa277312e5e3c2b97e72a56a56d0e378541a325d988b93fa)
                check_type(argname="argument days_before_expiry", value=days_before_expiry, expected_type=type_hints["days_before_expiry"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if days_before_expiry is not None:
                self._values["days_before_expiry"] = days_before_expiry

        @builtins.property
        def days_before_expiry(self) -> typing.Optional[jsii.Number]:
            '''This option specifies the number of days prior to certificate expiration when ACM starts generating ``EventBridge`` events.

            ACM sends one event per day per certificate until the certificate expires. By default, accounts receive events starting 45 days before certificate expiration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-account-expiryeventsconfiguration.html#cfn-certificatemanager-account-expiryeventsconfiguration-daysbeforeexpiry
            '''
            result = self._values.get("days_before_expiry")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExpiryEventsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_certificatemanager.mixins.CfnCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_authority_arn": "certificateAuthorityArn",
        "certificate_export": "certificateExport",
        "certificate_transparency_logging_preference": "certificateTransparencyLoggingPreference",
        "domain_name": "domainName",
        "domain_validation_options": "domainValidationOptions",
        "key_algorithm": "keyAlgorithm",
        "subject_alternative_names": "subjectAlternativeNames",
        "tags": "tags",
        "validation_method": "validationMethod",
    },
)
class CfnCertificateMixinProps:
    def __init__(
        self,
        *,
        certificate_authority_arn: typing.Optional[builtins.str] = None,
        certificate_export: typing.Optional[builtins.str] = None,
        certificate_transparency_logging_preference: typing.Optional[builtins.str] = None,
        domain_name: typing.Optional[builtins.str] = None,
        domain_validation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnCertificatePropsMixin.DomainValidationOptionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        key_algorithm: typing.Optional[builtins.str] = None,
        subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        validation_method: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCertificatePropsMixin.

        :param certificate_authority_arn: The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate. If you do not provide an ARN and you are trying to request a private certificate, ACM will attempt to issue a public certificate. For more information about private CAs, see the `AWS Private Certificate Authority <https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html>`_ user guide. The ARN must have the following form: ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``
        :param certificate_export: You can opt out of allowing export of your certificate by specifying the ``DISABLED`` option. Allow export of your certificate by specifying the ``ENABLED`` option. If you do not specify an export preference in a new CloudFormation template, it is the same as explicitly denying export of your certificate.
        :param certificate_transparency_logging_preference: You can opt out of certificate transparency logging by specifying the ``DISABLED`` option. Opt in by specifying ``ENABLED`` . This setting doces not apply to private certificates. If you do not specify a certificate transparency logging preference on a new CloudFormation template, or if you remove the logging preference from an existing template, this is the same as explicitly enabling the preference. Changing the certificate transparency logging preference will update the existing resource by calling ``UpdateCertificateOptions`` on the certificate. This action will not create a new resource.
        :param domain_name: The fully qualified domain name (FQDN), such as www.example.com, with which you want to secure an ACM certificate. Use an asterisk (*) to create a wildcard certificate that protects several sites in the same domain. For example, ``*.example.com`` protects ``www.example.com`` , ``site.example.com`` , and ``images.example.com.``.
        :param domain_validation_options: Domain information that domain name registrars use to verify your identity. .. epigraph:: In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the ``DomainName`` property needs to be identical to one of the ``DomainName`` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.
        :param key_algorithm: Specifies the algorithm of the public and private key pair that your certificate uses to encrypt data. RSA is the default key algorithm for ACM certificates. Elliptic Curve Digital Signature Algorithm (ECDSA) keys are smaller, offering security comparable to RSA keys but with greater computing efficiency. However, ECDSA is not supported by all network clients. Some AWS services may require RSA keys, or only support ECDSA keys of a particular size, while others allow the use of either RSA and ECDSA keys to ensure that compatibility is not broken. Check the requirements for the AWS service where you plan to deploy your certificate. For more information about selecting an algorithm, see `Key algorithms <https://docs.aws.amazon.com/acm/latest/userguide/acm-certificate-characteristics.html#algorithms-term>`_ . .. epigraph:: Algorithms supported for an ACM certificate request include: - ``RSA_2048`` - ``EC_prime256v1`` - ``EC_secp384r1`` Other listed algorithms are for imported certificates only. > When you request a private PKI certificate signed by a CA from AWS Private CA, the specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key. Default: RSA_2048
        :param subject_alternative_names: Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate. For example, you can add www.example.net to a certificate for which the ``DomainName`` field is www.example.com if users can reach your site by using either name.
        :param tags: Key-value pairs that can identify the certificate.
        :param validation_method: The method you want to use to validate that you own or control the domain associated with a public certificate. You can `validate with DNS <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`_ or `validate with email <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html>`_ . We recommend that you use DNS validation. If not specified, this property defaults to email validation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_certificatemanager import mixins as certificatemanager_mixins
            
            cfn_certificate_mixin_props = certificatemanager_mixins.CfnCertificateMixinProps(
                certificate_authority_arn="certificateAuthorityArn",
                certificate_export="certificateExport",
                certificate_transparency_logging_preference="certificateTransparencyLoggingPreference",
                domain_name="domainName",
                domain_validation_options=[certificatemanager_mixins.CfnCertificatePropsMixin.DomainValidationOptionProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId",
                    validation_domain="validationDomain"
                )],
                key_algorithm="keyAlgorithm",
                subject_alternative_names=["subjectAlternativeNames"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                validation_method="validationMethod"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3eeb8d4411f9ae809415d4606fd345e04463cdd9235a725db9df1a04df83d19)
            check_type(argname="argument certificate_authority_arn", value=certificate_authority_arn, expected_type=type_hints["certificate_authority_arn"])
            check_type(argname="argument certificate_export", value=certificate_export, expected_type=type_hints["certificate_export"])
            check_type(argname="argument certificate_transparency_logging_preference", value=certificate_transparency_logging_preference, expected_type=type_hints["certificate_transparency_logging_preference"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument domain_validation_options", value=domain_validation_options, expected_type=type_hints["domain_validation_options"])
            check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
            check_type(argname="argument subject_alternative_names", value=subject_alternative_names, expected_type=type_hints["subject_alternative_names"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument validation_method", value=validation_method, expected_type=type_hints["validation_method"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_authority_arn is not None:
            self._values["certificate_authority_arn"] = certificate_authority_arn
        if certificate_export is not None:
            self._values["certificate_export"] = certificate_export
        if certificate_transparency_logging_preference is not None:
            self._values["certificate_transparency_logging_preference"] = certificate_transparency_logging_preference
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if domain_validation_options is not None:
            self._values["domain_validation_options"] = domain_validation_options
        if key_algorithm is not None:
            self._values["key_algorithm"] = key_algorithm
        if subject_alternative_names is not None:
            self._values["subject_alternative_names"] = subject_alternative_names
        if tags is not None:
            self._values["tags"] = tags
        if validation_method is not None:
            self._values["validation_method"] = validation_method

    @builtins.property
    def certificate_authority_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the private certificate authority (CA) that will be used to issue the certificate.

        If you do not provide an ARN and you are trying to request a private certificate, ACM will attempt to issue a public certificate. For more information about private CAs, see the `AWS Private Certificate Authority <https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html>`_ user guide. The ARN must have the following form:

        ``arn:aws:acm-pca:region:account:certificate-authority/12345678-1234-1234-1234-123456789012``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificateauthorityarn
        '''
        result = self._values.get("certificate_authority_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_export(self) -> typing.Optional[builtins.str]:
        '''You can opt out of allowing export of your certificate by specifying the ``DISABLED`` option.

        Allow export of your certificate by specifying the ``ENABLED`` option.

        If you do not specify an export preference in a new CloudFormation template, it is the same as explicitly denying export of your certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificateexport
        '''
        result = self._values.get("certificate_export")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_transparency_logging_preference(
        self,
    ) -> typing.Optional[builtins.str]:
        '''You can opt out of certificate transparency logging by specifying the ``DISABLED`` option.

        Opt in by specifying ``ENABLED`` . This setting doces not apply to private certificates.

        If you do not specify a certificate transparency logging preference on a new CloudFormation template, or if you remove the logging preference from an existing template, this is the same as explicitly enabling the preference.

        Changing the certificate transparency logging preference will update the existing resource by calling ``UpdateCertificateOptions`` on the certificate. This action will not create a new resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-certificatetransparencyloggingpreference
        '''
        result = self._values.get("certificate_transparency_logging_preference")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''The fully qualified domain name (FQDN), such as www.example.com, with which you want to secure an ACM certificate. Use an asterisk (*) to create a wildcard certificate that protects several sites in the same domain. For example, ``*.example.com`` protects ``www.example.com`` , ``site.example.com`` , and ``images.example.com.``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainname
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_validation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.DomainValidationOptionProperty"]]]]:
        '''Domain information that domain name registrars use to verify your identity.

        .. epigraph::

           In order for a AWS::CertificateManager::Certificate to be provisioned and validated in CloudFormation automatically, the ``DomainName`` property needs to be identical to one of the ``DomainName`` property supplied in DomainValidationOptions, if the ValidationMethod is **DNS**. Failing to keep them like-for-like will result in failure to create the domain validation records in Route53.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-domainvalidationoptions
        '''
        result = self._values.get("domain_validation_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnCertificatePropsMixin.DomainValidationOptionProperty"]]]], result)

    @builtins.property
    def key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Specifies the algorithm of the public and private key pair that your certificate uses to encrypt data.

        RSA is the default key algorithm for ACM certificates. Elliptic Curve Digital Signature Algorithm (ECDSA) keys are smaller, offering security comparable to RSA keys but with greater computing efficiency. However, ECDSA is not supported by all network clients. Some AWS services may require RSA keys, or only support ECDSA keys of a particular size, while others allow the use of either RSA and ECDSA keys to ensure that compatibility is not broken. Check the requirements for the AWS service where you plan to deploy your certificate. For more information about selecting an algorithm, see `Key algorithms <https://docs.aws.amazon.com/acm/latest/userguide/acm-certificate-characteristics.html#algorithms-term>`_ .
        .. epigraph::

           Algorithms supported for an ACM certificate request include:

           - ``RSA_2048``
           - ``EC_prime256v1``
           - ``EC_secp384r1``

           Other listed algorithms are for imported certificates only. > When you request a private PKI certificate signed by a CA from AWS Private CA, the specified signing algorithm family (RSA or ECDSA) must match the algorithm family of the CA's secret key.

        Default: RSA_2048

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-keyalgorithm
        '''
        result = self._values.get("key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subject_alternative_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional FQDNs to be included in the Subject Alternative Name extension of the ACM certificate.

        For example, you can add www.example.net to a certificate for which the ``DomainName`` field is www.example.com if users can reach your site by using either name.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-subjectalternativenames
        '''
        result = self._values.get("subject_alternative_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can identify the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def validation_method(self) -> typing.Optional[builtins.str]:
        '''The method you want to use to validate that you own or control the domain associated with a public certificate.

        You can `validate with DNS <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-dns.html>`_ or `validate with email <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-validate-email.html>`_ . We recommend that you use DNS validation.

        If not specified, this property defaults to email validation.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html#cfn-certificatemanager-certificate-validationmethod
        '''
        result = self._values.get("validation_method")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_certificatemanager.mixins.CfnCertificatePropsMixin",
):
    '''The ``AWS::CertificateManager::Certificate`` resource requests an Certificate Manager ( ACM ) certificate that you can use to enable secure connections.

    For example, you can deploy an ACM certificate to an Elastic Load Balancer to enable HTTPS support. For more information, see `RequestCertificate <https://docs.aws.amazon.com/acm/latest/APIReference/API_RequestCertificate.html>`_ in the Certificate Manager API Reference.
    .. epigraph::

       When you use the ``AWS::CertificateManager::Certificate`` resource in a CloudFormation stack, domain validation is handled automatically if all three of the following are true: The certificate domain is hosted in Amazon Route 53, the domain resides in your AWS account , and you are using DNS validation.

       However, if the certificate uses email validation, or if the domain is not hosted in Route 53, then the stack will remain in the ``CREATE_IN_PROGRESS`` state. Further stack operations are delayed until you validate the certificate request, either by acting upon the instructions in the validation email, or by adding a CNAME record to your DNS configuration. For more information, see `Option 1: DNS Validation <https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html>`_ and `Option 2: Email Validation <https://docs.aws.amazon.com/acm/latest/userguide/email-validation.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html
    :cloudformationResource: AWS::CertificateManager::Certificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_certificatemanager import mixins as certificatemanager_mixins
        
        cfn_certificate_props_mixin = certificatemanager_mixins.CfnCertificatePropsMixin(certificatemanager_mixins.CfnCertificateMixinProps(
            certificate_authority_arn="certificateAuthorityArn",
            certificate_export="certificateExport",
            certificate_transparency_logging_preference="certificateTransparencyLoggingPreference",
            domain_name="domainName",
            domain_validation_options=[certificatemanager_mixins.CfnCertificatePropsMixin.DomainValidationOptionProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId",
                validation_domain="validationDomain"
            )],
            key_algorithm="keyAlgorithm",
            subject_alternative_names=["subjectAlternativeNames"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            validation_method="validationMethod"
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
        '''Create a mixin to apply properties to ``AWS::CertificateManager::Certificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeda1fe8de4a3ba6ef10e4804edccc526f07fa3ba9bb3080b391b7b756c1f8d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4593b3178e50b3babd1cca615a549bc053b8198795085ed828a43827684bb86b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602f4805931d85779193f5f8c8dadeb761fa73419c503f928244c27c8d02d165)
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
        jsii_type="@aws-cdk/mixins-preview.aws_certificatemanager.mixins.CfnCertificatePropsMixin.DomainValidationOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_name": "domainName",
            "hosted_zone_id": "hostedZoneId",
            "validation_domain": "validationDomain",
        },
    )
    class DomainValidationOptionProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
            validation_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''``DomainValidationOption`` is a property of the `AWS::CertificateManager::Certificate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-certificatemanager-certificate.html>`_ resource that specifies the Certificate Manager ( ACM ) certificate domain to validate. Depending on the chosen validation method, ACM checks the domain's DNS record for a validation CNAME, or it attempts to send a validation email message to the domain owner.

            :param domain_name: A fully qualified domain name (FQDN) in the certificate request.
            :param hosted_zone_id: The ``HostedZoneId`` option, which is available if you are using Route 53 as your domain registrar, causes ACM to add your CNAME to the domain record. Your list of ``DomainValidationOptions`` must contain one and only one of the domain-validation options, and the ``HostedZoneId`` can be used only when ``DNS`` is specified as your validation method. Use the Route 53 ``ListHostedZones`` API to discover IDs for available hosted zones. This option is required for publicly trusted certificates. .. epigraph:: The ``ListHostedZones`` API returns IDs in the format "/hostedzone/Z111111QQQQQQQ", but CloudFormation requires the IDs to be in the format "Z111111QQQQQQQ". When you change your ``DomainValidationOptions`` , a new resource is created.
            :param validation_domain: The domain name to which you want ACM to send validation emails. This domain name is the suffix of the email addresses that you want ACM to use. This must be the same as the ``DomainName`` value or a superdomain of the ``DomainName`` value. For example, if you request a certificate for ``testing.example.com`` , you can specify ``example.com`` as this value. In that case, ACM sends domain validation emails to the following five addresses: - admin@example.com - administrator@example.com - hostmaster@example.com - postmaster@example.com - webmaster@example.com

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_certificatemanager import mixins as certificatemanager_mixins
                
                domain_validation_option_property = certificatemanager_mixins.CfnCertificatePropsMixin.DomainValidationOptionProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId",
                    validation_domain="validationDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07b6338f76b85a5421bee7bab0fdde383a3629b1f2d40801b2ec487729bbcaed)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
                check_type(argname="argument validation_domain", value=validation_domain, expected_type=type_hints["validation_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id
            if validation_domain is not None:
                self._values["validation_domain"] = validation_domain

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''A fully qualified domain name (FQDN) in the certificate request.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ``HostedZoneId`` option, which is available if you are using Route 53 as your domain registrar, causes ACM to add your CNAME to the domain record.

            Your list of ``DomainValidationOptions`` must contain one and only one of the domain-validation options, and the ``HostedZoneId`` can be used only when ``DNS`` is specified as your validation method.

            Use the Route 53 ``ListHostedZones`` API to discover IDs for available hosted zones.

            This option is required for publicly trusted certificates.
            .. epigraph::

               The ``ListHostedZones`` API returns IDs in the format "/hostedzone/Z111111QQQQQQQ", but CloudFormation requires the IDs to be in the format "Z111111QQQQQQQ".

            When you change your ``DomainValidationOptions`` , a new resource is created.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def validation_domain(self) -> typing.Optional[builtins.str]:
            '''The domain name to which you want ACM to send validation emails.

            This domain name is the suffix of the email addresses that you want ACM to use. This must be the same as the ``DomainName`` value or a superdomain of the ``DomainName`` value. For example, if you request a certificate for ``testing.example.com`` , you can specify ``example.com`` as this value. In that case, ACM sends domain validation emails to the following five addresses:

            - admin@example.com
            - administrator@example.com
            - hostmaster@example.com
            - postmaster@example.com
            - webmaster@example.com

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-certificatemanager-certificate-domainvalidationoption.html#cfn-certificatemanager-certificate-domainvalidationoption-validationdomain
            '''
            result = self._values.get("validation_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DomainValidationOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAccountMixinProps",
    "CfnAccountPropsMixin",
    "CfnCertificateMixinProps",
    "CfnCertificatePropsMixin",
]

publication.publish()

def _typecheckingstub__8b5021daa81844fb97d05ae20e3e5446ee97c7bfa83b6b4d3bf6185303d853da(
    *,
    expiry_events_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAccountPropsMixin.ExpiryEventsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb0d62c722383d62a390c1d842806592de7e685d15548ff0ed082d1c1738486(
    props: typing.Union[CfnAccountMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c831530f38e8c253eaccb5593f8fff585c3861d88caffa249ace641325fd5b78(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843149febfcfd4efc6013a59365bc53562bcc4614c5db7a644aa29dccffa4bac(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed1081d5995edbffa277312e5e3c2b97e72a56a56d0e378541a325d988b93fa(
    *,
    days_before_expiry: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3eeb8d4411f9ae809415d4606fd345e04463cdd9235a725db9df1a04df83d19(
    *,
    certificate_authority_arn: typing.Optional[builtins.str] = None,
    certificate_export: typing.Optional[builtins.str] = None,
    certificate_transparency_logging_preference: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    domain_validation_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnCertificatePropsMixin.DomainValidationOptionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    key_algorithm: typing.Optional[builtins.str] = None,
    subject_alternative_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    validation_method: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeda1fe8de4a3ba6ef10e4804edccc526f07fa3ba9bb3080b391b7b756c1f8d1(
    props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4593b3178e50b3babd1cca615a549bc053b8198795085ed828a43827684bb86b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602f4805931d85779193f5f8c8dadeb761fa73419c503f928244c27c8d02d165(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07b6338f76b85a5421bee7bab0fdde383a3629b1f2d40801b2ec487729bbcaed(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
    validation_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
