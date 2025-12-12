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
    jsii_type="@aws-cdk/mixins-preview.aws_kms.mixins.CfnAliasMixinProps",
    jsii_struct_bases=[],
    name_mapping={"alias_name": "aliasName", "target_key_id": "targetKeyId"},
)
class CfnAliasMixinProps:
    def __init__(
        self,
        *,
        alias_name: typing.Optional[builtins.str] = None,
        target_key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnAliasPropsMixin.

        :param alias_name: Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias`` . .. epigraph:: If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC). The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/`` . The ``alias/aws/`` prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .
        :param target_key_id: Associates the alias with the specified `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ . The KMS key must be in the same AWS account and Region. A valid key ID is required. If you supply a null or empty string value, this operation returns an error. For help finding the key ID and ARN, see `Finding the key ID and ARN <https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn>`_ in the *AWS Key Management Service Developer Guide* . Specify the key ID or the key ARN of the KMS key. For example: - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` To get the key ID and key ARN for a KMS key, use `ListKeys <https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html>`_ or `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kms import mixins as kms_mixins
            
            cfn_alias_mixin_props = kms_mixins.CfnAliasMixinProps(
                alias_name="aliasName",
                target_key_id="targetKeyId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b791cbc86612400f303349e79b7d4e30901c91bc75150acb2568c1ad677d0af)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument target_key_id", value=target_key_id, expected_type=type_hints["target_key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alias_name is not None:
            self._values["alias_name"] = alias_name
        if target_key_id is not None:
            self._values["target_key_id"] = target_key_id

    @builtins.property
    def alias_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the alias name. This value must begin with ``alias/`` followed by a name, such as ``alias/ExampleAlias`` .

        .. epigraph::

           If you change the value of the ``AliasName`` property, the existing alias is deleted and a new alias is created for the specified KMS key. This change can disrupt applications that use the alias. It can also allow or deny access to a KMS key affected by attribute-based access control (ABAC).

        The alias must be string of 1-256 characters. It can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). The alias name cannot begin with ``alias/aws/`` . The ``alias/aws/`` prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-aliasname
        '''
        result = self._values.get("alias_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_key_id(self) -> typing.Optional[builtins.str]:
        '''Associates the alias with the specified `customer managed key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk>`_ . The KMS key must be in the same AWS account and Region.

        A valid key ID is required. If you supply a null or empty string value, this operation returns an error.

        For help finding the key ID and ARN, see `Finding the key ID and ARN <https://docs.aws.amazon.com/kms/latest/developerguide/viewing-keys.html#find-cmk-id-arn>`_ in the *AWS Key Management Service Developer Guide* .

        Specify the key ID or the key ARN of the KMS key.

        For example:

        - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
        - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``

        To get the key ID and key ARN for a KMS key, use `ListKeys <https://docs.aws.amazon.com/kms/latest/APIReference/API_ListKeys.html>`_ or `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html#cfn-kms-alias-targetkeyid
        '''
        result = self._values.get("target_key_id")
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
    jsii_type="@aws-cdk/mixins-preview.aws_kms.mixins.CfnAliasPropsMixin",
):
    '''The ``AWS::KMS::Alias`` resource specifies a display name for a `KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys>`_ . You can use an alias to identify a KMS key in the AWS  console, in the `DescribeKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DescribeKey.html>`_ operation, and in `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ , such as `Decrypt <https://docs.aws.amazon.com/kms/latest/APIReference/API_Decrypt.html>`_ and `GenerateDataKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_GenerateDataKey.html>`_ .

    .. epigraph::

       Adding, deleting, or updating an alias can allow or deny permission to the KMS key. For details, see `ABAC for AWS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

    Using an alias to refer to a KMS key can help you simplify key management. For example, an alias in your code can be associated with different KMS keys in different AWS Regions . For more information, see `Using aliases <https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html>`_ in the *AWS Key Management Service Developer Guide* .

    When specifying an alias, observe the following rules.

    - Each alias is associated with one KMS key, but multiple aliases can be associated with the same KMS key.
    - The alias and its associated KMS key must be in the same AWS account and Region.
    - The alias name must be unique in the AWS account and Region. However, you can create aliases with the same name in different AWS Regions . For example, you can have an ``alias/projectKey`` in multiple Regions, each of which is associated with a KMS key in its Region.
    - Each alias name must begin with ``alias/`` followed by a name, such as ``alias/exampleKey`` . The alias name can contain only alphanumeric characters, forward slashes (/), underscores (_), and dashes (-). Alias names cannot begin with ``alias/aws/`` . That alias name prefix is reserved for `AWS managed keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#aws-managed-cmk>`_ .

    *Regions*

    AWS  CloudFormation resources are available in all AWS Regions in which AWS  and CloudFormation are supported.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-alias.html
    :cloudformationResource: AWS::KMS::Alias
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kms import mixins as kms_mixins
        
        cfn_alias_props_mixin = kms_mixins.CfnAliasPropsMixin(kms_mixins.CfnAliasMixinProps(
            alias_name="aliasName",
            target_key_id="targetKeyId"
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
        '''Create a mixin to apply properties to ``AWS::KMS::Alias``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d43eab79966d8f362ca012437f1965b66fdd0f3d4f6682be68313171c9cf74)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1077779e7ef506ee71c3f5737b60a72053b6bee83e07bac998d4560eec5c4dc6)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7af15734af6409ec739451ad89fcd9a6efb82dcf6e136a3ec29e532daee7ba5)
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
    jsii_type="@aws-cdk/mixins-preview.aws_kms.mixins.CfnKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "bypass_policy_lockout_safety_check": "bypassPolicyLockoutSafetyCheck",
        "description": "description",
        "enabled": "enabled",
        "enable_key_rotation": "enableKeyRotation",
        "key_policy": "keyPolicy",
        "key_spec": "keySpec",
        "key_usage": "keyUsage",
        "multi_region": "multiRegion",
        "origin": "origin",
        "pending_window_in_days": "pendingWindowInDays",
        "rotation_period_in_days": "rotationPeriodInDays",
        "tags": "tags",
    },
)
class CfnKeyMixinProps:
    def __init__(
        self,
        *,
        bypass_policy_lockout_safety_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        key_policy: typing.Any = None,
        key_spec: typing.Optional[builtins.str] = None,
        key_usage: typing.Optional[builtins.str] = None,
        multi_region: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        origin: typing.Optional[builtins.str] = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        rotation_period_in_days: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnKeyPropsMixin.

        :param bypass_policy_lockout_safety_check: Skips ("bypasses") the key policy lockout safety check. The default value is false. .. epigraph:: Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately. For more information, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html#prevent-unmanageable-key>`_ in the *AWS Key Management Service Developer Guide* . Use this parameter only when you intend to prevent the principal that is making the request from making a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. Default: - false
        :param description: A description of the KMS key. Use a description that helps you to distinguish this KMS key from others in the account, such as its intended use.
        :param enabled: Specifies whether the KMS key is enabled. Disabled KMS keys cannot be used in cryptographic operations. When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` . The actual key state of the KMS key might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param enable_key_rotation: Enables automatic rotation of the key material for the specified KMS key. By default, automatic key rotation is not enabled. AWS supports automatic rotation only for symmetric encryption KMS keys ( ``KeySpec`` = ``SYMMETRIC_DEFAULT`` ). For asymmetric KMS keys, HMAC KMS keys, and KMS keys with Origin ``EXTERNAL`` , omit the ``EnableKeyRotation`` property or set it to ``false`` . To enable automatic key rotation of the key material for a multi-Region KMS key, set ``EnableKeyRotation`` to ``true`` on the primary key (created by using ``AWS::KMS::Key`` ). AWS copies the rotation status to all replica keys. For details, see `Rotating multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-manage.html#multi-region-rotate>`_ in the *AWS Key Management Service Developer Guide* . When you enable automatic rotation, AWS automatically creates new key material for the KMS key one year after the enable date and every year thereafter. AWS retains all key material until you delete the KMS key. For detailed information about automatic key rotation, see `Rotating KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param key_policy: The key policy to attach to the KMS key. If you provide a key policy, it must meet the following criteria: - The key policy must allow the caller to make a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ in the *AWS Key Management Service Developer Guide* . (To omit this condition, set ``BypassPolicyLockoutSafetyCheck`` to true.) - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* . If you do not provide a key policy, AWS attaches a default key policy to the KMS key. For more information, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default>`_ in the *AWS Key Management Service Developer Guide* . A key policy document can include only the following characters: - Printable ASCII characters - Printable characters in the Basic Latin and Latin-1 Supplement character set - The tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` ) special characters *Minimum* : ``1`` *Maximum* : ``32768``
        :param key_spec: Specifies the type of KMS key to create. The default value, ``SYMMETRIC_DEFAULT`` , creates a KMS key with a 256-bit symmetric key for encryption and decryption. In China Regions, ``SYMMETRIC_DEFAULT`` creates a 128-bit symmetric key that uses SM4 encryption. You can't change the ``KeySpec`` value after the KMS key is created. For help choosing a key spec for your KMS key, see `Choosing a KMS key type <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html>`_ in the *AWS Key Management Service Developer Guide* . The ``KeySpec`` property determines the type of key material in the KMS key and the algorithms that the KMS key supports. To further restrict the algorithms that can be used with the KMS key, use a condition key in its key policy or IAM policy. For more information, see `AWS condition keys <https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms>`_ in the *AWS Key Management Service Developer Guide* . .. epigraph:: If you change the value of the ``KeySpec`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. > `AWS services that are integrated with AWS <https://docs.aws.amazon.com/kms/features/#AWS_Service_Integration>`_ use symmetric encryption KMS keys to protect your data. These services do not support encryption with asymmetric KMS keys. For help determining whether a KMS key is asymmetric, see `Identifying asymmetric KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/find-symm-asymm.html>`_ in the *AWS Key Management Service Developer Guide* . AWS supports the following key specs for KMS keys: - Symmetric encryption key (default) - ``SYMMETRIC_DEFAULT`` (AES-256-GCM) - HMAC keys (symmetric) - ``HMAC_224`` - ``HMAC_256`` - ``HMAC_384`` - ``HMAC_512`` - Asymmetric RSA key pairs (encryption and decryption *or* signing and verification) - ``RSA_2048`` - ``RSA_3072`` - ``RSA_4096`` - Asymmetric NIST-recommended elliptic curve key pairs (signing and verification *or* deriving shared secrets) - ``ECC_NIST_P256`` (secp256r1) - ``ECC_NIST_P384`` (secp384r1) - ``ECC_NIST_P521`` (secp521r1) - ``ECC_NIST_EDWARDS25519`` (ed25519) - signing and verification only - *Note:* For ECC_NIST_EDWARDS25519 KMS keys, the ED25519_SHA_512 signing algorithm requires ```MessageType:RAW`` <https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html#KMS-Sign-request-MessageType>`_ , while ED25519_PH_SHA_512 requires ```MessageType:DIGEST`` <https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html#KMS-Sign-request-MessageType>`_ . These message types cannot be used interchangeably. - Other asymmetric elliptic curve key pairs (signing and verification) - ``ECC_SECG_P256K1`` (secp256k1), commonly used for cryptocurrencies. - Asymmetric ML-DSA key pairs (signing and verification) - ``ML_DSA_44`` - ``ML_DSA_65`` - ``ML_DSA_87`` - SM2 key pairs (encryption and decryption *or* signing and verification *or* deriving shared secrets) - ``SM2`` (China Regions only) Default: - "SYMMETRIC_DEFAULT"
        :param key_usage: Determines the `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ for which you can use the KMS key. The default value is ``ENCRYPT_DECRYPT`` . This property is required for asymmetric KMS keys and HMAC KMS keys. You can't change the ``KeyUsage`` value after the KMS key is created. .. epigraph:: If you change the value of the ``KeyUsage`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. Select only one valid value. - For symmetric encryption KMS keys, omit the parameter or specify ``ENCRYPT_DECRYPT`` . - For HMAC KMS keys (symmetric), specify ``GENERATE_VERIFY_MAC`` . - For asymmetric KMS keys with RSA key pairs, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` . - For asymmetric KMS keys with NIST-recommended elliptic curve key pairs, specify ``SIGN_VERIFY`` or ``KEY_AGREEMENT`` . - For asymmetric KMS keys with ``ECC_SECG_P256K1`` key pairs, specify ``SIGN_VERIFY`` . - For asymmetric KMS keys with ML-DSA key pairs, specify ``SIGN_VERIFY`` . - For asymmetric KMS keys with SM2 key pairs (China Regions only), specify ``ENCRYPT_DECRYPT`` , ``SIGN_VERIFY`` , or ``KEY_AGREEMENT`` . Default: - "ENCRYPT_DECRYPT"
        :param multi_region: Creates a multi-Region primary key that you can replicate in other AWS Regions . You can't change the ``MultiRegion`` value after the KMS key is created. For a list of AWS Regions in which multi-Region keys are supported, see `Multi-Region keys in AWS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** . .. epigraph:: If you change the value of the ``MultiRegion`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. For a multi-Region key, set to this property to ``true`` . For a single-Region key, omit this property or set it to ``false`` . The default value is ``false`` . *Multi-Region keys* are an AWS feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* . You can create a symmetric encryption, HMAC, or asymmetric multi-Region KMS key, and you can create a multi-Region key with imported key material. However, you cannot create a multi-Region key in a custom key store. To create a replica of this primary key in a different AWS Region , create an `AWS::KMS::ReplicaKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html>`_ resource in a CloudFormation stack in the replica Region. Specify the key ARN of this primary key. Default: - false
        :param origin: The source of the key material for the KMS key. You cannot change the origin after you create the KMS key. The default is ``AWS_KMS`` , which means that AWS creates the key material. To `create a KMS key with no key material <https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-create-cmk.html>`_ (for imported key material), set this value to ``EXTERNAL`` . For more information about importing key material into AWS , see `Importing Key Material <https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html>`_ in the *AWS Key Management Service Developer Guide* . You can ignore ``ENABLED`` when Origin is ``EXTERNAL`` . When a KMS key with Origin ``EXTERNAL`` is created, the key state is ``PENDING_IMPORT`` and ``ENABLED`` is ``false`` . After you import the key material, ``ENABLED`` updated to ``true`` . The KMS key can then be used for Cryptographic Operations. .. epigraph:: - CloudFormation doesn't support creating an ``Origin`` parameter of the ``AWS_CLOUDHSM`` or ``EXTERNAL_KEY_STORE`` values. - ``EXTERNAL`` is not supported for ML-DSA keys. Default: - "AWS_KMS"
        :param pending_window_in_days: Specifies the number of days in the waiting period before AWS deletes a KMS key that has been removed from a CloudFormation stack. Enter a value between 7 and 30 days. The default value is 30 days. When you remove a KMS key from a CloudFormation stack, AWS schedules the KMS key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of KMS key is ``Pending Deletion`` or ``Pending Replica Deletion`` , which prevents the KMS key from being used in cryptographic operations. When the waiting period expires, AWS permanently deletes the KMS key. AWS will not delete a `multi-Region primary key <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ that has replica keys. If you remove a multi-Region primary key from a CloudFormation stack, its key state changes to ``PendingReplicaDeletion`` so it cannot be replicated or used in cryptographic operations. This state can persist indefinitely. When the last of its replica keys is deleted, the key state of the primary key changes to ``PendingDeletion`` and the waiting period specified by ``PendingWindowInDays`` begins. When this waiting period expires, AWS deletes the primary key. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* . You cannot use a CloudFormation template to cancel deletion of the KMS key after you remove it from the stack, regardless of the waiting period. If you specify a KMS key in your template, even one with the same name, CloudFormation creates a new KMS key. To cancel deletion of a KMS key, use the AWS console or the `CancelKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_CancelKeyDeletion.html>`_ operation. For information about the ``Pending Deletion`` and ``Pending Replica Deletion`` key states, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param rotation_period_in_days: Specifies a custom period of time between each rotation date. If no value is specified, the default value is 365 days. The rotation period defines the number of days after you enable automatic key rotation that AWS will rotate your key material, and the number of days between each automatic rotation thereafter. You can use the ```kms:RotationPeriodInDays`` <https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-rotation-period-in-days>`_ condition key to further constrain the values that principals can specify in the ``RotationPeriodInDays`` parameter. For more information about rotating KMS keys and automatic rotation, see `Rotating keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* . Default: - 365
        :param tags: Assigns one or more tags to the replica key. .. epigraph:: Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in AWS , see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in CloudFormation, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kms import mixins as kms_mixins
            
            # key_policy: Any
            
            cfn_key_mixin_props = kms_mixins.CfnKeyMixinProps(
                bypass_policy_lockout_safety_check=False,
                description="description",
                enabled=False,
                enable_key_rotation=False,
                key_policy=key_policy,
                key_spec="keySpec",
                key_usage="keyUsage",
                multi_region=False,
                origin="origin",
                pending_window_in_days=123,
                rotation_period_in_days=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c5b75f87b25efdf85d7e80bd7c7bdc6a189f8c2989b0e5b7c5d5aaf90f9292)
            check_type(argname="argument bypass_policy_lockout_safety_check", value=bypass_policy_lockout_safety_check, expected_type=type_hints["bypass_policy_lockout_safety_check"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument key_policy", value=key_policy, expected_type=type_hints["key_policy"])
            check_type(argname="argument key_spec", value=key_spec, expected_type=type_hints["key_spec"])
            check_type(argname="argument key_usage", value=key_usage, expected_type=type_hints["key_usage"])
            check_type(argname="argument multi_region", value=multi_region, expected_type=type_hints["multi_region"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
            check_type(argname="argument pending_window_in_days", value=pending_window_in_days, expected_type=type_hints["pending_window_in_days"])
            check_type(argname="argument rotation_period_in_days", value=rotation_period_in_days, expected_type=type_hints["rotation_period_in_days"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bypass_policy_lockout_safety_check is not None:
            self._values["bypass_policy_lockout_safety_check"] = bypass_policy_lockout_safety_check
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if key_policy is not None:
            self._values["key_policy"] = key_policy
        if key_spec is not None:
            self._values["key_spec"] = key_spec
        if key_usage is not None:
            self._values["key_usage"] = key_usage
        if multi_region is not None:
            self._values["multi_region"] = multi_region
        if origin is not None:
            self._values["origin"] = origin
        if pending_window_in_days is not None:
            self._values["pending_window_in_days"] = pending_window_in_days
        if rotation_period_in_days is not None:
            self._values["rotation_period_in_days"] = rotation_period_in_days
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def bypass_policy_lockout_safety_check(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Skips ("bypasses") the key policy lockout safety check. The default value is false.

        .. epigraph::

           Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.

           For more information, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html#prevent-unmanageable-key>`_ in the *AWS Key Management Service Developer Guide* .

        Use this parameter only when you intend to prevent the principal that is making the request from making a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-bypasspolicylockoutsafetycheck
        '''
        result = self._values.get("bypass_policy_lockout_safety_check")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the KMS key.

        Use a description that helps you to distinguish this KMS key from others in the account, such as its intended use.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the KMS key is enabled. Disabled KMS keys cannot be used in cryptographic operations.

        When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` .

        The actual key state of the KMS key might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations.

        For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def enable_key_rotation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Enables automatic rotation of the key material for the specified KMS key.

        By default, automatic key rotation is not enabled.

        AWS  supports automatic rotation only for symmetric encryption KMS keys ( ``KeySpec`` = ``SYMMETRIC_DEFAULT`` ). For asymmetric KMS keys, HMAC KMS keys, and KMS keys with Origin ``EXTERNAL`` , omit the ``EnableKeyRotation`` property or set it to ``false`` .

        To enable automatic key rotation of the key material for a multi-Region KMS key, set ``EnableKeyRotation`` to ``true`` on the primary key (created by using ``AWS::KMS::Key`` ). AWS  copies the rotation status to all replica keys. For details, see `Rotating multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-manage.html#multi-region-rotate>`_ in the *AWS Key Management Service Developer Guide* .

        When you enable automatic rotation, AWS  automatically creates new key material for the KMS key one year after the enable date and every year thereafter. AWS  retains all key material until you delete the KMS key. For detailed information about automatic key rotation, see `Rotating KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-enablekeyrotation
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def key_policy(self) -> typing.Any:
        '''The key policy to attach to the KMS key.

        If you provide a key policy, it must meet the following criteria:

        - The key policy must allow the caller to make a subsequent `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ request on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ in the *AWS Key Management Service Developer Guide* . (To omit this condition, set ``BypassPolicyLockoutSafetyCheck`` to true.)
        - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS  . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS  . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* .

        If you do not provide a key policy, AWS  attaches a default key policy to the KMS key. For more information, see `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default>`_ in the *AWS Key Management Service Developer Guide* .

        A key policy document can include only the following characters:

        - Printable ASCII characters
        - Printable characters in the Basic Latin and Latin-1 Supplement character set
        - The tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` ) special characters

        *Minimum* : ``1``

        *Maximum* : ``32768``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keypolicy
        '''
        result = self._values.get("key_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def key_spec(self) -> typing.Optional[builtins.str]:
        '''Specifies the type of KMS key to create.

        The default value, ``SYMMETRIC_DEFAULT`` , creates a KMS key with a 256-bit symmetric key for encryption and decryption. In China Regions, ``SYMMETRIC_DEFAULT`` creates a 128-bit symmetric key that uses SM4 encryption. You can't change the ``KeySpec`` value after the KMS key is created. For help choosing a key spec for your KMS key, see `Choosing a KMS key type <https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html>`_ in the *AWS Key Management Service Developer Guide* .

        The ``KeySpec`` property determines the type of key material in the KMS key and the algorithms that the KMS key supports. To further restrict the algorithms that can be used with the KMS key, use a condition key in its key policy or IAM policy. For more information, see `AWS  condition keys <https://docs.aws.amazon.com/kms/latest/developerguide/policy-conditions.html#conditions-kms>`_ in the *AWS Key Management Service Developer Guide* .
        .. epigraph::

           If you change the value of the ``KeySpec`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value. > `AWS services that are integrated with AWS <https://docs.aws.amazon.com/kms/features/#AWS_Service_Integration>`_ use symmetric encryption KMS keys to protect your data. These services do not support encryption with asymmetric KMS keys. For help determining whether a KMS key is asymmetric, see `Identifying asymmetric KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/find-symm-asymm.html>`_ in the *AWS Key Management Service Developer Guide* .

        AWS  supports the following key specs for KMS keys:

        - Symmetric encryption key (default)
        - ``SYMMETRIC_DEFAULT`` (AES-256-GCM)
        - HMAC keys (symmetric)
        - ``HMAC_224``
        - ``HMAC_256``
        - ``HMAC_384``
        - ``HMAC_512``
        - Asymmetric RSA key pairs (encryption and decryption *or* signing and verification)
        - ``RSA_2048``
        - ``RSA_3072``
        - ``RSA_4096``
        - Asymmetric NIST-recommended elliptic curve key pairs (signing and verification *or* deriving shared secrets)
        - ``ECC_NIST_P256`` (secp256r1)
        - ``ECC_NIST_P384`` (secp384r1)
        - ``ECC_NIST_P521`` (secp521r1)
        - ``ECC_NIST_EDWARDS25519`` (ed25519) - signing and verification only
        - *Note:* For ECC_NIST_EDWARDS25519 KMS keys, the ED25519_SHA_512 signing algorithm requires ```MessageType:RAW`` <https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html#KMS-Sign-request-MessageType>`_ , while ED25519_PH_SHA_512 requires ```MessageType:DIGEST`` <https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html#KMS-Sign-request-MessageType>`_ . These message types cannot be used interchangeably.
        - Other asymmetric elliptic curve key pairs (signing and verification)
        - ``ECC_SECG_P256K1`` (secp256k1), commonly used for cryptocurrencies.
        - Asymmetric ML-DSA key pairs (signing and verification)
        - ``ML_DSA_44``
        - ``ML_DSA_65``
        - ``ML_DSA_87``
        - SM2 key pairs (encryption and decryption *or* signing and verification *or* deriving shared secrets)
        - ``SM2`` (China Regions only)

        :default: - "SYMMETRIC_DEFAULT"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyspec
        '''
        result = self._values.get("key_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_usage(self) -> typing.Optional[builtins.str]:
        '''Determines the `cryptographic operations <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations>`_ for which you can use the KMS key. The default value is ``ENCRYPT_DECRYPT`` . This property is required for asymmetric KMS keys and HMAC KMS keys. You can't change the ``KeyUsage`` value after the KMS key is created.

        .. epigraph::

           If you change the value of the ``KeyUsage`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value.

        Select only one valid value.

        - For symmetric encryption KMS keys, omit the parameter or specify ``ENCRYPT_DECRYPT`` .
        - For HMAC KMS keys (symmetric), specify ``GENERATE_VERIFY_MAC`` .
        - For asymmetric KMS keys with RSA key pairs, specify ``ENCRYPT_DECRYPT`` or ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with NIST-recommended elliptic curve key pairs, specify ``SIGN_VERIFY`` or ``KEY_AGREEMENT`` .
        - For asymmetric KMS keys with ``ECC_SECG_P256K1`` key pairs, specify ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with ML-DSA key pairs, specify ``SIGN_VERIFY`` .
        - For asymmetric KMS keys with SM2 key pairs (China Regions only), specify ``ENCRYPT_DECRYPT`` , ``SIGN_VERIFY`` , or ``KEY_AGREEMENT`` .

        :default: - "ENCRYPT_DECRYPT"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-keyusage
        '''
        result = self._values.get("key_usage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def multi_region(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Creates a multi-Region primary key that you can replicate in other AWS Regions .

        You can't change the ``MultiRegion`` value after the KMS key is created.

        For a list of AWS Regions in which multi-Region keys are supported, see `Multi-Region keys in AWS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** .
        .. epigraph::

           If you change the value of the ``MultiRegion`` property on an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing an immutable property value.

        For a multi-Region key, set to this property to ``true`` . For a single-Region key, omit this property or set it to ``false`` . The default value is ``false`` .

        *Multi-Region keys* are an AWS  feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

        You can create a symmetric encryption, HMAC, or asymmetric multi-Region KMS key, and you can create a multi-Region key with imported key material. However, you cannot create a multi-Region key in a custom key store.

        To create a replica of this primary key in a different AWS Region , create an `AWS::KMS::ReplicaKey <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html>`_ resource in a CloudFormation stack in the replica Region. Specify the key ARN of this primary key.

        :default: - false

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-multiregion
        '''
        result = self._values.get("multi_region")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def origin(self) -> typing.Optional[builtins.str]:
        '''The source of the key material for the KMS key.

        You cannot change the origin after you create the KMS key. The default is ``AWS_KMS`` , which means that AWS  creates the key material.

        To `create a KMS key with no key material <https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys-create-cmk.html>`_ (for imported key material), set this value to ``EXTERNAL`` . For more information about importing key material into AWS  , see `Importing Key Material <https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        You can ignore ``ENABLED`` when Origin is ``EXTERNAL`` . When a KMS key with Origin ``EXTERNAL`` is created, the key state is ``PENDING_IMPORT`` and ``ENABLED`` is ``false`` . After you import the key material, ``ENABLED`` updated to ``true`` . The KMS key can then be used for Cryptographic Operations.
        .. epigraph::

           - CloudFormation doesn't support creating an ``Origin`` parameter of the ``AWS_CLOUDHSM`` or ``EXTERNAL_KEY_STORE`` values.
           - ``EXTERNAL`` is not supported for ML-DSA keys.

        :default: - "AWS_KMS"

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-origin
        '''
        result = self._values.get("origin")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days in the waiting period before AWS  deletes a KMS key that has been removed from a CloudFormation stack.

        Enter a value between 7 and 30 days. The default value is 30 days.

        When you remove a KMS key from a CloudFormation stack, AWS  schedules the KMS key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of KMS key is ``Pending Deletion`` or ``Pending Replica Deletion`` , which prevents the KMS key from being used in cryptographic operations. When the waiting period expires, AWS  permanently deletes the KMS key.

        AWS  will not delete a `multi-Region primary key <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ that has replica keys. If you remove a multi-Region primary key from a CloudFormation stack, its key state changes to ``PendingReplicaDeletion`` so it cannot be replicated or used in cryptographic operations. This state can persist indefinitely. When the last of its replica keys is deleted, the key state of the primary key changes to ``PendingDeletion`` and the waiting period specified by ``PendingWindowInDays`` begins. When this waiting period expires, AWS  deletes the primary key. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* .

        You cannot use a CloudFormation template to cancel deletion of the KMS key after you remove it from the stack, regardless of the waiting period. If you specify a KMS key in your template, even one with the same name, CloudFormation creates a new KMS key. To cancel deletion of a KMS key, use the AWS  console or the `CancelKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_CancelKeyDeletion.html>`_ operation.

        For information about the ``Pending Deletion`` and ``Pending Replica Deletion`` key states, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-pendingwindowindays
        '''
        result = self._values.get("pending_window_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rotation_period_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies a custom period of time between each rotation date.

        If no value is specified, the default value is 365 days.

        The rotation period defines the number of days after you enable automatic key rotation that AWS  will rotate your key material, and the number of days between each automatic rotation thereafter.

        You can use the ```kms:RotationPeriodInDays`` <https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-rotation-period-in-days>`_ condition key to further constrain the values that principals can specify in the ``RotationPeriodInDays`` parameter.

        For more information about rotating KMS keys and automatic rotation, see `Rotating keys <https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        :default: - 365

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-rotationperiodindays
        '''
        result = self._values.get("rotation_period_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags to the replica key.

        .. epigraph::

           Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

        For information about tags in AWS  , see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ in the *AWS Key Management Service Developer Guide* . For information about tags in CloudFormation, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html#cfn-kms-key-tags
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
    jsii_type="@aws-cdk/mixins-preview.aws_kms.mixins.CfnKeyPropsMixin",
):
    '''The ``AWS::KMS::Key`` resource specifies an `KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys>`_ in AWS Key Management Service . You can use this resource to create symmetric encryption KMS keys, asymmetric KMS keys for encryption or signing, and symmetric HMAC KMS keys. You can use ``AWS::KMS::Key`` to create `multi-Region primary keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html#mrk-primary-key>`_ of all supported types. To replicate a multi-Region key, use the ``AWS::KMS::ReplicaKey`` resource.

    .. epigraph::

       If you change the value of the ``KeySpec`` , ``KeyUsage`` , ``Origin`` , or ``MultiRegion`` properties of an existing KMS key, the update request fails, regardless of the value of the ```UpdateReplacePolicy`` attribute <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-updatereplacepolicy.html>`_ . This prevents you from accidentally deleting a KMS key by changing any of its immutable property values. > AWS  replaced the term *customer master key (CMK)* with *AWS KMS key* and *KMS key* . The concept has not changed. To prevent breaking changes, AWS  is keeping some variations of this term.

    You can use symmetric encryption KMS keys to encrypt and decrypt small amounts of data, but they are more commonly used to generate data keys and data key pairs. You can also use a symmetric encryption KMS key to encrypt data stored in AWS services that are `integrated with AWS <https://docs.aws.amazon.com//kms/features/#AWS_Service_Integration>`_ . For more information, see `Symmetric encryption KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#symmetric-cmks>`_ in the *AWS Key Management Service Developer Guide* .

    You can use asymmetric KMS keys to encrypt and decrypt data or sign messages and verify signatures. To create an asymmetric key, you must specify an asymmetric ``KeySpec`` value and a ``KeyUsage`` value. For details, see `Asymmetric keys in AWS <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

    You can use HMAC KMS keys (which are also symmetric keys) to generate and verify hash-based message authentication codes. To create an HMAC key, you must specify an HMAC ``KeySpec`` value and a ``KeyUsage`` value of ``GENERATE_VERIFY_MAC`` . For details, see `HMAC keys in AWS <https://docs.aws.amazon.com/kms/latest/developerguide/hmac.html>`_ in the *AWS Key Management Service Developer Guide* .

    You can also create symmetric encryption, asymmetric, and HMAC multi-Region primary keys. To create a multi-Region primary key, set the ``MultiRegion`` property to ``true`` . For information about multi-Region keys, see `Multi-Region keys in AWS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

    You cannot use the ``AWS::KMS::Key`` resource to specify a KMS key with `imported key material <https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html>`_ or a KMS key in a `custom key store <https://docs.aws.amazon.com/kms/latest/developerguide/custom-key-store-overview.html>`_ .

    *Regions*

    AWS  CloudFormation resources are available in all Regions in which AWS  and CloudFormation are supported. You can use the ``AWS::KMS::Key`` resource to create and manage all KMS key types that are supported in a Region.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html
    :cloudformationResource: AWS::KMS::Key
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kms import mixins as kms_mixins
        
        # key_policy: Any
        
        cfn_key_props_mixin = kms_mixins.CfnKeyPropsMixin(kms_mixins.CfnKeyMixinProps(
            bypass_policy_lockout_safety_check=False,
            description="description",
            enabled=False,
            enable_key_rotation=False,
            key_policy=key_policy,
            key_spec="keySpec",
            key_usage="keyUsage",
            multi_region=False,
            origin="origin",
            pending_window_in_days=123,
            rotation_period_in_days=123,
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
        '''Create a mixin to apply properties to ``AWS::KMS::Key``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434527bb1c8d904ce726607206775f3b1be98c594d7f779e139492daf73e7265)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cec9a7ddfb01bce374727e403001e20522e58f85a9c337f656f9c7b3e244f4b8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71b7b01b92f5148a1cab82c877cbb7464f6f2116fe4b228567ea52c6fbc960c8)
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
    jsii_type="@aws-cdk/mixins-preview.aws_kms.mixins.CfnReplicaKeyMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "enabled": "enabled",
        "key_policy": "keyPolicy",
        "pending_window_in_days": "pendingWindowInDays",
        "primary_key_arn": "primaryKeyArn",
        "tags": "tags",
    },
)
class CfnReplicaKeyMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        key_policy: typing.Any = None,
        pending_window_in_days: typing.Optional[jsii.Number] = None,
        primary_key_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnReplicaKeyPropsMixin.

        :param description: A description of the KMS key. The default value is an empty string (no description). The description is not a shared property of multi-Region keys. You can specify the same description or a different description for each key in a set of related multi-Region keys. AWS Key Management Service does not synchronize this property.
        :param enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` . The actual key state of the replica might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. Also, while the replica key is being created, its key state is ``Creating`` . When the process is complete, the key state of the replica key changes to ``Enabled`` . For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param key_policy: The key policy that authorizes use of the replica key. The key policy is not a shared property of multi-Region keys. You can specify the same key policy or a different key policy for each key in a set of related multi-Region keys. AWS does not synchronize this property. The key policy must conform to the following rules. - The key policy must give the caller `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ permission on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** . - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* . A key policy document can include only the following characters: - Printable ASCII characters from the space character ( ``\\u0020`` ) through the end of the ASCII character range. - Printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ). - The tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` ) special characters *Minimum* : ``1`` *Maximum* : ``32768``
        :param pending_window_in_days: Specifies the number of days in the waiting period before AWS deletes a replica key that has been removed from a CloudFormation stack. Enter a value between 7 and 30 days. The default value is 30 days. When you remove a replica key from a CloudFormation stack, AWS schedules the replica key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of replica key is ``Pending Deletion`` , which prevents it from being used in cryptographic operations. When the waiting period expires, AWS permanently deletes the replica key. If the KMS key is a multi-Region primary key with replica keys, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately. You cannot use a CloudFormation template to cancel deletion of the replica after you remove it from the stack, regardless of the waiting period. However, if you specify a replica key in your template that is based on the same primary key as the original replica key, CloudFormation creates a new replica key with the same key ID, key material, and other shared properties of the original replica key. This new replica key can decrypt ciphertext that was encrypted under the original replica key, or any related multi-Region key. For detailed information about deleting multi-Region keys, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* . For information about the ``PendingDeletion`` key state, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .
        :param primary_key_arn: Specifies the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS partition. You can create only one replica of a given primary key in each AWS Region . .. epigraph:: If you change the ``PrimaryKeyArn`` value of a replica key, the existing replica key is scheduled for deletion and a new replica key is created based on the specified primary key. While it is scheduled for deletion, the existing replica key becomes unusable. You can cancel the scheduled deletion of the key outside of CloudFormation. However, if you inadvertently delete a replica key, you can decrypt ciphertext encrypted by that replica key by using any related multi-Region key. If necessary, you can recreate the replica in the same Region after the previous one is completely deleted. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* Specify the key ARN of an existing multi-Region primary key. For example, ``arn:aws:kms:us-east-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .
        :param tags: Assigns one or more tags to the replica key. .. epigraph:: Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* . Tags are not a shared property of multi-Region keys. You can specify the same tags or different tags for each key in a set of related multi-Region keys. AWS does not synchronize this property. Each tag consists of a tag key and a tag value. Both the tag key and the tag value are required, but the tag value can be an empty (null) string. You cannot have more than one tag on a KMS key with the same tag key. If you specify an existing tag key with a different tag value, AWS replaces the current tag value with the specified one. When you assign tags to an AWS resource, AWS generates a cost allocation report with usage and costs aggregated by tags. Tags can also be used to control access to a KMS key. For details, see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kms import mixins as kms_mixins
            
            # key_policy: Any
            
            cfn_replica_key_mixin_props = kms_mixins.CfnReplicaKeyMixinProps(
                description="description",
                enabled=False,
                key_policy=key_policy,
                pending_window_in_days=123,
                primary_key_arn="primaryKeyArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d0d8104f834aef3cce38c00592bd7089c7ad6c0f85cf36c7581fc942f2d3a8)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument key_policy", value=key_policy, expected_type=type_hints["key_policy"])
            check_type(argname="argument pending_window_in_days", value=pending_window_in_days, expected_type=type_hints["pending_window_in_days"])
            check_type(argname="argument primary_key_arn", value=primary_key_arn, expected_type=type_hints["primary_key_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if key_policy is not None:
            self._values["key_policy"] = key_policy
        if pending_window_in_days is not None:
            self._values["pending_window_in_days"] = pending_window_in_days
        if primary_key_arn is not None:
            self._values["primary_key_arn"] = primary_key_arn
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the KMS key.

        The default value is an empty string (no description).

        The description is not a shared property of multi-Region keys. You can specify the same description or a different description for each key in a set of related multi-Region keys. AWS Key Management Service does not synchronize this property.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations.

        When ``Enabled`` is ``true`` , the *key state* of the KMS key is ``Enabled`` . When ``Enabled`` is ``false`` , the key state of the KMS key is ``Disabled`` . The default value is ``true`` .

        The actual key state of the replica might be affected by actions taken outside of CloudFormation, such as running the `EnableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_EnableKey.html>`_ , `DisableKey <https://docs.aws.amazon.com/kms/latest/APIReference/API_DisableKey.html>`_ , or `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operations. Also, while the replica key is being created, its key state is ``Creating`` . When the process is complete, the key state of the replica key changes to ``Enabled`` .

        For information about the key states of a KMS key, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def key_policy(self) -> typing.Any:
        '''The key policy that authorizes use of the replica key.

        The key policy is not a shared property of multi-Region keys. You can specify the same key policy or a different key policy for each key in a set of related multi-Region keys. AWS  does not synchronize this property.

        The key policy must conform to the following rules.

        - The key policy must give the caller `PutKeyPolicy <https://docs.aws.amazon.com/kms/latest/APIReference/API_PutKeyPolicy.html>`_ permission on the KMS key. This reduces the risk that the KMS key becomes unmanageable. For more information, refer to the scenario in the `Default key policy <https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam>`_ section of the **AWS Key Management Service Developer Guide** .
        - Each statement in the key policy must contain one or more principals. The principals in the key policy must exist and be visible to AWS  . When you create a new AWS principal (for example, an IAM user or role), you might need to enforce a delay before including the new principal in a key policy because the new principal might not be immediately visible to AWS  . For more information, see `Changes that I make are not always immediately visible <https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_general.html#troubleshoot_general_eventual-consistency>`_ in the *AWS Identity and Access Management User Guide* .

        A key policy document can include only the following characters:

        - Printable ASCII characters from the space character ( ``\\u0020`` ) through the end of the ASCII character range.
        - Printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\u00FF`` ).
        - The tab ( ``\\u0009`` ), line feed ( ``\\u000A`` ), and carriage return ( ``\\u000D`` ) special characters

        *Minimum* : ``1``

        *Maximum* : ``32768``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-keypolicy
        '''
        result = self._values.get("key_policy")
        return typing.cast(typing.Any, result)

    @builtins.property
    def pending_window_in_days(self) -> typing.Optional[jsii.Number]:
        '''Specifies the number of days in the waiting period before AWS  deletes a replica key that has been removed from a CloudFormation stack.

        Enter a value between 7 and 30 days. The default value is 30 days.

        When you remove a replica key from a CloudFormation stack, AWS  schedules the replica key for deletion and starts the mandatory waiting period. The ``PendingWindowInDays`` property determines the length of waiting period. During the waiting period, the key state of replica key is ``Pending Deletion`` , which prevents it from being used in cryptographic operations. When the waiting period expires, AWS  permanently deletes the replica key.

        If the KMS key is a multi-Region primary key with replica keys, the waiting period begins when the last of its replica keys is deleted. Otherwise, the waiting period begins immediately.

        You cannot use a CloudFormation template to cancel deletion of the replica after you remove it from the stack, regardless of the waiting period. However, if you specify a replica key in your template that is based on the same primary key as the original replica key, CloudFormation creates a new replica key with the same key ID, key material, and other shared properties of the original replica key. This new replica key can decrypt ciphertext that was encrypted under the original replica key, or any related multi-Region key.

        For detailed information about deleting multi-Region keys, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide* .

        For information about the ``PendingDeletion`` key state, see `Key state: Effect on your KMS key <https://docs.aws.amazon.com/kms/latest/developerguide/key-state.html>`_ in the *AWS Key Management Service Developer Guide* . For more information about deleting KMS keys, see the `ScheduleKeyDeletion <https://docs.aws.amazon.com/kms/latest/APIReference/API_ScheduleKeyDeletion.html>`_ operation in the *AWS Key Management Service API Reference* and `Deleting KMS keys <https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-pendingwindowindays
        '''
        result = self._values.get("pending_window_in_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def primary_key_arn(self) -> typing.Optional[builtins.str]:
        '''Specifies the multi-Region primary key to replicate.

        The primary key must be in a different AWS Region of the same AWS partition. You can create only one replica of a given primary key in each AWS Region .
        .. epigraph::

           If you change the ``PrimaryKeyArn`` value of a replica key, the existing replica key is scheduled for deletion and a new replica key is created based on the specified primary key. While it is scheduled for deletion, the existing replica key becomes unusable. You can cancel the scheduled deletion of the key outside of CloudFormation.

           However, if you inadvertently delete a replica key, you can decrypt ciphertext encrypted by that replica key by using any related multi-Region key. If necessary, you can recreate the replica in the same Region after the previous one is completely deleted. For details, see `Deleting multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-delete.html>`_ in the *AWS Key Management Service Developer Guide*

        Specify the key ARN of an existing multi-Region primary key. For example, ``arn:aws:kms:us-east-2:111122223333:key/mrk-1234abcd12ab34cd56ef1234567890ab`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-primarykeyarn
        '''
        result = self._values.get("primary_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Assigns one or more tags to the replica key.

        .. epigraph::

           Tagging or untagging a KMS key can allow or deny permission to the KMS key. For details, see `ABAC for AWS <https://docs.aws.amazon.com/kms/latest/developerguide/abac.html>`_ in the *AWS Key Management Service Developer Guide* .

        Tags are not a shared property of multi-Region keys. You can specify the same tags or different tags for each key in a set of related multi-Region keys. AWS  does not synchronize this property.

        Each tag consists of a tag key and a tag value. Both the tag key and the tag value are required, but the tag value can be an empty (null) string. You cannot have more than one tag on a KMS key with the same tag key. If you specify an existing tag key with a different tag value, AWS  replaces the current tag value with the specified one.

        When you assign tags to an AWS resource, AWS generates a cost allocation report with usage and costs aggregated by tags. Tags can also be used to control access to a KMS key. For details, see `Tagging keys <https://docs.aws.amazon.com/kms/latest/developerguide/tagging-keys.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html#cfn-kms-replicakey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReplicaKeyMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnReplicaKeyPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kms.mixins.CfnReplicaKeyPropsMixin",
):
    '''The ``AWS::KMS::ReplicaKey`` resource specifies a multi-Region replica key that is based on a multi-Region primary key.

    *Multi-Region keys* are an AWS  feature that lets you create multiple interoperable KMS keys in different AWS Regions . Because these KMS keys have the same key ID, key material, and other metadata, you can use them to encrypt data in one AWS Region and decrypt it in a different AWS Region without making a cross-Region call or exposing the plaintext data. For more information, see `Multi-Region keys <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the *AWS Key Management Service Developer Guide* .

    A multi-Region *primary key* is a fully functional symmetric encryption KMS key, HMAC KMS key, or asymmetric KMS key that is also the model for replica keys in other AWS Regions . To create a multi-Region primary key, add an `AWS::KMS::Key <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-key.html>`_ resource to your CloudFormation stack. Set its ``MultiRegion`` property to true.

    A multi-Region *replica key* is a fully functional KMS key that has the same key ID and key material as a multi-Region primary key, but is located in a different AWS Region of the same AWS partition. There can be multiple replicas of a primary key, but each must be in a different AWS Region .

    When you create a replica key in CloudFormation , the replica key is created in the AWS Region represented by the endpoint you use for the request. If you try to replicate a multi-Region key into a Region in which the key type is not supported, the request will fail.

    A primary key and its replicas have the same key ID and key material. They also have the same key spec, key usage, key material origin, and automatic key rotation status. These properties are known as *shared properties* . If they change, AWS  synchronizes the change to all related multi-Region keys. All other properties of a replica key can differ, including its key policy, tags, aliases, and key state. AWS  does not synchronize these properties.

    *Regions*

    AWS  CloudFormation resources are available in all AWS Regions in which AWS  and CloudFormation are supported. You can use the ``AWS::KMS::ReplicaKey`` resource to create replica keys in all Regions that support multi-Region KMS keys. For details, see `Multi-Region keys in AWS <https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html>`_ in the ** .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kms-replicakey.html
    :cloudformationResource: AWS::KMS::ReplicaKey
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kms import mixins as kms_mixins
        
        # key_policy: Any
        
        cfn_replica_key_props_mixin = kms_mixins.CfnReplicaKeyPropsMixin(kms_mixins.CfnReplicaKeyMixinProps(
            description="description",
            enabled=False,
            key_policy=key_policy,
            pending_window_in_days=123,
            primary_key_arn="primaryKeyArn",
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
        props: typing.Union[CfnReplicaKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KMS::ReplicaKey``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbbc24b66c23da39bba621790a25dc1503f4157d7f89f50d3d5ec1a910e0bc5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a648a992e673c8422fb77c385abe14cb4dd3c6e3e2d4cc7be6254af3ac44bd1c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8529a0c7af9e48e865480396a74e5d669721dfe396690790345e4366092676f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnReplicaKeyMixinProps:
        return typing.cast(CfnReplicaKeyMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnAliasMixinProps",
    "CfnAliasPropsMixin",
    "CfnKeyMixinProps",
    "CfnKeyPropsMixin",
    "CfnReplicaKeyMixinProps",
    "CfnReplicaKeyPropsMixin",
]

publication.publish()

def _typecheckingstub__2b791cbc86612400f303349e79b7d4e30901c91bc75150acb2568c1ad677d0af(
    *,
    alias_name: typing.Optional[builtins.str] = None,
    target_key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d43eab79966d8f362ca012437f1965b66fdd0f3d4f6682be68313171c9cf74(
    props: typing.Union[CfnAliasMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1077779e7ef506ee71c3f5737b60a72053b6bee83e07bac998d4560eec5c4dc6(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7af15734af6409ec739451ad89fcd9a6efb82dcf6e136a3ec29e532daee7ba5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c5b75f87b25efdf85d7e80bd7c7bdc6a189f8c2989b0e5b7c5d5aaf90f9292(
    *,
    bypass_policy_lockout_safety_check: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    enable_key_rotation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_policy: typing.Any = None,
    key_spec: typing.Optional[builtins.str] = None,
    key_usage: typing.Optional[builtins.str] = None,
    multi_region: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    origin: typing.Optional[builtins.str] = None,
    pending_window_in_days: typing.Optional[jsii.Number] = None,
    rotation_period_in_days: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434527bb1c8d904ce726607206775f3b1be98c594d7f779e139492daf73e7265(
    props: typing.Union[CfnKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec9a7ddfb01bce374727e403001e20522e58f85a9c337f656f9c7b3e244f4b8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71b7b01b92f5148a1cab82c877cbb7464f6f2116fe4b228567ea52c6fbc960c8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d0d8104f834aef3cce38c00592bd7089c7ad6c0f85cf36c7581fc942f2d3a8(
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    key_policy: typing.Any = None,
    pending_window_in_days: typing.Optional[jsii.Number] = None,
    primary_key_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbbc24b66c23da39bba621790a25dc1503f4157d7f89f50d3d5ec1a910e0bc5(
    props: typing.Union[CfnReplicaKeyMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a648a992e673c8422fb77c385abe14cb4dd3c6e3e2d4cc7be6254af3ac44bd1c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8529a0c7af9e48e865480396a74e5d669721dfe396690790345e4366092676f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
