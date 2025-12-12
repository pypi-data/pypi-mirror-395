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
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_code": "applicationCode",
        "application_description": "applicationDescription",
        "application_name": "applicationName",
        "inputs": "inputs",
    },
)
class CfnApplicationMixinProps:
    def __init__(
        self,
        *,
        application_code: typing.Optional[builtins.str] = None,
        application_description: typing.Optional[builtins.str] = None,
        application_name: typing.Optional[builtins.str] = None,
        inputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationPropsMixin.

        :param application_code: One or more SQL statements that read input data, transform it, and generate output. For example, you can write a SQL statement that reads data from one in-application stream, generates a running average of the number of advertisement clicks by vendor, and insert resulting rows in another in-application stream using pumps. For more information about the typical pattern, see `Application Code <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-app-code.html>`_ . You can provide such series of SQL statements, where output of one statement can be used as the input for the next statement. You store intermediate results by creating in-application streams and pumps. Note that the application code must create the streams with names specified in the ``Outputs`` . For example, if your ``Outputs`` defines output streams named ``ExampleOutputStream1`` and ``ExampleOutputStream2`` , then your application code must create these streams.
        :param application_description: Summary description of the application.
        :param application_name: Name of your Amazon Kinesis Analytics application (for example, ``sample-app`` ).
        :param inputs: Use this parameter to configure the application input. You can configure your application to receive input from a single streaming source. In this configuration, you map this streaming source to an in-application stream that is created. Your application code can then query the in-application stream like a table (you can think of it as a constantly updating table). For the streaming source, you provide its Amazon Resource Name (ARN) and format of data on the stream (for example, JSON, CSV, etc.). You also must provide an IAM role that Amazon Kinesis Analytics can assume to read this stream on your behalf. To create the in-application stream, you need to specify a schema to transform your data into a schematized version used in SQL. In the schema, you provide the necessary mapping of the data elements in the streaming source to record columns in the in-app stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
            
            cfn_application_mixin_props = kinesisanalytics_mixins.CfnApplicationMixinProps(
                application_code="applicationCode",
                application_description="applicationDescription",
                application_name="applicationName",
                inputs=[kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProperty(
                    input_parallelism=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                        count=123
                    ),
                    input_processing_configuration=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                        input_lambda_processor=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                            resource_arn="resourceArn",
                            role_arn="roleArn"
                        )
                    ),
                    input_schema=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                        record_columns=[kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    kinesis_firehose_input=kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    kinesis_streams_input=kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    name_prefix="namePrefix"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9e374dbaafa595a010981b85eddeefbde43eb75dec2e04f5f152189c6f3cf59)
            check_type(argname="argument application_code", value=application_code, expected_type=type_hints["application_code"])
            check_type(argname="argument application_description", value=application_description, expected_type=type_hints["application_description"])
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument inputs", value=inputs, expected_type=type_hints["inputs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_code is not None:
            self._values["application_code"] = application_code
        if application_description is not None:
            self._values["application_description"] = application_description
        if application_name is not None:
            self._values["application_name"] = application_name
        if inputs is not None:
            self._values["inputs"] = inputs

    @builtins.property
    def application_code(self) -> typing.Optional[builtins.str]:
        '''One or more SQL statements that read input data, transform it, and generate output.

        For example, you can write a SQL statement that reads data from one in-application stream, generates a running average of the number of advertisement clicks by vendor, and insert resulting rows in another in-application stream using pumps. For more information about the typical pattern, see `Application Code <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-app-code.html>`_ .

        You can provide such series of SQL statements, where output of one statement can be used as the input for the next statement. You store intermediate results by creating in-application streams and pumps.

        Note that the application code must create the streams with names specified in the ``Outputs`` . For example, if your ``Outputs`` defines output streams named ``ExampleOutputStream1`` and ``ExampleOutputStream2`` , then your application code must create these streams.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationcode
        '''
        result = self._values.get("application_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_description(self) -> typing.Optional[builtins.str]:
        '''Summary description of the application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationdescription
        '''
        result = self._values.get("application_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''Name of your Amazon Kinesis Analytics application (for example, ``sample-app`` ).

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inputs(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProperty"]]]]:
        '''Use this parameter to configure the application input.

        You can configure your application to receive input from a single streaming source. In this configuration, you map this streaming source to an in-application stream that is created. Your application code can then query the in-application stream like a table (you can think of it as a constantly updating table).

        For the streaming source, you provide its Amazon Resource Name (ARN) and format of data on the stream (for example, JSON, CSV, etc.). You also must provide an IAM role that Amazon Kinesis Analytics can assume to read this stream on your behalf.

        To create the in-application stream, you need to specify a schema to transform your data into a schematized version used in SQL. In the schema, you provide the necessary mapping of the data elements in the streaming source to record columns in the in-app stream.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-inputs
        '''
        result = self._values.get("inputs")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProperty"]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputMixinProps",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName", "output": "output"},
)
class CfnApplicationOutputMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationOutputPropsMixin.OutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationOutputPropsMixin.

        :param application_name: Name of the application to which you want to add the output configuration.
        :param output: An array of objects, each describing one output configuration. In the output configuration, you specify the name of an in-application stream, a destination (that is, an Amazon Kinesis stream, an Amazon Kinesis Firehose delivery stream, or an AWS Lambda function), and record the formation to use when writing to the destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
            
            cfn_application_output_mixin_props = kinesisanalytics_mixins.CfnApplicationOutputMixinProps(
                application_name="applicationName",
                output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.OutputProperty(
                    destination_schema=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                        record_format_type="recordFormatType"
                    ),
                    kinesis_firehose_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    kinesis_streams_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    lambda_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    name="name"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46a64b62906ba1fd4b2fc265d0beba34d3af04c71794e1c951f51bf517440ae7)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if output is not None:
            self._values["output"] = output

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''Name of the application to which you want to add the output configuration.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.OutputProperty"]]:
        '''An array of objects, each describing one output configuration.

        In the output configuration, you specify the name of an in-application stream, a destination (that is, an Amazon Kinesis stream, an Amazon Kinesis Firehose delivery stream, or an AWS Lambda function), and record the formation to use when writing to the destination.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-output
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.OutputProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationOutputMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationOutputPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputPropsMixin",
):
    '''Adds an external destination to your Amazon Kinesis Analytics application.

    If you want Amazon Kinesis Analytics to deliver data from an in-application stream within your application to an external destination (such as an Amazon Kinesis stream, an Amazon Kinesis Firehose delivery stream, or an Amazon Lambda function), you add the relevant configuration to your application using this operation. You can configure one or more outputs for your application. Each output configuration maps an in-application stream and an external destination.

    You can use one of the output configurations to deliver data from your in-application error stream to an external destination so that you can analyze the errors. For more information, see `Understanding Application Output (Destination) <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-output.html>`_ .

    Any configuration update, including adding a streaming source using this operation, results in a new version of the application. You can use the ``DescribeApplication`` operation to find the current application version.

    For the limits on the number of application inputs and outputs you can configure, see `Limits <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/limits.html>`_ .

    This operation requires permissions to perform the ``kinesisanalytics:AddApplicationOutput`` action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html
    :cloudformationResource: AWS::KinesisAnalytics::ApplicationOutput
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
        
        cfn_application_output_props_mixin = kinesisanalytics_mixins.CfnApplicationOutputPropsMixin(kinesisanalytics_mixins.CfnApplicationOutputMixinProps(
            application_name="applicationName",
            output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.OutputProperty(
                destination_schema=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                    record_format_type="recordFormatType"
                ),
                kinesis_firehose_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                ),
                kinesis_streams_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                ),
                lambda_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                ),
                name="name"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisAnalytics::ApplicationOutput``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__791d674273cc92bb0cfdf9de4a85f5df512d5e873be32ae915df044c57097fb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__650ed974d7cdb433e9c2cd69088ee183e00c65da5f24eea6071b828d44afca07)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbd73f4fdec3b043f4671d0e2b90a91c8e17d1bbf7850a9c50db47f032b518e4)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationOutputMixinProps:
        return typing.cast(CfnApplicationOutputMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={"record_format_type": "recordFormatType"},
    )
    class DestinationSchemaProperty:
        def __init__(
            self,
            *,
            record_format_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the data format when records are written to the destination.

            For more information, see `Configuring Application Output <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-output.html>`_ .

            :param record_format_type: Specifies the format of the records on the output stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-destinationschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                destination_schema_property = kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                    record_format_type="recordFormatType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6043650cd5148ab6fa1730c402eba65fa61a2896a53e27199e03660f4560fa4d)
                check_type(argname="argument record_format_type", value=record_format_type, expected_type=type_hints["record_format_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_format_type is not None:
                self._values["record_format_type"] = record_format_type

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''Specifies the format of the records on the output stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-destinationschema.html#cfn-kinesisanalytics-applicationoutput-destinationschema-recordformattype
            '''
            result = self._values.get("record_format_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisFirehoseOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When configuring application output, identifies an Amazon Kinesis Firehose delivery stream as the destination.

            You provide the stream Amazon Resource Name (ARN) and an IAM role that enables Amazon Kinesis Analytics to write to the stream on your behalf.

            :param resource_arn: ARN of the destination Amazon Kinesis Firehose delivery stream to write to.
            :param role_arn: ARN of the IAM role that Amazon Kinesis Analytics can assume to write to the destination stream on your behalf. You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                kinesis_firehose_output_property = kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac44a156ed5323bc9ce41bd322c8c7ba2899a4adb56248dc73bdf036fc5ae775)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the destination Amazon Kinesis Firehose delivery stream to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisfirehoseoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that Amazon Kinesis Analytics can assume to write to the destination stream on your behalf.

            You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisfirehoseoutput-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisStreamsOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When configuring application output, identifies an Amazon Kinesis stream as the destination.

            You provide the stream Amazon Resource Name (ARN) and also an IAM role ARN that Amazon Kinesis Analytics can use to write to the stream on your behalf.

            :param resource_arn: ARN of the destination Amazon Kinesis stream to write to.
            :param role_arn: ARN of the IAM role that Amazon Kinesis Analytics can assume to write to the destination stream on your behalf. You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                kinesis_streams_output_property = kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e292dd4f596c35110afb674517d5e0480d17cc44cc33fead1c9d28ec542a7ef)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the destination Amazon Kinesis stream to write to.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisstreamsoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that Amazon Kinesis Analytics can assume to write to the destination stream on your behalf.

            You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisstreamsoutput-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamsOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class LambdaOutputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When configuring application output, identifies an AWS Lambda function as the destination.

            You provide the function Amazon Resource Name (ARN) and also an IAM role ARN that Amazon Kinesis Analytics can use to write to the function on your behalf.

            :param resource_arn: Amazon Resource Name (ARN) of the destination Lambda function to write to. .. epigraph:: To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: AWS Lambda <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_
            :param role_arn: ARN of the IAM role that Amazon Kinesis Analytics can assume to write to the destination function on your behalf. You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                lambda_output_property = kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9b488b68d3c3d4ce2ed7e369555027a14a0d3d9a526b5870e4f03cfcf3486738)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) of the destination Lambda function to write to.

            .. epigraph::

               To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: AWS Lambda <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html#cfn-kinesisanalytics-applicationoutput-lambdaoutput-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that Amazon Kinesis Analytics can assume to write to the destination function on your behalf.

            You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html#cfn-kinesisanalytics-applicationoutput-lambdaoutput-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaOutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationOutputPropsMixin.OutputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_schema": "destinationSchema",
            "kinesis_firehose_output": "kinesisFirehoseOutput",
            "kinesis_streams_output": "kinesisStreamsOutput",
            "lambda_output": "lambdaOutput",
            "name": "name",
        },
    )
    class OutputProperty:
        def __init__(
            self,
            *,
            destination_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationOutputPropsMixin.DestinationSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_firehose_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_streams_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationOutputPropsMixin.LambdaOutputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes application output configuration in which you identify an in-application stream and a destination where you want the in-application stream data to be written.

            The destination can be an Amazon Kinesis stream or an Amazon Kinesis Firehose delivery stream.

            For limits on how many destinations an application can write and other limitations, see `Limits <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/limits.html>`_ .

            :param destination_schema: Describes the data format when records are written to the destination. For more information, see `Configuring Application Output <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-output.html>`_ .
            :param kinesis_firehose_output: Identifies an Amazon Kinesis Firehose delivery stream as the destination.
            :param kinesis_streams_output: Identifies an Amazon Kinesis stream as the destination.
            :param lambda_output: Identifies an AWS Lambda function as the destination.
            :param name: Name of the in-application stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                output_property = kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.OutputProperty(
                    destination_schema=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.DestinationSchemaProperty(
                        record_format_type="recordFormatType"
                    ),
                    kinesis_firehose_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    kinesis_streams_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    lambda_output=kinesisanalytics_mixins.CfnApplicationOutputPropsMixin.LambdaOutputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd1176897bd226d4486b606f03f322fc50b194d166176ee08357ed0afeae73b4)
                check_type(argname="argument destination_schema", value=destination_schema, expected_type=type_hints["destination_schema"])
                check_type(argname="argument kinesis_firehose_output", value=kinesis_firehose_output, expected_type=type_hints["kinesis_firehose_output"])
                check_type(argname="argument kinesis_streams_output", value=kinesis_streams_output, expected_type=type_hints["kinesis_streams_output"])
                check_type(argname="argument lambda_output", value=lambda_output, expected_type=type_hints["lambda_output"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_schema is not None:
                self._values["destination_schema"] = destination_schema
            if kinesis_firehose_output is not None:
                self._values["kinesis_firehose_output"] = kinesis_firehose_output
            if kinesis_streams_output is not None:
                self._values["kinesis_streams_output"] = kinesis_streams_output
            if lambda_output is not None:
                self._values["lambda_output"] = lambda_output
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def destination_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.DestinationSchemaProperty"]]:
            '''Describes the data format when records are written to the destination.

            For more information, see `Configuring Application Output <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-output.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-destinationschema
            '''
            result = self._values.get("destination_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.DestinationSchemaProperty"]], result)

        @builtins.property
        def kinesis_firehose_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty"]]:
            '''Identifies an Amazon Kinesis Firehose delivery stream as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-kinesisfirehoseoutput
            '''
            result = self._values.get("kinesis_firehose_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty"]], result)

        @builtins.property
        def kinesis_streams_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty"]]:
            '''Identifies an Amazon Kinesis stream as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-kinesisstreamsoutput
            '''
            result = self._values.get("kinesis_streams_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty"]], result)

        @builtins.property
        def lambda_output(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.LambdaOutputProperty"]]:
            '''Identifies an AWS Lambda function as the destination.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-lambdaoutput
            '''
            result = self._values.get("lambda_output")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationOutputPropsMixin.LambdaOutputProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the in-application stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationPropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin",
):
    '''The ``AWS::KinesisAnalytics::Application`` resource creates an Amazon Kinesis Data Analytics application.

    For more information, see the `Amazon Kinesis Data Analytics Developer Guide <https://docs.aws.amazon.com//kinesisanalytics/latest/dev/what-is.html>`_ .

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html
    :cloudformationResource: AWS::KinesisAnalytics::Application
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
        
        cfn_application_props_mixin = kinesisanalytics_mixins.CfnApplicationPropsMixin(kinesisanalytics_mixins.CfnApplicationMixinProps(
            application_code="applicationCode",
            application_description="applicationDescription",
            application_name="applicationName",
            inputs=[kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProperty(
                input_parallelism=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                    count=123
                ),
                input_processing_configuration=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                    input_lambda_processor=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    )
                ),
                input_schema=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                    record_columns=[kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                ),
                kinesis_firehose_input=kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                ),
                kinesis_streams_input=kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                ),
                name_prefix="namePrefix"
            )]
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisAnalytics::Application``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e00d77e955b632f590993d43948a8e0c36e36375ae1452a92e3733735d9d7448)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a473dc4925e700581844f14769bd2d52d654e96e22b08a176a1a02c43fad0ca2)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856f2e62ca58600330b330e58569c04c6351069e8703fc2505e2aeea74e7685b)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationMixinProps:
        return typing.cast(CfnApplicationMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_column_delimiter": "recordColumnDelimiter",
            "record_row_delimiter": "recordRowDelimiter",
        },
    )
    class CSVMappingParametersProperty:
        def __init__(
            self,
            *,
            record_column_delimiter: typing.Optional[builtins.str] = None,
            record_row_delimiter: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides additional mapping information when the record format uses delimiters, such as CSV.

            For example, the following sample records use CSV format, where the records use the *'\\n'* as the row delimiter and a comma (",") as the column delimiter:

            ``"name1", "address1"``

            ``"name2", "address2"``

            :param record_column_delimiter: Column delimiter. For example, in a CSV format, a comma (",") is the typical column delimiter.
            :param record_row_delimiter: Row delimiter. For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                c_sVMapping_parameters_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                    record_column_delimiter="recordColumnDelimiter",
                    record_row_delimiter="recordRowDelimiter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e0c075242d3331278c5e3516cf0a1fe331ad587c3fb25fc2367b043269541e1c)
                check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
                check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_column_delimiter is not None:
                self._values["record_column_delimiter"] = record_column_delimiter
            if record_row_delimiter is not None:
                self._values["record_row_delimiter"] = record_row_delimiter

        @builtins.property
        def record_column_delimiter(self) -> typing.Optional[builtins.str]:
            '''Column delimiter.

            For example, in a CSV format, a comma (",") is the typical column delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html#cfn-kinesisanalytics-application-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_row_delimiter(self) -> typing.Optional[builtins.str]:
            '''Row delimiter.

            For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html#cfn-kinesisanalytics-application-csvmappingparameters-recordrowdelimiter
            '''
            result = self._values.get("record_row_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CSVMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class InputLambdaProcessorProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that contains the Amazon Resource Name (ARN) of the `AWS Lambda <https://docs.aws.amazon.com/lambda/>`_ function that is used to preprocess records in the stream, and the ARN of the IAM role that is used to access the AWS Lambda function.

            :param resource_arn: The ARN of the `AWS Lambda <https://docs.aws.amazon.com/lambda/>`_ function that operates on records in the stream. .. epigraph:: To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: AWS Lambda <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_
            :param role_arn: The ARN of the IAM role that is used to access the AWS Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                input_lambda_processor_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1f9d312a5332223f2c4335f9f5847e4e7d45debcd2babc7208b1d528a1787173)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the `AWS Lambda <https://docs.aws.amazon.com/lambda/>`_ function that operates on records in the stream.

            .. epigraph::

               To specify an earlier version of the Lambda function than the latest, include the Lambda function version in the Lambda function ARN. For more information about Lambda ARNs, see `Example ARNs: AWS Lambda <https://docs.aws.amazon.com//general/latest/gr/aws-arns-and-namespaces.html#arn-syntax-lambda>`_

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html#cfn-kinesisanalytics-application-inputlambdaprocessor-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the IAM role that is used to access the AWS Lambda function.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html#cfn-kinesisanalytics-application-inputlambdaprocessor-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputLambdaProcessorProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.InputParallelismProperty",
        jsii_struct_bases=[],
        name_mapping={"count": "count"},
    )
    class InputParallelismProperty:
        def __init__(self, *, count: typing.Optional[jsii.Number] = None) -> None:
            '''Describes the number of in-application streams to create for a given streaming source.

            For information about parallelism, see `Configuring Application Input <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-input.html>`_ .

            :param count: Number of in-application streams to create. For more information, see `Limits <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/limits.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputparallelism.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                input_parallelism_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                    count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__068ed952550a6debd6a78804d5567c5cef53ff599f13f4fd0001865ccbd05f96)
                check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if count is not None:
                self._values["count"] = count

        @builtins.property
        def count(self) -> typing.Optional[jsii.Number]:
            '''Number of in-application streams to create.

            For more information, see `Limits <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/limits.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputparallelism.html#cfn-kinesisanalytics-application-inputparallelism-count
            '''
            result = self._values.get("count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputParallelismProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"input_lambda_processor": "inputLambdaProcessor"},
    )
    class InputProcessingConfigurationProperty:
        def __init__(
            self,
            *,
            input_lambda_processor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputLambdaProcessorProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides a description of a processor that is used to preprocess the records in the stream before being processed by your application code.

            Currently, the only input processor available is `AWS Lambda <https://docs.aws.amazon.com/lambda/>`_ .

            :param input_lambda_processor: The `InputLambdaProcessor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html>`_ that is used to preprocess the records in the stream before being processed by your application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                input_processing_configuration_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                    input_lambda_processor=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ec67519137152bd4fd7d6ba238e116b40f461ead619074bc9aba7258f79ab556)
                check_type(argname="argument input_lambda_processor", value=input_lambda_processor, expected_type=type_hints["input_lambda_processor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_lambda_processor is not None:
                self._values["input_lambda_processor"] = input_lambda_processor

        @builtins.property
        def input_lambda_processor(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputLambdaProcessorProperty"]]:
            '''The `InputLambdaProcessor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html>`_ that is used to preprocess the records in the stream before being processed by your application code.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html#cfn-kinesisanalytics-application-inputprocessingconfiguration-inputlambdaprocessor
            '''
            result = self._values.get("input_lambda_processor")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputLambdaProcessorProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProcessingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.InputProperty",
        jsii_struct_bases=[],
        name_mapping={
            "input_parallelism": "inputParallelism",
            "input_processing_configuration": "inputProcessingConfiguration",
            "input_schema": "inputSchema",
            "kinesis_firehose_input": "kinesisFirehoseInput",
            "kinesis_streams_input": "kinesisStreamsInput",
            "name_prefix": "namePrefix",
        },
    )
    class InputProperty:
        def __init__(
            self,
            *,
            input_parallelism: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputParallelismProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputProcessingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            input_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.InputSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_firehose_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.KinesisFirehoseInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            kinesis_streams_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.KinesisStreamsInputProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name_prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When you configure the application input, you specify the streaming source, the in-application stream name that is created, and the mapping between the two.

            For more information, see `Configuring Application Input <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-input.html>`_ .

            :param input_parallelism: Describes the number of in-application streams to create. Data from your source is routed to these in-application input streams. See `Configuring Application Input <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-input.html>`_ .
            :param input_processing_configuration: The `InputProcessingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html>`_ for the input. An input processor transforms records as they are received from the stream, before the application's SQL code executes. Currently, the only input processing configuration available is `InputLambdaProcessor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html>`_ .
            :param input_schema: Describes the format of the data in the streaming source, and how each data element maps to corresponding columns in the in-application stream that is being created. Also used to describe the format of the reference data source.
            :param kinesis_firehose_input: If the streaming source is an Amazon Kinesis Firehose delivery stream, identifies the delivery stream's ARN and an IAM role that enables Amazon Kinesis Analytics to access the stream on your behalf. Note: Either ``KinesisStreamsInput`` or ``KinesisFirehoseInput`` is required.
            :param kinesis_streams_input: If the streaming source is an Amazon Kinesis stream, identifies the stream's Amazon Resource Name (ARN) and an IAM role that enables Amazon Kinesis Analytics to access the stream on your behalf. Note: Either ``KinesisStreamsInput`` or ``KinesisFirehoseInput`` is required.
            :param name_prefix: Name prefix to use when creating an in-application stream. Suppose that you specify a prefix "MyInApplicationStream." Amazon Kinesis Analytics then creates one or more (as per the ``InputParallelism`` count you specified) in-application streams with names "MyInApplicationStream_001," "MyInApplicationStream_002," and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                input_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProperty(
                    input_parallelism=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputParallelismProperty(
                        count=123
                    ),
                    input_processing_configuration=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputProcessingConfigurationProperty(
                        input_lambda_processor=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputLambdaProcessorProperty(
                            resource_arn="resourceArn",
                            role_arn="roleArn"
                        )
                    ),
                    input_schema=kinesisanalytics_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                        record_columns=[kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    kinesis_firehose_input=kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    kinesis_streams_input=kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                        resource_arn="resourceArn",
                        role_arn="roleArn"
                    ),
                    name_prefix="namePrefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b4708ba839862df699ed0dacd797c8ff4dcc46afe810304219b499fc715d3197)
                check_type(argname="argument input_parallelism", value=input_parallelism, expected_type=type_hints["input_parallelism"])
                check_type(argname="argument input_processing_configuration", value=input_processing_configuration, expected_type=type_hints["input_processing_configuration"])
                check_type(argname="argument input_schema", value=input_schema, expected_type=type_hints["input_schema"])
                check_type(argname="argument kinesis_firehose_input", value=kinesis_firehose_input, expected_type=type_hints["kinesis_firehose_input"])
                check_type(argname="argument kinesis_streams_input", value=kinesis_streams_input, expected_type=type_hints["kinesis_streams_input"])
                check_type(argname="argument name_prefix", value=name_prefix, expected_type=type_hints["name_prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if input_parallelism is not None:
                self._values["input_parallelism"] = input_parallelism
            if input_processing_configuration is not None:
                self._values["input_processing_configuration"] = input_processing_configuration
            if input_schema is not None:
                self._values["input_schema"] = input_schema
            if kinesis_firehose_input is not None:
                self._values["kinesis_firehose_input"] = kinesis_firehose_input
            if kinesis_streams_input is not None:
                self._values["kinesis_streams_input"] = kinesis_streams_input
            if name_prefix is not None:
                self._values["name_prefix"] = name_prefix

        @builtins.property
        def input_parallelism(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputParallelismProperty"]]:
            '''Describes the number of in-application streams to create.

            Data from your source is routed to these in-application input streams.

            See `Configuring Application Input <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-input.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputparallelism
            '''
            result = self._values.get("input_parallelism")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputParallelismProperty"]], result)

        @builtins.property
        def input_processing_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProcessingConfigurationProperty"]]:
            '''The `InputProcessingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html>`_ for the input. An input processor transforms records as they are received from the stream, before the application's SQL code executes. Currently, the only input processing configuration available is `InputLambdaProcessor <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html>`_ .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputprocessingconfiguration
            '''
            result = self._values.get("input_processing_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputProcessingConfigurationProperty"]], result)

        @builtins.property
        def input_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputSchemaProperty"]]:
            '''Describes the format of the data in the streaming source, and how each data element maps to corresponding columns in the in-application stream that is being created.

            Also used to describe the format of the reference data source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputschema
            '''
            result = self._values.get("input_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.InputSchemaProperty"]], result)

        @builtins.property
        def kinesis_firehose_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisFirehoseInputProperty"]]:
            '''If the streaming source is an Amazon Kinesis Firehose delivery stream, identifies the delivery stream's ARN and an IAM role that enables Amazon Kinesis Analytics to access the stream on your behalf.

            Note: Either ``KinesisStreamsInput`` or ``KinesisFirehoseInput`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-kinesisfirehoseinput
            '''
            result = self._values.get("kinesis_firehose_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisFirehoseInputProperty"]], result)

        @builtins.property
        def kinesis_streams_input(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisStreamsInputProperty"]]:
            '''If the streaming source is an Amazon Kinesis stream, identifies the stream's Amazon Resource Name (ARN) and an IAM role that enables Amazon Kinesis Analytics to access the stream on your behalf.

            Note: Either ``KinesisStreamsInput`` or ``KinesisFirehoseInput`` is required.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-kinesisstreamsinput
            '''
            result = self._values.get("kinesis_streams_input")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.KinesisStreamsInputProperty"]], result)

        @builtins.property
        def name_prefix(self) -> typing.Optional[builtins.str]:
            '''Name prefix to use when creating an in-application stream.

            Suppose that you specify a prefix "MyInApplicationStream." Amazon Kinesis Analytics then creates one or more (as per the ``InputParallelism`` count you specified) in-application streams with names "MyInApplicationStream_001," "MyInApplicationStream_002," and so on.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-nameprefix
            '''
            result = self._values.get("name_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.InputSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_columns": "recordColumns",
            "record_encoding": "recordEncoding",
            "record_format": "recordFormat",
        },
    )
    class InputSchemaProperty:
        def __init__(
            self,
            *,
            record_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.RecordColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            record_encoding: typing.Optional[builtins.str] = None,
            record_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.RecordFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the format of the data in the streaming source, and how each data element maps to corresponding columns in the in-application stream that is being created.

            Also used to describe the format of the reference data source.

            :param record_columns: A list of ``RecordColumn`` objects.
            :param record_encoding: Specifies the encoding of the records in the streaming source. For example, UTF-8.
            :param record_format: Specifies the format of the records on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                input_schema_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.InputSchemaProperty(
                    record_columns=[kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__871e9159edda5f5e305a3dd8015420da61ceefc2842604c233bca566e0f4e7af)
                check_type(argname="argument record_columns", value=record_columns, expected_type=type_hints["record_columns"])
                check_type(argname="argument record_encoding", value=record_encoding, expected_type=type_hints["record_encoding"])
                check_type(argname="argument record_format", value=record_format, expected_type=type_hints["record_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_columns is not None:
                self._values["record_columns"] = record_columns
            if record_encoding is not None:
                self._values["record_encoding"] = record_encoding
            if record_format is not None:
                self._values["record_format"] = record_format

        @builtins.property
        def record_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RecordColumnProperty"]]]]:
            '''A list of ``RecordColumn`` objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RecordColumnProperty"]]]], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''Specifies the encoding of the records in the streaming source.

            For example, UTF-8.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RecordFormatProperty"]]:
            '''Specifies the format of the records on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordformat
            '''
            result = self._values.get("record_format")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.RecordFormatProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InputSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(
            self,
            *,
            record_row_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides additional mapping information when JSON is the record format on the streaming source.

            :param record_row_path: Path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-jsonmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                j_sONMapping_parameters_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                    record_row_path="recordRowPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__740af017489e153d60d4b44615ceedd865e0727639246e8890cd064309e0f9ac)
                check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_row_path is not None:
                self._values["record_row_path"] = record_row_path

        @builtins.property
        def record_row_path(self) -> typing.Optional[builtins.str]:
            '''Path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-jsonmappingparameters.html#cfn-kinesisanalytics-application-jsonmappingparameters-recordrowpath
            '''
            result = self._values.get("record_row_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JSONMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisFirehoseInputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies an Amazon Kinesis Firehose delivery stream as the streaming source.

            You provide the delivery stream's Amazon Resource Name (ARN) and an IAM role ARN that enables Amazon Kinesis Analytics to access the stream on your behalf.

            :param resource_arn: ARN of the input delivery stream.
            :param role_arn: ARN of the IAM role that Amazon Kinesis Analytics can assume to access the stream on your behalf. You need to make sure that the role has the necessary permissions to access the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                kinesis_firehose_input_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisFirehoseInputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f76235a0e345bea7377767d3f80ce71dcbf02365c4a5bbb0aad99f0cff4af1b)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the input delivery stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html#cfn-kinesisanalytics-application-kinesisfirehoseinput-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that Amazon Kinesis Analytics can assume to access the stream on your behalf.

            You need to make sure that the role has the necessary permissions to access the stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html#cfn-kinesisanalytics-application-kinesisfirehoseinput-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty",
        jsii_struct_bases=[],
        name_mapping={"resource_arn": "resourceArn", "role_arn": "roleArn"},
    )
    class KinesisStreamsInputProperty:
        def __init__(
            self,
            *,
            resource_arn: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies an Amazon Kinesis stream as the streaming source.

            You provide the stream's Amazon Resource Name (ARN) and an IAM role ARN that enables Amazon Kinesis Analytics to access the stream on your behalf.

            :param resource_arn: ARN of the input Amazon Kinesis stream to read.
            :param role_arn: ARN of the IAM role that Amazon Kinesis Analytics can assume to access the stream on your behalf. You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                kinesis_streams_input_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.KinesisStreamsInputProperty(
                    resource_arn="resourceArn",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__17cfbc3f1e6b6396c9576a97864fe33ef467eeac87c99bfea0521521c8061c4f)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if resource_arn is not None:
                self._values["resource_arn"] = resource_arn
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def resource_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the input Amazon Kinesis stream to read.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html#cfn-kinesisanalytics-application-kinesisstreamsinput-resourcearn
            '''
            result = self._values.get("resource_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that Amazon Kinesis Analytics can assume to access the stream on your behalf.

            You need to grant the necessary permissions to this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html#cfn-kinesisanalytics-application-kinesisstreamsinput-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisStreamsInputProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.MappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_mapping_parameters": "csvMappingParameters",
            "json_mapping_parameters": "jsonMappingParameters",
        },
    )
    class MappingParametersProperty:
        def __init__(
            self,
            *,
            csv_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.CSVMappingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            json_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.JSONMappingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''When configuring application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :param csv_mapping_parameters: Provides additional mapping information when the record format uses delimiters (for example, CSV).
            :param json_mapping_parameters: Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                mapping_parameters_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                    csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                        record_column_delimiter="recordColumnDelimiter",
                        record_row_delimiter="recordRowDelimiter"
                    ),
                    json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                        record_row_path="recordRowPath"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad6e3446c3b474565b8793a1a41bf4545aaab2567e4880211f2bdb83803e5162)
                check_type(argname="argument csv_mapping_parameters", value=csv_mapping_parameters, expected_type=type_hints["csv_mapping_parameters"])
                check_type(argname="argument json_mapping_parameters", value=json_mapping_parameters, expected_type=type_hints["json_mapping_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv_mapping_parameters is not None:
                self._values["csv_mapping_parameters"] = csv_mapping_parameters
            if json_mapping_parameters is not None:
                self._values["json_mapping_parameters"] = json_mapping_parameters

        @builtins.property
        def csv_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CSVMappingParametersProperty"]]:
            '''Provides additional mapping information when the record format uses delimiters (for example, CSV).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html#cfn-kinesisanalytics-application-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.CSVMappingParametersProperty"]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.JSONMappingParametersProperty"]]:
            '''Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html#cfn-kinesisanalytics-application-mappingparameters-jsonmappingparameters
            '''
            result = self._values.get("json_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.JSONMappingParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.RecordColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"mapping": "mapping", "name": "name", "sql_type": "sqlType"},
    )
    class RecordColumnProperty:
        def __init__(
            self,
            *,
            mapping: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            sql_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the mapping of each data element in the streaming source to the corresponding column in the in-application stream.

            Also used to describe the format of the reference data source.

            :param mapping: Reference to the data element in the streaming input or the reference data source. This element is required if the `RecordFormatType <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/API_RecordFormat.html#analytics-Type-RecordFormat-RecordFormatTypel>`_ is ``JSON`` .
            :param name: Name of the column created in the in-application input stream or reference table.
            :param sql_type: Type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                record_column_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordColumnProperty(
                    mapping="mapping",
                    name="name",
                    sql_type="sqlType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__70e71c23fcd1cb63863f60bd24d399cce992c1b38ff7d72830ccd60192ba4085)
                check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sql_type", value=sql_type, expected_type=type_hints["sql_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mapping is not None:
                self._values["mapping"] = mapping
            if name is not None:
                self._values["name"] = name
            if sql_type is not None:
                self._values["sql_type"] = sql_type

        @builtins.property
        def mapping(self) -> typing.Optional[builtins.str]:
            '''Reference to the data element in the streaming input or the reference data source.

            This element is required if the `RecordFormatType <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/API_RecordFormat.html#analytics-Type-RecordFormat-RecordFormatTypel>`_ is ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql_type(self) -> typing.Optional[builtins.str]:
            '''Type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-sqltype
            '''
            result = self._values.get("sql_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationPropsMixin.RecordFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mapping_parameters": "mappingParameters",
            "record_format_type": "recordFormatType",
        },
    )
    class RecordFormatProperty:
        def __init__(
            self,
            *,
            mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationPropsMixin.MappingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            record_format_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the record format and relevant mapping information that should be applied to schematize the records on the stream.

            :param mapping_parameters: When configuring application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.
            :param record_format_type: The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                record_format_property = kinesisanalytics_mixins.CfnApplicationPropsMixin.RecordFormatProperty(
                    mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.MappingParametersProperty(
                        csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.CSVMappingParametersProperty(
                            record_column_delimiter="recordColumnDelimiter",
                            record_row_delimiter="recordRowDelimiter"
                        ),
                        json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationPropsMixin.JSONMappingParametersProperty(
                            record_row_path="recordRowPath"
                        )
                    ),
                    record_format_type="recordFormatType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7caa8fb5914b1d412d3bef4f100a261c674450e4083f8ac462bd9c9a669373e3)
                check_type(argname="argument mapping_parameters", value=mapping_parameters, expected_type=type_hints["mapping_parameters"])
                check_type(argname="argument record_format_type", value=record_format_type, expected_type=type_hints["record_format_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mapping_parameters is not None:
                self._values["mapping_parameters"] = mapping_parameters
            if record_format_type is not None:
                self._values["record_format_type"] = record_format_type

        @builtins.property
        def mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MappingParametersProperty"]]:
            '''When configuring application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html#cfn-kinesisanalytics-application-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationPropsMixin.MappingParametersProperty"]], result)

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html#cfn-kinesisanalytics-application-recordformat-recordformattype
            '''
            result = self._values.get("record_format_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourceMixinProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "reference_data_source": "referenceDataSource",
    },
)
class CfnApplicationReferenceDataSourceMixinProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        reference_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for CfnApplicationReferenceDataSourcePropsMixin.

        :param application_name: Name of an existing application.
        :param reference_data_source: The reference data source can be an object in your Amazon S3 bucket. Amazon Kinesis Analytics reads the object and copies the data into the in-application table that is created. You provide an S3 bucket, object key name, and the resulting in-application table that is created. You must also provide an IAM role with the necessary permissions that Amazon Kinesis Analytics can assume to read the object from your S3 bucket on your behalf.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
            
            cfn_application_reference_data_source_mixin_props = kinesisanalytics_mixins.CfnApplicationReferenceDataSourceMixinProps(
                application_name="applicationName",
                reference_data_source=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty(
                    reference_schema=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                        record_columns=[kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    s3_reference_data_source=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey",
                        reference_role_arn="referenceRoleArn"
                    ),
                    table_name="tableName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca45399e18779e0381c6755599105bb10bce05f364231394e65f2a5079517183)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument reference_data_source", value=reference_data_source, expected_type=type_hints["reference_data_source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if reference_data_source is not None:
            self._values["reference_data_source"] = reference_data_source

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''Name of an existing application.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reference_data_source(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty"]]:
        '''The reference data source can be an object in your Amazon S3 bucket.

        Amazon Kinesis Analytics reads the object and copies the data into the in-application table that is created. You provide an S3 bucket, object key name, and the resulting in-application table that is created. You must also provide an IAM role with the necessary permissions that Amazon Kinesis Analytics can assume to read the object from your S3 bucket on your behalf.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource
        '''
        result = self._values.get("reference_data_source")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationReferenceDataSourceMixinProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IMixin_11e4b965)
class CfnApplicationReferenceDataSourcePropsMixin(
    _Mixin_a69446c0,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin",
):
    '''Adds a reference data source to an existing application.

    Amazon Kinesis Analytics reads reference data (that is, an Amazon S3 object) and creates an in-application table within your application. In the request, you provide the source (S3 bucket name and object key name), name of the in-application table to create, and the necessary mapping information that describes how data in Amazon S3 object maps to columns in the resulting in-application table.

    For conceptual information, see `Configuring Application Input <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/how-it-works-input.html>`_ . For the limits on data sources you can add to your application, see `Limits <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/limits.html>`_ .

    This operation requires permissions to perform the ``kinesisanalytics:AddApplicationOutput`` action.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html
    :cloudformationResource: AWS::KinesisAnalytics::ApplicationReferenceDataSource
    :mixin: true
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk.mixins_preview import mixins
        from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
        
        cfn_application_reference_data_source_props_mixin = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin(kinesisanalytics_mixins.CfnApplicationReferenceDataSourceMixinProps(
            application_name="applicationName",
            reference_data_source=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty(
                reference_schema=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                    record_columns=[kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                ),
                s3_reference_data_source=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey",
                    reference_role_arn="referenceRoleArn"
                ),
                table_name="tableName"
            )
        ),
            strategy=mixins.PropertyMergeStrategy.OVERRIDE
        )
    '''

    def __init__(
        self,
        props: typing.Union[CfnApplicationReferenceDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
        *,
        strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
    ) -> None:
        '''Create a mixin to apply properties to ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

        :param props: L1 properties to apply.
        :param strategy: (experimental) Strategy for merging nested properties. Default: - PropertyMergeStrategy.MERGE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4867f5658613d279967c2c46d0125f3389d997e180236caea123bd65291ac81)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c925fecd1de42eda31545facd7fe0b2301604d54b909c423a26d8e6ec68d7c0c)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "applyTo", [construct]))

    @jsii.member(jsii_name="supports")
    def supports(self, construct: _constructs_77d1e7e8.IConstruct) -> builtins.bool:
        '''Check if this mixin supports the given construct.

        :param construct: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__317ad12db1edf7a7611c9ca54f7ef77fcbabd1cb72610cce249875ca4225d648)
            check_type(argname="argument construct", value=construct, expected_type=type_hints["construct"])
        return typing.cast(builtins.bool, jsii.invoke(self, "supports", [construct]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_PROPERTY_KEYS")
    def CFN_PROPERTY_KEYS(cls) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.sget(cls, "CFN_PROPERTY_KEYS"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> CfnApplicationReferenceDataSourceMixinProps:
        return typing.cast(CfnApplicationReferenceDataSourceMixinProps, jsii.get(self, "props"))

    @builtins.property
    @jsii.member(jsii_name="strategy")
    def _strategy(self) -> _PropertyMergeStrategy_49c157e8:
        return typing.cast(_PropertyMergeStrategy_49c157e8, jsii.get(self, "strategy"))

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_column_delimiter": "recordColumnDelimiter",
            "record_row_delimiter": "recordRowDelimiter",
        },
    )
    class CSVMappingParametersProperty:
        def __init__(
            self,
            *,
            record_column_delimiter: typing.Optional[builtins.str] = None,
            record_row_delimiter: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides additional mapping information when the record format uses delimiters, such as CSV.

            For example, the following sample records use CSV format, where the records use the *'\\n'* as the row delimiter and a comma (",") as the column delimiter:

            ``"name1", "address1"``

            ``"name2", "address2"``

            :param record_column_delimiter: Column delimiter. For example, in a CSV format, a comma (",") is the typical column delimiter.
            :param record_row_delimiter: Row delimiter. For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                c_sVMapping_parameters_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                    record_column_delimiter="recordColumnDelimiter",
                    record_row_delimiter="recordRowDelimiter"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__55bb264921879183f6e5829393c9d032eef45c8b9f258a8c05977c8299c5a265)
                check_type(argname="argument record_column_delimiter", value=record_column_delimiter, expected_type=type_hints["record_column_delimiter"])
                check_type(argname="argument record_row_delimiter", value=record_row_delimiter, expected_type=type_hints["record_row_delimiter"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_column_delimiter is not None:
                self._values["record_column_delimiter"] = record_column_delimiter
            if record_row_delimiter is not None:
                self._values["record_row_delimiter"] = record_row_delimiter

        @builtins.property
        def record_column_delimiter(self) -> typing.Optional[builtins.str]:
            '''Column delimiter.

            For example, in a CSV format, a comma (",") is the typical column delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-csvmappingparameters-recordcolumndelimiter
            '''
            result = self._values.get("record_column_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_row_delimiter(self) -> typing.Optional[builtins.str]:
            '''Row delimiter.

            For example, in a CSV format, *'\\n'* is the typical row delimiter.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-csvmappingparameters-recordrowdelimiter
            '''
            result = self._values.get("record_row_delimiter")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CSVMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={"record_row_path": "recordRowPath"},
    )
    class JSONMappingParametersProperty:
        def __init__(
            self,
            *,
            record_row_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides additional mapping information when JSON is the record format on the streaming source.

            :param record_row_path: Path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                j_sONMapping_parameters_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                    record_row_path="recordRowPath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fab9d3526a0301184def93ce4d4805e8086c38924e3c5e895ab52db560ccacc3)
                check_type(argname="argument record_row_path", value=record_row_path, expected_type=type_hints["record_row_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_row_path is not None:
                self._values["record_row_path"] = record_row_path

        @builtins.property
        def record_row_path(self) -> typing.Optional[builtins.str]:
            '''Path to the top-level parent that contains the records.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters-recordrowpath
            '''
            result = self._values.get("record_row_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "JSONMappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "csv_mapping_parameters": "csvMappingParameters",
            "json_mapping_parameters": "jsonMappingParameters",
        },
    )
    class MappingParametersProperty:
        def __init__(
            self,
            *,
            csv_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            json_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''When configuring application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :param csv_mapping_parameters: Provides additional mapping information when the record format uses delimiters (for example, CSV).
            :param json_mapping_parameters: Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                mapping_parameters_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                    csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                        record_column_delimiter="recordColumnDelimiter",
                        record_row_delimiter="recordRowDelimiter"
                    ),
                    json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                        record_row_path="recordRowPath"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2237e1e77061e3cb553dc9396eafb50855a9fe2cbb7466b0bf725aa129ef0985)
                check_type(argname="argument csv_mapping_parameters", value=csv_mapping_parameters, expected_type=type_hints["csv_mapping_parameters"])
                check_type(argname="argument json_mapping_parameters", value=json_mapping_parameters, expected_type=type_hints["json_mapping_parameters"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if csv_mapping_parameters is not None:
                self._values["csv_mapping_parameters"] = csv_mapping_parameters
            if json_mapping_parameters is not None:
                self._values["json_mapping_parameters"] = json_mapping_parameters

        @builtins.property
        def csv_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty"]]:
            '''Provides additional mapping information when the record format uses delimiters (for example, CSV).

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-mappingparameters-csvmappingparameters
            '''
            result = self._values.get("csv_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty"]], result)

        @builtins.property
        def json_mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty"]]:
            '''Provides additional mapping information when JSON is the record format on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-mappingparameters-jsonmappingparameters
            '''
            result = self._values.get("json_mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MappingParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty",
        jsii_struct_bases=[],
        name_mapping={"mapping": "mapping", "name": "name", "sql_type": "sqlType"},
    )
    class RecordColumnProperty:
        def __init__(
            self,
            *,
            mapping: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            sql_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the mapping of each data element in the streaming source to the corresponding column in the in-application stream.

            Also used to describe the format of the reference data source.

            :param mapping: Reference to the data element in the streaming input or the reference data source. This element is required if the `RecordFormatType <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/API_RecordFormat.html#analytics-Type-RecordFormat-RecordFormatTypel>`_ is ``JSON`` .
            :param name: Name of the column created in the in-application input stream or reference table.
            :param sql_type: Type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                record_column_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                    mapping="mapping",
                    name="name",
                    sql_type="sqlType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7814b74ad5b7ed94e0937ebd7193b9702c6218b15011a4f57bcd483a53a07103)
                check_type(argname="argument mapping", value=mapping, expected_type=type_hints["mapping"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sql_type", value=sql_type, expected_type=type_hints["sql_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mapping is not None:
                self._values["mapping"] = mapping
            if name is not None:
                self._values["name"] = name
            if sql_type is not None:
                self._values["sql_type"] = sql_type

        @builtins.property
        def mapping(self) -> typing.Optional[builtins.str]:
            '''Reference to the data element in the streaming input or the reference data source.

            This element is required if the `RecordFormatType <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/API_RecordFormat.html#analytics-Type-RecordFormat-RecordFormatTypel>`_ is ``JSON`` .

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-mapping
            '''
            result = self._values.get("mapping")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''Name of the column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sql_type(self) -> typing.Optional[builtins.str]:
            '''Type of column created in the in-application input stream or reference table.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-sqltype
            '''
            result = self._values.get("sql_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordColumnProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mapping_parameters": "mappingParameters",
            "record_format_type": "recordFormatType",
        },
    )
    class RecordFormatProperty:
        def __init__(
            self,
            *,
            mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            record_format_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the record format and relevant mapping information that should be applied to schematize the records on the stream.

            :param mapping_parameters: When configuring application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.
            :param record_format_type: The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                record_format_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                    mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                        csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                            record_column_delimiter="recordColumnDelimiter",
                            record_row_delimiter="recordRowDelimiter"
                        ),
                        json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                            record_row_path="recordRowPath"
                        )
                    ),
                    record_format_type="recordFormatType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac688aad569e7ea53a44233a4675b2199584a737d36cd8bc4dd4b3eabb3e7c4a)
                check_type(argname="argument mapping_parameters", value=mapping_parameters, expected_type=type_hints["mapping_parameters"])
                check_type(argname="argument record_format_type", value=record_format_type, expected_type=type_hints["record_format_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mapping_parameters is not None:
                self._values["mapping_parameters"] = mapping_parameters
            if record_format_type is not None:
                self._values["record_format_type"] = record_format_type

        @builtins.property
        def mapping_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty"]]:
            '''When configuring application input at the time of creating or updating an application, provides additional mapping information specific to the record format (such as JSON, CSV, or record fields delimited by some delimiter) on the streaming source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html#cfn-kinesisanalytics-applicationreferencedatasource-recordformat-mappingparameters
            '''
            result = self._values.get("mapping_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty"]], result)

        @builtins.property
        def record_format_type(self) -> typing.Optional[builtins.str]:
            '''The type of record format.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html#cfn-kinesisanalytics-applicationreferencedatasource-recordformat-recordformattype
            '''
            result = self._values.get("record_format_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RecordFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "reference_schema": "referenceSchema",
            "s3_reference_data_source": "s3ReferenceDataSource",
            "table_name": "tableName",
        },
    )
    class ReferenceDataSourceProperty:
        def __init__(
            self,
            *,
            reference_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_reference_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            table_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the reference data source by providing the source information (S3 bucket name and object key name), the resulting in-application table name that is created, and the necessary schema to map the data elements in the Amazon S3 object to the in-application table.

            :param reference_schema: Describes the format of the data in the streaming source, and how each data element maps to corresponding columns created in the in-application stream.
            :param s3_reference_data_source: Identifies the S3 bucket and object that contains the reference data. Also identifies the IAM role Amazon Kinesis Analytics can assume to read this object on your behalf. An Amazon Kinesis Analytics application loads reference data only once. If the data changes, you call the ``UpdateApplication`` operation to trigger reloading of data into your application.
            :param table_name: Name of the in-application table to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                reference_data_source_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty(
                    reference_schema=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                        record_columns=[kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                            mapping="mapping",
                            name="name",
                            sql_type="sqlType"
                        )],
                        record_encoding="recordEncoding",
                        record_format=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                            mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                                csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                    record_column_delimiter="recordColumnDelimiter",
                                    record_row_delimiter="recordRowDelimiter"
                                ),
                                json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                    record_row_path="recordRowPath"
                                )
                            ),
                            record_format_type="recordFormatType"
                        )
                    ),
                    s3_reference_data_source=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                        bucket_arn="bucketArn",
                        file_key="fileKey",
                        reference_role_arn="referenceRoleArn"
                    ),
                    table_name="tableName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e464884e130badca811a757cab9333fb64b73284ba2893a458a50a4e6197e3a2)
                check_type(argname="argument reference_schema", value=reference_schema, expected_type=type_hints["reference_schema"])
                check_type(argname="argument s3_reference_data_source", value=s3_reference_data_source, expected_type=type_hints["s3_reference_data_source"])
                check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference_schema is not None:
                self._values["reference_schema"] = reference_schema
            if s3_reference_data_source is not None:
                self._values["s3_reference_data_source"] = s3_reference_data_source
            if table_name is not None:
                self._values["table_name"] = table_name

        @builtins.property
        def reference_schema(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty"]]:
            '''Describes the format of the data in the streaming source, and how each data element maps to corresponding columns created in the in-application stream.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-referenceschema
            '''
            result = self._values.get("reference_schema")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty"]], result)

        @builtins.property
        def s3_reference_data_source(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty"]]:
            '''Identifies the S3 bucket and object that contains the reference data.

            Also identifies the IAM role Amazon Kinesis Analytics can assume to read this object on your behalf. An Amazon Kinesis Analytics application loads reference data only once. If the data changes, you call the ``UpdateApplication`` operation to trigger reloading of data into your application.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-s3referencedatasource
            '''
            result = self._values.get("s3_reference_data_source")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty"]], result)

        @builtins.property
        def table_name(self) -> typing.Optional[builtins.str]:
            '''Name of the in-application table to create.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-tablename
            '''
            result = self._values.get("table_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "record_columns": "recordColumns",
            "record_encoding": "recordEncoding",
            "record_format": "recordFormat",
        },
    )
    class ReferenceSchemaProperty:
        def __init__(
            self,
            *,
            record_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            record_encoding: typing.Optional[builtins.str] = None,
            record_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union["CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The ReferenceSchema property type specifies the format of the data in the reference source for a SQL-based Amazon Kinesis Data Analytics application.

            :param record_columns: A list of RecordColumn objects.
            :param record_encoding: Specifies the encoding of the records in the reference source. For example, UTF-8.
            :param record_format: Specifies the format of the records on the reference source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                reference_schema_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty(
                    record_columns=[kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty(
                        mapping="mapping",
                        name="name",
                        sql_type="sqlType"
                    )],
                    record_encoding="recordEncoding",
                    record_format=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty(
                        mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty(
                            csv_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty(
                                record_column_delimiter="recordColumnDelimiter",
                                record_row_delimiter="recordRowDelimiter"
                            ),
                            json_mapping_parameters=kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty(
                                record_row_path="recordRowPath"
                            )
                        ),
                        record_format_type="recordFormatType"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a4ec1c2d4a96b244b20ab8270c0b357589b01529b46422c7daf3aa5c81cb416)
                check_type(argname="argument record_columns", value=record_columns, expected_type=type_hints["record_columns"])
                check_type(argname="argument record_encoding", value=record_encoding, expected_type=type_hints["record_encoding"])
                check_type(argname="argument record_format", value=record_format, expected_type=type_hints["record_format"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if record_columns is not None:
                self._values["record_columns"] = record_columns
            if record_encoding is not None:
                self._values["record_encoding"] = record_encoding
            if record_format is not None:
                self._values["record_format"] = record_format

        @builtins.property
        def record_columns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty"]]]]:
            '''A list of RecordColumn objects.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordcolumns
            '''
            result = self._values.get("record_columns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty"]]]], result)

        @builtins.property
        def record_encoding(self) -> typing.Optional[builtins.str]:
            '''Specifies the encoding of the records in the reference source.

            For example, UTF-8.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordencoding
            '''
            result = self._values.get("record_encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def record_format(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty"]]:
            '''Specifies the format of the records on the reference source.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordformat
            '''
            result = self._values.get("record_format")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, "CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceSchemaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/mixins-preview.aws_kinesisanalytics.mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "file_key": "fileKey",
            "reference_role_arn": "referenceRoleArn",
        },
    )
    class S3ReferenceDataSourceProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            file_key: typing.Optional[builtins.str] = None,
            reference_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Identifies the S3 bucket and object that contains the reference data.

            Also identifies the IAM role Amazon Kinesis Analytics can assume to read this object on your behalf.

            An Amazon Kinesis Analytics application loads reference data only once. If the data changes, you call the `UpdateApplication <https://docs.aws.amazon.com/kinesisanalytics/latest/dev/API_UpdateApplication.html>`_ operation to trigger reloading of data into your application.

            :param bucket_arn: Amazon Resource Name (ARN) of the S3 bucket.
            :param file_key: Object key name containing reference data.
            :param reference_role_arn: ARN of the IAM role that the service can assume to read data on your behalf. This role must have permission for the ``s3:GetObject`` action on the object and trust policy that allows Amazon Kinesis Analytics service principal to assume this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk.mixins_preview.aws_kinesisanalytics import mixins as kinesisanalytics_mixins
                
                s3_reference_data_source_property = kinesisanalytics_mixins.CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty(
                    bucket_arn="bucketArn",
                    file_key="fileKey",
                    reference_role_arn="referenceRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1264babfb36bf3396826b98254c6a92f56d33b5a0f4fd491941daa34e5f85afd)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument file_key", value=file_key, expected_type=type_hints["file_key"])
                check_type(argname="argument reference_role_arn", value=reference_role_arn, expected_type=type_hints["reference_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if file_key is not None:
                self._values["file_key"] = file_key
            if reference_role_arn is not None:
                self._values["reference_role_arn"] = reference_role_arn

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) of the S3 bucket.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_key(self) -> typing.Optional[builtins.str]:
            '''Object key name containing reference data.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-filekey
            '''
            result = self._values.get("file_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reference_role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of the IAM role that the service can assume to read data on your behalf.

            This role must have permission for the ``s3:GetObject`` action on the object and trust policy that allows Amazon Kinesis Analytics service principal to assume this role.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-referencerolearn
            '''
            result = self._values.get("reference_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ReferenceDataSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


__all__ = [
    "CfnApplicationMixinProps",
    "CfnApplicationOutputMixinProps",
    "CfnApplicationOutputPropsMixin",
    "CfnApplicationPropsMixin",
    "CfnApplicationReferenceDataSourceMixinProps",
    "CfnApplicationReferenceDataSourcePropsMixin",
]

publication.publish()

def _typecheckingstub__e9e374dbaafa595a010981b85eddeefbde43eb75dec2e04f5f152189c6f3cf59(
    *,
    application_code: typing.Optional[builtins.str] = None,
    application_description: typing.Optional[builtins.str] = None,
    application_name: typing.Optional[builtins.str] = None,
    inputs: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46a64b62906ba1fd4b2fc265d0beba34d3af04c71794e1c951f51bf517440ae7(
    *,
    application_name: typing.Optional[builtins.str] = None,
    output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.OutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791d674273cc92bb0cfdf9de4a85f5df512d5e873be32ae915df044c57097fb2(
    props: typing.Union[CfnApplicationOutputMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650ed974d7cdb433e9c2cd69088ee183e00c65da5f24eea6071b828d44afca07(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd73f4fdec3b043f4671d0e2b90a91c8e17d1bbf7850a9c50db47f032b518e4(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6043650cd5148ab6fa1730c402eba65fa61a2896a53e27199e03660f4560fa4d(
    *,
    record_format_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac44a156ed5323bc9ce41bd322c8c7ba2899a4adb56248dc73bdf036fc5ae775(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e292dd4f596c35110afb674517d5e0480d17cc44cc33fead1c9d28ec542a7ef(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b488b68d3c3d4ce2ed7e369555027a14a0d3d9a526b5870e4f03cfcf3486738(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd1176897bd226d4486b606f03f322fc50b194d166176ee08357ed0afeae73b4(
    *,
    destination_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.DestinationSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_firehose_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.KinesisFirehoseOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_streams_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.KinesisStreamsOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_output: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationOutputPropsMixin.LambdaOutputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e00d77e955b632f590993d43948a8e0c36e36375ae1452a92e3733735d9d7448(
    props: typing.Union[CfnApplicationMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a473dc4925e700581844f14769bd2d52d654e96e22b08a176a1a02c43fad0ca2(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856f2e62ca58600330b330e58569c04c6351069e8703fc2505e2aeea74e7685b(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c075242d3331278c5e3516cf0a1fe331ad587c3fb25fc2367b043269541e1c(
    *,
    record_column_delimiter: typing.Optional[builtins.str] = None,
    record_row_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f9d312a5332223f2c4335f9f5847e4e7d45debcd2babc7208b1d528a1787173(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068ed952550a6debd6a78804d5567c5cef53ff599f13f4fd0001865ccbd05f96(
    *,
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec67519137152bd4fd7d6ba238e116b40f461ead619074bc9aba7258f79ab556(
    *,
    input_lambda_processor: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputLambdaProcessorProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4708ba839862df699ed0dacd797c8ff4dcc46afe810304219b499fc715d3197(
    *,
    input_parallelism: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputParallelismProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_processing_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputProcessingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    input_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.InputSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_firehose_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.KinesisFirehoseInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kinesis_streams_input: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.KinesisStreamsInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__871e9159edda5f5e305a3dd8015420da61ceefc2842604c233bca566e0f4e7af(
    *,
    record_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.RecordColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    record_encoding: typing.Optional[builtins.str] = None,
    record_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.RecordFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740af017489e153d60d4b44615ceedd865e0727639246e8890cd064309e0f9ac(
    *,
    record_row_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f76235a0e345bea7377767d3f80ce71dcbf02365c4a5bbb0aad99f0cff4af1b(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17cfbc3f1e6b6396c9576a97864fe33ef467eeac87c99bfea0521521c8061c4f(
    *,
    resource_arn: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6e3446c3b474565b8793a1a41bf4545aaab2567e4880211f2bdb83803e5162(
    *,
    csv_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.CSVMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.JSONMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e71c23fcd1cb63863f60bd24d399cce992c1b38ff7d72830ccd60192ba4085(
    *,
    mapping: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sql_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7caa8fb5914b1d412d3bef4f100a261c674450e4083f8ac462bd9c9a669373e3(
    *,
    mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationPropsMixin.MappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    record_format_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca45399e18779e0381c6755599105bb10bce05f364231394e65f2a5079517183(
    *,
    application_name: typing.Optional[builtins.str] = None,
    reference_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.ReferenceDataSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4867f5658613d279967c2c46d0125f3389d997e180236caea123bd65291ac81(
    props: typing.Union[CfnApplicationReferenceDataSourceMixinProps, typing.Dict[builtins.str, typing.Any]],
    *,
    strategy: typing.Optional[_PropertyMergeStrategy_49c157e8] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c925fecd1de42eda31545facd7fe0b2301604d54b909c423a26d8e6ec68d7c0c(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317ad12db1edf7a7611c9ca54f7ef77fcbabd1cb72610cce249875ca4225d648(
    construct: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55bb264921879183f6e5829393c9d032eef45c8b9f258a8c05977c8299c5a265(
    *,
    record_column_delimiter: typing.Optional[builtins.str] = None,
    record_row_delimiter: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab9d3526a0301184def93ce4d4805e8086c38924e3c5e895ab52db560ccacc3(
    *,
    record_row_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2237e1e77061e3cb553dc9396eafb50855a9fe2cbb7466b0bf725aa129ef0985(
    *,
    csv_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.CSVMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    json_mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.JSONMappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7814b74ad5b7ed94e0937ebd7193b9702c6218b15011a4f57bcd483a53a07103(
    *,
    mapping: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    sql_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac688aad569e7ea53a44233a4675b2199584a737d36cd8bc4dd4b3eabb3e7c4a(
    *,
    mapping_parameters: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.MappingParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    record_format_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e464884e130badca811a757cab9333fb64b73284ba2893a458a50a4e6197e3a2(
    *,
    reference_schema: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.ReferenceSchemaProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_reference_data_source: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.S3ReferenceDataSourceProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a4ec1c2d4a96b244b20ab8270c0b357589b01529b46422c7daf3aa5c81cb416(
    *,
    record_columns: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.RecordColumnProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    record_encoding: typing.Optional[builtins.str] = None,
    record_format: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[CfnApplicationReferenceDataSourcePropsMixin.RecordFormatProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1264babfb36bf3396826b98254c6a92f56d33b5a0f4fd491941daa34e5f85afd(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    file_key: typing.Optional[builtins.str] = None,
    reference_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
