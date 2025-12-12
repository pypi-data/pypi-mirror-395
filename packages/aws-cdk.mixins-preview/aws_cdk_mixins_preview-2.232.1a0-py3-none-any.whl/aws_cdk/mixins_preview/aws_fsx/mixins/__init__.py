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
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnDataRepositoryAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "batch_import_meta_data_on_create": "batchImportMetaDataOnCreate",
        "data_repository_path": "dataRepositoryPath",
        "file_system_id": "fileSystemId",
        "file_system_path": "fileSystemPath",
        "imported_file_chunk_size": "importedFileChunkSize",
        "s3": "s3",
        "tags": "tags",
    },
)
class CfnDataRepositoryAssociationMixinProps:
    def __init__(
        self,
        *,
        batch_import_meta_data_on_create: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        data_repository_path: typing.Optional[builtins.str] = None,
        file_system_id: typing.Optional[builtins.str] = None,
        file_system_path: typing.Optional[builtins.str] = None,
        imported_file_chunk_size: typing.Optional[jsii.Number] = None,
        s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataRepositoryAssociationPropsMixin.S3Property", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDataRepositoryAssociationPropsMixin.

        :param batch_import_meta_data_on_create: A boolean flag indicating whether an import data repository task to import metadata should run after the data repository association is created. The task runs if this flag is set to ``true`` .
        :param data_repository_path: The path to the Amazon S3 data repository that will be linked to the file system. The path can be an S3 bucket or prefix in the format ``s3://myBucket/myPrefix/`` . This path specifies where in the S3 data repository files will be imported from or exported to.
        :param file_system_id: The ID of the file system on which the data repository association is configured.
        :param file_system_path: A path on the Amazon FSx for Lustre file system that points to a high-level directory (such as ``/ns1/`` ) or subdirectory (such as ``/ns1/subdir/`` ) that will be mapped 1-1 with ``DataRepositoryPath`` . The leading forward slash in the name is required. Two data repository associations cannot have overlapping file system paths. For example, if a data repository is associated with file system path ``/ns1/`` , then you cannot link another data repository with file system path ``/ns1/ns2`` . This path specifies where in your file system files will be exported from or imported to. This file system directory can be linked to only one Amazon S3 bucket, and no other S3 bucket can be linked to the directory. .. epigraph:: If you specify only a forward slash ( ``/`` ) as the file system path, you can link only one data repository to the file system. You can only specify "/" as the file system path for the first data repository associated with a file system.
        :param imported_file_chunk_size: For files imported from a data repository, this value determines the stripe count and maximum amount of data per file (in MiB) stored on a single physical disk. The maximum number of disks that a single file can be striped across is limited by the total number of disks that make up the file system or cache. The default chunk size is 1,024 MiB (1 GiB) and can go as high as 512,000 MiB (500 GiB). Amazon S3 objects have a maximum size of 5 TB.
        :param s3: The configuration for an Amazon S3 data repository linked to an Amazon FSx Lustre file system with a data repository association. The configuration defines which file events (new, changed, or deleted files or directories) are automatically imported from the linked data repository to the file system or automatically exported from the file system to the data repository.
        :param tags: A list of ``Tag`` values, with a maximum of 50 elements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
            
            cfn_data_repository_association_mixin_props = fsx_mixins.CfnDataRepositoryAssociationMixinProps(
                batch_import_meta_data_on_create=False,
                data_repository_path="dataRepositoryPath",
                file_system_id="fileSystemId",
                file_system_path="fileSystemPath",
                imported_file_chunk_size=123,
                s3=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.S3Property(
                    auto_export_policy=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty(
                        events=["events"]
                    ),
                    auto_import_policy=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty(
                        events=["events"]
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f18c530cbd9b42943b33b04069285529c5e31fcc7c2077852fec479a76a675)
            check_type(argname="argument batch_import_meta_data_on_create", value=batch_import_meta_data_on_create, expected_type=type_hints["batch_import_meta_data_on_create"])
            check_type(argname="argument data_repository_path", value=data_repository_path, expected_type=type_hints["data_repository_path"])
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument file_system_path", value=file_system_path, expected_type=type_hints["file_system_path"])
            check_type(argname="argument imported_file_chunk_size", value=imported_file_chunk_size, expected_type=type_hints["imported_file_chunk_size"])
            check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if batch_import_meta_data_on_create is not None:
            self._values["batch_import_meta_data_on_create"] = batch_import_meta_data_on_create
        if data_repository_path is not None:
            self._values["data_repository_path"] = data_repository_path
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id
        if file_system_path is not None:
            self._values["file_system_path"] = file_system_path
        if imported_file_chunk_size is not None:
            self._values["imported_file_chunk_size"] = imported_file_chunk_size
        if s3 is not None:
            self._values["s3"] = s3
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def batch_import_meta_data_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''A boolean flag indicating whether an import data repository task to import metadata should run after the data repository association is created.

        The task runs if this flag is set to ``true`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-batchimportmetadataoncreate
        '''
        result = self._values.get("batch_import_meta_data_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def data_repository_path(self) -> typing.Optional[builtins.str]:
        '''The path to the Amazon S3 data repository that will be linked to the file system.

        The path can be an S3 bucket or prefix in the format ``s3://myBucket/myPrefix/`` . This path specifies where in the S3 data repository files will be imported from or exported to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-datarepositorypath
        '''
        result = self._values.get("data_repository_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the file system on which the data repository association is configured.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-filesystemid
        '''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_path(self) -> typing.Optional[builtins.str]:
        '''A path on the Amazon FSx for Lustre file system that points to a high-level directory (such as ``/ns1/`` ) or subdirectory (such as ``/ns1/subdir/`` ) that will be mapped 1-1 with ``DataRepositoryPath`` .

        The leading forward slash in the name is required. Two data repository associations cannot have overlapping file system paths. For example, if a data repository is associated with file system path ``/ns1/`` , then you cannot link another data repository with file system path ``/ns1/ns2`` .

        This path specifies where in your file system files will be exported from or imported to. This file system directory can be linked to only one Amazon S3 bucket, and no other S3 bucket can be linked to the directory.
        .. epigraph::

           If you specify only a forward slash ( ``/`` ) as the file system path, you can link only one data repository to the file system. You can only specify "/" as the file system path for the first data repository associated with a file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-filesystempath
        '''
        result = self._values.get("file_system_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def imported_file_chunk_size(self) -> typing.Optional[jsii.Number]:
        '''For files imported from a data repository, this value determines the stripe count and maximum amount of data per file (in MiB) stored on a single physical disk.

        The maximum number of disks that a single file can be striped across is limited by the total number of disks that make up the file system or cache.

        The default chunk size is 1,024 MiB (1 GiB) and can go as high as 512,000 MiB (500 GiB). Amazon S3 objects have a maximum size of 5 TB.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-importedfilechunksize
        '''
        result = self._values.get("imported_file_chunk_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def s3(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataRepositoryAssociationPropsMixin.S3Property"]]:
        '''The configuration for an Amazon S3 data repository linked to an Amazon FSx Lustre file system with a data repository association.

        The configuration defines which file events (new, changed, or deleted files or directories) are automatically imported from the linked data repository to the file system or automatically exported from the file system to the data repository.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-s3
        '''
        result = self._values.get("s3")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataRepositoryAssociationPropsMixin.S3Property"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of ``Tag`` values, with a maximum of 50 elements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html#cfn-fsx-datarepositoryassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataRepositoryAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataRepositoryAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnDataRepositoryAssociationPropsMixin",
):
    '''Creates an Amazon FSx for Lustre data repository association (DRA).

    A data repository association is a link between a directory on the file system and an Amazon S3 bucket or prefix. You can have a maximum of 8 data repository associations on a file system. Data repository associations are supported on all FSx for Lustre 2.12 and newer file systems, excluding ``scratch_1`` deployment type.

    Each data repository association must have a unique Amazon FSx file system directory and a unique S3 bucket or prefix associated with it. You can configure a data repository association for automatic import only, for automatic export only, or for both. To learn more about linking a data repository to your file system, see `Linking your file system to an S3 bucket <https://docs.aws.amazon.com/fsx/latest/LustreGuide/create-dra-linked-data-repo.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-datarepositoryassociation.html
    :cloudformationResource: AWS::FSx::DataRepositoryAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
        
        cfn_data_repository_association_props_mixin = fsx_mixins.CfnDataRepositoryAssociationPropsMixin(fsx_mixins.CfnDataRepositoryAssociationMixinProps(
            batch_import_meta_data_on_create=False,
            data_repository_path="dataRepositoryPath",
            file_system_id="fileSystemId",
            file_system_path="fileSystemPath",
            imported_file_chunk_size=123,
            s3=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.S3Property(
                auto_export_policy=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty(
                    events=["events"]
                ),
                auto_import_policy=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty(
                    events=["events"]
                )
            ),
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
        props: typing.Union[CfnDataRepositoryAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FSx::DataRepositoryAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3c3d9b62f18422bc87258d8dfb708b123d1af0a51008013b8aa470018d12ec7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b05785691cc9c9d2d219f29ef18713948044a3ebbd0f2e48f27a23830f4c0e0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c05b79e9665dcbe3f574f204554caebfe19effd751e8107e9b006f229e3bc4c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataRepositoryAssociationMixinProps:
        return typing.cast(CfnDataRepositoryAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class AutoExportPolicyProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes a data repository association's automatic export policy.

            The ``AutoExportPolicy`` defines the types of updated objects on the file system that will be automatically exported to the data repository. As you create, modify, or delete files, Amazon FSx for Lustre automatically exports the defined changes asynchronously once your application finishes modifying the file.

            The ``AutoExportPolicy`` is only supported on Amazon FSx for Lustre file systems with a data repository association.

            :param events: The ``AutoExportPolicy`` can have the following event values:. - ``NEW`` - New files and directories are automatically exported to the data repository as they are added to the file system. - ``CHANGED`` - Changes to files and directories on the file system are automatically exported to the data repository. - ``DELETED`` - Files and directories are automatically deleted on the data repository when they are deleted on the file system. You can define any combination of event types for your ``AutoExportPolicy`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-autoexportpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                auto_export_policy_property = fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty(
                    events=["events"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04e3a64c8ddef2fb2a82bec993fe465983d8b420c2fbe2dbed16ef0eb3d6986a)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ``AutoExportPolicy`` can have the following event values:.

            - ``NEW`` - New files and directories are automatically exported to the data repository as they are added to the file system.
            - ``CHANGED`` - Changes to files and directories on the file system are automatically exported to the data repository.
            - ``DELETED`` - Files and directories are automatically deleted on the data repository when they are deleted on the file system.

            You can define any combination of event types for your ``AutoExportPolicy`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-autoexportpolicy.html#cfn-fsx-datarepositoryassociation-autoexportpolicy-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoExportPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"events": "events"},
    )
    class AutoImportPolicyProperty:
        def __init__(
            self,
            *,
            events: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Describes the data repository association's automatic import policy.

            The AutoImportPolicy defines how Amazon FSx keeps your file metadata and directory listings up to date by importing changes to your Amazon FSx for Lustre file system as you modify objects in a linked S3 bucket.

            The ``AutoImportPolicy`` is only supported on Amazon FSx for Lustre file systems with a data repository association.

            :param events: The ``AutoImportPolicy`` can have the following event values:. - ``NEW`` - Amazon FSx automatically imports metadata of files added to the linked S3 bucket that do not currently exist in the FSx file system. - ``CHANGED`` - Amazon FSx automatically updates file metadata and invalidates existing file content on the file system as files change in the data repository. - ``DELETED`` - Amazon FSx automatically deletes files on the file system as corresponding files are deleted in the data repository. You can define any combination of event types for your ``AutoImportPolicy`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-autoimportpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                auto_import_policy_property = fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty(
                    events=["events"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70779f052bf7e3b2341abea080853e4ca2398b05e71b7ad22a51e918c15aa0ca)
                check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if events is not None:
                self._values["events"] = events

        @builtins.property
        def events(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The ``AutoImportPolicy`` can have the following event values:.

            - ``NEW`` - Amazon FSx automatically imports metadata of files added to the linked S3 bucket that do not currently exist in the FSx file system.
            - ``CHANGED`` - Amazon FSx automatically updates file metadata and invalidates existing file content on the file system as files change in the data repository.
            - ``DELETED`` - Amazon FSx automatically deletes files on the file system as corresponding files are deleted in the data repository.

            You can define any combination of event types for your ``AutoImportPolicy`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-autoimportpolicy.html#cfn-fsx-datarepositoryassociation-autoimportpolicy-events
            '''
            result = self._values.get("events")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoImportPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnDataRepositoryAssociationPropsMixin.S3Property",
        jsii_struct_bases=[],
        name_mapping={
            "auto_export_policy": "autoExportPolicy",
            "auto_import_policy": "autoImportPolicy",
        },
    )
    class S3Property:
        def __init__(
            self,
            *,
            auto_export_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            auto_import_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for an Amazon S3 data repository linked to an Amazon FSx Lustre file system with a data repository association.

            The configuration defines which file events (new, changed, or deleted files or directories) are automatically imported from the linked data repository to the file system or automatically exported from the file system to the data repository.

            :param auto_export_policy: Describes a data repository association's automatic export policy. The ``AutoExportPolicy`` defines the types of updated objects on the file system that will be automatically exported to the data repository. As you create, modify, or delete files, Amazon FSx for Lustre automatically exports the defined changes asynchronously once your application finishes modifying the file. The ``AutoExportPolicy`` is only supported on Amazon FSx for Lustre file systems with a data repository association.
            :param auto_import_policy: Describes the data repository association's automatic import policy. The AutoImportPolicy defines how Amazon FSx keeps your file metadata and directory listings up to date by importing changes to your Amazon FSx for Lustre file system as you modify objects in a linked S3 bucket. The ``AutoImportPolicy`` is only supported on Amazon FSx for Lustre file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-s3.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                s3_property = fsx_mixins.CfnDataRepositoryAssociationPropsMixin.S3Property(
                    auto_export_policy=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty(
                        events=["events"]
                    ),
                    auto_import_policy=fsx_mixins.CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty(
                        events=["events"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e69765532a2897097211596c19c2be0b5e490c0c2c5d76964455dc7527d63f91)
                check_type(argname="argument auto_export_policy", value=auto_export_policy, expected_type=type_hints["auto_export_policy"])
                check_type(argname="argument auto_import_policy", value=auto_import_policy, expected_type=type_hints["auto_import_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_export_policy is not None:
                self._values["auto_export_policy"] = auto_export_policy
            if auto_import_policy is not None:
                self._values["auto_import_policy"] = auto_import_policy

        @builtins.property
        def auto_export_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty"]]:
            '''Describes a data repository association's automatic export policy.

            The ``AutoExportPolicy`` defines the types of updated objects on the file system that will be automatically exported to the data repository. As you create, modify, or delete files, Amazon FSx for Lustre automatically exports the defined changes asynchronously once your application finishes modifying the file.

            The ``AutoExportPolicy`` is only supported on Amazon FSx for Lustre file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-s3.html#cfn-fsx-datarepositoryassociation-s3-autoexportpolicy
            '''
            result = self._values.get("auto_export_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty"]], result)

        @builtins.property
        def auto_import_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty"]]:
            '''Describes the data repository association's automatic import policy.

            The AutoImportPolicy defines how Amazon FSx keeps your file metadata and directory listings up to date by importing changes to your Amazon FSx for Lustre file system as you modify objects in a linked S3 bucket.

            The ``AutoImportPolicy`` is only supported on Amazon FSx for Lustre file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-datarepositoryassociation-s3.html#cfn-fsx-datarepositoryassociation-s3-autoimportpolicy
            '''
            result = self._values.get("auto_import_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3Property(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_id": "backupId",
        "file_system_type": "fileSystemType",
        "file_system_type_version": "fileSystemTypeVersion",
        "kms_key_id": "kmsKeyId",
        "lustre_configuration": "lustreConfiguration",
        "network_type": "networkType",
        "ontap_configuration": "ontapConfiguration",
        "open_zfs_configuration": "openZfsConfiguration",
        "security_group_ids": "securityGroupIds",
        "storage_capacity": "storageCapacity",
        "storage_type": "storageType",
        "subnet_ids": "subnetIds",
        "tags": "tags",
        "windows_configuration": "windowsConfiguration",
    },
)
class CfnFileSystemMixinProps:
    def __init__(
        self,
        *,
        backup_id: typing.Optional[builtins.str] = None,
        file_system_type: typing.Optional[builtins.str] = None,
        file_system_type_version: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        lustre_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.LustreConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        network_type: typing.Optional[builtins.str] = None,
        ontap_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.OntapConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        open_zfs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.OpenZFSConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_capacity: typing.Optional[jsii.Number] = None,
        storage_type: typing.Optional[builtins.str] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        windows_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.WindowsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnFileSystemPropsMixin.

        :param backup_id: The ID of the file system backup that you are using to create a file system. For more information, see `CreateFileSystemFromBackup <https://docs.aws.amazon.com/fsx/latest/APIReference/API_CreateFileSystemFromBackup.html>`_ .
        :param file_system_type: The type of Amazon FSx file system, which can be ``LUSTRE`` , ``WINDOWS`` , ``ONTAP`` , or ``OPENZFS`` .
        :param file_system_type_version: For FSx for Lustre file systems, sets the Lustre version for the file system that you're creating. Valid values are ``2.10`` , ``2.12`` , and ``2.15`` : - ``2.10`` is supported by the Scratch and Persistent_1 Lustre deployment types. - ``2.12`` is supported by all Lustre deployment types, except for ``PERSISTENT_2`` with a metadata configuration mode. - ``2.15`` is supported by all Lustre deployment types and is recommended for all new file systems. Default value is ``2.10`` , except for the following deployments: - Default value is ``2.12`` when ``DeploymentType`` is set to ``PERSISTENT_2`` without a metadata configuration mode. - Default value is ``2.15`` when ``DeploymentType`` is set to ``PERSISTENT_2`` with a metadata configuration mode.
        :param kms_key_id: The ID of the AWS Key Management Service ( AWS ) key used to encrypt Amazon FSx file system data. Used as follows with Amazon FSx file system types: - Amazon FSx for Lustre ``PERSISTENT_1`` and ``PERSISTENT_2`` deployment types only. ``SCRATCH_1`` and ``SCRATCH_2`` types are encrypted using the Amazon FSx service AWS key for your account. - Amazon FSx for NetApp ONTAP - Amazon FSx for OpenZFS - Amazon FSx for Windows File Server If this ID isn't specified, the Amazon FSx-managed key for your account is used. For more information, see `Encrypt <https://docs.aws.amazon.com//kms/latest/APIReference/API_Encrypt.html>`_ in the *AWS Key Management Service API Reference* .
        :param lustre_configuration: The Lustre configuration for the file system being created. This configuration is required if the ``FileSystemType`` is set to ``LUSTRE`` . .. epigraph:: The following parameters are not supported when creating Lustre file systems with a data repository association. - ``AutoImportPolicy`` - ``ExportPath`` - ``ImportedChunkSize`` - ``ImportPath``
        :param network_type: The network type of the file system.
        :param ontap_configuration: The ONTAP configuration properties of the FSx for ONTAP file system that you are creating. This configuration is required if the ``FileSystemType`` is set to ``ONTAP`` .
        :param open_zfs_configuration: The Amazon FSx for OpenZFS configuration properties for the file system that you are creating. This configuration is required if the ``FileSystemType`` is set to ``OPENZFS`` .
        :param security_group_ids: A list of IDs specifying the security groups to apply to all network interfaces created for file system access. This list isn't returned in later requests to describe the file system. .. epigraph:: You must specify a security group if you are creating a Multi-AZ FSx for ONTAP file system in a VPC subnet that has been shared with you.
        :param storage_capacity: Sets the storage capacity of the file system that you're creating. ``StorageCapacity`` is required if you are creating a new file system. It is not required if you are creating a file system by restoring a backup. *FSx for Lustre file systems* - The amount of storage capacity that you can configure depends on the value that you set for ``StorageType`` and the Lustre ``DeploymentType`` , as follows: - For ``SCRATCH_2`` , ``PERSISTENT_2`` and ``PERSISTENT_1`` deployment types using SSD storage type, the valid values are 1200 GiB, 2400 GiB, and increments of 2400 GiB. - For ``PERSISTENT_1`` HDD file systems, valid values are increments of 6000 GiB for 12 MB/s/TiB file systems and increments of 1800 GiB for 40 MB/s/TiB file systems. - For ``SCRATCH_1`` deployment type, valid values are 1200 GiB, 2400 GiB, and increments of 3600 GiB. *FSx for ONTAP file systems* - The amount of SSD storage capacity that you can configure depends on the value of the ``HAPairs`` property. The minimum value is calculated as 1,024 GiB * HAPairs and the maximum is calculated as 524,288 GiB * HAPairs, up to a maximum amount of SSD storage capacity of 1,048,576 GiB (1 pebibyte). *FSx for OpenZFS file systems* - The amount of storage capacity that you can configure is from 64 GiB up to 524,288 GiB (512 TiB). If you are creating a file system from a backup, you can specify a storage capacity equal to or greater than the original file system's storage capacity. *FSx for Windows File Server file systems* - The amount of storage capacity that you can configure depends on the value that you set for ``StorageType`` as follows: - For SSD storage, valid values are 32 GiB-65,536 GiB (64 TiB). - For HDD storage, valid values are 2000 GiB-65,536 GiB (64 TiB).
        :param storage_type: Sets the storage class for the file system that you're creating. Valid values are ``SSD`` , ``HDD`` , and ``INTELLIGENT_TIERING`` . - Set to ``SSD`` to use solid state drive storage. SSD is supported on all Windows, Lustre, ONTAP, and OpenZFS deployment types. - Set to ``HDD`` to use hard disk drive storage, which is supported on ``SINGLE_AZ_2`` and ``MULTI_AZ_1`` Windows file system deployment types, and on ``PERSISTENT_1`` Lustre file system deployment types. - Set to ``INTELLIGENT_TIERING`` to use fully elastic, intelligently-tiered storage. Intelligent-Tiering is only available for OpenZFS file systems with the Multi-AZ deployment type and for Lustre file systems with the Persistent_2 deployment type. Default value is ``SSD`` . For more information, see `Storage type options <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/optimize-fsx-costs.html#storage-type-options>`_ in the *FSx for Windows File Server User Guide* , `FSx for Lustre storage classes <https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-fsx-lustre.html#lustre-storage-classes>`_ in the *FSx for Lustre User Guide* , and `Working with Intelligent-Tiering <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance-intelligent-tiering>`_ in the *Amazon FSx for OpenZFS User Guide* .
        :param subnet_ids: Specifies the IDs of the subnets that the file system will be accessible from. For Windows and ONTAP ``MULTI_AZ_1`` deployment types,provide exactly two subnet IDs, one for the preferred file server and one for the standby file server. You specify one of these subnets as the preferred subnet using the ``WindowsConfiguration > PreferredSubnetID`` or ``OntapConfiguration > PreferredSubnetID`` properties. For more information about Multi-AZ file system configuration, see `Availability and durability: Single-AZ and Multi-AZ file systems <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html>`_ in the *Amazon FSx for Windows User Guide* and `Availability and durability <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/high-availability-multiAZ.html>`_ in the *Amazon FSx for ONTAP User Guide* . For Windows ``SINGLE_AZ_1`` and ``SINGLE_AZ_2`` and all Lustre deployment types, provide exactly one subnet ID. The file server is launched in that subnet's Availability Zone.
        :param tags: The tags to associate with the file system. For more information, see `Tagging your Amazon FSx resources <https://docs.aws.amazon.com/fsx/latest/LustreGuide/tag-resources.html>`_ in the *Amazon FSx for Lustre User Guide* .
        :param windows_configuration: The configuration object for the Microsoft Windows file system you are creating. This configuration is required if ``FileSystemType`` is set to ``WINDOWS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
            
            cfn_file_system_mixin_props = fsx_mixins.CfnFileSystemMixinProps(
                backup_id="backupId",
                file_system_type="fileSystemType",
                file_system_type_version="fileSystemTypeVersion",
                kms_key_id="kmsKeyId",
                lustre_configuration=fsx_mixins.CfnFileSystemPropsMixin.LustreConfigurationProperty(
                    auto_import_policy="autoImportPolicy",
                    automatic_backup_retention_days=123,
                    copy_tags_to_backups=False,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    data_compression_type="dataCompressionType",
                    data_read_cache_configuration=fsx_mixins.CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty(
                        size_gi_b=123,
                        sizing_mode="sizingMode"
                    ),
                    deployment_type="deploymentType",
                    drive_cache_type="driveCacheType",
                    efa_enabled=False,
                    export_path="exportPath",
                    imported_file_chunk_size=123,
                    import_path="importPath",
                    metadata_configuration=fsx_mixins.CfnFileSystemPropsMixin.MetadataConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    per_unit_storage_throughput=123,
                    throughput_capacity=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                ),
                network_type="networkType",
                ontap_configuration=fsx_mixins.CfnFileSystemPropsMixin.OntapConfigurationProperty(
                    automatic_backup_retention_days=123,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    deployment_type="deploymentType",
                    disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    endpoint_ip_address_range="endpointIpAddressRange",
                    endpoint_ipv6_address_range="endpointIpv6AddressRange",
                    fsx_admin_password="fsxAdminPassword",
                    ha_pairs=123,
                    preferred_subnet_id="preferredSubnetId",
                    route_table_ids=["routeTableIds"],
                    throughput_capacity=123,
                    throughput_capacity_per_ha_pair=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                ),
                open_zfs_configuration=fsx_mixins.CfnFileSystemPropsMixin.OpenZFSConfigurationProperty(
                    automatic_backup_retention_days=123,
                    copy_tags_to_backups=False,
                    copy_tags_to_volumes=False,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    deployment_type="deploymentType",
                    disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    endpoint_ip_address_range="endpointIpAddressRange",
                    endpoint_ipv6_address_range="endpointIpv6AddressRange",
                    options=["options"],
                    preferred_subnet_id="preferredSubnetId",
                    read_cache_configuration=fsx_mixins.CfnFileSystemPropsMixin.ReadCacheConfigurationProperty(
                        size_gi_b=123,
                        sizing_mode="sizingMode"
                    ),
                    root_volume_configuration=fsx_mixins.CfnFileSystemPropsMixin.RootVolumeConfigurationProperty(
                        copy_tags_to_snapshots=False,
                        data_compression_type="dataCompressionType",
                        nfs_exports=[fsx_mixins.CfnFileSystemPropsMixin.NfsExportsProperty(
                            client_configurations=[fsx_mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty(
                                clients="clients",
                                options=["options"]
                            )]
                        )],
                        read_only=False,
                        record_size_ki_b=123,
                        user_and_group_quotas=[fsx_mixins.CfnFileSystemPropsMixin.UserAndGroupQuotasProperty(
                            id=123,
                            storage_capacity_quota_gi_b=123,
                            type="type"
                        )]
                    ),
                    route_table_ids=["routeTableIds"],
                    throughput_capacity=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                ),
                security_group_ids=["securityGroupIds"],
                storage_capacity=123,
                storage_type="storageType",
                subnet_ids=["subnetIds"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                windows_configuration=fsx_mixins.CfnFileSystemPropsMixin.WindowsConfigurationProperty(
                    active_directory_id="activeDirectoryId",
                    aliases=["aliases"],
                    audit_log_configuration=fsx_mixins.CfnFileSystemPropsMixin.AuditLogConfigurationProperty(
                        audit_log_destination="auditLogDestination",
                        file_access_audit_log_level="fileAccessAuditLogLevel",
                        file_share_access_audit_log_level="fileShareAccessAuditLogLevel"
                    ),
                    automatic_backup_retention_days=123,
                    copy_tags_to_backups=False,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    deployment_type="deploymentType",
                    disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    preferred_subnet_id="preferredSubnetId",
                    self_managed_active_directory_configuration=fsx_mixins.CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                        dns_ips=["dnsIps"],
                        domain_join_service_account_secret="domainJoinServiceAccountSecret",
                        domain_name="domainName",
                        file_system_administrators_group="fileSystemAdministratorsGroup",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                        password="password",
                        user_name="userName"
                    ),
                    throughput_capacity=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3efed9332feac3aac4ec39dd5f1c76f8ca164e1adb99201db1336c9e9edb4e19)
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument file_system_type", value=file_system_type, expected_type=type_hints["file_system_type"])
            check_type(argname="argument file_system_type_version", value=file_system_type_version, expected_type=type_hints["file_system_type_version"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument lustre_configuration", value=lustre_configuration, expected_type=type_hints["lustre_configuration"])
            check_type(argname="argument network_type", value=network_type, expected_type=type_hints["network_type"])
            check_type(argname="argument ontap_configuration", value=ontap_configuration, expected_type=type_hints["ontap_configuration"])
            check_type(argname="argument open_zfs_configuration", value=open_zfs_configuration, expected_type=type_hints["open_zfs_configuration"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument storage_capacity", value=storage_capacity, expected_type=type_hints["storage_capacity"])
            check_type(argname="argument storage_type", value=storage_type, expected_type=type_hints["storage_type"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument windows_configuration", value=windows_configuration, expected_type=type_hints["windows_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if file_system_type is not None:
            self._values["file_system_type"] = file_system_type
        if file_system_type_version is not None:
            self._values["file_system_type_version"] = file_system_type_version
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if lustre_configuration is not None:
            self._values["lustre_configuration"] = lustre_configuration
        if network_type is not None:
            self._values["network_type"] = network_type
        if ontap_configuration is not None:
            self._values["ontap_configuration"] = ontap_configuration
        if open_zfs_configuration is not None:
            self._values["open_zfs_configuration"] = open_zfs_configuration
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if storage_capacity is not None:
            self._values["storage_capacity"] = storage_capacity
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags
        if windows_configuration is not None:
            self._values["windows_configuration"] = windows_configuration

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the file system backup that you are using to create a file system.

        For more information, see `CreateFileSystemFromBackup <https://docs.aws.amazon.com/fsx/latest/APIReference/API_CreateFileSystemFromBackup.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-backupid
        '''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_type(self) -> typing.Optional[builtins.str]:
        '''The type of Amazon FSx file system, which can be ``LUSTRE`` , ``WINDOWS`` , ``ONTAP`` , or ``OPENZFS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-filesystemtype
        '''
        result = self._values.get("file_system_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def file_system_type_version(self) -> typing.Optional[builtins.str]:
        '''For FSx for Lustre file systems, sets the Lustre version for the file system that you're creating.

        Valid values are ``2.10`` , ``2.12`` , and ``2.15`` :

        - ``2.10`` is supported by the Scratch and Persistent_1 Lustre deployment types.
        - ``2.12`` is supported by all Lustre deployment types, except for ``PERSISTENT_2`` with a metadata configuration mode.
        - ``2.15`` is supported by all Lustre deployment types and is recommended for all new file systems.

        Default value is ``2.10`` , except for the following deployments:

        - Default value is ``2.12`` when ``DeploymentType`` is set to ``PERSISTENT_2`` without a metadata configuration mode.
        - Default value is ``2.15`` when ``DeploymentType`` is set to ``PERSISTENT_2`` with a metadata configuration mode.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-filesystemtypeversion
        '''
        result = self._values.get("file_system_type_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service ( AWS  ) key used to encrypt Amazon FSx file system data.

        Used as follows with Amazon FSx file system types:

        - Amazon FSx for Lustre ``PERSISTENT_1`` and ``PERSISTENT_2`` deployment types only.

        ``SCRATCH_1`` and ``SCRATCH_2`` types are encrypted using the Amazon FSx service AWS  key for your account.

        - Amazon FSx for NetApp ONTAP
        - Amazon FSx for OpenZFS
        - Amazon FSx for Windows File Server

        If this ID isn't specified, the Amazon FSx-managed key for your account is used. For more information, see `Encrypt <https://docs.aws.amazon.com//kms/latest/APIReference/API_Encrypt.html>`_ in the *AWS Key Management Service API Reference* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lustre_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.LustreConfigurationProperty"]]:
        '''The Lustre configuration for the file system being created.

        This configuration is required if the ``FileSystemType`` is set to ``LUSTRE`` .
        .. epigraph::

           The following parameters are not supported when creating Lustre file systems with a data repository association.

           - ``AutoImportPolicy``
           - ``ExportPath``
           - ``ImportedChunkSize``
           - ``ImportPath``

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-lustreconfiguration
        '''
        result = self._values.get("lustre_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.LustreConfigurationProperty"]], result)

    @builtins.property
    def network_type(self) -> typing.Optional[builtins.str]:
        '''The network type of the file system.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-networktype
        '''
        result = self._values.get("network_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ontap_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.OntapConfigurationProperty"]]:
        '''The ONTAP configuration properties of the FSx for ONTAP file system that you are creating.

        This configuration is required if the ``FileSystemType`` is set to ``ONTAP`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-ontapconfiguration
        '''
        result = self._values.get("ontap_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.OntapConfigurationProperty"]], result)

    @builtins.property
    def open_zfs_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.OpenZFSConfigurationProperty"]]:
        '''The Amazon FSx for OpenZFS configuration properties for the file system that you are creating.

        This configuration is required if the ``FileSystemType`` is set to ``OPENZFS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-openzfsconfiguration
        '''
        result = self._values.get("open_zfs_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.OpenZFSConfigurationProperty"]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of IDs specifying the security groups to apply to all network interfaces created for file system access.

        This list isn't returned in later requests to describe the file system.
        .. epigraph::

           You must specify a security group if you are creating a Multi-AZ FSx for ONTAP file system in a VPC subnet that has been shared with you.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_capacity(self) -> typing.Optional[jsii.Number]:
        '''Sets the storage capacity of the file system that you're creating.

        ``StorageCapacity`` is required if you are creating a new file system. It is not required if you are creating a file system by restoring a backup.

        *FSx for Lustre file systems* - The amount of storage capacity that you can configure depends on the value that you set for ``StorageType`` and the Lustre ``DeploymentType`` , as follows:

        - For ``SCRATCH_2`` , ``PERSISTENT_2`` and ``PERSISTENT_1`` deployment types using SSD storage type, the valid values are 1200 GiB, 2400 GiB, and increments of 2400 GiB.
        - For ``PERSISTENT_1`` HDD file systems, valid values are increments of 6000 GiB for 12 MB/s/TiB file systems and increments of 1800 GiB for 40 MB/s/TiB file systems.
        - For ``SCRATCH_1`` deployment type, valid values are 1200 GiB, 2400 GiB, and increments of 3600 GiB.

        *FSx for ONTAP file systems* - The amount of SSD storage capacity that you can configure depends on the value of the ``HAPairs`` property. The minimum value is calculated as 1,024 GiB * HAPairs and the maximum is calculated as 524,288 GiB * HAPairs, up to a maximum amount of SSD storage capacity of 1,048,576 GiB (1 pebibyte).

        *FSx for OpenZFS file systems* - The amount of storage capacity that you can configure is from 64 GiB up to 524,288 GiB (512 TiB). If you are creating a file system from a backup, you can specify a storage capacity equal to or greater than the original file system's storage capacity.

        *FSx for Windows File Server file systems* - The amount of storage capacity that you can configure depends on the value that you set for ``StorageType`` as follows:

        - For SSD storage, valid values are 32 GiB-65,536 GiB (64 TiB).
        - For HDD storage, valid values are 2000 GiB-65,536 GiB (64 TiB).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-storagecapacity
        '''
        result = self._values.get("storage_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def storage_type(self) -> typing.Optional[builtins.str]:
        '''Sets the storage class for the file system that you're creating.

        Valid values are ``SSD`` , ``HDD`` , and ``INTELLIGENT_TIERING`` .

        - Set to ``SSD`` to use solid state drive storage. SSD is supported on all Windows, Lustre, ONTAP, and OpenZFS deployment types.
        - Set to ``HDD`` to use hard disk drive storage, which is supported on ``SINGLE_AZ_2`` and ``MULTI_AZ_1`` Windows file system deployment types, and on ``PERSISTENT_1`` Lustre file system deployment types.
        - Set to ``INTELLIGENT_TIERING`` to use fully elastic, intelligently-tiered storage. Intelligent-Tiering is only available for OpenZFS file systems with the Multi-AZ deployment type and for Lustre file systems with the Persistent_2 deployment type.

        Default value is ``SSD`` . For more information, see `Storage type options <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/optimize-fsx-costs.html#storage-type-options>`_ in the *FSx for Windows File Server User Guide* , `FSx for Lustre storage classes <https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-fsx-lustre.html#lustre-storage-classes>`_ in the *FSx for Lustre User Guide* , and `Working with Intelligent-Tiering <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance-intelligent-tiering>`_ in the *Amazon FSx for OpenZFS User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-storagetype
        '''
        result = self._values.get("storage_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies the IDs of the subnets that the file system will be accessible from.

        For Windows and ONTAP ``MULTI_AZ_1`` deployment types,provide exactly two subnet IDs, one for the preferred file server and one for the standby file server. You specify one of these subnets as the preferred subnet using the ``WindowsConfiguration > PreferredSubnetID`` or ``OntapConfiguration > PreferredSubnetID`` properties. For more information about Multi-AZ file system configuration, see `Availability and durability: Single-AZ and Multi-AZ file systems <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html>`_ in the *Amazon FSx for Windows User Guide* and `Availability and durability <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/high-availability-multiAZ.html>`_ in the *Amazon FSx for ONTAP User Guide* .

        For Windows ``SINGLE_AZ_1`` and ``SINGLE_AZ_2`` and all Lustre deployment types, provide exactly one subnet ID. The file server is launched in that subnet's Availability Zone.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The tags to associate with the file system.

        For more information, see `Tagging your Amazon FSx resources <https://docs.aws.amazon.com/fsx/latest/LustreGuide/tag-resources.html>`_ in the *Amazon FSx for Lustre User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def windows_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.WindowsConfigurationProperty"]]:
        '''The configuration object for the Microsoft Windows file system you are creating.

        This configuration is required if ``FileSystemType`` is set to ``WINDOWS`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html#cfn-fsx-filesystem-windowsconfiguration
        '''
        result = self._values.get("windows_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.WindowsConfigurationProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFileSystemMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnFileSystemPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin",
):
    '''The ``AWS::FSx::FileSystem`` resource is an Amazon FSx resource type that specifies an Amazon FSx file system.

    You can create any of the following supported file system types:

    - Amazon FSx for Lustre
    - Amazon FSx for NetApp ONTAP
    - FSx for OpenZFS
    - Amazon FSx for Windows File Server

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-filesystem.html
    :cloudformationResource: AWS::FSx::FileSystem
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
        
        cfn_file_system_props_mixin = fsx_mixins.CfnFileSystemPropsMixin(fsx_mixins.CfnFileSystemMixinProps(
            backup_id="backupId",
            file_system_type="fileSystemType",
            file_system_type_version="fileSystemTypeVersion",
            kms_key_id="kmsKeyId",
            lustre_configuration=fsx_mixins.CfnFileSystemPropsMixin.LustreConfigurationProperty(
                auto_import_policy="autoImportPolicy",
                automatic_backup_retention_days=123,
                copy_tags_to_backups=False,
                daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                data_compression_type="dataCompressionType",
                data_read_cache_configuration=fsx_mixins.CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty(
                    size_gi_b=123,
                    sizing_mode="sizingMode"
                ),
                deployment_type="deploymentType",
                drive_cache_type="driveCacheType",
                efa_enabled=False,
                export_path="exportPath",
                imported_file_chunk_size=123,
                import_path="importPath",
                metadata_configuration=fsx_mixins.CfnFileSystemPropsMixin.MetadataConfigurationProperty(
                    iops=123,
                    mode="mode"
                ),
                per_unit_storage_throughput=123,
                throughput_capacity=123,
                weekly_maintenance_start_time="weeklyMaintenanceStartTime"
            ),
            network_type="networkType",
            ontap_configuration=fsx_mixins.CfnFileSystemPropsMixin.OntapConfigurationProperty(
                automatic_backup_retention_days=123,
                daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                deployment_type="deploymentType",
                disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                    iops=123,
                    mode="mode"
                ),
                endpoint_ip_address_range="endpointIpAddressRange",
                endpoint_ipv6_address_range="endpointIpv6AddressRange",
                fsx_admin_password="fsxAdminPassword",
                ha_pairs=123,
                preferred_subnet_id="preferredSubnetId",
                route_table_ids=["routeTableIds"],
                throughput_capacity=123,
                throughput_capacity_per_ha_pair=123,
                weekly_maintenance_start_time="weeklyMaintenanceStartTime"
            ),
            open_zfs_configuration=fsx_mixins.CfnFileSystemPropsMixin.OpenZFSConfigurationProperty(
                automatic_backup_retention_days=123,
                copy_tags_to_backups=False,
                copy_tags_to_volumes=False,
                daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                deployment_type="deploymentType",
                disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                    iops=123,
                    mode="mode"
                ),
                endpoint_ip_address_range="endpointIpAddressRange",
                endpoint_ipv6_address_range="endpointIpv6AddressRange",
                options=["options"],
                preferred_subnet_id="preferredSubnetId",
                read_cache_configuration=fsx_mixins.CfnFileSystemPropsMixin.ReadCacheConfigurationProperty(
                    size_gi_b=123,
                    sizing_mode="sizingMode"
                ),
                root_volume_configuration=fsx_mixins.CfnFileSystemPropsMixin.RootVolumeConfigurationProperty(
                    copy_tags_to_snapshots=False,
                    data_compression_type="dataCompressionType",
                    nfs_exports=[fsx_mixins.CfnFileSystemPropsMixin.NfsExportsProperty(
                        client_configurations=[fsx_mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty(
                            clients="clients",
                            options=["options"]
                        )]
                    )],
                    read_only=False,
                    record_size_ki_b=123,
                    user_and_group_quotas=[fsx_mixins.CfnFileSystemPropsMixin.UserAndGroupQuotasProperty(
                        id=123,
                        storage_capacity_quota_gi_b=123,
                        type="type"
                    )]
                ),
                route_table_ids=["routeTableIds"],
                throughput_capacity=123,
                weekly_maintenance_start_time="weeklyMaintenanceStartTime"
            ),
            security_group_ids=["securityGroupIds"],
            storage_capacity=123,
            storage_type="storageType",
            subnet_ids=["subnetIds"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            windows_configuration=fsx_mixins.CfnFileSystemPropsMixin.WindowsConfigurationProperty(
                active_directory_id="activeDirectoryId",
                aliases=["aliases"],
                audit_log_configuration=fsx_mixins.CfnFileSystemPropsMixin.AuditLogConfigurationProperty(
                    audit_log_destination="auditLogDestination",
                    file_access_audit_log_level="fileAccessAuditLogLevel",
                    file_share_access_audit_log_level="fileShareAccessAuditLogLevel"
                ),
                automatic_backup_retention_days=123,
                copy_tags_to_backups=False,
                daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                deployment_type="deploymentType",
                disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                    iops=123,
                    mode="mode"
                ),
                preferred_subnet_id="preferredSubnetId",
                self_managed_active_directory_configuration=fsx_mixins.CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                    dns_ips=["dnsIps"],
                    domain_join_service_account_secret="domainJoinServiceAccountSecret",
                    domain_name="domainName",
                    file_system_administrators_group="fileSystemAdministratorsGroup",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                    password="password",
                    user_name="userName"
                ),
                throughput_capacity=123,
                weekly_maintenance_start_time="weeklyMaintenanceStartTime"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnFileSystemMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FSx::FileSystem``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4abfb06d1b695291099ea2cd1d7a4ca2ba8bec43056cd408317e947e72738f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c28e79c329ffbd8028e069c7a410455d5ace130792592908d2b877df23e42a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed093cb42d5388372c74ae2fd0af250ac1a539f312cad0072eda10d42f4a9766)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnFileSystemMixinProps:
        return typing.cast(CfnFileSystemMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.AuditLogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audit_log_destination": "auditLogDestination",
            "file_access_audit_log_level": "fileAccessAuditLogLevel",
            "file_share_access_audit_log_level": "fileShareAccessAuditLogLevel",
        },
    )
    class AuditLogConfigurationProperty:
        def __init__(
            self,
            *,
            audit_log_destination: typing.Optional[builtins.str] = None,
            file_access_audit_log_level: typing.Optional[builtins.str] = None,
            file_share_access_audit_log_level: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that Amazon FSx for Windows File Server uses to audit and log user accesses of files, folders, and file shares on the Amazon FSx for Windows File Server file system.

            :param audit_log_destination: The Amazon Resource Name (ARN) for the destination of the audit logs. The destination can be any Amazon CloudWatch Logs log group ARN or Amazon Kinesis Data Firehose delivery stream ARN. The name of the Amazon CloudWatch Logs log group must begin with the ``/aws/fsx`` prefix. The name of the Amazon Kinesis Data Firehose delivery stream must begin with the ``aws-fsx`` prefix. The destination ARN (either CloudWatch Logs log group or Kinesis Data Firehose delivery stream) must be in the same AWS partition, AWS Region , and AWS account as your Amazon FSx file system.
            :param file_access_audit_log_level: Sets which attempt type is logged by Amazon FSx for file and folder accesses. - ``SUCCESS_ONLY`` - only successful attempts to access files or folders are logged. - ``FAILURE_ONLY`` - only failed attempts to access files or folders are logged. - ``SUCCESS_AND_FAILURE`` - both successful attempts and failed attempts to access files or folders are logged. - ``DISABLED`` - access auditing of files and folders is turned off.
            :param file_share_access_audit_log_level: Sets which attempt type is logged by Amazon FSx for file share accesses. - ``SUCCESS_ONLY`` - only successful attempts to access file shares are logged. - ``FAILURE_ONLY`` - only failed attempts to access file shares are logged. - ``SUCCESS_AND_FAILURE`` - both successful attempts and failed attempts to access file shares are logged. - ``DISABLED`` - access auditing of file shares is turned off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-auditlogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                audit_log_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.AuditLogConfigurationProperty(
                    audit_log_destination="auditLogDestination",
                    file_access_audit_log_level="fileAccessAuditLogLevel",
                    file_share_access_audit_log_level="fileShareAccessAuditLogLevel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b9b3a33aa892a21210df0361c175fb3249662bb3e1e2671ce6f885c04d01b0c)
                check_type(argname="argument audit_log_destination", value=audit_log_destination, expected_type=type_hints["audit_log_destination"])
                check_type(argname="argument file_access_audit_log_level", value=file_access_audit_log_level, expected_type=type_hints["file_access_audit_log_level"])
                check_type(argname="argument file_share_access_audit_log_level", value=file_share_access_audit_log_level, expected_type=type_hints["file_share_access_audit_log_level"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audit_log_destination is not None:
                self._values["audit_log_destination"] = audit_log_destination
            if file_access_audit_log_level is not None:
                self._values["file_access_audit_log_level"] = file_access_audit_log_level
            if file_share_access_audit_log_level is not None:
                self._values["file_share_access_audit_log_level"] = file_share_access_audit_log_level

        @builtins.property
        def audit_log_destination(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the destination of the audit logs.

            The destination can be any Amazon CloudWatch Logs log group ARN or Amazon Kinesis Data Firehose delivery stream ARN.

            The name of the Amazon CloudWatch Logs log group must begin with the ``/aws/fsx`` prefix. The name of the Amazon Kinesis Data Firehose delivery stream must begin with the ``aws-fsx`` prefix.

            The destination ARN (either CloudWatch Logs log group or Kinesis Data Firehose delivery stream) must be in the same AWS partition, AWS Region , and AWS account as your Amazon FSx file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-auditlogconfiguration.html#cfn-fsx-filesystem-auditlogconfiguration-auditlogdestination
            '''
            result = self._values.get("audit_log_destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_access_audit_log_level(self) -> typing.Optional[builtins.str]:
            '''Sets which attempt type is logged by Amazon FSx for file and folder accesses.

            - ``SUCCESS_ONLY`` - only successful attempts to access files or folders are logged.
            - ``FAILURE_ONLY`` - only failed attempts to access files or folders are logged.
            - ``SUCCESS_AND_FAILURE`` - both successful attempts and failed attempts to access files or folders are logged.
            - ``DISABLED`` - access auditing of files and folders is turned off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-auditlogconfiguration.html#cfn-fsx-filesystem-auditlogconfiguration-fileaccessauditloglevel
            '''
            result = self._values.get("file_access_audit_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_share_access_audit_log_level(self) -> typing.Optional[builtins.str]:
            '''Sets which attempt type is logged by Amazon FSx for file share accesses.

            - ``SUCCESS_ONLY`` - only successful attempts to access file shares are logged.
            - ``FAILURE_ONLY`` - only failed attempts to access file shares are logged.
            - ``SUCCESS_AND_FAILURE`` - both successful attempts and failed attempts to access file shares are logged.
            - ``DISABLED`` - access auditing of file shares is turned off.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-auditlogconfiguration.html#cfn-fsx-filesystem-auditlogconfiguration-fileshareaccessauditloglevel
            '''
            result = self._values.get("file_share_access_audit_log_level")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuditLogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={"clients": "clients", "options": "options"},
    )
    class ClientConfigurationsProperty:
        def __init__(
            self,
            *,
            clients: typing.Optional[builtins.str] = None,
            options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies who can mount an OpenZFS file system and the options available while mounting the file system.

            :param clients: A value that specifies who can mount the file system. You can provide a wildcard character ( ``*`` ), an IP address ( ``0.0.0.0`` ), or a CIDR address ( ``192.0.2.0/24`` ). By default, Amazon FSx uses the wildcard character when specifying the client.
            :param options: The options to use when mounting the file system. For a list of options that you can use with Network File System (NFS), see the `exports(5) - Linux man page <https://docs.aws.amazon.com/https://linux.die.net/man/5/exports>`_ . When choosing your options, consider the following: - ``crossmnt`` is used by default. If you don't specify ``crossmnt`` when changing the client configuration, you won't be able to see or access snapshots in your file system's snapshot directory. - ``sync`` is used by default. If you instead specify ``async`` , the system acknowledges writes before writing to disk. If the system crashes before the writes are finished, you lose the unwritten data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-clientconfigurations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                client_configurations_property = fsx_mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty(
                    clients="clients",
                    options=["options"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6ea3e0235b0c5fd28fd74bedcefac302f669a038d9a91957bbfbeeaea8ca4d5d)
                check_type(argname="argument clients", value=clients, expected_type=type_hints["clients"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clients is not None:
                self._values["clients"] = clients
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def clients(self) -> typing.Optional[builtins.str]:
            '''A value that specifies who can mount the file system.

            You can provide a wildcard character ( ``*`` ), an IP address ( ``0.0.0.0`` ), or a CIDR address ( ``192.0.2.0/24`` ). By default, Amazon FSx uses the wildcard character when specifying the client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-clientconfigurations.html#cfn-fsx-filesystem-clientconfigurations-clients
            '''
            result = self._values.get("clients")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The options to use when mounting the file system.

            For a list of options that you can use with Network File System (NFS), see the `exports(5) - Linux man page <https://docs.aws.amazon.com/https://linux.die.net/man/5/exports>`_ . When choosing your options, consider the following:

            - ``crossmnt`` is used by default. If you don't specify ``crossmnt`` when changing the client configuration, you won't be able to see or access snapshots in your file system's snapshot directory.
            - ``sync`` is used by default. If you instead specify ``async`` , the system acknowledges writes before writing to disk. If the system crashes before the writes are finished, you lose the unwritten data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-clientconfigurations.html#cfn-fsx-filesystem-clientconfigurations-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"size_gib": "sizeGiB", "sizing_mode": "sizingMode"},
    )
    class DataReadCacheConfigurationProperty:
        def __init__(
            self,
            *,
            size_gib: typing.Optional[jsii.Number] = None,
            sizing_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the optional provisioned SSD read cache on Amazon FSx for Lustre file systems that use the Intelligent-Tiering storage class.

            :param size_gib: Required if ``SizingMode`` is set to ``USER_PROVISIONED`` . Specifies the size of the file system's SSD read cache, in gibibytes (GiB).
            :param sizing_mode: Specifies how the provisioned SSD read cache is sized, as follows:. - Set to ``NO_CACHE`` if you do not want to use an SSD read cache with your Intelligent-Tiering file system. - Set to ``USER_PROVISIONED`` to specify the exact size of your SSD read cache. - Set to ``PROPORTIONAL_TO_THROUGHPUT_CAPACITY`` to have your SSD read cache automatically sized based on your throughput capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-datareadcacheconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                data_read_cache_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty(
                    size_gi_b=123,
                    sizing_mode="sizingMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2b1aefdcecdc9b4434caa6370423269f48024d2e1ec72829e40f74f89bbe5fe)
                check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
                check_type(argname="argument sizing_mode", value=sizing_mode, expected_type=type_hints["sizing_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size_gib is not None:
                self._values["size_gib"] = size_gib
            if sizing_mode is not None:
                self._values["sizing_mode"] = sizing_mode

        @builtins.property
        def size_gib(self) -> typing.Optional[jsii.Number]:
            '''Required if ``SizingMode`` is set to ``USER_PROVISIONED`` .

            Specifies the size of the file system's SSD read cache, in gibibytes (GiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-datareadcacheconfiguration.html#cfn-fsx-filesystem-datareadcacheconfiguration-sizegib
            '''
            result = self._values.get("size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def sizing_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies how the provisioned SSD read cache is sized, as follows:.

            - Set to ``NO_CACHE`` if you do not want to use an SSD read cache with your Intelligent-Tiering file system.
            - Set to ``USER_PROVISIONED`` to specify the exact size of your SSD read cache.
            - Set to ``PROPORTIONAL_TO_THROUGHPUT_CAPACITY`` to have your SSD read cache automatically sized based on your throughput capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-datareadcacheconfiguration.html#cfn-fsx-filesystem-datareadcacheconfiguration-sizingmode
            '''
            result = self._values.get("sizing_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataReadCacheConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"iops": "iops", "mode": "mode"},
    )
    class DiskIopsConfigurationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The SSD IOPS (input/output operations per second) configuration for an Amazon FSx for NetApp ONTAP, Amazon FSx for Windows File Server, or FSx for OpenZFS file system.

            By default, Amazon FSx automatically provisions 3 IOPS per GB of storage capacity. You can provision additional IOPS per GB of storage. The configuration consists of the total number of provisioned SSD IOPS and how it is was provisioned, or the mode (by the customer or by Amazon FSx).

            :param iops: The total number of SSD IOPS provisioned for the file system. The minimum and maximum values for this property depend on the value of ``HAPairs`` and ``StorageCapacity`` . The minimum value is calculated as ``StorageCapacity`` * 3 * ``HAPairs`` (3 IOPS per GB of ``StorageCapacity`` ). The maximum value is calculated as 200,000 * ``HAPairs`` . Amazon FSx responds with an HTTP status code 400 (Bad Request) if the value of ``Iops`` is outside of the minimum or maximum values.
            :param mode: Specifies whether the file system is using the ``AUTOMATIC`` setting of SSD IOPS of 3 IOPS per GB of storage capacity, or if it using a ``USER_PROVISIONED`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-diskiopsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                disk_iops_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                    iops=123,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__101dc77495758d81f187868cd51d71e5e158eba7db4b41849fb3980a98857d06)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The total number of SSD IOPS provisioned for the file system.

            The minimum and maximum values for this property depend on the value of ``HAPairs`` and ``StorageCapacity`` . The minimum value is calculated as ``StorageCapacity`` * 3 * ``HAPairs`` (3 IOPS per GB of ``StorageCapacity`` ). The maximum value is calculated as 200,000 * ``HAPairs`` .

            Amazon FSx responds with an HTTP status code 400 (Bad Request) if the value of ``Iops`` is outside of the minimum or maximum values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-diskiopsconfiguration.html#cfn-fsx-filesystem-diskiopsconfiguration-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the file system is using the ``AUTOMATIC`` setting of SSD IOPS of 3 IOPS per GB of storage capacity, or if it using a ``USER_PROVISIONED`` value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-diskiopsconfiguration.html#cfn-fsx-filesystem-diskiopsconfiguration-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DiskIopsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.LustreConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_import_policy": "autoImportPolicy",
            "automatic_backup_retention_days": "automaticBackupRetentionDays",
            "copy_tags_to_backups": "copyTagsToBackups",
            "daily_automatic_backup_start_time": "dailyAutomaticBackupStartTime",
            "data_compression_type": "dataCompressionType",
            "data_read_cache_configuration": "dataReadCacheConfiguration",
            "deployment_type": "deploymentType",
            "drive_cache_type": "driveCacheType",
            "efa_enabled": "efaEnabled",
            "export_path": "exportPath",
            "imported_file_chunk_size": "importedFileChunkSize",
            "import_path": "importPath",
            "metadata_configuration": "metadataConfiguration",
            "per_unit_storage_throughput": "perUnitStorageThroughput",
            "throughput_capacity": "throughputCapacity",
            "weekly_maintenance_start_time": "weeklyMaintenanceStartTime",
        },
    )
    class LustreConfigurationProperty:
        def __init__(
            self,
            *,
            auto_import_policy: typing.Optional[builtins.str] = None,
            automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
            copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
            data_compression_type: typing.Optional[builtins.str] = None,
            data_read_cache_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            deployment_type: typing.Optional[builtins.str] = None,
            drive_cache_type: typing.Optional[builtins.str] = None,
            efa_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            export_path: typing.Optional[builtins.str] = None,
            imported_file_chunk_size: typing.Optional[jsii.Number] = None,
            import_path: typing.Optional[builtins.str] = None,
            metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.MetadataConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            per_unit_storage_throughput: typing.Optional[jsii.Number] = None,
            throughput_capacity: typing.Optional[jsii.Number] = None,
            weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the Amazon FSx for Lustre file system.

            :param auto_import_policy: (Optional) When you create your file system, your existing S3 objects appear as file and directory listings. Use this property to choose how Amazon FSx keeps your file and directory listings up to date as you add or modify objects in your linked S3 bucket. ``AutoImportPolicy`` can have the following values: - ``NONE`` - (Default) AutoImport is off. Amazon FSx only updates file and directory listings from the linked S3 bucket when the file system is created. FSx does not update file and directory listings for any new or changed objects after choosing this option. - ``NEW`` - AutoImport is on. Amazon FSx automatically imports directory listings of any new objects added to the linked S3 bucket that do not currently exist in the FSx file system. - ``NEW_CHANGED`` - AutoImport is on. Amazon FSx automatically imports file and directory listings of any new objects added to the S3 bucket and any existing objects that are changed in the S3 bucket after you choose this option. - ``NEW_CHANGED_DELETED`` - AutoImport is on. Amazon FSx automatically imports file and directory listings of any new objects added to the S3 bucket, any existing objects that are changed in the S3 bucket, and any objects that were deleted in the S3 bucket. For more information, see `Automatically import updates from your S3 bucket <https://docs.aws.amazon.com/fsx/latest/LustreGuide/autoimport-data-repo.html>`_ . .. epigraph:: This parameter is not supported for Lustre file systems with a data repository association.
            :param automatic_backup_retention_days: The number of days to retain automatic backups. Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``0`` .
            :param copy_tags_to_backups: (Optional) Not available for use with file systems that are linked to a data repository. A boolean flag indicating whether tags for the file system should be copied to backups. The default value is false. If ``CopyTagsToBackups`` is set to true, all file system tags are copied to all automatic and user-initiated backups when the user doesn't specify any backup-specific tags. If ``CopyTagsToBackups`` is set to true and you specify one or more backup tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the file system, regardless of this value. (Default = ``false`` ) For more information, see `Working with backups <https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-backups-fsx.html>`_ in the *Amazon FSx for Lustre User Guide* .
            :param daily_automatic_backup_start_time: A recurring daily time, in the format ``HH:MM`` . ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.
            :param data_compression_type: Sets the data compression configuration for the file system. ``DataCompressionType`` can have the following values:. - ``NONE`` - (Default) Data compression is turned off when the file system is created. - ``LZ4`` - Data compression is turned on with the LZ4 algorithm. For more information, see `Lustre data compression <https://docs.aws.amazon.com/fsx/latest/LustreGuide/data-compression.html>`_ in the *Amazon FSx for Lustre User Guide* .
            :param data_read_cache_configuration: Specifies the optional provisioned SSD read cache on FSx for Lustre file systems that use the Intelligent-Tiering storage class. Required when ``StorageType`` is set to ``INTELLIGENT_TIERING`` .
            :param deployment_type: (Optional) Choose ``SCRATCH_1`` and ``SCRATCH_2`` deployment types when you need temporary storage and shorter-term processing of data. The ``SCRATCH_2`` deployment type provides in-transit encryption of data and higher burst throughput capacity than ``SCRATCH_1`` . Choose ``PERSISTENT_1`` for longer-term storage and for throughput-focused workloads that aren’t latency-sensitive. ``PERSISTENT_1`` supports encryption of data in transit, and is available in all AWS Regions in which FSx for Lustre is available. Choose ``PERSISTENT_2`` for longer-term storage and for latency-sensitive workloads that require the highest levels of IOPS/throughput. ``PERSISTENT_2`` supports the SSD and Intelligent-Tiering storage classes. You can optionally specify a metadata configuration mode for ``PERSISTENT_2`` which supports increasing metadata performance. ``PERSISTENT_2`` is available in a limited number of AWS Regions . For more information, and an up-to-date list of AWS Regions in which ``PERSISTENT_2`` is available, see `Deployment and storage class options for FSx for Lustre file systems <https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-fsx-lustre.html>`_ in the *Amazon FSx for Lustre User Guide* . .. epigraph:: If you choose ``PERSISTENT_2`` , and you set ``FileSystemTypeVersion`` to ``2.10`` , the ``CreateFileSystem`` operation fails. Encryption of data in transit is automatically turned on when you access ``SCRATCH_2`` , ``PERSISTENT_1`` , and ``PERSISTENT_2`` file systems from Amazon EC2 instances that support automatic encryption in the AWS Regions where they are available. For more information about encryption in transit for FSx for Lustre file systems, see `Encrypting data in transit <https://docs.aws.amazon.com/fsx/latest/LustreGuide/encryption-in-transit-fsxl.html>`_ in the *Amazon FSx for Lustre User Guide* . (Default = ``SCRATCH_1`` )
            :param drive_cache_type: The type of drive cache used by ``PERSISTENT_1`` file systems that are provisioned with HDD storage devices. This parameter is required when storage type is HDD. Set this property to ``READ`` to improve the performance for frequently accessed files by caching up to 20% of the total storage capacity of the file system. This parameter is required when ``StorageType`` is set to ``HDD`` and ``DeploymentType`` is ``PERSISTENT_1`` .
            :param efa_enabled: (Optional) Specifies whether Elastic Fabric Adapter (EFA) and GPUDirect Storage (GDS) support is enabled for the Amazon FSx for Lustre file system. (Default = ``false`` )
            :param export_path: (Optional) Specifies the path in the Amazon S3 bucket where the root of your Amazon FSx file system is exported. The path must use the same Amazon S3 bucket as specified in ImportPath. You can provide an optional prefix to which new and changed data is to be exported from your Amazon FSx for Lustre file system. If an ``ExportPath`` value is not provided, Amazon FSx sets a default export path, ``s3://import-bucket/FSxLustre[creation-timestamp]`` . The timestamp is in UTC format, for example ``s3://import-bucket/FSxLustre20181105T222312Z`` . The Amazon S3 export bucket must be the same as the import bucket specified by ``ImportPath`` . If you specify only a bucket name, such as ``s3://import-bucket`` , you get a 1:1 mapping of file system objects to S3 bucket objects. This mapping means that the input data in S3 is overwritten on export. If you provide a custom prefix in the export path, such as ``s3://import-bucket/[custom-optional-prefix]`` , Amazon FSx exports the contents of your file system to that export prefix in the Amazon S3 bucket. .. epigraph:: This parameter is not supported for file systems with a data repository association.
            :param imported_file_chunk_size: (Optional) For files imported from a data repository, this value determines the stripe count and maximum amount of data per file (in MiB) stored on a single physical disk. The maximum number of disks that a single file can be striped across is limited by the total number of disks that make up the file system. The default chunk size is 1,024 MiB (1 GiB) and can go as high as 512,000 MiB (500 GiB). Amazon S3 objects have a maximum size of 5 TB. .. epigraph:: This parameter is not supported for Lustre file systems with a data repository association.
            :param import_path: (Optional) The path to the Amazon S3 bucket (including the optional prefix) that you're using as the data repository for your Amazon FSx for Lustre file system. The root of your FSx for Lustre file system will be mapped to the root of the Amazon S3 bucket you select. An example is ``s3://import-bucket/optional-prefix`` . If you specify a prefix after the Amazon S3 bucket name, only object keys with that prefix are loaded into the file system. .. epigraph:: This parameter is not supported for Lustre file systems with a data repository association.
            :param metadata_configuration: The Lustre metadata performance configuration for the creation of an FSx for Lustre file system using a ``PERSISTENT_2`` deployment type.
            :param per_unit_storage_throughput: Required with ``PERSISTENT_1`` and ``PERSISTENT_2`` deployment types, provisions the amount of read and write throughput for each 1 tebibyte (TiB) of file system storage capacity, in MB/s/TiB. File system throughput capacity is calculated by multiplying ﬁle system storage capacity (TiB) by the ``PerUnitStorageThroughput`` (MB/s/TiB). For a 2.4-TiB ﬁle system, provisioning 50 MB/s/TiB of ``PerUnitStorageThroughput`` yields 120 MB/s of ﬁle system throughput. You pay for the amount of throughput that you provision. Valid values: - For ``PERSISTENT_1`` SSD storage: 50, 100, 200 MB/s/TiB. - For ``PERSISTENT_1`` HDD storage: 12, 40 MB/s/TiB. - For ``PERSISTENT_2`` SSD storage: 125, 250, 500, 1000 MB/s/TiB.
            :param throughput_capacity: Specifies the throughput of an FSx for Lustre file system using the Intelligent-Tiering storage class, measured in megabytes per second (MBps). Valid values are 4000 MBps or multiples of 4000 MBps. You pay for the amount of throughput that you provision.
            :param weekly_maintenance_start_time: The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday. For example, ``1:05:00`` specifies maintenance at 5 AM Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                lustre_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.LustreConfigurationProperty(
                    auto_import_policy="autoImportPolicy",
                    automatic_backup_retention_days=123,
                    copy_tags_to_backups=False,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    data_compression_type="dataCompressionType",
                    data_read_cache_configuration=fsx_mixins.CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty(
                        size_gi_b=123,
                        sizing_mode="sizingMode"
                    ),
                    deployment_type="deploymentType",
                    drive_cache_type="driveCacheType",
                    efa_enabled=False,
                    export_path="exportPath",
                    imported_file_chunk_size=123,
                    import_path="importPath",
                    metadata_configuration=fsx_mixins.CfnFileSystemPropsMixin.MetadataConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    per_unit_storage_throughput=123,
                    throughput_capacity=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3b15289775c621967ea6402d7269d30696f4605f917cde995b3806e581b143c)
                check_type(argname="argument auto_import_policy", value=auto_import_policy, expected_type=type_hints["auto_import_policy"])
                check_type(argname="argument automatic_backup_retention_days", value=automatic_backup_retention_days, expected_type=type_hints["automatic_backup_retention_days"])
                check_type(argname="argument copy_tags_to_backups", value=copy_tags_to_backups, expected_type=type_hints["copy_tags_to_backups"])
                check_type(argname="argument daily_automatic_backup_start_time", value=daily_automatic_backup_start_time, expected_type=type_hints["daily_automatic_backup_start_time"])
                check_type(argname="argument data_compression_type", value=data_compression_type, expected_type=type_hints["data_compression_type"])
                check_type(argname="argument data_read_cache_configuration", value=data_read_cache_configuration, expected_type=type_hints["data_read_cache_configuration"])
                check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
                check_type(argname="argument drive_cache_type", value=drive_cache_type, expected_type=type_hints["drive_cache_type"])
                check_type(argname="argument efa_enabled", value=efa_enabled, expected_type=type_hints["efa_enabled"])
                check_type(argname="argument export_path", value=export_path, expected_type=type_hints["export_path"])
                check_type(argname="argument imported_file_chunk_size", value=imported_file_chunk_size, expected_type=type_hints["imported_file_chunk_size"])
                check_type(argname="argument import_path", value=import_path, expected_type=type_hints["import_path"])
                check_type(argname="argument metadata_configuration", value=metadata_configuration, expected_type=type_hints["metadata_configuration"])
                check_type(argname="argument per_unit_storage_throughput", value=per_unit_storage_throughput, expected_type=type_hints["per_unit_storage_throughput"])
                check_type(argname="argument throughput_capacity", value=throughput_capacity, expected_type=type_hints["throughput_capacity"])
                check_type(argname="argument weekly_maintenance_start_time", value=weekly_maintenance_start_time, expected_type=type_hints["weekly_maintenance_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_import_policy is not None:
                self._values["auto_import_policy"] = auto_import_policy
            if automatic_backup_retention_days is not None:
                self._values["automatic_backup_retention_days"] = automatic_backup_retention_days
            if copy_tags_to_backups is not None:
                self._values["copy_tags_to_backups"] = copy_tags_to_backups
            if daily_automatic_backup_start_time is not None:
                self._values["daily_automatic_backup_start_time"] = daily_automatic_backup_start_time
            if data_compression_type is not None:
                self._values["data_compression_type"] = data_compression_type
            if data_read_cache_configuration is not None:
                self._values["data_read_cache_configuration"] = data_read_cache_configuration
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type
            if drive_cache_type is not None:
                self._values["drive_cache_type"] = drive_cache_type
            if efa_enabled is not None:
                self._values["efa_enabled"] = efa_enabled
            if export_path is not None:
                self._values["export_path"] = export_path
            if imported_file_chunk_size is not None:
                self._values["imported_file_chunk_size"] = imported_file_chunk_size
            if import_path is not None:
                self._values["import_path"] = import_path
            if metadata_configuration is not None:
                self._values["metadata_configuration"] = metadata_configuration
            if per_unit_storage_throughput is not None:
                self._values["per_unit_storage_throughput"] = per_unit_storage_throughput
            if throughput_capacity is not None:
                self._values["throughput_capacity"] = throughput_capacity
            if weekly_maintenance_start_time is not None:
                self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

        @builtins.property
        def auto_import_policy(self) -> typing.Optional[builtins.str]:
            '''(Optional) When you create your file system, your existing S3 objects appear as file and directory listings.

            Use this property to choose how Amazon FSx keeps your file and directory listings up to date as you add or modify objects in your linked S3 bucket. ``AutoImportPolicy`` can have the following values:

            - ``NONE`` - (Default) AutoImport is off. Amazon FSx only updates file and directory listings from the linked S3 bucket when the file system is created. FSx does not update file and directory listings for any new or changed objects after choosing this option.
            - ``NEW`` - AutoImport is on. Amazon FSx automatically imports directory listings of any new objects added to the linked S3 bucket that do not currently exist in the FSx file system.
            - ``NEW_CHANGED`` - AutoImport is on. Amazon FSx automatically imports file and directory listings of any new objects added to the S3 bucket and any existing objects that are changed in the S3 bucket after you choose this option.
            - ``NEW_CHANGED_DELETED`` - AutoImport is on. Amazon FSx automatically imports file and directory listings of any new objects added to the S3 bucket, any existing objects that are changed in the S3 bucket, and any objects that were deleted in the S3 bucket.

            For more information, see `Automatically import updates from your S3 bucket <https://docs.aws.amazon.com/fsx/latest/LustreGuide/autoimport-data-repo.html>`_ .
            .. epigraph::

               This parameter is not supported for Lustre file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-autoimportpolicy
            '''
            result = self._values.get("auto_import_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def automatic_backup_retention_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days to retain automatic backups.

            Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``0`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-automaticbackupretentiondays
            '''
            result = self._values.get("automatic_backup_retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def copy_tags_to_backups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''(Optional) Not available for use with file systems that are linked to a data repository.

            A boolean flag indicating whether tags for the file system should be copied to backups. The default value is false. If ``CopyTagsToBackups`` is set to true, all file system tags are copied to all automatic and user-initiated backups when the user doesn't specify any backup-specific tags. If ``CopyTagsToBackups`` is set to true and you specify one or more backup tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the file system, regardless of this value.

            (Default = ``false`` )

            For more information, see `Working with backups <https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-backups-fsx.html>`_ in the *Amazon FSx for Lustre User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-copytagstobackups
            '''
            result = self._values.get("copy_tags_to_backups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def daily_automatic_backup_start_time(self) -> typing.Optional[builtins.str]:
            '''A recurring daily time, in the format ``HH:MM`` .

            ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-dailyautomaticbackupstarttime
            '''
            result = self._values.get("daily_automatic_backup_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_compression_type(self) -> typing.Optional[builtins.str]:
            '''Sets the data compression configuration for the file system. ``DataCompressionType`` can have the following values:.

            - ``NONE`` - (Default) Data compression is turned off when the file system is created.
            - ``LZ4`` - Data compression is turned on with the LZ4 algorithm.

            For more information, see `Lustre data compression <https://docs.aws.amazon.com/fsx/latest/LustreGuide/data-compression.html>`_ in the *Amazon FSx for Lustre User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-datacompressiontype
            '''
            result = self._values.get("data_compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_read_cache_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty"]]:
            '''Specifies the optional provisioned SSD read cache on FSx for Lustre file systems that use the Intelligent-Tiering storage class.

            Required when ``StorageType`` is set to ``INTELLIGENT_TIERING`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-datareadcacheconfiguration
            '''
            result = self._values.get("data_read_cache_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty"]], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''(Optional) Choose ``SCRATCH_1`` and ``SCRATCH_2`` deployment types when you need temporary storage and shorter-term processing of data.

            The ``SCRATCH_2`` deployment type provides in-transit encryption of data and higher burst throughput capacity than ``SCRATCH_1`` .

            Choose ``PERSISTENT_1`` for longer-term storage and for throughput-focused workloads that aren’t latency-sensitive. ``PERSISTENT_1`` supports encryption of data in transit, and is available in all AWS Regions in which FSx for Lustre is available.

            Choose ``PERSISTENT_2`` for longer-term storage and for latency-sensitive workloads that require the highest levels of IOPS/throughput. ``PERSISTENT_2`` supports the SSD and Intelligent-Tiering storage classes. You can optionally specify a metadata configuration mode for ``PERSISTENT_2`` which supports increasing metadata performance. ``PERSISTENT_2`` is available in a limited number of AWS Regions . For more information, and an up-to-date list of AWS Regions in which ``PERSISTENT_2`` is available, see `Deployment and storage class options for FSx for Lustre file systems <https://docs.aws.amazon.com/fsx/latest/LustreGuide/using-fsx-lustre.html>`_ in the *Amazon FSx for Lustre User Guide* .
            .. epigraph::

               If you choose ``PERSISTENT_2`` , and you set ``FileSystemTypeVersion`` to ``2.10`` , the ``CreateFileSystem`` operation fails.

            Encryption of data in transit is automatically turned on when you access ``SCRATCH_2`` , ``PERSISTENT_1`` , and ``PERSISTENT_2`` file systems from Amazon EC2 instances that support automatic encryption in the AWS Regions where they are available. For more information about encryption in transit for FSx for Lustre file systems, see `Encrypting data in transit <https://docs.aws.amazon.com/fsx/latest/LustreGuide/encryption-in-transit-fsxl.html>`_ in the *Amazon FSx for Lustre User Guide* .

            (Default = ``SCRATCH_1`` )

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def drive_cache_type(self) -> typing.Optional[builtins.str]:
            '''The type of drive cache used by ``PERSISTENT_1`` file systems that are provisioned with HDD storage devices.

            This parameter is required when storage type is HDD. Set this property to ``READ`` to improve the performance for frequently accessed files by caching up to 20% of the total storage capacity of the file system.

            This parameter is required when ``StorageType`` is set to ``HDD`` and ``DeploymentType`` is ``PERSISTENT_1`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-drivecachetype
            '''
            result = self._values.get("drive_cache_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def efa_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''(Optional) Specifies whether Elastic Fabric Adapter (EFA) and GPUDirect Storage (GDS) support is enabled for the Amazon FSx for Lustre file system.

            (Default = ``false`` )

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-efaenabled
            '''
            result = self._values.get("efa_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def export_path(self) -> typing.Optional[builtins.str]:
            '''(Optional) Specifies the path in the Amazon S3 bucket where the root of your Amazon FSx file system is exported.

            The path must use the same Amazon S3 bucket as specified in ImportPath. You can provide an optional prefix to which new and changed data is to be exported from your Amazon FSx for Lustre file system. If an ``ExportPath`` value is not provided, Amazon FSx sets a default export path, ``s3://import-bucket/FSxLustre[creation-timestamp]`` . The timestamp is in UTC format, for example ``s3://import-bucket/FSxLustre20181105T222312Z`` .

            The Amazon S3 export bucket must be the same as the import bucket specified by ``ImportPath`` . If you specify only a bucket name, such as ``s3://import-bucket`` , you get a 1:1 mapping of file system objects to S3 bucket objects. This mapping means that the input data in S3 is overwritten on export. If you provide a custom prefix in the export path, such as ``s3://import-bucket/[custom-optional-prefix]`` , Amazon FSx exports the contents of your file system to that export prefix in the Amazon S3 bucket.
            .. epigraph::

               This parameter is not supported for file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-exportpath
            '''
            result = self._values.get("export_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def imported_file_chunk_size(self) -> typing.Optional[jsii.Number]:
            '''(Optional) For files imported from a data repository, this value determines the stripe count and maximum amount of data per file (in MiB) stored on a single physical disk.

            The maximum number of disks that a single file can be striped across is limited by the total number of disks that make up the file system.

            The default chunk size is 1,024 MiB (1 GiB) and can go as high as 512,000 MiB (500 GiB). Amazon S3 objects have a maximum size of 5 TB.
            .. epigraph::

               This parameter is not supported for Lustre file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-importedfilechunksize
            '''
            result = self._values.get("imported_file_chunk_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def import_path(self) -> typing.Optional[builtins.str]:
            '''(Optional) The path to the Amazon S3 bucket (including the optional prefix) that you're using as the data repository for your Amazon FSx for Lustre file system.

            The root of your FSx for Lustre file system will be mapped to the root of the Amazon S3 bucket you select. An example is ``s3://import-bucket/optional-prefix`` . If you specify a prefix after the Amazon S3 bucket name, only object keys with that prefix are loaded into the file system.
            .. epigraph::

               This parameter is not supported for Lustre file systems with a data repository association.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-importpath
            '''
            result = self._values.get("import_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def metadata_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.MetadataConfigurationProperty"]]:
            '''The Lustre metadata performance configuration for the creation of an FSx for Lustre file system using a ``PERSISTENT_2`` deployment type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-metadataconfiguration
            '''
            result = self._values.get("metadata_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.MetadataConfigurationProperty"]], result)

        @builtins.property
        def per_unit_storage_throughput(self) -> typing.Optional[jsii.Number]:
            '''Required with ``PERSISTENT_1`` and ``PERSISTENT_2`` deployment types, provisions the amount of read and write throughput for each 1 tebibyte (TiB) of file system storage capacity, in MB/s/TiB.

            File system throughput capacity is calculated by multiplying ﬁle system storage capacity (TiB) by the ``PerUnitStorageThroughput`` (MB/s/TiB). For a 2.4-TiB ﬁle system, provisioning 50 MB/s/TiB of ``PerUnitStorageThroughput`` yields 120 MB/s of ﬁle system throughput. You pay for the amount of throughput that you provision.

            Valid values:

            - For ``PERSISTENT_1`` SSD storage: 50, 100, 200 MB/s/TiB.
            - For ``PERSISTENT_1`` HDD storage: 12, 40 MB/s/TiB.
            - For ``PERSISTENT_2`` SSD storage: 125, 250, 500, 1000 MB/s/TiB.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-perunitstoragethroughput
            '''
            result = self._values.get("per_unit_storage_throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput_capacity(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throughput of an FSx for Lustre file system using the Intelligent-Tiering storage class, measured in megabytes per second (MBps).

            Valid values are 4000 MBps or multiples of 4000 MBps. You pay for the amount of throughput that you provision.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-throughputcapacity
            '''
            result = self._values.get("throughput_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weekly_maintenance_start_time(self) -> typing.Optional[builtins.str]:
            '''The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday.

            For example, ``1:05:00`` specifies maintenance at 5 AM Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-lustreconfiguration.html#cfn-fsx-filesystem-lustreconfiguration-weeklymaintenancestarttime
            '''
            result = self._values.get("weekly_maintenance_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LustreConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.MetadataConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"iops": "iops", "mode": "mode"},
    )
    class MetadataConfigurationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that allows you to specify the performance of metadata operations for an FSx for Lustre file system.

            :param iops: The number of Metadata IOPS provisioned for the file system.
            :param mode: Specifies whether the file system is using the AUTOMATIC setting of metadata IOPS or if it is using a USER_PROVISIONED value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-metadataconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                metadata_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.MetadataConfigurationProperty(
                    iops=123,
                    mode="mode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__680b70587eb455466c32dbe775008c13c3b3f57bcd86768478c33065a3250212)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if mode is not None:
                self._values["mode"] = mode

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of Metadata IOPS provisioned for the file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-metadataconfiguration.html#cfn-fsx-filesystem-metadataconfiguration-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the file system is using the AUTOMATIC setting of metadata IOPS or if it is using a USER_PROVISIONED value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-metadataconfiguration.html#cfn-fsx-filesystem-metadataconfiguration-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.NfsExportsProperty",
        jsii_struct_bases=[],
        name_mapping={"client_configurations": "clientConfigurations"},
    )
    class NfsExportsProperty:
        def __init__(
            self,
            *,
            client_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.ClientConfigurationsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration object for mounting a file system.

            :param client_configurations: A list of configuration objects that contain the client and options for mounting the OpenZFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-nfsexports.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                nfs_exports_property = fsx_mixins.CfnFileSystemPropsMixin.NfsExportsProperty(
                    client_configurations=[fsx_mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty(
                        clients="clients",
                        options=["options"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17e89ee5c3cf47dcf9d2b96d985346a26d3215fc4e0fc706957d847afe96f35c)
                check_type(argname="argument client_configurations", value=client_configurations, expected_type=type_hints["client_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_configurations is not None:
                self._values["client_configurations"] = client_configurations

        @builtins.property
        def client_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.ClientConfigurationsProperty"]]]]:
            '''A list of configuration objects that contain the client and options for mounting the OpenZFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-nfsexports.html#cfn-fsx-filesystem-nfsexports-clientconfigurations
            '''
            result = self._values.get("client_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.ClientConfigurationsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NfsExportsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.OntapConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatic_backup_retention_days": "automaticBackupRetentionDays",
            "daily_automatic_backup_start_time": "dailyAutomaticBackupStartTime",
            "deployment_type": "deploymentType",
            "disk_iops_configuration": "diskIopsConfiguration",
            "endpoint_ip_address_range": "endpointIpAddressRange",
            "endpoint_ipv6_address_range": "endpointIpv6AddressRange",
            "fsx_admin_password": "fsxAdminPassword",
            "ha_pairs": "haPairs",
            "preferred_subnet_id": "preferredSubnetId",
            "route_table_ids": "routeTableIds",
            "throughput_capacity": "throughputCapacity",
            "throughput_capacity_per_ha_pair": "throughputCapacityPerHaPair",
            "weekly_maintenance_start_time": "weeklyMaintenanceStartTime",
        },
    )
    class OntapConfigurationProperty:
        def __init__(
            self,
            *,
            automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
            daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
            deployment_type: typing.Optional[builtins.str] = None,
            disk_iops_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.DiskIopsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            endpoint_ip_address_range: typing.Optional[builtins.str] = None,
            endpoint_ipv6_address_range: typing.Optional[builtins.str] = None,
            fsx_admin_password: typing.Optional[builtins.str] = None,
            ha_pairs: typing.Optional[jsii.Number] = None,
            preferred_subnet_id: typing.Optional[builtins.str] = None,
            route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            throughput_capacity: typing.Optional[jsii.Number] = None,
            throughput_capacity_per_ha_pair: typing.Optional[jsii.Number] = None,
            weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for this Amazon FSx for NetApp ONTAP file system.

            :param automatic_backup_retention_days: The number of days to retain automatic backups. Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``30`` .
            :param daily_automatic_backup_start_time: A recurring daily time, in the format ``HH:MM`` . ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.
            :param deployment_type: Specifies the FSx for ONTAP file system deployment type to use in creating the file system. - ``MULTI_AZ_1`` - A high availability file system configured for Multi-AZ redundancy to tolerate temporary Availability Zone (AZ) unavailability. This is a first-generation FSx for ONTAP file system. - ``MULTI_AZ_2`` - A high availability file system configured for Multi-AZ redundancy to tolerate temporary AZ unavailability. This is a second-generation FSx for ONTAP file system. - ``SINGLE_AZ_1`` - A file system configured for Single-AZ redundancy. This is a first-generation FSx for ONTAP file system. - ``SINGLE_AZ_2`` - A file system configured with multiple high-availability (HA) pairs for Single-AZ redundancy. This is a second-generation FSx for ONTAP file system. For information about the use cases for Multi-AZ and Single-AZ deployments, refer to `Choosing a file system deployment type <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/high-availability-AZ.html>`_ .
            :param disk_iops_configuration: The SSD IOPS configuration for the FSx for ONTAP file system.
            :param endpoint_ip_address_range: (Multi-AZ only) Specifies the IPv4 address range in which the endpoints to access your file system will be created. By default in the Amazon FSx API, Amazon FSx selects an unused IP address range for you from the 198.19.* range. By default in the Amazon FSx console, Amazon FSx chooses the last 64 IP addresses from the VPC’s primary CIDR range to use as the endpoint IP address range for the file system. You can have overlapping endpoint IP addresses for file systems deployed in the same VPC/route tables, as long as they don't overlap with any subnet.
            :param endpoint_ipv6_address_range: 
            :param fsx_admin_password: The ONTAP administrative password for the ``fsxadmin`` user with which you administer your file system using the NetApp ONTAP CLI and REST API.
            :param ha_pairs: Specifies how many high-availability (HA) pairs of file servers will power your file system. First-generation file systems are powered by 1 HA pair. Second-generation multi-AZ file systems are powered by 1 HA pair. Second generation single-AZ file systems are powered by up to 12 HA pairs. The default value is 1. The value of this property affects the values of ``StorageCapacity`` , ``Iops`` , and ``ThroughputCapacity`` . For more information, see `High-availability (HA) pairs <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/administering-file-systems.html#HA-pairs>`_ in the FSx for ONTAP user guide. Block storage protocol support (iSCSI and NVMe over TCP) is disabled on file systems with more than 6 HA pairs. For more information, see `Using block storage protocols <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/supported-fsx-clients.html#using-block-storage>`_ . Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions: - The value of ``HAPairs`` is less than 1 or greater than 12. - The value of ``HAPairs`` is greater than 1 and the value of ``DeploymentType`` is ``SINGLE_AZ_1`` , ``MULTI_AZ_1`` , or ``MULTI_AZ_2`` .
            :param preferred_subnet_id: Required when ``DeploymentType`` is set to ``MULTI_AZ_1`` or ``MULTI_AZ_2`` . This specifies the subnet in which you want the preferred file server to be located.
            :param route_table_ids: (Multi-AZ only) Specifies the route tables in which Amazon FSx creates the rules for routing traffic to the correct file server. You should specify all virtual private cloud (VPC) route tables associated with the subnets in which your clients are located. By default, Amazon FSx selects your VPC's default route table. .. epigraph:: Amazon FSx manages these route tables for Multi-AZ file systems using tag-based authentication. These route tables are tagged with ``Key: AmazonFSx; Value: ManagedByAmazonFSx`` . When creating FSx for ONTAP Multi-AZ file systems using CloudFormation we recommend that you add the ``Key: AmazonFSx; Value: ManagedByAmazonFSx`` tag manually.
            :param throughput_capacity: Sets the throughput capacity for the file system that you're creating in megabytes per second (MBps). For more information, see `Managing throughput capacity <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-throughput-capacity.html>`_ in the FSx for ONTAP User Guide. Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions: - The value of ``ThroughputCapacity`` and ``ThroughputCapacityPerHAPair`` are not the same value. - The value of ``ThroughputCapacity`` when divided by the value of ``HAPairs`` is outside of the valid range for ``ThroughputCapacity`` .
            :param throughput_capacity_per_ha_pair: Use to choose the throughput capacity per HA pair, rather than the total throughput for the file system. You can define either the ``ThroughputCapacityPerHAPair`` or the ``ThroughputCapacity`` when creating a file system, but not both. This field and ``ThroughputCapacity`` are the same for file systems powered by one HA pair. - For ``SINGLE_AZ_1`` and ``MULTI_AZ_1`` file systems, valid values are 128, 256, 512, 1024, 2048, or 4096 MBps. - For ``SINGLE_AZ_2`` , valid values are 1536, 3072, or 6144 MBps. - For ``MULTI_AZ_2`` , valid values are 384, 768, 1536, 3072, or 6144 MBps. Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions: - The value of ``ThroughputCapacity`` and ``ThroughputCapacityPerHAPair`` are not the same value for file systems with one HA pair. - The value of deployment type is ``SINGLE_AZ_2`` and ``ThroughputCapacity`` / ``ThroughputCapacityPerHAPair`` is not a valid HA pair (a value between 1 and 12). - The value of ``ThroughputCapacityPerHAPair`` is not a valid value.
            :param weekly_maintenance_start_time: The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday. For example, ``1:05:00`` specifies maintenance at 5 AM Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                ontap_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.OntapConfigurationProperty(
                    automatic_backup_retention_days=123,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    deployment_type="deploymentType",
                    disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    endpoint_ip_address_range="endpointIpAddressRange",
                    endpoint_ipv6_address_range="endpointIpv6AddressRange",
                    fsx_admin_password="fsxAdminPassword",
                    ha_pairs=123,
                    preferred_subnet_id="preferredSubnetId",
                    route_table_ids=["routeTableIds"],
                    throughput_capacity=123,
                    throughput_capacity_per_ha_pair=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5af92418f9f6da37b979cac247cb98340e798d0fed5f53fadcc6cb8f86322d3c)
                check_type(argname="argument automatic_backup_retention_days", value=automatic_backup_retention_days, expected_type=type_hints["automatic_backup_retention_days"])
                check_type(argname="argument daily_automatic_backup_start_time", value=daily_automatic_backup_start_time, expected_type=type_hints["daily_automatic_backup_start_time"])
                check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
                check_type(argname="argument disk_iops_configuration", value=disk_iops_configuration, expected_type=type_hints["disk_iops_configuration"])
                check_type(argname="argument endpoint_ip_address_range", value=endpoint_ip_address_range, expected_type=type_hints["endpoint_ip_address_range"])
                check_type(argname="argument endpoint_ipv6_address_range", value=endpoint_ipv6_address_range, expected_type=type_hints["endpoint_ipv6_address_range"])
                check_type(argname="argument fsx_admin_password", value=fsx_admin_password, expected_type=type_hints["fsx_admin_password"])
                check_type(argname="argument ha_pairs", value=ha_pairs, expected_type=type_hints["ha_pairs"])
                check_type(argname="argument preferred_subnet_id", value=preferred_subnet_id, expected_type=type_hints["preferred_subnet_id"])
                check_type(argname="argument route_table_ids", value=route_table_ids, expected_type=type_hints["route_table_ids"])
                check_type(argname="argument throughput_capacity", value=throughput_capacity, expected_type=type_hints["throughput_capacity"])
                check_type(argname="argument throughput_capacity_per_ha_pair", value=throughput_capacity_per_ha_pair, expected_type=type_hints["throughput_capacity_per_ha_pair"])
                check_type(argname="argument weekly_maintenance_start_time", value=weekly_maintenance_start_time, expected_type=type_hints["weekly_maintenance_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic_backup_retention_days is not None:
                self._values["automatic_backup_retention_days"] = automatic_backup_retention_days
            if daily_automatic_backup_start_time is not None:
                self._values["daily_automatic_backup_start_time"] = daily_automatic_backup_start_time
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type
            if disk_iops_configuration is not None:
                self._values["disk_iops_configuration"] = disk_iops_configuration
            if endpoint_ip_address_range is not None:
                self._values["endpoint_ip_address_range"] = endpoint_ip_address_range
            if endpoint_ipv6_address_range is not None:
                self._values["endpoint_ipv6_address_range"] = endpoint_ipv6_address_range
            if fsx_admin_password is not None:
                self._values["fsx_admin_password"] = fsx_admin_password
            if ha_pairs is not None:
                self._values["ha_pairs"] = ha_pairs
            if preferred_subnet_id is not None:
                self._values["preferred_subnet_id"] = preferred_subnet_id
            if route_table_ids is not None:
                self._values["route_table_ids"] = route_table_ids
            if throughput_capacity is not None:
                self._values["throughput_capacity"] = throughput_capacity
            if throughput_capacity_per_ha_pair is not None:
                self._values["throughput_capacity_per_ha_pair"] = throughput_capacity_per_ha_pair
            if weekly_maintenance_start_time is not None:
                self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

        @builtins.property
        def automatic_backup_retention_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days to retain automatic backups.

            Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``30`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-automaticbackupretentiondays
            '''
            result = self._values.get("automatic_backup_retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def daily_automatic_backup_start_time(self) -> typing.Optional[builtins.str]:
            '''A recurring daily time, in the format ``HH:MM`` .

            ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-dailyautomaticbackupstarttime
            '''
            result = self._values.get("daily_automatic_backup_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the FSx for ONTAP file system deployment type to use in creating the file system.

            - ``MULTI_AZ_1`` - A high availability file system configured for Multi-AZ redundancy to tolerate temporary Availability Zone (AZ) unavailability. This is a first-generation FSx for ONTAP file system.
            - ``MULTI_AZ_2`` - A high availability file system configured for Multi-AZ redundancy to tolerate temporary AZ unavailability. This is a second-generation FSx for ONTAP file system.
            - ``SINGLE_AZ_1`` - A file system configured for Single-AZ redundancy. This is a first-generation FSx for ONTAP file system.
            - ``SINGLE_AZ_2`` - A file system configured with multiple high-availability (HA) pairs for Single-AZ redundancy. This is a second-generation FSx for ONTAP file system.

            For information about the use cases for Multi-AZ and Single-AZ deployments, refer to `Choosing a file system deployment type <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/high-availability-AZ.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk_iops_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DiskIopsConfigurationProperty"]]:
            '''The SSD IOPS configuration for the FSx for ONTAP file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-diskiopsconfiguration
            '''
            result = self._values.get("disk_iops_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DiskIopsConfigurationProperty"]], result)

        @builtins.property
        def endpoint_ip_address_range(self) -> typing.Optional[builtins.str]:
            '''(Multi-AZ only) Specifies the IPv4 address range in which the endpoints to access your file system will be created.

            By default in the Amazon FSx API, Amazon FSx selects an unused IP address range for you from the 198.19.* range. By default in the Amazon FSx console, Amazon FSx chooses the last 64 IP addresses from the VPC’s primary CIDR range to use as the endpoint IP address range for the file system. You can have overlapping endpoint IP addresses for file systems deployed in the same VPC/route tables, as long as they don't overlap with any subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-endpointipaddressrange
            '''
            result = self._values.get("endpoint_ip_address_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_ipv6_address_range(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-endpointipv6addressrange
            '''
            result = self._values.get("endpoint_ipv6_address_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fsx_admin_password(self) -> typing.Optional[builtins.str]:
            '''The ONTAP administrative password for the ``fsxadmin`` user with which you administer your file system using the NetApp ONTAP CLI and REST API.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-fsxadminpassword
            '''
            result = self._values.get("fsx_admin_password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ha_pairs(self) -> typing.Optional[jsii.Number]:
            '''Specifies how many high-availability (HA) pairs of file servers will power your file system.

            First-generation file systems are powered by 1 HA pair. Second-generation multi-AZ file systems are powered by 1 HA pair. Second generation single-AZ file systems are powered by up to 12 HA pairs. The default value is 1. The value of this property affects the values of ``StorageCapacity`` , ``Iops`` , and ``ThroughputCapacity`` . For more information, see `High-availability (HA) pairs <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/administering-file-systems.html#HA-pairs>`_ in the FSx for ONTAP user guide. Block storage protocol support (iSCSI and NVMe over TCP) is disabled on file systems with more than 6 HA pairs. For more information, see `Using block storage protocols <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/supported-fsx-clients.html#using-block-storage>`_ .

            Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions:

            - The value of ``HAPairs`` is less than 1 or greater than 12.
            - The value of ``HAPairs`` is greater than 1 and the value of ``DeploymentType`` is ``SINGLE_AZ_1`` , ``MULTI_AZ_1`` , or ``MULTI_AZ_2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-hapairs
            '''
            result = self._values.get("ha_pairs")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def preferred_subnet_id(self) -> typing.Optional[builtins.str]:
            '''Required when ``DeploymentType`` is set to ``MULTI_AZ_1`` or ``MULTI_AZ_2`` .

            This specifies the subnet in which you want the preferred file server to be located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-preferredsubnetid
            '''
            result = self._values.get("preferred_subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def route_table_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''(Multi-AZ only) Specifies the route tables in which Amazon FSx creates the rules for routing traffic to the correct file server.

            You should specify all virtual private cloud (VPC) route tables associated with the subnets in which your clients are located. By default, Amazon FSx selects your VPC's default route table.
            .. epigraph::

               Amazon FSx manages these route tables for Multi-AZ file systems using tag-based authentication. These route tables are tagged with ``Key: AmazonFSx; Value: ManagedByAmazonFSx`` . When creating FSx for ONTAP Multi-AZ file systems using CloudFormation we recommend that you add the ``Key: AmazonFSx; Value: ManagedByAmazonFSx`` tag manually.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-routetableids
            '''
            result = self._values.get("route_table_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def throughput_capacity(self) -> typing.Optional[jsii.Number]:
            '''Sets the throughput capacity for the file system that you're creating in megabytes per second (MBps).

            For more information, see `Managing throughput capacity <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-throughput-capacity.html>`_ in the FSx for ONTAP User Guide.

            Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions:

            - The value of ``ThroughputCapacity`` and ``ThroughputCapacityPerHAPair`` are not the same value.
            - The value of ``ThroughputCapacity`` when divided by the value of ``HAPairs`` is outside of the valid range for ``ThroughputCapacity`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-throughputcapacity
            '''
            result = self._values.get("throughput_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput_capacity_per_ha_pair(self) -> typing.Optional[jsii.Number]:
            '''Use to choose the throughput capacity per HA pair, rather than the total throughput for the file system.

            You can define either the ``ThroughputCapacityPerHAPair`` or the ``ThroughputCapacity`` when creating a file system, but not both.

            This field and ``ThroughputCapacity`` are the same for file systems powered by one HA pair.

            - For ``SINGLE_AZ_1`` and ``MULTI_AZ_1`` file systems, valid values are 128, 256, 512, 1024, 2048, or 4096 MBps.
            - For ``SINGLE_AZ_2`` , valid values are 1536, 3072, or 6144 MBps.
            - For ``MULTI_AZ_2`` , valid values are 384, 768, 1536, 3072, or 6144 MBps.

            Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions:

            - The value of ``ThroughputCapacity`` and ``ThroughputCapacityPerHAPair`` are not the same value for file systems with one HA pair.
            - The value of deployment type is ``SINGLE_AZ_2`` and ``ThroughputCapacity`` / ``ThroughputCapacityPerHAPair`` is not a valid HA pair (a value between 1 and 12).
            - The value of ``ThroughputCapacityPerHAPair`` is not a valid value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-throughputcapacityperhapair
            '''
            result = self._values.get("throughput_capacity_per_ha_pair")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weekly_maintenance_start_time(self) -> typing.Optional[builtins.str]:
            '''The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday.

            For example, ``1:05:00`` specifies maintenance at 5 AM Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-ontapconfiguration.html#cfn-fsx-filesystem-ontapconfiguration-weeklymaintenancestarttime
            '''
            result = self._values.get("weekly_maintenance_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OntapConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.OpenZFSConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "automatic_backup_retention_days": "automaticBackupRetentionDays",
            "copy_tags_to_backups": "copyTagsToBackups",
            "copy_tags_to_volumes": "copyTagsToVolumes",
            "daily_automatic_backup_start_time": "dailyAutomaticBackupStartTime",
            "deployment_type": "deploymentType",
            "disk_iops_configuration": "diskIopsConfiguration",
            "endpoint_ip_address_range": "endpointIpAddressRange",
            "endpoint_ipv6_address_range": "endpointIpv6AddressRange",
            "options": "options",
            "preferred_subnet_id": "preferredSubnetId",
            "read_cache_configuration": "readCacheConfiguration",
            "root_volume_configuration": "rootVolumeConfiguration",
            "route_table_ids": "routeTableIds",
            "throughput_capacity": "throughputCapacity",
            "weekly_maintenance_start_time": "weeklyMaintenanceStartTime",
        },
    )
    class OpenZFSConfigurationProperty:
        def __init__(
            self,
            *,
            automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
            copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            copy_tags_to_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
            deployment_type: typing.Optional[builtins.str] = None,
            disk_iops_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.DiskIopsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            endpoint_ip_address_range: typing.Optional[builtins.str] = None,
            endpoint_ipv6_address_range: typing.Optional[builtins.str] = None,
            options: typing.Optional[typing.Sequence[builtins.str]] = None,
            preferred_subnet_id: typing.Optional[builtins.str] = None,
            read_cache_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.ReadCacheConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            root_volume_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.RootVolumeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            throughput_capacity: typing.Optional[jsii.Number] = None,
            weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The OpenZFS configuration for the file system that's being created.

            :param automatic_backup_retention_days: The number of days to retain automatic backups. Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``30`` .
            :param copy_tags_to_backups: A Boolean value indicating whether tags for the file system should be copied to backups. This value defaults to ``false`` . If it's set to ``true`` , all tags for the file system are copied to all automatic and user-initiated backups where the user doesn't specify tags. If this value is ``true`` , and you specify one or more tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the file system, regardless of this value.
            :param copy_tags_to_volumes: A Boolean value indicating whether tags for the file system should be copied to volumes. This value defaults to ``false`` . If it's set to ``true`` , all tags for the file system are copied to volumes where the user doesn't specify tags. If this value is ``true`` , and you specify one or more tags, only the specified tags are copied to volumes. If you specify one or more tags when creating the volume, no tags are copied from the file system, regardless of this value.
            :param daily_automatic_backup_start_time: A recurring daily time, in the format ``HH:MM`` . ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.
            :param deployment_type: Specifies the file system deployment type. Valid values are the following:. - ``MULTI_AZ_1`` - Creates file systems with high availability and durability by replicating your data and supporting failover across multiple Availability Zones in the same AWS Region . - ``SINGLE_AZ_HA_2`` - Creates file systems with high availability and throughput capacities of 160 - 10,240 MB/s using an NVMe L2ARC cache by deploying a primary and standby file system within the same Availability Zone. - ``SINGLE_AZ_HA_1`` - Creates file systems with high availability and throughput capacities of 64 - 4,096 MB/s by deploying a primary and standby file system within the same Availability Zone. - ``SINGLE_AZ_2`` - Creates file systems with throughput capacities of 160 - 10,240 MB/s using an NVMe L2ARC cache that automatically recover within a single Availability Zone. - ``SINGLE_AZ_1`` - Creates file systems with throughput capacities of 64 - 4,096 MBs that automatically recover within a single Availability Zone. For a list of which AWS Regions each deployment type is available in, see `Deployment type availability <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/availability-durability.html#available-aws-regions>`_ . For more information on the differences in performance between deployment types, see `File system performance <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance.html#zfs-fs-performance>`_ in the *Amazon FSx for OpenZFS User Guide* .
            :param disk_iops_configuration: The SSD IOPS (input/output operations per second) configuration for an Amazon FSx for NetApp ONTAP, Amazon FSx for Windows File Server, or FSx for OpenZFS file system. By default, Amazon FSx automatically provisions 3 IOPS per GB of storage capacity. You can provision additional IOPS per GB of storage. The configuration consists of the total number of provisioned SSD IOPS and how it is was provisioned, or the mode (by the customer or by Amazon FSx).
            :param endpoint_ip_address_range: (Multi-AZ only) Specifies the IPv4 address range in which the endpoints to access your file system will be created. By default in the Amazon FSx API and Amazon FSx console, Amazon FSx selects an available /28 IP address range for you from one of the VPC's CIDR ranges. You can have overlapping endpoint IP addresses for file systems deployed in the same VPC/route tables, as long as they don't overlap with any subnet.
            :param endpoint_ipv6_address_range: (Multi-AZ only) Specifies the IP address range in which the endpoints to access your file system will be created. By default in the Amazon FSx API and Amazon FSx console, Amazon FSx selects an available /118 IP address range for you from one of the VPC's CIDR ranges. You can have overlapping endpoint IP addresses for file systems deployed in the same VPC/route tables, as long as they don't overlap with any subnet.
            :param options: To delete a file system if there are child volumes present below the root volume, use the string ``DELETE_CHILD_VOLUMES_AND_SNAPSHOTS`` . If your file system has child volumes and you don't use this option, the delete request will fail.
            :param preferred_subnet_id: Required when ``DeploymentType`` is set to ``MULTI_AZ_1`` . This specifies the subnet in which you want the preferred file server to be located.
            :param read_cache_configuration: Specifies the optional provisioned SSD read cache on file systems that use the Intelligent-Tiering storage class.
            :param root_volume_configuration: The configuration Amazon FSx uses when creating the root value of the Amazon FSx for OpenZFS file system. All volumes are children of the root volume.
            :param route_table_ids: (Multi-AZ only) Specifies the route tables in which Amazon FSx creates the rules for routing traffic to the correct file server. You should specify all virtual private cloud (VPC) route tables associated with the subnets in which your clients are located. By default, Amazon FSx selects your VPC's default route table.
            :param throughput_capacity: Specifies the throughput of an Amazon FSx for OpenZFS file system, measured in megabytes per second (MBps). Required if you are creating a new file system. Valid values depend on the ``DeploymentType`` that you choose, as follows: - For ``MULTI_AZ_1`` and ``SINGLE_AZ_2`` , valid values are 160, 320, 640, 1280, 2560, 3840, 5120, 7680, or 10240 MBps. - For ``SINGLE_AZ_1`` , valid values are 64, 128, 256, 512, 1024, 2048, 3072, or 4096 MBps. You pay for additional throughput capacity that you provision.
            :param weekly_maintenance_start_time: The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday. For example, ``1:05:00`` specifies maintenance at 5 AM Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                open_zFSConfiguration_property = fsx_mixins.CfnFileSystemPropsMixin.OpenZFSConfigurationProperty(
                    automatic_backup_retention_days=123,
                    copy_tags_to_backups=False,
                    copy_tags_to_volumes=False,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    deployment_type="deploymentType",
                    disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    endpoint_ip_address_range="endpointIpAddressRange",
                    endpoint_ipv6_address_range="endpointIpv6AddressRange",
                    options=["options"],
                    preferred_subnet_id="preferredSubnetId",
                    read_cache_configuration=fsx_mixins.CfnFileSystemPropsMixin.ReadCacheConfigurationProperty(
                        size_gi_b=123,
                        sizing_mode="sizingMode"
                    ),
                    root_volume_configuration=fsx_mixins.CfnFileSystemPropsMixin.RootVolumeConfigurationProperty(
                        copy_tags_to_snapshots=False,
                        data_compression_type="dataCompressionType",
                        nfs_exports=[fsx_mixins.CfnFileSystemPropsMixin.NfsExportsProperty(
                            client_configurations=[fsx_mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty(
                                clients="clients",
                                options=["options"]
                            )]
                        )],
                        read_only=False,
                        record_size_ki_b=123,
                        user_and_group_quotas=[fsx_mixins.CfnFileSystemPropsMixin.UserAndGroupQuotasProperty(
                            id=123,
                            storage_capacity_quota_gi_b=123,
                            type="type"
                        )]
                    ),
                    route_table_ids=["routeTableIds"],
                    throughput_capacity=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5aee60985a3df3ba05cd1e4aae6945bdd924febd7257044e6628d346e19a4f90)
                check_type(argname="argument automatic_backup_retention_days", value=automatic_backup_retention_days, expected_type=type_hints["automatic_backup_retention_days"])
                check_type(argname="argument copy_tags_to_backups", value=copy_tags_to_backups, expected_type=type_hints["copy_tags_to_backups"])
                check_type(argname="argument copy_tags_to_volumes", value=copy_tags_to_volumes, expected_type=type_hints["copy_tags_to_volumes"])
                check_type(argname="argument daily_automatic_backup_start_time", value=daily_automatic_backup_start_time, expected_type=type_hints["daily_automatic_backup_start_time"])
                check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
                check_type(argname="argument disk_iops_configuration", value=disk_iops_configuration, expected_type=type_hints["disk_iops_configuration"])
                check_type(argname="argument endpoint_ip_address_range", value=endpoint_ip_address_range, expected_type=type_hints["endpoint_ip_address_range"])
                check_type(argname="argument endpoint_ipv6_address_range", value=endpoint_ipv6_address_range, expected_type=type_hints["endpoint_ipv6_address_range"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
                check_type(argname="argument preferred_subnet_id", value=preferred_subnet_id, expected_type=type_hints["preferred_subnet_id"])
                check_type(argname="argument read_cache_configuration", value=read_cache_configuration, expected_type=type_hints["read_cache_configuration"])
                check_type(argname="argument root_volume_configuration", value=root_volume_configuration, expected_type=type_hints["root_volume_configuration"])
                check_type(argname="argument route_table_ids", value=route_table_ids, expected_type=type_hints["route_table_ids"])
                check_type(argname="argument throughput_capacity", value=throughput_capacity, expected_type=type_hints["throughput_capacity"])
                check_type(argname="argument weekly_maintenance_start_time", value=weekly_maintenance_start_time, expected_type=type_hints["weekly_maintenance_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if automatic_backup_retention_days is not None:
                self._values["automatic_backup_retention_days"] = automatic_backup_retention_days
            if copy_tags_to_backups is not None:
                self._values["copy_tags_to_backups"] = copy_tags_to_backups
            if copy_tags_to_volumes is not None:
                self._values["copy_tags_to_volumes"] = copy_tags_to_volumes
            if daily_automatic_backup_start_time is not None:
                self._values["daily_automatic_backup_start_time"] = daily_automatic_backup_start_time
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type
            if disk_iops_configuration is not None:
                self._values["disk_iops_configuration"] = disk_iops_configuration
            if endpoint_ip_address_range is not None:
                self._values["endpoint_ip_address_range"] = endpoint_ip_address_range
            if endpoint_ipv6_address_range is not None:
                self._values["endpoint_ipv6_address_range"] = endpoint_ipv6_address_range
            if options is not None:
                self._values["options"] = options
            if preferred_subnet_id is not None:
                self._values["preferred_subnet_id"] = preferred_subnet_id
            if read_cache_configuration is not None:
                self._values["read_cache_configuration"] = read_cache_configuration
            if root_volume_configuration is not None:
                self._values["root_volume_configuration"] = root_volume_configuration
            if route_table_ids is not None:
                self._values["route_table_ids"] = route_table_ids
            if throughput_capacity is not None:
                self._values["throughput_capacity"] = throughput_capacity
            if weekly_maintenance_start_time is not None:
                self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

        @builtins.property
        def automatic_backup_retention_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days to retain automatic backups.

            Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``30`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-automaticbackupretentiondays
            '''
            result = self._values.get("automatic_backup_retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def copy_tags_to_backups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether tags for the file system should be copied to backups.

            This value defaults to ``false`` . If it's set to ``true`` , all tags for the file system are copied to all automatic and user-initiated backups where the user doesn't specify tags. If this value is ``true`` , and you specify one or more tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the file system, regardless of this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-copytagstobackups
            '''
            result = self._values.get("copy_tags_to_backups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def copy_tags_to_volumes(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether tags for the file system should be copied to volumes.

            This value defaults to ``false`` . If it's set to ``true`` , all tags for the file system are copied to volumes where the user doesn't specify tags. If this value is ``true`` , and you specify one or more tags, only the specified tags are copied to volumes. If you specify one or more tags when creating the volume, no tags are copied from the file system, regardless of this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-copytagstovolumes
            '''
            result = self._values.get("copy_tags_to_volumes")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def daily_automatic_backup_start_time(self) -> typing.Optional[builtins.str]:
            '''A recurring daily time, in the format ``HH:MM`` .

            ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-dailyautomaticbackupstarttime
            '''
            result = self._values.get("daily_automatic_backup_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the file system deployment type. Valid values are the following:.

            - ``MULTI_AZ_1`` - Creates file systems with high availability and durability by replicating your data and supporting failover across multiple Availability Zones in the same AWS Region .
            - ``SINGLE_AZ_HA_2`` - Creates file systems with high availability and throughput capacities of 160 - 10,240 MB/s using an NVMe L2ARC cache by deploying a primary and standby file system within the same Availability Zone.
            - ``SINGLE_AZ_HA_1`` - Creates file systems with high availability and throughput capacities of 64 - 4,096 MB/s by deploying a primary and standby file system within the same Availability Zone.
            - ``SINGLE_AZ_2`` - Creates file systems with throughput capacities of 160 - 10,240 MB/s using an NVMe L2ARC cache that automatically recover within a single Availability Zone.
            - ``SINGLE_AZ_1`` - Creates file systems with throughput capacities of 64 - 4,096 MBs that automatically recover within a single Availability Zone.

            For a list of which AWS Regions each deployment type is available in, see `Deployment type availability <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/availability-durability.html#available-aws-regions>`_ . For more information on the differences in performance between deployment types, see `File system performance <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance.html#zfs-fs-performance>`_ in the *Amazon FSx for OpenZFS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk_iops_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DiskIopsConfigurationProperty"]]:
            '''The SSD IOPS (input/output operations per second) configuration for an Amazon FSx for NetApp ONTAP, Amazon FSx for Windows File Server, or FSx for OpenZFS file system.

            By default, Amazon FSx automatically provisions 3 IOPS per GB of storage capacity. You can provision additional IOPS per GB of storage. The configuration consists of the total number of provisioned SSD IOPS and how it is was provisioned, or the mode (by the customer or by Amazon FSx).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-diskiopsconfiguration
            '''
            result = self._values.get("disk_iops_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DiskIopsConfigurationProperty"]], result)

        @builtins.property
        def endpoint_ip_address_range(self) -> typing.Optional[builtins.str]:
            '''(Multi-AZ only) Specifies the IPv4 address range in which the endpoints to access your file system will be created.

            By default in the Amazon FSx API and Amazon FSx console, Amazon FSx selects an available /28 IP address range for you from one of the VPC's CIDR ranges. You can have overlapping endpoint IP addresses for file systems deployed in the same VPC/route tables, as long as they don't overlap with any subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-endpointipaddressrange
            '''
            result = self._values.get("endpoint_ip_address_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint_ipv6_address_range(self) -> typing.Optional[builtins.str]:
            '''(Multi-AZ only) Specifies the IP address range in which the endpoints to access your file system will be created.

            By default in the Amazon FSx API and Amazon FSx console, Amazon FSx selects an available /118 IP address range for you from one of the VPC's CIDR ranges. You can have overlapping endpoint IP addresses for file systems deployed in the same VPC/route tables, as long as they don't overlap with any subnet.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-endpointipv6addressrange
            '''
            result = self._values.get("endpoint_ipv6_address_range")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''To delete a file system if there are child volumes present below the root volume, use the string ``DELETE_CHILD_VOLUMES_AND_SNAPSHOTS`` .

            If your file system has child volumes and you don't use this option, the delete request will fail.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def preferred_subnet_id(self) -> typing.Optional[builtins.str]:
            '''Required when ``DeploymentType`` is set to ``MULTI_AZ_1`` .

            This specifies the subnet in which you want the preferred file server to be located.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-preferredsubnetid
            '''
            result = self._values.get("preferred_subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_cache_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.ReadCacheConfigurationProperty"]]:
            '''Specifies the optional provisioned SSD read cache on file systems that use the Intelligent-Tiering storage class.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-readcacheconfiguration
            '''
            result = self._values.get("read_cache_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.ReadCacheConfigurationProperty"]], result)

        @builtins.property
        def root_volume_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.RootVolumeConfigurationProperty"]]:
            '''The configuration Amazon FSx uses when creating the root value of the Amazon FSx for OpenZFS file system.

            All volumes are children of the root volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-rootvolumeconfiguration
            '''
            result = self._values.get("root_volume_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.RootVolumeConfigurationProperty"]], result)

        @builtins.property
        def route_table_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''(Multi-AZ only) Specifies the route tables in which Amazon FSx creates the rules for routing traffic to the correct file server.

            You should specify all virtual private cloud (VPC) route tables associated with the subnets in which your clients are located. By default, Amazon FSx selects your VPC's default route table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-routetableids
            '''
            result = self._values.get("route_table_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def throughput_capacity(self) -> typing.Optional[jsii.Number]:
            '''Specifies the throughput of an Amazon FSx for OpenZFS file system, measured in megabytes per second (MBps).

            Required if you are creating a new file system.

            Valid values depend on the ``DeploymentType`` that you choose, as follows:

            - For ``MULTI_AZ_1`` and ``SINGLE_AZ_2`` , valid values are 160, 320, 640, 1280, 2560, 3840, 5120, 7680, or 10240 MBps.
            - For ``SINGLE_AZ_1`` , valid values are 64, 128, 256, 512, 1024, 2048, 3072, or 4096 MBps.

            You pay for additional throughput capacity that you provision.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-throughputcapacity
            '''
            result = self._values.get("throughput_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weekly_maintenance_start_time(self) -> typing.Optional[builtins.str]:
            '''The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday.

            For example, ``1:05:00`` specifies maintenance at 5 AM Monday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-openzfsconfiguration.html#cfn-fsx-filesystem-openzfsconfiguration-weeklymaintenancestarttime
            '''
            result = self._values.get("weekly_maintenance_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenZFSConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.ReadCacheConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"size_gib": "sizeGiB", "sizing_mode": "sizingMode"},
    )
    class ReadCacheConfigurationProperty:
        def __init__(
            self,
            *,
            size_gib: typing.Optional[jsii.Number] = None,
            sizing_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for the optional provisioned SSD read cache on Amazon FSx for OpenZFS file systems that use the Intelligent-Tiering storage class.

            :param size_gib: Required if ``SizingMode`` is set to ``USER_PROVISIONED`` . Specifies the size of the file system's SSD read cache, in gibibytes (GiB).
            :param sizing_mode: Specifies how the provisioned SSD read cache is sized, as follows:. - Set to ``NO_CACHE`` if you do not want to use an SSD read cache with your Intelligent-Tiering file system. - Set to ``USER_PROVISIONED`` to specify the exact size of your SSD read cache. - Set to ``PROPORTIONAL_TO_THROUGHPUT_CAPACITY`` to have your SSD read cache automatically sized based on your throughput capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-readcacheconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                read_cache_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.ReadCacheConfigurationProperty(
                    size_gi_b=123,
                    sizing_mode="sizingMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be91c926f4224f66fcb95ff8aec78a15829c35271a0e239329a27306a5fce7cc)
                check_type(argname="argument size_gib", value=size_gib, expected_type=type_hints["size_gib"])
                check_type(argname="argument sizing_mode", value=sizing_mode, expected_type=type_hints["sizing_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size_gib is not None:
                self._values["size_gib"] = size_gib
            if sizing_mode is not None:
                self._values["sizing_mode"] = sizing_mode

        @builtins.property
        def size_gib(self) -> typing.Optional[jsii.Number]:
            '''Required if ``SizingMode`` is set to ``USER_PROVISIONED`` .

            Specifies the size of the file system's SSD read cache, in gibibytes (GiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-readcacheconfiguration.html#cfn-fsx-filesystem-readcacheconfiguration-sizegib
            '''
            result = self._values.get("size_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def sizing_mode(self) -> typing.Optional[builtins.str]:
            '''Specifies how the provisioned SSD read cache is sized, as follows:.

            - Set to ``NO_CACHE`` if you do not want to use an SSD read cache with your Intelligent-Tiering file system.
            - Set to ``USER_PROVISIONED`` to specify the exact size of your SSD read cache.
            - Set to ``PROPORTIONAL_TO_THROUGHPUT_CAPACITY`` to have your SSD read cache automatically sized based on your throughput capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-readcacheconfiguration.html#cfn-fsx-filesystem-readcacheconfiguration-sizingmode
            '''
            result = self._values.get("sizing_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReadCacheConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.RootVolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_tags_to_snapshots": "copyTagsToSnapshots",
            "data_compression_type": "dataCompressionType",
            "nfs_exports": "nfsExports",
            "read_only": "readOnly",
            "record_size_kib": "recordSizeKiB",
            "user_and_group_quotas": "userAndGroupQuotas",
        },
    )
    class RootVolumeConfigurationProperty:
        def __init__(
            self,
            *,
            copy_tags_to_snapshots: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            data_compression_type: typing.Optional[builtins.str] = None,
            nfs_exports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.NfsExportsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            record_size_kib: typing.Optional[jsii.Number] = None,
            user_and_group_quotas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.UserAndGroupQuotasProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration of an Amazon FSx for OpenZFS root volume.

            :param copy_tags_to_snapshots: A Boolean value indicating whether tags for the volume should be copied to snapshots of the volume. This value defaults to ``false`` . If it's set to ``true`` , all tags for the volume are copied to snapshots where the user doesn't specify tags. If this value is ``true`` and you specify one or more tags, only the specified tags are copied to snapshots. If you specify one or more tags when creating the snapshot, no tags are copied from the volume, regardless of this value.
            :param data_compression_type: Specifies the method used to compress the data on the volume. The compression type is ``NONE`` by default. - ``NONE`` - Doesn't compress the data on the volume. ``NONE`` is the default. - ``ZSTD`` - Compresses the data in the volume using the Zstandard (ZSTD) compression algorithm. Compared to LZ4, Z-Standard provides a better compression ratio to minimize on-disk storage utilization. - ``LZ4`` - Compresses the data in the volume using the LZ4 compression algorithm. Compared to Z-Standard, LZ4 is less compute-intensive and delivers higher write throughput speeds.
            :param nfs_exports: The configuration object for mounting a file system.
            :param read_only: A Boolean value indicating whether the volume is read-only. Setting this value to ``true`` can be useful after you have completed changes to a volume and no longer want changes to occur.
            :param record_size_kib: Specifies the record size of an OpenZFS root volume, in kibibytes (KiB). Valid values are 4, 8, 16, 32, 64, 128, 256, 512, or 1024 KiB. The default is 128 KiB. Most workloads should use the default record size. Database workflows can benefit from a smaller record size, while streaming workflows can benefit from a larger record size. For additional guidance on setting a custom record size, see `Tips for maximizing performance <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance.html#performance-tips-zfs>`_ in the *Amazon FSx for OpenZFS User Guide* .
            :param user_and_group_quotas: An object specifying how much storage users or groups can use on the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                root_volume_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.RootVolumeConfigurationProperty(
                    copy_tags_to_snapshots=False,
                    data_compression_type="dataCompressionType",
                    nfs_exports=[fsx_mixins.CfnFileSystemPropsMixin.NfsExportsProperty(
                        client_configurations=[fsx_mixins.CfnFileSystemPropsMixin.ClientConfigurationsProperty(
                            clients="clients",
                            options=["options"]
                        )]
                    )],
                    read_only=False,
                    record_size_ki_b=123,
                    user_and_group_quotas=[fsx_mixins.CfnFileSystemPropsMixin.UserAndGroupQuotasProperty(
                        id=123,
                        storage_capacity_quota_gi_b=123,
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6bb9b98d7f59a7beec27dd797dcc2758f8db38184718fded8196d2041c828f8)
                check_type(argname="argument copy_tags_to_snapshots", value=copy_tags_to_snapshots, expected_type=type_hints["copy_tags_to_snapshots"])
                check_type(argname="argument data_compression_type", value=data_compression_type, expected_type=type_hints["data_compression_type"])
                check_type(argname="argument nfs_exports", value=nfs_exports, expected_type=type_hints["nfs_exports"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument record_size_kib", value=record_size_kib, expected_type=type_hints["record_size_kib"])
                check_type(argname="argument user_and_group_quotas", value=user_and_group_quotas, expected_type=type_hints["user_and_group_quotas"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_tags_to_snapshots is not None:
                self._values["copy_tags_to_snapshots"] = copy_tags_to_snapshots
            if data_compression_type is not None:
                self._values["data_compression_type"] = data_compression_type
            if nfs_exports is not None:
                self._values["nfs_exports"] = nfs_exports
            if read_only is not None:
                self._values["read_only"] = read_only
            if record_size_kib is not None:
                self._values["record_size_kib"] = record_size_kib
            if user_and_group_quotas is not None:
                self._values["user_and_group_quotas"] = user_and_group_quotas

        @builtins.property
        def copy_tags_to_snapshots(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether tags for the volume should be copied to snapshots of the volume.

            This value defaults to ``false`` . If it's set to ``true`` , all tags for the volume are copied to snapshots where the user doesn't specify tags. If this value is ``true`` and you specify one or more tags, only the specified tags are copied to snapshots. If you specify one or more tags when creating the snapshot, no tags are copied from the volume, regardless of this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html#cfn-fsx-filesystem-rootvolumeconfiguration-copytagstosnapshots
            '''
            result = self._values.get("copy_tags_to_snapshots")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_compression_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the method used to compress the data on the volume. The compression type is ``NONE`` by default.

            - ``NONE`` - Doesn't compress the data on the volume. ``NONE`` is the default.
            - ``ZSTD`` - Compresses the data in the volume using the Zstandard (ZSTD) compression algorithm. Compared to LZ4, Z-Standard provides a better compression ratio to minimize on-disk storage utilization.
            - ``LZ4`` - Compresses the data in the volume using the LZ4 compression algorithm. Compared to Z-Standard, LZ4 is less compute-intensive and delivers higher write throughput speeds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html#cfn-fsx-filesystem-rootvolumeconfiguration-datacompressiontype
            '''
            result = self._values.get("data_compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nfs_exports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.NfsExportsProperty"]]]]:
            '''The configuration object for mounting a file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html#cfn-fsx-filesystem-rootvolumeconfiguration-nfsexports
            '''
            result = self._values.get("nfs_exports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.NfsExportsProperty"]]]], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether the volume is read-only.

            Setting this value to ``true`` can be useful after you have completed changes to a volume and no longer want changes to occur.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html#cfn-fsx-filesystem-rootvolumeconfiguration-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def record_size_kib(self) -> typing.Optional[jsii.Number]:
            '''Specifies the record size of an OpenZFS root volume, in kibibytes (KiB).

            Valid values are 4, 8, 16, 32, 64, 128, 256, 512, or 1024 KiB. The default is 128 KiB. Most workloads should use the default record size. Database workflows can benefit from a smaller record size, while streaming workflows can benefit from a larger record size. For additional guidance on setting a custom record size, see `Tips for maximizing performance <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance.html#performance-tips-zfs>`_ in the *Amazon FSx for OpenZFS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html#cfn-fsx-filesystem-rootvolumeconfiguration-recordsizekib
            '''
            result = self._values.get("record_size_kib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_and_group_quotas(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.UserAndGroupQuotasProperty"]]]]:
            '''An object specifying how much storage users or groups can use on the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-rootvolumeconfiguration.html#cfn-fsx-filesystem-rootvolumeconfiguration-userandgroupquotas
            '''
            result = self._values.get("user_and_group_quotas")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.UserAndGroupQuotasProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RootVolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dns_ips": "dnsIps",
            "domain_join_service_account_secret": "domainJoinServiceAccountSecret",
            "domain_name": "domainName",
            "file_system_administrators_group": "fileSystemAdministratorsGroup",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
            "password": "password",
            "user_name": "userName",
        },
    )
    class SelfManagedActiveDirectoryConfigurationProperty:
        def __init__(
            self,
            *,
            dns_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
            domain_join_service_account_secret: typing.Optional[builtins.str] = None,
            domain_name: typing.Optional[builtins.str] = None,
            file_system_administrators_group: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
            password: typing.Optional[builtins.str] = None,
            user_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that Amazon FSx uses to join a FSx for Windows File Server file system or an FSx for ONTAP storage virtual machine (SVM) to a self-managed (including on-premises) Microsoft Active Directory (AD) directory.

            For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-managed-AD.html>`_ or `Managing FSx for ONTAP SVMs <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ .

            :param dns_ips: A list of up to three IP addresses of DNS servers or domain controllers in the self-managed AD directory.
            :param domain_join_service_account_secret: The Amazon Resource Name (ARN) of the AWS Secrets Manager secret containing the self-managed Active Directory domain join service account credentials. When provided, Amazon FSx uses the credentials stored in this secret to join the file system to your self-managed Active Directory domain. The secret must contain two key-value pairs: - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_USERNAME`` - The username for the service account - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_PASSWORD`` - The password for the service account For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-manage-prereqs.html>`_ or `Using Amazon FSx for ONTAP with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/self-manage-prereqs.html>`_ .
            :param domain_name: The fully qualified domain name of the self-managed AD directory, such as ``corp.example.com`` .
            :param file_system_administrators_group: (Optional) The name of the domain group whose members are granted administrative privileges for the file system. Administrative privileges include taking ownership of files and folders, setting audit controls (audit ACLs) on files and folders, and administering the file system remotely by using the FSx Remote PowerShell. The group that you specify must already exist in your domain. If you don't provide one, your AD domain's Domain Admins group is used.
            :param organizational_unit_distinguished_name: (Optional) The fully qualified distinguished name of the organizational unit within your self-managed AD directory. Amazon FSx only accepts OU as the direct parent of the file system. An example is ``OU=FSx,DC=yourdomain,DC=corp,DC=com`` . To learn more, see `RFC 2253 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2253>`_ . If none is provided, the FSx file system is created in the default location of your self-managed AD directory. .. epigraph:: Only Organizational Unit (OU) objects can be the direct parent of the file system that you're creating.
            :param password: The password for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain.
            :param user_name: The user name for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain. This account must have the permission to join computers to the domain in the organizational unit provided in ``OrganizationalUnitDistinguishedName`` , or in the default location of your AD domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                self_managed_active_directory_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                    dns_ips=["dnsIps"],
                    domain_join_service_account_secret="domainJoinServiceAccountSecret",
                    domain_name="domainName",
                    file_system_administrators_group="fileSystemAdministratorsGroup",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                    password="password",
                    user_name="userName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a431fd3da7f901199953df4d04d7d0c1ec8b7959b1119805dd3492755d043e0)
                check_type(argname="argument dns_ips", value=dns_ips, expected_type=type_hints["dns_ips"])
                check_type(argname="argument domain_join_service_account_secret", value=domain_join_service_account_secret, expected_type=type_hints["domain_join_service_account_secret"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument file_system_administrators_group", value=file_system_administrators_group, expected_type=type_hints["file_system_administrators_group"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_ips is not None:
                self._values["dns_ips"] = dns_ips
            if domain_join_service_account_secret is not None:
                self._values["domain_join_service_account_secret"] = domain_join_service_account_secret
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if file_system_administrators_group is not None:
                self._values["file_system_administrators_group"] = file_system_administrators_group
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name
            if password is not None:
                self._values["password"] = password
            if user_name is not None:
                self._values["user_name"] = user_name

        @builtins.property
        def dns_ips(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of up to three IP addresses of DNS servers or domain controllers in the self-managed AD directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-dnsips
            '''
            result = self._values.get("dns_ips")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def domain_join_service_account_secret(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager secret containing the self-managed Active Directory domain join service account credentials.

            When provided, Amazon FSx uses the credentials stored in this secret to join the file system to your self-managed Active Directory domain.

            The secret must contain two key-value pairs:

            - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_USERNAME`` - The username for the service account
            - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_PASSWORD`` - The password for the service account

            For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-manage-prereqs.html>`_ or `Using Amazon FSx for ONTAP with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/self-manage-prereqs.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-domainjoinserviceaccountsecret
            '''
            result = self._values.get("domain_join_service_account_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified domain name of the self-managed AD directory, such as ``corp.example.com`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_system_administrators_group(self) -> typing.Optional[builtins.str]:
            '''(Optional) The name of the domain group whose members are granted administrative privileges for the file system.

            Administrative privileges include taking ownership of files and folders, setting audit controls (audit ACLs) on files and folders, and administering the file system remotely by using the FSx Remote PowerShell. The group that you specify must already exist in your domain. If you don't provide one, your AD domain's Domain Admins group is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-filesystemadministratorsgroup
            '''
            result = self._values.get("file_system_administrators_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''(Optional) The fully qualified distinguished name of the organizational unit within your self-managed AD directory.

            Amazon FSx only accepts OU as the direct parent of the file system. An example is ``OU=FSx,DC=yourdomain,DC=corp,DC=com`` . To learn more, see `RFC 2253 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2253>`_ . If none is provided, the FSx file system is created in the default location of your self-managed AD directory.
            .. epigraph::

               Only Organizational Unit (OU) objects can be the direct parent of the file system that you're creating.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_name(self) -> typing.Optional[builtins.str]:
            '''The user name for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain.

            This account must have the permission to join computers to the domain in the organizational unit provided in ``OrganizationalUnitDistinguishedName`` , or in the default location of your AD domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-filesystem-selfmanagedactivedirectoryconfiguration-username
            '''
            result = self._values.get("user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedActiveDirectoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.UserAndGroupQuotasProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "storage_capacity_quota_gib": "storageCapacityQuotaGiB",
            "type": "type",
        },
    )
    class UserAndGroupQuotasProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[jsii.Number] = None,
            storage_capacity_quota_gib: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to configure quotas that define how much storage a user or group can use on an FSx for OpenZFS volume.

            For more information, see `Volume properties <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/managing-volumes.html#volume-properties>`_ in the FSx for OpenZFS User Guide.

            :param id: The ID of the user or group that the quota applies to.
            :param storage_capacity_quota_gib: The user or group's storage quota, in gibibytes (GiB).
            :param type: Specifies whether the quota applies to a user or group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-userandgroupquotas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                user_and_group_quotas_property = fsx_mixins.CfnFileSystemPropsMixin.UserAndGroupQuotasProperty(
                    id=123,
                    storage_capacity_quota_gi_b=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cc4796f4fdd0fcf5cf432d0c7c7a16852b381dd5e7aaf7a12ec78da49434aec2)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument storage_capacity_quota_gib", value=storage_capacity_quota_gib, expected_type=type_hints["storage_capacity_quota_gib"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if storage_capacity_quota_gib is not None:
                self._values["storage_capacity_quota_gib"] = storage_capacity_quota_gib
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def id(self) -> typing.Optional[jsii.Number]:
            '''The ID of the user or group that the quota applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-userandgroupquotas.html#cfn-fsx-filesystem-userandgroupquotas-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_capacity_quota_gib(self) -> typing.Optional[jsii.Number]:
            '''The user or group's storage quota, in gibibytes (GiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-userandgroupquotas.html#cfn-fsx-filesystem-userandgroupquotas-storagecapacityquotagib
            '''
            result = self._values.get("storage_capacity_quota_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the quota applies to a user or group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-userandgroupquotas.html#cfn-fsx-filesystem-userandgroupquotas-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserAndGroupQuotasProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnFileSystemPropsMixin.WindowsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_directory_id": "activeDirectoryId",
            "aliases": "aliases",
            "audit_log_configuration": "auditLogConfiguration",
            "automatic_backup_retention_days": "automaticBackupRetentionDays",
            "copy_tags_to_backups": "copyTagsToBackups",
            "daily_automatic_backup_start_time": "dailyAutomaticBackupStartTime",
            "deployment_type": "deploymentType",
            "disk_iops_configuration": "diskIopsConfiguration",
            "preferred_subnet_id": "preferredSubnetId",
            "self_managed_active_directory_configuration": "selfManagedActiveDirectoryConfiguration",
            "throughput_capacity": "throughputCapacity",
            "weekly_maintenance_start_time": "weeklyMaintenanceStartTime",
        },
    )
    class WindowsConfigurationProperty:
        def __init__(
            self,
            *,
            active_directory_id: typing.Optional[builtins.str] = None,
            aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
            audit_log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.AuditLogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
            copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
            deployment_type: typing.Optional[builtins.str] = None,
            disk_iops_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.DiskIopsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            preferred_subnet_id: typing.Optional[builtins.str] = None,
            self_managed_active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            throughput_capacity: typing.Optional[jsii.Number] = None,
            weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Microsoft Windows configuration for the file system that's being created.

            :param active_directory_id: The ID for an existing AWS Managed Microsoft Active Directory (AD) instance that the file system should join when it's created. Required if you are joining the file system to an existing AWS Managed Microsoft AD.
            :param aliases: An array of one or more DNS alias names that you want to associate with the Amazon FSx file system. Aliases allow you to use existing DNS names to access the data in your Amazon FSx file system. You can associate up to 50 aliases with a file system at any time. For more information, see `Working with DNS Aliases <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/managing-dns-aliases.html>`_ and `Walkthrough 5: Using DNS aliases to access your file system <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/walkthrough05-file-system-custom-CNAME.html>`_ , including additional steps you must take to be able to access your file system using a DNS alias. An alias name has to meet the following requirements: - Formatted as a fully-qualified domain name (FQDN), ``hostname.domain`` , for example, ``accounting.example.com`` . - Can contain alphanumeric characters, the underscore (_), and the hyphen (-). - Cannot start or end with a hyphen. - Can start with a numeric. For DNS alias names, Amazon FSx stores alphabetical characters as lowercase letters (a-z), regardless of how you specify them: as uppercase letters, lowercase letters, or the corresponding letters in escape codes.
            :param audit_log_configuration: The configuration that Amazon FSx for Windows File Server uses to audit and log user accesses of files, folders, and file shares on the Amazon FSx for Windows File Server file system.
            :param automatic_backup_retention_days: The number of days to retain automatic backups. Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``30`` .
            :param copy_tags_to_backups: A boolean flag indicating whether tags for the file system should be copied to backups. This value defaults to false. If it's set to true, all tags for the file system are copied to all automatic and user-initiated backups where the user doesn't specify tags. If this value is true, and you specify one or more tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the file system, regardless of this value.
            :param daily_automatic_backup_start_time: A recurring daily time, in the format ``HH:MM`` . ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.
            :param deployment_type: Specifies the file system deployment type, valid values are the following:. - ``MULTI_AZ_1`` - Deploys a high availability file system that is configured for Multi-AZ redundancy to tolerate temporary Availability Zone (AZ) unavailability. You can only deploy a Multi-AZ file system in AWS Regions that have a minimum of three Availability Zones. Also supports HDD storage type - ``SINGLE_AZ_1`` - (Default) Choose to deploy a file system that is configured for single AZ redundancy. - ``SINGLE_AZ_2`` - The latest generation Single AZ file system. Specifies a file system that is configured for single AZ redundancy and supports HDD storage type. For more information, see `Availability and Durability: Single-AZ and Multi-AZ File Systems <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html>`_ .
            :param disk_iops_configuration: The SSD IOPS (input/output operations per second) configuration for an Amazon FSx for Windows file system. By default, Amazon FSx automatically provisions 3 IOPS per GiB of storage capacity. You can provision additional IOPS per GiB of storage, up to the maximum limit associated with your chosen throughput capacity.
            :param preferred_subnet_id: Required when ``DeploymentType`` is set to ``MULTI_AZ_1`` . This specifies the subnet in which you want the preferred file server to be located. For in- AWS applications, we recommend that you launch your clients in the same availability zone as your preferred file server to reduce cross-availability zone data transfer costs and minimize latency.
            :param self_managed_active_directory_configuration: The configuration that Amazon FSx uses to join a FSx for Windows File Server file system or an FSx for ONTAP storage virtual machine (SVM) to a self-managed (including on-premises) Microsoft Active Directory (AD) directory. For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-managed-AD.html>`_ or `Managing FSx for ONTAP SVMs <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ .
            :param throughput_capacity: Sets the throughput capacity of an Amazon FSx file system, measured in megabytes per second (MB/s), in 2 to the *n* th increments, between 2^3 (8) and 2^11 (2048). .. epigraph:: To increase storage capacity, a file system must have a minimum throughput capacity of 16 MB/s.
            :param weekly_maintenance_start_time: The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                windows_configuration_property = fsx_mixins.CfnFileSystemPropsMixin.WindowsConfigurationProperty(
                    active_directory_id="activeDirectoryId",
                    aliases=["aliases"],
                    audit_log_configuration=fsx_mixins.CfnFileSystemPropsMixin.AuditLogConfigurationProperty(
                        audit_log_destination="auditLogDestination",
                        file_access_audit_log_level="fileAccessAuditLogLevel",
                        file_share_access_audit_log_level="fileShareAccessAuditLogLevel"
                    ),
                    automatic_backup_retention_days=123,
                    copy_tags_to_backups=False,
                    daily_automatic_backup_start_time="dailyAutomaticBackupStartTime",
                    deployment_type="deploymentType",
                    disk_iops_configuration=fsx_mixins.CfnFileSystemPropsMixin.DiskIopsConfigurationProperty(
                        iops=123,
                        mode="mode"
                    ),
                    preferred_subnet_id="preferredSubnetId",
                    self_managed_active_directory_configuration=fsx_mixins.CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                        dns_ips=["dnsIps"],
                        domain_join_service_account_secret="domainJoinServiceAccountSecret",
                        domain_name="domainName",
                        file_system_administrators_group="fileSystemAdministratorsGroup",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                        password="password",
                        user_name="userName"
                    ),
                    throughput_capacity=123,
                    weekly_maintenance_start_time="weeklyMaintenanceStartTime"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5e3c502b53ea552f6e56fbf9e348714477656e055126fc4cad7fd35fa94d23b)
                check_type(argname="argument active_directory_id", value=active_directory_id, expected_type=type_hints["active_directory_id"])
                check_type(argname="argument aliases", value=aliases, expected_type=type_hints["aliases"])
                check_type(argname="argument audit_log_configuration", value=audit_log_configuration, expected_type=type_hints["audit_log_configuration"])
                check_type(argname="argument automatic_backup_retention_days", value=automatic_backup_retention_days, expected_type=type_hints["automatic_backup_retention_days"])
                check_type(argname="argument copy_tags_to_backups", value=copy_tags_to_backups, expected_type=type_hints["copy_tags_to_backups"])
                check_type(argname="argument daily_automatic_backup_start_time", value=daily_automatic_backup_start_time, expected_type=type_hints["daily_automatic_backup_start_time"])
                check_type(argname="argument deployment_type", value=deployment_type, expected_type=type_hints["deployment_type"])
                check_type(argname="argument disk_iops_configuration", value=disk_iops_configuration, expected_type=type_hints["disk_iops_configuration"])
                check_type(argname="argument preferred_subnet_id", value=preferred_subnet_id, expected_type=type_hints["preferred_subnet_id"])
                check_type(argname="argument self_managed_active_directory_configuration", value=self_managed_active_directory_configuration, expected_type=type_hints["self_managed_active_directory_configuration"])
                check_type(argname="argument throughput_capacity", value=throughput_capacity, expected_type=type_hints["throughput_capacity"])
                check_type(argname="argument weekly_maintenance_start_time", value=weekly_maintenance_start_time, expected_type=type_hints["weekly_maintenance_start_time"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_directory_id is not None:
                self._values["active_directory_id"] = active_directory_id
            if aliases is not None:
                self._values["aliases"] = aliases
            if audit_log_configuration is not None:
                self._values["audit_log_configuration"] = audit_log_configuration
            if automatic_backup_retention_days is not None:
                self._values["automatic_backup_retention_days"] = automatic_backup_retention_days
            if copy_tags_to_backups is not None:
                self._values["copy_tags_to_backups"] = copy_tags_to_backups
            if daily_automatic_backup_start_time is not None:
                self._values["daily_automatic_backup_start_time"] = daily_automatic_backup_start_time
            if deployment_type is not None:
                self._values["deployment_type"] = deployment_type
            if disk_iops_configuration is not None:
                self._values["disk_iops_configuration"] = disk_iops_configuration
            if preferred_subnet_id is not None:
                self._values["preferred_subnet_id"] = preferred_subnet_id
            if self_managed_active_directory_configuration is not None:
                self._values["self_managed_active_directory_configuration"] = self_managed_active_directory_configuration
            if throughput_capacity is not None:
                self._values["throughput_capacity"] = throughput_capacity
            if weekly_maintenance_start_time is not None:
                self._values["weekly_maintenance_start_time"] = weekly_maintenance_start_time

        @builtins.property
        def active_directory_id(self) -> typing.Optional[builtins.str]:
            '''The ID for an existing AWS Managed Microsoft Active Directory (AD) instance that the file system should join when it's created.

            Required if you are joining the file system to an existing AWS Managed Microsoft AD.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-activedirectoryid
            '''
            result = self._values.get("active_directory_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def aliases(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of one or more DNS alias names that you want to associate with the Amazon FSx file system.

            Aliases allow you to use existing DNS names to access the data in your Amazon FSx file system. You can associate up to 50 aliases with a file system at any time.

            For more information, see `Working with DNS Aliases <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/managing-dns-aliases.html>`_ and `Walkthrough 5: Using DNS aliases to access your file system <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/walkthrough05-file-system-custom-CNAME.html>`_ , including additional steps you must take to be able to access your file system using a DNS alias.

            An alias name has to meet the following requirements:

            - Formatted as a fully-qualified domain name (FQDN), ``hostname.domain`` , for example, ``accounting.example.com`` .
            - Can contain alphanumeric characters, the underscore (_), and the hyphen (-).
            - Cannot start or end with a hyphen.
            - Can start with a numeric.

            For DNS alias names, Amazon FSx stores alphabetical characters as lowercase letters (a-z), regardless of how you specify them: as uppercase letters, lowercase letters, or the corresponding letters in escape codes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-aliases
            '''
            result = self._values.get("aliases")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def audit_log_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.AuditLogConfigurationProperty"]]:
            '''The configuration that Amazon FSx for Windows File Server uses to audit and log user accesses of files, folders, and file shares on the Amazon FSx for Windows File Server file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-auditlogconfiguration
            '''
            result = self._values.get("audit_log_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.AuditLogConfigurationProperty"]], result)

        @builtins.property
        def automatic_backup_retention_days(self) -> typing.Optional[jsii.Number]:
            '''The number of days to retain automatic backups.

            Setting this property to ``0`` disables automatic backups. You can retain automatic backups for a maximum of 90 days. The default is ``30`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-automaticbackupretentiondays
            '''
            result = self._values.get("automatic_backup_retention_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def copy_tags_to_backups(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A boolean flag indicating whether tags for the file system should be copied to backups.

            This value defaults to false. If it's set to true, all tags for the file system are copied to all automatic and user-initiated backups where the user doesn't specify tags. If this value is true, and you specify one or more tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the file system, regardless of this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-copytagstobackups
            '''
            result = self._values.get("copy_tags_to_backups")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def daily_automatic_backup_start_time(self) -> typing.Optional[builtins.str]:
            '''A recurring daily time, in the format ``HH:MM`` .

            ``HH`` is the zero-padded hour of the day (0-23), and ``MM`` is the zero-padded minute of the hour. For example, ``05:00`` specifies 5 AM daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-dailyautomaticbackupstarttime
            '''
            result = self._values.get("daily_automatic_backup_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def deployment_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the file system deployment type, valid values are the following:.

            - ``MULTI_AZ_1`` - Deploys a high availability file system that is configured for Multi-AZ redundancy to tolerate temporary Availability Zone (AZ) unavailability. You can only deploy a Multi-AZ file system in AWS Regions that have a minimum of three Availability Zones. Also supports HDD storage type
            - ``SINGLE_AZ_1`` - (Default) Choose to deploy a file system that is configured for single AZ redundancy.
            - ``SINGLE_AZ_2`` - The latest generation Single AZ file system. Specifies a file system that is configured for single AZ redundancy and supports HDD storage type.

            For more information, see `Availability and Durability: Single-AZ and Multi-AZ File Systems <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/high-availability-multiAZ.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-deploymenttype
            '''
            result = self._values.get("deployment_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def disk_iops_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DiskIopsConfigurationProperty"]]:
            '''The SSD IOPS (input/output operations per second) configuration for an Amazon FSx for Windows file system.

            By default, Amazon FSx automatically provisions 3 IOPS per GiB of storage capacity. You can provision additional IOPS per GiB of storage, up to the maximum limit associated with your chosen throughput capacity.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-diskiopsconfiguration
            '''
            result = self._values.get("disk_iops_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.DiskIopsConfigurationProperty"]], result)

        @builtins.property
        def preferred_subnet_id(self) -> typing.Optional[builtins.str]:
            '''Required when ``DeploymentType`` is set to ``MULTI_AZ_1`` .

            This specifies the subnet in which you want the preferred file server to be located. For in- AWS applications, we recommend that you launch your clients in the same availability zone as your preferred file server to reduce cross-availability zone data transfer costs and minimize latency.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-preferredsubnetid
            '''
            result = self._values.get("preferred_subnet_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def self_managed_active_directory_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty"]]:
            '''The configuration that Amazon FSx uses to join a FSx for Windows File Server file system or an FSx for ONTAP storage virtual machine (SVM) to a self-managed (including on-premises) Microsoft Active Directory (AD) directory.

            For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-managed-AD.html>`_ or `Managing FSx for ONTAP SVMs <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-svms.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-selfmanagedactivedirectoryconfiguration
            '''
            result = self._values.get("self_managed_active_directory_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty"]], result)

        @builtins.property
        def throughput_capacity(self) -> typing.Optional[jsii.Number]:
            '''Sets the throughput capacity of an Amazon FSx file system, measured in megabytes per second (MB/s), in 2 to the *n* th increments, between 2^3 (8) and 2^11 (2048).

            .. epigraph::

               To increase storage capacity, a file system must have a minimum throughput capacity of 16 MB/s.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-throughputcapacity
            '''
            result = self._values.get("throughput_capacity")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def weekly_maintenance_start_time(self) -> typing.Optional[builtins.str]:
            '''The preferred start time to perform weekly maintenance, formatted d:HH:MM in the UTC time zone, where d is the weekday number, from 1 through 7, beginning with Monday and ending with Sunday.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-filesystem-windowsconfiguration.html#cfn-fsx-filesystem-windowsconfiguration-weeklymaintenancestarttime
            '''
            result = self._values.get("weekly_maintenance_start_time")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WindowsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "ontap_configuration": "ontapConfiguration",
        "open_zfs_configuration": "openZfsConfiguration",
        "s3_access_point": "s3AccessPoint",
        "type": "type",
    },
)
class CfnS3AccessPointAttachmentMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        ontap_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        open_zfs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        s3_access_point: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnS3AccessPointAttachmentPropsMixin.

        :param name: The name of the S3 access point attachment; also used for the name of the S3 access point.
        :param ontap_configuration: 
        :param open_zfs_configuration: The OpenZFSConfiguration of the S3 access point attachment.
        :param s3_access_point: The S3 access point configuration of the S3 access point attachment.
        :param type: The type of Amazon FSx volume that the S3 access point is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
            
            # policy: Any
            
            cfn_s3_access_point_attachment_mixin_props = fsx_mixins.CfnS3AccessPointAttachmentMixinProps(
                name="name",
                ontap_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty(
                    file_system_identity=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty(
                        type="type",
                        unix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty(
                            name="name"
                        ),
                        windows_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty(
                            name="name"
                        )
                    ),
                    volume_id="volumeId"
                ),
                open_zfs_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty(
                    file_system_identity=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty(
                        posix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty(
                            gid=123,
                            secondary_gids=[fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty(
                                gid=123
                            )],
                            uid=123
                        ),
                        type="type"
                    ),
                    volume_id="volumeId"
                ),
                s3_access_point=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty(
                    alias="alias",
                    policy=policy,
                    resource_arn="resourceArn",
                    vpc_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty(
                        vpc_id="vpcId"
                    )
                ),
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e65d50c2b3aa1ecf41a8ad38c6395142b63033809f54900b51f04c068378a549)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ontap_configuration", value=ontap_configuration, expected_type=type_hints["ontap_configuration"])
            check_type(argname="argument open_zfs_configuration", value=open_zfs_configuration, expected_type=type_hints["open_zfs_configuration"])
            check_type(argname="argument s3_access_point", value=s3_access_point, expected_type=type_hints["s3_access_point"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if ontap_configuration is not None:
            self._values["ontap_configuration"] = ontap_configuration
        if open_zfs_configuration is not None:
            self._values["open_zfs_configuration"] = open_zfs_configuration
        if s3_access_point is not None:
            self._values["s3_access_point"] = s3_access_point
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the S3 access point attachment;

        also used for the name of the S3 access point.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html#cfn-fsx-s3accesspointattachment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ontap_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html#cfn-fsx-s3accesspointattachment-ontapconfiguration
        '''
        result = self._values.get("ontap_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty"]], result)

    @builtins.property
    def open_zfs_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty"]]:
        '''The OpenZFSConfiguration of the S3 access point attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html#cfn-fsx-s3accesspointattachment-openzfsconfiguration
        '''
        result = self._values.get("open_zfs_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty"]], result)

    @builtins.property
    def s3_access_point(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty"]]:
        '''The S3 access point configuration of the S3 access point attachment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html#cfn-fsx-s3accesspointattachment-s3accesspoint
        '''
        result = self._values.get("s3_access_point")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty"]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of Amazon FSx volume that the S3 access point is attached to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html#cfn-fsx-s3accesspointattachment-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnS3AccessPointAttachmentMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnS3AccessPointAttachmentPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin",
):
    '''An S3 access point attached to an Amazon FSx volume.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-s3accesspointattachment.html
    :cloudformationResource: AWS::FSx::S3AccessPointAttachment
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
        
        # policy: Any
        
        cfn_s3_access_point_attachment_props_mixin = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin(fsx_mixins.CfnS3AccessPointAttachmentMixinProps(
            name="name",
            ontap_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty(
                file_system_identity=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty(
                    type="type",
                    unix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty(
                        name="name"
                    ),
                    windows_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty(
                        name="name"
                    )
                ),
                volume_id="volumeId"
            ),
            open_zfs_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty(
                file_system_identity=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty(
                    posix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty(
                        gid=123,
                        secondary_gids=[fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty(
                            gid=123
                        )],
                        uid=123
                    ),
                    type="type"
                ),
                volume_id="volumeId"
            ),
            s3_access_point=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty(
                alias="alias",
                policy=policy,
                resource_arn="resourceArn",
                vpc_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            ),
            type="type"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnS3AccessPointAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FSx::S3AccessPointAttachment``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bb79e178c14bcf273fe1c6eeb57fc7c268bcfe79d2a43b69411d22f08a930e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eadcc9a424bc9fd7ae36dc6fbdaa80e4537fb24995ce5108784401053c2052f2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df074990cc2acb3c250290d63e586efa532f12d9a47a611f1ff05b156536a5f8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnS3AccessPointAttachmentMixinProps:
        return typing.cast(CfnS3AccessPointAttachmentMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid"},
    )
    class FileSystemGIDProperty:
        def __init__(self, *, gid: typing.Optional[jsii.Number] = None) -> None:
            '''The GID of the file system user.

            :param gid: The GID of the file system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-filesystemgid.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                file_system_gIDProperty = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty(
                    gid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65fcf240e099c8b4021a0a0ec51b6569aef70e1b9926ac95ac74110c510835bb)
                check_type(argname="argument gid", value=gid, expected_type=type_hints["gid"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if gid is not None:
                self._values["gid"] = gid

        @builtins.property
        def gid(self) -> typing.Optional[jsii.Number]:
            '''The GID of the file system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-filesystemgid.html#cfn-fsx-s3accesspointattachment-filesystemgid-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FileSystemGIDProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "unix_user": "unixUser",
            "windows_user": "windowsUser",
        },
    )
    class OntapFileSystemIdentityProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            unix_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            windows_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''
            :param type: Specifies the FSx for ONTAP user identity type, accepts either UNIX or WINDOWS.
            :param unix_user: 
            :param windows_user: 

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapfilesystemidentity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                ontap_file_system_identity_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty(
                    type="type",
                    unix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty(
                        name="name"
                    ),
                    windows_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty(
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bef2e643dccafc05f8cfce072f06962cdcb10f4a3279b1de596e80a042bb2882)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unix_user", value=unix_user, expected_type=type_hints["unix_user"])
                check_type(argname="argument windows_user", value=windows_user, expected_type=type_hints["windows_user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if unix_user is not None:
                self._values["unix_user"] = unix_user
            if windows_user is not None:
                self._values["windows_user"] = windows_user

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the FSx for ONTAP user identity type, accepts either UNIX or WINDOWS.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapfilesystemidentity.html#cfn-fsx-s3accesspointattachment-ontapfilesystemidentity-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unix_user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapfilesystemidentity.html#cfn-fsx-s3accesspointattachment-ontapfilesystemidentity-unixuser
            '''
            result = self._values.get("unix_user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty"]], result)

        @builtins.property
        def windows_user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapfilesystemidentity.html#cfn-fsx-s3accesspointattachment-ontapfilesystemidentity-windowsuser
            '''
            result = self._values.get("windows_user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OntapFileSystemIdentityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class OntapUnixFileSystemUserProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param name: The name of the UNIX user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapunixfilesystemuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                ontap_unix_file_system_user_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c0e9a2bfcd18108398d07bf96555de16c5fcc5616476be587f10f68aaa33e2c)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the UNIX user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapunixfilesystemuser.html#cfn-fsx-s3accesspointattachment-ontapunixfilesystemuser-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OntapUnixFileSystemUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name"},
    )
    class OntapWindowsFileSystemUserProperty:
        def __init__(self, *, name: typing.Optional[builtins.str] = None) -> None:
            '''
            :param name: The name of the Windows user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapwindowsfilesystemuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                ontap_windows_file_system_user_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty(
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1b22c2ece8e85799b2b230c4c73466844e914d64f0725dc11fbac5e2d8f1dcdb)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the Windows user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-ontapwindowsfilesystemuser.html#cfn-fsx-s3accesspointattachment-ontapwindowsfilesystemuser-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OntapWindowsFileSystemUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty",
        jsii_struct_bases=[],
        name_mapping={"posix_user": "posixUser", "type": "type"},
    )
    class OpenZFSFileSystemIdentityProperty:
        def __init__(
            self,
            *,
            posix_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the file system user identity that will be used for authorizing all file access requests that are made using the S3 access point.

            :param posix_user: Specifies the UID and GIDs of the file system POSIX user.
            :param type: Specifies the FSx for OpenZFS user identity type, accepts only ``POSIX`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsfilesystemidentity.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                open_zFSFile_system_identity_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty(
                    posix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty(
                        gid=123,
                        secondary_gids=[fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty(
                            gid=123
                        )],
                        uid=123
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc7f7d6e076581ab7b80568879c798170875d65c551a32d755465ed8dabfb9ac)
                check_type(argname="argument posix_user", value=posix_user, expected_type=type_hints["posix_user"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if posix_user is not None:
                self._values["posix_user"] = posix_user
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def posix_user(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty"]]:
            '''Specifies the UID and GIDs of the file system POSIX user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsfilesystemidentity.html#cfn-fsx-s3accesspointattachment-openzfsfilesystemidentity-posixuser
            '''
            result = self._values.get("posix_user")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies the FSx for OpenZFS user identity type, accepts only ``POSIX`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsfilesystemidentity.html#cfn-fsx-s3accesspointattachment-openzfsfilesystemidentity-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenZFSFileSystemIdentityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty",
        jsii_struct_bases=[],
        name_mapping={"gid": "gid", "secondary_gids": "secondaryGids", "uid": "uid"},
    )
    class OpenZFSPosixFileSystemUserProperty:
        def __init__(
            self,
            *,
            gid: typing.Optional[jsii.Number] = None,
            secondary_gids: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            uid: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The FSx for OpenZFS file system user that is used for authorizing all file access requests that are made using the S3 access point.

            :param gid: The GID of the file system user.
            :param secondary_gids: The list of secondary GIDs for the file system user.
            :param uid: The UID of the file system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsposixfilesystemuser.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                open_zFSPosix_file_system_user_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty(
                    gid=123,
                    secondary_gids=[fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty(
                        gid=123
                    )],
                    uid=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49a831c9a1bbfcea096c1ba6cce9c0d361dc86092ea2d1d5f081fc6f0d276432)
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
            '''The GID of the file system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsposixfilesystemuser.html#cfn-fsx-s3accesspointattachment-openzfsposixfilesystemuser-gid
            '''
            result = self._values.get("gid")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def secondary_gids(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty"]]]]:
            '''The list of secondary GIDs for the file system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsposixfilesystemuser.html#cfn-fsx-s3accesspointattachment-openzfsposixfilesystemuser-secondarygids
            '''
            result = self._values.get("secondary_gids")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty"]]]], result)

        @builtins.property
        def uid(self) -> typing.Optional[jsii.Number]:
            '''The UID of the file system user.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-openzfsposixfilesystemuser.html#cfn-fsx-s3accesspointattachment-openzfsposixfilesystemuser-uid
            '''
            result = self._values.get("uid")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenZFSPosixFileSystemUserProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "file_system_identity": "fileSystemIdentity",
            "volume_id": "volumeId",
        },
    )
    class S3AccessPointOntapConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param file_system_identity: 
            :param volume_id: The ID of the FSx for ONTAP volume that the S3 access point is attached to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointontapconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                s3_access_point_ontap_configuration_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty(
                    file_system_identity=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty(
                        type="type",
                        unix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty(
                            name="name"
                        ),
                        windows_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty(
                            name="name"
                        )
                    ),
                    volume_id="volumeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b7c735dd71e905f682434ec590b18b0aeff0a3e1e6b0055421a8180af87dfc30)
                check_type(argname="argument file_system_identity", value=file_system_identity, expected_type=type_hints["file_system_identity"])
                check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_system_identity is not None:
                self._values["file_system_identity"] = file_system_identity
            if volume_id is not None:
                self._values["volume_id"] = volume_id

        @builtins.property
        def file_system_identity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty"]]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointontapconfiguration.html#cfn-fsx-s3accesspointattachment-s3accesspointontapconfiguration-filesystemidentity
            '''
            result = self._values.get("file_system_identity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty"]], result)

        @builtins.property
        def volume_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the FSx for ONTAP volume that the S3 access point is attached to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointontapconfiguration.html#cfn-fsx-s3accesspointattachment-s3accesspointontapconfiguration-volumeid
            '''
            result = self._values.get("volume_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3AccessPointOntapConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "file_system_identity": "fileSystemIdentity",
            "volume_id": "volumeId",
        },
    )
    class S3AccessPointOpenZFSConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the FSx for OpenZFS attachment configuration of an S3 access point attachment.

            :param file_system_identity: The file system identity used to authorize file access requests made using the S3 access point.
            :param volume_id: The ID of the FSx for OpenZFS volume that the S3 access point is attached to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointopenzfsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                s3_access_point_open_zFSConfiguration_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty(
                    file_system_identity=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty(
                        posix_user=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty(
                            gid=123,
                            secondary_gids=[fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty(
                                gid=123
                            )],
                            uid=123
                        ),
                        type="type"
                    ),
                    volume_id="volumeId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__229fd8bc32cc5ce3f8efd3a8a9e28710082d5e6f4dfef89a1ac7844087c9404b)
                check_type(argname="argument file_system_identity", value=file_system_identity, expected_type=type_hints["file_system_identity"])
                check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if file_system_identity is not None:
                self._values["file_system_identity"] = file_system_identity
            if volume_id is not None:
                self._values["volume_id"] = volume_id

        @builtins.property
        def file_system_identity(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty"]]:
            '''The file system identity used to authorize file access requests made using the S3 access point.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointopenzfsconfiguration.html#cfn-fsx-s3accesspointattachment-s3accesspointopenzfsconfiguration-filesystemidentity
            '''
            result = self._values.get("file_system_identity")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty"]], result)

        @builtins.property
        def volume_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the FSx for OpenZFS volume that the S3 access point is attached to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointopenzfsconfiguration.html#cfn-fsx-s3accesspointattachment-s3accesspointopenzfsconfiguration-volumeid
            '''
            result = self._values.get("volume_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3AccessPointOpenZFSConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty",
        jsii_struct_bases=[],
        name_mapping={
            "alias": "alias",
            "policy": "policy",
            "resource_arn": "resourceArn",
            "vpc_configuration": "vpcConfiguration",
        },
    )
    class S3AccessPointProperty:
        def __init__(
            self,
            *,
            alias: typing.Optional[builtins.str] = None,
            policy: typing.Any = None,
            resource_arn: typing.Optional[builtins.str] = None,
            vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the S3 access point configuration of the S3 access point attachment.

            :param alias: The S3 access point's alias.
            :param policy: The S3 access point's policy.
            :param resource_arn: The S3 access point's ARN.
            :param vpc_configuration: The S3 access point's virtual private cloud (VPC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                # policy: Any
                
                s3_access_point_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty(
                    alias="alias",
                    policy=policy,
                    resource_arn="resourceArn",
                    vpc_configuration=fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty(
                        vpc_id="vpcId"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7a76fb14c8da3ec3987ec6d34d6915ba3f7108b390d96988ee6a580885bd19f1)
                check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument vpc_configuration", value=vpc_configuration, expected_type=type_hints["vpc_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alias is not None:
                self._values["alias"] = alias
            if policy is not None:
                self._values["policy"] = policy
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if vpc_configuration is not None:
                self._values["vpc_configuration"] = vpc_configuration

        @builtins.property
        def alias(self) -> typing.Optional[builtins.str]:
            '''The S3 access point's alias.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspoint.html#cfn-fsx-s3accesspointattachment-s3accesspoint-alias
            '''
            result = self._values.get("alias")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy(self) -> typing.Any:
            '''The S3 access point's policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspoint.html#cfn-fsx-s3accesspointattachment-s3accesspoint-policy
            '''
            result = self._values.get("policy")
            return typing.cast(typing.Any, result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The S3 access point's ARN.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspoint.html#cfn-fsx-s3accesspointattachment-s3accesspoint-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty"]]:
            '''The S3 access point's virtual private cloud (VPC) configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspoint.html#cfn-fsx-s3accesspointattachment-s3accesspoint-vpcconfiguration
            '''
            result = self._values.get("vpc_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3AccessPointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_id": "vpcId"},
    )
    class S3AccessPointVpcConfigurationProperty:
        def __init__(self, *, vpc_id: typing.Optional[builtins.str] = None) -> None:
            '''If included, Amazon S3 restricts access to this access point to requests from the specified virtual private cloud (VPC).

            :param vpc_id: Specifies the virtual private cloud (VPC) for the S3 access point VPC configuration, if one exists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointvpcconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                s3_access_point_vpc_configuration_property = fsx_mixins.CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty(
                    vpc_id="vpcId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c9aef700c8291216aa16e4133addb9c6d47809873813dac65638009cf024fb78)
                check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def vpc_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the virtual private cloud (VPC) for the S3 access point VPC configuration, if one exists.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-s3accesspointattachment-s3accesspointvpcconfiguration.html#cfn-fsx-s3accesspointattachment-s3accesspointvpcconfiguration-vpcid
            '''
            result = self._values.get("vpc_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3AccessPointVpcConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnSnapshotMixinProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "tags": "tags", "volume_id": "volumeId"},
)
class CfnSnapshotMixinProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        volume_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSnapshotPropsMixin.

        :param name: The name of the snapshot.
        :param tags: A list of ``Tag`` values, with a maximum of 50 elements.
        :param volume_id: The ID of the volume that the snapshot is of.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-snapshot.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
            
            cfn_snapshot_mixin_props = fsx_mixins.CfnSnapshotMixinProps(
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                volume_id="volumeId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8084cbbcad737f43724c08cec4be58008bfa452d88d3b6e1913b404478f3cab4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument volume_id", value=volume_id, expected_type=type_hints["volume_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if volume_id is not None:
            self._values["volume_id"] = volume_id

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the snapshot.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-snapshot.html#cfn-fsx-snapshot-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of ``Tag`` values, with a maximum of 50 elements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-snapshot.html#cfn-fsx-snapshot-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def volume_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the volume that the snapshot is of.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-snapshot.html#cfn-fsx-snapshot-volumeid
        '''
        result = self._values.get("volume_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSnapshotMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSnapshotPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnSnapshotPropsMixin",
):
    '''A snapshot of an Amazon FSx for OpenZFS volume.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-snapshot.html
    :cloudformationResource: AWS::FSx::Snapshot
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
        
        cfn_snapshot_props_mixin = fsx_mixins.CfnSnapshotPropsMixin(fsx_mixins.CfnSnapshotMixinProps(
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            volume_id="volumeId"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FSx::Snapshot``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3218db377f425947883de134759aa43e12e1ad7d3ab3d941cb9dc733059cebb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15f91c788faa245c0a1b561d53700e104b3c0dc40844f4fe6afee83c74fb975c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5070c97d1a7a8daebdf726786101bd42ce76cf55c8e6e5d3534e67dc9516bb14)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSnapshotMixinProps:
        return typing.cast(CfnSnapshotMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnStorageVirtualMachineMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "active_directory_configuration": "activeDirectoryConfiguration",
        "file_system_id": "fileSystemId",
        "name": "name",
        "root_volume_security_style": "rootVolumeSecurityStyle",
        "svm_admin_password": "svmAdminPassword",
        "tags": "tags",
    },
)
class CfnStorageVirtualMachineMixinProps:
    def __init__(
        self,
        *,
        active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        file_system_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        root_volume_security_style: typing.Optional[builtins.str] = None,
        svm_admin_password: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnStorageVirtualMachinePropsMixin.

        :param active_directory_configuration: Describes the Microsoft Active Directory configuration to which the SVM is joined, if applicable.
        :param file_system_id: Specifies the FSx for ONTAP file system on which to create the SVM.
        :param name: The name of the SVM.
        :param root_volume_security_style: The security style of the root volume of the SVM. Specify one of the following values:. - ``UNIX`` if the file system is managed by a UNIX administrator, the majority of users are NFS clients, and an application accessing the data uses a UNIX user as the service account. - ``NTFS`` if the file system is managed by a Microsoft Windows administrator, the majority of users are SMB clients, and an application accessing the data uses a Microsoft Windows user as the service account. - ``MIXED`` This is an advanced setting. For more information, see `Volume security style <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/volume-security-style.html>`_ in the Amazon FSx for NetApp ONTAP User Guide.
        :param svm_admin_password: Specifies the password to use when logging on to the SVM using a secure shell (SSH) connection to the SVM's management endpoint. Doing so enables you to manage the SVM using the NetApp ONTAP CLI or REST API. If you do not specify a password, you can still use the file system's ``fsxadmin`` user to manage the SVM. For more information, see `Managing SVMs using the NetApp ONTAP CLI <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-resources-ontap-apps.html#vsadmin-ontap-cli>`_ in the *FSx for ONTAP User Guide* .
        :param tags: A list of ``Tag`` values, with a maximum of 50 elements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
            
            cfn_storage_virtual_machine_mixin_props = fsx_mixins.CfnStorageVirtualMachineMixinProps(
                active_directory_configuration=fsx_mixins.CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty(
                    net_bios_name="netBiosName",
                    self_managed_active_directory_configuration=fsx_mixins.CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                        dns_ips=["dnsIps"],
                        domain_join_service_account_secret="domainJoinServiceAccountSecret",
                        domain_name="domainName",
                        file_system_administrators_group="fileSystemAdministratorsGroup",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                        password="password",
                        user_name="userName"
                    )
                ),
                file_system_id="fileSystemId",
                name="name",
                root_volume_security_style="rootVolumeSecurityStyle",
                svm_admin_password="svmAdminPassword",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6c1e89cd228a1eca651dbaa50e9d9f86b129ee22f5cca0042629f3bc4e1f487)
            check_type(argname="argument active_directory_configuration", value=active_directory_configuration, expected_type=type_hints["active_directory_configuration"])
            check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument root_volume_security_style", value=root_volume_security_style, expected_type=type_hints["root_volume_security_style"])
            check_type(argname="argument svm_admin_password", value=svm_admin_password, expected_type=type_hints["svm_admin_password"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_directory_configuration is not None:
            self._values["active_directory_configuration"] = active_directory_configuration
        if file_system_id is not None:
            self._values["file_system_id"] = file_system_id
        if name is not None:
            self._values["name"] = name
        if root_volume_security_style is not None:
            self._values["root_volume_security_style"] = root_volume_security_style
        if svm_admin_password is not None:
            self._values["svm_admin_password"] = svm_admin_password
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def active_directory_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty"]]:
        '''Describes the Microsoft Active Directory configuration to which the SVM is joined, if applicable.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html#cfn-fsx-storagevirtualmachine-activedirectoryconfiguration
        '''
        result = self._values.get("active_directory_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty"]], result)

    @builtins.property
    def file_system_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the FSx for ONTAP file system on which to create the SVM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html#cfn-fsx-storagevirtualmachine-filesystemid
        '''
        result = self._values.get("file_system_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the SVM.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html#cfn-fsx-storagevirtualmachine-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def root_volume_security_style(self) -> typing.Optional[builtins.str]:
        '''The security style of the root volume of the SVM. Specify one of the following values:.

        - ``UNIX`` if the file system is managed by a UNIX administrator, the majority of users are NFS clients, and an application accessing the data uses a UNIX user as the service account.
        - ``NTFS`` if the file system is managed by a Microsoft Windows administrator, the majority of users are SMB clients, and an application accessing the data uses a Microsoft Windows user as the service account.
        - ``MIXED`` This is an advanced setting. For more information, see `Volume security style <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/volume-security-style.html>`_ in the Amazon FSx for NetApp ONTAP User Guide.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html#cfn-fsx-storagevirtualmachine-rootvolumesecuritystyle
        '''
        result = self._values.get("root_volume_security_style")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def svm_admin_password(self) -> typing.Optional[builtins.str]:
        '''Specifies the password to use when logging on to the SVM using a secure shell (SSH) connection to the SVM's management endpoint.

        Doing so enables you to manage the SVM using the NetApp ONTAP CLI or REST API. If you do not specify a password, you can still use the file system's ``fsxadmin`` user to manage the SVM. For more information, see `Managing SVMs using the NetApp ONTAP CLI <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-resources-ontap-apps.html#vsadmin-ontap-cli>`_ in the *FSx for ONTAP User Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html#cfn-fsx-storagevirtualmachine-svmadminpassword
        '''
        result = self._values.get("svm_admin_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''A list of ``Tag`` values, with a maximum of 50 elements.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html#cfn-fsx-storagevirtualmachine-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStorageVirtualMachineMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnStorageVirtualMachinePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnStorageVirtualMachinePropsMixin",
):
    '''Creates a storage virtual machine (SVM) for an Amazon FSx for ONTAP file system.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-storagevirtualmachine.html
    :cloudformationResource: AWS::FSx::StorageVirtualMachine
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
        
        cfn_storage_virtual_machine_props_mixin = fsx_mixins.CfnStorageVirtualMachinePropsMixin(fsx_mixins.CfnStorageVirtualMachineMixinProps(
            active_directory_configuration=fsx_mixins.CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty(
                net_bios_name="netBiosName",
                self_managed_active_directory_configuration=fsx_mixins.CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                    dns_ips=["dnsIps"],
                    domain_join_service_account_secret="domainJoinServiceAccountSecret",
                    domain_name="domainName",
                    file_system_administrators_group="fileSystemAdministratorsGroup",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                    password="password",
                    user_name="userName"
                )
            ),
            file_system_id="fileSystemId",
            name="name",
            root_volume_security_style="rootVolumeSecurityStyle",
            svm_admin_password="svmAdminPassword",
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
        props: typing.Union[CfnStorageVirtualMachineMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FSx::StorageVirtualMachine``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58a67c52f725c575566eea8d232b7c0ea5be5fc8b88e778bcf7be8e64794bfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab324ec45035258f3b28454c4f3c1c12ef1f54e4e653e577fd8c76ad7c00976c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc041e92ed4f0e4c6cf0b1743002852e4234291b8ea5ae40064b748538880ea)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnStorageVirtualMachineMixinProps:
        return typing.cast(CfnStorageVirtualMachineMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "net_bios_name": "netBiosName",
            "self_managed_active_directory_configuration": "selfManagedActiveDirectoryConfiguration",
        },
    )
    class ActiveDirectoryConfigurationProperty:
        def __init__(
            self,
            *,
            net_bios_name: typing.Optional[builtins.str] = None,
            self_managed_active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the self-managed Microsoft Active Directory to which you want to join the SVM.

            Joining an Active Directory provides user authentication and access control for SMB clients, including Microsoft Windows and macOS clients accessing the file system.

            :param net_bios_name: The NetBIOS name of the Active Directory computer object that will be created for your SVM.
            :param self_managed_active_directory_configuration: The configuration that Amazon FSx uses to join the ONTAP storage virtual machine (SVM) to your self-managed (including on-premises) Microsoft Active Directory directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-activedirectoryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                active_directory_configuration_property = fsx_mixins.CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty(
                    net_bios_name="netBiosName",
                    self_managed_active_directory_configuration=fsx_mixins.CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                        dns_ips=["dnsIps"],
                        domain_join_service_account_secret="domainJoinServiceAccountSecret",
                        domain_name="domainName",
                        file_system_administrators_group="fileSystemAdministratorsGroup",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                        password="password",
                        user_name="userName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__35bd25593f8e2af906627ac77fa4c28d28df4926648d9c7bfce6332711684496)
                check_type(argname="argument net_bios_name", value=net_bios_name, expected_type=type_hints["net_bios_name"])
                check_type(argname="argument self_managed_active_directory_configuration", value=self_managed_active_directory_configuration, expected_type=type_hints["self_managed_active_directory_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if net_bios_name is not None:
                self._values["net_bios_name"] = net_bios_name
            if self_managed_active_directory_configuration is not None:
                self._values["self_managed_active_directory_configuration"] = self_managed_active_directory_configuration

        @builtins.property
        def net_bios_name(self) -> typing.Optional[builtins.str]:
            '''The NetBIOS name of the Active Directory computer object that will be created for your SVM.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-activedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-activedirectoryconfiguration-netbiosname
            '''
            result = self._values.get("net_bios_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def self_managed_active_directory_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty"]]:
            '''The configuration that Amazon FSx uses to join the ONTAP storage virtual machine (SVM) to your self-managed (including on-premises) Microsoft Active Directory directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-activedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-activedirectoryconfiguration-selfmanagedactivedirectoryconfiguration
            '''
            result = self._values.get("self_managed_active_directory_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActiveDirectoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dns_ips": "dnsIps",
            "domain_join_service_account_secret": "domainJoinServiceAccountSecret",
            "domain_name": "domainName",
            "file_system_administrators_group": "fileSystemAdministratorsGroup",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
            "password": "password",
            "user_name": "userName",
        },
    )
    class SelfManagedActiveDirectoryConfigurationProperty:
        def __init__(
            self,
            *,
            dns_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
            domain_join_service_account_secret: typing.Optional[builtins.str] = None,
            domain_name: typing.Optional[builtins.str] = None,
            file_system_administrators_group: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
            password: typing.Optional[builtins.str] = None,
            user_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration that Amazon FSx uses to join the ONTAP storage virtual machine (SVM) to your self-managed (including on-premises) Microsoft Active Directory directory.

            :param dns_ips: A list of up to three IP addresses of DNS servers or domain controllers in the self-managed AD directory.
            :param domain_join_service_account_secret: The Amazon Resource Name (ARN) of the AWS Secrets Manager secret containing the self-managed Active Directory domain join service account credentials. When provided, Amazon FSx uses the credentials stored in this secret to join the file system to your self-managed Active Directory domain. The secret must contain two key-value pairs: - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_USERNAME`` - The username for the service account - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_PASSWORD`` - The password for the service account For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-manage-prereqs.html>`_ or `Using Amazon FSx for ONTAP with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/self-manage-prereqs.html>`_ .
            :param domain_name: The fully qualified domain name of the self-managed AD directory, such as ``corp.example.com`` .
            :param file_system_administrators_group: (Optional) The name of the domain group whose members are granted administrative privileges for the file system. Administrative privileges include taking ownership of files and folders, setting audit controls (audit ACLs) on files and folders, and administering the file system remotely by using the FSx Remote PowerShell. The group that you specify must already exist in your domain. If you don't provide one, your AD domain's Domain Admins group is used.
            :param organizational_unit_distinguished_name: (Optional) The fully qualified distinguished name of the organizational unit within your self-managed AD directory. Amazon FSx only accepts OU as the direct parent of the file system. An example is ``OU=FSx,DC=yourdomain,DC=corp,DC=com`` . To learn more, see `RFC 2253 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2253>`_ . If none is provided, the FSx file system is created in the default location of your self-managed AD directory. .. epigraph:: Only Organizational Unit (OU) objects can be the direct parent of the file system that you're creating.
            :param password: The password for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain.
            :param user_name: The user name for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain. This account must have the permission to join computers to the domain in the organizational unit provided in ``OrganizationalUnitDistinguishedName`` , or in the default location of your AD domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                self_managed_active_directory_configuration_property = fsx_mixins.CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty(
                    dns_ips=["dnsIps"],
                    domain_join_service_account_secret="domainJoinServiceAccountSecret",
                    domain_name="domainName",
                    file_system_administrators_group="fileSystemAdministratorsGroup",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName",
                    password="password",
                    user_name="userName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5478ffee83e1e029f8efffb0eb39e13e4c7154d18dbe1a7c37f131d29e7b9703)
                check_type(argname="argument dns_ips", value=dns_ips, expected_type=type_hints["dns_ips"])
                check_type(argname="argument domain_join_service_account_secret", value=domain_join_service_account_secret, expected_type=type_hints["domain_join_service_account_secret"])
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument file_system_administrators_group", value=file_system_administrators_group, expected_type=type_hints["file_system_administrators_group"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_ips is not None:
                self._values["dns_ips"] = dns_ips
            if domain_join_service_account_secret is not None:
                self._values["domain_join_service_account_secret"] = domain_join_service_account_secret
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if file_system_administrators_group is not None:
                self._values["file_system_administrators_group"] = file_system_administrators_group
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name
            if password is not None:
                self._values["password"] = password
            if user_name is not None:
                self._values["user_name"] = user_name

        @builtins.property
        def dns_ips(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of up to three IP addresses of DNS servers or domain controllers in the self-managed AD directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-dnsips
            '''
            result = self._values.get("dns_ips")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def domain_join_service_account_secret(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the AWS Secrets Manager secret containing the self-managed Active Directory domain join service account credentials.

            When provided, Amazon FSx uses the credentials stored in this secret to join the file system to your self-managed Active Directory domain.

            The secret must contain two key-value pairs:

            - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_USERNAME`` - The username for the service account
            - ``CUSTOMER_MANAGED_ACTIVE_DIRECTORY_PASSWORD`` - The password for the service account

            For more information, see `Using Amazon FSx for Windows with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/WindowsGuide/self-manage-prereqs.html>`_ or `Using Amazon FSx for ONTAP with your self-managed Microsoft Active Directory <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/self-manage-prereqs.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-domainjoinserviceaccountsecret
            '''
            result = self._values.get("domain_join_service_account_secret")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The fully qualified domain name of the self-managed AD directory, such as ``corp.example.com`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_system_administrators_group(self) -> typing.Optional[builtins.str]:
            '''(Optional) The name of the domain group whose members are granted administrative privileges for the file system.

            Administrative privileges include taking ownership of files and folders, setting audit controls (audit ACLs) on files and folders, and administering the file system remotely by using the FSx Remote PowerShell. The group that you specify must already exist in your domain. If you don't provide one, your AD domain's Domain Admins group is used.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-filesystemadministratorsgroup
            '''
            result = self._values.get("file_system_administrators_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''(Optional) The fully qualified distinguished name of the organizational unit within your self-managed AD directory.

            Amazon FSx only accepts OU as the direct parent of the file system. An example is ``OU=FSx,DC=yourdomain,DC=corp,DC=com`` . To learn more, see `RFC 2253 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2253>`_ . If none is provided, the FSx file system is created in the default location of your self-managed AD directory.
            .. epigraph::

               Only Organizational Unit (OU) objects can be the direct parent of the file system that you're creating.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def user_name(self) -> typing.Optional[builtins.str]:
            '''The user name for the service account on your self-managed AD domain that Amazon FSx will use to join to your AD domain.

            This account must have the permission to join computers to the domain in the organizational unit provided in ``OrganizationalUnitDistinguishedName`` , or in the default location of your AD domain.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration.html#cfn-fsx-storagevirtualmachine-selfmanagedactivedirectoryconfiguration-username
            '''
            result = self._values.get("user_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SelfManagedActiveDirectoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_id": "backupId",
        "name": "name",
        "ontap_configuration": "ontapConfiguration",
        "open_zfs_configuration": "openZfsConfiguration",
        "tags": "tags",
        "volume_type": "volumeType",
    },
)
class CfnVolumeMixinProps:
    def __init__(
        self,
        *,
        backup_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        ontap_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.OntapConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        open_zfs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.OpenZFSConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        volume_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnVolumePropsMixin.

        :param backup_id: Specifies the ID of the volume backup to use to create a new volume.
        :param name: The name of the volume.
        :param ontap_configuration: The configuration of an Amazon FSx for NetApp ONTAP volume.
        :param open_zfs_configuration: The configuration of an Amazon FSx for OpenZFS volume.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param volume_type: The type of the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
            
            cfn_volume_mixin_props = fsx_mixins.CfnVolumeMixinProps(
                backup_id="backupId",
                name="name",
                ontap_configuration=fsx_mixins.CfnVolumePropsMixin.OntapConfigurationProperty(
                    aggregate_configuration=fsx_mixins.CfnVolumePropsMixin.AggregateConfigurationProperty(
                        aggregates=["aggregates"],
                        constituents_per_aggregate=123
                    ),
                    copy_tags_to_backups="copyTagsToBackups",
                    junction_path="junctionPath",
                    ontap_volume_type="ontapVolumeType",
                    security_style="securityStyle",
                    size_in_bytes="sizeInBytes",
                    size_in_megabytes="sizeInMegabytes",
                    snaplock_configuration=fsx_mixins.CfnVolumePropsMixin.SnaplockConfigurationProperty(
                        audit_log_volume="auditLogVolume",
                        autocommit_period=fsx_mixins.CfnVolumePropsMixin.AutocommitPeriodProperty(
                            type="type",
                            value=123
                        ),
                        privileged_delete="privilegedDelete",
                        retention_period=fsx_mixins.CfnVolumePropsMixin.SnaplockRetentionPeriodProperty(
                            default_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                                type="type",
                                value=123
                            ),
                            maximum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                                type="type",
                                value=123
                            ),
                            minimum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                                type="type",
                                value=123
                            )
                        ),
                        snaplock_type="snaplockType",
                        volume_append_mode_enabled="volumeAppendModeEnabled"
                    ),
                    snapshot_policy="snapshotPolicy",
                    storage_efficiency_enabled="storageEfficiencyEnabled",
                    storage_virtual_machine_id="storageVirtualMachineId",
                    tiering_policy=fsx_mixins.CfnVolumePropsMixin.TieringPolicyProperty(
                        cooling_period=123,
                        name="name"
                    ),
                    volume_style="volumeStyle"
                ),
                open_zfs_configuration=fsx_mixins.CfnVolumePropsMixin.OpenZFSConfigurationProperty(
                    copy_tags_to_snapshots=False,
                    data_compression_type="dataCompressionType",
                    nfs_exports=[fsx_mixins.CfnVolumePropsMixin.NfsExportsProperty(
                        client_configurations=[fsx_mixins.CfnVolumePropsMixin.ClientConfigurationsProperty(
                            clients="clients",
                            options=["options"]
                        )]
                    )],
                    options=["options"],
                    origin_snapshot=fsx_mixins.CfnVolumePropsMixin.OriginSnapshotProperty(
                        copy_strategy="copyStrategy",
                        snapshot_arn="snapshotArn"
                    ),
                    parent_volume_id="parentVolumeId",
                    read_only=False,
                    record_size_ki_b=123,
                    storage_capacity_quota_gi_b=123,
                    storage_capacity_reservation_gi_b=123,
                    user_and_group_quotas=[fsx_mixins.CfnVolumePropsMixin.UserAndGroupQuotasProperty(
                        id=123,
                        storage_capacity_quota_gi_b=123,
                        type="type"
                    )]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                volume_type="volumeType"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3af22a095953a4f4a77f8eec786177e5a52ae7f3465f7f6d6be681e93e21a6)
            check_type(argname="argument backup_id", value=backup_id, expected_type=type_hints["backup_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument ontap_configuration", value=ontap_configuration, expected_type=type_hints["ontap_configuration"])
            check_type(argname="argument open_zfs_configuration", value=open_zfs_configuration, expected_type=type_hints["open_zfs_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument volume_type", value=volume_type, expected_type=type_hints["volume_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if backup_id is not None:
            self._values["backup_id"] = backup_id
        if name is not None:
            self._values["name"] = name
        if ontap_configuration is not None:
            self._values["ontap_configuration"] = ontap_configuration
        if open_zfs_configuration is not None:
            self._values["open_zfs_configuration"] = open_zfs_configuration
        if tags is not None:
            self._values["tags"] = tags
        if volume_type is not None:
            self._values["volume_type"] = volume_type

    @builtins.property
    def backup_id(self) -> typing.Optional[builtins.str]:
        '''Specifies the ID of the volume backup to use to create a new volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html#cfn-fsx-volume-backupid
        '''
        result = self._values.get("backup_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html#cfn-fsx-volume-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ontap_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.OntapConfigurationProperty"]]:
        '''The configuration of an Amazon FSx for NetApp ONTAP volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html#cfn-fsx-volume-ontapconfiguration
        '''
        result = self._values.get("ontap_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.OntapConfigurationProperty"]], result)

    @builtins.property
    def open_zfs_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.OpenZFSConfigurationProperty"]]:
        '''The configuration of an Amazon FSx for OpenZFS volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html#cfn-fsx-volume-openzfsconfiguration
        '''
        result = self._values.get("open_zfs_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.OpenZFSConfigurationProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html#cfn-fsx-volume-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def volume_type(self) -> typing.Optional[builtins.str]:
        '''The type of the volume.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html#cfn-fsx-volume-volumetype
        '''
        result = self._values.get("volume_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVolumeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnVolumePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin",
):
    '''Creates an FSx for ONTAP or Amazon FSx for OpenZFS storage volume.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fsx-volume.html
    :cloudformationResource: AWS::FSx::Volume
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
        
        cfn_volume_props_mixin = fsx_mixins.CfnVolumePropsMixin(fsx_mixins.CfnVolumeMixinProps(
            backup_id="backupId",
            name="name",
            ontap_configuration=fsx_mixins.CfnVolumePropsMixin.OntapConfigurationProperty(
                aggregate_configuration=fsx_mixins.CfnVolumePropsMixin.AggregateConfigurationProperty(
                    aggregates=["aggregates"],
                    constituents_per_aggregate=123
                ),
                copy_tags_to_backups="copyTagsToBackups",
                junction_path="junctionPath",
                ontap_volume_type="ontapVolumeType",
                security_style="securityStyle",
                size_in_bytes="sizeInBytes",
                size_in_megabytes="sizeInMegabytes",
                snaplock_configuration=fsx_mixins.CfnVolumePropsMixin.SnaplockConfigurationProperty(
                    audit_log_volume="auditLogVolume",
                    autocommit_period=fsx_mixins.CfnVolumePropsMixin.AutocommitPeriodProperty(
                        type="type",
                        value=123
                    ),
                    privileged_delete="privilegedDelete",
                    retention_period=fsx_mixins.CfnVolumePropsMixin.SnaplockRetentionPeriodProperty(
                        default_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                            type="type",
                            value=123
                        ),
                        maximum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                            type="type",
                            value=123
                        ),
                        minimum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                            type="type",
                            value=123
                        )
                    ),
                    snaplock_type="snaplockType",
                    volume_append_mode_enabled="volumeAppendModeEnabled"
                ),
                snapshot_policy="snapshotPolicy",
                storage_efficiency_enabled="storageEfficiencyEnabled",
                storage_virtual_machine_id="storageVirtualMachineId",
                tiering_policy=fsx_mixins.CfnVolumePropsMixin.TieringPolicyProperty(
                    cooling_period=123,
                    name="name"
                ),
                volume_style="volumeStyle"
            ),
            open_zfs_configuration=fsx_mixins.CfnVolumePropsMixin.OpenZFSConfigurationProperty(
                copy_tags_to_snapshots=False,
                data_compression_type="dataCompressionType",
                nfs_exports=[fsx_mixins.CfnVolumePropsMixin.NfsExportsProperty(
                    client_configurations=[fsx_mixins.CfnVolumePropsMixin.ClientConfigurationsProperty(
                        clients="clients",
                        options=["options"]
                    )]
                )],
                options=["options"],
                origin_snapshot=fsx_mixins.CfnVolumePropsMixin.OriginSnapshotProperty(
                    copy_strategy="copyStrategy",
                    snapshot_arn="snapshotArn"
                ),
                parent_volume_id="parentVolumeId",
                read_only=False,
                record_size_ki_b=123,
                storage_capacity_quota_gi_b=123,
                storage_capacity_reservation_gi_b=123,
                user_and_group_quotas=[fsx_mixins.CfnVolumePropsMixin.UserAndGroupQuotasProperty(
                    id=123,
                    storage_capacity_quota_gi_b=123,
                    type="type"
                )]
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            volume_type="volumeType"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnVolumeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::FSx::Volume``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1441d3c30bc76399e1de4d38c0a3b94856bc318c32cfcb6fb6dcd522a6f615c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bc4c2d78ed2a80ce5410b770c949661d79c7303a50ca076c62d3f67eb89fec79)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80227bf44aea35f2e21c641e30d22dfe8c76f325ef2d594d676605377aa21a8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnVolumeMixinProps:
        return typing.cast(CfnVolumeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.AggregateConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregates": "aggregates",
            "constituents_per_aggregate": "constituentsPerAggregate",
        },
    )
    class AggregateConfigurationProperty:
        def __init__(
            self,
            *,
            aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
            constituents_per_aggregate: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use to specify configuration options for a volume’s storage aggregate or aggregates.

            :param aggregates: The list of aggregates that this volume resides on. Aggregates are storage pools which make up your primary storage tier. Each high-availability (HA) pair has one aggregate. The names of the aggregates map to the names of the aggregates in the ONTAP CLI and REST API. For FlexVols, there will always be a single entry. Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions: - The strings in the value of ``Aggregates`` are not are not formatted as ``aggrX`` , where X is a number between 1 and 12. - The value of ``Aggregates`` contains aggregates that are not present. - One or more of the aggregates supplied are too close to the volume limit to support adding more volumes.
            :param constituents_per_aggregate: Used to explicitly set the number of constituents within the FlexGroup per storage aggregate. This field is optional when creating a FlexGroup volume. If unspecified, the default value will be 8. This field cannot be provided when creating a FlexVol volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-aggregateconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                aggregate_configuration_property = fsx_mixins.CfnVolumePropsMixin.AggregateConfigurationProperty(
                    aggregates=["aggregates"],
                    constituents_per_aggregate=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0b9569343faa6529cb7865d1ee6c9d94f27c2a6c7a5d99c28ea64e627df4586c)
                check_type(argname="argument aggregates", value=aggregates, expected_type=type_hints["aggregates"])
                check_type(argname="argument constituents_per_aggregate", value=constituents_per_aggregate, expected_type=type_hints["constituents_per_aggregate"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregates is not None:
                self._values["aggregates"] = aggregates
            if constituents_per_aggregate is not None:
                self._values["constituents_per_aggregate"] = constituents_per_aggregate

        @builtins.property
        def aggregates(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of aggregates that this volume resides on.

            Aggregates are storage pools which make up your primary storage tier. Each high-availability (HA) pair has one aggregate. The names of the aggregates map to the names of the aggregates in the ONTAP CLI and REST API. For FlexVols, there will always be a single entry.

            Amazon FSx responds with an HTTP status code 400 (Bad Request) for the following conditions:

            - The strings in the value of ``Aggregates`` are not are not formatted as ``aggrX`` , where X is a number between 1 and 12.
            - The value of ``Aggregates`` contains aggregates that are not present.
            - One or more of the aggregates supplied are too close to the volume limit to support adding more volumes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-aggregateconfiguration.html#cfn-fsx-volume-aggregateconfiguration-aggregates
            '''
            result = self._values.get("aggregates")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def constituents_per_aggregate(self) -> typing.Optional[jsii.Number]:
            '''Used to explicitly set the number of constituents within the FlexGroup per storage aggregate.

            This field is optional when creating a FlexGroup volume. If unspecified, the default value will be 8. This field cannot be provided when creating a FlexVol volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-aggregateconfiguration.html#cfn-fsx-volume-aggregateconfiguration-constituentsperaggregate
            '''
            result = self._values.get("constituents_per_aggregate")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AggregateConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.AutocommitPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class AutocommitPeriodProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Sets the autocommit period of files in an FSx for ONTAP SnapLock volume, which determines how long the files must remain unmodified before they're automatically transitioned to the write once, read many (WORM) state.

            For more information, see `Autocommit <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/worm-state.html#worm-state-autocommit>`_ .

            :param type: Defines the type of time for the autocommit period of a file in an FSx for ONTAP SnapLock volume. Setting this value to ``NONE`` disables autocommit. The default value is ``NONE`` .
            :param value: Defines the amount of time for the autocommit period of a file in an FSx for ONTAP SnapLock volume. The following ranges are valid: - ``Minutes`` : 5 - 65,535 - ``Hours`` : 1 - 65,535 - ``Days`` : 1 - 3,650 - ``Months`` : 1 - 120 - ``Years`` : 1 - 10

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-autocommitperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                autocommit_period_property = fsx_mixins.CfnVolumePropsMixin.AutocommitPeriodProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac2880563386b390e0fc2a634c4916ca282708041929f0df7a84538239ab9d60)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Defines the type of time for the autocommit period of a file in an FSx for ONTAP SnapLock volume.

            Setting this value to ``NONE`` disables autocommit. The default value is ``NONE`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-autocommitperiod.html#cfn-fsx-volume-autocommitperiod-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''Defines the amount of time for the autocommit period of a file in an FSx for ONTAP SnapLock volume.

            The following ranges are valid:

            - ``Minutes`` : 5 - 65,535
            - ``Hours`` : 1 - 65,535
            - ``Days`` : 1 - 3,650
            - ``Months`` : 1 - 120
            - ``Years`` : 1 - 10

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-autocommitperiod.html#cfn-fsx-volume-autocommitperiod-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutocommitPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.ClientConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={"clients": "clients", "options": "options"},
    )
    class ClientConfigurationsProperty:
        def __init__(
            self,
            *,
            clients: typing.Optional[builtins.str] = None,
            options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies who can mount an OpenZFS file system and the options available while mounting the file system.

            :param clients: A value that specifies who can mount the file system. You can provide a wildcard character ( ``*`` ), an IP address ( ``0.0.0.0`` ), or a CIDR address ( ``192.0.2.0/24`` ). By default, Amazon FSx uses the wildcard character when specifying the client.
            :param options: The options to use when mounting the file system. For a list of options that you can use with Network File System (NFS), see the `exports(5) - Linux man page <https://docs.aws.amazon.com/https://linux.die.net/man/5/exports>`_ . When choosing your options, consider the following: - ``crossmnt`` is used by default. If you don't specify ``crossmnt`` when changing the client configuration, you won't be able to see or access snapshots in your file system's snapshot directory. - ``sync`` is used by default. If you instead specify ``async`` , the system acknowledges writes before writing to disk. If the system crashes before the writes are finished, you lose the unwritten data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-clientconfigurations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                client_configurations_property = fsx_mixins.CfnVolumePropsMixin.ClientConfigurationsProperty(
                    clients="clients",
                    options=["options"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b237336a5bd92dd5e2a97d6fac640b3995f82efdd9a151751d0659a4eab85cd9)
                check_type(argname="argument clients", value=clients, expected_type=type_hints["clients"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if clients is not None:
                self._values["clients"] = clients
            if options is not None:
                self._values["options"] = options

        @builtins.property
        def clients(self) -> typing.Optional[builtins.str]:
            '''A value that specifies who can mount the file system.

            You can provide a wildcard character ( ``*`` ), an IP address ( ``0.0.0.0`` ), or a CIDR address ( ``192.0.2.0/24`` ). By default, Amazon FSx uses the wildcard character when specifying the client.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-clientconfigurations.html#cfn-fsx-volume-clientconfigurations-clients
            '''
            result = self._values.get("clients")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The options to use when mounting the file system.

            For a list of options that you can use with Network File System (NFS), see the `exports(5) - Linux man page <https://docs.aws.amazon.com/https://linux.die.net/man/5/exports>`_ . When choosing your options, consider the following:

            - ``crossmnt`` is used by default. If you don't specify ``crossmnt`` when changing the client configuration, you won't be able to see or access snapshots in your file system's snapshot directory.
            - ``sync`` is used by default. If you instead specify ``async`` , the system acknowledges writes before writing to disk. If the system crashes before the writes are finished, you lose the unwritten data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-clientconfigurations.html#cfn-fsx-volume-clientconfigurations-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ClientConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.NfsExportsProperty",
        jsii_struct_bases=[],
        name_mapping={"client_configurations": "clientConfigurations"},
    )
    class NfsExportsProperty:
        def __init__(
            self,
            *,
            client_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.ClientConfigurationsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The configuration object for mounting a Network File System (NFS) file system.

            :param client_configurations: A list of configuration objects that contain the client and options for mounting the OpenZFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-nfsexports.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                nfs_exports_property = fsx_mixins.CfnVolumePropsMixin.NfsExportsProperty(
                    client_configurations=[fsx_mixins.CfnVolumePropsMixin.ClientConfigurationsProperty(
                        clients="clients",
                        options=["options"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4fe0a5e8c445fc1f2906c8db4fd59b991118137d35582825fed7e2c6b8f0952)
                check_type(argname="argument client_configurations", value=client_configurations, expected_type=type_hints["client_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if client_configurations is not None:
                self._values["client_configurations"] = client_configurations

        @builtins.property
        def client_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.ClientConfigurationsProperty"]]]]:
            '''A list of configuration objects that contain the client and options for mounting the OpenZFS file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-nfsexports.html#cfn-fsx-volume-nfsexports-clientconfigurations
            '''
            result = self._values.get("client_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.ClientConfigurationsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NfsExportsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.OntapConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "aggregate_configuration": "aggregateConfiguration",
            "copy_tags_to_backups": "copyTagsToBackups",
            "junction_path": "junctionPath",
            "ontap_volume_type": "ontapVolumeType",
            "security_style": "securityStyle",
            "size_in_bytes": "sizeInBytes",
            "size_in_megabytes": "sizeInMegabytes",
            "snaplock_configuration": "snaplockConfiguration",
            "snapshot_policy": "snapshotPolicy",
            "storage_efficiency_enabled": "storageEfficiencyEnabled",
            "storage_virtual_machine_id": "storageVirtualMachineId",
            "tiering_policy": "tieringPolicy",
            "volume_style": "volumeStyle",
        },
    )
    class OntapConfigurationProperty:
        def __init__(
            self,
            *,
            aggregate_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.AggregateConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            copy_tags_to_backups: typing.Optional[builtins.str] = None,
            junction_path: typing.Optional[builtins.str] = None,
            ontap_volume_type: typing.Optional[builtins.str] = None,
            security_style: typing.Optional[builtins.str] = None,
            size_in_bytes: typing.Optional[builtins.str] = None,
            size_in_megabytes: typing.Optional[builtins.str] = None,
            snaplock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.SnaplockConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snapshot_policy: typing.Optional[builtins.str] = None,
            storage_efficiency_enabled: typing.Optional[builtins.str] = None,
            storage_virtual_machine_id: typing.Optional[builtins.str] = None,
            tiering_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.TieringPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_style: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration of the ONTAP volume that you are creating.

            :param aggregate_configuration: Used to specify the configuration options for an FSx for ONTAP volume's storage aggregate or aggregates.
            :param copy_tags_to_backups: A boolean flag indicating whether tags for the volume should be copied to backups. This value defaults to false. If it's set to true, all tags for the volume are copied to all automatic and user-initiated backups where the user doesn't specify tags. If this value is true, and you specify one or more tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the volume, regardless of this value.
            :param junction_path: Specifies the location in the SVM's namespace where the volume is mounted. This parameter is required. The ``JunctionPath`` must have a leading forward slash, such as ``/vol3`` .
            :param ontap_volume_type: Specifies the type of volume you are creating. Valid values are the following:. - ``RW`` specifies a read/write volume. ``RW`` is the default. - ``DP`` specifies a data-protection volume. A ``DP`` volume is read-only and can be used as the destination of a NetApp SnapMirror relationship. For more information, see `Volume types <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html#volume-types>`_ in the Amazon FSx for NetApp ONTAP User Guide.
            :param security_style: Specifies the security style for the volume. If a volume's security style is not specified, it is automatically set to the root volume's security style. The security style determines the type of permissions that FSx for ONTAP uses to control data access. Specify one of the following values: - ``UNIX`` if the file system is managed by a UNIX administrator, the majority of users are NFS clients, and an application accessing the data uses a UNIX user as the service account. - ``NTFS`` if the file system is managed by a Windows administrator, the majority of users are SMB clients, and an application accessing the data uses a Windows user as the service account. - ``MIXED`` This is an advanced setting. For more information, see the topic `What the security styles and their effects are <https://docs.aws.amazon.com/https://docs.netapp.com/us-en/ontap/nfs-admin/security-styles-their-effects-concept.html>`_ in the NetApp Documentation Center. For more information, see `Volume security style <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html#volume-security-style>`_ in the FSx for ONTAP User Guide.
            :param size_in_bytes: Specifies the configured size of the volume, in bytes.
            :param size_in_megabytes: Use ``SizeInBytes`` instead. Specifies the size of the volume, in megabytes (MB), that you are creating.
            :param snaplock_configuration: The SnapLock configuration object for an FSx for ONTAP SnapLock volume.
            :param snapshot_policy: Specifies the snapshot policy for the volume. There are three built-in snapshot policies:. - ``default`` : This is the default policy. A maximum of six hourly snapshots taken five minutes past the hour. A maximum of two daily snapshots taken Monday through Saturday at 10 minutes after midnight. A maximum of two weekly snapshots taken every Sunday at 15 minutes after midnight. - ``default-1weekly`` : This policy is the same as the ``default`` policy except that it only retains one snapshot from the weekly schedule. - ``none`` : This policy does not take any snapshots. This policy can be assigned to volumes to prevent automatic snapshots from being taken. You can also provide the name of a custom policy that you created with the ONTAP CLI or REST API. For more information, see `Snapshot policies <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snapshots-ontap.html#snapshot-policies>`_ in the Amazon FSx for NetApp ONTAP User Guide.
            :param storage_efficiency_enabled: Set to true to enable deduplication, compression, and compaction storage efficiency features on the volume, or set to false to disable them. ``StorageEfficiencyEnabled`` is required when creating a ``RW`` volume ( ``OntapVolumeType`` set to ``RW`` ).
            :param storage_virtual_machine_id: Specifies the ONTAP SVM in which to create the volume.
            :param tiering_policy: Describes the data tiering policy for an ONTAP volume. When enabled, Amazon FSx for ONTAP's intelligent tiering automatically transitions a volume's data between the file system's primary storage and capacity pool storage based on your access patterns. Valid tiering policies are the following: - ``SNAPSHOT_ONLY`` - (Default value) moves cold snapshots to the capacity pool storage tier. - ``AUTO`` - moves cold user data and snapshots to the capacity pool storage tier based on your access patterns. - ``ALL`` - moves all user data blocks in both the active file system and Snapshot copies to the storage pool tier. - ``NONE`` - keeps a volume's data in the primary storage tier, preventing it from being moved to the capacity pool tier.
            :param volume_style: Use to specify the style of an ONTAP volume. FSx for ONTAP offers two styles of volumes that you can use for different purposes, FlexVol and FlexGroup volumes. For more information, see `Volume styles <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html#volume-styles>`_ in the Amazon FSx for NetApp ONTAP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                ontap_configuration_property = fsx_mixins.CfnVolumePropsMixin.OntapConfigurationProperty(
                    aggregate_configuration=fsx_mixins.CfnVolumePropsMixin.AggregateConfigurationProperty(
                        aggregates=["aggregates"],
                        constituents_per_aggregate=123
                    ),
                    copy_tags_to_backups="copyTagsToBackups",
                    junction_path="junctionPath",
                    ontap_volume_type="ontapVolumeType",
                    security_style="securityStyle",
                    size_in_bytes="sizeInBytes",
                    size_in_megabytes="sizeInMegabytes",
                    snaplock_configuration=fsx_mixins.CfnVolumePropsMixin.SnaplockConfigurationProperty(
                        audit_log_volume="auditLogVolume",
                        autocommit_period=fsx_mixins.CfnVolumePropsMixin.AutocommitPeriodProperty(
                            type="type",
                            value=123
                        ),
                        privileged_delete="privilegedDelete",
                        retention_period=fsx_mixins.CfnVolumePropsMixin.SnaplockRetentionPeriodProperty(
                            default_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                                type="type",
                                value=123
                            ),
                            maximum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                                type="type",
                                value=123
                            ),
                            minimum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                                type="type",
                                value=123
                            )
                        ),
                        snaplock_type="snaplockType",
                        volume_append_mode_enabled="volumeAppendModeEnabled"
                    ),
                    snapshot_policy="snapshotPolicy",
                    storage_efficiency_enabled="storageEfficiencyEnabled",
                    storage_virtual_machine_id="storageVirtualMachineId",
                    tiering_policy=fsx_mixins.CfnVolumePropsMixin.TieringPolicyProperty(
                        cooling_period=123,
                        name="name"
                    ),
                    volume_style="volumeStyle"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a54363825eaab112754a5d0edd4ff8b6fcfab199b029a378b9a11f4f97c02a8)
                check_type(argname="argument aggregate_configuration", value=aggregate_configuration, expected_type=type_hints["aggregate_configuration"])
                check_type(argname="argument copy_tags_to_backups", value=copy_tags_to_backups, expected_type=type_hints["copy_tags_to_backups"])
                check_type(argname="argument junction_path", value=junction_path, expected_type=type_hints["junction_path"])
                check_type(argname="argument ontap_volume_type", value=ontap_volume_type, expected_type=type_hints["ontap_volume_type"])
                check_type(argname="argument security_style", value=security_style, expected_type=type_hints["security_style"])
                check_type(argname="argument size_in_bytes", value=size_in_bytes, expected_type=type_hints["size_in_bytes"])
                check_type(argname="argument size_in_megabytes", value=size_in_megabytes, expected_type=type_hints["size_in_megabytes"])
                check_type(argname="argument snaplock_configuration", value=snaplock_configuration, expected_type=type_hints["snaplock_configuration"])
                check_type(argname="argument snapshot_policy", value=snapshot_policy, expected_type=type_hints["snapshot_policy"])
                check_type(argname="argument storage_efficiency_enabled", value=storage_efficiency_enabled, expected_type=type_hints["storage_efficiency_enabled"])
                check_type(argname="argument storage_virtual_machine_id", value=storage_virtual_machine_id, expected_type=type_hints["storage_virtual_machine_id"])
                check_type(argname="argument tiering_policy", value=tiering_policy, expected_type=type_hints["tiering_policy"])
                check_type(argname="argument volume_style", value=volume_style, expected_type=type_hints["volume_style"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aggregate_configuration is not None:
                self._values["aggregate_configuration"] = aggregate_configuration
            if copy_tags_to_backups is not None:
                self._values["copy_tags_to_backups"] = copy_tags_to_backups
            if junction_path is not None:
                self._values["junction_path"] = junction_path
            if ontap_volume_type is not None:
                self._values["ontap_volume_type"] = ontap_volume_type
            if security_style is not None:
                self._values["security_style"] = security_style
            if size_in_bytes is not None:
                self._values["size_in_bytes"] = size_in_bytes
            if size_in_megabytes is not None:
                self._values["size_in_megabytes"] = size_in_megabytes
            if snaplock_configuration is not None:
                self._values["snaplock_configuration"] = snaplock_configuration
            if snapshot_policy is not None:
                self._values["snapshot_policy"] = snapshot_policy
            if storage_efficiency_enabled is not None:
                self._values["storage_efficiency_enabled"] = storage_efficiency_enabled
            if storage_virtual_machine_id is not None:
                self._values["storage_virtual_machine_id"] = storage_virtual_machine_id
            if tiering_policy is not None:
                self._values["tiering_policy"] = tiering_policy
            if volume_style is not None:
                self._values["volume_style"] = volume_style

        @builtins.property
        def aggregate_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.AggregateConfigurationProperty"]]:
            '''Used to specify the configuration options for an FSx for ONTAP volume's storage aggregate or aggregates.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-aggregateconfiguration
            '''
            result = self._values.get("aggregate_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.AggregateConfigurationProperty"]], result)

        @builtins.property
        def copy_tags_to_backups(self) -> typing.Optional[builtins.str]:
            '''A boolean flag indicating whether tags for the volume should be copied to backups.

            This value defaults to false. If it's set to true, all tags for the volume are copied to all automatic and user-initiated backups where the user doesn't specify tags. If this value is true, and you specify one or more tags, only the specified tags are copied to backups. If you specify one or more tags when creating a user-initiated backup, no tags are copied from the volume, regardless of this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-copytagstobackups
            '''
            result = self._values.get("copy_tags_to_backups")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def junction_path(self) -> typing.Optional[builtins.str]:
            '''Specifies the location in the SVM's namespace where the volume is mounted.

            This parameter is required. The ``JunctionPath`` must have a leading forward slash, such as ``/vol3`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-junctionpath
            '''
            result = self._values.get("junction_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ontap_volume_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the type of volume you are creating. Valid values are the following:.

            - ``RW`` specifies a read/write volume. ``RW`` is the default.
            - ``DP`` specifies a data-protection volume. A ``DP`` volume is read-only and can be used as the destination of a NetApp SnapMirror relationship.

            For more information, see `Volume types <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html#volume-types>`_ in the Amazon FSx for NetApp ONTAP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-ontapvolumetype
            '''
            result = self._values.get("ontap_volume_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_style(self) -> typing.Optional[builtins.str]:
            '''Specifies the security style for the volume.

            If a volume's security style is not specified, it is automatically set to the root volume's security style. The security style determines the type of permissions that FSx for ONTAP uses to control data access. Specify one of the following values:

            - ``UNIX`` if the file system is managed by a UNIX administrator, the majority of users are NFS clients, and an application accessing the data uses a UNIX user as the service account.
            - ``NTFS`` if the file system is managed by a Windows administrator, the majority of users are SMB clients, and an application accessing the data uses a Windows user as the service account.
            - ``MIXED`` This is an advanced setting. For more information, see the topic `What the security styles and their effects are <https://docs.aws.amazon.com/https://docs.netapp.com/us-en/ontap/nfs-admin/security-styles-their-effects-concept.html>`_ in the NetApp Documentation Center.

            For more information, see `Volume security style <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html#volume-security-style>`_ in the FSx for ONTAP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-securitystyle
            '''
            result = self._values.get("security_style")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def size_in_bytes(self) -> typing.Optional[builtins.str]:
            '''Specifies the configured size of the volume, in bytes.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-sizeinbytes
            '''
            result = self._values.get("size_in_bytes")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def size_in_megabytes(self) -> typing.Optional[builtins.str]:
            '''Use ``SizeInBytes`` instead.

            Specifies the size of the volume, in megabytes (MB), that you are creating.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-sizeinmegabytes
            '''
            result = self._values.get("size_in_megabytes")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snaplock_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.SnaplockConfigurationProperty"]]:
            '''The SnapLock configuration object for an FSx for ONTAP SnapLock volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-snaplockconfiguration
            '''
            result = self._values.get("snaplock_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.SnaplockConfigurationProperty"]], result)

        @builtins.property
        def snapshot_policy(self) -> typing.Optional[builtins.str]:
            '''Specifies the snapshot policy for the volume. There are three built-in snapshot policies:.

            - ``default`` : This is the default policy. A maximum of six hourly snapshots taken five minutes past the hour. A maximum of two daily snapshots taken Monday through Saturday at 10 minutes after midnight. A maximum of two weekly snapshots taken every Sunday at 15 minutes after midnight.
            - ``default-1weekly`` : This policy is the same as the ``default`` policy except that it only retains one snapshot from the weekly schedule.
            - ``none`` : This policy does not take any snapshots. This policy can be assigned to volumes to prevent automatic snapshots from being taken.

            You can also provide the name of a custom policy that you created with the ONTAP CLI or REST API.

            For more information, see `Snapshot policies <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snapshots-ontap.html#snapshot-policies>`_ in the Amazon FSx for NetApp ONTAP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-snapshotpolicy
            '''
            result = self._values.get("snapshot_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_efficiency_enabled(self) -> typing.Optional[builtins.str]:
            '''Set to true to enable deduplication, compression, and compaction storage efficiency features on the volume, or set to false to disable them.

            ``StorageEfficiencyEnabled`` is required when creating a ``RW`` volume ( ``OntapVolumeType`` set to ``RW`` ).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-storageefficiencyenabled
            '''
            result = self._values.get("storage_efficiency_enabled")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def storage_virtual_machine_id(self) -> typing.Optional[builtins.str]:
            '''Specifies the ONTAP SVM in which to create the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-storagevirtualmachineid
            '''
            result = self._values.get("storage_virtual_machine_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tiering_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.TieringPolicyProperty"]]:
            '''Describes the data tiering policy for an ONTAP volume.

            When enabled, Amazon FSx for ONTAP's intelligent tiering automatically transitions a volume's data between the file system's primary storage and capacity pool storage based on your access patterns.

            Valid tiering policies are the following:

            - ``SNAPSHOT_ONLY`` - (Default value) moves cold snapshots to the capacity pool storage tier.
            - ``AUTO`` - moves cold user data and snapshots to the capacity pool storage tier based on your access patterns.
            - ``ALL`` - moves all user data blocks in both the active file system and Snapshot copies to the storage pool tier.
            - ``NONE`` - keeps a volume's data in the primary storage tier, preventing it from being moved to the capacity pool tier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-tieringpolicy
            '''
            result = self._values.get("tiering_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.TieringPolicyProperty"]], result)

        @builtins.property
        def volume_style(self) -> typing.Optional[builtins.str]:
            '''Use to specify the style of an ONTAP volume.

            FSx for ONTAP offers two styles of volumes that you can use for different purposes, FlexVol and FlexGroup volumes. For more information, see `Volume styles <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/managing-volumes.html#volume-styles>`_ in the Amazon FSx for NetApp ONTAP User Guide.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-ontapconfiguration.html#cfn-fsx-volume-ontapconfiguration-volumestyle
            '''
            result = self._values.get("volume_style")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OntapConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.OpenZFSConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "copy_tags_to_snapshots": "copyTagsToSnapshots",
            "data_compression_type": "dataCompressionType",
            "nfs_exports": "nfsExports",
            "options": "options",
            "origin_snapshot": "originSnapshot",
            "parent_volume_id": "parentVolumeId",
            "read_only": "readOnly",
            "record_size_kib": "recordSizeKiB",
            "storage_capacity_quota_gib": "storageCapacityQuotaGiB",
            "storage_capacity_reservation_gib": "storageCapacityReservationGiB",
            "user_and_group_quotas": "userAndGroupQuotas",
        },
    )
    class OpenZFSConfigurationProperty:
        def __init__(
            self,
            *,
            copy_tags_to_snapshots: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            data_compression_type: typing.Optional[builtins.str] = None,
            nfs_exports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.NfsExportsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            options: typing.Optional[typing.Sequence[builtins.str]] = None,
            origin_snapshot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.OriginSnapshotProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parent_volume_id: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            record_size_kib: typing.Optional[jsii.Number] = None,
            storage_capacity_quota_gib: typing.Optional[jsii.Number] = None,
            storage_capacity_reservation_gib: typing.Optional[jsii.Number] = None,
            user_and_group_quotas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.UserAndGroupQuotasProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Specifies the configuration of the Amazon FSx for OpenZFS volume that you are creating.

            :param copy_tags_to_snapshots: A Boolean value indicating whether tags for the volume should be copied to snapshots. This value defaults to ``false`` . If this value is set to ``true`` , and you do not specify any tags, all tags for the original volume are copied over to snapshots. If this value is set to ``true`` , and you do specify one or more tags, only the specified tags for the original volume are copied over to snapshots. If you specify one or more tags when creating a new snapshot, no tags are copied over from the original volume, regardless of this value.
            :param data_compression_type: Specifies the method used to compress the data on the volume. The compression type is ``NONE`` by default. - ``NONE`` - Doesn't compress the data on the volume. ``NONE`` is the default. - ``ZSTD`` - Compresses the data in the volume using the Zstandard (ZSTD) compression algorithm. Compared to LZ4, Z-Standard provides a better compression ratio to minimize on-disk storage utilization. - ``LZ4`` - Compresses the data in the volume using the LZ4 compression algorithm. Compared to Z-Standard, LZ4 is less compute-intensive and delivers higher write throughput speeds.
            :param nfs_exports: The configuration object for mounting a Network File System (NFS) file system.
            :param options: To delete the volume's child volumes, snapshots, and clones, use the string ``DELETE_CHILD_VOLUMES_AND_SNAPSHOTS`` .
            :param origin_snapshot: The configuration object that specifies the snapshot to use as the origin of the data for the volume.
            :param parent_volume_id: The ID of the volume to use as the parent volume of the volume that you are creating.
            :param read_only: A Boolean value indicating whether the volume is read-only.
            :param record_size_kib: Specifies the suggested block size for a volume in a ZFS dataset, in kibibytes (KiB). For file systems using the Intelligent-Tiering storage class, valid values are 128, 256, 512, 1024, 2048, or 4096 KiB, with a default of 1024 KiB. For all other file systems, valid values are 4, 8, 16, 32, 64, 128, 256, 512, or 1024 KiB, with a default of 128 KiB. We recommend using the default setting for the majority of use cases. Generally, workloads that write in fixed small or large record sizes may benefit from setting a custom record size, like database workloads (small record size) or media streaming workloads (large record size). For additional guidance on when to set a custom record size, see `ZFS Record size <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance.html#record-size-performance>`_ in the *Amazon FSx for OpenZFS User Guide* .
            :param storage_capacity_quota_gib: Sets the maximum storage size in gibibytes (GiB) for the volume. You can specify a quota that is larger than the storage on the parent volume. A volume quota limits the amount of storage that the volume can consume to the configured amount, but does not guarantee the space will be available on the parent volume. To guarantee quota space, you must also set ``StorageCapacityReservationGiB`` . To *not* specify a storage capacity quota, set this to ``-1`` . For more information, see `Volume properties <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/managing-volumes.html#volume-properties>`_ in the *Amazon FSx for OpenZFS User Guide* .
            :param storage_capacity_reservation_gib: Specifies the amount of storage in gibibytes (GiB) to reserve from the parent volume. Setting ``StorageCapacityReservationGiB`` guarantees that the specified amount of storage space on the parent volume will always be available for the volume. You can't reserve more storage than the parent volume has. To *not* specify a storage capacity reservation, set this to ``0`` or ``-1`` . For more information, see `Volume properties <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/managing-volumes.html#volume-properties>`_ in the *Amazon FSx for OpenZFS User Guide* .
            :param user_and_group_quotas: Configures how much storage users and groups can use on the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                open_zFSConfiguration_property = fsx_mixins.CfnVolumePropsMixin.OpenZFSConfigurationProperty(
                    copy_tags_to_snapshots=False,
                    data_compression_type="dataCompressionType",
                    nfs_exports=[fsx_mixins.CfnVolumePropsMixin.NfsExportsProperty(
                        client_configurations=[fsx_mixins.CfnVolumePropsMixin.ClientConfigurationsProperty(
                            clients="clients",
                            options=["options"]
                        )]
                    )],
                    options=["options"],
                    origin_snapshot=fsx_mixins.CfnVolumePropsMixin.OriginSnapshotProperty(
                        copy_strategy="copyStrategy",
                        snapshot_arn="snapshotArn"
                    ),
                    parent_volume_id="parentVolumeId",
                    read_only=False,
                    record_size_ki_b=123,
                    storage_capacity_quota_gi_b=123,
                    storage_capacity_reservation_gi_b=123,
                    user_and_group_quotas=[fsx_mixins.CfnVolumePropsMixin.UserAndGroupQuotasProperty(
                        id=123,
                        storage_capacity_quota_gi_b=123,
                        type="type"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b9cfce26d9c35376308f78d8f2124aa3b3113662de0490fa4cf4ffa0691c2a61)
                check_type(argname="argument copy_tags_to_snapshots", value=copy_tags_to_snapshots, expected_type=type_hints["copy_tags_to_snapshots"])
                check_type(argname="argument data_compression_type", value=data_compression_type, expected_type=type_hints["data_compression_type"])
                check_type(argname="argument nfs_exports", value=nfs_exports, expected_type=type_hints["nfs_exports"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
                check_type(argname="argument origin_snapshot", value=origin_snapshot, expected_type=type_hints["origin_snapshot"])
                check_type(argname="argument parent_volume_id", value=parent_volume_id, expected_type=type_hints["parent_volume_id"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument record_size_kib", value=record_size_kib, expected_type=type_hints["record_size_kib"])
                check_type(argname="argument storage_capacity_quota_gib", value=storage_capacity_quota_gib, expected_type=type_hints["storage_capacity_quota_gib"])
                check_type(argname="argument storage_capacity_reservation_gib", value=storage_capacity_reservation_gib, expected_type=type_hints["storage_capacity_reservation_gib"])
                check_type(argname="argument user_and_group_quotas", value=user_and_group_quotas, expected_type=type_hints["user_and_group_quotas"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_tags_to_snapshots is not None:
                self._values["copy_tags_to_snapshots"] = copy_tags_to_snapshots
            if data_compression_type is not None:
                self._values["data_compression_type"] = data_compression_type
            if nfs_exports is not None:
                self._values["nfs_exports"] = nfs_exports
            if options is not None:
                self._values["options"] = options
            if origin_snapshot is not None:
                self._values["origin_snapshot"] = origin_snapshot
            if parent_volume_id is not None:
                self._values["parent_volume_id"] = parent_volume_id
            if read_only is not None:
                self._values["read_only"] = read_only
            if record_size_kib is not None:
                self._values["record_size_kib"] = record_size_kib
            if storage_capacity_quota_gib is not None:
                self._values["storage_capacity_quota_gib"] = storage_capacity_quota_gib
            if storage_capacity_reservation_gib is not None:
                self._values["storage_capacity_reservation_gib"] = storage_capacity_reservation_gib
            if user_and_group_quotas is not None:
                self._values["user_and_group_quotas"] = user_and_group_quotas

        @builtins.property
        def copy_tags_to_snapshots(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether tags for the volume should be copied to snapshots.

            This value defaults to ``false`` . If this value is set to ``true`` , and you do not specify any tags, all tags for the original volume are copied over to snapshots. If this value is set to ``true`` , and you do specify one or more tags, only the specified tags for the original volume are copied over to snapshots. If you specify one or more tags when creating a new snapshot, no tags are copied over from the original volume, regardless of this value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-copytagstosnapshots
            '''
            result = self._values.get("copy_tags_to_snapshots")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def data_compression_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the method used to compress the data on the volume. The compression type is ``NONE`` by default.

            - ``NONE`` - Doesn't compress the data on the volume. ``NONE`` is the default.
            - ``ZSTD`` - Compresses the data in the volume using the Zstandard (ZSTD) compression algorithm. Compared to LZ4, Z-Standard provides a better compression ratio to minimize on-disk storage utilization.
            - ``LZ4`` - Compresses the data in the volume using the LZ4 compression algorithm. Compared to Z-Standard, LZ4 is less compute-intensive and delivers higher write throughput speeds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-datacompressiontype
            '''
            result = self._values.get("data_compression_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def nfs_exports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.NfsExportsProperty"]]]]:
            '''The configuration object for mounting a Network File System (NFS) file system.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-nfsexports
            '''
            result = self._values.get("nfs_exports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.NfsExportsProperty"]]]], result)

        @builtins.property
        def options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''To delete the volume's child volumes, snapshots, and clones, use the string ``DELETE_CHILD_VOLUMES_AND_SNAPSHOTS`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def origin_snapshot(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.OriginSnapshotProperty"]]:
            '''The configuration object that specifies the snapshot to use as the origin of the data for the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-originsnapshot
            '''
            result = self._values.get("origin_snapshot")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.OriginSnapshotProperty"]], result)

        @builtins.property
        def parent_volume_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the volume to use as the parent volume of the volume that you are creating.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-parentvolumeid
            '''
            result = self._values.get("parent_volume_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A Boolean value indicating whether the volume is read-only.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def record_size_kib(self) -> typing.Optional[jsii.Number]:
            '''Specifies the suggested block size for a volume in a ZFS dataset, in kibibytes (KiB).

            For file systems using the Intelligent-Tiering storage class, valid values are 128, 256, 512, 1024, 2048, or 4096 KiB, with a default of 1024 KiB. For all other file systems, valid values are 4, 8, 16, 32, 64, 128, 256, 512, or 1024 KiB, with a default of 128 KiB. We recommend using the default setting for the majority of use cases. Generally, workloads that write in fixed small or large record sizes may benefit from setting a custom record size, like database workloads (small record size) or media streaming workloads (large record size). For additional guidance on when to set a custom record size, see `ZFS Record size <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/performance.html#record-size-performance>`_ in the *Amazon FSx for OpenZFS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-recordsizekib
            '''
            result = self._values.get("record_size_kib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_capacity_quota_gib(self) -> typing.Optional[jsii.Number]:
            '''Sets the maximum storage size in gibibytes (GiB) for the volume.

            You can specify a quota that is larger than the storage on the parent volume. A volume quota limits the amount of storage that the volume can consume to the configured amount, but does not guarantee the space will be available on the parent volume. To guarantee quota space, you must also set ``StorageCapacityReservationGiB`` . To *not* specify a storage capacity quota, set this to ``-1`` .

            For more information, see `Volume properties <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/managing-volumes.html#volume-properties>`_ in the *Amazon FSx for OpenZFS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-storagecapacityquotagib
            '''
            result = self._values.get("storage_capacity_quota_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_capacity_reservation_gib(self) -> typing.Optional[jsii.Number]:
            '''Specifies the amount of storage in gibibytes (GiB) to reserve from the parent volume.

            Setting ``StorageCapacityReservationGiB`` guarantees that the specified amount of storage space on the parent volume will always be available for the volume. You can't reserve more storage than the parent volume has. To *not* specify a storage capacity reservation, set this to ``0`` or ``-1`` . For more information, see `Volume properties <https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/managing-volumes.html#volume-properties>`_ in the *Amazon FSx for OpenZFS User Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-storagecapacityreservationgib
            '''
            result = self._values.get("storage_capacity_reservation_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def user_and_group_quotas(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.UserAndGroupQuotasProperty"]]]]:
            '''Configures how much storage users and groups can use on the volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-openzfsconfiguration.html#cfn-fsx-volume-openzfsconfiguration-userandgroupquotas
            '''
            result = self._values.get("user_and_group_quotas")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.UserAndGroupQuotasProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OpenZFSConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.OriginSnapshotProperty",
        jsii_struct_bases=[],
        name_mapping={"copy_strategy": "copyStrategy", "snapshot_arn": "snapshotArn"},
    )
    class OriginSnapshotProperty:
        def __init__(
            self,
            *,
            copy_strategy: typing.Optional[builtins.str] = None,
            snapshot_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration object that specifies the snapshot to use as the origin of the data for the volume.

            :param copy_strategy: Specifies the strategy used when copying data from the snapshot to the new volume. - ``CLONE`` - The new volume references the data in the origin snapshot. Cloning a snapshot is faster than copying data from the snapshot to a new volume and doesn't consume disk throughput. However, the origin snapshot can't be deleted if there is a volume using its copied data. - ``FULL_COPY`` - Copies all data from the snapshot to the new volume. Specify this option to create the volume from a snapshot on another FSx for OpenZFS file system. .. epigraph:: The ``INCREMENTAL_COPY`` option is only for updating an existing volume by using a snapshot from another FSx for OpenZFS file system. For more information, see `CopySnapshotAndUpdateVolume <https://docs.aws.amazon.com/fsx/latest/APIReference/API_CopySnapshotAndUpdateVolume.html>`_ .
            :param snapshot_arn: Specifies the snapshot to use when creating an OpenZFS volume from a snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-originsnapshot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                origin_snapshot_property = fsx_mixins.CfnVolumePropsMixin.OriginSnapshotProperty(
                    copy_strategy="copyStrategy",
                    snapshot_arn="snapshotArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e5e750a6ba8313d0f0ecc78740e99917fba7728ebcc63e4017da59a2fb05a45e)
                check_type(argname="argument copy_strategy", value=copy_strategy, expected_type=type_hints["copy_strategy"])
                check_type(argname="argument snapshot_arn", value=snapshot_arn, expected_type=type_hints["snapshot_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if copy_strategy is not None:
                self._values["copy_strategy"] = copy_strategy
            if snapshot_arn is not None:
                self._values["snapshot_arn"] = snapshot_arn

        @builtins.property
        def copy_strategy(self) -> typing.Optional[builtins.str]:
            '''Specifies the strategy used when copying data from the snapshot to the new volume.

            - ``CLONE`` - The new volume references the data in the origin snapshot. Cloning a snapshot is faster than copying data from the snapshot to a new volume and doesn't consume disk throughput. However, the origin snapshot can't be deleted if there is a volume using its copied data.
            - ``FULL_COPY`` - Copies all data from the snapshot to the new volume.

            Specify this option to create the volume from a snapshot on another FSx for OpenZFS file system.
            .. epigraph::

               The ``INCREMENTAL_COPY`` option is only for updating an existing volume by using a snapshot from another FSx for OpenZFS file system. For more information, see `CopySnapshotAndUpdateVolume <https://docs.aws.amazon.com/fsx/latest/APIReference/API_CopySnapshotAndUpdateVolume.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-originsnapshot.html#cfn-fsx-volume-originsnapshot-copystrategy
            '''
            result = self._values.get("copy_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def snapshot_arn(self) -> typing.Optional[builtins.str]:
            '''Specifies the snapshot to use when creating an OpenZFS volume from a snapshot.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-originsnapshot.html#cfn-fsx-volume-originsnapshot-snapshotarn
            '''
            result = self._values.get("snapshot_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OriginSnapshotProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.RetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class RetentionPeriodProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the retention period of an FSx for ONTAP SnapLock volume.

            After it is set, it can't be changed. Files can't be deleted or modified during the retention period.

            For more information, see `Working with the retention period in SnapLock <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-retention.html>`_ .

            :param type: Defines the type of time for the retention period of an FSx for ONTAP SnapLock volume. Set it to one of the valid types. If you set it to ``INFINITE`` , the files are retained forever. If you set it to ``UNSPECIFIED`` , the files are retained until you set an explicit retention period.
            :param value: Defines the amount of time for the retention period of an FSx for ONTAP SnapLock volume. You can't set a value for ``INFINITE`` or ``UNSPECIFIED`` . For all other options, the following ranges are valid: - ``Seconds`` : 0 - 65,535 - ``Minutes`` : 0 - 65,535 - ``Hours`` : 0 - 24 - ``Days`` : 0 - 365 - ``Months`` : 0 - 12 - ``Years`` : 0 - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-retentionperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                retention_period_property = fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                    type="type",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f91c515aec5d01625bfb0c8854e00b181bc6d8db4ce337f934be52adb5b9542)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Defines the type of time for the retention period of an FSx for ONTAP SnapLock volume.

            Set it to one of the valid types. If you set it to ``INFINITE`` , the files are retained forever. If you set it to ``UNSPECIFIED`` , the files are retained until you set an explicit retention period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-retentionperiod.html#cfn-fsx-volume-retentionperiod-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''Defines the amount of time for the retention period of an FSx for ONTAP SnapLock volume.

            You can't set a value for ``INFINITE`` or ``UNSPECIFIED`` . For all other options, the following ranges are valid:

            - ``Seconds`` : 0 - 65,535
            - ``Minutes`` : 0 - 65,535
            - ``Hours`` : 0 - 24
            - ``Days`` : 0 - 365
            - ``Months`` : 0 - 12
            - ``Years`` : 0 - 100

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-retentionperiod.html#cfn-fsx-volume-retentionperiod-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.SnaplockConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "audit_log_volume": "auditLogVolume",
            "autocommit_period": "autocommitPeriod",
            "privileged_delete": "privilegedDelete",
            "retention_period": "retentionPeriod",
            "snaplock_type": "snaplockType",
            "volume_append_mode_enabled": "volumeAppendModeEnabled",
        },
    )
    class SnaplockConfigurationProperty:
        def __init__(
            self,
            *,
            audit_log_volume: typing.Optional[builtins.str] = None,
            autocommit_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.AutocommitPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            privileged_delete: typing.Optional[builtins.str] = None,
            retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.SnaplockRetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            snaplock_type: typing.Optional[builtins.str] = None,
            volume_append_mode_enabled: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the SnapLock configuration for an FSx for ONTAP SnapLock volume.

            :param audit_log_volume: Enables or disables the audit log volume for an FSx for ONTAP SnapLock volume. The default value is ``false`` . If you set ``AuditLogVolume`` to ``true`` , the SnapLock volume is created as an audit log volume. The minimum retention period for an audit log volume is six months. For more information, see `SnapLock audit log volumes <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/how-snaplock-works.html#snaplock-audit-log-volume>`_ .
            :param autocommit_period: The configuration object for setting the autocommit period of files in an FSx for ONTAP SnapLock volume.
            :param privileged_delete: Enables, disables, or permanently disables privileged delete on an FSx for ONTAP SnapLock Enterprise volume. Enabling privileged delete allows SnapLock administrators to delete write once, read many (WORM) files even if they have active retention periods. ``PERMANENTLY_DISABLED`` is a terminal state. If privileged delete is permanently disabled on a SnapLock volume, you can't re-enable it. The default value is ``DISABLED`` . For more information, see `Privileged delete <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-enterprise.html#privileged-delete>`_ .
            :param retention_period: Specifies the retention period of an FSx for ONTAP SnapLock volume.
            :param snaplock_type: Specifies the retention mode of an FSx for ONTAP SnapLock volume. After it is set, it can't be changed. You can choose one of the following retention modes: - ``COMPLIANCE`` : Files transitioned to write once, read many (WORM) on a Compliance volume can't be deleted until their retention periods expire. This retention mode is used to address government or industry-specific mandates or to protect against ransomware attacks. For more information, see `SnapLock Compliance <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-compliance.html>`_ . - ``ENTERPRISE`` : Files transitioned to WORM on an Enterprise volume can be deleted by authorized users before their retention periods expire using privileged delete. This retention mode is used to advance an organization's data integrity and internal compliance or to test retention settings before using SnapLock Compliance. For more information, see `SnapLock Enterprise <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-enterprise.html>`_ .
            :param volume_append_mode_enabled: Enables or disables volume-append mode on an FSx for ONTAP SnapLock volume. Volume-append mode allows you to create WORM-appendable files and write data to them incrementally. The default value is ``false`` . For more information, see `Volume-append mode <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/worm-state.html#worm-state-append>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                snaplock_configuration_property = fsx_mixins.CfnVolumePropsMixin.SnaplockConfigurationProperty(
                    audit_log_volume="auditLogVolume",
                    autocommit_period=fsx_mixins.CfnVolumePropsMixin.AutocommitPeriodProperty(
                        type="type",
                        value=123
                    ),
                    privileged_delete="privilegedDelete",
                    retention_period=fsx_mixins.CfnVolumePropsMixin.SnaplockRetentionPeriodProperty(
                        default_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                            type="type",
                            value=123
                        ),
                        maximum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                            type="type",
                            value=123
                        ),
                        minimum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                            type="type",
                            value=123
                        )
                    ),
                    snaplock_type="snaplockType",
                    volume_append_mode_enabled="volumeAppendModeEnabled"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__89a3a1caf26f0497f22aea203bbb1a9056e1232787e61718ae547e25e5434cbd)
                check_type(argname="argument audit_log_volume", value=audit_log_volume, expected_type=type_hints["audit_log_volume"])
                check_type(argname="argument autocommit_period", value=autocommit_period, expected_type=type_hints["autocommit_period"])
                check_type(argname="argument privileged_delete", value=privileged_delete, expected_type=type_hints["privileged_delete"])
                check_type(argname="argument retention_period", value=retention_period, expected_type=type_hints["retention_period"])
                check_type(argname="argument snaplock_type", value=snaplock_type, expected_type=type_hints["snaplock_type"])
                check_type(argname="argument volume_append_mode_enabled", value=volume_append_mode_enabled, expected_type=type_hints["volume_append_mode_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if audit_log_volume is not None:
                self._values["audit_log_volume"] = audit_log_volume
            if autocommit_period is not None:
                self._values["autocommit_period"] = autocommit_period
            if privileged_delete is not None:
                self._values["privileged_delete"] = privileged_delete
            if retention_period is not None:
                self._values["retention_period"] = retention_period
            if snaplock_type is not None:
                self._values["snaplock_type"] = snaplock_type
            if volume_append_mode_enabled is not None:
                self._values["volume_append_mode_enabled"] = volume_append_mode_enabled

        @builtins.property
        def audit_log_volume(self) -> typing.Optional[builtins.str]:
            '''Enables or disables the audit log volume for an FSx for ONTAP SnapLock volume.

            The default value is ``false`` . If you set ``AuditLogVolume`` to ``true`` , the SnapLock volume is created as an audit log volume. The minimum retention period for an audit log volume is six months.

            For more information, see `SnapLock audit log volumes <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/how-snaplock-works.html#snaplock-audit-log-volume>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html#cfn-fsx-volume-snaplockconfiguration-auditlogvolume
            '''
            result = self._values.get("audit_log_volume")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def autocommit_period(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.AutocommitPeriodProperty"]]:
            '''The configuration object for setting the autocommit period of files in an FSx for ONTAP SnapLock volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html#cfn-fsx-volume-snaplockconfiguration-autocommitperiod
            '''
            result = self._values.get("autocommit_period")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.AutocommitPeriodProperty"]], result)

        @builtins.property
        def privileged_delete(self) -> typing.Optional[builtins.str]:
            '''Enables, disables, or permanently disables privileged delete on an FSx for ONTAP SnapLock Enterprise volume.

            Enabling privileged delete allows SnapLock administrators to delete write once, read many (WORM) files even if they have active retention periods. ``PERMANENTLY_DISABLED`` is a terminal state. If privileged delete is permanently disabled on a SnapLock volume, you can't re-enable it. The default value is ``DISABLED`` .

            For more information, see `Privileged delete <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-enterprise.html#privileged-delete>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html#cfn-fsx-volume-snaplockconfiguration-privilegeddelete
            '''
            result = self._values.get("privileged_delete")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def retention_period(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.SnaplockRetentionPeriodProperty"]]:
            '''Specifies the retention period of an FSx for ONTAP SnapLock volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html#cfn-fsx-volume-snaplockconfiguration-retentionperiod
            '''
            result = self._values.get("retention_period")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.SnaplockRetentionPeriodProperty"]], result)

        @builtins.property
        def snaplock_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the retention mode of an FSx for ONTAP SnapLock volume.

            After it is set, it can't be changed. You can choose one of the following retention modes:

            - ``COMPLIANCE`` : Files transitioned to write once, read many (WORM) on a Compliance volume can't be deleted until their retention periods expire. This retention mode is used to address government or industry-specific mandates or to protect against ransomware attacks. For more information, see `SnapLock Compliance <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-compliance.html>`_ .
            - ``ENTERPRISE`` : Files transitioned to WORM on an Enterprise volume can be deleted by authorized users before their retention periods expire using privileged delete. This retention mode is used to advance an organization's data integrity and internal compliance or to test retention settings before using SnapLock Compliance. For more information, see `SnapLock Enterprise <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-enterprise.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html#cfn-fsx-volume-snaplockconfiguration-snaplocktype
            '''
            result = self._values.get("snaplock_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volume_append_mode_enabled(self) -> typing.Optional[builtins.str]:
            '''Enables or disables volume-append mode on an FSx for ONTAP SnapLock volume.

            Volume-append mode allows you to create WORM-appendable files and write data to them incrementally. The default value is ``false`` .

            For more information, see `Volume-append mode <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/worm-state.html#worm-state-append>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockconfiguration.html#cfn-fsx-volume-snaplockconfiguration-volumeappendmodeenabled
            '''
            result = self._values.get("volume_append_mode_enabled")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnaplockConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.SnaplockRetentionPeriodProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_retention": "defaultRetention",
            "maximum_retention": "maximumRetention",
            "minimum_retention": "minimumRetention",
        },
    )
    class SnaplockRetentionPeriodProperty:
        def __init__(
            self,
            *,
            default_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            maximum_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minimum_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnVolumePropsMixin.RetentionPeriodProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration to set the retention period of an FSx for ONTAP SnapLock volume.

            The retention period includes default, maximum, and minimum settings. For more information, see `Working with the retention period in SnapLock <https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/snaplock-retention.html>`_ .

            :param default_retention: The retention period assigned to a write once, read many (WORM) file by default if an explicit retention period is not set for an FSx for ONTAP SnapLock volume. The default retention period must be greater than or equal to the minimum retention period and less than or equal to the maximum retention period.
            :param maximum_retention: The longest retention period that can be assigned to a WORM file on an FSx for ONTAP SnapLock volume.
            :param minimum_retention: The shortest retention period that can be assigned to a WORM file on an FSx for ONTAP SnapLock volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockretentionperiod.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                snaplock_retention_period_property = fsx_mixins.CfnVolumePropsMixin.SnaplockRetentionPeriodProperty(
                    default_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                        type="type",
                        value=123
                    ),
                    maximum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                        type="type",
                        value=123
                    ),
                    minimum_retention=fsx_mixins.CfnVolumePropsMixin.RetentionPeriodProperty(
                        type="type",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aac702fd806a724cbf7367cbd6daa0042bf4d7e92ede255680c4e7e662808ba5)
                check_type(argname="argument default_retention", value=default_retention, expected_type=type_hints["default_retention"])
                check_type(argname="argument maximum_retention", value=maximum_retention, expected_type=type_hints["maximum_retention"])
                check_type(argname="argument minimum_retention", value=minimum_retention, expected_type=type_hints["minimum_retention"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if default_retention is not None:
                self._values["default_retention"] = default_retention
            if maximum_retention is not None:
                self._values["maximum_retention"] = maximum_retention
            if minimum_retention is not None:
                self._values["minimum_retention"] = minimum_retention

        @builtins.property
        def default_retention(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.RetentionPeriodProperty"]]:
            '''The retention period assigned to a write once, read many (WORM) file by default if an explicit retention period is not set for an FSx for ONTAP SnapLock volume.

            The default retention period must be greater than or equal to the minimum retention period and less than or equal to the maximum retention period.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockretentionperiod.html#cfn-fsx-volume-snaplockretentionperiod-defaultretention
            '''
            result = self._values.get("default_retention")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.RetentionPeriodProperty"]], result)

        @builtins.property
        def maximum_retention(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.RetentionPeriodProperty"]]:
            '''The longest retention period that can be assigned to a WORM file on an FSx for ONTAP SnapLock volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockretentionperiod.html#cfn-fsx-volume-snaplockretentionperiod-maximumretention
            '''
            result = self._values.get("maximum_retention")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.RetentionPeriodProperty"]], result)

        @builtins.property
        def minimum_retention(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.RetentionPeriodProperty"]]:
            '''The shortest retention period that can be assigned to a WORM file on an FSx for ONTAP SnapLock volume.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-snaplockretentionperiod.html#cfn-fsx-volume-snaplockretentionperiod-minimumretention
            '''
            result = self._values.get("minimum_retention")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnVolumePropsMixin.RetentionPeriodProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnaplockRetentionPeriodProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.TieringPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"cooling_period": "coolingPeriod", "name": "name"},
    )
    class TieringPolicyProperty:
        def __init__(
            self,
            *,
            cooling_period: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the data tiering policy for an ONTAP volume.

            When enabled, Amazon FSx for ONTAP's intelligent tiering automatically transitions a volume's data between the file system's primary storage and capacity pool storage based on your access patterns.

            Valid tiering policies are the following:

            - ``SNAPSHOT_ONLY`` - (Default value) moves cold snapshots to the capacity pool storage tier.
            - ``AUTO`` - moves cold user data and snapshots to the capacity pool storage tier based on your access patterns.
            - ``ALL`` - moves all user data blocks in both the active file system and Snapshot copies to the storage pool tier.
            - ``NONE`` - keeps a volume's data in the primary storage tier, preventing it from being moved to the capacity pool tier.

            :param cooling_period: Specifies the number of days that user data in a volume must remain inactive before it is considered "cold" and moved to the capacity pool. Used with the ``AUTO`` and ``SNAPSHOT_ONLY`` tiering policies. Enter a whole number between 2 and 183. Default values are 31 days for ``AUTO`` and 2 days for ``SNAPSHOT_ONLY`` .
            :param name: Specifies the tiering policy used to transition data. Default value is ``SNAPSHOT_ONLY`` . - ``SNAPSHOT_ONLY`` - moves cold snapshots to the capacity pool storage tier. - ``AUTO`` - moves cold user data and snapshots to the capacity pool storage tier based on your access patterns. - ``ALL`` - moves all user data blocks in both the active file system and Snapshot copies to the storage pool tier. - ``NONE`` - keeps a volume's data in the primary storage tier, preventing it from being moved to the capacity pool tier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-tieringpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                tiering_policy_property = fsx_mixins.CfnVolumePropsMixin.TieringPolicyProperty(
                    cooling_period=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fbdf29905a358616d5b72da1685461c34e2e3f5985d0e76c1efb36ffdd628b5)
                check_type(argname="argument cooling_period", value=cooling_period, expected_type=type_hints["cooling_period"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cooling_period is not None:
                self._values["cooling_period"] = cooling_period
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def cooling_period(self) -> typing.Optional[jsii.Number]:
            '''Specifies the number of days that user data in a volume must remain inactive before it is considered "cold" and moved to the capacity pool.

            Used with the ``AUTO`` and ``SNAPSHOT_ONLY`` tiering policies. Enter a whole number between 2 and 183. Default values are 31 days for ``AUTO`` and 2 days for ``SNAPSHOT_ONLY`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-tieringpolicy.html#cfn-fsx-volume-tieringpolicy-coolingperiod
            '''
            result = self._values.get("cooling_period")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Specifies the tiering policy used to transition data. Default value is ``SNAPSHOT_ONLY`` .

            - ``SNAPSHOT_ONLY`` - moves cold snapshots to the capacity pool storage tier.
            - ``AUTO`` - moves cold user data and snapshots to the capacity pool storage tier based on your access patterns.
            - ``ALL`` - moves all user data blocks in both the active file system and Snapshot copies to the storage pool tier.
            - ``NONE`` - keeps a volume's data in the primary storage tier, preventing it from being moved to the capacity pool tier.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-tieringpolicy.html#cfn-fsx-volume-tieringpolicy-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TieringPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_fsx.mixins.CfnVolumePropsMixin.UserAndGroupQuotasProperty",
        jsii_struct_bases=[],
        name_mapping={
            "id": "id",
            "storage_capacity_quota_gib": "storageCapacityQuotaGiB",
            "type": "type",
        },
    )
    class UserAndGroupQuotasProperty:
        def __init__(
            self,
            *,
            id: typing.Optional[jsii.Number] = None,
            storage_capacity_quota_gib: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures how much storage users and groups can use on the volume.

            :param id: The ID of the user or group that the quota applies to.
            :param storage_capacity_quota_gib: The user or group's storage quota, in gibibytes (GiB).
            :param type: Specifies whether the quota applies to a user or group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-userandgroupquotas.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_fsx import mixins as fsx_mixins
                
                user_and_group_quotas_property = fsx_mixins.CfnVolumePropsMixin.UserAndGroupQuotasProperty(
                    id=123,
                    storage_capacity_quota_gi_b=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bf00e63d888ff4c02559faf6411a4cad378fec8d82971c8f0b28f74685e23040)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument storage_capacity_quota_gib", value=storage_capacity_quota_gib, expected_type=type_hints["storage_capacity_quota_gib"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if id is not None:
                self._values["id"] = id
            if storage_capacity_quota_gib is not None:
                self._values["storage_capacity_quota_gib"] = storage_capacity_quota_gib
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def id(self) -> typing.Optional[jsii.Number]:
            '''The ID of the user or group that the quota applies to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-userandgroupquotas.html#cfn-fsx-volume-userandgroupquotas-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def storage_capacity_quota_gib(self) -> typing.Optional[jsii.Number]:
            '''The user or group's storage quota, in gibibytes (GiB).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-userandgroupquotas.html#cfn-fsx-volume-userandgroupquotas-storagecapacityquotagib
            '''
            result = self._values.get("storage_capacity_quota_gib")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''Specifies whether the quota applies to a user or group.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fsx-volume-userandgroupquotas.html#cfn-fsx-volume-userandgroupquotas-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UserAndGroupQuotasProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDataRepositoryAssociationMixinProps",
    "CfnDataRepositoryAssociationPropsMixin",
    "CfnFileSystemMixinProps",
    "CfnFileSystemPropsMixin",
    "CfnS3AccessPointAttachmentMixinProps",
    "CfnS3AccessPointAttachmentPropsMixin",
    "CfnSnapshotMixinProps",
    "CfnSnapshotPropsMixin",
    "CfnStorageVirtualMachineMixinProps",
    "CfnStorageVirtualMachinePropsMixin",
    "CfnVolumeMixinProps",
    "CfnVolumePropsMixin",
]

publication.publish()

def _typecheckingstub__f5f18c530cbd9b42943b33b04069285529c5e31fcc7c2077852fec479a76a675(
    *,
    batch_import_meta_data_on_create: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_repository_path: typing.Optional[builtins.str] = None,
    file_system_id: typing.Optional[builtins.str] = None,
    file_system_path: typing.Optional[builtins.str] = None,
    imported_file_chunk_size: typing.Optional[jsii.Number] = None,
    s3: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataRepositoryAssociationPropsMixin.S3Property, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c3d9b62f18422bc87258d8dfb708b123d1af0a51008013b8aa470018d12ec7(
    props: typing.Union[CfnDataRepositoryAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b05785691cc9c9d2d219f29ef18713948044a3ebbd0f2e48f27a23830f4c0e0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c05b79e9665dcbe3f574f204554caebfe19effd751e8107e9b006f229e3bc4c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e3a64c8ddef2fb2a82bec993fe465983d8b420c2fbe2dbed16ef0eb3d6986a(
    *,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70779f052bf7e3b2341abea080853e4ca2398b05e71b7ad22a51e918c15aa0ca(
    *,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69765532a2897097211596c19c2be0b5e490c0c2c5d76964455dc7527d63f91(
    *,
    auto_export_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataRepositoryAssociationPropsMixin.AutoExportPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_import_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataRepositoryAssociationPropsMixin.AutoImportPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3efed9332feac3aac4ec39dd5f1c76f8ca164e1adb99201db1336c9e9edb4e19(
    *,
    backup_id: typing.Optional[builtins.str] = None,
    file_system_type: typing.Optional[builtins.str] = None,
    file_system_type_version: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    lustre_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.LustreConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_type: typing.Optional[builtins.str] = None,
    ontap_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.OntapConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_zfs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.OpenZFSConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_capacity: typing.Optional[jsii.Number] = None,
    storage_type: typing.Optional[builtins.str] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    windows_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.WindowsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4abfb06d1b695291099ea2cd1d7a4ca2ba8bec43056cd408317e947e72738f4(
    props: typing.Union[CfnFileSystemMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c28e79c329ffbd8028e069c7a410455d5ace130792592908d2b877df23e42a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed093cb42d5388372c74ae2fd0af250ac1a539f312cad0072eda10d42f4a9766(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9b3a33aa892a21210df0361c175fb3249662bb3e1e2671ce6f885c04d01b0c(
    *,
    audit_log_destination: typing.Optional[builtins.str] = None,
    file_access_audit_log_level: typing.Optional[builtins.str] = None,
    file_share_access_audit_log_level: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ea3e0235b0c5fd28fd74bedcefac302f669a038d9a91957bbfbeeaea8ca4d5d(
    *,
    clients: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b1aefdcecdc9b4434caa6370423269f48024d2e1ec72829e40f74f89bbe5fe(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
    sizing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101dc77495758d81f187868cd51d71e5e158eba7db4b41849fb3980a98857d06(
    *,
    iops: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b15289775c621967ea6402d7269d30696f4605f917cde995b3806e581b143c(
    *,
    auto_import_policy: typing.Optional[builtins.str] = None,
    automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
    copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
    data_compression_type: typing.Optional[builtins.str] = None,
    data_read_cache_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.DataReadCacheConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    drive_cache_type: typing.Optional[builtins.str] = None,
    efa_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    export_path: typing.Optional[builtins.str] = None,
    imported_file_chunk_size: typing.Optional[jsii.Number] = None,
    import_path: typing.Optional[builtins.str] = None,
    metadata_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.MetadataConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    per_unit_storage_throughput: typing.Optional[jsii.Number] = None,
    throughput_capacity: typing.Optional[jsii.Number] = None,
    weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680b70587eb455466c32dbe775008c13c3b3f57bcd86768478c33065a3250212(
    *,
    iops: typing.Optional[jsii.Number] = None,
    mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17e89ee5c3cf47dcf9d2b96d985346a26d3215fc4e0fc706957d847afe96f35c(
    *,
    client_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.ClientConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5af92418f9f6da37b979cac247cb98340e798d0fed5f53fadcc6cb8f86322d3c(
    *,
    automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
    daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    disk_iops_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.DiskIopsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_ip_address_range: typing.Optional[builtins.str] = None,
    endpoint_ipv6_address_range: typing.Optional[builtins.str] = None,
    fsx_admin_password: typing.Optional[builtins.str] = None,
    ha_pairs: typing.Optional[jsii.Number] = None,
    preferred_subnet_id: typing.Optional[builtins.str] = None,
    route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    throughput_capacity: typing.Optional[jsii.Number] = None,
    throughput_capacity_per_ha_pair: typing.Optional[jsii.Number] = None,
    weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5aee60985a3df3ba05cd1e4aae6945bdd924febd7257044e6628d346e19a4f90(
    *,
    automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
    copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    copy_tags_to_volumes: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    disk_iops_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.DiskIopsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    endpoint_ip_address_range: typing.Optional[builtins.str] = None,
    endpoint_ipv6_address_range: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    preferred_subnet_id: typing.Optional[builtins.str] = None,
    read_cache_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.ReadCacheConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    root_volume_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.RootVolumeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    route_table_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    throughput_capacity: typing.Optional[jsii.Number] = None,
    weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be91c926f4224f66fcb95ff8aec78a15829c35271a0e239329a27306a5fce7cc(
    *,
    size_gib: typing.Optional[jsii.Number] = None,
    sizing_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6bb9b98d7f59a7beec27dd797dcc2758f8db38184718fded8196d2041c828f8(
    *,
    copy_tags_to_snapshots: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_compression_type: typing.Optional[builtins.str] = None,
    nfs_exports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.NfsExportsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    record_size_kib: typing.Optional[jsii.Number] = None,
    user_and_group_quotas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.UserAndGroupQuotasProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a431fd3da7f901199953df4d04d7d0c1ec8b7959b1119805dd3492755d043e0(
    *,
    dns_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_join_service_account_secret: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    file_system_administrators_group: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4796f4fdd0fcf5cf432d0c7c7a16852b381dd5e7aaf7a12ec78da49434aec2(
    *,
    id: typing.Optional[jsii.Number] = None,
    storage_capacity_quota_gib: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5e3c502b53ea552f6e56fbf9e348714477656e055126fc4cad7fd35fa94d23b(
    *,
    active_directory_id: typing.Optional[builtins.str] = None,
    aliases: typing.Optional[typing.Sequence[builtins.str]] = None,
    audit_log_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.AuditLogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    automatic_backup_retention_days: typing.Optional[jsii.Number] = None,
    copy_tags_to_backups: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    daily_automatic_backup_start_time: typing.Optional[builtins.str] = None,
    deployment_type: typing.Optional[builtins.str] = None,
    disk_iops_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.DiskIopsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    preferred_subnet_id: typing.Optional[builtins.str] = None,
    self_managed_active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnFileSystemPropsMixin.SelfManagedActiveDirectoryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    throughput_capacity: typing.Optional[jsii.Number] = None,
    weekly_maintenance_start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e65d50c2b3aa1ecf41a8ad38c6395142b63033809f54900b51f04c068378a549(
    *,
    name: typing.Optional[builtins.str] = None,
    ontap_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOntapConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_zfs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.S3AccessPointOpenZFSConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_access_point: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.S3AccessPointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bb79e178c14bcf273fe1c6eeb57fc7c268bcfe79d2a43b69411d22f08a930e(
    props: typing.Union[CfnS3AccessPointAttachmentMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eadcc9a424bc9fd7ae36dc6fbdaa80e4537fb24995ce5108784401053c2052f2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df074990cc2acb3c250290d63e586efa532f12d9a47a611f1ff05b156536a5f8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65fcf240e099c8b4021a0a0ec51b6569aef70e1b9926ac95ac74110c510835bb(
    *,
    gid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef2e643dccafc05f8cfce072f06962cdcb10f4a3279b1de596e80a042bb2882(
    *,
    type: typing.Optional[builtins.str] = None,
    unix_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.OntapUnixFileSystemUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    windows_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.OntapWindowsFileSystemUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0e9a2bfcd18108398d07bf96555de16c5fcc5616476be587f10f68aaa33e2c(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b22c2ece8e85799b2b230c4c73466844e914d64f0725dc11fbac5e2d8f1dcdb(
    *,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc7f7d6e076581ab7b80568879c798170875d65c551a32d755465ed8dabfb9ac(
    *,
    posix_user: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.OpenZFSPosixFileSystemUserProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49a831c9a1bbfcea096c1ba6cce9c0d361dc86092ea2d1d5f081fc6f0d276432(
    *,
    gid: typing.Optional[jsii.Number] = None,
    secondary_gids: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.FileSystemGIDProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    uid: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c735dd71e905f682434ec590b18b0aeff0a3e1e6b0055421a8180af87dfc30(
    *,
    file_system_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.OntapFileSystemIdentityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__229fd8bc32cc5ce3f8efd3a8a9e28710082d5e6f4dfef89a1ac7844087c9404b(
    *,
    file_system_identity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.OpenZFSFileSystemIdentityProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a76fb14c8da3ec3987ec6d34d6915ba3f7108b390d96988ee6a580885bd19f1(
    *,
    alias: typing.Optional[builtins.str] = None,
    policy: typing.Any = None,
    resource_arn: typing.Optional[builtins.str] = None,
    vpc_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnS3AccessPointAttachmentPropsMixin.S3AccessPointVpcConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9aef700c8291216aa16e4133addb9c6d47809873813dac65638009cf024fb78(
    *,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8084cbbcad737f43724c08cec4be58008bfa452d88d3b6e1913b404478f3cab4(
    *,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3218db377f425947883de134759aa43e12e1ad7d3ab3d941cb9dc733059cebb2(
    props: typing.Union[CfnSnapshotMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f91c788faa245c0a1b561d53700e104b3c0dc40844f4fe6afee83c74fb975c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5070c97d1a7a8daebdf726786101bd42ce76cf55c8e6e5d3534e67dc9516bb14(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c1e89cd228a1eca651dbaa50e9d9f86b129ee22f5cca0042629f3bc4e1f487(
    *,
    active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageVirtualMachinePropsMixin.ActiveDirectoryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    file_system_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    root_volume_security_style: typing.Optional[builtins.str] = None,
    svm_admin_password: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58a67c52f725c575566eea8d232b7c0ea5be5fc8b88e778bcf7be8e64794bfe(
    props: typing.Union[CfnStorageVirtualMachineMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab324ec45035258f3b28454c4f3c1c12ef1f54e4e653e577fd8c76ad7c00976c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc041e92ed4f0e4c6cf0b1743002852e4234291b8ea5ae40064b748538880ea(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bd25593f8e2af906627ac77fa4c28d28df4926648d9c7bfce6332711684496(
    *,
    net_bios_name: typing.Optional[builtins.str] = None,
    self_managed_active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnStorageVirtualMachinePropsMixin.SelfManagedActiveDirectoryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5478ffee83e1e029f8efffb0eb39e13e4c7154d18dbe1a7c37f131d29e7b9703(
    *,
    dns_ips: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_join_service_account_secret: typing.Optional[builtins.str] = None,
    domain_name: typing.Optional[builtins.str] = None,
    file_system_administrators_group: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
    password: typing.Optional[builtins.str] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa3af22a095953a4f4a77f8eec786177e5a52ae7f3465f7f6d6be681e93e21a6(
    *,
    backup_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    ontap_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.OntapConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    open_zfs_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.OpenZFSConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1441d3c30bc76399e1de4d38c0a3b94856bc318c32cfcb6fb6dcd522a6f615c(
    props: typing.Union[CfnVolumeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc4c2d78ed2a80ce5410b770c949661d79c7303a50ca076c62d3f67eb89fec79(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80227bf44aea35f2e21c641e30d22dfe8c76f325ef2d594d676605377aa21a8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b9569343faa6529cb7865d1ee6c9d94f27c2a6c7a5d99c28ea64e627df4586c(
    *,
    aggregates: typing.Optional[typing.Sequence[builtins.str]] = None,
    constituents_per_aggregate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2880563386b390e0fc2a634c4916ca282708041929f0df7a84538239ab9d60(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b237336a5bd92dd5e2a97d6fac640b3995f82efdd9a151751d0659a4eab85cd9(
    *,
    clients: typing.Optional[builtins.str] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4fe0a5e8c445fc1f2906c8db4fd59b991118137d35582825fed7e2c6b8f0952(
    *,
    client_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.ClientConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a54363825eaab112754a5d0edd4ff8b6fcfab199b029a378b9a11f4f97c02a8(
    *,
    aggregate_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.AggregateConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    copy_tags_to_backups: typing.Optional[builtins.str] = None,
    junction_path: typing.Optional[builtins.str] = None,
    ontap_volume_type: typing.Optional[builtins.str] = None,
    security_style: typing.Optional[builtins.str] = None,
    size_in_bytes: typing.Optional[builtins.str] = None,
    size_in_megabytes: typing.Optional[builtins.str] = None,
    snaplock_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.SnaplockConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snapshot_policy: typing.Optional[builtins.str] = None,
    storage_efficiency_enabled: typing.Optional[builtins.str] = None,
    storage_virtual_machine_id: typing.Optional[builtins.str] = None,
    tiering_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.TieringPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_style: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9cfce26d9c35376308f78d8f2124aa3b3113662de0490fa4cf4ffa0691c2a61(
    *,
    copy_tags_to_snapshots: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    data_compression_type: typing.Optional[builtins.str] = None,
    nfs_exports: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.NfsExportsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    options: typing.Optional[typing.Sequence[builtins.str]] = None,
    origin_snapshot: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.OriginSnapshotProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parent_volume_id: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    record_size_kib: typing.Optional[jsii.Number] = None,
    storage_capacity_quota_gib: typing.Optional[jsii.Number] = None,
    storage_capacity_reservation_gib: typing.Optional[jsii.Number] = None,
    user_and_group_quotas: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.UserAndGroupQuotasProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e750a6ba8313d0f0ecc78740e99917fba7728ebcc63e4017da59a2fb05a45e(
    *,
    copy_strategy: typing.Optional[builtins.str] = None,
    snapshot_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f91c515aec5d01625bfb0c8854e00b181bc6d8db4ce337f934be52adb5b9542(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a3a1caf26f0497f22aea203bbb1a9056e1232787e61718ae547e25e5434cbd(
    *,
    audit_log_volume: typing.Optional[builtins.str] = None,
    autocommit_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.AutocommitPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    privileged_delete: typing.Optional[builtins.str] = None,
    retention_period: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.SnaplockRetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    snaplock_type: typing.Optional[builtins.str] = None,
    volume_append_mode_enabled: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aac702fd806a724cbf7367cbd6daa0042bf4d7e92ede255680c4e7e662808ba5(
    *,
    default_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    maximum_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_retention: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnVolumePropsMixin.RetentionPeriodProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbdf29905a358616d5b72da1685461c34e2e3f5985d0e76c1efb36ffdd628b5(
    *,
    cooling_period: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf00e63d888ff4c02559faf6411a4cad378fec8d82971c8f0b28f74685e23040(
    *,
    id: typing.Optional[jsii.Number] = None,
    storage_capacity_quota_gib: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
