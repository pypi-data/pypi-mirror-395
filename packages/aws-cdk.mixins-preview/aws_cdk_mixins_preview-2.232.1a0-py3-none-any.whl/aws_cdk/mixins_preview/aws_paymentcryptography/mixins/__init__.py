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
    jsii_type="@aws-cdk/mixins-preview.aws_paymentcryptography.mixins.CfnAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName", "key_arn": "keyArn"},
)
class CfnAliasMixinProps:
    def __init__(
        self,
        *,
        alias_name: typing.Optional[builtins.str] = None,
        key_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAliasPropsMixin.

        :param alias_name: A friendly name that you can use to refer to a key. The value must begin with ``alias/`` . .. epigraph:: Do not include confidential or sensitive information in this field. This field may be displayed in plaintext in AWS CloudTrail logs and other output.
        :param key_arn: The ``KeyARN`` of the key associated with the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-alias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_paymentcryptography import mixins as paymentcryptography_mixins
            
            cfn_alias_mixin_props = paymentcryptography_mixins.CfnAliasMixinProps(
                alias_name="aliasName",
                key_arn="keyArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50c99ac458b0a2c05039b7cc2980ae069b910659f720080236d678bc497d1d7)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if key_arn is not None:
            self._values["key_arn"] = key_arn

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''A friendly name that you can use to refer to a key. The value must begin with ``alias/`` .

        .. epigraph::

           Do not include confidential or sensitive information in this field. This field may be displayed in plaintext in AWS CloudTrail logs and other output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-alias.html#cfn-paymentcryptography-alias-aliasname
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_arn(self) -> typing.Optional[builtins.str]:
        '''The ``KeyARN`` of the key associated with the alias.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-alias.html#cfn-paymentcryptography-alias-keyarn
        '''
        result = self._values.get("key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAliasMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAliasPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_paymentcryptography.mixins.CfnAliasPropsMixin",
):
    '''Creates an *alias* , or a friendly name, for an AWS Payment Cryptography key.

    You can use an alias to identify a key in the console and when you call cryptographic operations such as `EncryptData <https://docs.aws.amazon.com/payment-cryptography/latest/DataAPIReference/API_EncryptData.html>`_ or `DecryptData <https://docs.aws.amazon.com/payment-cryptography/latest/DataAPIReference/API_DecryptData.html>`_ .

    You can associate the alias with any key in the same AWS Region . Each alias is associated with only one key at a time, but a key can have multiple aliases. You can't create an alias without a key. The alias must be unique in the account and AWS Region , but you can create another alias with the same name in a different AWS Region .

    To change the key that's associated with the alias, call `UpdateAlias <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_UpdateAlias.html>`_ . To delete the alias, call `DeleteAlias <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_DeleteAlias.html>`_ . These operations don't affect the underlying key. To get the alias that you created, call `ListAliases <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_ListAliases.html>`_ .

    *Cross-account use* : This operation can't be used across different AWS accounts.

    *Related operations:*

    - `DeleteAlias <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_DeleteAlias.html>`_
    - `GetAlias <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_GetAlias.html>`_
    - `ListAliases <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_ListAliases.html>`_
    - `UpdateAlias <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_UpdateAlias.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-alias.html
    :cloudformationResource: AWS::PaymentCryptography::Alias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_paymentcryptography import mixins as paymentcryptography_mixins
        
        cfn_alias_props_mixin = paymentcryptography_mixins.CfnAliasPropsMixin(paymentcryptography_mixins.CfnAliasMixinProps(
            alias_name="aliasName",
            key_arn="keyArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PaymentCryptography::Alias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87b3d7cf29c9eeb1aa846e6ca61ed6ed1879c15dc176317d6d2d4aebfe84b6f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc3070c500ffbbe7d876d3ff1687ded93c23e0e5a0b42a419527fb95696cf664)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08249860c23124f8a25302d85a86fe61c6cf16e0e69ab4c89a3367f2f162d644)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAliasMixinProps:
        return typing.cast(CfnAliasMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_paymentcryptography.mixins.CfnKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "derive_key_usage": "deriveKeyUsage",
        "enabled": "enabled",
        "exportable": "exportable",
        "key_attributes": "keyAttributes",
        "key_check_value_algorithm": "keyCheckValueAlgorithm",
        "tags": "tags",
    },
)
class CfnKeyMixinProps:
    def __init__(
        self,
        *,
        derive_key_usage: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        exportable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKeyPropsMixin.KeyAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        key_check_value_algorithm: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnKeyPropsMixin.

        :param derive_key_usage: The cryptographic usage of an ECDH derived key as deﬁned in section A.5.2 of the TR-31 spec.
        :param enabled: Specifies whether the key is enabled.
        :param exportable: Specifies whether the key is exportable. This data is immutable after the key is created.
        :param key_attributes: The role of the key, the algorithm it supports, and the cryptographic operations allowed with the key. This data is immutable after the key is created.
        :param key_check_value_algorithm: The algorithm that AWS Payment Cryptography uses to calculate the key check value (KCV). It is used to validate the key integrity. For TDES keys, the KCV is computed by encrypting 8 bytes, each with value of zero, with the key to be checked and retaining the 3 highest order bytes of the encrypted result. For AES keys, the KCV is computed using a CMAC algorithm where the input data is 16 bytes of zero and retaining the 3 highest order bytes of the encrypted result.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_paymentcryptography import mixins as paymentcryptography_mixins
            
            cfn_key_mixin_props = paymentcryptography_mixins.CfnKeyMixinProps(
                derive_key_usage="deriveKeyUsage",
                enabled=False,
                exportable=False,
                key_attributes=paymentcryptography_mixins.CfnKeyPropsMixin.KeyAttributesProperty(
                    key_algorithm="keyAlgorithm",
                    key_class="keyClass",
                    key_modes_of_use=paymentcryptography_mixins.CfnKeyPropsMixin.KeyModesOfUseProperty(
                        decrypt=False,
                        derive_key=False,
                        encrypt=False,
                        generate=False,
                        no_restrictions=False,
                        sign=False,
                        unwrap=False,
                        verify=False,
                        wrap=False
                    ),
                    key_usage="keyUsage"
                ),
                key_check_value_algorithm="keyCheckValueAlgorithm",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d453fcbafbd3c11e664fb077da887ea054f463648d711124fe7e8b7c1ca3a4)
            check_type(argname="argument derive_key_usage", value=derive_key_usage, expected_type=type_hints["derive_key_usage"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument exportable", value=exportable, expected_type=type_hints["exportable"])
            check_type(argname="argument key_attributes", value=key_attributes, expected_type=type_hints["key_attributes"])
            check_type(argname="argument key_check_value_algorithm", value=key_check_value_algorithm, expected_type=type_hints["key_check_value_algorithm"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if derive_key_usage is not None:
            self._values["derive_key_usage"] = derive_key_usage
        if enabled is not None:
            self._values["enabled"] = enabled
        if exportable is not None:
            self._values["exportable"] = exportable
        if key_attributes is not None:
            self._values["key_attributes"] = key_attributes
        if key_check_value_algorithm is not None:
            self._values["key_check_value_algorithm"] = key_check_value_algorithm
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def derive_key_usage(self) -> typing.Optional[builtins.str]:
        '''The cryptographic usage of an ECDH derived key as deﬁned in section A.5.2 of the TR-31 spec.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html#cfn-paymentcryptography-key-derivekeyusage
        '''
        result = self._values.get("derive_key_usage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the key is enabled.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html#cfn-paymentcryptography-key-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def exportable(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the key is exportable.

        This data is immutable after the key is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html#cfn-paymentcryptography-key-exportable
        '''
        result = self._values.get("exportable")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def key_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKeyPropsMixin.KeyAttributesProperty"]]:
        '''The role of the key, the algorithm it supports, and the cryptographic operations allowed with the key.

        This data is immutable after the key is created.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html#cfn-paymentcryptography-key-keyattributes
        '''
        result = self._values.get("key_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKeyPropsMixin.KeyAttributesProperty"]], result)

    @builtins.property
    def key_check_value_algorithm(self) -> typing.Optional[builtins.str]:
        '''The algorithm that AWS Payment Cryptography uses to calculate the key check value (KCV).

        It is used to validate the key integrity.

        For TDES keys, the KCV is computed by encrypting 8 bytes, each with value of zero, with the key to be checked and retaining the 3 highest order bytes of the encrypted result. For AES keys, the KCV is computed using a CMAC algorithm where the input data is 16 bytes of zero and retaining the 3 highest order bytes of the encrypted result.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html#cfn-paymentcryptography-key-keycheckvaluealgorithm
        '''
        result = self._values.get("key_check_value_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html#cfn-paymentcryptography-key-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_paymentcryptography.mixins.CfnKeyPropsMixin",
):
    '''Creates an AWS Payment Cryptography key, a logical representation of a cryptographic key, that is unique in your account and AWS Region .

    You use keys for cryptographic functions such as encryption and decryption.

    In addition to the key material used in cryptographic operations, an AWS Payment Cryptography key includes metadata such as the key ARN, key usage, key origin, creation date, description, and key state.

    When you create a key, you specify both immutable and mutable data about the key. The immutable data contains key attributes that define the scope and cryptographic operations that you can perform using the key, for example key class (example: ``SYMMETRIC_KEY`` ), key algorithm (example: ``TDES_2KEY`` ), key usage (example: ``TR31_P0_PIN_ENCRYPTION_KEY`` ) and key modes of use (example: ``Encrypt`` ). AWS Payment Cryptography binds key attributes to keys using key blocks when you store or export them. AWS Payment Cryptography stores the key contents wrapped and never stores or transmits them in the clear.

    For information about valid combinations of key attributes, see `Understanding key attributes <https://docs.aws.amazon.com/payment-cryptography/latest/userguide/keys-validattributes.html>`_ in the *AWS Payment Cryptography User Guide* . The mutable data contained within a key includes usage timestamp and key deletion timestamp and can be modified after creation.

    You can use the ``CreateKey`` operation to generate an ECC (Elliptic Curve Cryptography) key pair used for establishing an ECDH (Elliptic Curve Diffie-Hellman) key agreement between two parties. In the ECDH key agreement process, both parties generate their own ECC key pair with key usage K3 and exchange the public keys. Each party then use their private key, the received public key from the other party, and the key derivation parameters including key derivation function, hash algorithm, derivation data, and key algorithm to derive a shared key.

    To maintain the single-use principle of cryptographic keys in payments, ECDH derived keys should not be used for multiple purposes, such as a ``TR31_P0_PIN_ENCRYPTION_KEY`` and ``TR31_K1_KEY_BLOCK_PROTECTION_KEY`` . When creating ECC key pairs in AWS Payment Cryptography you can optionally set the ``DeriveKeyUsage`` parameter, which defines the key usage bound to the symmetric key that will be derived using the ECC key pair.

    *Cross-account use* : This operation can't be used across different AWS accounts.

    *Related operations:*

    - `DeleteKey <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_DeleteKey.html>`_
    - `GetKey <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_GetKey.html>`_
    - `ListKeys <https://docs.aws.amazon.com/payment-cryptography/latest/APIReference/API_ListKeys.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-paymentcryptography-key.html
    :cloudformationResource: AWS::PaymentCryptography::Key
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_paymentcryptography import mixins as paymentcryptography_mixins
        
        cfn_key_props_mixin = paymentcryptography_mixins.CfnKeyPropsMixin(paymentcryptography_mixins.CfnKeyMixinProps(
            derive_key_usage="deriveKeyUsage",
            enabled=False,
            exportable=False,
            key_attributes=paymentcryptography_mixins.CfnKeyPropsMixin.KeyAttributesProperty(
                key_algorithm="keyAlgorithm",
                key_class="keyClass",
                key_modes_of_use=paymentcryptography_mixins.CfnKeyPropsMixin.KeyModesOfUseProperty(
                    decrypt=False,
                    derive_key=False,
                    encrypt=False,
                    generate=False,
                    no_restrictions=False,
                    sign=False,
                    unwrap=False,
                    verify=False,
                    wrap=False
                ),
                key_usage="keyUsage"
            ),
            key_check_value_algorithm="keyCheckValueAlgorithm",
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
        props: typing.Union[CfnKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::PaymentCryptography::Key``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7adef184889ea661d4af86d9c596c489c7a0f2fb1d2e36e26e8698d4a5ccd0c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b177817028110ac0b977ec0770a1847f019068b5d3596ca18f4ebc02d7adb19)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd04f7c45fa24d41c4e0bf438ccf5b3d04d42a24ee3c67da7ab806fbdec3e919)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnKeyMixinProps:
        return typing.cast(CfnKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_paymentcryptography.mixins.CfnKeyPropsMixin.KeyAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "key_algorithm": "keyAlgorithm",
            "key_class": "keyClass",
            "key_modes_of_use": "keyModesOfUse",
            "key_usage": "keyUsage",
        },
    )
    class KeyAttributesProperty:
        def __init__(
            self,
            *,
            key_algorithm: typing.Optional[builtins.str] = None,
            key_class: typing.Optional[builtins.str] = None,
            key_modes_of_use: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnKeyPropsMixin.KeyModesOfUseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            key_usage: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The role of the key, the algorithm it supports, and the cryptographic operations allowed with the key.

            This data is immutable after the key is created.

            :param key_algorithm: The key algorithm to be use during creation of an AWS Payment Cryptography key. For symmetric keys, AWS Payment Cryptography supports ``AES`` and ``TDES`` algorithms. For asymmetric keys, AWS Payment Cryptography supports ``RSA`` and ``ECC_NIST`` algorithms.
            :param key_class: The type of AWS Payment Cryptography key to create, which determines the classiﬁcation of the cryptographic method and whether AWS Payment Cryptography key contains a symmetric key or an asymmetric key pair.
            :param key_modes_of_use: The list of cryptographic operations that you can perform using the key.
            :param key_usage: The cryptographic usage of an AWS Payment Cryptography key as deﬁned in section A.5.2 of the TR-31 spec.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keyattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_paymentcryptography import mixins as paymentcryptography_mixins
                
                key_attributes_property = paymentcryptography_mixins.CfnKeyPropsMixin.KeyAttributesProperty(
                    key_algorithm="keyAlgorithm",
                    key_class="keyClass",
                    key_modes_of_use=paymentcryptography_mixins.CfnKeyPropsMixin.KeyModesOfUseProperty(
                        decrypt=False,
                        derive_key=False,
                        encrypt=False,
                        generate=False,
                        no_restrictions=False,
                        sign=False,
                        unwrap=False,
                        verify=False,
                        wrap=False
                    ),
                    key_usage="keyUsage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__788d01893ee99e59f9f4a4ab05c2c3a1b617f63760cf0546c1c1be5fdc5e61ef)
                check_type(argname="argument key_algorithm", value=key_algorithm, expected_type=type_hints["key_algorithm"])
                check_type(argname="argument key_class", value=key_class, expected_type=type_hints["key_class"])
                check_type(argname="argument key_modes_of_use", value=key_modes_of_use, expected_type=type_hints["key_modes_of_use"])
                check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key_algorithm is not None:
                self._values["key_algorithm"] = key_algorithm
            if key_class is not None:
                self._values["key_class"] = key_class
            if key_modes_of_use is not None:
                self._values["key_modes_of_use"] = key_modes_of_use
            if key_usage is not None:
                self._values["key_usage"] = key_usage

        @builtins.property
        def key_algorithm(self) -> typing.Optional[builtins.str]:
            '''The key algorithm to be use during creation of an AWS Payment Cryptography key.

            For symmetric keys, AWS Payment Cryptography supports ``AES`` and ``TDES`` algorithms. For asymmetric keys, AWS Payment Cryptography supports ``RSA`` and ``ECC_NIST`` algorithms.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keyattributes.html#cfn-paymentcryptography-key-keyattributes-keyalgorithm
            '''
            result = self._values.get("key_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_class(self) -> typing.Optional[builtins.str]:
            '''The type of AWS Payment Cryptography key to create, which determines the classiﬁcation of the cryptographic method and whether AWS Payment Cryptography key contains a symmetric key or an asymmetric key pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keyattributes.html#cfn-paymentcryptography-key-keyattributes-keyclass
            '''
            result = self._values.get("key_class")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_modes_of_use(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKeyPropsMixin.KeyModesOfUseProperty"]]:
            '''The list of cryptographic operations that you can perform using the key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keyattributes.html#cfn-paymentcryptography-key-keyattributes-keymodesofuse
            '''
            result = self._values.get("key_modes_of_use")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnKeyPropsMixin.KeyModesOfUseProperty"]], result)

        @builtins.property
        def key_usage(self) -> typing.Optional[builtins.str]:
            '''The cryptographic usage of an AWS Payment Cryptography key as deﬁned in section A.5.2 of the TR-31 spec.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keyattributes.html#cfn-paymentcryptography-key-keyattributes-keyusage
            '''
            result = self._values.get("key_usage")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_paymentcryptography.mixins.CfnKeyPropsMixin.KeyModesOfUseProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decrypt": "decrypt",
            "derive_key": "deriveKey",
            "encrypt": "encrypt",
            "generate": "generate",
            "no_restrictions": "noRestrictions",
            "sign": "sign",
            "unwrap": "unwrap",
            "verify": "verify",
            "wrap": "wrap",
        },
    )
    class KeyModesOfUseProperty:
        def __init__(
            self,
            *,
            decrypt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            derive_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            encrypt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            generate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            no_restrictions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            unwrap: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            verify: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            wrap: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''The list of cryptographic operations that you can perform using the key.

            The modes of use are deﬁned in section A.5.3 of the TR-31 spec.

            :param decrypt: Speciﬁes whether an AWS Payment Cryptography key can be used to decrypt data. Default: - false
            :param derive_key: Speciﬁes whether an AWS Payment Cryptography key can be used to derive new keys. Default: - false
            :param encrypt: Speciﬁes whether an AWS Payment Cryptography key can be used to encrypt data. Default: - false
            :param generate: Speciﬁes whether an AWS Payment Cryptography key can be used to generate and verify other card and PIN verification keys. Default: - false
            :param no_restrictions: Speciﬁes whether an AWS Payment Cryptography key has no special restrictions other than the restrictions implied by ``KeyUsage`` . Default: - false
            :param sign: Speciﬁes whether an AWS Payment Cryptography key can be used for signing. Default: - false
            :param unwrap: Default: - false
            :param verify: Speciﬁes whether an AWS Payment Cryptography key can be used to verify signatures. Default: - false
            :param wrap: Speciﬁes whether an AWS Payment Cryptography key can be used to wrap other keys. Default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_paymentcryptography import mixins as paymentcryptography_mixins
                
                key_modes_of_use_property = paymentcryptography_mixins.CfnKeyPropsMixin.KeyModesOfUseProperty(
                    decrypt=False,
                    derive_key=False,
                    encrypt=False,
                    generate=False,
                    no_restrictions=False,
                    sign=False,
                    unwrap=False,
                    verify=False,
                    wrap=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__901170d1eabaa5bc7e63baac6e1c9556b3c4a0df16164ce8721e9ee90787a013)
                check_type(argname="argument decrypt", value=decrypt, expected_type=type_hints["decrypt"])
                check_type(argname="argument derive_key", value=derive_key, expected_type=type_hints["derive_key"])
                check_type(argname="argument encrypt", value=encrypt, expected_type=type_hints["encrypt"])
                check_type(argname="argument generate", value=generate, expected_type=type_hints["generate"])
                check_type(argname="argument no_restrictions", value=no_restrictions, expected_type=type_hints["no_restrictions"])
                check_type(argname="argument sign", value=sign, expected_type=type_hints["sign"])
                check_type(argname="argument unwrap", value=unwrap, expected_type=type_hints["unwrap"])
                check_type(argname="argument verify", value=verify, expected_type=type_hints["verify"])
                check_type(argname="argument wrap", value=wrap, expected_type=type_hints["wrap"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decrypt is not None:
                self._values["decrypt"] = decrypt
            if derive_key is not None:
                self._values["derive_key"] = derive_key
            if encrypt is not None:
                self._values["encrypt"] = encrypt
            if generate is not None:
                self._values["generate"] = generate
            if no_restrictions is not None:
                self._values["no_restrictions"] = no_restrictions
            if sign is not None:
                self._values["sign"] = sign
            if unwrap is not None:
                self._values["unwrap"] = unwrap
            if verify is not None:
                self._values["verify"] = verify
            if wrap is not None:
                self._values["wrap"] = wrap

        @builtins.property
        def decrypt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used to decrypt data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-decrypt
            '''
            result = self._values.get("decrypt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def derive_key(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used to derive new keys.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-derivekey
            '''
            result = self._values.get("derive_key")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def encrypt(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used to encrypt data.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-encrypt
            '''
            result = self._values.get("encrypt")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def generate(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used to generate and verify other card and PIN verification keys.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-generate
            '''
            result = self._values.get("generate")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def no_restrictions(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key has no special restrictions other than the restrictions implied by ``KeyUsage`` .

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-norestrictions
            '''
            result = self._values.get("no_restrictions")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sign(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used for signing.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-sign
            '''
            result = self._values.get("sign")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def unwrap(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''
            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-unwrap
            '''
            result = self._values.get("unwrap")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def verify(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used to verify signatures.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-verify
            '''
            result = self._values.get("verify")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def wrap(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Speciﬁes whether an AWS Payment Cryptography key can be used to wrap other keys.

            :default: - false

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-paymentcryptography-key-keymodesofuse.html#cfn-paymentcryptography-key-keymodesofuse-wrap
            '''
            result = self._values.get("wrap")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KeyModesOfUseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAliasMixinProps",
    "CfnAliasPropsMixin",
    "CfnKeyMixinProps",
    "CfnKeyPropsMixin",
]

publication.publish()

def _typecheckingstub__b50c99ac458b0a2c05039b7cc2980ae069b910659f720080236d678bc497d1d7(
    *,
    alias_name: typing.Optional[builtins.str] = None,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87b3d7cf29c9eeb1aa846e6ca61ed6ed1879c15dc176317d6d2d4aebfe84b6f3(
    props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3070c500ffbbe7d876d3ff1687ded93c23e0e5a0b42a419527fb95696cf664(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08249860c23124f8a25302d85a86fe61c6cf16e0e69ab4c89a3367f2f162d644(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d453fcbafbd3c11e664fb077da887ea054f463648d711124fe7e8b7c1ca3a4(
    *,
    derive_key_usage: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    exportable: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKeyPropsMixin.KeyAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_check_value_algorithm: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7adef184889ea661d4af86d9c596c489c7a0f2fb1d2e36e26e8698d4a5ccd0c7(
    props: typing.Union[CfnKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b177817028110ac0b977ec0770a1847f019068b5d3596ca18f4ebc02d7adb19(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd04f7c45fa24d41c4e0bf438ccf5b3d04d42a24ee3c67da7ab806fbdec3e919(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788d01893ee99e59f9f4a4ab05c2c3a1b617f63760cf0546c1c1be5fdc5e61ef(
    *,
    key_algorithm: typing.Optional[builtins.str] = None,
    key_class: typing.Optional[builtins.str] = None,
    key_modes_of_use: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnKeyPropsMixin.KeyModesOfUseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    key_usage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901170d1eabaa5bc7e63baac6e1c9556b3c4a0df16164ce8721e9ee90787a013(
    *,
    decrypt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    derive_key: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    encrypt: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    generate: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    no_restrictions: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sign: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    unwrap: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    verify: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    wrap: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass
