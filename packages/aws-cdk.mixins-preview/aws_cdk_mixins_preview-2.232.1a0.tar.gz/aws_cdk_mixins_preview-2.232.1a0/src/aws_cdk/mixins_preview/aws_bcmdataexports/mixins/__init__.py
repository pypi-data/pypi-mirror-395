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
    jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportMixinProps",
    jsii_struct_bases=[],
    name_mapping={"export": "export", "tags": "tags"},
)
class CfnExportMixinProps:
    def __init__(
        self,
        *,
        export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExportPropsMixin.ExportProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnExportPropsMixin.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnExportPropsMixin.

        :param export: The details that are available for an export.
        :param tags: 

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bcmdataexports-export.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
            
            cfn_export_mixin_props = bcmdataexports_mixins.CfnExportMixinProps(
                export=bcmdataexports_mixins.CfnExportPropsMixin.ExportProperty(
                    data_query=bcmdataexports_mixins.CfnExportPropsMixin.DataQueryProperty(
                        query_statement="queryStatement",
                        table_configurations={
                            "table_configurations_key": {
                                "table_configurations_key": "tableConfigurations"
                            }
                        }
                    ),
                    description="description",
                    destination_configurations=bcmdataexports_mixins.CfnExportPropsMixin.DestinationConfigurationsProperty(
                        s3_destination=bcmdataexports_mixins.CfnExportPropsMixin.S3DestinationProperty(
                            s3_bucket="s3Bucket",
                            s3_output_configurations=bcmdataexports_mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty(
                                compression="compression",
                                format="format",
                                output_type="outputType",
                                overwrite="overwrite"
                            ),
                            s3_prefix="s3Prefix",
                            s3_region="s3Region"
                        )
                    ),
                    export_arn="exportArn",
                    name="name",
                    refresh_cadence=bcmdataexports_mixins.CfnExportPropsMixin.RefreshCadenceProperty(
                        frequency="frequency"
                    )
                ),
                tags=[bcmdataexports_mixins.CfnExportPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc0bb692d61c98bf82c1b5604121070ace3c9946285d03411e27f3bfff9bd53)
            check_type(argname="argument export", value=export, expected_type=type_hints["export"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if export is not None:
            self._values["export"] = export
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def export(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.ExportProperty"]]:
        '''The details that are available for an export.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bcmdataexports-export.html#cfn-bcmdataexports-export-export
        '''
        result = self._values.get("export")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.ExportProperty"]], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnExportPropsMixin.ResourceTagProperty"]]:
        '''
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bcmdataexports-export.html#cfn-bcmdataexports-export-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["CfnExportPropsMixin.ResourceTagProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExportMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnExportPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin",
):
    '''Creates a data export and specifies the data query, the delivery preference, and any optional resource tags.

    A ``DataQuery`` consists of both a ``QueryStatement`` and ``TableConfigurations`` .

    The ``QueryStatement`` is an SQL statement. Data Exports only supports a limited subset of the SQL syntax. For more information on the SQL syntax that is supported, see `Data query <https://docs.aws.amazon.com/cur/latest/userguide/de-data-query.html>`_ . To view the available tables and columns, see the `Data Exports table dictionary <https://docs.aws.amazon.com/cur/latest/userguide/de-table-dictionary.html>`_ .

    The ``TableConfigurations`` is a collection of specified ``TableProperties`` for the table being queried in the ``QueryStatement`` . TableProperties are additional configurations you can provide to change the data and schema of a table. Each table can have different TableProperties. However, tables are not required to have any TableProperties. Each table property has a default value that it assumes if not specified. For more information on table configurations, see `Data query <https://docs.aws.amazon.com/cur/latest/userguide/de-data-query.html>`_ . To view the table properties available for each table, see the `Data Exports table dictionary <https://docs.aws.amazon.com/cur/latest/userguide/de-table-dictionary.html>`_ or use the ``ListTables`` API to get a response of all tables and their available properties.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-bcmdataexports-export.html
    :cloudformationResource: AWS::BCMDataExports::Export
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
        
        cfn_export_props_mixin = bcmdataexports_mixins.CfnExportPropsMixin(bcmdataexports_mixins.CfnExportMixinProps(
            export=bcmdataexports_mixins.CfnExportPropsMixin.ExportProperty(
                data_query=bcmdataexports_mixins.CfnExportPropsMixin.DataQueryProperty(
                    query_statement="queryStatement",
                    table_configurations={
                        "table_configurations_key": {
                            "table_configurations_key": "tableConfigurations"
                        }
                    }
                ),
                description="description",
                destination_configurations=bcmdataexports_mixins.CfnExportPropsMixin.DestinationConfigurationsProperty(
                    s3_destination=bcmdataexports_mixins.CfnExportPropsMixin.S3DestinationProperty(
                        s3_bucket="s3Bucket",
                        s3_output_configurations=bcmdataexports_mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty(
                            compression="compression",
                            format="format",
                            output_type="outputType",
                            overwrite="overwrite"
                        ),
                        s3_prefix="s3Prefix",
                        s3_region="s3Region"
                    )
                ),
                export_arn="exportArn",
                name="name",
                refresh_cadence=bcmdataexports_mixins.CfnExportPropsMixin.RefreshCadenceProperty(
                    frequency="frequency"
                )
            ),
            tags=[bcmdataexports_mixins.CfnExportPropsMixin.ResourceTagProperty(
                key="key",
                value="value"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnExportMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::BCMDataExports::Export``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09b57cdb0a9e587f3721b63daab4517e95506b7bdd0fc773251bd6c7244730fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20925377fd39a825425a9beb7c7e138d25b6a31b5f97d0a3e4c9558cc6876b99)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__433206851d5c09131e0c6021d137495f8c8c5acb9ff2c4162b7508f5adb55e62)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnExportMixinProps:
        return typing.cast(CfnExportMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.DataQueryProperty",
        jsii_struct_bases=[],
        name_mapping={
            "query_statement": "queryStatement",
            "table_configurations": "tableConfigurations",
        },
    )
    class DataQueryProperty:
        def __init__(
            self,
            *,
            query_statement: typing.Optional[builtins.str] = None,
            table_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]]] = None,
        ) -> None:
            '''The SQL query of column selections and row filters from the data table you want.

            :param query_statement: The query statement.
            :param table_configurations: The table configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-dataquery.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                data_query_property = bcmdataexports_mixins.CfnExportPropsMixin.DataQueryProperty(
                    query_statement="queryStatement",
                    table_configurations={
                        "table_configurations_key": {
                            "table_configurations_key": "tableConfigurations"
                        }
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__88431171cbc24cf380aa01f2b93b6c9d35e801b3dc7000297bcb2b8517ab3dd6)
                check_type(argname="argument query_statement", value=query_statement, expected_type=type_hints["query_statement"])
                check_type(argname="argument table_configurations", value=table_configurations, expected_type=type_hints["table_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if query_statement is not None:
                self._values["query_statement"] = query_statement
            if table_configurations is not None:
                self._values["table_configurations"] = table_configurations

        @builtins.property
        def query_statement(self) -> typing.Optional[builtins.str]:
            '''The query statement.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-dataquery.html#cfn-bcmdataexports-export-dataquery-querystatement
            '''
            result = self._values.get("query_statement")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]]]:
            '''The table configuration.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-dataquery.html#cfn-bcmdataexports-export-dataquery-tableconfigurations
            '''
            result = self._values.get("table_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataQueryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.DestinationConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_destination": "s3Destination"},
    )
    class DestinationConfigurationsProperty:
        def __init__(
            self,
            *,
            s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExportPropsMixin.S3DestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The destinations used for data exports.

            :param s3_destination: An object that describes the destination of the data exports file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-destinationconfigurations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                destination_configurations_property = bcmdataexports_mixins.CfnExportPropsMixin.DestinationConfigurationsProperty(
                    s3_destination=bcmdataexports_mixins.CfnExportPropsMixin.S3DestinationProperty(
                        s3_bucket="s3Bucket",
                        s3_output_configurations=bcmdataexports_mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty(
                            compression="compression",
                            format="format",
                            output_type="outputType",
                            overwrite="overwrite"
                        ),
                        s3_prefix="s3Prefix",
                        s3_region="s3Region"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1672b3e93cffbd84df054624b288b71292d02b7c178fd204a517739f21b97336)
                check_type(argname="argument s3_destination", value=s3_destination, expected_type=type_hints["s3_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_destination is not None:
                self._values["s3_destination"] = s3_destination

        @builtins.property
        def s3_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.S3DestinationProperty"]]:
            '''An object that describes the destination of the data exports file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-destinationconfigurations.html#cfn-bcmdataexports-export-destinationconfigurations-s3destination
            '''
            result = self._values.get("s3_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.S3DestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.ExportProperty",
        jsii_struct_bases=[],
        name_mapping={
            "data_query": "dataQuery",
            "description": "description",
            "destination_configurations": "destinationConfigurations",
            "export_arn": "exportArn",
            "name": "name",
            "refresh_cadence": "refreshCadence",
        },
    )
    class ExportProperty:
        def __init__(
            self,
            *,
            data_query: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExportPropsMixin.DataQueryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            description: typing.Optional[builtins.str] = None,
            destination_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExportPropsMixin.DestinationConfigurationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            export_arn: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            refresh_cadence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExportPropsMixin.RefreshCadenceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The details that are available for an export.

            :param data_query: The data query for this specific data export.
            :param description: The description for this specific data export.
            :param destination_configurations: The destination configuration for this specific data export.
            :param export_arn: The Amazon Resource Name (ARN) for this export.
            :param name: The name of this specific data export.
            :param refresh_cadence: The cadence for AWS to update the export in your S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                export_property = bcmdataexports_mixins.CfnExportPropsMixin.ExportProperty(
                    data_query=bcmdataexports_mixins.CfnExportPropsMixin.DataQueryProperty(
                        query_statement="queryStatement",
                        table_configurations={
                            "table_configurations_key": {
                                "table_configurations_key": "tableConfigurations"
                            }
                        }
                    ),
                    description="description",
                    destination_configurations=bcmdataexports_mixins.CfnExportPropsMixin.DestinationConfigurationsProperty(
                        s3_destination=bcmdataexports_mixins.CfnExportPropsMixin.S3DestinationProperty(
                            s3_bucket="s3Bucket",
                            s3_output_configurations=bcmdataexports_mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty(
                                compression="compression",
                                format="format",
                                output_type="outputType",
                                overwrite="overwrite"
                            ),
                            s3_prefix="s3Prefix",
                            s3_region="s3Region"
                        )
                    ),
                    export_arn="exportArn",
                    name="name",
                    refresh_cadence=bcmdataexports_mixins.CfnExportPropsMixin.RefreshCadenceProperty(
                        frequency="frequency"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__32f52c7e51cb7cd0cc3720e4758a5a2cd3422699e1b19d5ba87db7203f03f65e)
                check_type(argname="argument data_query", value=data_query, expected_type=type_hints["data_query"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument destination_configurations", value=destination_configurations, expected_type=type_hints["destination_configurations"])
                check_type(argname="argument export_arn", value=export_arn, expected_type=type_hints["export_arn"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument refresh_cadence", value=refresh_cadence, expected_type=type_hints["refresh_cadence"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_query is not None:
                self._values["data_query"] = data_query
            if description is not None:
                self._values["description"] = description
            if destination_configurations is not None:
                self._values["destination_configurations"] = destination_configurations
            if export_arn is not None:
                self._values["export_arn"] = export_arn
            if name is not None:
                self._values["name"] = name
            if refresh_cadence is not None:
                self._values["refresh_cadence"] = refresh_cadence

        @builtins.property
        def data_query(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.DataQueryProperty"]]:
            '''The data query for this specific data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html#cfn-bcmdataexports-export-export-dataquery
            '''
            result = self._values.get("data_query")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.DataQueryProperty"]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''The description for this specific data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html#cfn-bcmdataexports-export-export-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.DestinationConfigurationsProperty"]]:
            '''The destination configuration for this specific data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html#cfn-bcmdataexports-export-export-destinationconfigurations
            '''
            result = self._values.get("destination_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.DestinationConfigurationsProperty"]], result)

        @builtins.property
        def export_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) for this export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html#cfn-bcmdataexports-export-export-exportarn
            '''
            result = self._values.get("export_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of this specific data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html#cfn-bcmdataexports-export-export-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def refresh_cadence(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.RefreshCadenceProperty"]]:
            '''The cadence for AWS to update the export in your S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-export.html#cfn-bcmdataexports-export-export-refreshcadence
            '''
            result = self._values.get("refresh_cadence")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.RefreshCadenceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExportProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.RefreshCadenceProperty",
        jsii_struct_bases=[],
        name_mapping={"frequency": "frequency"},
    )
    class RefreshCadenceProperty:
        def __init__(self, *, frequency: typing.Optional[builtins.str] = None) -> None:
            '''The cadence for AWS to update the data export in your S3 bucket.

            :param frequency: The frequency that data exports are updated. The export refreshes each time the source data updates, up to three times daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-refreshcadence.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                refresh_cadence_property = bcmdataexports_mixins.CfnExportPropsMixin.RefreshCadenceProperty(
                    frequency="frequency"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cd3ab41b2a1f29e704f15ef7b0c9510e455d4d1965f043ae7b697eb69fce10d)
                check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if frequency is not None:
                self._values["frequency"] = frequency

        @builtins.property
        def frequency(self) -> typing.Optional[builtins.str]:
            '''The frequency that data exports are updated.

            The export refreshes each time the source data updates, up to three times daily.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-refreshcadence.html#cfn-bcmdataexports-export-refreshcadence-frequency
            '''
            result = self._values.get("frequency")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RefreshCadenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The tag structure that contains a tag key and value.

            :param key: The key that's associated with the tag.
            :param value: The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                resource_tag_property = bcmdataexports_mixins.CfnExportPropsMixin.ResourceTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b831f4d829423cde1f34f8e4826398fa35e7d63d6ba265ff7679c3464f3046b)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-resourcetag.html#cfn-bcmdataexports-export-resourcetag-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value that's associated with the tag.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-resourcetag.html#cfn-bcmdataexports-export-resourcetag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.S3DestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "s3_bucket": "s3Bucket",
            "s3_output_configurations": "s3OutputConfigurations",
            "s3_prefix": "s3Prefix",
            "s3_region": "s3Region",
        },
    )
    class S3DestinationProperty:
        def __init__(
            self,
            *,
            s3_bucket: typing.Optional[builtins.str] = None,
            s3_output_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnExportPropsMixin.S3OutputConfigurationsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_prefix: typing.Optional[builtins.str] = None,
            s3_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the destination Amazon Simple Storage Service (Amazon S3) bucket name and object keys of a data exports file.

            :param s3_bucket: The name of the Amazon S3 bucket used as the destination of a data export file.
            :param s3_output_configurations: The output configuration for the data export.
            :param s3_prefix: The S3 path prefix you want prepended to the name of your data export.
            :param s3_region: The S3 bucket Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3destination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                s3_destination_property = bcmdataexports_mixins.CfnExportPropsMixin.S3DestinationProperty(
                    s3_bucket="s3Bucket",
                    s3_output_configurations=bcmdataexports_mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty(
                        compression="compression",
                        format="format",
                        output_type="outputType",
                        overwrite="overwrite"
                    ),
                    s3_prefix="s3Prefix",
                    s3_region="s3Region"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__758129350c5dabb6aa46d0f379c46bbad4efa23e5a262566177dd36ab3155e69)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_output_configurations", value=s3_output_configurations, expected_type=type_hints["s3_output_configurations"])
                check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
                check_type(argname="argument s3_region", value=s3_region, expected_type=type_hints["s3_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_output_configurations is not None:
                self._values["s3_output_configurations"] = s3_output_configurations
            if s3_prefix is not None:
                self._values["s3_prefix"] = s3_prefix
            if s3_region is not None:
                self._values["s3_region"] = s3_region

        @builtins.property
        def s3_bucket(self) -> typing.Optional[builtins.str]:
            '''The name of the Amazon S3 bucket used as the destination of a data export file.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3destination.html#cfn-bcmdataexports-export-s3destination-s3bucket
            '''
            result = self._values.get("s3_bucket")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_output_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.S3OutputConfigurationsProperty"]]:
            '''The output configuration for the data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3destination.html#cfn-bcmdataexports-export-s3destination-s3outputconfigurations
            '''
            result = self._values.get("s3_output_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnExportPropsMixin.S3OutputConfigurationsProperty"]], result)

        @builtins.property
        def s3_prefix(self) -> typing.Optional[builtins.str]:
            '''The S3 path prefix you want prepended to the name of your data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3destination.html#cfn-bcmdataexports-export-s3destination-s3prefix
            '''
            result = self._values.get("s3_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_region(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket Region.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3destination.html#cfn-bcmdataexports-export-s3destination-s3region
            '''
            result = self._values.get("s3_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_bcmdataexports.mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compression": "compression",
            "format": "format",
            "output_type": "outputType",
            "overwrite": "overwrite",
        },
    )
    class S3OutputConfigurationsProperty:
        def __init__(
            self,
            *,
            compression: typing.Optional[builtins.str] = None,
            format: typing.Optional[builtins.str] = None,
            output_type: typing.Optional[builtins.str] = None,
            overwrite: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The compression type, file format, and overwrite preference for the data export.

            :param compression: The compression type for the data export.
            :param format: The file format for the data export.
            :param output_type: The output type for the data export.
            :param overwrite: The rule to follow when generating a version of the data export file. You have the choice to overwrite the previous version or to be delivered in addition to the previous versions. Overwriting exports can save on Amazon S3 storage costs. Creating new export versions allows you to track the changes in cost and usage data over time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3outputconfigurations.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_bcmdataexports import mixins as bcmdataexports_mixins
                
                s3_output_configurations_property = bcmdataexports_mixins.CfnExportPropsMixin.S3OutputConfigurationsProperty(
                    compression="compression",
                    format="format",
                    output_type="outputType",
                    overwrite="overwrite"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d1096cffa3007a0b6660c40f6e6424093d7c49f29e74e25b3d18f997971249c)
                check_type(argname="argument compression", value=compression, expected_type=type_hints["compression"])
                check_type(argname="argument format", value=format, expected_type=type_hints["format"])
                check_type(argname="argument output_type", value=output_type, expected_type=type_hints["output_type"])
                check_type(argname="argument overwrite", value=overwrite, expected_type=type_hints["overwrite"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compression is not None:
                self._values["compression"] = compression
            if format is not None:
                self._values["format"] = format
            if output_type is not None:
                self._values["output_type"] = output_type
            if overwrite is not None:
                self._values["overwrite"] = overwrite

        @builtins.property
        def compression(self) -> typing.Optional[builtins.str]:
            '''The compression type for the data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3outputconfigurations.html#cfn-bcmdataexports-export-s3outputconfigurations-compression
            '''
            result = self._values.get("compression")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def format(self) -> typing.Optional[builtins.str]:
            '''The file format for the data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3outputconfigurations.html#cfn-bcmdataexports-export-s3outputconfigurations-format
            '''
            result = self._values.get("format")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def output_type(self) -> typing.Optional[builtins.str]:
            '''The output type for the data export.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3outputconfigurations.html#cfn-bcmdataexports-export-s3outputconfigurations-outputtype
            '''
            result = self._values.get("output_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def overwrite(self) -> typing.Optional[builtins.str]:
            '''The rule to follow when generating a version of the data export file.

            You have the choice to overwrite the previous version or to be delivered in addition to the previous versions. Overwriting exports can save on Amazon S3 storage costs. Creating new export versions allows you to track the changes in cost and usage data over time.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-bcmdataexports-export-s3outputconfigurations.html#cfn-bcmdataexports-export-s3outputconfigurations-overwrite
            '''
            result = self._values.get("overwrite")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3OutputConfigurationsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnExportMixinProps",
    "CfnExportPropsMixin",
]

publication.publish()

def _typecheckingstub__6fc0bb692d61c98bf82c1b5604121070ace3c9946285d03411e27f3bfff9bd53(
    *,
    export: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExportPropsMixin.ExportProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnExportPropsMixin.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09b57cdb0a9e587f3721b63daab4517e95506b7bdd0fc773251bd6c7244730fe(
    props: typing.Union[CfnExportMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20925377fd39a825425a9beb7c7e138d25b6a31b5f97d0a3e4c9558cc6876b99(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__433206851d5c09131e0c6021d137495f8c8c5acb9ff2c4162b7508f5adb55e62(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88431171cbc24cf380aa01f2b93b6c9d35e801b3dc7000297bcb2b8517ab3dd6(
    *,
    query_statement: typing.Optional[builtins.str] = None,
    table_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[typing.Mapping[builtins.str, builtins.str], _aws_cdk_ceddda9d.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1672b3e93cffbd84df054624b288b71292d02b7c178fd204a517739f21b97336(
    *,
    s3_destination: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExportPropsMixin.S3DestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f52c7e51cb7cd0cc3720e4758a5a2cd3422699e1b19d5ba87db7203f03f65e(
    *,
    data_query: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExportPropsMixin.DataQueryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    destination_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExportPropsMixin.DestinationConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    export_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    refresh_cadence: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExportPropsMixin.RefreshCadenceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd3ab41b2a1f29e704f15ef7b0c9510e455d4d1965f043ae7b697eb69fce10d(
    *,
    frequency: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b831f4d829423cde1f34f8e4826398fa35e7d63d6ba265ff7679c3464f3046b(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758129350c5dabb6aa46d0f379c46bbad4efa23e5a262566177dd36ab3155e69(
    *,
    s3_bucket: typing.Optional[builtins.str] = None,
    s3_output_configurations: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnExportPropsMixin.S3OutputConfigurationsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
    s3_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d1096cffa3007a0b6660c40f6e6424093d7c49f29e74e25b3d18f997971249c(
    *,
    compression: typing.Optional[builtins.str] = None,
    format: typing.Optional[builtins.str] = None,
    output_type: typing.Optional[builtins.str] = None,
    overwrite: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
