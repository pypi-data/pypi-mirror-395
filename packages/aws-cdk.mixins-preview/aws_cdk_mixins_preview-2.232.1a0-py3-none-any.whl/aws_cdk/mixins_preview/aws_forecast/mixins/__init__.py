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
    jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetGroupMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_arns": "datasetArns",
        "dataset_group_name": "datasetGroupName",
        "domain": "domain",
        "tags": "tags",
    },
)
class CfnDatasetGroupMixinProps:
    def __init__(
        self,
        *,
        dataset_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        dataset_group_name: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatasetGroupPropsMixin.

        :param dataset_arns: An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the dataset group.
        :param dataset_group_name: The name of the dataset group.
        :param domain: The domain associated with the dataset group. When you add a dataset to a dataset group, this value and the value specified for the ``Domain`` parameter of the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ operation must match. The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be present in training data that you import to a dataset. For example, if you choose the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your data. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
            
            cfn_dataset_group_mixin_props = forecast_mixins.CfnDatasetGroupMixinProps(
                dataset_arns=["datasetArns"],
                dataset_group_name="datasetGroupName",
                domain="domain",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1ba5a0a4a7045aa573d7b59ea74c3e0e0cad87ec4ad2f3509ae1afda771101)
            check_type(argname="argument dataset_arns", value=dataset_arns, expected_type=type_hints["dataset_arns"])
            check_type(argname="argument dataset_group_name", value=dataset_group_name, expected_type=type_hints["dataset_group_name"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_arns is not None:
            self._values["dataset_arns"] = dataset_arns
        if dataset_group_name is not None:
            self._values["dataset_group_name"] = dataset_group_name
        if domain is not None:
            self._values["domain"] = domain
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataset_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of Amazon Resource Names (ARNs) of the datasets that you want to include in the dataset group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-datasetarns
        '''
        result = self._values.get("dataset_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def dataset_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dataset group.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-datasetgroupname
        '''
        result = self._values.get("dataset_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain associated with the dataset group.

        When you add a dataset to a dataset group, this value and the value specified for the ``Domain`` parameter of the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ operation must match.

        The ``Domain`` and ``DatasetType`` that you choose determine the fields that must be present in training data that you import to a dataset. For example, if you choose the ``RETAIL`` domain and ``TARGET_TIME_SERIES`` as the ``DatasetType`` , Amazon Forecast requires that ``item_id`` , ``timestamp`` , and ``demand`` fields are present in your data. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html#cfn-forecast-datasetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetGroupPropsMixin",
):
    '''Creates a dataset group, which holds a collection of related datasets.

    You can add datasets to the dataset group when you create the dataset group, or later by using the `UpdateDatasetGroup <https://docs.aws.amazon.com/forecast/latest/dg/API_UpdateDatasetGroup.html>`_ operation.
    .. epigraph::

       Amazon Forecast is no longer available to new customers. Existing customers of Amazon Forecast can continue to use the service as normal. `Learn more" <https://docs.aws.amazon.com/machine-learning/transition-your-amazon-forecast-usage-to-amazon-sagemaker-canvas/>`_

    After creating a dataset group and adding datasets, you use the dataset group when you create a predictor. For more information, see `Dataset groups <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

    To get a list of all your datasets groups, use the `ListDatasetGroups <https://docs.aws.amazon.com/forecast/latest/dg/API_ListDatasetGroups.html>`_ operation.
    .. epigraph::

       The ``Status`` of a dataset group must be ``ACTIVE`` before you can use the dataset group to create a predictor. To get the status, use the `DescribeDatasetGroup <https://docs.aws.amazon.com/forecast/latest/dg/API_DescribeDatasetGroup.html>`_ operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-datasetgroup.html
    :cloudformationResource: AWS::Forecast::DatasetGroup
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
        
        cfn_dataset_group_props_mixin = forecast_mixins.CfnDatasetGroupPropsMixin(forecast_mixins.CfnDatasetGroupMixinProps(
            dataset_arns=["datasetArns"],
            dataset_group_name="datasetGroupName",
            domain="domain",
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
        props: typing.Union[CfnDatasetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::Forecast::DatasetGroup``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11af640f072c35ee5f7b9ec7b3cdc80286ca4f85e16e1a12238f4875a4bd86c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf225c3c5fbd4969cda7d9fe672b19087fc6b7423a3bd7146412134006b0fe21)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb764dbd9e0df9bf0f43821fd2ffd94a8126870f9be5e31b3690f5a57838bc27)
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
    jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_frequency": "dataFrequency",
        "dataset_name": "datasetName",
        "dataset_type": "datasetType",
        "domain": "domain",
        "encryption_config": "encryptionConfig",
        "schema": "schema",
        "tags": "tags",
    },
)
class CfnDatasetMixinProps:
    def __init__(
        self,
        *,
        data_frequency: typing.Optional[builtins.str] = None,
        dataset_name: typing.Optional[builtins.str] = None,
        dataset_type: typing.Optional[builtins.str] = None,
        domain: typing.Optional[builtins.str] = None,
        encryption_config: typing.Any = None,
        schema: typing.Any = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDatasetPropsMixin.TagsItemsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatasetPropsMixin.

        :param data_frequency: The frequency of data collection. This parameter is required for RELATED_TIME_SERIES datasets. Valid intervals are an integer followed by Y (Year), M (Month), W (Week), D (Day), H (Hour), and min (Minute). For example, "1D" indicates every day and "15min" indicates every 15 minutes. You cannot specify a value that would overlap with the next larger frequency. That means, for example, you cannot specify a frequency of 60 minutes, because that is equivalent to 1 hour. The valid values for each frequency are the following: - Minute - 1-59 - Hour - 1-23 - Day - 1-6 - Week - 1-4 - Month - 1-11 - Year - 1 Thus, if you want every other week forecasts, specify "2W". Or, if you want quarterly forecasts, you specify "3M".
        :param dataset_name: The name of the dataset.
        :param dataset_type: The dataset type.
        :param domain: The domain associated with the dataset.
        :param encryption_config: A Key Management Service (KMS) key and the Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.
        :param schema: The schema for the dataset. The schema attributes and their order must match the fields in your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required fields in your training data. For information about the required fields for a specific dataset domain and type, see `Dataset Domains and Dataset Types <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-domains-ds-types.html>`_ .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
            
            # encryption_config: Any
            # schema: Any
            
            cfn_dataset_mixin_props = forecast_mixins.CfnDatasetMixinProps(
                data_frequency="dataFrequency",
                dataset_name="datasetName",
                dataset_type="datasetType",
                domain="domain",
                encryption_config=encryption_config,
                schema=schema,
                tags=[forecast_mixins.CfnDatasetPropsMixin.TagsItemsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1f88997dc38783886f64fe6ff2e0013ad7097465214c380edcbd9285efa4c7)
            check_type(argname="argument data_frequency", value=data_frequency, expected_type=type_hints["data_frequency"])
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument dataset_type", value=dataset_type, expected_type=type_hints["dataset_type"])
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument encryption_config", value=encryption_config, expected_type=type_hints["encryption_config"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_frequency is not None:
            self._values["data_frequency"] = data_frequency
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if dataset_type is not None:
            self._values["dataset_type"] = dataset_type
        if domain is not None:
            self._values["domain"] = domain
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if schema is not None:
            self._values["schema"] = schema
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_frequency(self) -> typing.Optional[builtins.str]:
        '''The frequency of data collection. This parameter is required for RELATED_TIME_SERIES datasets.

        Valid intervals are an integer followed by Y (Year), M (Month), W (Week), D (Day), H (Hour), and min (Minute). For example, "1D" indicates every day and "15min" indicates every 15 minutes. You cannot specify a value that would overlap with the next larger frequency. That means, for example, you cannot specify a frequency of 60 minutes, because that is equivalent to 1 hour. The valid values for each frequency are the following:

        - Minute - 1-59
        - Hour - 1-23
        - Day - 1-6
        - Week - 1-4
        - Month - 1-11
        - Year - 1

        Thus, if you want every other week forecasts, specify "2W". Or, if you want quarterly forecasts, you specify "3M".

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datafrequency
        '''
        result = self._values.get("data_frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datasetname
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dataset_type(self) -> typing.Optional[builtins.str]:
        '''The dataset type.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-datasettype
        '''
        result = self._values.get("dataset_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain associated with the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-domain
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_config(self) -> typing.Any:
        '''A Key Management Service (KMS) key and the Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-encryptionconfig
        '''
        result = self._values.get("encryption_config")
        return typing.cast(typing.Any, result)

    @builtins.property
    def schema(self) -> typing.Any:
        '''The schema for the dataset.

        The schema attributes and their order must match the fields in your data. The dataset ``Domain`` and ``DatasetType`` that you choose determine the minimum required fields in your training data. For information about the required fields for a specific dataset domain and type, see `Dataset Domains and Dataset Types <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-domains-ds-types.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Any, result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnDatasetPropsMixin.TagsItemsProperty"]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html#cfn-forecast-dataset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnDatasetPropsMixin.TagsItemsProperty"]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetPropsMixin",
):
    '''Creates an Amazon Forecast dataset.

    .. epigraph::

       Amazon Forecast is no longer available to new customers. Existing customers of Amazon Forecast can continue to use the service as normal. `Learn more" <https://docs.aws.amazon.com/machine-learning/transition-your-amazon-forecast-usage-to-amazon-sagemaker-canvas/>`_

    The information about the dataset that you provide helps Forecast understand how to consume the data for model training. This includes the following:

    - *``DataFrequency``* - How frequently your historical time-series data is collected.
    - *``Domain``* and *``DatasetType``* - Each dataset has an associated dataset domain and a type within the domain. Amazon Forecast provides a list of predefined domains and types within each domain. For each unique dataset domain and type within the domain, Amazon Forecast requires your data to include a minimum set of predefined fields.
    - *``Schema``* - A schema specifies the fields in the dataset, including the field name and data type.

    After creating a dataset, you import your training data into it and add the dataset to a dataset group. You use the dataset group to create a predictor. For more information, see `Importing datasets <https://docs.aws.amazon.com/forecast/latest/dg/howitworks-datasets-groups.html>`_ .

    To get a list of all your datasets, use the `ListDatasets <https://docs.aws.amazon.com/forecast/latest/dg/API_ListDatasets.html>`_ operation.

    For example Forecast datasets, see the `Amazon Forecast Sample GitHub repository <https://docs.aws.amazon.com/https://github.com/aws-samples/amazon-forecast-samples>`_ .
    .. epigraph::

       The ``Status`` of a dataset must be ``ACTIVE`` before you can import training data. Use the `DescribeDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_DescribeDataset.html>`_ operation to get the status.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-forecast-dataset.html
    :cloudformationResource: AWS::Forecast::Dataset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
        
        # encryption_config: Any
        # schema: Any
        
        cfn_dataset_props_mixin = forecast_mixins.CfnDatasetPropsMixin(forecast_mixins.CfnDatasetMixinProps(
            data_frequency="dataFrequency",
            dataset_name="datasetName",
            dataset_type="datasetType",
            domain="domain",
            encryption_config=encryption_config,
            schema=schema,
            tags=[forecast_mixins.CfnDatasetPropsMixin.TagsItemsProperty(
                key="key",
                value="value"
            )]
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
        '''Create a mixin to apply properties to ``AWS::Forecast::Dataset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0dd4c0a1bdfed4404011e5ef7ae62e1807e0c99557f7837a1c554b033b3a14d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06443216a4a4f7a9df362164950e2618eef5a98bf69116df0ab871229dd9eb57)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0b978cae7fd9425fc9d5fff1db328c67ac3b26113de2c60f137f2c736ff17a)
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
        jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetPropsMixin.AttributesItemsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "attribute_name": "attributeName",
            "attribute_type": "attributeType",
        },
    )
    class AttributesItemsProperty:
        def __init__(
            self,
            *,
            attribute_name: typing.Optional[builtins.str] = None,
            attribute_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param attribute_name: Name of the dataset field.
            :param attribute_type: Data type of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-attributesitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
                
                attributes_items_property = forecast_mixins.CfnDatasetPropsMixin.AttributesItemsProperty(
                    attribute_name="attributeName",
                    attribute_type="attributeType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__acb5de88aa9b39bc9f6fb9c71d51abce181cbf5ee677560239ebff6ad8dfb116)
                check_type(argname="argument attribute_name", value=attribute_name, expected_type=type_hints["attribute_name"])
                check_type(argname="argument attribute_type", value=attribute_type, expected_type=type_hints["attribute_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attribute_name is not None:
                self._values["attribute_name"] = attribute_name
            if attribute_type is not None:
                self._values["attribute_type"] = attribute_type

        @builtins.property
        def attribute_name(self) -> typing.Optional[builtins.str]:
            '''Name of the dataset field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-attributesitems.html#cfn-forecast-dataset-attributesitems-attributename
            '''
            result = self._values.get("attribute_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def attribute_type(self) -> typing.Optional[builtins.str]:
            '''Data type of the field.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-attributesitems.html#cfn-forecast-dataset-attributesitems-attributetype
            '''
            result = self._values.get("attribute_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AttributesItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetPropsMixin.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_arn": "kmsKeyArn", "role_arn": "roleArn"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            kms_key_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An AWS Key Management Service (KMS) key and an AWS Identity and Access Management (IAM) role that Amazon Forecast can assume to access the key.

            You can specify this optional object in the `CreateDataset <https://docs.aws.amazon.com/forecast/latest/dg/API_CreateDataset.html>`_ and `CreatePredictor <https://docs.aws.amazon.com/forecast/latest/dg/API_CreatePredictor.html>`_ requests.

            :param kms_key_arn: The Amazon Resource Name (ARN) of the KMS key.
            :param role_arn: The ARN of the IAM role that Amazon Forecast can assume to access the AWS key. Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your account, you get an ``InvalidInputException`` error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-encryptionconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
                
                encryption_config_property = forecast_mixins.CfnDatasetPropsMixin.EncryptionConfigProperty(
                    kms_key_arn="kmsKeyArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb5a252d49d533d15fa036cfc7b1f10dbe0549bc6350b6c5e4317aada87eab3d)
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the KMS key.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-encryptionconfig.html#cfn-forecast-dataset-encryptionconfig-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that Amazon Forecast can assume to access the AWS  key.

            Passing a role across AWS accounts is not allowed. If you pass a role that isn't in your account, you get an ``InvalidInputException`` error.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-encryptionconfig.html#cfn-forecast-dataset-encryptionconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetPropsMixin.SchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes"},
    )
    class SchemaProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.AttributesItemsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines the fields of a dataset.

            :param attributes: An array of attributes specifying the name and type of each field in a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-schema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
                
                schema_property = forecast_mixins.CfnDatasetPropsMixin.SchemaProperty(
                    attributes=[forecast_mixins.CfnDatasetPropsMixin.AttributesItemsProperty(
                        attribute_name="attributeName",
                        attribute_type="attributeType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26c2b93f8df20e0a5f675e87dcdfb256e1bdb1969739aa89268f82f9488fcbc9)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.AttributesItemsProperty"]]]]:
            '''An array of attributes specifying the name and type of each field in a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-schema.html#cfn-forecast-dataset-schema-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.AttributesItemsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_forecast.mixins.CfnDatasetPropsMixin.TagsItemsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsItemsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair to associate with a resource.

            :param key: The key name of the tag. You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
            :param value: The value for the tag. You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-tagsitems.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_forecast import mixins as forecast_mixins
                
                tags_items_property = forecast_mixins.CfnDatasetPropsMixin.TagsItemsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e7fe69594f33ddddec3a54391f76db5e11394a828ceb4d9ca86e94b45fba7c2)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key name of the tag.

            You can specify a value that is 1 to 128 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-tagsitems.html#cfn-forecast-dataset-tagsitems-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the tag.

            You can specify a value that is 0 to 256 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-forecast-dataset-tagsitems.html#cfn-forecast-dataset-tagsitems-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsItemsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnDatasetGroupMixinProps",
    "CfnDatasetGroupPropsMixin",
    "CfnDatasetMixinProps",
    "CfnDatasetPropsMixin",
]

publication.publish()

def _typecheckingstub__bb1ba5a0a4a7045aa573d7b59ea74c3e0e0cad87ec4ad2f3509ae1afda771101(
    *,
    dataset_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    dataset_group_name: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11af640f072c35ee5f7b9ec7b3cdc80286ca4f85e16e1a12238f4875a4bd86c6(
    props: typing.Union[CfnDatasetGroupMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf225c3c5fbd4969cda7d9fe672b19087fc6b7423a3bd7146412134006b0fe21(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb764dbd9e0df9bf0f43821fd2ffd94a8126870f9be5e31b3690f5a57838bc27(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1f88997dc38783886f64fe6ff2e0013ad7097465214c380edcbd9285efa4c7(
    *,
    data_frequency: typing.Optional[builtins.str] = None,
    dataset_name: typing.Optional[builtins.str] = None,
    dataset_type: typing.Optional[builtins.str] = None,
    domain: typing.Optional[builtins.str] = None,
    encryption_config: typing.Any = None,
    schema: typing.Any = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDatasetPropsMixin.TagsItemsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0dd4c0a1bdfed4404011e5ef7ae62e1807e0c99557f7837a1c554b033b3a14d(
    props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06443216a4a4f7a9df362164950e2618eef5a98bf69116df0ab871229dd9eb57(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0b978cae7fd9425fc9d5fff1db328c67ac3b26113de2c60f137f2c736ff17a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb5de88aa9b39bc9f6fb9c71d51abce181cbf5ee677560239ebff6ad8dfb116(
    *,
    attribute_name: typing.Optional[builtins.str] = None,
    attribute_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5a252d49d533d15fa036cfc7b1f10dbe0549bc6350b6c5e4317aada87eab3d(
    *,
    kms_key_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c2b93f8df20e0a5f675e87dcdfb256e1bdb1969739aa89268f82f9488fcbc9(
    *,
    attributes: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.AttributesItemsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7fe69594f33ddddec3a54391f76db5e11394a828ceb4d9ca86e94b45fba7c2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
