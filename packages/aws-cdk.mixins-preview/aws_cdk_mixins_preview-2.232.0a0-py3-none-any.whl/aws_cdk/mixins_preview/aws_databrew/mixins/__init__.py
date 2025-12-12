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
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "format": "format",
        "format_options": "formatOptions",
        "input": "input",
        "name": "name",
        "path_options": "pathOptions",
        "source": "source",
        "tags": "tags",
    },
)
class CfnDatasetMixinProps:
    def __init__(
        self,
        *,
        format: typing.Optional[builtins.str] = None,
        format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.FormatOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.InputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        path_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.PathOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        source: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnDatasetPropsMixin.

        :param format: The file format of a dataset that is created from an Amazon S3 file or folder.
        :param format_options: A set of options that define how DataBrew interprets the data in the dataset.
        :param input: Information on how DataBrew can find the dataset, in either the AWS Glue Data Catalog or Amazon S3 .
        :param name: The unique name of the dataset.
        :param path_options: A set of options that defines how DataBrew interprets an Amazon S3 path of the dataset.
        :param source: The location of the data for the dataset, either Amazon S3 or the AWS Glue Data Catalog .
        :param tags: Metadata tags that have been applied to the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
            
            cfn_dataset_mixin_props = databrew_mixins.CfnDatasetMixinProps(
                format="format",
                format_options=databrew_mixins.CfnDatasetPropsMixin.FormatOptionsProperty(
                    csv=databrew_mixins.CfnDatasetPropsMixin.CsvOptionsProperty(
                        delimiter="delimiter",
                        header_row=False
                    ),
                    excel=databrew_mixins.CfnDatasetPropsMixin.ExcelOptionsProperty(
                        header_row=False,
                        sheet_indexes=[123],
                        sheet_names=["sheetNames"]
                    ),
                    json=databrew_mixins.CfnDatasetPropsMixin.JsonOptionsProperty(
                        multi_line=False
                    )
                ),
                input=databrew_mixins.CfnDatasetPropsMixin.InputProperty(
                    database_input_definition=databrew_mixins.CfnDatasetPropsMixin.DatabaseInputDefinitionProperty(
                        database_table_name="databaseTableName",
                        glue_connection_name="glueConnectionName",
                        query_string="queryString",
                        temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    data_catalog_input_definition=databrew_mixins.CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        table_name="tableName",
                        temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    metadata=databrew_mixins.CfnDatasetPropsMixin.MetadataProperty(
                        source_arn="sourceArn"
                    ),
                    s3_input_definition=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                ),
                name="name",
                path_options=databrew_mixins.CfnDatasetPropsMixin.PathOptionsProperty(
                    files_limit=databrew_mixins.CfnDatasetPropsMixin.FilesLimitProperty(
                        max_files=123,
                        order="order",
                        ordered_by="orderedBy"
                    ),
                    last_modified_date_condition=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                        expression="expression",
                        values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                            value="value",
                            value_reference="valueReference"
                        )]
                    ),
                    parameters=[databrew_mixins.CfnDatasetPropsMixin.PathParameterProperty(
                        dataset_parameter=databrew_mixins.CfnDatasetPropsMixin.DatasetParameterProperty(
                            create_column=False,
                            datetime_options=databrew_mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty(
                                format="format",
                                locale_code="localeCode",
                                timezone_offset="timezoneOffset"
                            ),
                            filter=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                                expression="expression",
                                values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                                    value="value",
                                    value_reference="valueReference"
                                )]
                            ),
                            name="name",
                            type="type"
                        ),
                        path_parameter_name="pathParameterName"
                    )]
                ),
                source="source",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__572029c63c693c197bca564ac00b49cc48704454f0a4e0e06decb8f668bd974f)
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument format_options", value=format_options, expected_type=type_hints["format_options"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path_options", value=path_options, expected_type=type_hints["path_options"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if format is not None:
            self._values["format"] = format
        if format_options is not None:
            self._values["format_options"] = format_options
        if input is not None:
            self._values["input"] = input
        if name is not None:
            self._values["name"] = name
        if path_options is not None:
            self._values["path_options"] = path_options
        if source is not None:
            self._values["source"] = source
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def format(self) -> typing.Optional[builtins.str]:
        '''The file format of a dataset that is created from an Amazon S3 file or folder.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-format
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def format_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FormatOptionsProperty"]]:
        '''A set of options that define how DataBrew interprets the data in the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-formatoptions
        '''
        result = self._values.get("format_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FormatOptionsProperty"]], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.InputProperty"]]:
        '''Information on how DataBrew can find the dataset, in either the AWS Glue Data Catalog or Amazon S3 .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-input
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.InputProperty"]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.PathOptionsProperty"]]:
        '''A set of options that defines how DataBrew interprets an Amazon S3 path of the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-pathoptions
        '''
        result = self._values.get("path_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.PathOptionsProperty"]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''The location of the data for the dataset, either Amazon S3 or the AWS Glue Data Catalog .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata tags that have been applied to the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html#cfn-databrew-dataset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

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
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin",
):
    '''Specifies a new DataBrew dataset.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-dataset.html
    :cloudformationResource: AWS::DataBrew::Dataset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
        
        cfn_dataset_props_mixin = databrew_mixins.CfnDatasetPropsMixin(databrew_mixins.CfnDatasetMixinProps(
            format="format",
            format_options=databrew_mixins.CfnDatasetPropsMixin.FormatOptionsProperty(
                csv=databrew_mixins.CfnDatasetPropsMixin.CsvOptionsProperty(
                    delimiter="delimiter",
                    header_row=False
                ),
                excel=databrew_mixins.CfnDatasetPropsMixin.ExcelOptionsProperty(
                    header_row=False,
                    sheet_indexes=[123],
                    sheet_names=["sheetNames"]
                ),
                json=databrew_mixins.CfnDatasetPropsMixin.JsonOptionsProperty(
                    multi_line=False
                )
            ),
            input=databrew_mixins.CfnDatasetPropsMixin.InputProperty(
                database_input_definition=databrew_mixins.CfnDatasetPropsMixin.DatabaseInputDefinitionProperty(
                    database_table_name="databaseTableName",
                    glue_connection_name="glueConnectionName",
                    query_string="queryString",
                    temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                ),
                data_catalog_input_definition=databrew_mixins.CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    table_name="tableName",
                    temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                ),
                metadata=databrew_mixins.CfnDatasetPropsMixin.MetadataProperty(
                    source_arn="sourceArn"
                ),
                s3_input_definition=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    key="key"
                )
            ),
            name="name",
            path_options=databrew_mixins.CfnDatasetPropsMixin.PathOptionsProperty(
                files_limit=databrew_mixins.CfnDatasetPropsMixin.FilesLimitProperty(
                    max_files=123,
                    order="order",
                    ordered_by="orderedBy"
                ),
                last_modified_date_condition=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                    expression="expression",
                    values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                        value="value",
                        value_reference="valueReference"
                    )]
                ),
                parameters=[databrew_mixins.CfnDatasetPropsMixin.PathParameterProperty(
                    dataset_parameter=databrew_mixins.CfnDatasetPropsMixin.DatasetParameterProperty(
                        create_column=False,
                        datetime_options=databrew_mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty(
                            format="format",
                            locale_code="localeCode",
                            timezone_offset="timezoneOffset"
                        ),
                        filter=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                            expression="expression",
                            values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                                value="value",
                                value_reference="valueReference"
                            )]
                        ),
                        name="name",
                        type="type"
                    ),
                    path_parameter_name="pathParameterName"
                )]
            ),
            source="source",
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
        props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataBrew::Dataset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a88bc9e5d8a5c17b8c58aee9ca5785cdd181702cc2ea0db698ce7a030a1846)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f52fd6a312c516c0ba047c29271839ae93ee7a3c76dcecada00071df65e6c9a)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08be38015b6a453925d5acc83c7203063b06a66057e75c1502f54e391dd19fb)
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
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.CsvOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"delimiter": "delimiter", "header_row": "headerRow"},
    )
    class CsvOptionsProperty:
        def __init__(
            self,
            *,
            delimiter: typing.Optional[builtins.str] = None,
            header_row: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Represents a set of options that define how DataBrew will read a comma-separated value (CSV) file when creating a dataset from that file.

            :param delimiter: A single character that specifies the delimiter being used in the CSV file.
            :param header_row: A variable that specifies whether the first row in the file is parsed as the header. If this value is false, column names are auto-generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-csvoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                csv_options_property = databrew_mixins.CfnDatasetPropsMixin.CsvOptionsProperty(
                    delimiter="delimiter",
                    header_row=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__37044d638c0fdbac004f87562d9c638ee6722f73fc0e83de9bb3aa4e53599fb8)
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
                check_type(argname="argument header_row", value=header_row, expected_type=type_hints["header_row"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter
            if header_row is not None:
                self._values["header_row"] = header_row

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''A single character that specifies the delimiter being used in the CSV file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-csvoptions.html#cfn-databrew-dataset-csvoptions-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def header_row(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A variable that specifies whether the first row in the file is parsed as the header.

            If this value is false, column names are auto-generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-csvoptions.html#cfn-databrew-dataset-csvoptions-headerrow
            '''
            result = self._values.get("header_row")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "table_name": "tableName",
            "temp_directory": "tempDirectory",
        },
    )
    class DataCatalogInputDefinitionProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
            temp_directory: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents how metadata stored in the AWS Glue Data Catalog is defined in a DataBrew dataset.

            :param catalog_id: The unique identifier of the AWS account that holds the Data Catalog that stores the data.
            :param database_name: The name of a database in the Data Catalog.
            :param table_name: The name of a database table in the Data Catalog. This table corresponds to a DataBrew dataset.
            :param temp_directory: An Amazon location that AWS Glue Data Catalog can use as a temporary directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datacataloginputdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                data_catalog_input_definition_property = databrew_mixins.CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    table_name="tableName",
                    temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d472f50d6302ca11e63c48e863f6392a6fb8d3c1ad9fc69673757fef28b4d386)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument temp_directory", value=temp_directory, expected_type=type_hints["temp_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if table_name is not None:
                self._values["table_name"] = table_name
            if temp_directory is not None:
                self._values["temp_directory"] = temp_directory

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the AWS account that holds the Data Catalog that stores the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datacataloginputdefinition.html#cfn-databrew-dataset-datacataloginputdefinition-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of a database in the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datacataloginputdefinition.html#cfn-databrew-dataset-datacataloginputdefinition-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of a database table in the Data Catalog.

            This table corresponds to a DataBrew dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datacataloginputdefinition.html#cfn-databrew-dataset-datacataloginputdefinition-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def temp_directory(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3LocationProperty"]]:
            '''An Amazon location that AWS Glue Data Catalog can use as a temporary directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datacataloginputdefinition.html#cfn-databrew-dataset-datacataloginputdefinition-tempdirectory
            '''
            result = self._values.get("temp_directory")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataCatalogInputDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.DatabaseInputDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_table_name": "databaseTableName",
            "glue_connection_name": "glueConnectionName",
            "query_string": "queryString",
            "temp_directory": "tempDirectory",
        },
    )
    class DatabaseInputDefinitionProperty:
        def __init__(
            self,
            *,
            database_table_name: typing.Optional[builtins.str] = None,
            glue_connection_name: typing.Optional[builtins.str] = None,
            query_string: typing.Optional[builtins.str] = None,
            temp_directory: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Connection information for dataset input files stored in a database.

            :param database_table_name: The table within the target database.
            :param glue_connection_name: The AWS Glue Connection that stores the connection information for the target database.
            :param query_string: Custom SQL to run against the provided AWS Glue connection. This SQL will be used as the input for DataBrew projects and jobs.
            :param temp_directory: An Amazon location that AWS Glue Data Catalog can use as a temporary directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-databaseinputdefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                database_input_definition_property = databrew_mixins.CfnDatasetPropsMixin.DatabaseInputDefinitionProperty(
                    database_table_name="databaseTableName",
                    glue_connection_name="glueConnectionName",
                    query_string="queryString",
                    temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__277507f77544e137de410c5a528e6a96afffb12ea9f40d4ad9171dfbc747aba7)
                check_type(argname="argument database_table_name", value=database_table_name, expected_type=type_hints["database_table_name"])
                check_type(argname="argument glue_connection_name", value=glue_connection_name, expected_type=type_hints["glue_connection_name"])
                check_type(argname="argument query_string", value=query_string, expected_type=type_hints["query_string"])
                check_type(argname="argument temp_directory", value=temp_directory, expected_type=type_hints["temp_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_table_name is not None:
                self._values["database_table_name"] = database_table_name
            if glue_connection_name is not None:
                self._values["glue_connection_name"] = glue_connection_name
            if query_string is not None:
                self._values["query_string"] = query_string
            if temp_directory is not None:
                self._values["temp_directory"] = temp_directory

        @builtins.property
        def database_table_name(self) -> typing.Optional[builtins.str]:
            '''The table within the target database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-databaseinputdefinition.html#cfn-databrew-dataset-databaseinputdefinition-databasetablename
            '''
            result = self._values.get("database_table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def glue_connection_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Glue Connection that stores the connection information for the target database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-databaseinputdefinition.html#cfn-databrew-dataset-databaseinputdefinition-glueconnectionname
            '''
            result = self._values.get("glue_connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def query_string(self) -> typing.Optional[builtins.str]:
            '''Custom SQL to run against the provided AWS Glue connection.

            This SQL will be used as the input for DataBrew projects and jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-databaseinputdefinition.html#cfn-databrew-dataset-databaseinputdefinition-querystring
            '''
            result = self._values.get("query_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def temp_directory(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3LocationProperty"]]:
            '''An Amazon location that AWS Glue Data Catalog can use as a temporary directory.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-databaseinputdefinition.html#cfn-databrew-dataset-databaseinputdefinition-tempdirectory
            '''
            result = self._values.get("temp_directory")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseInputDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.DatasetParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "create_column": "createColumn",
            "datetime_options": "datetimeOptions",
            "filter": "filter",
            "name": "name",
            "type": "type",
        },
    )
    class DatasetParameterProperty:
        def __init__(
            self,
            *,
            create_column: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            datetime_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatetimeOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.FilterExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a dataset paramater that defines type and conditions for a parameter in the Amazon S3 path of the dataset.

            :param create_column: Optional boolean value that defines whether the captured value of this parameter should be loaded as an additional column in the dataset.
            :param datetime_options: Additional parameter options such as a format and a timezone. Required for datetime parameters.
            :param filter: The optional filter expression structure to apply additional matching criteria to the parameter.
            :param name: The name of the parameter that is used in the dataset's Amazon S3 path.
            :param type: The type of the dataset parameter, can be one of a 'String', 'Number' or 'Datetime'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datasetparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                dataset_parameter_property = databrew_mixins.CfnDatasetPropsMixin.DatasetParameterProperty(
                    create_column=False,
                    datetime_options=databrew_mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty(
                        format="format",
                        locale_code="localeCode",
                        timezone_offset="timezoneOffset"
                    ),
                    filter=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                        expression="expression",
                        values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                            value="value",
                            value_reference="valueReference"
                        )]
                    ),
                    name="name",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2e85578646a1ed424a9a333d8a38da666077a9e7bea291f023ddb265c957931)
                check_type(argname="argument create_column", value=create_column, expected_type=type_hints["create_column"])
                check_type(argname="argument datetime_options", value=datetime_options, expected_type=type_hints["datetime_options"])
                check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if create_column is not None:
                self._values["create_column"] = create_column
            if datetime_options is not None:
                self._values["datetime_options"] = datetime_options
            if filter is not None:
                self._values["filter"] = filter
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def create_column(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''Optional boolean value that defines whether the captured value of this parameter should be loaded as an additional column in the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datasetparameter.html#cfn-databrew-dataset-datasetparameter-createcolumn
            '''
            result = self._values.get("create_column")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def datetime_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatetimeOptionsProperty"]]:
            '''Additional parameter options such as a format and a timezone.

            Required for datetime parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datasetparameter.html#cfn-databrew-dataset-datasetparameter-datetimeoptions
            '''
            result = self._values.get("datetime_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatetimeOptionsProperty"]], result)

        @builtins.property
        def filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterExpressionProperty"]]:
            '''The optional filter expression structure to apply additional matching criteria to the parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datasetparameter.html#cfn-databrew-dataset-datasetparameter-filter
            '''
            result = self._values.get("filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterExpressionProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the parameter that is used in the dataset's Amazon S3 path.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datasetparameter.html#cfn-databrew-dataset-datasetparameter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of the dataset parameter, can be one of a 'String', 'Number' or 'Datetime'.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datasetparameter.html#cfn-databrew-dataset-datasetparameter-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "format": "format",
            "locale_code": "localeCode",
            "timezone_offset": "timezoneOffset",
        },
    )
    class DatetimeOptionsProperty:
        def __init__(
            self,
            *,
            format: typing.Optional[builtins.str] = None,
            locale_code: typing.Optional[builtins.str] = None,
            timezone_offset: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents additional options for correct interpretation of datetime parameters used in the Amazon S3 path of a dataset.

            :param format: Required option, that defines the datetime format used for a date parameter in the Amazon S3 path. Should use only supported datetime specifiers and separation characters, all litera a-z or A-Z character should be escaped with single quotes. E.g. "MM.dd.yyyy-'at'-HH:mm".
            :param locale_code: Optional value for a non-US locale code, needed for correct interpretation of some date formats.
            :param timezone_offset: Optional value for a timezone offset of the datetime parameter value in the Amazon S3 path. Shouldn't be used if Format for this parameter includes timezone fields. If no offset specified, UTC is assumed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datetimeoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                datetime_options_property = databrew_mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty(
                    format="format",
                    locale_code="localeCode",
                    timezone_offset="timezoneOffset"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e9c5ef567cbfc8b58b5ab0e177dd8e31b96d77317c559d0822c3c235bec9a06c)
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument locale_code", value=locale_code, expected_type=type_hints["locale_code"])
                check_type(argname="argument timezone_offset", value=timezone_offset, expected_type=type_hints["timezone_offset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if format is not None:
                self._values["format"] = format
            if locale_code is not None:
                self._values["locale_code"] = locale_code
            if timezone_offset is not None:
                self._values["timezone_offset"] = timezone_offset

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''Required option, that defines the datetime format used for a date parameter in the Amazon S3 path.

            Should use only supported datetime specifiers and separation characters, all litera a-z or A-Z character should be escaped with single quotes. E.g. "MM.dd.yyyy-'at'-HH:mm".

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datetimeoptions.html#cfn-databrew-dataset-datetimeoptions-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def locale_code(self) -> typing.Optional[builtins.str]:
            '''Optional value for a non-US locale code, needed for correct interpretation of some date formats.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datetimeoptions.html#cfn-databrew-dataset-datetimeoptions-localecode
            '''
            result = self._values.get("locale_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timezone_offset(self) -> typing.Optional[builtins.str]:
            '''Optional value for a timezone offset of the datetime parameter value in the Amazon S3 path.

            Shouldn't be used if Format for this parameter includes timezone fields. If no offset specified, UTC is assumed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-datetimeoptions.html#cfn-databrew-dataset-datetimeoptions-timezoneoffset
            '''
            result = self._values.get("timezone_offset")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatetimeOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.ExcelOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_row": "headerRow",
            "sheet_indexes": "sheetIndexes",
            "sheet_names": "sheetNames",
        },
    )
    class ExcelOptionsProperty:
        def __init__(
            self,
            *,
            header_row: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            sheet_indexes: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
            sheet_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Represents a set of options that define how DataBrew will interpret a Microsoft Excel file when creating a dataset from that file.

            :param header_row: A variable that specifies whether the first row in the file is parsed as the header. If this value is false, column names are auto-generated.
            :param sheet_indexes: One or more sheet numbers in the Excel file that will be included in the dataset.
            :param sheet_names: One or more named sheets in the Excel file that will be included in the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-exceloptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                excel_options_property = databrew_mixins.CfnDatasetPropsMixin.ExcelOptionsProperty(
                    header_row=False,
                    sheet_indexes=[123],
                    sheet_names=["sheetNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ceb0747143850b3edc4490f181e5de1c6c4d7243e0f281049c8b60a90bd5c836)
                check_type(argname="argument header_row", value=header_row, expected_type=type_hints["header_row"])
                check_type(argname="argument sheet_indexes", value=sheet_indexes, expected_type=type_hints["sheet_indexes"])
                check_type(argname="argument sheet_names", value=sheet_names, expected_type=type_hints["sheet_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_row is not None:
                self._values["header_row"] = header_row
            if sheet_indexes is not None:
                self._values["sheet_indexes"] = sheet_indexes
            if sheet_names is not None:
                self._values["sheet_names"] = sheet_names

        @builtins.property
        def header_row(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A variable that specifies whether the first row in the file is parsed as the header.

            If this value is false, column names are auto-generated.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-exceloptions.html#cfn-databrew-dataset-exceloptions-headerrow
            '''
            result = self._values.get("header_row")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sheet_indexes(
            self,
        ) -> typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]]:
            '''One or more sheet numbers in the Excel file that will be included in the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-exceloptions.html#cfn-databrew-dataset-exceloptions-sheetindexes
            '''
            result = self._values.get("sheet_indexes")
            return typing.cast(typing.Optional[typing.Union[typing.List[jsii.Number], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def sheet_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more named sheets in the Excel file that will be included in the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-exceloptions.html#cfn-databrew-dataset-exceloptions-sheetnames
            '''
            result = self._values.get("sheet_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExcelOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.FilesLimitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "max_files": "maxFiles",
            "order": "order",
            "ordered_by": "orderedBy",
        },
    )
    class FilesLimitProperty:
        def __init__(
            self,
            *,
            max_files: typing.Optional[jsii.Number] = None,
            order: typing.Optional[builtins.str] = None,
            ordered_by: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a limit imposed on number of Amazon S3 files that should be selected for a dataset from a connected Amazon S3 path.

            :param max_files: The number of Amazon S3 files to select.
            :param order: A criteria to use for Amazon S3 files sorting before their selection. By default uses DESCENDING order, i.e. most recent files are selected first. Anotherpossible value is ASCENDING.
            :param ordered_by: A criteria to use for Amazon S3 files sorting before their selection. By default uses LAST_MODIFIED_DATE as a sorting criteria. Currently it's the only allowed value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-fileslimit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                files_limit_property = databrew_mixins.CfnDatasetPropsMixin.FilesLimitProperty(
                    max_files=123,
                    order="order",
                    ordered_by="orderedBy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a958430f9e0b57cc1ea47825f3aca32a163b97aba2c908d275cb2787dfb0a280)
                check_type(argname="argument max_files", value=max_files, expected_type=type_hints["max_files"])
                check_type(argname="argument order", value=order, expected_type=type_hints["order"])
                check_type(argname="argument ordered_by", value=ordered_by, expected_type=type_hints["ordered_by"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_files is not None:
                self._values["max_files"] = max_files
            if order is not None:
                self._values["order"] = order
            if ordered_by is not None:
                self._values["ordered_by"] = ordered_by

        @builtins.property
        def max_files(self) -> typing.Optional[jsii.Number]:
            '''The number of Amazon S3 files to select.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-fileslimit.html#cfn-databrew-dataset-fileslimit-maxfiles
            '''
            result = self._values.get("max_files")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def order(self) -> typing.Optional[builtins.str]:
            '''A criteria to use for Amazon S3 files sorting before their selection.

            By default uses DESCENDING order, i.e. most recent files are selected first. Anotherpossible value is ASCENDING.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-fileslimit.html#cfn-databrew-dataset-fileslimit-order
            '''
            result = self._values.get("order")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ordered_by(self) -> typing.Optional[builtins.str]:
            '''A criteria to use for Amazon S3 files sorting before their selection.

            By default uses LAST_MODIFIED_DATE as a sorting criteria. Currently it's the only allowed value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-fileslimit.html#cfn-databrew-dataset-fileslimit-orderedby
            '''
            result = self._values.get("ordered_by")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilesLimitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.FilterExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={"expression": "expression", "values_map": "valuesMap"},
    )
    class FilterExpressionProperty:
        def __init__(
            self,
            *,
            expression: typing.Optional[builtins.str] = None,
            values_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.FilterValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents a structure for defining parameter conditions.

            :param expression: The expression which includes condition names followed by substitution variables, possibly grouped and combined with other conditions. For example, "(starts_with :prefix1 or starts_with :prefix2) and (ends_with :suffix1 or ends_with :suffix2)". Substitution variables should start with ':' symbol.
            :param values_map: The map of substitution variable names to their values used in this filter expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-filterexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                filter_expression_property = databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                    expression="expression",
                    values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                        value="value",
                        value_reference="valueReference"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f3c026466622cbf141686d83153af1ff2b90fb3977041baab4e055258ca38e3)
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument values_map", value=values_map, expected_type=type_hints["values_map"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if expression is not None:
                self._values["expression"] = expression
            if values_map is not None:
                self._values["values_map"] = values_map

        @builtins.property
        def expression(self) -> typing.Optional[builtins.str]:
            '''The expression which includes condition names followed by substitution variables, possibly grouped and combined with other conditions.

            For example, "(starts_with :prefix1 or starts_with :prefix2) and (ends_with :suffix1 or ends_with :suffix2)". Substitution variables should start with ':' symbol.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-filterexpression.html#cfn-databrew-dataset-filterexpression-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def values_map(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterValueProperty"]]]]:
            '''The map of substitution variable names to their values used in this filter expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-filterexpression.html#cfn-databrew-dataset-filterexpression-valuesmap
            '''
            result = self._values.get("values_map")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterValueProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.FilterValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "value_reference": "valueReference"},
    )
    class FilterValueProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[builtins.str] = None,
            value_reference: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a single entry in the ``ValuesMap`` of a ``FilterExpression`` .

            A ``FilterValue`` associates the name of a substitution variable in an expression to its value.

            :param value: The value to be associated with the substitution variable.
            :param value_reference: The substitution variable reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-filtervalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                filter_value_property = databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                    value="value",
                    value_reference="valueReference"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff1379955d0f05517da830c52e6a33544911be512257e70c0d0ea56d67914f78)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_reference", value=value_reference, expected_type=type_hints["value_reference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if value_reference is not None:
                self._values["value_reference"] = value_reference

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value to be associated with the substitution variable.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-filtervalue.html#cfn-databrew-dataset-filtervalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_reference(self) -> typing.Optional[builtins.str]:
            '''The substitution variable reference.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-filtervalue.html#cfn-databrew-dataset-filtervalue-valuereference
            '''
            result = self._values.get("value_reference")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.FormatOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"csv": "csv", "excel": "excel", "json": "json"},
    )
    class FormatOptionsProperty:
        def __init__(
            self,
            *,
            csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.CsvOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            excel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.ExcelOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.JsonOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents a set of options that define the structure of either comma-separated value (CSV), Excel, or JSON input.

            :param csv: Options that define how CSV input is to be interpreted by DataBrew.
            :param excel: Options that define how Excel input is to be interpreted by DataBrew.
            :param json: Options that define how JSON input is to be interpreted by DataBrew.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-formatoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                format_options_property = databrew_mixins.CfnDatasetPropsMixin.FormatOptionsProperty(
                    csv=databrew_mixins.CfnDatasetPropsMixin.CsvOptionsProperty(
                        delimiter="delimiter",
                        header_row=False
                    ),
                    excel=databrew_mixins.CfnDatasetPropsMixin.ExcelOptionsProperty(
                        header_row=False,
                        sheet_indexes=[123],
                        sheet_names=["sheetNames"]
                    ),
                    json=databrew_mixins.CfnDatasetPropsMixin.JsonOptionsProperty(
                        multi_line=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fb9cb3a28b0b0804fc7f035be105b89c60e017bef8cffa433fff01563fa25f6f)
                check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
                check_type(argname="argument excel", value=excel, expected_type=type_hints["excel"])
                check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv is not None:
                self._values["csv"] = csv
            if excel is not None:
                self._values["excel"] = excel
            if json is not None:
                self._values["json"] = json

        @builtins.property
        def csv(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.CsvOptionsProperty"]]:
            '''Options that define how CSV input is to be interpreted by DataBrew.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-formatoptions.html#cfn-databrew-dataset-formatoptions-csv
            '''
            result = self._values.get("csv")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.CsvOptionsProperty"]], result)

        @builtins.property
        def excel(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ExcelOptionsProperty"]]:
            '''Options that define how Excel input is to be interpreted by DataBrew.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-formatoptions.html#cfn-databrew-dataset-formatoptions-excel
            '''
            result = self._values.get("excel")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.ExcelOptionsProperty"]], result)

        @builtins.property
        def json(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.JsonOptionsProperty"]]:
            '''Options that define how JSON input is to be interpreted by DataBrew.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-formatoptions.html#cfn-databrew-dataset-formatoptions-json
            '''
            result = self._values.get("json")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.JsonOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FormatOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.InputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_input_definition": "databaseInputDefinition",
            "data_catalog_input_definition": "dataCatalogInputDefinition",
            "metadata": "metadata",
            "s3_input_definition": "s3InputDefinition",
        },
    )
    class InputProperty:
        def __init__(
            self,
            *,
            database_input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatabaseInputDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_catalog_input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.MetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents information on how DataBrew can find data, in either the AWS Glue Data Catalog or Amazon S3.

            :param database_input_definition: Connection information for dataset input files stored in a database.
            :param data_catalog_input_definition: The AWS Glue Data Catalog parameters for the data.
            :param metadata: Contains additional resource information needed for specific datasets.
            :param s3_input_definition: The Amazon S3 location where the data is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-input.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                input_property = databrew_mixins.CfnDatasetPropsMixin.InputProperty(
                    database_input_definition=databrew_mixins.CfnDatasetPropsMixin.DatabaseInputDefinitionProperty(
                        database_table_name="databaseTableName",
                        glue_connection_name="glueConnectionName",
                        query_string="queryString",
                        temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    data_catalog_input_definition=databrew_mixins.CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        table_name="tableName",
                        temp_directory=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    metadata=databrew_mixins.CfnDatasetPropsMixin.MetadataProperty(
                        source_arn="sourceArn"
                    ),
                    s3_input_definition=databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e0fb3a46c593a06ebaf0d711c86f989a59162c128605f00ce0552c64e54b01f)
                check_type(argname="argument database_input_definition", value=database_input_definition, expected_type=type_hints["database_input_definition"])
                check_type(argname="argument data_catalog_input_definition", value=data_catalog_input_definition, expected_type=type_hints["data_catalog_input_definition"])
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument s3_input_definition", value=s3_input_definition, expected_type=type_hints["s3_input_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_input_definition is not None:
                self._values["database_input_definition"] = database_input_definition
            if data_catalog_input_definition is not None:
                self._values["data_catalog_input_definition"] = data_catalog_input_definition
            if metadata is not None:
                self._values["metadata"] = metadata
            if s3_input_definition is not None:
                self._values["s3_input_definition"] = s3_input_definition

        @builtins.property
        def database_input_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatabaseInputDefinitionProperty"]]:
            '''Connection information for dataset input files stored in a database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-input.html#cfn-databrew-dataset-input-databaseinputdefinition
            '''
            result = self._values.get("database_input_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatabaseInputDefinitionProperty"]], result)

        @builtins.property
        def data_catalog_input_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty"]]:
            '''The AWS Glue Data Catalog parameters for the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-input.html#cfn-databrew-dataset-input-datacataloginputdefinition
            '''
            result = self._values.get("data_catalog_input_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty"]], result)

        @builtins.property
        def metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.MetadataProperty"]]:
            '''Contains additional resource information needed for specific datasets.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-input.html#cfn-databrew-dataset-input-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.MetadataProperty"]], result)

        @builtins.property
        def s3_input_definition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3LocationProperty"]]:
            '''The Amazon S3 location where the data is stored.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-input.html#cfn-databrew-dataset-input-s3inputdefinition
            '''
            result = self._values.get("s3_input_definition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.JsonOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"multi_line": "multiLine"},
    )
    class JsonOptionsProperty:
        def __init__(
            self,
            *,
            multi_line: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Represents the JSON-specific options that define how input is to be interpreted by AWS Glue DataBrew .

            :param multi_line: A value that specifies whether JSON input contains embedded new line characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-jsonoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                json_options_property = databrew_mixins.CfnDatasetPropsMixin.JsonOptionsProperty(
                    multi_line=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2b56424ceeb01c65c56a2f3561a58ac22e5ca94625ae27ac1d3116698a38e23e)
                check_type(argname="argument multi_line", value=multi_line, expected_type=type_hints["multi_line"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if multi_line is not None:
                self._values["multi_line"] = multi_line

        @builtins.property
        def multi_line(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies whether JSON input contains embedded new line characters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-jsonoptions.html#cfn-databrew-dataset-jsonoptions-multiline
            '''
            result = self._values.get("multi_line")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JsonOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.MetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"source_arn": "sourceArn"},
    )
    class MetadataProperty:
        def __init__(self, *, source_arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains additional resource information needed for specific datasets.

            :param source_arn: The Amazon Resource Name (ARN) associated with the dataset. Currently, DataBrew only supports ARNs from Amazon AppFlow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-metadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                metadata_property = databrew_mixins.CfnDatasetPropsMixin.MetadataProperty(
                    source_arn="sourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9798b689d4334fd3542d2192a33de38e53f4fccc9f31b6cadd57afad464e9c4b)
                check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_arn is not None:
                self._values["source_arn"] = source_arn

        @builtins.property
        def source_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) associated with the dataset.

            Currently, DataBrew only supports ARNs from Amazon AppFlow.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-metadata.html#cfn-databrew-dataset-metadata-sourcearn
            '''
            result = self._values.get("source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.PathOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "files_limit": "filesLimit",
            "last_modified_date_condition": "lastModifiedDateCondition",
            "parameters": "parameters",
        },
    )
    class PathOptionsProperty:
        def __init__(
            self,
            *,
            files_limit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.FilesLimitProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            last_modified_date_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.FilterExpressionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.PathParameterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents a set of options that define how DataBrew selects files for a given Amazon S3 path in a dataset.

            :param files_limit: If provided, this structure imposes a limit on a number of files that should be selected.
            :param last_modified_date_condition: If provided, this structure defines a date range for matching Amazon S3 objects based on their LastModifiedDate attribute in Amazon S3 .
            :param parameters: A structure that maps names of parameters used in the Amazon S3 path of a dataset to their definitions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                path_options_property = databrew_mixins.CfnDatasetPropsMixin.PathOptionsProperty(
                    files_limit=databrew_mixins.CfnDatasetPropsMixin.FilesLimitProperty(
                        max_files=123,
                        order="order",
                        ordered_by="orderedBy"
                    ),
                    last_modified_date_condition=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                        expression="expression",
                        values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                            value="value",
                            value_reference="valueReference"
                        )]
                    ),
                    parameters=[databrew_mixins.CfnDatasetPropsMixin.PathParameterProperty(
                        dataset_parameter=databrew_mixins.CfnDatasetPropsMixin.DatasetParameterProperty(
                            create_column=False,
                            datetime_options=databrew_mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty(
                                format="format",
                                locale_code="localeCode",
                                timezone_offset="timezoneOffset"
                            ),
                            filter=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                                expression="expression",
                                values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                                    value="value",
                                    value_reference="valueReference"
                                )]
                            ),
                            name="name",
                            type="type"
                        ),
                        path_parameter_name="pathParameterName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94ed326a7800dca90c00dcf4e33a6937f731a00f568bd6f039be0ef40227e9f3)
                check_type(argname="argument files_limit", value=files_limit, expected_type=type_hints["files_limit"])
                check_type(argname="argument last_modified_date_condition", value=last_modified_date_condition, expected_type=type_hints["last_modified_date_condition"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if files_limit is not None:
                self._values["files_limit"] = files_limit
            if last_modified_date_condition is not None:
                self._values["last_modified_date_condition"] = last_modified_date_condition
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def files_limit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilesLimitProperty"]]:
            '''If provided, this structure imposes a limit on a number of files that should be selected.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathoptions.html#cfn-databrew-dataset-pathoptions-fileslimit
            '''
            result = self._values.get("files_limit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilesLimitProperty"]], result)

        @builtins.property
        def last_modified_date_condition(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterExpressionProperty"]]:
            '''If provided, this structure defines a date range for matching Amazon S3 objects based on their LastModifiedDate attribute in Amazon S3 .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathoptions.html#cfn-databrew-dataset-pathoptions-lastmodifieddatecondition
            '''
            result = self._values.get("last_modified_date_condition")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.FilterExpressionProperty"]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.PathParameterProperty"]]]]:
            '''A structure that maps names of parameters used in the Amazon S3 path of a dataset to their definitions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathoptions.html#cfn-databrew-dataset-pathoptions-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.PathParameterProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.PathParameterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dataset_parameter": "datasetParameter",
            "path_parameter_name": "pathParameterName",
        },
    )
    class PathParameterProperty:
        def __init__(
            self,
            *,
            dataset_parameter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDatasetPropsMixin.DatasetParameterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path_parameter_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a single entry in the path parameters of a dataset.

            Each ``PathParameter`` consists of a name and a parameter definition.

            :param dataset_parameter: The path parameter definition.
            :param path_parameter_name: The name of the path parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathparameter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                path_parameter_property = databrew_mixins.CfnDatasetPropsMixin.PathParameterProperty(
                    dataset_parameter=databrew_mixins.CfnDatasetPropsMixin.DatasetParameterProperty(
                        create_column=False,
                        datetime_options=databrew_mixins.CfnDatasetPropsMixin.DatetimeOptionsProperty(
                            format="format",
                            locale_code="localeCode",
                            timezone_offset="timezoneOffset"
                        ),
                        filter=databrew_mixins.CfnDatasetPropsMixin.FilterExpressionProperty(
                            expression="expression",
                            values_map=[databrew_mixins.CfnDatasetPropsMixin.FilterValueProperty(
                                value="value",
                                value_reference="valueReference"
                            )]
                        ),
                        name="name",
                        type="type"
                    ),
                    path_parameter_name="pathParameterName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca4a5839ae4d73f90ab344404ddc32c1b19afe7c95099fe9292b334d4a925f28)
                check_type(argname="argument dataset_parameter", value=dataset_parameter, expected_type=type_hints["dataset_parameter"])
                check_type(argname="argument path_parameter_name", value=path_parameter_name, expected_type=type_hints["path_parameter_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataset_parameter is not None:
                self._values["dataset_parameter"] = dataset_parameter
            if path_parameter_name is not None:
                self._values["path_parameter_name"] = path_parameter_name

        @builtins.property
        def dataset_parameter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetParameterProperty"]]:
            '''The path parameter definition.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathparameter.html#cfn-databrew-dataset-pathparameter-datasetparameter
            '''
            result = self._values.get("dataset_parameter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDatasetPropsMixin.DatasetParameterProperty"]], result)

        @builtins.property
        def path_parameter_name(self) -> typing.Optional[builtins.str]:
            '''The name of the path parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-pathparameter.html#cfn-databrew-dataset-pathparameter-pathparametername
            '''
            result = self._values.get("path_parameter_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathParameterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnDatasetPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "bucket_owner": "bucketOwner", "key": "key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents an Amazon S3 location (bucket name, bucket owner, and object key) where DataBrew can read input data, or write output from a job.

            :param bucket: The Amazon S3 bucket name.
            :param bucket_owner: The AWS account ID of the bucket owner.
            :param key: The unique name of the object in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                s3_location_property = databrew_mixins.CfnDatasetPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aca1a2049cfebe1041dfb5913fff398e5a340604400d7ce74e1190acdb97dcc1)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-s3location.html#cfn-databrew-dataset-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The AWS account ID of the bucket owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-s3location.html#cfn-databrew-dataset-s3location-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The unique name of the object in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-dataset-s3location.html#cfn-databrew-dataset-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_outputs": "databaseOutputs",
        "data_catalog_outputs": "dataCatalogOutputs",
        "dataset_name": "datasetName",
        "encryption_key_arn": "encryptionKeyArn",
        "encryption_mode": "encryptionMode",
        "job_sample": "jobSample",
        "log_subscription": "logSubscription",
        "max_capacity": "maxCapacity",
        "max_retries": "maxRetries",
        "name": "name",
        "output_location": "outputLocation",
        "outputs": "outputs",
        "profile_configuration": "profileConfiguration",
        "project_name": "projectName",
        "recipe": "recipe",
        "role_arn": "roleArn",
        "tags": "tags",
        "timeout": "timeout",
        "type": "type",
        "validation_configurations": "validationConfigurations",
    },
)
class CfnJobMixinProps:
    def __init__(
        self,
        *,
        database_outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.DatabaseOutputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        data_catalog_outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.DataCatalogOutputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        dataset_name: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
        encryption_mode: typing.Optional[builtins.str] = None,
        job_sample: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.JobSampleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        log_subscription: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        output_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.OutputLocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.OutputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        profile_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ProfileConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        recipe: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.RecipeProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        timeout: typing.Optional[jsii.Number] = None,
        type: typing.Optional[builtins.str] = None,
        validation_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ValidationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnJobPropsMixin.

        :param database_outputs: Represents a list of JDBC database output objects which defines the output destination for a DataBrew recipe job to write into.
        :param data_catalog_outputs: One or more artifacts that represent the AWS Glue Data Catalog output from running the job.
        :param dataset_name: A dataset that the job is to process.
        :param encryption_key_arn: The Amazon Resource Name (ARN) of an encryption key that is used to protect the job output. For more information, see `Encrypting data written by DataBrew jobs <https://docs.aws.amazon.com/databrew/latest/dg/encryption-security-configuration.html>`_
        :param encryption_mode: The encryption mode for the job, which can be one of the following:. - ``SSE-KMS`` - Server-side encryption with keys managed by AWS . - ``SSE-S3`` - Server-side encryption with keys managed by Amazon S3.
        :param job_sample: A sample configuration for profile jobs only, which determines the number of rows on which the profile job is run. If a ``JobSample`` value isn't provided, the default value is used. The default value is CUSTOM_ROWS for the mode parameter and 20,000 for the size parameter.
        :param log_subscription: The current status of Amazon CloudWatch logging for the job.
        :param max_capacity: The maximum number of nodes that can be consumed when the job processes data.
        :param max_retries: The maximum number of times to retry the job after a job run fails.
        :param name: The unique name of the job.
        :param output_location: The location in Amazon S3 where the job writes its output.
        :param outputs: One or more artifacts that represent output from running the job.
        :param profile_configuration: Configuration for profile jobs. Configuration can be used to select columns, do evaluations, and override default parameters of evaluations. When configuration is undefined, the profile job will apply default settings to all supported columns.
        :param project_name: The name of the project that the job is associated with.
        :param recipe: A series of data transformation steps that the job runs.
        :param role_arn: The Amazon Resource Name (ARN) of the role to be assumed for this job.
        :param tags: Metadata tags that have been applied to the job.
        :param timeout: The job's timeout in minutes. A job that attempts to run longer than this timeout period ends with a status of ``TIMEOUT`` .
        :param type: The job type of the job, which must be one of the following:. - ``PROFILE`` - A job to analyze a dataset, to determine its size, data types, data distribution, and more. - ``RECIPE`` - A job to apply one or more transformations to a dataset.
        :param validation_configurations: List of validation configurations that are applied to the profile job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
            
            cfn_job_mixin_props = databrew_mixins.CfnJobMixinProps(
                database_outputs=[databrew_mixins.CfnJobPropsMixin.DatabaseOutputProperty(
                    database_options=databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                        table_name="tableName",
                        temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    database_output_mode="databaseOutputMode",
                    glue_connection_name="glueConnectionName"
                )],
                data_catalog_outputs=[databrew_mixins.CfnJobPropsMixin.DataCatalogOutputProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    database_options=databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                        table_name="tableName",
                        temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    overwrite=False,
                    s3_options=databrew_mixins.CfnJobPropsMixin.S3TableOutputOptionsProperty(
                        location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    table_name="tableName"
                )],
                dataset_name="datasetName",
                encryption_key_arn="encryptionKeyArn",
                encryption_mode="encryptionMode",
                job_sample=databrew_mixins.CfnJobPropsMixin.JobSampleProperty(
                    mode="mode",
                    size=123
                ),
                log_subscription="logSubscription",
                max_capacity=123,
                max_retries=123,
                name="name",
                output_location=databrew_mixins.CfnJobPropsMixin.OutputLocationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    key="key"
                ),
                outputs=[databrew_mixins.CfnJobPropsMixin.OutputProperty(
                    compression_format="compressionFormat",
                    format="format",
                    format_options=databrew_mixins.CfnJobPropsMixin.OutputFormatOptionsProperty(
                        csv=databrew_mixins.CfnJobPropsMixin.CsvOutputOptionsProperty(
                            delimiter="delimiter"
                        )
                    ),
                    location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    ),
                    max_output_files=123,
                    overwrite=False,
                    partition_columns=["partitionColumns"]
                )],
                profile_configuration=databrew_mixins.CfnJobPropsMixin.ProfileConfigurationProperty(
                    column_statistics_configurations=[databrew_mixins.CfnJobPropsMixin.ColumnStatisticsConfigurationProperty(
                        selectors=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                            name="name",
                            regex="regex"
                        )],
                        statistics=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                            included_statistics=["includedStatistics"],
                            overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                                parameters={
                                    "parameters_key": "parameters"
                                },
                                statistic="statistic"
                            )]
                        )
                    )],
                    dataset_statistics_configuration=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                        included_statistics=["includedStatistics"],
                        overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                            parameters={
                                "parameters_key": "parameters"
                            },
                            statistic="statistic"
                        )]
                    ),
                    entity_detector_configuration=databrew_mixins.CfnJobPropsMixin.EntityDetectorConfigurationProperty(
                        allowed_statistics=databrew_mixins.CfnJobPropsMixin.AllowedStatisticsProperty(
                            statistics=["statistics"]
                        ),
                        entity_types=["entityTypes"]
                    ),
                    profile_columns=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                        name="name",
                        regex="regex"
                    )]
                ),
                project_name="projectName",
                recipe=databrew_mixins.CfnJobPropsMixin.RecipeProperty(
                    name="name",
                    version="version"
                ),
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                timeout=123,
                type="type",
                validation_configurations=[databrew_mixins.CfnJobPropsMixin.ValidationConfigurationProperty(
                    ruleset_arn="rulesetArn",
                    validation_mode="validationMode"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84df583f5478f15f2d41d1372bd6cc295bcd006aab73101d9e496d75e85eca74)
            check_type(argname="argument database_outputs", value=database_outputs, expected_type=type_hints["database_outputs"])
            check_type(argname="argument data_catalog_outputs", value=data_catalog_outputs, expected_type=type_hints["data_catalog_outputs"])
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
            check_type(argname="argument encryption_mode", value=encryption_mode, expected_type=type_hints["encryption_mode"])
            check_type(argname="argument job_sample", value=job_sample, expected_type=type_hints["job_sample"])
            check_type(argname="argument log_subscription", value=log_subscription, expected_type=type_hints["log_subscription"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument output_location", value=output_location, expected_type=type_hints["output_location"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument profile_configuration", value=profile_configuration, expected_type=type_hints["profile_configuration"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument recipe", value=recipe, expected_type=type_hints["recipe"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument validation_configurations", value=validation_configurations, expected_type=type_hints["validation_configurations"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_outputs is not None:
            self._values["database_outputs"] = database_outputs
        if data_catalog_outputs is not None:
            self._values["data_catalog_outputs"] = data_catalog_outputs
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if encryption_key_arn is not None:
            self._values["encryption_key_arn"] = encryption_key_arn
        if encryption_mode is not None:
            self._values["encryption_mode"] = encryption_mode
        if job_sample is not None:
            self._values["job_sample"] = job_sample
        if log_subscription is not None:
            self._values["log_subscription"] = log_subscription
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if name is not None:
            self._values["name"] = name
        if output_location is not None:
            self._values["output_location"] = output_location
        if outputs is not None:
            self._values["outputs"] = outputs
        if profile_configuration is not None:
            self._values["profile_configuration"] = profile_configuration
        if project_name is not None:
            self._values["project_name"] = project_name
        if recipe is not None:
            self._values["recipe"] = recipe
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if type is not None:
            self._values["type"] = type
        if validation_configurations is not None:
            self._values["validation_configurations"] = validation_configurations

    @builtins.property
    def database_outputs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DatabaseOutputProperty"]]]]:
        '''Represents a list of JDBC database output objects which defines the output destination for a DataBrew recipe job to write into.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-databaseoutputs
        '''
        result = self._values.get("database_outputs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DatabaseOutputProperty"]]]], result)

    @builtins.property
    def data_catalog_outputs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DataCatalogOutputProperty"]]]]:
        '''One or more artifacts that represent the AWS Glue Data Catalog output from running the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-datacatalogoutputs
        '''
        result = self._values.get("data_catalog_outputs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DataCatalogOutputProperty"]]]], result)

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''A dataset that the job is to process.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-datasetname
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of an encryption key that is used to protect the job output.

        For more information, see `Encrypting data written by DataBrew jobs <https://docs.aws.amazon.com/databrew/latest/dg/encryption-security-configuration.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-encryptionkeyarn
        '''
        result = self._values.get("encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_mode(self) -> typing.Optional[builtins.str]:
        '''The encryption mode for the job, which can be one of the following:.

        - ``SSE-KMS`` - Server-side encryption with keys managed by AWS  .
        - ``SSE-S3`` - Server-side encryption with keys managed by Amazon S3.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-encryptionmode
        '''
        result = self._values.get("encryption_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_sample(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.JobSampleProperty"]]:
        '''A sample configuration for profile jobs only, which determines the number of rows on which the profile job is run.

        If a ``JobSample`` value isn't provided, the default value is used. The default value is CUSTOM_ROWS for the mode parameter and 20,000 for the size parameter.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-jobsample
        '''
        result = self._values.get("job_sample")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.JobSampleProperty"]], result)

    @builtins.property
    def log_subscription(self) -> typing.Optional[builtins.str]:
        '''The current status of Amazon CloudWatch logging for the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-logsubscription
        '''
        result = self._values.get("log_subscription")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of nodes that can be consumed when the job processes data.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-maxcapacity
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry the job after a job run fails.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-maxretries
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name of the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_location(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.OutputLocationProperty"]]:
        '''The location in Amazon S3 where the job writes its output.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-outputlocation
        '''
        result = self._values.get("output_location")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.OutputLocationProperty"]], result)

    @builtins.property
    def outputs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.OutputProperty"]]]]:
        '''One or more artifacts that represent output from running the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-outputs
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.OutputProperty"]]]], result)

    @builtins.property
    def profile_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ProfileConfigurationProperty"]]:
        '''Configuration for profile jobs.

        Configuration can be used to select columns, do evaluations, and override default parameters of evaluations. When configuration is undefined, the profile job will apply default settings to all supported columns.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-profileconfiguration
        '''
        result = self._values.get("profile_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ProfileConfigurationProperty"]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''The name of the project that the job is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-projectname
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipe(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.RecipeProperty"]]:
        '''A series of data transformation steps that the job runs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-recipe
        '''
        result = self._values.get("recipe")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.RecipeProperty"]], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role to be assumed for this job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata tags that have been applied to the job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[jsii.Number]:
        '''The job's timeout in minutes.

        A job that attempts to run longer than this timeout period ends with a status of ``TIMEOUT`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The job type of the job, which must be one of the following:.

        - ``PROFILE`` - A job to analyze a dataset, to determine its size, data types, data distribution, and more.
        - ``RECIPE`` - A job to apply one or more transformations to a dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validation_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ValidationConfigurationProperty"]]]]:
        '''List of validation configurations that are applied to the profile job.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html#cfn-databrew-job-validationconfigurations
        '''
        result = self._values.get("validation_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ValidationConfigurationProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnJobPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin",
):
    '''Specifies a new DataBrew job.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-job.html
    :cloudformationResource: AWS::DataBrew::Job
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
        
        cfn_job_props_mixin = databrew_mixins.CfnJobPropsMixin(databrew_mixins.CfnJobMixinProps(
            database_outputs=[databrew_mixins.CfnJobPropsMixin.DatabaseOutputProperty(
                database_options=databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                    table_name="tableName",
                    temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                ),
                database_output_mode="databaseOutputMode",
                glue_connection_name="glueConnectionName"
            )],
            data_catalog_outputs=[databrew_mixins.CfnJobPropsMixin.DataCatalogOutputProperty(
                catalog_id="catalogId",
                database_name="databaseName",
                database_options=databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                    table_name="tableName",
                    temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                ),
                overwrite=False,
                s3_options=databrew_mixins.CfnJobPropsMixin.S3TableOutputOptionsProperty(
                    location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                ),
                table_name="tableName"
            )],
            dataset_name="datasetName",
            encryption_key_arn="encryptionKeyArn",
            encryption_mode="encryptionMode",
            job_sample=databrew_mixins.CfnJobPropsMixin.JobSampleProperty(
                mode="mode",
                size=123
            ),
            log_subscription="logSubscription",
            max_capacity=123,
            max_retries=123,
            name="name",
            output_location=databrew_mixins.CfnJobPropsMixin.OutputLocationProperty(
                bucket="bucket",
                bucket_owner="bucketOwner",
                key="key"
            ),
            outputs=[databrew_mixins.CfnJobPropsMixin.OutputProperty(
                compression_format="compressionFormat",
                format="format",
                format_options=databrew_mixins.CfnJobPropsMixin.OutputFormatOptionsProperty(
                    csv=databrew_mixins.CfnJobPropsMixin.CsvOutputOptionsProperty(
                        delimiter="delimiter"
                    )
                ),
                location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    key="key"
                ),
                max_output_files=123,
                overwrite=False,
                partition_columns=["partitionColumns"]
            )],
            profile_configuration=databrew_mixins.CfnJobPropsMixin.ProfileConfigurationProperty(
                column_statistics_configurations=[databrew_mixins.CfnJobPropsMixin.ColumnStatisticsConfigurationProperty(
                    selectors=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                        name="name",
                        regex="regex"
                    )],
                    statistics=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                        included_statistics=["includedStatistics"],
                        overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                            parameters={
                                "parameters_key": "parameters"
                            },
                            statistic="statistic"
                        )]
                    )
                )],
                dataset_statistics_configuration=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                    included_statistics=["includedStatistics"],
                    overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                        parameters={
                            "parameters_key": "parameters"
                        },
                        statistic="statistic"
                    )]
                ),
                entity_detector_configuration=databrew_mixins.CfnJobPropsMixin.EntityDetectorConfigurationProperty(
                    allowed_statistics=databrew_mixins.CfnJobPropsMixin.AllowedStatisticsProperty(
                        statistics=["statistics"]
                    ),
                    entity_types=["entityTypes"]
                ),
                profile_columns=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                    name="name",
                    regex="regex"
                )]
            ),
            project_name="projectName",
            recipe=databrew_mixins.CfnJobPropsMixin.RecipeProperty(
                name="name",
                version="version"
            ),
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            timeout=123,
            type="type",
            validation_configurations=[databrew_mixins.CfnJobPropsMixin.ValidationConfigurationProperty(
                ruleset_arn="rulesetArn",
                validation_mode="validationMode"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnJobMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataBrew::Job``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc3ae97865bd3e7154165989507375f8d168cb47ebcfa43da54733350ef32d83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62a5f5fdcd345105ecfd099a51b6355c69e1a79b5852fc040fc88febdc3b9364)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9cbfec3ea049dedb89d100f317bf305b05957c1d579fd60c935d7a473831a0)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnJobMixinProps:
        return typing.cast(CfnJobMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.AllowedStatisticsProperty",
        jsii_struct_bases=[],
        name_mapping={"statistics": "statistics"},
    )
    class AllowedStatisticsProperty:
        def __init__(
            self,
            *,
            statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration of statistics that are allowed to be run on columns that contain detected entities.

            When undefined, no statistics will be computed on columns that contain detected entities.

            :param statistics: One or more column statistics to allow for columns that contain detected entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-allowedstatistics.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                allowed_statistics_property = databrew_mixins.CfnJobPropsMixin.AllowedStatisticsProperty(
                    statistics=["statistics"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d2f05263dee92a6877276ed6aee8300ebd748c370752c3cf0d896f12e1188f7)
                check_type(argname="argument statistics", value=statistics, expected_type=type_hints["statistics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if statistics is not None:
                self._values["statistics"] = statistics

        @builtins.property
        def statistics(self) -> typing.Optional[typing.List[builtins.str]]:
            '''One or more column statistics to allow for columns that contain detected entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-allowedstatistics.html#cfn-databrew-job-allowedstatistics-statistics
            '''
            result = self._values.get("statistics")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AllowedStatisticsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.ColumnSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "regex": "regex"},
    )
    class ColumnSelectorProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            regex: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Selector of a column from a dataset for profile job configuration.

            One selector includes either a column name or a regular expression.

            :param name: The name of a column from a dataset.
            :param regex: A regular expression for selecting a column from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-columnselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                column_selector_property = databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                    name="name",
                    regex="regex"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcc3a4cdeed67724d4144296d54609e62bd8a570b10d72fca3c2900802cfc0c3)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if regex is not None:
                self._values["regex"] = regex

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a column from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-columnselector.html#cfn-databrew-job-columnselector-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for selecting a column from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-columnselector.html#cfn-databrew-job-columnselector-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.ColumnStatisticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"selectors": "selectors", "statistics": "statistics"},
    )
    class ColumnStatisticsConfigurationProperty:
        def __init__(
            self,
            *,
            selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ColumnSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            statistics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.StatisticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Configuration for column evaluations for a profile job.

            ColumnStatisticsConfiguration can be used to select evaluations and override parameters of evaluations for particular columns.

            :param selectors: List of column selectors. Selectors can be used to select columns from the dataset. When selectors are undefined, configuration will be applied to all supported columns.
            :param statistics: Configuration for evaluations. Statistics can be used to select evaluations and override parameters of evaluations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-columnstatisticsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                column_statistics_configuration_property = databrew_mixins.CfnJobPropsMixin.ColumnStatisticsConfigurationProperty(
                    selectors=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                        name="name",
                        regex="regex"
                    )],
                    statistics=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                        included_statistics=["includedStatistics"],
                        overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                            parameters={
                                "parameters_key": "parameters"
                            },
                            statistic="statistic"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6246721ae8baff7d08ac19d69bbdc9448e8e8d9862ac186f35d6bfd78aa69bdd)
                check_type(argname="argument selectors", value=selectors, expected_type=type_hints["selectors"])
                check_type(argname="argument statistics", value=statistics, expected_type=type_hints["statistics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if selectors is not None:
                self._values["selectors"] = selectors
            if statistics is not None:
                self._values["statistics"] = statistics

        @builtins.property
        def selectors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ColumnSelectorProperty"]]]]:
            '''List of column selectors.

            Selectors can be used to select columns from the dataset. When selectors are undefined, configuration will be applied to all supported columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-columnstatisticsconfiguration.html#cfn-databrew-job-columnstatisticsconfiguration-selectors
            '''
            result = self._values.get("selectors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ColumnSelectorProperty"]]]], result)

        @builtins.property
        def statistics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.StatisticsConfigurationProperty"]]:
            '''Configuration for evaluations.

            Statistics can be used to select evaluations and override parameters of evaluations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-columnstatisticsconfiguration.html#cfn-databrew-job-columnstatisticsconfiguration-statistics
            '''
            result = self._values.get("statistics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.StatisticsConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnStatisticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.CsvOutputOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"delimiter": "delimiter"},
    )
    class CsvOutputOptionsProperty:
        def __init__(self, *, delimiter: typing.Optional[builtins.str] = None) -> None:
            '''Represents a set of options that define how DataBrew will write a comma-separated value (CSV) file.

            :param delimiter: A single character that specifies the delimiter used to create CSV job output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-csvoutputoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                csv_output_options_property = databrew_mixins.CfnJobPropsMixin.CsvOutputOptionsProperty(
                    delimiter="delimiter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cd05dd61d0ab62613b80eee1967fa9a1693ff1d56f2b3b68f32e99a18a760227)
                check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delimiter is not None:
                self._values["delimiter"] = delimiter

        @builtins.property
        def delimiter(self) -> typing.Optional[builtins.str]:
            '''A single character that specifies the delimiter used to create CSV job output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-csvoutputoptions.html#cfn-databrew-job-csvoutputoptions-delimiter
            '''
            result = self._values.get("delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CsvOutputOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.DataCatalogOutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "database_options": "databaseOptions",
            "overwrite": "overwrite",
            "s3_options": "s3Options",
            "table_name": "tableName",
        },
    )
    class DataCatalogOutputProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            database_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.DatabaseTableOutputOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            overwrite: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            s3_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.S3TableOutputOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents options that specify how and where in the AWS Glue Data Catalog DataBrew writes the output generated by recipe jobs.

            :param catalog_id: The unique identifier of the AWS account that holds the Data Catalog that stores the data.
            :param database_name: The name of a database in the Data Catalog.
            :param database_options: Represents options that specify how and where DataBrew writes the database output generated by recipe jobs.
            :param overwrite: A value that, if true, means that any data in the location specified for output is overwritten with new output. Not supported with DatabaseOptions.
            :param s3_options: Represents options that specify how and where DataBrew writes the Amazon S3 output generated by recipe jobs.
            :param table_name: The name of a table in the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                data_catalog_output_property = databrew_mixins.CfnJobPropsMixin.DataCatalogOutputProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    database_options=databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                        table_name="tableName",
                        temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    overwrite=False,
                    s3_options=databrew_mixins.CfnJobPropsMixin.S3TableOutputOptionsProperty(
                        location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c056e5c9bd67b68bc334e93b6089914de70e44881b6dd847d8f704540fe42b83)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument database_options", value=database_options, expected_type=type_hints["database_options"])
                check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
                check_type(argname="argument s3_options", value=s3_options, expected_type=type_hints["s3_options"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if database_options is not None:
                self._values["database_options"] = database_options
            if overwrite is not None:
                self._values["overwrite"] = overwrite
            if s3_options is not None:
                self._values["s3_options"] = s3_options
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier of the AWS account that holds the Data Catalog that stores the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html#cfn-databrew-job-datacatalogoutput-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of a database in the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html#cfn-databrew-job-datacatalogoutput-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DatabaseTableOutputOptionsProperty"]]:
            '''Represents options that specify how and where DataBrew writes the database output generated by recipe jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html#cfn-databrew-job-datacatalogoutput-databaseoptions
            '''
            result = self._values.get("database_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DatabaseTableOutputOptionsProperty"]], result)

        @builtins.property
        def overwrite(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that, if true, means that any data in the location specified for output is overwritten with new output.

            Not supported with DatabaseOptions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html#cfn-databrew-job-datacatalogoutput-overwrite
            '''
            result = self._values.get("overwrite")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def s3_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3TableOutputOptionsProperty"]]:
            '''Represents options that specify how and where DataBrew writes the Amazon S3 output generated by recipe jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html#cfn-databrew-job-datacatalogoutput-s3options
            '''
            result = self._values.get("s3_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3TableOutputOptionsProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of a table in the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-datacatalogoutput.html#cfn-databrew-job-datacatalogoutput-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataCatalogOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.DatabaseOutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_options": "databaseOptions",
            "database_output_mode": "databaseOutputMode",
            "glue_connection_name": "glueConnectionName",
        },
    )
    class DatabaseOutputProperty:
        def __init__(
            self,
            *,
            database_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.DatabaseTableOutputOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_output_mode: typing.Optional[builtins.str] = None,
            glue_connection_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents a JDBC database output object which defines the output destination for a DataBrew recipe job to write into.

            :param database_options: Represents options that specify how and where DataBrew writes the database output generated by recipe jobs.
            :param database_output_mode: The output mode to write into the database. Currently supported option: NEW_TABLE.
            :param glue_connection_name: The AWS Glue connection that stores the connection information for the target database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databaseoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                database_output_property = databrew_mixins.CfnJobPropsMixin.DatabaseOutputProperty(
                    database_options=databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                        table_name="tableName",
                        temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                            bucket="bucket",
                            bucket_owner="bucketOwner",
                            key="key"
                        )
                    ),
                    database_output_mode="databaseOutputMode",
                    glue_connection_name="glueConnectionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c4855366ffaf0b4b88eded6bdb428b5ddc80df57d9f18cd066a8f5128cc5607)
                check_type(argname="argument database_options", value=database_options, expected_type=type_hints["database_options"])
                check_type(argname="argument database_output_mode", value=database_output_mode, expected_type=type_hints["database_output_mode"])
                check_type(argname="argument glue_connection_name", value=glue_connection_name, expected_type=type_hints["glue_connection_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_options is not None:
                self._values["database_options"] = database_options
            if database_output_mode is not None:
                self._values["database_output_mode"] = database_output_mode
            if glue_connection_name is not None:
                self._values["glue_connection_name"] = glue_connection_name

        @builtins.property
        def database_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DatabaseTableOutputOptionsProperty"]]:
            '''Represents options that specify how and where DataBrew writes the database output generated by recipe jobs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databaseoutput.html#cfn-databrew-job-databaseoutput-databaseoptions
            '''
            result = self._values.get("database_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.DatabaseTableOutputOptionsProperty"]], result)

        @builtins.property
        def database_output_mode(self) -> typing.Optional[builtins.str]:
            '''The output mode to write into the database.

            Currently supported option: NEW_TABLE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databaseoutput.html#cfn-databrew-job-databaseoutput-databaseoutputmode
            '''
            result = self._values.get("database_output_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def glue_connection_name(self) -> typing.Optional[builtins.str]:
            '''The AWS Glue connection that stores the connection information for the target database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databaseoutput.html#cfn-databrew-job-databaseoutput-glueconnectionname
            '''
            result = self._values.get("glue_connection_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"table_name": "tableName", "temp_directory": "tempDirectory"},
    )
    class DatabaseTableOutputOptionsProperty:
        def __init__(
            self,
            *,
            table_name: typing.Optional[builtins.str] = None,
            temp_directory: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents options that specify how and where DataBrew writes the database output generated by recipe jobs.

            :param table_name: A prefix for the name of a table DataBrew will create in the database.
            :param temp_directory: Represents an Amazon S3 location (bucket name and object key) where DataBrew can store intermediate results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databasetableoutputoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                database_table_output_options_property = databrew_mixins.CfnJobPropsMixin.DatabaseTableOutputOptionsProperty(
                    table_name="tableName",
                    temp_directory=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03ed3bf6e161a524f2b5c83f38670a6722c2956d19151514e74ec3af8394660c)
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
                check_type(argname="argument temp_directory", value=temp_directory, expected_type=type_hints["temp_directory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if table_name is not None:
                self._values["table_name"] = table_name
            if temp_directory is not None:
                self._values["temp_directory"] = temp_directory

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''A prefix for the name of a table DataBrew will create in the database.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databasetableoutputoptions.html#cfn-databrew-job-databasetableoutputoptions-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def temp_directory(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3LocationProperty"]]:
            '''Represents an Amazon S3 location (bucket name and object key) where DataBrew can store intermediate results.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-databasetableoutputoptions.html#cfn-databrew-job-databasetableoutputoptions-tempdirectory
            '''
            result = self._values.get("temp_directory")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseTableOutputOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.EntityDetectorConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allowed_statistics": "allowedStatistics",
            "entity_types": "entityTypes",
        },
    )
    class EntityDetectorConfigurationProperty:
        def __init__(
            self,
            *,
            allowed_statistics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.AllowedStatisticsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            entity_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Configuration of entity detection for a profile job.

            When undefined, entity detection is disabled.

            :param allowed_statistics: Configuration of statistics that are allowed to be run on columns that contain detected entities. When undefined, no statistics will be computed on columns that contain detected entities.
            :param entity_types: Entity types to detect. Can be any of the following:. - USA_SSN - EMAIL - USA_ITIN - USA_PASSPORT_NUMBER - PHONE_NUMBER - USA_DRIVING_LICENSE - BANK_ACCOUNT - CREDIT_CARD - IP_ADDRESS - MAC_ADDRESS - USA_DEA_NUMBER - USA_HCPCS_CODE - USA_NATIONAL_PROVIDER_IDENTIFIER - USA_NATIONAL_DRUG_CODE - USA_HEALTH_INSURANCE_CLAIM_NUMBER - USA_MEDICARE_BENEFICIARY_IDENTIFIER - USA_CPT_CODE - PERSON_NAME - DATE The Entity type group USA_ALL is also supported, and includes all of the above entity types except PERSON_NAME and DATE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-entitydetectorconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                entity_detector_configuration_property = databrew_mixins.CfnJobPropsMixin.EntityDetectorConfigurationProperty(
                    allowed_statistics=databrew_mixins.CfnJobPropsMixin.AllowedStatisticsProperty(
                        statistics=["statistics"]
                    ),
                    entity_types=["entityTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98b18375f2ebdb0f36bf7340feb56c7c25dfc36b272edc674766a0d09c061f08)
                check_type(argname="argument allowed_statistics", value=allowed_statistics, expected_type=type_hints["allowed_statistics"])
                check_type(argname="argument entity_types", value=entity_types, expected_type=type_hints["entity_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if allowed_statistics is not None:
                self._values["allowed_statistics"] = allowed_statistics
            if entity_types is not None:
                self._values["entity_types"] = entity_types

        @builtins.property
        def allowed_statistics(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.AllowedStatisticsProperty"]]:
            '''Configuration of statistics that are allowed to be run on columns that contain detected entities.

            When undefined, no statistics will be computed on columns that contain detected entities.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-entitydetectorconfiguration.html#cfn-databrew-job-entitydetectorconfiguration-allowedstatistics
            '''
            result = self._values.get("allowed_statistics")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.AllowedStatisticsProperty"]], result)

        @builtins.property
        def entity_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Entity types to detect. Can be any of the following:.

            - USA_SSN
            - EMAIL
            - USA_ITIN
            - USA_PASSPORT_NUMBER
            - PHONE_NUMBER
            - USA_DRIVING_LICENSE
            - BANK_ACCOUNT
            - CREDIT_CARD
            - IP_ADDRESS
            - MAC_ADDRESS
            - USA_DEA_NUMBER
            - USA_HCPCS_CODE
            - USA_NATIONAL_PROVIDER_IDENTIFIER
            - USA_NATIONAL_DRUG_CODE
            - USA_HEALTH_INSURANCE_CLAIM_NUMBER
            - USA_MEDICARE_BENEFICIARY_IDENTIFIER
            - USA_CPT_CODE
            - PERSON_NAME
            - DATE

            The Entity type group USA_ALL is also supported, and includes all of the above entity types except PERSON_NAME and DATE.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-entitydetectorconfiguration.html#cfn-databrew-job-entitydetectorconfiguration-entitytypes
            '''
            result = self._values.get("entity_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntityDetectorConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.JobSampleProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode", "size": "size"},
    )
    class JobSampleProperty:
        def __init__(
            self,
            *,
            mode: typing.Optional[builtins.str] = None,
            size: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A sample configuration for profile jobs only, which determines the number of rows on which the profile job is run.

            If a ``JobSample`` value isn't provided, the default is used. The default value is CUSTOM_ROWS for the mode parameter and 20,000 for the size parameter.

            :param mode: A value that determines whether the profile job is run on the entire dataset or a specified number of rows. This value must be one of the following: - FULL_DATASET - The profile job is run on the entire dataset. - CUSTOM_ROWS - The profile job is run on the number of rows specified in the ``Size`` parameter.
            :param size: The ``Size`` parameter is only required when the mode is CUSTOM_ROWS. The profile job is run on the specified number of rows. The maximum value for size is Long.MAX_VALUE. Long.MAX_VALUE = 9223372036854775807

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-jobsample.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                job_sample_property = databrew_mixins.CfnJobPropsMixin.JobSampleProperty(
                    mode="mode",
                    size=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcd189c544201f87d17763c74321ccee091137a0cee9535bd715078c50f1f673)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mode is not None:
                self._values["mode"] = mode
            if size is not None:
                self._values["size"] = size

        @builtins.property
        def mode(self) -> typing.Optional[builtins.str]:
            '''A value that determines whether the profile job is run on the entire dataset or a specified number of rows.

            This value must be one of the following:

            - FULL_DATASET - The profile job is run on the entire dataset.
            - CUSTOM_ROWS - The profile job is run on the number of rows specified in the ``Size`` parameter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-jobsample.html#cfn-databrew-job-jobsample-mode
            '''
            result = self._values.get("mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The ``Size`` parameter is only required when the mode is CUSTOM_ROWS.

            The profile job is run on the specified number of rows. The maximum value for size is Long.MAX_VALUE.

            Long.MAX_VALUE = 9223372036854775807

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-jobsample.html#cfn-databrew-job-jobsample-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JobSampleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.OutputFormatOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"csv": "csv"},
    )
    class OutputFormatOptionsProperty:
        def __init__(
            self,
            *,
            csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.CsvOutputOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents a set of options that define the structure of comma-separated (CSV) job output.

            :param csv: Represents a set of options that define the structure of comma-separated value (CSV) job output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-outputformatoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                output_format_options_property = databrew_mixins.CfnJobPropsMixin.OutputFormatOptionsProperty(
                    csv=databrew_mixins.CfnJobPropsMixin.CsvOutputOptionsProperty(
                        delimiter="delimiter"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f0610c17b906852a51abd6f00e02caff1a543f08dff082a9abed393749f0154)
                check_type(argname="argument csv", value=csv, expected_type=type_hints["csv"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv is not None:
                self._values["csv"] = csv

        @builtins.property
        def csv(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.CsvOutputOptionsProperty"]]:
            '''Represents a set of options that define the structure of comma-separated value (CSV) job output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-outputformatoptions.html#cfn-databrew-job-outputformatoptions-csv
            '''
            result = self._values.get("csv")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.CsvOutputOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputFormatOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.OutputLocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "bucket_owner": "bucketOwner", "key": "key"},
    )
    class OutputLocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The location in Amazon S3 or AWS Glue Data Catalog where the job writes its output.

            :param bucket: The Amazon S3 bucket name.
            :param bucket_owner: 
            :param key: The unique name of the object in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-outputlocation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                output_location_property = databrew_mixins.CfnJobPropsMixin.OutputLocationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a79763da5ac5ae187122eba5e1c48af80287391e5495c5b8060c9ce4ed329a9)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-outputlocation.html#cfn-databrew-job-outputlocation-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-outputlocation.html#cfn-databrew-job-outputlocation-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The unique name of the object in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-outputlocation.html#cfn-databrew-job-outputlocation-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputLocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compression_format": "compressionFormat",
            "format": "format",
            "format_options": "formatOptions",
            "location": "location",
            "max_output_files": "maxOutputFiles",
            "overwrite": "overwrite",
            "partition_columns": "partitionColumns",
        },
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            compression_format: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
            format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.OutputFormatOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_output_files: typing.Optional[jsii.Number] = None,
            overwrite: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            partition_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Represents options that specify how and where in Amazon S3 DataBrew writes the output generated by recipe jobs or profile jobs.

            :param compression_format: The compression algorithm used to compress the output text of the job.
            :param format: The data format of the output of the job.
            :param format_options: Represents options that define how DataBrew formats job output files.
            :param location: The location in Amazon S3 where the job writes its output.
            :param max_output_files: The maximum number of files to be generated by the job and written to the output folder.
            :param overwrite: A value that, if true, means that any data in the location specified for output is overwritten with new output.
            :param partition_columns: The names of one or more partition columns for the output of the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                output_property = databrew_mixins.CfnJobPropsMixin.OutputProperty(
                    compression_format="compressionFormat",
                    format="format",
                    format_options=databrew_mixins.CfnJobPropsMixin.OutputFormatOptionsProperty(
                        csv=databrew_mixins.CfnJobPropsMixin.CsvOutputOptionsProperty(
                            delimiter="delimiter"
                        )
                    ),
                    location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    ),
                    max_output_files=123,
                    overwrite=False,
                    partition_columns=["partitionColumns"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__67e96978e0bc250d4dffebd54c9005ad3692306fee8897cb71fb4d5e6b3fbe44)
                check_type(argname="argument compression_format", value=compression_format, expected_type=type_hints["compression_format"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument format_options", value=format_options, expected_type=type_hints["format_options"])
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
                check_type(argname="argument max_output_files", value=max_output_files, expected_type=type_hints["max_output_files"])
                check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
                check_type(argname="argument partition_columns", value=partition_columns, expected_type=type_hints["partition_columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compression_format is not None:
                self._values["compression_format"] = compression_format
            if format is not None:
                self._values["format"] = format
            if format_options is not None:
                self._values["format_options"] = format_options
            if location is not None:
                self._values["location"] = location
            if max_output_files is not None:
                self._values["max_output_files"] = max_output_files
            if overwrite is not None:
                self._values["overwrite"] = overwrite
            if partition_columns is not None:
                self._values["partition_columns"] = partition_columns

        @builtins.property
        def compression_format(self) -> typing.Optional[builtins.str]:
            '''The compression algorithm used to compress the output text of the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-compressionformat
            '''
            result = self._values.get("compression_format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''The data format of the output of the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.OutputFormatOptionsProperty"]]:
            '''Represents options that define how DataBrew formats job output files.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-formatoptions
            '''
            result = self._values.get("format_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.OutputFormatOptionsProperty"]], result)

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3LocationProperty"]]:
            '''The location in Amazon S3 where the job writes its output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3LocationProperty"]], result)

        @builtins.property
        def max_output_files(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of files to be generated by the job and written to the output folder.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-maxoutputfiles
            '''
            result = self._values.get("max_output_files")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def overwrite(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that, if true, means that any data in the location specified for output is overwritten with new output.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-overwrite
            '''
            result = self._values.get("overwrite")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def partition_columns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The names of one or more partition columns for the output of the job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-output.html#cfn-databrew-job-output-partitioncolumns
            '''
            result = self._values.get("partition_columns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.ProfileConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "column_statistics_configurations": "columnStatisticsConfigurations",
            "dataset_statistics_configuration": "datasetStatisticsConfiguration",
            "entity_detector_configuration": "entityDetectorConfiguration",
            "profile_columns": "profileColumns",
        },
    )
    class ProfileConfigurationProperty:
        def __init__(
            self,
            *,
            column_statistics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ColumnStatisticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            dataset_statistics_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.StatisticsConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            entity_detector_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.EntityDetectorConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            profile_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.ColumnSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration for profile jobs.

            Configuration can be used to select columns, do evaluations, and override default parameters of evaluations. When configuration is undefined, the profile job will apply default settings to all supported columns.

            :param column_statistics_configurations: List of configurations for column evaluations. ColumnStatisticsConfigurations are used to select evaluations and override parameters of evaluations for particular columns. When ColumnStatisticsConfigurations is undefined, the profile job will profile all supported columns and run all supported evaluations.
            :param dataset_statistics_configuration: Configuration for inter-column evaluations. Configuration can be used to select evaluations and override parameters of evaluations. When configuration is undefined, the profile job will run all supported inter-column evaluations.
            :param entity_detector_configuration: Configuration of entity detection for a profile job. When undefined, entity detection is disabled.
            :param profile_columns: List of column selectors. ProfileColumns can be used to select columns from the dataset. When ProfileColumns is undefined, the profile job will profile all supported columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-profileconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                profile_configuration_property = databrew_mixins.CfnJobPropsMixin.ProfileConfigurationProperty(
                    column_statistics_configurations=[databrew_mixins.CfnJobPropsMixin.ColumnStatisticsConfigurationProperty(
                        selectors=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                            name="name",
                            regex="regex"
                        )],
                        statistics=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                            included_statistics=["includedStatistics"],
                            overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                                parameters={
                                    "parameters_key": "parameters"
                                },
                                statistic="statistic"
                            )]
                        )
                    )],
                    dataset_statistics_configuration=databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                        included_statistics=["includedStatistics"],
                        overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                            parameters={
                                "parameters_key": "parameters"
                            },
                            statistic="statistic"
                        )]
                    ),
                    entity_detector_configuration=databrew_mixins.CfnJobPropsMixin.EntityDetectorConfigurationProperty(
                        allowed_statistics=databrew_mixins.CfnJobPropsMixin.AllowedStatisticsProperty(
                            statistics=["statistics"]
                        ),
                        entity_types=["entityTypes"]
                    ),
                    profile_columns=[databrew_mixins.CfnJobPropsMixin.ColumnSelectorProperty(
                        name="name",
                        regex="regex"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28b1a7f4e87cf4119874b4288f017a1b063be509a05e141b92786c0e9668c0ee)
                check_type(argname="argument column_statistics_configurations", value=column_statistics_configurations, expected_type=type_hints["column_statistics_configurations"])
                check_type(argname="argument dataset_statistics_configuration", value=dataset_statistics_configuration, expected_type=type_hints["dataset_statistics_configuration"])
                check_type(argname="argument entity_detector_configuration", value=entity_detector_configuration, expected_type=type_hints["entity_detector_configuration"])
                check_type(argname="argument profile_columns", value=profile_columns, expected_type=type_hints["profile_columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_statistics_configurations is not None:
                self._values["column_statistics_configurations"] = column_statistics_configurations
            if dataset_statistics_configuration is not None:
                self._values["dataset_statistics_configuration"] = dataset_statistics_configuration
            if entity_detector_configuration is not None:
                self._values["entity_detector_configuration"] = entity_detector_configuration
            if profile_columns is not None:
                self._values["profile_columns"] = profile_columns

        @builtins.property
        def column_statistics_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ColumnStatisticsConfigurationProperty"]]]]:
            '''List of configurations for column evaluations.

            ColumnStatisticsConfigurations are used to select evaluations and override parameters of evaluations for particular columns. When ColumnStatisticsConfigurations is undefined, the profile job will profile all supported columns and run all supported evaluations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-profileconfiguration.html#cfn-databrew-job-profileconfiguration-columnstatisticsconfigurations
            '''
            result = self._values.get("column_statistics_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ColumnStatisticsConfigurationProperty"]]]], result)

        @builtins.property
        def dataset_statistics_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.StatisticsConfigurationProperty"]]:
            '''Configuration for inter-column evaluations.

            Configuration can be used to select evaluations and override parameters of evaluations. When configuration is undefined, the profile job will run all supported inter-column evaluations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-profileconfiguration.html#cfn-databrew-job-profileconfiguration-datasetstatisticsconfiguration
            '''
            result = self._values.get("dataset_statistics_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.StatisticsConfigurationProperty"]], result)

        @builtins.property
        def entity_detector_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.EntityDetectorConfigurationProperty"]]:
            '''Configuration of entity detection for a profile job.

            When undefined, entity detection is disabled.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-profileconfiguration.html#cfn-databrew-job-profileconfiguration-entitydetectorconfiguration
            '''
            result = self._values.get("entity_detector_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.EntityDetectorConfigurationProperty"]], result)

        @builtins.property
        def profile_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ColumnSelectorProperty"]]]]:
            '''List of column selectors.

            ProfileColumns can be used to select columns from the dataset. When ProfileColumns is undefined, the profile job will profile all supported columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-profileconfiguration.html#cfn-databrew-job-profileconfiguration-profilecolumns
            '''
            result = self._values.get("profile_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.ColumnSelectorProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProfileConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.RecipeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "version": "version"},
    )
    class RecipeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents one or more actions to be performed on a DataBrew dataset.

            :param name: The unique name for the recipe.
            :param version: The identifier for the version for the recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-recipe.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                recipe_property = databrew_mixins.CfnJobPropsMixin.RecipeProperty(
                    name="name",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d3e247536a8b293798aba3515f7a73aa01d66292635a7651b78e9bf689c60f9b)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The unique name for the recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-recipe.html#cfn-databrew-job-recipe-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The identifier for the version for the recipe.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-recipe.html#cfn-databrew-job-recipe-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.S3LocationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket": "bucket", "bucket_owner": "bucketOwner", "key": "key"},
    )
    class S3LocationProperty:
        def __init__(
            self,
            *,
            bucket: typing.Optional[builtins.str] = None,
            bucket_owner: typing.Optional[builtins.str] = None,
            key: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents an Amazon S3 location (bucket name, bucket owner, and object key) where DataBrew can read input data, or write output from a job.

            :param bucket: The Amazon S3 bucket name.
            :param bucket_owner: The AWS account ID of the bucket owner.
            :param key: The unique name of the object in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                s3_location_property = databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                    bucket="bucket",
                    bucket_owner="bucketOwner",
                    key="key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5e368163b635c7536dccd6f4fb6b0e528679d96e2fd3d1fd11bbf6faff454206)
                check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
                check_type(argname="argument bucket_owner", value=bucket_owner, expected_type=type_hints["bucket_owner"])
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket is not None:
                self._values["bucket"] = bucket
            if bucket_owner is not None:
                self._values["bucket_owner"] = bucket_owner
            if key is not None:
                self._values["key"] = key

        @builtins.property
        def bucket(self) -> typing.Optional[builtins.str]:
            '''The Amazon S3 bucket name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html#cfn-databrew-job-s3location-bucket
            '''
            result = self._values.get("bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bucket_owner(self) -> typing.Optional[builtins.str]:
            '''The AWS account ID of the bucket owner.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html#cfn-databrew-job-s3location-bucketowner
            '''
            result = self._values.get("bucket_owner")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The unique name of the object in the bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3location.html#cfn-databrew-job-s3location-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3LocationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.S3TableOutputOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"location": "location"},
    )
    class S3TableOutputOptionsProperty:
        def __init__(
            self,
            *,
            location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.S3LocationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents options that specify how and where DataBrew writes the Amazon S3 output generated by recipe jobs.

            :param location: Represents an Amazon S3 location (bucket name and object key) where DataBrew can write output from a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3tableoutputoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                s3_table_output_options_property = databrew_mixins.CfnJobPropsMixin.S3TableOutputOptionsProperty(
                    location=databrew_mixins.CfnJobPropsMixin.S3LocationProperty(
                        bucket="bucket",
                        bucket_owner="bucketOwner",
                        key="key"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bbe2655ab1376c38e247f87d6a5b5a80c823316977dca9650f5d7b751329d9d0)
                check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if location is not None:
                self._values["location"] = location

        @builtins.property
        def location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3LocationProperty"]]:
            '''Represents an Amazon S3 location (bucket name and object key) where DataBrew can write output from a job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-s3tableoutputoptions.html#cfn-databrew-job-s3tableoutputoptions-location
            '''
            result = self._values.get("location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.S3LocationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3TableOutputOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.StatisticOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"parameters": "parameters", "statistic": "statistic"},
    )
    class StatisticOverrideProperty:
        def __init__(
            self,
            *,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
            statistic: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Override of a particular evaluation for a profile job.

            :param parameters: A map that includes overrides of an evaluation’s parameters.
            :param statistic: The name of an evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-statisticoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                statistic_override_property = databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                    parameters={
                        "parameters_key": "parameters"
                    },
                    statistic="statistic"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__491407575dcff3b4bb3ed51ce3b25e47e423d7aa998adc82f367600ee9945033)
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument statistic", value=statistic, expected_type=type_hints["statistic"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if parameters is not None:
                self._values["parameters"] = parameters
            if statistic is not None:
                self._values["statistic"] = statistic

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''A map that includes overrides of an evaluation’s parameters.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-statisticoverride.html#cfn-databrew-job-statisticoverride-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def statistic(self) -> typing.Optional[builtins.str]:
            '''The name of an evaluation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-statisticoverride.html#cfn-databrew-job-statisticoverride-statistic
            '''
            result = self._values.get("statistic")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatisticOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.StatisticsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "included_statistics": "includedStatistics",
            "overrides": "overrides",
        },
    )
    class StatisticsConfigurationProperty:
        def __init__(
            self,
            *,
            included_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
            overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnJobPropsMixin.StatisticOverrideProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configuration of evaluations for a profile job.

            This configuration can be used to select evaluations and override the parameters of selected evaluations.

            :param included_statistics: List of included evaluations. When the list is undefined, all supported evaluations will be included.
            :param overrides: List of overrides for evaluations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-statisticsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                statistics_configuration_property = databrew_mixins.CfnJobPropsMixin.StatisticsConfigurationProperty(
                    included_statistics=["includedStatistics"],
                    overrides=[databrew_mixins.CfnJobPropsMixin.StatisticOverrideProperty(
                        parameters={
                            "parameters_key": "parameters"
                        },
                        statistic="statistic"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__03206af021d2e3138c3c250e7cc50cebf7c10a8e6732c6ea78b703420a10a095)
                check_type(argname="argument included_statistics", value=included_statistics, expected_type=type_hints["included_statistics"])
                check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if included_statistics is not None:
                self._values["included_statistics"] = included_statistics
            if overrides is not None:
                self._values["overrides"] = overrides

        @builtins.property
        def included_statistics(self) -> typing.Optional[typing.List[builtins.str]]:
            '''List of included evaluations.

            When the list is undefined, all supported evaluations will be included.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-statisticsconfiguration.html#cfn-databrew-job-statisticsconfiguration-includedstatistics
            '''
            result = self._values.get("included_statistics")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def overrides(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.StatisticOverrideProperty"]]]]:
            '''List of overrides for evaluations.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-statisticsconfiguration.html#cfn-databrew-job-statisticsconfiguration-overrides
            '''
            result = self._values.get("overrides")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnJobPropsMixin.StatisticOverrideProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatisticsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnJobPropsMixin.ValidationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ruleset_arn": "rulesetArn",
            "validation_mode": "validationMode",
        },
    )
    class ValidationConfigurationProperty:
        def __init__(
            self,
            *,
            ruleset_arn: typing.Optional[builtins.str] = None,
            validation_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration for data quality validation.

            Used to select the Rulesets and Validation Mode to be used in the profile job. When ValidationConfiguration is null, the profile job will run without data quality validation.

            :param ruleset_arn: The Amazon Resource Name (ARN) for the ruleset to be validated in the profile job. The TargetArn of the selected ruleset should be the same as the Amazon Resource Name (ARN) of the dataset that is associated with the profile job.
            :param validation_mode: Mode of data quality validation. Default mode is “CHECK_ALL” which verifies all rules defined in the selected ruleset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-validationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                validation_configuration_property = databrew_mixins.CfnJobPropsMixin.ValidationConfigurationProperty(
                    ruleset_arn="rulesetArn",
                    validation_mode="validationMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9ddec38e98cbe1204a848f4adc30c2effe2c9e879f80473caad04c4477139d06)
                check_type(argname="argument ruleset_arn", value=ruleset_arn, expected_type=type_hints["ruleset_arn"])
                check_type(argname="argument validation_mode", value=validation_mode, expected_type=type_hints["validation_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ruleset_arn is not None:
                self._values["ruleset_arn"] = ruleset_arn
            if validation_mode is not None:
                self._values["validation_mode"] = validation_mode

        @builtins.property
        def ruleset_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for the ruleset to be validated in the profile job.

            The TargetArn of the selected ruleset should be the same as the Amazon Resource Name (ARN) of the dataset that is associated with the profile job.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-validationconfiguration.html#cfn-databrew-job-validationconfiguration-rulesetarn
            '''
            result = self._values.get("ruleset_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def validation_mode(self) -> typing.Optional[builtins.str]:
            '''Mode of data quality validation.

            Default mode is “CHECK_ALL” which verifies all rules defined in the selected ruleset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-job-validationconfiguration.html#cfn-databrew-job-validationconfiguration-validationmode
            '''
            result = self._values.get("validation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnProjectMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataset_name": "datasetName",
        "name": "name",
        "recipe_name": "recipeName",
        "role_arn": "roleArn",
        "sample": "sample",
        "tags": "tags",
    },
)
class CfnProjectMixinProps:
    def __init__(
        self,
        *,
        dataset_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recipe_name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        sample: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnProjectPropsMixin.SampleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnProjectPropsMixin.

        :param dataset_name: The dataset that the project is to act upon.
        :param name: The unique name of a project.
        :param recipe_name: The name of a recipe that will be developed during a project session.
        :param role_arn: The Amazon Resource Name (ARN) of the role that will be assumed for this project.
        :param sample: The sample size and sampling type to apply to the data. If this parameter isn't specified, then the sample consists of the first 500 rows from the dataset.
        :param tags: Metadata tags that have been applied to the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
            
            cfn_project_mixin_props = databrew_mixins.CfnProjectMixinProps(
                dataset_name="datasetName",
                name="name",
                recipe_name="recipeName",
                role_arn="roleArn",
                sample=databrew_mixins.CfnProjectPropsMixin.SampleProperty(
                    size=123,
                    type="type"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32e2cc0d5f230193680959fa33bd407641dc188660edb36f86ffeabdca1391d)
            check_type(argname="argument dataset_name", value=dataset_name, expected_type=type_hints["dataset_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recipe_name", value=recipe_name, expected_type=type_hints["recipe_name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument sample", value=sample, expected_type=type_hints["sample"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dataset_name is not None:
            self._values["dataset_name"] = dataset_name
        if name is not None:
            self._values["name"] = name
        if recipe_name is not None:
            self._values["recipe_name"] = recipe_name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if sample is not None:
            self._values["sample"] = sample
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataset_name(self) -> typing.Optional[builtins.str]:
        '''The dataset that the project is to act upon.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-datasetname
        '''
        result = self._values.get("dataset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name of a project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipe_name(self) -> typing.Optional[builtins.str]:
        '''The name of a recipe that will be developed during a project session.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-recipename
        '''
        result = self._values.get("recipe_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the role that will be assumed for this project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SampleProperty"]]:
        '''The sample size and sampling type to apply to the data.

        If this parameter isn't specified, then the sample consists of the first 500 rows from the dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-sample
        '''
        result = self._values.get("sample")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnProjectPropsMixin.SampleProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata tags that have been applied to the project.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html#cfn-databrew-project-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProjectMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnProjectPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnProjectPropsMixin",
):
    '''Specifies a new AWS Glue DataBrew project.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-project.html
    :cloudformationResource: AWS::DataBrew::Project
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
        
        cfn_project_props_mixin = databrew_mixins.CfnProjectPropsMixin(databrew_mixins.CfnProjectMixinProps(
            dataset_name="datasetName",
            name="name",
            recipe_name="recipeName",
            role_arn="roleArn",
            sample=databrew_mixins.CfnProjectPropsMixin.SampleProperty(
                size=123,
                type="type"
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
        props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataBrew::Project``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59d83c216248a7a62fa73f1c509a9fe3fd85973f31036fc4e904f3b7274403d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bea4ebadea25d06b83b9fa5caede4761d2c5699854f114a820ccc83e884eec81)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0d7a3d5e7f3f7ce6fbd6618e77b4d6c7564b9054986cb8a5b422f2e4ad15941)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnProjectMixinProps:
        return typing.cast(CfnProjectMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnProjectPropsMixin.SampleProperty",
        jsii_struct_bases=[],
        name_mapping={"size": "size", "type": "type"},
    )
    class SampleProperty:
        def __init__(
            self,
            *,
            size: typing.Optional[jsii.Number] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents the sample size and sampling type for DataBrew to use for interactive data analysis.

            :param size: The number of rows in the sample.
            :param type: The way in which DataBrew obtains rows from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-project-sample.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                sample_property = databrew_mixins.CfnProjectPropsMixin.SampleProperty(
                    size=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2f47506b7746b974ed46beb37c413c13e61a3bd256005a4fb9a5841780d52e65)
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if size is not None:
                self._values["size"] = size
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The number of rows in the sample.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-project-sample.html#cfn-databrew-project-sample-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The way in which DataBrew obtains rows from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-project-sample.html#cfn-databrew-project-sample-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SampleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRecipeMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "steps": "steps",
        "tags": "tags",
    },
)
class CfnRecipeMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecipePropsMixin.RecipeStepProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnRecipePropsMixin.

        :param description: The description of the recipe.
        :param name: The unique name for the recipe.
        :param steps: A list of steps that are defined by the recipe.
        :param tags: Metadata tags that have been applied to the recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
            
            cfn_recipe_mixin_props = databrew_mixins.CfnRecipeMixinProps(
                description="description",
                name="name",
                steps=[databrew_mixins.CfnRecipePropsMixin.RecipeStepProperty(
                    action=databrew_mixins.CfnRecipePropsMixin.ActionProperty(
                        operation="operation",
                        parameters={
                            "parameters_key": "parameters"
                        }
                    ),
                    condition_expressions=[databrew_mixins.CfnRecipePropsMixin.ConditionExpressionProperty(
                        condition="condition",
                        target_column="targetColumn",
                        value="value"
                    )]
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194a64e22770ffe5c0afa528cf0f77aa66b5976ff171a2779e32a1a9eb6e07fe)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if steps is not None:
            self._values["steps"] = steps
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The unique name for the recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def steps(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecipePropsMixin.RecipeStepProperty"]]]]:
        '''A list of steps that are defined by the recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-steps
        '''
        result = self._values.get("steps")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecipePropsMixin.RecipeStepProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata tags that have been applied to the recipe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html#cfn-databrew-recipe-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecipeMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRecipePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRecipePropsMixin",
):
    '''Specifies a new AWS Glue DataBrew transformation recipe.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-recipe.html
    :cloudformationResource: AWS::DataBrew::Recipe
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
        
        cfn_recipe_props_mixin = databrew_mixins.CfnRecipePropsMixin(databrew_mixins.CfnRecipeMixinProps(
            description="description",
            name="name",
            steps=[databrew_mixins.CfnRecipePropsMixin.RecipeStepProperty(
                action=databrew_mixins.CfnRecipePropsMixin.ActionProperty(
                    operation="operation",
                    parameters={
                        "parameters_key": "parameters"
                    }
                ),
                condition_expressions=[databrew_mixins.CfnRecipePropsMixin.ConditionExpressionProperty(
                    condition="condition",
                    target_column="targetColumn",
                    value="value"
                )]
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
        props: typing.Union[CfnRecipeMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataBrew::Recipe``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b5942ca5f2407c194dc45dbf8eceffd6e0c57635201efc45645337539b36a5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b38581db9b51da228d899ef680dbbd815f08f6c4eb0a5877797313d919ebdc97)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81de91a4b5483e302d48029d85ae2cd6b5425c27b0e2d15ba9cf47cb7d196719)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRecipeMixinProps:
        return typing.cast(CfnRecipeMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRecipePropsMixin.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"operation": "operation", "parameters": "parameters"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            operation: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
        ) -> None:
            '''Represents a transformation and associated parameters that are used to apply a change to an AWS Glue DataBrew dataset.

            :param operation: The name of a valid DataBrew transformation to be performed on the data.
            :param parameters: Contextual parameters for the transformation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                action_property = databrew_mixins.CfnRecipePropsMixin.ActionProperty(
                    operation="operation",
                    parameters={
                        "parameters_key": "parameters"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53918d3ef3eb358bce3e1c174ca9669ca7bacb200b00e40dd734f8e7daabcffb)
                check_type(argname="argument operation", value=operation, expected_type=type_hints["operation"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if operation is not None:
                self._values["operation"] = operation
            if parameters is not None:
                self._values["parameters"] = parameters

        @builtins.property
        def operation(self) -> typing.Optional[builtins.str]:
            '''The name of a valid DataBrew transformation to be performed on the data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-action.html#cfn-databrew-recipe-action-operation
            '''
            result = self._values.get("operation")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]:
            '''Contextual parameters for the transformation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-action.html#cfn-databrew-recipe-action-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRecipePropsMixin.ConditionExpressionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "condition": "condition",
            "target_column": "targetColumn",
            "value": "value",
        },
    )
    class ConditionExpressionProperty:
        def __init__(
            self,
            *,
            condition: typing.Optional[builtins.str] = None,
            target_column: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Represents an individual condition that evaluates to true or false.

            Conditions are used with recipe actions. The action is only performed for column values where the condition evaluates to true.

            If a recipe requires more than one condition, then the recipe must specify multiple ``ConditionExpression`` elements. Each condition is applied to the rows in a dataset first, before the recipe action is performed.

            :param condition: A specific condition to apply to a recipe action. For more information, see `Recipe structure <https://docs.aws.amazon.com/databrew/latest/dg/recipe-structure.html>`_ in the *AWS Glue DataBrew Developer Guide* .
            :param target_column: A column to apply this condition to.
            :param value: A value that the condition must evaluate to for the condition to succeed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                condition_expression_property = databrew_mixins.CfnRecipePropsMixin.ConditionExpressionProperty(
                    condition="condition",
                    target_column="targetColumn",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42b03963b8e3f38c72476ec4f0f0f3c1001281eba569667fe76f6177942d6186)
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument target_column", value=target_column, expected_type=type_hints["target_column"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if condition is not None:
                self._values["condition"] = condition
            if target_column is not None:
                self._values["target_column"] = target_column
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''A specific condition to apply to a recipe action.

            For more information, see `Recipe structure <https://docs.aws.amazon.com/databrew/latest/dg/recipe-structure.html>`_ in the *AWS Glue DataBrew Developer Guide* .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html#cfn-databrew-recipe-conditionexpression-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def target_column(self) -> typing.Optional[builtins.str]:
            '''A column to apply this condition to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html#cfn-databrew-recipe-conditionexpression-targetcolumn
            '''
            result = self._values.get("target_column")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A value that the condition must evaluate to for the condition to succeed.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-conditionexpression.html#cfn-databrew-recipe-conditionexpression-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConditionExpressionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRecipePropsMixin.RecipeStepProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "condition_expressions": "conditionExpressions",
        },
    )
    class RecipeStepProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecipePropsMixin.ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            condition_expressions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRecipePropsMixin.ConditionExpressionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Represents a single step from a DataBrew recipe to be performed.

            :param action: The particular action to be performed in the recipe step.
            :param condition_expressions: One or more conditions that must be met for the recipe step to succeed. .. epigraph:: All of the conditions in the array must be met. In other words, all of the conditions must be combined using a logical AND operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipestep.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                recipe_step_property = databrew_mixins.CfnRecipePropsMixin.RecipeStepProperty(
                    action=databrew_mixins.CfnRecipePropsMixin.ActionProperty(
                        operation="operation",
                        parameters={
                            "parameters_key": "parameters"
                        }
                    ),
                    condition_expressions=[databrew_mixins.CfnRecipePropsMixin.ConditionExpressionProperty(
                        condition="condition",
                        target_column="targetColumn",
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d734ae90ad8f107a966e2bf60ed507214065c5d272d3872c9b97bb4fa53327b)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument condition_expressions", value=condition_expressions, expected_type=type_hints["condition_expressions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if condition_expressions is not None:
                self._values["condition_expressions"] = condition_expressions

        @builtins.property
        def action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecipePropsMixin.ActionProperty"]]:
            '''The particular action to be performed in the recipe step.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipestep.html#cfn-databrew-recipe-recipestep-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecipePropsMixin.ActionProperty"]], result)

        @builtins.property
        def condition_expressions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecipePropsMixin.ConditionExpressionProperty"]]]]:
            '''One or more conditions that must be met for the recipe step to succeed.

            .. epigraph::

               All of the conditions in the array must be met. In other words, all of the conditions must be combined using a logical AND operation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-recipe-recipestep.html#cfn-databrew-recipe-recipestep-conditionexpressions
            '''
            result = self._values.get("condition_expressions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRecipePropsMixin.ConditionExpressionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecipeStepProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRulesetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "rules": "rules",
        "tags": "tags",
        "target_arn": "targetArn",
    },
)
class CfnRulesetMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulesetPropsMixin.RuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnRulesetPropsMixin.

        :param description: The description of the ruleset.
        :param name: The name of the ruleset.
        :param rules: Contains metadata about the ruleset.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param target_arn: The Amazon Resource Name (ARN) of a resource (dataset) that the ruleset is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
            
            cfn_ruleset_mixin_props = databrew_mixins.CfnRulesetMixinProps(
                description="description",
                name="name",
                rules=[databrew_mixins.CfnRulesetPropsMixin.RuleProperty(
                    check_expression="checkExpression",
                    column_selectors=[databrew_mixins.CfnRulesetPropsMixin.ColumnSelectorProperty(
                        name="name",
                        regex="regex"
                    )],
                    disabled=False,
                    name="name",
                    substitution_map=[databrew_mixins.CfnRulesetPropsMixin.SubstitutionValueProperty(
                        value="value",
                        value_reference="valueReference"
                    )],
                    threshold=databrew_mixins.CfnRulesetPropsMixin.ThresholdProperty(
                        type="type",
                        unit="unit",
                        value=123
                    )
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_arn="targetArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2fc3b1d468aa801d2e96b551b7ca5d5cdfb0fdd0f033f9b69edb99a5e82e0d)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules
        if tags is not None:
            self._values["tags"] = tags
        if target_arn is not None:
            self._values["target_arn"] = target_arn

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the ruleset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html#cfn-databrew-ruleset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the ruleset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html#cfn-databrew-ruleset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.RuleProperty"]]]]:
        '''Contains metadata about the ruleset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html#cfn-databrew-ruleset-rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.RuleProperty"]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html#cfn-databrew-ruleset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def target_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of a resource (dataset) that the ruleset is associated with.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html#cfn-databrew-ruleset-targetarn
        '''
        result = self._values.get("target_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRulesetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnRulesetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRulesetPropsMixin",
):
    '''Specifies a new ruleset that can be used in a profile job to validate the data quality of a dataset.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-ruleset.html
    :cloudformationResource: AWS::DataBrew::Ruleset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
        
        cfn_ruleset_props_mixin = databrew_mixins.CfnRulesetPropsMixin(databrew_mixins.CfnRulesetMixinProps(
            description="description",
            name="name",
            rules=[databrew_mixins.CfnRulesetPropsMixin.RuleProperty(
                check_expression="checkExpression",
                column_selectors=[databrew_mixins.CfnRulesetPropsMixin.ColumnSelectorProperty(
                    name="name",
                    regex="regex"
                )],
                disabled=False,
                name="name",
                substitution_map=[databrew_mixins.CfnRulesetPropsMixin.SubstitutionValueProperty(
                    value="value",
                    value_reference="valueReference"
                )],
                threshold=databrew_mixins.CfnRulesetPropsMixin.ThresholdProperty(
                    type="type",
                    unit="unit",
                    value=123
                )
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_arn="targetArn"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnRulesetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataBrew::Ruleset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28f06f1300c570478e3f437b6066416c30408f0f32d21d1dd48a0cc91f6b4c29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85f6f15b6e3f881761dfbe77530f80a333d957fcc29716d24934128cd06a2da4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901b3a3d6ad5f98e44c6a977cda69411b250344135c5dee45e073f0d01aec281)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnRulesetMixinProps:
        return typing.cast(CfnRulesetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRulesetPropsMixin.ColumnSelectorProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "regex": "regex"},
    )
    class ColumnSelectorProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            regex: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Selector of a column from a dataset for profile job configuration.

            One selector includes either a column name or a regular expression.

            :param name: The name of a column from a dataset.
            :param regex: A regular expression for selecting a column from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-columnselector.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                column_selector_property = databrew_mixins.CfnRulesetPropsMixin.ColumnSelectorProperty(
                    name="name",
                    regex="regex"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8bc9700c10bae5334d69c3c8418346ad843d99553043390693c7cd58614e8517)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if regex is not None:
                self._values["regex"] = regex

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of a column from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-columnselector.html#cfn-databrew-ruleset-columnselector-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def regex(self) -> typing.Optional[builtins.str]:
            '''A regular expression for selecting a column from a dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-columnselector.html#cfn-databrew-ruleset-columnselector-regex
            '''
            result = self._values.get("regex")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnSelectorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRulesetPropsMixin.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "check_expression": "checkExpression",
            "column_selectors": "columnSelectors",
            "disabled": "disabled",
            "name": "name",
            "substitution_map": "substitutionMap",
            "threshold": "threshold",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            check_expression: typing.Optional[builtins.str] = None,
            column_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulesetPropsMixin.ColumnSelectorProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            substitution_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulesetPropsMixin.SubstitutionValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnRulesetPropsMixin.ThresholdProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Represents a single data quality requirement that should be validated in the scope of this dataset.

            :param check_expression: The expression which includes column references, condition names followed by variable references, possibly grouped and combined with other conditions. For example, ``(:col1 starts_with :prefix1 or :col1 starts_with :prefix2) and (:col1 ends_with :suffix1 or :col1 ends_with :suffix2)`` . Column and value references are substitution variables that should start with the ':' symbol. Depending on the context, substitution variables' values can be either an actual value or a column name. These values are defined in the SubstitutionMap. If a CheckExpression starts with a column reference, then ColumnSelectors in the rule should be null. If ColumnSelectors has been defined, then there should be no columnn reference in the left side of a condition, for example, ``is_between :val1 and :val2`` .
            :param column_selectors: List of column selectors. Selectors can be used to select columns using a name or regular expression from the dataset. Rule will be applied to selected columns.
            :param disabled: A value that specifies whether the rule is disabled. Once a rule is disabled, a profile job will not validate it during a job run. Default value is false.
            :param name: The name of the rule.
            :param substitution_map: The map of substitution variable names to their values used in a check expression. Variable names should start with a ':' (colon). Variable values can either be actual values or column names. To differentiate between the two, column names should be enclosed in backticks, for example, ``":col1": "``Column A``".``
            :param threshold: The threshold used with a non-aggregate check expression. Non-aggregate check expressions will be applied to each row in a specific column, and the threshold will be used to determine whether the validation succeeds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                rule_property = databrew_mixins.CfnRulesetPropsMixin.RuleProperty(
                    check_expression="checkExpression",
                    column_selectors=[databrew_mixins.CfnRulesetPropsMixin.ColumnSelectorProperty(
                        name="name",
                        regex="regex"
                    )],
                    disabled=False,
                    name="name",
                    substitution_map=[databrew_mixins.CfnRulesetPropsMixin.SubstitutionValueProperty(
                        value="value",
                        value_reference="valueReference"
                    )],
                    threshold=databrew_mixins.CfnRulesetPropsMixin.ThresholdProperty(
                        type="type",
                        unit="unit",
                        value=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2702498cb6ac0228365f39a2341355b13e7f5911f98b03ad273218a88391f078)
                check_type(argname="argument check_expression", value=check_expression, expected_type=type_hints["check_expression"])
                check_type(argname="argument column_selectors", value=column_selectors, expected_type=type_hints["column_selectors"])
                check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument substitution_map", value=substitution_map, expected_type=type_hints["substitution_map"])
                check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if check_expression is not None:
                self._values["check_expression"] = check_expression
            if column_selectors is not None:
                self._values["column_selectors"] = column_selectors
            if disabled is not None:
                self._values["disabled"] = disabled
            if name is not None:
                self._values["name"] = name
            if substitution_map is not None:
                self._values["substitution_map"] = substitution_map
            if threshold is not None:
                self._values["threshold"] = threshold

        @builtins.property
        def check_expression(self) -> typing.Optional[builtins.str]:
            '''The expression which includes column references, condition names followed by variable references, possibly grouped and combined with other conditions.

            For example, ``(:col1 starts_with :prefix1 or :col1 starts_with :prefix2) and (:col1 ends_with :suffix1 or :col1 ends_with :suffix2)`` . Column and value references are substitution variables that should start with the ':' symbol. Depending on the context, substitution variables' values can be either an actual value or a column name. These values are defined in the SubstitutionMap. If a CheckExpression starts with a column reference, then ColumnSelectors in the rule should be null. If ColumnSelectors has been defined, then there should be no columnn reference in the left side of a condition, for example, ``is_between :val1 and :val2`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html#cfn-databrew-ruleset-rule-checkexpression
            '''
            result = self._values.get("check_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_selectors(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.ColumnSelectorProperty"]]]]:
            '''List of column selectors.

            Selectors can be used to select columns using a name or regular expression from the dataset. Rule will be applied to selected columns.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html#cfn-databrew-ruleset-rule-columnselectors
            '''
            result = self._values.get("column_selectors")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.ColumnSelectorProperty"]]]], result)

        @builtins.property
        def disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
            '''A value that specifies whether the rule is disabled.

            Once a rule is disabled, a profile job will not validate it during a job run. Default value is false.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html#cfn-databrew-ruleset-rule-disabled
            '''
            result = self._values.get("disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the rule.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html#cfn-databrew-ruleset-rule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def substitution_map(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.SubstitutionValueProperty"]]]]:
            '''The map of substitution variable names to their values used in a check expression.

            Variable names should start with a ':' (colon). Variable values can either be actual values or column names. To differentiate between the two, column names should be enclosed in backticks, for example, ``":col1": "``Column A``".``

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html#cfn-databrew-ruleset-rule-substitutionmap
            '''
            result = self._values.get("substitution_map")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.SubstitutionValueProperty"]]]], result)

        @builtins.property
        def threshold(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.ThresholdProperty"]]:
            '''The threshold used with a non-aggregate check expression.

            Non-aggregate check expressions will be applied to each row in a specific column, and the threshold will be used to determine whether the validation succeeds.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-rule.html#cfn-databrew-ruleset-rule-threshold
            '''
            result = self._values.get("threshold")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnRulesetPropsMixin.ThresholdProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRulesetPropsMixin.SubstitutionValueProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value", "value_reference": "valueReference"},
    )
    class SubstitutionValueProperty:
        def __init__(
            self,
            *,
            value: typing.Optional[builtins.str] = None,
            value_reference: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A key-value pair to associate an expression's substitution variable names with their values.

            :param value: Value or column name.
            :param value_reference: Variable name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-substitutionvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                substitution_value_property = databrew_mixins.CfnRulesetPropsMixin.SubstitutionValueProperty(
                    value="value",
                    value_reference="valueReference"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__efd562b081daadc30eb8a2c550b3b3bbed5134488d7690562495df3c7467c17c)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
                check_type(argname="argument value_reference", value=value_reference, expected_type=type_hints["value_reference"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if value is not None:
                self._values["value"] = value
            if value_reference is not None:
                self._values["value_reference"] = value_reference

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''Value or column name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-substitutionvalue.html#cfn-databrew-ruleset-substitutionvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value_reference(self) -> typing.Optional[builtins.str]:
            '''Variable name.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-substitutionvalue.html#cfn-databrew-ruleset-substitutionvalue-valuereference
            '''
            result = self._values.get("value_reference")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubstitutionValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnRulesetPropsMixin.ThresholdProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "unit": "unit", "value": "value"},
    )
    class ThresholdProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            unit: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The threshold used with a non-aggregate check expression.

            The non-aggregate check expression will be applied to each row in a specific column. Then the threshold will be used to determine whether the validation succeeds.

            :param type: The type of a threshold. Used for comparison of an actual count of rows that satisfy the rule to the threshold value.
            :param unit: Unit of threshold value. Can be either a COUNT or PERCENTAGE of the full sample size used for validation.
            :param value: The value of a threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-threshold.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
                
                threshold_property = databrew_mixins.CfnRulesetPropsMixin.ThresholdProperty(
                    type="type",
                    unit="unit",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__363cd061156e5aa665a48f69bff5b2b7d3c6647ae5819b1cca33d756ced55b56)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument unit", value=unit, expected_type=type_hints["unit"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if unit is not None:
                self._values["unit"] = unit
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of a threshold.

            Used for comparison of an actual count of rows that satisfy the rule to the threshold value.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-threshold.html#cfn-databrew-ruleset-threshold-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unit(self) -> typing.Optional[builtins.str]:
            '''Unit of threshold value.

            Can be either a COUNT or PERCENTAGE of the full sample size used for validation.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-threshold.html#cfn-databrew-ruleset-threshold-unit
            '''
            result = self._values.get("unit")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of a threshold.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-databrew-ruleset-threshold.html#cfn-databrew-ruleset-threshold-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThresholdProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnScheduleMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "cron_expression": "cronExpression",
        "job_names": "jobNames",
        "name": "name",
        "tags": "tags",
    },
)
class CfnScheduleMixinProps:
    def __init__(
        self,
        *,
        cron_expression: typing.Optional[builtins.str] = None,
        job_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnSchedulePropsMixin.

        :param cron_expression: The dates and times when the job is to run. For more information, see `Working with cron expressions for recipe jobs <https://docs.aws.amazon.com/databrew/latest/dg/jobs.recipe.html#jobs.cron>`_ in the *AWS Glue DataBrew Developer Guide* .
        :param job_names: A list of jobs to be run, according to the schedule.
        :param name: The name of the schedule.
        :param tags: Metadata tags that have been applied to the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
            
            cfn_schedule_mixin_props = databrew_mixins.CfnScheduleMixinProps(
                cron_expression="cronExpression",
                job_names=["jobNames"],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d399fc1acb2327791a25953e95605b3399046523f1da4c59ca0247f4e0611a2c)
            check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
            check_type(argname="argument job_names", value=job_names, expected_type=type_hints["job_names"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cron_expression is not None:
            self._values["cron_expression"] = cron_expression
        if job_names is not None:
            self._values["job_names"] = job_names
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def cron_expression(self) -> typing.Optional[builtins.str]:
        '''The dates and times when the job is to run.

        For more information, see `Working with cron expressions for recipe jobs <https://docs.aws.amazon.com/databrew/latest/dg/jobs.recipe.html#jobs.cron>`_ in the *AWS Glue DataBrew Developer Guide* .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-cronexpression
        '''
        result = self._values.get("cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of jobs to be run, according to the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-jobnames
        '''
        result = self._values.get("job_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''Metadata tags that have been applied to the schedule.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html#cfn-databrew-schedule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnScheduleMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnSchedulePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_databrew.mixins.CfnSchedulePropsMixin",
):
    '''Specifies a new schedule for one or more AWS Glue DataBrew jobs.

    Jobs can be run at a specific date and time, or at regular intervals.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-databrew-schedule.html
    :cloudformationResource: AWS::DataBrew::Schedule
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_databrew import mixins as databrew_mixins
        
        cfn_schedule_props_mixin = databrew_mixins.CfnSchedulePropsMixin(databrew_mixins.CfnScheduleMixinProps(
            cron_expression="cronExpression",
            job_names=["jobNames"],
            name="name",
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
        props: typing.Union[CfnScheduleMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::DataBrew::Schedule``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff6c4e7021ddb288b3261e8656e675bc16be0824a477115c43ba947bd7fbd45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a39840c9a7d00587f279e90be458e0a0ee9f60517a8af9cf3e1eab53dd474e5e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44bdbd391029604ad99e525c7fce69f4704c9747f838bf79b2d27fb3e7c47be9)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnScheduleMixinProps:
        return typing.cast(CfnScheduleMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnDatasetMixinProps",
    "CfnDatasetPropsMixin",
    "CfnJobMixinProps",
    "CfnJobPropsMixin",
    "CfnProjectMixinProps",
    "CfnProjectPropsMixin",
    "CfnRecipeMixinProps",
    "CfnRecipePropsMixin",
    "CfnRulesetMixinProps",
    "CfnRulesetPropsMixin",
    "CfnScheduleMixinProps",
    "CfnSchedulePropsMixin",
]

publication.publish()

def _typecheckingstub__572029c63c693c197bca564ac00b49cc48704454f0a4e0e06decb8f668bd974f(
    *,
    format: typing.Optional[builtins.str] = None,
    format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.FormatOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.InputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    path_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.PathOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    source: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a88bc9e5d8a5c17b8c58aee9ca5785cdd181702cc2ea0db698ce7a030a1846(
    props: typing.Union[CfnDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f52fd6a312c516c0ba047c29271839ae93ee7a3c76dcecada00071df65e6c9a(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08be38015b6a453925d5acc83c7203063b06a66057e75c1502f54e391dd19fb(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37044d638c0fdbac004f87562d9c638ee6722f73fc0e83de9bb3aa4e53599fb8(
    *,
    delimiter: typing.Optional[builtins.str] = None,
    header_row: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d472f50d6302ca11e63c48e863f6392a6fb8d3c1ad9fc69673757fef28b4d386(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
    temp_directory: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277507f77544e137de410c5a528e6a96afffb12ea9f40d4ad9171dfbc747aba7(
    *,
    database_table_name: typing.Optional[builtins.str] = None,
    glue_connection_name: typing.Optional[builtins.str] = None,
    query_string: typing.Optional[builtins.str] = None,
    temp_directory: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2e85578646a1ed424a9a333d8a38da666077a9e7bea291f023ddb265c957931(
    *,
    create_column: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    datetime_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatetimeOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.FilterExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9c5ef567cbfc8b58b5ab0e177dd8e31b96d77317c559d0822c3c235bec9a06c(
    *,
    format: typing.Optional[builtins.str] = None,
    locale_code: typing.Optional[builtins.str] = None,
    timezone_offset: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceb0747143850b3edc4490f181e5de1c6c4d7243e0f281049c8b60a90bd5c836(
    *,
    header_row: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    sheet_indexes: typing.Optional[typing.Union[typing.Sequence[jsii.Number], _aws_cdk_ceddda9d.IResolvable]] = None,
    sheet_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a958430f9e0b57cc1ea47825f3aca32a163b97aba2c908d275cb2787dfb0a280(
    *,
    max_files: typing.Optional[jsii.Number] = None,
    order: typing.Optional[builtins.str] = None,
    ordered_by: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3c026466622cbf141686d83153af1ff2b90fb3977041baab4e055258ca38e3(
    *,
    expression: typing.Optional[builtins.str] = None,
    values_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.FilterValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff1379955d0f05517da830c52e6a33544911be512257e70c0d0ea56d67914f78(
    *,
    value: typing.Optional[builtins.str] = None,
    value_reference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9cb3a28b0b0804fc7f035be105b89c60e017bef8cffa433fff01563fa25f6f(
    *,
    csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.CsvOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    excel: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.ExcelOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.JsonOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0fb3a46c593a06ebaf0d711c86f989a59162c128605f00ce0552c64e54b01f(
    *,
    database_input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatabaseInputDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_catalog_input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DataCatalogInputDefinitionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    metadata: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.MetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_input_definition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b56424ceeb01c65c56a2f3561a58ac22e5ca94625ae27ac1d3116698a38e23e(
    *,
    multi_line: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9798b689d4334fd3542d2192a33de38e53f4fccc9f31b6cadd57afad464e9c4b(
    *,
    source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ed326a7800dca90c00dcf4e33a6937f731a00f568bd6f039be0ef40227e9f3(
    *,
    files_limit: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.FilesLimitProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    last_modified_date_condition: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.FilterExpressionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.PathParameterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca4a5839ae4d73f90ab344404ddc32c1b19afe7c95099fe9292b334d4a925f28(
    *,
    dataset_parameter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDatasetPropsMixin.DatasetParameterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path_parameter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aca1a2049cfebe1041dfb5913fff398e5a340604400d7ce74e1190acdb97dcc1(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84df583f5478f15f2d41d1372bd6cc295bcd006aab73101d9e496d75e85eca74(
    *,
    database_outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.DatabaseOutputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    data_catalog_outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.DataCatalogOutputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dataset_name: typing.Optional[builtins.str] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
    encryption_mode: typing.Optional[builtins.str] = None,
    job_sample: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.JobSampleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_subscription: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    output_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.OutputLocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    outputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.OutputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    profile_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ProfileConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_name: typing.Optional[builtins.str] = None,
    recipe: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.RecipeProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    timeout: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
    validation_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ValidationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc3ae97865bd3e7154165989507375f8d168cb47ebcfa43da54733350ef32d83(
    props: typing.Union[CfnJobMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a5f5fdcd345105ecfd099a51b6355c69e1a79b5852fc040fc88febdc3b9364(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9cbfec3ea049dedb89d100f317bf305b05957c1d579fd60c935d7a473831a0(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2f05263dee92a6877276ed6aee8300ebd748c370752c3cf0d896f12e1188f7(
    *,
    statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc3a4cdeed67724d4144296d54609e62bd8a570b10d72fca3c2900802cfc0c3(
    *,
    name: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6246721ae8baff7d08ac19d69bbdc9448e8e8d9862ac186f35d6bfd78aa69bdd(
    *,
    selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ColumnSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    statistics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.StatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd05dd61d0ab62613b80eee1967fa9a1693ff1d56f2b3b68f32e99a18a760227(
    *,
    delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c056e5c9bd67b68bc334e93b6089914de70e44881b6dd847d8f704540fe42b83(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    database_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.DatabaseTableOutputOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    overwrite: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    s3_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.S3TableOutputOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c4855366ffaf0b4b88eded6bdb428b5ddc80df57d9f18cd066a8f5128cc5607(
    *,
    database_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.DatabaseTableOutputOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_output_mode: typing.Optional[builtins.str] = None,
    glue_connection_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03ed3bf6e161a524f2b5c83f38670a6722c2956d19151514e74ec3af8394660c(
    *,
    table_name: typing.Optional[builtins.str] = None,
    temp_directory: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b18375f2ebdb0f36bf7340feb56c7c25dfc36b272edc674766a0d09c061f08(
    *,
    allowed_statistics: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.AllowedStatisticsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entity_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd189c544201f87d17763c74321ccee091137a0cee9535bd715078c50f1f673(
    *,
    mode: typing.Optional[builtins.str] = None,
    size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f0610c17b906852a51abd6f00e02caff1a543f08dff082a9abed393749f0154(
    *,
    csv: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.CsvOutputOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a79763da5ac5ae187122eba5e1c48af80287391e5495c5b8060c9ce4ed329a9(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67e96978e0bc250d4dffebd54c9005ad3692306fee8897cb71fb4d5e6b3fbe44(
    *,
    compression_format: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    format_options: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.OutputFormatOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_output_files: typing.Optional[jsii.Number] = None,
    overwrite: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    partition_columns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b1a7f4e87cf4119874b4288f017a1b063be509a05e141b92786c0e9668c0ee(
    *,
    column_statistics_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ColumnStatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dataset_statistics_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.StatisticsConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    entity_detector_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.EntityDetectorConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    profile_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.ColumnSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e247536a8b293798aba3515f7a73aa01d66292635a7651b78e9bf689c60f9b(
    *,
    name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e368163b635c7536dccd6f4fb6b0e528679d96e2fd3d1fd11bbf6faff454206(
    *,
    bucket: typing.Optional[builtins.str] = None,
    bucket_owner: typing.Optional[builtins.str] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe2655ab1376c38e247f87d6a5b5a80c823316977dca9650f5d7b751329d9d0(
    *,
    location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.S3LocationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491407575dcff3b4bb3ed51ce3b25e47e423d7aa998adc82f367600ee9945033(
    *,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
    statistic: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03206af021d2e3138c3c250e7cc50cebf7c10a8e6732c6ea78b703420a10a095(
    *,
    included_statistics: typing.Optional[typing.Sequence[builtins.str]] = None,
    overrides: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnJobPropsMixin.StatisticOverrideProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ddec38e98cbe1204a848f4adc30c2effe2c9e879f80473caad04c4477139d06(
    *,
    ruleset_arn: typing.Optional[builtins.str] = None,
    validation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32e2cc0d5f230193680959fa33bd407641dc188660edb36f86ffeabdca1391d(
    *,
    dataset_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    recipe_name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    sample: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnProjectPropsMixin.SampleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d83c216248a7a62fa73f1c509a9fe3fd85973f31036fc4e904f3b7274403d3(
    props: typing.Union[CfnProjectMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea4ebadea25d06b83b9fa5caede4761d2c5699854f114a820ccc83e884eec81(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0d7a3d5e7f3f7ce6fbd6618e77b4d6c7564b9054986cb8a5b422f2e4ad15941(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f47506b7746b974ed46beb37c413c13e61a3bd256005a4fb9a5841780d52e65(
    *,
    size: typing.Optional[jsii.Number] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194a64e22770ffe5c0afa528cf0f77aa66b5976ff171a2779e32a1a9eb6e07fe(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    steps: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecipePropsMixin.RecipeStepProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b5942ca5f2407c194dc45dbf8eceffd6e0c57635201efc45645337539b36a5d(
    props: typing.Union[CfnRecipeMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b38581db9b51da228d899ef680dbbd815f08f6c4eb0a5877797313d919ebdc97(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81de91a4b5483e302d48029d85ae2cd6b5425c27b0e2d15ba9cf47cb7d196719(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53918d3ef3eb358bce3e1c174ca9669ca7bacb200b00e40dd734f8e7daabcffb(
    *,
    operation: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b03963b8e3f38c72476ec4f0f0f3c1001281eba569667fe76f6177942d6186(
    *,
    condition: typing.Optional[builtins.str] = None,
    target_column: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d734ae90ad8f107a966e2bf60ed507214065c5d272d3872c9b97bb4fa53327b(
    *,
    action: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecipePropsMixin.ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    condition_expressions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRecipePropsMixin.ConditionExpressionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2fc3b1d468aa801d2e96b551b7ca5d5cdfb0fdd0f033f9b69edb99a5e82e0d(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulesetPropsMixin.RuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f06f1300c570478e3f437b6066416c30408f0f32d21d1dd48a0cc91f6b4c29(
    props: typing.Union[CfnRulesetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85f6f15b6e3f881761dfbe77530f80a333d957fcc29716d24934128cd06a2da4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901b3a3d6ad5f98e44c6a977cda69411b250344135c5dee45e073f0d01aec281(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc9700c10bae5334d69c3c8418346ad843d99553043390693c7cd58614e8517(
    *,
    name: typing.Optional[builtins.str] = None,
    regex: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2702498cb6ac0228365f39a2341355b13e7f5911f98b03ad273218a88391f078(
    *,
    check_expression: typing.Optional[builtins.str] = None,
    column_selectors: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulesetPropsMixin.ColumnSelectorProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    substitution_map: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulesetPropsMixin.SubstitutionValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    threshold: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnRulesetPropsMixin.ThresholdProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd562b081daadc30eb8a2c550b3b3bbed5134488d7690562495df3c7467c17c(
    *,
    value: typing.Optional[builtins.str] = None,
    value_reference: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363cd061156e5aa665a48f69bff5b2b7d3c6647ae5819b1cca33d756ced55b56(
    *,
    type: typing.Optional[builtins.str] = None,
    unit: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d399fc1acb2327791a25953e95605b3399046523f1da4c59ca0247f4e0611a2c(
    *,
    cron_expression: typing.Optional[builtins.str] = None,
    job_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff6c4e7021ddb288b3261e8656e675bc16be0824a477115c43ba947bd7fbd45(
    props: typing.Union[CfnScheduleMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39840c9a7d00587f279e90be458e0a0ee9f60517a8af9cf3e1eab53dd474e5e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bdbd391029604ad99e525c7fce69f4704c9747f838bf79b2d27fb3e7c47be9(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
