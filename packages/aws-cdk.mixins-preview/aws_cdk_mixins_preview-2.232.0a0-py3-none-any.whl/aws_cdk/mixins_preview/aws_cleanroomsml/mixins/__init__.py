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
    jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "role_arn": "roleArn",
        "tags": "tags",
        "training_data": "trainingData",
    },
)
class CfnTrainingDatasetMixinProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        training_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrainingDatasetPropsMixin.DatasetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnTrainingDatasetPropsMixin.

        :param description: The description of the training dataset.
        :param name: The name of the training dataset.
        :param role_arn: The ARN of the IAM role that Clean Rooms ML can assume to read the data referred to in the ``dataSource`` field of each dataset. Passing a role across accounts is not allowed. If you pass a role that isn't in your account, you get an ``AccessDeniedException`` error.
        :param tags: The optional metadata that you apply to the resource to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. The following basic restrictions apply to tags: - Maximum number of tags per resource - 50. - For each resource, each tag key must be unique, and each tag key can have only one value. - Maximum key length - 128 Unicode characters in UTF-8. - Maximum value length - 256 Unicode characters in UTF-8. - If your tagging schema is used across multiple services and resources, remember that other services may have restrictions on allowed characters. Generally allowed characters are: letters, numbers, and spaces representable in UTF-8, and the following characters: + - = . _ : /
        :param training_data: An array of information that lists the Dataset objects, which specifies the dataset type and details on its location and schema. You must provide a role that has read access to these tables.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
            
            cfn_training_dataset_mixin_props = cleanroomsml_mixins.CfnTrainingDatasetMixinProps(
                description="description",
                name="name",
                role_arn="roleArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                training_data=[cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetProperty(
                    input_config=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty(
                        data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DataSourceProperty(
                            glue_data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty(
                                catalog_id="catalogId",
                                database_name="databaseName",
                                table_name="tableName"
                            )
                        ),
                        schema=[cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.ColumnSchemaProperty(
                            column_name="columnName",
                            column_types=["columnTypes"]
                        )]
                    ),
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38f7d72d40c56417a7d56f91c0afcd86a8d80613593108164b81e61d0700db52)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument training_data", value=training_data, expected_type=type_hints["training_data"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if tags is not None:
            self._values["tags"] = tags
        if training_data is not None:
            self._values["training_data"] = training_data

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the training dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html#cfn-cleanroomsml-trainingdataset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the training dataset.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html#cfn-cleanroomsml-trainingdataset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the IAM role that Clean Rooms ML can assume to read the data referred to in the ``dataSource`` field of each dataset.

        Passing a role across accounts is not allowed. If you pass a role that isn't in your account, you get an ``AccessDeniedException`` error.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html#cfn-cleanroomsml-trainingdataset-rolearn
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]]:
        '''The optional metadata that you apply to the resource to help you categorize and organize them.

        Each tag consists of a key and an optional value, both of which you define.

        The following basic restrictions apply to tags:

        - Maximum number of tags per resource - 50.
        - For each resource, each tag key must be unique, and each tag key can have only one value.
        - Maximum key length - 128 Unicode characters in UTF-8.
        - Maximum value length - 256 Unicode characters in UTF-8.
        - If your tagging schema is used across multiple services and resources, remember that other services may have restrictions on allowed characters. Generally allowed characters are: letters, numbers, and spaces representable in UTF-8, and the following characters: + - = . _ : /

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html#cfn-cleanroomsml-trainingdataset-tags
        ::

        .

        - Tag keys and values are case sensitive.
        - Do not use ``aws:`` , ``AWS:`` , or any upper or lowercase combination of such as a prefix for keys as it is reserved. You cannot edit or delete tag keys with this prefix. Values can have this prefix. If a tag value has ``aws`` as its prefix but the key does not, then Clean Rooms ML considers it to be a user tag and will count against the limit of 50 tags. Tags with only the key prefix of ``aws`` do not count against your tags per resource limit.
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.CfnTag]], result)

    @builtins.property
    def training_data(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.DatasetProperty"]]]]:
        '''An array of information that lists the Dataset objects, which specifies the dataset type and details on its location and schema.

        You must provide a role that has read access to these tables.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html#cfn-cleanroomsml-trainingdataset-trainingdata
        '''
        result = self._values.get("training_data")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.DatasetProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTrainingDatasetMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnTrainingDatasetPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetPropsMixin",
):
    '''Defines the information necessary to create a training dataset.

    In Clean Rooms ML, the ``TrainingDataset`` is metadata that points to a Glue table, which is read only during ``AudienceModel`` creation.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cleanroomsml-trainingdataset.html
    :cloudformationResource: AWS::CleanRoomsML::TrainingDataset
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
        
        cfn_training_dataset_props_mixin = cleanroomsml_mixins.CfnTrainingDatasetPropsMixin(cleanroomsml_mixins.CfnTrainingDatasetMixinProps(
            description="description",
            name="name",
            role_arn="roleArn",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            training_data=[cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetProperty(
                input_config=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty(
                    data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DataSourceProperty(
                        glue_data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty(
                            catalog_id="catalogId",
                            database_name="databaseName",
                            table_name="tableName"
                        )
                    ),
                    schema=[cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.ColumnSchemaProperty(
                        column_name="columnName",
                        column_types=["columnTypes"]
                    )]
                ),
                type="type"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnTrainingDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::CleanRoomsML::TrainingDataset``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f8b66ceb56ac19d810a7f3706d32899a884adb81c04017f6f81ec8e10783bef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eba6d20adf6114ee228329180e563d67a8b47b6b17909f009e60e7e33cd7a701)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__382760c8e74195be57f6745511868238bff9217e76bf74790ffa9f5671423bdd)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnTrainingDatasetMixinProps:
        return typing.cast(CfnTrainingDatasetMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetPropsMixin.ColumnSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"column_name": "columnName", "column_types": "columnTypes"},
    )
    class ColumnSchemaProperty:
        def __init__(
            self,
            *,
            column_name: typing.Optional[builtins.str] = None,
            column_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Metadata for a column.

            :param column_name: The name of a column.
            :param column_types: The data type of column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-columnschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
                
                column_schema_property = cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.ColumnSchemaProperty(
                    column_name="columnName",
                    column_types=["columnTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c6bce9b353eb37c1706ba29591814550d83b138941c297d3ee009e3f9a0ac9f3)
                check_type(argname="argument column_name", value=column_name, expected_type=type_hints["column_name"])
                check_type(argname="argument column_types", value=column_types, expected_type=type_hints["column_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if column_name is not None:
                self._values["column_name"] = column_name
            if column_types is not None:
                self._values["column_types"] = column_types

        @builtins.property
        def column_name(self) -> typing.Optional[builtins.str]:
            '''The name of a column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-columnschema.html#cfn-cleanroomsml-trainingdataset-columnschema-columnname
            '''
            result = self._values.get("column_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def column_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The data type of column.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-columnschema.html#cfn-cleanroomsml-trainingdataset-columnschema-columntypes
            '''
            result = self._values.get("column_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ColumnSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetPropsMixin.DataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"glue_data_source": "glueDataSource"},
    )
    class DataSourceProperty:
        def __init__(
            self,
            *,
            glue_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrainingDatasetPropsMixin.GlueDataSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines information about the Glue data source that contains the training data.

            :param glue_data_source: A GlueDataSource object that defines the catalog ID, database name, and table name for the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-datasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
                
                data_source_property = cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DataSourceProperty(
                    glue_data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty(
                        catalog_id="catalogId",
                        database_name="databaseName",
                        table_name="tableName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a7fe1d362859bd2262b7d1c0963b1ac84f407917f3f230dd98ed811bd1a25bc)
                check_type(argname="argument glue_data_source", value=glue_data_source, expected_type=type_hints["glue_data_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if glue_data_source is not None:
                self._values["glue_data_source"] = glue_data_source

        @builtins.property
        def glue_data_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.GlueDataSourceProperty"]]:
            '''A GlueDataSource object that defines the catalog ID, database name, and table name for the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-datasource.html#cfn-cleanroomsml-trainingdataset-datasource-gluedatasource
            '''
            result = self._values.get("glue_data_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.GlueDataSourceProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"data_source": "dataSource", "schema": "schema"},
    )
    class DatasetInputConfigProperty:
        def __init__(
            self,
            *,
            data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrainingDatasetPropsMixin.DataSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrainingDatasetPropsMixin.ColumnSchemaProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Defines the Glue data source and schema mapping information.

            :param data_source: A DataSource object that specifies the Glue data source for the training data.
            :param schema: The schema information for the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-datasetinputconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
                
                dataset_input_config_property = cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty(
                    data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DataSourceProperty(
                        glue_data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty(
                            catalog_id="catalogId",
                            database_name="databaseName",
                            table_name="tableName"
                        )
                    ),
                    schema=[cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.ColumnSchemaProperty(
                        column_name="columnName",
                        column_types=["columnTypes"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a64fb834e1b190a7e07db2a4c15cd7c6904a23511d53fab86d34c3220e5d606)
                check_type(argname="argument data_source", value=data_source, expected_type=type_hints["data_source"])
                check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if data_source is not None:
                self._values["data_source"] = data_source
            if schema is not None:
                self._values["schema"] = schema

        @builtins.property
        def data_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.DataSourceProperty"]]:
            '''A DataSource object that specifies the Glue data source for the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-datasetinputconfig.html#cfn-cleanroomsml-trainingdataset-datasetinputconfig-datasource
            '''
            result = self._values.get("data_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.DataSourceProperty"]], result)

        @builtins.property
        def schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.ColumnSchemaProperty"]]]]:
            '''The schema information for the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-datasetinputconfig.html#cfn-cleanroomsml-trainingdataset-datasetinputconfig-schema
            '''
            result = self._values.get("schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.ColumnSchemaProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetInputConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetPropsMixin.DatasetProperty",
        jsii_struct_bases=[],
        name_mapping={"input_config": "inputConfig", "type": "type"},
    )
    class DatasetProperty:
        def __init__(
            self,
            *,
            input_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines where the training dataset is located, what type of data it contains, and how to access the data.

            :param input_config: A DatasetInputConfig object that defines the data source and schema mapping.
            :param type: What type of information is found in the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-dataset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
                
                dataset_property = cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetProperty(
                    input_config=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty(
                        data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.DataSourceProperty(
                            glue_data_source=cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty(
                                catalog_id="catalogId",
                                database_name="databaseName",
                                table_name="tableName"
                            )
                        ),
                        schema=[cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.ColumnSchemaProperty(
                            column_name="columnName",
                            column_types=["columnTypes"]
                        )]
                    ),
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fad63cdd2022e019da9bd98038f8c3ab758b44f72f2c4b74516d33475e4dea16)
                check_type(argname="argument input_config", value=input_config, expected_type=type_hints["input_config"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_config is not None:
                self._values["input_config"] = input_config
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def input_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty"]]:
            '''A DatasetInputConfig object that defines the data source and schema mapping.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-dataset.html#cfn-cleanroomsml-trainingdataset-dataset-inputconfig
            '''
            result = self._values.get("input_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty"]], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''What type of information is found in the dataset.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-dataset.html#cfn-cleanroomsml-trainingdataset-dataset-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DatasetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_cleanroomsml.mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "catalog_id": "catalogId",
            "database_name": "databaseName",
            "table_name": "tableName",
        },
    )
    class GlueDataSourceProperty:
        def __init__(
            self,
            *,
            catalog_id: typing.Optional[builtins.str] = None,
            database_name: typing.Optional[builtins.str] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines the Glue data source that contains the training data.

            :param catalog_id: The Glue catalog that contains the training data.
            :param database_name: The Glue database that contains the training data.
            :param table_name: The Glue table that contains the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-gluedatasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_cleanroomsml import mixins as cleanroomsml_mixins
                
                glue_data_source_property = cleanroomsml_mixins.CfnTrainingDatasetPropsMixin.GlueDataSourceProperty(
                    catalog_id="catalogId",
                    database_name="databaseName",
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d269c00f918761bead6475ef69bcd2b87e36d1f5fd9a8bf601f43bad28e4d5b0)
                check_type(argname="argument catalog_id", value=catalog_id, expected_type=type_hints["catalog_id"])
                check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if catalog_id is not None:
                self._values["catalog_id"] = catalog_id
            if database_name is not None:
                self._values["database_name"] = database_name
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def catalog_id(self) -> typing.Optional[builtins.str]:
            '''The Glue catalog that contains the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-gluedatasource.html#cfn-cleanroomsml-trainingdataset-gluedatasource-catalogid
            '''
            result = self._values.get("catalog_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def database_name(self) -> typing.Optional[builtins.str]:
            '''The Glue database that contains the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-gluedatasource.html#cfn-cleanroomsml-trainingdataset-gluedatasource-databasename
            '''
            result = self._values.get("database_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''The Glue table that contains the training data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cleanroomsml-trainingdataset-gluedatasource.html#cfn-cleanroomsml-trainingdataset-gluedatasource-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GlueDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnTrainingDatasetMixinProps",
    "CfnTrainingDatasetPropsMixin",
]

publication.publish()

def _typecheckingstub__38f7d72d40c56417a7d56f91c0afcd86a8d80613593108164b81e61d0700db52(
    *,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_ceddda9d.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    training_data: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrainingDatasetPropsMixin.DatasetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f8b66ceb56ac19d810a7f3706d32899a884adb81c04017f6f81ec8e10783bef(
    props: typing.Union[CfnTrainingDatasetMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba6d20adf6114ee228329180e563d67a8b47b6b17909f009e60e7e33cd7a701(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382760c8e74195be57f6745511868238bff9217e76bf74790ffa9f5671423bdd(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6bce9b353eb37c1706ba29591814550d83b138941c297d3ee009e3f9a0ac9f3(
    *,
    column_name: typing.Optional[builtins.str] = None,
    column_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7fe1d362859bd2262b7d1c0963b1ac84f407917f3f230dd98ed811bd1a25bc(
    *,
    glue_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrainingDatasetPropsMixin.GlueDataSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a64fb834e1b190a7e07db2a4c15cd7c6904a23511d53fab86d34c3220e5d606(
    *,
    data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrainingDatasetPropsMixin.DataSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrainingDatasetPropsMixin.ColumnSchemaProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad63cdd2022e019da9bd98038f8c3ab758b44f72f2c4b74516d33475e4dea16(
    *,
    input_config: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnTrainingDatasetPropsMixin.DatasetInputConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d269c00f918761bead6475ef69bcd2b87e36d1f5fd9a8bf601f43bad28e4d5b0(
    *,
    catalog_id: typing.Optional[builtins.str] = None,
    database_name: typing.Optional[builtins.str] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
