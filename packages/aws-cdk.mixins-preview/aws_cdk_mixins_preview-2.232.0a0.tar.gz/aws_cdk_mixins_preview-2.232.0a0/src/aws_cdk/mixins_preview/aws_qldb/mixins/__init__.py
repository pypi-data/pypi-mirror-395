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
    jsii_type="@aws-cdk/mixins-preview.aws_qldb.mixins.CfnLedgerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "deletion_protection": "deletionProtection",
        "kms_key": "kmsKey",
        "name": "name",
        "permissions_mode": "permissionsMode",
        "tags": "tags",
    },
)
class CfnLedgerMixinProps:
    def __init__(
        self,
        *,
        deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        kms_key: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        permissions_mode: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnLedgerPropsMixin.

        :param deletion_protection: Specifies whether the ledger is protected from being deleted by any user. If not defined during ledger creation, this feature is enabled ( ``true`` ) by default. If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the ``UpdateLedger`` operation to set this parameter to ``false`` .
        :param kms_key: The key in AWS Key Management Service ( AWS ) to use for encryption of data at rest in the ledger. For more information, see `Encryption at rest <https://docs.aws.amazon.com/qldb/latest/developerguide/encryption-at-rest.html>`_ in the *Amazon QLDB Developer Guide* . Use one of the following options to specify this parameter: - ``AWS_OWNED_KMS_KEY`` : Use an AWS key that is owned and managed by AWS on your behalf. - *Undefined* : By default, use an AWS owned KMS key. - *A valid symmetric customer managed KMS key* : Use the specified symmetric encryption KMS key in your account that you create, own, and manage. Amazon QLDB does not support asymmetric keys. For more information, see `Using symmetric and asymmetric keys <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* . To specify a customer managed KMS key, you can use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. When using an alias name, prefix it with ``"alias/"`` . To specify a key in a different AWS account , you must use the key ARN or alias ARN. For example: - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab`` - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab`` - Alias name: ``alias/ExampleAlias`` - Alias ARN: ``arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias`` For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .
        :param name: The name of the ledger that you want to create. The name must be unique among all of the ledgers in your AWS account in the current Region. Naming constraints for ledger names are defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .
        :param permissions_mode: The permissions mode to assign to the ledger that you want to create. This parameter can have one of the following values: - ``ALLOW_ALL`` : A legacy permissions mode that enables access control with API-level granularity for ledgers. This mode allows users who have the ``SendCommand`` API permission for this ledger to run all PartiQL commands (hence, ``ALLOW_ALL`` ) on any tables in the specified ledger. This mode disregards any table-level or command-level IAM permissions policies that you create for the ledger. - ``STANDARD`` : ( *Recommended* ) A permissions mode that enables access control with finer granularity for ledgers, tables, and PartiQL commands. By default, this mode denies all user requests to run any PartiQL commands on any tables in this ledger. To allow PartiQL commands to run, you must create IAM permissions policies for specific table resources and PartiQL actions, in addition to the ``SendCommand`` API permission for the ledger. For information, see `Getting started with the standard permissions mode <https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html>`_ in the *Amazon QLDB Developer Guide* . .. epigraph:: We strongly recommend using the ``STANDARD`` permissions mode to maximize the security of your ledger data.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qldb import mixins as qldb_mixins
            
            cfn_ledger_mixin_props = qldb_mixins.CfnLedgerMixinProps(
                deletion_protection=False,
                kms_key="kmsKey",
                name="name",
                permissions_mode="permissionsMode",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__364626c801033c5fd29b84dbcf27e3782014ef2ab7dc992fcb372b7a5159ceb8)
            check_type(argname="argument deletion_protection", value=deletion_protection, expected_type=type_hints["deletion_protection"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions_mode", value=permissions_mode, expected_type=type_hints["permissions_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if name is not None:
            self._values["name"] = name
        if permissions_mode is not None:
            self._values["permissions_mode"] = permissions_mode
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether the ledger is protected from being deleted by any user.

        If not defined during ledger creation, this feature is enabled ( ``true`` ) by default.

        If deletion protection is enabled, you must first disable it before you can delete the ledger. You can disable it by calling the ``UpdateLedger`` operation to set this parameter to ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-deletionprotection
        '''
        result = self._values.get("deletion_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[builtins.str]:
        '''The key in AWS Key Management Service ( AWS  ) to use for encryption of data at rest in the ledger.

        For more information, see `Encryption at rest <https://docs.aws.amazon.com/qldb/latest/developerguide/encryption-at-rest.html>`_ in the *Amazon QLDB Developer Guide* .

        Use one of the following options to specify this parameter:

        - ``AWS_OWNED_KMS_KEY`` : Use an AWS  key that is owned and managed by AWS on your behalf.
        - *Undefined* : By default, use an AWS owned KMS key.
        - *A valid symmetric customer managed KMS key* : Use the specified symmetric encryption KMS key in your account that you create, own, and manage.

        Amazon QLDB does not support asymmetric keys. For more information, see `Using symmetric and asymmetric keys <https://docs.aws.amazon.com/kms/latest/developerguide/symmetric-asymmetric.html>`_ in the *AWS Key Management Service Developer Guide* .

        To specify a customer managed KMS key, you can use its key ID, Amazon Resource Name (ARN), alias name, or alias ARN. When using an alias name, prefix it with ``"alias/"`` . To specify a key in a different AWS account , you must use the key ARN or alias ARN.

        For example:

        - Key ID: ``1234abcd-12ab-34cd-56ef-1234567890ab``
        - Key ARN: ``arn:aws:kms:us-east-2:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab``
        - Alias name: ``alias/ExampleAlias``
        - Alias ARN: ``arn:aws:kms:us-east-2:111122223333:alias/ExampleAlias``

        For more information, see `Key identifiers (KeyId) <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-id>`_ in the *AWS Key Management Service Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-kmskey
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ledger that you want to create.

        The name must be unique among all of the ledgers in your AWS account in the current Region.

        Naming constraints for ledger names are defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_mode(self) -> typing.Optional[builtins.str]:
        '''The permissions mode to assign to the ledger that you want to create.

        This parameter can have one of the following values:

        - ``ALLOW_ALL`` : A legacy permissions mode that enables access control with API-level granularity for ledgers.

        This mode allows users who have the ``SendCommand`` API permission for this ledger to run all PartiQL commands (hence, ``ALLOW_ALL`` ) on any tables in the specified ledger. This mode disregards any table-level or command-level IAM permissions policies that you create for the ledger.

        - ``STANDARD`` : ( *Recommended* ) A permissions mode that enables access control with finer granularity for ledgers, tables, and PartiQL commands.

        By default, this mode denies all user requests to run any PartiQL commands on any tables in this ledger. To allow PartiQL commands to run, you must create IAM permissions policies for specific table resources and PartiQL actions, in addition to the ``SendCommand`` API permission for the ledger. For information, see `Getting started with the standard permissions mode <https://docs.aws.amazon.com/qldb/latest/developerguide/getting-started-standard-mode.html>`_ in the *Amazon QLDB Developer Guide* .
        .. epigraph::

           We strongly recommend using the ``STANDARD`` permissions mode to maximize the security of your ledger data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-permissionsmode
        '''
        result = self._values.get("permissions_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html#cfn-qldb-ledger-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLedgerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnLedgerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qldb.mixins.CfnLedgerPropsMixin",
):
    '''The ``AWS::QLDB::Ledger`` resource specifies a new Amazon Quantum Ledger Database (Amazon QLDB) ledger in your AWS account .

    Amazon QLDB is a fully managed ledger database that provides a transparent, immutable, and cryptographically verifiable transaction log owned by a central trusted authority. You can use QLDB to track all application data changes, and maintain a complete and verifiable history of changes over time.

    For more information, see `CreateLedger <https://docs.aws.amazon.com/qldb/latest/developerguide/API_CreateLedger.html>`_ in the *Amazon QLDB API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-ledger.html
    :cloudformationResource: AWS::QLDB::Ledger
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qldb import mixins as qldb_mixins
        
        cfn_ledger_props_mixin = qldb_mixins.CfnLedgerPropsMixin(qldb_mixins.CfnLedgerMixinProps(
            deletion_protection=False,
            kms_key="kmsKey",
            name="name",
            permissions_mode="permissionsMode",
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
        props: typing.Union[CfnLedgerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QLDB::Ledger``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f85eca9d1b7582bb0fe82e5f3a0fe3e55b05cec637b237147e7abf90aeee8b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7942e90a2eb705cfe30d7c1e8b11c09d96493212b6b8ed614d504c910938f4d2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6050b30d754f1283668c713f839d18cb4e922a7c1260ac658192880fc47c4b71)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnLedgerMixinProps:
        return typing.cast(CfnLedgerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_qldb.mixins.CfnStreamMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "exclusive_end_time": "exclusiveEndTime",
        "inclusive_start_time": "inclusiveStartTime",
        "kinesis_configuration": "kinesisConfiguration",
        "ledger_name": "ledgerName",
        "role_arn": "roleArn",
        "stream_name": "streamName",
        "tags": "tags",
    },
)
class CfnStreamMixinProps:
    def __init__(
        self,
        *,
        exclusive_end_time: typing.Optional[builtins.str] = None,
        inclusive_start_time: typing.Optional[builtins.str] = None,
        kinesis_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStreamPropsMixin.KinesisConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ledger_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        stream_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStreamPropsMixin.

        :param exclusive_end_time: The exclusive date and time that specifies when the stream ends. If you don't define this parameter, the stream runs indefinitely until you cancel it. The ``ExclusiveEndTime`` must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .
        :param inclusive_start_time: The inclusive start date and time from which to start streaming journal data. This parameter must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` . The ``InclusiveStartTime`` cannot be in the future and must be before ``ExclusiveEndTime`` . If you provide an ``InclusiveStartTime`` that is before the ledger's ``CreationDateTime`` , QLDB effectively defaults it to the ledger's ``CreationDateTime`` .
        :param kinesis_configuration: The configuration settings of the Kinesis Data Streams destination for your stream request.
        :param ledger_name: The name of the ledger.
        :param role_arn: The Amazon Resource Name (ARN) of the IAM role that grants QLDB permissions for a journal stream to write data records to a Kinesis Data Streams resource. To pass a role to QLDB when requesting a journal stream, you must have permissions to perform the ``iam:PassRole`` action on the IAM role resource. This is required for all journal stream requests.
        :param stream_name: The name that you want to assign to the QLDB journal stream. User-defined names can help identify and indicate the purpose of a stream. Your stream name must be unique among other *active* streams for a given ledger. Stream names have the same naming constraints as ledger names, as defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_qldb import mixins as qldb_mixins
            
            cfn_stream_mixin_props = qldb_mixins.CfnStreamMixinProps(
                exclusive_end_time="exclusiveEndTime",
                inclusive_start_time="inclusiveStartTime",
                kinesis_configuration=qldb_mixins.CfnStreamPropsMixin.KinesisConfigurationProperty(
                    aggregation_enabled=False,
                    stream_arn="streamArn"
                ),
                ledger_name="ledgerName",
                role_arn="roleArn",
                stream_name="streamName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e48d609d9e222e1e7e58a60dd44228c35ca0c38abce687bd47956a47e141909)
            check_type(argname="argument exclusive_end_time", value=exclusive_end_time, expected_type=type_hints["exclusive_end_time"])
            check_type(argname="argument inclusive_start_time", value=inclusive_start_time, expected_type=type_hints["inclusive_start_time"])
            check_type(argname="argument kinesis_configuration", value=kinesis_configuration, expected_type=type_hints["kinesis_configuration"])
            check_type(argname="argument ledger_name", value=ledger_name, expected_type=type_hints["ledger_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stream_name", value=stream_name, expected_type=type_hints["stream_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclusive_end_time is not None:
            self._values["exclusive_end_time"] = exclusive_end_time
        if inclusive_start_time is not None:
            self._values["inclusive_start_time"] = inclusive_start_time
        if kinesis_configuration is not None:
            self._values["kinesis_configuration"] = kinesis_configuration
        if ledger_name is not None:
            self._values["ledger_name"] = ledger_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if stream_name is not None:
            self._values["stream_name"] = stream_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def exclusive_end_time(self) -> typing.Optional[builtins.str]:
        '''The exclusive date and time that specifies when the stream ends.

        If you don't define this parameter, the stream runs indefinitely until you cancel it.

        The ``ExclusiveEndTime`` must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-exclusiveendtime
        '''
        result = self._values.get("exclusive_end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inclusive_start_time(self) -> typing.Optional[builtins.str]:
        '''The inclusive start date and time from which to start streaming journal data.

        This parameter must be in ``ISO 8601`` date and time format and in Universal Coordinated Time (UTC). For example: ``2019-06-13T21:36:34Z`` .

        The ``InclusiveStartTime`` cannot be in the future and must be before ``ExclusiveEndTime`` .

        If you provide an ``InclusiveStartTime`` that is before the ledger's ``CreationDateTime`` , QLDB effectively defaults it to the ledger's ``CreationDateTime`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-inclusivestarttime
        '''
        result = self._values.get("inclusive_start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kinesis_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.KinesisConfigurationProperty"]]:
        '''The configuration settings of the Kinesis Data Streams destination for your stream request.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-kinesisconfiguration
        '''
        result = self._values.get("kinesis_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStreamPropsMixin.KinesisConfigurationProperty"]], result)

    @builtins.property
    def ledger_name(self) -> typing.Optional[builtins.str]:
        '''The name of the ledger.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-ledgername
        '''
        result = self._values.get("ledger_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the IAM role that grants QLDB permissions for a journal stream to write data records to a Kinesis Data Streams resource.

        To pass a role to QLDB when requesting a journal stream, you must have permissions to perform the ``iam:PassRole`` action on the IAM role resource. This is required for all journal stream requests.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_name(self) -> typing.Optional[builtins.str]:
        '''The name that you want to assign to the QLDB journal stream.

        User-defined names can help identify and indicate the purpose of a stream.

        Your stream name must be unique among other *active* streams for a given ledger. Stream names have the same naming constraints as ledger names, as defined in `Quotas in Amazon QLDB <https://docs.aws.amazon.com/qldb/latest/developerguide/limits.html#limits.naming>`_ in the *Amazon QLDB Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-streamname
        '''
        result = self._values.get("stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html#cfn-qldb-stream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStreamPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_qldb.mixins.CfnStreamPropsMixin",
):
    '''The ``AWS::QLDB::Stream`` resource specifies a journal stream for a given Amazon Quantum Ledger Database (Amazon QLDB) ledger.

    The stream captures every document revision that is committed to the ledger's journal and delivers the data to a specified Amazon Kinesis Data Streams resource.

    For more information, see `StreamJournalToKinesis <https://docs.aws.amazon.com/qldb/latest/developerguide/API_StreamJournalToKinesis.html>`_ in the *Amazon QLDB API Reference* .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-qldb-stream.html
    :cloudformationResource: AWS::QLDB::Stream
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_qldb import mixins as qldb_mixins
        
        cfn_stream_props_mixin = qldb_mixins.CfnStreamPropsMixin(qldb_mixins.CfnStreamMixinProps(
            exclusive_end_time="exclusiveEndTime",
            inclusive_start_time="inclusiveStartTime",
            kinesis_configuration=qldb_mixins.CfnStreamPropsMixin.KinesisConfigurationProperty(
                aggregation_enabled=False,
                stream_arn="streamArn"
            ),
            ledger_name="ledgerName",
            role_arn="roleArn",
            stream_name="streamName",
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
        props: typing.Union[CfnStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::QLDB::Stream``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c9655cccf635169d2e8038e073e8f183e1ff016055c83f3404b779cc9c0e0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e59924db37f52e293ba88cc89d5a077d4b8b71b36b34875adaa1a8b7374dc404)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64dc7aeb7889287c65ef4efd2ebc3fc6a7c7fa365bbed5e161416d4be2931284)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStreamMixinProps:
        return typing.cast(CfnStreamMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_qldb.mixins.CfnStreamPropsMixin.KinesisConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregation_enabled": "aggregationEnabled",
            "stream_arn": "streamArn",
        },
    )
    class KinesisConfigurationProperty:
        def __init__(
            self,
            *,
            aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            stream_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration settings of the Amazon Kinesis Data Streams destination for an Amazon QLDB journal stream.

            :param aggregation_enabled: Enables QLDB to publish multiple data records in a single Kinesis Data Streams record, increasing the number of records sent per API call. Default: ``True`` .. epigraph:: Record aggregation has important implications for processing records and requires de-aggregation in your stream consumer. To learn more, see `KPL Key Concepts <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-concepts.html>`_ and `Consumer De-aggregation <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-consumer-deaggregation.html>`_ in the *Amazon Kinesis Data Streams Developer Guide* .
            :param stream_arn: The Amazon Resource Name (ARN) of the Kinesis Data Streams resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qldb-stream-kinesisconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_qldb import mixins as qldb_mixins
                
                kinesis_configuration_property = qldb_mixins.CfnStreamPropsMixin.KinesisConfigurationProperty(
                    aggregation_enabled=False,
                    stream_arn="streamArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__460985055827e76d8768105759afd124184c871620ccb9e72756b08abdcc54fc)
                check_type(argname="argument aggregation_enabled", value=aggregation_enabled, expected_type=type_hints["aggregation_enabled"])
                check_type(argname="argument stream_arn", value=stream_arn, expected_type=type_hints["stream_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregation_enabled is not None:
                self._values["aggregation_enabled"] = aggregation_enabled
            if stream_arn is not None:
                self._values["stream_arn"] = stream_arn

        @builtins.property
        def aggregation_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Enables QLDB to publish multiple data records in a single Kinesis Data Streams record, increasing the number of records sent per API call.

            Default: ``True``
            .. epigraph::

               Record aggregation has important implications for processing records and requires de-aggregation in your stream consumer. To learn more, see `KPL Key Concepts <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-concepts.html>`_ and `Consumer De-aggregation <https://docs.aws.amazon.com/streams/latest/dev/kinesis-kpl-consumer-deaggregation.html>`_ in the *Amazon Kinesis Data Streams Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qldb-stream-kinesisconfiguration.html#cfn-qldb-stream-kinesisconfiguration-aggregationenabled
            '''
            result = self._values.get("aggregation_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def stream_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Kinesis Data Streams resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-qldb-stream-kinesisconfiguration.html#cfn-qldb-stream-kinesisconfiguration-streamarn
            '''
            result = self._values.get("stream_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnLedgerMixinProps",
    "CfnLedgerPropsMixin",
    "CfnStreamMixinProps",
    "CfnStreamPropsMixin",
]

publication.publish()

def _typecheckingstub__364626c801033c5fd29b84dbcf27e3782014ef2ab7dc992fcb372b7a5159ceb8(
    *,
    deletion_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    kms_key: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    permissions_mode: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f85eca9d1b7582bb0fe82e5f3a0fe3e55b05cec637b237147e7abf90aeee8b5(
    props: typing.Union[CfnLedgerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7942e90a2eb705cfe30d7c1e8b11c09d96493212b6b8ed614d504c910938f4d2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6050b30d754f1283668c713f839d18cb4e922a7c1260ac658192880fc47c4b71(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e48d609d9e222e1e7e58a60dd44228c35ca0c38abce687bd47956a47e141909(
    *,
    exclusive_end_time: typing.Optional[builtins.str] = None,
    inclusive_start_time: typing.Optional[builtins.str] = None,
    kinesis_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStreamPropsMixin.KinesisConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ledger_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    stream_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c9655cccf635169d2e8038e073e8f183e1ff016055c83f3404b779cc9c0e0b(
    props: typing.Union[CfnStreamMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59924db37f52e293ba88cc89d5a077d4b8b71b36b34875adaa1a8b7374dc404(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64dc7aeb7889287c65ef4efd2ebc3fc6a7c7fa365bbed5e161416d4be2931284(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460985055827e76d8768105759afd124184c871620ccb9e72756b08abdcc54fc(
    *,
    aggregation_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    stream_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
