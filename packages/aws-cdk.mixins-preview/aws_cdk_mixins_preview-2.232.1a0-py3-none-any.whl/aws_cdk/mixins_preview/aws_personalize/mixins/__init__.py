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
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnDatasetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain": "domain",
        "kms_key_arn": "kmsKeyArn",
        "name": "name",
        "role_arn": "roleArn",
    },
)
class CfnDatasetGroupMixinProps:
    def __init__(
        self,
        *,
        domain: typing.Optional[builtins.str] = None,
        kms_key_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDatasetGroupPropsMixin.

        :param domain: The domain of a Domain dataset group.
        :param kms_key_arn: The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key used to encrypt the datasets.
        :param name: The name of the dataset group.
        :param role_arn: The ARN of the AWS Identity and Access Management (IAM) role that has permissions to access the AWS Key Management Service (KMS) key. Supplying an IAM role is only valid when also specifying a KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
            
            cfn_dataset_group_mixin_props = personalize_mixins.CfnDatasetGroupMixinProps(
                domain="domain",
                kms_key_arn="kmsKeyArn",
                name="name",
                role_arn="roleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5a28907a1567d8a2161fbc98024577cb269a3a2fa61bd622e89ae4df90db26)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of a Domain dataset group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the AWS Key Management Service (KMS) key used to encrypt the datasets.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the dataset group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the AWS Identity and Access Management (IAM) role that has permissions to access the AWS Key Management Service (KMS) key.

        Supplying an IAM role is only valid when also specifying a KMS key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html#cfn-personalize-datasetgroup-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetGroupMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatasetGroupPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnDatasetGroupPropsMixin",
):
    '''A dataset group is a collection of related datasets (Item interactions, Users, Items, Actions, Action interactions).

    You create a dataset group by calling `CreateDatasetGroup <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetGroup.html>`_ . You then create a dataset and add it to a dataset group by calling `CreateDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDataset.html>`_ . The dataset group is used to create and train a solution by calling `CreateSolution <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateSolution.html>`_ . A dataset group can contain only one of each type of dataset.

    You can specify an AWS Key Management Service (KMS) key to encrypt the datasets in the group.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-datasetgroup.html
    :cloudformationResource: AWS::Personalize::DatasetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
        
        cfn_dataset_group_props_mixin = personalize_mixins.CfnDatasetGroupPropsMixin(personalize_mixins.CfnDatasetGroupMixinProps(
            domain="domain",
            kms_key_arn="kmsKeyArn",
            name="name",
            role_arn="roleArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDatasetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Personalize::DatasetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__041e1657cda32f819dcdbd4145cc55d07b6b62b2ab29805d4771aa9d5366dd1b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80cffbb1f4b2eb364f29580291952b29167969a18f4b204f9f413113e3df9cde)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959cb0349adfda8311e1e66a24d7111ab641e624efaebf3cef98dd5dbe33a70c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatasetGroupMixinProps:
        return typing.cast(CfnDatasetGroupMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnDatasetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_group_arn": "datasetGroupArn",
        "dataset_import_job": "datasetImportJob",
        "dataset_type": "datasetType",
        "name": "name",
        "schema_arn": "schemaArn",
    },
)
class CfnDatasetMixinProps:
    def __init__(
        self,
        *,
        dataset_group_arn: typing.Optional[builtins.str] = None,
        dataset_import_job: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatasetImportJobProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dataset_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schema_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDatasetPropsMixin.

        :param dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group.
        :param dataset_import_job: Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset. If you specify a dataset import job as part of a dataset, all dataset import job fields are required.
        :param dataset_type: One of the following values:. - Interactions - Items - Users .. epigraph:: You can't use CloudFormation to create an Action Interactions or Actions dataset.
        :param name: The name of the dataset.
        :param schema_arn: The ARN of the associated schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
            
            # data_source: Any
            
            cfn_dataset_mixin_props = personalize_mixins.CfnDatasetMixinProps(
                dataset_group_arn="datasetGroupArn",
                dataset_import_job=personalize_mixins.CfnDatasetPropsMixin.DatasetImportJobProperty(
                    dataset_arn="datasetArn",
                    dataset_import_job_arn="datasetImportJobArn",
                    data_source=data_source,
                    job_name="jobName",
                    role_arn="roleArn"
                ),
                dataset_type="datasetType",
                name="name",
                schema_arn="schemaArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10951eca9b0a1000032fce4977464821f9f44c33051f746adf65d1401d9adf0)
            check_type(argname="argument dataset_group_arn", value=dataset_group_arn, expected_type=type_hints["dataset_group_arn"])
            check_type(argname="argument dataset_import_job", value=dataset_import_job, expected_type=type_hints["dataset_import_job"])
            check_type(argname="argument dataset_type", value=dataset_type, expected_type=type_hints["dataset_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema_arn", value=schema_arn, expected_type=type_hints["schema_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_group_arn is not None:
            self._values["dataset_group_arn"] = dataset_group_arn
        if dataset_import_job is not None:
            self._values["dataset_import_job"] = dataset_import_job
        if dataset_type is not None:
            self._values["dataset_type"] = dataset_type
        if name is not None:
            self._values["name"] = name
        if schema_arn is not None:
            self._values["schema_arn"] = schema_arn

    @builtins.property
    def dataset_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the dataset group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasetgrouparn
        '''
        result = self._values.get("dataset_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataset_import_job(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetImportJobProperty"]]:
        '''Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.

        If you specify a dataset import job as part of a dataset, all dataset import job fields are required.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasetimportjob
        '''
        result = self._values.get("dataset_import_job")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetImportJobProperty"]], result)

    @builtins.property
    def dataset_type(self) -> typing.Optional[builtins.str]:
        '''One of the following values:.

        - Interactions
        - Items
        - Users

        .. epigraph::

           You can't use CloudFormation to create an Action Interactions or Actions dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-datasettype
        '''
        result = self._values.get("dataset_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the associated schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html#cfn-personalize-dataset-schemaarn
        '''
        result = self._values.get("schema_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDatasetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDatasetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnDatasetPropsMixin",
):
    '''Creates an empty dataset and adds it to the specified dataset group.

    Use `CreateDatasetImportJob <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetImportJob.html>`_ to import your training data to a dataset.

    There are 5 types of datasets:

    - Item interactions
    - Items
    - Users
    - Action interactions (you can't use CloudFormation to create an Action interactions dataset)
    - Actions (you can't use CloudFormation to create an Actions dataset)

    Each dataset type has an associated schema with required field types. Only the ``Item interactions`` dataset is required in order to train a model (also referred to as creating a solution).

    A dataset can be in one of the following states:

    - CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED
    - DELETE PENDING > DELETE IN_PROGRESS

    To get the status of the dataset, call `DescribeDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_DescribeDataset.html>`_ .

    **Related APIs** - `CreateDatasetGroup <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDatasetGroup.html>`_

    - `ListDatasets <https://docs.aws.amazon.com/personalize/latest/dg/API_ListDatasets.html>`_
    - `DescribeDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_DescribeDataset.html>`_
    - `DeleteDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_DeleteDataset.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-dataset.html
    :cloudformationResource: AWS::Personalize::Dataset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
        
        # data_source: Any
        
        cfn_dataset_props_mixin = personalize_mixins.CfnDatasetPropsMixin(personalize_mixins.CfnDatasetMixinProps(
            dataset_group_arn="datasetGroupArn",
            dataset_import_job=personalize_mixins.CfnDatasetPropsMixin.DatasetImportJobProperty(
                dataset_arn="datasetArn",
                dataset_import_job_arn="datasetImportJobArn",
                data_source=data_source,
                job_name="jobName",
                role_arn="roleArn"
            ),
            dataset_type="datasetType",
            name="name",
            schema_arn="schemaArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Personalize::Dataset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__180e395c48585977798952900f666c9649bd8ed4ddcbf35fbb820e4359582eed)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb2af26cd6f980d8c14d479184f3c85d0168e53c75a12d6627528f5a2e39590f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af4ff66d592fa2c0f63666a513ba084e9a2135a9e3c6a3f197d59a27f4d35a68)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDatasetMixinProps:
        return typing.cast(CfnDatasetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnDatasetPropsMixin.DatasetImportJobProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dataset_arn": "datasetArn",
            "dataset_import_job_arn": "datasetImportJobArn",
            "data_source": "dataSource",
            "job_name": "jobName",
            "role_arn": "roleArn",
        },
    )
    class DatasetImportJobProperty:
        def __init__(
            self,
            *,
            dataset_arn: typing.Optional[builtins.str] = None,
            dataset_import_job_arn: typing.Optional[builtins.str] = None,
            data_source: typing.Any = None,
            job_name: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a job that imports training data from a data source (Amazon S3 bucket) to an Amazon Personalize dataset.

            A dataset import job can be in one of the following states:

            - CREATE PENDING > CREATE IN_PROGRESS > ACTIVE -or- CREATE FAILED

            If you specify a dataset import job as part of a dataset, all dataset import job fields are required.

            :param dataset_arn: The Amazon Resource Name (ARN) of the dataset that receives the imported data.
            :param dataset_import_job_arn: The ARN of the dataset import job.
            :param data_source: The Amazon S3 bucket that contains the training data to import.
            :param job_name: The name of the import job.
            :param role_arn: The ARN of the IAM role that has permissions to read from the Amazon S3 data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
                
                # data_source: Any
                
                dataset_import_job_property = personalize_mixins.CfnDatasetPropsMixin.DatasetImportJobProperty(
                    dataset_arn="datasetArn",
                    dataset_import_job_arn="datasetImportJobArn",
                    data_source=data_source,
                    job_name="jobName",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53334e86868422e342e3046b78ac54cbd5759e2a4577be124a5e9829eca638de)
                check_type(argname="argument dataset_arn", value=dataset_arn, expected_type=type_hints["dataset_arn"])
                check_type(argname="argument dataset_import_job_arn", value=dataset_import_job_arn, expected_type=type_hints["dataset_import_job_arn"])
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataset_arn is not None:
                self._values["dataset_arn"] = dataset_arn
            if dataset_import_job_arn is not None:
                self._values["dataset_import_job_arn"] = dataset_import_job_arn
            if data_source is not None:
                self._values["data_source"] = data_source
            if job_name is not None:
                self._values["job_name"] = job_name
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def dataset_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the dataset that receives the imported data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-datasetarn
            '''
            result = self._values.get("dataset_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dataset_import_job_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the dataset import job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-datasetimportjobarn
            '''
            result = self._values.get("dataset_import_job_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def data_source(self) -> typing.Any:
            '''The Amazon S3 bucket that contains the training data to import.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Any, result)

        @builtins.property
        def job_name(self) -> typing.Optional[builtins.str]:
            '''The name of the import job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-jobname
            '''
            result = self._values.get("job_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that has permissions to read from the Amazon S3 data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-dataset-datasetimportjob.html#cfn-personalize-dataset-datasetimportjob-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetImportJobProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnSchemaMixinProps",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "name": "name", "schema": "schema"},
)
class CfnSchemaMixinProps:
    def __init__(
        self,
        *,
        domain: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        schema: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnSchemaPropsMixin.

        :param domain: The domain of a schema that you created for a dataset in a Domain dataset group.
        :param name: The name of the schema.
        :param schema: The schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
            
            cfn_schema_mixin_props = personalize_mixins.CfnSchemaMixinProps(
                domain="domain",
                name="name",
                schema="schema"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e959cbd6a60bcd172af1e715187e136108fdae2d27a7b1c7953ad5a43e1d791)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if name is not None:
            self._values["name"] = name
        if schema is not None:
            self._values["schema"] = schema

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain of a schema that you created for a dataset in a Domain dataset group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''The schema.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html#cfn-personalize-schema-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchemaMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchemaPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnSchemaPropsMixin",
):
    '''Creates an Amazon Personalize schema from the specified schema string.

    The schema you create must be in Avro JSON format.

    Amazon Personalize recognizes three schema variants. Each schema is associated with a dataset type and has a set of required field and keywords. If you are creating a schema for a dataset in a Domain dataset group, you provide the domain of the Domain dataset group. You specify a schema when you call `CreateDataset <https://docs.aws.amazon.com/personalize/latest/dg/API_CreateDataset.html>`_ .

    For more information on schemas, see `Datasets and schemas <https://docs.aws.amazon.com/personalize/latest/dg/how-it-works-dataset-schema.html>`_ .

    **Related APIs** - `ListSchemas <https://docs.aws.amazon.com/personalize/latest/dg/API_ListSchemas.html>`_

    - `DescribeSchema <https://docs.aws.amazon.com/personalize/latest/dg/API_DescribeSchema.html>`_
    - `DeleteSchema <https://docs.aws.amazon.com/personalize/latest/dg/API_DeleteSchema.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-schema.html
    :cloudformationResource: AWS::Personalize::Schema
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
        
        cfn_schema_props_mixin = personalize_mixins.CfnSchemaPropsMixin(personalize_mixins.CfnSchemaMixinProps(
            domain="domain",
            name="name",
            schema="schema"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Personalize::Schema``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed1e0a0489e79057bf2056ab72452d7b08366a1d369a336b269b03296096a050)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1814ada5d90bd59b53533fccd93d676717b38798b6d14626bc8b27d5d11dac0e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf5e6472053deca8d044ed765991729db7fe4d53acaba39bc71637cfcdc81af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSchemaMixinProps:
        return typing.cast(CfnSchemaMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnSolutionMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_group_arn": "datasetGroupArn",
        "event_type": "eventType",
        "name": "name",
        "perform_auto_ml": "performAutoMl",
        "perform_hpo": "performHpo",
        "recipe_arn": "recipeArn",
        "solution_config": "solutionConfig",
    },
)
class CfnSolutionMixinProps:
    def __init__(
        self,
        *,
        dataset_group_arn: typing.Optional[builtins.str] = None,
        event_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        perform_auto_ml: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        perform_hpo: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        recipe_arn: typing.Optional[builtins.str] = None,
        solution_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnSolutionPropsMixin.SolutionConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSolutionPropsMixin.

        :param dataset_group_arn: The Amazon Resource Name (ARN) of the dataset group that provides the training data.
        :param event_type: The event type (for example, 'click' or 'like') that is used for training the model. If no ``eventType`` is provided, Amazon Personalize uses all interactions for training with equal weight regardless of type.
        :param name: The name of the solution.
        :param perform_auto_ml: .. epigraph:: We don't recommend enabling automated machine learning. Instead, match your use case to the available Amazon Personalize recipes. For more information, see `Determining your use case. <https://docs.aws.amazon.com/personalize/latest/dg/determining-use-case.html>`_ When true, Amazon Personalize performs a search for the best USER_PERSONALIZATION recipe from the list specified in the solution configuration ( ``recipeArn`` must not be specified). When false (the default), Amazon Personalize uses ``recipeArn`` for training.
        :param perform_hpo: Whether to perform hyperparameter optimization (HPO) on the chosen recipe. The default is ``false`` .
        :param recipe_arn: The ARN of the recipe used to create the solution. This is required when ``performAutoML`` is false.
        :param solution_config: Describes the configuration properties for the solution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
            
            # auto_ml_config: Any
            # hpo_config: Any
            
            cfn_solution_mixin_props = personalize_mixins.CfnSolutionMixinProps(
                dataset_group_arn="datasetGroupArn",
                event_type="eventType",
                name="name",
                perform_auto_ml=False,
                perform_hpo=False,
                recipe_arn="recipeArn",
                solution_config=personalize_mixins.CfnSolutionPropsMixin.SolutionConfigProperty(
                    algorithm_hyper_parameters={
                        "algorithm_hyper_parameters_key": "algorithmHyperParameters"
                    },
                    auto_ml_config=auto_ml_config,
                    event_value_threshold="eventValueThreshold",
                    feature_transformation_parameters={
                        "feature_transformation_parameters_key": "featureTransformationParameters"
                    },
                    hpo_config=hpo_config
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0700eeae4eecd1f53ff6df4cd468d13531cdd8e6fa70c0bc528b8cf904b8bc05)
            check_type(argname="argument dataset_group_arn", value=dataset_group_arn, expected_type=type_hints["dataset_group_arn"])
            check_type(argname="argument event_type", value=event_type, expected_type=type_hints["event_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument perform_auto_ml", value=perform_auto_ml, expected_type=type_hints["perform_auto_ml"])
            check_type(argname="argument perform_hpo", value=perform_hpo, expected_type=type_hints["perform_hpo"])
            check_type(argname="argument recipe_arn", value=recipe_arn, expected_type=type_hints["recipe_arn"])
            check_type(argname="argument solution_config", value=solution_config, expected_type=type_hints["solution_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_group_arn is not None:
            self._values["dataset_group_arn"] = dataset_group_arn
        if event_type is not None:
            self._values["event_type"] = event_type
        if name is not None:
            self._values["name"] = name
        if perform_auto_ml is not None:
            self._values["perform_auto_ml"] = perform_auto_ml
        if perform_hpo is not None:
            self._values["perform_hpo"] = perform_hpo
        if recipe_arn is not None:
            self._values["recipe_arn"] = recipe_arn
        if solution_config is not None:
            self._values["solution_config"] = solution_config

    @builtins.property
    def dataset_group_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the dataset group that provides the training data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-datasetgrouparn
        '''
        result = self._values.get("dataset_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_type(self) -> typing.Optional[builtins.str]:
        '''The event type (for example, 'click' or 'like') that is used for training the model.

        If no ``eventType`` is provided, Amazon Personalize uses all interactions for training with equal weight regardless of type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-eventtype
        '''
        result = self._values.get("event_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the solution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def perform_auto_ml(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''.. epigraph::

   We don't recommend enabling automated machine learning.

        Instead, match your use case to the available Amazon Personalize recipes. For more information, see `Determining your use case. <https://docs.aws.amazon.com/personalize/latest/dg/determining-use-case.html>`_

        When true, Amazon Personalize performs a search for the best USER_PERSONALIZATION recipe from the list specified in the solution configuration ( ``recipeArn`` must not be specified). When false (the default), Amazon Personalize uses ``recipeArn`` for training.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-performautoml
        '''
        result = self._values.get("perform_auto_ml")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def perform_hpo(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to perform hyperparameter optimization (HPO) on the chosen recipe.

        The default is ``false`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-performhpo
        '''
        result = self._values.get("perform_hpo")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def recipe_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the recipe used to create the solution.

        This is required when ``performAutoML`` is false.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-recipearn
        '''
        result = self._values.get("recipe_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def solution_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSolutionPropsMixin.SolutionConfigProperty"]]:
        '''Describes the configuration properties for the solution.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html#cfn-personalize-solution-solutionconfig
        '''
        result = self._values.get("solution_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnSolutionPropsMixin.SolutionConfigProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSolutionMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSolutionPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnSolutionPropsMixin",
):
    '''.. epigraph::

   By default, all new solutions use automatic training.

    With automatic training, you incur training costs while your solution is active. To avoid unnecessary costs, when you are finished you can `update the solution <https://docs.aws.amazon.com/personalize/latest/dg/API_UpdateSolution.html>`_ to turn off automatic training. For information about training costs, see `Amazon Personalize pricing <https://docs.aws.amazon.com/https://aws.amazon.com/personalize/pricing/>`_ .

    An object that provides information about a solution. A solution includes the custom recipe, customized parameters, and trained models (Solution Versions) that Amazon Personalize uses to generate recommendations.

    After you create a solution, you can’t change its configuration. If you need to make changes, you can `clone the solution <https://docs.aws.amazon.com/personalize/latest/dg/cloning-solution.html>`_ with the Amazon Personalize console or create a new one.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-personalize-solution.html
    :cloudformationResource: AWS::Personalize::Solution
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
        
        # auto_ml_config: Any
        # hpo_config: Any
        
        cfn_solution_props_mixin = personalize_mixins.CfnSolutionPropsMixin(personalize_mixins.CfnSolutionMixinProps(
            dataset_group_arn="datasetGroupArn",
            event_type="eventType",
            name="name",
            perform_auto_ml=False,
            perform_hpo=False,
            recipe_arn="recipeArn",
            solution_config=personalize_mixins.CfnSolutionPropsMixin.SolutionConfigProperty(
                algorithm_hyper_parameters={
                    "algorithm_hyper_parameters_key": "algorithmHyperParameters"
                },
                auto_ml_config=auto_ml_config,
                event_value_threshold="eventValueThreshold",
                feature_transformation_parameters={
                    "feature_transformation_parameters_key": "featureTransformationParameters"
                },
                hpo_config=hpo_config
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnSolutionMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Personalize::Solution``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98722fcb608fba4e7d8bfe6fb8c08464cc860152070f4e5ef1aaf5c5f603dbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f565d161970ecc2c7855644afc5ebbfe0df841537f9f10d74990b705bbebe4a9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da58371729dad2485b7fc3027f2a9e0b70e3ebc7f48ec3c4653b15d349023d62)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnSolutionMixinProps:
        return typing.cast(CfnSolutionMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_personalize.mixins.CfnSolutionPropsMixin.SolutionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm_hyper_parameters": "algorithmHyperParameters",
            "auto_ml_config": "autoMlConfig",
            "event_value_threshold": "eventValueThreshold",
            "feature_transformation_parameters": "featureTransformationParameters",
            "hpo_config": "hpoConfig",
        },
    )
    class SolutionConfigProperty:
        def __init__(
            self,
            *,
            algorithm_hyper_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            auto_ml_config: typing.Any = None,
            event_value_threshold: typing.Optional[builtins.str] = None,
            feature_transformation_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            hpo_config: typing.Any = None,
        ) -> None:
            '''Describes the configuration properties for the solution.

            :param algorithm_hyper_parameters: Lists the algorithm hyperparameters and their values.
            :param auto_ml_config: The `AutoMLConfig <https://docs.aws.amazon.com/personalize/latest/dg/API_AutoMLConfig.html>`_ object containing a list of recipes to search when AutoML is performed.
            :param event_value_threshold: Only events with a value greater than or equal to this threshold are used for training a model.
            :param feature_transformation_parameters: Lists the feature transformation parameters.
            :param hpo_config: Describes the properties for hyperparameter optimization (HPO).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_personalize import mixins as personalize_mixins
                
                # auto_ml_config: Any
                # hpo_config: Any
                
                solution_config_property = personalize_mixins.CfnSolutionPropsMixin.SolutionConfigProperty(
                    algorithm_hyper_parameters={
                        "algorithm_hyper_parameters_key": "algorithmHyperParameters"
                    },
                    auto_ml_config=auto_ml_config,
                    event_value_threshold="eventValueThreshold",
                    feature_transformation_parameters={
                        "feature_transformation_parameters_key": "featureTransformationParameters"
                    },
                    hpo_config=hpo_config
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__556c5fc4a5be423564f115ba06db28066aea3711b85c3af8d2d452ee0f01b412)
                check_type(argname="argument algorithm_hyper_parameters", value=algorithm_hyper_parameters, expected_type=type_hints["algorithm_hyper_parameters"])
                check_type(argname="argument auto_ml_config", value=auto_ml_config, expected_type=type_hints["auto_ml_config"])
                check_type(argname="argument event_value_threshold", value=event_value_threshold, expected_type=type_hints["event_value_threshold"])
                check_type(argname="argument feature_transformation_parameters", value=feature_transformation_parameters, expected_type=type_hints["feature_transformation_parameters"])
                check_type(argname="argument hpo_config", value=hpo_config, expected_type=type_hints["hpo_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if algorithm_hyper_parameters is not None:
                self._values["algorithm_hyper_parameters"] = algorithm_hyper_parameters
            if auto_ml_config is not None:
                self._values["auto_ml_config"] = auto_ml_config
            if event_value_threshold is not None:
                self._values["event_value_threshold"] = event_value_threshold
            if feature_transformation_parameters is not None:
                self._values["feature_transformation_parameters"] = feature_transformation_parameters
            if hpo_config is not None:
                self._values["hpo_config"] = hpo_config

        @builtins.property
        def algorithm_hyper_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Lists the algorithm hyperparameters and their values.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-algorithmhyperparameters
            '''
            result = self._values.get("algorithm_hyper_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def auto_ml_config(self) -> typing.Any:
            '''The `AutoMLConfig <https://docs.aws.amazon.com/personalize/latest/dg/API_AutoMLConfig.html>`_ object containing a list of recipes to search when AutoML is performed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-automlconfig
            '''
            result = self._values.get("auto_ml_config")
            return typing.cast(typing.Any, result)

        @builtins.property
        def event_value_threshold(self) -> typing.Optional[builtins.str]:
            '''Only events with a value greater than or equal to this threshold are used for training a model.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-eventvaluethreshold
            '''
            result = self._values.get("event_value_threshold")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def feature_transformation_parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Lists the feature transformation parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-featuretransformationparameters
            '''
            result = self._values.get("feature_transformation_parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def hpo_config(self) -> typing.Any:
            '''Describes the properties for hyperparameter optimization (HPO).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-personalize-solution-solutionconfig.html#cfn-personalize-solution-solutionconfig-hpoconfig
            '''
            result = self._values.get("hpo_config")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SolutionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDatasetGroupMixinProps",
    "CfnDatasetGroupPropsMixin",
    "CfnDatasetMixinProps",
    "CfnDatasetPropsMixin",
    "CfnSchemaMixinProps",
    "CfnSchemaPropsMixin",
    "CfnSolutionMixinProps",
    "CfnSolutionPropsMixin",
]

publication.publish()

def _typecheckingstub__2b5a28907a1567d8a2161fbc98024577cb269a3a2fa61bd622e89ae4df90db26(
    *,
    domain: typing.Optional[builtins.str] = None,
    kms_key_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041e1657cda32f819dcdbd4145cc55d07b6b62b2ab29805d4771aa9d5366dd1b(
    props: typing.Union[CfnDatasetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cffbb1f4b2eb364f29580291952b29167969a18f4b204f9f413113e3df9cde(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959cb0349adfda8311e1e66a24d7111ab641e624efaebf3cef98dd5dbe33a70c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10951eca9b0a1000032fce4977464821f9f44c33051f746adf65d1401d9adf0(
    *,
    dataset_group_arn: typing.Optional[builtins.str] = None,
    dataset_import_job: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatasetImportJobProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dataset_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schema_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__180e395c48585977798952900f666c9649bd8ed4ddcbf35fbb820e4359582eed(
    props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2af26cd6f980d8c14d479184f3c85d0168e53c75a12d6627528f5a2e39590f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af4ff66d592fa2c0f63666a513ba084e9a2135a9e3c6a3f197d59a27f4d35a68(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53334e86868422e342e3046b78ac54cbd5759e2a4577be124a5e9829eca638de(
    *,
    dataset_arn: typing.Optional[builtins.str] = None,
    dataset_import_job_arn: typing.Optional[builtins.str] = None,
    data_source: typing.Any = None,
    job_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e959cbd6a60bcd172af1e715187e136108fdae2d27a7b1c7953ad5a43e1d791(
    *,
    domain: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    schema: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed1e0a0489e79057bf2056ab72452d7b08366a1d369a336b269b03296096a050(
    props: typing.Union[CfnSchemaMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1814ada5d90bd59b53533fccd93d676717b38798b6d14626bc8b27d5d11dac0e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf5e6472053deca8d044ed765991729db7fe4d53acaba39bc71637cfcdc81af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0700eeae4eecd1f53ff6df4cd468d13531cdd8e6fa70c0bc528b8cf904b8bc05(
    *,
    dataset_group_arn: typing.Optional[builtins.str] = None,
    event_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    perform_auto_ml: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    perform_hpo: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    recipe_arn: typing.Optional[builtins.str] = None,
    solution_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnSolutionPropsMixin.SolutionConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98722fcb608fba4e7d8bfe6fb8c08464cc860152070f4e5ef1aaf5c5f603dbb(
    props: typing.Union[CfnSolutionMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f565d161970ecc2c7855644afc5ebbfe0df841537f9f10d74990b705bbebe4a9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da58371729dad2485b7fc3027f2a9e0b70e3ebc7f48ec3c4653b15d349023d62(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__556c5fc4a5be423564f115ba06db28066aea3711b85c3af8d2d452ee0f01b412(
    *,
    algorithm_hyper_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    auto_ml_config: typing.Any = None,
    event_value_threshold: typing.Optional[builtins.str] = None,
    feature_transformation_parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    hpo_config: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
