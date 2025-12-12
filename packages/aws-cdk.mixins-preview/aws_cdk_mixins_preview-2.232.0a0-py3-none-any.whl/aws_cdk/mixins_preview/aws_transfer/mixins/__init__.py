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
import aws_cdk.interfaces.aws_kinesisfirehose as _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d
import aws_cdk.interfaces.aws_logs as _aws_cdk_interfaces_aws_logs_ceddda9d
import aws_cdk.interfaces.aws_s3 as _aws_cdk_interfaces_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8
from ...aws_logs import ILogsDelivery as _ILogsDelivery_0d3c9e29
from ...core import IMixin as _IMixin_11e4b965, Mixin as _Mixin_a69446c0
from ...mixins import (
    CfnPropertyMixinOptions as _CfnPropertyMixinOptions_9cbff649,
    PropertyMergeStrategy as _PropertyMergeStrategy_49c157e8,
)


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnAgreementMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_role": "accessRole",
        "base_directory": "baseDirectory",
        "custom_directories": "customDirectories",
        "description": "description",
        "enforce_message_signing": "enforceMessageSigning",
        "local_profile_id": "localProfileId",
        "partner_profile_id": "partnerProfileId",
        "preserve_filename": "preserveFilename",
        "server_id": "serverId",
        "status": "status",
        "tags": "tags",
    },
)
class CfnAgreementMixinProps:
    def __init__(
        self,
        *,
        access_role: typing.Optional[builtins.str] = None,
        base_directory: typing.Optional[builtins.str] = None,
        custom_directories: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnAgreementPropsMixin.CustomDirectoriesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enforce_message_signing: typing.Optional[builtins.str] = None,
        local_profile_id: typing.Optional[builtins.str] = None,
        partner_profile_id: typing.Optional[builtins.str] = None,
        preserve_filename: typing.Optional[builtins.str] = None,
        server_id: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnAgreementPropsMixin.

        :param access_role: Connectors are used to send files using either the AS2 or SFTP protocol. For the access role, provide the Amazon Resource Name (ARN) of the AWS Identity and Access Management role to use. *For AS2 connectors* With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` . If you are using Basic authentication for your AS2 connector, the access role requires the ``secretsmanager:GetSecretValue`` permission for the secret. If the secret is encrypted using a customer-managed key instead of the AWS managed key in Secrets Manager, then the role also needs the ``kms:Decrypt`` permission for that key. *For SFTP connectors* Make sure that the access role provides read and write access to the parent directory of the file location that's used in the ``StartFileTransfer`` request. Additionally, make sure that the role provides ``secretsmanager:GetSecretValue`` permission to AWS Secrets Manager .
        :param base_directory: The landing directory (folder) for files that are transferred by using the AS2 protocol.
        :param custom_directories: A ``CustomDirectoriesType`` structure. This structure specifies custom directories for storing various AS2 message files. You can specify directories for the following types of files. - Failed files - MDN files - Payload files - Status files - Temporary files
        :param description: The name or short description that's used to identify the agreement.
        :param enforce_message_signing: Determines whether or not unsigned messages from your trading partners will be accepted. - ``ENABLED`` : Transfer Family rejects unsigned messages from your trading partner. - ``DISABLED`` (default value): Transfer Family accepts unsigned messages from your trading partner.
        :param local_profile_id: A unique identifier for the AS2 local profile.
        :param partner_profile_id: A unique identifier for the partner profile used in the agreement.
        :param preserve_filename: Determines whether or not Transfer Family appends a unique string of characters to the end of the AS2 message payload filename when saving it. - ``ENABLED`` : the filename provided by your trading parter is preserved when the file is saved. - ``DISABLED`` (default value): when Transfer Family saves the file, the filename is adjusted, as described in `File names and locations <https://docs.aws.amazon.com/transfer/latest/userguide/send-as2-messages.html#file-names-as2>`_ .
        :param server_id: A system-assigned unique identifier for a server instance. This identifier indicates the specific server that the agreement uses.
        :param status: The current status of the agreement, either ``ACTIVE`` or ``INACTIVE`` .
        :param tags: Key-value pairs that can be used to group and search for agreements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            cfn_agreement_mixin_props = transfer_mixins.CfnAgreementMixinProps(
                access_role="accessRole",
                base_directory="baseDirectory",
                custom_directories=transfer_mixins.CfnAgreementPropsMixin.CustomDirectoriesProperty(
                    failed_files_directory="failedFilesDirectory",
                    mdn_files_directory="mdnFilesDirectory",
                    payload_files_directory="payloadFilesDirectory",
                    status_files_directory="statusFilesDirectory",
                    temporary_files_directory="temporaryFilesDirectory"
                ),
                description="description",
                enforce_message_signing="enforceMessageSigning",
                local_profile_id="localProfileId",
                partner_profile_id="partnerProfileId",
                preserve_filename="preserveFilename",
                server_id="serverId",
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69081525ccc245470012ee56728763c06bee4c625b9ee7161d0bb4243e01079b)
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument base_directory", value=base_directory, expected_type=type_hints["base_directory"])
            check_type(argname="argument custom_directories", value=custom_directories, expected_type=type_hints["custom_directories"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enforce_message_signing", value=enforce_message_signing, expected_type=type_hints["enforce_message_signing"])
            check_type(argname="argument local_profile_id", value=local_profile_id, expected_type=type_hints["local_profile_id"])
            check_type(argname="argument partner_profile_id", value=partner_profile_id, expected_type=type_hints["partner_profile_id"])
            check_type(argname="argument preserve_filename", value=preserve_filename, expected_type=type_hints["preserve_filename"])
            check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_role is not None:
            self._values["access_role"] = access_role
        if base_directory is not None:
            self._values["base_directory"] = base_directory
        if custom_directories is not None:
            self._values["custom_directories"] = custom_directories
        if description is not None:
            self._values["description"] = description
        if enforce_message_signing is not None:
            self._values["enforce_message_signing"] = enforce_message_signing
        if local_profile_id is not None:
            self._values["local_profile_id"] = local_profile_id
        if partner_profile_id is not None:
            self._values["partner_profile_id"] = partner_profile_id
        if preserve_filename is not None:
            self._values["preserve_filename"] = preserve_filename
        if server_id is not None:
            self._values["server_id"] = server_id
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def access_role(self) -> typing.Optional[builtins.str]:
        '''Connectors are used to send files using either the AS2 or SFTP protocol.

        For the access role, provide the Amazon Resource Name (ARN) of the AWS Identity and Access Management role to use.

        *For AS2 connectors*

        With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .

        If you are using Basic authentication for your AS2 connector, the access role requires the ``secretsmanager:GetSecretValue`` permission for the secret. If the secret is encrypted using a customer-managed key instead of the AWS managed key in Secrets Manager, then the role also needs the ``kms:Decrypt`` permission for that key.

        *For SFTP connectors*

        Make sure that the access role provides read and write access to the parent directory of the file location that's used in the ``StartFileTransfer`` request. Additionally, make sure that the role provides ``secretsmanager:GetSecretValue`` permission to AWS Secrets Manager .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-accessrole
        '''
        result = self._values.get("access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def base_directory(self) -> typing.Optional[builtins.str]:
        '''The landing directory (folder) for files that are transferred by using the AS2 protocol.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-basedirectory
        '''
        result = self._values.get("base_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_directories(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAgreementPropsMixin.CustomDirectoriesProperty"]]:
        '''A ``CustomDirectoriesType`` structure.

        This structure specifies custom directories for storing various AS2 message files. You can specify directories for the following types of files.

        - Failed files
        - MDN files
        - Payload files
        - Status files
        - Temporary files

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-customdirectories
        '''
        result = self._values.get("custom_directories")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnAgreementPropsMixin.CustomDirectoriesProperty"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The name or short description that's used to identify the agreement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enforce_message_signing(self) -> typing.Optional[builtins.str]:
        '''Determines whether or not unsigned messages from your trading partners will be accepted.

        - ``ENABLED`` : Transfer Family rejects unsigned messages from your trading partner.
        - ``DISABLED`` (default value): Transfer Family accepts unsigned messages from your trading partner.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-enforcemessagesigning
        '''
        result = self._values.get("enforce_message_signing")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_profile_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the AS2 local profile.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-localprofileid
        '''
        result = self._values.get("local_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def partner_profile_id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the partner profile used in the agreement.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-partnerprofileid
        '''
        result = self._values.get("partner_profile_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_filename(self) -> typing.Optional[builtins.str]:
        '''Determines whether or not Transfer Family appends a unique string of characters to the end of the AS2 message payload filename when saving it.

        - ``ENABLED`` : the filename provided by your trading parter is preserved when the file is saved.
        - ``DISABLED`` (default value): when Transfer Family saves the file, the filename is adjusted, as described in `File names and locations <https://docs.aws.amazon.com/transfer/latest/userguide/send-as2-messages.html#file-names-as2>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-preservefilename
        '''
        result = self._values.get("preserve_filename")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_id(self) -> typing.Optional[builtins.str]:
        '''A system-assigned unique identifier for a server instance.

        This identifier indicates the specific server that the agreement uses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-serverid
        '''
        result = self._values.get("server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The current status of the agreement, either ``ACTIVE`` or ``INACTIVE`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for agreements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html#cfn-transfer-agreement-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAgreementMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnAgreementPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnAgreementPropsMixin",
):
    '''Creates an agreement.

    An agreement is a bilateral trading partner agreement, or partnership, between an AWS Transfer Family server and an AS2 process. The agreement defines the file and message transfer relationship between the server and the AS2 process. To define an agreement, Transfer Family combines a server, local profile, partner profile, certificate, and other attributes.

    The partner is identified with the ``PartnerProfileId`` , and the AS2 process is identified with the ``LocalProfileId`` .
    .. epigraph::

       Specify *either* ``BaseDirectory`` or ``CustomDirectories`` , but not both. Specifying both causes the command to fail.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-agreement.html
    :cloudformationResource: AWS::Transfer::Agreement
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_agreement_props_mixin = transfer_mixins.CfnAgreementPropsMixin(transfer_mixins.CfnAgreementMixinProps(
            access_role="accessRole",
            base_directory="baseDirectory",
            custom_directories=transfer_mixins.CfnAgreementPropsMixin.CustomDirectoriesProperty(
                failed_files_directory="failedFilesDirectory",
                mdn_files_directory="mdnFilesDirectory",
                payload_files_directory="payloadFilesDirectory",
                status_files_directory="statusFilesDirectory",
                temporary_files_directory="temporaryFilesDirectory"
            ),
            description="description",
            enforce_message_signing="enforceMessageSigning",
            local_profile_id="localProfileId",
            partner_profile_id="partnerProfileId",
            preserve_filename="preserveFilename",
            server_id="serverId",
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
        props: typing.Union[CfnAgreementMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Transfer::Agreement``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf9ee4277584841d8c416b64df8c07fd337444c69ee24b2a8371bbd20831c51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__93c3b7d14a59b13056f08fb48e04a5b50d33aa1f57fce368436d692a044048da)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984009c8037cf7f05f3775b89fb922d3fec08dbe368c34eca6440d2373b51b79)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnAgreementMixinProps:
        return typing.cast(CfnAgreementMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnAgreementPropsMixin.CustomDirectoriesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failed_files_directory": "failedFilesDirectory",
            "mdn_files_directory": "mdnFilesDirectory",
            "payload_files_directory": "payloadFilesDirectory",
            "status_files_directory": "statusFilesDirectory",
            "temporary_files_directory": "temporaryFilesDirectory",
        },
    )
    class CustomDirectoriesProperty:
        def __init__(
            self,
            *,
            failed_files_directory: typing.Optional[builtins.str] = None,
            mdn_files_directory: typing.Optional[builtins.str] = None,
            payload_files_directory: typing.Optional[builtins.str] = None,
            status_files_directory: typing.Optional[builtins.str] = None,
            temporary_files_directory: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a separate directory for each type of file to store for an AS2 message.

            :param failed_files_directory: Specifies a location to store the failed files for an AS2 message.
            :param mdn_files_directory: Specifies a location to store the MDN file for an AS2 message.
            :param payload_files_directory: Specifies a location to store the payload file for an AS2 message.
            :param status_files_directory: Specifies a location to store the status file for an AS2 message.
            :param temporary_files_directory: Specifies a location to store the temporary processing file for an AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-agreement-customdirectories.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                custom_directories_property = transfer_mixins.CfnAgreementPropsMixin.CustomDirectoriesProperty(
                    failed_files_directory="failedFilesDirectory",
                    mdn_files_directory="mdnFilesDirectory",
                    payload_files_directory="payloadFilesDirectory",
                    status_files_directory="statusFilesDirectory",
                    temporary_files_directory="temporaryFilesDirectory"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ed407a6bd6348e690858794f859e516c7fea6ab07d591e9ebe1a74c28ba4977)
                check_type(argname="argument failed_files_directory", value=failed_files_directory, expected_type=type_hints["failed_files_directory"])
                check_type(argname="argument mdn_files_directory", value=mdn_files_directory, expected_type=type_hints["mdn_files_directory"])
                check_type(argname="argument payload_files_directory", value=payload_files_directory, expected_type=type_hints["payload_files_directory"])
                check_type(argname="argument status_files_directory", value=status_files_directory, expected_type=type_hints["status_files_directory"])
                check_type(argname="argument temporary_files_directory", value=temporary_files_directory, expected_type=type_hints["temporary_files_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failed_files_directory is not None:
                self._values["failed_files_directory"] = failed_files_directory
            if mdn_files_directory is not None:
                self._values["mdn_files_directory"] = mdn_files_directory
            if payload_files_directory is not None:
                self._values["payload_files_directory"] = payload_files_directory
            if status_files_directory is not None:
                self._values["status_files_directory"] = status_files_directory
            if temporary_files_directory is not None:
                self._values["temporary_files_directory"] = temporary_files_directory

        @builtins.property
        def failed_files_directory(self) -> typing.Optional[builtins.str]:
            '''Specifies a location to store the failed files for an AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-agreement-customdirectories.html#cfn-transfer-agreement-customdirectories-failedfilesdirectory
            '''
            result = self._values.get("failed_files_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mdn_files_directory(self) -> typing.Optional[builtins.str]:
            '''Specifies a location to store the MDN file for an AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-agreement-customdirectories.html#cfn-transfer-agreement-customdirectories-mdnfilesdirectory
            '''
            result = self._values.get("mdn_files_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def payload_files_directory(self) -> typing.Optional[builtins.str]:
            '''Specifies a location to store the payload file for an AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-agreement-customdirectories.html#cfn-transfer-agreement-customdirectories-payloadfilesdirectory
            '''
            result = self._values.get("payload_files_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status_files_directory(self) -> typing.Optional[builtins.str]:
            '''Specifies a location to store the status file for an AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-agreement-customdirectories.html#cfn-transfer-agreement-customdirectories-statusfilesdirectory
            '''
            result = self._values.get("status_files_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def temporary_files_directory(self) -> typing.Optional[builtins.str]:
            '''Specifies a location to store the temporary processing file for an AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-agreement-customdirectories.html#cfn-transfer-agreement-customdirectories-temporaryfilesdirectory
            '''
            result = self._values.get("temporary_files_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomDirectoriesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnCertificateMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "active_date": "activeDate",
        "certificate": "certificate",
        "certificate_chain": "certificateChain",
        "description": "description",
        "inactive_date": "inactiveDate",
        "private_key": "privateKey",
        "tags": "tags",
        "usage": "usage",
    },
)
class CfnCertificateMixinProps:
    def __init__(
        self,
        *,
        active_date: typing.Optional[builtins.str] = None,
        certificate: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        inactive_date: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        usage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnCertificatePropsMixin.

        :param active_date: An optional date that specifies when the certificate becomes active. If you do not specify a value, ``ActiveDate`` takes the same value as ``NotBeforeDate`` , which is specified by the CA.
        :param certificate: The file name for the certificate.
        :param certificate_chain: The list of certificates that make up the chain for the certificate.
        :param description: The name or description that's used to identity the certificate.
        :param inactive_date: An optional date that specifies when the certificate becomes inactive. If you do not specify a value, ``InactiveDate`` takes the same value as ``NotAfterDate`` , which is specified by the CA.
        :param private_key: The file that contains the private key for the certificate that's being imported.
        :param tags: Key-value pairs that can be used to group and search for certificates.
        :param usage: Specifies how this certificate is used. It can be used in the following ways:. - ``SIGNING`` : For signing AS2 messages - ``ENCRYPTION`` : For encrypting AS2 messages - ``TLS`` : For securing AS2 communications sent over HTTPS

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            cfn_certificate_mixin_props = transfer_mixins.CfnCertificateMixinProps(
                active_date="activeDate",
                certificate="certificate",
                certificate_chain="certificateChain",
                description="description",
                inactive_date="inactiveDate",
                private_key="privateKey",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                usage="usage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1501f7486d5313b59c737955e1b87fffc6cc048843e524bf433288836f149cc)
            check_type(argname="argument active_date", value=active_date, expected_type=type_hints["active_date"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument inactive_date", value=inactive_date, expected_type=type_hints["inactive_date"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_date is not None:
            self._values["active_date"] = active_date
        if certificate is not None:
            self._values["certificate"] = certificate
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if description is not None:
            self._values["description"] = description
        if inactive_date is not None:
            self._values["inactive_date"] = inactive_date
        if private_key is not None:
            self._values["private_key"] = private_key
        if tags is not None:
            self._values["tags"] = tags
        if usage is not None:
            self._values["usage"] = usage

    @builtins.property
    def active_date(self) -> typing.Optional[builtins.str]:
        '''An optional date that specifies when the certificate becomes active.

        If you do not specify a value, ``ActiveDate`` takes the same value as ``NotBeforeDate`` , which is specified by the CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-activedate
        '''
        result = self._values.get("active_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The file name for the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The list of certificates that make up the chain for the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The name or description that's used to identity the certificate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inactive_date(self) -> typing.Optional[builtins.str]:
        '''An optional date that specifies when the certificate becomes inactive.

        If you do not specify a value, ``InactiveDate`` takes the same value as ``NotAfterDate`` , which is specified by the CA.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-inactivedate
        '''
        result = self._values.get("inactive_date")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The file that contains the private key for the certificate that's being imported.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for certificates.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def usage(self) -> typing.Optional[builtins.str]:
        '''Specifies how this certificate is used. It can be used in the following ways:.

        - ``SIGNING`` : For signing AS2 messages
        - ``ENCRYPTION`` : For encrypting AS2 messages
        - ``TLS`` : For securing AS2 communications sent over HTTPS

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html#cfn-transfer-certificate-usage
        '''
        result = self._values.get("usage")
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
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnCertificatePropsMixin",
):
    '''Imports the signing and encryption certificates that you need to create local (AS2) profiles and partner profiles.

    You can import both the certificate and its chain in the ``Certificate`` parameter.

    After importing a certificate, AWS Transfer Family automatically creates a Amazon CloudWatch metric called ``DaysUntilExpiry`` that tracks the number of days until the certificate expires. The metric is based on the ``InactiveDate`` parameter and is published daily in the ``AWS/Transfer`` namespace.
    .. epigraph::

       It can take up to a full day after importing a certificate for Transfer Family to emit the ``DaysUntilExpiry`` metric to your account. > If you use the ``Certificate`` parameter to upload both the certificate and its chain, don't use the ``CertificateChain`` parameter.

    *CloudWatch monitoring*

    The ``DaysUntilExpiry`` metric includes the following specifications:

    - *Units:* Count (days)
    - *Dimensions:* ``CertificateId`` (always present), ``Description`` (if provided during certificate import)
    - *Statistics:* Minimum, Maximum, Average
    - *Frequency:* Published daily

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-certificate.html
    :cloudformationResource: AWS::Transfer::Certificate
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_certificate_props_mixin = transfer_mixins.CfnCertificatePropsMixin(transfer_mixins.CfnCertificateMixinProps(
            active_date="activeDate",
            certificate="certificate",
            certificate_chain="certificateChain",
            description="description",
            inactive_date="inactiveDate",
            private_key="privateKey",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            usage="usage"
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
        '''Create a mixin to apply properties to ``AWS::Transfer::Certificate``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a023a88da1e7fb1d8b0004b3b470a502ce63e40ccbee86c6370f1e876f9d5816)
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c1b96c8442a81e6f5ab40067780d3c2cb0f409b46ae59a25512e158c61ce67)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0fc50d5d96f262b80cd2d6ca5a83d90b6a120478a3c6cbde1af549e8480b8f)
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
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnConnectorMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_role": "accessRole",
        "as2_config": "as2Config",
        "egress_config": "egressConfig",
        "egress_type": "egressType",
        "logging_role": "loggingRole",
        "security_policy_name": "securityPolicyName",
        "sftp_config": "sftpConfig",
        "tags": "tags",
        "url": "url",
    },
)
class CfnConnectorMixinProps:
    def __init__(
        self,
        *,
        access_role: typing.Optional[builtins.str] = None,
        as2_config: typing.Any = None,
        egress_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ConnectorEgressConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        egress_type: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        sftp_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.SftpConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnConnectorPropsMixin.

        :param access_role: Connectors are used to send files using either the AS2 or SFTP protocol. For the access role, provide the Amazon Resource Name (ARN) of the AWS Identity and Access Management role to use. *For AS2 connectors* With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` . If you are using Basic authentication for your AS2 connector, the access role requires the ``secretsmanager:GetSecretValue`` permission for the secret. If the secret is encrypted using a customer-managed key instead of the AWS managed key in Secrets Manager, then the role also needs the ``kms:Decrypt`` permission for that key. *For SFTP connectors* Make sure that the access role provides read and write access to the parent directory of the file location that's used in the ``StartFileTransfer`` request. Additionally, make sure that the role provides ``secretsmanager:GetSecretValue`` permission to AWS Secrets Manager .
        :param as2_config: A structure that contains the parameters for an AS2 connector object.
        :param egress_config: Current egress configuration of the connector, showing how traffic is routed to the SFTP server. Contains VPC Lattice settings when using VPC_LATTICE egress type. When using the VPC_LATTICE egress type, AWS Transfer Family uses a managed Service Network to simplify the resource sharing process.
        :param egress_type: Type of egress configuration for the connector. SERVICE_MANAGED uses Transfer Family managed NAT gateways, while VPC_LATTICE routes traffic through customer VPCs using VPC Lattice.
        :param logging_role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a connector to turn on CloudWatch logging for Amazon S3 events. When set, you can view connector activity in your CloudWatch logs.
        :param security_policy_name: The text name of the security policy for the specified connector.
        :param sftp_config: A structure that contains the parameters for an SFTP connector object.
        :param tags: Key-value pairs that can be used to group and search for connectors.
        :param url: The URL of the partner's AS2 or SFTP endpoint. When creating AS2 connectors or service-managed SFTP connectors (connectors without egress configuration), you must provide a URL to specify the remote server endpoint. For VPC Lattice type connectors, the URL must be null.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            # as2_config: Any
            
            cfn_connector_mixin_props = transfer_mixins.CfnConnectorMixinProps(
                access_role="accessRole",
                as2_config=as2_config,
                egress_config=transfer_mixins.CfnConnectorPropsMixin.ConnectorEgressConfigProperty(
                    vpc_lattice=transfer_mixins.CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty(
                        port_number=123,
                        resource_configuration_arn="resourceConfigurationArn"
                    )
                ),
                egress_type="egressType",
                logging_role="loggingRole",
                security_policy_name="securityPolicyName",
                sftp_config=transfer_mixins.CfnConnectorPropsMixin.SftpConfigProperty(
                    max_concurrent_connections=123,
                    trusted_host_keys=["trustedHostKeys"],
                    user_secret_id="userSecretId"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                url="url"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc0508e75702fe89770cfc3b90c3d58ef5edbf1b0c9444864e4c6f0a8003994)
            check_type(argname="argument access_role", value=access_role, expected_type=type_hints["access_role"])
            check_type(argname="argument as2_config", value=as2_config, expected_type=type_hints["as2_config"])
            check_type(argname="argument egress_config", value=egress_config, expected_type=type_hints["egress_config"])
            check_type(argname="argument egress_type", value=egress_type, expected_type=type_hints["egress_type"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument security_policy_name", value=security_policy_name, expected_type=type_hints["security_policy_name"])
            check_type(argname="argument sftp_config", value=sftp_config, expected_type=type_hints["sftp_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_role is not None:
            self._values["access_role"] = access_role
        if as2_config is not None:
            self._values["as2_config"] = as2_config
        if egress_config is not None:
            self._values["egress_config"] = egress_config
        if egress_type is not None:
            self._values["egress_type"] = egress_type
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if sftp_config is not None:
            self._values["sftp_config"] = sftp_config
        if tags is not None:
            self._values["tags"] = tags
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def access_role(self) -> typing.Optional[builtins.str]:
        '''Connectors are used to send files using either the AS2 or SFTP protocol.

        For the access role, provide the Amazon Resource Name (ARN) of the AWS Identity and Access Management role to use.

        *For AS2 connectors*

        With AS2, you can send files by calling ``StartFileTransfer`` and specifying the file paths in the request parameter, ``SendFilePaths`` . We use the file’s parent directory (for example, for ``--send-file-paths /bucket/dir/file.txt`` , parent directory is ``/bucket/dir/`` ) to temporarily store a processed AS2 message file, store the MDN when we receive them from the partner, and write a final JSON file containing relevant metadata of the transmission. So, the ``AccessRole`` needs to provide read and write access to the parent directory of the file location used in the ``StartFileTransfer`` request. Additionally, you need to provide read and write access to the parent directory of the files that you intend to send with ``StartFileTransfer`` .

        If you are using Basic authentication for your AS2 connector, the access role requires the ``secretsmanager:GetSecretValue`` permission for the secret. If the secret is encrypted using a customer-managed key instead of the AWS managed key in Secrets Manager, then the role also needs the ``kms:Decrypt`` permission for that key.

        *For SFTP connectors*

        Make sure that the access role provides read and write access to the parent directory of the file location that's used in the ``StartFileTransfer`` request. Additionally, make sure that the role provides ``secretsmanager:GetSecretValue`` permission to AWS Secrets Manager .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-accessrole
        '''
        result = self._values.get("access_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def as2_config(self) -> typing.Any:
        '''A structure that contains the parameters for an AS2 connector object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-as2config
        '''
        result = self._values.get("as2_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def egress_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ConnectorEgressConfigProperty"]]:
        '''Current egress configuration of the connector, showing how traffic is routed to the SFTP server.

        Contains VPC Lattice settings when using VPC_LATTICE egress type.

        When using the VPC_LATTICE egress type, AWS Transfer Family uses a managed Service Network to simplify the resource sharing process.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-egressconfig
        '''
        result = self._values.get("egress_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ConnectorEgressConfigProperty"]], result)

    @builtins.property
    def egress_type(self) -> typing.Optional[builtins.str]:
        '''Type of egress configuration for the connector.

        SERVICE_MANAGED uses Transfer Family managed NAT gateways, while VPC_LATTICE routes traffic through customer VPCs using VPC Lattice.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-egresstype
        '''
        result = self._values.get("egress_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a connector to turn on CloudWatch logging for Amazon S3 events.

        When set, you can view connector activity in your CloudWatch logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-loggingrole
        '''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''The text name of the security policy for the specified connector.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-securitypolicyname
        '''
        result = self._values.get("security_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sftp_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.SftpConfigProperty"]]:
        '''A structure that contains the parameters for an SFTP connector object.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-sftpconfig
        '''
        result = self._values.get("sftp_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.SftpConfigProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for connectors.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL of the partner's AS2 or SFTP endpoint.

        When creating AS2 connectors or service-managed SFTP connectors (connectors without egress configuration), you must provide a URL to specify the remote server endpoint. For VPC Lattice type connectors, the URL must be null.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html#cfn-transfer-connector-url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnConnectorPropsMixin",
):
    '''Creates the connector, which captures the parameters for a connection for the AS2 or SFTP protocol.

    For AS2, the connector is required for sending files to an externally hosted AS2 server. For SFTP, the connector is required when sending files to an SFTP server or receiving files from an SFTP server. For more details about connectors, see `Configure AS2 connectors <https://docs.aws.amazon.com/transfer/latest/userguide/configure-as2-connector.html>`_ and `Create SFTP connectors <https://docs.aws.amazon.com/transfer/latest/userguide/configure-sftp-connector.html>`_ .
    .. epigraph::

       You must specify exactly one configuration object: either for AS2 ( ``As2Config`` ) or SFTP ( ``SftpConfig`` ).

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-connector.html
    :cloudformationResource: AWS::Transfer::Connector
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        # as2_config: Any
        
        cfn_connector_props_mixin = transfer_mixins.CfnConnectorPropsMixin(transfer_mixins.CfnConnectorMixinProps(
            access_role="accessRole",
            as2_config=as2_config,
            egress_config=transfer_mixins.CfnConnectorPropsMixin.ConnectorEgressConfigProperty(
                vpc_lattice=transfer_mixins.CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty(
                    port_number=123,
                    resource_configuration_arn="resourceConfigurationArn"
                )
            ),
            egress_type="egressType",
            logging_role="loggingRole",
            security_policy_name="securityPolicyName",
            sftp_config=transfer_mixins.CfnConnectorPropsMixin.SftpConfigProperty(
                max_concurrent_connections=123,
                trusted_host_keys=["trustedHostKeys"],
                user_secret_id="userSecretId"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            url="url"
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
        '''Create a mixin to apply properties to ``AWS::Transfer::Connector``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d0a380f1de06a6f3212525c0f0c68974e5ceeca99257cc6bff28296979a2470)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8af4a003c083a71a1d3e9cb70db4b3d454448b977c0833147fbfce53b9ff48e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c55594f024abbed39743f7a4ee5613b32c46b506e4f55d756da9e079dff0c05)
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
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnConnectorPropsMixin.As2ConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "basic_auth_secret_id": "basicAuthSecretId",
            "compression": "compression",
            "encryption_algorithm": "encryptionAlgorithm",
            "local_profile_id": "localProfileId",
            "mdn_response": "mdnResponse",
            "mdn_signing_algorithm": "mdnSigningAlgorithm",
            "message_subject": "messageSubject",
            "partner_profile_id": "partnerProfileId",
            "preserve_content_type": "preserveContentType",
            "signing_algorithm": "signingAlgorithm",
        },
    )
    class As2ConfigProperty:
        def __init__(
            self,
            *,
            basic_auth_secret_id: typing.Optional[builtins.str] = None,
            compression: typing.Optional[builtins.str] = None,
            encryption_algorithm: typing.Optional[builtins.str] = None,
            local_profile_id: typing.Optional[builtins.str] = None,
            mdn_response: typing.Optional[builtins.str] = None,
            mdn_signing_algorithm: typing.Optional[builtins.str] = None,
            message_subject: typing.Optional[builtins.str] = None,
            partner_profile_id: typing.Optional[builtins.str] = None,
            preserve_content_type: typing.Optional[builtins.str] = None,
            signing_algorithm: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the parameters for an AS2 connector object.

            :param basic_auth_secret_id: Provides Basic authentication support to the AS2 Connectors API. To use Basic authentication, you must provide the name or Amazon Resource Name (ARN) of a secret in AWS Secrets Manager . The default value for this parameter is ``null`` , which indicates that Basic authentication is not enabled for the connector. If the connector should use Basic authentication, the secret needs to be in the following format: ``{ "Username": "user-name", "Password": "user-password" }`` Replace ``user-name`` and ``user-password`` with the credentials for the actual user that is being authenticated. Note the following: - You are storing these credentials in Secrets Manager, *not passing them directly* into this API. - If you are using the API, SDKs, or CloudFormation to configure your connector, then you must create the secret before you can enable Basic authentication. However, if you are using the AWS management console, you can have the system create the secret for you. If you have previously enabled Basic authentication for a connector, you can disable it by using the ``UpdateConnector`` API call. For example, if you are using the CLI, you can run the following command to remove Basic authentication: ``update-connector --connector-id my-connector-id --as2-config 'BasicAuthSecretId=""'``
            :param compression: Specifies whether the AS2 file is compressed.
            :param encryption_algorithm: The algorithm that is used to encrypt the file. Note the following: - Do not use the ``DES_EDE3_CBC`` algorithm unless you must support a legacy client that requires it, as it is a weak encryption algorithm. - You can only specify ``NONE`` if the URL for your connector uses HTTPS. Using HTTPS ensures that no traffic is sent in clear text.
            :param local_profile_id: A unique identifier for the AS2 local profile.
            :param mdn_response: Used for outbound requests (from an AWS Transfer Family connector to a partner AS2 server) to determine whether the partner response for transfers is synchronous or asynchronous. Specify either of the following values: - ``SYNC`` : The system expects a synchronous MDN response, confirming that the file was transferred successfully (or not). - ``NONE`` : Specifies that no MDN response is required.
            :param mdn_signing_algorithm: The signing algorithm for the MDN response. .. epigraph:: If set to DEFAULT (or not set at all), the value for ``SigningAlgorithm`` is used.
            :param message_subject: Used as the ``Subject`` HTTP header attribute in AS2 messages that are being sent with the connector.
            :param partner_profile_id: A unique identifier for the partner profile for the connector.
            :param preserve_content_type: Specifies whether to use the AWS S3 object content-type as the content-type for the AS2 message.
            :param signing_algorithm: The algorithm that is used to sign the AS2 messages sent with the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                as2_config_property = transfer_mixins.CfnConnectorPropsMixin.As2ConfigProperty(
                    basic_auth_secret_id="basicAuthSecretId",
                    compression="compression",
                    encryption_algorithm="encryptionAlgorithm",
                    local_profile_id="localProfileId",
                    mdn_response="mdnResponse",
                    mdn_signing_algorithm="mdnSigningAlgorithm",
                    message_subject="messageSubject",
                    partner_profile_id="partnerProfileId",
                    preserve_content_type="preserveContentType",
                    signing_algorithm="signingAlgorithm"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eb071ac4a495fc03e6fa98ff69e60ba390f28bf9ca26809d3f2da14cf8b3cb31)
                check_type(argname="argument basic_auth_secret_id", value=basic_auth_secret_id, expected_type=type_hints["basic_auth_secret_id"])
                check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
                check_type(argname="argument encryption_algorithm", value=encryption_algorithm, expected_type=type_hints["encryption_algorithm"])
                check_type(argname="argument local_profile_id", value=local_profile_id, expected_type=type_hints["local_profile_id"])
                check_type(argname="argument mdn_response", value=mdn_response, expected_type=type_hints["mdn_response"])
                check_type(argname="argument mdn_signing_algorithm", value=mdn_signing_algorithm, expected_type=type_hints["mdn_signing_algorithm"])
                check_type(argname="argument message_subject", value=message_subject, expected_type=type_hints["message_subject"])
                check_type(argname="argument partner_profile_id", value=partner_profile_id, expected_type=type_hints["partner_profile_id"])
                check_type(argname="argument preserve_content_type", value=preserve_content_type, expected_type=type_hints["preserve_content_type"])
                check_type(argname="argument signing_algorithm", value=signing_algorithm, expected_type=type_hints["signing_algorithm"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if basic_auth_secret_id is not None:
                self._values["basic_auth_secret_id"] = basic_auth_secret_id
            if compression is not None:
                self._values["compression"] = compression
            if encryption_algorithm is not None:
                self._values["encryption_algorithm"] = encryption_algorithm
            if local_profile_id is not None:
                self._values["local_profile_id"] = local_profile_id
            if mdn_response is not None:
                self._values["mdn_response"] = mdn_response
            if mdn_signing_algorithm is not None:
                self._values["mdn_signing_algorithm"] = mdn_signing_algorithm
            if message_subject is not None:
                self._values["message_subject"] = message_subject
            if partner_profile_id is not None:
                self._values["partner_profile_id"] = partner_profile_id
            if preserve_content_type is not None:
                self._values["preserve_content_type"] = preserve_content_type
            if signing_algorithm is not None:
                self._values["signing_algorithm"] = signing_algorithm

        @builtins.property
        def basic_auth_secret_id(self) -> typing.Optional[builtins.str]:
            '''Provides Basic authentication support to the AS2 Connectors API.

            To use Basic authentication, you must provide the name or Amazon Resource Name (ARN) of a secret in AWS Secrets Manager .

            The default value for this parameter is ``null`` , which indicates that Basic authentication is not enabled for the connector.

            If the connector should use Basic authentication, the secret needs to be in the following format:

            ``{ "Username": "user-name", "Password": "user-password" }``

            Replace ``user-name`` and ``user-password`` with the credentials for the actual user that is being authenticated.

            Note the following:

            - You are storing these credentials in Secrets Manager, *not passing them directly* into this API.
            - If you are using the API, SDKs, or CloudFormation to configure your connector, then you must create the secret before you can enable Basic authentication. However, if you are using the AWS management console, you can have the system create the secret for you.

            If you have previously enabled Basic authentication for a connector, you can disable it by using the ``UpdateConnector`` API call. For example, if you are using the CLI, you can run the following command to remove Basic authentication:

            ``update-connector --connector-id my-connector-id --as2-config 'BasicAuthSecretId=""'``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-basicauthsecretid
            '''
            result = self._values.get("basic_auth_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the AS2 file is compressed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-compression
            '''
            result = self._values.get("compression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def encryption_algorithm(self) -> typing.Optional[builtins.str]:
            '''The algorithm that is used to encrypt the file.

            Note the following:

            - Do not use the ``DES_EDE3_CBC`` algorithm unless you must support a legacy client that requires it, as it is a weak encryption algorithm.
            - You can only specify ``NONE`` if the URL for your connector uses HTTPS. Using HTTPS ensures that no traffic is sent in clear text.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-encryptionalgorithm
            '''
            result = self._values.get("encryption_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def local_profile_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the AS2 local profile.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-localprofileid
            '''
            result = self._values.get("local_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mdn_response(self) -> typing.Optional[builtins.str]:
            '''Used for outbound requests (from an AWS Transfer Family connector to a partner AS2 server) to determine whether the partner response for transfers is synchronous or asynchronous.

            Specify either of the following values:

            - ``SYNC`` : The system expects a synchronous MDN response, confirming that the file was transferred successfully (or not).
            - ``NONE`` : Specifies that no MDN response is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-mdnresponse
            '''
            result = self._values.get("mdn_response")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mdn_signing_algorithm(self) -> typing.Optional[builtins.str]:
            '''The signing algorithm for the MDN response.

            .. epigraph::

               If set to DEFAULT (or not set at all), the value for ``SigningAlgorithm`` is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-mdnsigningalgorithm
            '''
            result = self._values.get("mdn_signing_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def message_subject(self) -> typing.Optional[builtins.str]:
            '''Used as the ``Subject`` HTTP header attribute in AS2 messages that are being sent with the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-messagesubject
            '''
            result = self._values.get("message_subject")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def partner_profile_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the partner profile for the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-partnerprofileid
            '''
            result = self._values.get("partner_profile_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def preserve_content_type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether to use the AWS S3 object content-type as the content-type for the AS2 message.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-preservecontenttype
            '''
            result = self._values.get("preserve_content_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def signing_algorithm(self) -> typing.Optional[builtins.str]:
            '''The algorithm that is used to sign the AS2 messages sent with the connector.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-as2config.html#cfn-transfer-connector-as2config-signingalgorithm
            '''
            result = self._values.get("signing_algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "As2ConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnConnectorPropsMixin.ConnectorEgressConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_lattice": "vpcLattice"},
    )
    class ConnectorEgressConfigProperty:
        def __init__(
            self,
            *,
            vpc_lattice: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration structure that defines how traffic is routed from the connector to the SFTP server.

            Contains VPC Lattice settings when using VPC_LATTICE egress type for private connectivity through customer VPCs.

            :param vpc_lattice: VPC_LATTICE configuration for routing connector traffic through customer VPCs. Enables private connectivity to SFTP servers without requiring public internet access or complex network configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-connectoregressconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                connector_egress_config_property = transfer_mixins.CfnConnectorPropsMixin.ConnectorEgressConfigProperty(
                    vpc_lattice=transfer_mixins.CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty(
                        port_number=123,
                        resource_configuration_arn="resourceConfigurationArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__656490d886d172145f69b8d98e70a59952bed873b179e0d251c9b79d758b68cc)
                check_type(argname="argument vpc_lattice", value=vpc_lattice, expected_type=type_hints["vpc_lattice"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_lattice is not None:
                self._values["vpc_lattice"] = vpc_lattice

        @builtins.property
        def vpc_lattice(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty"]]:
            '''VPC_LATTICE configuration for routing connector traffic through customer VPCs.

            Enables private connectivity to SFTP servers without requiring public internet access or complex network configurations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-connectoregressconfig.html#cfn-transfer-connector-connectoregressconfig-vpclattice
            '''
            result = self._values.get("vpc_lattice")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorEgressConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port_number": "portNumber",
            "resource_configuration_arn": "resourceConfigurationArn",
        },
    )
    class ConnectorVpcLatticeEgressConfigProperty:
        def __init__(
            self,
            *,
            port_number: typing.Optional[jsii.Number] = None,
            resource_configuration_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''VPC_LATTICE egress configuration that specifies the Resource Configuration ARN and port for connecting to SFTP servers through customer VPCs.

            Requires a valid Resource Configuration with appropriate network access.

            :param port_number: Port number for connecting to the SFTP server through VPC_LATTICE. Defaults to 22 if not specified. Must match the port on which the target SFTP server is listening.
            :param resource_configuration_arn: ARN of the VPC_LATTICE Resource Configuration that defines the target SFTP server location. Must point to a valid Resource Configuration in the customer's VPC with appropriate network connectivity to the SFTP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-connectorvpclatticeegressconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                connector_vpc_lattice_egress_config_property = transfer_mixins.CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty(
                    port_number=123,
                    resource_configuration_arn="resourceConfigurationArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e6ee7ad90d1f9bf04c456c2a1c673083f72f93dede70b5311e6b67743f885420)
                check_type(argname="argument port_number", value=port_number, expected_type=type_hints["port_number"])
                check_type(argname="argument resource_configuration_arn", value=resource_configuration_arn, expected_type=type_hints["resource_configuration_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if port_number is not None:
                self._values["port_number"] = port_number
            if resource_configuration_arn is not None:
                self._values["resource_configuration_arn"] = resource_configuration_arn

        @builtins.property
        def port_number(self) -> typing.Optional[jsii.Number]:
            '''Port number for connecting to the SFTP server through VPC_LATTICE.

            Defaults to 22 if not specified. Must match the port on which the target SFTP server is listening.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-connectorvpclatticeegressconfig.html#cfn-transfer-connector-connectorvpclatticeegressconfig-portnumber
            '''
            result = self._values.get("port_number")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_configuration_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the VPC_LATTICE Resource Configuration that defines the target SFTP server location.

            Must point to a valid Resource Configuration in the customer's VPC with appropriate network connectivity to the SFTP server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-connectorvpclatticeegressconfig.html#cfn-transfer-connector-connectorvpclatticeegressconfig-resourceconfigurationarn
            '''
            result = self._values.get("resource_configuration_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectorVpcLatticeEgressConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnConnectorPropsMixin.SftpConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_concurrent_connections": "maxConcurrentConnections",
            "trusted_host_keys": "trustedHostKeys",
            "user_secret_id": "userSecretId",
        },
    )
    class SftpConfigProperty:
        def __init__(
            self,
            *,
            max_concurrent_connections: typing.Optional[jsii.Number] = None,
            trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
            user_secret_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the parameters for an SFTP connector object.

            :param max_concurrent_connections: Specify the number of concurrent connections that your connector creates to the remote server. The default value is ``1`` . The maximum values is ``5`` . .. epigraph:: If you are using the AWS Management Console , the default value is ``5`` . This parameter specifies the number of active connections that your connector can establish with the remote server at the same time. Increasing this value can enhance connector performance when transferring large file batches by enabling parallel operations. Default: - 1
            :param trusted_host_keys: The public portion of the host key, or keys, that are used to identify the external server to which you are connecting. You can use the ``ssh-keyscan`` command against the SFTP server to retrieve the necessary key. .. epigraph:: ``TrustedHostKeys`` is optional for ``CreateConnector`` . If not provided, you can use ``TestConnection`` to retrieve the server host key during the initial connection attempt, and subsequently update the connector with the observed host key. When creating connectors with egress config (VPC_LATTICE type connectors), since host name is not something we can verify, the only accepted trusted host key format is ``key-type key-body`` without the host name. For example: ``ssh-rsa AAAAB3Nza...<long-string-for-public-key>`` The three standard SSH public key format elements are ``<key type>`` , ``<body base64>`` , and an optional ``<comment>`` , with spaces between each element. Specify only the ``<key type>`` and ``<body base64>`` : do not enter the ``<comment>`` portion of the key. For the trusted host key, AWS Transfer Family accepts RSA and ECDSA keys. - For RSA keys, the ``<key type>`` string is ``ssh-rsa`` . - For ECDSA keys, the ``<key type>`` string is either ``ecdsa-sha2-nistp256`` , ``ecdsa-sha2-nistp384`` , or ``ecdsa-sha2-nistp521`` , depending on the size of the key you generated. Run this command to retrieve the SFTP server host key, where your SFTP server name is ``ftp.host.com`` . ``ssh-keyscan ftp.host.com`` This prints the public host key to standard output. ``ftp.host.com ssh-rsa AAAAB3Nza...<long-string-for-public-key>`` Copy and paste this string into the ``TrustedHostKeys`` field for the ``create-connector`` command or into the *Trusted host keys* field in the console. For VPC Lattice type connectors (VPC_LATTICE), remove the hostname from the key and use only the ``key-type key-body`` format. In this example, it should be: ``ssh-rsa AAAAB3Nza...<long-string-for-public-key>``
            :param user_secret_id: The identifier for the secret (in AWS Secrets Manager) that contains the SFTP user's private key, password, or both. The identifier must be the Amazon Resource Name (ARN) of the secret. .. epigraph:: - Required when creating an SFTP connector - Optional when updating an existing SFTP connector

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-sftpconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                sftp_config_property = transfer_mixins.CfnConnectorPropsMixin.SftpConfigProperty(
                    max_concurrent_connections=123,
                    trusted_host_keys=["trustedHostKeys"],
                    user_secret_id="userSecretId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__63436161c886f895a24f2f45c1e1b8e392991e8a860e12bd776e7c511183f876)
                check_type(argname="argument max_concurrent_connections", value=max_concurrent_connections, expected_type=type_hints["max_concurrent_connections"])
                check_type(argname="argument trusted_host_keys", value=trusted_host_keys, expected_type=type_hints["trusted_host_keys"])
                check_type(argname="argument user_secret_id", value=user_secret_id, expected_type=type_hints["user_secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_concurrent_connections is not None:
                self._values["max_concurrent_connections"] = max_concurrent_connections
            if trusted_host_keys is not None:
                self._values["trusted_host_keys"] = trusted_host_keys
            if user_secret_id is not None:
                self._values["user_secret_id"] = user_secret_id

        @builtins.property
        def max_concurrent_connections(self) -> typing.Optional[jsii.Number]:
            '''Specify the number of concurrent connections that your connector creates to the remote server.

            The default value is ``1`` . The maximum values is ``5`` .
            .. epigraph::

               If you are using the AWS Management Console , the default value is ``5`` .

            This parameter specifies the number of active connections that your connector can establish with the remote server at the same time. Increasing this value can enhance connector performance when transferring large file batches by enabling parallel operations.

            :default: - 1

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-sftpconfig.html#cfn-transfer-connector-sftpconfig-maxconcurrentconnections
            '''
            result = self._values.get("max_concurrent_connections")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def trusted_host_keys(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The public portion of the host key, or keys, that are used to identify the external server to which you are connecting.

            You can use the ``ssh-keyscan`` command against the SFTP server to retrieve the necessary key.
            .. epigraph::

               ``TrustedHostKeys`` is optional for ``CreateConnector`` . If not provided, you can use ``TestConnection`` to retrieve the server host key during the initial connection attempt, and subsequently update the connector with the observed host key.

            When creating connectors with egress config (VPC_LATTICE type connectors), since host name is not something we can verify, the only accepted trusted host key format is ``key-type key-body`` without the host name. For example: ``ssh-rsa AAAAB3Nza...<long-string-for-public-key>``

            The three standard SSH public key format elements are ``<key type>`` , ``<body base64>`` , and an optional ``<comment>`` , with spaces between each element. Specify only the ``<key type>`` and ``<body base64>`` : do not enter the ``<comment>`` portion of the key.

            For the trusted host key, AWS Transfer Family accepts RSA and ECDSA keys.

            - For RSA keys, the ``<key type>`` string is ``ssh-rsa`` .
            - For ECDSA keys, the ``<key type>`` string is either ``ecdsa-sha2-nistp256`` , ``ecdsa-sha2-nistp384`` , or ``ecdsa-sha2-nistp521`` , depending on the size of the key you generated.

            Run this command to retrieve the SFTP server host key, where your SFTP server name is ``ftp.host.com`` .

            ``ssh-keyscan ftp.host.com``

            This prints the public host key to standard output.

            ``ftp.host.com ssh-rsa AAAAB3Nza...<long-string-for-public-key>``

            Copy and paste this string into the ``TrustedHostKeys`` field for the ``create-connector`` command or into the *Trusted host keys* field in the console.

            For VPC Lattice type connectors (VPC_LATTICE), remove the hostname from the key and use only the ``key-type key-body`` format. In this example, it should be: ``ssh-rsa AAAAB3Nza...<long-string-for-public-key>``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-sftpconfig.html#cfn-transfer-connector-sftpconfig-trustedhostkeys
            '''
            result = self._values.get("trusted_host_keys")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def user_secret_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the secret (in AWS Secrets Manager) that contains the SFTP user's private key, password, or both.

            The identifier must be the Amazon Resource Name (ARN) of the secret.
            .. epigraph::

               - Required when creating an SFTP connector
               - Optional when updating an existing SFTP connector

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-connector-sftpconfig.html#cfn-transfer-connector-sftpconfig-usersecretid
            '''
            result = self._values.get("user_secret_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SftpConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnProfileMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "as2_id": "as2Id",
        "certificate_ids": "certificateIds",
        "profile_type": "profileType",
        "tags": "tags",
    },
)
class CfnProfileMixinProps:
    def __init__(
        self,
        *,
        as2_id: typing.Optional[builtins.str] = None,
        certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        profile_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProfilePropsMixin.

        :param as2_id: The ``As2Id`` is the *AS2-name* , as defined in the `RFC 4130 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc4130>`_ . For inbound transfers, this is the ``AS2-From`` header for the AS2 messages sent from the partner. For outbound connectors, this is the ``AS2-To`` header for the AS2 messages sent to the partner using the ``StartFileTransfer`` API operation. This ID cannot include spaces.
        :param certificate_ids: An array of identifiers for the imported certificates. You use this identifier for working with profiles and partner profiles.
        :param profile_type: Indicates whether to list only ``LOCAL`` type profiles or only ``PARTNER`` type profiles. If not supplied in the request, the command lists all types of profiles.
        :param tags: Key-value pairs that can be used to group and search for profiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            cfn_profile_mixin_props = transfer_mixins.CfnProfileMixinProps(
                as2_id="as2Id",
                certificate_ids=["certificateIds"],
                profile_type="profileType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b14335fbb9ee1cda416c677c3a38d55bb2cd6ea86efef248143f337da5b1b3)
            check_type(argname="argument as2_id", value=as2_id, expected_type=type_hints["as2_id"])
            check_type(argname="argument certificate_ids", value=certificate_ids, expected_type=type_hints["certificate_ids"])
            check_type(argname="argument profile_type", value=profile_type, expected_type=type_hints["profile_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if as2_id is not None:
            self._values["as2_id"] = as2_id
        if certificate_ids is not None:
            self._values["certificate_ids"] = certificate_ids
        if profile_type is not None:
            self._values["profile_type"] = profile_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def as2_id(self) -> typing.Optional[builtins.str]:
        '''The ``As2Id`` is the *AS2-name* , as defined in the `RFC 4130 <https://docs.aws.amazon.com/https://datatracker.ietf.org/doc/html/rfc4130>`_ . For inbound transfers, this is the ``AS2-From`` header for the AS2 messages sent from the partner. For outbound connectors, this is the ``AS2-To`` header for the AS2 messages sent to the partner using the ``StartFileTransfer`` API operation. This ID cannot include spaces.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-as2id
        '''
        result = self._values.get("as2_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of identifiers for the imported certificates.

        You use this identifier for working with profiles and partner profiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-certificateids
        '''
        result = self._values.get("certificate_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def profile_type(self) -> typing.Optional[builtins.str]:
        '''Indicates whether to list only ``LOCAL`` type profiles or only ``PARTNER`` type profiles.

        If not supplied in the request, the command lists all types of profiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-profiletype
        '''
        result = self._values.get("profile_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for profiles.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html#cfn-transfer-profile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfileMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProfilePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnProfilePropsMixin",
):
    '''Creates the local or partner profile to use for AS2 transfers.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-profile.html
    :cloudformationResource: AWS::Transfer::Profile
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_profile_props_mixin = transfer_mixins.CfnProfilePropsMixin(transfer_mixins.CfnProfileMixinProps(
            as2_id="as2Id",
            certificate_ids=["certificateIds"],
            profile_type="profileType",
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
        props: typing.Union[CfnProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Transfer::Profile``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5144fe085aac82b899c9a4a6099b3f9c4a12c068db11676403417f96ebaac730)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1765a2a01ecc0c0a37c32777e8fd85a2ec44b9cbe5faad97f31621c6063536b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1035a5e8b5f717c7d075c3aa0e5165f6953e5fd8ecdb9baeb134cf4f4f203f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProfileMixinProps:
        return typing.cast(CfnProfileMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.implements(_IMixin_11e4b965)
class CfnServerLogsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerLogsMixin",
):
    '''Instantiates an auto-scaling virtual server based on the selected file transfer protocol in AWS .

    When you make updates to your file transfer protocol-enabled server or when you work with users, use the service-generated ``ServerId`` property that is assigned to the newly created server.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    :cloudformationResource: AWS::Transfer::Server
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import aws_logs as logs
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        # logs_delivery: logs.ILogsDelivery
        
        cfn_server_logs_mixin = transfer_mixins.CfnServerLogsMixin("logType", logs_delivery)
    '''

    def __init__(
        self,
        log_type: builtins.str,
        log_delivery: _ILogsDelivery_0d3c9e29,
    ) -> None:
        '''Create a mixin to enable vended logs for ``AWS::Transfer::Server``.

        :param log_type: Type of logs that are getting vended.
        :param log_delivery: Object in charge of setting up the delivery destination and delivery connection.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e36964bb0bddab8f68c308f08eb47db7e1d25d6ea0174df761b6fb46b58dd3d)
            check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            check_type(argname="argument log_delivery", value=log_delivery, expected_type=type_hints["log_delivery"])
        jsii.create(self.__class__, self, [log_type, log_delivery])

    @jsii.member(jsii_name="applyTo")
    def apply_to(
        self,
        resource: _constructs_77d1e7e8.IConstruct,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Apply vended logs configuration to the construct.

        :param resource: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71970669867afa57b4745db45525041367a3fbe006e3a5a4adc8738a2ddbcf82)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [resource]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct (has vendedLogs property).

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e0a334f483938fcdf24a2c87e3557cbb614fbab77871bdbd7b11c8e67189477)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TRANSFER_LOGS")
    def TRANSFER_LOGS(cls) -> "CfnServerTransferLogs":
        return typing.cast("CfnServerTransferLogs", jsii.sget(cls, "TRANSFER_LOGS"))

    @builtins.property
    @jsii.member(jsii_name="logDelivery")
    def _log_delivery(self) -> _ILogsDelivery_0d3c9e29:
        return typing.cast(_ILogsDelivery_0d3c9e29, jsii.get(self, "logDelivery"))

    @builtins.property
    @jsii.member(jsii_name="logType")
    def _log_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logType"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "domain": "domain",
        "endpoint_details": "endpointDetails",
        "endpoint_type": "endpointType",
        "identity_provider_details": "identityProviderDetails",
        "identity_provider_type": "identityProviderType",
        "ip_address_type": "ipAddressType",
        "logging_role": "loggingRole",
        "post_authentication_login_banner": "postAuthenticationLoginBanner",
        "pre_authentication_login_banner": "preAuthenticationLoginBanner",
        "protocol_details": "protocolDetails",
        "protocols": "protocols",
        "s3_storage_options": "s3StorageOptions",
        "security_policy_name": "securityPolicyName",
        "structured_log_destinations": "structuredLogDestinations",
        "tags": "tags",
        "workflow_details": "workflowDetails",
    },
)
class CfnServerMixinProps:
    def __init__(
        self,
        *,
        certificate: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        endpoint_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.EndpointDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        endpoint_type: typing.Optional[builtins.str] = None,
        identity_provider_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.IdentityProviderDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        identity_provider_type: typing.Optional[builtins.str] = None,
        ip_address_type: typing.Optional[builtins.str] = None,
        logging_role: typing.Optional[builtins.str] = None,
        post_authentication_login_banner: typing.Optional[builtins.str] = None,
        pre_authentication_login_banner: typing.Optional[builtins.str] = None,
        protocol_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.ProtocolDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
        s3_storage_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.S3StorageOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_policy_name: typing.Optional[builtins.str] = None,
        structured_log_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        workflow_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.WorkflowDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnServerPropsMixin.

        :param certificate: The Amazon Resource Name (ARN) of the Certificate Manager (ACM) certificate. Required when ``Protocols`` is set to ``FTPS`` . To request a new public certificate, see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ in the *Certificate Manager User Guide* . To import an existing certificate into ACM, see `Importing certificates into ACM <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *Certificate Manager User Guide* . To request a private certificate to use FTPS through private IP addresses, see `Request a private certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html>`_ in the *Certificate Manager User Guide* . Certificates with the following cryptographic algorithms and key sizes are supported: - 2048-bit RSA (RSA_2048) - 4096-bit RSA (RSA_4096) - Elliptic Prime Curve 256 bit (EC_prime256v1) - Elliptic Prime Curve 384 bit (EC_secp384r1) - Elliptic Prime Curve 521 bit (EC_secp521r1) .. epigraph:: The certificate must be a valid SSL/TLS X.509 version 3 certificate with FQDN or IP address specified and information about the issuer.
        :param domain: Specifies the domain of the storage system that is used for file transfers. There are two domains available: Amazon Simple Storage Service (Amazon S3) and Amazon Elastic File System (Amazon EFS). The default value is S3.
        :param endpoint_details: The virtual private cloud (VPC) endpoint settings that are configured for your server. When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.
        :param endpoint_type: The type of endpoint that you want your server to use. You can choose to make your server's endpoint publicly accessible (PUBLIC) or host it inside your VPC. With an endpoint that is hosted in a VPC, you can restrict access to your server and resources only within your VPC or choose to make it internet facing by attaching Elastic IP addresses directly to it. .. epigraph:: After May 19, 2021, you won't be able to create a server using ``EndpointType=VPC_ENDPOINT`` in your AWS account if your account hasn't already done so before May 19, 2021. If you have already created servers with ``EndpointType=VPC_ENDPOINT`` in your AWS account on or before May 19, 2021, you will not be affected. After this date, use ``EndpointType`` = ``VPC`` . For more information, see `Discontinuing the use of VPC_ENDPOINT <https://docs.aws.amazon.com//transfer/latest/userguide/create-server-in-vpc.html#deprecate-vpc-endpoint>`_ . It is recommended that you use ``VPC`` as the ``EndpointType`` . With this endpoint type, you have the option to directly associate up to three Elastic IPv4 addresses (BYO IP included) with your server's endpoint and use VPC security groups to restrict traffic by the client's public IP address. This is not possible with ``EndpointType`` set to ``VPC_ENDPOINT`` .
        :param identity_provider_details: Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` , ``AWS _LAMBDA`` or ``API_GATEWAY`` . Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Cannot be specified when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .
        :param identity_provider_type: The mode of authentication for a server. The default value is ``SERVICE_MANAGED`` , which allows you to store and access user credentials within the AWS Transfer Family service. Use ``AWS_DIRECTORY_SERVICE`` to provide access to Active Directory groups in AWS Directory Service for Microsoft Active Directory or Microsoft Active Directory in your on-premises environment or in AWS using AD Connector. This option also requires you to provide a Directory ID by using the ``IdentityProviderDetails`` parameter. Use the ``API_GATEWAY`` value to integrate with an identity provider of your choosing. The ``API_GATEWAY`` setting requires you to provide an Amazon API Gateway endpoint URL to call for authentication by using the ``IdentityProviderDetails`` parameter. Use the ``AWS_LAMBDA`` value to directly use an AWS Lambda function as your identity provider. If you choose this value, you must specify the ARN for the Lambda function in the ``Function`` parameter for the ``IdentityProviderDetails`` data type.
        :param ip_address_type: Specifies whether to use IPv4 only, or to use dual-stack (IPv4 and IPv6) for your AWS Transfer Family endpoint. The default value is ``IPV4`` . .. epigraph:: The ``IpAddressType`` parameter has the following limitations: - It cannot be changed while the server is online. You must stop the server before modifying this parameter. - It cannot be updated to ``DUALSTACK`` if the server has ``AddressAllocationIds`` specified. > When using ``DUALSTACK`` as the ``IpAddressType`` , you cannot set the ``AddressAllocationIds`` parameter for the `EndpointDetails <https://docs.aws.amazon.com/transfer/latest/APIReference/API_EndpointDetails.html>`_ for the server.
        :param logging_role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a server to turn on Amazon CloudWatch logging for Amazon S3 or Amazon EFS events. When set, you can view user activity in your CloudWatch logs.
        :param post_authentication_login_banner: Specifies a string to display when users connect to a server. This string is displayed after the user authenticates. .. epigraph:: The SFTP protocol does not support post-authentication display banners.
        :param pre_authentication_login_banner: Specifies a string to display when users connect to a server. This string is displayed before the user authenticates. For example, the following banner displays details about using the system: ``This system is for the use of authorized users only. Individuals using this computer system without authority, or in excess of their authority, are subject to having all of their activities on this system monitored and recorded by system personnel.``
        :param protocol_details: The protocol settings that are configured for your server. - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer. - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call. - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter. - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported. The ``Protocols`` parameter is an array of strings. *Allowed values* : One or more of ``SFTP`` , ``FTPS`` , ``FTP`` , ``AS2``
        :param protocols: Specifies the file transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint. The available protocols are: - ``SFTP`` (Secure Shell (SSH) File Transfer Protocol): File transfer over SSH - ``FTPS`` (File Transfer Protocol Secure): File transfer with TLS encryption - ``FTP`` (File Transfer Protocol): Unencrypted file transfer - ``AS2`` (Applicability Statement 2): used for transporting structured business-to-business data .. epigraph:: - If you select ``FTPS`` , you must choose a certificate stored in Certificate Manager (ACM) which is used to identify your server when clients connect to it over FTPS. - If ``Protocol`` includes either ``FTP`` or ``FTPS`` , then the ``EndpointType`` must be ``VPC`` and the ``IdentityProviderType`` must be either ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` . - If ``Protocol`` includes ``FTP`` , then ``AddressAllocationIds`` cannot be associated. - If ``Protocol`` is set only to ``SFTP`` , the ``EndpointType`` can be set to ``PUBLIC`` and the ``IdentityProviderType`` can be set any of the supported identity types: ``SERVICE_MANAGED`` , ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` . - If ``Protocol`` includes ``AS2`` , then the ``EndpointType`` must be ``VPC`` , and domain must be Amazon S3. The ``Protocols`` parameter is an array of strings. *Allowed values* : One or more of ``SFTP`` , ``FTPS`` , ``FTP`` , ``AS2``
        :param s3_storage_options: Specifies whether or not performance for your Amazon S3 directories is optimized. - If using the console, this is enabled by default. - If using the API or CLI, this is disabled by default. By default, home directory mappings have a ``TYPE`` of ``DIRECTORY`` . If you enable this option, you would then need to explicitly set the ``HomeDirectoryMapEntry`` ``Type`` to ``FILE`` if you want a mapping to have a file target.
        :param security_policy_name: Specifies the name of the security policy for the server.
        :param structured_log_destinations: Specifies the log groups to which your server logs are sent. To specify a log group, you must provide the ARN for an existing log group. In this case, the format of the log group is as follows: ``arn:aws:logs:region-name:amazon-account-id:log-group:log-group-name:*`` For example, ``arn:aws:logs:us-east-1:111122223333:log-group:mytestgroup:*`` If you have previously specified a log group for a server, you can clear it, and in effect turn off structured logging, by providing an empty value for this parameter in an ``update-server`` call. For example: ``update-server --server-id s-1234567890abcdef0 --structured-log-destinations``
        :param tags: Key-value pairs that can be used to group and search for servers.
        :param workflow_details: Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow. In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            cfn_server_mixin_props = transfer_mixins.CfnServerMixinProps(
                certificate="certificate",
                domain="domain",
                endpoint_details=transfer_mixins.CfnServerPropsMixin.EndpointDetailsProperty(
                    address_allocation_ids=["addressAllocationIds"],
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                ),
                endpoint_type="endpointType",
                identity_provider_details=transfer_mixins.CfnServerPropsMixin.IdentityProviderDetailsProperty(
                    directory_id="directoryId",
                    function="function",
                    invocation_role="invocationRole",
                    sftp_authentication_methods="sftpAuthenticationMethods",
                    url="url"
                ),
                identity_provider_type="identityProviderType",
                ip_address_type="ipAddressType",
                logging_role="loggingRole",
                post_authentication_login_banner="postAuthenticationLoginBanner",
                pre_authentication_login_banner="preAuthenticationLoginBanner",
                protocol_details=transfer_mixins.CfnServerPropsMixin.ProtocolDetailsProperty(
                    as2_transports=["as2Transports"],
                    passive_ip="passiveIp",
                    set_stat_option="setStatOption",
                    tls_session_resumption_mode="tlsSessionResumptionMode"
                ),
                protocols=["protocols"],
                s3_storage_options=transfer_mixins.CfnServerPropsMixin.S3StorageOptionsProperty(
                    directory_listing_optimization="directoryListingOptimization"
                ),
                security_policy_name="securityPolicyName",
                structured_log_destinations=["structuredLogDestinations"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                workflow_details=transfer_mixins.CfnServerPropsMixin.WorkflowDetailsProperty(
                    on_partial_upload=[transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )],
                    on_upload=[transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1730dca516700d62c941dc912d24b68bd2a56ffef28f4c561a827c1d2580d414)
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument endpoint_details", value=endpoint_details, expected_type=type_hints["endpoint_details"])
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument identity_provider_details", value=identity_provider_details, expected_type=type_hints["identity_provider_details"])
            check_type(argname="argument identity_provider_type", value=identity_provider_type, expected_type=type_hints["identity_provider_type"])
            check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
            check_type(argname="argument logging_role", value=logging_role, expected_type=type_hints["logging_role"])
            check_type(argname="argument post_authentication_login_banner", value=post_authentication_login_banner, expected_type=type_hints["post_authentication_login_banner"])
            check_type(argname="argument pre_authentication_login_banner", value=pre_authentication_login_banner, expected_type=type_hints["pre_authentication_login_banner"])
            check_type(argname="argument protocol_details", value=protocol_details, expected_type=type_hints["protocol_details"])
            check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
            check_type(argname="argument s3_storage_options", value=s3_storage_options, expected_type=type_hints["s3_storage_options"])
            check_type(argname="argument security_policy_name", value=security_policy_name, expected_type=type_hints["security_policy_name"])
            check_type(argname="argument structured_log_destinations", value=structured_log_destinations, expected_type=type_hints["structured_log_destinations"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument workflow_details", value=workflow_details, expected_type=type_hints["workflow_details"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate is not None:
            self._values["certificate"] = certificate
        if domain is not None:
            self._values["domain"] = domain
        if endpoint_details is not None:
            self._values["endpoint_details"] = endpoint_details
        if endpoint_type is not None:
            self._values["endpoint_type"] = endpoint_type
        if identity_provider_details is not None:
            self._values["identity_provider_details"] = identity_provider_details
        if identity_provider_type is not None:
            self._values["identity_provider_type"] = identity_provider_type
        if ip_address_type is not None:
            self._values["ip_address_type"] = ip_address_type
        if logging_role is not None:
            self._values["logging_role"] = logging_role
        if post_authentication_login_banner is not None:
            self._values["post_authentication_login_banner"] = post_authentication_login_banner
        if pre_authentication_login_banner is not None:
            self._values["pre_authentication_login_banner"] = pre_authentication_login_banner
        if protocol_details is not None:
            self._values["protocol_details"] = protocol_details
        if protocols is not None:
            self._values["protocols"] = protocols
        if s3_storage_options is not None:
            self._values["s3_storage_options"] = s3_storage_options
        if security_policy_name is not None:
            self._values["security_policy_name"] = security_policy_name
        if structured_log_destinations is not None:
            self._values["structured_log_destinations"] = structured_log_destinations
        if tags is not None:
            self._values["tags"] = tags
        if workflow_details is not None:
            self._values["workflow_details"] = workflow_details

    @builtins.property
    def certificate(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Certificate Manager (ACM) certificate. Required when ``Protocols`` is set to ``FTPS`` .

        To request a new public certificate, see `Request a public certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html>`_ in the *Certificate Manager User Guide* .

        To import an existing certificate into ACM, see `Importing certificates into ACM <https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html>`_ in the *Certificate Manager User Guide* .

        To request a private certificate to use FTPS through private IP addresses, see `Request a private certificate <https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-private.html>`_ in the *Certificate Manager User Guide* .

        Certificates with the following cryptographic algorithms and key sizes are supported:

        - 2048-bit RSA (RSA_2048)
        - 4096-bit RSA (RSA_4096)
        - Elliptic Prime Curve 256 bit (EC_prime256v1)
        - Elliptic Prime Curve 384 bit (EC_secp384r1)
        - Elliptic Prime Curve 521 bit (EC_secp521r1)

        .. epigraph::

           The certificate must be a valid SSL/TLS X.509 version 3 certificate with FQDN or IP address specified and information about the issuer.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-certificate
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''Specifies the domain of the storage system that is used for file transfers.

        There are two domains available: Amazon Simple Storage Service (Amazon S3) and Amazon Elastic File System (Amazon EFS). The default value is S3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.EndpointDetailsProperty"]]:
        '''The virtual private cloud (VPC) endpoint settings that are configured for your server.

        When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointdetails
        '''
        result = self._values.get("endpoint_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.EndpointDetailsProperty"]], result)

    @builtins.property
    def endpoint_type(self) -> typing.Optional[builtins.str]:
        '''The type of endpoint that you want your server to use.

        You can choose to make your server's endpoint publicly accessible (PUBLIC) or host it inside your VPC. With an endpoint that is hosted in a VPC, you can restrict access to your server and resources only within your VPC or choose to make it internet facing by attaching Elastic IP addresses directly to it.
        .. epigraph::

           After May 19, 2021, you won't be able to create a server using ``EndpointType=VPC_ENDPOINT`` in your AWS account if your account hasn't already done so before May 19, 2021. If you have already created servers with ``EndpointType=VPC_ENDPOINT`` in your AWS account on or before May 19, 2021, you will not be affected. After this date, use ``EndpointType`` = ``VPC`` .

           For more information, see `Discontinuing the use of VPC_ENDPOINT <https://docs.aws.amazon.com//transfer/latest/userguide/create-server-in-vpc.html#deprecate-vpc-endpoint>`_ .

           It is recommended that you use ``VPC`` as the ``EndpointType`` . With this endpoint type, you have the option to directly associate up to three Elastic IPv4 addresses (BYO IP included) with your server's endpoint and use VPC security groups to restrict traffic by the client's public IP address. This is not possible with ``EndpointType`` set to ``VPC_ENDPOINT`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-endpointtype
        '''
        result = self._values.get("endpoint_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.IdentityProviderDetailsProperty"]]:
        '''Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` , ``AWS _LAMBDA`` or ``API_GATEWAY`` .

        Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Cannot be specified when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityproviderdetails
        '''
        result = self._values.get("identity_provider_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.IdentityProviderDetailsProperty"]], result)

    @builtins.property
    def identity_provider_type(self) -> typing.Optional[builtins.str]:
        '''The mode of authentication for a server.

        The default value is ``SERVICE_MANAGED`` , which allows you to store and access user credentials within the AWS Transfer Family service.

        Use ``AWS_DIRECTORY_SERVICE`` to provide access to Active Directory groups in AWS Directory Service for Microsoft Active Directory or Microsoft Active Directory in your on-premises environment or in AWS using AD Connector. This option also requires you to provide a Directory ID by using the ``IdentityProviderDetails`` parameter.

        Use the ``API_GATEWAY`` value to integrate with an identity provider of your choosing. The ``API_GATEWAY`` setting requires you to provide an Amazon API Gateway endpoint URL to call for authentication by using the ``IdentityProviderDetails`` parameter.

        Use the ``AWS_LAMBDA`` value to directly use an AWS Lambda function as your identity provider. If you choose this value, you must specify the ARN for the Lambda function in the ``Function`` parameter for the ``IdentityProviderDetails`` data type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-identityprovidertype
        '''
        result = self._values.get("identity_provider_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_address_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether to use IPv4 only, or to use dual-stack (IPv4 and IPv6) for your AWS Transfer Family endpoint.

        The default value is ``IPV4`` .
        .. epigraph::

           The ``IpAddressType`` parameter has the following limitations:

           - It cannot be changed while the server is online. You must stop the server before modifying this parameter.
           - It cannot be updated to ``DUALSTACK`` if the server has ``AddressAllocationIds`` specified. > When using ``DUALSTACK`` as the ``IpAddressType`` , you cannot set the ``AddressAllocationIds`` parameter for the `EndpointDetails <https://docs.aws.amazon.com/transfer/latest/APIReference/API_EndpointDetails.html>`_ for the server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-ipaddresstype
        '''
        result = self._values.get("ip_address_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logging_role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that allows a server to turn on Amazon CloudWatch logging for Amazon S3 or Amazon EFS events.

        When set, you can view user activity in your CloudWatch logs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-loggingrole
        '''
        result = self._values.get("logging_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def post_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Specifies a string to display when users connect to a server. This string is displayed after the user authenticates.

        .. epigraph::

           The SFTP protocol does not support post-authentication display banners.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-postauthenticationloginbanner
        '''
        result = self._values.get("post_authentication_login_banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_authentication_login_banner(self) -> typing.Optional[builtins.str]:
        '''Specifies a string to display when users connect to a server.

        This string is displayed before the user authenticates. For example, the following banner displays details about using the system:

        ``This system is for the use of authorized users only. Individuals using this computer system without authority, or in excess of their authority, are subject to having all of their activities on this system monitored and recorded by system personnel.``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-preauthenticationloginbanner
        '''
        result = self._values.get("pre_authentication_login_banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.ProtocolDetailsProperty"]]:
        '''The protocol settings that are configured for your server.

        - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer.
        - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call.
        - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter.
        - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported.

        The ``Protocols`` parameter is an array of strings.

        *Allowed values* : One or more of ``SFTP`` , ``FTPS`` , ``FTP`` , ``AS2``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocoldetails
        '''
        result = self._values.get("protocol_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.ProtocolDetailsProperty"]], result)

    @builtins.property
    def protocols(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the file transfer protocol or protocols over which your file transfer protocol client can connect to your server's endpoint.

        The available protocols are:

        - ``SFTP`` (Secure Shell (SSH) File Transfer Protocol): File transfer over SSH
        - ``FTPS`` (File Transfer Protocol Secure): File transfer with TLS encryption
        - ``FTP`` (File Transfer Protocol): Unencrypted file transfer
        - ``AS2`` (Applicability Statement 2): used for transporting structured business-to-business data

        .. epigraph::

           - If you select ``FTPS`` , you must choose a certificate stored in Certificate Manager (ACM) which is used to identify your server when clients connect to it over FTPS.
           - If ``Protocol`` includes either ``FTP`` or ``FTPS`` , then the ``EndpointType`` must be ``VPC`` and the ``IdentityProviderType`` must be either ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` .
           - If ``Protocol`` includes ``FTP`` , then ``AddressAllocationIds`` cannot be associated.
           - If ``Protocol`` is set only to ``SFTP`` , the ``EndpointType`` can be set to ``PUBLIC`` and the ``IdentityProviderType`` can be set any of the supported identity types: ``SERVICE_MANAGED`` , ``AWS_DIRECTORY_SERVICE`` , ``AWS_LAMBDA`` , or ``API_GATEWAY`` .
           - If ``Protocol`` includes ``AS2`` , then the ``EndpointType`` must be ``VPC`` , and domain must be Amazon S3.

        The ``Protocols`` parameter is an array of strings.

        *Allowed values* : One or more of ``SFTP`` , ``FTPS`` , ``FTP`` , ``AS2``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-protocols
        '''
        result = self._values.get("protocols")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def s3_storage_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.S3StorageOptionsProperty"]]:
        '''Specifies whether or not performance for your Amazon S3 directories is optimized.

        - If using the console, this is enabled by default.
        - If using the API or CLI, this is disabled by default.

        By default, home directory mappings have a ``TYPE`` of ``DIRECTORY`` . If you enable this option, you would then need to explicitly set the ``HomeDirectoryMapEntry`` ``Type`` to ``FILE`` if you want a mapping to have a file target.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-s3storageoptions
        '''
        result = self._values.get("s3_storage_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.S3StorageOptionsProperty"]], result)

    @builtins.property
    def security_policy_name(self) -> typing.Optional[builtins.str]:
        '''Specifies the name of the security policy for the server.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-securitypolicyname
        '''
        result = self._values.get("security_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def structured_log_destinations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the log groups to which your server logs are sent.

        To specify a log group, you must provide the ARN for an existing log group. In this case, the format of the log group is as follows:

        ``arn:aws:logs:region-name:amazon-account-id:log-group:log-group-name:*``

        For example, ``arn:aws:logs:us-east-1:111122223333:log-group:mytestgroup:*``

        If you have previously specified a log group for a server, you can clear it, and in effect turn off structured logging, by providing an empty value for this parameter in an ``update-server`` call. For example:

        ``update-server --server-id s-1234567890abcdef0 --structured-log-destinations``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-structuredlogdestinations
        '''
        result = self._values.get("structured_log_destinations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for servers.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def workflow_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.WorkflowDetailsProperty"]]:
        '''Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow.

        In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html#cfn-transfer-server-workflowdetails
        '''
        result = self._values.get("workflow_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.WorkflowDetailsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnServerPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin",
):
    '''Instantiates an auto-scaling virtual server based on the selected file transfer protocol in AWS .

    When you make updates to your file transfer protocol-enabled server or when you work with users, use the service-generated ``ServerId`` property that is assigned to the newly created server.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-server.html
    :cloudformationResource: AWS::Transfer::Server
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_server_props_mixin = transfer_mixins.CfnServerPropsMixin(transfer_mixins.CfnServerMixinProps(
            certificate="certificate",
            domain="domain",
            endpoint_details=transfer_mixins.CfnServerPropsMixin.EndpointDetailsProperty(
                address_allocation_ids=["addressAllocationIds"],
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"],
                vpc_endpoint_id="vpcEndpointId",
                vpc_id="vpcId"
            ),
            endpoint_type="endpointType",
            identity_provider_details=transfer_mixins.CfnServerPropsMixin.IdentityProviderDetailsProperty(
                directory_id="directoryId",
                function="function",
                invocation_role="invocationRole",
                sftp_authentication_methods="sftpAuthenticationMethods",
                url="url"
            ),
            identity_provider_type="identityProviderType",
            ip_address_type="ipAddressType",
            logging_role="loggingRole",
            post_authentication_login_banner="postAuthenticationLoginBanner",
            pre_authentication_login_banner="preAuthenticationLoginBanner",
            protocol_details=transfer_mixins.CfnServerPropsMixin.ProtocolDetailsProperty(
                as2_transports=["as2Transports"],
                passive_ip="passiveIp",
                set_stat_option="setStatOption",
                tls_session_resumption_mode="tlsSessionResumptionMode"
            ),
            protocols=["protocols"],
            s3_storage_options=transfer_mixins.CfnServerPropsMixin.S3StorageOptionsProperty(
                directory_listing_optimization="directoryListingOptimization"
            ),
            security_policy_name="securityPolicyName",
            structured_log_destinations=["structuredLogDestinations"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            workflow_details=transfer_mixins.CfnServerPropsMixin.WorkflowDetailsProperty(
                on_partial_upload=[transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                    execution_role="executionRole",
                    workflow_id="workflowId"
                )],
                on_upload=[transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                    execution_role="executionRole",
                    workflow_id="workflowId"
                )]
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnServerMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Transfer::Server``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__042ccbbfdf7e7d36884ff20c8712ccef4b964a4f0eac99b9d1eb0db2ebfbe99b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd56694becd16517df00056a56eddd784fa8b918f7060b202dc1bd5a6c0a60d)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d324374c59b0a60a64977bd3b412d44e65253f8366f02aa8d3cd2992065112e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnServerMixinProps:
        return typing.cast(CfnServerMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin.EndpointDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "address_allocation_ids": "addressAllocationIds",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_endpoint_id": "vpcEndpointId",
            "vpc_id": "vpcId",
        },
    )
    class EndpointDetailsProperty:
        def __init__(
            self,
            *,
            address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            vpc_endpoint_id: typing.Optional[builtins.str] = None,
            vpc_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The virtual private cloud (VPC) endpoint settings that are configured for your server.

            When you host your endpoint within your VPC, you can make your endpoint accessible only to resources within your VPC, or you can attach Elastic IP addresses and make your endpoint accessible to clients over the internet. Your VPC's default security groups are automatically assigned to your endpoint.

            :param address_allocation_ids: A list of address allocation IDs that are required to attach an Elastic IP address to your server's endpoint. An address allocation ID corresponds to the allocation ID of an Elastic IP address. This value can be retrieved from the ``allocationId`` field from the Amazon EC2 `Address <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Address.html>`_ data type. One way to retrieve this value is by calling the EC2 `DescribeAddresses <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAddresses.html>`_ API. This parameter is optional. Set this parameter if you want to make your VPC endpoint public-facing. For details, see `Create an internet-facing endpoint for your server <https://docs.aws.amazon.com/transfer/latest/userguide/create-server-in-vpc.html#create-internet-facing-endpoint>`_ . .. epigraph:: This property can only be set as follows: - ``EndpointType`` must be set to ``VPC`` - The Transfer Family server must be offline. - You cannot set this parameter for Transfer Family servers that use the FTP protocol. - The server must already have ``SubnetIds`` populated ( ``SubnetIds`` and ``AddressAllocationIds`` cannot be updated simultaneously). - ``AddressAllocationIds`` can't contain duplicates, and must be equal in length to ``SubnetIds`` . For example, if you have three subnet IDs, you must also specify three address allocation IDs. - Call the ``UpdateServer`` API to set or change this parameter. - You can't set address allocation IDs for servers that have an ``IpAddressType`` set to ``DUALSTACK`` You can only set this property if ``IpAddressType`` is set to ``IPV4`` .
            :param security_group_ids: A list of security groups IDs that are available to attach to your server's endpoint. .. epigraph:: While ``SecurityGroupIds`` appears in the response syntax for consistency with ``CreateServer`` and ``UpdateServer`` operations, this field is not populated in ``DescribeServer`` responses. Security groups are managed at the VPC endpoint level and can be modified outside of the Transfer Family service. To retrieve current security group information, use the EC2 ``DescribeVpcEndpoints`` API with the ``VpcEndpointId`` returned in the response. This property can only be set when ``EndpointType`` is set to ``VPC`` . You can edit the ``SecurityGroupIds`` property in the `UpdateServer <https://docs.aws.amazon.com/transfer/latest/userguide/API_UpdateServer.html>`_ API only if you are changing the ``EndpointType`` from ``PUBLIC`` or ``VPC_ENDPOINT`` to ``VPC`` . To change security groups associated with your server's VPC endpoint after creation, use the Amazon EC2 `ModifyVpcEndpoint <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpoint.html>`_ API.
            :param subnet_ids: A list of subnet IDs that are required to host your server endpoint in your VPC. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC`` .
            :param vpc_endpoint_id: The ID of the VPC endpoint. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC_ENDPOINT`` .
            :param vpc_id: The VPC ID of the virtual private cloud in which the server's endpoint will be hosted. .. epigraph:: This property can only be set when ``EndpointType`` is set to ``VPC`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                endpoint_details_property = transfer_mixins.CfnServerPropsMixin.EndpointDetailsProperty(
                    address_allocation_ids=["addressAllocationIds"],
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"],
                    vpc_endpoint_id="vpcEndpointId",
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9cc3e97a93d07e5cf5024032138214d503a99dcd2e3b21f90dcd0d0c7e1921ca)
                check_type(argname="argument address_allocation_ids", value=address_allocation_ids, expected_type=type_hints["address_allocation_ids"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
                check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address_allocation_ids is not None:
                self._values["address_allocation_ids"] = address_allocation_ids
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids
            if vpc_endpoint_id is not None:
                self._values["vpc_endpoint_id"] = vpc_endpoint_id
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def address_allocation_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of address allocation IDs that are required to attach an Elastic IP address to your server's endpoint.

            An address allocation ID corresponds to the allocation ID of an Elastic IP address. This value can be retrieved from the ``allocationId`` field from the Amazon EC2 `Address <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Address.html>`_ data type. One way to retrieve this value is by calling the EC2 `DescribeAddresses <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeAddresses.html>`_ API.

            This parameter is optional. Set this parameter if you want to make your VPC endpoint public-facing. For details, see `Create an internet-facing endpoint for your server <https://docs.aws.amazon.com/transfer/latest/userguide/create-server-in-vpc.html#create-internet-facing-endpoint>`_ .
            .. epigraph::

               This property can only be set as follows:

               - ``EndpointType`` must be set to ``VPC``
               - The Transfer Family server must be offline.
               - You cannot set this parameter for Transfer Family servers that use the FTP protocol.
               - The server must already have ``SubnetIds`` populated ( ``SubnetIds`` and ``AddressAllocationIds`` cannot be updated simultaneously).
               - ``AddressAllocationIds`` can't contain duplicates, and must be equal in length to ``SubnetIds`` . For example, if you have three subnet IDs, you must also specify three address allocation IDs.
               - Call the ``UpdateServer`` API to set or change this parameter.
               - You can't set address allocation IDs for servers that have an ``IpAddressType`` set to ``DUALSTACK`` You can only set this property if ``IpAddressType`` is set to ``IPV4`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-addressallocationids
            '''
            result = self._values.get("address_allocation_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of security groups IDs that are available to attach to your server's endpoint.

            .. epigraph::

               While ``SecurityGroupIds`` appears in the response syntax for consistency with ``CreateServer`` and ``UpdateServer`` operations, this field is not populated in ``DescribeServer`` responses. Security groups are managed at the VPC endpoint level and can be modified outside of the Transfer Family service. To retrieve current security group information, use the EC2 ``DescribeVpcEndpoints`` API with the ``VpcEndpointId`` returned in the response.

               This property can only be set when ``EndpointType`` is set to ``VPC`` .

               You can edit the ``SecurityGroupIds`` property in the `UpdateServer <https://docs.aws.amazon.com/transfer/latest/userguide/API_UpdateServer.html>`_ API only if you are changing the ``EndpointType`` from ``PUBLIC`` or ``VPC_ENDPOINT`` to ``VPC`` . To change security groups associated with your server's VPC endpoint after creation, use the Amazon EC2 `ModifyVpcEndpoint <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_ModifyVpcEndpoint.html>`_ API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of subnet IDs that are required to host your server endpoint in your VPC.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def vpc_endpoint_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the VPC endpoint.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC_ENDPOINT`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcendpointid
            '''
            result = self._values.get("vpc_endpoint_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''The VPC ID of the virtual private cloud in which the server's endpoint will be hosted.

            .. epigraph::

               This property can only be set when ``EndpointType`` is set to ``VPC`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-endpointdetails.html#cfn-transfer-server-endpointdetails-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin.IdentityProviderDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_id": "directoryId",
            "function": "function",
            "invocation_role": "invocationRole",
            "sftp_authentication_methods": "sftpAuthenticationMethods",
            "url": "url",
        },
    )
    class IdentityProviderDetailsProperty:
        def __init__(
            self,
            *,
            directory_id: typing.Optional[builtins.str] = None,
            function: typing.Optional[builtins.str] = None,
            invocation_role: typing.Optional[builtins.str] = None,
            sftp_authentication_methods: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Required when ``IdentityProviderType`` is set to ``AWS_DIRECTORY_SERVICE`` , ``AWS _LAMBDA`` or ``API_GATEWAY`` .

            Accepts an array containing all of the information required to use a directory in ``AWS_DIRECTORY_SERVICE`` or invoke a customer-supplied authentication API, including the API Gateway URL. Cannot be specified when ``IdentityProviderType`` is set to ``SERVICE_MANAGED`` .

            :param directory_id: The identifier of the AWS Directory Service directory that you want to use as your identity provider.
            :param function: The ARN for a Lambda function to use for the Identity provider.
            :param invocation_role: This parameter is only applicable if your ``IdentityProviderType`` is ``API_GATEWAY`` . Provides the type of ``InvocationRole`` used to authenticate the user account.
            :param sftp_authentication_methods: For SFTP-enabled servers, and for custom identity providers *only* , you can specify whether to authenticate using a password, SSH key pair, or both. - ``PASSWORD`` - users must provide their password to connect. - ``PUBLIC_KEY`` - users must provide their private key to connect. - ``PUBLIC_KEY_OR_PASSWORD`` - users can authenticate with either their password or their key. This is the default value. - ``PUBLIC_KEY_AND_PASSWORD`` - users must provide both their private key and their password to connect. The server checks the key first, and then if the key is valid, the system prompts for a password. If the private key provided does not match the public key that is stored, authentication fails.
            :param url: Provides the location of the service endpoint used to authenticate users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                identity_provider_details_property = transfer_mixins.CfnServerPropsMixin.IdentityProviderDetailsProperty(
                    directory_id="directoryId",
                    function="function",
                    invocation_role="invocationRole",
                    sftp_authentication_methods="sftpAuthenticationMethods",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cb15ffc531949f7af8888c15d886123265e21091319aa3063240a26eed2981b)
                check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
                check_type(argname="argument function", value=function, expected_type=type_hints["function"])
                check_type(argname="argument invocation_role", value=invocation_role, expected_type=type_hints["invocation_role"])
                check_type(argname="argument sftp_authentication_methods", value=sftp_authentication_methods, expected_type=type_hints["sftp_authentication_methods"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_id is not None:
                self._values["directory_id"] = directory_id
            if function is not None:
                self._values["function"] = function
            if invocation_role is not None:
                self._values["invocation_role"] = invocation_role
            if sftp_authentication_methods is not None:
                self._values["sftp_authentication_methods"] = sftp_authentication_methods
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def directory_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the AWS Directory Service directory that you want to use as your identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-directoryid
            '''
            result = self._values.get("directory_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def function(self) -> typing.Optional[builtins.str]:
            '''The ARN for a Lambda function to use for the Identity provider.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-function
            '''
            result = self._values.get("function")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def invocation_role(self) -> typing.Optional[builtins.str]:
            '''This parameter is only applicable if your ``IdentityProviderType`` is ``API_GATEWAY`` .

            Provides the type of ``InvocationRole`` used to authenticate the user account.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-invocationrole
            '''
            result = self._values.get("invocation_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sftp_authentication_methods(self) -> typing.Optional[builtins.str]:
            '''For SFTP-enabled servers, and for custom identity providers *only* , you can specify whether to authenticate using a password, SSH key pair, or both.

            - ``PASSWORD`` - users must provide their password to connect.
            - ``PUBLIC_KEY`` - users must provide their private key to connect.
            - ``PUBLIC_KEY_OR_PASSWORD`` - users can authenticate with either their password or their key. This is the default value.
            - ``PUBLIC_KEY_AND_PASSWORD`` - users must provide both their private key and their password to connect. The server checks the key first, and then if the key is valid, the system prompts for a password. If the private key provided does not match the public key that is stored, authentication fails.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-sftpauthenticationmethods
            '''
            result = self._values.get("sftp_authentication_methods")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''Provides the location of the service endpoint used to authenticate users.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-identityproviderdetails.html#cfn-transfer-server-identityproviderdetails-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityProviderDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin.ProtocolDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "as2_transports": "as2Transports",
            "passive_ip": "passiveIp",
            "set_stat_option": "setStatOption",
            "tls_session_resumption_mode": "tlsSessionResumptionMode",
        },
    )
    class ProtocolDetailsProperty:
        def __init__(
            self,
            *,
            as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
            passive_ip: typing.Optional[builtins.str] = None,
            set_stat_option: typing.Optional[builtins.str] = None,
            tls_session_resumption_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The protocol settings that are configured for your server.

            .. epigraph::

               Avoid placing Network Load Balancers (NLBs) or NAT gateways in front of AWS Transfer Family servers, as this increases costs and can cause performance issues, including reduced connection limits for FTPS. For more details, see `Avoid placing NLBs and NATs in front of AWS Transfer Family <https://docs.aws.amazon.com/transfer/latest/userguide/infrastructure-security.html#nlb-considerations>`_ .

            - To indicate passive mode (for FTP and FTPS protocols), use the ``PassiveIp`` parameter. Enter a single dotted-quad IPv4 address, such as the external IP address of a firewall, router, or load balancer.
            - To ignore the error that is generated when the client attempts to use the ``SETSTAT`` command on a file that you are uploading to an Amazon S3 bucket, use the ``SetStatOption`` parameter. To have the AWS Transfer Family server ignore the ``SETSTAT`` command and upload files without needing to make any changes to your SFTP client, set the value to ``ENABLE_NO_OP`` . If you set the ``SetStatOption`` parameter to ``ENABLE_NO_OP`` , Transfer Family generates a log entry to Amazon CloudWatch Logs, so that you can determine when the client is making a ``SETSTAT`` call.
            - To determine whether your AWS Transfer Family server resumes recent, negotiated sessions through a unique session ID, use the ``TlsSessionResumptionMode`` parameter.
            - ``As2Transports`` indicates the transport method for the AS2 messages. Currently, only HTTP is supported.

            :param as2_transports: List of ``As2Transport`` objects.
            :param passive_ip: Indicates passive mode, for FTP and FTPS protocols. Enter a single IPv4 address, such as the public IP address of a firewall, router, or load balancer. For example: ``aws transfer update-server --protocol-details PassiveIp=0.0.0.0`` Replace ``0.0.0.0`` in the example above with the actual IP address you want to use. .. epigraph:: If you change the ``PassiveIp`` value, you must stop and then restart your Transfer Family server for the change to take effect. For details on using passive mode (PASV) in a NAT environment, see `Configuring your FTPS server behind a firewall or NAT with AWS Transfer Family <https://docs.aws.amazon.com/storage/configuring-your-ftps-server-behind-a-firewall-or-nat-with-aws-transfer-family/>`_ . Additionally, avoid placing Network Load Balancers (NLBs) or NAT gateways in front of AWS Transfer Family servers. This configuration increases costs and can cause performance issues. When NLBs or NATs are in the communication path, Transfer Family cannot accurately recognize client IP addresses, which impacts connection sharding and limits FTPS servers to only 300 simultaneous connections instead of 10,000. If you must use an NLB, use port 21 for health checks and enable TLS session resumption by setting ``TlsSessionResumptionMode = ENFORCED`` . For optimal performance, migrate to VPC endpoints with Elastic IP addresses instead of using NLBs. For more details, see `Avoid placing NLBs and NATs in front of AWS Transfer Family <https://docs.aws.amazon.com/transfer/latest/userguide/infrastructure-security.html#nlb-considerations>`_ . *Special values* The ``AUTO`` and ``0.0.0.0`` are special values for the ``PassiveIp`` parameter. The value ``PassiveIp=AUTO`` is assigned by default to FTP and FTPS type servers. In this case, the server automatically responds with one of the endpoint IPs within the PASV response. ``PassiveIp=0.0.0.0`` has a more unique application for its usage. For example, if you have a High Availability (HA) Network Load Balancer (NLB) environment, where you have 3 subnets, you can only specify a single IP address using the ``PassiveIp`` parameter. This reduces the effectiveness of having High Availability. In this case, you can specify ``PassiveIp=0.0.0.0`` . This tells the client to use the same IP address as the Control connection and utilize all AZs for their connections. Note, however, that not all FTP clients support the ``PassiveIp=0.0.0.0`` response. FileZilla and WinSCP do support it. If you are using other clients, check to see if your client supports the ``PassiveIp=0.0.0.0`` response.
            :param set_stat_option: Use the ``SetStatOption`` to ignore the error that is generated when the client attempts to use ``SETSTAT`` on a file you are uploading to an S3 bucket. Some SFTP file transfer clients can attempt to change the attributes of remote files, including timestamp and permissions, using commands, such as ``SETSTAT`` when uploading the file. However, these commands are not compatible with object storage systems, such as Amazon S3. Due to this incompatibility, file uploads from these clients can result in errors even when the file is otherwise successfully uploaded. Set the value to ``ENABLE_NO_OP`` to have the Transfer Family server ignore the ``SETSTAT`` command, and upload files without needing to make any changes to your SFTP client. While the ``SetStatOption`` ``ENABLE_NO_OP`` setting ignores the error, it does generate a log entry in Amazon CloudWatch Logs, so you can determine when the client is making a ``SETSTAT`` call. .. epigraph:: If you want to preserve the original timestamp for your file, and modify other file attributes using ``SETSTAT`` , you can use Amazon EFS as backend storage with Transfer Family.
            :param tls_session_resumption_mode: A property used with Transfer Family servers that use the FTPS protocol. TLS Session Resumption provides a mechanism to resume or share a negotiated secret key between the control and data connection for an FTPS session. ``TlsSessionResumptionMode`` determines whether or not the server resumes recent, negotiated sessions through a unique session ID. This property is available during ``CreateServer`` and ``UpdateServer`` calls. If a ``TlsSessionResumptionMode`` value is not specified during ``CreateServer`` , it is set to ``ENFORCED`` by default. - ``DISABLED`` : the server does not process TLS session resumption client requests and creates a new TLS session for each request. - ``ENABLED`` : the server processes and accepts clients that are performing TLS session resumption. The server doesn't reject client data connections that do not perform the TLS session resumption client processing. - ``ENFORCED`` : the server processes and accepts clients that are performing TLS session resumption. The server rejects client data connections that do not perform the TLS session resumption client processing. Before you set the value to ``ENFORCED`` , test your clients. .. epigraph:: Not all FTPS clients perform TLS session resumption. So, if you choose to enforce TLS session resumption, you prevent any connections from FTPS clients that don't perform the protocol negotiation. To determine whether or not you can use the ``ENFORCED`` value, you need to test your clients.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                protocol_details_property = transfer_mixins.CfnServerPropsMixin.ProtocolDetailsProperty(
                    as2_transports=["as2Transports"],
                    passive_ip="passiveIp",
                    set_stat_option="setStatOption",
                    tls_session_resumption_mode="tlsSessionResumptionMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f62871d14b99a94e2c324b17e50f60798405a65380dc80e27778e1d321d7012)
                check_type(argname="argument as2_transports", value=as2_transports, expected_type=type_hints["as2_transports"])
                check_type(argname="argument passive_ip", value=passive_ip, expected_type=type_hints["passive_ip"])
                check_type(argname="argument set_stat_option", value=set_stat_option, expected_type=type_hints["set_stat_option"])
                check_type(argname="argument tls_session_resumption_mode", value=tls_session_resumption_mode, expected_type=type_hints["tls_session_resumption_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if as2_transports is not None:
                self._values["as2_transports"] = as2_transports
            if passive_ip is not None:
                self._values["passive_ip"] = passive_ip
            if set_stat_option is not None:
                self._values["set_stat_option"] = set_stat_option
            if tls_session_resumption_mode is not None:
                self._values["tls_session_resumption_mode"] = tls_session_resumption_mode

        @builtins.property
        def as2_transports(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of ``As2Transport`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-as2transports
            '''
            result = self._values.get("as2_transports")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def passive_ip(self) -> typing.Optional[builtins.str]:
            '''Indicates passive mode, for FTP and FTPS protocols.

            Enter a single IPv4 address, such as the public IP address of a firewall, router, or load balancer. For example:

            ``aws transfer update-server --protocol-details PassiveIp=0.0.0.0``

            Replace ``0.0.0.0`` in the example above with the actual IP address you want to use.
            .. epigraph::

               If you change the ``PassiveIp`` value, you must stop and then restart your Transfer Family server for the change to take effect. For details on using passive mode (PASV) in a NAT environment, see `Configuring your FTPS server behind a firewall or NAT with AWS Transfer Family <https://docs.aws.amazon.com/storage/configuring-your-ftps-server-behind-a-firewall-or-nat-with-aws-transfer-family/>`_ .

               Additionally, avoid placing Network Load Balancers (NLBs) or NAT gateways in front of AWS Transfer Family servers. This configuration increases costs and can cause performance issues. When NLBs or NATs are in the communication path, Transfer Family cannot accurately recognize client IP addresses, which impacts connection sharding and limits FTPS servers to only 300 simultaneous connections instead of 10,000. If you must use an NLB, use port 21 for health checks and enable TLS session resumption by setting ``TlsSessionResumptionMode = ENFORCED`` . For optimal performance, migrate to VPC endpoints with Elastic IP addresses instead of using NLBs. For more details, see `Avoid placing NLBs and NATs in front of AWS Transfer Family <https://docs.aws.amazon.com/transfer/latest/userguide/infrastructure-security.html#nlb-considerations>`_ .

            *Special values*

            The ``AUTO`` and ``0.0.0.0`` are special values for the ``PassiveIp`` parameter. The value ``PassiveIp=AUTO`` is assigned by default to FTP and FTPS type servers. In this case, the server automatically responds with one of the endpoint IPs within the PASV response. ``PassiveIp=0.0.0.0`` has a more unique application for its usage. For example, if you have a High Availability (HA) Network Load Balancer (NLB) environment, where you have 3 subnets, you can only specify a single IP address using the ``PassiveIp`` parameter. This reduces the effectiveness of having High Availability. In this case, you can specify ``PassiveIp=0.0.0.0`` . This tells the client to use the same IP address as the Control connection and utilize all AZs for their connections. Note, however, that not all FTP clients support the ``PassiveIp=0.0.0.0`` response. FileZilla and WinSCP do support it. If you are using other clients, check to see if your client supports the ``PassiveIp=0.0.0.0`` response.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-passiveip
            '''
            result = self._values.get("passive_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def set_stat_option(self) -> typing.Optional[builtins.str]:
            '''Use the ``SetStatOption`` to ignore the error that is generated when the client attempts to use ``SETSTAT`` on a file you are uploading to an S3 bucket.

            Some SFTP file transfer clients can attempt to change the attributes of remote files, including timestamp and permissions, using commands, such as ``SETSTAT`` when uploading the file. However, these commands are not compatible with object storage systems, such as Amazon S3. Due to this incompatibility, file uploads from these clients can result in errors even when the file is otherwise successfully uploaded.

            Set the value to ``ENABLE_NO_OP`` to have the Transfer Family server ignore the ``SETSTAT`` command, and upload files without needing to make any changes to your SFTP client. While the ``SetStatOption`` ``ENABLE_NO_OP`` setting ignores the error, it does generate a log entry in Amazon CloudWatch Logs, so you can determine when the client is making a ``SETSTAT`` call.
            .. epigraph::

               If you want to preserve the original timestamp for your file, and modify other file attributes using ``SETSTAT`` , you can use Amazon EFS as backend storage with Transfer Family.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-setstatoption
            '''
            result = self._values.get("set_stat_option")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tls_session_resumption_mode(self) -> typing.Optional[builtins.str]:
            '''A property used with Transfer Family servers that use the FTPS protocol.

            TLS Session Resumption provides a mechanism to resume or share a negotiated secret key between the control and data connection for an FTPS session. ``TlsSessionResumptionMode`` determines whether or not the server resumes recent, negotiated sessions through a unique session ID. This property is available during ``CreateServer`` and ``UpdateServer`` calls. If a ``TlsSessionResumptionMode`` value is not specified during ``CreateServer`` , it is set to ``ENFORCED`` by default.

            - ``DISABLED`` : the server does not process TLS session resumption client requests and creates a new TLS session for each request.
            - ``ENABLED`` : the server processes and accepts clients that are performing TLS session resumption. The server doesn't reject client data connections that do not perform the TLS session resumption client processing.
            - ``ENFORCED`` : the server processes and accepts clients that are performing TLS session resumption. The server rejects client data connections that do not perform the TLS session resumption client processing. Before you set the value to ``ENFORCED`` , test your clients.

            .. epigraph::

               Not all FTPS clients perform TLS session resumption. So, if you choose to enforce TLS session resumption, you prevent any connections from FTPS clients that don't perform the protocol negotiation. To determine whether or not you can use the ``ENFORCED`` value, you need to test your clients.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-protocoldetails.html#cfn-transfer-server-protocoldetails-tlssessionresumptionmode
            '''
            result = self._values.get("tls_session_resumption_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProtocolDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin.S3StorageOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "directory_listing_optimization": "directoryListingOptimization",
        },
    )
    class S3StorageOptionsProperty:
        def __init__(
            self,
            *,
            directory_listing_optimization: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Amazon S3 storage options that are configured for your server.

            :param directory_listing_optimization: Specifies whether or not performance for your Amazon S3 directories is optimized. - If using the console, this is enabled by default. - If using the API or CLI, this is disabled by default. By default, home directory mappings have a ``TYPE`` of ``DIRECTORY`` . If you enable this option, you would then need to explicitly set the ``HomeDirectoryMapEntry`` ``Type`` to ``FILE`` if you want a mapping to have a file target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-s3storageoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                s3_storage_options_property = transfer_mixins.CfnServerPropsMixin.S3StorageOptionsProperty(
                    directory_listing_optimization="directoryListingOptimization"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6300e1ee54b5d168c996be8c027cf633a9a9199e52ad11dd0e028d1eec31ffe)
                check_type(argname="argument directory_listing_optimization", value=directory_listing_optimization, expected_type=type_hints["directory_listing_optimization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if directory_listing_optimization is not None:
                self._values["directory_listing_optimization"] = directory_listing_optimization

        @builtins.property
        def directory_listing_optimization(self) -> typing.Optional[builtins.str]:
            '''Specifies whether or not performance for your Amazon S3 directories is optimized.

            - If using the console, this is enabled by default.
            - If using the API or CLI, this is disabled by default.

            By default, home directory mappings have a ``TYPE`` of ``DIRECTORY`` . If you enable this option, you would then need to explicitly set the ``HomeDirectoryMapEntry`` ``Type`` to ``FILE`` if you want a mapping to have a file target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-s3storageoptions.html#cfn-transfer-server-s3storageoptions-directorylistingoptimization
            '''
            result = self._values.get("directory_listing_optimization")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3StorageOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin.WorkflowDetailProperty",
        jsii_struct_bases=[],
        name_mapping={"execution_role": "executionRole", "workflow_id": "workflowId"},
    )
    class WorkflowDetailProperty:
        def __init__(
            self,
            *,
            execution_role: typing.Optional[builtins.str] = None,
            workflow_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the workflow ID for the workflow to assign and the execution role that's used for executing the workflow.

            In addition to a workflow to execute when a file is uploaded completely, ``WorkflowDetails`` can also contain a workflow ID (and execution role) for a workflow to execute on partial upload. A partial upload occurs when a file is open when the session disconnects.

            :param execution_role: Includes the necessary permissions for S3, EFS, and Lambda operations that Transfer can assume, so that all workflow steps can operate on the required resources.
            :param workflow_id: A unique identifier for the workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetail.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                workflow_detail_property = transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                    execution_role="executionRole",
                    workflow_id="workflowId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8c57d019e7cc747b76d8d4e9ec313943badd96d5289c563bb4aaa78c33bd4a3c)
                check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
                check_type(argname="argument workflow_id", value=workflow_id, expected_type=type_hints["workflow_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if execution_role is not None:
                self._values["execution_role"] = execution_role
            if workflow_id is not None:
                self._values["workflow_id"] = workflow_id

        @builtins.property
        def execution_role(self) -> typing.Optional[builtins.str]:
            '''Includes the necessary permissions for S3, EFS, and Lambda operations that Transfer can assume, so that all workflow steps can operate on the required resources.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetail.html#cfn-transfer-server-workflowdetail-executionrole
            '''
            result = self._values.get("execution_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def workflow_id(self) -> typing.Optional[builtins.str]:
            '''A unique identifier for the workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetail.html#cfn-transfer-server-workflowdetail-workflowid
            '''
            result = self._values.get("workflow_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowDetailProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerPropsMixin.WorkflowDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"on_partial_upload": "onPartialUpload", "on_upload": "onUpload"},
    )
    class WorkflowDetailsProperty:
        def __init__(
            self,
            *,
            on_partial_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.WorkflowDetailProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            on_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnServerPropsMixin.WorkflowDetailProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Container for the ``WorkflowDetail`` data type.

            It is used by actions that trigger a workflow to begin execution.

            :param on_partial_upload: A trigger that starts a workflow if a file is only partially uploaded. You can attach a workflow to a server that executes whenever there is a partial upload. A *partial upload* occurs when a file is open when the session disconnects. .. epigraph:: ``OnPartialUpload`` can contain a maximum of one ``WorkflowDetail`` object.
            :param on_upload: A trigger that starts a workflow: the workflow begins to execute after a file is uploaded. To remove an associated workflow from a server, you can provide an empty ``OnUpload`` object, as in the following example. ``aws transfer update-server --server-id s-01234567890abcdef --workflow-details '{"OnUpload":[]}'`` .. epigraph:: ``OnUpload`` can contain a maximum of one ``WorkflowDetail`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                workflow_details_property = transfer_mixins.CfnServerPropsMixin.WorkflowDetailsProperty(
                    on_partial_upload=[transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )],
                    on_upload=[transfer_mixins.CfnServerPropsMixin.WorkflowDetailProperty(
                        execution_role="executionRole",
                        workflow_id="workflowId"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__38d2a768c518ec10b5e053a1e5be4054aa635f59b2a91e0d7476242c84a8b8df)
                check_type(argname="argument on_partial_upload", value=on_partial_upload, expected_type=type_hints["on_partial_upload"])
                check_type(argname="argument on_upload", value=on_upload, expected_type=type_hints["on_upload"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if on_partial_upload is not None:
                self._values["on_partial_upload"] = on_partial_upload
            if on_upload is not None:
                self._values["on_upload"] = on_upload

        @builtins.property
        def on_partial_upload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.WorkflowDetailProperty"]]]]:
            '''A trigger that starts a workflow if a file is only partially uploaded.

            You can attach a workflow to a server that executes whenever there is a partial upload.

            A *partial upload* occurs when a file is open when the session disconnects.
            .. epigraph::

               ``OnPartialUpload`` can contain a maximum of one ``WorkflowDetail`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetails.html#cfn-transfer-server-workflowdetails-onpartialupload
            '''
            result = self._values.get("on_partial_upload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.WorkflowDetailProperty"]]]], result)

        @builtins.property
        def on_upload(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.WorkflowDetailProperty"]]]]:
            '''A trigger that starts a workflow: the workflow begins to execute after a file is uploaded.

            To remove an associated workflow from a server, you can provide an empty ``OnUpload`` object, as in the following example.

            ``aws transfer update-server --server-id s-01234567890abcdef --workflow-details '{"OnUpload":[]}'``
            .. epigraph::

               ``OnUpload`` can contain a maximum of one ``WorkflowDetail`` object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-server-workflowdetails.html#cfn-transfer-server-workflowdetails-onupload
            '''
            result = self._values.get("on_upload")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnServerPropsMixin.WorkflowDetailProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


class CfnServerTransferLogs(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnServerTransferLogs",
):
    '''Builder for CfnServerLogsMixin to generate TRANSFER_LOGS for CfnServer.

    :cloudformationResource: AWS::Transfer::Server
    :logType: TRANSFER_LOGS
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_server_transfer_logs = transfer_mixins.CfnServerTransferLogs()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toFirehose")
    def to_firehose(
        self,
        delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
    ) -> CfnServerLogsMixin:
        '''Send logs to a Firehose Delivery Stream.

        :param delivery_stream: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__701804f8ee33dd080a247a81b17de6877df2c232c23b6183613b4b7ad5dac72c)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        return typing.cast(CfnServerLogsMixin, jsii.invoke(self, "toFirehose", [delivery_stream]))

    @jsii.member(jsii_name="toLogGroup")
    def to_log_group(
        self,
        log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
    ) -> CfnServerLogsMixin:
        '''Send logs to a CloudWatch Log Group.

        :param log_group: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52035871dbd9089c365e00bbeb4469b7e497d279f01fefe35caf62fbd22a2051)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        return typing.cast(CfnServerLogsMixin, jsii.invoke(self, "toLogGroup", [log_group]))

    @jsii.member(jsii_name="toS3")
    def to_s3(
        self,
        bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
    ) -> CfnServerLogsMixin:
        '''Send logs to an S3 Bucket.

        :param bucket: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35618fdf0b584693dc925ac9a475d367d84ccf5e2a8c4717d0c2b1bd1a121a0c)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(CfnServerLogsMixin, jsii.invoke(self, "toS3", [bucket]))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnUserMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "home_directory": "homeDirectory",
        "home_directory_mappings": "homeDirectoryMappings",
        "home_directory_type": "homeDirectoryType",
        "policy": "policy",
        "posix_profile": "posixProfile",
        "role": "role",
        "server_id": "serverId",
        "ssh_public_keys": "sshPublicKeys",
        "tags": "tags",
        "user_name": "userName",
    },
)
class CfnUserMixinProps:
    def __init__(
        self,
        *,
        home_directory: typing.Optional[builtins.str] = None,
        home_directory_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.HomeDirectoryMapEntryProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        home_directory_type: typing.Optional[builtins.str] = None,
        policy: typing.Optional[builtins.str] = None,
        posix_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnUserPropsMixin.PosixProfileProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role: typing.Optional[builtins.str] = None,
        server_id: typing.Optional[builtins.str] = None,
        ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnUserPropsMixin.

        :param home_directory: The landing directory (folder) for a user when they log in to the server using the client. A ``HomeDirectory`` example is ``/bucket_name/home/mydirectory`` . .. epigraph:: You can use the ``HomeDirectory`` parameter for ``HomeDirectoryType`` when it is set to either ``PATH`` or ``LOGICAL`` .
        :param home_directory_mappings: Logical directory mappings that specify what Amazon S3 or Amazon EFS paths and keys should be visible to your user and how you want to make them visible. You must specify the ``Entry`` and ``Target`` pair, where ``Entry`` shows how the path is made visible and ``Target`` is the actual Amazon S3 or Amazon EFS path. If you only specify a target, it is displayed as is. You also must ensure that your AWS Identity and Access Management (IAM) role provides access to paths in ``Target`` . This value can be set only when ``HomeDirectoryType`` is set to *LOGICAL* . The following is an ``Entry`` and ``Target`` pair example. ``[ { "Entry": "/directory1", "Target": "/bucket_name/home/mydirectory" } ]`` In most cases, you can use this value instead of the session policy to lock your user down to the designated home directory (" ``chroot`` "). To do this, you can set ``Entry`` to ``/`` and set ``Target`` to the value the user should see for their home directory when they log in. The following is an ``Entry`` and ``Target`` pair example for ``chroot`` . ``[ { "Entry": "/", "Target": "/bucket_name/home/mydirectory" } ]``
        :param home_directory_type: The type of landing directory (folder) that you want your users' home directory to be when they log in to the server. If you set it to ``PATH`` , the user will see the absolute Amazon S3 bucket or Amazon EFS path as is in their file transfer protocol clients. If you set it to ``LOGICAL`` , you need to provide mappings in the ``HomeDirectoryMappings`` for how you want to make Amazon S3 or Amazon EFS paths visible to your users. .. epigraph:: If ``HomeDirectoryType`` is ``LOGICAL`` , you must provide mappings, using the ``HomeDirectoryMappings`` parameter. If, on the other hand, ``HomeDirectoryType`` is ``PATH`` , you provide an absolute path using the ``HomeDirectory`` parameter. You cannot have both ``HomeDirectory`` and ``HomeDirectoryMappings`` in your template.
        :param policy: A session policy for your user so you can use the same IAM role across multiple users. This policy restricts user access to portions of their Amazon S3 bucket. Variables that you can use inside this policy include ``${Transfer:UserName}`` , ``${Transfer:HomeDirectory}`` , and ``${Transfer:HomeBucket}`` . .. epigraph:: For session policies, AWS Transfer Family stores the policy as a JSON blob, instead of the Amazon Resource Name (ARN) of the policy. You save the policy as a JSON blob and pass it in the ``Policy`` argument. For an example of a session policy, see `Example session policy <https://docs.aws.amazon.com/transfer/latest/userguide/session-policy.html>`_ . For more information, see `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ in the *AWS Security Token Service API Reference* .
        :param posix_profile: Specifies the full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon Elastic File System (Amazon EFS) file systems. The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.
        :param role: The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that controls your users' access to your Amazon S3 bucket or Amazon EFS file system. The policies attached to this role determine the level of access that you want to provide your users when transferring files into and out of your Amazon S3 bucket or Amazon EFS file system. The IAM role should also contain a trust relationship that allows the server to access your resources when servicing your users' transfer requests.
        :param server_id: A system-assigned unique identifier for a server instance. This is the specific server that you added your user to.
        :param ssh_public_keys: Specifies the public key portion of the Secure Shell (SSH) keys stored for the described user. .. epigraph:: To delete the public key body, set its value to zero keys, as shown here: ``SshPublicKeys: []``
        :param tags: Key-value pairs that can be used to group and search for users. Tags are metadata attached to users for any purpose.
        :param user_name: A unique string that identifies a user and is associated with a ``ServerId`` . This user name must be a minimum of 3 and a maximum of 100 characters long. The following are valid characters: a-z, A-Z, 0-9, underscore '_', hyphen '-', period '.', and at sign '@'. The user name can't start with a hyphen, period, or at sign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            cfn_user_mixin_props = transfer_mixins.CfnUserMixinProps(
                home_directory="homeDirectory",
                home_directory_mappings=[transfer_mixins.CfnUserPropsMixin.HomeDirectoryMapEntryProperty(
                    entry="entry",
                    target="target",
                    type="type"
                )],
                home_directory_type="homeDirectoryType",
                policy="policy",
                posix_profile=transfer_mixins.CfnUserPropsMixin.PosixProfileProperty(
                    gid=123,
                    secondary_gids=[123],
                    uid=123
                ),
                role="role",
                server_id="serverId",
                ssh_public_keys=["sshPublicKeys"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f131b1d49a86f76530944ce2a9e56d84fcb94508d16fb2513d44322a42ae0dac)
            check_type(argname="argument home_directory", value=home_directory, expected_type=type_hints["home_directory"])
            check_type(argname="argument home_directory_mappings", value=home_directory_mappings, expected_type=type_hints["home_directory_mappings"])
            check_type(argname="argument home_directory_type", value=home_directory_type, expected_type=type_hints["home_directory_type"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument posix_profile", value=posix_profile, expected_type=type_hints["posix_profile"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument server_id", value=server_id, expected_type=type_hints["server_id"])
            check_type(argname="argument ssh_public_keys", value=ssh_public_keys, expected_type=type_hints["ssh_public_keys"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if home_directory is not None:
            self._values["home_directory"] = home_directory
        if home_directory_mappings is not None:
            self._values["home_directory_mappings"] = home_directory_mappings
        if home_directory_type is not None:
            self._values["home_directory_type"] = home_directory_type
        if policy is not None:
            self._values["policy"] = policy
        if posix_profile is not None:
            self._values["posix_profile"] = posix_profile
        if role is not None:
            self._values["role"] = role
        if server_id is not None:
            self._values["server_id"] = server_id
        if ssh_public_keys is not None:
            self._values["ssh_public_keys"] = ssh_public_keys
        if tags is not None:
            self._values["tags"] = tags
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def home_directory(self) -> typing.Optional[builtins.str]:
        '''The landing directory (folder) for a user when they log in to the server using the client.

        A ``HomeDirectory`` example is ``/bucket_name/home/mydirectory`` .
        .. epigraph::

           You can use the ``HomeDirectory`` parameter for ``HomeDirectoryType`` when it is set to either ``PATH`` or ``LOGICAL`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectory
        '''
        result = self._values.get("home_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def home_directory_mappings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.HomeDirectoryMapEntryProperty"]]]]:
        '''Logical directory mappings that specify what Amazon S3 or Amazon EFS paths and keys should be visible to your user and how you want to make them visible.

        You must specify the ``Entry`` and ``Target`` pair, where ``Entry`` shows how the path is made visible and ``Target`` is the actual Amazon S3 or Amazon EFS path. If you only specify a target, it is displayed as is. You also must ensure that your AWS Identity and Access Management (IAM) role provides access to paths in ``Target`` . This value can be set only when ``HomeDirectoryType`` is set to *LOGICAL* .

        The following is an ``Entry`` and ``Target`` pair example.

        ``[ { "Entry": "/directory1", "Target": "/bucket_name/home/mydirectory" } ]``

        In most cases, you can use this value instead of the session policy to lock your user down to the designated home directory (" ``chroot`` "). To do this, you can set ``Entry`` to ``/`` and set ``Target`` to the value the user should see for their home directory when they log in.

        The following is an ``Entry`` and ``Target`` pair example for ``chroot`` .

        ``[ { "Entry": "/", "Target": "/bucket_name/home/mydirectory" } ]``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorymappings
        '''
        result = self._values.get("home_directory_mappings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.HomeDirectoryMapEntryProperty"]]]], result)

    @builtins.property
    def home_directory_type(self) -> typing.Optional[builtins.str]:
        '''The type of landing directory (folder) that you want your users' home directory to be when they log in to the server.

        If you set it to ``PATH`` , the user will see the absolute Amazon S3 bucket or Amazon EFS path as is in their file transfer protocol clients. If you set it to ``LOGICAL`` , you need to provide mappings in the ``HomeDirectoryMappings`` for how you want to make Amazon S3 or Amazon EFS paths visible to your users.
        .. epigraph::

           If ``HomeDirectoryType`` is ``LOGICAL`` , you must provide mappings, using the ``HomeDirectoryMappings`` parameter. If, on the other hand, ``HomeDirectoryType`` is ``PATH`` , you provide an absolute path using the ``HomeDirectory`` parameter. You cannot have both ``HomeDirectory`` and ``HomeDirectoryMappings`` in your template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-homedirectorytype
        '''
        result = self._values.get("home_directory_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[builtins.str]:
        '''A session policy for your user so you can use the same IAM role across multiple users.

        This policy restricts user access to portions of their Amazon S3 bucket. Variables that you can use inside this policy include ``${Transfer:UserName}`` , ``${Transfer:HomeDirectory}`` , and ``${Transfer:HomeBucket}`` .
        .. epigraph::

           For session policies, AWS Transfer Family stores the policy as a JSON blob, instead of the Amazon Resource Name (ARN) of the policy. You save the policy as a JSON blob and pass it in the ``Policy`` argument.

           For an example of a session policy, see `Example session policy <https://docs.aws.amazon.com/transfer/latest/userguide/session-policy.html>`_ .

           For more information, see `AssumeRole <https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html>`_ in the *AWS Security Token Service API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-policy
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def posix_profile(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.PosixProfileProperty"]]:
        '''Specifies the full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon Elastic File System (Amazon EFS) file systems.

        The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-posixprofile
        '''
        result = self._values.get("posix_profile")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnUserPropsMixin.PosixProfileProperty"]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role that controls your users' access to your Amazon S3 bucket or Amazon EFS file system.

        The policies attached to this role determine the level of access that you want to provide your users when transferring files into and out of your Amazon S3 bucket or Amazon EFS file system. The IAM role should also contain a trust relationship that allows the server to access your resources when servicing your users' transfer requests.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-role
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_id(self) -> typing.Optional[builtins.str]:
        '''A system-assigned unique identifier for a server instance.

        This is the specific server that you added your user to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-serverid
        '''
        result = self._values.get("server_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the public key portion of the Secure Shell (SSH) keys stored for the described user.

        .. epigraph::

           To delete the public key body, set its value to zero keys, as shown here:

           ``SshPublicKeys: []``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-sshpublickeys
        '''
        result = self._values.get("ssh_public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for users.

        Tags are metadata attached to users for any purpose.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''A unique string that identifies a user and is associated with a ``ServerId`` .

        This user name must be a minimum of 3 and a maximum of 100 characters long. The following are valid characters: a-z, A-Z, 0-9, underscore '_', hyphen '-', period '.', and at sign '@'. The user name can't start with a hyphen, period, or at sign.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html#cfn-transfer-user-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnUserPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnUserPropsMixin",
):
    '''The ``AWS::Transfer::User`` resource creates a user and associates them with an existing server.

    You can only create and associate users with servers that have the ``IdentityProviderType`` set to ``SERVICE_MANAGED`` . Using parameters for ``CreateUser`` , you can specify the user name, set the home directory, store the user's public key, and assign the user's AWS Identity and Access Management (IAM) role. You can also optionally add a session policy, and assign metadata with tags that can be used to group and search for users.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-user.html
    :cloudformationResource: AWS::Transfer::User
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_user_props_mixin = transfer_mixins.CfnUserPropsMixin(transfer_mixins.CfnUserMixinProps(
            home_directory="homeDirectory",
            home_directory_mappings=[transfer_mixins.CfnUserPropsMixin.HomeDirectoryMapEntryProperty(
                entry="entry",
                target="target",
                type="type"
            )],
            home_directory_type="homeDirectoryType",
            policy="policy",
            posix_profile=transfer_mixins.CfnUserPropsMixin.PosixProfileProperty(
                gid=123,
                secondary_gids=[123],
                uid=123
            ),
            role="role",
            server_id="serverId",
            ssh_public_keys=["sshPublicKeys"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_name="userName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Transfer::User``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfe9230efd44d1f97d0546d6a30817fc6a829908800ac86ef02b104bcc59bc5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf3d308ff859ce0f05178b5f801df6284b6dfc8091d3d18c3d316450bd030cb5)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b71d9a8beeec157ea99d1b1be028f3679bdc87592e788a0ae25b21f1cd2e412)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnUserMixinProps:
        return typing.cast(CfnUserMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnUserPropsMixin.HomeDirectoryMapEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"entry": "entry", "target": "target", "type": "type"},
    )
    class HomeDirectoryMapEntryProperty:
        def __init__(
            self,
            *,
            entry: typing.Optional[builtins.str] = None,
            target: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents an object that contains entries and targets for ``HomeDirectoryMappings`` .

            :param entry: Represents an entry for ``HomeDirectoryMappings`` .
            :param target: Represents the map target that is used in a ``HomeDirectoryMapEntry`` .
            :param type: Specifies the type of mapping. Set the type to ``FILE`` if you want the mapping to point to a file, or ``DIRECTORY`` for the directory to point to a directory. .. epigraph:: By default, home directory mappings have a ``Type`` of ``DIRECTORY`` when you create a Transfer Family server. You would need to explicitly set ``Type`` to ``FILE`` if you want a mapping to have a file target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                home_directory_map_entry_property = transfer_mixins.CfnUserPropsMixin.HomeDirectoryMapEntryProperty(
                    entry="entry",
                    target="target",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1676ef100f1046872ec34d8923d1d18cbc0f97e4e811bde1732e86643db80898)
                check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if entry is not None:
                self._values["entry"] = entry
            if target is not None:
                self._values["target"] = target
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def entry(self) -> typing.Optional[builtins.str]:
            '''Represents an entry for ``HomeDirectoryMappings`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-entry
            '''
            result = self._values.get("entry")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target(self) -> typing.Optional[builtins.str]:
            '''Represents the map target that is used in a ``HomeDirectoryMapEntry`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-target
            '''
            result = self._values.get("target")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of mapping.

            Set the type to ``FILE`` if you want the mapping to point to a file, or ``DIRECTORY`` for the directory to point to a directory.
            .. epigraph::

               By default, home directory mappings have a ``Type`` of ``DIRECTORY`` when you create a Transfer Family server. You would need to explicitly set ``Type`` to ``FILE`` if you want a mapping to have a file target.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-homedirectorymapentry.html#cfn-transfer-user-homedirectorymapentry-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HomeDirectoryMapEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnUserPropsMixin.PosixProfileProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "secondary_gids": "secondaryGids", "uid": "uid"},
    )
    class PosixProfileProperty:
        def __init__(
            self,
            *,
            gid: typing.Optional[jsii.Number] = None,
            secondary_gids: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            uid: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The full POSIX identity, including user ID ( ``Uid`` ), group ID ( ``Gid`` ), and any secondary groups IDs ( ``SecondaryGids`` ), that controls your users' access to your Amazon EFS file systems.

            The POSIX permissions that are set on files and directories in your file system determine the level of access your users get when transferring files into and out of your Amazon EFS file systems.

            :param gid: The POSIX group ID used for all EFS operations by this user.
            :param secondary_gids: The secondary POSIX group IDs used for all EFS operations by this user.
            :param uid: The POSIX user ID used for all EFS operations by this user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                posix_profile_property = transfer_mixins.CfnUserPropsMixin.PosixProfileProperty(
                    gid=123,
                    secondary_gids=[123],
                    uid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e10e8bd6f0999cd597162a9926843f28bd1ad182473c8eeb8b30ef14bc185c44)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
                check_type(argname="argument secondary_gids", value=secondary_gids, expected_type=type_hints["secondary_gids"])
                check_type(argname="argument uid", value=uid, expected_type=type_hints["uid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gid is not None:
                self._values["gid"] = gid
            if secondary_gids is not None:
                self._values["secondary_gids"] = secondary_gids
            if uid is not None:
                self._values["uid"] = uid

        @builtins.property
        def gid(self) -> typing.Optional[jsii.Number]:
            '''The POSIX group ID used for all EFS operations by this user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html#cfn-transfer-user-posixprofile-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secondary_gids(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''The secondary POSIX group IDs used for all EFS operations by this user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html#cfn-transfer-user-posixprofile-secondarygids
            '''
            result = self._values.get("secondary_gids")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def uid(self) -> typing.Optional[jsii.Number]:
            '''The POSIX user ID used for all EFS operations by this user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-user-posixprofile.html#cfn-transfer-user-posixprofile-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PosixProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWebAppMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_endpoint": "accessEndpoint",
        "identity_provider_details": "identityProviderDetails",
        "tags": "tags",
        "web_app_customization": "webAppCustomization",
        "web_app_endpoint_policy": "webAppEndpointPolicy",
        "web_app_units": "webAppUnits",
    },
)
class CfnWebAppMixinProps:
    def __init__(
        self,
        *,
        access_endpoint: typing.Optional[builtins.str] = None,
        identity_provider_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebAppPropsMixin.IdentityProviderDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        web_app_customization: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebAppPropsMixin.WebAppCustomizationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        web_app_endpoint_policy: typing.Optional[builtins.str] = None,
        web_app_units: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWebAppPropsMixin.WebAppUnitsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWebAppPropsMixin.

        :param access_endpoint: The ``AccessEndpoint`` is the URL that you provide to your users for them to interact with the Transfer Family web app. You can specify a custom URL or use the default value. Before you enter a custom URL for this parameter, follow the steps described in `Update your access endpoint with a custom URL <https://docs.aws.amazon.com//transfer/latest/userguide/webapp-customize.html>`_ .
        :param identity_provider_details: You can provide a structure that contains the details for the identity provider to use with your web app. For more details about this parameter, see `Configure your identity provider for Transfer Family web apps <https://docs.aws.amazon.com//transfer/latest/userguide/webapp-identity-center.html>`_ .
        :param tags: Key-value pairs that can be used to group and search for web apps. Tags are metadata attached to web apps for any purpose.
        :param web_app_customization: A structure that contains the customization fields for the web app. You can provide a title, logo, and icon to customize the appearance of your web app.
        :param web_app_endpoint_policy: Setting for the type of endpoint policy for the web app. The default value is ``STANDARD`` . If your web app was created in an AWS GovCloud (US) Region , the value of this parameter can be ``FIPS`` , which indicates the web app endpoint is FIPS-compliant.
        :param web_app_units: A union that contains the value for number of concurrent connections or the user sessions on your web app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            cfn_web_app_mixin_props = transfer_mixins.CfnWebAppMixinProps(
                access_endpoint="accessEndpoint",
                identity_provider_details=transfer_mixins.CfnWebAppPropsMixin.IdentityProviderDetailsProperty(
                    application_arn="applicationArn",
                    instance_arn="instanceArn",
                    role="role"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                web_app_customization=transfer_mixins.CfnWebAppPropsMixin.WebAppCustomizationProperty(
                    favicon_file="faviconFile",
                    logo_file="logoFile",
                    title="title"
                ),
                web_app_endpoint_policy="webAppEndpointPolicy",
                web_app_units=transfer_mixins.CfnWebAppPropsMixin.WebAppUnitsProperty(
                    provisioned=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed9b006dbf6af3d1efe34030aa53f0da2b8e9e85e3519fbcb45860363580edef)
            check_type(argname="argument access_endpoint", value=access_endpoint, expected_type=type_hints["access_endpoint"])
            check_type(argname="argument identity_provider_details", value=identity_provider_details, expected_type=type_hints["identity_provider_details"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument web_app_customization", value=web_app_customization, expected_type=type_hints["web_app_customization"])
            check_type(argname="argument web_app_endpoint_policy", value=web_app_endpoint_policy, expected_type=type_hints["web_app_endpoint_policy"])
            check_type(argname="argument web_app_units", value=web_app_units, expected_type=type_hints["web_app_units"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_endpoint is not None:
            self._values["access_endpoint"] = access_endpoint
        if identity_provider_details is not None:
            self._values["identity_provider_details"] = identity_provider_details
        if tags is not None:
            self._values["tags"] = tags
        if web_app_customization is not None:
            self._values["web_app_customization"] = web_app_customization
        if web_app_endpoint_policy is not None:
            self._values["web_app_endpoint_policy"] = web_app_endpoint_policy
        if web_app_units is not None:
            self._values["web_app_units"] = web_app_units

    @builtins.property
    def access_endpoint(self) -> typing.Optional[builtins.str]:
        '''The ``AccessEndpoint`` is the URL that you provide to your users for them to interact with the Transfer Family web app.

        You can specify a custom URL or use the default value.

        Before you enter a custom URL for this parameter, follow the steps described in `Update your access endpoint with a custom URL <https://docs.aws.amazon.com//transfer/latest/userguide/webapp-customize.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html#cfn-transfer-webapp-accessendpoint
        '''
        result = self._values.get("access_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_provider_details(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebAppPropsMixin.IdentityProviderDetailsProperty"]]:
        '''You can provide a structure that contains the details for the identity provider to use with your web app.

        For more details about this parameter, see `Configure your identity provider for Transfer Family web apps <https://docs.aws.amazon.com//transfer/latest/userguide/webapp-identity-center.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html#cfn-transfer-webapp-identityproviderdetails
        '''
        result = self._values.get("identity_provider_details")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebAppPropsMixin.IdentityProviderDetailsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for web apps.

        Tags are metadata attached to web apps for any purpose.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html#cfn-transfer-webapp-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def web_app_customization(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebAppPropsMixin.WebAppCustomizationProperty"]]:
        '''A structure that contains the customization fields for the web app.

        You can provide a title, logo, and icon to customize the appearance of your web app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html#cfn-transfer-webapp-webappcustomization
        '''
        result = self._values.get("web_app_customization")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebAppPropsMixin.WebAppCustomizationProperty"]], result)

    @builtins.property
    def web_app_endpoint_policy(self) -> typing.Optional[builtins.str]:
        '''Setting for the type of endpoint policy for the web app. The default value is ``STANDARD`` .

        If your web app was created in an AWS GovCloud (US) Region , the value of this parameter can be ``FIPS`` , which indicates the web app endpoint is FIPS-compliant.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html#cfn-transfer-webapp-webappendpointpolicy
        '''
        result = self._values.get("web_app_endpoint_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def web_app_units(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebAppPropsMixin.WebAppUnitsProperty"]]:
        '''A union that contains the value for number of concurrent connections or the user sessions on your web app.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html#cfn-transfer-webapp-webappunits
        '''
        result = self._values.get("web_app_units")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWebAppPropsMixin.WebAppUnitsProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWebAppMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWebAppPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWebAppPropsMixin",
):
    '''Creates a web app based on specified parameters, and returns the ID for the new web app.

    You can configure the web app to be publicly accessible or hosted within a VPC.

    For more information about using VPC endpoints with AWS Transfer Family , see `Create a Transfer Family web app in a VPC <https://docs.aws.amazon.com/transfer/latest/userguide/create-webapp-in-vpc.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-webapp.html
    :cloudformationResource: AWS::Transfer::WebApp
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        cfn_web_app_props_mixin = transfer_mixins.CfnWebAppPropsMixin(transfer_mixins.CfnWebAppMixinProps(
            access_endpoint="accessEndpoint",
            identity_provider_details=transfer_mixins.CfnWebAppPropsMixin.IdentityProviderDetailsProperty(
                application_arn="applicationArn",
                instance_arn="instanceArn",
                role="role"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            web_app_customization=transfer_mixins.CfnWebAppPropsMixin.WebAppCustomizationProperty(
                favicon_file="faviconFile",
                logo_file="logoFile",
                title="title"
            ),
            web_app_endpoint_policy="webAppEndpointPolicy",
            web_app_units=transfer_mixins.CfnWebAppPropsMixin.WebAppUnitsProperty(
                provisioned=123
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnWebAppMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Transfer::WebApp``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a21016eccb46d0452ec65244d3115b725a15ae6e5e5c2abcddc3edacfa3c708)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f0f815c696b02614203a39b0b97c86376173c79173d6ae08c44f387edb51a50)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0a4c5c9b32c22cab118372eb24aefaa1b7098cffc35d7f027715574054e431c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWebAppMixinProps:
        return typing.cast(CfnWebAppMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWebAppPropsMixin.IdentityProviderDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_arn": "applicationArn",
            "instance_arn": "instanceArn",
            "role": "role",
        },
    )
    class IdentityProviderDetailsProperty:
        def __init__(
            self,
            *,
            application_arn: typing.Optional[builtins.str] = None,
            instance_arn: typing.Optional[builtins.str] = None,
            role: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that describes the values to use for the IAM Identity Center settings when you create or update a web app.

            :param application_arn: The Amazon Resource Name (ARN) for the IAM Identity Center application: this value is set automatically when you create your web app.
            :param instance_arn: The Amazon Resource Name (ARN) for the IAM Identity Center used for the web app.
            :param role: The IAM role in IAM Identity Center used for the web app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-identityproviderdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                identity_provider_details_property = transfer_mixins.CfnWebAppPropsMixin.IdentityProviderDetailsProperty(
                    application_arn="applicationArn",
                    instance_arn="instanceArn",
                    role="role"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10efe00320dcf9ea5d7895b8c83d3c1f095a4b12e1827e22f645eee3ac45b50b)
                check_type(argname="argument application_arn", value=application_arn, expected_type=type_hints["application_arn"])
                check_type(argname="argument instance_arn", value=instance_arn, expected_type=type_hints["instance_arn"])
                check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if application_arn is not None:
                self._values["application_arn"] = application_arn
            if instance_arn is not None:
                self._values["instance_arn"] = instance_arn
            if role is not None:
                self._values["role"] = role

        @builtins.property
        def application_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the IAM Identity Center application: this value is set automatically when you create your web app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-identityproviderdetails.html#cfn-transfer-webapp-identityproviderdetails-applicationarn
            '''
            result = self._values.get("application_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the IAM Identity Center used for the web app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-identityproviderdetails.html#cfn-transfer-webapp-identityproviderdetails-instancearn
            '''
            result = self._values.get("instance_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role(self) -> typing.Optional[builtins.str]:
            '''The IAM role in IAM Identity Center used for the web app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-identityproviderdetails.html#cfn-transfer-webapp-identityproviderdetails-role
            '''
            result = self._values.get("role")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IdentityProviderDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWebAppPropsMixin.WebAppCustomizationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "favicon_file": "faviconFile",
            "logo_file": "logoFile",
            "title": "title",
        },
    )
    class WebAppCustomizationProperty:
        def __init__(
            self,
            *,
            favicon_file: typing.Optional[builtins.str] = None,
            logo_file: typing.Optional[builtins.str] = None,
            title: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that contains the customization fields for the web app.

            You can provide a title, logo, and icon to customize the appearance of your web app.

            :param favicon_file: Returns an icon file data string (in base64 encoding).
            :param logo_file: Returns a logo file data string (in base64 encoding).
            :param title: Returns the page title that you defined for your web app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-webappcustomization.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                web_app_customization_property = transfer_mixins.CfnWebAppPropsMixin.WebAppCustomizationProperty(
                    favicon_file="faviconFile",
                    logo_file="logoFile",
                    title="title"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__01fa090c55edb450208ff8db50e7262f0949917c032add96b087e556e516c85d)
                check_type(argname="argument favicon_file", value=favicon_file, expected_type=type_hints["favicon_file"])
                check_type(argname="argument logo_file", value=logo_file, expected_type=type_hints["logo_file"])
                check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if favicon_file is not None:
                self._values["favicon_file"] = favicon_file
            if logo_file is not None:
                self._values["logo_file"] = logo_file
            if title is not None:
                self._values["title"] = title

        @builtins.property
        def favicon_file(self) -> typing.Optional[builtins.str]:
            '''Returns an icon file data string (in base64 encoding).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-webappcustomization.html#cfn-transfer-webapp-webappcustomization-faviconfile
            '''
            result = self._values.get("favicon_file")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def logo_file(self) -> typing.Optional[builtins.str]:
            '''Returns a logo file data string (in base64 encoding).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-webappcustomization.html#cfn-transfer-webapp-webappcustomization-logofile
            '''
            result = self._values.get("logo_file")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def title(self) -> typing.Optional[builtins.str]:
            '''Returns the page title that you defined for your web app.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-webappcustomization.html#cfn-transfer-webapp-webappcustomization-title
            '''
            result = self._values.get("title")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebAppCustomizationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWebAppPropsMixin.WebAppUnitsProperty",
        jsii_struct_bases=[],
        name_mapping={"provisioned": "provisioned"},
    )
    class WebAppUnitsProperty:
        def __init__(self, *, provisioned: typing.Optional[jsii.Number] = None) -> None:
            '''Contains an integer value that represents the value for number of concurrent connections or the user sessions on your web app.

            :param provisioned: An integer that represents the number of units for your desired number of concurrent connections, or the number of user sessions on your web app at the same time. Each increment allows an additional 250 concurrent sessions: a value of ``1`` sets the number of concurrent sessions to 250; ``2`` sets a value of 500, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-webappunits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                web_app_units_property = transfer_mixins.CfnWebAppPropsMixin.WebAppUnitsProperty(
                    provisioned=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2dc2c0867850e846c5ba7e3a76048278af8ae96382b362776a6e6dafd923f182)
                check_type(argname="argument provisioned", value=provisioned, expected_type=type_hints["provisioned"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if provisioned is not None:
                self._values["provisioned"] = provisioned

        @builtins.property
        def provisioned(self) -> typing.Optional[jsii.Number]:
            '''An integer that represents the number of units for your desired number of concurrent connections, or the number of user sessions on your web app at the same time.

            Each increment allows an additional 250 concurrent sessions: a value of ``1`` sets the number of concurrent sessions to 250; ``2`` sets a value of 500, and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-webapp-webappunits.html#cfn-transfer-webapp-webappunits-provisioned
            '''
            result = self._values.get("provisioned")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WebAppUnitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "on_exception_steps": "onExceptionSteps",
        "steps": "steps",
        "tags": "tags",
    },
)
class CfnWorkflowMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        on_exception_steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.WorkflowStepProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.WorkflowStepProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnWorkflowPropsMixin.

        :param description: Specifies the text description for the workflow.
        :param on_exception_steps: Specifies the steps (actions) to take if errors are encountered during execution of the workflow.
        :param steps: Specifies the details for the steps that are in the specified workflow.
        :param tags: Key-value pairs that can be used to group and search for workflows. Tags are metadata attached to workflows for any purpose.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
            
            # copy_step_details: Any
            # custom_step_details: Any
            # delete_step_details: Any
            # tag_step_details: Any
            
            cfn_workflow_mixin_props = transfer_mixins.CfnWorkflowMixinProps(
                description="description",
                on_exception_steps=[transfer_mixins.CfnWorkflowPropsMixin.WorkflowStepProperty(
                    copy_step_details=copy_step_details,
                    custom_step_details=custom_step_details,
                    decrypt_step_details=transfer_mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty(
                        destination_file_location=transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                            efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                                file_system_id="fileSystemId",
                                path="path"
                            ),
                            s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        name="name",
                        overwrite_existing="overwriteExisting",
                        source_file_location="sourceFileLocation",
                        type="type"
                    ),
                    delete_step_details=delete_step_details,
                    tag_step_details=tag_step_details,
                    type="type"
                )],
                steps=[transfer_mixins.CfnWorkflowPropsMixin.WorkflowStepProperty(
                    copy_step_details=copy_step_details,
                    custom_step_details=custom_step_details,
                    decrypt_step_details=transfer_mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty(
                        destination_file_location=transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                            efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                                file_system_id="fileSystemId",
                                path="path"
                            ),
                            s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        name="name",
                        overwrite_existing="overwriteExisting",
                        source_file_location="sourceFileLocation",
                        type="type"
                    ),
                    delete_step_details=delete_step_details,
                    tag_step_details=tag_step_details,
                    type="type"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2a5769fc8ecec392bcafea9f3eb2eb3ae8311dbdafd6960514aae8ba21ed30)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument on_exception_steps", value=on_exception_steps, expected_type=type_hints["on_exception_steps"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if on_exception_steps is not None:
            self._values["on_exception_steps"] = on_exception_steps
        if steps is not None:
            self._values["steps"] = steps
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Specifies the text description for the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_exception_steps(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.WorkflowStepProperty"]]]]:
        '''Specifies the steps (actions) to take if errors are encountered during execution of the workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-onexceptionsteps
        '''
        result = self._values.get("on_exception_steps")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.WorkflowStepProperty"]]]], result)

    @builtins.property
    def steps(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.WorkflowStepProperty"]]]]:
        '''Specifies the details for the steps that are in the specified workflow.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-steps
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.WorkflowStepProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Key-value pairs that can be used to group and search for workflows.

        Tags are metadata attached to workflows for any purpose.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html#cfn-transfer-workflow-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnWorkflowMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnWorkflowPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowPropsMixin",
):
    '''Allows you to create a workflow with specified steps and step details the workflow invokes after file transfer completes.

    After creating a workflow, you can associate the workflow created with any transfer servers by specifying the ``workflow-details`` field in ``CreateServer`` and ``UpdateServer`` operations.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-transfer-workflow.html
    :cloudformationResource: AWS::Transfer::Workflow
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
        
        # copy_step_details: Any
        # custom_step_details: Any
        # delete_step_details: Any
        # tag_step_details: Any
        
        cfn_workflow_props_mixin = transfer_mixins.CfnWorkflowPropsMixin(transfer_mixins.CfnWorkflowMixinProps(
            description="description",
            on_exception_steps=[transfer_mixins.CfnWorkflowPropsMixin.WorkflowStepProperty(
                copy_step_details=copy_step_details,
                custom_step_details=custom_step_details,
                decrypt_step_details=transfer_mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty(
                    destination_file_location=transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                        efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                            file_system_id="fileSystemId",
                            path="path"
                        ),
                        s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    name="name",
                    overwrite_existing="overwriteExisting",
                    source_file_location="sourceFileLocation",
                    type="type"
                ),
                delete_step_details=delete_step_details,
                tag_step_details=tag_step_details,
                type="type"
            )],
            steps=[transfer_mixins.CfnWorkflowPropsMixin.WorkflowStepProperty(
                copy_step_details=copy_step_details,
                custom_step_details=custom_step_details,
                decrypt_step_details=transfer_mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty(
                    destination_file_location=transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                        efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                            file_system_id="fileSystemId",
                            path="path"
                        ),
                        s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    name="name",
                    overwrite_existing="overwriteExisting",
                    source_file_location="sourceFileLocation",
                    type="type"
                ),
                delete_step_details=delete_step_details,
                tag_step_details=tag_step_details,
                type="type"
            )],
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
        props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Transfer::Workflow``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__228a8b1a7e62595aa087fe397106c0935f500ec5f900e89539240ee721610ffd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd95daa1bbb426ad9817192fefb5ff6d13367c950a67e7b45c446543dc39af31)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97421d541661ce64d659bfc869752b8c253edd5242cf5195d642f2df8cd27270)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnWorkflowMixinProps:
        return typing.cast(CfnWorkflowMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_file_location": "destinationFileLocation",
            "name": "name",
            "overwrite_existing": "overwriteExisting",
            "source_file_location": "sourceFileLocation",
            "type": "type",
        },
    )
    class DecryptStepDetailsProperty:
        def __init__(
            self,
            *,
            destination_file_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.InputFileLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            overwrite_existing: typing.Optional[builtins.str] = None,
            source_file_location: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details for a step that decrypts an encrypted file.

            Consists of the following values:

            - A descriptive name
            - An Amazon S3 or Amazon Elastic File System (Amazon EFS) location for the source file to decrypt.
            - An S3 or Amazon EFS location for the destination of the file decryption.
            - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .
            - The type of encryption that's used. Currently, only PGP encryption is supported.

            :param destination_file_location: Specifies the location for the file being decrypted. Use ``${Transfer:UserName}`` or ``${Transfer:UploadDate}`` in this field to parametrize the destination prefix by username or uploaded date. - Set the value of ``DestinationFileLocation`` to ``${Transfer:UserName}`` to decrypt uploaded files to an Amazon S3 bucket that is prefixed with the name of the Transfer Family user that uploaded the file. - Set the value of ``DestinationFileLocation`` to ``${Transfer:UploadDate}`` to decrypt uploaded files to an Amazon S3 bucket that is prefixed with the date of the upload. .. epigraph:: The system resolves ``UploadDate`` to a date format of *YYYY-MM-DD* , based on the date the file is uploaded in UTC.
            :param name: The name of the step, used as an identifier.
            :param overwrite_existing: A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` . If the workflow is processing a file that has the same name as an existing file, the behavior is as follows: - If ``OverwriteExisting`` is ``TRUE`` , the existing file is replaced with the file being processed. - If ``OverwriteExisting`` is ``FALSE`` , nothing happens, and the workflow processing stops.
            :param source_file_location: Specifies which file to use as input to the workflow step: either the output from the previous step, or the originally uploaded file for the workflow. - To use the previous file as the input, enter ``${previous.file}`` . In this case, this workflow step uses the output file from the previous workflow step as input. This is the default value. - To use the originally uploaded file location as input for this step, enter ``${original.file}`` .
            :param type: The type of encryption used. Currently, this value must be ``PGP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-decryptstepdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                decrypt_step_details_property = transfer_mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty(
                    destination_file_location=transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                        efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                            file_system_id="fileSystemId",
                            path="path"
                        ),
                        s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                            bucket="bucket",
                            key="key"
                        )
                    ),
                    name="name",
                    overwrite_existing="overwriteExisting",
                    source_file_location="sourceFileLocation",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8ca3fd8aff855c5d572103531040a0181ca9e8a00f880b4a39437dd28da88529)
                check_type(argname="argument destination_file_location", value=destination_file_location, expected_type=type_hints["destination_file_location"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument overwrite_existing", value=overwrite_existing, expected_type=type_hints["overwrite_existing"])
                check_type(argname="argument source_file_location", value=source_file_location, expected_type=type_hints["source_file_location"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_file_location is not None:
                self._values["destination_file_location"] = destination_file_location
            if name is not None:
                self._values["name"] = name
            if overwrite_existing is not None:
                self._values["overwrite_existing"] = overwrite_existing
            if source_file_location is not None:
                self._values["source_file_location"] = source_file_location
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def destination_file_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.InputFileLocationProperty"]]:
            '''Specifies the location for the file being decrypted.

            Use ``${Transfer:UserName}`` or ``${Transfer:UploadDate}`` in this field to parametrize the destination prefix by username or uploaded date.

            - Set the value of ``DestinationFileLocation`` to ``${Transfer:UserName}`` to decrypt uploaded files to an Amazon S3 bucket that is prefixed with the name of the Transfer Family user that uploaded the file.
            - Set the value of ``DestinationFileLocation`` to ``${Transfer:UploadDate}`` to decrypt uploaded files to an Amazon S3 bucket that is prefixed with the date of the upload.

            .. epigraph::

               The system resolves ``UploadDate`` to a date format of *YYYY-MM-DD* , based on the date the file is uploaded in UTC.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-decryptstepdetails.html#cfn-transfer-workflow-decryptstepdetails-destinationfilelocation
            '''
            result = self._values.get("destination_file_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.InputFileLocationProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the step, used as an identifier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-decryptstepdetails.html#cfn-transfer-workflow-decryptstepdetails-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite_existing(self) -> typing.Optional[builtins.str]:
            '''A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .

            If the workflow is processing a file that has the same name as an existing file, the behavior is as follows:

            - If ``OverwriteExisting`` is ``TRUE`` , the existing file is replaced with the file being processed.
            - If ``OverwriteExisting`` is ``FALSE`` , nothing happens, and the workflow processing stops.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-decryptstepdetails.html#cfn-transfer-workflow-decryptstepdetails-overwriteexisting
            '''
            result = self._values.get("overwrite_existing")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_file_location(self) -> typing.Optional[builtins.str]:
            '''Specifies which file to use as input to the workflow step: either the output from the previous step, or the originally uploaded file for the workflow.

            - To use the previous file as the input, enter ``${previous.file}`` . In this case, this workflow step uses the output file from the previous workflow step as input. This is the default value.
            - To use the originally uploaded file location as input for this step, enter ``${original.file}`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-decryptstepdetails.html#cfn-transfer-workflow-decryptstepdetails-sourcefilelocation
            '''
            result = self._values.get("source_file_location")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of encryption used.

            Currently, this value must be ``PGP`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-decryptstepdetails.html#cfn-transfer-workflow-decryptstepdetails-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DecryptStepDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"file_system_id": "fileSystemId", "path": "path"},
    )
    class EfsInputFileLocationProperty:
        def __init__(
            self,
            *,
            file_system_id: typing.Optional[builtins.str] = None,
            path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the Amazon EFS identifier and the path for the file being used.

            :param file_system_id: The identifier of the file system, assigned by Amazon EFS.
            :param path: The pathname for the folder being used by a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-efsinputfilelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                efs_input_file_location_property = transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                    file_system_id="fileSystemId",
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8faa5abb5271a667b22b9b80b3dd7036ff7b50bde7f2e102cb3455ad35d483e1)
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_system_id is not None:
                self._values["file_system_id"] = file_system_id
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def file_system_id(self) -> typing.Optional[builtins.str]:
            '''The identifier of the file system, assigned by Amazon EFS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-efsinputfilelocation.html#cfn-transfer-workflow-efsinputfilelocation-filesystemid
            '''
            result = self._values.get("file_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The pathname for the folder being used by a workflow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-efsinputfilelocation.html#cfn-transfer-workflow-efsinputfilelocation-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EfsInputFileLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowPropsMixin.InputFileLocationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "efs_file_location": "efsFileLocation",
            "s3_file_location": "s3FileLocation",
        },
    )
    class InputFileLocationProperty:
        def __init__(
            self,
            *,
            efs_file_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.EfsInputFileLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_file_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.S3InputFileLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies the location for the file that's being processed.

            :param efs_file_location: Specifies the details for the Amazon Elastic File System (Amazon EFS) file that's being decrypted.
            :param s3_file_location: Specifies the details for the Amazon S3 file that's being copied or decrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-inputfilelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                input_file_location_property = transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                    efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                        file_system_id="fileSystemId",
                        path="path"
                    ),
                    s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                        bucket="bucket",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__226464fc6e49951d7ce4f42aafdff4eee86f55c995773d31ac5770ddb571fa51)
                check_type(argname="argument efs_file_location", value=efs_file_location, expected_type=type_hints["efs_file_location"])
                check_type(argname="argument s3_file_location", value=s3_file_location, expected_type=type_hints["s3_file_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if efs_file_location is not None:
                self._values["efs_file_location"] = efs_file_location
            if s3_file_location is not None:
                self._values["s3_file_location"] = s3_file_location

        @builtins.property
        def efs_file_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.EfsInputFileLocationProperty"]]:
            '''Specifies the details for the Amazon Elastic File System (Amazon EFS) file that's being decrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-inputfilelocation.html#cfn-transfer-workflow-inputfilelocation-efsfilelocation
            '''
            result = self._values.get("efs_file_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.EfsInputFileLocationProperty"]], result)

        @builtins.property
        def s3_file_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.S3InputFileLocationProperty"]]:
            '''Specifies the details for the Amazon S3 file that's being copied or decrypted.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-inputfilelocation.html#cfn-transfer-workflow-inputfilelocation-s3filelocation
            '''
            result = self._values.get("s3_file_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.S3InputFileLocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputFileLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "key": "key"},
    )
    class S3InputFileLocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the details for the Amazon S3 location for an input file to a workflow.

            :param bucket: Specifies the S3 bucket for the customer input file.
            :param key: The name assigned to the file when it was created in Amazon S3. You use the object key to retrieve the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3inputfilelocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                s3_input_file_location_property = transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                    bucket="bucket",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a6e7ded4b787a500924cc244dd8eebbd4df1d8c090528a3600acfea291ed6ce)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''Specifies the S3 bucket for the customer input file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3inputfilelocation.html#cfn-transfer-workflow-s3inputfilelocation-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The name assigned to the file when it was created in Amazon S3.

            You use the object key to retrieve the object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-s3inputfilelocation.html#cfn-transfer-workflow-s3inputfilelocation-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3InputFileLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_transfer.mixins.CfnWorkflowPropsMixin.WorkflowStepProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_step_details": "copyStepDetails",
            "custom_step_details": "customStepDetails",
            "decrypt_step_details": "decryptStepDetails",
            "delete_step_details": "deleteStepDetails",
            "tag_step_details": "tagStepDetails",
            "type": "type",
        },
    )
    class WorkflowStepProperty:
        def __init__(
            self,
            *,
            copy_step_details: typing.Any = None,
            custom_step_details: typing.Any = None,
            decrypt_step_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnWorkflowPropsMixin.DecryptStepDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            delete_step_details: typing.Any = None,
            tag_step_details: typing.Any = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The basic building block of a workflow.

            :param copy_step_details: Details for a step that performs a file copy. Consists of the following values: - A description - An Amazon S3 location for the destination of the file copy. - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .
            :param custom_step_details: Details for a step that invokes an AWS Lambda function. Consists of the Lambda function's name, target, and timeout (in seconds).
            :param decrypt_step_details: Details for a step that decrypts an encrypted file. Consists of the following values: - A descriptive name - An Amazon S3 or Amazon Elastic File System (Amazon EFS) location for the source file to decrypt. - An S3 or Amazon EFS location for the destination of the file decryption. - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` . - The type of encryption that's used. Currently, only PGP encryption is supported.
            :param delete_step_details: Details for a step that deletes the file.
            :param tag_step_details: Details for a step that creates one or more tags. You specify one or more tags. Each tag contains a key-value pair.
            :param type: Currently, the following step types are supported. - *``COPY``* - Copy the file to another location. - *``CUSTOM``* - Perform a custom step with an AWS Lambda function target. - *``DECRYPT``* - Decrypt a file that was encrypted before it was uploaded. - *``DELETE``* - Delete the file. - *``TAG``* - Add a tag to the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_transfer import mixins as transfer_mixins
                
                # copy_step_details: Any
                # custom_step_details: Any
                # delete_step_details: Any
                # tag_step_details: Any
                
                workflow_step_property = transfer_mixins.CfnWorkflowPropsMixin.WorkflowStepProperty(
                    copy_step_details=copy_step_details,
                    custom_step_details=custom_step_details,
                    decrypt_step_details=transfer_mixins.CfnWorkflowPropsMixin.DecryptStepDetailsProperty(
                        destination_file_location=transfer_mixins.CfnWorkflowPropsMixin.InputFileLocationProperty(
                            efs_file_location=transfer_mixins.CfnWorkflowPropsMixin.EfsInputFileLocationProperty(
                                file_system_id="fileSystemId",
                                path="path"
                            ),
                            s3_file_location=transfer_mixins.CfnWorkflowPropsMixin.S3InputFileLocationProperty(
                                bucket="bucket",
                                key="key"
                            )
                        ),
                        name="name",
                        overwrite_existing="overwriteExisting",
                        source_file_location="sourceFileLocation",
                        type="type"
                    ),
                    delete_step_details=delete_step_details,
                    tag_step_details=tag_step_details,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dbd04be9f0ca672447e5e8e67b00f97aa6e6c09a582ccf531c153bc7265ca91b)
                check_type(argname="argument copy_step_details", value=copy_step_details, expected_type=type_hints["copy_step_details"])
                check_type(argname="argument custom_step_details", value=custom_step_details, expected_type=type_hints["custom_step_details"])
                check_type(argname="argument decrypt_step_details", value=decrypt_step_details, expected_type=type_hints["decrypt_step_details"])
                check_type(argname="argument delete_step_details", value=delete_step_details, expected_type=type_hints["delete_step_details"])
                check_type(argname="argument tag_step_details", value=tag_step_details, expected_type=type_hints["tag_step_details"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_step_details is not None:
                self._values["copy_step_details"] = copy_step_details
            if custom_step_details is not None:
                self._values["custom_step_details"] = custom_step_details
            if decrypt_step_details is not None:
                self._values["decrypt_step_details"] = decrypt_step_details
            if delete_step_details is not None:
                self._values["delete_step_details"] = delete_step_details
            if tag_step_details is not None:
                self._values["tag_step_details"] = tag_step_details
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def copy_step_details(self) -> typing.Any:
            '''Details for a step that performs a file copy.

            Consists of the following values:

            - A description
            - An Amazon S3 location for the destination of the file copy.
            - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-copystepdetails
            '''
            result = self._values.get("copy_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def custom_step_details(self) -> typing.Any:
            '''Details for a step that invokes an AWS Lambda function.

            Consists of the Lambda function's name, target, and timeout (in seconds).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-customstepdetails
            '''
            result = self._values.get("custom_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def decrypt_step_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.DecryptStepDetailsProperty"]]:
            '''Details for a step that decrypts an encrypted file.

            Consists of the following values:

            - A descriptive name
            - An Amazon S3 or Amazon Elastic File System (Amazon EFS) location for the source file to decrypt.
            - An S3 or Amazon EFS location for the destination of the file decryption.
            - A flag that indicates whether to overwrite an existing file of the same name. The default is ``FALSE`` .
            - The type of encryption that's used. Currently, only PGP encryption is supported.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-decryptstepdetails
            '''
            result = self._values.get("decrypt_step_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnWorkflowPropsMixin.DecryptStepDetailsProperty"]], result)

        @builtins.property
        def delete_step_details(self) -> typing.Any:
            '''Details for a step that deletes the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-deletestepdetails
            '''
            result = self._values.get("delete_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def tag_step_details(self) -> typing.Any:
            '''Details for a step that creates one or more tags.

            You specify one or more tags. Each tag contains a key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-tagstepdetails
            '''
            result = self._values.get("tag_step_details")
            return typing.cast(typing.Any, result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Currently, the following step types are supported.

            - *``COPY``* - Copy the file to another location.
            - *``CUSTOM``* - Perform a custom step with an AWS Lambda function target.
            - *``DECRYPT``* - Decrypt a file that was encrypted before it was uploaded.
            - *``DELETE``* - Delete the file.
            - *``TAG``* - Add a tag to the file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-transfer-workflow-workflowstep.html#cfn-transfer-workflow-workflowstep-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkflowStepProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnAgreementMixinProps",
    "CfnAgreementPropsMixin",
    "CfnCertificateMixinProps",
    "CfnCertificatePropsMixin",
    "CfnConnectorMixinProps",
    "CfnConnectorPropsMixin",
    "CfnProfileMixinProps",
    "CfnProfilePropsMixin",
    "CfnServerLogsMixin",
    "CfnServerMixinProps",
    "CfnServerPropsMixin",
    "CfnServerTransferLogs",
    "CfnUserMixinProps",
    "CfnUserPropsMixin",
    "CfnWebAppMixinProps",
    "CfnWebAppPropsMixin",
    "CfnWorkflowMixinProps",
    "CfnWorkflowPropsMixin",
]

publication.publish()

def _typecheckingstub__69081525ccc245470012ee56728763c06bee4c625b9ee7161d0bb4243e01079b(
    *,
    access_role: typing.Optional[builtins.str] = None,
    base_directory: typing.Optional[builtins.str] = None,
    custom_directories: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnAgreementPropsMixin.CustomDirectoriesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enforce_message_signing: typing.Optional[builtins.str] = None,
    local_profile_id: typing.Optional[builtins.str] = None,
    partner_profile_id: typing.Optional[builtins.str] = None,
    preserve_filename: typing.Optional[builtins.str] = None,
    server_id: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf9ee4277584841d8c416b64df8c07fd337444c69ee24b2a8371bbd20831c51(
    props: typing.Union[CfnAgreementMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c3b7d14a59b13056f08fb48e04a5b50d33aa1f57fce368436d692a044048da(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984009c8037cf7f05f3775b89fb922d3fec08dbe368c34eca6440d2373b51b79(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ed407a6bd6348e690858794f859e516c7fea6ab07d591e9ebe1a74c28ba4977(
    *,
    failed_files_directory: typing.Optional[builtins.str] = None,
    mdn_files_directory: typing.Optional[builtins.str] = None,
    payload_files_directory: typing.Optional[builtins.str] = None,
    status_files_directory: typing.Optional[builtins.str] = None,
    temporary_files_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1501f7486d5313b59c737955e1b87fffc6cc048843e524bf433288836f149cc(
    *,
    active_date: typing.Optional[builtins.str] = None,
    certificate: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    inactive_date: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    usage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a023a88da1e7fb1d8b0004b3b470a502ce63e40ccbee86c6370f1e876f9d5816(
    props: typing.Union[CfnCertificateMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c1b96c8442a81e6f5ab40067780d3c2cb0f409b46ae59a25512e158c61ce67(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0fc50d5d96f262b80cd2d6ca5a83d90b6a120478a3c6cbde1af549e8480b8f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc0508e75702fe89770cfc3b90c3d58ef5edbf1b0c9444864e4c6f0a8003994(
    *,
    access_role: typing.Optional[builtins.str] = None,
    as2_config: typing.Any = None,
    egress_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ConnectorEgressConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    egress_type: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    sftp_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.SftpConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d0a380f1de06a6f3212525c0f0c68974e5ceeca99257cc6bff28296979a2470(
    props: typing.Union[CfnConnectorMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8af4a003c083a71a1d3e9cb70db4b3d454448b977c0833147fbfce53b9ff48e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c55594f024abbed39743f7a4ee5613b32c46b506e4f55d756da9e079dff0c05(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb071ac4a495fc03e6fa98ff69e60ba390f28bf9ca26809d3f2da14cf8b3cb31(
    *,
    basic_auth_secret_id: typing.Optional[builtins.str] = None,
    compression: typing.Optional[builtins.str] = None,
    encryption_algorithm: typing.Optional[builtins.str] = None,
    local_profile_id: typing.Optional[builtins.str] = None,
    mdn_response: typing.Optional[builtins.str] = None,
    mdn_signing_algorithm: typing.Optional[builtins.str] = None,
    message_subject: typing.Optional[builtins.str] = None,
    partner_profile_id: typing.Optional[builtins.str] = None,
    preserve_content_type: typing.Optional[builtins.str] = None,
    signing_algorithm: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656490d886d172145f69b8d98e70a59952bed873b179e0d251c9b79d758b68cc(
    *,
    vpc_lattice: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnConnectorPropsMixin.ConnectorVpcLatticeEgressConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6ee7ad90d1f9bf04c456c2a1c673083f72f93dede70b5311e6b67743f885420(
    *,
    port_number: typing.Optional[jsii.Number] = None,
    resource_configuration_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63436161c886f895a24f2f45c1e1b8e392991e8a860e12bd776e7c511183f876(
    *,
    max_concurrent_connections: typing.Optional[jsii.Number] = None,
    trusted_host_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_secret_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b14335fbb9ee1cda416c677c3a38d55bb2cd6ea86efef248143f337da5b1b3(
    *,
    as2_id: typing.Optional[builtins.str] = None,
    certificate_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    profile_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5144fe085aac82b899c9a4a6099b3f9c4a12c068db11676403417f96ebaac730(
    props: typing.Union[CfnProfileMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1765a2a01ecc0c0a37c32777e8fd85a2ec44b9cbe5faad97f31621c6063536b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1035a5e8b5f717c7d075c3aa0e5165f6953e5fd8ecdb9baeb134cf4f4f203f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e36964bb0bddab8f68c308f08eb47db7e1d25d6ea0174df761b6fb46b58dd3d(
    log_type: builtins.str,
    log_delivery: _ILogsDelivery_0d3c9e29,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71970669867afa57b4745db45525041367a3fbe006e3a5a4adc8738a2ddbcf82(
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e0a334f483938fcdf24a2c87e3557cbb614fbab77871bdbd7b11c8e67189477(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1730dca516700d62c941dc912d24b68bd2a56ffef28f4c561a827c1d2580d414(
    *,
    certificate: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    endpoint_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_type: typing.Optional[builtins.str] = None,
    identity_provider_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.IdentityProviderDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    identity_provider_type: typing.Optional[builtins.str] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    logging_role: typing.Optional[builtins.str] = None,
    post_authentication_login_banner: typing.Optional[builtins.str] = None,
    pre_authentication_login_banner: typing.Optional[builtins.str] = None,
    protocol_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.ProtocolDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    protocols: typing.Optional[typing.Sequence[builtins.str]] = None,
    s3_storage_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.S3StorageOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_policy_name: typing.Optional[builtins.str] = None,
    structured_log_destinations: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    workflow_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.WorkflowDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__042ccbbfdf7e7d36884ff20c8712ccef4b964a4f0eac99b9d1eb0db2ebfbe99b(
    props: typing.Union[CfnServerMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd56694becd16517df00056a56eddd784fa8b918f7060b202dc1bd5a6c0a60d(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d324374c59b0a60a64977bd3b412d44e65253f8366f02aa8d3cd2992065112e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cc3e97a93d07e5cf5024032138214d503a99dcd2e3b21f90dcd0d0c7e1921ca(
    *,
    address_allocation_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc_endpoint_id: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb15ffc531949f7af8888c15d886123265e21091319aa3063240a26eed2981b(
    *,
    directory_id: typing.Optional[builtins.str] = None,
    function: typing.Optional[builtins.str] = None,
    invocation_role: typing.Optional[builtins.str] = None,
    sftp_authentication_methods: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f62871d14b99a94e2c324b17e50f60798405a65380dc80e27778e1d321d7012(
    *,
    as2_transports: typing.Optional[typing.Sequence[builtins.str]] = None,
    passive_ip: typing.Optional[builtins.str] = None,
    set_stat_option: typing.Optional[builtins.str] = None,
    tls_session_resumption_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6300e1ee54b5d168c996be8c027cf633a9a9199e52ad11dd0e028d1eec31ffe(
    *,
    directory_listing_optimization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c57d019e7cc747b76d8d4e9ec313943badd96d5289c563bb4aaa78c33bd4a3c(
    *,
    execution_role: typing.Optional[builtins.str] = None,
    workflow_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d2a768c518ec10b5e053a1e5be4054aa635f59b2a91e0d7476242c84a8b8df(
    *,
    on_partial_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.WorkflowDetailProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    on_upload: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnServerPropsMixin.WorkflowDetailProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__701804f8ee33dd080a247a81b17de6877df2c232c23b6183613b4b7ad5dac72c(
    delivery_stream: _aws_cdk_interfaces_aws_kinesisfirehose_ceddda9d.IDeliveryStreamRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52035871dbd9089c365e00bbeb4469b7e497d279f01fefe35caf62fbd22a2051(
    log_group: _aws_cdk_interfaces_aws_logs_ceddda9d.ILogGroupRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35618fdf0b584693dc925ac9a475d367d84ccf5e2a8c4717d0c2b1bd1a121a0c(
    bucket: _aws_cdk_interfaces_aws_s3_ceddda9d.IBucketRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f131b1d49a86f76530944ce2a9e56d84fcb94508d16fb2513d44322a42ae0dac(
    *,
    home_directory: typing.Optional[builtins.str] = None,
    home_directory_mappings: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.HomeDirectoryMapEntryProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    home_directory_type: typing.Optional[builtins.str] = None,
    policy: typing.Optional[builtins.str] = None,
    posix_profile: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnUserPropsMixin.PosixProfileProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role: typing.Optional[builtins.str] = None,
    server_id: typing.Optional[builtins.str] = None,
    ssh_public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfe9230efd44d1f97d0546d6a30817fc6a829908800ac86ef02b104bcc59bc5a(
    props: typing.Union[CfnUserMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3d308ff859ce0f05178b5f801df6284b6dfc8091d3d18c3d316450bd030cb5(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b71d9a8beeec157ea99d1b1be028f3679bdc87592e788a0ae25b21f1cd2e412(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1676ef100f1046872ec34d8923d1d18cbc0f97e4e811bde1732e86643db80898(
    *,
    entry: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10e8bd6f0999cd597162a9926843f28bd1ad182473c8eeb8b30ef14bc185c44(
    *,
    gid: typing.Optional[jsii.Number] = None,
    secondary_gids: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed9b006dbf6af3d1efe34030aa53f0da2b8e9e85e3519fbcb45860363580edef(
    *,
    access_endpoint: typing.Optional[builtins.str] = None,
    identity_provider_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebAppPropsMixin.IdentityProviderDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_app_customization: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebAppPropsMixin.WebAppCustomizationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_app_endpoint_policy: typing.Optional[builtins.str] = None,
    web_app_units: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWebAppPropsMixin.WebAppUnitsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a21016eccb46d0452ec65244d3115b725a15ae6e5e5c2abcddc3edacfa3c708(
    props: typing.Union[CfnWebAppMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0f815c696b02614203a39b0b97c86376173c79173d6ae08c44f387edb51a50(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0a4c5c9b32c22cab118372eb24aefaa1b7098cffc35d7f027715574054e431c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10efe00320dcf9ea5d7895b8c83d3c1f095a4b12e1827e22f645eee3ac45b50b(
    *,
    application_arn: typing.Optional[builtins.str] = None,
    instance_arn: typing.Optional[builtins.str] = None,
    role: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fa090c55edb450208ff8db50e7262f0949917c032add96b087e556e516c85d(
    *,
    favicon_file: typing.Optional[builtins.str] = None,
    logo_file: typing.Optional[builtins.str] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc2c0867850e846c5ba7e3a76048278af8ae96382b362776a6e6dafd923f182(
    *,
    provisioned: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2a5769fc8ecec392bcafea9f3eb2eb3ae8311dbdafd6960514aae8ba21ed30(
    *,
    description: typing.Optional[builtins.str] = None,
    on_exception_steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.WorkflowStepProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228a8b1a7e62595aa087fe397106c0935f500ec5f900e89539240ee721610ffd(
    props: typing.Union[CfnWorkflowMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd95daa1bbb426ad9817192fefb5ff6d13367c950a67e7b45c446543dc39af31(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97421d541661ce64d659bfc869752b8c253edd5242cf5195d642f2df8cd27270(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ca3fd8aff855c5d572103531040a0181ca9e8a00f880b4a39437dd28da88529(
    *,
    destination_file_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.InputFileLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    overwrite_existing: typing.Optional[builtins.str] = None,
    source_file_location: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8faa5abb5271a667b22b9b80b3dd7036ff7b50bde7f2e102cb3455ad35d483e1(
    *,
    file_system_id: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__226464fc6e49951d7ce4f42aafdff4eee86f55c995773d31ac5770ddb571fa51(
    *,
    efs_file_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.EfsInputFileLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_file_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.S3InputFileLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6e7ded4b787a500924cc244dd8eebbd4df1d8c090528a3600acfea291ed6ce(
    *,
    bucket: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd04be9f0ca672447e5e8e67b00f97aa6e6c09a582ccf531c153bc7265ca91b(
    *,
    copy_step_details: typing.Any = None,
    custom_step_details: typing.Any = None,
    decrypt_step_details: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnWorkflowPropsMixin.DecryptStepDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    delete_step_details: typing.Any = None,
    tag_step_details: typing.Any = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
