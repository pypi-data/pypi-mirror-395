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
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataCellsFilterMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "column_names": "columnNames",
        "column_wildcard": "columnWildcard",
        "database_name": "databaseName",
        "name": "name",
        "row_filter": "rowFilter",
        "table_catalog_id": "tableCatalogId",
        "table_name": "tableName",
    },
)
class CfnDataCellsFilterMixinProps:
    def __init__(
        self,
        *,
        column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        column_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataCellsFilterPropsMixin.ColumnWildcardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        database_name: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        row_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataCellsFilterPropsMixin.RowFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        table_catalog_id: typing.Optional[builtins.str] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for CfnDataCellsFilterPropsMixin.

        :param column_names: An array of UTF-8 strings. A list of column names.
        :param column_wildcard: A wildcard with exclusions. You must specify either a ``ColumnNames`` list or the ``ColumnWildCard`` .
        :param database_name: UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ . A database in the Data Catalog .
        :param name: UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ . The name given by the user to the data filter cell.
        :param row_filter: A PartiQL predicate.
        :param table_catalog_id: Catalog id string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ . The ID of the catalog to which the table belongs.
        :param table_name: UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ . A table in the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            # all_rows_wildcard: Any
            
            cfn_data_cells_filter_mixin_props = lakeformation_mixins.CfnDataCellsFilterMixinProps(
                column_names=["columnNames"],
                column_wildcard=lakeformation_mixins.CfnDataCellsFilterPropsMixin.ColumnWildcardProperty(
                    excluded_column_names=["excludedColumnNames"]
                ),
                database_name="databaseName",
                name="name",
                row_filter=lakeformation_mixins.CfnDataCellsFilterPropsMixin.RowFilterProperty(
                    all_rows_wildcard=all_rows_wildcard,
                    filter_expression="filterExpression"
                ),
                table_catalog_id="tableCatalogId",
                table_name="tableName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b5b1cfba93c97ab9cf7c371c0fbeaf23dd274c2ee5e463bab081c331c58f78)
            check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
            check_type(argname="argument column_wildcard", value=column_wildcard, expected_type=type_hints["column_wildcard"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument row_filter", value=row_filter, expected_type=type_hints["row_filter"])
            check_type(argname="argument table_catalog_id", value=table_catalog_id, expected_type=type_hints["table_catalog_id"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if column_names is not None:
            self._values["column_names"] = column_names
        if column_wildcard is not None:
            self._values["column_wildcard"] = column_wildcard
        if database_name is not None:
            self._values["database_name"] = database_name
        if name is not None:
            self._values["name"] = name
        if row_filter is not None:
            self._values["row_filter"] = row_filter
        if table_catalog_id is not None:
            self._values["table_catalog_id"] = table_catalog_id
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of UTF-8 strings.

        A list of column names.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-columnnames
        '''
        result = self._values.get("column_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def column_wildcard(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCellsFilterPropsMixin.ColumnWildcardProperty"]]:
        '''A wildcard with exclusions.

        You must specify either a ``ColumnNames`` list or the ``ColumnWildCard`` .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-columnwildcard
        '''
        result = self._values.get("column_wildcard")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCellsFilterPropsMixin.ColumnWildcardProperty"]], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ .

        A database in the Data Catalog .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-databasename
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ .

        The name given by the user to the data filter cell.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def row_filter(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCellsFilterPropsMixin.RowFilterProperty"]]:
        '''A PartiQL predicate.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-rowfilter
        '''
        result = self._values.get("row_filter")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataCellsFilterPropsMixin.RowFilterProperty"]], result)

    @builtins.property
    def table_catalog_id(self) -> typing.Optional[builtins.str]:
        '''Catalog id string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ .

        The ID of the catalog to which the table belongs.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-tablecatalogid
        '''
        result = self._values.get("table_catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ .

        A table in the database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html#cfn-lakeformation-datacellsfilter-tablename
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataCellsFilterMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataCellsFilterPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataCellsFilterPropsMixin",
):
    '''A structure that represents a data cell filter with column-level, row-level, and/or cell-level security.

    Data cell filters belong to a specific table in a Data Catalog . During a stack operation, AWS CloudFormation calls the AWS Lake Formation ``CreateDataCellsFilter`` API operation to create a ``DataCellsFilter`` resource, and calls the ``DeleteDataCellsFilter`` API operation to delete it.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datacellsfilter.html
    :cloudformationResource: AWS::LakeFormation::DataCellsFilter
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        # all_rows_wildcard: Any
        
        cfn_data_cells_filter_props_mixin = lakeformation_mixins.CfnDataCellsFilterPropsMixin(lakeformation_mixins.CfnDataCellsFilterMixinProps(
            column_names=["columnNames"],
            column_wildcard=lakeformation_mixins.CfnDataCellsFilterPropsMixin.ColumnWildcardProperty(
                excluded_column_names=["excludedColumnNames"]
            ),
            database_name="databaseName",
            name="name",
            row_filter=lakeformation_mixins.CfnDataCellsFilterPropsMixin.RowFilterProperty(
                all_rows_wildcard=all_rows_wildcard,
                filter_expression="filterExpression"
            ),
            table_catalog_id="tableCatalogId",
            table_name="tableName"
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataCellsFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::DataCellsFilter``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce18c68e1eb9beed3354e15295d4f27d893439bd3eebf8e2ce84fe9bc99cebe5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d8fbeadb1f6b71bcc8e526204679616627a01d02e3475a4b3920137a805d007)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88e8c6eeaf74c833576c61f43ad270f1235cde3e744966c7a82ef3aa46d7017f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataCellsFilterMixinProps:
        return typing.cast(CfnDataCellsFilterMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataCellsFilterPropsMixin.ColumnWildcardProperty",
        jsii_struct_bases=[],
        name_mapping={"excluded_column_names": "excludedColumnNames"},
    )
    class ColumnWildcardProperty:
        def __init__(
            self,
            *,
            excluded_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A wildcard object, consisting of an optional list of excluded column names or indexes.

            :param excluded_column_names: Excludes column names. Any column with this name will be excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datacellsfilter-columnwildcard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                column_wildcard_property = lakeformation_mixins.CfnDataCellsFilterPropsMixin.ColumnWildcardProperty(
                    excluded_column_names=["excludedColumnNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad1bd2f14fde5b0890d0817efcce3bac1e8ee9c72ea105a6fb2d2f97876cd13c)
                check_type(argname="argument excluded_column_names", value=excluded_column_names, expected_type=type_hints["excluded_column_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded_column_names is not None:
                self._values["excluded_column_names"] = excluded_column_names

        @builtins.property
        def excluded_column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Excludes column names.

            Any column with this name will be excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datacellsfilter-columnwildcard.html#cfn-lakeformation-datacellsfilter-columnwildcard-excludedcolumnnames
            '''
            result = self._values.get("excluded_column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnWildcardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataCellsFilterPropsMixin.RowFilterProperty",
        jsii_struct_bases=[],
        name_mapping={
            "all_rows_wildcard": "allRowsWildcard",
            "filter_expression": "filterExpression",
        },
    )
    class RowFilterProperty:
        def __init__(
            self,
            *,
            all_rows_wildcard: typing.Any = None,
            filter_expression: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A PartiQL predicate.

            :param all_rows_wildcard: A wildcard for all rows.
            :param filter_expression: A filter expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datacellsfilter-rowfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                # all_rows_wildcard: Any
                
                row_filter_property = lakeformation_mixins.CfnDataCellsFilterPropsMixin.RowFilterProperty(
                    all_rows_wildcard=all_rows_wildcard,
                    filter_expression="filterExpression"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3573d92c6712ce717f6e5c4424095e2c86ba0e31304dd5de2f15363ed876a25e)
                check_type(argname="argument all_rows_wildcard", value=all_rows_wildcard, expected_type=type_hints["all_rows_wildcard"])
                check_type(argname="argument filter_expression", value=filter_expression, expected_type=type_hints["filter_expression"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if all_rows_wildcard is not None:
                self._values["all_rows_wildcard"] = all_rows_wildcard
            if filter_expression is not None:
                self._values["filter_expression"] = filter_expression

        @builtins.property
        def all_rows_wildcard(self) -> typing.Any:
            '''A wildcard for all rows.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datacellsfilter-rowfilter.html#cfn-lakeformation-datacellsfilter-rowfilter-allrowswildcard
            '''
            result = self._values.get("all_rows_wildcard")
            return typing.cast(typing.Any, result)

        @builtins.property
        def filter_expression(self) -> typing.Optional[builtins.str]:
            '''A filter expression.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datacellsfilter-rowfilter.html#cfn-lakeformation-datacellsfilter-rowfilter-filterexpression
            '''
            result = self._values.get("filter_expression")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RowFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataLakeSettingsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "admins": "admins",
        "allow_external_data_filtering": "allowExternalDataFiltering",
        "allow_full_table_external_data_access": "allowFullTableExternalDataAccess",
        "authorized_session_tag_value_list": "authorizedSessionTagValueList",
        "create_database_default_permissions": "createDatabaseDefaultPermissions",
        "create_table_default_permissions": "createTableDefaultPermissions",
        "external_data_filtering_allow_list": "externalDataFilteringAllowList",
        "mutation_type": "mutationType",
        "parameters": "parameters",
        "read_only_admins": "readOnlyAdmins",
        "trusted_resource_owners": "trustedResourceOwners",
    },
)
class CfnDataLakeSettingsMixinProps:
    def __init__(
        self,
        *,
        admins: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        allow_external_data_filtering: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        allow_full_table_external_data_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        authorized_session_tag_value_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        create_database_default_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        create_table_default_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        external_data_filtering_allow_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        mutation_type: typing.Optional[builtins.str] = None,
        parameters: typing.Any = None,
        read_only_admins: typing.Any = None,
        trusted_resource_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnDataLakeSettingsPropsMixin.

        :param admins: A list of AWS Lake Formation principals.
        :param allow_external_data_filtering: Whether to allow Amazon EMR clusters or other third-party query engines to access data managed by Lake Formation . If set to true, you allow Amazon EMR clusters or other third-party engines to access data in Amazon S3 locations that are registered with Lake Formation . If false or null, no third-party query engines will be able to access data in Amazon S3 locations that are registered with Lake Formation. For more information, see `External data filtering setting <https://docs.aws.amazon.com/lake-formation/latest/dg/initial-LF-setup.html#external-data-filter>`_ .
        :param allow_full_table_external_data_access: Specifies whether query engines and applications can get credentials without IAM session tags if the user has full table access. It provides query engines and applications performance benefits as well as simplifies data access. Amazon EMR on Amazon EC2 is able to leverage this setting. For more information, see ` <https://docs.aws.amazon.com/lake-formation/latest/dg/using-cred-vending.html>`_
        :param authorized_session_tag_value_list: Lake Formation relies on a privileged process secured by Amazon EMR or the third party integrator to tag the user's role while assuming it. Lake Formation will publish the acceptable key-value pair, for example key = "LakeFormationTrustedCaller" and value = "TRUE" and the third party integrator must properly tag the temporary security credentials that will be used to call Lake Formation 's administrative API operations.
        :param create_database_default_permissions: Specifies whether access control on a newly created database is managed by Lake Formation permissions or exclusively by IAM permissions. A null value indicates that the access is controlled by Lake Formation permissions. ``ALL`` permissions assigned to ``IAM_ALLOWED_PRINCIPALS`` group indicates that the user's IAM permissions determine the access to the database. This is referred to as the setting "Use only IAM access control," and is to support backward compatibility with the AWS Glue permission model implemented by IAM permissions. The only permitted values are an empty array or an array that contains a single JSON object that grants ``ALL`` to ``IAM_ALLOWED_PRINCIPALS`` . For more information, see `Changing the default security settings for your data lake <https://docs.aws.amazon.com/lake-formation/latest/dg/change-settings.html>`_ .
        :param create_table_default_permissions: Specifies whether access control on a newly created table is managed by Lake Formation permissions or exclusively by IAM permissions. A null value indicates that the access is controlled by Lake Formation permissions. ``ALL`` permissions assigned to ``IAM_ALLOWED_PRINCIPALS`` group indicate that the user's IAM permissions determine the access to the table. This is referred to as the setting "Use only IAM access control," and is to support the backward compatibility with the AWS Glue permission model implemented by IAM permissions. The only permitted values are an empty array or an array that contains a single JSON object that grants ``ALL`` permissions to ``IAM_ALLOWED_PRINCIPALS`` . For more information, see `Changing the default security settings for your data lake <https://docs.aws.amazon.com/lake-formation/latest/dg/change-settings.html>`_ .
        :param external_data_filtering_allow_list: A list of the account IDs of AWS accounts with Amazon EMR clusters or third-party engines that are allwed to perform data filtering.
        :param mutation_type: Specifies whether the data lake settings are updated by adding new values to the current settings ( ``APPEND`` ) or by replacing the current settings with new settings ( ``REPLACE`` ). .. epigraph:: If you choose ``REPLACE`` , your current data lake settings will be replaced with the new values in your template.
        :param parameters: A key-value map that provides an additional configuration on your data lake. ``CrossAccountVersion`` is the key you can configure in the ``Parameters`` field. Accepted values for the ``CrossAccountVersion`` key are 1, 2, 3, and 4.
        :param read_only_admins: 
        :param trusted_resource_owners: An array of UTF-8 strings. A list of the resource-owning account IDs that the caller's account can use to share their user access details (user ARNs). The user ARNs can be logged in the resource owner's CloudTrail log. You may want to specify this property when you are in a high-trust boundary, such as the same team or company.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            # parameters: Any
            # read_only_admins: Any
            
            cfn_data_lake_settings_mixin_props = lakeformation_mixins.CfnDataLakeSettingsMixinProps(
                admins=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )],
                allow_external_data_filtering=False,
                allow_full_table_external_data_access=False,
                authorized_session_tag_value_list=["authorizedSessionTagValueList"],
                create_database_default_permissions=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty(
                    permissions=["permissions"],
                    principal=lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                        data_lake_principal_identifier="dataLakePrincipalIdentifier"
                    )
                )],
                create_table_default_permissions=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty(
                    permissions=["permissions"],
                    principal=lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                        data_lake_principal_identifier="dataLakePrincipalIdentifier"
                    )
                )],
                external_data_filtering_allow_list=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )],
                mutation_type="mutationType",
                parameters=parameters,
                read_only_admins=read_only_admins,
                trusted_resource_owners=["trustedResourceOwners"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b03a943a1cef7730efd57e4c1cb590f279d4724853d765b3364b2582af96f2b5)
            check_type(argname="argument admins", value=admins, expected_type=type_hints["admins"])
            check_type(argname="argument allow_external_data_filtering", value=allow_external_data_filtering, expected_type=type_hints["allow_external_data_filtering"])
            check_type(argname="argument allow_full_table_external_data_access", value=allow_full_table_external_data_access, expected_type=type_hints["allow_full_table_external_data_access"])
            check_type(argname="argument authorized_session_tag_value_list", value=authorized_session_tag_value_list, expected_type=type_hints["authorized_session_tag_value_list"])
            check_type(argname="argument create_database_default_permissions", value=create_database_default_permissions, expected_type=type_hints["create_database_default_permissions"])
            check_type(argname="argument create_table_default_permissions", value=create_table_default_permissions, expected_type=type_hints["create_table_default_permissions"])
            check_type(argname="argument external_data_filtering_allow_list", value=external_data_filtering_allow_list, expected_type=type_hints["external_data_filtering_allow_list"])
            check_type(argname="argument mutation_type", value=mutation_type, expected_type=type_hints["mutation_type"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument read_only_admins", value=read_only_admins, expected_type=type_hints["read_only_admins"])
            check_type(argname="argument trusted_resource_owners", value=trusted_resource_owners, expected_type=type_hints["trusted_resource_owners"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if admins is not None:
            self._values["admins"] = admins
        if allow_external_data_filtering is not None:
            self._values["allow_external_data_filtering"] = allow_external_data_filtering
        if allow_full_table_external_data_access is not None:
            self._values["allow_full_table_external_data_access"] = allow_full_table_external_data_access
        if authorized_session_tag_value_list is not None:
            self._values["authorized_session_tag_value_list"] = authorized_session_tag_value_list
        if create_database_default_permissions is not None:
            self._values["create_database_default_permissions"] = create_database_default_permissions
        if create_table_default_permissions is not None:
            self._values["create_table_default_permissions"] = create_table_default_permissions
        if external_data_filtering_allow_list is not None:
            self._values["external_data_filtering_allow_list"] = external_data_filtering_allow_list
        if mutation_type is not None:
            self._values["mutation_type"] = mutation_type
        if parameters is not None:
            self._values["parameters"] = parameters
        if read_only_admins is not None:
            self._values["read_only_admins"] = read_only_admins
        if trusted_resource_owners is not None:
            self._values["trusted_resource_owners"] = trusted_resource_owners

    @builtins.property
    def admins(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty"]]]]:
        '''A list of AWS Lake Formation principals.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-admins
        '''
        result = self._values.get("admins")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty"]]]], result)

    @builtins.property
    def allow_external_data_filtering(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Whether to allow Amazon EMR clusters or other third-party query engines to access data managed by Lake Formation .

        If set to true, you allow Amazon EMR clusters or other third-party engines to access data in Amazon S3 locations that are registered with Lake Formation .

        If false or null, no third-party query engines will be able to access data in Amazon S3 locations that are registered with Lake Formation.

        For more information, see `External data filtering setting <https://docs.aws.amazon.com/lake-formation/latest/dg/initial-LF-setup.html#external-data-filter>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-allowexternaldatafiltering
        '''
        result = self._values.get("allow_external_data_filtering")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def allow_full_table_external_data_access(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Specifies whether query engines and applications can get credentials without IAM session tags if the user has full table access.

        It provides query engines and applications performance benefits as well as simplifies data access. Amazon EMR on Amazon EC2 is able to leverage this setting.

        For more information, see ` <https://docs.aws.amazon.com/lake-formation/latest/dg/using-cred-vending.html>`_

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-allowfulltableexternaldataaccess
        '''
        result = self._values.get("allow_full_table_external_data_access")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def authorized_session_tag_value_list(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Lake Formation relies on a privileged process secured by Amazon EMR or the third party integrator to tag the user's role while assuming it.

        Lake Formation will publish the acceptable key-value pair, for example key = "LakeFormationTrustedCaller" and value = "TRUE" and the third party integrator must properly tag the temporary security credentials that will be used to call Lake Formation 's administrative API operations.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-authorizedsessiontagvaluelist
        '''
        result = self._values.get("authorized_session_tag_value_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def create_database_default_permissions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty"]]]]:
        '''Specifies whether access control on a newly created database is managed by Lake Formation permissions or exclusively by IAM permissions.

        A null value indicates that the access is controlled by Lake Formation permissions. ``ALL`` permissions assigned to ``IAM_ALLOWED_PRINCIPALS`` group indicates that the user's IAM permissions determine the access to the database. This is referred to as the setting "Use only IAM access control," and is to support backward compatibility with the AWS Glue permission model implemented by IAM permissions.

        The only permitted values are an empty array or an array that contains a single JSON object that grants ``ALL`` to ``IAM_ALLOWED_PRINCIPALS`` .

        For more information, see `Changing the default security settings for your data lake <https://docs.aws.amazon.com/lake-formation/latest/dg/change-settings.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-createdatabasedefaultpermissions
        '''
        result = self._values.get("create_database_default_permissions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty"]]]], result)

    @builtins.property
    def create_table_default_permissions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty"]]]]:
        '''Specifies whether access control on a newly created table is managed by Lake Formation permissions or exclusively by IAM permissions.

        A null value indicates that the access is controlled by Lake Formation permissions. ``ALL`` permissions assigned to ``IAM_ALLOWED_PRINCIPALS`` group indicate that the user's IAM permissions determine the access to the table. This is referred to as the setting "Use only IAM access control," and is to support the backward compatibility with the AWS Glue permission model implemented by IAM permissions.

        The only permitted values are an empty array or an array that contains a single JSON object that grants ``ALL`` permissions to ``IAM_ALLOWED_PRINCIPALS`` .

        For more information, see `Changing the default security settings for your data lake <https://docs.aws.amazon.com/lake-formation/latest/dg/change-settings.html>`_ .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-createtabledefaultpermissions
        '''
        result = self._values.get("create_table_default_permissions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty"]]]], result)

    @builtins.property
    def external_data_filtering_allow_list(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty"]]]]:
        '''A list of the account IDs of AWS accounts with Amazon EMR clusters or third-party engines that are allwed to perform data filtering.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-externaldatafilteringallowlist
        '''
        result = self._values.get("external_data_filtering_allow_list")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty"]]]], result)

    @builtins.property
    def mutation_type(self) -> typing.Optional[builtins.str]:
        '''Specifies whether the data lake settings are updated by adding new values to the current settings ( ``APPEND`` ) or by replacing the current settings with new settings ( ``REPLACE`` ).

        .. epigraph::

           If you choose ``REPLACE`` , your current data lake settings will be replaced with the new values in your template.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-mutationtype
        '''
        result = self._values.get("mutation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''A key-value map that provides an additional configuration on your data lake.

        ``CrossAccountVersion`` is the key you can configure in the ``Parameters`` field. Accepted values for the ``CrossAccountVersion`` key are 1, 2, 3, and 4.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def read_only_admins(self) -> typing.Any:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-readonlyadmins
        '''
        result = self._values.get("read_only_admins")
        return typing.cast(typing.Any, result)

    @builtins.property
    def trusted_resource_owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of UTF-8 strings.

        A list of the resource-owning account IDs that the caller's account can use to share their user access details (user ARNs). The user ARNs can be logged in the resource owner's CloudTrail log. You may want to specify this property when you are in a high-trust boundary, such as the same team or company.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html#cfn-lakeformation-datalakesettings-trustedresourceowners
        '''
        result = self._values.get("trusted_resource_owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataLakeSettingsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnDataLakeSettingsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataLakeSettingsPropsMixin",
):
    '''The ``AWS::LakeFormation::DataLakeSettings`` resource is an AWS Lake Formation resource type that manages the data lake settings for your account.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-datalakesettings.html
    :cloudformationResource: AWS::LakeFormation::DataLakeSettings
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        # parameters: Any
        # read_only_admins: Any
        
        cfn_data_lake_settings_props_mixin = lakeformation_mixins.CfnDataLakeSettingsPropsMixin(lakeformation_mixins.CfnDataLakeSettingsMixinProps(
            admins=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                data_lake_principal_identifier="dataLakePrincipalIdentifier"
            )],
            allow_external_data_filtering=False,
            allow_full_table_external_data_access=False,
            authorized_session_tag_value_list=["authorizedSessionTagValueList"],
            create_database_default_permissions=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty(
                permissions=["permissions"],
                principal=lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )
            )],
            create_table_default_permissions=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty(
                permissions=["permissions"],
                principal=lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )
            )],
            external_data_filtering_allow_list=[lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                data_lake_principal_identifier="dataLakePrincipalIdentifier"
            )],
            mutation_type="mutationType",
            parameters=parameters,
            read_only_admins=read_only_admins,
            trusted_resource_owners=["trustedResourceOwners"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnDataLakeSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::DataLakeSettings``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__687052b691f6142b961d21096a86ab7f732496b399e44bc529cd90b6f0d04918)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae7b8507a99d32dbf773f11b927348bf3c491ce97549882d7a3486769214ca19)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be4c54fe0be1b5510e07b38df29773828cbf9826b58e9920fd6b52fdcc838512)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnDataLakeSettingsMixinProps:
        return typing.cast(CfnDataLakeSettingsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={"data_lake_principal_identifier": "dataLakePrincipalIdentifier"},
    )
    class DataLakePrincipalProperty:
        def __init__(
            self,
            *,
            data_lake_principal_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Lake Formation principal.

            :param data_lake_principal_identifier: An identifier for the Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-datalakeprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                data_lake_principal_property = lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdc9c527d29a44cfa2900deeb29cb00f60df5a368dbb1dac23617da678619454)
                check_type(argname="argument data_lake_principal_identifier", value=data_lake_principal_identifier, expected_type=type_hints["data_lake_principal_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_lake_principal_identifier is not None:
                self._values["data_lake_principal_identifier"] = data_lake_principal_identifier

        @builtins.property
        def data_lake_principal_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for the Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-datalakeprincipal.html#cfn-lakeformation-datalakesettings-datalakeprincipal-datalakeprincipalidentifier
            '''
            result = self._values.get("data_lake_principal_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataLakePrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty",
        jsii_struct_bases=[],
        name_mapping={"permissions": "permissions", "principal": "principal"},
    )
    class PrincipalPermissionsProperty:
        def __init__(
            self,
            *,
            permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
            principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Permissions granted to a principal.

            :param permissions: The permissions that are granted to the principal.
            :param principal: The principal who is granted permissions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-principalpermissions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                principal_permissions_property = lakeformation_mixins.CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty(
                    permissions=["permissions"],
                    principal=lakeformation_mixins.CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty(
                        data_lake_principal_identifier="dataLakePrincipalIdentifier"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22748d14e6a87912d551e817226e75956a66403cc352139c8bbe2afc42f55f88)
                check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
                check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if permissions is not None:
                self._values["permissions"] = permissions
            if principal is not None:
                self._values["principal"] = principal

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The permissions that are granted to the principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-principalpermissions.html#cfn-lakeformation-datalakesettings-principalpermissions-permissions
            '''
            result = self._values.get("permissions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def principal(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty"]]:
            '''The principal who is granted permissions.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-datalakesettings-principalpermissions.html#cfn-lakeformation-datalakesettings-principalpermissions-principal
            '''
            result = self._values.get("principal")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrincipalPermissionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_lake_principal": "dataLakePrincipal",
        "permissions": "permissions",
        "permissions_with_grant_option": "permissionsWithGrantOption",
        "resource": "resource",
    },
)
class CfnPermissionsMixinProps:
    def __init__(
        self,
        *,
        data_lake_principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.DataLakePrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_with_grant_option: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.ResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPermissionsPropsMixin.

        :param data_lake_principal: The AWS Lake Formation principal.
        :param permissions: The permissions granted or revoked.
        :param permissions_with_grant_option: Indicates the ability to grant permissions (as a subset of permissions granted).
        :param resource: A structure for the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            cfn_permissions_mixin_props = lakeformation_mixins.CfnPermissionsMixinProps(
                data_lake_principal=lakeformation_mixins.CfnPermissionsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                ),
                permissions=["permissions"],
                permissions_with_grant_option=["permissionsWithGrantOption"],
                resource=lakeformation_mixins.CfnPermissionsPropsMixin.ResourceProperty(
                    database_resource=lakeformation_mixins.CfnPermissionsPropsMixin.DatabaseResourceProperty(
                        catalog_id="catalogId",
                        name="name"
                    ),
                    data_location_resource=lakeformation_mixins.CfnPermissionsPropsMixin.DataLocationResourceProperty(
                        catalog_id="catalogId",
                        s3_resource="s3Resource"
                    ),
                    table_resource=lakeformation_mixins.CfnPermissionsPropsMixin.TableResourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        table_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.TableWildcardProperty()
                    ),
                    table_with_columns_resource=lakeformation_mixins.CfnPermissionsPropsMixin.TableWithColumnsResourceProperty(
                        catalog_id="catalogId",
                        column_names=["columnNames"],
                        column_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.ColumnWildcardProperty(
                            excluded_column_names=["excludedColumnNames"]
                        ),
                        database_name="databaseName",
                        name="name"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39b4ed862805580aff5883205a49745c1b7ae28aadf88cd1f46ec1b843440f96)
            check_type(argname="argument data_lake_principal", value=data_lake_principal, expected_type=type_hints["data_lake_principal"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument permissions_with_grant_option", value=permissions_with_grant_option, expected_type=type_hints["permissions_with_grant_option"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_lake_principal is not None:
            self._values["data_lake_principal"] = data_lake_principal
        if permissions is not None:
            self._values["permissions"] = permissions
        if permissions_with_grant_option is not None:
            self._values["permissions_with_grant_option"] = permissions_with_grant_option
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def data_lake_principal(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.DataLakePrincipalProperty"]]:
        '''The AWS Lake Formation principal.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-datalakeprincipal
        '''
        result = self._values.get("data_lake_principal")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.DataLakePrincipalProperty"]], result)

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions granted or revoked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-permissions
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_with_grant_option(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Indicates the ability to grant permissions (as a subset of permissions granted).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-permissionswithgrantoption
        '''
        result = self._values.get("permissions_with_grant_option")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.ResourceProperty"]]:
        '''A structure for the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html#cfn-lakeformation-permissions-resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.ResourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPermissionsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPermissionsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin",
):
    '''The ``AWS::LakeFormation::Permissions`` resource represents the permissions that a principal has on an AWS Glue Data Catalog resource (such as AWS Glue database or AWS Glue tables).

    When you upload a permissions stack, the permissions are granted to the principal and when you remove the stack, the permissions are revoked from the principal. If you remove a stack, and the principal does not have the permissions referenced in the stack then AWS Lake Formation will throw an error because you can’t call revoke on non-existing permissions. To successfully remove the stack, you’ll need to regrant those permissions and then remove the stack.
    .. epigraph::

       New versions of AWS Lake Formation permission resources are now available. For more information, see: `AWS:LakeFormation::PrincipalPermissions <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html>`_

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-permissions.html
    :cloudformationResource: AWS::LakeFormation::Permissions
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        cfn_permissions_props_mixin = lakeformation_mixins.CfnPermissionsPropsMixin(lakeformation_mixins.CfnPermissionsMixinProps(
            data_lake_principal=lakeformation_mixins.CfnPermissionsPropsMixin.DataLakePrincipalProperty(
                data_lake_principal_identifier="dataLakePrincipalIdentifier"
            ),
            permissions=["permissions"],
            permissions_with_grant_option=["permissionsWithGrantOption"],
            resource=lakeformation_mixins.CfnPermissionsPropsMixin.ResourceProperty(
                database_resource=lakeformation_mixins.CfnPermissionsPropsMixin.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                ),
                data_location_resource=lakeformation_mixins.CfnPermissionsPropsMixin.DataLocationResourceProperty(
                    catalog_id="catalogId",
                    s3_resource="s3Resource"
                ),
                table_resource=lakeformation_mixins.CfnPermissionsPropsMixin.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.TableWildcardProperty()
                ),
                table_with_columns_resource=lakeformation_mixins.CfnPermissionsPropsMixin.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    column_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.ColumnWildcardProperty(
                        excluded_column_names=["excludedColumnNames"]
                    ),
                    database_name="databaseName",
                    name="name"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPermissionsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::Permissions``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d33f0a721abf007794f63031c9872dd512c5434b840accd42ef5f774d5eeef8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e106c7f65218bf190839a420b2a2a5f2f025ed93fe12e9d095294c6c2da8317f)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c061c73cafd0fb5688bda09f40ab232bd22486d00e5807b4a03ce4e48c23620e)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPermissionsMixinProps:
        return typing.cast(CfnPermissionsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.ColumnWildcardProperty",
        jsii_struct_bases=[],
        name_mapping={"excluded_column_names": "excludedColumnNames"},
    )
    class ColumnWildcardProperty:
        def __init__(
            self,
            *,
            excluded_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A wildcard object, consisting of an optional list of excluded column names or indexes.

            :param excluded_column_names: Excludes column names. Any column with this name will be excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-columnwildcard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                column_wildcard_property = lakeformation_mixins.CfnPermissionsPropsMixin.ColumnWildcardProperty(
                    excluded_column_names=["excludedColumnNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__da1d9c7b76b43e8fc1b67a723bf20222502e79521b2c1d6c56e718a36352f4e9)
                check_type(argname="argument excluded_column_names", value=excluded_column_names, expected_type=type_hints["excluded_column_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded_column_names is not None:
                self._values["excluded_column_names"] = excluded_column_names

        @builtins.property
        def excluded_column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Excludes column names.

            Any column with this name will be excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-columnwildcard.html#cfn-lakeformation-permissions-columnwildcard-excludedcolumnnames
            '''
            result = self._values.get("excluded_column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnWildcardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.DataLakePrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={"data_lake_principal_identifier": "dataLakePrincipalIdentifier"},
    )
    class DataLakePrincipalProperty:
        def __init__(
            self,
            *,
            data_lake_principal_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Lake Formation principal.

            :param data_lake_principal_identifier: An identifier for the Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalakeprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                data_lake_principal_property = lakeformation_mixins.CfnPermissionsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1443e7cdfdc517e51c0cb25aecb52ed01d94ea73ef77c65a6359de87c200e972)
                check_type(argname="argument data_lake_principal_identifier", value=data_lake_principal_identifier, expected_type=type_hints["data_lake_principal_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_lake_principal_identifier is not None:
                self._values["data_lake_principal_identifier"] = data_lake_principal_identifier

        @builtins.property
        def data_lake_principal_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for the Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalakeprincipal.html#cfn-lakeformation-permissions-datalakeprincipal-datalakeprincipalidentifier
            '''
            result = self._values.get("data_lake_principal_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataLakePrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.DataLocationResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"catalog_id": "catalogId", "s3_resource": "s3Resource"},
    )
    class DataLocationResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            s3_resource: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for a data location object where permissions are granted or revoked.

            :param catalog_id: The identifier for the Data Catalog . By default, it is the account ID of the caller.
            :param s3_resource: The Amazon Resource Name (ARN) that uniquely identifies the data location resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalocationresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                data_location_resource_property = lakeformation_mixins.CfnPermissionsPropsMixin.DataLocationResourceProperty(
                    catalog_id="catalogId",
                    s3_resource="s3Resource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3f900bbeba687094a5dc2271642a880d2075786fe7961a01bfbea89377d1438c)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument s3_resource", value=s3_resource, expected_type=type_hints["s3_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if s3_resource is not None:
                self._values["s3_resource"] = s3_resource

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalocationresource.html#cfn-lakeformation-permissions-datalocationresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_resource(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that uniquely identifies the data location resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-datalocationresource.html#cfn-lakeformation-permissions-datalocationresource-s3resource
            '''
            result = self._values.get("s3_resource")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataLocationResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.DatabaseResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"catalog_id": "catalogId", "name": "name"},
    )
    class DatabaseResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for the database object.

            :param catalog_id: The identifier for the Data Catalog . By default, it is the account ID of the caller.
            :param name: The name of the database resource. Unique to the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-databaseresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                database_resource_property = lakeformation_mixins.CfnPermissionsPropsMixin.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__901c99e2ec641bbfc93a307cb22099fe11bf836c91f895fa74f8993f5a2ef8d0)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-databaseresource.html#cfn-lakeformation-permissions-databaseresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the database resource.

            Unique to the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-databaseresource.html#cfn-lakeformation-permissions-databaseresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.ResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_resource": "databaseResource",
            "data_location_resource": "dataLocationResource",
            "table_resource": "tableResource",
            "table_with_columns_resource": "tableWithColumnsResource",
        },
    )
    class ResourceProperty:
        def __init__(
            self,
            *,
            database_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.DatabaseResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_location_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.DataLocationResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.TableResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_with_columns_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.TableWithColumnsResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure for the resource.

            :param database_resource: A structure for the database object.
            :param data_location_resource: A structure for a data location object where permissions are granted or revoked.
            :param table_resource: A structure for the table object. A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.
            :param table_with_columns_resource: A structure for a table with columns object. This object is only used when granting a SELECT permission.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                resource_property = lakeformation_mixins.CfnPermissionsPropsMixin.ResourceProperty(
                    database_resource=lakeformation_mixins.CfnPermissionsPropsMixin.DatabaseResourceProperty(
                        catalog_id="catalogId",
                        name="name"
                    ),
                    data_location_resource=lakeformation_mixins.CfnPermissionsPropsMixin.DataLocationResourceProperty(
                        catalog_id="catalogId",
                        s3_resource="s3Resource"
                    ),
                    table_resource=lakeformation_mixins.CfnPermissionsPropsMixin.TableResourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        table_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.TableWildcardProperty()
                    ),
                    table_with_columns_resource=lakeformation_mixins.CfnPermissionsPropsMixin.TableWithColumnsResourceProperty(
                        catalog_id="catalogId",
                        column_names=["columnNames"],
                        column_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.ColumnWildcardProperty(
                            excluded_column_names=["excludedColumnNames"]
                        ),
                        database_name="databaseName",
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f6c2a5e21ec7e3c0ef44049cba48832f83d85108bfc1e13413575fa7545d0559)
                check_type(argname="argument database_resource", value=database_resource, expected_type=type_hints["database_resource"])
                check_type(argname="argument data_location_resource", value=data_location_resource, expected_type=type_hints["data_location_resource"])
                check_type(argname="argument table_resource", value=table_resource, expected_type=type_hints["table_resource"])
                check_type(argname="argument table_with_columns_resource", value=table_with_columns_resource, expected_type=type_hints["table_with_columns_resource"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_resource is not None:
                self._values["database_resource"] = database_resource
            if data_location_resource is not None:
                self._values["data_location_resource"] = data_location_resource
            if table_resource is not None:
                self._values["table_resource"] = table_resource
            if table_with_columns_resource is not None:
                self._values["table_with_columns_resource"] = table_with_columns_resource

        @builtins.property
        def database_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.DatabaseResourceProperty"]]:
            '''A structure for the database object.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-databaseresource
            '''
            result = self._values.get("database_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.DatabaseResourceProperty"]], result)

        @builtins.property
        def data_location_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.DataLocationResourceProperty"]]:
            '''A structure for a data location object where permissions are granted or revoked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-datalocationresource
            '''
            result = self._values.get("data_location_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.DataLocationResourceProperty"]], result)

        @builtins.property
        def table_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.TableResourceProperty"]]:
            '''A structure for the table object.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-tableresource
            '''
            result = self._values.get("table_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.TableResourceProperty"]], result)

        @builtins.property
        def table_with_columns_resource(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.TableWithColumnsResourceProperty"]]:
            '''A structure for a table with columns object.

            This object is only used when granting a SELECT permission.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-resource.html#cfn-lakeformation-permissions-resource-tablewithcolumnsresource
            '''
            result = self._values.get("table_with_columns_resource")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.TableWithColumnsResourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.TableResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "name": "name",
            "table_wildcard": "tableWildcard",
        },
    )
    class TableResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            table_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.TableWildcardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure for the table object.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :param catalog_id: The identifier for the Data Catalog . By default, it is the account ID of the caller.
            :param database_name: The name of the database for the table. Unique to a Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.
            :param name: The name of the table.
            :param table_wildcard: An empty object representing all tables under a database. If this field is specified instead of the ``Name`` field, all tables under ``DatabaseName`` will have permission changes applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                table_resource_property = lakeformation_mixins.CfnPermissionsPropsMixin.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.TableWildcardProperty()
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e84cb67cae0b4e05cf3a9f2ceb950d0f500185cb26f29f2b2aae0e50595a06cc)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument table_wildcard", value=table_wildcard, expected_type=type_hints["table_wildcard"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name
            if table_wildcard is not None:
                self._values["table_wildcard"] = table_wildcard

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html#cfn-lakeformation-permissions-tableresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database for the table.

            Unique to a Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html#cfn-lakeformation-permissions-tableresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html#cfn-lakeformation-permissions-tableresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_wildcard(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.TableWildcardProperty"]]:
            '''An empty object representing all tables under a database.

            If this field is specified instead of the ``Name`` field, all tables under ``DatabaseName`` will have permission changes applied.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tableresource.html#cfn-lakeformation-permissions-tableresource-tablewildcard
            '''
            result = self._values.get("table_wildcard")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.TableWildcardProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.TableWildcardProperty",
        jsii_struct_bases=[],
        name_mapping={},
    )
    class TableWildcardProperty:
        def __init__(self) -> None:
            '''
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewildcard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                table_wildcard_property = lakeformation_mixins.CfnPermissionsPropsMixin.TableWildcardProperty()
            '''
            self._values: typing.Dict[builtins.str, typing.Any] = {}

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableWildcardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPermissionsPropsMixin.TableWithColumnsResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "column_names": "columnNames",
            "column_wildcard": "columnWildcard",
            "database_name": "databaseName",
            "name": "name",
        },
    )
    class TableWithColumnsResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            column_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPermissionsPropsMixin.ColumnWildcardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for a table with columns object. This object is only used when granting a SELECT permission.

            This object must take a value for at least one of ``ColumnsNames`` , ``ColumnsIndexes`` , or ``ColumnsWildcard`` .

            :param catalog_id: The identifier for the Data Catalog . By default, it is the account ID of the caller.
            :param column_names: The list of column names for the table. At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.
            :param column_wildcard: A wildcard specified by a ``ColumnWildcard`` object. At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.
            :param database_name: The name of the database for the table with columns resource. Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.
            :param name: The name of the table resource. A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                table_with_columns_resource_property = lakeformation_mixins.CfnPermissionsPropsMixin.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    column_wildcard=lakeformation_mixins.CfnPermissionsPropsMixin.ColumnWildcardProperty(
                        excluded_column_names=["excludedColumnNames"]
                    ),
                    database_name="databaseName",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ff0321efce106cf8535e115a64d34eaf54d4c02ea46e516bf3ae199016dc77de)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
                check_type(argname="argument column_wildcard", value=column_wildcard, expected_type=type_hints["column_wildcard"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if column_names is not None:
                self._values["column_names"] = column_names
            if column_wildcard is not None:
                self._values["column_wildcard"] = column_wildcard
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of column names for the table.

            At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-columnnames
            '''
            result = self._values.get("column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def column_wildcard(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.ColumnWildcardProperty"]]:
            '''A wildcard specified by a ``ColumnWildcard`` object.

            At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-columnwildcard
            '''
            result = self._values.get("column_wildcard")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPermissionsPropsMixin.ColumnWildcardProperty"]], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database for the table with columns resource.

            Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the table resource.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-permissions-tablewithcolumnsresource.html#cfn-lakeformation-permissions-tablewithcolumnsresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableWithColumnsResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog": "catalog",
        "permissions": "permissions",
        "permissions_with_grant_option": "permissionsWithGrantOption",
        "principal": "principal",
        "resource": "resource",
    },
)
class CfnPrincipalPermissionsMixinProps:
    def __init__(
        self,
        *,
        catalog: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        permissions_with_grant_option: typing.Optional[typing.Sequence[builtins.str]] = None,
        principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.ResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnPrincipalPermissionsPropsMixin.

        :param catalog: The identifier for the Data Catalog . By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your Lake Formation environment.
        :param permissions: The permissions granted or revoked.
        :param permissions_with_grant_option: Indicates the ability to grant permissions (as a subset of permissions granted).
        :param principal: The principal to be granted a permission.
        :param resource: The resource to be granted or revoked permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            # catalog: Any
            # table_wildcard: Any
            
            cfn_principal_permissions_mixin_props = lakeformation_mixins.CfnPrincipalPermissionsMixinProps(
                catalog="catalog",
                permissions=["permissions"],
                permissions_with_grant_option=["permissionsWithGrantOption"],
                principal=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                ),
                resource=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ResourceProperty(
                    catalog=catalog,
                    database=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty(
                        catalog_id="catalogId",
                        name="name"
                    ),
                    data_cells_filter=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty(
                        database_name="databaseName",
                        name="name",
                        table_catalog_id="tableCatalogId",
                        table_name="tableName"
                    ),
                    data_location=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty(
                        catalog_id="catalogId",
                        resource_arn="resourceArn"
                    ),
                    lf_tag=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty(
                        catalog_id="catalogId",
                        tag_key="tagKey",
                        tag_values=["tagValues"]
                    ),
                    lf_tag_policy=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty(
                        catalog_id="catalogId",
                        expression=[lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagProperty(
                            tag_key="tagKey",
                            tag_values=["tagValues"]
                        )],
                        resource_type="resourceType"
                    ),
                    table=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableResourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        table_wildcard=table_wildcard
                    ),
                    table_with_columns=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty(
                        catalog_id="catalogId",
                        column_names=["columnNames"],
                        column_wildcard=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty(
                            excluded_column_names=["excludedColumnNames"]
                        ),
                        database_name="databaseName",
                        name="name"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6574abfa4b65ac51b3727f81e59c879fbe6402b2b08312b444bf502f21205fee)
            check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument permissions_with_grant_option", value=permissions_with_grant_option, expected_type=type_hints["permissions_with_grant_option"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog is not None:
            self._values["catalog"] = catalog
        if permissions is not None:
            self._values["permissions"] = permissions
        if permissions_with_grant_option is not None:
            self._values["permissions_with_grant_option"] = permissions_with_grant_option
        if principal is not None:
            self._values["principal"] = principal
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def catalog(self) -> typing.Optional[builtins.str]:
        '''The identifier for the Data Catalog .

        By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your Lake Formation environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html#cfn-lakeformation-principalpermissions-catalog
        '''
        result = self._values.get("catalog")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The permissions granted or revoked.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html#cfn-lakeformation-principalpermissions-permissions
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def permissions_with_grant_option(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Indicates the ability to grant permissions (as a subset of permissions granted).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html#cfn-lakeformation-principalpermissions-permissionswithgrantoption
        '''
        result = self._values.get("permissions_with_grant_option")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principal(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty"]]:
        '''The principal to be granted a permission.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html#cfn-lakeformation-principalpermissions-principal
        '''
        result = self._values.get("principal")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty"]], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.ResourceProperty"]]:
        '''The resource to be granted or revoked permissions.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html#cfn-lakeformation-principalpermissions-resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.ResourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrincipalPermissionsMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnPrincipalPermissionsPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin",
):
    '''The ``AWS::LakeFormation::PrincipalPermissions`` resource represents the permissions that a principal has on a Data Catalog resource (such as AWS Glue databases or AWS Glue tables).

    When you create a ``PrincipalPermissions`` resource, the permissions are granted via the AWS Lake Formation ``GrantPermissions`` API operation. When you delete a ``PrincipalPermissions`` resource, the permissions on principal-resource pair are revoked via the AWS Lake Formation ``RevokePermissions`` API operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-principalpermissions.html
    :cloudformationResource: AWS::LakeFormation::PrincipalPermissions
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        # catalog: Any
        # table_wildcard: Any
        
        cfn_principal_permissions_props_mixin = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin(lakeformation_mixins.CfnPrincipalPermissionsMixinProps(
            catalog="catalog",
            permissions=["permissions"],
            permissions_with_grant_option=["permissionsWithGrantOption"],
            principal=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty(
                data_lake_principal_identifier="dataLakePrincipalIdentifier"
            ),
            resource=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ResourceProperty(
                catalog=catalog,
                database=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                ),
                data_cells_filter=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty(
                    database_name="databaseName",
                    name="name",
                    table_catalog_id="tableCatalogId",
                    table_name="tableName"
                ),
                data_location=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty(
                    catalog_id="catalogId",
                    resource_arn="resourceArn"
                ),
                lf_tag=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty(
                    catalog_id="catalogId",
                    tag_key="tagKey",
                    tag_values=["tagValues"]
                ),
                lf_tag_policy=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty(
                    catalog_id="catalogId",
                    expression=[lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagProperty(
                        tag_key="tagKey",
                        tag_values=["tagValues"]
                    )],
                    resource_type="resourceType"
                ),
                table=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=table_wildcard
                ),
                table_with_columns=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    column_wildcard=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty(
                        excluded_column_names=["excludedColumnNames"]
                    ),
                    database_name="databaseName",
                    name="name"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnPrincipalPermissionsMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::PrincipalPermissions``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d6e22796425129674ff6fede698cb52fe6af5370503610a1c2b19ec9f8e7fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c811259dbc26da971aaf7eb408caabfbe69bfa98f3db862e524d22d12c04c59)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2343335c5df3c2cb38e77c12e6df95da5143d56e775025a54b75949baf9b58)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnPrincipalPermissionsMixinProps:
        return typing.cast(CfnPrincipalPermissionsMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty",
        jsii_struct_bases=[],
        name_mapping={"excluded_column_names": "excludedColumnNames"},
    )
    class ColumnWildcardProperty:
        def __init__(
            self,
            *,
            excluded_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A wildcard object, consisting of an optional list of excluded column names or indexes.

            :param excluded_column_names: Excludes column names. Any column with this name will be excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-columnwildcard.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                column_wildcard_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty(
                    excluded_column_names=["excludedColumnNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fdb69a22f33a33ea9a1ed414d76b7c20cdd148d844e92cb5a09bfe9dbcc2cb2d)
                check_type(argname="argument excluded_column_names", value=excluded_column_names, expected_type=type_hints["excluded_column_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if excluded_column_names is not None:
                self._values["excluded_column_names"] = excluded_column_names

        @builtins.property
        def excluded_column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''Excludes column names.

            Any column with this name will be excluded.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-columnwildcard.html#cfn-lakeformation-principalpermissions-columnwildcard-excludedcolumnnames
            '''
            result = self._values.get("excluded_column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnWildcardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "database_name": "databaseName",
            "name": "name",
            "table_catalog_id": "tableCatalogId",
            "table_name": "tableName",
        },
    )
    class DataCellsFilterResourceProperty:
        def __init__(
            self,
            *,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            table_catalog_id: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure that describes certain columns on certain rows.

            :param database_name: A database in the Data Catalog .
            :param name: The name given by the user to the data filter cell.
            :param table_catalog_id: The ID of the catalog to which the table belongs.
            :param table_name: The name of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datacellsfilterresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                data_cells_filter_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty(
                    database_name="databaseName",
                    name="name",
                    table_catalog_id="tableCatalogId",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__923a55cfd67b3599fac73a6429b240a9b27d499b872a73204824a3aab3604fa2)
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument table_catalog_id", value=table_catalog_id, expected_type=type_hints["table_catalog_id"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name
            if table_catalog_id is not None:
                self._values["table_catalog_id"] = table_catalog_id
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''A database in the Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datacellsfilterresource.html#cfn-lakeformation-principalpermissions-datacellsfilterresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name given by the user to the data filter cell.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datacellsfilterresource.html#cfn-lakeformation-principalpermissions-datacellsfilterresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_catalog_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the catalog to which the table belongs.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datacellsfilterresource.html#cfn-lakeformation-principalpermissions-datacellsfilterresource-tablecatalogid
            '''
            result = self._values.get("table_catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The name of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datacellsfilterresource.html#cfn-lakeformation-principalpermissions-datacellsfilterresource-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataCellsFilterResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty",
        jsii_struct_bases=[],
        name_mapping={"data_lake_principal_identifier": "dataLakePrincipalIdentifier"},
    )
    class DataLakePrincipalProperty:
        def __init__(
            self,
            *,
            data_lake_principal_identifier: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The AWS Lake Formation principal.

            :param data_lake_principal_identifier: An identifier for the AWS Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datalakeprincipal.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                data_lake_principal_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty(
                    data_lake_principal_identifier="dataLakePrincipalIdentifier"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__781bfa08092e4bb6e087b1d4cbd94843ca39078b4ac101a99b874a9867de2ebd)
                check_type(argname="argument data_lake_principal_identifier", value=data_lake_principal_identifier, expected_type=type_hints["data_lake_principal_identifier"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_lake_principal_identifier is not None:
                self._values["data_lake_principal_identifier"] = data_lake_principal_identifier

        @builtins.property
        def data_lake_principal_identifier(self) -> typing.Optional[builtins.str]:
            '''An identifier for the AWS Lake Formation principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datalakeprincipal.html#cfn-lakeformation-principalpermissions-datalakeprincipal-datalakeprincipalidentifier
            '''
            result = self._values.get("data_lake_principal_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataLakePrincipalProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"catalog_id": "catalogId", "resource_arn": "resourceArn"},
    )
    class DataLocationResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            resource_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for a data location object where permissions are granted or revoked.

            :param catalog_id: The identifier for the Data Catalog where the location is registered with AWS Lake Formation .
            :param resource_arn: The Amazon Resource Name (ARN) that uniquely identifies the data location resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datalocationresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                data_location_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty(
                    catalog_id="catalogId",
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__774cebaf6a1ac9185cc269e59d93857f1fe2c05b3fe111dd34aab8089c4340b6)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog where the location is registered with AWS Lake Formation .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datalocationresource.html#cfn-lakeformation-principalpermissions-datalocationresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) that uniquely identifies the data location resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-datalocationresource.html#cfn-lakeformation-principalpermissions-datalocationresource-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataLocationResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"catalog_id": "catalogId", "name": "name"},
    )
    class DatabaseResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for the database object.

            :param catalog_id: The identifier for the Data Catalog. By default, it is the account ID of the caller.
            :param name: The name of the database resource. Unique to the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-databaseresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                database_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7b1b5c6819111cf684e441ec3de16dd5804f117b71770f481daed0876705ff5c)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog.

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-databaseresource.html#cfn-lakeformation-principalpermissions-databaseresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the database resource.

            Unique to the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-databaseresource.html#cfn-lakeformation-principalpermissions-databaseresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "tag_key": "tagKey",
            "tag_values": "tagValues",
        },
    )
    class LFTagKeyResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            tag_key: typing.Optional[builtins.str] = None,
            tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A structure containing an LF-tag key and values for a resource.

            :param catalog_id: The identifier for the Data Catalog where the location is registered with Data Catalog .
            :param tag_key: The key-name for the LF-tag.
            :param tag_values: A list of possible values for the corresponding ``TagKey`` of an LF-tag key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagkeyresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                l_fTag_key_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty(
                    catalog_id="catalogId",
                    tag_key="tagKey",
                    tag_values=["tagValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8c959015e3866b0057d1cd6ecafadf9b5a42680f1bfadb698919f58768c7197)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
                check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if tag_key is not None:
                self._values["tag_key"] = tag_key
            if tag_values is not None:
                self._values["tag_values"] = tag_values

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog where the location is registered with Data Catalog .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagkeyresource.html#cfn-lakeformation-principalpermissions-lftagkeyresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_key(self) -> typing.Optional[builtins.str]:
            '''The key-name for the LF-tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagkeyresource.html#cfn-lakeformation-principalpermissions-lftagkeyresource-tagkey
            '''
            result = self._values.get("tag_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values for the corresponding ``TagKey`` of an LF-tag key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagkeyresource.html#cfn-lakeformation-principalpermissions-lftagkeyresource-tagvalues
            '''
            result = self._values.get("tag_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LFTagKeyResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "expression": "expression",
            "resource_type": "resourceType",
        },
    )
    class LFTagPolicyResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.LFTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            resource_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of LF-tag conditions that define a resource's LF-tag policy.

            A structure that allows an admin to grant user permissions on certain conditions. For example, granting a role access to all columns that do not have the LF-tag 'PII' in tables that have the LF-tag 'Prod'.

            :param catalog_id: The identifier for the Data Catalog . The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.
            :param expression: A list of LF-tag conditions that apply to the resource's LF-tag policy.
            :param resource_type: The resource type for which the LF-tag policy applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagpolicyresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                l_fTag_policy_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty(
                    catalog_id="catalogId",
                    expression=[lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagProperty(
                        tag_key="tagKey",
                        tag_values=["tagValues"]
                    )],
                    resource_type="resourceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e58e0c68ec0e128cb1bf042655fc513dd901afb773761aaf471a62cfc8575579)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if expression is not None:
                self._values["expression"] = expression
            if resource_type is not None:
                self._values["resource_type"] = resource_type

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagpolicyresource.html#cfn-lakeformation-principalpermissions-lftagpolicyresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def expression(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.LFTagProperty"]]]]:
            '''A list of LF-tag conditions that apply to the resource's LF-tag policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagpolicyresource.html#cfn-lakeformation-principalpermissions-lftagpolicyresource-expression
            '''
            result = self._values.get("expression")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.LFTagProperty"]]]], result)

        @builtins.property
        def resource_type(self) -> typing.Optional[builtins.str]:
            '''The resource type for which the LF-tag policy applies.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftagpolicyresource.html#cfn-lakeformation-principalpermissions-lftagpolicyresource-resourcetype
            '''
            result = self._values.get("resource_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LFTagPolicyResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.LFTagProperty",
        jsii_struct_bases=[],
        name_mapping={"tag_key": "tagKey", "tag_values": "tagValues"},
    )
    class LFTagProperty:
        def __init__(
            self,
            *,
            tag_key: typing.Optional[builtins.str] = None,
            tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The LF-tag key and values attached to a resource.

            :param tag_key: The key-name for the LF-tag.
            :param tag_values: A list of possible values of the corresponding ``TagKey`` of an LF-tag key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                l_fTag_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagProperty(
                    tag_key="tagKey",
                    tag_values=["tagValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__74a738813e8a6fdd03b9bd900d45aec297fb08fb345ed7e21b28d38f32b26a84)
                check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
                check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if tag_key is not None:
                self._values["tag_key"] = tag_key
            if tag_values is not None:
                self._values["tag_values"] = tag_values

        @builtins.property
        def tag_key(self) -> typing.Optional[builtins.str]:
            '''The key-name for the LF-tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftag.html#cfn-lakeformation-principalpermissions-lftag-tagkey
            '''
            result = self._values.get("tag_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values of the corresponding ``TagKey`` of an LF-tag key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-lftag.html#cfn-lakeformation-principalpermissions-lftag-tagvalues
            '''
            result = self._values.get("tag_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LFTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.ResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog": "catalog",
            "database": "database",
            "data_cells_filter": "dataCellsFilter",
            "data_location": "dataLocation",
            "lf_tag": "lfTag",
            "lf_tag_policy": "lfTagPolicy",
            "table": "table",
            "table_with_columns": "tableWithColumns",
        },
    )
    class ResourceProperty:
        def __init__(
            self,
            *,
            catalog: typing.Any = None,
            database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_cells_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            data_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lf_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lf_tag_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.TableResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_with_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure for the resource.

            :param catalog: The identifier for the Data Catalog. By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.
            :param database: The database for the resource. Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database permissions to a principal.
            :param data_cells_filter: A data cell filter.
            :param data_location: The location of an Amazon S3 path where permissions are granted or revoked.
            :param lf_tag: The LF-tag key and values attached to a resource.
            :param lf_tag_policy: A list of LF-tag conditions that define a resource's LF-tag policy.
            :param table: The table for the resource. A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.
            :param table_with_columns: The table with columns for the resource. A principal with permissions to this resource can select metadata from the columns of a table in the Data Catalog and the underlying data in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                # catalog: Any
                # table_wildcard: Any
                
                resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ResourceProperty(
                    catalog=catalog,
                    database=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty(
                        catalog_id="catalogId",
                        name="name"
                    ),
                    data_cells_filter=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty(
                        database_name="databaseName",
                        name="name",
                        table_catalog_id="tableCatalogId",
                        table_name="tableName"
                    ),
                    data_location=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty(
                        catalog_id="catalogId",
                        resource_arn="resourceArn"
                    ),
                    lf_tag=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty(
                        catalog_id="catalogId",
                        tag_key="tagKey",
                        tag_values=["tagValues"]
                    ),
                    lf_tag_policy=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty(
                        catalog_id="catalogId",
                        expression=[lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.LFTagProperty(
                            tag_key="tagKey",
                            tag_values=["tagValues"]
                        )],
                        resource_type="resourceType"
                    ),
                    table=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableResourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        table_wildcard=table_wildcard
                    ),
                    table_with_columns=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty(
                        catalog_id="catalogId",
                        column_names=["columnNames"],
                        column_wildcard=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty(
                            excluded_column_names=["excludedColumnNames"]
                        ),
                        database_name="databaseName",
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7ded674061a655c4073e8c16765acb74ad9f0f47b8bb46a36f9aa25699583ccc)
                check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
                check_type(argname="argument database", value=database, expected_type=type_hints["database"])
                check_type(argname="argument data_cells_filter", value=data_cells_filter, expected_type=type_hints["data_cells_filter"])
                check_type(argname="argument data_location", value=data_location, expected_type=type_hints["data_location"])
                check_type(argname="argument lf_tag", value=lf_tag, expected_type=type_hints["lf_tag"])
                check_type(argname="argument lf_tag_policy", value=lf_tag_policy, expected_type=type_hints["lf_tag_policy"])
                check_type(argname="argument table", value=table, expected_type=type_hints["table"])
                check_type(argname="argument table_with_columns", value=table_with_columns, expected_type=type_hints["table_with_columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog is not None:
                self._values["catalog"] = catalog
            if database is not None:
                self._values["database"] = database
            if data_cells_filter is not None:
                self._values["data_cells_filter"] = data_cells_filter
            if data_location is not None:
                self._values["data_location"] = data_location
            if lf_tag is not None:
                self._values["lf_tag"] = lf_tag
            if lf_tag_policy is not None:
                self._values["lf_tag_policy"] = lf_tag_policy
            if table is not None:
                self._values["table"] = table
            if table_with_columns is not None:
                self._values["table_with_columns"] = table_with_columns

        @builtins.property
        def catalog(self) -> typing.Any:
            '''The identifier for the Data Catalog.

            By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-catalog
            '''
            result = self._values.get("catalog")
            return typing.cast(typing.Any, result)

        @builtins.property
        def database(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty"]]:
            '''The database for the resource.

            Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database permissions to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-database
            '''
            result = self._values.get("database")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty"]], result)

        @builtins.property
        def data_cells_filter(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty"]]:
            '''A data cell filter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-datacellsfilter
            '''
            result = self._values.get("data_cells_filter")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty"]], result)

        @builtins.property
        def data_location(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty"]]:
            '''The location of an Amazon S3 path where permissions are granted or revoked.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-datalocation
            '''
            result = self._values.get("data_location")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty"]], result)

        @builtins.property
        def lf_tag(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty"]]:
            '''The LF-tag key and values attached to a resource.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-lftag
            '''
            result = self._values.get("lf_tag")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty"]], result)

        @builtins.property
        def lf_tag_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty"]]:
            '''A list of LF-tag conditions that define a resource's LF-tag policy.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-lftagpolicy
            '''
            result = self._values.get("lf_tag_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty"]], result)

        @builtins.property
        def table(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.TableResourceProperty"]]:
            '''The table for the resource.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-table
            '''
            result = self._values.get("table")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.TableResourceProperty"]], result)

        @builtins.property
        def table_with_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty"]]:
            '''The table with columns for the resource.

            A principal with permissions to this resource can select metadata from the columns of a table in the Data Catalog and the underlying data in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-resource.html#cfn-lakeformation-principalpermissions-resource-tablewithcolumns
            '''
            result = self._values.get("table_with_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.TableResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "name": "name",
            "table_wildcard": "tableWildcard",
        },
    )
    class TableResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            table_wildcard: typing.Any = None,
        ) -> None:
            '''A structure for the table object.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :param catalog_id: The identifier for the Data Catalog. By default, it is the account ID of the caller.
            :param database_name: The name of the database for the table. Unique to a Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.
            :param name: The name of the table.
            :param table_wildcard: A wildcard object representing every table under a database. At least one of ``TableResource$Name`` or ``TableResource$TableWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tableresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                # table_wildcard: Any
                
                table_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=table_wildcard
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d006cc389193b1cd2f40853e1d8bf9ac87b2ea23fabf8451f86fe52876517ea4)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument table_wildcard", value=table_wildcard, expected_type=type_hints["table_wildcard"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name
            if table_wildcard is not None:
                self._values["table_wildcard"] = table_wildcard

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog.

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tableresource.html#cfn-lakeformation-principalpermissions-tableresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database for the table.

            Unique to a Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tableresource.html#cfn-lakeformation-principalpermissions-tableresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tableresource.html#cfn-lakeformation-principalpermissions-tableresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_wildcard(self) -> typing.Any:
            '''A wildcard object representing every table under a database.

            At least one of ``TableResource$Name`` or ``TableResource$TableWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tableresource.html#cfn-lakeformation-principalpermissions-tableresource-tablewildcard
            '''
            result = self._values.get("table_wildcard")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "column_names": "columnNames",
            "column_wildcard": "columnWildcard",
            "database_name": "databaseName",
            "name": "name",
        },
    )
    class TableWithColumnsResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            column_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for a table with columns object. This object is only used when granting a SELECT permission.

            This object must take a value for at least one of ``ColumnsNames`` , ``ColumnsIndexes`` , or ``ColumnsWildcard`` .

            :param catalog_id: The identifier for the Data Catalog where the location is registered with AWS Lake Formation .
            :param column_names: The list of column names for the table. At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.
            :param column_wildcard: A wildcard specified by a ``ColumnWildcard`` object. At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.
            :param database_name: The name of the database for the table with columns resource. Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.
            :param name: The name of the table resource. A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tablewithcolumnsresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                table_with_columns_resource_property = lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    column_wildcard=lakeformation_mixins.CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty(
                        excluded_column_names=["excludedColumnNames"]
                    ),
                    database_name="databaseName",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__26eb9749aa21b3406627009151eaaf3a2f5dd02d1b4fc4884be09aac24e34b78)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
                check_type(argname="argument column_wildcard", value=column_wildcard, expected_type=type_hints["column_wildcard"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if column_names is not None:
                self._values["column_names"] = column_names
            if column_wildcard is not None:
                self._values["column_wildcard"] = column_wildcard
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog where the location is registered with AWS Lake Formation .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tablewithcolumnsresource.html#cfn-lakeformation-principalpermissions-tablewithcolumnsresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of column names for the table.

            At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tablewithcolumnsresource.html#cfn-lakeformation-principalpermissions-tablewithcolumnsresource-columnnames
            '''
            result = self._values.get("column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def column_wildcard(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty"]]:
            '''A wildcard specified by a ``ColumnWildcard`` object.

            At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tablewithcolumnsresource.html#cfn-lakeformation-principalpermissions-tablewithcolumnsresource-columnwildcard
            '''
            result = self._values.get("column_wildcard")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty"]], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database for the table with columns resource.

            Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tablewithcolumnsresource.html#cfn-lakeformation-principalpermissions-tablewithcolumnsresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the table resource.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-principalpermissions-tablewithcolumnsresource.html#cfn-lakeformation-principalpermissions-tablewithcolumnsresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableWithColumnsResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnResourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "hybrid_access_enabled": "hybridAccessEnabled",
        "resource_arn": "resourceArn",
        "role_arn": "roleArn",
        "use_service_linked_role": "useServiceLinkedRole",
        "with_federation": "withFederation",
    },
)
class CfnResourceMixinProps:
    def __init__(
        self,
        *,
        hybrid_access_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        resource_arn: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        use_service_linked_role: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
        with_federation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    ) -> None:
        '''Properties for CfnResourcePropsMixin.

        :param hybrid_access_enabled: Indicates whether the data access of tables pointing to the location can be managed by both Lake Formation permissions as well as Amazon S3 bucket policies.
        :param resource_arn: The Amazon Resource Name (ARN) of the resource.
        :param role_arn: The IAM role that registered a resource.
        :param use_service_linked_role: Designates a trusted caller, an IAM principal, by registering this caller with the Data Catalog .
        :param with_federation: Allows Lake Formation to assume a role to access tables in a federated database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            cfn_resource_mixin_props = lakeformation_mixins.CfnResourceMixinProps(
                hybrid_access_enabled=False,
                resource_arn="resourceArn",
                role_arn="roleArn",
                use_service_linked_role=False,
                with_federation=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c41eb075679d616c7c1eaca7277ad58e4f397a2a344b9a42a9ea6f5095b33fde)
            check_type(argname="argument hybrid_access_enabled", value=hybrid_access_enabled, expected_type=type_hints["hybrid_access_enabled"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument use_service_linked_role", value=use_service_linked_role, expected_type=type_hints["use_service_linked_role"])
            check_type(argname="argument with_federation", value=with_federation, expected_type=type_hints["with_federation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hybrid_access_enabled is not None:
            self._values["hybrid_access_enabled"] = hybrid_access_enabled
        if resource_arn is not None:
            self._values["resource_arn"] = resource_arn
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if use_service_linked_role is not None:
            self._values["use_service_linked_role"] = use_service_linked_role
        if with_federation is not None:
            self._values["with_federation"] = with_federation

    @builtins.property
    def hybrid_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Indicates whether the data access of tables pointing to the location can be managed by both Lake Formation permissions as well as Amazon S3 bucket policies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-hybridaccessenabled
        '''
        result = self._values.get("hybrid_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def resource_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-resourcearn
        '''
        result = self._values.get("resource_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The IAM role that registered a resource.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_service_linked_role(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Designates a trusted caller, an IAM principal, by registering this caller with the Data Catalog .

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-useservicelinkedrole
        '''
        result = self._values.get("use_service_linked_role")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    @builtins.property
    def with_federation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]]:
        '''Allows Lake Formation to assume a role to access tables in a federated database.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html#cfn-lakeformation-resource-withfederation
        '''
        result = self._values.get("with_federation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnResourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnResourcePropsMixin",
):
    '''The ``AWS::LakeFormation::Resource`` represents the data (  buckets and folders) that is being registered with AWS Lake Formation .

    During a stack operation, AWS CloudFormation calls the AWS Lake Formation ```RegisterResource`` <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-credential-vending.html#aws-lake-formation-api-credential-vending-RegisterResource>`_ API operation to register the resource. To remove a ``Resource`` type, AWS CloudFormation calls the AWS Lake Formation ```DeregisterResource`` <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-credential-vending.html#aws-lake-formation-api-credential-vending-DeregisterResource>`_ API operation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-resource.html
    :cloudformationResource: AWS::LakeFormation::Resource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        cfn_resource_props_mixin = lakeformation_mixins.CfnResourcePropsMixin(lakeformation_mixins.CfnResourceMixinProps(
            hybrid_access_enabled=False,
            resource_arn="resourceArn",
            role_arn="roleArn",
            use_service_linked_role=False,
            with_federation=False
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::Resource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e069b8fffddc48e31b6053fb2bf38c452f81f08c43788d3d9c026f42de145aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7dc05d1e733caacbf130131a92e87617eb2bb661e50396328a0dc411a1c21af)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922281826fae987707054c09717eab09c022d38c26852b84961eaf534aa554c1)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnResourceMixinProps:
        return typing.cast(CfnResourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationMixinProps",
    jsii_struct_bases=[],
    name_mapping={"lf_tags": "lfTags", "resource": "resource"},
)
class CfnTagAssociationMixinProps:
    def __init__(
        self,
        *,
        lf_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTagAssociationPropsMixin.LFTagPairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTagAssociationPropsMixin.ResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnTagAssociationPropsMixin.

        :param lf_tags: A structure containing an LF-tag key-value pair.
        :param resource: UTF-8 string (valid values: ``DATABASE | TABLE`` ). The resource for which the LF-tag policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tagassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            # catalog: Any
            # table_wildcard: Any
            
            cfn_tag_association_mixin_props = lakeformation_mixins.CfnTagAssociationMixinProps(
                lf_tags=[lakeformation_mixins.CfnTagAssociationPropsMixin.LFTagPairProperty(
                    catalog_id="catalogId",
                    tag_key="tagKey",
                    tag_values=["tagValues"]
                )],
                resource=lakeformation_mixins.CfnTagAssociationPropsMixin.ResourceProperty(
                    catalog=catalog,
                    database=lakeformation_mixins.CfnTagAssociationPropsMixin.DatabaseResourceProperty(
                        catalog_id="catalogId",
                        name="name"
                    ),
                    table=lakeformation_mixins.CfnTagAssociationPropsMixin.TableResourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        table_wildcard=table_wildcard
                    ),
                    table_with_columns=lakeformation_mixins.CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty(
                        catalog_id="catalogId",
                        column_names=["columnNames"],
                        database_name="databaseName",
                        name="name"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dac7320cb1c043eb0184f7931255ee6ae14ee6c483194f8b4e9ffef11440869)
            check_type(argname="argument lf_tags", value=lf_tags, expected_type=type_hints["lf_tags"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if lf_tags is not None:
            self._values["lf_tags"] = lf_tags
        if resource is not None:
            self._values["resource"] = resource

    @builtins.property
    def lf_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.LFTagPairProperty"]]]]:
        '''A structure containing an LF-tag key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tagassociation.html#cfn-lakeformation-tagassociation-lftags
        '''
        result = self._values.get("lf_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.LFTagPairProperty"]]]], result)

    @builtins.property
    def resource(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.ResourceProperty"]]:
        '''UTF-8 string (valid values: ``DATABASE | TABLE`` ).

        The resource for which the LF-tag policy applies.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tagassociation.html#cfn-lakeformation-tagassociation-resource
        '''
        result = self._values.get("resource")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.ResourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagAssociationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTagAssociationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationPropsMixin",
):
    '''The ``AWS::LakeFormation::TagAssociation`` resource represents an assignment of an LF-tag to a Data Catalog resource (database, table, or column).

    During a stack operation, CloudFormation calls AWS Lake Formation ``AddLFTagsToResource`` API to create a ``TagAssociation`` resource and calls the ``RemoveLFTagsToResource`` API to delete it.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tagassociation.html
    :cloudformationResource: AWS::LakeFormation::TagAssociation
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        # catalog: Any
        # table_wildcard: Any
        
        cfn_tag_association_props_mixin = lakeformation_mixins.CfnTagAssociationPropsMixin(lakeformation_mixins.CfnTagAssociationMixinProps(
            lf_tags=[lakeformation_mixins.CfnTagAssociationPropsMixin.LFTagPairProperty(
                catalog_id="catalogId",
                tag_key="tagKey",
                tag_values=["tagValues"]
            )],
            resource=lakeformation_mixins.CfnTagAssociationPropsMixin.ResourceProperty(
                catalog=catalog,
                database=lakeformation_mixins.CfnTagAssociationPropsMixin.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                ),
                table=lakeformation_mixins.CfnTagAssociationPropsMixin.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=table_wildcard
                ),
                table_with_columns=lakeformation_mixins.CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    database_name="databaseName",
                    name="name"
                )
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTagAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::TagAssociation``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94ffc108ee09de9749567de3986cf204c44510274edefa3edebb0abb219f503e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__351a15ece0896b45d091c16aae035057b31aa45927007e6025f565f0df098477)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a99f19972f30da19bd58a6d09f4bfa943c7d07b92709b2cdff336243c0e72c05)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTagAssociationMixinProps:
        return typing.cast(CfnTagAssociationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationPropsMixin.DatabaseResourceProperty",
        jsii_struct_bases=[],
        name_mapping={"catalog_id": "catalogId", "name": "name"},
    )
    class DatabaseResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for the database object.

            :param catalog_id: The identifier for the Data Catalog . By default, it should be the account ID of the caller.
            :param name: The name of the database resource. Unique to the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-databaseresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                database_resource_property = lakeformation_mixins.CfnTagAssociationPropsMixin.DatabaseResourceProperty(
                    catalog_id="catalogId",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c050027a46524443b98307cdeac426ac5155810dcb4fbc4c1658438b7ca8b4c3)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it should be the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-databaseresource.html#cfn-lakeformation-tagassociation-databaseresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the database resource.

            Unique to the Data Catalog.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-databaseresource.html#cfn-lakeformation-tagassociation-databaseresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatabaseResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationPropsMixin.LFTagPairProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "tag_key": "tagKey",
            "tag_values": "tagValues",
        },
    )
    class LFTagPairProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            tag_key: typing.Optional[builtins.str] = None,
            tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A structure containing the catalog ID, tag key, and tag values of an LF-tag key-value pair.

            :param catalog_id: The identifier for the Data Catalog . By default, it is the account ID of the caller.
            :param tag_key: The key-name for the LF-tag.
            :param tag_values: A list of possible values of the corresponding ``TagKey`` of an LF-tag key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-lftagpair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                l_fTag_pair_property = lakeformation_mixins.CfnTagAssociationPropsMixin.LFTagPairProperty(
                    catalog_id="catalogId",
                    tag_key="tagKey",
                    tag_values=["tagValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f4247cdcf6f0a2078477f7d00810d1ffb788da3b241779953920ae33b40f5807)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
                check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if tag_key is not None:
                self._values["tag_key"] = tag_key
            if tag_values is not None:
                self._values["tag_values"] = tag_values

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-lftagpair.html#cfn-lakeformation-tagassociation-lftagpair-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_key(self) -> typing.Optional[builtins.str]:
            '''The key-name for the LF-tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-lftagpair.html#cfn-lakeformation-tagassociation-lftagpair-tagkey
            '''
            result = self._values.get("tag_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list of possible values of the corresponding ``TagKey`` of an LF-tag key-value pair.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-lftagpair.html#cfn-lakeformation-tagassociation-lftagpair-tagvalues
            '''
            result = self._values.get("tag_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LFTagPairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationPropsMixin.ResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog": "catalog",
            "database": "database",
            "table": "table",
            "table_with_columns": "tableWithColumns",
        },
    )
    class ResourceProperty:
        def __init__(
            self,
            *,
            catalog: typing.Any = None,
            database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTagAssociationPropsMixin.DatabaseResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTagAssociationPropsMixin.TableResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_with_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A structure for the resource.

            :param catalog: The identifier for the Data Catalog. By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.
            :param database: The database for the resource. Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database permissions to a principal.
            :param table: The table for the resource. A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.
            :param table_with_columns: The table with columns for the resource. A principal with permissions to this resource can select metadata from the columns of a table in the Data Catalog and the underlying data in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-resource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                # catalog: Any
                # table_wildcard: Any
                
                resource_property = lakeformation_mixins.CfnTagAssociationPropsMixin.ResourceProperty(
                    catalog=catalog,
                    database=lakeformation_mixins.CfnTagAssociationPropsMixin.DatabaseResourceProperty(
                        catalog_id="catalogId",
                        name="name"
                    ),
                    table=lakeformation_mixins.CfnTagAssociationPropsMixin.TableResourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        name="name",
                        table_wildcard=table_wildcard
                    ),
                    table_with_columns=lakeformation_mixins.CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty(
                        catalog_id="catalogId",
                        column_names=["columnNames"],
                        database_name="databaseName",
                        name="name"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3dc33f8bb7c0ecc754be3f27b1539c14a619d1bf85f2d1baa93870e3db6c01ef)
                check_type(argname="argument catalog", value=catalog, expected_type=type_hints["catalog"])
                check_type(argname="argument database", value=database, expected_type=type_hints["database"])
                check_type(argname="argument table", value=table, expected_type=type_hints["table"])
                check_type(argname="argument table_with_columns", value=table_with_columns, expected_type=type_hints["table_with_columns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog is not None:
                self._values["catalog"] = catalog
            if database is not None:
                self._values["database"] = database
            if table is not None:
                self._values["table"] = table
            if table_with_columns is not None:
                self._values["table_with_columns"] = table_with_columns

        @builtins.property
        def catalog(self) -> typing.Any:
            '''The identifier for the Data Catalog.

            By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-resource.html#cfn-lakeformation-tagassociation-resource-catalog
            '''
            result = self._values.get("catalog")
            return typing.cast(typing.Any, result)

        @builtins.property
        def database(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.DatabaseResourceProperty"]]:
            '''The database for the resource.

            Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database permissions to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-resource.html#cfn-lakeformation-tagassociation-resource-database
            '''
            result = self._values.get("database")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.DatabaseResourceProperty"]], result)

        @builtins.property
        def table(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.TableResourceProperty"]]:
            '''The table for the resource.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-resource.html#cfn-lakeformation-tagassociation-resource-table
            '''
            result = self._values.get("table")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.TableResourceProperty"]], result)

        @builtins.property
        def table_with_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty"]]:
            '''The table with columns for the resource.

            A principal with permissions to this resource can select metadata from the columns of a table in the Data Catalog and the underlying data in Amazon S3.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-resource.html#cfn-lakeformation-tagassociation-resource-tablewithcolumns
            '''
            result = self._values.get("table_with_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationPropsMixin.TableResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "name": "name",
            "table_wildcard": "tableWildcard",
        },
    )
    class TableResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            table_wildcard: typing.Any = None,
        ) -> None:
            '''A structure for the table object.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :param catalog_id: The identifier for the Data Catalog . By default, it is the account ID of the caller.
            :param database_name: The name of the database for the table. Unique to a Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.
            :param name: The name of the table.
            :param table_wildcard: A wildcard object representing every table under a database.This is an object with no properties that effectively behaves as a true or false depending on whether not it is passed as a parameter. The valid inputs for a property with this type in either yaml or json is null or {}. At least one of ``TableResource$Name`` or ``TableResource$TableWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tableresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                # table_wildcard: Any
                
                table_resource_property = lakeformation_mixins.CfnTagAssociationPropsMixin.TableResourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    name="name",
                    table_wildcard=table_wildcard
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c51fe272b72e518f823329b998b47c7a62a25cfb72fb75144a47c38e7ce81457)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument table_wildcard", value=table_wildcard, expected_type=type_hints["table_wildcard"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name
            if table_wildcard is not None:
                self._values["table_wildcard"] = table_wildcard

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the Data Catalog .

            By default, it is the account ID of the caller.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tableresource.html#cfn-lakeformation-tagassociation-tableresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database for the table.

            Unique to a Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tableresource.html#cfn-lakeformation-tagassociation-tableresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tableresource.html#cfn-lakeformation-tagassociation-tableresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_wildcard(self) -> typing.Any:
            '''A wildcard object representing every table under a database.This is an object with no properties that effectively behaves as a true or false depending on whether not it is passed as a parameter. The valid inputs for a property with this type in either yaml or json is null or {}.

            At least one of ``TableResource$Name`` or ``TableResource$TableWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tableresource.html#cfn-lakeformation-tagassociation-tableresource-tablewildcard
            '''
            result = self._values.get("table_wildcard")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "column_names": "columnNames",
            "database_name": "databaseName",
            "name": "name",
        },
    )
    class TableWithColumnsResourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
            database_name: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A structure for a table with columns object. This object is only used when granting a SELECT permission.

            This object must take a value for at least one of ``ColumnsNames`` , ``ColumnsIndexes`` , or ``ColumnsWildcard`` .

            :param catalog_id: A wildcard object representing every table under a database. At least one of TableResource$Name or TableResource$TableWildcard is required.
            :param column_names: The list of column names for the table. At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.
            :param database_name: The name of the database for the table with columns resource. Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.
            :param name: The name of the table resource. A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tablewithcolumnsresource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
                
                table_with_columns_resource_property = lakeformation_mixins.CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty(
                    catalog_id="catalogId",
                    column_names=["columnNames"],
                    database_name="databaseName",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2181dc01ebb2a890f449629e5dd2a6399678e708c0d1faaa8e964790d18ea7c)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument column_names", value=column_names, expected_type=type_hints["column_names"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if column_names is not None:
                self._values["column_names"] = column_names
            if database_name is not None:
                self._values["database_name"] = database_name
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''A wildcard object representing every table under a database.

            At least one of TableResource$Name or TableResource$TableWildcard is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tablewithcolumnsresource.html#cfn-lakeformation-tagassociation-tablewithcolumnsresource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of column names for the table.

            At least one of ``ColumnNames`` or ``ColumnWildcard`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tablewithcolumnsresource.html#cfn-lakeformation-tagassociation-tablewithcolumnsresource-columnnames
            '''
            result = self._values.get("column_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The name of the database for the table with columns resource.

            Unique to the Data Catalog. A database is a set of associated table definitions organized into a logical group. You can Grant and Revoke database privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tablewithcolumnsresource.html#cfn-lakeformation-tagassociation-tablewithcolumnsresource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the table resource.

            A table is a metadata definition that represents your data. You can Grant and Revoke table privileges to a principal.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-lakeformation-tagassociation-tablewithcolumnsresource.html#cfn-lakeformation-tagassociation-tablewithcolumnsresource-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TableWithColumnsResourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "catalog_id": "catalogId",
        "tag_key": "tagKey",
        "tag_values": "tagValues",
    },
)
class CfnTagMixinProps:
    def __init__(
        self,
        *,
        catalog_id: typing.Optional[builtins.str] = None,
        tag_key: typing.Optional[builtins.str] = None,
        tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for CfnTagPropsMixin.

        :param catalog_id: Catalog id string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ . The identifier for the Data Catalog . By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.
        :param tag_key: UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ . The key-name for the LF-tag.
        :param tag_values: An array of UTF-8 strings, not less than 1 or more than 50 strings. A list of possible values of the corresponding ``TagKey`` of an LF-tag key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tag.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
            
            cfn_tag_mixin_props = lakeformation_mixins.CfnTagMixinProps(
                catalog_id="catalogId",
                tag_key="tagKey",
                tag_values=["tagValues"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1f5256b117f75c6922e4ea2421520b84d64dda244566d4b01c569814527f0b)
            check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
            check_type(argname="argument tag_key", value=tag_key, expected_type=type_hints["tag_key"])
            check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if catalog_id is not None:
            self._values["catalog_id"] = catalog_id
        if tag_key is not None:
            self._values["tag_key"] = tag_key
        if tag_values is not None:
            self._values["tag_values"] = tag_values

    @builtins.property
    def catalog_id(self) -> typing.Optional[builtins.str]:
        '''Catalog id string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ .

        The identifier for the Data Catalog . By default, the account ID. The Data Catalog is the persistent metadata store. It contains database definitions, table definitions, and other control information to manage your AWS Lake Formation environment.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tag.html#cfn-lakeformation-tag-catalogid
        '''
        result = self._values.get("catalog_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_key(self) -> typing.Optional[builtins.str]:
        '''UTF-8 string, not less than 1 or more than 255 bytes long, matching the `single-line string pattern <https://docs.aws.amazon.com/lake-formation/latest/dg/aws-lake-formation-api-aws-lake-formation-api-common.html>`_ .

        The key-name for the LF-tag.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tag.html#cfn-lakeformation-tag-tagkey
        '''
        result = self._values.get("tag_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tag_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of UTF-8 strings, not less than 1 or more than 50 strings.

        A list of possible values of the corresponding ``TagKey`` of an LF-tag key-value pair.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tag.html#cfn-lakeformation-tag-tagvalues
        '''
        result = self._values.get("tag_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTagMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTagPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_lakeformation.mixins.CfnTagPropsMixin",
):
    '''The ``AWS::LakeFormation::Tag`` resource represents an LF-tag, which consists of a key and one or more possible values for the key.

    During a stack operation, AWS CloudFormation calls the AWS Lake Formation ``CreateLFTag`` API to create a tag, and ``UpdateLFTag`` API to update a tag resource, and a ``DeleteLFTag`` to delete it.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-lakeformation-tag.html
    :cloudformationResource: AWS::LakeFormation::Tag
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_lakeformation import mixins as lakeformation_mixins
        
        cfn_tag_props_mixin = lakeformation_mixins.CfnTagPropsMixin(lakeformation_mixins.CfnTagMixinProps(
            catalog_id="catalogId",
            tag_key="tagKey",
            tag_values=["tagValues"]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTagMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::LakeFormation::Tag``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e607a4f330c9087d4ba0d91a5ee49334b1bb86522ab3eefd3578d0fdfa84b6d0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c582c6a45e6258c22133b17e1d4c893e90cc2e47b8e641c1070f0a07f344bf8)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d05c2494cc92737a9150b4b730669779feee88836d58c714d05c39c072988fdf)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTagMixinProps:
        return typing.cast(CfnTagMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))


__all__ = [
    "CfnDataCellsFilterMixinProps",
    "CfnDataCellsFilterPropsMixin",
    "CfnDataLakeSettingsMixinProps",
    "CfnDataLakeSettingsPropsMixin",
    "CfnPermissionsMixinProps",
    "CfnPermissionsPropsMixin",
    "CfnPrincipalPermissionsMixinProps",
    "CfnPrincipalPermissionsPropsMixin",
    "CfnResourceMixinProps",
    "CfnResourcePropsMixin",
    "CfnTagAssociationMixinProps",
    "CfnTagAssociationPropsMixin",
    "CfnTagMixinProps",
    "CfnTagPropsMixin",
]

publication.publish()

def _typecheckingstub__12b5b1cfba93c97ab9cf7c371c0fbeaf23dd274c2ee5e463bab081c331c58f78(
    *,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    column_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataCellsFilterPropsMixin.ColumnWildcardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    row_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataCellsFilterPropsMixin.RowFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_catalog_id: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce18c68e1eb9beed3354e15295d4f27d893439bd3eebf8e2ce84fe9bc99cebe5(
    props: typing.Union[CfnDataCellsFilterMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8fbeadb1f6b71bcc8e526204679616627a01d02e3475a4b3920137a805d007(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88e8c6eeaf74c833576c61f43ad270f1235cde3e744966c7a82ef3aa46d7017f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1bd2f14fde5b0890d0817efcce3bac1e8ee9c72ea105a6fb2d2f97876cd13c(
    *,
    excluded_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3573d92c6712ce717f6e5c4424095e2c86ba0e31304dd5de2f15363ed876a25e(
    *,
    all_rows_wildcard: typing.Any = None,
    filter_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b03a943a1cef7730efd57e4c1cb590f279d4724853d765b3364b2582af96f2b5(
    *,
    admins: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    allow_external_data_filtering: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    allow_full_table_external_data_access: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    authorized_session_tag_value_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_database_default_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    create_table_default_permissions: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakeSettingsPropsMixin.PrincipalPermissionsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    external_data_filtering_allow_list: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    mutation_type: typing.Optional[builtins.str] = None,
    parameters: typing.Any = None,
    read_only_admins: typing.Any = None,
    trusted_resource_owners: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__687052b691f6142b961d21096a86ab7f732496b399e44bc529cd90b6f0d04918(
    props: typing.Union[CfnDataLakeSettingsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7b8507a99d32dbf773f11b927348bf3c491ce97549882d7a3486769214ca19(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be4c54fe0be1b5510e07b38df29773828cbf9826b58e9920fd6b52fdcc838512(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc9c527d29a44cfa2900deeb29cb00f60df5a368dbb1dac23617da678619454(
    *,
    data_lake_principal_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22748d14e6a87912d551e817226e75956a66403cc352139c8bbe2afc42f55f88(
    *,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnDataLakeSettingsPropsMixin.DataLakePrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39b4ed862805580aff5883205a49745c1b7ae28aadf88cd1f46ec1b843440f96(
    *,
    data_lake_principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.DataLakePrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_with_grant_option: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.ResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d33f0a721abf007794f63031c9872dd512c5434b840accd42ef5f774d5eeef8(
    props: typing.Union[CfnPermissionsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e106c7f65218bf190839a420b2a2a5f2f025ed93fe12e9d095294c6c2da8317f(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c061c73cafd0fb5688bda09f40ab232bd22486d00e5807b4a03ce4e48c23620e(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1d9c7b76b43e8fc1b67a723bf20222502e79521b2c1d6c56e718a36352f4e9(
    *,
    excluded_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1443e7cdfdc517e51c0cb25aecb52ed01d94ea73ef77c65a6359de87c200e972(
    *,
    data_lake_principal_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f900bbeba687094a5dc2271642a880d2075786fe7961a01bfbea89377d1438c(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    s3_resource: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901c99e2ec641bbfc93a307cb22099fe11bf836c91f895fa74f8993f5a2ef8d0(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6c2a5e21ec7e3c0ef44049cba48832f83d85108bfc1e13413575fa7545d0559(
    *,
    database_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.DatabaseResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_location_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.DataLocationResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.TableResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_with_columns_resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.TableWithColumnsResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84cb67cae0b4e05cf3a9f2ceb950d0f500185cb26f29f2b2aae0e50595a06cc(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    table_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.TableWildcardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff0321efce106cf8535e115a64d34eaf54d4c02ea46e516bf3ae199016dc77de(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    column_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPermissionsPropsMixin.ColumnWildcardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6574abfa4b65ac51b3727f81e59c879fbe6402b2b08312b444bf502f21205fee(
    *,
    catalog: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
    permissions_with_grant_option: typing.Optional[typing.Sequence[builtins.str]] = None,
    principal: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.DataLakePrincipalProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.ResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d6e22796425129674ff6fede698cb52fe6af5370503610a1c2b19ec9f8e7fb(
    props: typing.Union[CfnPrincipalPermissionsMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c811259dbc26da971aaf7eb408caabfbe69bfa98f3db862e524d22d12c04c59(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2343335c5df3c2cb38e77c12e6df95da5143d56e775025a54b75949baf9b58(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdb69a22f33a33ea9a1ed414d76b7c20cdd148d844e92cb5a09bfe9dbcc2cb2d(
    *,
    excluded_column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__923a55cfd67b3599fac73a6429b240a9b27d499b872a73204824a3aab3604fa2(
    *,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    table_catalog_id: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781bfa08092e4bb6e087b1d4cbd94843ca39078b4ac101a99b874a9867de2ebd(
    *,
    data_lake_principal_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__774cebaf6a1ac9185cc269e59d93857f1fe2c05b3fe111dd34aab8089c4340b6(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    resource_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b1b5c6819111cf684e441ec3de16dd5804f117b71770f481daed0876705ff5c(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c959015e3866b0057d1cd6ecafadf9b5a42680f1bfadb698919f58768c7197(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e58e0c68ec0e128cb1bf042655fc513dd901afb773761aaf471a62cfc8575579(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    expression: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.LFTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a738813e8a6fdd03b9bd900d45aec297fb08fb345ed7e21b28d38f32b26a84(
    *,
    tag_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ded674061a655c4073e8c16765acb74ad9f0f47b8bb46a36f9aa25699583ccc(
    *,
    catalog: typing.Any = None,
    database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.DatabaseResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_cells_filter: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.DataCellsFilterResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    data_location: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.DataLocationResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lf_tag: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.LFTagKeyResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lf_tag_policy: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.LFTagPolicyResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.TableResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_with_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.TableWithColumnsResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d006cc389193b1cd2f40853e1d8bf9ac87b2ea23fabf8451f86fe52876517ea4(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    table_wildcard: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26eb9749aa21b3406627009151eaaf3a2f5dd02d1b4fc4884be09aac24e34b78(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    column_wildcard: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnPrincipalPermissionsPropsMixin.ColumnWildcardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c41eb075679d616c7c1eaca7277ad58e4f397a2a344b9a42a9ea6f5095b33fde(
    *,
    hybrid_access_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    use_service_linked_role: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
    with_federation: typing.Optional[typing.Union[builtins.bool, _aws_cdk_ceddda9d.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e069b8fffddc48e31b6053fb2bf38c452f81f08c43788d3d9c026f42de145aa(
    props: typing.Union[CfnResourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7dc05d1e733caacbf130131a92e87617eb2bb661e50396328a0dc411a1c21af(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922281826fae987707054c09717eab09c022d38c26852b84961eaf534aa554c1(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dac7320cb1c043eb0184f7931255ee6ae14ee6c483194f8b4e9ffef11440869(
    *,
    lf_tags: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTagAssociationPropsMixin.LFTagPairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTagAssociationPropsMixin.ResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94ffc108ee09de9749567de3986cf204c44510274edefa3edebb0abb219f503e(
    props: typing.Union[CfnTagAssociationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__351a15ece0896b45d091c16aae035057b31aa45927007e6025f565f0df098477(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99f19972f30da19bd58a6d09f4bfa943c7d07b92709b2cdff336243c0e72c05(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c050027a46524443b98307cdeac426ac5155810dcb4fbc4c1658438b7ca8b4c3(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4247cdcf6f0a2078477f7d00810d1ffb788da3b241779953920ae33b40f5807(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc33f8bb7c0ecc754be3f27b1539c14a619d1bf85f2d1baa93870e3db6c01ef(
    *,
    catalog: typing.Any = None,
    database: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTagAssociationPropsMixin.DatabaseResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTagAssociationPropsMixin.TableResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_with_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTagAssociationPropsMixin.TableWithColumnsResourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51fe272b72e518f823329b998b47c7a62a25cfb72fb75144a47c38e7ce81457(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    table_wildcard: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2181dc01ebb2a890f449629e5dd2a6399678e708c0d1faaa8e964790d18ea7c(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    column_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    database_name: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1f5256b117f75c6922e4ea2421520b84d64dda244566d4b01c569814527f0b(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    tag_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e607a4f330c9087d4ba0d91a5ee49334b1bb86522ab3eefd3578d0fdfa84b6d0(
    props: typing.Union[CfnTagMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c582c6a45e6258c22133b17e1d4c893e90cc2e47b8e641c1070f0a07f344bf8(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05c2494cc92737a9150b4b730669779feee88836d58c714d05c39c072988fdf(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass
